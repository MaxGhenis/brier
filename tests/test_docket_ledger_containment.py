from __future__ import annotations

import hashlib
import json
import pathlib
import re
import urllib.request
from typing import Any

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCKET_PATH = ROOT / "scripts" / "docket_series.json"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "ledger_series_catalog.json"
PIN_PATH = ROOT / "site" / "src" / "data" / "ledger-pin.json"
CATALOG_PATH = "ledger/series_catalog.json"
# Frozen on catalog generator v3: identity = (concept, geography
# level/id/vintage, entity), uuid authority = the ledger's append-only
# series_uuid_registry (digest embedded below), source labels demoted to
# per-row source_concepts provenance. Any upstream shape drift must fail
# here loudly.
CATALOG_TOP_LEVEL_KEYS = {
    "generator_version",
    "observations_sha256",
    "observation_rows",
    "docket_seed_sha256",
    "uuid_registry_sha256",
    "suspect_segments",
    "stripped_segments",
    "ambiguous_aliases",
    "series",
}
CATALOG_OPTIONAL_TOP_LEVEL_KEYS = {"comment"}
CADENCE_MAP = {
    "weekly": "week_ending",
    "monthly": "month",
    "quarterly": "quarter",
    "annual": "year",
}
CATALOG_ROW_KEYS = {
    "uuid",
    "concept",
    "family_patterns",
    "status",
    "unit",
    "cadence",
    "geography",
    "entity",
    "sources",
    "aliases",
    "source_concepts",
    "rid_patterns",
    "first_observed_period",
    "last_observed_period",
    "observation_count",
}
# Pure magnitude units and their scale relative to one unit. Kept in sync,
# deliberately by duplication, with scripts/stamp_docket_ledger_refs.py:
# this gate must not import the tool whose output it audits.
UNIT_SCALE = {"units": 1.0, "thousands": 1e3, "millions": 1e6, "billions": 1e9}


def _units_agree(
    target_unit: object, catalog_unit: object, value_scale: object
) -> bool:
    """Whether a docket targetUnit is the catalog unit modulo valueScale.

    Identical units always agree (valueScale describes the transform from
    the publisher's raw feed, whose reference frame varies by entry).
    Differing units agree only when both are pure magnitude units and the
    declared valueScale converts catalog-unit values into target-unit
    values: value_in_target = value_in_catalog * valueScale.
    """
    if target_unit is None or catalog_unit is None:
        return True
    if target_unit == catalog_unit:
        return True
    if type(value_scale) not in (int, float) or not value_scale:
        return False
    target_scale = UNIT_SCALE.get(target_unit)
    catalog_scale = UNIT_SCALE.get(catalog_unit)
    if target_scale is None or catalog_scale is None:
        return False
    return abs(target_scale - catalog_scale / value_scale) < 1e-9


def _object(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        pytest.fail(f"{label} is not valid JSON: {exc}")
    assert type(value) is dict, f"{label} must be a JSON object"
    return value


def _load(path: pathlib.Path, label: str) -> dict[str, Any]:
    return _object(path.read_bytes(), label)


def _assert_containment(
    catalog: dict[str, Any],
    label: str,
    *,
    docket_path: pathlib.Path = DOCKET_PATH,
) -> None:
    docket = _load(docket_path, "docket")
    missing_top_level = CATALOG_TOP_LEVEL_KEYS - set(catalog)
    unknown_top_level = set(catalog) - (
        CATALOG_TOP_LEVEL_KEYS | CATALOG_OPTIONAL_TOP_LEVEL_KEYS
    )
    assert not missing_top_level, (
        f"{label} is missing frozen top-level fields: {sorted(missing_top_level)}"
    )
    assert not unknown_top_level, (
        f"{label} has unknown top-level fields: {sorted(unknown_top_level)}"
    )
    assert "comment" not in catalog or type(catalog["comment"]) is str, (
        f"{label}.comment must be a string when present"
    )
    assert type(catalog["generator_version"]) is int, (
        f"{label}.generator_version must be an integer"
    )
    for digest_key in (
        "observations_sha256",
        "docket_seed_sha256",
        "uuid_registry_sha256",
    ):
        assert type(catalog[digest_key]) is str and re.fullmatch(
            r"[0-9a-f]{64}", catalog[digest_key]
        ), f"{label}.{digest_key} must be a SHA-256 digest"
    assert (
        type(catalog["observation_rows"]) is int
        and catalog["observation_rows"] >= 0
    ), f"{label}.observation_rows must be a non-negative integer"
    for list_key in ("suspect_segments", "ambiguous_aliases"):
        assert type(catalog[list_key]) is list and all(
            type(item) is str for item in catalog[list_key]
        ), f"{label}.{list_key} must be a list of strings"
    stripped = catalog["stripped_segments"]
    assert type(stripped) is dict and all(
        type(segment) is str
        and type(concepts) is list
        and concepts
        and all(type(c) is str for c in concepts)
        for segment, concepts in stripped.items()
    ), f"{label}.stripped_segments must map spellings to concept lists"
    docket_rows = docket.get("series")
    catalog_rows = catalog.get("series")
    assert type(docket_rows) is list, "docket.series must be a list"
    assert type(catalog_rows) is list, f"{label}.series must be a list"

    malformed_catalog_rows: list[str] = []
    by_uuid: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(catalog_rows):
        if type(row) is not dict:
            malformed_catalog_rows.append(f"row {index}: not an object")
            continue
        if set(row) != CATALOG_ROW_KEYS:
            malformed_catalog_rows.append(
                f"row {index} ({row.get('concept')}): "
                f"missing={sorted(CATALOG_ROW_KEYS - set(row))}, "
                f"unknown={sorted(set(row) - CATALOG_ROW_KEYS)}"
            )
            continue
        concept = row["concept"]
        if type(concept) is not str or not concept:
            malformed_catalog_rows.append(f"row {index}: invalid concept {concept!r}")
            continue
        uuid = row["uuid"]
        if type(uuid) is not str or not re.fullmatch(
            r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
            uuid,
        ):
            malformed_catalog_rows.append(
                f"row {index} ({concept}): uuid {uuid!r} is not canonical UUIDv4"
            )
            continue
        if uuid in by_uuid:
            malformed_catalog_rows.append(
                f"duplicate uuid {uuid} "
                f"({by_uuid[uuid]['concept']}, {concept})"
            )
            continue
        by_uuid[uuid] = row
    assert not malformed_catalog_rows, (
        f"{label} violates the frozen catalog row schema:\n- "
        + "\n- ".join(malformed_catalog_rows)
    )

    missing_refs: list[str] = []
    mismatched_refs: list[str] = []
    cadence_mismatches: list[str] = []
    unit_mismatches: list[str] = []
    uuid_owners: dict[str, list[str]] = {}
    for index, entry in enumerate(docket_rows):
        series = entry.get("series") if type(entry) is dict else None
        ledger = entry.get("ledger") if type(entry) is dict else None
        if (
            type(series) is not str
            or type(ledger) is not dict
            or type(ledger.get("uuid")) is not str
            or not ledger["uuid"]
            or type(ledger.get("concept")) is not str
            or not ledger["concept"]
        ):
            missing_refs.append(f"row {index}: {series!r}")
            continue

        uuid_owners.setdefault(ledger["uuid"], []).append(series)
        # Rows are addressed by uuid: catalog v3 concepts are not unique
        # (state splits and entity-drift lineages share a concept), and the
        # uuid is exactly the identity the registry promises never to
        # re-mint.
        catalog_row = by_uuid.get(ledger["uuid"])
        if catalog_row is None:
            mismatched_refs.append(
                f"{series}: catalog has no row with uuid {ledger['uuid']}"
            )
            continue
        if catalog_row["concept"] != ledger["concept"]:
            mismatched_refs.append(
                f"{series}: docket concept {ledger['concept']!r} != catalog "
                f"concept {catalog_row['concept']!r} for uuid {ledger['uuid']}"
            )
        aliases = catalog_row["aliases"]
        if series != catalog_row["concept"] and series not in aliases:
            mismatched_refs.append(
                f"{series}: neither canonical concept nor alias of "
                f"{catalog_row['concept']}"
            )

        docket_cadence = entry.get("cadence")
        expected_cadence = CADENCE_MAP.get(docket_cadence)
        if expected_cadence is None:
            cadence_mismatches.append(
                f"{series}: unsupported docket cadence {docket_cadence!r}"
            )
        elif catalog_row["status"] == "observed":
            if catalog_row["cadence"] != expected_cadence:
                cadence_mismatches.append(
                    f"{series}: docket {docket_cadence} maps to "
                    f"{expected_cadence}, catalog has {catalog_row['cadence']}"
                )
        else:
            # Docket-only rows were minted from this registry, so their cadence
            # is inherited rather than independent evidence for containment.
            assert catalog_row["status"] == "docket-only", (
                f"{series}: unsupported catalog status {catalog_row['status']!r}"
            )

        extras = entry.get("extras")
        target_unit = extras.get("targetUnit") if type(extras) is dict else None
        value_scale = extras.get("valueScale") if type(extras) is dict else None
        if not _units_agree(target_unit, catalog_row["unit"], value_scale):
            unit_mismatches.append(
                f"{series}: docket targetUnit={target_unit!r} does not agree "
                f"with catalog unit={catalog_row['unit']!r} under declared "
                f"valueScale={value_scale!r}"
            )

    duplicate_uuids = {
        uuid: owners for uuid, owners in uuid_owners.items() if len(owners) > 1
    }
    failures: list[str] = []
    if missing_refs:
        failures.append(
            "missing ledger.uuid/ledger.concept:\n- " + "\n- ".join(missing_refs)
        )
    if mismatched_refs:
        failures.append(
            "catalog reference mismatches:\n- " + "\n- ".join(mismatched_refs)
        )
    if cadence_mismatches:
        failures.append("cadence mismatches:\n- " + "\n- ".join(cadence_mismatches))
    if unit_mismatches:
        failures.append("unit mismatches:\n- " + "\n- ".join(unit_mismatches))
    if duplicate_uuids:
        failures.append(
            "duplicate docket ledger UUIDs:\n- "
            + "\n- ".join(
                f"{uuid}: {', '.join(owners)}"
                for uuid, owners in sorted(duplicate_uuids.items())
            )
        )
    assert not failures, f"docket is not contained in {label}:\n" + "\n".join(failures)


def _catalog_shell(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "generator_version": 3,
        "observations_sha256": "0" * 64,
        "observation_rows": 1,
        "docket_seed_sha256": "1" * 64,
        "uuid_registry_sha256": "2" * 64,
        "suspect_segments": [],
        "stripped_segments": {},
        "ambiguous_aliases": [],
        "series": rows,
    }


def _catalog_row(**overrides: Any) -> dict[str, Any]:
    row = {
        "uuid": "00000000-0000-4000-8000-000000000001",
        "concept": "unrelated.series",
        "family_patterns": ["unrelated.series.{P}"],
        "status": "observed",
        "unit": None,
        "cadence": "month",
        "geography": {
            "id": "0100000US",
            "level": "country",
            "vintage": "current",
            "name": "United States",
        },
        "entity": {"name": "economy", "role": "aggregate"},
        "sources": ["test"],
        "aliases": [],
        "source_concepts": [],
        "rid_patterns": ["unrelated.series.{P}.first_print"],
        "first_observed_period": "2029-12",
        "last_observed_period": "2029-12",
        "observation_count": 1,
    }
    row.update(overrides)
    return row


def _docket_file(tmp_path: pathlib.Path, entries: list[dict[str, Any]]):
    docket_path = tmp_path / "docket.json"
    docket_path.write_text(json.dumps({"series": entries}, indent=2) + "\n")
    return docket_path


def test_docket_is_contained_in_frozen_catalog_fixture() -> None:
    _assert_containment(_load(FIXTURE_PATH, "frozen catalog fixture"), "fixture")


def test_containment_rejects_unrelated_catalog_reference(
    tmp_path: pathlib.Path,
) -> None:
    docket_path = _docket_file(
        tmp_path,
        [
            {
                "series": "docket.series",
                "cadence": "monthly",
                "slug": "docket-series-{month}-{year}",
                "ledger": {
                    "uuid": "00000000-0000-4000-8000-000000000001",
                    "concept": "unrelated.series",
                },
            }
        ],
    )
    catalog = _catalog_shell([_catalog_row()])
    with pytest.raises(AssertionError, match="neither canonical concept nor alias"):
        _assert_containment(catalog, "test catalog", docket_path=docket_path)


def test_containment_resolves_duplicate_concepts_by_uuid(
    tmp_path: pathlib.Path,
) -> None:
    # Catalog v3: one concept, two identities (entity-drift lineages). The
    # docket pin addresses the row by uuid, so containment must too.
    lineage_a = _catalog_row(
        uuid="00000000-0000-4000-8000-00000000000a",
        concept="shared.concept",
        entity={"name": "person", "role": "civilian_labor_force"},
        first_observed_period="2029-11",
    )
    lineage_b = _catalog_row(
        uuid="00000000-0000-4000-8000-00000000000b",
        concept="shared.concept",
        entity={"name": "economy", "role": "aggregate"},
    )
    docket_path = _docket_file(
        tmp_path,
        [
            {
                "series": "shared.concept",
                "cadence": "monthly",
                "slug": "shared-{month}",
                "ledger": {
                    "uuid": "00000000-0000-4000-8000-00000000000a",
                    "concept": "shared.concept",
                },
            }
        ],
    )
    _assert_containment(
        _catalog_shell([lineage_a, lineage_b]),
        "test catalog",
        docket_path=docket_path,
    )
    with pytest.raises(AssertionError, match="duplicate uuid"):
        _assert_containment(
            _catalog_shell([lineage_a, dict(lineage_a)]),
            "test catalog",
            docket_path=docket_path,
        )


def test_containment_units_agree_modulo_declared_transform(
    tmp_path: pathlib.Path,
) -> None:
    # The six bls.cps.employed_people_by_occupation docket entries target
    # millions while the ledger records thousands with valueScale 0.001.
    row = _catalog_row(
        uuid="00000000-0000-4000-8000-00000000000c",
        concept="occupation.series",
        unit="thousands",
    )

    def entry(extras: dict[str, Any]) -> dict[str, Any]:
        return {
            "series": "occupation.series",
            "cadence": "monthly",
            "slug": "occupation-{month}",
            "extras": extras,
            "ledger": {
                "uuid": "00000000-0000-4000-8000-00000000000c",
                "concept": "occupation.series",
            },
        }

    good = _docket_file(
        tmp_path, [entry({"targetUnit": "millions", "valueScale": 0.001})]
    )
    _assert_containment(_catalog_shell([row]), "test catalog", docket_path=good)

    for bad_extras in (
        {"targetUnit": "millions"},  # transform not declared
        {"targetUnit": "millions", "valueScale": 0.01},  # wrong transform
        {"targetUnit": "percent", "valueScale": 0.001},  # not a magnitude
    ):
        bad = _docket_file(tmp_path, [entry(bad_extras)])
        with pytest.raises(AssertionError, match="unit mismatches"):
            _assert_containment(
                _catalog_shell([row]), "test catalog", docket_path=bad
            )


def test_containment_rejects_stale_uuid(tmp_path: pathlib.Path) -> None:
    docket_path = _docket_file(
        tmp_path,
        [
            {
                "series": "unrelated.series",
                "cadence": "monthly",
                "slug": "unrelated-{month}",
                "ledger": {
                    "uuid": "99999999-9999-4999-8999-999999999999",
                    "concept": "unrelated.series",
                },
            }
        ],
    )
    with pytest.raises(AssertionError, match="no row with uuid"):
        _assert_containment(
            _catalog_shell([_catalog_row()]),
            "test catalog",
            docket_path=docket_path,
        )


def test_docket_is_contained_in_pinned_catalog() -> None:
    pin = _load(PIN_PATH, "committed ledger pin")
    catalog_pin_keys = {"catalogSha256", "catalogBytes"} & set(pin)
    if not catalog_pin_keys:
        pytest.skip(
            "PINNED CATALOG NOT YET AVAILABLE: committed ledger pin "
            f"{pin.get('sha')} predates the catalog-bearing SHA; the trusted "
            "pin workflow must advance it with --require-catalog"
        )
    assert catalog_pin_keys == {"catalogSha256", "catalogBytes"}, (
        "committed pin must carry catalogSha256 and catalogBytes together"
    )
    catalog_sha256 = pin.get("catalogSha256")
    catalog_bytes = pin.get("catalogBytes")
    assert type(catalog_sha256) is str and re.fullmatch(
        r"[0-9a-f]{64}", catalog_sha256
    ), "pin catalogSha256 must be a SHA-256 digest"
    assert type(catalog_bytes) is int and catalog_bytes >= 0, (
        "pin catalogBytes must be a non-negative integer"
    )
    url = f"https://raw.githubusercontent.com/{pin['repo']}/{pin['sha']}/{CATALOG_PATH}"
    request = urllib.request.Request(
        url, headers={"User-Agent": "thesis-containment-test"}
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        raw = response.read()
    assert len(raw) == catalog_bytes, (
        f"pinned catalog byte count mismatch: expected {catalog_bytes}, got {len(raw)}"
    )
    assert hashlib.sha256(raw).hexdigest() == catalog_sha256, (
        "pinned catalog SHA-256 does not match ledger-pin.json"
    )
    _assert_containment(_object(raw, "pinned catalog"), "pinned catalog")
