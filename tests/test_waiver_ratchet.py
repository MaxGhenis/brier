"""Grandfather sets may only shrink.

Each waiver in waivers.json names an exception population to a fail-closed
rule that newer machinery enforces (schema cutovers, docket binding
templates, custody inventory v2). These tests recompute every population
from live repository state and fail the moment one exceeds its manifest:
growth requires a deliberate, reviewable edit to waivers.json, never a
silent join. Pattern adapted from Axiom's validation-waiver ratchet.
"""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "waivers.json").read_text())
WAIVERS = MANIFEST["waivers"]


def registration_schema_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for path in sorted((ROOT / "records" / "targets").glob("*.json")):
        schema = json.loads(path.read_text()).get("schemaVersion", "?")
        counts[schema] = counts.get(schema, 0) + 1
    return counts


def test_manifest_shape() -> None:
    assert MANIFEST["schemaVersion"] == "thesis_waiver_manifest_v1"
    for name, waiver in WAIVERS.items():
        assert waiver.get("description"), f"waiver {name} lacks a description"
        assert ("frozenCount" in waiver) != ("members" in waiver), (
            f"waiver {name} must declare exactly one of frozenCount/members"
        )


def test_pre_cutover_registration_schemas_are_frozen() -> None:
    counts = registration_schema_counts()
    # Frozen exactly: these snapshots are immutable append-only history, so
    # the population can neither grow (cutover forbids minting) nor shrink
    # (records are never deleted). Any drift in either direction is an
    # integrity signal, not a ratchet event.
    assert counts.get("thesis_target_registration_v1", 0) == (
        WAIVERS["pre_cutover_v1_registrations"]["frozenCount"]
    )
    assert counts.get("thesis_target_registration_v2", 0) == (
        WAIVERS["pre_cutover_v2_registrations"]["frozenCount"]
    )


def test_templateless_docket_series_only_shrink() -> None:
    docket = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    actual = {
        entry["series"]
        for entry in docket["series"]
        if not (
            isinstance(entry.get("extras"), dict)
            and isinstance(entry["extras"].get("sourceBinding"), dict)
        )
    }
    waived = set(WAIVERS["templateless_docket_series"]["members"])
    joined = sorted(actual - waived)
    assert not joined, (
        "docket series without a committed sourceBinding template joined "
        f"outside the waiver manifest: {joined} — new series must ship with "
        "a template, or be deliberately added to waivers.json"
    )
    healed = sorted(waived - actual)
    if healed:
        # Shrinking is the goal; keep the manifest honest as members heal.
        print(
            "waiver manifest lists template-less series that now have "
            f"templates — prune them from waivers.json: {healed}"
        )


def test_legacy_incomplete_custody_roots_are_frozen() -> None:
    timeline = json.loads(
        (ROOT / "records" / "witnessed-timeline.json").read_text()
    )
    legacy = [
        root
        for root, row in timeline["custodyRoots"].items()
        if row.get("inventoryStatus") == "legacy-incomplete"
    ]
    # Custody inventory v2 predates every new run: nothing may ever join
    # the legacy-incomplete population.
    assert len(legacy) == (
        WAIVERS["legacy_incomplete_custody_roots"]["frozenCount"]
    ), (
        "the legacy-incomplete custody root population changed; it is "
        "immutable history and must stay frozen"
    )
    for root, row in timeline["custodyRoots"].items():
        assert row.get("inventoryStatus") in {"complete", "legacy-incomplete"}, (
            f"unknown inventoryStatus for {root}: {row.get('inventoryStatus')!r}"
        )
