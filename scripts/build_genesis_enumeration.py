#!/usr/bin/env python3
"""One-shot builder for the complete legacy enumeration and chain cutover."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from canonical_json import canonical_bytes, canonical_sha256
from verify_custody import verify_run
from verify_record_chain import logical_path, physical_path, sha256_file, verify_chain

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECORDS = ROOT / "records"
SHA_RE = re.compile(r"[0-9a-f]{40,64}")
RUN_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


class BuildError(ValueError):
    pass


def _git(arguments: list[str], *, binary: bool = False) -> bytes | str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode(errors="replace").strip()
        raise BuildError(f"git {' '.join(arguments)} failed: {detail}")
    return completed.stdout if binary else completed.stdout.decode()


def _source_paths(source_commit: str) -> list[tuple[str, int]]:
    raw = _git(
        ["ls-tree", "-r", "-z", "--long", source_commit, "--", "records"],
        binary=True,
    )
    assert isinstance(raw, bytes)
    entries: list[tuple[str, int]] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        metadata, separator, path_bytes = item.partition(b"\t")
        if not separator:
            raise BuildError("unexpected git ls-tree output")
        fields = metadata.decode().split()
        if len(fields) != 4:
            raise BuildError("unexpected git ls-tree metadata")
        mode, object_type, _object_id, size_text = fields
        try:
            path = path_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise BuildError("legacy record path is not UTF-8") from exc
        if mode != "100644" or object_type != "blob":
            raise BuildError(
                "legacy enumeration refuses non-regular file "
                f"{path} ({mode} {object_type})"
            )
        entries.append((path, int(size_text)))
    if not entries:
        raise BuildError("source commit has no records files")
    paths = [path for path, _ in entries]
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise BuildError("source Git tree paths are not sorted and unique")
    return entries


def build_enumeration(source_commit: str) -> dict[str, Any]:
    if not SHA_RE.fullmatch(source_commit):
        raise BuildError("source commit must be a full Git object ID")
    changed = _git(
        [
            "diff",
            "--name-only",
            "--diff-filter=MDT",
            source_commit,
            "--",
            "records",
        ]
    )
    assert isinstance(changed, str)
    if changed.strip():
        raise BuildError(
            "legacy source-tree files changed after the cutoff:\n" + changed.strip()
        )
    entries: list[dict[str, Any]] = []
    total_size = 0
    for logical, git_size in _source_paths(source_commit):
        path = ROOT / logical
        if not path.exists():
            raise BuildError(f"legacy record is missing from the worktree: {logical}")
        mode = path.lstat().st_mode
        if not stat.S_ISREG(mode) or path.is_symlink():
            raise BuildError(f"legacy record is not a regular file: {logical}")
        raw = path.read_bytes()
        if len(raw) != git_size:
            raise BuildError(
                "legacy record size differs from cutoff tree for "
                f"{logical}: {len(raw)} != {git_size}"
            )
        entries.append(
            {
                "path": logical,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "size": len(raw),
            }
        )
        total_size += len(raw)
    return {
        "schemaVersion": "thesis_legacy_record_enumeration_v1",
        "sourceCommit": source_commit,
        "entryCount": len(entries),
        "totalSize": total_size,
        "entries": entries,
    }


def _write_once(path: Path, data: bytes) -> None:
    if path.exists():
        if path.read_bytes() != data:
            raise BuildError(
                f"refusing to overwrite different one-shot artifact: {path}"
            )
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(data)


def _enumeration_reference(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "canonicalJsonSha256": canonical_sha256(payload),
        "size": len(raw),
        "entryCount": payload["entryCount"],
        "totalSize": payload["totalSize"],
        "sourceCommit": payload["sourceCommit"],
    }


def _file_commitment(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_bytes())
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": sha256_file(path),
        "size": path.stat().st_size,
        "canonicalJsonSha256": canonical_sha256(payload),
    }


def _trust_bundle_commitment(path: Path) -> dict[str, Any]:
    commitment = _file_commitment(path)
    payload = json.loads(path.read_bytes())
    bundle_id = payload.get("bundleId")
    if not isinstance(bundle_id, str) or not bundle_id:
        raise BuildError(f"trust bundle lacks bundleId: {path}")
    return {"bundleId": bundle_id, **commitment}


def _anchored_source_commit(records: Path) -> str:
    genesis = json.loads((records / "CHAIN_GENESIS.json").read_bytes())
    first = physical_path(records, str(genesis.get("firstSnapshot", "")))
    payload = json.loads(first.read_bytes())
    dependencies = payload.get("dependencies")
    source = (
        dependencies.get("recorderRepositoryCommit")
        if isinstance(dependencies, dict)
        else None
    )
    if not isinstance(source, str) or not SHA_RE.fullmatch(source):
        raise BuildError("first chained snapshot lacks recorderRepositoryCommit")
    return source


def _custody_commitments(records: Path) -> list[dict[str, Any]]:
    commitments = []
    for root_path in sorted(records.glob("**/custody_root.json")):
        run_dir = root_path.parent
        result = verify_run(run_dir)
        manifest_path = run_dir / "manifest.json"
        commitments.append(
            {
                "runDirectory": run_dir.relative_to(ROOT).as_posix(),
                "custodyRootPath": root_path.relative_to(ROOT).as_posix(),
                "custodyRootSha256": result.custody_root_sha256,
                "custodyRootFileSha256": sha256_file(root_path),
                "custodyRootSize": root_path.stat().st_size,
                "custodyInventoryVersion": result.custody_inventory_version,
                "manifestPath": manifest_path.relative_to(ROOT).as_posix(),
                "manifestSha256": sha256_file(manifest_path),
                "manifestSize": manifest_path.stat().st_size,
            }
        )
    return commitments


def _registration_commitments(records: Path) -> list[dict[str, Any]]:
    return [
        _file_commitment(path) for path in sorted((records / "targets").glob("*.json"))
    ]


def append_cutover(
    records: Path,
    enumeration_path: Path,
    enumeration: dict[str, Any],
    *,
    recorded_at: str,
    run_id: str,
) -> Path:
    if not RUN_ID_RE.fullmatch(run_id):
        raise BuildError("cutover run ID contains unsafe characters")
    try:
        timestamp = datetime.fromisoformat(recorded_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise BuildError("cutover recorded-at is not RFC 3339") from exc
    if timestamp.tzinfo is None or not recorded_at.endswith("Z"):
        raise BuildError("cutover recorded-at must be UTC with a Z suffix")

    trust_path = records / "trust" / "tsa-anchors-v1.json"
    trust_reference = _trust_bundle_commitment(trust_path)
    verification = verify_chain(
        records,
        allow_pre_enumeration=True,
        bootstrap_trust_bundle=trust_reference,
    )
    previous = verification.ordered[-1]
    genesis_path = records / "CHAIN_GENESIS.json"
    genesis = json.loads(genesis_path.read_bytes())
    cutover_path = records / recorded_at[:10] / f"digest-{run_id}.json"
    reference = _enumeration_reference(enumeration_path, enumeration)
    genesis["legacyEnumeration"] = reference
    genesis["tsaTrustBundle"] = trust_reference
    genesis["enumerationCutoverSnapshot"] = cutover_path.relative_to(ROOT).as_posix()
    genesis_bytes = (json.dumps(genesis, indent=2) + "\n").encode()
    genesis_path.write_bytes(genesis_bytes)

    payload = {
        "schemaVersion": "thesis_record_snapshot_v2",
        "snapshotKind": "genesis_enumeration_cutover",
        "runId": run_id,
        "recordedAt": recorded_at,
        "chain": {
            "prevDigestPath": logical_path(records, previous),
            "prevDigestSha256": sha256_file(previous),
        },
        "genesisCommitments": {
            "legacyEnumeration": reference,
            "chainGenesis": _file_commitment(genesis_path),
            "tsaTrustBundle": trust_reference,
        },
        "artifactCommitments": {
            "custodyRoots": _custody_commitments(records),
            "registrationSnapshots": _registration_commitments(records),
        },
        "note": (
            "One-shot integrity cutover. External chronology begins only when this "
            "digest or a chained successor receives a valid pinned RFC 3161 witness."
        ),
    }
    cutover_bytes = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    _write_once(cutover_path, cutover_bytes)
    digest_sha = hashlib.sha256(cutover_bytes).hexdigest()
    witness_path = cutover_path.with_suffix(".witness.json")
    witness = {
        "schemaVersion": "thesis_rfc3161_witness_v1",
        "status": "unavailable",
        "digestSha256": digest_sha,
        "tsa": "https://freetsa.org/tsr",
        "tsaAnchorId": "freetsa-root-2016",
        "trustBundleId": trust_reference["bundleId"],
        "trustBundlePath": trust_reference["path"],
        "trustBundleSha256": trust_reference["sha256"],
        "reason": (
            "Implementation sandbox had no network. Obtain a pinned RFC 3161 token "
            "for this exact digest before claiming the cutover was externally "
            "witnessed."
        ),
    }
    _write_once(witness_path, (json.dumps(witness, indent=2) + "\n").encode())
    head = {
        "schemaVersion": "thesis_record_chain_head_v1",
        "snapshotPath": cutover_path.relative_to(ROOT).as_posix(),
        "snapshotSha256": digest_sha,
    }
    (records / "CHAIN_HEAD.json").write_text(json.dumps(head, indent=2) + "\n")
    snapshots = sorted(
        path.name
        for path in cutover_path.parent.glob("digest-*.json")
        if not path.name.endswith(".witness.json")
    )
    index = {
        "schemaVersion": "thesis_record_day_index_v1",
        "integrityNote": "informational only; chain links are authoritative",
        "snapshots": snapshots,
    }
    (cutover_path.parent / "index.json").write_text(json.dumps(index, indent=2) + "\n")
    verify_chain(records)
    return cutover_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_RECORDS / "GENESIS_RECORDS.json"
    )
    parser.add_argument("--append-cutover", action="store_true")
    parser.add_argument("--cutover-recorded-at")
    parser.add_argument("--cutover-run-id", default="genesis-enumeration-v1")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    records = args.records.resolve()
    output = args.output.resolve()
    anchored_source = _anchored_source_commit(records)
    if args.source_commit != anchored_source:
        raise SystemExit(
            "--source-commit must equal the recorderRepositoryCommit fixed by "
            f"the first chained snapshot: {anchored_source}"
        )
    enumeration = build_enumeration(args.source_commit)
    data = canonical_bytes(enumeration)
    if args.check:
        if not output.is_file() or output.read_bytes() != data:
            raise SystemExit("genesis enumeration is missing or not reproducible")
        print(
            f"enumeration reproducible: {output} entries={enumeration['entryCount']} "
            f"bytes={enumeration['totalSize']} "
            f"sha256={hashlib.sha256(data).hexdigest()}"
        )
        return 0
    _write_once(output, data)
    print(
        f"wrote {output}: entries={enumeration['entryCount']} "
        f"bytes={enumeration['totalSize']} sha256={hashlib.sha256(data).hexdigest()}"
    )
    if args.append_cutover:
        if not args.cutover_recorded_at:
            raise SystemExit("--append-cutover requires --cutover-recorded-at")
        cutover = append_cutover(
            records,
            output,
            enumeration,
            recorded_at=args.cutover_recorded_at,
            run_id=args.cutover_run_id,
        )
        print(f"appended pending-witness cutover: {cutover}")
    elif args.cutover_recorded_at:
        raise SystemExit("--cutover-recorded-at requires --append-cutover")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
