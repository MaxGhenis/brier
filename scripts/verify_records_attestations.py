#!/usr/bin/env python3
"""Verify workflow provenance for every records commit on main.

Every commit that touches records/** after the enforcement epoch must carry a
GitHub artifact attestation (Sigstore provenance) over the canonical subject
built by scripts/attest_subject.py, signed by one of the allowlisted
records-publishing workflows on refs/heads/main. A records commit with no
valid attestation — a direct local push, a foreign workflow, a forged
subject — fails this check and turns main red.

Scope and honesty: this is a detective control, not prevention. It binds each
records commit to the exact workflow run that produced it, complementing the
RFC 3161 witness chain (which proves when, not who). It inherits the standard
SLSA caveats: an actor who can rewrite the workflows themselves on main, or
who controls repository administration, is outside this control's reach.

The enforcement epoch is self-anchoring: the commit that introduced this
script. Commits before it predate the control and are exempt.

Usage:
  verify_records_attestations.py                  # epoch..HEAD (full audit)
  verify_records_attestations.py --range A..B     # push-event range
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from attest_subject import subject_bytes, subject_name  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
SELF_RELPATH = "scripts/verify_records_attestations.py"
PROTECTED_PREFIX = "records/"
ALLOWED_WORKFLOWS = {
    ".github/workflows/roll-docket.yml",
    ".github/workflows/strategy-docket.yml",
    ".github/workflows/prospect-docket.yml",
    ".github/workflows/record-forecasts.yml",
    ".github/workflows/resolve-and-rebuild.yml",
}
ALLOWED_REF = "refs/heads/main"
SIGNER_RE = re.compile(
    r"github\.com/(?P<repo>[^/]+/[^/]+)/(?P<workflow>\.github/workflows/[^@]+)"
    r"@(?P<ref>refs/\S+)"
)
FRESH_COMMIT_GRACE_SECONDS = 15 * 60
VERIFY_RETRIES = 6
VERIFY_RETRY_DELAY_SECONDS = 20

# The immutable GitHub repository id, invariant across transfers/renames.
# Every accepted attestation's certificate must name it, so certificates
# minted by a DIFFERENT repository that later occupies a historical slug
# can never vouch for a records commit (Sol era-review finding 1).
PINNED_SOURCE_REPOSITORY_ID = "1113415529"

# Repository identity eras. A GitHub transfer/rename changes the slug that
# appears inside both the signed subject bytes and the Sigstore certificate
# identity, but attestations are immutable: each commit must be verified
# against the slug that was current when its workflow signed it. GitHub's
# attestation store is keyed by the OWNER at signing time and does not
# follow a transfer, so each era also pins the owner account whose store
# holds its bundles (verified empirically 2026-07-22: the historical
# store lives under /users/MaxGhenis, repository_id 1113415529). Each
# entry pins (boundary_commit, slug, store_owner): a commit that is an
# ancestor of the boundary was attested under that slug and is looked up
# via `gh attestation verify --owner store_owner`. Entries are consulted
# in order, first ancestor match wins; commits matching no era use the
# live slug with a --repo lookup.
REPOSITORY_ERAS: tuple[tuple[str, str, str], ...] = (
    # 2026-07-22: MaxGhenis/brier transferred to ThesisInstitute and
    # renamed to thesis. Everything up to this boundary (the last main
    # commit before the transfer) was attested under the old slug.
    ("e62143459d4acc2d527529c774e35a6331008a8c", "MaxGhenis/brier", "MaxGhenis"),
)

# Records commits that were pushed OUTSIDE the allowlisted workflows and
# therefore have no attestation to verify. Each waiver is a permanent,
# public admission, never a silent pass: the audit prints a WAIVED line.
# 2026-07-22: an operator session pushed the Next50 aging/broadband wave
# from a local machine instead of through the workflow path; the cells'
# content is covered by the witness chain, but their push provenance is
# not, and this list is the honest record of that miss. Shrink-only.
WAIVED_UNATTESTED_COMMITS: dict[str, str] = {
    "8d1e6aa5c678035218a2ed310b259d855108b058": "Next50 wave local push",
    "56f14cc760f2a55cc789e499a0129a51f2e8bb75": "Next50 wave local push",
    "9e5d820916408af773912aa97267e4fc914c4d94": "Next50 wave local push",
    "4a4ac86dbf92b51a14d9fd29626bdd19b482cf0a": "Next50 wave local push",
    "08aac46200a7745621fd64f828734c716dcf7a69": "Next50 wave local push",
    # 2026-07-22 late: the QCEW aircraft target completion was also pushed
    # locally, hours after the waiver list shipped — same operator-session
    # pattern, admitted the same way. The preventive ruleset (blocking
    # non-workflow pushes to records/**) is the actual fix.
    "8ad16ab611ab89cacaff570f43e419e0552bdbaf": "QCEW completion local push",
    # 2026-07-24: the broadband-65+ vintage repair — the anchored
    # network-enabled rerun replacing the 5-year-corrupted published cell
    # before its 2026-09-10 resolution — was an operator-session local
    # push, admitted the same way. Same fix remains: the preventive
    # ruleset blocking non-workflow pushes to records/**.
    "2c02b44382a0e88e0b5104ff82fb891367be64e8": (
        "Broadband vintage-repair local push"
    ),
}
ERA_BOUNDARY_RE = re.compile(r"^[0-9a-f]{40}$")
ERA_SLUG_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
ERA_OWNER_RE = re.compile(r"^[A-Za-z0-9-]+$")


def validate_repository_eras() -> None:
    """Structurally validate EVERY era entry before any matching.

    First-match resolution must never mask a malformed later entry
    (Sol era-review finding 3).
    """

    for boundary, slug, owner in REPOSITORY_ERAS:
        if not ERA_BOUNDARY_RE.fullmatch(boundary):
            raise ProvenanceError(f"malformed era boundary: {boundary!r}")
        if not ERA_SLUG_RE.fullmatch(slug):
            raise ProvenanceError(f"malformed era slug: {slug!r}")
        if not ERA_OWNER_RE.fullmatch(owner):
            raise ProvenanceError(f"malformed era owner: {owner!r}")
        exists = subprocess.run(
            ["git", "cat-file", "-e", f"{boundary}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
        )
        if exists.returncode != 0:
            raise ProvenanceError(
                f"era boundary is not a commit in this repository: {boundary}"
            )


def era_repository(commit: str, current: str) -> tuple[str, str] | None:
    """(slug, store_owner) for an era commit, or None for the live era."""

    validate_repository_eras()
    for boundary, slug, owner in REPOSITORY_ERAS:
        proc = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, boundary],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            return (slug, owner)
        if proc.returncode != 1:
            raise ProvenanceError(
                f"era ancestry check failed for {commit} vs {boundary}: "
                f"{proc.stderr.strip()}"
            )
    return None


class ProvenanceError(RuntimeError):
    """A records commit failed provenance verification."""


def git_output(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, stderr=subprocess.PIPE
    ).strip()


def enforcement_epoch() -> str:
    commits = git_output(
        "log", "--full-history", "--diff-filter=A", "--format=%H",
        "--", SELF_RELPATH,
    ).splitlines()
    if len(commits) != 1:
        raise ProvenanceError(
            "enforcement epoch must be exactly one introducing commit for "
            f"{SELF_RELPATH}; found {len(commits)}"
        )
    return commits[0]


def records_commits(rev_range: str) -> list[str]:
    # --full-history: path simplification may otherwise drop a records
    # commit that arrived on a side branch (Sol review P1-2).
    output = git_output(
        "log", "--full-history", "--format=%H", rev_range,
        "--", PROTECTED_PREFIX,
    )
    return output.splitlines() if output else []


def commit_age_seconds(commit: str) -> int:
    committed = int(git_output("show", "-s", "--format=%ct", commit))
    return max(0, int(time.time()) - committed)


def repository_slug() -> str:
    url = git_output("remote", "get-url", "origin")
    match = re.search(r"github\.com[:/]+([^/]+/[^/.]+)", url)
    if not match:
        raise ProvenanceError(f"cannot derive repository slug from {url!r}")
    return match.group(1)


def extract_certificate_identities(payload: object) -> set[str]:
    """Signer URIs from verificationResult.signature.certificate ONLY.

    Log-line cosmetics, never authorization (gh enforces identity) — but a
    key merely NAMED certificate anywhere in the attester-influenced
    statement must not spoof the logged signer (Sol P2-6).
    """

    identities: set[str] = set()
    results = payload if isinstance(payload, list) else [payload]
    for result in results:
        if not isinstance(result, dict):
            continue
        certificate = (
            (result.get("verificationResult") or {})
            .get("signature", {})
            .get("certificate", {})
            if isinstance(result.get("verificationResult"), dict)
            else {}
        )
        if not isinstance(certificate, dict):
            continue
        for value in certificate.values():
            if isinstance(value, str):
                for match in SIGNER_RE.finditer(value):
                    identities.add(match.group(0))
    return identities


def cert_identity_pattern(repository: str) -> str:
    """The exact signer identities gh must enforce during verification.

    Identity checking happens INSIDE gh against the Sigstore certificate —
    never by scanning verification output, which contains attester-influenced
    statement fields alongside the certificate.
    """

    workflows = "|".join(re.escape(workflow) for workflow in sorted(ALLOWED_WORKFLOWS))
    return (
        f"^https://github\\.com/{re.escape(repository)}/"
        f"({workflows})@{re.escape(ALLOWED_REF)}$"
    )


def pinned_id_results(payload: object) -> list:
    """The verified results whose certificate names the pinned repo id.

    The id is immutable across transfers and renames, so a certificate
    minted by any other repository — including a future occupant of a
    historical slug — never counts (Sol era-review finding 1). gh returns
    one array entry per verified attestation; results are FILTERED rather
    than all-required, so a coexisting foreign-id result can neither
    authorize a commit nor deny service, and (Sol round-3 P2) can never
    control the logged signer attribution either. Certificates are read
    only from verificationResult.signature.certificate, never
    attester-influenced statement fields.
    """

    results = payload if isinstance(payload, list) else [payload]
    pinned = []
    for result in results:
        if not isinstance(result, dict):
            continue
        verification = result.get("verificationResult")
        certificate = (
            verification.get("signature", {}).get("certificate", {})
            if isinstance(verification, dict)
            else {}
        )
        if not isinstance(certificate, dict):
            continue
        if (
            certificate.get("sourceRepositoryIdentifier")
            == PINNED_SOURCE_REPOSITORY_ID
        ):
            pinned.append(result)
    if not pinned:
        raise ProvenanceError(
            "no verified certificate carries pinned source repository id "
            + PINNED_SOURCE_REPOSITORY_ID
        )
    return pinned


def verify_commit(
    commit: str, repository: str, era: tuple[str, str] | None = None
) -> str:
    """Verify one commit's attestation; return the accepted signer identity.

    ``era`` is ``(slug, store_owner)`` for commits signed before a
    transfer/rename, else ``None`` for the live era. Era commits verify
    ENTIRELY under their era identity — subject bytes and certificate
    regex use the era slug, and the lookup uses ``--owner store_owner``
    because GitHub's attestation store is keyed by the signing-time owner
    and does not follow transfers. Live commits look up via ``--repo``.
    Both paths additionally require the certificate to carry the pinned
    immutable repository id, so neither slug reuse nor owner-store
    breadth can admit a foreign repository's certificate.
    """

    if era is None:
        era_slug, store_flag = repository, ("--repo", repository)
    else:
        era_slug, store_flag = era[0], ("--owner", era[1])
    if not ERA_SLUG_RE.fullmatch(era_slug):
        raise ProvenanceError(f"malformed verification slug: {era_slug!r}")
    payload = subject_bytes(era_slug, commit)
    with tempfile.TemporaryDirectory() as tmp:
        subject_path = pathlib.Path(tmp) / subject_name(commit)
        subject_path.write_bytes(payload)
        attempts = (
            VERIFY_RETRIES
            if commit_age_seconds(commit) < FRESH_COMMIT_GRACE_SECONDS
            else 1
        )
        last_error = ""
        for attempt in range(1, attempts + 1):
            completed = subprocess.run(
                [
                    "gh",
                    "attestation",
                    "verify",
                    str(subject_path),
                    *store_flag,
                    "--cert-identity-regex",
                    cert_identity_pattern(era_slug),
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if completed.returncode == 0:
                # gh already enforced the certificate identity. The pinned
                # repository id is enforced HERE, fail-closed, on the same
                # verified certificate; the identity parse-back is for the
                # log line only.
                try:
                    parsed = json.loads(completed.stdout)
                except json.JSONDecodeError as exc:
                    raise ProvenanceError(
                        f"{commit}: gh verify output was not JSON"
                    ) from exc
                pinned = pinned_id_results(parsed)
                identities = extract_certificate_identities(pinned)
                return sorted(identities)[0] if identities else "<verified>"
            last_error = (completed.stderr or completed.stdout).strip()
            if attempt < attempts:
                time.sleep(VERIFY_RETRY_DELAY_SECONDS)
        raise ProvenanceError(
            f"{commit}: no valid attestation for its records push subject "
            f"({last_error.splitlines()[-1] if last_error else 'no detail'})"
        )


def commit_in_scope(commit: str, epoch: str) -> bool:
    """Exempt ONLY commits proven ancestors of the epoch.

    They predate the control. A commit merely incomparable to the epoch —
    e.g. a side branch forked pre-epoch and merged after — stays in scope;
    descendant-of-epoch filtering silently exempted those (Sol P1-2).
    Merge-base errors are fatal, never an exemption.
    """

    probe = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, epoch],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if probe.returncode == 0:
        return False
    if probe.returncode == 1:
        return True
    raise ProvenanceError(
        f"merge-base --is-ancestor failed for {commit}: "
        f"{probe.stderr.decode(errors='replace').strip()}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--range",
        dest="rev_range",
        help="git rev range A..B to check (default: enforcement epoch..HEAD)",
    )
    args = parser.parse_args()

    repository = repository_slug()
    epoch = enforcement_epoch()
    rev_range = args.rev_range
    if not rev_range or rev_range.startswith("0" * 40):
        rev_range = f"{epoch}..HEAD"
    elif ".." not in rev_range:
        raise ProvenanceError(f"--range must be A..B, got {rev_range!r}")

    validate_repository_eras()
    commits = [
        commit
        for commit in records_commits(rev_range)
        if commit_in_scope(commit, epoch)
    ]
    if not commits:
        print(f"records provenance OK: no records commits in {rev_range}")
        return 0

    failures: list[str] = []
    waived = 0
    for commit in commits:
        if commit in WAIVED_UNATTESTED_COMMITS:
            waived += 1
            print(
                f"records provenance WAIVED: {commit} "
                f"({WAIVED_UNATTESTED_COMMITS[commit]})"
            )
            continue
        try:
            identity = verify_commit(
                commit, repository, era_repository(commit, repository)
            )
            print(f"records provenance OK: {commit} <- {identity}")
        except ProvenanceError as exc:
            failures.append(str(exc))
            print(f"records provenance FAIL: {exc}", file=sys.stderr)

    if failures:
        print(
            f"\n{len(failures)} records commit(s) lack allowlisted workflow "
            "provenance",
            file=sys.stderr,
        )
        return 1
    verified = len(commits) - waived
    summary = f"records provenance OK: {verified} commit(s) verified"
    if waived:
        summary += f", {waived} permanently waived (unattested local pushes)"
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
