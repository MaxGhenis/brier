from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "witness-sba-pdf.yml"
sys.path.insert(0, str(ROOT / "scripts"))

import verify_records_attestations as provenance  # noqa: E402


def _workflow() -> dict:
    parsed = yaml.safe_load(WORKFLOW.read_text())
    assert isinstance(parsed, dict)
    return parsed


def test_sba_witness_workflow_runs_daily_and_captures_every_outcome() -> None:
    source = WORKFLOW.read_text()
    workflow = _workflow()
    trigger = workflow.get("on", workflow.get(True))
    assert trigger == {
        "schedule": [{"cron": "5 13 * * *"}],
        "workflow_dispatch": {},
    }

    assert source.count("scripts/witness_sba_pdf.py") == 1
    assert "uv run --locked --extra custody python scripts/witness_sba_pdf.py" in source
    assert 'echo "outcome=$OUTCOME"' in source
    assert '} >> "$GITHUB_OUTPUT"' in source
    assert 'git add -- "$RUN_DIR"' in source
    assert "git add records" not in source

    steps = workflow["jobs"]["capture"]["steps"]
    for name in (
        "Commit the sealed SBA capture attempt",
        "Rebase, reverify, and push the capture",
        "Attest the SBA capture push",
        "Dispatch the recorder for the published attempt",
    ):
        step = next(item for item in steps if item.get("name") == name)
        assert "if" not in step


def test_sba_witness_workflow_reverifies_and_witnesses_after_publish() -> None:
    source = WORKFLOW.read_text()
    capture = source.index("scripts/witness_sba_pdf.py")
    first_verify = source.index('scripts/verify_custody.py "$RUN_DIR"')
    commit = source.index('git commit -m "Witness SBA PDF bundle')
    rebase = source.index("git pull --rebase origin main")
    second_verify = source.index(
        'scripts/verify_custody.py "$RUN_DIR"', first_verify + 1
    )
    chain_verify = source.index("scripts/verify_record_chain.py records")
    push = source.index("push origin main")
    attest = source.index("uses: ./.github/actions/attest-records-push")
    dispatch = source.index("gh workflow run record-forecasts.yml --ref main")
    flag_failure = source.index("name: Flag a sealed source failure")
    alert = source.index("name: Alert on failure")

    assert capture < first_verify < commit < rebase < second_verify
    assert second_verify < chain_verify < push < attest < dispatch
    assert dispatch < flag_failure < alert
    assert source.count('scripts/verify_custody.py "$RUN_DIR"') == 2
    assert source.count("scripts/verify_record_chain.py records") == 1
    assert "for attempt in 1 2 3" in source
    assert "PUBLISHED=$(git log -1 --diff-filter=A --format=%H" in source
    assert "git ls-remote" not in source

    steps = _workflow()["jobs"]["capture"]["steps"]
    flag_step = next(
        step for step in steps if step.get("name") == "Flag a sealed source failure"
    )
    alert_step = next(step for step in steps if step.get("name") == "Alert on failure")
    assert flag_step["if"] == "steps.capture.outputs.outcome == 'failed'"
    assert "exit 1" in flag_step["run"]
    assert alert_step["if"] == "failure()"
    assert steps[-1] == alert_step


def test_sba_witness_workflow_has_records_publisher_permissions() -> None:
    workflow = _workflow()

    assert workflow["permissions"] == {
        "actions": "write",
        "contents": "write",
        "issues": "write",
        "id-token": "write",
        "attestations": "write",
    }
    assert workflow["concurrency"] == {
        "group": "witness-sba-pdf",
        "cancel-in-progress": False,
    }
    assert set(workflow["jobs"]) == {"capture"}
    checkout = next(
        step
        for step in workflow["jobs"]["capture"]["steps"]
        if step.get("uses") == "actions/checkout@v5"
    )
    assert checkout["with"] == {
        "ref": "main",
        "fetch-depth": 0,
        "persist-credentials": False,
    }
    assert ".github/workflows/witness-sba-pdf.yml" in provenance.ALLOWED_WORKFLOWS
