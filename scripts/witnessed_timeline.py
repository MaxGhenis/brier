#!/usr/bin/env python3
"""Extract externally witnessed chronology from the verified record chain."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from canonical_json import canonical_bytes, canonical_sha256
from verify_custody import CustodyError, verify_run
from verify_record_chain import (
    ChainError,
    ChainVerification,
    logical_path,
    physical_path,
    verify_chain,
)

ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST_SCHEMAS = {
    "thesis_analyst_run_manifest_v1",
    "thesis_derived_ensemble_manifest_v1",
    "brier_reasoning_judge_run_manifest_v1",
}


class TimelineError(ValueError):
    pass


@dataclass(frozen=True)
class ProofCandidate:
    earliest_witnessed_at: str
    witness_digest: str
    tsa_gen_time: str
    coverage: str

    def as_json(self) -> dict[str, str]:
        return {
            "earliestWitnessedAt": self.earliest_witnessed_at,
            "witnessDigest": self.witness_digest,
            "tsaGenTime": self.tsa_gen_time,
            "coverage": self.coverage,
        }


def _safe_logical(value: str) -> PurePosixPath:
    if not value or "\\" in value:
        raise TimelineError(f"invalid logical path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.parts[0] != "records":
        raise TimelineError(f"unsafe logical path: {value!r}")
    if path.as_posix() != value:
        raise TimelineError(f"non-normalized logical path: {value!r}")
    return path


def _winner(
    verification: ChainVerification,
    snapshot_index: int,
    *,
    force_transitive: bool,
    records: Path,
) -> ProofCandidate | None:
    candidates: list[ProofCandidate] = []
    for witness_index in range(snapshot_index, len(verification.ordered)):
        digest = verification.ordered[witness_index]
        evidence = verification.witnesses[digest]
        if evidence.status != "available" or not evidence.gen_time:
            continue
        coverage = (
            "transitive"
            if force_transitive or witness_index != snapshot_index
            else "direct"
        )
        candidates.append(
            ProofCandidate(
                earliest_witnessed_at=evidence.gen_time,
                witness_digest=logical_path(records, digest),
                tsa_gen_time=evidence.gen_time,
                coverage=coverage,
            )
        )
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda item: (
            datetime.fromisoformat(item.tsa_gen_time.replace("Z", "+00:00")),
            0 if item.coverage == "direct" else 1,
            item.witness_digest,
        ),
    )


def _put(
    output: dict[str, dict[str, Any]], key: str, candidate: ProofCandidate | None
) -> None:
    if candidate is None:
        return
    current = output.get(key)
    proposed = candidate.as_json()
    if current is None:
        output[key] = proposed
        return
    current_key = (
        datetime.fromisoformat(current["tsaGenTime"].replace("Z", "+00:00")),
        0 if current["coverage"] == "direct" else 1,
        current["witnessDigest"],
    )
    proposed_key = (
        datetime.fromisoformat(proposed["tsaGenTime"].replace("Z", "+00:00")),
        0 if proposed["coverage"] == "direct" else 1,
        proposed["witnessDigest"],
    )
    if proposed_key < current_key:
        output[key] = proposed


def _validate_registration(
    records: Path,
    logical: str,
    *,
    raw_sha256: str | None = None,
    size: int | None = None,
    canonical_hash: str | None = None,
) -> None:
    _safe_logical(logical)
    path = physical_path(records, logical)
    if not path.is_file() or path.is_symlink():
        raise TimelineError(f"committed registration snapshot is absent: {logical}")
    raw = path.read_bytes()
    if raw_sha256 is not None and hashlib.sha256(raw).hexdigest() != raw_sha256:
        raise TimelineError(f"registration raw SHA-256 mismatch: {logical}")
    if size is not None and len(raw) != size:
        raise TimelineError(f"registration size mismatch: {logical}")
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise TimelineError(f"invalid registration JSON {logical}: {exc}") from exc
    if canonical_hash is not None and canonical_sha256(payload) != canonical_hash:
        raise TimelineError(f"registration canonical SHA-256 mismatch: {logical}")


def _registration_from_manifest(
    records: Path,
    run_dir: Path,
    proof: ProofCandidate | None,
    registrations: dict[str, dict[str, str]],
) -> None:
    manifest = json.loads((run_dir / "manifest.json").read_bytes())
    context = manifest.get("targetContext")
    if not isinstance(context, dict):
        return
    logical = context.get("targetRegistrationPath")
    content_hash = context.get("targetContentHash")
    if logical is None and content_hash is None:
        return
    if not isinstance(logical, str) or not isinstance(content_hash, str):
        raise TimelineError(f"incomplete target registration reference in {run_dir}")
    _validate_registration(records, logical, canonical_hash=content_hash)
    _put(registrations, logical, proof)


def _commit_root(
    records: Path,
    commitment: dict[str, Any],
    root_proof: ProofCandidate | None,
    contents_proof: ProofCandidate | None,
    runs: dict[str, dict[str, str]],
    roots: dict[str, dict[str, Any]],
    registrations: dict[str, dict[str, str]],
) -> None:
    run_logical = str(commitment.get("runDirectory", ""))
    root_logical = str(commitment.get("custodyRootPath", ""))
    manifest_logical = str(commitment.get("manifestPath", ""))
    _safe_logical(run_logical)
    _safe_logical(root_logical)
    _safe_logical(manifest_logical)
    run_dir = physical_path(records, run_logical)
    root_path = physical_path(records, root_logical)
    manifest_path = physical_path(records, manifest_logical)
    if root_path.parent != run_dir or manifest_path.parent != run_dir:
        raise TimelineError(f"custody commitment paths disagree for {run_logical}")
    if hashlib.sha256(root_path.read_bytes()).hexdigest() != commitment.get(
        "custodyRootFileSha256"
    ) or root_path.stat().st_size != commitment.get("custodyRootSize"):
        raise TimelineError(f"committed custody root file mismatch: {root_logical}")
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != commitment.get(
        "manifestSha256"
    ) or manifest_path.stat().st_size != commitment.get("manifestSize"):
        raise TimelineError(f"committed custody manifest mismatch: {manifest_logical}")
    try:
        verified = verify_run(run_dir)
    except CustodyError as exc:
        raise TimelineError(
            f"covered custody root does not verify: {run_logical}: {exc}"
        ) from exc
    root_hash = str(commitment.get("custodyRootSha256", ""))
    if verified.custody_root_sha256 != root_hash:
        raise TimelineError(f"custody root identity mismatch: {run_logical}")
    if verified.custody_inventory_version != commitment.get("custodyInventoryVersion"):
        raise TimelineError(f"custody inventory version mismatch: {run_logical}")
    # The digest names the custody-root object itself. The run directory and
    # registration are fixed only through the root's artifact/manifest links.
    _put(roots, root_hash, root_proof)
    if root_hash in roots:
        roots[root_hash].update(
            {
                "custodyInventoryVersion": verified.custody_inventory_version,
                "inventoryStatus": verified.inventory_status,
                "headlineEligible": verified.headline_eligible,
            }
        )
    _put(runs, run_logical, contents_proof)
    _registration_from_manifest(records, run_dir, contents_proof, registrations)


def _walk_objects(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_objects(child)


def _archive_json(records: Path, record: dict[str, Any]) -> Any:
    logical = str(record.get("archivePath", ""))
    _safe_logical(logical)
    path = physical_path(records, logical)
    if not path.is_file() or path.is_symlink():
        raise TimelineError(f"covered recorder archive is absent: {logical}")
    compressed = path.read_bytes()
    if hashlib.sha256(compressed).hexdigest() != record.get("archiveSha256") or len(
        compressed
    ) != record.get("archiveBytes"):
        raise TimelineError(f"covered recorder archive mismatch: {logical}")
    try:
        raw = gzip.decompress(compressed)
    except (OSError, EOFError) as exc:
        raise TimelineError(f"invalid recorder gzip {logical}: {exc}") from exc
    if hashlib.sha256(raw).hexdigest() != record.get("sha256") or len(
        raw
    ) != record.get("bytes"):
        raise TimelineError(f"covered recorder raw body mismatch: {logical}")
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise TimelineError(f"invalid recorder JSON body {logical}: {exc}") from exc


def _root_commitments_from_log(
    records: Path, digest: dict[str, Any]
) -> list[dict[str, Any]]:
    surfaces = digest.get("surfaces")
    if not isinstance(surfaces, dict) or not isinstance(surfaces.get("log"), dict):
        return []
    log_manifest = _archive_json(records, surfaces["log"])
    documents = [log_manifest]
    log_chunks = digest.get("logChunks") or {}
    if not isinstance(log_chunks, dict):
        raise TimelineError("recorder logChunks is not an object")
    if log_manifest.get("schemaVersion") == "thesis_log_v3":
        collections = log_manifest.get("collections")
        if not isinstance(collections, dict):
            raise TimelineError("recorder v3 log manifest lacks collections")
        expected: dict[str, tuple[str, int, dict[str, Any]]] = {}
        for collection, collection_manifest in collections.items():
            references = (
                collection_manifest.get("chunks")
                if isinstance(collection_manifest, dict)
                else None
            )
            if not isinstance(references, list):
                raise TimelineError(
                    f"recorder v3 log collection {collection} lacks chunks"
                )
            for expected_index, reference in enumerate(references):
                if (
                    not isinstance(reference, dict)
                    or reference.get("index") != expected_index
                ):
                    raise TimelineError(
                        f"recorder v3 {collection} chunk indexes are invalid"
                    )
                expected[f"{collection}:{expected_index}"] = (
                    str(collection),
                    expected_index,
                    reference,
                )
        if set(log_chunks) != set(expected):
            raise TimelineError(
                "recorder v3 log chunk inventory differs from its manifest"
            )
        for key, (collection, index, reference) in expected.items():
            record = log_chunks[key]
            if not isinstance(record, dict):
                raise TimelineError(f"recorder v3 log chunk {key} is not an object")
            if record.get("manifestSha256") != reference.get("sha256"):
                raise TimelineError(
                    f"recorder v3 log chunk {key} manifest link mismatch"
                )
            chunk = _archive_json(records, record)
            expected_fields = {
                "schemaVersion": "thesis_log_chunk_v1",
                "logSchemaVersion": "thesis_log_v3",
                "collection": collection,
                "chunkIndex": index,
                "count": reference.get("count"),
            }
            if any(chunk.get(name) != value for name, value in expected_fields.items()):
                raise TimelineError(f"recorder v3 log chunk {key} metadata mismatch")
            if len(chunk.get("rows", [])) != reference.get("count"):
                raise TimelineError(f"recorder v3 log chunk {key} row count mismatch")
            if canonical_sha256(chunk) != reference.get("sha256"):
                raise TimelineError(
                    f"recorder v3 log chunk {key} canonical hash mismatch"
                )
            documents.append(chunk)
    elif log_chunks:
        raise TimelineError("non-v3 recorder log unexpectedly has chunks")
    commitments: list[dict[str, Any]] = []
    for document in documents:
        for value in _walk_objects(document):
            root_hash = value.get("custodyRootSha256")
            if not isinstance(root_hash, str):
                continue
            activity = value.get("activityLog")
            if not isinstance(activity, list):
                continue
            manifest_refs = [
                ref
                for ref in activity
                if isinstance(ref, dict) and ref.get("artifactType") == "manifest"
            ]
            if len(manifest_refs) != 1:
                continue
            manifest_logical = str(manifest_refs[0].get("path", ""))
            _safe_logical(manifest_logical)
            manifest_path = physical_path(records, manifest_logical)
            run_dir = manifest_path.parent
            root_path = run_dir / "custody_root.json"
            if not root_path.is_file():
                raise TimelineError(
                    f"log commits a custody root with no local root: {manifest_logical}"
                )
            commitments.append(
                {
                    "runDirectory": run_dir.relative_to(records.parent).as_posix(),
                    "custodyRootPath": root_path.relative_to(records.parent).as_posix(),
                    "custodyRootSha256": root_hash,
                    "custodyRootFileSha256": hashlib.sha256(
                        root_path.read_bytes()
                    ).hexdigest(),
                    "custodyRootSize": root_path.stat().st_size,
                    "custodyInventoryVersion": (
                        json.loads(root_path.read_bytes()).get(
                            "custodyInventoryVersion"
                        )
                        or 1
                    ),
                    "manifestPath": manifest_logical,
                    "manifestSha256": hashlib.sha256(
                        manifest_path.read_bytes()
                    ).hexdigest(),
                    "manifestSize": manifest_path.stat().st_size,
                }
            )
    unique: dict[tuple[str, str], dict[str, Any]] = {}
    for commitment in commitments:
        unique[(commitment["runDirectory"], commitment["custodyRootSha256"])] = (
            commitment
        )
    return list(unique.values())


def extract_timeline(records: Path) -> dict[str, Any]:
    records = records.resolve()
    try:
        verification = verify_chain(records)
    except ChainError as exc:
        raise TimelineError(f"record chain does not verify: {exc}") from exc
    runs: dict[str, dict[str, str]] = {}
    roots: dict[str, dict[str, Any]] = {}
    registrations: dict[str, dict[str, str]] = {}
    genesis = json.loads((records / "CHAIN_GENESIS.json").read_bytes())
    for index, snapshot_path in enumerate(verification.ordered):
        digest = json.loads(snapshot_path.read_bytes())
        direct_proof = _winner(
            verification,
            index,
            force_transitive=False,
            records=records,
        )
        container_proof = _winner(
            verification,
            index,
            force_transitive=True,
            records=records,
        )
        commitments = digest.get("artifactCommitments") or {}
        if not isinstance(commitments, dict):
            raise TimelineError(
                f"artifactCommitments is not an object in {snapshot_path}"
            )
        custody = commitments.get("custodyRoots") or []
        registrations_committed = commitments.get("registrationSnapshots") or []
        if not isinstance(custody, list) or not isinstance(
            registrations_committed, list
        ):
            raise TimelineError(f"invalid artifact commitment lists in {snapshot_path}")
        for commitment in custody:
            if not isinstance(commitment, dict):
                raise TimelineError("custody root commitment is not an object")
            _commit_root(
                records,
                commitment,
                direct_proof,
                container_proof,
                runs,
                roots,
                registrations,
            )
        for commitment in registrations_committed:
            if not isinstance(commitment, dict):
                raise TimelineError("registration commitment is not an object")
            logical = str(commitment.get("path", ""))
            _validate_registration(
                records,
                logical,
                raw_sha256=commitment.get("sha256"),
                size=commitment.get("size"),
                canonical_hash=commitment.get("canonicalJsonSha256"),
            )
            _put(registrations, logical, direct_proof)

        if snapshot_path == verification.enumeration_cutover:
            genesis_commitments = digest.get("genesisCommitments")
            enumeration_ref = genesis.get("legacyEnumeration")
            if (
                not isinstance(genesis_commitments, dict)
                or genesis_commitments.get("legacyEnumeration") != enumeration_ref
            ):
                raise TimelineError(
                    "validated cutover enumeration differs from CHAIN_GENESIS"
                )
            if not isinstance(enumeration_ref, dict):
                raise TimelineError("legacy enumeration commitment is not an object")
            enumeration_path = physical_path(
                records, str(enumeration_ref.get("path", ""))
            )
            raw_enumeration = enumeration_path.read_bytes()
            if hashlib.sha256(raw_enumeration).hexdigest() != enumeration_ref.get(
                "sha256"
            ) or len(raw_enumeration) != enumeration_ref.get("size"):
                raise TimelineError("validated legacy enumeration bytes mismatch")
            enumeration = json.loads(raw_enumeration)
            if canonical_sha256(enumeration) != enumeration_ref.get(
                "canonicalJsonSha256"
            ):
                raise TimelineError("validated legacy enumeration hash mismatch")
            for entry in enumeration.get("entries", []):
                logical = str(entry.get("path", ""))
                parts = PurePosixPath(logical).parts
                if (
                    len(parts) >= 4
                    and parts[0] == "records"
                    and parts[-1] == ("manifest.json")
                ):
                    manifest_path = physical_path(records, logical)
                    manifest = json.loads(manifest_path.read_bytes())
                    if manifest.get("schemaVersion") in RUN_MANIFEST_SCHEMAS:
                        _put(
                            runs,
                            PurePosixPath(*parts[:-1]).as_posix(),
                            container_proof,
                        )
                elif (
                    len(parts) == 3
                    and parts[0:2] == ("records", "targets")
                    and parts[-1].endswith(".json")
                ):
                    _validate_registration(
                        records,
                        logical,
                        raw_sha256=entry.get("sha256"),
                        size=entry.get("size"),
                    )
                    _put(registrations, logical, container_proof)

        for commitment in _root_commitments_from_log(records, digest):
            _commit_root(
                records,
                commitment,
                container_proof,
                container_proof,
                runs,
                roots,
                registrations,
            )
    return {
        "schemaVersion": "thesis_witnessed_timeline_v1",
        "runs": runs,
        "custodyRoots": roots,
        "registrationSnapshots": registrations,
    }


def write_timeline(records: Path, output: Path) -> dict[str, Any]:
    timeline = extract_timeline(records)
    data = canonical_bytes(timeline) + b"\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    return timeline


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=Path, default=ROOT / "records")
    parser.add_argument(
        "--output", type=Path, default=ROOT / "records" / "witnessed-timeline.json"
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        timeline = extract_timeline(args.records)
    except TimelineError as exc:
        print(f"TIMELINE BROKEN: {exc}", file=sys.stderr)
        return 1
    data = canonical_bytes(timeline) + b"\n"
    if args.check:
        if not args.output.is_file() or args.output.read_bytes() != data:
            print("witnessed timeline is stale", file=sys.stderr)
            return 1
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(data)
    print(
        f"timeline OK: runs={len(timeline['runs'])} "
        f"custodyRoots={len(timeline['custodyRoots'])} "
        f"registrationSnapshots={len(timeline['registrationSnapshots'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
