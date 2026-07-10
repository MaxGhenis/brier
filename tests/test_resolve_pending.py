from __future__ import annotations

import gzip
import pathlib
import sys
from types import SimpleNamespace

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import resolve_pending  # noqa: E402
from canonical_json import canonical_bytes, canonical_sha256  # noqa: E402
from verify_custody import verify_run  # noqa: E402


def test_archives_raw_response_and_attaches_append_provenance(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    monkeypatch.setattr(resolve_pending, "ROOT", tmp_path)
    data_point_id = "us.dol.initial_claims.sa.week_2030-01-05"
    snapshot = {
        "schemaVersion": "thesis_target_registration_v1",
        "targets": [{"dataPointId": data_point_id}],
    }
    content_hash = canonical_sha256(snapshot)
    records = tmp_path / "records" / "targets"
    records.mkdir(parents=True)
    (records / f"2030-01-01-{content_hash}.json").write_bytes(
        canonical_bytes(snapshot) + b"\n"
    )
    target_hashes = resolve_pending.registration_hashes(records)
    raw = b"observation_date,ICSA_20300110\n2030-01-05,245000\n"
    run_dir = tmp_path / "records" / "resolutions" / "2030-01-10" / "run"
    run_dir.mkdir(parents=True)
    row = {"source_record_id": data_point_id, "value": 245.0}

    enriched = resolve_pending.attach_resolution_provenance(
        row,
        run_dir=run_dir,
        series_id="ICSA",
        vintage="2030-01-10",
        raw=raw,
        retrieved_at="2030-01-10T13:40:00Z",
        ledger_repo_sha="a" * 40,
        target_hashes=target_hashes,
    )

    archive = enriched["responseArchive"]
    assert enriched["targetContentHash"] == content_hash
    assert enriched["ledgerRepoSha"] == "a" * 40
    assert enriched["sourceVintage"] == "2030-01-10"
    assert enriched["retrievedAt"] == "2030-01-10T13:40:00Z"
    assert archive["contentEncoding"] == "gzip"
    assert gzip.decompress((tmp_path / archive["path"]).read_bytes()) == raw
    assert len(archive["sha256"]) == 64
    assert len(archive["gzipSha256"]) == 64

    manifest = resolve_pending.finalize_resolution_manifest(
        run_dir,
        {
            "schemaVersion": "thesis_resolution_run_v1",
            "retrievedAt": enriched["retrievedAt"],
            "ledgerRepo": "PolicyEngine/ledger",
            "ledgerBranch": "facts",
            "ledgerRepoSha": enriched["ledgerRepoSha"],
            "facts": [
                {
                    "dataPointId": data_point_id,
                    "sourceVintage": enriched["sourceVintage"],
                    "retrievedAt": enriched["retrievedAt"],
                    "targetContentHash": enriched["targetContentHash"],
                    "responseArchive": archive,
                }
            ],
        },
    )
    result = verify_run(run_dir)
    assert manifest["custodyInventoryVersion"] == 2
    assert result.run_mode == "resolver"
    assert result.inventory_status == "complete"
    assert result.headline_eligible is False


def test_pending_claims_uses_recorded_release_date_not_a_fixed_offset() -> None:
    data_point_id = "us.dol.initial_claims.sa.week_2030-07-01"
    log = {
        "entries": [
            {
                "kind": "prediction_recorded",
                "forecastSlug": "initial-claims-week-2030-07-01",
                # Holiday-shift fixture: deliberately not week-ending + 5.
                "resolutionDate": "2030-07-05",
            }
        ],
        "resolutionLinks": [
            {
                "forecastSlug": "initial-claims-week-2030-07-01",
                "targetFactRef": data_point_id,
                "status": "pending",
            }
        ],
    }

    assert resolve_pending.pending_claims_refs(log) == [
        (data_point_id, "2030-07-01", "initial", "2030-07-05")
    ]


def test_ledger_state_pins_content_fetch_to_the_recorded_repo_sha(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_run(command, **_kwargs):
        calls.append(command)
        if "/commits/" in command[2]:
            return SimpleNamespace(stdout="a" * 40 + "\n")
        return SimpleNamespace(stdout='{"sha":"blob-sha","content":"e30K"}')

    monkeypatch.setattr(resolve_pending.subprocess, "run", fake_run)

    content, blob_sha, repo_sha = resolve_pending.ledger_state(
        "PolicyEngine/ledger", "facts", "ledger/facts.jsonl"
    )

    assert content == "{}\n"
    assert blob_sha == "blob-sha"
    assert repo_sha == "a" * 40
    assert calls[1][2].endswith(f"?ref={'a' * 40}")


def test_parse_ref_period_handles_all_dialects() -> None:
    cases = [
        ("bls.cps.unemployment_rate.june_2026.first_print",
         "bls.cps.unemployment_rate", ("month", "2026-06")),
        ("us.bea.core_pce.mom_sa.2026-05", "us.bea.core_pce.mom_sa",
         ("month", "2026-05")),
        ("bea.real_gdp.saar.q1_2026.third_estimate", "bea.real_gdp.saar",
         ("quarter", "2026-01")),
        ("bea.real_gdp.saar.2026_q3.advance_estimate", "bea.real_gdp.saar",
         ("quarter", "2026-07")),
    ]
    for ref, stem, expected in cases:
        assert resolve_pending.parse_ref_period(ref, stem) == expected
    assert resolve_pending.parse_ref_period(
        "bls.cps.unemployment_rate.sometime", "bls.cps.unemployment_rate"
    ) is None


def test_apply_transform_level_diff_and_pct() -> None:
    rows = {"2026-05-01": 100.0, "2026-06-01": 102.0}
    assert resolve_pending.apply_transform(
        rows, {"transform": "level"}, "month", "2026-06"
    ) == 102.0
    assert resolve_pending.apply_transform(
        rows, {"transform": "mom_diff"}, "month", "2026-06"
    ) == 2.0
    assert resolve_pending.apply_transform(
        rows, {"transform": "pct_change_1d"}, "month", "2026-06"
    ) == 2.0
    assert resolve_pending.apply_transform(
        rows, {"transform": "level", "scale": 0.001, "round": 3},
        "month", "2026-06",
    ) == 0.102
    # Missing prior period fails closed rather than fabricating a change.
    assert resolve_pending.apply_transform(
        {"2026-06-01": 102.0}, {"transform": "mom_diff"}, "month", "2026-06"
    ) is None


def test_value_plausibility_gate_blocks_scale_blunders() -> None:
    forecast = {"interval80": {"lower": 7.0, "upper": 8.0}}
    assert resolve_pending.value_plausible(7.5, forecast)
    assert resolve_pending.value_plausible(10.0, forecast)  # surprise, fine
    # thousands-vs-millions class: 1000x outside the interval is refused
    assert not resolve_pending.value_plausible(7594.0, forecast)
    assert resolve_pending.value_plausible(7594.0, {})  # no interval, no gate


def test_a19_parse_reads_current_month_column() -> None:
    html = (
        "<table><tr><td>Healthcare support occupations</td>"
        "<td>5,950</td><td>5,691</td></tr>"
        "<tr><td>Production occupations</td><td>7,938</td><td>7,759</td></tr>"
        "</table>"
    )
    values = resolve_pending.a19_values_from_html(html)
    assert values["healthcare_support"] == 5691.0
    assert values["production"] == 7759.0


def test_pending_adapter_refs_maps_and_gates_units() -> None:
    log = {
        "entries": [
            {"kind": "prediction_recorded", "forecastSlug": "a",
             "resolutionDate": "2026-07-02", "unit": "thousands",
             "interval80": {"lower": 35, "upper": 245}},
            {"kind": "prediction_recorded", "forecastSlug": "b",
             "resolutionDate": "2026-07-02", "unit": "percent",
             "interval80": {"lower": 4.1, "upper": 4.5}},
        ],
        "resolutionLinks": [
            {"status": "pending", "forecastSlug": "a",
             "targetFactRef":
                 "bls.ces.total_nonfarm_payroll_change.june_2026.first_print"},
            {"status": "pending", "forecastSlug": "b",
             "targetFactRef":
                 "bls.cps.employed_people_by_occupation.healthcare_support"
                 ".june_2026.first_print"},
            {"status": "pending", "forecastSlug": "b",
             "targetFactRef": "statcan.cpi.allitems.yoy.2026-05"},
        ],
    }
    todo = resolve_pending.pending_adapter_refs(log)
    refs = {item[0]: item for item in todo}
    assert (
        "bls.ces.total_nonfarm_payroll_change.june_2026.first_print" in refs
    )
    a19 = refs[
        "bls.cps.employed_people_by_occupation.healthcare_support"
        ".june_2026.first_print"
    ]
    assert a19[1] == "a19" and a19[4] == "2026-06"
    # No adapter claims the international series yet.
    assert "statcan.cpi.allitems.yoy.2026-05" not in refs
