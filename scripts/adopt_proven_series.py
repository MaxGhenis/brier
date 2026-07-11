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
import datetime as dt
import json
import pathlib
import re
import sys

from thesis_log_client import load_thesis_log

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "scripts" / "docket_series.json"
RECORDS = ROOT / "records" / "thesis-analyst"
LOG_URL = "https://app.thesisinstitute.org/log.json"
SOURCE_BINDING_DERIVED_KEYS = {"expectedReleaseWindow", "allowedHosts"}
SOURCE_BINDING_TEMPLATE_KEYS = {
    "adapter",
    "sourceUrl",
    "sourceSeriesId",
    "field",
    "table",
    "transform",
    "releasePolicy",
}

MONTH_NAMES = [m.lower() for m in calendar.month_name]


def replace_whole_token(value: str, token: str, replacement: str) -> str | None:
    """Replace slug tokens only at non-alphanumeric boundaries."""
    pattern = re.compile(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])")
    if not pattern.search(value):
        return None
    return pattern.sub(lambda _: replacement, value)


def replace_nearest_period_tokens(
    value: str,
    first: str,
    first_replacement: str,
    second: str,
    second_replacement: str,
) -> str | None:
    """Replace the closest whole-token period pair, leaving literals intact."""
    token_matches = []
    for token in (first, second):
        pattern = re.compile(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])")
        matches = list(pattern.finditer(value))
        if not matches:
            return None
        token_matches.append(matches)
    left, right = min(
        (
            (left_match, right_match)
            for left_match in token_matches[0]
            for right_match in token_matches[1]
        ),
        key=lambda pair: min(
            abs(pair[0].end() - pair[1].start()),
            abs(pair[1].end() - pair[0].start()),
        ),
    )
    replacements = sorted(
        [
            (left.start(), left.end(), first_replacement),
            (right.start(), right.end(), second_replacement),
        ],
        reverse=True,
    )
    output = value
    for start, end, replacement in replacements:
        output = output[:start] + replacement + output[end:]
    return output


def scored_slugs() -> set[str]:
    log = load_thesis_log(LOG_URL)
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
        try:
            dt.date.fromisoformat(date)
        except ValueError:
            return None
        return replace_whole_token(slug, date, "{period}")
    if cadence == "monthly":
        match = re.fullmatch(r"(\d{4})-(\d{2})", period)
        if not match:
            return None
        year, month = match.group(1), int(match.group(2))
        if month < 1 or month > 12:
            return None
        name = MONTH_NAMES[month]
        return replace_nearest_period_tokens(slug, name, "{month}", year, "{year}")
    m = re.fullmatch(r"(\d{4})-Q([1-4])", period)
    if m:
        return replace_nearest_period_tokens(
            slug,
            f"q{m.group(2)}",
            "q{quarter}",
            m.group(1),
            "{year}",
        )
    return None


def cadence_of(period: str) -> str | None:
    weekly = re.fullmatch(r"week_(\d{4}-\d{2}-\d{2})", period)
    if weekly:
        try:
            dt.date.fromisoformat(weekly.group(1))
        except ValueError:
            return None
        return "weekly"
    monthly = re.fullmatch(r"\d{4}-(\d{2})", period)
    if monthly and 1 <= int(monthly.group(1)) <= 12:
        return "monthly"
    if re.fullmatch(r"\d{4}-Q[1-4]", period):
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
            print(
                f"  cannot derive template for {series} ({slug}) — leaving on probation"
            )
            continue
        context = manifest.get("targetContext") or {}
        source_binding = context.get("sourceBinding")
        if not isinstance(source_binding, dict) or set(source_binding) != (
            SOURCE_BINDING_TEMPLATE_KEYS | SOURCE_BINDING_DERIVED_KEYS
        ):
            print(
                f"  cannot derive source-binding template for {series} "
                "— leaving on probation"
            )
            continue
        extras = {
            key: context[key]
            for key in ("valueScale", "targetUnit", "country", "sourceBinding")
            if key in context
        }
        extras["sourceBinding"] = {
            key: value
            for key, value in source_binding.items()
            if key not in SOURCE_BINDING_DERIVED_KEYS
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
