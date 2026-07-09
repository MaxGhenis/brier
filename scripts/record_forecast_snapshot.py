#!/usr/bin/env python3
"""Create one immutable, body-archiving forecast-surface snapshot."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import urllib.parse
from pathlib import Path
from typing import Any

from thesis_log_client import load_thesis_log_from_directory
from verify_record_chain import logical_path, verify_records

SURFACES = {
    "log": ("log.json", "https://app.thesisinstitute.org/log.json"),
    "ledger": ("ledger.json", "https://app.thesisinstitute.org/ledger.json"),
    "targets": ("targets.json", "https://app.thesisinstitute.org/targets.json"),
    "reward": ("reward.json", "https://app.thesisinstitute.org/brier/reward.json"),
    "build": ("build.json", "https://app.thesisinstitute.org/build.json"),
    "ledgerCommitApi": (
        "ledger-commit.json",
        "https://api.github.com/repos/PolicyEngine/arch-data/commits/"
        "codex/thesis-ledger-facts",
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def archive_body(source: Path, destination: Path) -> dict[str, Any]:
    raw = source.read_bytes()
    json.loads(raw)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(f"refusing to overwrite archive: {destination}")
    with destination.open("xb") as stream:
        with gzip.GzipFile(filename="", mode="wb", fileobj=stream, mtime=0) as zipped:
            zipped.write(raw)
    compressed = destination.read_bytes()
    return {
        "sha256": sha256(raw),
        "bytes": len(raw),
        "archivePath": str(destination),
        "archiveSha256": sha256(compressed),
        "archiveBytes": len(compressed),
        "contentEncoding": "gzip",
    }


def exclusive_json_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=Path, default=Path("records"))
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--recorded-at", required=True)
    parser.add_argument("--repo-sha", required=True)
    parser.add_argument("--ledger-sha", required=True)
    args = parser.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.run_id):
        raise SystemExit(
            "run-id may contain only letters, digits, dot, underscore, dash"
        )
    ordered = verify_records(args.records)
    previous = ordered[-1]
    day = args.recorded_at[:10]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        raise SystemExit("recorded-at must begin with an ISO UTC date")

    day_dir = args.records / day
    digest_path = day_dir / f"digest-{args.run_id}.json"
    body_dir = day_dir / f"bodies-{args.run_id}"
    repo_root = args.records.parent.resolve()
    surface_records: dict[str, Any] = {}
    for name, (filename, url) in SURFACES.items():
        source = args.source_dir / filename
        if not source.is_file():
            raise SystemExit(f"missing fetched response body: {source}")
        destination = body_dir / f"{filename}.gz"
        record = archive_body(source, destination)
        record["archivePath"] = str(destination.resolve().relative_to(repo_root))
        record["url"] = url
        surface_records[name] = record

    log_chunk_records: dict[str, Any] = {}
    log_manifest = json.loads((args.source_dir / "log.json").read_text())
    if log_manifest.get("schemaVersion") == "thesis_log_v3":
        for collection, collection_manifest in log_manifest["collections"].items():
            for reference in collection_manifest["chunks"]:
                relative = Path(reference["url"].lstrip("/"))
                source = args.source_dir / relative
                destination = body_dir / Path(f"{relative}.gz")
                record = archive_body(source, destination)
                record["archivePath"] = str(
                    destination.resolve().relative_to(repo_root)
                )
                record["url"] = urllib.parse.urljoin(
                    "https://app.thesisinstitute.org/log.json", reference["url"]
                )
                record["manifestSha256"] = reference["sha256"]
                log_chunk_records[f"{collection}:{reference['index']}"] = record

    live_records: dict[str, Any] = {}
    live_source = args.source_dir / "live"
    if live_source.is_dir():
        for source in sorted(live_source.glob("*.json")):
            destination = body_dir / "live" / f"{source.name}.gz"
            record = archive_body(source, destination)
            record["archivePath"] = str(destination.resolve().relative_to(repo_root))
            live_records[source.stem] = record

    log = load_thesis_log_from_directory(args.source_dir)
    entries = log.get("entries", [])
    recorded = [
        entry for entry in entries if entry.get("kind") == "prediction_recorded"
    ]
    resolved = [
        entry for entry in entries if entry.get("kind") == "prediction_resolved"
    ]
    build_payload = json.loads((args.source_dir / "build.json").read_text())
    payload = {
        "schemaVersion": "thesis_record_snapshot_v2",
        "snapshotKind": "recorder_run",
        "runId": args.run_id,
        "recordedAt": args.recorded_at,
        "chain": {
            "prevDigestPath": logical_path(args.records.resolve(), previous),
            "prevDigestSha256": sha256(previous.read_bytes()),
        },
        "dependencies": {
            "recorderRepositoryCommit": args.repo_sha,
            "ledgerRepository": "PolicyEngine/arch-data",
            "ledgerBranch": "codex/thesis-ledger-facts",
            "ledgerBranchCommit": args.ledger_sha,
            "liveBuildCanary": build_payload,
        },
        "surfaces": surface_records,
        "logChunks": log_chunk_records,
        "liveForecasts": live_records,
        "counts": {"recorded": len(recorded), "resolved": len(resolved)},
        "predictions": [
            {
                key: entry.get(key)
                for key in (
                    "forecastSlug",
                    "pointEstimate",
                    "interval80",
                    "resolutionDate",
                    "recordedAt",
                )
            }
            for entry in recorded
        ],
        "resolutions": resolved,
    }
    exclusive_json_write(digest_path, payload)

    index_path = day_dir / "index.json"
    snapshots = sorted(
        path.name
        for path in day_dir.glob("digest-*.json")
        if not path.name.endswith(".witness.json")
    )
    index_path.write_text(
        json.dumps(
            {
                "schemaVersion": "thesis_record_day_index_v1",
                "integrityNote": "informational only; chain links are authoritative",
                "snapshots": snapshots,
            },
            indent=2,
        )
        + "\n"
    )
    print(digest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
