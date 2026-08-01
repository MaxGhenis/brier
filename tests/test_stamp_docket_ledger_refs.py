from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stamp_docket_ledger_refs import StampError, stamp_docket  # noqa: E402


def _catalog() -> dict:
    return {
        "series": [
            {
                "uuid": "direct-uuid",
                "concept": "direct.series",
                "aliases": [],
            },
            {
                "uuid": "legacy-uuid",
                "concept": "legacy.series",
                "aliases": ["direct.series", "alias.series"],
            },
        ]
    }


def test_canonical_concept_precedes_alias_and_alias_match_records_concept() -> None:
    docket = {
        "comment": "fixture",
        "series": [
            {"series": "direct.series", "cadence": "monthly", "slug": "a"},
            {"series": "alias.series", "cadence": "monthly", "slug": "b"},
        ],
    }

    stamped, notes = stamp_docket(_catalog(), docket)

    assert stamped["series"][0]["ledger"] == {
        "uuid": "direct-uuid",
        "concept": "direct.series",
    }
    assert stamped["series"][1]["ledger"] == {
        "uuid": "legacy-uuid",
        "concept": "legacy.series",
    }
    assert notes == ["alias match: alias.series -> legacy.series"]
    assert list(stamped["series"][0]) == ["series", "cadence", "slug", "ledger"]


def _row(uuid: str, concept: str, **overrides) -> dict:
    row = {
        "uuid": uuid,
        "concept": concept,
        "aliases": [],
        "status": "observed",
        "unit": "percent",
        "cadence": "month",
        "geography": {"level": "country", "id": "0100000US",
                      "vintage": "current"},
        "entity": {"name": "economy", "role": "aggregate"},
        "source_concepts": [],
        "first_observed_period": "2026-06",
    }
    row.update(overrides)
    return row


def test_duplicate_concepts_resolve_by_earliest_national_lineage() -> None:
    # Catalog v3 keeps entity-drift lineages of one series as separate rows;
    # the docket pins the earliest lineage (append-invariant, and the
    # survivor a future ledger merge would keep).
    catalog = {
        "series": [
            _row("uuid-june", "bls.cps.unemployment_rate"),
            _row(
                "uuid-may",
                "bls.cps.unemployment_rate",
                entity={"name": "person", "role": "civilian_labor_force"},
                first_observed_period="2026-05",
            ),
            _row(
                "uuid-state",
                "bls.cps.unemployment_rate",
                geography={"level": "state", "id": "0400000US06",
                           "vintage": "current"},
                first_observed_period="2026-01",
            ),
        ]
    }
    docket = {
        "series": [
            {"series": "bls.cps.unemployment_rate", "cadence": "monthly",
             "slug": "u3"}
        ]
    }

    stamped, notes = stamp_docket(catalog, docket)

    # The state row is earliest overall but not national; the May national
    # lineage wins.
    assert stamped["series"][0]["ledger"]["uuid"] == "uuid-may"
    assert notes and "lineage pick" in notes[0]


def test_duplicate_concepts_disambiguate_by_cadence_and_unit() -> None:
    catalog = {
        "series": [
            _row("uuid-weekly", "us.dol.initial_claims.sa",
                 cadence="week_ending", unit="thousands"),
            _row("uuid-monthly", "us.dol.initial_claims.sa",
                 unit="thousands"),
        ]
    }
    docket = {
        "series": [
            {
                "series": "us.dol.initial_claims.sa",
                "cadence": "weekly",
                "slug": "claims",
                "extras": {"targetUnit": "thousands", "valueScale": 0.001},
            }
        ]
    }

    stamped, notes = stamp_docket(catalog, docket)

    assert stamped["series"][0]["ledger"]["uuid"] == "uuid-weekly"
    assert notes == []  # unique after filters: no lineage judgment involved

    scaled = {
        "series": [
            _row("uuid-thousands", "occ.series", unit="thousands"),
            _row("uuid-percent", "occ.series", unit="percent"),
        ]
    }
    docket = {
        "series": [
            {
                "series": "occ.series",
                "cadence": "monthly",
                "slug": "occ",
                "extras": {"targetUnit": "millions", "valueScale": 0.001},
            }
        ]
    }
    stamped, _ = stamp_docket(scaled, docket)
    assert stamped["series"][0]["ledger"]["uuid"] == "uuid-thousands"


def test_lineage_tie_is_a_hard_error() -> None:
    catalog = {
        "series": [
            _row("uuid-a", "tied.series"),
            _row(
                "uuid-b",
                "tied.series",
                entity={"name": "person", "role": "other"},
            ),
        ]
    }
    docket = {
        "series": [{"series": "tied.series", "cadence": "monthly", "slug": "t"}]
    }

    with pytest.raises(StampError, match="earliest-lineage tie"):
        stamp_docket(catalog, docket)


def test_duplicate_catalog_uuid_is_invalid() -> None:
    catalog = {
        "series": [
            _row("same-uuid", "one.series"),
            _row("same-uuid", "two.series"),
        ]
    }
    docket = {
        "series": [{"series": "one.series", "cadence": "monthly", "slug": "o"}]
    }

    with pytest.raises(StampError, match="duplicate catalog uuid"):
        stamp_docket(catalog, docket)


def test_missing_docket_series_are_listed_together() -> None:
    docket = {
        "series": [
            {"series": "missing.b", "cadence": "monthly", "slug": "b"},
            {"series": "missing.a", "cadence": "monthly", "slug": "a"},
        ]
    }

    with pytest.raises(StampError) as exc_info:
        stamp_docket(_catalog(), docket)

    assert "missing.a" in str(exc_info.value)
    assert "missing.b" in str(exc_info.value)


def test_cli_is_idempotent_and_writes_indent_two_with_trailing_newline(
    tmp_path: pathlib.Path,
) -> None:
    catalog_path = tmp_path / "catalog.json"
    docket_path = tmp_path / "docket.json"
    catalog_path.write_text(json.dumps(_catalog(), indent=2) + "\n")
    docket_path.write_text(
        json.dumps(
            {
                "series": [
                    {
                        "series": "alias.series",
                        "cadence": "monthly",
                        "slug": "alias",
                    }
                ]
            },
            indent=2,
        )
        + "\n"
    )
    command = [
        sys.executable,
        str(ROOT / "scripts" / "stamp_docket_ledger_refs.py"),
        "--catalog",
        str(catalog_path),
        "--docket",
        str(docket_path),
    ]

    first = subprocess.run(command, check=True, capture_output=True, text=True)
    first_bytes = docket_path.read_bytes()
    second = subprocess.run(command, check=True, capture_output=True, text=True)

    assert "updated" in first.stdout
    assert "alias match: alias.series -> legacy.series" in first.stdout
    assert "unchanged" in second.stdout
    assert docket_path.read_bytes() == first_bytes
    assert first_bytes.endswith(b"\n")
    assert b'  "series": [' in first_bytes


def test_source_binding_overrides_earliest_lineage() -> None:
    # The docket's own feed binding is authoritative about which lineage
    # it observes; earliest-lineage is only the fallback.
    catalog = {
        "series": [
            _row("uuid-indpro",
                 "fed.g17.industrial_production.total_index_mom",
                 source_concepts=["INDPRO"]),
            _row(
                "uuid-early",
                "fed.g17.industrial_production.total_index_mom",
                entity={"name": "institutional_sector",
                        "role": "total_industrial_production"},
                first_observed_period="2026-05",
                source_concepts=["fed.g17.industrial_production"],
            ),
        ]
    }
    docket = {
        "series": [
            {
                "series": "fed.g17.industrial_production.total_index_mom",
                "cadence": "monthly",
                "slug": "ip",
                "extras": {
                    "targetUnit": "percent",
                    "sourceBinding": {"sourceSeriesId": "INDPRO"},
                },
            }
        ]
    }

    stamped, notes = stamp_docket(catalog, docket)

    assert stamped["series"][0]["ledger"]["uuid"] == "uuid-indpro"
    assert notes and "source binding pick" in notes[0]
