#!/usr/bin/env python3
"""Resolve pending forecast cells whose official numbers have published.

Adapter-based: each adapter claims a family of targetFactRefs from the live
catalog's resolutionLinks, checks whether the official first print exists
yet, and emits a PolicyEngine-Ledger fact row (the JSONL schema the site's
build fetches and joins on source_record_id == targetFactRef). Appending a
row is what resolves a cell: the next site build scores it.

First adapters: DOL UI weekly claims (initial + continued, seasonally
adjusted), read from FRED's ICSA/CCSA series — the advance vintage named by
the cells' own resolver rules.

Usage:
    python3 scripts/resolve_pending.py [--dry-run]
        [--ledger-repo PolicyEngine/arch-data]
        [--ledger-branch codex/thesis-ledger-facts]
        [--ledger-path ledger/official_observations.jsonl]

Requires `gh` auth with write access to the ledger repo unless --dry-run.
Idempotent: refs already present in the ledger are skipped.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import re
import subprocess
import sys
import urllib.request

from thesis_log_client import load_thesis_log

LOG_URL = "https://app.thesisinstitute.org/log.json"
# ALFRED with a vintage date pins the ADVANCE print (what the resolver rules
# name); plain FRED would silently hand back revised values on backfills.
FRED_CSV = (
    "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
    "?id={series}&vintage_date={vintage}"
)


def fred_advance_value(series_id: str, week: str, vintage: str) -> float | None:
    """The series value for `week` as printed on `vintage` (advance print)."""
    url = FRED_CSV.format(series=series_id, vintage=vintage)
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            text = r.read().decode()
    except urllib.error.HTTPError:
        return None  # vintage predates the release -> not yet published
    for row in csv.DictReader(io.StringIO(text)):
        date = row.get("observation_date") or row.get("DATE")
        value = row.get(f"{series_id}_{vintage.replace('-', '')}") or row.get(series_id)
        if date == week and value not in (None, "", "."):
            return float(value)
    return None


def claims_fact(ref: str, week: str, raw: float, kind: str) -> dict:
    """Build a ledger fact row for a weekly claims first print."""
    if kind == "initial":
        value, unit = round(raw / 1_000, 1), "thousands"
        concept = "us.dol.initial_claims.sa"
        fred_id, label = "ICSA", "US initial claims (SA, advance)"
    else:
        value, unit = round(raw / 1_000_000, 3), "millions"
        concept = "dol.eta.continued_claims.sa"
        fred_id, label = "CCSA", "US insured unemployment (SA, advance)"
    # Initial claims for week W print the following Thursday (W+5); the
    # advance continued-claims figure lags one release behind (W+12).
    lag = 5 if kind == "initial" else 12
    release_day = dt.date.fromisoformat(week) + dt.timedelta(days=lag)
    source_url = FRED_CSV.format(series=fred_id, vintage=release_day.isoformat())
    return {
        "source_record_id": ref,
        "label": f"{label}, week ending {week}",
        "value": value,
        "observed_at": release_day.isoformat(),
        "period": {"type": "week_ending", "value": week},
        "domain": "labor",
        "geography": {
            "level": "country",
            "id": "0100000US",
            "vintage": "current",
            "name": "United States",
        },
        "entity": {"name": "person", "role": "ui_claimant"},
        "measure": {
            "concept": concept,
            "unit": unit,
            "source_concept": fred_id,
            "concept_relation": "source_label",
            "concept_authority": "dol_eta",
            "concept_evidence_url": source_url,
            "concept_evidence_notes": (
                f"DOL ETA UI Weekly Claims news release, advance seasonally "
                f"adjusted figure for the week ending {week}, read from FRED "
                f"{fred_id} (advance vintage) as the cell's resolver names."
            ),
        },
        "aggregation": {"method": "level"},
        "filters": {},
        "source": {
            "source_name": "dol_eta",
            "source_table": "Unemployment Insurance Weekly Claims (advance)",
            "source_file": "fredgraph.csv",
            "url": source_url,
            "vintage": "advance",
            "extracted_at": dt.date.today().isoformat(),
            "extraction_method": (
                "Automated first-print capture via FRED series "
                f"{fred_id} by scripts/resolve_pending.py"
            ),
        },
        "source_row_keys": [week],
        "source_cell_keys": [fred_id],
    }


def pending_claims_refs(log: dict) -> list[tuple[str, str, str]]:
    """(ref, week, kind) for pending claims cells."""
    out = []
    for link in log["resolutionLinks"]:
        if link.get("status") != "pending":
            continue
        ref = link.get("targetFactRef")
        if not ref:
            continue
        m = re.match(r"us\.dol\.initial_claims\.sa\.week_(\d{4}-\d{2}-\d{2})$", ref)
        if m:
            out.append((ref, m.group(1), "initial"))
            continue
        m = re.match(
            r"dol\.eta\.continued_claims\.sa\.week_(\d{4}-\d{2}-\d{2})(\.first_print)?$",
            ref,
        )
        if m:
            out.append((ref, m.group(1), "continued"))
    return out


def ledger_state(repo: str, branch: str, path: str) -> tuple[str, str]:
    """Return (content, blob_sha) of the ledger file."""
    raw = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}?ref={branch}",
         "--jq", "{sha: .sha, content: .content}"],
        capture_output=True, text=True, check=True,
    ).stdout
    payload = json.loads(raw)
    import base64
    return base64.b64decode(payload["content"]).decode(), payload["sha"]


def push_ledger(repo: str, branch: str, path: str, content: str, sha: str, added: int) -> None:
    import base64
    body = {
        "message": f"Record {added} first-print observation(s) via resolve_pending.py",
        "content": base64.b64encode(content.encode()).decode(),
        "sha": sha,
        "branch": branch,
    }
    completed = subprocess.run(
        ["gh", "api", "-X", "PUT", f"repos/{repo}/contents/{path}", "--input", "-"],
        input=json.dumps(body), capture_output=True, text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"ledger push failed: {completed.stderr.strip()[:500]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--ledger-repo", default="PolicyEngine/ledger")
    parser.add_argument("--ledger-branch", default="codex/thesis-ledger-facts")
    parser.add_argument("--ledger-path", default="ledger/official_observations.jsonl")
    args = parser.parse_args()

    log = load_thesis_log(LOG_URL)
    todo = pending_claims_refs(log)
    if not todo:
        print("no pending claims cells")
        return 0

    content, sha = ledger_state(args.ledger_repo, args.ledger_branch, args.ledger_path)
    existing_ids = {
        json.loads(line)["source_record_id"]
        for line in content.splitlines() if line.strip()
    }

    new_rows = []
    today = dt.date.today()
    for ref, week, kind in todo:
        if ref in existing_ids:
            print(f"  already recorded: {ref}")
            continue
        lag = 5 if kind == "initial" else 12
        release_day = dt.date.fromisoformat(week) + dt.timedelta(days=lag)
        if release_day > today:
            print(f"  release {release_day} not reached: {ref}")
            continue
        series_id = "ICSA" if kind == "initial" else "CCSA"
        raw = fred_advance_value(series_id, week, release_day.isoformat())
        if raw is None:
            print(f"  not yet published: {ref}")
            continue
        row = claims_fact(ref, week, raw, kind)
        new_rows.append(row)
        print(f"  resolve {ref} -> {row['value']} {row['measure']['unit']}")

    if not new_rows:
        print("nothing new to record")
        return 0
    if args.dry_run:
        print(f"dry-run: would append {len(new_rows)} row(s)")
        for row in new_rows:
            print(json.dumps(row)[:200])
        return 0

    updated = content.rstrip("\n") + "\n" + "\n".join(
        json.dumps(row, separators=(",", ":")) for row in new_rows
    ) + "\n"
    push_ledger(args.ledger_repo, args.ledger_branch, args.ledger_path,
                updated, sha, len(new_rows))
    print(f"appended {len(new_rows)} observation(s) to "
          f"{args.ledger_repo}@{args.ledger_branch}:{args.ledger_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
