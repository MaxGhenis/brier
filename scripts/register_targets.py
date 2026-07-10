#!/usr/bin/env python3
"""Preregister docket targets before any forecast is generated.

The input is a ``run_thesis_batch.py`` targets file.  This command derives a
resolver binding from the docket registry/prospect record and the previous
published target, writes one immutable canonical-JSON snapshot per target under
``records/targets/``, appends preregistered runtime targets, and enriches the
batch target context with the committed contract.

The content hash covers the schema and contract, but deliberately excludes the
snapshot's real ``registeredAtUtc``. The privileged workflow commits and pushes
that byte-exact snapshot before forecasting, making Git history the timing
witness while keeping the contract hash timestamp-independent.
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
from typing import Any
from urllib.parse import urlparse

from canonical_json import canonical_bytes, canonical_sha256

ROOT = pathlib.Path(__file__).resolve().parents[1]
GENERATED_TARGETS = ROOT / "site" / "src" / "data" / "ledger-targets.generated.ts"

REGISTRATION_SCHEMA = "thesis_target_registration_v2"
LEGACY_REGISTRATION_SCHEMA = "thesis_target_registration_v1"
REGISTRATION_SET_SCHEMA = "thesis_target_registration_set_v1"
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


def utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def parse_utc_instant(value: str) -> dt.datetime:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        raise RegistrationError(
            f"registeredAtUtc must be a second-precision UTC instant: {value!r}"
        )
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RegistrationError(f"invalid registeredAtUtc {value!r}") from exc
    if parsed.utcoffset() != dt.timedelta(0):
        raise RegistrationError(f"registeredAtUtc is not UTC: {value!r}")
    return parsed


def registration_hash_payload(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Return the immutable contract projection committed by targetContentHash.

    v2 deliberately excludes the operational registration instant. Git commit
    ancestry and the pushed commit time witness that instant; the content hash
    remains stable for a byte-identical target contract.
    """

    schema = snapshot.get("schemaVersion")
    if schema not in {REGISTRATION_SCHEMA, LEGACY_REGISTRATION_SCHEMA}:
        raise RegistrationError(f"unsupported target registration schema {schema!r}")
    expected_keys = (
        {"schemaVersion", "registeredAtUtc", "targets"}
        if schema == REGISTRATION_SCHEMA
        else {"schemaVersion", "targets"}
    )
    if set(snapshot) != expected_keys:
        raise RegistrationError(
            "registration snapshot has unexpected top-level fields: "
            f"{sorted(set(snapshot) - expected_keys)}"
        )
    if schema == REGISTRATION_SCHEMA:
        parse_utc_instant(str(snapshot.get("registeredAtUtc") or ""))
    targets = snapshot.get("targets")
    if not isinstance(targets, list) or not all(
        isinstance(target, dict) for target in targets
    ):
        raise RegistrationError("registration snapshot targets must be an object list")
    return {"schemaVersion": schema, "targets": targets}


def registration_content_hash(snapshot: dict[str, Any]) -> str:
    return canonical_sha256(registration_hash_payload(snapshot))


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
    # Official series legitimately span sibling hosts (news release page,
    # data-file host, ALFRED mirror). The binding allows every host the
    # series' published history actually used — the previous cell's
    # resolver plus each URL its run fetched — so an agent citing an
    # established official host passes while a novel host still fails.
    allowed_hosts = {_host(source_url)}
    if previous:
        prior_url = previous.get("resolutionSourceUrl")
        if prior_url:
            allowed_hosts.add(_host(str(prior_url)))
        for context_url in previous.get("sourceContext") or []:
            try:
                allowed_hosts.add(_host(str(context_url)))
            except RegistrationError:
                continue
    return {
        "adapter": adapter,
        "sourceUrl": source_url,
        "sourceSeriesId": source_series_id,
        "field": field,
        "table": table,
        "transform": transform,
        "releasePolicy": release_policy,
        "expectedReleaseWindow": window,
        "allowedHosts": sorted(allowed_hosts),
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
    targets: list[dict[str, Any]],
    registration_date: dt.date,
    registered_at_utc: str | None = None,
) -> dict[str, Any]:
    contracts = [build_contract(target, registration_date) for target in targets]
    contracts.sort(key=lambda row: (row["dataPointId"], row["catalogSlug"]))
    ids = [row["dataPointId"] for row in contracts]
    if len(ids) != len(set(ids)):
        raise RegistrationError("registration contains duplicate dataPointIds")
    registered_at_utc = registered_at_utc or utc_now()
    parse_utc_instant(registered_at_utc)
    return {
        "schemaVersion": REGISTRATION_SCHEMA,
        "registeredAtUtc": registered_at_utc,
        "targets": contracts,
    }


def ts_literal(entry: dict[str, Any]) -> str:
    lines = ["  {"]
    for key, value in entry.items():
        rendered = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        lines.append(f"    {key}: {rendered},")
    lines.append("  },")
    return "\n".join(lines)


def _entry_for(
    contract: dict[str, Any], content_hash: str, registered_at_utc: str
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
        "registeredAt": registered_at_utc,
        "targetContentHash": content_hash,
        "series": contract["series"],
        "period": contract["period"],
        "catalogSlug": contract["catalogSlug"],
        "valueScale": contract["valueScale"],
        "sourceBinding": binding,
    }


def _generated_block(source: str, data_point_id: str) -> str | None:
    id_pattern = rf'dataPointId:\s*\n?\s*"{re.escape(data_point_id)}"'
    return next(
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


def _block_value(block: str, key: str) -> Any:
    match = re.search(rf"^    {re.escape(key)}: (.*),$", block, re.MULTILINE)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def _published_block_matches_registration(
    block: str, registration: dict[str, Any]
) -> bool:
    contract = registration["contract"]
    expected = {
        "registrationState": "published",
        "dataPointId": contract["dataPointId"],
        "unit": contract["unit"],
        "registeredAt": registration["registeredAtUtc"],
        "targetContentHash": registration["targetContentHash"],
        "series": contract["series"],
        "period": contract["period"],
        "catalogSlug": contract["catalogSlug"],
        "valueScale": contract["valueScale"],
        "sourceBinding": contract["sourceBinding"],
    }
    return all(
        canonical_bytes(_block_value(block, key)) == canonical_bytes(value)
        for key, value in expected.items()
    )


def render_generated_targets(
    registrations: list[dict[str, Any]], *, allow_published: bool = False
) -> str:
    """Validate existing preregistrations and render only genuinely new ones."""

    source = GENERATED_TARGETS.read_text()
    blocks = []
    for registration in registrations:
        contract = registration["contract"]
        content_hash = registration["targetContentHash"]
        registered_at_utc = registration["registeredAtUtc"]
        data_point_id = contract["dataPointId"]
        expected_block = ts_literal(
            _entry_for(contract, content_hash, registered_at_utc)
        )
        existing_block = _generated_block(source, data_point_id)
        if existing_block:
            if existing_block == expected_block:
                continue
            if allow_published and _published_block_matches_registration(
                existing_block, registration
            ):
                continue
            raise RegistrationError(
                "existing generated target is not the exact immutable "
                f"preregistration for {data_point_id}"
            )
        if registration["existing"]:
            raise RegistrationError(
                f"existing snapshot has no generated preregistration: {data_point_id}"
            )
        blocks.append(expected_block)
    if not blocks:
        return source
    closer = "] satisfies" if "] satisfies" in source else "];"
    index = source.rindex(closer)
    return source[:index] + "\n".join(blocks) + "\n" + source[index:]


def _load_snapshot(path: pathlib.Path) -> dict[str, Any]:
    try:
        snapshot = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise RegistrationError(f"invalid registration snapshot {path}: {exc}") from exc
    if snapshot.get("schemaVersion") != REGISTRATION_SCHEMA:
        raise RegistrationError(
            f"retry snapshot must use {REGISTRATION_SCHEMA}: {path}"
        )
    registered_at_utc = snapshot.get("registeredAtUtc")
    if not isinstance(registered_at_utc, str):
        raise RegistrationError(f"snapshot lacks registeredAtUtc: {path}")
    parse_utc_instant(registered_at_utc)
    if path.read_bytes() != canonical_bytes(snapshot) + b"\n":
        raise RegistrationError(f"registration snapshot is not canonical: {path}")
    return snapshot


def _plan_registration(
    contract: dict[str, Any], registration_date: dt.date, registered_at_utc: str
) -> dict[str, Any]:
    snapshot = {
        "schemaVersion": REGISTRATION_SCHEMA,
        "registeredAtUtc": registered_at_utc,
        "targets": [contract],
    }
    # Use the canonical JSON round-trip as the sole representation feeding both
    # the snapshot bytes and generated TypeScript. This avoids retry drift from
    # dict insertion order or JSON's normalization of integral floats.
    snapshot = json.loads(canonical_bytes(snapshot))
    contract = snapshot["targets"][0]
    content_hash = registration_content_hash(snapshot)
    targets_root = ROOT / "records" / "targets"
    candidates = sorted(targets_root.glob(f"*-{content_hash}.json"))
    if len(candidates) > 1:
        raise RegistrationError(
            f"multiple snapshots restate target content hash {content_hash}"
        )
    if candidates:
        path = candidates[0]
        existing_snapshot = _load_snapshot(path)
        if (
            registration_content_hash(existing_snapshot) != content_hash
            or existing_snapshot["targets"] != [contract]
        ):
            raise RegistrationError(f"registration snapshot hash collision: {path}")
        snapshot = existing_snapshot
        contract = existing_snapshot["targets"][0]
        existing = True
    else:
        path = targets_root / f"{registration_date.isoformat()}-{content_hash}.json"
        if path.exists():
            raise RegistrationError(f"registration snapshot collision: {path}")
        existing = False
    return {
        "path": path,
        "contract": contract,
        "snapshot": snapshot,
        "targetContentHash": content_hash,
        "registeredAtUtc": snapshot["registeredAtUtc"],
        "existing": existing,
    }


def _target_registration_fields(registration: dict[str, Any]) -> dict[str, Any]:
    contract = registration["contract"]
    return {
        "country": contract["country"],
        "dataPointId": contract["dataPointId"],
        "targetUnit": contract["unit"],
        "valueScale": contract["valueScale"],
        "sourceBinding": contract["sourceBinding"],
        "registrationState": "preregistered",
        "registeredAt": registration["registeredAtUtc"],
        "registeredAtUtc": registration["registeredAtUtc"],
        "targetContentHash": registration["targetContentHash"],
        "targetRegistrationPath": registration["path"].relative_to(ROOT).as_posix(),
    }


def register(
    targets_path: pathlib.Path,
    registration_date: dt.date,
    registered_at_utc: str | None = None,
) -> list[dict[str, Any]]:
    payload = json.loads(targets_path.read_text())
    targets = payload.get("targets") if isinstance(payload, dict) else None
    if not isinstance(targets, list) or not all(
        isinstance(row, dict) for row in targets
    ):
        raise RegistrationError("targets file must contain an object-list 'targets'")
    if not targets:
        return []
    registered_at_utc = registered_at_utc or utc_now()
    registered_at = parse_utc_instant(registered_at_utc)
    if registered_at.date() != registration_date:
        raise RegistrationError(
            "registration date must match registeredAtUtc date: "
            f"{registration_date} != {registered_at.date()}"
        )
    contracts = [build_contract(target, registration_date) for target in targets]
    ids = [contract["dataPointId"] for contract in contracts]
    slugs = [contract["catalogSlug"] for contract in contracts]
    if len(ids) != len(set(ids)):
        raise RegistrationError("registration contains duplicate dataPointIds")
    if len(slugs) != len(set(slugs)):
        raise RegistrationError("registration contains duplicate catalogSlugs")

    registrations = [
        _plan_registration(contract, registration_date, registered_at_utc)
        for contract in contracts
    ]
    generated_source = render_generated_targets(registrations, allow_published=True)

    for registration in registrations:
        if not registration["existing"]:
            path = registration["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(canonical_bytes(registration["snapshot"]) + b"\n")
    if generated_source != GENERATED_TARGETS.read_text():
        GENERATED_TARGETS.write_text(generated_source)

    by_slug = {
        registration["contract"]["catalogSlug"]: registration
        for registration in registrations
    }
    for target in targets:
        target.update(_target_registration_fields(by_slug[target["catalogSlug"]]))
        target.pop("previousTarget", None)
    targets_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return registrations


def _git_output(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, text=True, stderr=subprocess.PIPE
        ).strip()
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip()
        raise RegistrationError(
            f"git {' '.join(args)} failed" + (f": {detail}" if detail else "")
        ) from exc


def bind_registration_commits(
    targets_path: pathlib.Path, head: str = "HEAD"
) -> dict[str, Any]:
    """Bind each ephemeral target to the commit that first added its snapshot."""

    source_commit = _git_output("rev-parse", f"{head}^{{commit}}")
    payload = json.loads(targets_path.read_text())
    targets = payload.get("targets") if isinstance(payload, dict) else None
    if not isinstance(targets, list):
        raise RegistrationError("targets file must contain an object-list 'targets'")
    registrations = []
    for target in targets:
        relative = pathlib.PurePosixPath(
            str(target.get("targetRegistrationPath") or "")
        )
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or pathlib.PurePosixPath("records/targets") not in relative.parents
        ):
            raise RegistrationError(f"unsafe targetRegistrationPath: {relative}")
        path = ROOT.joinpath(*relative.parts)
        snapshot = _load_snapshot(path)
        content_hash = registration_content_hash(snapshot)
        if (
            content_hash != target.get("targetContentHash")
            or not relative.name.endswith(f"-{content_hash}.json")
        ):
            raise RegistrationError(f"target content hash mismatch: {relative}")
        contract = next(
            (
                row
                for row in snapshot["targets"]
                if row.get("catalogSlug") == target.get("catalogSlug")
            ),
            None,
        )
        if contract is None or len(snapshot["targets"]) != 1:
            raise RegistrationError(
                f"per-target snapshot does not bind {target.get('catalogSlug')}: "
                f"{relative}"
            )
        expected = {
            "series": target.get("series"),
            "period": target.get("period"),
            "catalogSlug": target.get("catalogSlug"),
            "dataPointId": target.get("dataPointId"),
            "country": target.get("country"),
            "unit": target.get("targetUnit"),
            "valueScale": target.get("valueScale"),
            "sourceBinding": target.get("sourceBinding"),
        }
        for key, value in expected.items():
            if canonical_bytes(contract.get(key)) != canonical_bytes(value):
                raise RegistrationError(
                    f"target registration contract mismatch for {key}: {relative}"
                )
        if target.get("registeredAtUtc") != snapshot["registeredAtUtc"]:
            raise RegistrationError(f"registeredAtUtc mismatch: {relative}")
        commits = _git_output(
            "log",
            source_commit,
            "--diff-filter=A",
            "--format=%H",
            "--",
            relative.as_posix(),
        ).splitlines()
        if len(commits) != 1:
            raise RegistrationError(
                f"expected one introducing commit for {relative}, found {len(commits)}"
            )
        registration_commit = commits[0]
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", registration_commit, source_commit],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        committed = subprocess.check_output(
            ["git", "show", f"{registration_commit}:{relative.as_posix()}"],
            cwd=ROOT,
        )
        if committed != path.read_bytes():
            raise RegistrationError(
                "introducing commit does not contain current snapshot bytes: "
                f"{relative}"
            )
        target["registrationCommit"] = registration_commit
        registrations.append(
            {
                "path": path,
                "contract": contract,
                "snapshot": snapshot,
                "targetContentHash": content_hash,
                "registeredAtUtc": snapshot["registeredAtUtc"],
                "existing": True,
            }
        )

    # A retry is a verification pass, not a chance to recreate or repair the
    # preregistration module. Missing or non-identical blocks fail closed.
    if (
        render_generated_targets(registrations, allow_published=True)
        != GENERATED_TARGETS.read_text()
    ):
        raise RegistrationError("binding registration commits would rewrite targets")

    targets_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    bindings = [
        {
            "catalogSlug": target.get("catalogSlug"),
            "registrationCommit": target.get("registrationCommit"),
            "targetContentHash": target.get("targetContentHash"),
            "targetRegistrationPath": target.get("targetRegistrationPath"),
        }
        for target in targets
    ]
    bindings.sort(key=lambda row: str(row["catalogSlug"]))
    return {
        "schemaVersion": REGISTRATION_SET_SCHEMA,
        "sourceCommit": source_commit,
        "registrationSetHash": canonical_sha256({"targets": targets}),
        "registrationCommits": sorted(
            {str(row["registrationCommit"]) for row in bindings}
        ),
        "targetContentHashes": sorted(
            {str(row["targetContentHash"]) for row in bindings}
        ),
        "targets": bindings,
    }


def registration_metadata(registrations: list[dict[str, Any]]) -> dict[str, Any]:
    rows = [
        {
            "catalogSlug": registration["contract"]["catalogSlug"],
            "registeredAtUtc": registration["registeredAtUtc"],
            "targetContentHash": registration["targetContentHash"],
            "targetRegistrationPath": registration["path"]
            .relative_to(ROOT)
            .as_posix(),
            "existing": registration["existing"],
        }
        for registration in registrations
    ]
    rows.sort(key=lambda row: row["catalogSlug"])
    return {
        "schemaVersion": REGISTRATION_SET_SCHEMA,
        "registrationSetHash": canonical_sha256(rows),
        "targetContentHashes": sorted(
            {str(row["targetContentHash"]) for row in rows}
        ),
        "targets": rows,
    }


def materialize_registration_snapshots(paths: list[pathlib.Path]) -> None:
    """Regenerate preregistration TypeScript from canonical snapshot data.

    This is called only by trusted publisher code after the data bundle has
    passed validation. It lets publication consume JSON-only artifacts while
    preserving the exact preregistered contract used by allowedHosts checks.
    """

    registrations = []
    for path in sorted({path.resolve() for path in paths}):
        try:
            relative = path.relative_to(ROOT).as_posix()
        except ValueError as exc:
            raise RegistrationError(
                f"snapshot is outside the repository: {path}"
            ) from exc
        if not re.fullmatch(
            r"records/targets/\d{4}-\d{2}-\d{2}-[0-9a-f]{64}\.json",
            relative,
        ):
            raise RegistrationError(f"invalid registration snapshot path: {relative}")
        snapshot = _load_snapshot(path)
        content_hash = registration_content_hash(snapshot)
        if not relative.endswith(f"-{content_hash}.json"):
            raise RegistrationError(f"registration snapshot hash mismatch: {relative}")
        for contract in snapshot["targets"]:
            registrations.append(
                {
                    "path": path,
                    "contract": contract,
                    "snapshot": snapshot,
                    "targetContentHash": content_hash,
                    "registeredAtUtc": snapshot["registeredAtUtc"],
                    # Publisher materialization is allowed to create a missing
                    # block, but never to replace a non-identical one.
                    "existing": False,
                }
            )
    rendered = render_generated_targets(registrations, allow_published=True)
    if rendered != GENERATED_TARGETS.read_text():
        GENERATED_TARGETS.write_text(rendered)


def registration_for_cell(cell: dict[str, Any]) -> dict[str, Any]:
    """Load the canonical registration metadata used to finalize one cell."""

    relative = str(cell.get("targetRegistrationPath") or "")
    if not re.fullmatch(
        r"records/targets/\d{4}-\d{2}-\d{2}-[0-9a-f]{64}\.json", relative
    ):
        raise RegistrationError(
            f"cell has no canonical targetRegistrationPath: {relative!r}"
        )
    path = ROOT.joinpath(*pathlib.PurePosixPath(relative).parts)
    snapshot = _load_snapshot(path)
    content_hash = registration_content_hash(snapshot)
    if (
        cell.get("targetContentHash") != content_hash
        or not relative.endswith(f"-{content_hash}.json")
    ):
        raise RegistrationError(f"cell target registration hash mismatch: {relative}")
    if len(snapshot["targets"]) != 1:
        raise RegistrationError(
            f"cell registration must contain exactly one target: {relative}"
        )
    contract = snapshot["targets"][0]
    checks = {
        "dataPointId": cell.get("dataPointId"),
        "country": cell.get("country"),
        "unit": cell.get("unit"),
        "catalogSlug": cell.get("slug"),
    }
    for key, value in checks.items():
        if canonical_bytes(contract.get(key)) != canonical_bytes(value):
            raise RegistrationError(
                f"cell does not match registration {key}: {relative}"
            )
    if cell.get("registeredAtUtc") != snapshot["registeredAtUtc"]:
        raise RegistrationError(f"cell registeredAtUtc mismatch: {relative}")
    return {
        "unit": contract["unit"],
        "registeredAt": snapshot["registeredAtUtc"],
        "targetContentHash": content_hash,
        "series": contract["series"],
        "period": contract["period"],
        "catalogSlug": contract["catalogSlug"],
        "valueScale": contract["valueScale"],
        "sourceBinding": contract["sourceBinding"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets-file", type=pathlib.Path, required=True)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--registered-at-utc")
    parser.add_argument("--bind-registration-commits", action="store_true")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--metadata-out", type=pathlib.Path)
    args = parser.parse_args()
    try:
        if args.bind_registration_commits:
            metadata = bind_registration_commits(args.targets_file, args.head)
            count = len(metadata["targets"])
            message = (
                f"bound {count} target(s) to registration commits at "
                f"{metadata['sourceCommit']}"
            )
        else:
            registrations = register(
                args.targets_file,
                _iso_date(args.date),
                args.registered_at_utc,
            )
            metadata = registration_metadata(registrations)
            count = len(registrations)
            reused = sum(1 for row in registrations if row["existing"])
            message = (
                f"preregistered {count} target(s) ({reused} immutable restatement(s))"
            )
        if args.metadata_out:
            args.metadata_out.parent.mkdir(parents=True, exist_ok=True)
            args.metadata_out.write_text(json.dumps(metadata, indent=2) + "\n")
    except (
        OSError,
        KeyError,
        TypeError,
        json.JSONDecodeError,
        RegistrationError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"target registration failed: {exc}", file=sys.stderr)
        return 1
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
