#!/usr/bin/env python3
"""Compute the next docket targets for every registry series.

For recurring registry entries, the docket cursor is the latest PUBLISHED
period (recovered from the live catalog by inverting the slug template):
failed or unpublished attempts keep the cursor in place and are retried on
the next roll rather than silently skipped (F10). Reviewed annual snapshot
entries are one-shot seeds with an explicit fiscal year and capture window.
The records/ directories still provide attempt visibility, and the live
catalog's slug set is the final duplicate guard.

Usage:
    python3 scripts/roll_docket.py [--cadence weekly|monthly|quarterly|annual]
        [--max-targets N] [--out targets.json] [--dry-run]

Emits a run_thesis_batch.py-compatible targets file. Weekly targets sort
first (they resolve fastest), then reviewed one-shot snapshot seeds and
earliest next-period first. Exits 0 with an empty targets list when there
is nothing to roll — idempotent by construction, so the schedule can fire
as often as it likes.
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
SNAPSHOT_SEED_HORIZON_DAYS = 75

MONTH_NAMES = [m.lower() for m in calendar.month_name]
OFFICIAL_CALENDAR_ADAPTERS = frozenset(
    {
        "abs-data-api",
        "abs-release-page",
        "eurostat-api",
        "ons-timeseries",
        "statcan-wds",
    }
)


def slugify_series(series: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", series.lower()).strip("-")


def latest_recorded_period(series: str, cadence: str) -> str | None:
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
            if period_key(period, cadence) is not None:
                periods.append(period)
    if not periods:
        return None
    return max(periods, key=lambda period: period_key(period, cadence) or ())


def period_key(period: str, cadence: str) -> tuple[int, ...] | None:
    """Return a semantic sort key, rejecting impossible captured periods."""
    try:
        if cadence == "weekly":
            match = re.fullmatch(r"week_(\d{4}-\d{2}-\d{2})", period)
            if not match:
                return None
            day = dt.date.fromisoformat(match.group(1))
            return (day.toordinal(),)
        if cadence == "monthly":
            match = re.fullmatch(r"(\d{4})-(\d{2})", period)
            if not match:
                return None
            year, month = int(match.group(1)), int(match.group(2))
            if month < 1 or month > 12:
                return None
            return (year, month)
        if cadence == "quarterly":
            match = re.fullmatch(r"(\d{4})-[Qq]([1-4])", period)
            if not match:
                return None
            return (int(match.group(1)), int(match.group(2)))
    except ValueError:
        return None
    return None


def warn_malformed_period(operation: str, period: str, cadence: str) -> None:
    print(
        f"  warning: skip malformed {cadence} period {period!r} during {operation}",
        file=sys.stderr,
    )


def step_period(period: str, cadence: str) -> str | None:
    key = period_key(period, cadence)
    if key is None:
        warn_malformed_period("step", period, cadence)
        return None
    if cadence == "weekly":
        day = dt.date.fromordinal(key[0])
        return f"week_{day + dt.timedelta(days=7)}"
    if cadence == "monthly":
        year, month = key
        month += 1
        if month == 13:
            year, month = year + 1, 1
        return f"{year}-{month:02d}"
    if cadence == "quarterly":
        year, quarter = key[0], key[1] + 1
        if quarter == 5:
            year, quarter = year + 1, 1
        return f"{year}-Q{quarter}"
    warn_malformed_period("step", period, cadence)
    return None


def format_slug(template: str, period: str, cadence: str) -> str:
    if period_key(period, cadence) is None:
        raise ValueError(f"malformed {cadence} period: {period}")
    if cadence == "weekly":
        return template.format(period=period.removeprefix("week_"))
    if cadence == "monthly":
        year, month = period[:4], int(period[5:7])
        return template.format(month=MONTH_NAMES[month], year=year)
    m = re.fullmatch(r"(\d{4})-Q(\d)", period)
    return template.format(quarter=m.group(2), year=m.group(1))


def not_too_far_ahead(period: str, cadence: str, today: dt.date) -> bool:
    """Don't forecast periods that haven't meaningfully begun."""
    key = period_key(period, cadence)
    if key is None:
        warn_malformed_period("horizon check", period, cadence)
        return False
    if cadence == "weekly":
        day = dt.date.fromordinal(key[0])
        return day <= today + dt.timedelta(days=7)
    if cadence == "monthly":
        year, month = key
        return (year, month) <= (today.year, today.month)
    if cadence == "quarterly":
        quarter = (today.month - 1) // 3 + 1
        return key <= (today.year, quarter)
    warn_malformed_period("horizon check", period, cadence)
    return False


def live_catalog() -> tuple[set[str], dict[str, dict], set[str]]:
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
    observed_slugs = {
        entry["forecastSlug"]
        for entry in log.get("entries", [])
        if entry.get("kind") == "prediction_resolved" and entry.get("forecastSlug")
    }
    return set(links), forecasts, observed_slugs


def template_regex(template: str, cadence: str) -> re.Pattern[str]:
    """Invert a registry slug template into a period-extracting regex."""
    token_specs = {
        "weekly": {"period": ("date", r"\d{4}-\d{2}-\d{2}")},
        "monthly": {
            "month": ("month", r"[a-z]+"),
            "year": ("year", r"\d{4}"),
        },
        "quarterly": {
            "quarter": ("quarter", r"\d+"),
            "year": ("year", r"\d{4}"),
        },
    }.get(cadence, {})
    token_pattern = re.compile(r"\{([a-z]+)\}")
    parts: list[str] = []
    seen_groups: set[str] = set()
    cursor = 0
    for match in token_pattern.finditer(template):
        parts.append(re.escape(template[cursor : match.start()]))
        token = match.group(1)
        spec = token_specs.get(token)
        if spec is None:
            parts.append(re.escape(match.group(0)))
        else:
            group, value_pattern = spec
            if group in seen_groups:
                parts.append(f"(?P={group})")
            else:
                parts.append(f"(?P<{group}>{value_pattern})")
                seen_groups.add(group)
        cursor = match.end()
    parts.append(re.escape(template[cursor:]))
    return re.compile(f"^{''.join(parts)}$")


def captured_period(match: re.Match[str], cadence: str) -> str | None:
    """Build and semantically validate a period captured from a slug."""
    try:
        if cadence == "weekly":
            period = f"week_{match.group('date')}"
        elif cadence == "monthly":
            month_name = match.group("month")
            if month_name not in MONTH_NAMES:
                return None
            month = MONTH_NAMES.index(month_name)
            period = f"{match.group('year')}-{month:02d}"
        elif cadence == "quarterly":
            period = f"{match.group('year')}-Q{match.group('quarter')}"
        else:
            return None
    except (IndexError, ValueError):
        return None
    return period if period_key(period, cadence) is not None else None


def published_periods(entry: dict, catalog_slugs: set[str]) -> list[tuple[str, str]]:
    pattern = template_regex(entry["slug"], entry["cadence"])
    periods: list[tuple[str, str]] = []
    for slug in catalog_slugs:
        match = pattern.match(slug)
        if not match:
            continue
        period = captured_period(match, entry["cadence"])
        if period is None:
            print(
                f"  warning: skip slug with invalid captured period: {slug}",
                file=sys.stderr,
            )
            continue
        periods.append((period, slug))
    return periods


def latest_published_period(
    entry: dict, catalog_slugs: set[str]
) -> tuple[str, str] | None:
    """Latest period with a PUBLISHED cell in the live catalog.

    The docket cursor advances only past published work: a run that
    failed validation, tests, or deployment keeps the cursor in place
    and is retried on the next roll instead of silently vanishing from
    the public record (review finding F10).
    """
    periods = published_periods(entry, catalog_slugs)
    if not periods:
        return None
    return max(
        periods,
        key=lambda item: period_key(item[0], entry["cadence"]) or (),
    )


def next_roll_period(
    entry: dict,
    catalog_slugs: set[str],
    observed_slugs: set[str],
    today: dt.date,
) -> tuple[str, str] | None:
    """Choose the normal successor or recover the earliest eligible gap.

    A syntactically valid far-future published slug must not freeze a series.
    If its successor is beyond the horizon, scan forward from the last
    ledger-observed period and select the earliest unpublished, eligible gap
    before the maximum published period.
    """
    periods = published_periods(entry, catalog_slugs)
    if not periods:
        return None
    cadence = entry["cadence"]
    latest, latest_slug = max(
        periods, key=lambda item: period_key(item[0], cadence) or ()
    )
    successor = step_period(latest, cadence)
    if successor is None:
        return None
    if not_too_far_ahead(successor, cadence, today):
        return successor, latest_slug

    observed_periods = published_periods(entry, catalog_slugs & observed_slugs)
    if not observed_periods:
        return None
    last_observed, _ = max(
        observed_periods, key=lambda item: period_key(item[0], cadence) or ()
    )
    max_key = period_key(latest, cadence)
    cursor = last_observed
    while max_key is not None:
        candidate = step_period(cursor, cadence)
        if candidate is None:
            return None
        candidate_key = period_key(candidate, cadence)
        if candidate_key is None or candidate_key >= max_key:
            return None
        if not not_too_far_ahead(candidate, cadence, today):
            return None
        slug = format_slug(entry["slug"], candidate, cadence)
        if slug not in catalog_slugs:
            earlier = [
                item
                for item in periods
                if (period_key(item[0], cadence) or ()) < candidate_key
            ]
            previous_slug = max(
                earlier, key=lambda item: period_key(item[0], cadence) or ()
            )[1]
            print(
                f"  recover {entry['series']} gap {candidate}: "
                f"max published period {latest} is beyond the horizon"
            )
            return candidate, previous_slug
        cursor = candidate
    return None


def snapshot_seed_target(
    entry: dict,
    catalog_slugs: set[str],
    today: dt.date,
    *,
    horizon_days: int = SNAPSHOT_SEED_HORIZON_DAYS,
) -> dict | None:
    """Admit one reviewed annual registered-query snapshot seed.

    Annual snapshots deliberately do not use the normal published-period
    cursor: their capture date cannot be inferred from cadence. The registry
    must instead pin both the fiscal-year period and the capture window. Once
    that concrete slug is published, this helper never steps it to another
    fiscal year; a future seed requires another reviewed registry change.
    """

    if entry.get("cadence") != "annual":
        return None
    extras = entry.get("extras")
    binding = extras.get("sourceBinding") if isinstance(extras, dict) else None
    if not isinstance(binding, dict) or (
        binding.get("releasePolicy") != "registered_query_snapshot"
    ):
        print(
            f"  warning: skip {entry.get('series', '?')}: annual seed is not "
            "a registered_query_snapshot",
            file=sys.stderr,
        )
        return None
    period = entry.get("period")
    if not isinstance(period, str) or not re.fullmatch(r"FY\d{4}", period):
        print(
            f"  warning: skip {entry.get('series', '?')}: malformed annual "
            f"snapshot period {period!r}",
            file=sys.stderr,
        )
        return None
    window = extras.get("expectedReleaseWindow")
    if not isinstance(window, dict) or set(window) != {"start", "end"}:
        print(
            f"  warning: skip {entry.get('series', '?')}: annual snapshot "
            "requires an exact expectedReleaseWindow",
            file=sys.stderr,
        )
        return None
    try:
        if not all(isinstance(window[key], str) for key in ("start", "end")):
            raise ValueError
        start = dt.date.fromisoformat(window["start"])
        end = dt.date.fromisoformat(window["end"])
    except ValueError:
        print(
            f"  warning: skip {entry.get('series', '?')}: malformed annual "
            "snapshot window",
            file=sys.stderr,
        )
        return None
    if start > end:
        print(
            f"  warning: skip {entry.get('series', '?')}: annual snapshot "
            "window ends before it starts",
            file=sys.stderr,
        )
        return None
    if not (today < start <= today + dt.timedelta(days=horizon_days)):
        return None
    try:
        slug = entry["slug"].format(period=period.lower())
    except (KeyError, TypeError, ValueError):
        print(
            f"  warning: skip {entry.get('series', '?')}: malformed annual "
            "snapshot slug template",
            file=sys.stderr,
        )
        return None
    if slug in catalog_slugs:
        return None
    return {
        "series": entry["series"],
        "period": period,
        "catalogSlug": slug,
        **extras,
    }




def target_extras_for_period(entry: dict, period: str) -> dict | None:
    """Return target extras, requiring a dated calendar slot for native APIs.

    A previous target's resolution date is not evidence for the next official
    release date. Native international adapters therefore roll only when the
    committed registry maps the exact reference period to an agency-published
    date and records the calendar used to verify it.
    """
    extras = entry.get("extras") or {}
    binding = extras.get("sourceBinding") if isinstance(extras, dict) else None
    adapter = binding.get("adapter") if isinstance(binding, dict) else None
    if adapter not in OFFICIAL_CALENDAR_ADAPTERS:
        return dict(extras)

    release_dates = entry.get("releaseDates")
    release_date = (
        release_dates.get(period) if isinstance(release_dates, dict) else None
    )
    calendar_url = entry.get("releaseCalendarUrl")
    try:
        if not isinstance(release_date, str):
            raise ValueError("missing date")
        dt.date.fromisoformat(release_date)
        if not isinstance(calendar_url, str) or not calendar_url.startswith(
            "https://"
        ):
            raise ValueError("missing HTTPS calendar URL")
    except ValueError:
        print(
            f"  warning: skip {entry.get('series', '?')} {period}: "
            "native adapter has no valid explicit official release date "
            "and releaseCalendarUrl in the docket registry",
            file=sys.stderr,
        )
        return None

    return {
        **extras,
        "expectedReleaseDate": release_date,
        "releaseCalendarUrl": calendar_url,
    }


def advance_past_released_native_periods(
    entry: dict, period: str, today: dt.date
) -> str | None:
    """Advance over never-forecast periods whose official print is now known.

    The normal docket cursor advances only through published forecasts. A
    newly adopted series can therefore point at a missed historical period.
    Native calendar metadata lets us skip that known outcome without ever
    generating a post-release forecast, then select the first still-unreleased
    period that has meaningfully begun.
    """
    extras = entry.get("extras") or {}
    binding = extras.get("sourceBinding") if isinstance(extras, dict) else None
    adapter = binding.get("adapter") if isinstance(binding, dict) else None
    if adapter not in OFFICIAL_CALENDAR_ADAPTERS:
        return period

    candidate = period
    release_dates = entry.get("releaseDates")
    while True:
        release_value = (
            release_dates.get(candidate)
            if isinstance(release_dates, dict)
            else None
        )
        try:
            release_day = dt.date.fromisoformat(str(release_value))
        except ValueError:
            # target_extras_for_period emits the precise missing-date warning.
            return candidate
        if release_day > today:
            return candidate
        print(
            f"  skip {entry.get('series', '?')} {candidate}: official "
            f"release {release_day} is not after docket date {today}",
            file=sys.stderr,
        )
        following = step_period(candidate, entry["cadence"])
        if following is None or not not_too_far_ahead(
            following, entry["cadence"], today
        ):
            return None
        candidate = following


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cadence", choices=["weekly", "monthly", "quarterly", "annual"]
    )
    parser.add_argument("--max-targets", type=int, default=12)
    parser.add_argument("--out")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    registry = json.loads(REGISTRY.read_text())["series"]
    existing, published_forecasts, observed_slugs = live_catalog()
    today = dt.date.today()

    candidates: list[tuple[int, str, dict]] = []
    for entry in registry:
        if args.cadence and entry["cadence"] != args.cadence:
            continue
        if entry["cadence"] == "annual":
            target = snapshot_seed_target(entry, existing, today)
            if target is None:
                print(
                    f"  skip {entry['series']}: no eligible reviewed "
                    "snapshot seed"
                )
                continue
            window_start = target["expectedReleaseWindow"]["start"]
            candidates.append((1, window_start, target))
            continue
        next_result = next_roll_period(entry, existing, observed_slugs, today)
        if next_result is None:
            print(f"  skip {entry['series']}: no published cell to step from")
            continue
        nxt, latest_slug = next_result
        nxt = advance_past_released_native_periods(entry, nxt, today)
        if nxt is None:
            continue
        latest = latest_published_period(entry, existing)
        previous_period = next(
            period
            for period, published_slug in published_periods(entry, existing)
            if published_slug == latest_slug
        )
        attempted = latest_recorded_period(entry["series"], entry["cadence"])
        if (
            latest
            and attempted is not None
            and (period_key(attempted, entry["cadence"]) or ())
            > (period_key(latest[0], entry["cadence"]) or ())
        ):
            print(
                f"  retry {entry['series']} {nxt}: an attempt for "
                f"{attempted} was recorded but never published"
            )
        slug = format_slug(entry["slug"], nxt, entry["cadence"])
        if slug in existing:
            continue
        extras = target_extras_for_period(entry, nxt)
        if extras is None:
            continue
        target = {
            "series": entry["series"],
            "period": nxt,
            "catalogSlug": slug,
            **extras,
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
                    "sourceContext",
                )
                if previous.get(key) not in (None, "")
            }
            target["previousTarget"]["period"] = previous_period
        # One-shot snapshots get the middle lane so a permanently busy
        # monthly docket cannot starve their finite preregistration window.
        priority = 0 if entry["cadence"] == "weekly" else 2
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
