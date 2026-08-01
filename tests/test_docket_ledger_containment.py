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
CATALOG_TOP_LEVEL_KEYS = {
    "generator_version",
    "observations_sha256",
    "observation_rows",
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
    "rid_patterns",
    "first_observed_period",
    "last_observed_period",
    "observation_count",
}


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
    assert type(catalog["observations_sha256"]) is str and re.fullmatch(
        r"[0-9a-f]{64}", catalog["observations_sha256"]
    ), f"{label}.observations_sha256 must be a SHA-256 digest"
    assert (
        type(catalog["observation_rows"]) is int
        and catalog["observation_rows"] >= 0
    ), f"{label}.observation_rows must be a non-negative integer"
    docket_rows = docket.get("series")
    catalog_rows = catalog.get("series")
    assert type(docket_rows) is list, "docket.series must be a list"
    assert type(catalog_rows) is list, f"{label}.series must be a list"

    malformed_catalog_rows: list[str] = []
    by_concept: dict[str, dict[str, Any]] = {}
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
        if concept in by_concept:
            malformed_catalog_rows.append(f"duplicate concept {concept}")
            continue
        by_concept[concept] = row
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
        catalog_row = by_concept.get(ledger["concept"])
        if catalog_row is None:
            mismatched_refs.append(
                f"{series}: catalog has no concept {ledger['concept']!r}"
            )
            continue
        if catalog_row["uuid"] != ledger["uuid"]:
            mismatched_refs.append(
                f"{series}: docket uuid {ledger['uuid']} != "
                f"catalog uuid {catalog_row['uuid']} for {ledger['concept']}"
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
        catalog_unit = catalog_row["unit"]
        if target_unit is not None and catalog_unit is not None:
            if target_unit != catalog_unit:
                unit_mismatches.append(
                    f"{series}: docket targetUnit={target_unit!r}, "
                    f"catalog unit={catalog_unit!r}"
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


def test_docket_is_contained_in_frozen_catalog_fixture() -> None:
    _assert_containment(_load(FIXTURE_PATH, "frozen catalog fixture"), "fixture")


def test_containment_rejects_unrelated_catalog_reference(
    tmp_path: pathlib.Path,
) -> None:
    docket_path = tmp_path / "docket.json"
    docket_path.write_text(
        json.dumps(
            {
                "series": [
                    {
                        "series": "docket.series",
                        "cadence": "monthly",
                        "slug": "docket-series-{month}-{year}",
                        "ledger": {
                            "uuid": "00000000-0000-4000-8000-000000000001",
                            "concept": "unrelated.series",
                        },
                    }
                ]
            },
            indent=2,
        )
        + "\n"
    )
    catalog = {
        "generator_version": 1,
        "observations_sha256": "0" * 64,
        "observation_rows": 1,
        "series": [
            {
                "uuid": "00000000-0000-4000-8000-000000000001",
                "concept": "unrelated.series",
                "family_patterns": ["unrelated.series.{P}"],
                "status": "observed",
                "unit": None,
                "cadence": "month",
                "geography": {"id": "US", "level": "country", "name": "US"},
                "entity": {"name": "economy", "role": "aggregate"},
                "sources": ["test"],
                "aliases": [],
                "rid_patterns": ["unrelated.series.{P}.first_print"],
                "first_observed_period": "2029-12",
                "last_observed_period": "2029-12",
                "observation_count": 1,
            }
        ]
    }

    with pytest.raises(AssertionError, match="neither canonical concept nor alias"):
        _assert_containment(catalog, "test catalog", docket_path=docket_path)


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
