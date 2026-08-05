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

REGISTRATION_SCHEMA = "thesis_target_registration_v3"
V2_REGISTRATION_SCHEMA = "thesis_target_registration_v2"
V1_REGISTRATION_SCHEMA = "thesis_target_registration_v1"
LEGACY_REGISTRATION_SCHEMAS = {V1_REGISTRATION_SCHEMA, V2_REGISTRATION_SCHEMA}
# The first commit whose privileged register jobs mint v3 snapshots. Trusted
# history can only introduce v2 registrations strictly before this commit, so
# a consumer that grandfathers v2 (the strategy comparison lane) must verify
# the snapshot's introducing commit is a strict ancestor of it.
V3_REGISTRATION_CUTOVER_COMMIT = "bd9316c5e3e63306eefbcd4f1611bcf4ce5da0f5"
REGISTRATION_SET_SCHEMA = "thesis_target_registration_set_v1"
LEDGER_PIN_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "site"
    / "src"
    / "data"
    / "ledger-pin.json"
)
LEDGER_PIN_BINDING_KEYS = {"repo", "branch", "sha", "jsonlSha256", "lineCount"}
SOURCE_ADAPTERS = {
    "abs-data-api",
    "abs-release-page",
    "alfred-fred",
    "census-spm-annual-report",
    "eurostat-api",
    "fsa-crp-monthly-summary",
    "generic-url",
    "irs-soi-pub1304",
    "ons-timeseries",
    "statcan-wds",
    "usaspending-api",
}
# Some reviewed adapters resolve through a sibling official data host that is
# distinct from the registered landing/announcement URL. Keep that expansion
# trusted and adapter-specific; target proposals cannot widen allowedHosts.
SOURCE_ADAPTER_ALLOWED_HOSTS = {
    "census-spm-annual-report": {"www.census.gov", "www2.census.gov"},
}
NATIVE_INTL_SOURCE_ADAPTERS = {
    "abs-data-api",
    "abs-release-page",
    "eurostat-api",
    "ons-timeseries",
    "statcan-wds",
}
RELEASE_POLICIES = {"first_print", "advance_vintage", "registered_query_snapshot"}
RESOLUTION_DATE_BASES = {"release-calendar", "resolve-by-bound"}
DEFAULT_RESOLUTION_DATE_BASIS = "release-calendar"
LEGACY_BOUNDED_CONDITIONAL_IDS = {
    "irs.actc.total_claims.2027.first_print.threshold_one_dollar",
    "irs.actc.total_claims.2027.first_print.current_law",
}
SOURCE_BINDING_DERIVED_KEYS = {"expectedReleaseWindow", "allowedHosts"}
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


def validate_ledger_pin_binding(pin: Any) -> dict[str, Any]:
    """The pinned ledger state a v3 registration commits to."""

    if not isinstance(pin, dict) or set(pin) != LEDGER_PIN_BINDING_KEYS:
        raise RegistrationError(
            "registration ledgerPin must bind exactly "
            f"{sorted(LEDGER_PIN_BINDING_KEYS)}"
        )
    if not re.fullmatch(r"[0-9a-f]{40}", str(pin["sha"])):
        raise RegistrationError(f"ledgerPin sha is not a commit SHA: {pin['sha']!r}")
    if not re.fullmatch(r"[0-9a-f]{64}", str(pin["jsonlSha256"])):
        raise RegistrationError("ledgerPin jsonlSha256 is not a SHA-256 digest")
    # bool subclasses int, and a boolean lineCount renders ledgerPinLineCount:
    # true, which the site's typeof-number N5 gate then skips. Require an exact
    # int so the backfill boundary can never be disabled by a truthy value.
    if type(pin["lineCount"]) is not int or pin["lineCount"] < 0:
        raise RegistrationError("ledgerPin lineCount must be a non-negative int")
    if not pin["repo"] or not pin["branch"]:
        raise RegistrationError("ledgerPin repo/branch must be non-empty")
    return pin


def load_ledger_pin_binding() -> dict[str, Any]:
    """Project the committed site pin into the registration binding."""

    try:
        pin = json.loads(LEDGER_PIN_PATH.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise RegistrationError(
            f"cannot register without the committed ledger pin: {exc}"
        ) from exc
    if pin.get("schemaVersion") != "thesis_ledger_pin_v1":
        raise RegistrationError(
            f"unsupported ledger pin schema {pin.get('schemaVersion')!r}"
        )
    return validate_ledger_pin_binding(
        {key: pin[key] for key in sorted(LEDGER_PIN_BINDING_KEYS)}
    )


def registration_hash_payload(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Return the immutable contract projection committed by targetContentHash.

    v2+ deliberately excludes the operational registration instant. Git commit
    ancestry and the pushed commit time witness that instant; the content hash
    remains stable for a byte-identical target contract. v3 additionally
    commits the pinned ledger state, so the accepted history a target was
    registered against is part of its contract (a resolving print must enter
    the ledger after that state; review finding N5).
    """

    schema = snapshot.get("schemaVersion")
    if schema not in {REGISTRATION_SCHEMA, *LEGACY_REGISTRATION_SCHEMAS}:
        raise RegistrationError(f"unsupported target registration schema {schema!r}")
    if schema == REGISTRATION_SCHEMA:
        expected_keys = {"schemaVersion", "registeredAtUtc", "targets", "ledgerPin"}
    elif schema == V2_REGISTRATION_SCHEMA:
        expected_keys = {"schemaVersion", "registeredAtUtc", "targets"}
    else:
        expected_keys = {"schemaVersion", "targets"}
    if set(snapshot) != expected_keys:
        raise RegistrationError(
            "registration snapshot top-level fields do not match "
            f"{schema}: extra={sorted(set(snapshot) - expected_keys)}, "
            f"missing={sorted(expected_keys - set(snapshot))}"
        )
    if "registeredAtUtc" in expected_keys:
        parse_utc_instant(str(snapshot.get("registeredAtUtc") or ""))
    targets = snapshot.get("targets")
    if not isinstance(targets, list) or not all(
        isinstance(target, dict) for target in targets
    ):
        raise RegistrationError("registration snapshot targets must be an object list")
    for index, target in enumerate(targets):
        binding = target.get("sourceBinding")
        window = (
            binding.get("expectedReleaseWindow")
            if isinstance(binding, dict)
            else None
        )
        validate_resolution_date_semantics(
            target.get("resolutionDateBasis", DEFAULT_RESOLUTION_DATE_BASIS),
            target.get("resolutionDate"),
            window,
            label=f"registration target {index}",
        )
    payload = {"schemaVersion": schema, "targets": targets}
    if schema == REGISTRATION_SCHEMA:
        payload["ledgerPin"] = validate_ledger_pin_binding(snapshot.get("ledgerPin"))
    return payload


def registration_content_hash(snapshot: dict[str, Any]) -> str:
    return canonical_sha256(registration_hash_payload(snapshot))


def _iso_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise RegistrationError(f"invalid ISO date {value!r}") from exc


def validate_resolution_date_semantics(
    basis_value: Any,
    resolution_date: Any,
    expected_release_window: Any,
    *,
    label: str = "target",
) -> tuple[str, str | None]:
    """Validate calendar/default or bounded resolution-date semantics.

    This runs both while building a contract and whenever an immutable
    snapshot is consumed. Legacy contracts omit the basis and therefore pass
    ``release-calendar`` as their effective default.
    """

    if not isinstance(basis_value, str) or basis_value not in RESOLUTION_DATE_BASES:
        raise RegistrationError(
            "resolutionDateBasis must be one of "
            f"{sorted(RESOLUTION_DATE_BASES)}, got {basis_value!r} ({label})"
        )
    if basis_value == DEFAULT_RESOLUTION_DATE_BASIS:
        return basis_value, None
    if not (
        isinstance(expected_release_window, dict)
        and set(expected_release_window) == {"start", "end"}
    ):
        raise RegistrationError(
            "resolve-by-bound target requires an exact expectedReleaseWindow"
        )
    start_value = expected_release_window["start"]
    end_value = expected_release_window["end"]
    if not isinstance(start_value, str) or not isinstance(end_value, str):
        raise RegistrationError(
            "resolve-by-bound expectedReleaseWindow dates must be canonical ISO dates"
        )
    start = _iso_date(start_value).isoformat()
    end = _iso_date(end_value).isoformat()
    if start != start_value or end != end_value:
        raise RegistrationError(
            "resolve-by-bound expectedReleaseWindow dates must be canonical ISO dates"
        )
    if start > end:
        raise RegistrationError("expected release window ends before it starts")
    if not isinstance(resolution_date, str):
        raise RegistrationError(
            "resolve-by-bound target requires resolutionDate to equal "
            "expectedReleaseWindow.end"
        )
    resolution_bound = _iso_date(resolution_date).isoformat()
    if resolution_bound != resolution_date or resolution_bound != end:
        raise RegistrationError(
            "resolve-by-bound target requires resolutionDate to equal "
            "expectedReleaseWindow.end"
        )
    return basis_value, resolution_bound


def legacy_bounded_target_projection(
    contract: dict[str, Any], target: dict[str, Any]
) -> bool:
    """The exact pre-property IRS contracts that may inherit docket semantics."""

    binding = contract.get("sourceBinding")
    return (
        "resolutionDateBasis" not in contract
        and "resolutionDate" not in contract
        and target.get("resolutionDateBasis") == "resolve-by-bound"
        and contract.get("dataPointId") in LEGACY_BOUNDED_CONDITIONAL_IDS
        and isinstance(binding, dict)
        and binding.get("adapter") == "irs-soi-pub1304"
    )


def validate_target_resolution_projection(
    contract: dict[str, Any], target: dict[str, Any], *, label: str
) -> None:
    """Require batch context to preserve a snapshot's date-basis semantics."""

    contract_binding = contract.get("sourceBinding")
    contract_window = (
        contract_binding.get("expectedReleaseWindow")
        if isinstance(contract_binding, dict)
        else None
    )
    contract_basis, _contract_bound = validate_resolution_date_semantics(
        contract.get("resolutionDateBasis", DEFAULT_RESOLUTION_DATE_BASIS),
        contract.get("resolutionDate"),
        contract_window,
        label=f"registered contract {label}",
    )
    target_binding = target.get("sourceBinding")
    target_window = target.get("expectedReleaseWindow")
    if target_window is None and isinstance(target_binding, dict):
        target_window = target_binding.get("expectedReleaseWindow")
    target_basis, _target_bound = validate_resolution_date_semantics(
        target.get("resolutionDateBasis", DEFAULT_RESOLUTION_DATE_BASIS),
        target.get("resolutionDate"),
        target_window,
        label=f"batch target {label}",
    )
    if contract_basis == target_basis:
        return
    if legacy_bounded_target_projection(contract, target):
        return
    raise RegistrationError(
        "target registration contract mismatch for resolutionDateBasis: "
        f"{label}"
    )


def resolution_date_basis(target: dict[str, Any]) -> str:
    """Return and validate the target's resolution-date semantics."""

    basis = target.get("resolutionDateBasis", DEFAULT_RESOLUTION_DATE_BASIS)
    if not isinstance(basis, str) or basis not in RESOLUTION_DATE_BASES:
        raise RegistrationError(
            "resolutionDateBasis must be one of "
            f"{sorted(RESOLUTION_DATE_BASES)}, got {basis!r}"
        )
    return str(basis)


def _add_months(day: dt.date, months: int) -> dt.date:
    month_index = day.year * 12 + day.month - 1 + months
    year, month_index = divmod(month_index, 12)
    month = month_index + 1
    return day.replace(
        year=year,
        month=month,
        day=min(day.day, calendar.monthrange(year, month)[1]),
    )


def source_binding_seed(
    target: dict[str, Any], previous: dict[str, Any] | None
) -> dict[str, Any]:
    """Return the same effective binding seed for every registration stage."""
    supplied = target.get("sourceBinding")
    if isinstance(supplied, dict):
        return supplied
    inherited = (previous or {}).get("sourceBinding")
    return inherited if isinstance(inherited, dict) else {}


def expected_release_window(
    target: dict[str, Any], previous: dict[str, Any] | None, registration_date: dt.date
) -> dict[str, str]:
    supplied = target.get("expectedReleaseWindow")
    seed_binding = source_binding_seed(target, previous)
    adapter = (
        seed_binding.get("adapter")
        if isinstance(seed_binding, dict)
        else None
    )
    has_explicit_window = bool(
        isinstance(supplied, dict)
        and supplied.get("start")
        and supplied.get("end")
    )
    if adapter in NATIVE_INTL_SOURCE_ADAPTERS:
        calendar_url = target.get("releaseCalendarUrl")
        if (
            not isinstance(calendar_url, str)
            or urlparse(calendar_url).scheme.lower() != "https"
            or not urlparse(calendar_url).hostname
        ):
            raise RegistrationError(
                "native international target requires an HTTPS "
                "releaseCalendarUrl"
            )
        if not has_explicit_window and not target.get("expectedReleaseDate"):
            raise RegistrationError(
                "native international target requires an explicit official "
                "expectedReleaseDate or expectedReleaseWindow"
            )
    if has_explicit_window:
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
    if start <= registration_date:
        raise RegistrationError(
            "expected release window must start after the registration date"
        )
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
    seed_binding = source_binding_seed(target, previous)
    seed_adapter = (
        seed_binding.get("adapter")
        if isinstance(seed_binding, dict)
        else None
    )
    if seed_adapter in NATIVE_INTL_SOURCE_ADAPTERS:
        # Do not perpetuate a legacy descriptive alias from the previous
        # target. New native registrations use the docket's canonical series
        # as their id stem, so the resolver, target contract, and site scoring
        # agree on identity end to end.
        token = period.lower().replace("-", "_")
        return f"{series}.{token}.first_print"
    if previous and previous.get("dataPointId") and previous.get("period"):
        prior_id = str(previous["dataPointId"])
        old_variants = _period_variants(str(previous["period"]))
        for old in old_variants:
            if old not in prior_id:
                continue
            replacement = _replacement_period_variant(old, period)
            return prior_id.replace(old, replacement, 1)
    token = period.lower().replace("-", "_")
    seed_policy = (
        seed_binding.get("releasePolicy") if isinstance(seed_binding, dict) else None
    )
    if seed_policy == "registered_query_snapshot":
        # Time-anchored semantics: the outcome is whatever the registered
        # query returns on the registered date, not a source first print.
        return f"{series}.{token}.registered_query_snapshot"
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
    seed = source_binding_seed(target, previous)
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
    if release_policy == "registered_query_snapshot":
        supplied_window = target.get("expectedReleaseWindow")
        if not (
            isinstance(supplied_window, dict)
            and supplied_window.get("start")
            and supplied_window.get("end")
        ):
            raise RegistrationError(
                "registered_query_snapshot requires an explicit "
                "expectedReleaseWindow: start = the registered query date, "
                "end = start plus the retry margin"
            )
    _host(source_url)
    # Official series legitimately span sibling hosts (news release page,
    # data-file host, ALFRED mirror). The binding allows every host the
    # series' published history actually used — the previous cell's
    # resolver plus each URL its run fetched — so an agent citing an
    # established official host passes while a novel host still fails.
    allowed_hosts = {
        _host(source_url),
        *SOURCE_ADAPTER_ALLOWED_HOSTS.get(adapter, set()),
    }
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
    basis, resolution_bound = validate_resolution_date_semantics(
        target.get("resolutionDateBasis", DEFAULT_RESOLUTION_DATE_BASIS),
        target.get("resolutionDate"),
        target.get("expectedReleaseWindow"),
        label=str(target.get("catalogSlug") or target.get("series") or "target"),
    )
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
    # Absence is the byte-compatible spelling of the release-calendar
    # default for registrations that predate this property. Explicit values,
    # and every bounded target, are content-hashed into the contract.
    if "resolutionDateBasis" in target:
        contract["resolutionDateBasis"] = basis
    if resolution_bound is not None:
        contract["resolutionDate"] = resolution_bound
    conditional = target.get("conditional")
    if conditional is not None:
        # A conditional arm's legal-state text, condition identity, and
        # deadline are part of the immutable preregistered contract: the
        # batch runner passes the text to the analyst, the run manifest and
        # cells must repeat it byte-for-byte, the site's condition registry
        # matches on the exact string, and the bind step regenerates the
        # whole contract from the committed docket. Baking all three into
        # the content-hashed snapshot makes the condition itself
        # chronology-witnessed.
        if not isinstance(conditional, str) or not conditional.strip():
            raise RegistrationError(
                "conditional must be a non-empty string when present"
            )
        condition_id = target.get("conditionId")
        if not isinstance(condition_id, str) or not condition_id.strip():
            raise RegistrationError(
                "conditional target requires a non-empty conditionId"
            )
        deadline = _iso_date(str(target.get("conditionDeadline")))
        if deadline.isoformat() >= binding["expectedReleaseWindow"]["start"]:
            raise RegistrationError(
                "conditionDeadline must precede the expected release window"
            )
        contract["conditional"] = conditional
        contract["conditionId"] = condition_id
        contract["conditionDeadline"] = deadline.isoformat()
    seed_period = target.get("seedPeriod")
    if seed_period is not None:
        if not isinstance(seed_period, str) or seed_period != contract["period"]:
            raise RegistrationError(
                "recurring seedPeriod must exactly match the target period"
            )
        # This marker is part of the immutable registration content hash. It
        # makes the privileged bind step reauthenticate the seed's one-day
        # release window and calendar against the committed docket after any
        # register-job rebase.
        contract["seedPeriod"] = seed_period
    return contract


def build_snapshot(
    targets: list[dict[str, Any]],
    registration_date: dt.date,
    registered_at_utc: str | None = None,
    ledger_pin: dict[str, Any] | None = None,
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
        "ledgerPin": validate_ledger_pin_binding(
            ledger_pin if ledger_pin is not None else load_ledger_pin_binding()
        ),
    }


def ts_literal(entry: dict[str, Any]) -> str:
    lines = ["  {"]
    for key, value in entry.items():
        rendered = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        lines.append(f"    {key}: {rendered},")
    lines.append("  },")
    return "\n".join(lines)


def _entry_for(
    contract: dict[str, Any],
    content_hash: str,
    registered_at_utc: str,
    ledger_pin: dict[str, Any] | None = None,
) -> dict[str, Any]:
    binding = contract["sourceBinding"]
    source_url = binding["sourceUrl"]
    source = binding["table"] or _host(source_url)
    pin_fields: dict[str, Any] = {}
    if ledger_pin is not None:
        # The pinned ledger state is part of the registered contract: a
        # resolving observation must be accepted into the ledger at a
        # sequence at or beyond this count (a print already inside the
        # pinned state would be a backfill grading a pre-registered target).
        pin_fields = {
            "ledgerPinSha": ledger_pin["sha"],
            "ledgerPinLineCount": ledger_pin["lineCount"],
        }
    entry = {
        "kind": "target_registered",
        "dataPointId": contract["dataPointId"],
        "observationId": f"obs.{contract['dataPointId']}",
        "country": contract["country"],
        "periodLabel": contract["period"],
        "unit": contract["unit"],
        # A preregistration has an expected window, not a claimed exact release
        # date.  The upper bound keeps legacy runtime consumers total until the
        # published cell finalizes this entry with the verified date.
        "resolutionDate": contract.get(
            "resolutionDate", binding["expectedReleaseWindow"]["end"]
        ),
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
        **pin_fields,
    }
    if "resolutionDateBasis" in contract:
        entry["resolutionDateBasis"] = contract["resolutionDateBasis"]
    return entry


def _generated_entries(source: str) -> list[str]:
    """Extract top-level generated array objects without assuming formatting."""

    marker = re.search(r"\bGENERATED_FORECAST_TARGETS\s*=\s*\[", source)
    if marker is None:
        return []

    entries: list[str] = []
    index = marker.end()
    while index < len(source):
        if source.startswith("//", index):
            newline = source.find("\n", index + 2)
            index = len(source) if newline < 0 else newline + 1
            continue
        if source.startswith("/*", index):
            closer = source.find("*/", index + 2)
            if closer < 0:
                return []
            index = closer + 2
            continue
        if source[index] == "]":
            break
        if source[index] != "{":
            index += 1
            continue

        line_start = source.rfind("\n", marker.end(), index) + 1
        entry_start = (
            line_start if not source[line_start:index].strip() else index
        )
        depth = 1
        cursor = index + 1
        quote: str | None = None
        escaped = False
        while cursor < len(source) and depth:
            char = source[cursor]
            if quote is not None:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = None
                cursor += 1
                continue
            if source.startswith("//", cursor):
                newline = source.find("\n", cursor + 2)
                cursor = len(source) if newline < 0 else newline + 1
                continue
            if source.startswith("/*", cursor):
                closer = source.find("*/", cursor + 2)
                if closer < 0:
                    return []
                cursor = closer + 2
                continue
            if char in {'"', "'", "`"}:
                quote = char
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            cursor += 1
        if depth:
            return []
        while cursor < len(source) and source[cursor] in " \t":
            cursor += 1
        if cursor < len(source) and source[cursor] == ",":
            cursor += 1
        entries.append(source[entry_start:cursor])
        index = cursor
    return entries


def _generated_blocks(source: str, data_point_id: str) -> list[str]:
    return [
        block
        for block in _generated_entries(source)
        if _block_value(block, "dataPointId") == data_point_id
    ]


def _generated_block(source: str, data_point_id: str) -> str | None:
    return next(iter(_generated_blocks(source, data_point_id)), None)


def _block_value(block: str, key: str) -> Any:
    key_pattern = re.escape(key)
    pattern = rf'(?:^|[{{,])\s*(?:{key_pattern}|"{key_pattern}")\s*:\s*'
    for match in re.finditer(pattern, block, re.MULTILINE):
        try:
            value, _ = json.JSONDecoder().raw_decode(block, match.end())
        except json.JSONDecodeError:
            continue
        return value
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
    # A v3 registration's published block must retain its pinned ledger state,
    # or a retry could accept a published block that dropped the N5 boundary.
    pin = registration["snapshot"].get("ledgerPin")
    if isinstance(pin, dict):
        expected["ledgerPinSha"] = pin["sha"]
        expected["ledgerPinLineCount"] = pin["lineCount"]
    return all(
        canonical_bytes(_block_value(block, key)) == canonical_bytes(value)
        for key, value in expected.items()
    )


def _reject_duplicate_object_keys(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise RegistrationError(
                f"committed docket contains duplicate JSON key {key!r}"
            )
        value[key] = item
    return value


def _load_committed_docket(head_commit: str) -> list[Any]:
    """Load the series entries committed at one exact trusted revision."""

    try:
        docket = json.loads(
            _git_output("show", f"{head_commit}:scripts/docket_series.json"),
            object_pairs_hook=_reject_duplicate_object_keys,
        )
    except json.JSONDecodeError as exc:
        raise RegistrationError(f"committed docket is not valid JSON: {exc}") from exc
    entries = docket.get("series") if isinstance(docket, dict) else None
    if not isinstance(entries, list):
        raise RegistrationError("committed docket must contain a series list")
    return entries


def _binding_matches_template(binding: Any, template: Any) -> bool:
    if not isinstance(binding, dict) or not isinstance(template, dict):
        return False
    if set(binding) - set(template) != SOURCE_BINDING_DERIVED_KEYS:
        return False
    projection = {
        key: value
        for key, value in binding.items()
        if key not in SOURCE_BINDING_DERIVED_KEYS
    }
    return canonical_bytes(projection) == canonical_bytes(template)


def validate_committed_calendar_contract(
    contract: dict[str, Any], target: dict[str, Any], docket_entry: dict[str, Any]
) -> None:
    """Bind a dated registration's exact window to committed calendar data."""
    binding = contract.get("sourceBinding")
    adapter = binding.get("adapter") if isinstance(binding, dict) else None
    seed_period = contract.get("seedPeriod")
    is_recurring_seed = seed_period is not None
    if adapter not in NATIVE_INTL_SOURCE_ADAPTERS and not is_recurring_seed:
        return
    if is_recurring_seed and (
        not isinstance(seed_period, str)
        or seed_period != contract.get("period")
        or docket_entry.get("seedPeriod") != seed_period
    ):
        raise RegistrationError(
            "recurring seed registration disagrees with the committed "
            "docket seedPeriod"
        )
    release_dates = docket_entry.get("releaseDates")
    release_date = (
        release_dates.get(contract.get("period"))
        if isinstance(release_dates, dict)
        else None
    )
    calendar_url = docket_entry.get("releaseCalendarUrl")
    if not isinstance(release_date, str) or not isinstance(calendar_url, str):
        raise RegistrationError(
            "committed dated docket entry lacks the target period's "
            "release date or calendar URL"
        )
    expected_window = {"start": release_date, "end": release_date}
    if binding.get("expectedReleaseWindow") != expected_window:
        raise RegistrationError(
            "target release window disagrees with the committed "
            "docket calendar"
        )
    if target.get("releaseCalendarUrl") != calendar_url:
        raise RegistrationError(
            "target releaseCalendarUrl disagrees with the committed "
            "docket calendar"
        )


def validate_native_calendar_contract(
    contract: dict[str, Any], target: dict[str, Any], docket_entry: dict[str, Any]
) -> None:
    """Backward-compatible entry point for committed calendar validation."""
    validate_committed_calendar_contract(contract, target, docket_entry)


def require_seed_docket_template(
    contract: dict[str, Any], template_matches: list[dict[str, Any]]
) -> None:
    """Require one committed registry authority for a recurring seed."""
    if contract.get("seedPeriod") is None:
        return
    if len(template_matches) != 1:
        raise RegistrationError(
            "recurring seed target requires exactly one committed docket "
            "template"
        )
    extras = template_matches[0].get("extras")
    template = extras.get("sourceBinding") if isinstance(extras, dict) else None
    if not isinstance(template, dict):
        raise RegistrationError(
            "recurring seed target requires a committed sourceBinding "
            "template"
        )


def require_conditional_docket_template(
    contract: dict[str, Any],
    template_matches: list[dict[str, Any]],
    registered_at_utc: str | None = None,
    batch_target: dict[str, Any] | None = None,
) -> None:
    """Reauthenticate a conditional contract against the committed docket.

    The binding and publication steps re-run after every rebase, so the
    committed registry at the CURRENT trusted checkout — not any earlier
    computation — is the authority for which conditional arms exist. The
    check is total: the committed entry must REGENERATE the bound contract
    byte-for-byte (series, period, slug, dataPointId, conditional text,
    conditionId, deadline, unit, valueScale, and the full source binding
    including its window); with a batch target supplied, every other
    committed target field (resolutionDate, anchors, …) must match it too;
    the sibling arm must still be present and well-formed; and a series
    whose committed entry carries a conditionalPair is conditional-only —
    NO unconditional contract may register under it. Any committed-entry
    drift after registration fails closed before forecasting or
    publication.
    """

    label = (
        f"{contract.get('dataPointId')} in series {contract.get('series')}"
    )
    conditional = contract.get("conditional")
    pair = (
        template_matches[0].get("conditionalPair")
        if len(template_matches) == 1
        else None
    )
    arms = pair.get("arms") if isinstance(pair, dict) else None
    if conditional is None:
        # Checked across EVERY committed match, so a duplicate-series
        # registry state can never launder an unconditional contract past
        # the conditional-only rule.
        if any(
            isinstance(entry, dict)
            and entry.get("conditionalPair") is not None
            for entry in template_matches
        ):
            raise RegistrationError(
                "committed docket makes this series conditional-only; an "
                f"unconditional contract may not register under it: {label}"
            )
        return
    if len(template_matches) != 1:
        raise RegistrationError(
            "conditional target requires exactly one committed docket "
            f"entry: {label}"
        )
    entry = template_matches[0]
    extras = entry.get("extras")
    if not isinstance(arms, list) or len(arms) != 2:
        raise RegistrationError(
            "committed docket entry has no two-arm conditionalPair: "
            f"{label}"
        )
    if not isinstance(extras, dict):
        raise RegistrationError(
            f"committed conditional entry lacks extras: {label}"
        )
    for field in ("catalogSlug", "dataPointId", "conditional", "conditionId"):
        values = [
            arm.get(field) if isinstance(arm, dict) else None for arm in arms
        ]
        if len(set(map(str, values))) != 2 or not all(
            isinstance(value, str) and value.strip() for value in values
        ):
            raise RegistrationError(
                "committed conditional arms are malformed or "
                f"non-distinct on {field}: {label}"
            )
    reserved = {
        "series",
        "period",
        "catalogSlug",
        "dataPointId",
        "conditional",
        "conditionId",
        "conditionDeadline",
    }
    clashing = reserved & set(extras)
    if clashing:
        raise RegistrationError(
            "committed conditional extras restate reserved target keys "
            f"{sorted(clashing)}: {label}"
        )
    for sibling in arms:
        period_token = str(entry.get("period")).replace("-", "_")
        if not re.fullmatch(
            rf"{re.escape(str(entry.get('series')))}"
            rf"\.{re.escape(period_token)}"
            r"\.first_print\.[a-z0-9_]+",
            str(sibling.get("dataPointId")),
        ):
            raise RegistrationError(
                "committed conditional arm dataPointId "
                f"{sibling.get('dataPointId')!r} is not "
                "<series>.<period>.first_print.<condition_token>: "
                f"{label}"
            )
    matching = [
        arm for arm in arms if arm.get("catalogSlug") == contract.get("catalogSlug")
    ]
    if len(matching) != 1:
        raise RegistrationError(
            "committed conditional pair does not name this catalogSlug "
            f"exactly once: {label}"
        )
    arm = matching[0]
    reconstructed_target = {
        **extras,
        "series": entry.get("series"),
        "period": entry.get("period"),
        "catalogSlug": arm.get("catalogSlug"),
        "dataPointId": arm.get("dataPointId"),
        "conditional": arm.get("conditional"),
        "conditionId": arm.get("conditionId"),
        "conditionDeadline": pair.get("conditionDeadline"),
    }
    if batch_target is not None:
        # Preserve the established run-context drift verdict for the fields
        # that are consumed by the analyst beyond resolver identity. Bounded
        # targets additionally sign resolutionDate into the contract, but a
        # changed/deleted docket bound is still first and foremost a mismatch
        # with the exact context the batch ran under.
        context_drifted = sorted(
            key
            for key in ("resolutionDate", "anchors")
            if canonical_bytes(
                [key in reconstructed_target, reconstructed_target.get(key)]
            )
            != canonical_bytes([key in batch_target, batch_target.get(key)])
        )
        if context_drifted:
            raise RegistrationError(
                "committed docket entry no longer generates the batch "
                f"target's run context (drifted: {context_drifted}): {label}"
            )
    try:
        registered_date = (
            parse_utc_instant(registered_at_utc).date()
            if registered_at_utc
            else dt.date.today()
        )
        rebuilt = build_contract(reconstructed_target, registered_date)
    except RegistrationError as exc:
        raise RegistrationError(
            "committed docket entry no longer regenerates a valid "
            f"conditional contract: {label} ({exc})"
        ) from exc
    rebuilt = json.loads(canonical_bytes(rebuilt))
    comparable_rebuilt = rebuilt
    legacy_bounded_contract = legacy_bounded_target_projection(
        contract, reconstructed_target
    )
    if legacy_bounded_contract:
        # The two IRS conditional arms were registered immediately before the
        # basis property existed. Their immutable v3 snapshots already bind
        # the same window and resolve-by day. Let the now-declared docket basis
        # supply only those redundant fields; every pre-existing contract byte
        # must still match. Scope the compatibility to those exact ids and
        # adapter so a later docket edit cannot retrofit bounded semantics
        # onto an unrelated legacy contract without changing its hash.
        comparable_rebuilt = dict(rebuilt)
        comparable_rebuilt.pop("resolutionDateBasis", None)
        comparable_rebuilt.pop("resolutionDate", None)
    if canonical_bytes(comparable_rebuilt) != canonical_bytes(contract):
        drifted = sorted(
            key
            for key in set(comparable_rebuilt) | set(contract)
            if canonical_bytes(comparable_rebuilt.get(key))
            != canonical_bytes(contract.get(key))
        )
        raise RegistrationError(
            "committed docket entry no longer regenerates the registered "
            f"conditional contract (drifted: {drifted}): {label}"
        )
    if batch_target is not None:
        # The contract equality above covers the registration projection;
        # every remaining committed target field (resolutionDate, anchors,
        # and any other extras the analyst runs under) must also still
        # match what the committed entry generates — SYMMETRICALLY, so a
        # committed-field deletion (the reconstruction losing a key the
        # batch ran with) fails exactly like a value change, and presence
        # is distinguished from an explicit null. sourceBinding is
        # excluded because the batch carries the DERIVED binding, already
        # proven equal through the contract; the registration-enrichment
        # keys are the register step's own additions.
        enrichment = {
            "registrationState",
            "registeredAt",
            "registeredAtUtc",
            "targetContentHash",
            "targetRegistrationPath",
            "registrationCommit",
        }
        comparable_target = reconstructed_target
        if legacy_bounded_contract and "resolutionDateBasis" not in batch_target:
            comparable_target = dict(reconstructed_target)
            comparable_target.pop("resolutionDateBasis", None)
        keys = (
            set(comparable_target) | set(batch_target)
        ) - enrichment - {"sourceBinding"}
        drifted = sorted(
            key
            for key in keys
            if canonical_bytes(
                [key in comparable_target, comparable_target.get(key)]
            )
            != canonical_bytes([key in batch_target, batch_target.get(key)])
        )
        if drifted:
            raise RegistrationError(
                "committed docket entry no longer generates the batch "
                f"target's run context (drifted: {drifted}): {label}"
            )


def require_native_docket_template(
    contract: dict[str, Any], template_matches: list[dict[str, Any]]
) -> None:
    """Require one committed series/calendar authority for native targets."""
    binding = contract.get("sourceBinding")
    adapter = binding.get("adapter") if isinstance(binding, dict) else None
    if adapter not in NATIVE_INTL_SOURCE_ADAPTERS:
        return
    if len(template_matches) != 1:
        raise RegistrationError(
            "native international target requires exactly one committed "
            "docket template for "
            f"{contract.get('dataPointId')} in series {contract.get('series')}"
        )
    extras = template_matches[0].get("extras")
    template = extras.get("sourceBinding") if isinstance(extras, dict) else None
    if not isinstance(template, dict):
        raise RegistrationError(
            "native international target requires a committed sourceBinding "
            "template for "
            f"{contract.get('dataPointId')} in series {contract.get('series')}"
        )


def _binding_is_committed_template(
    contract: dict[str, Any], head_commit: str
) -> bool:
    """Authorize a source binding only from its series template at trusted HEAD."""

    try:
        entries = _load_committed_docket(head_commit)
        matches = []
        for entry in entries:
            if not isinstance(entry, dict) or "series" not in entry:
                return False
            if entry["series"] == contract["series"]:
                matches.append(entry)
        if len(matches) != 1:
            return False
        template = matches[0]["extras"]["sourceBinding"]
        return _binding_matches_template(contract["sourceBinding"], template)
    except Exception:
        return False


def _may_supersede(
    existing_block: str,
    registration: dict[str, Any],
    *,
    head_commit: str,
    source: str,
) -> bool:
    """Authenticate and strictly tighten one unpublished preregistration."""

    try:
        data_point_id = registration["contract"]["dataPointId"]
        working_blocks = _generated_blocks(source, data_point_id)
        if len(working_blocks) != 1 or working_blocks[0] != existing_block:
            return False

        generated_relpath = GENERATED_TARGETS.relative_to(ROOT).as_posix()
        committed_source = _git_output(
            "show", f"{head_commit}:{generated_relpath}"
        )
        committed_blocks = _generated_blocks(committed_source, data_point_id)
        if len(committed_blocks) != 1 or committed_blocks[0] != existing_block:
            return False
        if _block_value(existing_block, "registrationState") != "preregistered":
            return False

        content_hash = _block_value(existing_block, "targetContentHash")
        if not isinstance(content_hash, str) or not re.fullmatch(
            r"[0-9a-f]{64}", content_hash
        ):
            return False
        targets_root = ROOT / "records" / "targets"
        snapshot_paths = sorted(targets_root.glob(f"*-{content_hash}.json"))
        if len(snapshot_paths) != 1:
            return False
        snapshot_path = snapshot_paths[0]
        if not snapshot_path.is_file() or snapshot_path.is_symlink():
            return False
        snapshot_relpath = snapshot_path.relative_to(ROOT).as_posix()
        if not re.fullmatch(
            rf"records/targets/\d{{4}}-\d{{2}}-\d{{2}}-{content_hash}\.json",
            snapshot_relpath,
        ):
            return False

        introducing_commits = _git_output(
            "log",
            head_commit,
            "--diff-filter=A",
            "--format=%H",
            "--",
            snapshot_relpath,
        ).splitlines()
        if len(introducing_commits) != 1:
            return False
        introducing_commit = introducing_commits[0]
        _git_output(
            "merge-base", "--is-ancestor", introducing_commit, head_commit
        )
        committed_snapshot_bytes = subprocess.check_output(
            ["git", "show", f"{introducing_commit}:{snapshot_relpath}"],
            cwd=ROOT,
            stderr=subprocess.PIPE,
        )
        if committed_snapshot_bytes != snapshot_path.read_bytes():
            return False
        authenticated_snapshot = _load_snapshot(snapshot_path)
        if (
            registration_content_hash(authenticated_snapshot) != content_hash
            or len(authenticated_snapshot["targets"]) != 1
        ):
            return False
        old_contract = authenticated_snapshot["targets"][0]
        authenticated_block = ts_literal(
            _entry_for(
                old_contract,
                content_hash,
                authenticated_snapshot["registeredAtUtc"],
                authenticated_snapshot.get("ledgerPin"),
            )
        )
        if authenticated_block != existing_block:
            return False

        if authenticated_snapshot["schemaVersion"] == V2_REGISTRATION_SCHEMA:
            cutover_commit = V3_REGISTRATION_CUTOVER_COMMIT
            _git_output("cat-file", "-e", f"{cutover_commit}^{{commit}}")
            if introducing_commit == cutover_commit:
                return False
            _git_output(
                "merge-base", "--is-ancestor", introducing_commit, cutover_commit
            )

        new_contract = registration["contract"]
        if canonical_bytes(old_contract) != canonical_bytes(new_contract):
            old_identity = {**old_contract, "sourceBinding": None}
            new_identity = {**new_contract, "sourceBinding": None}
            if canonical_bytes(old_identity) != canonical_bytes(
                new_identity
            ) or not _binding_is_committed_template(new_contract, head_commit):
                return False
        if parse_utc_instant(registration["registeredAtUtc"]) <= parse_utc_instant(
            authenticated_snapshot["registeredAtUtc"]
        ):
            return False

        new_pin = registration["snapshot"].get("ledgerPin")
        if not isinstance(new_pin, dict):
            return False
        new_pin = validate_ledger_pin_binding(new_pin)
        old_pin = authenticated_snapshot.get("ledgerPin")
        if old_pin is not None:
            old_pin = validate_ledger_pin_binding(old_pin)
            if (
                new_pin["repo"] != old_pin["repo"]
                or new_pin["branch"] != old_pin["branch"]
                or new_pin["lineCount"] < old_pin["lineCount"]
                or (
                    new_pin["lineCount"] == old_pin["lineCount"]
                    and new_pin["jsonlSha256"] != old_pin["jsonlSha256"]
                )
            ):
                return False
        return True
    except Exception:
        return False


def render_generated_targets(
    registrations: list[dict[str, Any]],
    *,
    allow_published: bool = False,
    allow_supersede: bool = False,
) -> str:
    """Validate existing preregistrations and render only genuinely new ones."""

    source = GENERATED_TARGETS.read_text()
    blocks = []
    head_commit: str | None = None
    for registration in registrations:
        contract = registration["contract"]
        content_hash = registration["targetContentHash"]
        registered_at_utc = registration["registeredAtUtc"]
        data_point_id = contract["dataPointId"]
        expected_block = ts_literal(
            _entry_for(
                contract,
                content_hash,
                registered_at_utc,
                registration["snapshot"].get("ledgerPin"),
            )
        )
        existing_block = _generated_block(source, data_point_id)
        if existing_block:
            if existing_block == expected_block:
                continue
            if allow_published and _published_block_matches_registration(
                existing_block, registration
            ):
                continue
            if allow_supersede:
                try:
                    if head_commit is None:
                        head_commit = _git_output("rev-parse", "HEAD^{commit}")
                except Exception:
                    head_commit = ""
                if head_commit and _may_supersede(
                    existing_block,
                    registration,
                    head_commit=head_commit,
                    source=source,
                ):
                    entry_count = len(_generated_entries(source))
                    source = source.replace(existing_block, expected_block, 1)
                    if _generated_blocks(source, data_point_id) != [
                        expected_block
                    ] or len(_generated_entries(source)) != entry_count:
                        # A raw byte replacement can be misdirected by block
                        # bytes sitting outside the parsed array (for example
                        # inside a comment); refuse rather than emit a file
                        # whose parsed state disagrees with the supersession.
                        raise RegistrationError(
                            "supersession did not replace the generated "
                            f"target block for {data_point_id}"
                        )
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
    if snapshot.get("schemaVersion") not in {
        REGISTRATION_SCHEMA,
        V2_REGISTRATION_SCHEMA,
    }:
        raise RegistrationError(
            f"snapshot must use {REGISTRATION_SCHEMA} "
            f"(or the still-live {V2_REGISTRATION_SCHEMA}): {path}"
        )
    registered_at_utc = snapshot.get("registeredAtUtc")
    if not isinstance(registered_at_utc, str):
        raise RegistrationError(f"snapshot lacks registeredAtUtc: {path}")
    parse_utc_instant(registered_at_utc)
    # Re-running the payload validation enforces the per-schema key set and,
    # for v3, the ledgerPin binding shape.
    registration_hash_payload(snapshot)
    if path.read_bytes() != canonical_bytes(snapshot) + b"\n":
        raise RegistrationError(f"registration snapshot is not canonical: {path}")
    return snapshot


def _plan_registration(
    contract: dict[str, Any],
    registration_date: dt.date,
    registered_at_utc: str,
    ledger_pin: dict[str, Any],
) -> dict[str, Any]:
    snapshot = {
        "schemaVersion": REGISTRATION_SCHEMA,
        "registeredAtUtc": registered_at_utc,
        "targets": [contract],
        "ledgerPin": validate_ledger_pin_binding(ledger_pin),
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
    fields = {
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
    if "resolutionDate" in contract:
        fields["resolutionDate"] = contract["resolutionDate"]
    if "resolutionDateBasis" in contract:
        fields["resolutionDateBasis"] = contract["resolutionDateBasis"]
    return fields


def register(
    targets_path: pathlib.Path,
    registration_date: dt.date,
    registered_at_utc: str | None = None,
    skip_unbindable: bool = False,
    *,
    reuse_existing_only: bool = False,
) -> list[dict[str, Any]]:
    if reuse_existing_only and skip_unbindable:
        raise RegistrationError(
            "--reuse-existing-only cannot be combined with --skip-unbindable"
        )
    payload = json.loads(targets_path.read_text())
    targets = payload.get("targets") if isinstance(payload, dict) else None
    if not isinstance(targets, list) or not all(
        isinstance(row, dict) for row in targets
    ):
        raise RegistrationError("targets file must contain an object-list 'targets'")
    if not targets:
        return []
    if skip_unbindable:
        # A docket roll should register every bindable target rather than
        # abort the whole wave on the first series that cannot yet be bound
        # independently. Skipped targets stay OUT of the targets file (the
        # analyst never runs an unregistered target) and are reported loudly
        # so their series get bindings.
        bindable: list[dict[str, Any]] = []
        skipped_conditional_keys: set[tuple[str, str]] = set()
        for target in targets:
            try:
                build_contract(target, registration_date)
            except RegistrationError as exc:
                print(
                    "skipping unbindable target "
                    f"{target.get('catalogSlug', target.get('series', '?'))}: {exc}",
                    file=sys.stderr,
                )
                if target.get("conditional") is not None:
                    skipped_conditional_keys.add(
                        (str(target.get("series")), str(target.get("period")))
                    )
                continue
            bindable.append(target)
        if skipped_conditional_keys:
            # Pair atomicity must survive pruning: selection admits a
            # conditional pair only as one unit (a lone arm is emitted only
            # when its sibling is already published), so if pruning removes
            # a conditional arm HERE, registering the arms it shipped with
            # would publish one premise alone and hand the pruned arm a
            # later, better-informed wave. Drop the siblings too, loudly;
            # the whole pair retries together on a later roll.
            kept: list[dict[str, Any]] = []
            for target in bindable:
                key = (str(target.get("series")), str(target.get("period")))
                if (
                    target.get("conditional") is not None
                    and key in skipped_conditional_keys
                ):
                    print(
                        "skipping sibling conditional arm "
                        f"{target.get('catalogSlug', '?')}: its pair-mate "
                        "failed to bind; the pair retries together on a "
                        "later roll",
                        file=sys.stderr,
                    )
                    continue
                kept.append(target)
            bindable = kept
        if not bindable:
            raise RegistrationError("no bindable targets in this roll")
        targets = bindable
        payload["targets"] = targets
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

    ledger_pin = load_ledger_pin_binding()
    registrations = [
        _plan_registration(contract, registration_date, registered_at_utc, ledger_pin)
        for contract in contracts
    ]
    if reuse_existing_only:
        unregistered = sorted(
            registration["contract"]["catalogSlug"]
            for registration in registrations
            if not registration["existing"]
        )
        if unregistered:
            raise RegistrationError(
                "--reuse-existing-only refused target(s) without an existing "
                "immutable registration: " + ", ".join(unregistered)
            )
        generated_source = render_generated_targets(
            registrations, allow_published=True
        )
    else:
        generated_source = render_generated_targets(
            registrations, allow_published=True, allow_supersede=True
        )

    for registration in registrations:
        if not registration["existing"]:
            path = registration["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(canonical_bytes(registration["snapshot"]) + b"\n")
    if generated_source != GENERATED_TARGETS.read_text():
        if reuse_existing_only:
            raise RegistrationError(
                "--reuse-existing-only refused because generated targets "
                "would be rewritten"
            )
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
    docket_entries = _load_committed_docket(source_commit)
    for index, entry in enumerate(docket_entries):
        if not isinstance(entry, dict) or "series" not in entry:
            raise RegistrationError(
                f"committed docket entry {index} must be an object with series"
            )
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
            "seedPeriod": target.get("seedPeriod"),
            "conditional": target.get("conditional"),
            "conditionId": target.get("conditionId"),
            "conditionDeadline": target.get("conditionDeadline"),
        }
        validate_target_resolution_projection(
            contract, target, label=relative.as_posix()
        )
        for key, value in expected.items():
            if canonical_bytes(contract.get(key)) != canonical_bytes(value):
                raise RegistrationError(
                    f"target registration contract mismatch for {key}: {relative}"
                )
        if target.get("registeredAtUtc") != snapshot["registeredAtUtc"]:
            raise RegistrationError(f"registeredAtUtc mismatch: {relative}")
        series = contract.get("series")
        data_point_id = contract.get("dataPointId")
        template_matches = [
            entry for entry in docket_entries if entry["series"] == series
        ]
        require_native_docket_template(contract, template_matches)
        require_seed_docket_template(contract, template_matches)
        require_conditional_docket_template(
            contract,
            template_matches,
            snapshot["registeredAtUtc"],
            batch_target=target,
        )
        if len(template_matches) > 1:
            raise RegistrationError(
                "ambiguous committed docket template for "
                f"{data_point_id} in series {series}"
            )
        if template_matches:
            entry = template_matches[0]
            extras = entry.get("extras")
            if "extras" in entry and not isinstance(extras, dict):
                raise RegistrationError(
                    "committed docket sourceBinding template is malformed for "
                    f"{data_point_id} in series {series}"
                )
            if isinstance(extras, dict) and "sourceBinding" in extras:
                template = extras["sourceBinding"]
                if not isinstance(template, dict):
                    raise RegistrationError(
                        "committed docket sourceBinding template is malformed for "
                        f"{data_point_id} in series {series}"
                    )
                if not _binding_matches_template(
                    contract.get("sourceBinding"), template
                ):
                    raise RegistrationError(
                        "target registration sourceBinding disagrees with the "
                        "committed docket template for "
                        f"{data_point_id} in series {series}"
                    )
            validate_committed_calendar_contract(contract, target, entry)
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
    finalized = {
        "unit": contract["unit"],
        "registeredAt": snapshot["registeredAtUtc"],
        "targetContentHash": content_hash,
        "series": contract["series"],
        "period": contract["period"],
        "catalogSlug": contract["catalogSlug"],
        "valueScale": contract["valueScale"],
        "sourceBinding": contract["sourceBinding"],
    }
    if "resolutionDateBasis" in contract:
        finalized["resolutionDateBasis"] = contract["resolutionDateBasis"]
    ledger_pin = snapshot.get("ledgerPin")
    if ledger_pin is not None:
        finalized["ledgerPinSha"] = ledger_pin["sha"]
        finalized["ledgerPinLineCount"] = ledger_pin["lineCount"]
    return finalized


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets-file", type=pathlib.Path, required=True)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--registered-at-utc")
    parser.add_argument("--bind-registration-commits", action="store_true")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--metadata-out", type=pathlib.Path)
    parser.add_argument("--skip-unbindable", action="store_true")
    parser.add_argument("--reuse-existing-only", action="store_true")
    args = parser.parse_args()
    try:
        if args.reuse_existing_only and args.bind_registration_commits:
            raise RegistrationError(
                "--reuse-existing-only cannot be combined with "
                "--bind-registration-commits"
            )
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
                args.skip_unbindable,
                reuse_existing_only=args.reuse_existing_only,
            )
            metadata = registration_metadata(registrations)
            count = len(registrations)
            reused = sum(1 for row in registrations if row["existing"])
            if args.reuse_existing_only:
                message = f"verified {count} already-registered target(s)"
            else:
                message = (
                    f"preregistered {count} target(s) "
                    f"({reused} immutable restatement(s))"
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
