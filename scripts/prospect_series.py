#!/usr/bin/env python3
"""Propose brand-new forecast series for the docket.

The roll loop deepens existing series; this widens the docket. A codex call
proposes candidate series from official statistical release calendars, hard
validation filters the output (enums, duplicates, release window, period
shapes), and survivors are emitted in the versioned prospect-proposal
envelope. The privileged registrar independently replays validation before
the analyst pipeline researches a candidate — a proposal here is a lead, not
a published cell.

New series do NOT enter the roll registry from this path. Adoption happens
in scripts/adopt_proven_series.py only after a series' first cell resolves
and scores — seed, prove, then roll.

Usage:
    python3 scripts/prospect_series.py [--count 3] [--focus "UK, health"]
        [--out targets.json] [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys

from prospect_targets import (
    ALLOWED_COUNTRIES,
    ALLOWED_UNITS,
    validate_codex_raw_proposal,
    write_proposal_envelope,
)
from thesis_log_client import load_thesis_log

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "scripts" / "docket_series.json"
LOG_URL = "https://app.thesisinstitute.org/log.json"
CODEX = "codex"

COUNTRIES = ALLOWED_COUNTRIES
UNITS = ALLOWED_UNITS


def prompt(
    registry_series: list[str], sample_slugs: list[str], count: int, focus: str | None
) -> str:
    focus_line = f"Focus areas requested: {focus}.\n" if focus else ""
    return f"""# Thesis docket prospecting

Propose {count} NEW forecast target series for an open forecasting docket of
official government statistics. Search the web for official statistical
release calendars to verify each proposal.

Hard requirements for every proposal:
- Published by an official statistical agency or central bank
  (BLS, BEA, Census, DOL, FNS, SSA, CMS, ONS, Eurostat, ECB, Statistics
  Canada, ABS, Statbel, NBB, Statistics Bureau of Japan, and peers).
- Recurring cadence (weekly, monthly, or quarterly) with a published
  release calendar; the NEXT release must land within 75 days.
- Resolves mechanically from a first print: one named table/field, one
  named variant (SA vs NSA, gross vs smoothed), no judgment calls.
- Not already covered — including under a DIFFERENT slug wording. The
  full list of existing catalog slugs follows; do not propose the same
  quantity for any period, and match an official series' actual period
  structure (e.g. ONS LFS unemployment is a rolling three-month quarter,
  not a single month):
  {", ".join(sample_slugs)}.
  Existing registry series: {", ".join(registry_series)}.
- country must be one of US, UK, CA, AU, EA, JP, BE. Prefer filling
  coverage gaps (UK has none in the registry today).
{focus_line}
Output STRICT JSON only — an array of exactly {count} objects, no prose:
[{{
  "series": "agency.family.measure (lowercase dotted, e.g. ons.cpi.cpih_yoy)",
  "period": "the next unreleased period: YYYY-MM, YYYY-Q#, or week_YYYY-MM-DD",
  "catalogSlug": "kebab-case, period-specific, e.g. uk-cpih-annual-rate-august-2026",
  "country": "US|UK|CA|AU|EA|JP|BE",
  "targetUnit": "one of: {", ".join(sorted(UNITS))}",
  "expectedReleaseDate": "YYYY-MM-DD",
  "resolutionSourceUrl": "the agency's release/table page",
  "sourceSeriesId": "official series or dataset identifier",
  "sourceField": "exact value field/row identifier",
  "sourceTable": "exact official table, release, or dataset",
  "transform": {{"operation": "identity or multiply", "factor": 1}},
  "rationale": "one sentence on why this series matters"
}}]
"""


def run_codex(text: str) -> str:
    completed = subprocess.run(
        [
            CODEX,
            "--search",
            "exec",
            "--ignore-user-config",
            "-m",
            "gpt-5.5",
            "-c",
            'service_tier="fast"',
            "--sandbox",
            "read-only",
            "-",
        ],
        input=text,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"codex failed: {completed.stderr[-400:]}")
    return completed.stdout


def extract_json(text: str) -> list[dict]:
    start = text.find("[")
    end = text.rfind("]")
    if start < 0 or end <= start:
        raise ValueError("no JSON array in codex output")
    payload = json.loads(text[start : end + 1])
    if not isinstance(payload, list):
        raise ValueError("codex output is not a JSON array")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--focus")
    parser.add_argument("--out")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    registry = json.loads(REGISTRY.read_text())["series"]
    registry_series = sorted({entry["series"] for entry in registry})
    log = load_thesis_log(LOG_URL)
    existing_slugs = {link["forecastSlug"] for link in log["resolutionLinks"]}
    sample_slugs = sorted(existing_slugs)

    raw = run_codex(prompt(registry_series, sample_slugs, args.count, args.focus))
    proposals = extract_json(raw)

    today = dt.date.today()
    targets = []
    for p in proposals:
        target, problems = validate_codex_raw_proposal(
            p,
            today=today,
            existing_slugs=existing_slugs,
            registry_series=set(registry_series),
        )
        if problems:
            slug = p.get("catalogSlug", "?") if isinstance(p, dict) else "?"
            print(f"  reject {slug}: {'; '.join(problems)}")
            continue
        assert target is not None
        targets.append(target)
        rationale = str(p.get("rationale", ""))[:90] if isinstance(p, dict) else ""
        print(
            f"  prospect {target['catalogSlug']} "
            f"({target['series']} {target['period']}) — {rationale}"
        )

    print(f"{len(targets)} of {len(proposals)} proposals accepted")
    if args.out and not args.dry_run:
        write_proposal_envelope(pathlib.Path(args.out), "codex", targets)
    return 0


if __name__ == "__main__":
    sys.exit(main())
