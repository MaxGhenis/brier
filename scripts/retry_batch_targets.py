#!/usr/bin/env python3
"""Rebuild a trusted roll-targets file from a committed batch manifest.

The roll workflow's generation leg runs once per registration wave; a
target whose analyst run fails validation (a unit-string mismatch, a
provenance slip, a transient fetch) keeps its immutable registration but
never receives a cell, and after TARGET_PREREGISTRATION_ORPHAN_GRACE_DAYS
the registration can only terminate in the expired-unforecast ratchet.
This selector closes that gap: it reconstructs the exact batch-target
dicts the failed runs consumed — from the committed, immutable batch
manifest, not from any mutable input — so the roll workflow can rerun
generation against the original registrations while their grace window
is still open.

Trust properties:
- Input is a committed manifest (``records/thesis-analyst/batches/…``);
  every selected target must name a registration snapshot that exists in
  the tree and whose content hash matches both the target dict and the
  snapshot filename. Registration is then re-verified by the workflow via
  ``register_targets.py --reuse-existing-only`` and the usual
  ``--bind-registration-commits`` passes; this script adds no authority.
- Only targets whose recorded run failed are eligible by default;
  ``--slugs`` narrows (never widens past the manifest) and refuses slugs
  whose recorded run succeeded unless ``--allow-succeeded`` is given.
- A target outside its orphan grace window is refused outright: past
  grace the honest terminal state is the expired-unforecast ratchet, not
  a late run against a stale information set.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

BATCH_MANIFEST_SCHEMA = "thesis_batch_manifest_v1"

# Must equal TARGET_PREREGISTRATION_ORPHAN_GRACE_DAYS in
# site/src/data/ledger-targets.ts — the site enforces the same window on
# every build, and tests/test_retry_batch_targets.py pins the two
# constants together.
ORPHAN_GRACE_DAYS = 7


class RetrySelectionError(Exception):
    pass


def _parse_utc(value: str, *, label: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise RetrySelectionError(f"invalid UTC instant for {label}: {value!r}") from exc
    if parsed.tzinfo is None:
        raise RetrySelectionError(f"{label} must be timezone-aware: {value!r}")
    return parsed.astimezone(dt.timezone.utc)


def load_manifest(path: pathlib.Path) -> dict:
    relative = path.resolve()
    batches_root = (ROOT / "records" / "thesis-analyst" / "batches").resolve()
    if batches_root not in relative.parents:
        raise RetrySelectionError(
            "batch manifest must live under records/thesis-analyst/batches/ "
            f"(got {path})"
        )
    try:
        manifest = json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise RetrySelectionError(f"batch manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RetrySelectionError(f"batch manifest is not JSON: {path}") from exc
    if manifest.get("schemaVersion") != BATCH_MANIFEST_SCHEMA:
        raise RetrySelectionError(
            "batch manifest schemaVersion must be "
            f"{BATCH_MANIFEST_SCHEMA!r}, got {manifest.get('schemaVersion')!r}"
        )
    results = manifest.get("results")
    if not isinstance(results, list) or not results:
        raise RetrySelectionError("batch manifest has no results")
    return manifest


def verify_registration_binding(target: dict, *, label: str) -> None:
    relative = target.get("targetRegistrationPath")
    content_hash = target.get("targetContentHash")
    if not isinstance(relative, str) or not isinstance(content_hash, str):
        raise RetrySelectionError(
            f"{label} lacks targetRegistrationPath/targetContentHash"
        )
    if not re.fullmatch(r"[0-9a-f]{64}", content_hash):
        raise RetrySelectionError(f"{label} content hash is not 64-hex")
    parts = pathlib.PurePosixPath(relative)
    if parts.is_absolute() or ".." in parts.parts:
        raise RetrySelectionError(f"{label} has an unsafe registration path")
    snapshot_path = ROOT.joinpath(*parts.parts)
    if not snapshot_path.is_file():
        raise RetrySelectionError(
            f"{label} registration snapshot missing from tree: {relative}"
        )
    if not parts.name.endswith(f"-{content_hash}.json"):
        raise RetrySelectionError(
            f"{label} registration filename does not carry its content hash"
        )


def select_retry_targets(
    manifest: dict,
    *,
    slugs: list[str] | None,
    allow_succeeded: bool,
    now_utc: dt.datetime,
) -> list[dict]:
    results = manifest["results"]
    by_slug: dict[str, dict] = {}
    for index, result in enumerate(results):
        target = result.get("target")
        if not isinstance(target, dict) or not target.get("catalogSlug"):
            raise RetrySelectionError(f"result {index} lacks a batch target")
        slug = str(target["catalogSlug"])
        if slug in by_slug:
            raise RetrySelectionError(f"duplicate result for {slug}")
        by_slug[slug] = result

    if slugs is None:
        chosen = [slug for slug, row in by_slug.items() if not row.get("ok")]
        if not chosen:
            raise RetrySelectionError(
                "no failed targets in this batch; pass --slugs to retry "
                "specific targets"
            )
    else:
        chosen = []
        for slug in slugs:
            if slug not in by_slug:
                raise RetrySelectionError(
                    f"slug {slug!r} is not in this batch manifest"
                )
            if by_slug[slug].get("ok") and not allow_succeeded:
                raise RetrySelectionError(
                    f"slug {slug!r} succeeded in the recorded run; pass "
                    "--allow-succeeded to rerun it anyway"
                )
            chosen.append(slug)

    targets = []
    for slug in chosen:
        target = by_slug[slug]["target"]
        label = f"target {slug}"
        registered_at = target.get("registeredAtUtc")
        if not registered_at:
            raise RetrySelectionError(f"{label} lacks registeredAtUtc")
        registered = _parse_utc(registered_at, label=f"{label} registeredAtUtc")
        deadline = registered + dt.timedelta(days=ORPHAN_GRACE_DAYS)
        if now_utc >= deadline:
            raise RetrySelectionError(
                f"{label} left its orphan grace window at "
                f"{deadline.isoformat().replace('+00:00', 'Z')}; the honest "
                "terminal state is the expired-unforecast ratchet, not a "
                "late rerun"
            )
        verify_registration_binding(target, label=label)
        targets.append(target)
    return targets


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=pathlib.Path, required=True)
    parser.add_argument("--out", type=pathlib.Path, required=True)
    parser.add_argument(
        "--slugs",
        help="comma-separated catalog slugs (default: every failed target)",
    )
    parser.add_argument("--allow-succeeded", action="store_true")
    parser.add_argument(
        "--now-utc",
        help="override the clock (tests only); ISO-8601 UTC",
    )
    args = parser.parse_args()
    try:
        manifest = load_manifest(args.batch)
        now = (
            _parse_utc(args.now_utc, label="--now-utc")
            if args.now_utc
            else dt.datetime.now(dt.timezone.utc)
        )
        slugs = None
        if args.slugs:
            slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
            if not slugs:
                raise RetrySelectionError("--slugs given but empty")
        targets = select_retry_targets(
            manifest,
            slugs=slugs,
            allow_succeeded=args.allow_succeeded,
            now_utc=now,
        )
    except RetrySelectionError as exc:
        print(f"retry selection failed: {exc}", file=sys.stderr)
        return 1
    args.out.write_text(json.dumps({"targets": targets}, indent=1) + "\n")
    for target in targets:
        print(f"  retry {target['catalogSlug']} ({target.get('dataPointId')})")
    print(f"{len(targets)} targets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
