#!/usr/bin/env python3
"""Propose brand-new forecast series for the docket.

The roll loop deepens existing series; this widens the docket. A codex call
proposes candidate series from official statistical release calendars, hard
validation filters the output (enums, duplicates, release window, period
shapes), and survivors are emitted as a normal batch targets file. The
analyst pipeline then researches each candidate independently — a proposal
here is a lead, not a published cell.

New series do NOT enter the roll registry from this path. Adoption happens
in scripts/adopt_proven_series.py only after a series' first cell resolves
and scores — seed, prove, then roll.

Usage:
    python3 scripts/prospect_series.py [--count 3] [--focus "UK, health"]
        [--out targets.json] [--dry-run]
"""

from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import pathlib
import re
import subprocess
import sys
import urllib.parse

from thesis_log_client import load_thesis_log

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "scripts" / "docket_series.json"
LOG_URL = "https://app.thesisinstitute.org/log.json"
CODEX = "codex"

COUNTRIES = {"US", "UK", "CA", "AU", "EA", "JP", "BE"}
UNITS = {
    "count",
    "percent",
    "gbp_billions",
    "usd",
    "usd_billions",
    "usd_monthly",
    "thousands",
    "millions",
    "per_1000_live_births",
    "ratio",
    "minutes",
    "percent_growth",
    "index_points",
}
PERIOD_RE = re.compile(r"\d{4}-\d{2}|\d{4}-Q\d|week_\d{4}-\d{2}-\d{2}")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SERIES_RE = re.compile(r"^[a-z0-9_]+(\.[a-z0-9_]+)+$")


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
    return json.loads(text[start : end + 1])


GENERIC_TOKENS = (
    {
        "rate",
        "annual",
        "monthly",
        "weekly",
        "total",
        "index",
        "yoy",
        "mom",
        "us",
        "uk",
        "euro",
        "area",
        "japan",
        "canada",
        "australia",
        "belgium",
        "week",
        "prelim",
        "flash",
        "sa",
    }
    | set(m.lower() for m in calendar.month_name if m)
    | {str(y) for y in range(2024, 2032)}
)


def near_duplicate(slug: str, existing: set[str]) -> str | None:
    """An existing slug describing the same quantity in different words."""
    tokens = {t for t in slug.split("-") if t not in GENERIC_TOKENS and not t.isdigit()}
    if not tokens:
        return None
    for other in existing:
        other_tokens = {
            t for t in other.split("-") if t not in GENERIC_TOKENS and not t.isdigit()
        }
        if len(tokens & other_tokens) >= 2 or (
            len(tokens & other_tokens) == 1 and tokens <= other_tokens
        ):
            return other
    return None


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
    horizon = today + dt.timedelta(days=75)
    targets = []
    for p in proposals:
        problems = []
        if not SERIES_RE.fullmatch(p.get("series", "")):
            problems.append("bad series id")
        if p.get("series") in registry_series:
            problems.append("series already in registry")
        if not PERIOD_RE.fullmatch(p.get("period", "")):
            problems.append("bad period")
        if not SLUG_RE.fullmatch(p.get("catalogSlug", "")):
            problems.append("bad slug")
        if p.get("catalogSlug") in existing_slugs:
            problems.append("slug exists")
        if p.get("country") not in COUNTRIES:
            problems.append("bad country")
        if p.get("targetUnit") not in UNITS:
            problems.append("bad unit")
        overlap = near_duplicate(p.get("catalogSlug", ""), existing_slugs)
        if overlap:
            problems.append(f"same quantity as existing {overlap}")
        try:
            release = dt.date.fromisoformat(p.get("expectedReleaseDate", ""))
            if not (today < release <= horizon):
                problems.append("release outside (today, +75d]")
        except ValueError:
            problems.append("bad release date")
        try:
            source_host = urllib.parse.urlparse(
                p.get("resolutionSourceUrl", "")
            ).hostname
        except ValueError:
            source_host = None
        if not source_host:
            problems.append("bad resolution source URL")
        for key in ("sourceSeriesId", "sourceField", "sourceTable"):
            if not str(p.get(key) or "").strip():
                problems.append(f"missing {key}")
        if problems:
            print(f"  reject {p.get('catalogSlug', '?')}: {'; '.join(problems)}")
            continue
        target = {
            "series": p["series"],
            "period": p["period"],
            "catalogSlug": p["catalogSlug"],
            "country": p["country"],
            "targetUnit": p["targetUnit"],
            "expectedReleaseDate": p["expectedReleaseDate"],
            "resolutionSourceUrl": p["resolutionSourceUrl"],
            "sourceSeriesId": p["sourceSeriesId"],
            "sourceField": p["sourceField"],
            "sourceTable": p["sourceTable"],
            "transform": p.get("transform")
            or {
                "operation": "identity",
                "factor": 1,
            },
        }
        targets.append(target)
        rationale = str(p.get("rationale", ""))[:90]
        print(
            f"  prospect {p['catalogSlug']} ({p['series']} {p['period']}) — {rationale}"
        )

    print(f"{len(targets)} of {len(proposals)} proposals accepted")
    if args.out and not args.dry_run and targets:
        pathlib.Path(args.out).write_text(
            json.dumps({"targets": targets}, indent=1) + "\n"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
