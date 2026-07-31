#!/usr/bin/env python3
"""Select targets that were preregistered on main but never forecast.

The docket loop registers a target in privileged Git history BEFORE the
analyst runs. When the generate or publish leg fails the registration
survives with no forecast, and nothing reliably picks it back up. Prospect
and ledger-gap registrations name series the committed docket registry does
not contain, so ``roll_docket.py`` never rolls them at all; a registry-backed
orphan is retried only as an accident of cursor arithmetic, because the roll
asks whether a period is the published cursor's successor and never whether
the registered release window is still open. This lane asks the second
question: it retries an orphan while its window is still in the future, the
only interval in which forecasting it is honest chronology.

Selection is deliberately narrow. A target is emitted only when it is

1. registered on main (a canonical ``records/targets`` snapshot plus its
   ``registrationState: "preregistered"`` block in the generated ledger),
2. unforecast (no published cell claims its catalog slug),
3. absent from ``site/src/data/expired-unforecast-registrations.ts``, the
   reviewed terminal list, and
4. strictly before its registered ``expectedReleaseWindow.start``.

Nothing here mints a registration. Each emitted entry is REBUILT from the
docket registry with ``roll_docket``'s own construction helpers and then
re-derived through ``register_targets.build_contract``; a target whose rebuilt
contract is not byte-identical to the committed snapshot is dropped, loudly.
The privileged legs still re-run ``register_targets.py
--bind-registration-commits`` against trusted Git history, which is the
authoritative fail-closed check — this one just refuses to spend analyst time
on a target that could not survive it.

Usage:
    python3 scripts/awaiting_forecast_targets.py [--max-targets N]
        [--out targets.json] [--today YYYY-MM-DD] [--dry-run]

Exits 0 with an empty targets list when nothing is awaiting a forecast, so the
schedule can fire as often as it likes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

import register_targets as registration
import roll_docket as roll
from canonical_json import canonical_bytes

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "scripts" / "docket_series.json"
GENERATED_TARGETS = ROOT / "site" / "src" / "data" / "ledger-targets.generated.ts"
EXPIRED_REGISTRATIONS = (
    ROOT / "site" / "src" / "data" / "expired-unforecast-registrations.ts"
)
TARGET_SNAPSHOTS = ROOT / "records" / "targets"


def expired_unforecast_ids() -> set[str]:
    """The reviewed terminal list of registrations that expired unforecast."""
    source = EXPIRED_REGISTRATIONS.read_text(encoding="utf-8")
    match = re.search(
        r"EXPIRED_UNFORECAST_REGISTRATIONS\s*(?::[^=]+)?=\s*\[(.*?)\]\s*as const;",
        source,
        re.DOTALL,
    )
    if match is None:
        raise SystemExit(
            "cannot read EXPIRED_UNFORECAST_REGISTRATIONS; refusing to retry "
            "targets that may have been terminally retired"
        )
    body = re.sub(r"//[^\n]*", "", match.group(1))
    return set(re.findall(r'"([^"]+)"', body))


def preregistered_blocks() -> list[dict]:
    """Every generated ledger entry still in the preregistered state.

    Publication rewrites a target's block to ``registrationState:
    "published"`` (``generate_ledger_targets.py``), so this is main's own
    answer to "registered but not yet forecast".
    """
    source = GENERATED_TARGETS.read_text(encoding="utf-8")
    blocks = []
    for block in registration._generated_entries(source):
        if registration._block_value(block, "registrationState") != "preregistered":
            continue
        blocks.append(
            {
                key: registration._block_value(block, key)
                for key in (
                    "dataPointId",
                    "series",
                    "period",
                    "catalogSlug",
                    "targetContentHash",
                    "registeredAt",
                    "sourceBinding",
                )
            }
        )
    return blocks


def snapshot_for(content_hash: str) -> tuple[pathlib.Path, dict]:
    """Load the single canonical registration snapshot for a content hash."""
    if not re.fullmatch(r"[0-9a-f]{64}", str(content_hash or "")):
        raise registration.RegistrationError(
            f"malformed targetContentHash {content_hash!r}"
        )
    candidates = sorted(TARGET_SNAPSHOTS.glob(f"*-{content_hash}.json"))
    if len(candidates) != 1:
        raise registration.RegistrationError(
            f"expected exactly one registration snapshot for {content_hash}, "
            f"found {len(candidates)}"
        )
    path = candidates[0]
    snapshot = registration._load_snapshot(path)
    if registration.registration_content_hash(snapshot) != content_hash:
        raise registration.RegistrationError(f"snapshot hash mismatch: {path}")
    if len(snapshot["targets"]) != 1:
        raise registration.RegistrationError(
            f"retry requires a single-target registration snapshot: {path}"
        )
    return path, snapshot["targets"][0]


def rebuild_target(
    entry: dict | None,
    contract: dict,
    catalog_slugs: set[str],
    published_forecasts: dict[str, dict],
) -> dict:
    """Rebuild the raw roll target that produced ``contract``.

    Registry-backed series go back through ``roll_docket``'s own construction
    path so the rebuilt entry is the same object the original roll emitted.
    A prospect-mined series has no committed registry template to rebuild
    from; its raw target is restated from the registration's own contract,
    with every derived field (dataPointId, allowedHosts, window) left to
    ``build_contract`` so the restatement is still checked, not assumed.
    """
    series, period = contract["series"], contract["period"]
    if entry is None:
        binding = contract["sourceBinding"]
        return {
            "series": series,
            "period": period,
            "catalogSlug": contract["catalogSlug"],
            "country": contract["country"],
            "targetUnit": contract["unit"],
            "valueScale": contract["valueScale"],
            "sourceBinding": {
                key: value
                for key, value in binding.items()
                if key not in registration.SOURCE_BINDING_DERIVED_KEYS
            },
            "expectedReleaseWindow": binding["expectedReleaseWindow"],
        }

    extras = entry.get("extras")
    if entry["cadence"] == "annual":
        # Reviewed one-shot snapshot seeds pin both the fiscal-year period and
        # the capture window in the registry; the slug takes the period alone.
        return {
            "series": series,
            "period": period,
            "catalogSlug": entry["slug"].format(period=period.lower()),
            **(extras if isinstance(extras, dict) else {}),
        }

    period_extras = roll.target_extras_for_period(entry, period)
    if period_extras is None:
        raise registration.RegistrationError(
            "committed registry no longer dates this period"
        )
    target = {
        "series": series,
        "period": period,
        "catalogSlug": roll.format_slug(entry["slug"], period, entry["cadence"]),
        **period_extras,
    }
    if contract.get("seedPeriod") is not None:
        release_dates = entry.get("releaseDates")
        release_date = (
            release_dates.get(period) if isinstance(release_dates, dict) else None
        )
        target["seedPeriod"] = period
        target["expectedReleaseDate"] = release_date
        target["releaseCalendarUrl"] = entry.get("releaseCalendarUrl")
        return target
    previous = roll.latest_published_before(entry, period, catalog_slugs)
    if previous is not None:
        previous_period, previous_slug = previous
        published_cell = published_forecasts.get(previous_slug)
        if published_cell:
            target["previousTarget"] = roll.previous_target_block(
                published_cell, previous_period
            )
    return target


def select(
    today: dt.date,
    catalog_slugs: set[str],
    published_forecasts: dict[str, dict],
) -> list[tuple[str, str, dict]]:
    """Return (window start, dataPointId, enriched target) for every retry."""
    registry = {
        entry["series"]: entry for entry in json.loads(REGISTRY.read_text())["series"]
    }
    expired = expired_unforecast_ids()
    selected: list[tuple[str, str, dict]] = []
    for block in preregistered_blocks():
        data_point_id = str(block["dataPointId"])
        window = (block.get("sourceBinding") or {}).get("expectedReleaseWindow") or {}
        start = str(window.get("start") or "")
        if data_point_id in expired:
            print(f"  skip {data_point_id}: retired as expired unforecast")
            continue
        try:
            window_start = dt.date.fromisoformat(start)
        except ValueError:
            print(
                f"  skip {data_point_id}: malformed expected release window",
                file=sys.stderr,
            )
            continue
        if window_start <= today:
            print(
                f"  skip {data_point_id}: release window opened {window_start}; "
                "forecasting it now would fabricate chronology"
            )
            continue
        if block.get("catalogSlug") in catalog_slugs:
            # Defense in depth: the generated ledger says preregistered, but
            # a published cell already claims the slug in the live catalog.
            print(
                f"  skip {data_point_id}: catalog already publishes "
                f"{block.get('catalogSlug')}"
            )
            continue
        try:
            path, contract = snapshot_for(str(block["targetContentHash"]))
            for key in ("dataPointId", "series", "period", "catalogSlug"):
                if contract.get(key) != block.get(key):
                    raise registration.RegistrationError(
                        f"generated ledger {key} disagrees with {path.name}"
                    )
            registered_at = str(block["registeredAt"])
            registration.parse_utc_instant(registered_at)
            entry = registry.get(str(block["series"]))
            target = rebuild_target(entry, contract, catalog_slugs, published_forecasts)
            rebuilt = registration.build_contract(
                target, dt.date.fromisoformat(registered_at[:10])
            )
            if canonical_bytes(rebuilt) != canonical_bytes(contract):
                raise registration.RegistrationError(
                    "rebuilt contract is not byte-identical to the committed "
                    "registration"
                )
        except (
            KeyError,
            TypeError,
            ValueError,
            registration.RegistrationError,
        ) as exc:
            print(f"  skip {data_point_id}: {exc}", file=sys.stderr)
            continue
        target.pop("previousTarget", None)
        target.update(
            registration._target_registration_fields(
                {
                    "path": path,
                    "contract": contract,
                    "targetContentHash": str(block["targetContentHash"]),
                    "registeredAtUtc": registered_at,
                }
            )
        )
        selected.append((start, data_point_id, target))
    selected.sort(key=lambda item: (item[0], item[1]))
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-targets", type=int, default=12)
    parser.add_argument("--out")
    parser.add_argument("--today", help="override the selection date (UTC)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    today = (
        dt.date.fromisoformat(args.today)
        if args.today
        else dt.datetime.now(dt.timezone.utc).date()
    )
    catalog_slugs, published_forecasts, _ = roll.live_catalog()
    try:
        selected = select(today, catalog_slugs, published_forecasts)
    except registration.RegistrationError as exc:
        print(f"awaiting-forecast selection failed: {exc}", file=sys.stderr)
        return 1

    targets = [target for _, _, target in selected[: args.max_targets]]
    dropped = len(selected) - len(targets)
    if dropped > 0:
        print(f"  capped: {dropped} further retries deferred to the next run")
    for start, data_point_id, target in selected[: args.max_targets]:
        print(
            f"  retry {target['catalogSlug']} ({data_point_id}) "
            f"window opens {start}"
        )
    print(f"{len(targets)} targets")

    if args.out and not args.dry_run:
        # Same shape and formatting register_targets.py leaves behind, so the
        # privileged bind step rewrites nothing.
        pathlib.Path(args.out).write_text(
            json.dumps({"targets": targets}, indent=2, sort_keys=True) + "\n"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
