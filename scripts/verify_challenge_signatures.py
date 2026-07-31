#!/usr/bin/env python3
"""Verify submitter signatures across the challenge inbox.

For every submission under ``challenge/inbox/`` this checks, fail-closed:

- inbox hygiene: only submissions, their sidecar bundles, and README.md;
  no symlinks, no orphan bundles (a bundle whose submission is gone);
- for each signed submission: the Sigstore bundle cryptographically
  verifies over the submission's exact bytes (Fulcio chain, Rekor
  inclusion, signed entry timestamp — delegated to sigstore-python),
  the bundle's digest matches the file, and the Rekor ``integratedTime``
  strictly precedes the target's release instant (registry day floor, or
  ``--release-at`` when the caller knows the actual first-print instant);
- unsigned submissions are reported and remain valid — signing is
  optional (issue #52; PR #49 is grandfathered).

A present-but-invalid bundle always fails the run: a broken proof is
tampering evidence, not a missing option. ``--json`` emits the exact
``thesis_challenge_signature_v1`` provenance blocks the publish adapter
stores alongside each record's merge SHA.

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
        help="verify only these submissions (repeatable)",
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
        help="fail if any signed submission's Rekor time does not precede "
        "the release instant",
    )
    parser.add_argument(
        "--require-identity",
        default=None,
        help="enforce this certificate identity (needs --require-issuer)",
    )
    parser.add_argument(
        "--require-issuer",
        default=None,
        help="OIDC issuer for --require-identity",
    )
    parser.add_argument(
        "--staging",
        action="store_true",
        help="verify against Sigstore staging trust roots (rehearsals only)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit thesis_challenge_signature_v1 provenance blocks",
    )
    args = parser.parse_args(argv)

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
        failures.append(f"orphan bundle without a submission: {orphan}")
    for unexpected in audit.unexpected:
        failures.append(
            f"unexpected inbox entry (not a regular submission "
            f"or bundle): {unexpected}"
        )

    selected = audit.submissions
    if args.submission:
        requested = {path.resolve() for path in args.submission}
        selected = [p for p in audit.submissions if p.resolve() in requested]
        missing = requested - {p.resolve() for p in selected}
        for path in sorted(missing):
            failures.append(f"requested submission is not in the inbox: {path}")

    blocks = []
    signed = unsigned = 0
    for submission in selected:
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
                print(f"unsigned {relative} (valid; signing is optional)")
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
        print(
            f"signed   {relative}: rekor logIndex="
            f"{verification.metadata.log_index} "
            f"integrated={verification.integrated_time_utc:%Y-%m-%dT%H:%M:%SZ} "
            f"{verdict}"
        )
        if args.require_prerelease and not verification.precedes_release:
            failures.append(
                f"signature does not precede the release instant: {relative}"
            )
        blocks.append(
            signature_provenance_block(verification, repo_root=_block_root(root))
        )

    if args.json:
        print(json.dumps(blocks, indent=2, sort_keys=True))
    print(
        f"checked {len(selected)} submission(s): {signed} signed, "
        f"{unsigned} unsigned, {len(failures)} failure(s)"
    )
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
