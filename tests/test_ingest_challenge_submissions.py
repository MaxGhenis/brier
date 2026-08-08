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


def test_duplicate_target_submissions_from_one_challenger_all_reject(
    submission_repo: dict[str, Any],
) -> None:
    # One shot per (challenger, target): a second file naming the same
    # dataPointId has no trusted order against the first (generatedAtUtc
    # is a claim), so the whole group rejects fail-closed while other
    # challengers' rows survive.
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
    assert challengers == ["github:other-user"]


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
