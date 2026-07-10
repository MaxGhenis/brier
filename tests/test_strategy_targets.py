from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from strategy_targets import (  # noqa: E402
    StrategyTargetError,
    ensure_open,
    select_targets,
    selection_hash,
    stamp_artifact,
    verify_artifact,
    verify_selection,
)

OPEN_SLUG = "australia-cpi-annual-rate-july-2026"
OPEN_DATA_POINT = "abs.cpi.all_groups.yoy.2026-07.first_print"


def head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def empty_ledger(tmp_path: pathlib.Path) -> pathlib.Path:
    path = tmp_path / "official_observations.jsonl"
    path.write_text("")
    return path


def selection(
    tmp_path: pathlib.Path,
    *,
    slug: str = OPEN_SLUG,
    selected_at: str = "2026-07-10T07:00:00Z",
    ledger: pathlib.Path | None = None,
) -> dict:
    return select_targets(
        root=ROOT,
        source_sha=head(),
        selected_at_utc=selected_at,
        checked_at_utc=selected_at,
        workflow={"repository": "example/thesis", "runId": 123, "runAttempt": 1},
        requested_slugs=[slug],
        auto_select=False,
        max_targets=1,
        suite="both",
        ledger_path=ledger or empty_ledger(tmp_path),
        ledger_repository="PolicyEngine/ledger",
        ledger_branch="codex/thesis-ledger-facts",
        ledger_logical_path="ledger/official_observations.jsonl",
        ledger_repository_commit="a" * 40,
        ledger_blob_sha="b" * 40,
    )


def test_selector_resolves_one_published_v2_target_and_replays(
    tmp_path: pathlib.Path,
) -> None:
    ledger = empty_ledger(tmp_path)
    payload = selection(tmp_path, ledger=ledger)

    assert payload["schemaVersion"] == "thesis_strategy_selection_v1"
    assert payload["sourceSha"] == head()
    assert payload["targets"][0]["catalogSlug"] == OPEN_SLUG
    assert payload["targets"][0]["comparisonTarget"] is True
    assert payload["targets"][0]["registrationCommit"] == (
        "f2738042716881427217caa9c3c13aa4ca8783e5"
    )
    assert payload["targets"][0]["resolutionDate"] == "2026-08-26"
    assert payload["targets"][0]["targetRegistrationPath"].startswith(
        "records/targets/"
    )
    assert payload["localResolutionEvidence"]["resolvedDataPointIds"] == []
    assert payload["ledgerEvidence"]["resolvedDataPointIds"] == []
    assert payload["selectionSetHash"] == selection_hash(payload)

    stamped = stamp_artifact(
        payload,
        artifact_id=456,
        artifact_name="strategy-selection-probe-123-1",
        artifact_digest="c" * 64,
        artifact_created_at_utc="2026-07-10T07:01:00Z",
    )
    verify_selection(stamped, root=ROOT, ledger_path=ledger)


def test_selector_rejects_unknown_unpublished_resolved_and_release_day(
    tmp_path: pathlib.Path,
) -> None:
    with pytest.raises(StrategyTargetError, match="unknown catalog slug"):
        selection(tmp_path, slug="definitely-not-a-catalog-target")

    with pytest.raises(StrategyTargetError, match="not published"):
        selection(tmp_path, slug="australia-unemployment-rate-july-2026")

    with pytest.raises(StrategyTargetError, match="not contemporaneous"):
        selection(tmp_path, slug="ons-cpi-annual-rate-june-2026")

    resolved = tmp_path / "resolved.jsonl"
    resolved.write_text(json.dumps({"source_record_id": OPEN_DATA_POINT}) + "\n")
    with pytest.raises(StrategyTargetError, match="pinned official ledger"):
        selection(tmp_path, ledger=resolved)

    with pytest.raises(StrategyTargetError, match="release day"):
        selection(tmp_path, selected_at="2026-08-26T00:00:00Z")


def test_selector_requires_registration_commit_strictly_before_selection(
    tmp_path: pathlib.Path,
) -> None:
    with pytest.raises(StrategyTargetError, match="strictly predate"):
        selection(tmp_path, selected_at="2026-07-10T05:03:57Z")


def test_selector_artifact_witness_and_latest_open_checks(
    tmp_path: pathlib.Path,
) -> None:
    payload = stamp_artifact(
        selection(tmp_path),
        artifact_id=456,
        artifact_name="strategy-selection-probe-123-1",
        artifact_digest="d" * 64,
        artifact_created_at_utc="2026-07-10T07:01:00Z",
    )
    artifact = {
        "id": 456,
        "name": "strategy-selection-probe-123-1",
        "digest": f"sha256:{'d' * 64}",
        "created_at": "2026-07-10T07:01:00Z",
        "expired": False,
        "workflow_run": {"id": 123},
    }
    verify_artifact(payload, artifact)

    tampered = json.loads(json.dumps(artifact))
    tampered["workflow_run"]["id"] = 999
    with pytest.raises(StrategyTargetError, match="different workflow run"):
        verify_artifact(payload, tampered)

    missing_expiry = json.loads(json.dumps(artifact))
    missing_expiry.pop("expired")
    with pytest.raises(StrategyTargetError, match="unexpired status"):
        verify_artifact(payload, missing_expiry)

    resolved = tmp_path / "latest-resolved.jsonl"
    resolved.write_text(json.dumps({"source_record_id": OPEN_DATA_POINT}) + "\n")
    with pytest.raises(StrategyTargetError, match="became resolved"):
        ensure_open(
            payload,
            root=ROOT,
            ledger_path=resolved,
            checked_at_utc="2026-07-10T07:02:00Z",
        )


def test_selection_hash_rejects_boolean_number_substitution(
    tmp_path: pathlib.Path,
) -> None:
    payload = selection(tmp_path)
    payload["request"]["maxTargets"] = True
    assert selection_hash(payload) != payload["selectionSetHash"]


def test_require_pre_cutover_commit_semantics(tmp_path: pathlib.Path) -> None:
    import strategy_targets as module
    from strategy_targets import require_pre_cutover_commit

    repo = tmp_path / "repo"
    repo.mkdir()

    def git(*args: str) -> str:
        return subprocess.check_output(
            [
                "git",
                "-c",
                "user.name=test",
                "-c",
                "user.email=test@example.com",
                *args,
            ],
            cwd=repo,
            text=True,
        ).strip()

    git("init")
    (repo / "a").write_text("a\n")
    git("add", "a")
    git("commit", "-m", "first")
    first = git("rev-parse", "HEAD")
    (repo / "b").write_text("b\n")
    git("add", "b")
    git("commit", "-m", "cutover")
    cutover = git("rev-parse", "HEAD")

    monkey = pytest.MonkeyPatch()
    try:
        monkey.setattr(module, "V3_REGISTRATION_CUTOVER_COMMIT", cutover)
        require_pre_cutover_commit(repo, first)
        with pytest.raises(StrategyTargetError, match="strictly predate"):
            require_pre_cutover_commit(repo, cutover)
        monkey.setattr(module, "V3_REGISTRATION_CUTOVER_COMMIT", first)
        with pytest.raises(StrategyTargetError, match="strictly predate"):
            require_pre_cutover_commit(repo, cutover)
    finally:
        monkey.undo()
