from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "prospect-docket.yml"


def job_block(source: str, name: str, next_name: str | None) -> str:
    start = source.index(f"\n  {name}:\n")
    end = source.index(f"\n  {next_name}:\n", start) if next_name else len(source)
    return source[start:end]


def test_prospect_workflow_has_four_phase_permission_boundary() -> None:
    source = WORKFLOW.read_text()
    propose = job_block(source, "propose", "register")
    register = job_block(source, "register", "generate")
    generate = job_block(source, "generate", "publish")
    publish = job_block(source, "publish", None)

    assert "contents: write" not in propose
    assert "contents: write" in register
    assert "contents: write" not in generate
    assert "contents: write" in publish
    assert "OPENAI_API_KEY" not in register
    assert "codex" not in register.lower()
    assert "needs: propose" in register
    assert "needs: register" in generate
    assert "needs: [register, generate]" in publish


def test_register_replays_untrusted_proposals_and_binds_before_generation() -> None:
    source = WORKFLOW.read_text()
    propose = job_block(source, "propose", "register")
    register = job_block(source, "register", "generate")
    generate = job_block(source, "generate", "publish")

    assert "prospect_targets.py filter" in propose
    assert "prospect_targets.py validate" in register
    assert "--registered-at-utc" in register
    assert "--bind-registration-commits" in register
    assert "--registered-at-utc" not in generate
    assert 'count: ${{ steps.targets.outputs.count }}' in register
    assert "needs.propose.outputs.count" not in source
    assert "ref: ${{ needs.register.outputs.source_sha }}" in generate
    assert "EXPECTED_SET_HASH" in generate


def test_artifact_and_batch_names_are_attempt_safe() -> None:
    source = WORKFLOW.read_text()

    assert "prospect-${GITHUB_RUN_ID}-a${GITHUB_RUN_ATTEMPT}.json" in source
    assert (
        "proposals_artifact: ${{ steps.proposals.outputs.proposals_artifact }}"
        in source
    )
    assert (
        "registration_artifact: ${{ steps.targets.outputs.registration_artifact }}"
        in source
    )
    assert (
        "publication_artifact: ${{ steps.bundle.outputs.publication_artifact }}"
        in source
    )
    assert "name: ${{ needs.propose.outputs.proposals_artifact }}" in source
    assert "name: ${{ needs.register.outputs.registration_artifact }}" in source
    assert "name: ${{ needs.generate.outputs.publication_artifact }}" in source
    assert "GITHUB_RUN_NUMBER" not in source


def test_publication_is_single_commit_and_fully_reverified() -> None:
    source = WORKFLOW.read_text()
    generate = job_block(source, "generate", "publish")
    publish = job_block(source, "publish", None)

    assert "--trusted-targets" in generate
    assert publish.count("--trusted-targets") == 2
    assert publish.count("--publish-validated-at-utc") == 2
    assert "--allow-path" not in source
    assert "[skip ci]" not in source
    assert "Commit run records" not in source
    assert "verify_record_chain.py records" in publish
    assert "verify_custody.py" in publish
    assert 'WAVE_NAME="auto-$DAY-$WAVE_HASH"' in publish
    assert "bun run test" in publish
    assert "bun run build" in publish
    assert publish.count("for attempt in 1 2 3") == 1
    assert "git diff --exit-code" in publish
    assert "git diff --cached --exit-code" in publish
    assert "gh workflow run record-forecasts.yml --ref main" in publish
    assert '-f expected_sha="$SHA"' in publish


def test_count_zero_path_is_an_explicit_publish_noop() -> None:
    source = WORKFLOW.read_text()
    generate = job_block(source, "generate", "publish")
    publish = job_block(source, "publish", None)

    assert "needs.register.outputs.count != '0'" in generate
    assert (
        "(needs.register.outputs.count != '0' && needs.generate.result != 'success')"
        in publish
    )
    assert "if: ${{ always() }}" in publish
