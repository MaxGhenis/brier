"""Shared historical-print floor and reviewed young-series authorization.

The forecast runner and the TypeScript promotion adapter both import this
module.  Keep the policy here so a cell cannot pass one publication path while
failing another.
"""

from __future__ import annotations

import json
import math
import pathlib
import re
import subprocess
from datetime import date
from typing import Any

HISTORY_PRINT_FLOOR = 6
HISTORY_MINIMUM_PRINTS = 3
HISTORY_FLOOR_AGENT_VERSION = "2.5.10"
HISTORY_FLOOR_AGENT_VERSION_PARTS = (2, 5, 10)
HISTORY_AVAILABILITY_STATUS = "official_source_exposes_fewer_than_six_prints"
HISTORY_FLOOR_AUTHORIZATION_KEY = "historyFloorAuthorization"

_SEMVER_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z.-]+)?")
_MONTH_RE = re.compile(r"(\d{4})-(\d{2})")
_QUARTER_RE = re.compile(r"(\d{4})-Q([1-4])")
_YEAR_RE = re.compile(r"\d{4}")
_SHA_RE = re.compile(r"[0-9a-f]{40}")
_PERIOD_TYPES = {"month", "quarter", "year", "fiscal_year", "week_ending"}


def agent_version_enforces_history_floor(agent_version: Any) -> bool:
    """Grandfather only runs carrying a valid pre-floor agent version."""

    if not isinstance(agent_version, str):
        return True
    match = _SEMVER_RE.fullmatch(agent_version)
    if match is None:
        return True
    return (
        tuple(int(part) for part in match.groups()) >= HISTORY_FLOOR_AGENT_VERSION_PARTS
    )


def valid_agent_version(agent_version: Any) -> bool:
    return (
        isinstance(agent_version, str)
        and _SEMVER_RE.fullmatch(agent_version) is not None
    )


def canonical_period_identity(value: Any) -> tuple[str, str] | None:
    """Return a strict, canonical period identity or ``None``.

    Labels remain presentation-only.  Current cells use this object instead:
    ``{"type": "month", "value": "2026-04"}`` (and analogous quarter,
    year, fiscal-year, and week-ending forms).
    """

    if not isinstance(value, dict) or set(value) != {"type", "value"}:
        return None
    period_type = value.get("type")
    period_value = value.get("value")
    if period_type not in _PERIOD_TYPES or not isinstance(period_value, str):
        return None

    if period_type == "month":
        match = _MONTH_RE.fullmatch(period_value)
        if match is None:
            return None
        try:
            date(int(match.group(1)), int(match.group(2)), 1)
        except ValueError:
            return None
    elif period_type == "quarter":
        if _QUARTER_RE.fullmatch(period_value) is None:
            return None
    elif period_type in {"year", "fiscal_year"}:
        if _YEAR_RE.fullmatch(period_value) is None:
            return None
    else:
        try:
            if date.fromisoformat(period_value).isoformat() != period_value:
                return None
        except ValueError:
            return None
    return period_type, period_value


def _numeric_history_rows(
    cell: dict[str, Any],
) -> tuple[list[tuple[str, str]], list[str]]:
    history = cell.get("historicalContext")
    if not isinstance(history, list):
        return [], ["historicalContext must be a list"]

    identities: list[tuple[str, str]] = []
    errors: list[str] = []
    for index, entry in enumerate(history):
        if not isinstance(entry, dict):
            errors.append(f"historicalContext[{index}] must be an object")
            continue
        label = entry.get("label")
        value = entry.get("value")
        if not isinstance(label, str) or not label.strip():
            errors.append(f"historicalContext[{index}] has no nonempty label")
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(float(value))
        ):
            errors.append(f"historicalContext[{index}] has no finite numeric value")
        identity = canonical_period_identity(entry.get("period"))
        if identity is None:
            errors.append(
                f"historicalContext[{index}] has no valid canonical period identity"
            )
        else:
            identities.append(identity)
    return identities, errors


def history_floor_requires_authorization(
    cell: dict[str, Any], agent_version: Any
) -> bool:
    """Whether this run can pass only through a reviewed authorization."""

    if not agent_version_enforces_history_floor(agent_version):
        return False
    identities, _errors = _numeric_history_rows(cell)
    return len(set(identities)) < HISTORY_PRINT_FLOOR


def validate_history_floor_authorization(
    authorization: Any,
    *,
    target_period: str | None = None,
) -> dict[str, Any]:
    """Validate and normalize one reviewed docket authorization."""

    if not isinstance(authorization, dict):
        raise ValueError("history-floor authorization must be an object")
    expected_keys = {
        "targetPeriod",
        "status",
        "availablePrintCount",
        "availablePeriods",
    }
    if set(authorization) != expected_keys:
        raise ValueError(
            "history-floor authorization must contain exactly "
            + ", ".join(sorted(expected_keys))
        )
    authorized_target = authorization.get("targetPeriod")
    if not isinstance(authorized_target, str) or not authorized_target:
        raise ValueError("history-floor authorization targetPeriod is invalid")
    if target_period is not None and authorized_target != target_period:
        raise ValueError(
            "history-floor authorization targetPeriod does not match the run: "
            f"{authorized_target!r} != {target_period!r}"
        )
    if authorization.get("status") != HISTORY_AVAILABILITY_STATUS:
        raise ValueError("history-floor authorization status is invalid")
    count = authorization.get("availablePrintCount")
    if (
        type(count) is not int
        or not HISTORY_MINIMUM_PRINTS <= count < HISTORY_PRINT_FLOOR
    ):
        raise ValueError(
            "history-floor authorization availablePrintCount must be an integer "
            f"from {HISTORY_MINIMUM_PRINTS} through {HISTORY_PRINT_FLOOR - 1}"
        )
    periods = authorization.get("availablePeriods")
    if not isinstance(periods, list) or len(periods) != count:
        raise ValueError(
            "history-floor authorization availablePeriods length must equal "
            "availablePrintCount"
        )
    identities = [canonical_period_identity(period) for period in periods]
    if any(identity is None for identity in identities):
        raise ValueError(
            "history-floor authorization contains an invalid canonical period"
        )
    canonical = [identity for identity in identities if identity is not None]
    if len(set(canonical)) != len(canonical):
        raise ValueError(
            "history-floor authorization availablePeriods must be distinct"
        )
    if len({period_type for period_type, _ in canonical}) != 1:
        raise ValueError(
            "history-floor authorization availablePeriods must use one period type"
        )
    return {
        "targetPeriod": authorized_target,
        "status": HISTORY_AVAILABILITY_STATUS,
        "availablePrintCount": count,
        "availablePeriods": [
            {"type": period_type, "value": period_value}
            for period_type, period_value in canonical
        ],
    }


def reviewed_history_floor_authorization(
    repo_root: pathlib.Path,
    *,
    checkout_sha: Any,
    series: Any,
    target_period: Any,
) -> dict[str, Any] | None:
    """Read an exact authorization from the run's reviewed checkout.

    The cell and its copied target context are model/operator-controlled data
    at this boundary.  Only ``git show <sealed checkout>:docket_series.json``
    is authoritative.
    """

    if (
        checkout_sha in (None, "")
        or series in (None, "")
        or target_period
        in (
            None,
            "",
        )
    ):
        return None
    if not isinstance(checkout_sha, str) or _SHA_RE.fullmatch(checkout_sha) is None:
        raise ValueError("sealed checkoutSha is not a full lowercase Git SHA")
    if not isinstance(series, str) or not isinstance(target_period, str):
        raise ValueError("sealed series and period must be strings")

    ancestry = subprocess.run(
        [
            "git",
            "--no-replace-objects",
            "-C",
            str(repo_root),
            "merge-base",
            "--is-ancestor",
            checkout_sha,
            "HEAD",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if ancestry.returncode != 0:
        detail = ancestry.stderr.strip() or "commit is not an ancestor of HEAD"
        raise ValueError(
            f"sealed checkoutSha is not trusted by this checkout: {detail}"
        )

    shown = subprocess.run(
        [
            "git",
            "--no-replace-objects",
            "-C",
            str(repo_root),
            "show",
            f"{checkout_sha}:scripts/docket_series.json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if shown.returncode != 0:
        detail = shown.stderr.strip() or "docket snapshot is unavailable"
        raise ValueError(f"cannot read reviewed docket at sealed checkout: {detail}")
    try:
        registry = json.loads(shown.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("reviewed docket snapshot is invalid JSON") from exc
    entries = registry.get("series") if isinstance(registry, dict) else None
    if not isinstance(entries, list):
        raise ValueError("reviewed docket snapshot has no series list")

    matching: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("series") != series:
            continue
        extras = entry.get("extras")
        if not isinstance(extras, dict):
            continue
        raw = extras.get(HISTORY_FLOOR_AUTHORIZATION_KEY)
        if raw is None:
            continue
        authorization = validate_history_floor_authorization(raw)
        if authorization["targetPeriod"] == target_period:
            matching.append(authorization)
    if len(matching) > 1:
        raise ValueError(
            "reviewed docket contains multiple history-floor authorizations for "
            f"{series!r} {target_period!r}"
        )
    return matching[0] if matching else None


def history_floor_errors(
    cell: dict[str, Any],
    *,
    agent_version: Any,
    trusted_history_authorization: dict[str, Any] | None = None,
) -> list[str]:
    """Apply the version-aware history floor using canonical periods."""

    history = cell.get("historicalContext")
    if not valid_agent_version(agent_version):
        version_errors = [
            "sealed agentVersion is missing or malformed; current history floor applies"
        ]
    else:
        version_errors = []
        if not agent_version_enforces_history_floor(agent_version):
            if not isinstance(history, list) or len(history) < HISTORY_MINIMUM_PRINTS:
                return [f"needs >={HISTORY_MINIMUM_PRINTS} historical points"]
            return []

    identities, errors = _numeric_history_rows(cell)
    errors = version_errors + errors
    unique_identities = set(identities)
    if len(unique_identities) != len(identities):
        errors.append(
            "historicalContext contains duplicate canonical periods; label aliases "
            "do not count as distinct prints"
        )
    if identities and len({period_type for period_type, _ in identities}) != 1:
        errors.append("historicalContext canonical periods must use one period type")

    print_count = len(unique_identities)
    if print_count < HISTORY_MINIMUM_PRINTS:
        errors.append(
            f"historicalContext needs at least {HISTORY_MINIMUM_PRINTS} distinct "
            "canonical prints"
        )
    if print_count >= HISTORY_PRINT_FLOOR:
        return errors

    availability = cell.get("historyAvailability")
    if availability is not None:
        if not isinstance(availability, dict):
            errors.append("historyAvailability audit commentary must be an object")
        elif (
            availability.get("status") != HISTORY_AVAILABILITY_STATUS
            or type(availability.get("availablePrintCount")) is not int
            or availability.get("availablePrintCount") != print_count
            or not isinstance(availability.get("detail"), str)
            or not availability.get("detail", "").strip()
        ):
            errors.append(
                "historyAvailability audit commentary does not match the canonical "
                "history count"
            )

    if trusted_history_authorization is None:
        errors.append(
            f"historicalContext has {print_count} distinct canonical prints; at "
            f"least {HISTORY_PRINT_FLOOR} are mandatory unless the sealed checkout's "
            "reviewed docket authorizes this exact series and target period"
        )
        return errors

    try:
        authorization = validate_history_floor_authorization(
            trusted_history_authorization
        )
    except ValueError as exc:
        errors.append(f"reviewed history-floor authorization is invalid: {exc}")
        return errors
    authorized = {
        (period["type"], period["value"])
        for period in authorization["availablePeriods"]
    }
    if authorization["availablePrintCount"] != print_count:
        errors.append(
            "reviewed history-floor authorization count does not match the run's "
            f"canonical history count ({authorization['availablePrintCount']} != "
            f"{print_count})"
        )
    if authorized != unique_identities:
        errors.append(
            "reviewed history-floor authorization periods do not exactly match the "
            "run's canonical history periods"
        )
    return errors
