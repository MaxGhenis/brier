#!/usr/bin/env python3
"""Keyless-sign a challenge submission before opening the inbox PR.

One command from any laptop (https://github.com/ThesisInstitute/thesis/issues/52):

    uvx --from sigstore sigstore sign challenge/inbox/<you>/<cell>.json

That is the whole protocol — a browser window opens for GitHub OIDC, the
signature lands in the Rekor transparency log, and the bundle is written
beside the submission as ``<cell>.json.sigstore.json``. Commit both files
in the PR. cosign works too:

    cosign sign-blob --new-bundle-format \
        --bundle challenge/inbox/<you>/<cell>.json.sigstore.json \
        challenge/inbox/<you>/<cell>.json

This wrapper adds inbox guardrails around the same sigstore invocation:
it validates the submission parses against the schema, refuses paths
outside ``challenge/inbox/``, refuses to overwrite an existing bundle,
and after signing reports the Rekor entry (log index, UUID, integrated
time) plus a transparency-log search link. Signing is optional — unsigned
submissions stay valid.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from challenge_signing import (  # noqa: E402
    ChallengeSigningError,
    bundle_path_for,
    inbox_root,
    load_submission,
    parse_bundle_metadata,
    sha256_file,
)


def _require_inbox_path(submission: pathlib.Path) -> pathlib.Path:
    resolved = submission.resolve()
    root = inbox_root().resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ChallengeSigningError(
            f"submissions live under {root}; refusing to sign {submission}"
        ) from None
    if resolved.suffix != ".json" or resolved.name.endswith(".sigstore.json"):
        raise ChallengeSigningError(
            f"expected a <cell>.json submission file: {submission}"
        )
    return resolved


def sign(submission: pathlib.Path, *, staging: bool) -> pathlib.Path:
    submission = _require_inbox_path(submission)
    load_submission(submission)  # schema sanity before any network flow
    bundle = bundle_path_for(submission)
    if bundle.exists():
        raise ChallengeSigningError(
            f"refusing to overwrite an existing bundle: {bundle} "
            "(a re-sign would orphan any copy already cited in a PR)"
        )
    command = [
        sys.executable,
        "-m",
        "sigstore",
        *(["--staging"] if staging else []),
        "sign",
        "--bundle",
        str(bundle),
        str(submission),
    ]
    try:
        completed = subprocess.run(command, check=False)
    except FileNotFoundError as exc:  # pragma: no cover - interpreter exists
        raise ChallengeSigningError(str(exc)) from exc
    if completed.returncode != 0:
        raise ChallengeSigningError(
            "sigstore sign failed; if the package is missing run "
            "`uv sync --extra challenge` or use the uvx one-liner from "
            "docs/challenge-signing.md"
        )
    if not bundle.is_file():
        raise ChallengeSigningError(
            f"sigstore sign reported success but wrote no bundle: {bundle}"
        )
    return bundle


def report(submission: pathlib.Path, bundle: pathlib.Path) -> None:
    metadata = parse_bundle_metadata(json.loads(bundle.read_text()))
    integrated = datetime.fromtimestamp(metadata.integrated_time, tz=timezone.utc)
    print(f"signed   {submission}")
    print(f"bundle   {bundle}")
    print(f"sha256   {sha256_file(submission)}")
    print(f"rekor    logIndex={metadata.log_index} uuid={metadata.entry_uuid}")
    print(f"time     {integrated.strftime('%Y-%m-%dT%H:%M:%SZ')} (Rekor integrated)")
    print(f"inspect  https://search.sigstore.dev/?logIndex={metadata.log_index}")
    print("Commit BOTH files in your challenge PR.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=pathlib.Path)
    parser.add_argument(
        "--staging",
        action="store_true",
        help="sign against the Sigstore staging environment (rehearsal only; "
        "staging bundles do not verify against production trust roots)",
    )
    args = parser.parse_args(argv)
    try:
        bundle = sign(args.submission, staging=args.staging)
        report(args.submission, bundle)
    except ChallengeSigningError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
