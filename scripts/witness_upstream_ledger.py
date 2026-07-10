#!/usr/bin/env python3
"""Witness the upstream fact ledger's exact bytes into the record chain.

The recorder archives the site's DERIVED ledger.json, but the upstream
``official_observations.jsonl`` on PolicyEngine/ledger's thesis-facts branch
remained mutable history: nothing in Thesis's witnessed records held the raw
bytes. This run archives, custody-rooted and chain-committed by the next
recorder digest:

- the observation JSONL bytes at one immutable commit SHA (never a branch);
- the GitHub commit API responses for the thesis-facts branch head and the
  ledger main head, binding both SHAs to their commit metadata;
- optional extra upstream artifacts (``--extra name=path-or-url``), e.g. the
  populace consumer-artifact bytes a population release was built from.

Ledger mutability stops mattering for history once these bytes are inside
brier's witnessed chain.

Usage:
    python3 scripts/witness_upstream_ledger.py [--ledger-sha SHA]
        [--expect-line-count N] [--expect-jsonl-sha256 HEX]
        [--extra name=path-or-url ...] [--note TEXT]
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import gzip
import hashlib
import json
import os
import pathlib
import re
import sys
import urllib.request
from typing import Any

from canonical_json import canonical_bytes, canonical_sha256
from verify_custody import verify_run

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER_REPO = "PolicyEngine/ledger"
LEDGER_BRANCH = "codex/thesis-ledger-facts"
LEDGER_JSONL_PATH = "ledger/official_observations.jsonl"
ARCHIVE_NAME_RE = re.compile(r"[a-z0-9][a-z0-9._-]*")


def utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "thesis-witness"})
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def _commit_api(ref: str) -> tuple[str, bytes]:
    raw = _fetch(f"https://api.github.com/repos/{LEDGER_REPO}/commits/{ref}")
    sha = str(json.loads(raw).get("sha", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError(f"ledger commit API returned a non-commit value: {sha!r}")
    return sha, raw


def _archive(
    run_dir: pathlib.Path, name: str, raw: bytes, *, role: str, url: str | None
) -> dict[str, Any]:
    if not ARCHIVE_NAME_RE.fullmatch(name):
        raise ValueError(f"invalid witness archive name: {name!r}")
    compressed = gzip.compress(raw, mtime=0)
    path = run_dir / "upstream" / f"{name}.gz"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"refusing to overwrite witness archive: {path}")
    path.write_bytes(compressed)
    record: dict[str, Any] = {
        "name": name,
        "role": role,
        "archive": {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "gzipSha256": hashlib.sha256(compressed).hexdigest(),
            "gzipBytes": len(compressed),
            "contentEncoding": "gzip",
        },
    }
    if url:
        record["url"] = url
    return record


def _validate_jsonl(raw: bytes) -> dict[str, Any]:
    lines = [line for line in raw.decode("utf-8").splitlines() if line.strip()]
    seen: set[str] = set()
    for number, line in enumerate(lines, start=1):
        row = json.loads(line)
        if not isinstance(row, dict) or not row.get("source_record_id"):
            raise ValueError(f"jsonl line {number} lacks source_record_id")
        seen.add(str(row["source_record_id"]))
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "lineCount": len(lines),
        "sourceRecordIdCount": len(seen),
    }


def _seal(run_dir: pathlib.Path, manifest: dict[str, Any]) -> None:
    """Seal the witness inventory exactly like the resolver custody flow."""

    created_at = str(manifest["retrievedAt"])
    refs: list[dict[str, Any]] = []
    rooted: list[dict[str, Any]] = []
    for record in manifest["upstream"]:
        archive = record["archive"]
        path = ROOT / archive["path"]
        relative = path.resolve().relative_to(run_dir.resolve()).as_posix()
        ref = {
            "artifactType": "upstream_archive",
            "path": path.resolve().relative_to(ROOT).as_posix(),
            "sha256": archive["gzipSha256"],
            "bytes": archive["gzipBytes"],
            "createdAt": created_at,
        }
        refs.append(ref)
        rooted.append({**ref, "path": relative})
    manifest.update(
        {
            "custodyInventoryVersion": 2,
            "runMode": "ledger_witness",
            "ok": True,
            "manifestHashSemantics": (
                "canonical-json-v1; exclude artifacts where "
                "artifactType=manifest and exclude custodyRootSha256"
            ),
            "artifacts": refs,
        }
    )
    self_payload = copy.deepcopy(manifest)
    self_payload.pop("custodyRootSha256", None)
    self_bytes = canonical_bytes(self_payload)
    manifest_ref = {
        "artifactType": "manifest",
        "path": (run_dir / "manifest.json").resolve().relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(self_bytes).hexdigest(),
        "bytes": len(self_bytes),
        "createdAt": created_at,
        "hashMode": manifest["manifestHashSemantics"],
    }
    manifest["artifacts"] = [*refs, manifest_ref]
    custody = {
        "schemaVersion": "thesis_custody_root_v1",
        "custodyInventoryVersion": 2,
        "runMode": "ledger_witness",
        "hashAlgorithm": "sha256",
        "canonicalJson": (
            "UTF-16 code-unit key order; ECMAScript JSON number/string encoding"
        ),
        "artifacts": rooted,
        "manifestWithoutCustodyRoot": {
            "path": "manifest.json",
            "excludedField": "custodyRootSha256",
            "canonicalJsonSha256": canonical_sha256(manifest),
        },
    }
    (run_dir / "custody_root.json").write_text(json.dumps(custody, indent=2) + "\n")
    manifest["custodyRootSha256"] = canonical_sha256(custody)
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    verify_run(run_dir)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ledger-sha", help="witness this exact commit (default: branch head)"
    )
    parser.add_argument("--expect-line-count", type=int)
    parser.add_argument("--expect-jsonl-sha256")
    parser.add_argument(
        "--extra",
        action="append",
        default=[],
        metavar="NAME=PATH_OR_URL",
        help="additional upstream artifact to witness alongside the ledger",
    )
    parser.add_argument("--note")
    args = parser.parse_args()

    retrieved_at = utc_now()
    branch_sha, branch_commit_raw = _commit_api(args.ledger_sha or LEDGER_BRANCH)
    if args.ledger_sha and branch_sha != args.ledger_sha:
        raise SystemExit(
            f"ledger commit API resolved {branch_sha}, expected {args.ledger_sha}"
        )
    main_sha, main_commit_raw = _commit_api("main")

    jsonl_url = (
        f"https://raw.githubusercontent.com/{LEDGER_REPO}/{branch_sha}/"
        f"{LEDGER_JSONL_PATH}"
    )
    jsonl_raw = _fetch(jsonl_url)
    jsonl = _validate_jsonl(jsonl_raw)
    expected_count = args.expect_line_count
    if expected_count is not None and jsonl["lineCount"] != expected_count:
        raise SystemExit(
            f"jsonl has {jsonl['lineCount']} rows, expected {expected_count}"
        )
    if args.expect_jsonl_sha256 and jsonl["sha256"] != args.expect_jsonl_sha256:
        raise SystemExit(
            f"jsonl sha256 {jsonl['sha256']} != expected {args.expect_jsonl_sha256}"
        )

    stamp = retrieved_at.lower().replace(":", "-")
    run_dir = ROOT / "records" / retrieved_at[:10] / f"{stamp}-ledger-witness"
    run_dir.mkdir(parents=True, exist_ok=False)

    upstream = [
        _archive(
            run_dir,
            "official-observations.jsonl",
            jsonl_raw,
            role="official_observations_jsonl",
            url=jsonl_url,
        ),
        _archive(
            run_dir,
            "ledger-branch-commit.json",
            branch_commit_raw,
            role="ledger_branch_commit_api",
            url=f"https://api.github.com/repos/{LEDGER_REPO}/commits/{branch_sha}",
        ),
        _archive(
            run_dir,
            "ledger-main-commit.json",
            main_commit_raw,
            role="ledger_main_commit_api",
            url=f"https://api.github.com/repos/{LEDGER_REPO}/commits/{main_sha}",
        ),
    ]
    for extra in args.extra:
        name, _, location = extra.partition("=")
        if not location:
            raise SystemExit(f"--extra needs NAME=PATH_OR_URL, got {extra!r}")
        if location.startswith("https://"):
            raw = _fetch(location)
            upstream.append(
                _archive(run_dir, name, raw, role="extra_upstream", url=location)
            )
        else:
            raw = pathlib.Path(location).read_bytes()
            upstream.append(
                _archive(run_dir, name, raw, role="extra_upstream", url=None)
            )

    manifest: dict[str, Any] = {
        "schemaVersion": "thesis_ledger_witness_run_v1",
        "retrievedAt": retrieved_at,
        "ledgerRepo": LEDGER_REPO,
        "ledgerBranch": LEDGER_BRANCH,
        "ledgerBranchSha": branch_sha,
        "ledgerMainSha": main_sha,
        "jsonl": jsonl,
        "upstream": upstream,
    }
    if args.note:
        manifest["note"] = args.note
    _seal(run_dir, manifest)
    print(run_dir / "manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
