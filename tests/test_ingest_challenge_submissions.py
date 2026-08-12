from __future__ import annotations

import json
import logging
import pathlib
import subprocess
import sys
from copy import deepcopy
from typing import Any

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ingest_challenge_submissions as ingest  # noqa: E402
from record_forecast_snapshot import build_snapshot_predictions  # noqa: E402


def write_json(path: pathlib.Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def git(repo: pathlib.Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def commit_all(repo: pathlib.Path, message: str) -> str:
    git(repo, "add", ".")
    git(
        repo,
        "-c",
        "user.name=Challenge Adapter Test",
        "-c",
        "user.email=challenge-adapter@example.com",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-m",
        message,
    )
    return git(repo, "rev-parse", "HEAD")


@pytest.fixture
def submission_repo(tmp_path: pathlib.Path) -> dict[str, Any]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "--quiet")

    target = {
        "schemaVersion": "thesis_target_registration_v3",
        "registeredAtUtc": "2030-01-01T00:00:00Z",
        "targets": [
            {
                "catalogSlug": "fixture-rate-january-2030",
                "country": "US",
                "dataPointId": "agency.fixture.rate.2030_01.first_print",
                "period": "2030-01",
                "series": "agency.fixture.rate",
                "sourceBinding": {
                    "adapter": "fixture",
                    "expectedReleaseWindow": {
                        "start": "2030-02-01",
                        "end": "2030-02-01",
                    },
                },
                "unit": "percent",
                "valueScale": 1,
            }
        ],
    }
    quantiles = [
        {"p": 0.05, "value": 2.7},
        {"p": 0.1, "value": 2.8},
        {"p": 0.25, "value": 2.9},
        {"p": 0.5, "value": 3.0},
        {"p": 0.75, "value": 3.1},
        {"p": 0.9, "value": 3.2},
        {"p": 0.95, "value": 3.3},
    ]
    submission = {
        "schemaVersion": "thesis_challenge_submission_v1",
        "challenger": "github:fixture-user",
        "systemType": "ai",
        "systemName": "Fixture Forecaster 1",
        "dataPointId": "agency.fixture.rate.2030_01.first_print",
        "pointEstimate": 3.0,
        "ciLow": 2.8,
        "ciHigh": 3.2,
        "quantiles": quantiles,
        "generatedAtUtc": "2030-01-31T12:00:00Z",
        "notes": "Fixture notes are retained.",
    }
    targets_dir = repo / "records" / "targets"
    inbox_dir = repo / "challenge" / "inbox"
    submission_path = inbox_dir / "fixture-user" / "fixture-rate.json"
    write_json(targets_dir / "2030-01-01-fixture.json", target)
    write_json(submission_path, submission)
    # The adapter refuses ids on the shared expired-registration ratchet
    # and fails closed when the file is absent, so the fixture repo
    # carries a minimal real-shaped copy with one expired fixture id.
    ratchet = repo / "site" / "src" / "data" / "expired-unforecast-registrations.ts"
    ratchet.parent.mkdir(parents=True, exist_ok=True)
    ratchet.write_text(
        "export const EXPIRED_UNFORECAST_REGISTRATIONS = [\n"
        '  "agency.fixture.expired.2029_12.first_print",\n'
        "] as const;\n"
    )
    head = commit_all(repo, "Add registered target and challenge submission")
    return {
        "repo": repo,
        "targets_dir": targets_dir,
        "inbox_dir": inbox_dir,
        "submission_path": submission_path,
        "submission": submission,
        "quantiles": quantiles,
        "head": head,
    }


def run_ingest(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return ingest.ingest_challenge_submissions(
        inbox_dir=fixture["inbox_dir"],
        targets_dir=fixture["targets_dir"],
        repo_root=fixture["repo"],
    )


def rewrite_and_commit(
    fixture: dict[str, Any], payload: dict[str, Any], message: str
) -> None:
    write_json(fixture["submission_path"], payload)
    fixture["head"] = commit_all(fixture["repo"], message)


def test_valid_submission_is_included_with_verbatim_quantiles_and_provenance(
    submission_repo: dict[str, Any],
) -> None:
    records = run_ingest(submission_repo)

    assert len(records) == 1
    record = records[0]
    assert record["forecastSlug"] == "fixture-rate-january-2030"
    assert record["dataPointId"] == "agency.fixture.rate.2030_01.first_print"
    assert record["forecasterId"] == ("github:fixture-user::Fixture Forecaster 1")
    assert record["pointEstimate"] == 3.0
    assert record["interval80"] == {"lower": 2.8, "upper": 3.2}
    assert record["quantiles"] == submission_repo["quantiles"]
    assert record["generatedAtUtc"] == "2030-01-31T12:00:00Z"
    assert record["recordedAt"] == "2030-01-31T12:00:00Z"
    assert record["resolutionDate"] == "2030-02-01"
    assert record["notes"] == "Fixture notes are retained."
    assert record["provenance"] == {
        "submissionPath": "challenge/inbox/fixture-user/fixture-rate.json",
        "mergeCommit": submission_repo["head"],
        "schemaVersion": "thesis_challenge_submission_v1",
    }


def test_second_shot_rejects_while_first_accepted_survives(
    submission_repo: dict[str, Any],
) -> None:
    # One shot per (challenger, target): git history orders acceptance,
    # so the first accepted content IS the forecast; a later divergent
    # file rejects while the original and rival challengers survive.
    duplicate = dict(submission_repo["submission"])
    duplicate["pointEstimate"] = 3.1
    write_json(
        submission_repo["inbox_dir"] / "fixture-user" / "second-shot.json",
        duplicate,
    )
    other = dict(submission_repo["submission"])
    other["challenger"] = "github:other-user"
    other["systemName"] = "Other Forecaster"
    write_json(
        submission_repo["inbox_dir"] / "other-user" / "fixture-rate.json",
        other,
    )
    commit_all(submission_repo["repo"], "Add duplicate and rival submissions")

    records = run_ingest(submission_repo)

    challengers = sorted(record["challenger"] for record in records)
    assert challengers == ["github:fixture-user", "github:other-user"]
    fixture_rows = [
        record for record in records if record["challenger"] == "github:fixture-user"
    ]
    assert len(fixture_rows) == 1
    assert fixture_rows[0]["pointEstimate"] == 3.0


def test_case_variant_challenger_cannot_double_enter(
    submission_repo: dict[str, Any],
) -> None:
    # GitHub logins are case-insensitive: GITHUB:FIXTURE-USER is the same
    # challenger, so the variant rejects against the first accepted
    # content while the original forecast survives.
    variant = dict(submission_repo["submission"])
    variant["challenger"] = "github:FIXTURE-USER"
    write_json(
        submission_repo["inbox_dir"] / "fixture-user-alias" / "same-target.json",
        variant,
    )
    commit_all(submission_repo["repo"], "Add case-variant duplicate")

    records = run_ingest(submission_repo)
    assert [record["challenger"] for record in records] == ["github:fixture-user"]


def test_rename_plus_edit_cannot_replace_the_forecast(
    submission_repo: dict[str, Any],
) -> None:
    # The round-3 bypass: delete the accepted file and re-add it under a
    # new name with a changed forecast. Canonical content is keyed to
    # (challenger, dataPointId) across history, so the replacement
    # rejects and nothing survives for the key until the challenger's PR
    # restores the accepted content.
    edited = dict(submission_repo["submission"])
    edited["pointEstimate"] = 3.2
    submission_repo["submission_path"].unlink()
    write_json(
        submission_repo["inbox_dir"] / "fixture-user" / "renamed-shot.json",
        edited,
    )
    commit_all(submission_repo["repo"], "Rename and edit the submission")

    assert run_ingest(submission_repo) == []


def test_merge_introduced_forecast_is_canonical_and_immutable(
    submission_repo: dict[str, Any],
) -> None:
    # A forecast accepted via a merge commit (branch -> mainline) must
    # enter the canonical map at the merge, so a later rename-plus-edit
    # still rejects.
    repo = submission_repo["repo"]
    git(repo, "checkout", "-q", "-b", "side")
    other = dict(submission_repo["submission"])
    other["challenger"] = "github:merge-user"
    path = submission_repo["inbox_dir"] / "merge-user" / "fixture-rate.json"
    write_json(path, other)
    commit_all(repo, "Side-branch submission")
    git(repo, "checkout", "-q", "-")
    git(
        repo,
        "-c",
        "user.name=Challenge Adapter Test",
        "-c",
        "user.email=challenge-adapter@example.com",
        "-c",
        "commit.gpgsign=false",
        "merge",
        "--no-ff",
        "-q",
        "-m",
        "Accept side submission",
        "side",
    )
    records = run_ingest(submission_repo)
    assert sorted(record["challenger"] for record in records) == [
        "github:fixture-user",
        "github:merge-user",
    ]

    edited = dict(other)
    edited["pointEstimate"] = 3.3
    path.unlink()
    write_json(submission_repo["inbox_dir"] / "merge-user" / "renamed.json", edited)
    commit_all(repo, "Rename and edit the merged submission")
    records = run_ingest(submission_repo)
    assert sorted(record["challenger"] for record in records) == ["github:fixture-user"]


def test_stale_branch_merged_later_cannot_predate_the_first_forecast(
    submission_repo: dict[str, Any],
) -> None:
    # Acceptance order is the first-parent chain: a divergent draft
    # committed on an old side branch and merged AFTER the real
    # submission landed must not become canonical.
    repo = submission_repo["repo"]
    # The side branch forks from the CURRENT tip and carries a divergent
    # draft for the fixture challenger's target at a different path.
    git(repo, "checkout", "-q", "-b", "stale")
    draft = dict(submission_repo["submission"])
    draft["pointEstimate"] = 9.9
    write_json(submission_repo["inbox_dir"] / "fixture-user" / "draft.json", draft)
    commit_all(repo, "Stale divergent draft")
    git(repo, "checkout", "-q", "-")
    git(
        repo,
        "-c",
        "user.name=Challenge Adapter Test",
        "-c",
        "user.email=challenge-adapter@example.com",
        "-c",
        "commit.gpgsign=false",
        "merge",
        "--no-ff",
        "-q",
        "-m",
        "Merge stale draft later",
        "stale",
    )
    records = run_ingest(submission_repo)
    # The mainline submission stays canonical; the draft is a divergent
    # surplus and rejects.
    assert [record["challenger"] for record in records] == ["github:fixture-user"]
    assert records[0]["pointEstimate"] == 3.0


def test_fixed_in_place_file_canonicalizes_and_then_locks(
    submission_repo: dict[str, Any],
) -> None:
    # Round-5 finding: an undecodable ADD followed by a valid
    # modification must canonicalize the first valid content — the key
    # must not stay fail-open. The fixed content survives, and a later
    # rewrite rejects against it.
    repo = submission_repo["repo"]
    path = submission_repo["inbox_dir"] / "fix-user" / "fixture-rate.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\xff\xfe{ not json")
    commit_all(repo, "Add undecodable submission")

    fixed = dict(submission_repo["submission"])
    fixed["challenger"] = "github:fix-user"
    write_json(path, fixed)
    commit_all(repo, "Fix the submission in place")

    records = run_ingest(submission_repo)
    assert sorted(record["challenger"] for record in records) == [
        "github:fix-user",
        "github:fixture-user",
    ]

    rewritten = dict(fixed)
    rewritten["pointEstimate"] = 3.4
    write_json(path, rewritten)
    commit_all(repo, "Rewrite after acceptance")

    records = run_ingest(submission_repo)
    assert sorted(record["challenger"] for record in records) == ["github:fixture-user"]


def test_undecodable_history_does_not_abort_the_batch(
    submission_repo: dict[str, Any],
) -> None:
    bad = submission_repo["inbox_dir"] / "fixture-user" / "garbled.json"
    bad.write_bytes(b"\xff\xfe{ not json")
    commit_all(submission_repo["repo"], "Add undecodable file")
    bad.unlink()
    commit_all(submission_repo["repo"], "Remove undecodable file")

    records = run_ingest(submission_repo)
    assert [record["challenger"] for record in records] == ["github:fixture-user"]


def test_pure_rename_of_accepted_content_survives(
    submission_repo: dict[str, Any],
) -> None:
    # A byte-identical file at a new path is the same forecast.
    original_bytes = submission_repo["submission_path"].read_bytes()
    submission_repo["submission_path"].unlink()
    new_path = submission_repo["inbox_dir"] / "fixture-user" / "renamed.json"
    new_path.write_bytes(original_bytes)
    commit_all(submission_repo["repo"], "Rename the submission unchanged")

    records = run_ingest(submission_repo)
    assert [record["challenger"] for record in records] == ["github:fixture-user"]
    assert records[0]["pointEstimate"] == 3.0


def test_edited_accepted_submission_is_refused(
    submission_repo: dict[str, Any],
) -> None:
    # One shot per target includes the content: editing the accepted file
    # in a later commit must not replace the forecast.
    edited = dict(submission_repo["submission"])
    edited["pointEstimate"] = 3.05
    rewrite_and_commit(submission_repo, edited, "Nudge the point estimate")

    assert run_ingest(submission_repo) == []


def test_interval_must_equal_q10_and_q90(
    submission_repo: dict[str, Any],
) -> None:
    inconsistent = dict(submission_repo["submission"])
    inconsistent["ciLow"] = 2.75
    write_json(
        submission_repo["inbox_dir"] / "other-user" / "inconsistent.json",
        {**inconsistent, "challenger": "github:other-user"},
    )
    commit_all(submission_repo["repo"], "Add interval-inconsistent submission")

    records = run_ingest(submission_repo)
    challengers = sorted(record["challenger"] for record in records)
    assert challengers == ["github:fixture-user"]


def test_non_registered_submission_is_skipped(
    submission_repo: dict[str, Any],
    caplog: pytest.LogCaptureFixture,
) -> None:
    payload = deepcopy(submission_repo["submission"])
    payload["dataPointId"] = "agency.fixture.missing.2030_01.first_print"
    rewrite_and_commit(submission_repo, payload, "Make target unregistered")

    with caplog.at_level(logging.WARNING, logger=ingest.__name__):
        records = run_ingest(submission_repo)

    assert records == []
    assert "challenge/inbox/fixture-user/fixture-rate.json" in caplog.text
    assert "unregistered dataPointId" in caplog.text


def test_post_release_submission_is_skipped_at_release_day_floor(
    submission_repo: dict[str, Any],
    caplog: pytest.LogCaptureFixture,
) -> None:
    payload = deepcopy(submission_repo["submission"])
    payload["generatedAtUtc"] = "2030-02-01T00:00:00Z"
    rewrite_and_commit(submission_repo, payload, "Move submission to release")

    with caplog.at_level(logging.WARNING, logger=ingest.__name__):
        records = run_ingest(submission_repo)

    assert records == []
    assert "does not precede release 2030-02-01T00:00:00Z" in caplog.text


def test_non_monotone_quantiles_are_skipped(
    submission_repo: dict[str, Any],
    caplog: pytest.LogCaptureFixture,
) -> None:
    payload = deepcopy(submission_repo["submission"])
    payload["quantiles"][3]["value"] = payload["quantiles"][2]["value"]
    rewrite_and_commit(submission_repo, payload, "Make quantiles non-monotone")

    with caplog.at_level(logging.WARNING, logger=ingest.__name__):
        records = run_ingest(submission_repo)

    assert records == []
    assert "quantile values must be strictly increasing" in caplog.text


def test_quantile_probability_grid_must_match_exactly(
    submission_repo: dict[str, Any],
    caplog: pytest.LogCaptureFixture,
) -> None:
    payload = deepcopy(submission_repo["submission"])
    payload["quantiles"][2]["p"] = 0.2
    rewrite_and_commit(submission_repo, payload, "Change quantile grid")

    with caplog.at_level(logging.WARNING, logger=ingest.__name__):
        records = run_ingest(submission_repo)

    assert records == []
    assert "quantile probabilities must be exactly" in caplog.text


def test_invalid_submissions_do_not_block_valid_batch_member(
    submission_repo: dict[str, Any],
    caplog: pytest.LogCaptureFixture,
) -> None:
    valid = submission_repo["submission"]

    unknown = deepcopy(valid)
    unknown["dataPointId"] = "agency.fixture.unknown.2030_01.first_print"
    write_json(
        submission_repo["inbox_dir"] / "other" / "unknown.json",
        unknown,
    )

    late = deepcopy(valid)
    late["generatedAtUtc"] = "2030-02-02T12:00:00Z"
    write_json(
        submission_repo["inbox_dir"] / "other" / "late.json",
        late,
    )

    non_monotone = deepcopy(valid)
    non_monotone["quantiles"][4]["value"] = non_monotone["quantiles"][3]["value"]
    write_json(
        submission_repo["inbox_dir"] / "other" / "non-monotone.json",
        non_monotone,
    )
    commit_all(submission_repo["repo"], "Add invalid batch members")

    with caplog.at_level(logging.WARNING, logger=ingest.__name__):
        records = run_ingest(submission_repo)

    assert [record["forecastSlug"] for record in records] == [
        "fixture-rate-january-2030"
    ]
    assert caplog.text.count("Skipping challenge submission") == 3
    assert "unregistered dataPointId" in caplog.text
    assert "does not precede release" in caplog.text
    assert "strictly increasing" in caplog.text


def test_timestamp_normalization_overflow_does_not_block_valid_sibling(
    submission_repo: dict[str, Any],
    caplog: pytest.LogCaptureFixture,
) -> None:
    overflow = deepcopy(submission_repo["submission"])
    overflow["generatedAtUtc"] = "0001-01-01T00:00:00+23:59"
    write_json(
        submission_repo["inbox_dir"] / "other" / "overflow.json",
        overflow,
    )
    commit_all(submission_repo["repo"], "Add overflowing timestamp")

    with caplog.at_level(logging.WARNING, logger=ingest.__name__):
        records = run_ingest(submission_repo)

    assert [record["forecastSlug"] for record in records] == [
        "fixture-rate-january-2030"
    ]
    assert "outside the supported UTC datetime range" in caplog.text


def test_recorder_projection_appends_challenges_without_reshaping_models() -> None:
    recorded = [
        {
            "kind": "prediction_recorded",
            "forecastSlug": "model-forecast",
            "pointEstimate": 4.2,
            "interval80": {"lower": 4.0, "upper": 4.4},
            "resolutionDate": "2030-02-01",
            "recordedAt": "2030-01-01T00:00:00Z",
            "agent": "thesis.analyst",
        }
    ]
    challenge = [
        {
            "forecastSlug": "model-forecast",
            "forecasterId": "github:fixture::Fixture Forecaster",
            "quantiles": [{"p": 0.05, "value": 3.9}],
            "provenance": {
                "submissionPath": "challenge/inbox/fixture/cell.json",
                "mergeCommit": "a" * 40,
                "schemaVersion": "thesis_challenge_submission_v1",
            },
        }
    ]

    predictions = build_snapshot_predictions(recorded, challenge)

    assert predictions[0] == {
        "forecastSlug": "model-forecast",
        "pointEstimate": 4.2,
        "interval80": {"lower": 4.0, "upper": 4.4},
        "resolutionDate": "2030-02-01",
        "recordedAt": "2030-01-01T00:00:00Z",
    }
    assert predictions[1] == challenge[0]
    assert len(predictions) == len(recorded) + len(challenge)


def test_recorder_workflow_wires_challenge_inputs() -> None:
    workflow = (ROOT / ".github/workflows/record-forecasts.yml").read_text()

    assert "--challenge-inbox challenge/inbox" in workflow
    assert "--target-registrations records/targets" in workflow


def test_expired_ratcheted_registration_refuses_challenge_rows(
    submission_repo: dict[str, Any],
) -> None:
    # Review of the ONS expiry ratchet: the challenge adapter accepted
    # any registered target with a pre-release timestamp, so a
    # post-grace submission could still be recorded for a terminally
    # expired id (the recorder commits without the site suite). The
    # adapter now consults the shared ratchet file itself.
    fixture = submission_repo
    expired_target = {
        "schemaVersion": "thesis_target_registration_v3",
        "registeredAtUtc": "2029-12-01T00:00:00Z",
        "targets": [
            {
                "catalogSlug": "fixture-expired-december-2029",
                "country": "US",
                "dataPointId": "agency.fixture.expired.2029_12.first_print",
                "period": "2029-12",
                "series": "agency.fixture.expired",
                "sourceBinding": {
                    "adapter": "fixture",
                    "expectedReleaseWindow": {
                        "start": "2030-02-01",
                        "end": "2030-02-01",
                    },
                },
                "unit": "percent",
                "valueScale": 1,
            }
        ],
    }
    write_json(
        fixture["targets_dir"] / "2029-12-01-fixture-expired.json", expired_target
    )
    expired_submission = dict(fixture["submission"])
    expired_submission["dataPointId"] = "agency.fixture.expired.2029_12.first_print"
    write_json(
        fixture["inbox_dir"] / "fixture-user" / "expired-rate.json",
        expired_submission,
    )
    fixture["head"] = commit_all(fixture["repo"], "Add expired-target submission")

    records = run_ingest(fixture)

    # The expired id is refused; the healthy sibling still lands.
    ids = [record["dataPointId"] for record in records]
    assert "agency.fixture.expired.2029_12.first_print" not in ids
    assert "agency.fixture.rate.2030_01.first_print" in ids


def test_missing_ratchet_file_fails_closed(
    submission_repo: dict[str, Any],
) -> None:
    fixture = submission_repo
    ratchet = (
        fixture["repo"] / "site" / "src" / "data"
        / "expired-unforecast-registrations.ts"
    )
    ratchet.unlink()
    fixture["head"] = commit_all(fixture["repo"], "Drop the ratchet file")
    # Without the ratchet the adapter cannot prove any id is admissible;
    # the whole ingest aborts loudly rather than admitting rows.
    with pytest.raises(ingest.ChallengeSubmissionError, match="cannot read"):
        run_ingest(fixture)


def test_quoted_comments_do_not_expire_ids(
    submission_repo: dict[str, Any],
) -> None:
    ratchet = (
        submission_repo["repo"] / "site" / "src" / "data"
        / "expired-unforecast-registrations.ts"
    )
    ratchet.write_text(
        "export const EXPIRED_UNFORECAST_REGISTRATIONS = [\n"
        '  // replacement is "agency.fixture.rate.2030_01.first_print"\n'
        '  "agency.fixture.expired.2029_12.first_print",\n'
        "] as const;\n"
    )
    submission_repo["head"] = commit_all(
        submission_repo["repo"], "Quoted comment in ratchet"
    )
    records = run_ingest(submission_repo)
    # The commented id is NOT expired; the healthy submission still lands.
    assert [r["dataPointId"] for r in records] == [
        "agency.fixture.rate.2030_01.first_print"
    ]


def test_comment_only_ratchet_array_fails_closed(
    submission_repo: dict[str, Any],
) -> None:
    ratchet = (
        submission_repo["repo"] / "site" / "src" / "data"
        / "expired-unforecast-registrations.ts"
    )
    ratchet.write_text(
        "export const EXPIRED_UNFORECAST_REGISTRATIONS = [\n"
        '  // only prose here, including a quoted "not.an.entry"\n'
        "] as const;\n"
    )
    submission_repo["head"] = commit_all(
        submission_repo["repo"], "Comment-only ratchet"
    )
    with pytest.raises(ingest.ChallengeSubmissionError, match="empty expired set"):
        run_ingest(submission_repo)
