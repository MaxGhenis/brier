#!/usr/bin/env python3
"""Mint and inspect one-use authorizations for attested local generation.

Tickets are permanent records.  They bind a public nonce, a registered target
set, and the exact generation policy that an untrusted local runner may use.
The eventual batch day is deliberately absent: the batch manifest is named by
the ticket but lives under the UTC day on which the batch actually starts.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import pathlib
import re
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
TICKET_SCHEMA = "generation_ticket_v1"

TICKET_KEYS = {
    "schemaVersion",
    "ticketId",
    "nonce",
    "mintedAtUtc",
    "expiresAtUtc",
    "attempt",
    "supersedesTicketId",
    "supersededOutcome",
    "targets",
    "registrationSetHash",
    "policy",
}
TARGET_REQUIRED_KEYS = {
    "registrationCommit",
    "targetContentHash",
    "targetRegistrationPath",
    "registeredAtUtc",
    "catalogSlug",
    "series",
    "period",
}
POLICY_KEYS = {
    "promptMode",
    "codexModel",
    "codexReasoningEffort",
    "codexSandbox",
    "codexNetwork",
    "reviewCodexModel",
    "reviewCodexSearch",
    "timeoutSeconds",
}
SUPERSEDED_OUTCOMES = {"failed", "expired", "abandoned"}
PROMPT_MODES = {"full", "fast", "ladder", "ladder_v2"}
CODEX_SANDBOXES = {"read-only", "workspace-write"}

TICKET_ID_RE = re.compile(r"^(?P<day>\d{4}-\d{2}-\d{2})-(?P<opaque>[0-9a-f]+)$")
TARGET_REGISTRATION_RE = re.compile(
    r"^records/targets/\d{4}-\d{2}-\d{2}-[0-9a-f]{64}\.json$"
)


class TicketError(ValueError):
    """A generation ticket is malformed or has ambiguous provenance."""


# A descriptive alias is useful to callers without creating a second error
# type that they would need to catch.
GenerationTicketError = TicketError


def _parse_utc_instant(value: Any, field: str) -> dt.datetime:
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value
    ):
        raise TicketError(
            f"ticket {field} must be a second-precision UTC instant: {value!r}"
        )
    try:
        return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=dt.timezone.utc
        )
    except ValueError as exc:
        raise TicketError(
            f"ticket {field} is not a valid UTC instant: {value!r}"
        ) from exc


def _parse_ticket_id(value: Any, field: str = "ticketId") -> tuple[str, str]:
    if not isinstance(value, str):
        raise TicketError(
            f"ticket {field} must be <YYYY-MM-DD>-<lowercase hex>: {value!r}"
        )
    match = TICKET_ID_RE.fullmatch(value)
    if match is None:
        raise TicketError(
            f"ticket {field} must be <YYYY-MM-DD>-<lowercase hex>: {value!r}"
        )
    try:
        dt.date.fromisoformat(match.group("day"))
    except ValueError as exc:
        raise TicketError(f"ticket {field} has an invalid date: {value!r}") from exc
    return match.group("day"), match.group("opaque")


def _require_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TicketError(f"{label} must be a nonempty string")
    return value


def _require_json_value(value: Any, label: str) -> None:
    try:
        json.dumps(value, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise TicketError(f"{label} contains a non-JSON value: {exc}") from exc


def _validate_target(target: Any, index: int) -> None:
    if not isinstance(target, dict):
        raise TicketError(f"ticket target {index} must be an object")
    if not all(isinstance(key, str) for key in target):
        raise TicketError(f"ticket target {index} keys must be strings")
    missing = TARGET_REQUIRED_KEYS - set(target)
    if missing:
        raise TicketError(f"ticket target {index} is missing fields: {sorted(missing)}")

    registration_commit = target["registrationCommit"]
    if not isinstance(registration_commit, str) or not re.fullmatch(
        r"[0-9a-f]{40}", registration_commit
    ):
        raise TicketError(
            f"ticket target {index} registrationCommit must be a 40-character "
            "lowercase hex commit"
        )
    content_hash = target["targetContentHash"]
    if not isinstance(content_hash, str) or not re.fullmatch(
        r"[0-9a-f]{64}", content_hash
    ):
        raise TicketError(
            f"ticket target {index} targetContentHash must be a lowercase "
            "SHA-256 digest"
        )
    registration_path = target["targetRegistrationPath"]
    if not isinstance(registration_path, str) or not TARGET_REGISTRATION_RE.fullmatch(
        registration_path
    ):
        raise TicketError(
            f"ticket target {index} targetRegistrationPath is not a target "
            f"registration path: {registration_path!r}"
        )
    _parse_utc_instant(target["registeredAtUtc"], f"target {index} registeredAtUtc")
    for field in ("catalogSlug", "series", "period"):
        _require_nonempty_string(target[field], f"ticket target {index} {field}")


def _validate_policy(policy: Any) -> None:
    if not isinstance(policy, dict):
        raise TicketError("ticket policy must be an object")
    extra = set(policy) - POLICY_KEYS
    if extra:
        raise TicketError(f"ticket policy has unknown keys: {sorted(extra)}")
    missing = POLICY_KEYS - set(policy)
    if missing:
        raise TicketError(f"ticket policy is missing keys: {sorted(missing)}")

    for field in (
        "codexModel",
        "codexReasoningEffort",
        "reviewCodexModel",
    ):
        _require_nonempty_string(policy[field], f"ticket policy {field}")
    if policy["promptMode"] not in PROMPT_MODES:
        raise TicketError(
            f"ticket policy promptMode must be one of {sorted(PROMPT_MODES)}"
        )
    if policy["codexSandbox"] not in CODEX_SANDBOXES:
        raise TicketError(
            f"ticket policy codexSandbox must be one of {sorted(CODEX_SANDBOXES)}"
        )
    for field in ("codexNetwork", "reviewCodexSearch"):
        if type(policy[field]) is not bool:
            raise TicketError(f"ticket policy {field} must be a boolean")
    if policy["codexNetwork"] and policy["codexSandbox"] != "workspace-write":
        raise TicketError(
            "ticket policy codexNetwork requires codexSandbox workspace-write"
        )
    if type(policy["timeoutSeconds"]) is not int or policy["timeoutSeconds"] <= 0:
        raise TicketError("ticket policy timeoutSeconds must be a positive integer")


def validate_ticket(ticket: Any) -> dict[str, Any]:
    """Validate and return a generation ticket without weakening its shape."""

    if not isinstance(ticket, dict):
        raise TicketError("generation ticket must be an object")
    extra = set(ticket) - TICKET_KEYS
    if extra:
        raise TicketError(f"generation ticket has unknown keys: {sorted(extra)}")
    missing = TICKET_KEYS - set(ticket)
    if missing:
        raise TicketError(f"generation ticket is missing keys: {sorted(missing)}")
    if ticket["schemaVersion"] != TICKET_SCHEMA:
        raise TicketError(
            f"unsupported generation ticket schema {ticket['schemaVersion']!r}"
        )

    ticket_day, _ = _parse_ticket_id(ticket["ticketId"])
    nonce = ticket["nonce"]
    if not isinstance(nonce, str) or not re.fullmatch(r"[0-9a-f]{64}", nonce):
        raise TicketError("ticket nonce must be 64 lowercase hex characters")

    minted = _parse_utc_instant(ticket["mintedAtUtc"], "mintedAtUtc")
    expires = _parse_utc_instant(ticket["expiresAtUtc"], "expiresAtUtc")
    if expires <= minted:
        raise TicketError("ticket expiresAtUtc must be later than mintedAtUtc")
    if ticket_day != minted.date().isoformat():
        raise TicketError(
            "ticketId date must equal the mintedAtUtc date: "
            f"{ticket_day} != {minted.date().isoformat()}"
        )

    attempt = ticket["attempt"]
    if type(attempt) is not int or attempt < 1:
        raise TicketError(
            "ticket attempt must be an integer greater than or equal to 1"
        )

    supersedes = ticket["supersedesTicketId"]
    superseded_outcome = ticket["supersededOutcome"]
    if supersedes is not None and superseded_outcome is None:
        raise TicketError("ticket supersedesTicketId requires supersededOutcome")
    if supersedes is None and superseded_outcome is not None:
        raise TicketError("ticket supersededOutcome requires supersedesTicketId")
    if supersedes is not None:
        _parse_ticket_id(supersedes, "supersedesTicketId")
        if supersedes == ticket["ticketId"]:
            raise TicketError("ticket cannot supersede itself")
        if not isinstance(superseded_outcome, dict) or set(superseded_outcome) != {
            "outcome",
            "reason",
        }:
            raise TicketError(
                "ticket supersededOutcome must be an object with exactly outcome "
                "and reason"
            )
        outcome = superseded_outcome["outcome"]
        if not isinstance(outcome, str) or outcome not in SUPERSEDED_OUTCOMES:
            raise TicketError(
                "ticket supersededOutcome outcome must be one of "
                f"{sorted(SUPERSEDED_OUTCOMES)}"
            )
        _require_nonempty_string(
            superseded_outcome["reason"], "ticket supersededOutcome reason"
        )

    targets = ticket["targets"]
    if not isinstance(targets, list) or not targets:
        raise TicketError("ticket targets must be a nonempty object list")
    for index, target in enumerate(targets):
        _validate_target(target, index)

    registration_set_hash = ticket["registrationSetHash"]
    if not isinstance(registration_set_hash, str) or not re.fullmatch(
        r"[0-9a-f]{64}", registration_set_hash
    ):
        raise TicketError(
            "ticket registrationSetHash must be a lowercase SHA-256 digest"
        )
    _validate_policy(ticket["policy"])

    _require_json_value(ticket, "generation ticket")
    return ticket


def mint_ticket(
    targets: list[dict[str, Any]],
    policy: dict[str, Any],
    *,
    nonce: str,
    minted_at_utc: str,
    expires_at_utc: str,
    attempt: int,
    supersedes: str | None = None,
    superseded_outcome: dict[str, str] | None = None,
    registration_set_hash: str,
) -> dict[str, Any]:
    """Build a validated ticket from trusted registration and policy inputs."""

    minted = _parse_utc_instant(minted_at_utc, "mintedAtUtc")
    if not isinstance(nonce, str) or not re.fullmatch(r"[0-9a-f]{64}", nonce):
        raise TicketError("ticket nonce must be 64 lowercase hex characters")
    _require_json_value(targets, "ticket targets")
    _require_json_value(policy, "ticket policy")
    _require_json_value(superseded_outcome, "ticket supersededOutcome")
    ticket = {
        "schemaVersion": TICKET_SCHEMA,
        "ticketId": f"{minted.date().isoformat()}-{nonce}",
        "nonce": nonce,
        "mintedAtUtc": minted_at_utc,
        "expiresAtUtc": expires_at_utc,
        "attempt": attempt,
        "supersedesTicketId": supersedes,
        "supersededOutcome": copy.deepcopy(superseded_outcome),
        "targets": copy.deepcopy(targets),
        "registrationSetHash": registration_set_hash,
        "policy": copy.deepcopy(policy),
    }
    return validate_ticket(ticket)


def load_ticket(path: str | pathlib.Path) -> dict[str, Any]:
    """Parse and fully validate a ticket JSON file."""

    ticket_path = pathlib.Path(path)
    try:
        ticket = json.loads(ticket_path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise TicketError(
            f"cannot load generation ticket {ticket_path}: {exc}"
        ) from exc
    return validate_ticket(ticket)


def ticket_batch_filename(ticket: dict[str, Any]) -> str:
    """Return the batch filename pinned by a ticket, without pinning its day."""

    if not isinstance(ticket, dict) or "ticketId" not in ticket:
        raise TicketError("generation ticket has no ticketId")
    _parse_ticket_id(ticket["ticketId"])
    return f"attested-{ticket['ticketId']}.json"


def _git_relative_path(
    path: str | pathlib.Path, cwd: str | pathlib.Path
) -> tuple[pathlib.Path, pathlib.PurePosixPath]:
    repo = pathlib.Path(cwd).resolve()
    candidate = pathlib.Path(path)
    if not candidate.is_absolute():
        candidate = repo / candidate
    try:
        relative = candidate.resolve().relative_to(repo)
    except ValueError as exc:
        raise TicketError(f"ticket path is outside the repository: {path}") from exc
    if not relative.parts:
        raise TicketError(f"ticket path is not a file: {path}")
    return repo, pathlib.PurePosixPath(relative.as_posix())


def ticket_introducing_commit(
    ticket_path: str | pathlib.Path, cwd: str | pathlib.Path
) -> str:
    """Return the sole commit on HEAD history that added ``ticket_path``."""

    repo, relative = _git_relative_path(ticket_path, cwd)
    completed = subprocess.run(
        [
            "git",
            "log",
            "--full-history",
            "--diff-filter=A",
            "--format=%H",
            "HEAD",
            "--",
            relative.as_posix(),
        ],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or f"git exited {completed.returncode}"
        raise TicketError(f"cannot inspect introducing commit for {relative}: {detail}")
    commits = [line for line in completed.stdout.splitlines() if line]
    if len(commits) != 1:
        raise TicketError(
            "generation ticket must have exactly one introducing commit on "
            f"HEAD history: {relative}; found {len(commits)}"
        )
    return commits[0]


def _relative_match(path: pathlib.Path, repo_root: pathlib.Path) -> str:
    return path.relative_to(repo_root).as_posix()


def find_ticket_consumption(
    ticket_id: str, repo_root: str | pathlib.Path
) -> str | None:
    """Return the repository-relative batch path that consumed ``ticket_id``."""

    _parse_ticket_id(ticket_id)
    root = pathlib.Path(repo_root).resolve()
    matches = sorted(
        path
        for path in (root / "records" / "thesis-analyst" / "batches").glob(
            f"*/attested-{ticket_id}.json"
        )
        if path.is_file()
    )
    if not matches:
        return None
    if len(matches) != 1:
        raise TicketError(
            f"generation ticket {ticket_id} has multiple consuming batches: "
            f"{[_relative_match(path, root) for path in matches]}"
        )
    return _relative_match(matches[0], root)


def find_ticket_successor(ticket_id: str, repo_root: str | pathlib.Path) -> str | None:
    """Return the repository-relative ticket path that supersedes a ticket."""

    _parse_ticket_id(ticket_id)
    root = pathlib.Path(repo_root).resolve()
    tickets_root = root / "records" / "tickets"
    matches: list[pathlib.Path] = []
    for path in sorted(tickets_root.glob("*/*.json")):
        if not path.is_file():
            continue
        ticket = load_ticket(path)
        expected = tickets_root / ticket["ticketId"][:10] / f"{ticket['ticketId']}.json"
        if path != expected:
            raise TicketError(
                "generation ticket path does not match its identity: "
                f"{_relative_match(path, root)} != {_relative_match(expected, root)}"
            )
        if ticket["supersedesTicketId"] == ticket_id:
            matches.append(path)
    if not matches:
        return None
    if len(matches) != 1:
        raise TicketError(
            f"generation ticket {ticket_id} has multiple successors: "
            f"{[_relative_match(path, root) for path in matches]}"
        )
    return _relative_match(matches[0], root)


def _load_json(path: str | pathlib.Path, label: str) -> Any:
    source = pathlib.Path(path)
    try:
        return json.loads(source.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise TicketError(f"cannot load {label} {source}: {exc}") from exc


def load_target_file(path: str | pathlib.Path) -> list[dict[str, Any]]:
    """Load the exact object-list shape emitted by ``roll_docket.py``."""

    payload = _load_json(path, "target file")
    if not isinstance(payload, dict) or set(payload) != {"targets"}:
        raise TicketError("target file must be an object containing only targets")
    targets = payload["targets"]
    if not isinstance(targets, list) or not all(
        isinstance(target, dict) for target in targets
    ):
        raise TicketError("target file targets must be an object list")
    return targets


def parse_requested_slugs(values: list[str]) -> list[str]:
    """Parse comma/newline-separated exact catalog slugs."""

    slugs: list[str] = []
    for value in values:
        slugs.extend(part.strip() for part in re.split(r"[,\n]", value) if part.strip())
    if not slugs:
        raise TicketError("--slugs must name at least one catalog slug")
    if len(slugs) != len(set(slugs)):
        raise TicketError("requested catalog slugs contain duplicates")
    for slug in slugs:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
            raise TicketError(f"invalid requested catalog slug: {slug!r}")
    return slugs


def select_targets(
    targets: list[dict[str, Any]],
    *,
    series: str | None = None,
    slugs: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Select an exact series or exact slug set without inventing targets."""

    if bool(series) == bool(slugs):
        raise TicketError("ticket mint requires exactly one of series or slugs")
    by_slug: dict[str, dict[str, Any]] = {}
    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            raise TicketError(f"target selection item {index} must be an object")
        slug = target.get("catalogSlug")
        target_series = target.get("series")
        if not isinstance(slug, str) or not slug:
            raise TicketError(f"target selection item {index} lacks catalogSlug")
        if not isinstance(target_series, str) or not target_series:
            raise TicketError(f"target selection item {index} lacks series")
        if slug in by_slug:
            raise TicketError(f"target selection has duplicate catalog slug: {slug}")
        by_slug[slug] = target

    if series:
        selected = [target for target in targets if target["series"] == series]
        if not selected:
            raise TicketError(f"requested series has no targets: {series}")
        return copy.deepcopy(selected)

    assert slugs is not None
    missing = sorted(set(slugs) - set(by_slug))
    if missing:
        raise TicketError(f"requested catalog slugs are not targets: {missing}")
    requested = set(slugs)
    conditional_groups: dict[tuple[str, str], set[str]] = {}
    for target in targets:
        if isinstance(target.get("conditional"), str) and target["conditional"].strip():
            key = (target["series"], str(target.get("period") or ""))
            conditional_groups.setdefault(key, set()).add(target["catalogSlug"])
    for (target_series, period), required in sorted(conditional_groups.items()):
        included = requested & required
        if included and included != required:
            raise TicketError(
                f"conditional target selection for {target_series} {period} "
                f"requires all slugs: {sorted(required)}"
            )
    return copy.deepcopy(
        [target for target in targets if target["catalogSlug"] in requested]
    )


def _conventional_ticket_path(ticket_id: str) -> pathlib.PurePosixPath:
    day, _ = _parse_ticket_id(ticket_id)
    return pathlib.PurePosixPath("records", "tickets", day, f"{ticket_id}.json")


def validate_ticket_supersession(
    ticket_id: str,
    repo_root: str | pathlib.Path,
    *,
    attempt: int,
    allow_successor_path: str | pathlib.Path | None = None,
) -> dict[str, Any]:
    """Verify that a predecessor is available for exactly its next attempt."""

    root = pathlib.Path(repo_root).resolve()
    relative = _conventional_ticket_path(ticket_id)
    predecessor_path = root.joinpath(*relative.parts)
    if not predecessor_path.is_file():
        raise TicketError(f"superseded generation ticket does not exist: {relative}")
    predecessor = load_ticket(predecessor_path)
    if predecessor["ticketId"] != ticket_id:
        raise TicketError(
            f"superseded generation ticket path does not match its ticketId: {relative}"
        )
    expected_attempt = predecessor["attempt"] + 1
    if type(attempt) is not int or attempt != expected_attempt:
        raise TicketError(
            f"generation ticket attempt must be {expected_attempt} when superseding "
            f"{ticket_id}; got {attempt!r}"
        )
    consumption = find_ticket_consumption(ticket_id, root)
    if consumption is not None:
        raise TicketError(
            f"generation ticket {ticket_id} was already consumed by {consumption}"
        )

    successor = find_ticket_successor(ticket_id, root)
    allowed: str | None = None
    if allow_successor_path is not None:
        _, allowed_relative = _git_relative_path(allow_successor_path, root)
        allowed = allowed_relative.as_posix()
        expected_allowed = _conventional_ticket_path(
            pathlib.PurePosixPath(allowed).stem
        ).as_posix()
        if allowed != expected_allowed:
            raise TicketError(
                f"allowed successor path is not canonical: {allowed} != "
                f"{expected_allowed}"
            )
    if successor is not None and successor != allowed:
        raise TicketError(
            f"generation ticket {ticket_id} was already superseded by {successor}"
        )
    if allowed is not None and successor is None:
        raise TicketError(
            f"generation ticket {ticket_id} has no successor at allowed path {allowed}"
        )
    return predecessor


def load_registration_binding(
    targets: list[dict[str, Any]], metadata_path: str | pathlib.Path
) -> str:
    """Cross-check bind metadata against the fully hydrated target file."""

    metadata = _load_json(metadata_path, "registration metadata")
    expected_keys = {
        "schemaVersion",
        "sourceCommit",
        "registrationSetHash",
        "registrationCommits",
        "targetContentHashes",
        "targets",
    }
    if not isinstance(metadata, dict) or set(metadata) != expected_keys:
        raise TicketError(
            "registration metadata fields do not match bound registration output"
        )
    if metadata["schemaVersion"] != "thesis_target_registration_set_v1":
        raise TicketError(
            f"unsupported registration metadata schema {metadata['schemaVersion']!r}"
        )
    if not isinstance(metadata["sourceCommit"], str) or not re.fullmatch(
        r"[0-9a-f]{40}", metadata["sourceCommit"]
    ):
        raise TicketError("registration metadata sourceCommit is not a commit SHA")
    registration_set_hash = metadata["registrationSetHash"]
    if not isinstance(registration_set_hash, str) or not re.fullmatch(
        r"[0-9a-f]{64}", registration_set_hash
    ):
        raise TicketError(
            "registration metadata registrationSetHash is not a SHA-256 digest"
        )

    binding_keys = {
        "catalogSlug",
        "registrationCommit",
        "targetContentHash",
        "targetRegistrationPath",
    }
    rows = metadata["targets"]
    if not isinstance(rows, list) or not all(
        isinstance(row, dict) and set(row) == binding_keys for row in rows
    ):
        raise TicketError("registration metadata targets are not exact binding rows")
    metadata_by_slug = {row["catalogSlug"]: row for row in rows}
    target_by_slug = {
        target.get("catalogSlug"): target
        for target in targets
        if isinstance(target, dict)
    }
    if (
        len(metadata_by_slug) != len(rows)
        or len(target_by_slug) != len(targets)
        or None in target_by_slug
        or set(metadata_by_slug) != set(target_by_slug)
    ):
        raise TicketError("registration metadata target inventory differs from targets")
    for slug, row in metadata_by_slug.items():
        target = target_by_slug[slug]
        for key in binding_keys:
            if target.get(key) != row[key]:
                raise TicketError(
                    f"registration metadata binding mismatch for {slug}: {key}"
                )
    commits = sorted({str(row["registrationCommit"]) for row in rows})
    hashes = sorted({str(row["targetContentHash"]) for row in rows})
    if metadata["registrationCommits"] != commits:
        raise TicketError("registration metadata registrationCommits mismatch")
    if metadata["targetContentHashes"] != hashes:
        raise TicketError("registration metadata targetContentHashes mismatch")
    return registration_set_hash


def write_minted_ticket(ticket: dict[str, Any], repo_root: str | pathlib.Path) -> str:
    """Write a ticket at its sole conventional repository-relative path."""

    root = pathlib.Path(repo_root).resolve()
    relative = _conventional_ticket_path(ticket["ticketId"])
    destination = root.joinpath(*relative.parts)
    if destination.exists():
        raise TicketError(f"refusing to overwrite generation ticket: {relative}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(ticket, indent=2, sort_keys=True) + "\n")
    return relative.as_posix()


def _select_command(args: argparse.Namespace) -> dict[str, Any]:
    targets = load_target_file(args.targets_file)
    slugs = parse_requested_slugs(args.slugs) if args.slugs else None
    selected = select_targets(targets, series=args.series, slugs=slugs)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"targets": selected}, indent=2, sort_keys=True) + "\n"
    )
    return {"out": str(args.out), "targets": len(selected)}


def _check_supersession_command(args: argparse.Namespace) -> dict[str, Any]:
    predecessor = validate_ticket_supersession(
        args.ticket_id,
        args.repo_root,
        attempt=args.attempt,
        allow_successor_path=args.allow_successor_path,
    )
    return {
        "predecessorTicketId": predecessor["ticketId"],
        "predecessorPath": _conventional_ticket_path(
            predecessor["ticketId"]
        ).as_posix(),
    }


def _mint_command(args: argparse.Namespace) -> dict[str, Any]:
    supersession_values = (
        args.supersedes_ticket_id,
        args.superseded_outcome,
        args.superseded_reason,
    )
    if any(value is not None for value in supersession_values) and not all(
        value is not None for value in supersession_values
    ):
        raise TicketError(
            "--supersedes-ticket-id, --superseded-outcome, and "
            "--superseded-reason must be provided together"
        )
    if args.supersedes_ticket_id is None and args.attempt != 1:
        raise TicketError(
            f"ticket attempt must be 1 without supersedesTicketId; got {args.attempt!r}"
        )
    targets = load_target_file(args.targets_file)
    registration_set_hash = load_registration_binding(
        targets, args.registration_metadata
    )
    if args.supersedes_ticket_id is not None:
        validate_ticket_supersession(
            args.supersedes_ticket_id,
            args.repo_root,
            attempt=args.attempt,
        )
    outcome = None
    if args.superseded_outcome is not None or args.superseded_reason is not None:
        outcome = {
            "outcome": args.superseded_outcome,
            "reason": args.superseded_reason,
        }
    ticket = mint_ticket(
        targets,
        {
            "promptMode": args.prompt_mode,
            "codexModel": args.codex_model,
            "codexReasoningEffort": args.codex_reasoning_effort,
            "codexSandbox": args.codex_sandbox,
            "codexNetwork": args.codex_network,
            "reviewCodexModel": args.review_codex_model,
            "reviewCodexSearch": args.review_codex_search,
            "timeoutSeconds": args.timeout_seconds,
        },
        nonce=args.nonce,
        minted_at_utc=args.minted_at_utc,
        expires_at_utc=args.expires_at_utc,
        attempt=args.attempt,
        supersedes=args.supersedes_ticket_id,
        superseded_outcome=outcome,
        registration_set_hash=registration_set_hash,
    )
    ticket_path = write_minted_ticket(ticket, args.repo_root)
    return {"ticketId": ticket["ticketId"], "ticketPath": ticket_path}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    select = subparsers.add_parser("select")
    select.add_argument("--targets-file", type=pathlib.Path, required=True)
    select.add_argument("--series")
    select.add_argument("--slugs", action="append")
    select.add_argument("--out", type=pathlib.Path, required=True)
    select.set_defaults(handler=_select_command)

    check = subparsers.add_parser("check-supersession")
    check.add_argument("--ticket-id", required=True)
    check.add_argument("--attempt", type=int, required=True)
    check.add_argument("--repo-root", type=pathlib.Path, default=ROOT)
    check.add_argument("--allow-successor-path")
    check.set_defaults(handler=_check_supersession_command)

    mint = subparsers.add_parser("mint")
    mint.add_argument("--targets-file", type=pathlib.Path, required=True)
    mint.add_argument("--registration-metadata", type=pathlib.Path, required=True)
    mint.add_argument("--nonce", required=True)
    mint.add_argument("--minted-at-utc", required=True)
    mint.add_argument("--expires-at-utc", required=True)
    mint.add_argument("--attempt", type=int, required=True)
    mint.add_argument("--supersedes-ticket-id")
    mint.add_argument("--superseded-outcome", choices=sorted(SUPERSEDED_OUTCOMES))
    mint.add_argument("--superseded-reason")
    mint.add_argument("--prompt-mode", choices=sorted(PROMPT_MODES), required=True)
    mint.add_argument("--codex-model", required=True)
    mint.add_argument("--codex-reasoning-effort", required=True)
    mint.add_argument("--codex-sandbox", choices=sorted(CODEX_SANDBOXES), required=True)
    mint.add_argument("--codex-network", action="store_true")
    mint.add_argument("--review-codex-model", required=True)
    mint.add_argument("--review-codex-search", action="store_true")
    mint.add_argument("--timeout-seconds", type=int, required=True)
    mint.add_argument("--repo-root", type=pathlib.Path, default=ROOT)
    mint.set_defaults(handler=_mint_command)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = args.handler(args)
    except (OSError, TicketError) as exc:
        print(f"generation ticket failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
