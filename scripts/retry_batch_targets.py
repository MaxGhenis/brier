#!/usr/bin/env python3
"""Rebuild a trusted roll-targets file from a committed batch manifest.

The roll workflow's generation leg runs once per registration wave; a
target whose analyst run fails validation (a unit-string mismatch, a
provenance slip, a transient fetch) keeps its immutable registration but
never receives a cell, and after TARGET_PREREGISTRATION_ORPHAN_GRACE_DAYS
the registration can only terminate in the expired-unforecast ratchet.
This selector closes that gap: the roll workflow can rerun generation
against the original registrations while their grace window is open.

Trust properties:
- The committed manifest only NAMES which targets failed and where their
  registration snapshots live. Every emitted batch target is
  reconstructed from the registration snapshot itself — the immutable,
  content-hashed record — via the same field mapping the registration
  writer uses (`register_targets._target_registration_fields`). Nothing
  else from the manifest row survives, so a tampered manifest cannot
  smuggle prompt- or validation-affecting fields (resolution overrides,
  anchors, comparison flags) into the rerun. The snapshot's content hash
  is recomputed from its bytes and must match both the manifest row and
  the snapshot filename.
- This mode is restricted to the ordinary release-calendar lane:
  manifests carrying a generation ticket, targets whose contracts are
  resolve-by-bound, and manifest rows carrying comparison/anchored/
  cursor context (`comparisonTarget`, `anchors`, `previousTarget`,
  `expectedReleaseDate`) are refused outright. Bounded targets belong to
  the attested local lane; rows whose original run context cannot be
  reconstructed from trusted state alone are not retryable here.
- A target outside its orphan grace window — or registered in the
  future — is refused outright: past grace the honest terminal state is
  the expired-unforecast ratchet, not a late run against a stale
  information set. The workflow re-enforces grace at trusted
  publication time against the authenticated run timestamps
  (docket_publication.py --enforce-run-grace), so selection-time
  approval cannot leak past the deadline.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import register_targets  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent

BATCH_MANIFEST_SCHEMA = "thesis_batch_manifest_v1"

# Must equal TARGET_PREREGISTRATION_ORPHAN_GRACE_DAYS in
# site/src/data/ledger-targets.ts — the site enforces the same window on
# every build, and tests/test_retry_batch_targets.py pins the two
# constants together.
ORPHAN_GRACE_DAYS = 7

# The complete key population an ordinary release-calendar registration
# contract may carry (register_targets.build_contract). A snapshot with
# any other key is from a lane this selector does not understand and is
# refused rather than partially reconstructed.
KNOWN_CONTRACT_KEYS = frozenset(
    {
        "series",
        "period",
        "catalogSlug",
        "dataPointId",
        "country",
        "unit",
        "valueScale",
        "sourceBinding",
        "seedPeriod",
        "conditional",
        "conditionId",
        "conditionDeadline",
        "resolutionDate",
        "resolutionDateBasis",
    }
)

# Manifest-row context that affected the original run but cannot be
# reconstructed from trusted state by this selector. Rows carrying any
# of these are refused (not silently stripped) so the rerun can never
# quietly differ from the recorded run's contract.
UNRECONSTRUCTABLE_ROW_KEYS = (
    "comparisonTarget",
    "anchors",
    "previousTarget",
    "expectedReleaseDate",
)


class RetrySelectionError(Exception):
    pass


def _parse_utc(value: str, *, label: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise RetrySelectionError(
            f"invalid UTC instant for {label}: {value!r}"
        ) from exc
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
    if "generationTicket" in manifest:
        raise RetrySelectionError(
            "batch manifest carries a generation ticket; ticketed runs "
            "belong to the attested local lane and are never retried here"
        )
    results = manifest.get("results")
    if not isinstance(results, list) or not results:
        raise RetrySelectionError("batch manifest has no results")
    return manifest


def load_verified_snapshot(
    row_target: dict, *, label: str
) -> tuple[dict, pathlib.Path]:
    """Load a row's registration snapshot, proving path and content hash."""

    relative = row_target.get("targetRegistrationPath")
    claimed_hash = row_target.get("targetContentHash")
    if not isinstance(relative, str) or not isinstance(claimed_hash, str):
        raise RetrySelectionError(
            f"{label} lacks targetRegistrationPath/targetContentHash"
        )
    if not re.fullmatch(r"[0-9a-f]{64}", claimed_hash):
        raise RetrySelectionError(f"{label} content hash is not 64-hex")
    parts = pathlib.PurePosixPath(relative)
    if (
        parts.is_absolute()
        or ".." in parts.parts
        or pathlib.PurePosixPath("records/targets") not in parts.parents
    ):
        raise RetrySelectionError(f"{label} has an unsafe registration path")
    snapshot_path = ROOT.joinpath(*parts.parts)
    if not snapshot_path.is_file():
        raise RetrySelectionError(
            f"{label} registration snapshot missing from tree: {relative}"
        )
    snapshot = json.loads(snapshot_path.read_text())
    content_hash = register_targets.registration_content_hash(snapshot)
    if content_hash != claimed_hash:
        raise RetrySelectionError(
            f"{label} snapshot bytes hash to {content_hash[:12]}…, not the "
            "manifest's recorded content hash"
        )
    if not parts.name.endswith(f"-{content_hash}.json"):
        raise RetrySelectionError(
            f"{label} registration filename does not carry its content hash"
        )
    targets = snapshot.get("targets")
    if not isinstance(targets, list) or len(targets) != 1:
        raise RetrySelectionError(
            f"{label} registration must contain exactly one target: {relative}"
        )
    # Snapshot-to-row identity: a row that names a valid but UNRELATED
    # registration (the round-3 sibling-substitution attack) is refused
    # here, for every consumer — reconstruction and pair scans alike.
    if targets[0].get("catalogSlug") != row_target.get("catalogSlug"):
        raise RetrySelectionError(
            f"{label} snapshot binds {targets[0].get('catalogSlug')!r}, not "
            "the manifest row's slug"
        )
    return snapshot, snapshot_path


def rebuild_target_from_snapshot(row_target: dict, *, label: str) -> dict:
    """Reconstruct the trusted batch target from its registration snapshot.

    The manifest row contributes only the snapshot's location and the
    claimed content hash; every emitted field comes from the snapshot
    contract through the registration writer's own field mapping.
    """

    for key in UNRECONSTRUCTABLE_ROW_KEYS:
        if key in row_target:
            raise RetrySelectionError(
                f"{label} carries {key!r}, run context this selector cannot "
                "reconstruct from trusted state; not retryable here"
            )
    snapshot, snapshot_path = load_verified_snapshot(row_target, label=label)
    contract = snapshot["targets"][0]
    unknown = set(contract) - KNOWN_CONTRACT_KEYS
    if unknown:
        raise RetrySelectionError(
            f"{label} contract carries unknown field(s) {sorted(unknown)}; "
            "refusing to reconstruct a run context this selector does not "
            "understand"
        )
    if contract.get("resolutionDateBasis") not in (None, "release-calendar"):
        raise RetrySelectionError(
            f"{label} is a {contract.get('resolutionDateBasis')!r} target; "
            "bounded targets belong to the attested generation-ticket lane"
        )
    registered_at = snapshot.get("registeredAtUtc")
    if row_target.get("registeredAtUtc") not in (None, registered_at):
        raise RetrySelectionError(
            f"{label} manifest registeredAtUtc disagrees with the snapshot"
        )
    return register_targets.rebuild_registered_target(
        snapshot, path=snapshot_path, root=ROOT
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
        if not isinstance(result.get("ok"), bool):
            raise RetrySelectionError(
                f"result {index} has no boolean recorded outcome"
            )
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
    rebuilt_by_slug: dict[str, dict] = {}
    for slug in chosen:
        label = f"target {slug}"
        rebuilt = rebuild_target_from_snapshot(
            by_slug[slug]["target"], label=label
        )
        registered = _parse_utc(
            rebuilt["registeredAtUtc"], label=f"{label} registeredAtUtc"
        )
        if registered > now_utc:
            raise RetrySelectionError(
                f"{label} claims a future registration instant; refusing"
            )
        deadline = registered + dt.timedelta(days=ORPHAN_GRACE_DAYS)
        if now_utc >= deadline:
            raise RetrySelectionError(
                f"{label} left its orphan grace window at "
                f"{deadline.isoformat().replace('+00:00', 'Z')}; the honest "
                "terminal state is the expired-unforecast ratchet, not a "
                "late rerun"
            )
        rebuilt_by_slug[slug] = rebuilt
        targets.append(rebuilt)

    # Pair atomicity (roll_docket F10): a conditional pair's unpublished
    # arms are one unit — publishing one arm ahead of a sibling that also
    # remains unpublished would hand the later arm extra information.
    # Retrying a lone failed arm is valid only when every sibling in the
    # recorded batch succeeded (published); otherwise the retry must
    # carry the whole failed set together. Arm-ness of BOTH sides comes
    # from verified registration snapshots — manifest rows contribute
    # only membership and recorded outcomes, so omitting fields from a
    # sibling row cannot hide the pair.
    if any(rebuilt.get("conditional") is not None for rebuilt in targets):
        contract_by_slug = {
            slug: load_verified_snapshot(
                result["target"], label=f"target {slug}"
            )[0]["targets"][0]
            for slug, result in by_slug.items()
        }
        for slug, rebuilt in rebuilt_by_slug.items():
            if rebuilt.get("conditional") is None:
                continue
            for sibling, sibling_result in by_slug.items():
                sibling_contract = contract_by_slug[sibling]
                if (
                    sibling == slug
                    or sibling_contract.get("conditional") is None
                    or sibling_contract.get("series") != rebuilt.get("series")
                    or sibling_contract.get("period") != rebuilt.get("period")
                ):
                    continue
                if (
                    not sibling_result.get("ok")
                    and sibling not in rebuilt_by_slug
                ):
                    raise RetrySelectionError(
                        f"target {slug} is a conditional arm whose sibling "
                        f"{sibling} also failed and is not selected; "
                        "unpublished pair arms retry together or not at all"
                    )
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
