#!/usr/bin/env python3
"""Mint and inspect one-use authorizations for attested local generation.

Tickets are permanent records.  They bind a public nonce, a registered target
set, and the exact generation policy that an untrusted local runner may use.
The eventual batch day is deliberately absent: the batch manifest is named by
the ticket but lives under the UTC day on which the batch actually starts.
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import pathlib
import re
import subprocess
from typing import Any

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
            "ticket policy promptMode must be one of "
            f"{sorted(PROMPT_MODES)}"
        )
    if policy["codexSandbox"] not in CODEX_SANDBOXES:
        raise TicketError(
            "ticket policy codexSandbox must be one of "
            f"{sorted(CODEX_SANDBOXES)}"
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
