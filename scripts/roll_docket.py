#!/usr/bin/env python3
"""Compute the next docket targets for every registry series.

The registry (scripts/docket_series.json) lists every series with a
rubric-passing published run. For each, the docket cursor is the latest
PUBLISHED period (recovered from the live catalog by inverting the slug
template): failed or unpublished attempts keep the cursor in place and
are retried on the next roll rather than silently skipped (F10). The
records/ directories still provide attempt visibility, and the live
catalog's slug set is the final duplicate guard.

Usage:
    python3 scripts/roll_docket.py [--cadence weekly|monthly|quarterly]
        [--max-targets N] [--out targets.json] [--dry-run]

Emits a run_thesis_batch.py-compatible targets file. Weekly targets sort
first (they resolve fastest), then earliest next-period first. Exits 0
with an empty targets list when there is nothing to roll — idempotent by
construction, so the schedule can fire as often as it likes.
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

MONTH_NAMES = [m.lower() for m in calendar.month_name]


def slugify_series(series: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", series.lower()).strip("-")


def latest_recorded_period(series: str) -> str | None:
    """Latest period attempted for a series, from run directory names.

    Run dirs look like 2026-07-07t13-48-08z-{series-slug}-{period-slug};
    period slugs are 2026-04, 2026-q2, or week-2026-07-04 (period
    underscores become hyphens in the dir name).
    """
    marker = f"-{slugify_series(series)}-"
    periods: list[str] = []
    if not RECORDS.exists():
        return None
    for day_dir in RECORDS.iterdir():
        if not day_dir.is_dir():
            continue
        for run_dir in day_dir.iterdir():
            name = run_dir.name
            idx = name.find(marker)
            if idx < 0:
                continue
            period = name[idx + len(marker) :].replace("week-", "week_")
            # A shorter series name can match inside a longer one's dir
            # (eurostat.unemployment_rate vs ...unemployment_rate.belgium);
            # only accept strings that look like periods.
            if re.fullmatch(r"\d{4}-\d{2}|\d{4}-q\d|week_\d{4}-\d{2}-\d{2}", period):
                periods.append(period)
    if not periods:
        return None
    return max(periods)


def step_period(period: str, cadence: str) -> str:
    if cadence == "weekly":
        day = dt.date.fromisoformat(period.removeprefix("week_"))
        return f"week_{day + dt.timedelta(days=7)}"
    if cadence == "monthly":
        year, month = int(period[:4]), int(period[5:7])
        month += 1
        if month == 13:
            year, month = year + 1, 1
        return f"{year}-{month:02d}"
    if cadence == "quarterly":
        m = re.fullmatch(r"(\d{4})-q(\d)", period.lower())
        year, quarter = int(m.group(1)), int(m.group(2)) + 1
        if quarter == 5:
            year, quarter = year + 1, 1
        return f"{year}-Q{quarter}"
    raise ValueError(cadence)


def format_slug(template: str, period: str, cadence: str) -> str:
    if cadence == "weekly":
        return template.format(period=period.removeprefix("week_"))
    if cadence == "monthly":
        year, month = period[:4], int(period[5:7])
        return template.format(month=MONTH_NAMES[month], year=year)
    m = re.fullmatch(r"(\d{4})-Q(\d)", period)
    return template.format(quarter=m.group(2), year=m.group(1))


def not_too_far_ahead(period: str, cadence: str, today: dt.date) -> bool:
    """Don't forecast periods that haven't meaningfully begun."""
    if cadence == "weekly":
        day = dt.date.fromisoformat(period.removeprefix("week_"))
        return day <= today + dt.timedelta(days=7)
    if cadence == "monthly":
        year, month = int(period[:4]), int(period[5:7])
        return (year, month) <= (today.year, today.month)
    m = re.fullmatch(r"(\d{4})-Q(\d)", period)
    quarter = (today.month - 1) // 3 + 1
    return (int(m.group(1)), int(m.group(2))) <= (today.year, quarter)


def live_catalog() -> tuple[set[str], dict[str, dict]]:
    """Published slugs and their latest recorded target contract."""
    log = load_thesis_log(LOG_URL)
    links = {
        link["forecastSlug"]: link
        for link in log["resolutionLinks"]
        if link.get("forecastSlug")
    }
    forecasts: dict[str, dict] = {}
    for entry in log.get("entries", []):
        if entry.get("kind") != "prediction_recorded":
            continue
        slug = entry.get("forecastSlug")
        if not slug or slug not in links:
            continue
        current = forecasts.get(slug)
        if current is None or str(entry.get("recordedAt") or "") > str(
            current.get("recordedAt") or ""
        ):
            forecasts[slug] = entry
    for slug, link in links.items():
        if slug in forecasts and link.get("targetFactRef"):
            forecasts[slug]["dataPointId"] = link["targetFactRef"]
    return set(links), forecasts


def template_regex(template: str, cadence: str) -> re.Pattern[str]:
    """Invert a registry slug template into a period-extracting regex."""
    escaped = re.escape(template)
    if cadence == "weekly":
        pattern = escaped.replace(re.escape("{period}"), r"(?P<date>\d{4}-\d{2}-\d{2})")
    elif cadence == "monthly":
        pattern = escaped.replace(re.escape("{month}"), r"(?P<month>[a-z]+)").replace(
            re.escape("{year}"), r"(?P<year>\d{4})"
        )
    else:
        pattern = escaped.replace(re.escape("q{quarter}"), r"q(?P<quarter>\d)").replace(
            re.escape("{year}"), r"(?P<year>\d{4})"
        )
    return re.compile(f"^{pattern}$")


def latest_published_period(
    entry: dict, catalog_slugs: set[str]
) -> tuple[str, str] | None:
    """Latest period with a PUBLISHED cell in the live catalog.

    The docket cursor advances only past published work: a run that
    failed validation, tests, or deployment keeps the cursor in place
    and is retried on the next roll instead of silently vanishing from
    the public record (review finding F10).
    """
    pattern = template_regex(entry["slug"], entry["cadence"])
    periods: list[tuple[str, str]] = []
    for slug in catalog_slugs:
        match = pattern.match(slug)
        if not match:
            continue
        if entry["cadence"] == "weekly":
            periods.append((f"week_{match.group('date')}", slug))
        elif entry["cadence"] == "monthly":
            month_name = match.group("month")
            if month_name not in MONTH_NAMES:
                continue
            month = MONTH_NAMES.index(month_name)
            periods.append((f"{match.group('year')}-{month:02d}", slug))
        else:
            periods.append((f"{match.group('year')}-Q{match.group('quarter')}", slug))
    if not periods:
        return None
    return max(periods)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadence", choices=["weekly", "monthly", "quarterly"])
    parser.add_argument("--max-targets", type=int, default=12)
    parser.add_argument("--out")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    registry = json.loads(REGISTRY.read_text())["series"]
    existing, published_forecasts = live_catalog()
    today = dt.date.today()

    candidates: list[tuple[int, str, dict]] = []
    for entry in registry:
        if args.cadence and entry["cadence"] != args.cadence:
            continue
        latest_result = latest_published_period(entry, existing)
        if latest_result is None:
            print(f"  skip {entry['series']}: no published cell to step from")
            continue
        latest, latest_slug = latest_result
        nxt = step_period(latest, entry["cadence"])
        attempted = latest_recorded_period(entry["series"])
        if attempted is not None and attempted.lower() > latest.lower():
            print(
                f"  retry {entry['series']} {nxt}: an attempt for "
                f"{attempted} was recorded but never published"
            )
        if not not_too_far_ahead(nxt, entry["cadence"], today):
            continue
        slug = format_slug(entry["slug"], nxt, entry["cadence"])
        if slug in existing:
            continue
        target = {
            "series": entry["series"],
            "period": nxt,
            "catalogSlug": slug,
            **entry.get("extras", {}),
        }
        previous = published_forecasts.get(latest_slug)
        if previous:
            target["previousTarget"] = {
                key: previous[key]
                for key in (
                    "country",
                    "unit",
                    "dataPointId",
                    "resolutionDate",
                    "resolutionSource",
                    "resolutionSourceUrl",
                    "resolutionRule",
                    "resolutionPolicy",
                )
                if previous.get(key) not in (None, "")
            }
            target["previousTarget"]["period"] = latest
        priority = 0 if entry["cadence"] == "weekly" else 1
        candidates.append((priority, nxt, target))

    candidates.sort(key=lambda item: (item[0], item[1]))
    targets = [target for _, _, target in candidates[: args.max_targets]]
    dropped = len(candidates) - len(targets)
    if dropped > 0:
        print(f"  capped: {dropped} further targets deferred to the next run")

    for target in targets:
        print(f"  roll {target['catalogSlug']} ({target['series']} {target['period']})")
    print(f"{len(targets)} targets")

    if args.out and not args.dry_run:
        pathlib.Path(args.out).write_text(
            json.dumps({"targets": targets}, indent=1) + "\n"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
