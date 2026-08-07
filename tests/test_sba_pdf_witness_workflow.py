from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "witness-sba-pdf.yml"
sys.path.insert(0, str(ROOT / "scripts"))

import verify_records_attestations as provenance  # noqa: E402


def test_sba_witness_workflow_runs_daily_and_captures_every_outcome() -> None:
    source = WORKFLOW.read_text()

    assert 'cron: "5 13 * * *"' in source
    assert "workflow_dispatch: {}" in source
    assert source.count("scripts/witness_sba_pdf.py") == 1
    assert "uv run --locked --extra custody python scripts/witness_sba_pdf.py" in source
    # Outcome handling belongs to the capture command. The workflow publishes
    # whichever sealed run it returns, including unchanged and failed attempts.
    assert "steps.capture.outputs.outcome" not in source
    assert 'git add -- "$RUN_DIR"' in source
    assert "git add records" not in source


def test_sba_witness_workflow_reverifies_and_witnesses_after_publish() -> None:
    source = WORKFLOW.read_text()
    capture = source.index("scripts/witness_sba_pdf.py")
    first_verify = source.index('scripts/verify_custody.py "$RUN_DIR"')
    commit = source.index('git commit -m "Witness SBA PDF bundle')
    rebase = source.index("git pull --rebase origin main")
    second_verify = source.index(
        'scripts/verify_custody.py "$RUN_DIR"', first_verify + 1
    )
    push = source.index("push origin main")
    attest = source.index("uses: ./.github/actions/attest-records-push")
    dispatch = source.index("gh workflow run record-forecasts.yml --ref main")

    assert capture < first_verify < commit < rebase < second_verify
    assert second_verify < push < attest < dispatch
    assert source.count('scripts/verify_custody.py "$RUN_DIR"') == 2
    assert "for attempt in 1 2 3" in source
    assert "PUBLISHED=$(git log -1 --diff-filter=A --format=%H" in source
    assert "git ls-remote" not in source


def test_sba_witness_workflow_has_records_publisher_permissions() -> None:
    source = WORKFLOW.read_text()

    assert "actions: write" in source
    assert "contents: write" in source
    assert "id-token: write" in source
    assert "attestations: write" in source
    assert "persist-credentials: false" in source
    assert ".github/workflows/witness-sba-pdf.yml" in provenance.ALLOWED_WORKFLOWS
