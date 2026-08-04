from __future__ import annotations

import copy
import json
import pathlib
import subprocess
import sys
from typing import Any

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generation_tickets  # noqa: E402
from generation_tickets import TicketError  # noqa: E402

NONCE = "a" * 64
MINTED_AT = "2030-01-10T12:00:00Z"
EXPIRES_AT = "2030-01-17T12:00:00Z"


def sample_target() -> dict[str, Any]:
    return {
        "series": "canary.synthetic.series",
        "period": "2030-Q1",
        "catalogSlug": "synthetic-series-2030-q1",
        "registrationCommit": "b" * 40,
        "targetContentHash": "c" * 64,
        "targetRegistrationPath": f"records/targets/2030-01-10-{'c' * 64}.json",
        "registeredAtUtc": "2030-01-10T10:00:00Z",
        "conditional": "Synthetic condition",
    }


def sample_policy() -> dict[str, Any]:
    return {
        "promptMode": "fast",
        "codexModel": "gpt-test",
        "codexReasoningEffort": "low",
        "codexSandbox": "read-only",
        "codexNetwork": False,
        "reviewCodexModel": "gpt-review-test",
        "reviewCodexSearch": False,
        "timeoutSeconds": 540,
    }


def sample_ticket(**overrides: Any) -> dict[str, Any]:
    ticket = generation_tickets.mint_ticket(
        [sample_target()],
        sample_policy(),
        nonce=NONCE,
        minted_at_utc=MINTED_AT,
        expires_at_utc=EXPIRES_AT,
        attempt=1,
        registration_set_hash="d" * 64,
    )
    ticket.update(overrides)
    return ticket


def write_ticket(path: pathlib.Path, ticket: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ticket, sort_keys=True) + "\n")


def git(repo: pathlib.Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def commit(repo: pathlib.Path, message: str) -> str:
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=test",
            "-c",
            "user.email=test@example.com",
            "commit",
            "-m",
            message,
        ],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()


def test_mint_and_load_ticket_round_trip(tmp_path: pathlib.Path) -> None:
    targets = [sample_target()]
    policy = sample_policy()

    ticket = generation_tickets.mint_ticket(
        targets,
        policy,
        nonce=NONCE,
        minted_at_utc=MINTED_AT,
        expires_at_utc=EXPIRES_AT,
        attempt=1,
        registration_set_hash="d" * 64,
    )

    assert ticket["schemaVersion"] == generation_tickets.TICKET_SCHEMA
    assert ticket["ticketId"] == f"2030-01-10-{NONCE}"
    assert ticket["targets"] == targets
    assert ticket["policy"] == policy
    assert "batchPath" not in ticket
    assert (
        generation_tickets.ticket_batch_filename(ticket)
        == f"attested-2030-01-10-{NONCE}.json"
    )

    targets[0]["series"] = "mutated"
    policy["promptMode"] = "full"
    assert ticket["targets"][0]["series"] == "canary.synthetic.series"
    assert ticket["policy"]["promptMode"] == "fast"

    path = tmp_path / "ticket.json"
    write_ticket(path, ticket)
    assert generation_tickets.load_ticket(path) == ticket


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda ticket: ticket.update({"unknown": True}),
            "generation ticket has unknown keys: ['unknown']",
        ),
        (
            lambda ticket: ticket.pop("registrationSetHash"),
            "generation ticket is missing keys: ['registrationSetHash']",
        ),
        (
            lambda ticket: ticket.update({"schemaVersion": "generation_ticket_v2"}),
            "unsupported generation ticket schema 'generation_ticket_v2'",
        ),
        (
            lambda ticket: ticket.update({"nonce": "A" * 64}),
            "ticket nonce must be 64 lowercase hex characters",
        ),
        (
            lambda ticket: ticket.update({"mintedAtUtc": "2030-01-10T12:00Z"}),
            "ticket mintedAtUtc must be a second-precision UTC instant: "
            "'2030-01-10T12:00Z'",
        ),
        (
            lambda ticket: ticket.update({"expiresAtUtc": MINTED_AT}),
            "ticket expiresAtUtc must be later than mintedAtUtc",
        ),
        (
            lambda ticket: ticket.update({"ticketId": f"2030-01-09-{NONCE}"}),
            "ticketId date must equal the mintedAtUtc date: 2030-01-09 != "
            "2030-01-10",
        ),
        (
            lambda ticket: ticket.update({"attempt": 0}),
            "ticket attempt must be an integer greater than or equal to 1",
        ),
        (
            lambda ticket: ticket.update({"attempt": True}),
            "ticket attempt must be an integer greater than or equal to 1",
        ),
        (
            lambda ticket: ticket.update(
                {"supersedesTicketId": f"2030-01-09-{'e' * 64}"}
            ),
            "ticket supersedesTicketId requires supersededOutcome",
        ),
        (
            lambda ticket: ticket.update(
                {"supersededOutcome": {"outcome": "failed", "reason": "bad run"}}
            ),
            "ticket supersededOutcome requires supersedesTicketId",
        ),
        (
            lambda ticket: ticket.update({"targets": []}),
            "ticket targets must be a nonempty object list",
        ),
        (
            lambda ticket: ticket.update({"registrationSetHash": "bad"}),
            "ticket registrationSetHash must be a lowercase SHA-256 digest",
        ),
    ],
)
def test_ticket_shape_refusals_are_literal(
    mutate: Any, message: str
) -> None:
    ticket = sample_ticket()
    mutate(ticket)

    with pytest.raises(TicketError) as error:
        generation_tickets.validate_ticket(ticket)

    assert str(error.value) == message


@pytest.mark.parametrize("attempt", [0, -1, True, 1.5, "1"])
def test_mint_refuses_invalid_attempt_literally(attempt: Any) -> None:
    with pytest.raises(TicketError) as error:
        generation_tickets.mint_ticket(
            [sample_target()],
            sample_policy(),
            nonce=NONCE,
            minted_at_utc=MINTED_AT,
            expires_at_utc=EXPIRES_AT,
            attempt=attempt,
            registration_set_hash="d" * 64,
        )

    assert str(error.value) == (
        "ticket attempt must be an integer greater than or equal to 1"
    )


def test_mint_refuses_supersedes_without_outcome_literally() -> None:
    with pytest.raises(TicketError) as error:
        generation_tickets.mint_ticket(
            [sample_target()],
            sample_policy(),
            nonce=NONCE,
            minted_at_utc=MINTED_AT,
            expires_at_utc=EXPIRES_AT,
            attempt=2,
            supersedes=f"2030-01-09-{'e' * 64}",
            registration_set_hash="d" * 64,
        )

    assert str(error.value) == (
        "ticket supersedesTicketId requires supersededOutcome"
    )


def test_mint_refuses_outcome_without_supersedes_literally() -> None:
    with pytest.raises(TicketError) as error:
        generation_tickets.mint_ticket(
            [sample_target()],
            sample_policy(),
            nonce=NONCE,
            minted_at_utc=MINTED_AT,
            expires_at_utc=EXPIRES_AT,
            attempt=2,
            superseded_outcome={"outcome": "failed", "reason": "bad run"},
            registration_set_hash="d" * 64,
        )

    assert str(error.value) == (
        "ticket supersededOutcome requires supersedesTicketId"
    )


@pytest.mark.parametrize(
    ("outcome", "message"),
    [
        (
            {"outcome": "retried", "reason": "bad run"},
            "ticket supersededOutcome outcome must be one of "
            "['abandoned', 'expired', 'failed']",
        ),
        (
            {"outcome": "failed", "reason": ""},
            "ticket supersededOutcome reason must be a nonempty string",
        ),
        (
            {"outcome": "failed"},
            "ticket supersededOutcome must be an object with exactly outcome "
            "and reason",
        ),
    ],
)
def test_mint_refuses_invalid_superseded_outcome_literally(
    outcome: dict[str, str], message: str
) -> None:
    with pytest.raises(TicketError) as error:
        generation_tickets.mint_ticket(
            [sample_target()],
            sample_policy(),
            nonce=NONCE,
            minted_at_utc=MINTED_AT,
            expires_at_utc=EXPIRES_AT,
            attempt=2,
            supersedes=f"2030-01-09-{'e' * 64}",
            superseded_outcome=outcome,
            registration_set_hash="d" * 64,
        )

    assert str(error.value) == message


def test_policy_refuses_unknown_key_literally() -> None:
    policy = sample_policy()
    policy["command"] = "codex exec"

    with pytest.raises(TicketError) as error:
        generation_tickets.mint_ticket(
            [sample_target()],
            policy,
            nonce=NONCE,
            minted_at_utc=MINTED_AT,
            expires_at_utc=EXPIRES_AT,
            attempt=1,
            registration_set_hash="d" * 64,
        )

    assert str(error.value) == "ticket policy has unknown keys: ['command']"


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        (
            "promptMode",
            "turbo",
            "ticket policy promptMode must be one of "
            "['fast', 'full', 'ladder', 'ladder_v2']",
        ),
        (
            "codexSandbox",
            "danger-full-access",
            "ticket policy codexSandbox must be one of "
            "['read-only', 'workspace-write']",
        ),
    ],
)
def test_policy_refuses_unknown_modes_literally(
    field: str, value: str, message: str
) -> None:
    policy = sample_policy()
    policy[field] = value

    with pytest.raises(TicketError) as error:
        generation_tickets.mint_ticket(
            [sample_target()],
            policy,
            nonce=NONCE,
            minted_at_utc=MINTED_AT,
            expires_at_utc=EXPIRES_AT,
            attempt=1,
            registration_set_hash="d" * 64,
        )

    assert str(error.value) == message


def test_policy_refuses_network_under_read_only_sandbox_literally() -> None:
    policy = sample_policy()
    policy["codexNetwork"] = True

    with pytest.raises(TicketError) as error:
        generation_tickets.mint_ticket(
            [sample_target()],
            policy,
            nonce=NONCE,
            minted_at_utc=MINTED_AT,
            expires_at_utc=EXPIRES_AT,
            attempt=1,
            registration_set_hash="d" * 64,
        )

    assert str(error.value) == (
        "ticket policy codexNetwork requires codexSandbox workspace-write"
    )


@pytest.mark.parametrize("missing", sorted(generation_tickets.TARGET_REQUIRED_KEYS))
def test_target_refuses_each_missing_required_field_literally(missing: str) -> None:
    target = sample_target()
    target.pop(missing)

    with pytest.raises(TicketError) as error:
        generation_tickets.mint_ticket(
            [target],
            sample_policy(),
            nonce=NONCE,
            minted_at_utc=MINTED_AT,
            expires_at_utc=EXPIRES_AT,
            attempt=1,
            registration_set_hash="d" * 64,
        )

    assert str(error.value) == f"ticket target 0 is missing fields: ['{missing}']"


def test_load_ticket_refuses_invalid_json_literally(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "ticket.json"
    path.write_text("{")

    with pytest.raises(TicketError) as error:
        generation_tickets.load_ticket(path)

    assert str(error.value).startswith(f"cannot load generation ticket {path}:")


def test_ticket_introducing_commit_uses_single_addition(
    tmp_path: pathlib.Path,
) -> None:
    git(tmp_path, "init")
    ticket = sample_ticket()
    relative = pathlib.Path("records/tickets") / "2030-01-10" / (
        f"{ticket['ticketId']}.json"
    )
    write_ticket(tmp_path / relative, ticket)
    git(tmp_path, "add", relative.as_posix())
    introducing_commit = commit(tmp_path, "Mint generation ticket")

    assert (
        generation_tickets.ticket_introducing_commit(relative, tmp_path)
        == introducing_commit
    )
    assert (
        generation_tickets.ticket_introducing_commit(tmp_path / relative, tmp_path)
        == introducing_commit
    )


def test_ticket_introducing_commit_refuses_zero_additions(
    tmp_path: pathlib.Path,
) -> None:
    git(tmp_path, "init")
    base = tmp_path / "base.txt"
    base.write_text("base\n")
    git(tmp_path, "add", "base.txt")
    commit(tmp_path, "Base")

    relative = pathlib.Path("records/tickets/2030-01-10/missing.json")
    with pytest.raises(TicketError) as error:
        generation_tickets.ticket_introducing_commit(relative, tmp_path)

    assert str(error.value) == (
        "generation ticket must have exactly one introducing commit on HEAD "
        f"history: {relative.as_posix()}; found 0"
    )


def test_ticket_introducing_commit_refuses_multiple_additions(
    tmp_path: pathlib.Path,
) -> None:
    git(tmp_path, "init")
    ticket = sample_ticket()
    relative = pathlib.Path("records/tickets") / "2030-01-10" / (
        f"{ticket['ticketId']}.json"
    )
    write_ticket(tmp_path / relative, ticket)
    git(tmp_path, "add", relative.as_posix())
    commit(tmp_path, "First addition")
    git(tmp_path, "rm", relative.as_posix())
    commit(tmp_path, "Remove ticket")
    write_ticket(tmp_path / relative, ticket)
    git(tmp_path, "add", relative.as_posix())
    commit(tmp_path, "Second addition")

    with pytest.raises(TicketError) as error:
        generation_tickets.ticket_introducing_commit(relative, tmp_path)

    assert str(error.value) == (
        "generation ticket must have exactly one introducing commit on HEAD "
        f"history: {relative.as_posix()}; found 2"
    )


def test_find_ticket_consumption_scans_batch_days(tmp_path: pathlib.Path) -> None:
    ticket_id = sample_ticket()["ticketId"]

    assert generation_tickets.find_ticket_consumption(ticket_id, tmp_path) is None

    consumption = (
        tmp_path
        / "records"
        / "thesis-analyst"
        / "batches"
        / "2030-01-12"
        / f"attested-{ticket_id}.json"
    )
    consumption.parent.mkdir(parents=True)
    consumption.write_text("{}\n")

    assert generation_tickets.find_ticket_consumption(ticket_id, tmp_path) == (
        "records/thesis-analyst/batches/2030-01-12/"
        f"attested-{ticket_id}.json"
    )


def test_find_ticket_successor_scans_ticket_records(tmp_path: pathlib.Path) -> None:
    predecessor = sample_ticket()
    successor = generation_tickets.mint_ticket(
        [sample_target()],
        sample_policy(),
        nonce="e" * 64,
        minted_at_utc="2030-01-11T12:00:00Z",
        expires_at_utc="2030-01-18T12:00:00Z",
        attempt=2,
        supersedes=predecessor["ticketId"],
        superseded_outcome={"outcome": "failed", "reason": "agent failed"},
        registration_set_hash="d" * 64,
    )

    assert (
        generation_tickets.find_ticket_successor(predecessor["ticketId"], tmp_path)
        is None
    )

    relative = pathlib.Path("records/tickets/2030-01-11") / (
        f"{successor['ticketId']}.json"
    )
    write_ticket(tmp_path / relative, successor)

    assert generation_tickets.find_ticket_successor(
        predecessor["ticketId"], tmp_path
    ) == relative.as_posix()


def test_valid_superseding_ticket_round_trip(tmp_path: pathlib.Path) -> None:
    predecessor = sample_ticket()
    successor = generation_tickets.mint_ticket(
        [copy.deepcopy(sample_target())],
        copy.deepcopy(sample_policy()),
        nonce="f" * 64,
        minted_at_utc="2030-01-11T12:00:00Z",
        expires_at_utc="2030-01-18T12:00:00Z",
        attempt=2,
        supersedes=predecessor["ticketId"],
        superseded_outcome={"outcome": "expired", "reason": "window elapsed"},
        registration_set_hash="d" * 64,
    )
    path = tmp_path / "successor.json"
    write_ticket(path, successor)

    assert generation_tickets.load_ticket(path) == successor
