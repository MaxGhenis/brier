#!/usr/bin/env python3
"""Pin the fact ledger to one immutable commit and index row acceptance.

The site build must consume the thesis-facts observation file at an exact
commit SHA whose bytes are committed here as a pin, never at a branch name a
writer can move. Row eligibility at a cutoff must mean "the ledger contained
this row then" — acceptance into the append-only file, derived from the
branch's own commit history — never the publisher's ``observed_at``, which a
backfill can predate (review finding N5).

Two committed outputs:

- ``site/src/data/ledger-pin.json`` — the exact state the site build fetches
  and verifies byte-for-byte.
- ``records/ledger/availability.json`` (+ a generated TypeScript mirror) —
  per-row ``acceptedSequence``/``acceptedAtUtc``/``acceptedCommit`` with a
  custody flag; rows whose content changed after introduction are marked
  ``rewritten_in_place``, never silently adopted. The legacy quarantine
  boundary freezes the row count at first indexing: earlier rows predate
  contract binding and are flagged wherever they grade forecasts.

Refreshes verify every intermediate commit extends the previous version
line-for-line. A rewritten or truncated upstream state refuses to advance the
pin; adopting one requires deliberate ``--rebuild-from-history``, which
re-derives custody flags rather than blessing the rewrite.

Usage:
    python3 scripts/pin_ledger.py                       # incremental refresh
    python3 scripts/pin_ledger.py --rebuild-from-history --ledger-git PATH
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.request
from typing import Any

from canonical_json import canonical_bytes, canonical_sha256

ROOT = pathlib.Path(__file__).resolve().parents[1]
PIN_PATH = ROOT / "site" / "src" / "data" / "ledger-pin.json"
AVAILABILITY_PATH = ROOT / "records" / "ledger" / "availability.json"
GENERATED_PATH = ROOT / "site" / "src" / "data" / "ledger-availability.generated.ts"
LEDGER_REPO = "PolicyEngine/ledger"
LEDGER_BRANCH = "codex/thesis-ledger-facts"
LEDGER_JSONL_PATH = "ledger/official_observations.jsonl"
PIN_SCHEMA = "thesis_ledger_pin_v1"
AVAILABILITY_SCHEMA = "thesis_ledger_availability_v1"


class PinError(ValueError):
    """The upstream ledger state cannot be adopted."""


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _utc_instant(value: str) -> str:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise PinError(f"commit timestamp lacks a timezone: {value!r}")
    return (
        parsed.astimezone(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "thesis-pin"})
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def _api(path: str) -> Any:
    return json.loads(_fetch(f"https://api.github.com/repos/{LEDGER_REPO}/{path}"))


def _jsonl_at(sha: str) -> bytes:
    return _fetch(
        f"https://raw.githubusercontent.com/{LEDGER_REPO}/{sha}/{LEDGER_JSONL_PATH}"
    )


def _lines(raw: bytes) -> list[str]:
    return [line for line in raw.decode("utf-8").split("\n") if line.strip()]


def _source_record_id(line: str, index: int) -> str:
    row = json.loads(line)
    record_id = row.get("source_record_id") if isinstance(row, dict) else None
    if not record_id:
        raise PinError(f"ledger line {index + 1} lacks source_record_id")
    return str(record_id)


def _require_extension(
    previous: list[str], current: list[str], *, label: str
) -> None:
    if len(current) < len(previous):
        raise PinError(f"{label} truncates the ledger: "
                       f"{len(previous)} -> {len(current)} rows")
    for index, line in enumerate(previous):
        if current[index] != line:
            raise PinError(
                f"{label} rewrites ledger line {index + 1} "
                f"({_source_record_id(line, index)}); refusing to advance the pin"
            )


def _row(
    index: int, line: str, accepted_at: str, commit: str, custody: str
) -> dict[str, Any]:
    return {
        "sourceRecordId": _source_record_id(line, index),
        "acceptedSequence": index,
        "acceptedAtUtc": accepted_at,
        "acceptedCommit": commit,
        "lineSha256": sha256_hex(line.encode("utf-8")),
        "custody": custody,
    }


def load_pin() -> dict[str, Any] | None:
    if not PIN_PATH.exists():
        return None
    pin = json.loads(PIN_PATH.read_text())
    if pin.get("schemaVersion") != PIN_SCHEMA:
        raise PinError(f"unsupported pin schema: {pin.get('schemaVersion')!r}")
    return pin


def load_availability() -> dict[str, Any] | None:
    if not AVAILABILITY_PATH.exists():
        return None
    snapshot = json.loads(AVAILABILITY_PATH.read_text())
    if snapshot.get("schemaVersion") != AVAILABILITY_SCHEMA:
        raise PinError(
            f"unsupported availability schema: {snapshot.get('schemaVersion')!r}"
        )
    if AVAILABILITY_PATH.read_bytes() != canonical_bytes(snapshot) + b"\n":
        raise PinError("availability snapshot is not canonical JSON")
    return snapshot


def _write_outputs(
    *,
    sha: str,
    raw: bytes,
    rows: list[dict[str, Any]],
    quarantine_count: int,
    anomalies: list[dict[str, Any]],
    pinned_at: str,
) -> None:
    lines = _lines(raw)
    if len(rows) != len(lines):
        raise PinError(f"availability covers {len(rows)} of {len(lines)} rows")
    for index, (row, line) in enumerate(zip(rows, lines)):
        if row["acceptedSequence"] != index:
            raise PinError(f"availability sequence gap at {index}")
        if row["lineSha256"] != sha256_hex(line.encode("utf-8")):
            raise PinError(f"availability hash mismatch at line {index + 1}")
    pin = {
        "schemaVersion": PIN_SCHEMA,
        "repo": LEDGER_REPO,
        "branch": LEDGER_BRANCH,
        "sha": sha,
        "jsonlSha256": sha256_hex(raw),
        "jsonlBytes": len(raw),
        "lineCount": len(lines),
        "pinnedAtUtc": pinned_at,
    }
    availability = {
        "schemaVersion": AVAILABILITY_SCHEMA,
        "repo": LEDGER_REPO,
        "branch": LEDGER_BRANCH,
        "headSha": sha,
        "jsonlSha256": pin["jsonlSha256"],
        "legacyQuarantineLineCount": quarantine_count,
        "historyAnomalies": anomalies,
        "rows": rows,
    }
    PIN_PATH.write_text(json.dumps(pin, indent=2) + "\n")
    AVAILABILITY_PATH.parent.mkdir(parents=True, exist_ok=True)
    AVAILABILITY_PATH.write_bytes(canonical_bytes(availability) + b"\n")
    body = ",\n".join(
        "  " + json.dumps(row, separators=(",", ":")) for row in rows
    )
    GENERATED_PATH.write_text(
        "// Generated by scripts/pin_ledger.py from the thesis-facts branch\n"
        "// history. Do not edit: acceptance times witness when each row\n"
        "// entered the append-only ledger, independent of publisher dates.\n"
        "export interface LedgerAvailabilityRow {\n"
        "  sourceRecordId: string;\n"
        "  acceptedSequence: number;\n"
        "  acceptedAtUtc: string;\n"
        "  acceptedCommit: string;\n"
        "  lineSha256: string;\n"
        '  custody: "append_derived" | "rewritten_in_place";\n'
        "}\n\n"
        f"export const LEDGER_AVAILABILITY_HEAD_SHA = {json.dumps(sha)};\n"
        "export const LEDGER_LEGACY_QUARANTINE_LINE_COUNT = "
        f"{quarantine_count};\n\n"
        "export const LEDGER_AVAILABILITY: readonly LedgerAvailabilityRow[] = [\n"
        f"{body}\n"
        "];\n"
    )
    availability_hash = canonical_sha256(availability)
    print(f"pinned {sha} ({len(lines)} rows, jsonl {pin['jsonlSha256'][:16]}…)")
    print(f"availability {availability_hash[:16]}… quarantine<{quarantine_count}")


def _git(ledger_git: pathlib.Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ledger_git, text=True
    ).strip()


def rebuild_from_history(ledger_git: pathlib.Path, head: str | None) -> None:
    """Derive per-row acceptance from the branch's full commit history."""

    ref = head or f"origin/{LEDGER_BRANCH}"
    head_sha = _git(ledger_git, "rev-parse", f"{ref}^{{commit}}")
    commit_list = _git(
        ledger_git,
        "log",
        "--reverse",
        "--format=%H %cI",
        head_sha,
        "--",
        LEDGER_JSONL_PATH,
    ).splitlines()
    if not commit_list:
        raise PinError(f"no history for {LEDGER_JSONL_PATH} at {head_sha}")

    previous_lines: list[str] = []
    accepted: list[tuple[str, str]] = []  # per index: (acceptedAtUtc, commit)
    introduced: list[str] = []  # per index: first content seen
    rewritten: set[int] = set()
    anomalies: list[dict[str, Any]] = []
    for entry in commit_list:
        commit, _, stamp = entry.partition(" ")
        accepted_at = _utc_instant(stamp)
        raw = subprocess.check_output(
            ["git", "show", f"{commit}:{LEDGER_JSONL_PATH}"], cwd=ledger_git
        )
        lines = _lines(raw)
        if len(lines) < len(previous_lines):
            anomalies.append(
                {
                    "kind": "truncation",
                    "commit": commit,
                    "fromRows": len(previous_lines),
                    "toRows": len(lines),
                }
            )
            del accepted[len(lines):]
            del introduced[len(lines):]
            rewritten = {index for index in rewritten if index < len(lines)}
        for index, line in enumerate(lines):
            if index >= len(accepted):
                accepted.append((accepted_at, commit))
                introduced.append(line)
            elif index < len(previous_lines) and previous_lines[index] != line:
                rewritten.add(index)
                accepted[index] = (accepted_at, commit)
                anomalies.append(
                    {
                        "kind": "in_place_rewrite",
                        "commit": commit,
                        "line": index + 1,
                        "sourceRecordId": _source_record_id(line, index),
                    }
                )
        previous_lines = lines

    raw = subprocess.check_output(
        ["git", "show", f"{head_sha}:{LEDGER_JSONL_PATH}"], cwd=ledger_git
    )
    lines = _lines(raw)
    rows = [
        _row(
            index,
            line,
            accepted[index][0],
            accepted[index][1],
            "rewritten_in_place" if index in rewritten else "append_derived",
        )
        for index, line in enumerate(lines)
    ]
    existing = load_availability()
    quarantine_count = (
        int(existing["legacyQuarantineLineCount"]) if existing else len(lines)
    )
    _write_outputs(
        sha=head_sha,
        raw=raw,
        rows=rows,
        quarantine_count=quarantine_count,
        anomalies=anomalies,
        pinned_at=utc_now(),
    )


def refresh() -> None:
    """Advance the pin to the branch head, verifying append-only extension."""

    pin = load_pin()
    availability = load_availability()
    if pin is None or availability is None:
        raise PinError(
            "no committed pin/availability; run --rebuild-from-history first"
        )
    head = _api(f"commits/{LEDGER_BRANCH}")
    head_sha = str(head.get("sha", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", head_sha):
        raise PinError(f"ledger API returned a non-commit value: {head_sha!r}")
    if head_sha == pin["sha"]:
        print(f"pin already at {head_sha}")
        return

    old_raw = _jsonl_at(pin["sha"])
    if sha256_hex(old_raw) != pin["jsonlSha256"]:
        raise PinError(
            "pinned bytes no longer match the pin — upstream history changed"
        )
    old_lines = _lines(old_raw)

    # Every intermediate commit must extend its parent line-for-line, so a
    # rewrite-then-restore between refreshes cannot hide.
    compare = _api(f"compare/{pin['sha']}...{head_sha}")
    commits = compare.get("commits")
    if not isinstance(commits, list) or not commits:
        raise PinError(f"cannot enumerate commits {pin['sha']}..{head_sha}")

    rows = list(availability["rows"])
    previous_lines = old_lines
    for commit in commits:
        commit_sha = str(commit["sha"])
        raw = _jsonl_at(commit_sha)
        lines = _lines(raw)
        if lines == previous_lines:
            previous_lines = lines
            continue
        _require_extension(previous_lines, lines, label=f"commit {commit_sha[:12]}")
        accepted_at = _utc_instant(
            str(commit["commit"]["committer"]["date"])
        )
        for index in range(len(previous_lines), len(lines)):
            rows.append(
                _row(index, lines[index], accepted_at, commit_sha, "append_derived")
            )
        previous_lines = lines

    head_raw = _jsonl_at(head_sha)
    if _lines(head_raw) != previous_lines:
        raise PinError("branch head bytes disagree with its own commit history")
    _write_outputs(
        sha=head_sha,
        raw=head_raw,
        rows=rows,
        quarantine_count=int(availability["legacyQuarantineLineCount"]),
        anomalies=list(availability["historyAnomalies"]),
        pinned_at=utc_now(),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild-from-history", action="store_true")
    parser.add_argument(
        "--ledger-git",
        type=pathlib.Path,
        help="local clone of PolicyEngine/ledger with the thesis-facts branch",
    )
    parser.add_argument(
        "--head", help="pin this commit instead of the branch head (rebuild only)"
    )
    args = parser.parse_args()
    try:
        if args.rebuild_from_history:
            if not args.ledger_git:
                raise PinError("--rebuild-from-history requires --ledger-git")
            rebuild_from_history(args.ledger_git, args.head)
        else:
            refresh()
    except (PinError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"ledger pin failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
