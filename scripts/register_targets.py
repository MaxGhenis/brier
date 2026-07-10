#!/usr/bin/env python3
"""Preregister docket targets before any forecast is generated.

The input is a ``run_thesis_batch.py`` targets file.  This command derives a
resolver binding from the docket registry/prospect record and the previous
published target, writes an immutable canonical-JSON snapshot under
``records/targets/``, appends preregistered runtime targets, and enriches the
batch target context with the committed contract.

The snapshot hash covers only the sorted contracts.  Operational timestamps
and paths live outside the snapshot, so repeating the same registration is
byte-for-byte and hash stable.
"""

from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import pathlib
import re
import sys
from typing import Any
from urllib.parse import urlparse

from canonical_json import canonical_bytes, canonical_sha256

ROOT = pathlib.Path(__file__).resolve().parents[1]
GENERATED_TARGETS = ROOT / "site" / "src" / "data" / "ledger-targets.generated.ts"

REGISTRATION_SCHEMA = "thesis_target_registration_v1"
SOURCE_ADAPTERS = {"alfred-fred", "generic-url"}
RELEASE_POLICIES = {"first_print", "advance_vintage"}
SERIES_BINDINGS: dict[str, dict[str, Any]] = {
    "us.dol.initial_claims.sa": {
        "adapter": "alfred-fred",
        "sourceSeriesId": "ICSA",
        "field": "ICSA",
        "table": "ALFRED graph CSV",
        "transform": {"operation": "multiply", "factor": 0.001},
        "releasePolicy": "advance_vintage",
        "releaseLagDays": 5,
        "dataPointSuffix": "week_{period}",
    },
    "dol.eta.continued_claims.sa": {
        "adapter": "alfred-fred",
        "sourceSeriesId": "CCSA",
        "field": "CCSA",
        "table": "ALFRED graph CSV",
        "transform": {"operation": "multiply", "factor": 0.000001},
        "releasePolicy": "advance_vintage",
        "releaseLagDays": 12,
        "dataPointSuffix": "week_{period}.first_print",
    },
}


class RegistrationError(ValueError):
    """A target cannot be bound independently enough to forecast."""


def _iso_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise RegistrationError(f"invalid ISO date {value!r}") from exc


def _add_months(day: dt.date, months: int) -> dt.date:
    month_index = day.year * 12 + day.month - 1 + months
    year, month_index = divmod(month_index, 12)
    month = month_index + 1
    return day.replace(
        year=year,
        month=month,
        day=min(day.day, calendar.monthrange(year, month)[1]),
    )


def expected_release_window(
    target: dict[str, Any], previous: dict[str, Any] | None, registration_date: dt.date
) -> dict[str, str]:
    supplied = target.get("expectedReleaseWindow")
    if isinstance(supplied, dict) and supplied.get("start") and supplied.get("end"):
        start, end = _iso_date(str(supplied["start"])), _iso_date(str(supplied["end"]))
    elif target.get("expectedReleaseDate"):
        start = end = _iso_date(str(target["expectedReleaseDate"]))
    elif previous and previous.get("resolutionDate"):
        prior = _iso_date(str(previous["resolutionDate"]))
        period = str(target["period"])
        if period.startswith("week_"):
            center = prior + dt.timedelta(days=7)
            start, end = center - dt.timedelta(days=2), center + dt.timedelta(days=2)
        elif re.fullmatch(r"\d{4}-\d{2}", period):
            center = _add_months(prior, 1)
            start, end = center - dt.timedelta(days=4), center + dt.timedelta(days=4)
        elif re.fullmatch(r"\d{4}-Q\d", period, re.IGNORECASE):
            center = _add_months(prior, 3)
            start, end = center - dt.timedelta(days=7), center + dt.timedelta(days=7)
        else:
            start, end = (
                registration_date + dt.timedelta(days=1),
                registration_date + dt.timedelta(days=75),
            )
    elif target["series"] in SERIES_BINDINGS:
        week = _iso_date(str(target["period"]).removeprefix("week_"))
        lag = int(SERIES_BINDINGS[str(target["series"])]["releaseLagDays"])
        center = week + dt.timedelta(days=lag)
        start, end = center - dt.timedelta(days=2), center + dt.timedelta(days=2)
    else:
        # Prospect/mined targets without an exact official date are admitted
        # only to a broad expected window.  The analyst must verify the exact
        # date; it is deliberately not inferred from cadence.
        start, end = (
            registration_date + dt.timedelta(days=1),
            registration_date + dt.timedelta(days=75),
        )
    if end < start:
        raise RegistrationError("expected release window ends before it starts")
    return {"start": start.isoformat(), "end": end.isoformat()}


def _period_variants(period: str) -> list[str]:
    value = period.removeprefix("week_")
    variants = [period, value, period.replace("-", "_"), value.replace("-", "_")]
    month = re.fullmatch(r"(\d{4})-(\d{2})", period)
    if month:
        year, number = month.groups()
        variants.extend(
            [
                f"{calendar.month_name[int(number)].lower()}_{year}",
                f"{calendar.month_name[int(number)].lower()}-{year}",
            ]
        )
    quarter = re.fullmatch(r"(\d{4})-Q(\d)", period, re.IGNORECASE)
    if quarter:
        year, number = quarter.groups()
        variants.extend([f"{year}_q{number}", f"q{number}_{year}"])
    return sorted(set(variants), key=len, reverse=True)


def derive_data_point_id(
    target: dict[str, Any], previous: dict[str, Any] | None
) -> str:
    if target.get("dataPointId"):
        return str(target["dataPointId"])
    series, period = str(target["series"]), str(target["period"])
    if series in SERIES_BINDINGS:
        suffix = str(SERIES_BINDINGS[series]["dataPointSuffix"]).format(
            period=period.removeprefix("week_")
        )
        return f"{series}.{suffix}"
    if previous and previous.get("dataPointId") and previous.get("period"):
        prior_id = str(previous["dataPointId"])
        old_variants = _period_variants(str(previous["period"]))
        for old in old_variants:
            if old not in prior_id:
                continue
            replacement = _replacement_period_variant(old, period)
            return prior_id.replace(old, replacement, 1)
    token = period.lower().replace("-", "_")
    return f"{series}.{token}.first_print"


def _replacement_period_variant(old: str, new_period: str) -> str:
    if old.startswith("week_"):
        return new_period
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", old):
        return new_period.removeprefix("week_")
    if re.fullmatch(r"\d{4}_\d{2}", old):
        return new_period.replace("-", "_").lower()
    if re.fullmatch(r"\d{4}-\d{2}", old):
        return new_period.lower()
    month = re.fullmatch(r"[a-z]+([_-])\d{4}", old)
    new_month = re.fullmatch(r"(\d{4})-(\d{2})", new_period)
    if month and new_month:
        separator = month.group(1)
        year, number = new_month.groups()
        return f"{calendar.month_name[int(number)].lower()}{separator}{year}"
    quarter = re.fullmatch(r"(\d{4})_q\d", old)
    new_quarter = re.fullmatch(r"(\d{4})-Q(\d)", new_period, re.IGNORECASE)
    if quarter and new_quarter:
        return f"{new_quarter.group(1)}_q{new_quarter.group(2)}"
    quarter = re.fullmatch(r"q\d_(\d{4})", old)
    if quarter and new_quarter:
        return f"q{new_quarter.group(2)}_{new_quarter.group(1)}"
    return new_period.replace("-", "_").lower()


def _host(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    if not host:
        raise RegistrationError(f"source URL has no host: {url!r}")
    return host


def derive_source_binding(
    target: dict[str, Any],
    previous: dict[str, Any] | None,
    window: dict[str, str],
    value_scale: float,
) -> dict[str, Any]:
    supplied = target.get("sourceBinding")
    previous_binding = (previous or {}).get("sourceBinding")
    seed = supplied if isinstance(supplied, dict) else previous_binding
    seed = seed if isinstance(seed, dict) else {}
    series = str(target["series"])
    if series in SERIES_BINDINGS:
        registered = SERIES_BINDINGS[series]
        source_series_id = str(registered["sourceSeriesId"])
        source_url = (
            f"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={source_series_id}"
        )
        adapter = str(registered["adapter"])
        release_policy = str(registered["releasePolicy"])
        field = str(registered["field"])
        table = str(registered["table"])
        transform: Any = registered["transform"]
    else:
        source_url = str(
            seed.get("sourceUrl")
            or target.get("resolutionSourceUrl")
            or (previous or {}).get("resolutionSourceUrl")
            or ""
        )
        if not source_url:
            raise RegistrationError(
                f"{target.get('catalogSlug', series)} has no independent source URL"
            )
        adapter = str(seed.get("adapter") or "generic-url")
        release_policy = str(seed.get("releasePolicy") or "first_print")
        source_series_id = str(
            seed.get("sourceSeriesId") or target.get("sourceSeriesId") or series
        )
        field = str(
            seed.get("field")
            or target.get("sourceField")
            or (previous or {}).get("sourceField")
            or source_series_id
        )
        table = str(
            seed.get("table")
            or target.get("sourceTable")
            or (previous or {}).get("resolutionSource")
            or _host(source_url)
        )
        transform = (
            seed.get("transform")
            or target.get("transform")
            or {
                "operation": "multiply",
                "factor": value_scale,
            }
        )
    if adapter not in SOURCE_ADAPTERS:
        raise RegistrationError(f"unsupported source adapter {adapter!r}")
    if release_policy not in RELEASE_POLICIES:
        raise RegistrationError(f"unsupported release policy {release_policy!r}")
    _host(source_url)
    return {
        "adapter": adapter,
        "sourceUrl": source_url,
        "sourceSeriesId": source_series_id,
        "field": field,
        "table": table,
        "transform": transform,
        "releasePolicy": release_policy,
        "expectedReleaseWindow": window,
    }


def build_contract(
    target: dict[str, Any], registration_date: dt.date
) -> dict[str, Any]:
    previous = target.get("previousTarget")
    if previous is not None and not isinstance(previous, dict):
        raise RegistrationError("previousTarget must be an object")
    unit = target.get("targetUnit") or (previous or {}).get("unit")
    if not unit:
        raise RegistrationError(f"{target.get('catalogSlug', '?')} has no target unit")
    value_scale = float(target.get("valueScale", 1))
    window = expected_release_window(target, previous, registration_date)
    binding = derive_source_binding(target, previous, window, value_scale)
    contract = {
        "series": str(target["series"]),
        "period": str(target["period"]),
        "catalogSlug": str(target["catalogSlug"]),
        "dataPointId": derive_data_point_id(target, previous),
        "country": str(
            target.get("country") or (previous or {}).get("country") or "US"
        ),
        "unit": str(unit),
        "valueScale": value_scale,
        "sourceBinding": binding,
    }
    return contract


def build_snapshot(
    targets: list[dict[str, Any]], registration_date: dt.date
) -> dict[str, Any]:
    contracts = [build_contract(target, registration_date) for target in targets]
    contracts.sort(key=lambda row: (row["dataPointId"], row["catalogSlug"]))
    ids = [row["dataPointId"] for row in contracts]
    if len(ids) != len(set(ids)):
        raise RegistrationError("registration contains duplicate dataPointIds")
    return {"schemaVersion": REGISTRATION_SCHEMA, "targets": contracts}


def ts_literal(entry: dict[str, Any]) -> str:
    lines = ["  {"]
    for key, value in entry.items():
        rendered = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        lines.append(f"    {key}: {rendered},")
    lines.append("  },")
    return "\n".join(lines)


def _entry_for(
    contract: dict[str, Any], content_hash: str, registration_date: dt.date
) -> dict[str, Any]:
    binding = contract["sourceBinding"]
    source_url = binding["sourceUrl"]
    source = binding["table"] or _host(source_url)
    return {
        "kind": "target_registered",
        "dataPointId": contract["dataPointId"],
        "observationId": f"obs.{contract['dataPointId']}",
        "country": contract["country"],
        "periodLabel": contract["period"],
        "unit": contract["unit"],
        # A preregistration has an expected window, not a claimed exact release
        # date.  The upper bound keeps legacy runtime consumers total until the
        # published cell finalizes this entry with the verified date.
        "resolutionDate": binding["expectedReleaseWindow"]["end"],
        "resolutionSource": source,
        "resolutionSourceUrl": source_url,
        "resolutionRule": (
            "Preregistered resolver binding. The analyst must supply the precise "
            "first-print rule without changing the bound source, field/table, "
            "transform, or release policy."
        ),
        "resolutionPolicy": "first_print",
        "sourceKind": "official_release",
        "source": source,
        "sourceUrl": source_url,
        "note": f"Preregistered before forecasting for {contract['catalogSlug']}.",
        "registrationState": "preregistered",
        "registeredAt": f"{registration_date.isoformat()}T00:00:00Z",
        "targetContentHash": content_hash,
        "series": contract["series"],
        "period": contract["period"],
        "catalogSlug": contract["catalogSlug"],
        "valueScale": contract["valueScale"],
        "sourceBinding": binding,
    }


def append_generated_targets(
    contracts: list[dict[str, Any]], content_hash: str, registration_date: dt.date
) -> None:
    source = GENERATED_TARGETS.read_text()
    blocks = []
    for contract in contracts:
        data_point_id = contract["dataPointId"]
        id_pattern = rf'dataPointId:\s*\n?\s*"{re.escape(data_point_id)}"'
        existing_block = next(
            (
                match.group(0)
                for match in re.finditer(
                    r"^  \{\n(?:(?!^  \},$)[\s\S])*?^  \},$",
                    source,
                    re.MULTILINE,
                )
                if re.search(id_pattern, match.group(0))
            ),
            None,
        )
        if existing_block:
            hash_match = re.search(
                r'targetContentHash:\s*"([0-9a-f]{64})"', existing_block
            )
            if hash_match and hash_match.group(1) == content_hash:
                continue
            raise RegistrationError(f"dataPointId already registered: {data_point_id}")
        blocks.append(ts_literal(_entry_for(contract, content_hash, registration_date)))
    if not blocks:
        return
    closer = "] satisfies" if "] satisfies" in source else "];"
    index = source.rindex(closer)
    GENERATED_TARGETS.write_text(
        source[:index] + "\n".join(blocks) + "\n" + source[index:]
    )


def register(
    targets_path: pathlib.Path, registration_date: dt.date
) -> tuple[pathlib.Path, str, dict[str, Any]]:
    payload = json.loads(targets_path.read_text())
    targets = payload.get("targets") if isinstance(payload, dict) else None
    if not isinstance(targets, list) or not all(
        isinstance(row, dict) for row in targets
    ):
        raise RegistrationError("targets file must contain an object-list 'targets'")
    snapshot = build_snapshot(targets, registration_date)
    content_hash = canonical_sha256(snapshot)
    relative = (
        pathlib.Path("records")
        / "targets"
        / f"{registration_date.isoformat()}-{content_hash}.json"
    )
    snapshot_path = ROOT / relative
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_bytes(snapshot) + b"\n"
    if snapshot_path.exists() and snapshot_path.read_bytes() != raw:
        raise RegistrationError(f"registration snapshot collision: {relative}")
    snapshot_path.write_bytes(raw)
    append_generated_targets(snapshot["targets"], content_hash, registration_date)

    by_slug = {row["catalogSlug"]: row for row in snapshot["targets"]}
    for target in targets:
        contract = by_slug[target["catalogSlug"]]
        target.update(
            {
                "dataPointId": contract["dataPointId"],
                "targetUnit": contract["unit"],
                "valueScale": contract["valueScale"],
                "sourceBinding": contract["sourceBinding"],
                "registrationState": "preregistered",
                "registeredAt": f"{registration_date.isoformat()}T00:00:00Z",
                "targetContentHash": content_hash,
                "targetRegistrationPath": relative.as_posix(),
            }
        )
        target.pop("previousTarget", None)
    targets_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return snapshot_path, content_hash, snapshot


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets-file", type=pathlib.Path, required=True)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()
    try:
        path, content_hash, snapshot = register(args.targets_file, _iso_date(args.date))
    except (
        OSError,
        KeyError,
        TypeError,
        json.JSONDecodeError,
        RegistrationError,
    ) as exc:
        print(f"target registration failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"preregistered {len(snapshot['targets'])} target(s) -> "
        f"{path.relative_to(ROOT)} ({content_hash})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
