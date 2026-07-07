#!/usr/bin/env python3
"""Graduate proven series into the roll registry.

The prospecting loop seeds new series; a series earns a place in
scripts/docket_series.json only after one of its cells has resolved and
been scored (the probation gate). This script scans scored cells, finds
series absent from the registry, derives their slug template and cadence
from the recorded run, and appends registry entries.

Run inside the roll workflow before computing targets, so adoption and the
first roll of a proven series land in the same commit.

Usage: python3 scripts/adopt_proven_series.py [--dry-run]
"""

from __future__ import annotations

import argparse
import calendar
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "scripts" / "docket_series.json"
RECORDS = ROOT / "records" / "thesis-analyst"
LOG_URL = "https://app.thesisinstitute.org/log.json"

MONTH_NAMES = [m.lower() for m in calendar.month_name]


def scored_slugs() -> set[str]:
    with urllib.request.urlopen(LOG_URL, timeout=120) as response:
        log = json.load(response)
    return {score["forecastSlug"] for score in log["scores"]}


def run_manifests():
    if not RECORDS.exists():
        return
    for day_dir in sorted(RECORDS.iterdir()):
        if not day_dir.is_dir():
            continue
        for run_dir in sorted(day_dir.iterdir()):
            manifest = run_dir / "manifest.json"
            if manifest.exists():
                try:
                    yield json.loads(manifest.read_text())
                except json.JSONDecodeError:
                    continue


def slug_template(slug: str, period: str, cadence: str) -> str | None:
    """Derive the registry slug template from a concrete slug + period."""
    if cadence == "weekly":
        date = period.removeprefix("week_")
        return slug.replace(date, "{period}") if date in slug else None
    if cadence == "monthly":
        year, month = period[:4], int(period[5:7])
        name = MONTH_NAMES[month]
        if name in slug and year in slug:
            return slug.replace(name, "{month}").replace(year, "{year}")
        return None
    m = re.fullmatch(r"(\d{4})-Q(\d)", period)
    if m and f"q{m.group(2)}" in slug and m.group(1) in slug:
        return slug.replace(f"q{m.group(2)}", "q{quarter}").replace(m.group(1), "{year}")
    return None


def cadence_of(period: str) -> str | None:
    if re.fullmatch(r"week_\d{4}-\d{2}-\d{2}", period):
        return "weekly"
    if re.fullmatch(r"\d{4}-\d{2}", period):
        return "monthly"
    if re.fullmatch(r"\d{4}-Q\d", period):
        return "quarterly"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    registry = json.loads(REGISTRY.read_text())
    known = {entry["series"] for entry in registry["series"]}
    proven = scored_slugs()

    adopted = []
    for manifest in run_manifests():
        series = manifest.get("series")
        period = str(manifest.get("period") or "")
        if not series or series in known or not manifest.get("ok"):
            continue
        cells_path = manifest.get("cellsPath")
        if not cells_path:
            continue
        try:
            cells = json.loads((ROOT / cells_path).read_text())
        except (OSError, json.JSONDecodeError):
            continue
        slug = next((c["slug"] for c in cells if c["slug"] in proven), None)
        if slug is None:
            continue  # not scored yet — still on probation
        cadence = cadence_of(period)
        template = slug_template(slug, period, cadence) if cadence else None
        if not template:
            print(f"  cannot derive template for {series} ({slug}) — leaving on probation")
            continue
        context = manifest.get("targetContext") or {}
        extras = {
            key: context[key]
            for key in ("valueScale", "targetUnit", "country")
            if key in context
        }
        entry = {"series": series, "cadence": cadence, "slug": template}
        if extras:
            entry["extras"] = extras
        adopted.append(entry)
        known.add(series)
        print(f"  adopt {series} ({cadence}) -> {template}")

    if not adopted:
        print("no series ready for adoption")
        return 0
    if args.dry_run:
        print(f"dry-run: would adopt {len(adopted)} series")
        return 0

    registry["series"].extend(adopted)
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")
    print(f"adopted {len(adopted)} series into the registry")
    return 0


if __name__ == "__main__":
    sys.exit(main())
