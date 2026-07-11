from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import verify_records_attestations as provenance  # noqa: E402
from attest_subject import subject_bytes, subject_name  # noqa: E402


def test_subject_bytes_are_canonical_and_validated() -> None:
    commit = "a" * 40
    payload = subject_bytes("MaxGhenis/brier", commit)
    assert payload.endswith(b"\n")
    parsed = json.loads(payload)
    assert parsed == {
        "schemaVersion": "thesis_records_push_subject_v1",
        "repository": "MaxGhenis/brier",
        "commit": commit,
    }
    # Deterministic: same inputs, same bytes.
    assert payload == subject_bytes("MaxGhenis/brier", commit)
    assert subject_name(commit) == f"records-push-{commit}.json"

    with pytest.raises(ValueError, match="40-hex"):
        subject_bytes("MaxGhenis/brier", "abc123")
    with pytest.raises(ValueError, match="repository"):
        subject_bytes("not a slug", commit)


def test_cert_identity_pattern_admits_only_allowlisted_main_workflows() -> None:
    import re as re_module

    pattern = re_module.compile(
        provenance.cert_identity_pattern("MaxGhenis/brier")
    )
    assert pattern.fullmatch(
        "https://github.com/MaxGhenis/brier/.github/workflows/"
        "roll-docket.yml@refs/heads/main"
    )
    assert pattern.fullmatch(
        "https://github.com/MaxGhenis/brier/.github/workflows/"
        "record-forecasts.yml@refs/heads/main"
    )
    # Foreign repo, non-main ref, unlisted workflow, and prefix tricks all
    # fail the anchored pattern.
    rejected = [
        "https://github.com/Evil/fork/.github/workflows/roll-docket.yml@refs/heads/main",
        "https://github.com/MaxGhenis/brier/.github/workflows/roll-docket.yml@refs/heads/feature",
        "https://github.com/MaxGhenis/brier/.github/workflows/ci.yml@refs/heads/main",
        "https://github.com/MaxGhenis/brier/.github/workflows/roll-docket.yml@refs/heads/main.evil",
        "https://github.com/MaxGhenis/brierX/.github/workflows/roll-docket.yml@refs/heads/main",
    ]
    for identity in rejected:
        assert not pattern.fullmatch(identity), identity


def test_certificate_identity_extraction_ignores_statement_fields() -> None:
    payload = {
        "verificationResult": {
            "signature": {
                "certificate": {
                    "buildSignerURI": (
                        "https://github.com/MaxGhenis/brier/.github/workflows/"
                        "roll-docket.yml@refs/heads/main"
                    )
                }
            },
            "statement": {
                "predicate": {
                    "attacker": (
                        "github.com/Evil/fork/.github/workflows/"
                        "roll-docket.yml@refs/heads/main"
                    )
                }
            },
        }
    }
    identities = provenance.extract_certificate_identities(payload)
    assert identities == {
        "github.com/MaxGhenis/brier/.github/workflows/"
        "roll-docket.yml@refs/heads/main"
    }


def _fake_gh(payload: dict, returncode: int = 0, seen: list | None = None):
    def run(args, **kwargs):
        if args[:3] == ["gh", "attestation", "verify"]:
            if seen is not None:
                seen.append(args)
            return subprocess.CompletedProcess(
                args, returncode, stdout=json.dumps(payload), stderr=""
            )
        raise AssertionError(f"unexpected subprocess: {args}")

    return run


def test_verify_commit_delegates_identity_to_gh_and_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commit = "b" * 40
    monkeypatch.setattr(provenance, "commit_age_seconds", lambda _c: 10**9)

    seen: list = []
    good = {
        "verificationResult": {
            "signature": {
                "certificate": {
                    "buildSignerURI": (
                        "https://github.com/MaxGhenis/brier/.github/workflows/"
                        "record-forecasts.yml@refs/heads/main"
                    )
                }
            }
        }
    }
    monkeypatch.setattr(
        provenance.subprocess, "run", _fake_gh(good, seen=seen)
    )
    identity = provenance.verify_commit(commit, "MaxGhenis/brier")
    assert "record-forecasts.yml@refs/heads/main" in identity
    # The identity constraint must be enforced inside gh itself.
    args = seen[0]
    flag_index = args.index("--cert-identity-regex")
    assert args[flag_index + 1] == provenance.cert_identity_pattern(
        "MaxGhenis/brier"
    )

    # gh rejection (no attestation, or identity regex unmatched) fails
    # closed, with a single attempt for an old commit.
    monkeypatch.setattr(
        provenance.subprocess, "run", _fake_gh({}, returncode=1)
    )
    with pytest.raises(provenance.ProvenanceError, match="no valid attestation"):
        provenance.verify_commit(commit, "MaxGhenis/brier")


def test_allowlist_covers_exactly_the_records_pushing_workflows() -> None:
    workflows_dir = ROOT / ".github" / "workflows"
    for workflow in sorted(provenance.ALLOWED_WORKFLOWS):
        path = ROOT / workflow
        assert path.is_file(), f"allowlisted workflow missing: {workflow}"
        text = path.read_text()
        assert "attest-records-push" in text, (
            f"{workflow} is allowlisted but never attests its pushes"
        )
    # Any workflow that attests must be allowlisted (no orphan signers).
    for path in sorted(workflows_dir.glob("*.yml")):
        relative = f".github/workflows/{path.name}"
        if "attest-records-push" in path.read_text():
            assert relative in provenance.ALLOWED_WORKFLOWS, (
                f"{relative} attests records pushes but is not allowlisted"
            )


def test_enforcement_epoch_requires_single_introducing_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(provenance, "git_output", lambda *a: "")
    with pytest.raises(provenance.ProvenanceError, match="enforcement epoch"):
        provenance.enforcement_epoch()

    monkeypatch.setattr(
        provenance, "git_output", lambda *a: "a" * 40 + "\n" + "b" * 40
    )
    with pytest.raises(provenance.ProvenanceError, match="enforcement epoch"):
        provenance.enforcement_epoch()

    monkeypatch.setattr(provenance, "git_output", lambda *a: "c" * 40)
    assert provenance.enforcement_epoch() == "c" * 40


def test_attesting_jobs_have_exact_permissions_and_generate_jobs_none() -> None:
    import yaml  # a hard dependency here: a skip would silence the boundary check
    for workflow in sorted(provenance.ALLOWED_WORKFLOWS):
        parsed = yaml.safe_load((ROOT / workflow).read_text())
        for job_name, job in parsed["jobs"].items():
            steps = job.get("steps") or []
            attests = any(
                "attest-records-push" in str(step.get("uses", ""))
                for step in steps
            )
            pushes = any(
                "push origin main" in str(step.get("run", ""))
                for step in steps
            )
            perms = job.get("permissions") or parsed.get("permissions") or {}
            if attests:
                assert perms.get("id-token") == "write", (
                    f"{workflow}:{job_name} attests without id-token: write"
                )
                assert perms.get("attestations") == "write", (
                    f"{workflow}:{job_name} attests without attestations: write"
                )
            if pushes:
                assert attests, (
                    f"{workflow}:{job_name} pushes to main but never attests"
                )
            if job_name == "generate":
                assert perms.get("id-token") != "write", (
                    f"{workflow}: untrusted generate job gained id-token"
                )
                assert perms.get("attestations") != "write", (
                    f"{workflow}: untrusted generate job gained attestations"
                )
                assert not attests and not pushes, (
                    f"{workflow}: untrusted generate job pushes or attests"
                )


def _git(repo: pathlib.Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True
    ).strip()


def _commit(repo: pathlib.Path, path: str, message: str) -> str:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(message + "\n")
    _git(repo, "add", "-A")
    _git(
        repo,
        "-c", "user.name=t", "-c", "user.email=t@example.com",
        "commit", "-m", message,
    )
    return _git(repo, "rev-parse", "HEAD")


def test_scope_predicate_on_real_merge_dags(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    base = _commit(repo, "records/base.txt", "base records")
    epoch = _commit(repo, "scripts/verify_records_attestations.py", "epoch")

    # Side branch forked BEFORE the epoch, adding records, merged after:
    # must stay IN scope (Sol P1-2 reproduction).
    _git(repo, "checkout", "-q", "-b", "side", base)
    side = _commit(repo, "records/side.txt", "side records")
    _git(repo, "checkout", "-q", "main")
    _git(
        repo,
        "-c", "user.name=t", "-c", "user.email=t@example.com",
        "merge", "-q", "--no-ff", "-m", "merge side", "side",
    )
    post = _commit(repo, "records/post.txt", "post-epoch records")

    monkeypatch.setattr(provenance, "ROOT", repo)
    assert provenance.commit_in_scope(base, epoch) is False  # ancestor
    assert provenance.commit_in_scope(epoch, epoch) is False  # the epoch
    assert provenance.commit_in_scope(side, epoch) is True  # incomparable
    assert provenance.commit_in_scope(post, epoch) is True  # descendant

    # Full-history enumeration must surface the side-branch records commit.
    monkeypatch.setattr(provenance, "git_output", lambda *a: _git(repo, *a))
    commits = provenance.records_commits(f"{epoch}..HEAD")
    assert side in commits, "path simplification hid the side-branch commit"

    with pytest.raises(provenance.ProvenanceError, match="merge-base"):
        provenance.commit_in_scope("f" * 40, epoch)
