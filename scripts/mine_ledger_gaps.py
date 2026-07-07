#!/usr/bin/env python3
"""Mine the fact ledger for families we resolve but do not forecast.

Every fact in the ledger is a quantity that has already been resolved from
an official source with recorded provenance — the strongest possible
evidence that a forecast cell on its NEXT period is resolvable. This script
groups ledger facts into families (source_record_id minus its period
token), skips families the roll registry already covers or that have a
pending cell, and emits next-period batch targets for the rest.

Unlike the codex prospector, no fuzzy near-duplicate guard applies here:
coverage is checked against exact fact refs, because the families are
provenance-proven distinct quantities.

Usage:
    python3 scripts/mine_ledger_gaps.py [--max-targets 6] [--out targets.json]
        [--dry-run] [--include-annual]
"""

from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "scripts" / "docket_series.json"
LOG_URL = "https://app.thesisinstitute.org/log.json"
LEDGER_URL = (
    "https://github.com/PolicyEngine/ledger/raw/refs/heads/"
    "codex/thesis-ledger-facts/ledger/official_observations.jsonl"
)

MONTHS = [m.lower() for m in calendar.month_abbr]  # "", jan, feb, ...
COUNTRY_BY_NAME = {
    "united states": "US", "united kingdom": "UK", "canada": "CA",
    "australia": "AU", "euro area": "EA", "japan": "JP", "belgium": "BE",
}


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read().decode()


def period_token(period: dict) -> str | None:
    """The period token as it appears inside a source_record_id."""
    ptype, value = period.get("type"), period.get("value")
    if ptype == "fiscal_year":
        return f"fy{value}"
    if ptype == "month":
        # e.g. {"type": "month", "value": "2026-05"} -> may_2026
        m = re.fullmatch(r"(\d{4})-(\d{2})", str(value))
        if m:
            return f"{MONTHS[int(m.group(2))]}_{m.group(1)}"
        return None
    if ptype == "week_ending":
        return f"week_{value}"
    return None


def step(period: dict) -> tuple[dict, str] | None:
    """Next period (structured) and its id token."""
    ptype, value = period.get("type"), period.get("value")
    if ptype == "fiscal_year":
        nxt = {"type": "fiscal_year", "value": int(value) + 1}
        return nxt, f"fy{nxt['value']}"
    if ptype == "month":
        m = re.fullmatch(r"(\d{4})-(\d{2})", str(value))
        if not m:
            return None
        year, month = int(m.group(1)), int(m.group(2)) + 1
        if month == 13:
            year, month = year + 1, 1
        nxt = {"type": "month", "value": f"{year}-{month:02d}"}
        return nxt, f"{MONTHS[month]}_{year}"
    if ptype == "week_ending":
        day = dt.date.fromisoformat(str(value)) + dt.timedelta(days=7)
        nxt = {"type": "week_ending", "value": day.isoformat()}
        return nxt, f"week_{day.isoformat()}"
    return None


def batch_period(period: dict) -> str:
    """run_thesis_batch-style period string."""
    ptype, value = period["type"], period["value"]
    if ptype == "fiscal_year":
        return f"fy{value}"
    if ptype == "week_ending":
        return f"week_{value}"
    return str(value)  # month: YYYY-MM


def slug_for(family_series: str, period: dict) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", family_series.lower()).strip("-")
    ptype, value = period["type"], period["value"]
    if ptype == "fiscal_year":
        suffix = f"fy{value}"
    elif ptype == "month":
        year, month = str(value)[:4], int(str(value)[5:7])
        suffix = f"{calendar.month_name[month].lower()}-{year}"
    else:
        suffix = str(value)
    return f"{base}-{suffix}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-targets", type=int, default=6)
    parser.add_argument("--out")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--include-annual", action="store_true")
    args = parser.parse_args()

    rows = [json.loads(l) for l in fetch(LEDGER_URL).splitlines() if l.strip()]
    log = json.loads(fetch(LOG_URL))
    registry_series = {e["series"] for e in json.loads(REGISTRY.read_text())["series"]}
    existing_slugs = {l["forecastSlug"] for l in log["resolutionLinks"]}
    all_refs = {l.get("targetFactRef", "") for l in log["resolutionLinks"]}
    pending_refs = {
        l.get("targetFactRef", "")
        for l in log["resolutionLinks"] if l.get("status") == "pending"
    }

    # Group ledger facts into families keyed by id-with-period-token-removed.
    families: dict[str, dict] = {}
    for row in rows:
        rid = row["source_record_id"]
        token = period_token(row.get("period") or {})
        if not token or f".{token}" not in rid:
            continue
        family = rid.replace(f".{token}", ".{P}")
        entry = families.setdefault(family, {"latest": None, "row": None})
        current = entry["latest"]
        value = str((row.get("period") or {}).get("value"))
        if current is None or value > str((entry["row"]["period"] or {}).get("value")):
            entry["latest"] = row["period"]
            entry["row"] = row

    candidates = []
    for family, entry in sorted(families.items()):
        period = entry["latest"]
        if period["type"] == "fiscal_year" and not args.include_annual:
            continue
        # The forecast series id: the family without variant suffixes.
        series = family.replace(".{P}", "")
        series = re.sub(
            r"\.(first_print|original_submission|official_release|advance|final_first_print)$",
            "", series)
        if series in registry_series:
            continue  # the roll loop owns it
        if any(ref.startswith(series + ".") and ref in pending_refs for ref in pending_refs):
            continue  # a future cell already exists
        stepped = step(period)
        if not stepped:
            continue
        nxt, token = stepped
        # Clamp stale monthlies forward: the ledger may lag by months (CMS
        # PI publishes ~4 months behind), and stepping into an
        # already-published period is leakage bait. Last month is the
        # earliest period that can still plausibly be pre-registered.
        if nxt["type"] == "month":
            today = dt.date.today()
            floor_year, floor_month = (today.year, today.month - 1) if today.month > 1 else (today.year - 1, 12)
            floor_val = f"{floor_year}-{floor_month:02d}"
            while str(nxt["value"]) < floor_val:
                nxt, token = step(nxt)
        next_ref = family.replace("{P}", token)
        if next_ref in all_refs:
            continue  # already forecast (any status)
        slug = slug_for(series, nxt)
        if slug in existing_slugs:
            continue
        unit = ((entry["row"].get("measure") or {}).get("unit"))
        geo = ((entry["row"].get("geography") or {}).get("name") or "").lower()
        country = COUNTRY_BY_NAME.get(geo, "US")
        target = {
            "series": series,
            "period": batch_period(nxt),
            "catalogSlug": slug,
            "country": country,
        }
        if unit:
            target["targetUnit"] = unit
        candidates.append(target)
        print(f"  gap {slug} ({series} -> {batch_period(nxt)}, unit {unit})")

    targets = candidates[: args.max_targets]
    if len(candidates) > len(targets):
        print(f"  capped: {len(candidates) - len(targets)} more gaps wait for the next run")
    print(f"{len(targets)} targets")
    if args.out and not args.dry_run and targets:
        pathlib.Path(args.out).write_text(json.dumps({"targets": targets}, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
