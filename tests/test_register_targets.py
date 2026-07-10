from __future__ import annotations

import datetime as dt
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_ledger_targets  # noqa: E402
import register_targets  # noqa: E402
from canonical_json import canonical_bytes, canonical_sha256  # noqa: E402


def sample_target() -> dict:
    return {
        "series": "agency.test.rate",
        "period": "2030-01",
        "catalogSlug": "agency-test-rate-january-2030",
        "targetUnit": "percent",
        "valueScale": 1,
        "previousTarget": {
            "period": "2029-12",
            "dataPointId": "agency.test.rate.2029_12.first_print",
            "country": "US",
            "unit": "percent",
            "resolutionDate": "2030-01-15",
            "resolutionSource": "Agency table A",
            "resolutionSourceUrl": "https://data.example.gov/table-a",
        },
    }


def test_registration_snapshot_round_trip_and_hash_stability(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    generated = tmp_path / "ledger-targets.generated.ts"
    generated.write_text(
        'import type { TargetRegisteredLedgerEntry } from "./ledger-targets";\n'
        "export const GENERATED_FORECAST_TARGETS = [\n"
        "] satisfies TargetRegisteredLedgerEntry[];\n"
    )
    monkeypatch.setattr(register_targets, "ROOT", tmp_path)
    monkeypatch.setattr(register_targets, "GENERATED_TARGETS", generated)

    registration_date = dt.date(2030, 1, 10)
    target = sample_target()
    reordered = dict(reversed(list(target.items())))
    assert canonical_sha256(
        register_targets.build_snapshot([target], registration_date)
    ) == canonical_sha256(
        register_targets.build_snapshot([reordered], registration_date)
    )

    targets_path = tmp_path / "targets.json"
    targets_path.write_text(json.dumps({"targets": [target]}))
    snapshot_path, content_hash, snapshot = register_targets.register(
        targets_path, registration_date
    )

    assert snapshot_path.name == f"2030-01-10-{content_hash}.json"
    assert snapshot_path.read_bytes() == canonical_bytes(snapshot) + b"\n"
    assert canonical_sha256(json.loads(snapshot_path.read_text())) == content_hash
    round_trip = json.loads(targets_path.read_text())["targets"][0]
    contract = snapshot["targets"][0]
    assert contract["dataPointId"] == "agency.test.rate.2030_01.first_print"
    assert round_trip["dataPointId"] == contract["dataPointId"]
    assert round_trip["sourceBinding"] == contract["sourceBinding"]
    assert round_trip["targetContentHash"] == content_hash
    assert round_trip["targetRegistrationPath"].startswith("records/targets/")
    generated_text = generated.read_text()
    assert 'registrationState: "preregistered"' in generated_text
    assert f'targetContentHash: "{content_hash}"' in generated_text
    preregistration = generate_ledger_targets.preregistration_for(
        generated_text, contract["dataPointId"]
    )
    assert preregistration is not None
    _, registration = preregistration
    cell = {
        "dataPointId": contract["dataPointId"],
        "unit": "percent",
        "resolutionSourceUrl": "https://data.example.gov/releases/january",
        "country": "US",
        "resolutionDate": "2030-02-15",
        "resolutionSource": "Agency table A",
        "resolutionRule": "First published January 2030 value.",
        "title": "Agency test rate",
    }
    generate_ledger_targets.validate_preregistered_contract(cell, registration)
    assert (
        generate_ledger_targets.entry_for(cell, registration)["registrationState"]
        == "published"
    )


def test_claims_binding_is_data_driven_and_advance_vintage() -> None:
    contract = register_targets.build_contract(
        {
            "series": "us.dol.initial_claims.sa",
            "period": "week_2030-01-05",
            "catalogSlug": "initial-claims-week-2030-01-05",
            "targetUnit": "thousands",
            "valueScale": 0.001,
        },
        dt.date(2030, 1, 6),
    )

    assert contract["dataPointId"] == "us.dol.initial_claims.sa.week_2030-01-05"
    assert contract["sourceBinding"] == {
        "adapter": "alfred-fred",
        "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA",
        "sourceSeriesId": "ICSA",
        "field": "ICSA",
        "table": "ALFRED graph CSV",
        "transform": {"operation": "multiply", "factor": 0.001},
        "releasePolicy": "advance_vintage",
        "expectedReleaseWindow": {"start": "2030-01-08", "end": "2030-01-12"},
    }
