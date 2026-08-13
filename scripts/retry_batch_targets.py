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
  resolve-by-bound, and manifest rows carrying comparison or cursor
  context (`comparisonTarget`, `previousTarget`, `expectedReleaseDate`)
  are refused outright. Bounded targets belong to the attested local
  lane; rows whose original run context cannot be reconstructed from
  trusted state alone are not retryable here. Validation `anchors` ARE
  reconstructable: they come from the committed docket entry's extras
  (never the manifest row), and a row claiming different anchors than
  the docket is refused.
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
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import register_targets  # noqa: E402
import spawned_cells_to_ts  # noqa: E402

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
    rebuilt = register_targets.rebuild_registered_target(
        snapshot, path=snapshot_path, root=ROOT
    )
    # Validation anchors reconstruct from the committed docket entry,
    # never the manifest row: the roll splats entry extras into batch
    # targets, so the trusted copy is the docket's. A row claiming
    # different anchors than the docket is refused rather than trusted;
    # a docket entry without anchors leaves the rerun unanchored exactly
    # as a fresh roll would.
    docket = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    entries = docket.get("series", [])
    matches = register_targets.matching_docket_templates(contract, entries)
    if len(matches) > 1:
        raise RetrySelectionError(
            f"{label} has ambiguous committed docket authority for "
            f"{contract['series']} period {contract['period']}"
        )
    entry = matches[0] if matches else None
    docket_anchors = ((entry or {}).get("extras") or {}).get("anchors")
    row_anchors = row_target.get("anchors")
    if row_anchors is not None and row_anchors != docket_anchors:
        raise RetrySelectionError(
            f"{label} manifest anchors disagree with the committed docket"
        )
    if docket_anchors is not None:
        rebuilt["anchors"] = docket_anchors
    return rebuilt


def published_catalog_index(repo_root: pathlib.Path) -> dict[str, str | None]:
    """slug -> dataPointId for every published cell, from the EVALUATED
    site catalog.

    The batch manifest freezes outcomes at the original roll; a later
    retry may have published some of its failed targets, and the publish
    leg refuses a regenerated duplicate of a published cell (run
    31728802794). The selector therefore reads CURRENT publication
    state. That state comes from executing the catalog module itself
    (scripts/dump_published_cells.ts under bun) — a regex over TS source
    is not authoritative: measured against the evaluated catalog it
    missed 186 dynamically constructed slugs (OEWS, SNAP) and invented
    10 phantoms, and a phantom is authorization to split a conditional
    pair. Every failure here refuses selection; an empty or partial
    view must never fall through to "nothing is published".
    """

    script = repo_root / "scripts" / "dump_published_cells.ts"
    try:
        proc = subprocess.run(
            ["bun", str(script)],
            capture_output=True,
            text=True,
            cwd=repo_root,
            timeout=300,
        )
    except FileNotFoundError as exc:
        raise RetrySelectionError(
            "published-catalog evaluation needs bun on PATH; refusing to "
            "select without an authoritative publication view"
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise RetrySelectionError(
            "published-catalog evaluation timed out"
        ) from exc
    if proc.returncode != 0:
        raise RetrySelectionError(
            "published-catalog evaluation failed: "
            + proc.stderr.strip()[-400:]
        )
    try:
        rows = json.loads(proc.stdout)
    except ValueError as exc:
        raise RetrySelectionError(
            f"published-catalog evaluation emitted non-JSON: {exc}"
        ) from exc
    if not isinstance(rows, list):
        raise RetrySelectionError(
            "published-catalog evaluation emitted non-list JSON"
        )
    if not rows:
        raise RetrySelectionError(
            "published-catalog evaluation emitted an empty catalog; "
            "refusing — the site catalog is never empty, so an empty "
            "view means the evaluation broke, not that nothing is "
            "published"
        )
    index: dict[str, str | None] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("slug"), str):
            raise RetrySelectionError("published-catalog row lacks a slug")
        slug = row["slug"]
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
            raise RetrySelectionError(
                f"published-catalog slug {slug!r} is not a well-formed "
                "catalog slug"
            )
        data_point_id = row.get("dataPointId")
        if data_point_id is not None and not isinstance(data_point_id, str):
            raise RetrySelectionError(
                f"published-catalog row {slug!r} has a non-string dataPointId"
            )
        if slug in index and index[slug] != data_point_id:
            raise RetrySelectionError(
                f"published-catalog slug {slug!r} appears with conflicting "
                "registration identities"
            )
        index[slug] = data_point_id
    return index


def _published_identity_matches(
    slug: str, published: dict[str, str | None], row: dict
) -> bool:
    """True iff the published cell at ``slug`` IS this row's registration.

    Publication satisfies a target (or a pair sibling) only when the
    published cell's dataPointId equals the one in the row's VERIFIED
    registration snapshot — slug membership alone is not identity: a
    fresh registration can reuse a slug whose old occupant published
    under a different dataPointId, and treating that as satisfied would
    split a conditional pair. A published cell without a dataPointId
    never matches (fail closed).
    """

    if slug not in published:
        return False
    published_id = published[slug]
    if published_id is None:
        return False
    contract = load_verified_snapshot(row["target"], label=f"target {slug}")[0][
        "targets"
    ][0]
    return contract.get("dataPointId") == published_id


def raw_text_catalog_slugs(repo_root: pathlib.Path) -> frozenset[str]:
    """Slug literals scraped from site data text — the corroboration view.

    Independent of the bun evaluation: every roll-published cell is a
    static json.dumps literal in an auto-*.ts file, so a slug that this
    scrape sees but the evaluated index lacks means the evaluator
    regressed to a valid-but-partial catalog (the round-3 replay: a
    zero-exit singleton index authorized re-emitting published
    targets). The scrape may contain phantoms and misses dynamic
    entries — it is only ever used to REFUSE, never to authorize.
    """

    site_data = repo_root / "site" / "src" / "data"
    return frozenset(
        spawned_cells_to_ts.existing_slugs(
            site_data, site_data / "__retry_selector_no_output__.ts"
        )
    )


def _corroborate_absence(
    slug: str,
    published: dict[str, str | None],
    raw_text_slugs: frozenset[str],
) -> None:
    """Refuse when the evaluated index and the raw-text scrape disagree.

    Absence from the index is the load-bearing direction — it is what
    authorizes emitting a target — so it must be corroborated: if the
    slug's literal appears in site data text while the evaluated
    catalog claims it is unpublished, the evaluation is not to be
    trusted and selection refuses.
    """

    if slug not in published and slug in raw_text_slugs:
        raise RetrySelectionError(
            f"evaluated catalog omits slug {slug!r} whose literal appears "
            "in site data; the publication view is partial or broken — "
            "refusing selection"
        )


def select_retry_targets(
    manifest: dict,
    *,
    slugs: list[str] | None,
    allow_succeeded: bool,
    now_utc: dt.datetime,
    published: dict[str, str | None],
    raw_text_slugs: frozenset[str] = frozenset(),
) -> list[dict]:
    results = manifest["results"]
    by_slug: dict[str, dict] = {}
    for index, result in enumerate(results):
        target = result.get("target")
        if not isinstance(target, dict) or not target.get("catalogSlug"):
            raise RetrySelectionError(f"result {index} lacks a batch target")
        if not isinstance(result.get("ok"), bool):
            raise RetrySelectionError(f"result {index} has no boolean recorded outcome")
        slug = str(target["catalogSlug"])
        if slug in by_slug:
            raise RetrySelectionError(f"duplicate result for {slug}")
        by_slug[slug] = result

    if slugs is None:
        chosen = []
        for slug, row in by_slug.items():
            if row.get("ok"):
                continue
            _corroborate_absence(slug, published, raw_text_slugs)
            if slug in published:
                if not _published_identity_matches(slug, published, row):
                    raise RetrySelectionError(
                        f"slug {slug!r} is published under a different "
                        "registration than this batch's verified snapshot; "
                        "refusing — this target can never publish and the "
                        "registry needs human review"
                    )
                # A later retry already published this exact registration;
                # never re-emit a published target (roll seed invariant).
                print(f"  skip {slug}: already published")
                continue
            chosen.append(slug)
        if not chosen:
            raise RetrySelectionError(
                "no unpublished failed targets remain in this batch; "
                "every recorded failure is already published"
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
            _corroborate_absence(slug, published, raw_text_slugs)
            if slug in published:
                if _published_identity_matches(slug, published, by_slug[slug]):
                    raise RetrySelectionError(
                        f"slug {slug!r} is already published; a published "
                        "target is never re-emitted"
                    )
                raise RetrySelectionError(
                    f"slug {slug!r} is published under a different "
                    "registration than this batch's verified snapshot; "
                    "refusing — this target can never publish and the "
                    "registry needs human review"
                )
            chosen.append(slug)

    targets = []
    rebuilt_by_slug: dict[str, dict] = {}
    for slug in chosen:
        label = f"target {slug}"
        rebuilt = rebuild_target_from_snapshot(by_slug[slug]["target"], label=label)
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
    # Retrying a lone failed arm is valid only when every failed sibling
    # is either selected alongside it or already published (by the
    # original run or a later retry); otherwise the retry must carry the
    # whole unpublished failed set together. Arm-ness of BOTH sides comes
    # from verified registration snapshots — manifest rows contribute
    # only membership and recorded outcomes, so omitting fields from a
    # sibling row cannot hide the pair.
    if any(rebuilt.get("conditional") is not None for rebuilt in targets):
        contract_by_slug = {
            slug: load_verified_snapshot(result["target"], label=f"target {slug}")[0][
                "targets"
            ][0]
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
                if sibling_result.get("ok") or sibling in rebuilt_by_slug:
                    continue
                _corroborate_absence(sibling, published, raw_text_slugs)
                if _published_identity_matches(sibling, published, sibling_result):
                    continue
                if sibling in published:
                    raise RetrySelectionError(
                        f"target {slug} is a conditional arm whose sibling "
                        f"{sibling} slug is published under a different "
                        "registration than the sibling's verified snapshot; "
                        "the pair is wedged and the registry needs human "
                        "review"
                    )
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
            published=published_catalog_index(ROOT),
            raw_text_slugs=raw_text_catalog_slugs(ROOT),
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
