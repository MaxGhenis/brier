from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/publish-attested.yml"


def load_workflow() -> dict:
    parsed = yaml.safe_load(WORKFLOW.read_text())
    assert isinstance(parsed, dict)
    return parsed


def test_publish_attested_is_one_trusted_dispatch_job() -> None:
    workflow = load_workflow()
    trigger = workflow.get("on", workflow.get(True))
    assert set(trigger) == {"workflow_dispatch"}
    inputs = trigger["workflow_dispatch"]["inputs"]
    assert set(inputs) == {"ticket_path", "bundle_sha"}
    assert all(value["required"] is True for value in inputs.values())
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["concurrency"] == {
        "group": "docket-writers",
        "cancel-in-progress": False,
    }
    assert set(workflow["jobs"]) == {"publish"}
    job = workflow["jobs"]["publish"]
    assert job["permissions"] == {
        "contents": "write",
        "issues": "write",
        "actions": "write",
        "id-token": "write",
        "attestations": "write",
    }
    checkout = next(
        step for step in job["steps"] if step.get("uses") == "actions/checkout@v5"
    )
    assert checkout["with"] == {
        "ref": "main",
        "fetch-depth": 0,
        "persist-credentials": False,
    }


def test_publish_attested_transport_is_content_addressed_and_safely_extracted() -> None:
    source = WORKFLOW.read_text()

    assert "^[0-9a-f]{40}$" in source
    assert 'git fetch --no-tags origin "$BUNDLE_SHA"' in source
    assert "--contains \"$BUNDLE_SHA\" refs/remotes/origin/" in source
    assert 'expected = {"bundle.tar.zst", "bundle.sha256"}' in source
    assert '(mode, kind) != ("100644", "blob")' in source
    assert "compressed archive exceeds 1 GiB" in source
    assert "bundle.sha256 exceeds 256 bytes" in source
    assert source.index("bundle sha256 mismatch") < source.index(
        '["zstd", "-q", "-d", "--stdout"'
    )
    assert "expanded archive exceeds 2 GiB" in source
    assert "archive has too many members" in source
    assert "archive.getmembers()" not in source
    assert "for member in archive:" in source
    assert "raw_name.startswith(\"/\")" in source
    assert '".." in relative.parts' in source
    assert "links and special archive" in source
    assert 'target.open("xb")' in source
    assert "bundle_manifest.json and repo" in source
    assert "tar --" not in source


def test_publish_attested_reconstructs_trust_before_applying() -> None:
    source = WORKFLOW.read_text()

    assert source.count("scripts/verify_attested_bundle.py") == 2
    assert source.index("scripts/verify_attested_bundle.py") < source.index(
        "scripts/register_targets.py"
    )
    assert source.index("scripts/verify_attested_bundle.py") < source.index(
        "scripts/docket_publication.py validate"
    )
    assert 'json.dumps({"targets": ticket["targets"]}' in source
    assert "ticket_batch_filename(ticket)" in source
    assert source.count("--bind-registration-commits") == 2
    assert source.count("registrationSetHash") >= 3
    assert source.count("scripts/docket_publication.py validate") == 2
    assert source.count("--trusted-targets") == 2
    assert source.count("--publish-validated-at-utc") == 2
    assert source.count("--allow-published-wave") == 2
    assert source.count("--apply") == 1


def test_publish_attested_reverifies_every_push_candidate() -> None:
    source = WORKFLOW.read_text()

    assert source.count("for attempt in 1 2 3; do") == 1
    loop = source[source.index("for attempt in 1 2 3; do") :]
    assert "git pull --rebase origin main" in loop
    assert 'git worktree add --detach "$TRUSTED_MAIN" origin/main' in loop
    assert '--repo-root "$TRUSTED_MAIN"' in loop
    assert "never bypass consumption" in loop
    assert "scripts/verify_attested_bundle.py" in loop
    assert "scripts/register_targets.py" in loop
    assert "scripts/docket_publication.py validate" in loop
    assert "git diff --exit-code" in loop
    assert "git diff --cached --exit-code" in loop
    assert "refusing a no-op push" in loop
    assert "push origin main" in loop
    assert "git ls-remote origin refs/heads/main" not in loop.split(
        "- name: Attest the publication push"
    )[0]
    assert "Never put a" in loop
    push_success = loop[loop.index("push origin main") : loop.index("sleep 2")]
    assert push_success.index("pushed=1") < push_success.index("break")


def test_publish_attested_copies_the_existing_trusted_publish_tail() -> None:
    source = WORKFLOW.read_text()

    assert source.count("scripts/verify_record_chain.py records") == 2
    assert source.count("scripts/verify_custody.py") == 2
    assert source.count("scripts/register_wave.py") == 2
    assert 'WAVE_NAME="auto-$DAY-$WAVE_HASH"' in source
    assert source.count("bun run test") == 2
    assert source.count("bun run build") == 2
    assert source.index("scripts/docket_publication.py scan-staged") < source.index(
        'git commit -m "Publish attested generation $TICKET_ID"'
    )
    assert "uses: ./.github/actions/attest-records-push" in source
    assert "commit: ${{ steps.final_push.outputs.attest_commit }}" in source
    assert source.index("uses: ./.github/actions/attest-records-push") < source.index(
        "git ls-remote origin refs/heads/main"
    )
    assert 'git merge-base --is-ancestor "$PUSHED_COMMIT" origin/main' in source
    assert "https://app.thesisinstitute.org/build.json" in source
    assert "gh workflow run record-forecasts.yml --ref main" in source
    assert '-f expected_sha="$SHA"' in source
    assert "Alert on failure" in source


def test_publish_attested_has_no_generation_or_artifact_trust_shortcuts() -> None:
    source = WORKFLOW.read_text()

    assert "OPENAI_API_KEY" not in source
    assert "run_thesis_analyst.py" not in source
    assert "actions/upload-artifact" not in source
    assert "actions/download-artifact" not in source
    assert "THESIS_ALLOW_RECORDS_PUSH" not in source


def test_publish_attested_is_in_records_attestation_allowlist() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    import verify_records_attestations as provenance

    assert ".github/workflows/publish-attested.yml" in provenance.ALLOWED_WORKFLOWS
