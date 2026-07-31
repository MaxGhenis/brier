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
                    ),
                    "sourceRepositoryIdentifier": "1113415529"
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


def test_era_verification_binds_subject_and_identity_to_the_signing_slug(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Post-rename, old commits verify under the slug their workflow signed.

    The subject bytes and the gh-enforced certificate identity must both come
    from the era slug; the store lookup tries the live slug first and falls
    back to the era slug (redirect coverage), never the other way around.
    """

    commit = "c" * 40
    monkeypatch.setattr(provenance, "commit_age_seconds", lambda _c: 10**9)

    seen: list = []
    good = {
        "verificationResult": {
            "signature": {
                "certificate": {
                    "buildSignerURI": (
                        "https://github.com/MaxGhenis/brier/.github/workflows/"
                        "record-forecasts.yml@refs/heads/main"
                    ),
                    "sourceRepositoryIdentifier": "1113415529"
                }
            }
        }
    }
    monkeypatch.setattr(
        provenance.subprocess, "run", _fake_gh(good, seen=seen)
    )
    identity = provenance.verify_commit(
        commit, "ThesisInstitute/thesis", ("MaxGhenis/brier", "MaxGhenis")
    )
    assert "record-forecasts.yml@refs/heads/main" in identity
    args = seen[0]
    # Era commits verify ENTIRELY under their era identity: the subject and
    # certificate regex carry the era slug, and the store lookup uses the
    # signing-time OWNER (GitHub's attestation store is owner-keyed and does
    # not follow transfers — verified empirically 2026-07-22).
    assert "--repo" not in args
    assert args[args.index("--owner") + 1] == "MaxGhenis"
    assert args[args.index("--cert-identity-regex") + 1] == (
        provenance.cert_identity_pattern("MaxGhenis/brier")
    )
    assert len(seen) == 1
    # An empty era slug is a malformed table, never a silent fall-through
    # to the live identity (Sol era-review finding 2).
    with pytest.raises(provenance.ProvenanceError, match="malformed verif"):
        provenance.verify_commit(
            commit, "ThesisInstitute/thesis", ("", "MaxGhenis")
        )

    # A verified certificate WITHOUT the pinned immutable repository id
    # fails closed — a future occupant of a historical slug mints
    # certificates with a different id (Sol era-review finding 1).
    impostor = {
        "verificationResult": {
            "signature": {
                "certificate": {
                    "buildSignerURI": (
                        "https://github.com/MaxGhenis/brier/.github/workflows/"
                        "record-forecasts.yml@refs/heads/main"
                    ),
                    "sourceRepositoryIdentifier": "9999999999",
                }
            }
        }
    }
    monkeypatch.setattr(provenance.subprocess, "run", _fake_gh(impostor))
    with pytest.raises(provenance.ProvenanceError, match="pinned source repo"):
        provenance.verify_commit(
            commit, "ThesisInstitute/thesis", ("MaxGhenis/brier", "MaxGhenis")
        )


def test_era_repository_resolves_by_ancestry(tmp_path: pathlib.Path) -> None:
    """Ancestors of the pinned boundary use the era slug; later commits the
    live slug; an unknown boundary fails closed instead of guessing."""

    repo = tmp_path / "era-dag"
    repo.mkdir()

    def git(*args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(repo), *args], text=True
        ).strip()

    git("init", "-q", "-b", "main")
    git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q",
        "--allow-empty", "-m", "old-era")
    old_commit = git("rev-parse", "HEAD")
    git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q",
        "--allow-empty", "-m", "boundary")
    boundary = git("rev-parse", "HEAD")
    git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q",
        "--allow-empty", "-m", "new-era")
    new_commit = git("rev-parse", "HEAD")

    original_root = provenance.ROOT
    original_eras = provenance.REPOSITORY_ERAS
    provenance.ROOT = repo
    provenance.REPOSITORY_ERAS = ((boundary, "MaxGhenis/brier", "MaxGhenis"),)
    try:
        assert provenance.era_repository(old_commit, "live/slug") == (
            ("MaxGhenis/brier", "MaxGhenis")
        )
        assert provenance.era_repository(boundary, "live/slug") == (
            ("MaxGhenis/brier", "MaxGhenis")
        )
        assert provenance.era_repository(new_commit, "live/slug") is None
        provenance.REPOSITORY_ERAS = (("f" * 40, "MaxGhenis/brier", "MaxGhenis"),)
        with pytest.raises(provenance.ProvenanceError, match="not a commit"):
            provenance.era_repository(new_commit, "live/slug")
        # A malformed LATER entry fails before any matching — first-match
        # resolution never masks table corruption (Sol era-review finding 3).
        provenance.REPOSITORY_ERAS = (
            (boundary, "MaxGhenis/brier", "MaxGhenis"),
            ("not-a-sha", "MaxGhenis/brier", "MaxGhenis"),
        )
        with pytest.raises(provenance.ProvenanceError, match="malformed era b"):
            provenance.era_repository(old_commit, "live/slug")
        provenance.REPOSITORY_ERAS = ((boundary, "", "MaxGhenis"),)
        with pytest.raises(provenance.ProvenanceError, match="malformed era s"):
            provenance.era_repository(old_commit, "live/slug")
        provenance.REPOSITORY_ERAS = ((boundary, "MaxGhenis/brier", "bad owner"),)
        with pytest.raises(provenance.ProvenanceError, match="malformed era o"):
            provenance.era_repository(old_commit, "live/slug")
    finally:
        provenance.ROOT = original_root
        provenance.REPOSITORY_ERAS = original_eras


def test_waiver_list_is_pinned_exactly() -> None:
    """The waived-unattested set is a permanent public record: the five
    2026-07-22 Next50 local pushes, the 2026-07-22 QCEW completion, and
    the two 2026-07-24 broadband vintage-repair session pushes (the
    anchors-gate rejection record and the repair itself) — full shas,
    disjoint from eras."""

    assert set(provenance.WAIVED_UNATTESTED_COMMITS) == {
        "8d1e6aa5c678035218a2ed310b259d855108b058",
        "56f14cc760f2a55cc789e499a0129a51f2e8bb75",
        "9e5d820916408af773912aa97267e4fc914c4d94",
        "4a4ac86dbf92b51a14d9fd29626bdd19b482cf0a",
        "08aac46200a7745621fd64f828734c716dcf7a69",
        "8ad16ab611ab89cacaff570f43e419e0552bdbaf",
        "4c3fa5ccb5e03c5c6ac2af8d20bbcaddafaa5871",
        "2c02b44382a0e88e0b5104ff82fb891367be64e8",
        "346e506feba487f8d016a078c3f7ab16b846b51b",
    }
    for sha, reason in provenance.WAIVED_UNATTESTED_COMMITS.items():
        assert provenance.ERA_BOUNDARY_RE.fullmatch(sha)
        assert reason.strip()
    era_boundaries = {b for b, _s, _o in provenance.REPOSITORY_ERAS}
    assert not era_boundaries & set(provenance.WAIVED_UNATTESTED_COMMITS)


def test_mixed_result_arrays_attribute_only_pinned_certificates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """gh returns one array entry per verified attestation; a coexisting
    wrong-id certificate neither denies service nor controls the logged
    signer (Sol round-3 P2)."""

    commit = "d" * 40
    monkeypatch.setattr(provenance, "commit_age_seconds", lambda _c: 10**9)

    def cert(workflow: str, repo_id: str) -> dict:
        return {
            "verificationResult": {
                "signature": {
                    "certificate": {
                        "buildSignerURI": (
                            "https://github.com/MaxGhenis/brier/.github/"
                            f"workflows/{workflow}@refs/heads/main"
                        ),
                        "sourceRepositoryIdentifier": repo_id,
                    }
                }
            }
        }

    mixed = [
        cert("prospect-docket.yml", "9999999999"),
        cert("strategy-docket.yml", provenance.PINNED_SOURCE_REPOSITORY_ID),
    ]
    monkeypatch.setattr(provenance.subprocess, "run", _fake_gh(mixed))
    identity = provenance.verify_commit(
        commit, "ThesisInstitute/thesis", ("MaxGhenis/brier", "MaxGhenis")
    )
    assert "strategy-docket.yml" in identity
    assert "prospect-docket" not in identity

    # All-foreign arrays fail closed.
    monkeypatch.setattr(
        provenance.subprocess,
        "run",
        _fake_gh([cert("roll-docket.yml", "9999999999")]),
    )
    with pytest.raises(provenance.ProvenanceError, match="pinned source repo"):
        provenance.verify_commit(commit, "ThesisInstitute/thesis")

    # Non-JSON stdout on a zero exit is an error, never "<verified>".
    def garbled(args, **kwargs):  # noqa: ANN001
        return subprocess.CompletedProcess(args, 0, stdout="ok!", stderr="")

    monkeypatch.setattr(provenance.subprocess, "run", garbled)
    with pytest.raises(provenance.ProvenanceError, match="not JSON"):
        provenance.verify_commit(commit, "ThesisInstitute/thesis")


def _merge(repo: pathlib.Path, message: str, ref: str, *extra: str) -> str:
    _git(
        repo,
        "-c", "user.name=t", "-c", "user.email=t@example.com",
        "merge", "-q", "--no-ff", *extra, "-m", message, ref,
    )
    return _git(repo, "rev-parse", "HEAD")


def test_noop_pr_merges_are_exempt_and_content_merges_are_not(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """PR-only regime (2026-07-31): a GitHub merge of a branch forked before
    a workflow's records push is enumerated by --full-history yet introduces
    nothing under records/** — exempt as a no-op. A merge that carries
    records content, and the smuggled branch commit itself, stay required."""

    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _commit(repo, "records/base.txt", "base records")
    epoch = _commit(repo, "scripts/verify_records_attestations.py", "epoch")
    workflow_push = _commit(repo, "records/wave.txt", "workflow records push")

    _git(repo, "checkout", "-q", "-b", "pr-site", epoch)
    _commit(repo, "site/page.tsx", "site-only change")
    _git(repo, "checkout", "-q", "main")
    noop_merge = _merge(repo, "merge pr-site", "pr-site")

    _git(repo, "checkout", "-q", "-b", "pr-records", epoch)
    smuggled = _commit(repo, "records/smuggled.txt", "smuggled records")
    _git(repo, "checkout", "-q", "main")
    content_merge = _merge(repo, "merge pr-records", "pr-records")

    monkeypatch.setattr(provenance, "ROOT", repo)
    monkeypatch.setattr(provenance, "git_output", lambda *a: _git(repo, *a))

    # Exemption is classification, never enumeration: everything stays listed.
    listed = provenance.records_commits(f"{epoch}..HEAD")
    assert noop_merge in listed
    assert smuggled in listed
    assert content_merge in listed

    assert provenance.merge_is_records_noop(noop_merge, epoch) is True
    assert provenance.merge_is_records_noop(content_merge, epoch) is False
    # Non-merges never take the exemption path.
    assert provenance.merge_is_records_noop(workflow_push, epoch) is False

    # The update-branch shape (live case cf9f6509, 2026-07-31): merging
    # main INTO a lagging branch makes a commit whose records tree matches
    # its SECOND parent (main). It reaches main history via the PR merge
    # and must be exempt the same way.
    _git(repo, "checkout", "-q", "-b", "pr-refresh", epoch)
    _commit(repo, "site/other.tsx", "another site-only change")
    update_merge = _merge(repo, "merge main into pr-refresh", "main")
    assert provenance.merge_is_records_noop(update_merge, epoch) is True


def test_rollback_shaped_merges_never_self_exempt(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A merge whose FIRST parent predates the epoch cannot claim the no-op
    exemption even when records/** is byte-identical to that parent — the
    ancient-rollback shape stays attestation-required forever."""

    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    base = _commit(repo, "records/base.txt", "base records")
    epoch = _commit(repo, "scripts/verify_records_attestations.py", "epoch")
    _commit(repo, "records/wave.txt", "workflow records push")

    _git(repo, "checkout", "-q", base)
    rollback = _merge(repo, "rollback merge", "main", "-s", "ours")

    monkeypatch.setattr(provenance, "ROOT", repo)
    assert provenance.merge_is_records_noop(rollback, epoch) is False


def test_range_closure_refuses_unattested_content_change(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Parent-order trickery: a merge onto a stale post-epoch first parent is
    individually no-op-exempt, but a push range whose endpoints disagree
    about records content with nothing attestable in between fails closed."""

    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _commit(repo, "records/base.txt", "base records")
    epoch = _commit(repo, "scripts/verify_records_attestations.py", "epoch")
    stale = _commit(repo, "records/state.txt", "records v1")
    tip = _commit(repo, "records/state.txt", "records v2")

    _git(repo, "checkout", "-q", stale)
    swap = _merge(repo, "parent-swap merge", "main", "-s", "ours")

    monkeypatch.setattr(provenance, "ROOT", repo)
    # In isolation the crafted merge looks like a no-op vs its first parent…
    assert provenance.merge_is_records_noop(swap, epoch) is True
    # …but the push range's endpoints disagree about records content.
    with pytest.raises(
        provenance.ProvenanceError, match="no commit in .* requires"
    ):
        provenance.enforce_range_content_closure(f"{tip}..{swap}", [])
    # Endpoints that agree pass, and any attestable commit short-circuits.
    provenance.enforce_range_content_closure(f"{stale}..{swap}", [])
    provenance.enforce_range_content_closure(f"{tip}..{swap}", [tip])

    # Same trap with the parents reversed (records tree == stale SECOND
    # parent), built with commit-tree because no merge strategy produces
    # it honestly: exempt in isolation, refused by the range closure.
    stale_tree = _git(repo, "rev-parse", f"{stale}^{{tree}}")
    swap2 = _git(
        repo,
        "-c", "user.name=t", "-c", "user.email=t@example.com",
        "commit-tree", stale_tree, "-p", tip, "-p", stale,
        "-m", "reversed parent-swap",
    )
    assert provenance.merge_is_records_noop(swap2, epoch) is True
    with pytest.raises(
        provenance.ProvenanceError, match="no commit in .* requires"
    ):
        provenance.enforce_range_content_closure(f"{tip}..{swap2}", [])
