from __future__ import annotations

import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/mint-generation-ticket.yml"


def load_workflow() -> dict:
    parsed = yaml.safe_load(WORKFLOW.read_text())
    assert isinstance(parsed, dict)
    return parsed


def test_mint_workflow_is_one_trusted_dispatch_job() -> None:
    workflow = load_workflow()
    trigger = workflow.get("on", workflow.get(True))
    assert set(trigger) == {"workflow_dispatch"}
    inputs = trigger["workflow_dispatch"]["inputs"]
    assert set(inputs) == {
        "series",
        "slugs",
        "prompt_mode",
        "codex_model",
        "codex_reasoning_effort",
        "codex_network",
        "review_codex_model",
        "review_codex_search",
        "timeout_seconds",
        "attempt",
        "supersedes_ticket_id",
        "superseded_outcome",
        "superseded_reason",
        "expires_hours",
    }
    assert inputs["expires_hours"]["default"] == "168"
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["concurrency"] == {
        "group": "docket-writers",
        "cancel-in-progress": False,
    }
    assert set(workflow["jobs"]) == {"mint"}
    job = workflow["jobs"]["mint"]
    assert job["permissions"] == {
        "contents": "write",
        "id-token": "write",
        "attestations": "write",
    }
    checkout = next(
        step
        for step in job["steps"]
        if step.get("uses") == "actions/checkout@v5"
    )
    assert checkout["with"] == {
        "ref": "main",
        "fetch-depth": 0,
        "persist-credentials": False,
    }


def test_mint_workflow_reuses_registration_and_commits_only_ticket() -> None:
    source = WORKFLOW.read_text()

    assert "scripts/roll_docket.py" in source
    assert "scripts/generation_tickets.py select" in source
    assert source.index("--reuse-existing-only") < source.index(
        "--bind-registration-commits"
    )
    assert "--bind-registration-commits" in source
    assert "--head HEAD" in source
    assert "openssl rand -hex 32" in source
    assert "scripts/generation_tickets.py mint" in source
    assert "expires_hours must not exceed 336" in source
    assert "earliest_resolution_boundary" in source
    assert 'min(' in source
    assert '--expires-hours "$EXPIRES_HOURS"' in source
    assert "--expires-at-utc" not in source
    assert "scripts/generation_tickets.py check-supersession" in source
    assert "find_ticket_consumption" not in source  # kept in the tested helper
    assert 'git add -- "$TICKET_PATH"' in source
    assert 'if [ "$STAGED" != "$TICKET_PATH" ]; then' in source
    assert "scripts/docket_publication.py scan-staged" in source
    assert "git add records/" not in source
    assert "--skip-unbindable" not in source
    assert "adopt_proven_series.py" not in source


def test_mint_workflow_reverifies_every_push_candidate_and_attests() -> None:
    source = WORKFLOW.read_text()

    assert source.count("for attempt in 1 2 3; do") == 1
    assert source.count("--bind-registration-commits") == 2
    assert source.count("check-supersession") == 2
    assert "ticket_introducing_commit" in source
    assert "verify_record_chain.py records" in source
    assert "verify_custody.py" in source
    assert "git pull --rebase origin main" in source
    assert "push origin main" in source
    assert "git ls-remote origin refs/heads/main" in source
    assert "uses: ./.github/actions/attest-records-push" in source
    assert "commit: ${{ steps.sync.outputs.pushed_sha }}" in source


def test_mint_workflow_is_in_records_attestation_allowlist() -> None:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    import verify_records_attestations as provenance

    assert (
        ".github/workflows/mint-generation-ticket.yml"
        in provenance.ALLOWED_WORKFLOWS
    )
