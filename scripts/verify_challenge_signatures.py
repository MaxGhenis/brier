#!/usr/bin/env python3
"""Verify submitter signatures across the challenge inbox.

The sweep always covers the ENTIRE inbox, fail-closed:

- inbox hygiene: entries must be ``<login>/<cell>.json`` submissions,
  their sidecar bundles, or the root README.md; symlinks (including a
  symlinked inbox root), orphan bundles, and any other name shape fail
  the run — the anchored name shape also makes printed paths
  injection-proof;
- every signed submission: the Sigstore bundle cryptographically verifies
  over the submission's exact bytes (Fulcio chain, Merkle inclusion proof
  against the signed checkpoint, Signed Entry Timestamp — delegated to
  sigstore-python), a Signed Entry Timestamp is REQUIRED (a bundle whose
  ``integratedTime`` is not SET-bound has no authenticated Rekor
  chronology and is refused), the raw bundle metadata must match the
  verified transparency-log entry exactly, and the SET-bound
  ``integratedTime`` strictly precedes the target's release instant
  (registry day floor, or ``--release-at`` when the caller knows the
  actual first-print instant);
- unsigned submissions are reported and remain schema-valid — signing is
  optional (issue #52; PR #49 grandfathered). Full intake validation
  happens at publication, not here.

``--submission`` narrows only which provenance blocks are exported —
hygiene and signature verification always cover everything discovered. A
present-but-invalid bundle always fails the run: a broken proof is
tampering evidence, not a missing option.

``--json`` writes exactly one JSON document (the
``thesis_challenge_signature_v1`` provenance blocks the publish adapter
stores alongside each record's merge SHA) to stdout; all diagnostics go
to stderr. ``--staging`` verifies against Sigstore staging trust roots
for rehearsals and refuses ``--json``: staging proof must never feed the
adapter. A successful default exit does NOT mean every signature precedes
its release — publishers must read ``precedesRelease`` (or gate with
``--require-prerelease``).

Exit codes: 0 verified/clean, 1 verification or hygiene failure, 2 usage.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from challenge_signing import (  # noqa: E402
    ChallengeSigningError,
    audit_inbox,
    inbox_root,
    load_submission,
    parse_utc_instant,
    signature_provenance_block,
    verify_submission,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def _block_root(inbox: pathlib.Path) -> pathlib.Path:
    """Provenance paths are repo-relative: <root>/challenge/inbox -> <root>.

    An inbox that is not at the canonical relpath (tests, ad-hoc trees)
    anchors paths at the inbox itself rather than inventing a repo layout.
    """

    resolved = inbox.resolve()
    if resolved.parts[-2:] == ("challenge", "inbox"):
        return resolved.parents[1]
    return resolved


def _sanitized(path: pathlib.Path) -> str:
    """Render a possibly attacker-named path without control characters."""

    text = str(path)
    if text.isprintable():
        return text
    return repr(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inbox",
        type=pathlib.Path,
        default=None,
        help="inbox root (default: challenge/inbox)",
    )
    parser.add_argument(
        "--submission",
        type=pathlib.Path,
        action="append",
        default=None,
        help="export provenance blocks only for these submissions "
        "(repeatable); hygiene and verification still cover the whole inbox",
    )
    parser.add_argument(
        "--release-at",
        default=None,
        help="ISO-8601 release instant override (e.g. the actual first-print "
        "instant at scoring time); default derives a conservative day floor "
        "from the registered target",
    )
    parser.add_argument(
        "--targets-file",
        type=pathlib.Path,
        default=None,
        help="alternate ledger-targets.generated.ts (tests)",
    )
    parser.add_argument(
        "--require-signature",
        action="store_true",
        help="fail if any submission is unsigned (future prize/ranked tier)",
    )
    parser.add_argument(
        "--require-prerelease",
        action="store_true",
        help="fail if any signed submission's SET-bound Rekor time does not "
        "precede the release instant",
    )
    parser.add_argument(
        "--require-identity",
        default=None,
        help="enforce this certificate identity (needs --require-issuer; "
        "both must be nonempty)",
    )
    parser.add_argument(
        "--require-issuer",
        default=None,
        help="OIDC issuer for --require-identity",
    )
    parser.add_argument(
        "--staging",
        action="store_true",
        help="verify against Sigstore staging trust roots (rehearsals only; "
        "incompatible with --json)",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="do not refresh Sigstore trust roots over the network",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="write exactly one JSON document of "
        "thesis_challenge_signature_v1 provenance blocks to stdout "
        "(diagnostics go to stderr)",
    )
    args = parser.parse_args(argv)

    if args.staging and args.json:
        print(
            "--staging is a rehearsal mode; refusing --json export so "
            "staging proof can never feed the publish adapter",
            file=sys.stderr,
        )
        return 2

    info_stream = sys.stderr if args.json else sys.stdout

    def info(message: str) -> None:
        print(message, file=info_stream)

    release_at = None
    if args.release_at is not None:
        try:
            release_at = parse_utc_instant(args.release_at, label="--release-at")
        except ChallengeSigningError as exc:
            print(str(exc), file=sys.stderr)
            return 2

    root = args.inbox or inbox_root()
    try:
        audit = audit_inbox(root)
    except ChallengeSigningError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    failures: list[str] = []
    for orphan in audit.orphan_bundles:
        failures.append(f"orphan bundle without a submission: {_sanitized(orphan)}")
    for unexpected in audit.unexpected:
        failures.append(
            "unexpected inbox entry (not a <login>/<cell>.json submission "
            f"or its bundle): {_sanitized(unexpected)}"
        )

    exported = None
    if args.submission:
        exported = {path.resolve() for path in args.submission}
        known = {p.resolve() for p in audit.submissions}
        for path in sorted(exported - known):
            failures.append(f"requested submission is not in the inbox: {path}")

    blocks = []
    signed = unsigned = 0
    for submission in audit.submissions:
        relative = submission.resolve().relative_to(root.resolve())
        bundle = audit.bundles.get(submission)
        if bundle is None:
            try:
                load_submission(submission)
            except ChallengeSigningError as exc:
                failures.append(str(exc))
                continue
            unsigned += 1
            if args.require_signature:
                failures.append(f"unsigned submission: {relative}")
            else:
                info(f"unsigned {relative} (signature optional; schema-checked only)")
            continue
        try:
            verification = verify_submission(
                submission,
                bundle,
                release_at=release_at,
                targets_path=args.targets_file,
                expected_identity=args.require_identity,
                expected_issuer=args.require_issuer,
                staging=args.staging,
                offline=args.offline,
            )
        except ChallengeSigningError as exc:
            failures.append(str(exc))
            continue
        signed += 1
        verdict = (
            "precedes release"
            if verification.precedes_release
            else "does NOT precede release"
        )
        info(
            f"signed   {relative}: rekor logIndex="
            f"{verification.verified.log_index} "
            f"integrated={verification.integrated_time_utc:%Y-%m-%dT%H:%M:%SZ} "
            f"[{verification.verified.environment}] {verdict}"
        )
        if args.require_prerelease and not verification.precedes_release:
            failures.append(
                f"signature does not precede the release instant: {relative}"
            )
        if exported is None or submission.resolve() in exported:
            blocks.append(
                signature_provenance_block(verification, repo_root=_block_root(root))
            )

    if args.json:
        print(json.dumps(blocks, indent=2, sort_keys=True))
    info(
        f"checked {len(audit.submissions)} submission(s): {signed} signed, "
        f"{unsigned} unsigned, {len(failures)} failure(s)"
    )
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
