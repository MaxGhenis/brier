#!/usr/bin/env python3
"""Request and pin-verify independent RFC 3161 witnesses for one snapshot."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from verify_custody import verify_recorder_snapshot
from verify_record_chain import (
    ChainError,
    ChainVerification,
    TokenEvidence,
    _load_trust_bundle,
    _run_openssl,
    _select_anchor,
    _supplemental_candidates,
    _trust_bundle_updates,
    load_json,
    logical_path,
    preferred_active_trust_bundle,
    sha256_file,
    verify_chain,
    verify_timestamp_token,
)

MAX_TOKEN_BYTES = 1024 * 1024
Requester = Callable[[str, bytes, float], bytes]


class WitnessWriteError(RuntimeError):
    pass


@dataclass(frozen=True)
class WitnessTarget:
    bundle_reference: dict[str, Any]
    anchor: dict[str, Any]
    supplemental: bool


def request_timestamp(endpoint: str, query: bytes, timeout_seconds: float) -> bytes:
    request = urllib.request.Request(
        endpoint,
        data=query,
        headers={
            "Content-Type": "application/timestamp-query",
            "User-Agent": "Thesis-RFC3161-Witness/2",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        body = response.read(MAX_TOKEN_BYTES + 1)
    if not body:
        raise WitnessWriteError("TSA returned an empty response")
    if len(body) > MAX_TOKEN_BYTES:
        raise WitnessWriteError("TSA response exceeds the one-megabyte limit")
    return body


def _exclusive_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)


def _atomic_json_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(payload, indent=2) + "\n").encode()
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _deduplicate_updates(
    references: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    deduplicated: dict[str, dict[str, Any]] = {}
    for reference in references:
        path = str(reference["path"])
        existing = deduplicated.get(path)
        if existing is not None and existing != reference:
            raise ChainError(f"conflicting pending TSA trust references: {path}")
        deduplicated[path] = reference
    return list(deduplicated.values())


def witness_targets(
    records: Path,
    verification: ChainVerification,
    snapshot_payload: dict[str, Any],
) -> tuple[dict[str, Any], list[WitnessTarget], list[dict[str, Any]]]:
    evidence_bundle = preferred_active_trust_bundle(verification.active_trust_bundles)
    _path, evidence_trust = _load_trust_bundle(records, evidence_bundle)
    targets = [
        WitnessTarget(evidence_bundle, anchor, False)
        for anchor in evidence_trust["anchors"]
    ]
    transition_updates = _deduplicate_updates(
        [
            *verification.pending_trust_bundle_updates,
            *_trust_bundle_updates(records, snapshot_payload),
        ]
    )
    supplemental = _supplemental_candidates(
        records,
        verification.active_trust_bundles,
        transition_updates,
    )
    targets.extend(
        WitnessTarget(reference, anchor, True)
        for reference, anchor in supplemental.values()
    )
    for target in targets:
        _path, trust = _load_trust_bundle(records, target.bundle_reference)
        _select_anchor(
            records,
            {
                "tsaAnchorId": target.anchor["id"],
                "tsa": target.anchor["endpoint"],
            },
            trust,
        )
    return evidence_bundle, targets, transition_updates


def _token_path(digest: Path, anchor_id: str) -> Path:
    return digest.with_name(f"{digest.stem}.{anchor_id}.tsr")


def _available_claims(evidence: TokenEvidence) -> dict[str, str]:
    return {
        "tsaPolicyOid": evidence.policy_oid,
        "tsaImprintAlgorithmOid": evidence.imprint_algorithm_oid,
        "tsaGenTime": evidence.gen_time,
        "tsaSignerCertificateSha256": evidence.tsa_certificate_sha256,
        "tsaSignerSpkiSha256": evidence.tsa_spki_sha256,
    }


def _request_outcome(
    records: Path,
    digest: Path,
    query: bytes,
    target: WitnessTarget,
    *,
    requester: Requester,
    timeout_seconds: float,
) -> dict[str, Any]:
    reference = target.bundle_reference
    anchor = target.anchor
    outcome: dict[str, Any] = {
        "status": "unavailable",
        "tsa": anchor["endpoint"],
        "tsaAnchorId": anchor["id"],
    }
    if target.supplemental:
        outcome.update(
            {
                "role": "pending_trust_bundle",
                "trustBundleId": reference["bundleId"],
                "trustBundlePath": reference["path"],
                "trustBundleSha256": reference["sha256"],
            }
        )
    try:
        token_bytes = requester(anchor["endpoint"], query, timeout_seconds)
    except (
        http.client.HTTPException,
        OSError,
        WitnessWriteError,
    ) as exc:
        outcome["reason"] = f"timestamp request failed: {exc}"
        return outcome

    token_path = _token_path(digest, str(anchor["id"]))
    token_logical = logical_path(records, token_path)
    _exclusive_write(token_path, token_bytes)
    claim = {
        **outcome,
        "status": "available",
        "trustBundleId": reference["bundleId"],
        "trustBundlePath": reference["path"],
        "trustBundleSha256": reference["sha256"],
        "tokenPath": token_logical,
        "tokenSha256": hashlib.sha256(token_bytes).hexdigest(),
    }
    try:
        evidence = verify_timestamp_token(
            digest,
            claim,
            reference,
            records=records,
        )
    except ChainError as exc:
        token_path.unlink()
        outcome["reason"] = f"pinned timestamp verification failed: {exc}"
        return outcome
    outcome.update(
        {
            "status": "available",
            "tokenPath": token_logical,
            "tokenSha256": evidence.token_sha256,
            **_available_claims(evidence),
        }
    )
    return outcome


def witness_snapshot(
    records: Path,
    digest: Path,
    *,
    requester: Requester = request_timestamp,
    timeout_seconds: float = 45,
) -> Path:
    records = records.resolve()
    digest = digest.resolve()
    try:
        digest.relative_to(records)
    except ValueError as exc:
        raise WitnessWriteError("digest must be inside the records directory") from exc
    if digest.with_suffix(".witness.json").exists():
        raise WitnessWriteError("refusing to overwrite an existing witness marker")
    verify_recorder_snapshot(digest)
    verification = verify_chain(records, pending_snapshot=digest)
    snapshot_payload = load_json(digest)
    evidence_bundle, targets, _transition_updates = witness_targets(
        records, verification, snapshot_payload
    )

    with tempfile.TemporaryDirectory(prefix="thesis-witness-query-") as temporary:
        query_path = Path(temporary) / "request.tsq"
        _run_openssl(
            [
                "ts",
                "-query",
                "-config",
                "/dev/null",
                "-data",
                str(digest),
                "-sha256",
                "-cert",
                "-out",
                str(query_path),
            ]
        )
        query = query_path.read_bytes()

    evidence_outcomes: list[dict[str, Any]] = []
    supplemental_outcomes: list[dict[str, Any]] = []
    for target in targets:
        outcome = _request_outcome(
            records,
            digest,
            query,
            target,
            requester=requester,
            timeout_seconds=timeout_seconds,
        )
        collection = supplemental_outcomes if target.supplemental else evidence_outcomes
        collection.append(outcome)

    available = any(outcome["status"] == "available" for outcome in evidence_outcomes)
    marker: dict[str, Any] = {
        "schemaVersion": "thesis_rfc3161_witness_v2",
        "status": "available" if available else "unavailable",
        "digestSha256": sha256_file(digest),
        "trustBundleId": evidence_bundle["bundleId"],
        "trustBundlePath": evidence_bundle["path"],
        "trustBundleSha256": evidence_bundle["sha256"],
        "anchorOutcomes": evidence_outcomes,
        "supplementalOutcomes": supplemental_outcomes,
    }
    if not available:
        marker["reason"] = "all active-bundle TSA requests or verifications failed"

    witness_path = digest.with_suffix(".witness.json")
    _exclusive_write(witness_path, (json.dumps(marker, indent=2) + "\n").encode())
    _atomic_json_write(
        records / "CHAIN_HEAD.json",
        {
            "schemaVersion": "thesis_record_chain_head_v1",
            "snapshotPath": logical_path(records, digest),
            "snapshotSha256": marker["digestSha256"],
        },
    )
    verify_chain(records)
    return witness_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=Path, default=Path("records"))
    parser.add_argument("--digest", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=float, default=45)
    args = parser.parse_args()
    try:
        witness_path = witness_snapshot(
            args.records,
            args.digest,
            timeout_seconds=args.timeout_seconds,
        )
    except (ChainError, WitnessWriteError, OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    print(witness_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
