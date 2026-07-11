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


def verify_commit(commit: str, repository: str) -> str:
    """Verify one commit's attestation; return the accepted signer identity."""

    payload = subject_bytes(repository, commit)
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
                    "--repo",
                    repository,
                    "--cert-identity-regex",
                    cert_identity_pattern(repository),
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if completed.returncode == 0:
                # gh already enforced the certificate identity; parse it back
                # out of the certificate fields for the log line only.
                try:
                    parsed = json.loads(completed.stdout)
                except json.JSONDecodeError:
                    parsed = None
                identities = extract_certificate_identities(parsed)
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

    commits = [
        commit
        for commit in records_commits(rev_range)
        if commit_in_scope(commit, epoch)
    ]
    if not commits:
        print(f"records provenance OK: no records commits in {rev_range}")
        return 0

    failures: list[str] = []
    for commit in commits:
        try:
            identity = verify_commit(commit, repository)
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
    print(f"records provenance OK: {len(commits)} commit(s) verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
