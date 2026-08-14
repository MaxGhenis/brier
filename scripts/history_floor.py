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
MAX_AGENT_VERSION_LENGTH = 256
MAX_PERIOD_LABEL_LENGTH = 512

_SEMVER_CORE_IDENTIFIER = r"(?:0|[1-9][0-9]*)"
_SEMVER_PRERELEASE_IDENTIFIER = (
    rf"(?:{_SEMVER_CORE_IDENTIFIER}|"
    r"[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)"
)
_SEMVER_RE = re.compile(
    rf"(?P<major>{_SEMVER_CORE_IDENTIFIER})\."
    rf"(?P<minor>{_SEMVER_CORE_IDENTIFIER})\."
    rf"(?P<patch>{_SEMVER_CORE_IDENTIFIER})"
    rf"(?:-(?P<prerelease>{_SEMVER_PRERELEASE_IDENTIFIER}"
    rf"(?:\.{_SEMVER_PRERELEASE_IDENTIFIER})*))?"
    r"(?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
)
_MONTH_RE = re.compile(r"([0-9]{4})-([0-9]{2})")
_QUARTER_RE = re.compile(r"([0-9]{4})-Q([1-4])")
_YEAR_RE = re.compile(r"[0-9]{4}")
_WEEK_ENDING_RE = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})")
_SHA_RE = re.compile(r"[0-9a-f]{40}")
_PERIOD_TYPES = {"month", "quarter", "year", "fiscal_year", "week_ending"}

_MONTH_NAMES = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}
_MONTH_NAME_PATTERN = "|".join(
    sorted(_MONTH_NAMES, key=lambda name: (-len(name), name))
)
_LABEL_WEEK_ENDING_RE = re.compile(
    r"(?:week +ending +)?([0-9]{4})-([0-9]{2})-([0-9]{2})",
    re.IGNORECASE | re.ASCII,
)
_LABEL_QUARTER_RE = re.compile(
    r"(?:"
    r"(?P<year_first>[0-9]{4})(?:-| +)Q(?P<quarter_after>[1-4])|"
    r"Q(?P<quarter_first>[1-4]) +(?P<year_after>[0-9]{4})"
    r")",
    re.IGNORECASE | re.ASCII,
)
_LABEL_MONTH_RE = re.compile(r"([0-9]{4})-([0-9]{2})")
_LABEL_MONTH_NAME_RE = re.compile(
    rf"(?:"
    rf"(?P<month_first>{_MONTH_NAME_PATTERN})\.? +"
    rf"(?P<month_year_after>[0-9]{{4}})|"
    rf"(?P<month_year_first>[0-9]{{4}}) +"
    rf"(?P<month_after>{_MONTH_NAME_PATTERN})\.?)",
    re.IGNORECASE | re.ASCII,
)
_LABEL_FISCAL_YEAR_RE = re.compile(
    r"(?:"
    r"FY(?P<fy_compact>[0-9]{4})|"
    r"fiscal +year +(?P<fy_words>[0-9]{4})"
    r")",
    re.IGNORECASE | re.ASCII,
)
_LABEL_YEAR_RE = re.compile(
    r"(?:calendar +year +)?([0-9]{4})",
    re.IGNORECASE | re.ASCII,
)


def _agent_version_match(agent_version: Any) -> re.Match[str] | None:
    if (
        not isinstance(agent_version, str)
        or len(agent_version) > MAX_AGENT_VERSION_LENGTH
    ):
        return None
    return _SEMVER_RE.fullmatch(agent_version)


def agent_version_enforces_history_floor(agent_version: Any) -> bool:
    """Grandfather only valid versions whose numeric core predates the floor.

    A prerelease suffix on the 2.5.10 version family does not waive the floor.
    That intentionally fail-closed policy preserves the existing enforcement
    set while strict SemVer grammar decides whether metadata is valid at all.
    """

    match = _agent_version_match(agent_version)
    if match is None:
        return True
    parts = tuple(match.group(name) for name in ("major", "minor", "patch"))
    for part, minimum in zip(parts, HISTORY_FLOOR_AGENT_VERSION_PARTS):
        minimum_text = str(minimum)
        if len(part) != len(minimum_text):
            return len(part) > len(minimum_text)
        if part != minimum_text:
            return part > minimum_text
    return True


def valid_agent_version(agent_version: Any) -> bool:
    return _agent_version_match(agent_version) is not None


def canonical_period_identity(value: Any) -> tuple[str, str] | None:
    """Return a strict, canonical period identity or ``None``.

    Current cells pair this object with a display label that independently
    names the same period: ``{"type": "month", "value": "2026-04"}``
    (and analogous quarter, year, fiscal-year, and week-ending forms).
    """

    if not isinstance(value, dict) or set(value) != {"type", "value"}:
        return None
    period_type = value.get("type")
    period_value = value.get("value")
    if (
        not isinstance(period_type, str)
        or period_type not in _PERIOD_TYPES
        or not isinstance(period_value, str)
    ):
        return None

    if period_type == "month":
        match = _MONTH_RE.fullmatch(period_value)
        if match is None:
            return None
        try:
            parsed = date(int(match.group(1)), int(match.group(2)), 1)
        except ValueError:
            return None
        canonical_value = f"{parsed.year:04d}-{parsed.month:02d}"
    elif period_type == "quarter":
        match = _QUARTER_RE.fullmatch(period_value)
        if match is None:
            return None
        year = int(match.group(1))
        try:
            date(year, 1, 1)
        except ValueError:
            return None
        canonical_value = f"{year:04d}-Q{match.group(2)}"
    elif period_type in {"year", "fiscal_year"}:
        if _YEAR_RE.fullmatch(period_value) is None:
            return None
        year = int(period_value)
        try:
            date(year, 1, 1)
        except ValueError:
            return None
        canonical_value = f"{year:04d}"
    else:
        if _WEEK_ENDING_RE.fullmatch(period_value) is None:
            return None
        try:
            canonical_value = date.fromisoformat(period_value).isoformat()
        except ValueError:
            return None
    return period_type, canonical_value


def _closed_label_period_identity(
    label: Any,
) -> tuple[tuple[str, str] | None, str | None]:
    """Parse the entire label with the closed single-period grammar."""

    if not isinstance(label, str) or not label.strip(" "):
        return None, None
    if len(label) > MAX_PERIOD_LABEL_LENGTH:
        return None, f"exceeds {MAX_PERIOD_LABEL_LENGTH} characters"
    if any(not 0x20 <= ord(char) <= 0x7E for char in label):
        return None, "contains characters outside printable ASCII"

    stripped = label.strip(" ")
    match = _LABEL_WEEK_ENDING_RE.fullmatch(stripped)
    if match is not None:
        raw_period = {
            "type": "week_ending",
            "value": "-".join(match.groups()),
        }
    else:
        match = _LABEL_QUARTER_RE.fullmatch(stripped)
        if match is not None:
            raw_period = {
                "type": "quarter",
                "value": (
                    f"{match.group('year_first')}-Q{match.group('quarter_after')}"
                    if match.group("year_first")
                    else (
                        f"{match.group('year_after')}-Q{match.group('quarter_first')}"
                    )
                ),
            }
        else:
            match = _LABEL_MONTH_RE.fullmatch(stripped)
            if match is not None:
                raw_period = {
                    "type": "month",
                    "value": f"{match.group(1)}-{match.group(2)}",
                }
            else:
                match = _LABEL_MONTH_NAME_RE.fullmatch(stripped)
                if match is not None:
                    raw_period = {
                        "type": "month",
                        "value": (
                            f"{match.group('month_year_after')}-"
                            f"{_MONTH_NAMES[match.group('month_first').lower()]:02d}"
                            if match.group("month_first")
                            else (
                                f"{match.group('month_year_first')}-"
                                f"{_MONTH_NAMES[match.group('month_after').lower()]:02d}"
                            )
                        ),
                    }
                else:
                    match = _LABEL_FISCAL_YEAR_RE.fullmatch(stripped)
                    if match is not None:
                        raw_period = {
                            "type": "fiscal_year",
                            "value": match.group("fy_compact")
                            or match.group("fy_words"),
                        }
                    else:
                        match = _LABEL_YEAR_RE.fullmatch(stripped)
                        if match is None:
                            return (
                                None,
                                "does not match the closed single-period label grammar",
                            )
                        raw_period = {"type": "year", "value": match.group(1)}

    identity = canonical_period_identity(raw_period)
    if identity is None:
        return None, "contains an invalid canonical period"
    return identity, None


def canonical_period_identities_from_label(label: Any) -> set[tuple[str, str]]:
    """Parse one label only when the entire label names one canonical period."""

    identity, problem = _closed_label_period_identity(label)
    return {identity} if identity is not None and problem is None else set()


def _period_label_syntax_problem(label: Any) -> str | None:
    """Return why a label falls outside the closed single-period grammar."""

    _identity, problem = _closed_label_period_identity(label)
    return problem


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
        finite_numeric = False
        if not isinstance(value, bool) and isinstance(value, (int, float)):
            try:
                finite_numeric = math.isfinite(float(value))
            except (OverflowError, ValueError):
                finite_numeric = False
        if not finite_numeric:
            errors.append(f"historicalContext[{index}] has no finite numeric value")
        identity = canonical_period_identity(entry.get("period"))
        if identity is None:
            errors.append(
                f"historicalContext[{index}] has no valid canonical period identity"
            )
            continue
        label_identities = canonical_period_identities_from_label(label)
        label_problem = _period_label_syntax_problem(label)
        if len(label_identities) > 1:
            errors.append(
                f"historicalContext[{index}] label identifies multiple canonical "
                "periods"
            )
        elif label_problem is not None:
            errors.append(
                f"historicalContext[{index}] label has ambiguous or unsupported "
                f"period syntax: {label_problem}"
            )
        elif not label_identities:
            errors.append(
                f"historicalContext[{index}] label does not identify a canonical period"
            )
        elif next(iter(label_identities)) != identity:
            label_type, label_value = next(iter(label_identities))
            period_type, period_value = identity
            errors.append(
                f"historicalContext[{index}] label period {label_type} "
                f"{label_value} does not match canonical period {period_type} "
                f"{period_value}"
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
