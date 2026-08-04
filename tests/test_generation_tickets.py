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


def write_bound_inputs(
    root: pathlib.Path, targets: list[dict[str, Any]] | None = None
) -> tuple[pathlib.Path, pathlib.Path]:
    bound_targets = targets or [sample_target()]
    targets_path = root / "bound-targets.json"
    targets_path.write_text(json.dumps({"targets": bound_targets}) + "\n")
    rows = [
        {
            "catalogSlug": target["catalogSlug"],
            "registrationCommit": target["registrationCommit"],
            "targetContentHash": target["targetContentHash"],
            "targetRegistrationPath": target["targetRegistrationPath"],
        }
        for target in bound_targets
    ]
    rows.sort(key=lambda row: row["catalogSlug"])
    metadata = {
        "schemaVersion": "thesis_target_registration_set_v1",
        "sourceCommit": "9" * 40,
        "registrationSetHash": "d" * 64,
        "registrationCommits": sorted({str(row["registrationCommit"]) for row in rows}),
        "targetContentHashes": sorted({str(row["targetContentHash"]) for row in rows}),
        "targets": rows,
    }
    metadata_path = root / "registration.json"
    metadata_path.write_text(json.dumps(metadata) + "\n")
    return targets_path, metadata_path


def conventional_ticket_path(
    root: pathlib.Path, ticket: dict[str, Any]
) -> pathlib.Path:
    return (
        root
        / "records"
        / "tickets"
        / ticket["ticketId"][:10]
        / f"{ticket['ticketId']}.json"
    )


def mint_cli_args(
    targets_path: pathlib.Path,
    metadata_path: pathlib.Path,
    repo_root: pathlib.Path,
    *,
    attempt: int = 1,
) -> list[str]:
    return [
        "mint",
        "--targets-file",
        str(targets_path),
        "--registration-metadata",
        str(metadata_path),
        "--nonce",
        NONCE,
        "--minted-at-utc",
        MINTED_AT,
        "--expires-at-utc",
        EXPIRES_AT,
        "--attempt",
        str(attempt),
        "--prompt-mode",
        "fast",
        "--codex-model",
        "gpt-test",
        "--codex-reasoning-effort",
        "low",
        "--codex-sandbox",
        "read-only",
        "--review-codex-model",
        "gpt-review-test",
        "--timeout-seconds",
        "540",
        "--repo-root",
        str(repo_root),
    ]


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


def test_mint_refuses_non_json_target_before_copy() -> None:
    class CopyProbe:
        copied = False

        def __deepcopy__(self, memo: dict[int, Any]) -> CopyProbe:
            self.copied = True
            return self

    probe = CopyProbe()
    target = sample_target()
    target["probe"] = probe

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

    assert str(error.value).startswith(
        "ticket targets contains a non-JSON value: Object of type CopyProbe"
    )
    assert not probe.copied


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
            "ticketId date must equal the mintedAtUtc date: 2030-01-09 != 2030-01-10",
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
def test_ticket_shape_refusals_are_literal(mutate: Any, message: str) -> None:
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

    assert str(error.value) == ("ticket supersedesTicketId requires supersededOutcome")


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

    assert str(error.value) == ("ticket supersededOutcome requires supersedesTicketId")


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
    relative = (
        pathlib.Path("records/tickets") / "2030-01-10" / (f"{ticket['ticketId']}.json")
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
    relative = (
        pathlib.Path("records/tickets") / "2030-01-10" / (f"{ticket['ticketId']}.json")
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
        f"records/thesis-analyst/batches/2030-01-12/attested-{ticket_id}.json"
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

    assert (
        generation_tickets.find_ticket_successor(predecessor["ticketId"], tmp_path)
        == relative.as_posix()
    )


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


def test_select_targets_by_exact_series_and_slugs() -> None:
    first = sample_target()
    second = {**sample_target(), "catalogSlug": "synthetic-series-second"}
    third = {
        **sample_target(),
        "series": "canary.other.series",
        "catalogSlug": "other-series",
    }
    targets = [first, second, third]
    for target in targets:
        target.pop("conditional")

    assert generation_tickets.select_targets(
        targets, series="canary.synthetic.series"
    ) == [first, second]
    assert generation_tickets.select_targets(
        targets, slugs=["other-series", "synthetic-series-2030-q1"]
    ) == [first, third]


@pytest.mark.parametrize(
    ("series", "slugs", "message"),
    [
        (None, None, "ticket mint requires exactly one of series or slugs"),
        (
            "canary.synthetic.series",
            ["synthetic-series-2030-q1"],
            "ticket mint requires exactly one of series or slugs",
        ),
        (
            "canary.missing",
            None,
            "requested series has no targets: canary.missing",
        ),
        (
            None,
            ["missing-slug"],
            "requested catalog slugs are not targets: ['missing-slug']",
        ),
    ],
)
def test_select_targets_refusals_are_literal(
    series: str | None, slugs: list[str] | None, message: str
) -> None:
    with pytest.raises(TicketError) as error:
        generation_tickets.select_targets([sample_target()], series=series, slugs=slugs)

    assert str(error.value) == message


def test_select_targets_refuses_partial_conditional_group_literally() -> None:
    first = {
        **sample_target(),
        "catalogSlug": "synthetic-enacted",
        "conditional": "Synthetic provision is enacted.",
    }
    second = {
        **sample_target(),
        "catalogSlug": "synthetic-current-law",
        "conditional": "Synthetic provision is not enacted.",
    }

    with pytest.raises(TicketError) as error:
        generation_tickets.select_targets([first, second], slugs=["synthetic-enacted"])

    assert str(error.value) == (
        "conditional target selection for canary.synthetic.series 2030-Q1 "
        "requires all slugs: ['synthetic-current-law', 'synthetic-enacted']"
    )


def test_select_cli_parses_comma_and_newline_slugs(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    first = sample_target()
    second = {**sample_target(), "catalogSlug": "synthetic-series-second"}
    targets_path = tmp_path / "targets.json"
    targets_path.write_text(json.dumps({"targets": [first, second]}) + "\n")
    out = tmp_path / "selected.json"

    assert (
        generation_tickets.main(
            [
                "select",
                "--targets-file",
                str(targets_path),
                "--slugs",
                "synthetic-series-second,\nsynthetic-series-2030-q1",
                "--out",
                str(out),
            ]
        )
        == 0
    )

    assert json.loads(out.read_text()) == {"targets": [first, second]}
    assert json.loads(capsys.readouterr().out) == {
        "out": str(out),
        "targets": 2,
    }


def test_select_cli_refuses_missing_selector_without_argparse_exit(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    targets_path = tmp_path / "targets.json"
    targets_path.write_text(json.dumps({"targets": [sample_target()]}) + "\n")

    assert (
        generation_tickets.main(
            [
                "select",
                "--targets-file",
                str(targets_path),
                "--out",
                str(tmp_path / "selected.json"),
            ]
        )
        == 1
    )
    assert capsys.readouterr().err == (
        "generation ticket failed: ticket mint requires exactly one of series "
        "or slugs\n"
    )


def test_registration_metadata_is_cross_checked_literally(
    tmp_path: pathlib.Path,
) -> None:
    targets_path, metadata_path = write_bound_inputs(tmp_path)
    targets = generation_tickets.load_target_file(targets_path)
    metadata = json.loads(metadata_path.read_text())
    metadata["targets"][0]["targetContentHash"] = "e" * 64
    metadata_path.write_text(json.dumps(metadata) + "\n")

    with pytest.raises(TicketError) as error:
        generation_tickets.load_registration_binding(targets, metadata_path)

    assert str(error.value) == (
        "registration metadata binding mismatch for synthetic-series-2030-q1: "
        "targetContentHash"
    )


def test_validate_supersession_requires_next_attempt(
    tmp_path: pathlib.Path,
) -> None:
    predecessor = sample_ticket()
    write_ticket(conventional_ticket_path(tmp_path, predecessor), predecessor)

    with pytest.raises(TicketError) as error:
        generation_tickets.validate_ticket_supersession(
            predecessor["ticketId"], tmp_path, attempt=3
        )

    assert str(error.value) == (
        f"generation ticket attempt must be 2 when superseding "
        f"{predecessor['ticketId']}; got 3"
    )


def test_validate_supersession_refuses_consumed_ticket(
    tmp_path: pathlib.Path,
) -> None:
    predecessor = sample_ticket()
    write_ticket(conventional_ticket_path(tmp_path, predecessor), predecessor)
    consumption = (
        tmp_path
        / "records"
        / "thesis-analyst"
        / "batches"
        / "2030-01-11"
        / f"attested-{predecessor['ticketId']}.json"
    )
    consumption.parent.mkdir(parents=True)
    consumption.write_text("{}\n")

    with pytest.raises(TicketError) as error:
        generation_tickets.validate_ticket_supersession(
            predecessor["ticketId"], tmp_path, attempt=2
        )

    assert str(error.value) == (
        f"generation ticket {predecessor['ticketId']} was already consumed by "
        "records/thesis-analyst/batches/2030-01-11/"
        f"attested-{predecessor['ticketId']}.json"
    )


def test_validate_supersession_allows_only_exact_current_successor(
    tmp_path: pathlib.Path,
) -> None:
    predecessor = sample_ticket()
    write_ticket(conventional_ticket_path(tmp_path, predecessor), predecessor)
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
    successor_path = conventional_ticket_path(tmp_path, successor)
    write_ticket(successor_path, successor)
    relative = successor_path.relative_to(tmp_path).as_posix()

    with pytest.raises(TicketError) as error:
        generation_tickets.validate_ticket_supersession(
            predecessor["ticketId"], tmp_path, attempt=2
        )
    assert str(error.value) == (
        f"generation ticket {predecessor['ticketId']} was already superseded by "
        f"{relative}"
    )

    assert (
        generation_tickets.validate_ticket_supersession(
            predecessor["ticketId"],
            tmp_path,
            attempt=2,
            allow_successor_path=relative,
        )
        == predecessor
    )


def test_mint_cli_writes_only_conventional_ticket_path(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    targets_path, metadata_path = write_bound_inputs(tmp_path)

    assert (
        generation_tickets.main(mint_cli_args(targets_path, metadata_path, tmp_path))
        == 0
    )

    result = json.loads(capsys.readouterr().out)
    assert result == {
        "ticketId": f"2030-01-10-{NONCE}",
        "ticketPath": f"records/tickets/2030-01-10/2030-01-10-{NONCE}.json",
    }
    ticket_path = tmp_path / result["ticketPath"]
    ticket = generation_tickets.load_ticket(ticket_path)
    assert ticket["registrationSetHash"] == "d" * 64
    assert ticket["targets"] == [sample_target()]

    files = sorted(
        path.relative_to(tmp_path).as_posix()
        for path in (tmp_path / "records").rglob("*")
        if path.is_file()
    )
    assert files == [result["ticketPath"]]


def test_mint_cli_requires_attempt_one_without_predecessor(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    targets_path, metadata_path = write_bound_inputs(tmp_path)

    assert (
        generation_tickets.main(
            mint_cli_args(targets_path, metadata_path, tmp_path, attempt=2)
        )
        == 1
    )

    assert capsys.readouterr().err == (
        "generation ticket failed: ticket attempt must be 1 without "
        "supersedesTicketId; got 2\n"
    )
    assert not (tmp_path / "records").exists()


def test_mint_cli_requires_complete_supersession_fields(
    tmp_path: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    targets_path, metadata_path = write_bound_inputs(tmp_path)
    argv = mint_cli_args(targets_path, metadata_path, tmp_path, attempt=2)
    argv.extend(["--supersedes-ticket-id", f"2030-01-09-{'e' * 64}"])

    assert generation_tickets.main(argv) == 1

    assert capsys.readouterr().err == (
        "generation ticket failed: --supersedes-ticket-id, "
        "--superseded-outcome, and --superseded-reason must be provided together\n"
    )
    assert not (tmp_path / "records").exists()
