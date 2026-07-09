#!/usr/bin/env python3
"""Verify a thesis.analyst run's exact bytes and canonical custody root."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from canonical_json import canonical_bytes, canonical_sha256


class CustodyError(ValueError):
    pass


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_artifact_path(run_dir: Path, relative: str) -> Path:
    path = (run_dir / relative).resolve()
    try:
        path.relative_to(run_dir.resolve())
    except ValueError as exc:
        raise CustodyError(f"artifact path escapes run directory: {relative}") from exc
    return path


def _self_hash_payload(manifest: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(manifest)
    payload.pop("custodyRootSha256", None)
    payload["artifacts"] = [
        artifact
        for artifact in payload.get("artifacts", [])
        if artifact.get("artifactType") != "manifest"
    ]
    return payload


def verify_run(run_dir: Path) -> None:
    run_dir = run_dir.resolve()
    root_path = run_dir / "custody_root.json"
    manifest_path = run_dir / "manifest.json"
    if not root_path.is_file():
        raise CustodyError(f"missing custody root: {root_path}")
    if not manifest_path.is_file():
        raise CustodyError(f"missing manifest: {manifest_path}")

    try:
        custody = json.loads(root_path.read_bytes())
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CustodyError(f"invalid JSON in {root_path}: {exc}") from exc
    try:
        manifest = json.loads(manifest_path.read_bytes())
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CustodyError(f"invalid JSON in {manifest_path}: {exc}") from exc

    if custody.get("schemaVersion") != "thesis_custody_root_v1":
        raise CustodyError(
            f"unsupported custody schema: {custody.get('schemaVersion')!r}"
        )

    entries = custody.get("artifacts")
    if not isinstance(entries, list):
        raise CustodyError("custody_root.json artifacts must be a list")
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise CustodyError("custody artifact entry is not an object")
        artifact_type = str(entry.get("artifactType"))
        relative = str(entry.get("path"))
        identity = (artifact_type, relative)
        if identity in seen:
            raise CustodyError(
                f"duplicate custody artifact: {artifact_type} {relative}"
            )
        seen.add(identity)
        path = _safe_artifact_path(run_dir, relative)
        if not path.is_file():
            raise CustodyError(f"missing artifact {artifact_type}: {relative}")
        raw = path.read_bytes()
        actual_sha = _sha256(raw)
        if actual_sha != entry.get("sha256"):
            raise CustodyError(
                f"raw SHA-256 mismatch for {artifact_type} {relative}: "
                f"expected {entry.get('sha256')}, got {actual_sha}"
            )
        if len(raw) != entry.get("bytes"):
            raise CustodyError(
                f"byte-count mismatch for {artifact_type} {relative}: "
                f"expected {entry.get('bytes')}, got {len(raw)}"
            )
        if "canonicalJsonSha256" in entry:
            try:
                value = json.loads(raw)
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise CustodyError(
                    f"artifact marked as JSON is invalid: {relative}: {exc}"
                ) from exc
            actual_canonical = canonical_sha256(value)
            if actual_canonical != entry["canonicalJsonSha256"]:
                raise CustodyError(
                    f"canonical JSON SHA-256 mismatch for {artifact_type} "
                    f"{relative}: expected {entry['canonicalJsonSha256']}, "
                    f"got {actual_canonical}"
                )

    referenced = {
        (str(ref.get("artifactType")), Path(str(ref.get("path"))).name)
        for ref in manifest.get("artifacts", [])
        if ref.get("artifactType") != "manifest"
    }
    if seen != referenced:
        missing = sorted(referenced - seen)
        extra = sorted(seen - referenced)
        raise CustodyError(
            f"custody artifact coverage mismatch: missing={missing}, extra={extra}"
        )

    if manifest.get("ok"):
        required = {"prompt", "command", "normalized_cell", "cells_with_activity"}
        present = {artifact_type for artifact_type, _ in seen}
        absent = sorted(required - present)
        if absent:
            raise CustodyError(
                "successful run is missing required custody artifact types: "
                + ", ".join(absent)
            )

    manifest_without_root = copy.deepcopy(manifest)
    manifest_without_root.pop("custodyRootSha256", None)
    manifest_commitment = custody.get("manifestWithoutCustodyRoot") or {}
    actual_manifest_sha = canonical_sha256(manifest_without_root)
    if actual_manifest_sha != manifest_commitment.get("canonicalJsonSha256"):
        raise CustodyError(
            "manifest-without-root canonical SHA-256 mismatch: expected "
            f"{manifest_commitment.get('canonicalJsonSha256')}, "
            f"got {actual_manifest_sha}"
        )

    self_refs = [
        ref
        for ref in manifest.get("artifacts", [])
        if ref.get("artifactType") == "manifest"
    ]
    if len(self_refs) != 1:
        raise CustodyError(
            "manifest must contain exactly one self artifact entry, got "
            f"{len(self_refs)}"
        )
    self_bytes = canonical_bytes(_self_hash_payload(manifest))
    self_sha = _sha256(self_bytes)
    if self_sha != self_refs[0].get("sha256"):
        raise CustodyError(
            "manifest self-entry SHA-256 mismatch: expected "
            f"{self_refs[0].get('sha256')}, got {self_sha}"
        )
    if len(self_bytes) != self_refs[0].get("bytes"):
        raise CustodyError(
            "manifest self-entry byte-count mismatch: expected "
            f"{self_refs[0].get('bytes')}, got {len(self_bytes)}"
        )

    actual_root_sha = canonical_sha256(custody)
    if actual_root_sha != manifest.get("custodyRootSha256"):
        raise CustodyError(
            "custody root SHA-256 mismatch: expected "
            f"{manifest.get('custodyRootSha256')}, got {actual_root_sha}"
        )


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_custody.py <run-dir>", file=sys.stderr)
        return 2
    try:
        verify_run(Path(sys.argv[1]))
    except CustodyError as exc:
        print(f"CUSTODY BROKEN: {exc}", file=sys.stderr)
        return 1
    print(f"custody OK: {sys.argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
