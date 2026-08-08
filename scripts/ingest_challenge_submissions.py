#!/usr/bin/env python3
"""Adapt merged challenge-inbox cells into recorder forecast records.

The adapter is deliberately read-only. It returns (or, as a standalone
command, prints) normalized records for the established forecast-snapshot
writer to include. A malformed submission is isolated to that file and
reported on stderr so one challenger cannot stop the daily recorder batch.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SUBMISSION_SCHEMA_VERSION = "thesis_challenge_submission_v1"
EXPECTED_QUANTILE_PS = (0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95)
SYSTEM_TYPES = {"ai", "human", "hybrid"}

LOGGER = logging.getLogger(__name__)
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
_COMMIT_RE = re.compile(r"[0-9a-fA-F]{40,64}\Z")


class ChallengeSubmissionError(ValueError):
    """A single challenge submission cannot be published."""


@dataclass(frozen=True)
class RegisteredTarget:
    data_point_id: str
    catalog_slug: str
    release_at: datetime


def parse_utc_datetime(value: Any, *, field: str, allow_date: bool = False) -> datetime:
    """Parse an offset-aware ISO instant and normalize it to UTC.

    Target registrations currently carry release windows as dates. A date
    is conservatively interpreted as the first instant of that UTC day: a
    day-granularity registration cannot prove that a same-day forecast came
    before the release.
    """

    if not isinstance(value, str) or not value:
        raise ChallengeSubmissionError(f"{field} must be an ISO-8601 string")
    candidate = value
    if allow_date and _DATE_RE.fullmatch(candidate):
        candidate = f"{candidate}T00:00:00+00:00"
    try:
        parsed = datetime.fromisoformat(candidate.replace("Z", "+00:00"))
    except (OverflowError, ValueError) as error:
        raise ChallengeSubmissionError(
            f"{field} is not a valid ISO-8601 datetime: {value!r}"
        ) from error
    if parsed.tzinfo is None:
        raise ChallengeSubmissionError(
            f"{field} must include an explicit UTC offset: {value!r}"
        )
    try:
        return parsed.astimezone(timezone.utc)
    except (OverflowError, ValueError) as error:
        raise ChallengeSubmissionError(
            f"{field} is outside the supported UTC datetime range: {value!r}"
        ) from error


def _utc_string(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _required_string(payload: dict[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ChallengeSubmissionError(f"{field} must be a non-empty string")
    return value


def _finite_number(value: Any, *, field: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ChallengeSubmissionError(f"{field} must be a finite number")
    try:
        finite = math.isfinite(value)
    except OverflowError as error:
        raise ChallengeSubmissionError(f"{field} must be a finite number") from error
    if not finite:
        raise ChallengeSubmissionError(f"{field} must be a finite number")
    return value


def load_registered_targets(targets_dir: Path) -> dict[str, RegisteredTarget]:
    """Index every recorded target registration by dataPointId.

    Registrations are append-only snapshots, so an ID may legitimately occur
    more than once. The earliest recorded release instant is the conservative
    chronology boundary and makes duplicate handling deterministic.
    """

    if not targets_dir.is_dir():
        raise ChallengeSubmissionError(
            f"registered-target directory does not exist: {targets_dir}"
        )

    registered: dict[str, RegisteredTarget] = {}
    for snapshot_path in sorted(targets_dir.glob("*.json")):
        try:
            payload = json.loads(snapshot_path.read_text())
        except (OSError, json.JSONDecodeError) as error:
            raise ChallengeSubmissionError(
                f"cannot read target registration {snapshot_path}: {error}"
            ) from error
        targets = payload.get("targets") if isinstance(payload, dict) else None
        if not isinstance(targets, list):
            raise ChallengeSubmissionError(
                f"target registration has no targets array: {snapshot_path}"
            )
        for target in targets:
            if not isinstance(target, dict):
                continue
            data_point_id = target.get("dataPointId")
            catalog_slug = target.get("catalogSlug")
            source_binding = target.get("sourceBinding")
            release_window = (
                source_binding.get("expectedReleaseWindow")
                if isinstance(source_binding, dict)
                else None
            )
            release_value = (
                release_window.get("start")
                if isinstance(release_window, dict)
                else None
            )
            if not isinstance(data_point_id, str) or not data_point_id:
                continue
            if not isinstance(catalog_slug, str) or not catalog_slug:
                continue
            try:
                release_at = parse_utc_datetime(
                    release_value,
                    field=(
                        "expectedReleaseWindow.start for registered target "
                        f"{data_point_id}"
                    ),
                    allow_date=True,
                )
            except ChallengeSubmissionError as error:
                LOGGER.warning(
                    "Skipping registered target in %s: %s",
                    snapshot_path,
                    error,
                )
                continue

            candidate = RegisteredTarget(data_point_id, catalog_slug, release_at)
            current = registered.get(data_point_id)
            if current is None or (
                candidate.release_at,
                candidate.catalog_slug,
            ) < (current.release_at, current.catalog_slug):
                registered[data_point_id] = candidate
    return registered


def validate_quantiles(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate the required seven-rung grid without rewriting it."""

    quantiles = payload.get("quantiles")
    if not isinstance(quantiles, list):
        raise ChallengeSubmissionError("quantiles must be an array")
    probabilities: list[int | float] = []
    values: list[int | float] = []
    for index, quantile in enumerate(quantiles):
        if not isinstance(quantile, dict):
            raise ChallengeSubmissionError(f"quantiles[{index}] must be an object")
        probabilities.append(
            _finite_number(quantile.get("p"), field=f"quantiles[{index}].p")
        )
        values.append(
            _finite_number(quantile.get("value"), field=f"quantiles[{index}].value")
        )
    if tuple(probabilities) != EXPECTED_QUANTILE_PS:
        raise ChallengeSubmissionError(
            "quantile probabilities must be exactly "
            f"{list(EXPECTED_QUANTILE_PS)} in increasing order"
        )
    if any(left >= right for left, right in zip(values, values[1:])):
        raise ChallengeSubmissionError("quantile values must be strictly increasing")
    return quantiles


def forecaster_id(challenger: str, system_name: str) -> str:
    """Build a reversible competing-system identity from both declared parts."""

    return f"{challenger}::{system_name}"


def submission_path(path: Path, repo_root: Path) -> str:
    try:
        return (
            path.resolve(strict=True)
            .relative_to(repo_root.resolve(strict=True))
            .as_posix()
        )
    except (OSError, ValueError) as error:
        raise ChallengeSubmissionError(
            f"submission path is not inside the repository: {path}"
        ) from error


def first_accepted_content(
    inbox_dir: Path, repo_root: Path
) -> dict[tuple[str, str], tuple[bytes, str]]:
    """Map each (challenger, dataPointId) to its first-accepted bytes and path.

    One shot per target binds the CONTENT, not a pathname: walking the
    inbox history oldest-first and recording the earliest parseable file
    for each key means an edit, a rename, or a delete-and-readd all
    leave the canonical bytes unchanged — any current file whose bytes
    differ from them is refused. A predecessor that never parsed (and so
    was never an accepted forecast) does not define canonical content.
    """

    inbox_rel = (
        inbox_dir.resolve(strict=True)
        .relative_to(repo_root.resolve(strict=True))
        .as_posix()
    )
    try:
        # Acceptance order is the FIRST-PARENT chain: a file counts as
        # accepted when it lands on the mainline, whether by a direct
        # commit or inside a merge result (-m diffs merges against their
        # first parent, so branch-introduced files appear as additions at
        # the merge that accepted them). Plain --reverse would walk the
        # whole DAG, letting a stale side branch merged later pre-date
        # the true first forecast.
        log = subprocess.run(
            [
                "git",
                "log",
                "--reverse",
                "--first-parent",
                "-m",
                "--format=%H",
                "--name-status",
                "--diff-filter=A",
                "--",
                inbox_rel,
            ],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise ChallengeSubmissionError(
            f"cannot walk the inbox history for {inbox_rel}: {error}"
        ) from error
    canonical: dict[tuple[str, str], bytes] = {}
    commit = ""
    for line in log.stdout.splitlines():
        if _COMMIT_RE.fullmatch(line.strip()):
            commit = line.strip()
            continue
        if not line.startswith("A\t"):
            continue
        added = line.split("\t", 1)[1]
        if not added.endswith(".json") or added.endswith(".sigstore.json"):
            continue
        try:
            raw = subprocess.run(
                ["git", "show", f"{commit}:{added}"],
                cwd=repo_root,
                check=True,
                capture_output=True,
            ).stdout
        except (OSError, subprocess.CalledProcessError):
            continue
        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Undecodable or unparseable history was never an accepted
            # forecast; it must not define canonical content or abort
            # the batch.
            continue
        if not isinstance(payload, dict):
            continue
        challenger = payload.get("challenger")
        data_point_id = payload.get("dataPointId")
        if not isinstance(challenger, str) or not isinstance(data_point_id, str):
            continue
        key = (challenger.lower(), data_point_id)
        canonical.setdefault(key, (raw, added))
    return canonical


def merge_commit_for(path: Path, repo_root: Path) -> str:
    """Return the exact commit requested by the challenge provenance contract."""

    relative = submission_path(path, repo_root)
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", relative],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise ChallengeSubmissionError(
            f"cannot resolve merge commit with git log for {relative}: {error}"
        ) from error
    commit = result.stdout.strip()
    if not _COMMIT_RE.fullmatch(commit):
        raise ChallengeSubmissionError(
            f"git log returned no full merge commit for {relative}"
        )
    return commit


def adapt_submission(
    path: Path,
    *,
    registered_targets: dict[str, RegisteredTarget],
    repo_root: Path,
) -> dict[str, Any]:
    """Validate and adapt one inbox JSON file into a snapshot prediction row."""

    if path.is_symlink() or not path.is_file():
        raise ChallengeSubmissionError("submission must be a regular file")
    try:
        payload = json.loads(path.read_text())
    except (OSError, RecursionError, UnicodeError, json.JSONDecodeError) as error:
        raise ChallengeSubmissionError(
            f"submission is not readable JSON: {error}"
        ) from error
    if not isinstance(payload, dict):
        raise ChallengeSubmissionError("submission must be a JSON object")
    if payload.get("schemaVersion") != SUBMISSION_SCHEMA_VERSION:
        raise ChallengeSubmissionError(
            "schemaVersion must be " + SUBMISSION_SCHEMA_VERSION
        )

    challenger = _required_string(payload, "challenger")
    system_type = _required_string(payload, "systemType")
    if system_type not in SYSTEM_TYPES:
        raise ChallengeSubmissionError(
            f"systemType must be one of {sorted(SYSTEM_TYPES)}"
        )
    system_name = _required_string(payload, "systemName")
    data_point_id = _required_string(payload, "dataPointId")
    target = registered_targets.get(data_point_id)
    if target is None:
        raise ChallengeSubmissionError(f"unregistered dataPointId: {data_point_id}")

    point_estimate = _finite_number(payload.get("pointEstimate"), field="pointEstimate")
    quantiles = validate_quantiles(payload)
    # ciLow/ciHigh and the 0.1/0.9 rungs describe the same 80% band; a
    # submission that disagrees with itself is refused rather than
    # silently resolved in favor of the grid.
    ci_low = _finite_number(payload.get("ciLow"), field="ciLow")
    ci_high = _finite_number(payload.get("ciHigh"), field="ciHigh")
    if ci_low != quantiles[1]["value"] or ci_high != quantiles[5]["value"]:
        raise ChallengeSubmissionError(
            "ciLow/ciHigh must equal the 0.1 and 0.9 quantile values"
        )
    generated_value = _required_string(payload, "generatedAtUtc")
    generated_at = parse_utc_datetime(generated_value, field="generatedAtUtc")
    if generated_at >= target.release_at:
        raise ChallengeSubmissionError(
            f"generatedAtUtc {generated_value} does not precede release "
            f"{_utc_string(target.release_at)}"
        )

    notes = payload.get("notes")
    if notes is not None and not isinstance(notes, str):
        raise ChallengeSubmissionError("notes must be a string when present")

    relative = submission_path(path, repo_root)
    record: dict[str, Any] = {
        "forecastSlug": target.catalog_slug,
        "dataPointId": data_point_id,
        "forecasterId": forecaster_id(challenger, system_name),
        "challenger": challenger,
        "systemType": system_type,
        "systemName": system_name,
        "pointEstimate": point_estimate,
        "interval80": {
            "lower": quantiles[1]["value"],
            "upper": quantiles[5]["value"],
        },
        # Keep the submitted rungs and values exactly as parsed; do not sort,
        # interpolate, or materialize a replacement distribution here.
        "quantiles": quantiles,
        "generatedAtUtc": generated_value,
        "recordedAt": generated_value,
        "resolutionDate": target.release_at.date().isoformat(),
        "provenance": {
            "submissionPath": relative,
            "mergeCommit": merge_commit_for(path, repo_root),
            "schemaVersion": SUBMISSION_SCHEMA_VERSION,
        },
    }
    if notes is not None:
        record["notes"] = notes
    return record


def ingest_challenge_submissions(
    *,
    inbox_dir: Path,
    targets_dir: Path,
    repo_root: Path,
) -> list[dict[str, Any]]:
    """Return valid challenge rows while isolating every invalid inbox file."""

    if not inbox_dir.is_dir():
        raise ChallengeSubmissionError(
            f"challenge inbox directory does not exist: {inbox_dir}"
        )
    registered_targets = load_registered_targets(targets_dir)
    records: list[dict[str, Any]] = []
    for path in sorted(inbox_dir.glob("*/*.json")):
        # Sigstore sidecars also end in .json but are provenance for a cell,
        # not forecast submissions themselves.
        if path.name.endswith(".sigstore.json"):
            continue
        try:
            record = adapt_submission(
                path,
                registered_targets=registered_targets,
                repo_root=repo_root,
            )
        except ChallengeSubmissionError as error:
            try:
                display_path = path.relative_to(repo_root).as_posix()
            except ValueError:
                display_path = str(path)
            LOGGER.warning("Skipping challenge submission %s: %s", display_path, error)
            continue
        records.append(record)
    canonical = first_accepted_content(inbox_dir, repo_root)
    records = _reject_replaced_content(records, canonical, repo_root)
    return _reject_duplicate_targets(records, canonical)


def _reject_replaced_content(
    records: list[dict[str, Any]],
    canonical: dict[tuple[str, str], tuple[bytes, str]],
    repo_root: Path,
) -> list[dict[str, Any]]:
    """Refuse any record whose bytes differ from the first-accepted bytes
    for its (challenger, dataPointId) — edits, renames, and
    delete-and-readd games all land here."""

    kept: list[dict[str, Any]] = []
    for record in records:
        key = (
            str(record.get("challenger")).lower(),
            str(record.get("dataPointId")),
        )
        relative = str(record.get("provenance", {}).get("submissionPath", ""))
        current = (repo_root / relative).read_bytes()
        entry = canonical.get(key)
        if entry is not None and current != entry[0]:
            LOGGER.warning(
                "Rejecting %s: content differs from the first accepted "
                "submission for %s / %s; one shot per target is final",
                relative,
                record.get("challenger"),
                record.get("dataPointId"),
            )
            continue
        kept.append(record)
    return kept


def _reject_duplicate_targets(
    records: list[dict[str, Any]],
    canonical: dict[tuple[str, str], tuple[bytes, str]],
) -> list[dict[str, Any]]:
    """Enforce one shot per (challenger, dataPointId).

    Records reaching here are byte-identical to the first-accepted
    content for their key, so duplicates are surplus copies: exactly one
    survives — the file at the first-accepted path when it still exists,
    else the lexicographically first path — and the rest reject with a
    warning. Keys are case-insensitive on the challenger because GitHub
    logins are.
    """

    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for record in records:
        key = (
            str(record.get("challenger")).lower(),
            str(record.get("dataPointId")),
        )
        groups.setdefault(key, []).append(record)
    kept: list[dict[str, Any]] = []
    for key, group in groups.items():
        if len(group) == 1:
            kept.extend(group)
            continue

        def _path(record: dict[str, Any]) -> str:
            return str(record.get("provenance", {}).get("submissionPath", ""))

        first_path = canonical.get(key, (b"", ""))[1]
        chosen = next(
            (record for record in group if _path(record) == first_path),
            min(group, key=_path),
        )
        for record in group:
            if record is chosen:
                continue
            LOGGER.warning(
                "Rejecting surplus copy %s for %s / %s: one shot per target",
                _path(record),
                record.get("challenger"),
                record.get("dataPointId"),
            )
        kept.append(chosen)
    kept.sort(
        key=lambda record: str(record.get("provenance", {}).get("submissionPath", ""))
    )
    return kept


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and print merged challenge forecast records"
    )
    default_root = Path(__file__).resolve().parent.parent
    parser.add_argument("--repo-root", type=Path, default=default_root)
    parser.add_argument("--inbox", type=Path)
    parser.add_argument("--targets", type=Path)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    repo_root = args.repo_root.resolve()
    records = ingest_challenge_submissions(
        inbox_dir=args.inbox or repo_root / "challenge" / "inbox",
        targets_dir=args.targets or repo_root / "records" / "targets",
        repo_root=repo_root,
    )
    json.dump(records, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
