#!/usr/bin/env python3
"""Fail-closed verification for the per-invocation forecast record chain."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SNAPSHOT_RE = re.compile(r"digest-[A-Za-z0-9][A-Za-z0-9._-]*\.json$")


class ChainError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def logical_path(records: Path, path: Path) -> str:
    return str(Path("records") / path.relative_to(records))


def physical_path(records: Path, value: str) -> Path:
    logical = Path(value)
    if logical.is_absolute() or ".." in logical.parts:
        raise ChainError(f"unsafe record path in genesis/chain: {value!r}")
    if logical.parts and logical.parts[0] == "records":
        logical = Path(*logical.parts[1:])
    return records / logical


def snapshot_paths(records: Path) -> list[Path]:
    return sorted(
        path
        for path in records.glob("????-??-??/digest-*.json")
        if SNAPSHOT_RE.fullmatch(path.name) and not path.name.endswith(".witness.json")
    )


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ChainError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ChainError(f"record must be a JSON object: {path}")
    return value


def verify_witness(path: Path) -> None:
    digest_sha = sha256_file(path)
    witness_path = path.with_suffix(".witness.json")
    if not witness_path.is_file():
        raise ChainError(f"missing explicit witness marker for {path}")
    witness = load_json(witness_path)
    if witness.get("digestSha256") != digest_sha:
        raise ChainError(
            f"witness digest mismatch for {path}: expected {digest_sha}, "
            f"got {witness.get('digestSha256')}"
        )
    status = witness.get("status")
    if status not in {"available", "unavailable"}:
        raise ChainError(f"invalid witness status for {path}: {status!r}")
    if status == "available":
        token_path = physical_path(path.parents[1], str(witness.get("tokenPath", "")))
        if not token_path.is_file():
            raise ChainError(f"witness token is missing for {path}: {token_path}")
        if sha256_file(token_path) != witness.get("tokenSha256"):
            raise ChainError(f"witness token hash mismatch for {path}")
        ca_path = physical_path(
            path.parents[1], str(witness.get("caCertificatePath", ""))
        )
        tsa_path = physical_path(
            path.parents[1], str(witness.get("tsaCertificatePath", ""))
        )
        if not ca_path.is_file() or not tsa_path.is_file():
            raise ChainError(f"witness certificate archive is missing for {path}")
        if sha256_file(ca_path) != witness.get("caCertificateSha256"):
            raise ChainError(f"witness CA certificate hash mismatch for {path}")
        if sha256_file(tsa_path) != witness.get("tsaCertificateSha256"):
            raise ChainError(f"witness TSA certificate hash mismatch for {path}")
        try:
            completed = subprocess.run(
                [
                    "openssl",
                    "ts",
                    "-verify",
                    "-data",
                    str(path),
                    "-in",
                    str(token_path),
                    "-CAfile",
                    str(ca_path),
                    "-untrusted",
                    str(tsa_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError as exc:
            raise ChainError("openssl is required to verify RFC 3161 tokens") from exc
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip()
            raise ChainError(f"RFC 3161 verification failed for {path}: {detail}")
    elif not witness.get("reason"):
        raise ChainError(f"unavailable witness lacks a reason for {path}")


def verify_records(records: Path) -> list[Path]:
    records = records.resolve()
    genesis_path = records / "CHAIN_GENESIS.json"
    if not genesis_path.is_file():
        raise ChainError(f"missing chain genesis: {genesis_path}")
    genesis = load_json(genesis_path)
    if genesis.get("schemaVersion") != "thesis_record_chain_genesis_v1":
        raise ChainError(
            f"unsupported genesis schema: {genesis.get('schemaVersion')!r}"
        )

    legacy_entries = genesis.get("legacyDigests")
    if not isinstance(legacy_entries, list):
        raise ChainError("genesis legacyDigests must be a list")
    listed_legacy: set[str] = set()
    for entry in legacy_entries:
        if not isinstance(entry, dict):
            raise ChainError("legacy digest entry must be an object")
        logical = str(entry.get("path"))
        if logical in listed_legacy:
            raise ChainError(f"duplicate legacy digest in genesis: {logical}")
        listed_legacy.add(logical)
        path = physical_path(records, logical)
        if not path.is_file():
            raise ChainError(f"genesis-listed legacy digest is missing: {logical}")
        actual = sha256_file(path)
        if actual != entry.get("sha256"):
            raise ChainError(
                f"legacy digest hash mismatch for {logical}: "
                f"expected {entry.get('sha256')}, got {actual}"
            )
    discovered_legacy = {
        logical_path(records, path) for path in records.glob("????-??-??/digest.json")
    }
    if discovered_legacy != listed_legacy:
        raise ChainError(
            "legacy digest enumeration mismatch: "
            f"unlisted={sorted(discovered_legacy - listed_legacy)}, "
            f"missing={sorted(listed_legacy - discovered_legacy)}"
        )

    snapshots = snapshot_paths(records)
    first_logical = genesis.get("firstSnapshot")
    if not isinstance(first_logical, str) or not first_logical:
        raise ChainError("genesis firstSnapshot must name one snapshot")
    first = physical_path(records, first_logical)
    if first not in snapshots:
        raise ChainError(f"genesis snapshot is missing or malformed: {first_logical}")

    snapshot_set = set(snapshots)
    successors: dict[Path, list[Path]] = {path: [] for path in snapshots}
    for path in snapshots:
        payload = load_json(path)
        if payload.get("schemaVersion") != "thesis_record_snapshot_v2":
            raise ChainError(f"unsupported snapshot schema in {path}")
        chain = payload.get("chain")
        if path == first:
            if chain is not None:
                raise ChainError(
                    f"genesis snapshot must not have a chain block: {path}"
                )
        else:
            if not isinstance(chain, dict):
                raise ChainError(f"missing chain block after genesis: {path}")
            previous_logical = chain.get("prevDigestPath")
            if not isinstance(previous_logical, str):
                raise ChainError(f"missing chain.prevDigestPath in {path}")
            previous = physical_path(records, previous_logical)
            if previous not in snapshot_set:
                raise ChainError(f"missing predecessor for {path}: {previous_logical}")
            expected_sha = sha256_file(previous)
            if chain.get("prevDigestSha256") != expected_sha:
                raise ChainError(
                    f"predecessor hash mismatch in {path}: "
                    f"expected {expected_sha}, got {chain.get('prevDigestSha256')}"
                )
            successors[previous].append(path)
        verify_witness(path)

    ordered = [first]
    visited = {first}
    cursor = first
    while successors[cursor]:
        children = successors[cursor]
        if len(children) != 1:
            raise ChainError(
                f"fork after {logical_path(records, cursor)}: "
                + ", ".join(logical_path(records, child) for child in children)
            )
        cursor = children[0]
        if cursor in visited:
            raise ChainError(f"cycle at {logical_path(records, cursor)}")
        visited.add(cursor)
        ordered.append(cursor)
    if visited != snapshot_set:
        raise ChainError(
            "orphaned snapshot(s) not reachable from genesis: "
            + ", ".join(
                logical_path(records, path) for path in sorted(snapshot_set - visited)
            )
        )
    head_path = records / "CHAIN_HEAD.json"
    if not head_path.is_file():
        raise ChainError(f"missing chain head commitment: {head_path}")
    head = load_json(head_path)
    if head.get("schemaVersion") != "thesis_record_chain_head_v1":
        raise ChainError(
            f"unsupported chain head schema: {head.get('schemaVersion')!r}"
        )
    expected_head_path = logical_path(records, ordered[-1])
    expected_head_sha = sha256_file(ordered[-1])
    if head.get("snapshotPath") != expected_head_path:
        raise ChainError(
            "chain head path mismatch: "
            f"expected {expected_head_path}, got {head.get('snapshotPath')}"
        )
    if head.get("snapshotSha256") != expected_head_sha:
        raise ChainError(
            "chain head hash mismatch: "
            f"expected {expected_head_sha}, got {head.get('snapshotSha256')}"
        )
    return ordered


def main() -> int:
    records = Path(sys.argv[1] if len(sys.argv) > 1 else "records")
    try:
        ordered = verify_records(records)
    except ChainError as exc:
        print(f"CHAIN BROKEN: {exc}", file=sys.stderr)
        return 1
    print(f"chain OK: {len(ordered)} snapshot(s), head={ordered[-1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
