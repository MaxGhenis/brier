#!/usr/bin/env python3
"""Build the canonical attestation subject for a records push.

Every workflow that pushes records/** to main attests a small canonical
subject file naming the pushed commit. The subject is reconstructable from
git alone, so a verifier can independently derive the expected bytes for any
commit and ask GitHub's attestation store whether an allowlisted workflow
signed them. This binds each records commit to the exact workflow run that
produced it (who/how), complementing the RFC 3161 witness chain (when).

Usage: attest_subject.py --commit <sha> --out <path> [--repository owner/name]
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from canonical_json import canonical_bytes  # noqa: E402

DEFAULT_REPOSITORY = "MaxGhenis/brier"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SUBJECT_SCHEMA = "thesis_records_push_subject_v1"


def subject_bytes(repository: str, commit: str) -> bytes:
    if not COMMIT_RE.fullmatch(commit):
        raise ValueError(f"subject requires a full 40-hex commit sha: {commit!r}")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError(f"invalid repository slug: {repository!r}")
    return (
        canonical_bytes(
            {
                "schemaVersion": SUBJECT_SCHEMA,
                "repository": repository,
                "commit": commit,
            }
        )
        + b"\n"
    )


def subject_name(commit: str) -> str:
    return f"records-push-{commit}.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", required=True)
    parser.add_argument("--out", type=pathlib.Path, required=True)
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    args = parser.parse_args()
    payload = subject_bytes(args.repository, args.commit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(payload)
    print(f"wrote {args.out} ({len(payload)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
