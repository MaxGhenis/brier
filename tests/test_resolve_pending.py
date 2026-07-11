from __future__ import annotations

import base64
import datetime as dt
import gzip
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
from types import SimpleNamespace

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ledger_release_chain  # noqa: E402
import resolve_pending  # noqa: E402
from canonical_json import canonical_bytes, canonical_sha256  # noqa: E402
from verify_custody import verify_run  # noqa: E402


def test_archives_raw_response_and_attaches_append_provenance(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    monkeypatch.setattr(resolve_pending, "ROOT", tmp_path)
    data_point_id = "us.dol.initial_claims.sa.week_2030-01-05"
    contract = {
        "dataPointId": data_point_id,
        "series": "us.dol.initial_claims.sa",
        "period": "2030-01-05",
        "unit": "thousands",
        "sourceBinding": {
            "releasePolicy": "advance_vintage",
            "table": "ALFRED graph CSV",
            "field": "ICSA",
            "transform": {"operation": "multiply", "factor": 0.001},
        },
    }
    snapshot = {
        "schemaVersion": "thesis_target_registration_v1",
        "targets": [contract],
    }
    content_hash = canonical_sha256(snapshot)
    records = tmp_path / "records" / "targets"
    records.mkdir(parents=True)
    (records / f"2030-01-01-{content_hash}.json").write_bytes(
        canonical_bytes(snapshot) + b"\n"
    )
    target_contracts = resolve_pending.registration_contracts(records)
    raw = b"observation_date,ICSA_20300110\n2030-01-05,245000\n"
    run_dir = tmp_path / "records" / "resolutions" / "2030-01-10" / "run"
    run_dir.mkdir(parents=True)
    row = {
        "source_record_id": data_point_id,
        "value": 245.0,
        "observed_at": "2030-01-10",
        "measure": {"concept": "us.dol.initial_claims.sa", "unit": "thousands"},
        "source": {"source_name": "dol_eta", "vintage": "advance"},
    }

    enriched = resolve_pending.attach_resolution_provenance(
        row,
        run_dir=run_dir,
        series_id="ICSA",
        vintage="2030-01-10",
        raw=raw,
        retrieved_at="2030-01-10T13:40:00Z",
        ledger_repo_sha="a" * 40,
        target_contracts=target_contracts,
    )

    archive = enriched["responseArchive"]
    assert enriched["targetContentHash"] == content_hash
    projection = enriched["sourceBindingProjection"]
    assert projection["unit"] == "thousands"
    assert projection["field"] == "ICSA"
    assert projection["responseSha256"] == archive["sha256"]
    assert enriched["assertionVersion"]["id"].startswith("av2:")
    assert enriched["assertionVersion"]["supersedes"] is None
    # The assertion version binds the archived response digest, so it must be
    # computed over the enriched row (with responseArchive), not the bare row.
    assert (
        enriched["assertionVersion"]["id"]
        == resolve_pending.assertion_version(enriched)["id"]
    )
    assert (
        enriched["assertionVersion"]["id"]
        != resolve_pending.assertion_version(row)["id"]
    )
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


def test_main_removes_signing_secret_before_any_resolver_work(
    monkeypatch, capsys
) -> None:
    signing_key = "generated-test-signing-key"
    monkeypatch.setenv(resolve_pending.PRODUCER_SIGNING_KEY_ENV, signing_key)

    def load_log(_url: str) -> dict:
        assert resolve_pending.PRODUCER_SIGNING_KEY_ENV not in os.environ
        return {"entries": [], "resolutionLinks": []}

    monkeypatch.setattr(resolve_pending, "load_thesis_log", load_log)
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py"])

    assert resolve_pending.main() == 0
    assert capsys.readouterr().out == "no pending adapter-covered cells\n"
    assert resolve_pending.PRODUCER_SIGNING_KEY_ENV not in os.environ


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
    # International series route to the native-source adapters.
    intl = refs["statcan.cpi.allitems.yoy.2026-05"]
    assert intl[1] == "intl" and intl[4] == "2026-05"


def test_manifest_dedupes_shared_response_archives(tmp_path) -> None:
    original_root = resolve_pending.ROOT
    resolve_pending.ROOT = tmp_path
    try:
        run_dir = tmp_path / "records" / "resolutions" / "run"
        raw = b"date,value\n2026-05-01,1\n"
        archive = resolve_pending.archive_response(
            run_dir, series_id="PCEPILFE", vintage="2026-06-25", raw=raw
        )
        manifest = {
            "schemaVersion": "thesis_resolution_run_v1",
            "retrievedAt": "2026-07-10T12:00:00Z",
            "ledgerRepo": "PolicyEngine/ledger",
            "ledgerBranch": "test",
            "ledgerRepoSha": "0" * 40,
            "facts": [
                {"dataPointId": "bea.pce.core_mom.may_2026.first_print",
                 "sourceVintage": "2026-06-25", "retrievedAt": "t",
                 "responseArchive": archive},
                {"dataPointId": "us.bea.core_pce.mom_sa.2026-05",
                 "sourceVintage": "2026-06-25", "retrievedAt": "t",
                 "responseArchive": archive},
            ],
        }
        sealed = resolve_pending.finalize_resolution_manifest(run_dir, manifest)
        responses = [
            ref for ref in sealed["artifacts"]
            if ref["artifactType"] == "resolver_response"
        ]
        assert len(responses) == 1
    finally:
        resolve_pending.ROOT = original_root


def test_write_side_rejects_a_fact_whose_unit_contradicts_its_contract() -> None:
    registration = {
        "targetContentHash": "a" * 64,
        "contract": {
            "dataPointId": "test.series.2030",
            "series": "test.series",
            "period": "2030",
            "unit": "thousands",
            "sourceBinding": {
                "releasePolicy": "advance_vintage",
                "table": "ALFRED graph CSV",
                "field": "TEST",
                "transform": {"operation": "multiply", "factor": 0.001},
            },
        },
        "ledgerPin": None,
    }
    row = {
        "source_record_id": "test.series.2030",
        "value": 1.5,
        "measure": {"concept": "test.series", "unit": "millions"},
    }

    try:
        resolve_pending.source_binding_projection(registration, row, b"raw")
    except ValueError as error:
        assert "millions" in str(error) and "thousands" in str(error)
    else:
        raise AssertionError("wrong-unit fact was not rejected at write time")


def test_write_side_rejects_a_fact_from_a_different_concept() -> None:
    # Finding 1: a row carrying the registered source_record_id but a
    # different measure concept (a different publisher/series) must not
    # stamp the registered projection.
    registration = {
        "targetContentHash": "a" * 64,
        "contract": {
            "dataPointId": "test.series.2030",
            "series": "test.series",
            "period": "2030",
            "unit": "thousands",
            "sourceBinding": {
                "releasePolicy": "advance_vintage",
                "table": "ALFRED graph CSV",
                "field": "TEST",
                "transform": {"operation": "multiply", "factor": 0.001},
                "allowedHosts": ["alfred.stlouisfed.org"],
            },
        },
        "ledgerPin": None,
    }
    wrong_concept = {
        "source_record_id": "test.series.2030",
        "value": 999.0,
        "measure": {"concept": "unrelated.other.series", "unit": "thousands"},
        "source": {"url": "https://alfred.stlouisfed.org/x"},
    }
    try:
        resolve_pending.source_binding_projection(registration, wrong_concept, b"x")
    except ValueError as error:
        assert "concept" in str(error)
    else:
        raise AssertionError("wrong-concept fact was not rejected")

    wrong_host = {
        "source_record_id": "test.series.2030",
        "value": 5.0,
        "measure": {"concept": "test.series", "unit": "thousands"},
        "source": {"url": "https://evil.example.com/x"},
    }
    try:
        resolve_pending.source_binding_projection(registration, wrong_host, b"x")
    except ValueError as error:
        assert "host" in str(error)
    else:
        raise AssertionError("novel-host fact was not rejected")


def test_registration_contracts_resolves_duplicates_to_published_hash(
    tmp_path,
) -> None:
    # Finding 9: two registrations for one dataPointId resolve to whichever
    # the published target committed, not lexical file order.
    records = tmp_path / "records" / "targets"
    records.mkdir(parents=True)
    dpid = "test.dup.series.2030"
    for series in ("a.series", "b.series"):
        contract = {
            "dataPointId": dpid,
            "series": series,
            "period": "2030",
            "unit": "count",
            "sourceBinding": {"releasePolicy": "first_print", "table": "t"},
        }
        snap = {"schemaVersion": "thesis_target_registration_v1", "targets": [contract]}
        ch = canonical_sha256(snap)
        (records / f"2030-01-01-{ch}.json").write_bytes(canonical_bytes(snap) + b"\n")
    # Determine the two hashes and publish the lexically-FIRST one.
    hashes = sorted(p.name[11:75] for p in records.glob("*.json"))
    published = hashes[0]
    generated = tmp_path / "generated.ts"
    generated.write_text(
        f'  {{\n    dataPointId: "{dpid}",\n'
        f'    targetContentHash: "{published}",\n  }},\n'
    )
    resolve_pending._PUBLISHED_TARGET_HASHES = None
    try:
        pub = resolve_pending.published_target_hashes(generated)
        resolve_pending._PUBLISHED_TARGET_HASHES = pub
        contracts = resolve_pending.registration_contracts(records)
    finally:
        resolve_pending._PUBLISHED_TARGET_HASHES = None
    assert contracts[dpid]["targetContentHash"] == published


BLS_DOD_PAYLOAD = {
    "status": "REQUEST_SUCCEEDED",
    "responseTime": 88,
    "message": [],
    "Results": {
        "series": [
            {
                "seriesID": "CES9091911001",
                "data": [
                    {
                        "year": "2026",
                        "period": "M05",
                        "periodName": "May",
                        "latest": "true",
                        "value": "476.2",
                        "footnotes": [{"code": "P", "text": "preliminary"}],
                    },
                    {
                        "year": "2026",
                        "period": "M04",
                        "periodName": "April",
                        "value": "476.6",
                        "footnotes": [{}],
                    },
                    {
                        "year": "2026",
                        "period": "M02",
                        "periodName": "February",
                        "value": "478.2",
                        "footnotes": [{}],
                    },
                    # Annual-average rows (M13) must never masquerade as
                    # a month.
                    {
                        "year": "2025",
                        "period": "M13",
                        "periodName": "Annual",
                        "value": "999.9",
                        "footnotes": [{}],
                    },
                    {
                        "year": "2025",
                        "period": "M12",
                        "periodName": "December",
                        "value": "490.1",
                        "footnotes": [{}],
                    },
                    {
                        "year": "2025",
                        "period": "M06",
                        "periodName": "June",
                        "value": "560.0",
                        "footnotes": [{}],
                    },
                ],
            }
        ]
    },
}


def test_bls_rows_parse_latest_and_preliminary_markers() -> None:
    import json as json_module

    raw = json_module.dumps(BLS_DOD_PAYLOAD).encode()
    rows = resolve_pending.bls_rows_from_payload(raw, "CES9091911001")

    assert rows["2026-05"] == {
        "value": 476.2,
        "latest": True,
        "preliminary": True,
    }
    assert rows["2026-04"] == {
        "value": 476.6,
        "latest": False,
        "preliminary": False,
    }
    assert "2025-13" not in rows and len(rows) == 5


def test_bls_rows_fail_closed_on_errors_and_wrong_series() -> None:
    import json as json_module

    raw = json_module.dumps(BLS_DOD_PAYLOAD).encode()
    assert resolve_pending.bls_rows_from_payload(raw, "CES3133640001") == {}
    error = json_module.dumps(
        {"status": "REQUEST_NOT_PROCESSED", "message": ["daily threshold"]}
    ).encode()
    assert resolve_pending.bls_rows_from_payload(error, "CES9091911001") == {}
    assert resolve_pending.bls_rows_from_payload(b"not json", "X") == {}


def test_bls_first_print_defers_absent_and_refuses_revised() -> None:
    rows = {
        "2026-05": {"value": 476.2, "latest": True, "preliminary": True},
        "2026-04": {"value": 476.6, "latest": False, "preliminary": False},
    }
    # June absent: not yet published, defer without refusing.
    assert resolve_pending.bls_first_print(rows, "2026-06") == (None, None)
    # May is the latest preliminary print: capture.
    value, refusal = resolve_pending.bls_first_print(rows, "2026-05")
    assert value == 476.2 and refusal is None
    # April is published but revised: refusing is the only honest option.
    value, refusal = resolve_pending.bls_first_print(rows, "2026-04")
    assert value is None and "first-print window" in refusal


def test_bls_anchor_gate_tolerates_revisions_but_not_wrong_series() -> None:
    anchors = {"2026-02": 478.2, "2026-04": 474.9}
    # CES revised April's first print 474.9 -> 476.6 (+0.36%): tolerated.
    revised = {
        "2026-02": {"value": 478.2, "latest": False, "preliminary": False},
        "2026-04": {"value": 476.6, "latest": False, "preliminary": False},
    }
    assert resolve_pending.bls_anchor_mismatches(revised, anchors) == []
    # A different series' history is far outside publication tolerance.
    wrong_series = {
        "2026-02": {"value": 579.9, "latest": False, "preliminary": False},
        "2026-04": {"value": 585.4, "latest": False, "preliminary": False},
    }
    problems = resolve_pending.bls_anchor_mismatches(wrong_series, anchors)
    assert len(problems) == 2
    # A missing anchor period is a mismatch, never silently skipped.
    assert resolve_pending.bls_anchor_mismatches({}, anchors) != []


def test_pending_adapter_refs_maps_bls_defense_cells() -> None:
    log = {
        "entries": [
            {
                "kind": "prediction_recorded",
                "forecastSlug": "dod",
                "resolutionDate": "2026-07-02",
                "unit": "thousands",
                "interval80": {"lower": 452, "upper": 501},
            },
        ],
        "resolutionLinks": [
            {
                "status": "pending",
                "forecastSlug": "dod",
                "targetFactRef": (
                    "bls.ces.federal_department_of_defense_employment"
                    ".june_2026.first_print"
                ),
            },
        ],
    }

    todo = resolve_pending.pending_adapter_refs(log)

    assert len(todo) == 1
    ref, kind, spec, period_type, period, release_date, forecast = todo[0]
    assert kind == "bls_api"
    assert spec["series_id"] == "CES9091911001"
    # The main loop's unit-mismatch gate compares these two operands.
    assert spec["unit"] == forecast["unit"] == "thousands"
    assert (period_type, period) == ("month", "2026-06")
    assert release_date == "2026-07-02"


def test_bls_json_archive_passes_custody_verification(tmp_path) -> None:
    import json as json_module

    original_root = resolve_pending.ROOT
    resolve_pending.ROOT = tmp_path
    try:
        run_dir = tmp_path / "records" / "resolutions" / "run"
        raw = json_module.dumps(BLS_DOD_PAYLOAD).encode()
        archive = resolve_pending.archive_response(
            run_dir,
            series_id="CES9091911001",
            vintage="2026-08-07",
            raw=raw,
            extension="json",
        )
        assert archive["path"].endswith(".json.gz")
        manifest = resolve_pending.finalize_resolution_manifest(
            run_dir,
            {
                "schemaVersion": "thesis_resolution_run_v1",
                "retrievedAt": "2026-08-07T13:40:00Z",
                "ledgerRepo": "PolicyEngine/ledger",
                "ledgerBranch": "test",
                "ledgerRepoSha": "0" * 40,
                "facts": [
                    {
                        "dataPointId": (
                            "bls.ces.federal_department_of_defense_employment"
                            ".june_2026.first_print"
                        ),
                        "sourceVintage": "2026-08-07",
                        "retrievedAt": "2026-08-07T13:40:00Z",
                        "responseArchive": archive,
                    }
                ],
            },
        )
        result = verify_run(run_dir)
        assert result.inventory_status == "complete"
        assert manifest["ok"] is True
    finally:
        resolve_pending.ROOT = original_root


def test_assertion_version_changes_when_the_value_changes() -> None:
    row = {
        "source_record_id": "test.series.2030",
        "value": 1.5,
        "observed_at": "2030-01-10",
        "period": {"type": "month", "value": "2030-01"},
        "measure": {"concept": "test.series", "unit": "millions"},
        "source": {"source_name": "test", "vintage": "advance"},
    }

    original = resolve_pending.assertion_version(row)
    corrected = resolve_pending.assertion_version({**row, "value": 2.5})

    assert original["id"].startswith("av2:")
    assert original["id"] != corrected["id"]


def _local_timestamp_requester(
    tsa_root: pathlib.Path,
    *,
    signer_overrides: dict[str, str] | None = None,
):
    endpoint_slots = {
        endpoint: slot for slot, endpoint in resolve_pending.TSA_ENDPOINTS.items()
    }
    counter = 0

    def request(endpoint: str, query: bytes, _timeout_seconds: float) -> bytes:
        nonlocal counter
        counter += 1
        slot = endpoint_slots[endpoint]
        signer = (signer_overrides or {}).get(slot, slot)
        query_path = tsa_root / f"request-{counter}.tsq"
        receipt_path = tsa_root / f"response-{counter}.tsr"
        query_path.write_bytes(query)
        subprocess.run(
            [
                "openssl",
                "ts",
                "-reply",
                "-config",
                "openssl-ts.cnf",
                "-queryfile",
                str(query_path),
                "-out",
                str(receipt_path),
            ],
            cwd=tsa_root / signer,
            check=True,
            capture_output=True,
            text=True,
        )
        return receipt_path.read_bytes()

    return request


def _generate_test_producer_keypair(
    root: pathlib.Path,
) -> tuple[pathlib.Path, str]:
    private_key = root / "producer-test-private.pem"
    public_key = root / "anchors" / "producer-ed25519.pub"
    subprocess.run(
        [
            "openssl",
            "genpkey",
            "-algorithm",
            "ED25519",
            "-out",
            str(private_key),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [
            "openssl",
            "pkey",
            "-in",
            str(private_key),
            "-pubout",
            "-out",
            str(public_key),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return private_key, private_key.read_text()


def _sign_test_manifest(
    root: pathlib.Path,
    private_key: pathlib.Path,
    manifest: bytes,
) -> bytes:
    manifest_path = root / "producer-genesis-manifest.json"
    signature_path = root / "producer-genesis.sig"
    manifest_path.write_bytes(manifest)
    subprocess.run(
        [
            "openssl",
            "pkeyutl",
            "-sign",
            "-inkey",
            str(private_key),
            "-rawin",
            "-in",
            str(manifest_path),
            "-out",
            str(signature_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return signature_path.read_bytes()


def _release_fixture_tree(
    tmp_path: pathlib.Path,
) -> tuple[
    resolve_pending.RepositoryTree,
    pathlib.Path,
    resolve_pending.TimestampRequester,
    str,
]:
    tsa_root = tmp_path / "release_tsa"
    shutil.copytree(ROOT / "tests" / "fixtures" / "release_tsa", tsa_root)
    anchor_dir = tsa_root / "anchors"
    producer_private_key, signing_key_pem = _generate_test_producer_keypair(
        tsa_root
    )
    requester = _local_timestamp_requester(tsa_root)
    ledger = b'{"source_record_id":"fixture.base","value":0}\n'
    immutable_prefix = b'{"prefixLineCount":0}\n'
    created_at = (
        dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=2)
    ).isoformat(timespec="seconds").replace("+00:00", "Z")
    manifest = {
        "schemaVersion": "thesis_ledger_release_v1",
        "releaseIndex": 0,
        "previousManifestSha256": None,
        "state": {
            "path": "ledger/official_observations.jsonl",
            "jsonlSha256": hashlib.sha256(ledger).hexdigest(),
            "lineCount": 1,
            "immutablePrefixSha256": hashlib.sha256(immutable_prefix).hexdigest(),
        },
        "append": None,
        "createdAtUtc": created_at,
        "producer": {"repo": "PolicyEngine/ledger", "branch": "fixture"},
    }
    manifest_raw = canonical_bytes(manifest) + b"\n"
    manifest_name = ledger_release_chain.manifest_filename(0, manifest_raw)
    producer_signature = _sign_test_manifest(
        tsa_root,
        producer_private_key,
        manifest_raw,
    )
    query = resolve_pending._build_timestamp_query(manifest_raw, 10)
    receipts = {
        slot: requester(endpoint, query, 10)
        for slot, endpoint in resolve_pending.TSA_ENDPOINTS.items()
    }
    manifest_path = f"releases/manifests/{manifest_name}"
    files = {
        "ledger/official_observations.jsonl": ledger,
        "ledger/immutable_prefix.json": immutable_prefix,
        manifest_path: manifest_raw,
        **{
            f"releases/manifests/{pathlib.PurePosixPath(manifest_name).stem}."
            f"{slot}.tsr": receipt
            for slot, receipt in receipts.items()
        },
        (
            "releases/manifests/"
            f"{pathlib.PurePosixPath(manifest_name).stem}.producer.sig"
        ): producer_signature,
        **{
            f"releases/anchors/{anchor.name}": anchor.read_bytes()
            for anchor in anchor_dir.iterdir()
        },
    }
    return (
        resolve_pending.RepositoryTree(
            tree_sha="1" * 40,
            files=files,
            modes={relative: "100644" for relative in files},
            blob_shas={relative: "a" * 40 for relative in files},
        ),
        anchor_dir,
        requester,
        signing_key_pem,
    )


def _pre_genesis_tree() -> resolve_pending.RepositoryTree:
    path = "ledger/official_observations.jsonl"
    files = {path: b'{"source_record_id":"fixture.base","value":0}\n'}
    return resolve_pending.RepositoryTree(
        tree_sha="1" * 40,
        files=files,
        modes={path: "100644"},
        blob_shas={path: "a" * 40},
    )


def _proposal_api_stub(
    gate_conclusion: str,
    calls: list[tuple[tuple[str, ...], dict | None]],
    *,
    fail_ref_creation: bool = False,
    fail_pr_creation: bool = False,
    recover_pr_number: int | None = None,
    merge_payload: dict | None = None,
):
    merged = False

    def api(*args: str, input_body=None) -> str:
        nonlocal merged
        calls.append((args, input_body))
        joined = " ".join(args)
        if "/git/refs" in joined and "POST" in args:
            if fail_ref_creation:
                raise RuntimeError("simulated ref creation failure")
            return "{}"
        if "/git/ref/heads/" in joined:
            return json.dumps({"object": {"sha": "c" * 40}})
        if "/pulls?state=open" in joined:
            return json.dumps(
                [] if recover_pr_number is None else [{"number": recover_pr_number}]
            )
        if joined.endswith("/pulls") and "POST" in args:
            if fail_pr_creation:
                raise RuntimeError("simulated PR creation failure")
            return json.dumps({"number": 7})
        if "/check-runs" in joined:
            return json.dumps(
                {
                    "check_runs": [
                        {
                            "name": "Append gate",
                            "status": "completed",
                            "conclusion": gate_conclusion,
                        }
                    ]
                }
            )
        if "/merge" in joined:
            result = (
                merge_payload
                if merge_payload is not None
                else {"merged": True, "sha": "d" * 40}
            )
            if type(result) is dict and result.get("merged") is True:
                merged = True
            return json.dumps(result)
        if joined.endswith("/pulls/7") and "PATCH" not in args:
            return json.dumps(
                {
                    "merged": merged,
                    "merge_commit_sha": "d" * 40 if merged else None,
                    "head": {"sha": "c" * 40},
                    "base": {
                        "ref": "codex/thesis-ledger-facts",
                        "sha": "b" * 40,
                    },
                }
            )
        if "PATCH" in args or "DELETE" in args:
            return "{}"
        raise AssertionError(f"unexpected gh call: {joined}")

    return api


def _install_proposal_transport(
    monkeypatch,
    tree: resolve_pending.RepositoryTree,
    calls: list[tuple[tuple[str, ...], dict | None]],
    *,
    gate_conclusion: str = "success",
    fail_ref_creation: bool = False,
    fail_pr_creation: bool = False,
    recover_pr_number: int | None = None,
    merge_payload: dict | None = None,
    published: list[dict[str, bytes]] | None = None,
) -> None:
    monkeypatch.setattr(resolve_pending, "_fetch_repository_tree", lambda *_: tree)

    def publish(*_args, changes, **_kwargs):
        if published is not None:
            published.append(dict(changes))
        return "c" * 40

    monkeypatch.setattr(resolve_pending, "_publish_proposal_commit", publish)
    monkeypatch.setattr(resolve_pending, "_branch_head", lambda *_: "b" * 40)
    monkeypatch.setattr(
        resolve_pending,
        "_verify_remote_proposal_state",
        lambda *_args, **_kwargs: None,
    )
    monkeypatch.setattr(
        resolve_pending,
        "_gh_api",
        _proposal_api_stub(
            gate_conclusion,
            calls,
            fail_ref_creation=fail_ref_creation,
            fail_pr_creation=fail_pr_creation,
            recover_pr_number=recover_pr_number,
            merge_payload=merge_payload,
        ),
    )


def test_append_proposal_builds_byte_correct_verified_release(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    tree, anchor_dir, requester, signing_key_pem = _release_fixture_tree(tmp_path)
    monkeypatch.setenv(resolve_pending.PRODUCER_SIGNING_KEY_ENV, signing_key_pem)
    calls: list[tuple[tuple[str, ...], dict | None]] = []
    published: list[dict[str, bytes]] = []
    _install_proposal_transport(monkeypatch, tree, calls, published=published)
    real_verify = resolve_pending.verify_release_chain
    real_verify_signature = resolve_pending.verify_producer_signature_bytes
    verify_calls: list[dict] = []
    signature_anchor_checks: list[bytes] = []

    def tracking_verify(*args, **kwargs):
        verify_calls.append(dict(kwargs))
        # Test keys intentionally do not match production code pins. Keeping
        # anchor_dir unset in the proposal call exercises the production path:
        # the anchor must come from the staged immutable base tree.
        kwargs["enforce_production_pins"] = False
        return real_verify(*args, **kwargs)

    def tracking_signature_verify(*args, **kwargs):
        selected_anchor = kwargs["anchor_dir"] / "producer-ed25519.pub"
        signature_anchor_checks.append(selected_anchor.read_bytes())
        assert kwargs["anchor_dir"] != anchor_dir
        kwargs["enforce_production_pin"] = False
        return real_verify_signature(*args, **kwargs)

    monkeypatch.setattr(resolve_pending, "verify_release_chain", tracking_verify)
    monkeypatch.setattr(
        resolve_pending,
        "verify_producer_signature_bytes",
        tracking_signature_verify,
    )
    appended = b'{"source_record_id":"test.series.2030","value":1}\n'
    candidate = tree.files["ledger/official_observations.jsonl"] + appended

    release_now = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=2)
    merged = resolve_pending.propose_ledger_append(
        "PolicyEngine/ledger",
        "codex/thesis-ledger-facts",
        "ledger/official_observations.jsonl",
        candidate.decode(),
        "a" * 40,
        "b" * 40,
        1,
        poll_seconds=0,
        poll_attempts=1,
        timestamp_requester=requester,
        release_now=release_now,
    )

    assert merged == "d" * 40
    assert len(published) == 1
    changes = published[0]
    assert changes["ledger/official_observations.jsonl"] == candidate
    release_paths = [path for path in changes if path.startswith("releases/")]
    assert len(release_paths) == 4
    manifest_path = next(path for path in release_paths if path.endswith(".json"))
    producer_signature_path = next(
        path for path in release_paths if path.endswith(".producer.sig")
    )
    assert producer_signature_path == (
        f"releases/manifests/{pathlib.PurePosixPath(manifest_path).stem}.producer.sig"
    )
    assert len(changes[producer_signature_path]) == 64
    manifest_raw = changes[manifest_path]
    manifest = json.loads(manifest_raw)
    assert manifest_raw == canonical_bytes(manifest) + b"\n"
    assert pathlib.PurePosixPath(manifest_path).name == (
        ledger_release_chain.manifest_filename(1, manifest_raw)
    )
    assert manifest["previousManifestSha256"] == hashlib.sha256(
        next(
            payload
            for path, payload in tree.files.items()
            if path.startswith("releases/manifests/") and path.endswith(".json")
        )
    ).hexdigest()
    assert manifest["append"] == {
        "previousLineCount": 1,
        "appendedRowCount": 1,
        "appendedBytesSha256": hashlib.sha256(appended).hexdigest(),
    }
    assert manifest["createdAtUtc"] == release_now.isoformat(
        timespec="seconds"
    ).replace("+00:00", "Z")
    assert manifest["producer"] == {
        "repo": "PolicyEngine/ledger",
        "branch": "codex/thesis-ledger-facts",
    }
    assert manifest["state"] == {
        "path": "ledger/official_observations.jsonl",
        "jsonlSha256": hashlib.sha256(candidate).hexdigest(),
        "lineCount": 2,
        "immutablePrefixSha256": hashlib.sha256(
            tree.files["ledger/immutable_prefix.json"]
        ).hexdigest(),
    }
    assert len(verify_calls) == 2
    assert all(call["require_chain"] is True for call in verify_calls)
    assert all(call["verify_state"] is True for call in verify_calls)
    assert signature_anchor_checks == [
        tree.files["releases/anchors/producer-ed25519.pub"]
    ]
    assert resolve_pending.PRODUCER_SIGNING_KEY_ENV not in os.environ
    assert not any("/contents/" in " ".join(args) for args, _ in calls)
    merge_call = next(
        (args, body) for args, body in calls if "/merge" in " ".join(args)
    )
    assert merge_call[1] == {"merge_method": "rebase", "sha": "c" * 40}


@pytest.mark.parametrize("signing_key", [None, ""])
def test_append_proposal_missing_signing_key_has_no_remote_mutation(
    tmp_path: pathlib.Path,
    monkeypatch,
    signing_key: str | None,
) -> None:
    tree, anchor_dir, _requester, _valid_key = _release_fixture_tree(tmp_path)
    if signing_key is None:
        monkeypatch.delenv(resolve_pending.PRODUCER_SIGNING_KEY_ENV, raising=False)
    else:
        monkeypatch.setenv(resolve_pending.PRODUCER_SIGNING_KEY_ENV, signing_key)
    monkeypatch.setattr(resolve_pending, "_fetch_repository_tree", lambda *_: tree)
    mutations: list[str] = []
    timestamp_calls: list[str] = []
    monkeypatch.setattr(
        resolve_pending,
        "_publish_proposal_commit",
        lambda *_args, **_kwargs: mutations.append("publish"),
    )

    def unexpected_timestamp(endpoint: str, *_args) -> bytes:
        timestamp_calls.append(endpoint)
        return b"unexpected"

    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.no-key","value":1}\n'
    )
    with pytest.raises(
        resolve_pending.LedgerProposalError,
        match=resolve_pending.PRODUCER_SIGNING_KEY_ENV,
    ):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
            timestamp_requester=unexpected_timestamp,
            release_anchor_dir=anchor_dir,
        )

    assert mutations == []
    assert timestamp_calls == []
    assert resolve_pending.PRODUCER_SIGNING_KEY_ENV not in os.environ


def test_append_proposal_signing_failure_erases_key_and_has_no_remote_mutation(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    tree, anchor_dir, _requester, signing_key_pem = _release_fixture_tree(tmp_path)
    monkeypatch.setenv(resolve_pending.PRODUCER_SIGNING_KEY_ENV, signing_key_pem)
    monkeypatch.setattr(resolve_pending, "_fetch_repository_tree", lambda *_: tree)
    mutations: list[str] = []
    timestamp_calls: list[str] = []
    monkeypatch.setattr(
        resolve_pending,
        "_publish_proposal_commit",
        lambda *_args, **_kwargs: mutations.append("publish"),
    )

    real_open = resolve_pending.os.open
    key_open: dict[str, object] = {}

    def tracking_open(path, flags, mode=0o777, *, dir_fd=None):
        if pathlib.Path(path).name == "producer-private.pem":
            key_open.update(path=pathlib.Path(path), flags=flags, mode=mode)
        if dir_fd is None:
            return real_open(path, flags, mode)
        return real_open(path, flags, mode, dir_fd=dir_fd)

    real_run = resolve_pending.subprocess.run

    def failing_sign(command, **kwargs):
        if command[:3] == ["openssl", "pkeyutl", "-sign"]:
            key_path = pathlib.Path(command[command.index("-inkey") + 1])
            assert key_path.read_text() == signing_key_pem
            assert key_path.stat().st_mode & 0o777 == 0o600
            assert resolve_pending.PRODUCER_SIGNING_KEY_ENV not in kwargs["env"]
            assert signing_key_pem not in " ".join(command)
            return SimpleNamespace(
                returncode=23,
                stdout="",
                # A hostile diagnostic must not be propagated, even in part.
                stderr=signing_key_pem[:40],
            )
        return real_run(command, **kwargs)

    monkeypatch.setattr(resolve_pending.os, "open", tracking_open)
    monkeypatch.setattr(resolve_pending.subprocess, "run", failing_sign)

    def unexpected_timestamp(endpoint: str, *_args) -> bytes:
        timestamp_calls.append(endpoint)
        return b"unexpected"

    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.sign-fail","value":1}\n'
    )
    with pytest.raises(
        resolve_pending.LedgerProposalError,
        match="producer signing failed with exit code 23",
    ) as caught:
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
            timestamp_requester=unexpected_timestamp,
            release_anchor_dir=anchor_dir,
        )

    assert signing_key_pem not in str(caught.value)
    assert signing_key_pem[:40] not in str(caught.value)
    assert key_open["flags"] & os.O_EXCL
    assert key_open["mode"] == 0o600
    key_path = key_open["path"]
    assert isinstance(key_path, pathlib.Path)
    assert not key_path.exists()
    assert not key_path.parent.exists()
    assert mutations == []
    assert timestamp_calls == []
    assert resolve_pending.PRODUCER_SIGNING_KEY_ENV not in os.environ


def test_append_proposal_self_verify_failure_precedes_tsa_and_remote_mutation(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    tree, anchor_dir, _requester, _valid_key = _release_fixture_tree(tmp_path)
    wrong_root = tmp_path / "wrong_producer"
    (wrong_root / "anchors").mkdir(parents=True)
    _wrong_key_path, wrong_key_pem = _generate_test_producer_keypair(wrong_root)
    monkeypatch.setenv(resolve_pending.PRODUCER_SIGNING_KEY_ENV, wrong_key_pem)
    monkeypatch.setattr(resolve_pending, "_fetch_repository_tree", lambda *_: tree)
    mutations: list[str] = []
    timestamp_calls: list[str] = []
    monkeypatch.setattr(
        resolve_pending,
        "_publish_proposal_commit",
        lambda *_args, **_kwargs: mutations.append("publish"),
    )

    def unexpected_timestamp(endpoint: str, *_args) -> bytes:
        timestamp_calls.append(endpoint)
        return b"unexpected"

    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.wrong-key","value":1}\n'
    )
    with pytest.raises(
        ledger_release_chain.ReleaseChainError,
        match="producer Ed25519 signature verification failed",
    ):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
            timestamp_requester=unexpected_timestamp,
            release_anchor_dir=anchor_dir,
        )

    assert mutations == []
    assert timestamp_calls == []
    assert resolve_pending.PRODUCER_SIGNING_KEY_ENV not in os.environ


def test_append_proposal_bad_receipt_has_no_remote_mutation(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    tree, anchor_dir, _requester, signing_key_pem = _release_fixture_tree(tmp_path)
    monkeypatch.setenv(resolve_pending.PRODUCER_SIGNING_KEY_ENV, signing_key_pem)
    bad_requester = _local_timestamp_requester(
        anchor_dir.parent,
        signer_overrides={"digicert": "freetsa"},
    )
    monkeypatch.setattr(resolve_pending, "_fetch_repository_tree", lambda *_: tree)
    mutations: list[str] = []
    monkeypatch.setattr(
        resolve_pending,
        "_publish_proposal_commit",
        lambda *_args, **_kwargs: mutations.append("publish"),
    )
    appended = b'{"source_record_id":"test.series.bad","value":1}\n'
    candidate = tree.files["ledger/official_observations.jsonl"] + appended

    with pytest.raises(ledger_release_chain.ReleaseChainError):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
            timestamp_requester=bad_requester,
            release_anchor_dir=anchor_dir,
        )

    assert mutations == []


def test_append_proposal_tsa_failure_has_no_remote_mutation(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    tree, anchor_dir, _requester, signing_key_pem = _release_fixture_tree(tmp_path)
    monkeypatch.setenv(resolve_pending.PRODUCER_SIGNING_KEY_ENV, signing_key_pem)
    monkeypatch.setattr(resolve_pending, "_fetch_repository_tree", lambda *_: tree)
    mutations: list[str] = []
    monkeypatch.setattr(
        resolve_pending,
        "_publish_proposal_commit",
        lambda *_args, **_kwargs: mutations.append("publish"),
    )
    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.tsa","value":1}\n'
    )

    def fail_tsa(*_args):
        raise OSError("TSA unavailable")

    with pytest.raises(resolve_pending.LedgerProposalError, match="timestamp request"):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
            timestamp_requester=fail_tsa,
            release_anchor_dir=anchor_dir,
        )

    assert mutations == []


def test_postmerge_state_is_fully_reverified(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    base_tree, anchor_dir, requester, signing_key_pem = _release_fixture_tree(
        tmp_path
    )
    monkeypatch.setenv(resolve_pending.PRODUCER_SIGNING_KEY_ENV, signing_key_pem)
    path = "ledger/official_observations.jsonl"
    candidate = (
        base_tree.files[path]
        + b'{"source_record_id":"test.series.postmerge","value":1}\n'
    )
    release_files = resolve_pending._prepare_release_files(
        base_tree,
        path=path,
        candidate_ledger=candidate,
        added=1,
        requester=requester,
        timeout_seconds=10,
        clock_skew_seconds=resolve_pending.DEFAULT_CLOCK_SKEW_SECONDS,
        anchor_dir=anchor_dir,
        now=dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=2),
        producer_signing_key=signing_key_pem,
    )
    files = {**base_tree.files, path: candidate, **release_files}
    merged_tree = resolve_pending.RepositoryTree(
        tree_sha="9" * 40,
        files=files,
        modes={relative: "100644" for relative in files},
        blob_shas={relative: "8" * 40 for relative in files},
    )
    monkeypatch.setattr(
        resolve_pending,
        "_fetch_repository_tree",
        lambda *_args: merged_tree,
    )

    resolve_pending._verify_remote_proposal_state(
        "PolicyEngine/ledger",
        "d" * 40,
        path=path,
        candidate_ledger=candidate,
        release_files=release_files,
        clock_skew_seconds=resolve_pending.DEFAULT_CLOCK_SKEW_SECONDS,
        anchor_dir=anchor_dir,
    )

    old_receipt = next(
        relative
        for relative in files
        if relative.endswith(".digicert.tsr") and relative not in release_files
    )
    files[old_receipt] = b"tampered historical receipt"
    with pytest.raises(ledger_release_chain.ReleaseChainError):
        resolve_pending._verify_remote_proposal_state(
            "PolicyEngine/ledger",
            "d" * 40,
            path=path,
            candidate_ledger=candidate,
            release_files=release_files,
            clock_skew_seconds=resolve_pending.DEFAULT_CLOCK_SKEW_SECONDS,
            anchor_dir=anchor_dir,
        )


def test_pre_genesis_append_emits_no_release_files_or_tsa(monkeypatch) -> None:
    tree = _pre_genesis_tree()
    calls: list[tuple[tuple[str, ...], dict | None]] = []
    published: list[dict[str, bytes]] = []
    _install_proposal_transport(monkeypatch, tree, calls, published=published)
    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.legacy","value":1}\n'
    )

    def unexpected_tsa(*_args):
        raise AssertionError("pre-genesis proposal contacted a TSA")

    merged = resolve_pending.propose_ledger_append(
        "PolicyEngine/ledger",
        "codex/thesis-ledger-facts",
        "ledger/official_observations.jsonl",
        candidate.decode(),
        "a" * 40,
        "b" * 40,
        1,
        poll_seconds=0,
        poll_attempts=1,
        timestamp_requester=unexpected_tsa,
    )

    assert merged == "d" * 40
    assert list(published[0]) == ["ledger/official_observations.jsonl"]


def test_append_proposal_refuses_to_merge_and_cleans_gate_failure(
    monkeypatch,
) -> None:
    tree = _pre_genesis_tree()
    calls: list[tuple[tuple[str, ...], dict | None]] = []
    _install_proposal_transport(
        monkeypatch,
        tree,
        calls,
        gate_conclusion="failure",
    )
    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.gate","value":1}\n'
    )

    with pytest.raises(resolve_pending.LedgerProposalError, match="append gate"):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
            poll_seconds=0,
            poll_attempts=1,
        )

    joined = [" ".join(args) for args, _ in calls]
    assert not any("/merge" in call for call in joined)
    assert any("PATCH" in call and "/pulls/7" in call for call in joined)
    assert any("DELETE" in call and "/git/refs/heads/" in call for call in joined)


def test_append_proposal_cleans_pr_and_branch_when_merge_is_refused(
    monkeypatch,
) -> None:
    tree = _pre_genesis_tree()
    calls: list[tuple[tuple[str, ...], dict | None]] = []
    _install_proposal_transport(
        monkeypatch,
        tree,
        calls,
        merge_payload={"merged": False, "message": "base moved"},
    )
    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.merge","value":1}\n'
    )

    with pytest.raises(resolve_pending.LedgerProposalError, match="did not merge"):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
            poll_seconds=0,
            poll_attempts=1,
        )

    joined = [" ".join(args) for args, _ in calls]
    assert any("/merge" in call for call in joined)
    assert any("PATCH" in call and "/pulls/7" in call for call in joined)
    assert any("DELETE" in call and "/git/refs/heads/" in call for call in joined)


def test_append_proposal_refuses_if_base_moves_during_gate_poll(
    monkeypatch,
) -> None:
    tree = _pre_genesis_tree()
    calls: list[tuple[tuple[str, ...], dict | None]] = []
    _install_proposal_transport(monkeypatch, tree, calls)
    heads = iter(["b" * 40, "e" * 40])
    monkeypatch.setattr(resolve_pending, "_branch_head", lambda *_: next(heads))
    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.race","value":1}\n'
    )

    with pytest.raises(
        resolve_pending.LedgerProposalError,
        match="moved while proposal awaited the append gate",
    ):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
            poll_seconds=0,
            poll_attempts=1,
        )

    joined = [" ".join(args) for args, _ in calls]
    assert not any("/merge" in call for call in joined)
    assert any("PATCH" in call and "/pulls/7" in call for call in joined)
    assert any("DELETE" in call and "/git/refs/heads/" in call for call in joined)


def test_append_proposal_recovers_ambiguous_successful_merge(monkeypatch) -> None:
    tree = _pre_genesis_tree()
    calls: list[tuple[tuple[str, ...], dict | None]] = []
    _install_proposal_transport(monkeypatch, tree, calls)
    base_api = resolve_pending._gh_api
    merge_attempted = False

    def ambiguous_api(*args: str, input_body=None) -> str:
        nonlocal merge_attempted
        joined = " ".join(args)
        if "/merge" in joined:
            merge_attempted = True
            raise RuntimeError("merge response lost after server success")
        if (
            merge_attempted
            and joined.endswith("/pulls/7")
            and "PATCH" not in args
        ):
            return json.dumps(
                {
                    "merged": True,
                    "merge_commit_sha": "d" * 40,
                    "head": {"sha": "c" * 40},
                    "base": {"ref": "codex/thesis-ledger-facts"},
                }
            )
        return base_api(*args, input_body=input_body)

    verified: list[str] = []
    monkeypatch.setattr(resolve_pending, "_gh_api", ambiguous_api)
    monkeypatch.setattr(
        resolve_pending,
        "_verify_remote_proposal_state",
        lambda _repo, sha, **_kwargs: verified.append(sha),
    )
    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.ambiguous","value":1}\n'
    )

    merged = resolve_pending.propose_ledger_append(
        "PolicyEngine/ledger",
        "codex/thesis-ledger-facts",
        "ledger/official_observations.jsonl",
        candidate.decode(),
        "a" * 40,
        "b" * 40,
        1,
        poll_seconds=0,
        poll_attempts=1,
    )

    assert merged == "d" * 40
    assert verified == ["d" * 40]


def test_append_proposal_rejects_retarget_after_normal_merge_response(
    monkeypatch,
) -> None:
    tree = _pre_genesis_tree()
    calls: list[tuple[tuple[str, ...], dict | None]] = []
    _install_proposal_transport(monkeypatch, tree, calls)
    base_api = resolve_pending._gh_api
    pr_reads = 0

    def retargeting_api(*args: str, input_body=None) -> str:
        nonlocal pr_reads
        joined = " ".join(args)
        if joined.endswith("/pulls/7") and "PATCH" not in args:
            pr_reads += 1
            if pr_reads >= 2:
                return json.dumps(
                    {
                        "merged": True,
                        "merge_commit_sha": "d" * 40,
                        "head": {"sha": "c" * 40},
                        "base": {"ref": "attacker-retarget", "sha": "b" * 40},
                    }
                )
        return base_api(*args, input_body=input_body)

    verified: list[str] = []
    monkeypatch.setattr(resolve_pending, "_gh_api", retargeting_api)
    monkeypatch.setattr(
        resolve_pending,
        "_verify_remote_proposal_state",
        lambda _repo, sha, **_kwargs: verified.append(sha),
    )
    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.retarget","value":1}\n'
    )

    with pytest.raises(
        resolve_pending.LedgerProposalError,
        match="expected proposal head and base",
    ):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
            poll_seconds=0,
            poll_attempts=1,
        )

    assert any("/merge" in " ".join(args) for args, _body in calls)
    assert verified == []


def test_append_proposal_rejects_merge_response_sha_disagreement(monkeypatch) -> None:
    tree = _pre_genesis_tree()
    calls: list[tuple[tuple[str, ...], dict | None]] = []
    _install_proposal_transport(
        monkeypatch,
        tree,
        calls,
        merge_payload={"merged": True, "sha": "e" * 40},
    )
    verified: list[str] = []
    monkeypatch.setattr(
        resolve_pending,
        "_verify_remote_proposal_state",
        lambda _repo, sha, **_kwargs: verified.append(sha),
    )
    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.sha-mismatch","value":1}\n'
    )

    with pytest.raises(
        resolve_pending.LedgerProposalError,
        match="SHA disagrees with pull-request state",
    ):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
            poll_seconds=0,
            poll_attempts=1,
        )

    assert verified == []


def test_merge_recovery_rejects_retargeted_pull_request(monkeypatch) -> None:
    monkeypatch.setattr(
        resolve_pending,
        "_gh_api",
        lambda *_args, **_kwargs: json.dumps(
            {
                "merged": True,
                "merge_commit_sha": "d" * 40,
                "head": {"sha": "e" * 40},
                "base": {"ref": "other-branch"},
            }
        ),
    )

    with pytest.raises(
        resolve_pending.LedgerProposalError,
        match="expected proposal head and base",
    ):
        resolve_pending._merged_proposal_sha(
            "PolicyEngine/ledger",
            7,
            expected_head_sha="c" * 40,
            expected_base="codex/thesis-ledger-facts",
        )


def test_append_proposal_recovers_and_cleans_ambiguous_ref_creation(
    monkeypatch,
) -> None:
    tree = _pre_genesis_tree()
    calls: list[tuple[tuple[str, ...], dict | None]] = []
    _install_proposal_transport(
        monkeypatch,
        tree,
        calls,
        fail_ref_creation=True,
    )
    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.ref","value":1}\n'
    )

    with pytest.raises(RuntimeError, match="ref creation"):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
        )

    joined = [" ".join(args) for args, _ in calls]
    assert any("/git/ref/heads/" in call for call in joined)
    assert any("DELETE" in call and "/git/refs/heads/" in call for call in joined)
    assert not any("/pulls" in call for call in joined)


def test_append_proposal_recovers_and_cleans_ambiguous_pr_creation(
    monkeypatch,
) -> None:
    tree = _pre_genesis_tree()
    calls: list[tuple[tuple[str, ...], dict | None]] = []
    _install_proposal_transport(
        monkeypatch,
        tree,
        calls,
        fail_pr_creation=True,
        recover_pr_number=7,
    )
    candidate = (
        tree.files["ledger/official_observations.jsonl"]
        + b'{"source_record_id":"test.series.pr","value":1}\n'
    )

    with pytest.raises(RuntimeError, match="PR creation"):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
        )

    joined = [" ".join(args) for args, _ in calls]
    assert any("DELETE" in call and "/git/refs/heads/" in call for call in joined)
    assert any("PATCH" in call and "/pulls/7" in call for call in joined)


def test_publish_proposal_uses_one_tree_and_one_commit(monkeypatch) -> None:
    calls: list[tuple[tuple[str, ...], dict | None]] = []
    blob_number = 0

    def api(*args: str, input_body=None) -> str:
        nonlocal blob_number
        calls.append((args, input_body))
        endpoint = args[-1]
        if endpoint.endswith("/git/blobs"):
            blob_number += 1
            return json.dumps({"sha": f"{blob_number:040x}"})
        if endpoint.endswith("/git/trees"):
            return json.dumps({"sha": "e" * 40})
        if endpoint.endswith("/git/commits"):
            return json.dumps({"sha": "f" * 40})
        raise AssertionError(endpoint)

    monkeypatch.setattr(resolve_pending, "_gh_api", api)
    changes = {
        "ledger/official_observations.jsonl": b"ledger\n",
        "releases/manifests/0001-a.json": b"manifest\n",
        "releases/manifests/0001-a.freetsa.tsr": b"one",
        "releases/manifests/0001-a.digicert.tsr": b"two",
        "releases/manifests/0001-a.producer.sig": b"signature",
    }

    commit = resolve_pending._publish_proposal_commit(
        "PolicyEngine/ledger",
        base_sha="b" * 40,
        base_tree_sha="c" * 40,
        message="test",
        changes=changes,
    )

    assert commit == "f" * 40
    blob_calls = [call for call in calls if call[0][-1].endswith("/git/blobs")]
    tree_calls = [call for call in calls if call[0][-1].endswith("/git/trees")]
    commit_calls = [call for call in calls if call[0][-1].endswith("/git/commits")]
    assert len(blob_calls) == len(changes)
    assert len(tree_calls) == 1
    assert len(commit_calls) == 1
    assert tree_calls[0][1]["base_tree"] == "c" * 40
    assert {entry["path"] for entry in tree_calls[0][1]["tree"]} == set(changes)
    assert commit_calls[0][1]["parents"] == ["b" * 40]


def test_fetch_git_blob_binds_response_and_bytes_to_requested_sha(monkeypatch) -> None:
    raw = b"tree-bound blob bytes"
    requested_sha = hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw,
        usedforsecurity=False,
    ).hexdigest()
    payload = {
        "sha": requested_sha,
        "encoding": "base64",
        "content": base64.b64encode(raw).decode("ascii"),
        "size": len(raw),
    }
    monkeypatch.setattr(resolve_pending, "_gh_api", lambda *_args: json.dumps(payload))

    assert resolve_pending._fetch_git_blob("PolicyEngine/ledger", requested_sha) == raw

    payload["sha"] = "0" * 40
    with pytest.raises(resolve_pending.LedgerProposalError, match="requested blob"):
        resolve_pending._fetch_git_blob("PolicyEngine/ledger", requested_sha)

    payload["sha"] = requested_sha
    payload["content"] = base64.b64encode(b"same reported size!!").decode("ascii")
    payload["size"] = len(b"same reported size!!")
    with pytest.raises(resolve_pending.LedgerProposalError, match="do not match"):
        resolve_pending._fetch_git_blob("PolicyEngine/ledger", requested_sha)


def test_fetch_repository_tree_binds_commit_trees_and_blobs(monkeypatch) -> None:
    repo = "PolicyEngine/ledger"
    commit_sha = "a" * 40
    ledger_path = "ledger/official_observations.jsonl"
    blobs = {
        "immutable_prefix.json": b"{}\n",
        "official_observations.jsonl": b'{"source_record_id":"base"}\n',
    }
    blob_shas = {
        name: hashlib.sha1(
            f"blob {len(raw)}\0".encode("ascii") + raw,
            usedforsecurity=False,
        ).hexdigest()
        for name, raw in blobs.items()
    }
    ledger_entries = [
        {"path": name, "mode": "100644", "type": "blob", "sha": blob_shas[name]}
        for name in sorted(blobs)
    ]
    ledger_tree_sha = resolve_pending._git_tree_object_sha(ledger_entries)
    root_entries = [
        {
            "path": "ledger",
            "mode": "040000",
            "type": "tree",
            "sha": ledger_tree_sha,
        }
    ]
    root_tree_sha = resolve_pending._git_tree_object_sha(root_entries)

    def api(*args: str, input_body=None) -> str:
        del input_body
        endpoint = args[-1]
        if endpoint.endswith(f"/git/commits/{commit_sha}"):
            return json.dumps({"sha": commit_sha, "tree": {"sha": root_tree_sha}})
        if endpoint.endswith(f"/git/trees/{root_tree_sha}"):
            return json.dumps(
                {"sha": root_tree_sha, "tree": root_entries, "truncated": False}
            )
        if endpoint.endswith(f"/git/trees/{ledger_tree_sha}"):
            return json.dumps(
                {
                    "sha": ledger_tree_sha,
                    "tree": ledger_entries,
                    "truncated": False,
                }
            )
        for name, blob_sha in blob_shas.items():
            if endpoint.endswith(f"/git/blobs/{blob_sha}"):
                raw = blobs[name]
                return json.dumps(
                    {
                        "sha": blob_sha,
                        "encoding": "base64",
                        "content": base64.b64encode(raw).decode(),
                        "size": len(raw),
                    }
                )
        raise AssertionError(endpoint)

    monkeypatch.setattr(resolve_pending, "_gh_api", api)

    tree = resolve_pending._fetch_repository_tree(repo, commit_sha, ledger_path)

    assert tree.tree_sha == root_tree_sha
    assert tree.files == {
        ledger_path: blobs["official_observations.jsonl"],
        "ledger/immutable_prefix.json": blobs["immutable_prefix.json"],
    }


def test_fetch_repository_tree_rejects_swapped_commit_response(monkeypatch) -> None:
    monkeypatch.setattr(
        resolve_pending,
        "_gh_api",
        lambda *_args: json.dumps(
            {"sha": "b" * 40, "tree": {"sha": "c" * 40}}
        ),
    )

    with pytest.raises(resolve_pending.LedgerProposalError, match="requested commit"):
        resolve_pending._fetch_repository_tree(
            "PolicyEngine/ledger",
            "a" * 40,
            "ledger/official_observations.jsonl",
        )


def test_fetch_repository_tree_rejects_partial_tree_with_claimed_sha(
    monkeypatch,
) -> None:
    commit_sha = "a" * 40
    claimed_tree_sha = "c" * 40

    def api(*args: str, input_body=None) -> str:
        del input_body
        if "/git/commits/" in args[-1]:
            return json.dumps(
                {"sha": commit_sha, "tree": {"sha": claimed_tree_sha}}
            )
        return json.dumps(
            {"sha": claimed_tree_sha, "tree": [], "truncated": False}
        )

    monkeypatch.setattr(resolve_pending, "_gh_api", api)

    with pytest.raises(resolve_pending.LedgerProposalError, match="partial base state"):
        resolve_pending._fetch_repository_tree(
            "PolicyEngine/ledger",
            commit_sha,
            "ledger/official_observations.jsonl",
        )


def test_append_proposal_rejects_unwitnessed_base_state(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    tree, anchor_dir, requester, _signing_key_pem = _release_fixture_tree(tmp_path)
    path = "ledger/official_observations.jsonl"
    tree.files[path] += b'{"source_record_id":"unwitnessed","value":1}\n'
    monkeypatch.setattr(resolve_pending, "_fetch_repository_tree", lambda *_: tree)
    mutations: list[str] = []
    monkeypatch.setattr(
        resolve_pending,
        "_publish_proposal_commit",
        lambda *_args, **_kwargs: mutations.append("publish"),
    )
    candidate = tree.files[path] + b'{"source_record_id":"next","value":2}\n'

    with pytest.raises(ledger_release_chain.ReleaseChainError, match="HEAD release"):
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            path,
            candidate.decode(),
            "a" * 40,
            "b" * 40,
            1,
            timestamp_requester=requester,
            release_anchor_dir=anchor_dir,
        )

    assert mutations == []


def test_assertion_version_binds_measure_mapping_and_lineage() -> None:
    # Finding 6: av2 must change when concept mapping, authority, source
    # file/digest, lineage, or the response digest change — not only value.
    base = {
        "source_record_id": "test.series.2030",
        "value": 1.5,
        "observed_at": "2030-01-10",
        "period": {"type": "month", "value": "2030-01"},
        "measure": {
            "concept": "test.series",
            "unit": "millions",
            "source_concept": "SRC",
            "concept_authority": "auth",
        },
        "source": {"source_name": "test", "vintage": "advance", "source_file": "a.csv"},
        "source_row_keys": ["r1"],
        "responseArchive": {"sha256": "d" * 64},
    }
    base_id = resolve_pending.assertion_version(base)["id"]
    variants = [
        {"measure": {**base["measure"], "source_concept": "OTHER"}},
        {"measure": {**base["measure"], "concept_authority": "other"}},
        {"source": {**base["source"], "source_file": "b.csv"}},
        {"source_row_keys": ["r2"]},
        {"responseArchive": {"sha256": "e" * 64}},
    ]
    for override in variants:
        changed = resolve_pending.assertion_version({**base, **override})["id"]
        assert changed != base_id, f"av2 did not change for {override}"
# --------------------------------------------------------------------------
# International native-source adapters


def test_parse_ref_period_handles_international_dialects() -> None:
    cases = [
        (
            "statcan.cpi.all_items_annual_rate.canada.may_2026.first_print",
            "statcan.cpi.all_items_annual_rate.canada",
            ("month", "2026-05"),
        ),
        ("statcan.cpi.allitems.yoy.2026-05", "statcan.cpi.allitems.yoy",
         ("month", "2026-05")),
        (
            "statcan.36-10-0434-01.all_industries.month_to_month_percent_change"
            ".2026-05.first_print",
            "statcan.36-10-0434-01.all_industries.month_to_month_percent_change",
            ("month", "2026-05"),
        ),
        (
            "eurostat.hicp.all_items_annual_rate.euro_area.june_2026.flash",
            "eurostat.hicp.all_items_annual_rate.euro_area",
            ("month", "2026-06"),
        ),
        (
            "statjp.cpi.tokyo_all_items_annual_rate.june_2026.preliminary",
            "statjp.cpi.tokyo_all_items_annual_rate",
            ("month", "2026-06"),
        ),
    ]
    for ref, stem, expected in cases:
        assert resolve_pending.parse_ref_period(ref, stem) == expected
    # A final-first-print dialect is NOT silently claimed as the flash.
    assert resolve_pending.parse_ref_period(
        "eurostat.hicp.all_items_annual_rate.euro_area.may_2026"
        ".final_first_print",
        "eurostat.hicp.all_items_annual_rate.euro_area",
    ) is None


def test_pending_adapter_refs_claims_international_stems_with_units() -> None:
    def entry(slug, unit):
        return {
            "kind": "prediction_recorded",
            "forecastSlug": slug,
            "resolutionDate": "2026-07-01",
            "unit": unit,
            "interval80": {"lower": 0, "upper": 10},
        }

    refs_and_units = [
        ("statcan.cpi.all_items_annual_rate.canada.may_2026.first_print",
         "percent"),
        ("statcan.cpi.allitems.yoy.2026-05", "percent"),
        ("statcan.gdp_by_industry.monthly_growth.april_2026.first_print",
         "percent_growth"),
        ("statcan.employment_insurance.regular_beneficiaries.canada"
         ".may_2026.first_print", "thousands"),
        ("abs.cpi.all_groups.yoy.2026-06.first_print", "percent"),
        ("abs.labour.unemployment_rate.australia.may_2026.first_print",
         "percent"),
        ("abs.labour.employment_change.australia.may_2026.first_print",
         "thousands"),
        ("abs.building_approvals.total_dwellings_mom.australia.may_2026"
         ".first_print", "percent_growth"),
        ("statjp.cpi.tokyo_all_items_annual_rate.june_2026.preliminary",
         "percent"),
        ("statjp.lfs.unemployment_rate.japan.may_2026.first_print", "percent"),
        ("statjp.household_spending.real_yoy.two_or_more_person_households"
         ".may_2026.first_print", "percent_growth"),
        ("eurostat.hicp.all_items_annual_rate.euro_area.june_2026.flash",
         "percent"),
        ("eurostat.ea.hicp.flash.yoy.2026-06", "percent"),
        ("eurostat.unemployment_rate.euro_area.may_2026.first_print",
         "percent"),
        ("eurostat.retail_trade.volume_mom.euro_area.may_2026.first_print",
         "percent_growth"),
    ]
    log = {
        "entries": [
            entry(f"cell-{i}", unit)
            for i, (_, unit) in enumerate(refs_and_units)
        ],
        "resolutionLinks": [
            {"status": "pending", "forecastSlug": f"cell-{i}",
             "targetFactRef": ref}
            for i, (ref, _) in enumerate(refs_and_units)
        ]
        + [
            # Belgium is owned by its own lane; the euro-area stems must
            # not claim it.
            {"status": "pending", "forecastSlug": "cell-0",
             "targetFactRef":
                 "eurostat.une_rt_m.unemployment_rate.belgium.2026_06"
                 ".first_print"},
        ],
    }
    todo = resolve_pending.pending_adapter_refs(log)
    claimed = {item[0]: item for item in todo}
    for ref, unit in refs_and_units:
        assert ref in claimed, ref
        _, kind, spec, period_type, _, _, _ = claimed[ref]
        assert kind == "intl"
        assert period_type == "month"
        # The adapter's declared unit must equal the cell's recorded unit;
        # the resolution loop refuses on any mismatch.
        assert spec["unit"] == unit, ref
    assert (
        "eurostat.une_rt_m.unemployment_rate.belgium.2026_06.first_print"
        not in claimed
    )


def test_intl_transforms_reproduce_published_rounding() -> None:
    # YoY from rounded index, one decimal — how StatCan and the Statistics
    # Bureau publish 12-month CPI changes.
    spec = {"transform": "yoy_from_index", "round": 1}
    series = {"2025-05": 164.3, "2026-05": 169.6}
    assert resolve_pending.intl_transformed_value(spec, series, "2026-05") == 3.2
    # MoM percent from SA levels, one decimal (StatCan monthly GDP).
    spec = {"transform": "mom_pct", "round": 1}
    series = {"2026-03": 2340099.0, "2026-04": 2352903.0}
    assert resolve_pending.intl_transformed_value(spec, series, "2026-04") == 0.5
    # MoM diff in thousands, one decimal (ABS employment change).
    spec = {"transform": "mom_diff", "round": 1}
    series = {"2026-04": 14698.4961423, "2026-05": 14738.83914046}
    assert resolve_pending.intl_transformed_value(spec, series, "2026-05") == 40.3
    # Level with persons->thousands scaling (StatCan EI beneficiaries).
    spec = {"transform": "level", "scale": 0.001, "round": 2}
    series = {"2026-04": 544440.0}
    assert (
        resolve_pending.intl_transformed_value(spec, series, "2026-04")
        == 544.44
    )
    # Missing prior periods fail closed rather than fabricating a change.
    spec = {"transform": "yoy_from_index", "round": 1}
    assert (
        resolve_pending.intl_transformed_value(
            spec, {"2026-05": 169.6}, "2026-05"
        )
        is None
    )


def test_intl_anchor_gate_refuses_series_that_cannot_reproduce_history() -> None:
    spec = {
        "transform": "level",
        "round": 1,
        "anchors": {"2026-03": 4.3, "2026-04": 4.5},
        "anchor_tolerance": 0.15,
    }
    good = {"2026-03": 4.27841116, "2026-04": 4.48133963, "2026-05": 4.35594887}
    assert resolve_pending.intl_anchor_failures(spec, good) == []
    # A neighboring series (participation rate ~66.7) cannot reproduce the
    # recorded unemployment-rate history and must be refused.
    wrong_series = {"2026-03": 66.8, "2026-04": 66.7, "2026-05": 66.7}
    failures = resolve_pending.intl_anchor_failures(spec, wrong_series)
    assert len(failures) == 2
    # A missing anchor period is a failure, never a silent pass.
    assert resolve_pending.intl_anchor_failures(spec, {"2026-04": 4.5}) != []
    # raw_level anchors pin the fetched series itself (ABS employment).
    raw_spec = {
        "transform": "mom_diff",
        "round": 1,
        "anchor_transform": "raw_level",
        "anchors": {"2026-05": 14738.8},
        "anchor_tolerance": 60.0,
    }
    assert resolve_pending.intl_anchor_failures(raw_spec, good | {
        "2026-05": 14738.83914046
    }) == []
    assert resolve_pending.intl_anchor_failures(
        raw_spec, {"2026-05": 14698.5 - 200}
    ) != []


def test_intl_plausibility_gate_blocks_per_adapter_scale_blunders() -> None:
    # Canada CPI cell (percent): the index level must never resolve the
    # YoY cell.
    forecast = {"interval80": {"lower": 2.1, "upper": 3.3}}
    assert not resolve_pending.value_plausible(169.6, forecast)
    assert resolve_pending.value_plausible(3.2, forecast)
    # EI beneficiaries cell (thousands): raw persons must be refused.
    forecast = {"interval80": {"lower": 520, "upper": 557}}
    assert not resolve_pending.value_plausible(544440.0, forecast)
    assert resolve_pending.value_plausible(544.44, forecast)
    # ABS employment change cell (thousands): the level is not the change.
    forecast = {"interval80": {"lower": -35, "upper": 75}}
    assert not resolve_pending.value_plausible(14738.8, forecast)
    assert resolve_pending.value_plausible(40.3, forecast)
    # Euro retail MoM (percent_growth): a YoY-style 12-month rate of the
    # wrong magnitude class is caught by the interval gate.
    forecast = {"interval80": {"lower": -0.8, "upper": 0.9}}
    assert not resolve_pending.value_plausible(12.0, forecast)
    assert resolve_pending.value_plausible(0.2, forecast)


def test_eurostat_flash_flag_gate() -> None:
    spec = {"require_flag": True}
    # June still flagged as estimate: the flash vintage is retrievable.
    assert not resolve_pending.flash_vintage_missing(
        spec, {"2026-06": "e"}, "2026-06"
    )
    # Finals published: the flag is gone and the flash must not resolve
    # from this endpoint anymore.
    assert resolve_pending.flash_vintage_missing(spec, {}, "2026-06")
    # Non-flash specs are unaffected.
    assert not resolve_pending.flash_vintage_missing({}, {}, "2026-06")


def test_tokyo_july_cell_is_held_for_anchor_contradiction() -> None:
    ref = "statjp.cpi.tokyo_all_items_annual_rate.july_2026.preliminary"
    assert ref in resolve_pending.INTL_RESOLUTION_HOLDS
    assert "contradicts" in resolve_pending.INTL_RESOLUTION_HOLDS[ref] or (
        "reviewed" in resolve_pending.INTL_RESOLUTION_HOLDS[ref]
    )


def test_jp_page_parsers_and_reference_month() -> None:
    lfs_html = (
        "<html><body>労働力調査（基本集計）　2026年（令和8年）5月分結果　"
        "2026年6月30日公表 <table>年平均 月次（季節調整値） 2023年 2024年 "
        "2025年 2026年2月 3月 4月 5月 完全失業率 2.6% 2.5% 2.5% 2.6% 2.7% "
        "2.5% 2.5%</table></body></html>"
    ).encode("utf-8")
    assert resolve_pending.jp_page_reference_period(lfs_html) == "2026-05"
    series = resolve_pending.jp_lfs_unemployment_series(lfs_html)
    assert series["2026-02"] == 2.6
    assert series["2026-03"] == 2.7
    assert series["2026-04"] == 2.5
    assert series["2026-05"] == 2.5

    kakei_html = (
        "<html><body>家計調査（二人以上の世帯）2026年（令和8年）5月分 "
        "（2026年7月7日公表）<table>月次（前年同月比、【&nbsp;】内は前月比"
        "（季節調整値）％） <td>2023年</td><td>2024年</td><td>2025年</td>"
        "<td>2026年2月</td><td>3月</td><td>4月</td><td>5月</td>"
        "<td>【二人以上の世帯】</td><td>&nbsp;消費支出（実質）</td><td></td>"
        "<td>▲2.6</td><td>▲1.1</td><td>0.9</td><td>▲1.8</td><td>【1.5】</td>"
        "<td>▲2.9</td><td>【▲1.3】</td><td>▲0.5</td><td>【1.6】</td>"
        "<td>▲0.4</td><td>【3.7】</td> ≪ポイント≫</table></body></html>"
    ).encode("utf-8")
    assert resolve_pending.jp_page_reference_period(kakei_html) == "2026-05"
    series = resolve_pending.jp_kakei_real_yoy_series(kakei_html)
    assert series["2026-02"] == -1.8
    assert series["2026-03"] == -2.9
    assert series["2026-04"] == -0.5
    assert series["2026-05"] == -0.4


def test_release_page_headline_parsers_sign_and_month_binding() -> None:
    retail = (
        "<h1>Volume of retail trade up by 0.2% in the euro area and by "
        "0.5% in the EU</h1><p>In May 2026, compared with April 2026, the "
        "seasonally adjusted retail trade volume increased by 0.2% in the "
        "euro area and by 0.5% in the EU.</p>"
    ).encode()
    assert resolve_pending.eurostat_retail_headline(retail, "2026-05") == 0.2
    # The parser binds to the page's own reference month: asking the May
    # page for April returns nothing rather than the wrong month's print.
    assert resolve_pending.eurostat_retail_headline(retail, "2026-04") is None
    falling = retail.replace(b"increased", b"decreased")
    assert resolve_pending.eurostat_retail_headline(falling, "2026-05") == -0.2

    approvals = (
        "<h2>Key statistics</h2><p>The May 2026 seasonally adjusted "
        "estimate:</p><ul><li>Total dwellings approved fell 1.1% to "
        "17,019.</li></ul>"
    ).encode()
    assert resolve_pending.abs_ba_headline(approvals, "2026-05") == -1.1
    assert resolve_pending.abs_ba_headline(approvals, "2026-04") is None
    rising = approvals.replace(b"fell 1.1%", b"rose 3.4%")
    assert resolve_pending.abs_ba_headline(rising, "2026-05") == 3.4


def test_estat_xlsx_parser_maps_sparse_cells_by_column() -> None:
    import io as io_module
    import zipfile

    shared_strings = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/'
        'main" count="4" uniqueCount="4">'
        "<si><t>類・品目符号</t></si><si><t>0001</t></si>"
        "<si><t>0161</t></si><si><t>東京都区部</t></si></sst>"
    )
    # Row 2 is the code row (J=0001, K=0161); data rows carry sparse cells
    # so document order lies about columns — exactly the recent-row shape
    # of the real workbook.
    sheet = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/'
        '2006/main"><sheetData>'
        '<row r="2"><c r="A2" t="s"><v>0</v></c><c r="J2" t="s"><v>1</v></c>'
        '<c r="K2" t="s"><v>2</v></c></row>'
        '<row r="3"><c r="B3"><v>202605</v></c><c r="I3" t="s"><v>3</v></c>'
        '<c r="J3"><v>112.7</v></c><c r="K3"><v>112.0</v></c></row>'
        '<row r="4"><c r="B4"><v>202606</v></c>'
        '<c r="J4"><v>112.7</v></c></row>'
        '<row r="5"><c r="B5"><v>202506</v></c><c r="E5"><v>6</v></c>'
        '<c r="J5"><v>110.8</v></c></row>'
        "</sheetData></worksheet>"
    )
    buffer = io_module.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("xl/sharedStrings.xml", shared_strings)
        archive.writestr("xl/worksheets/sheet1.xml", sheet)
    series = resolve_pending.estat_xlsx_index_series(buffer.getvalue())
    assert series == {"2026-05": 112.7, "2026-06": 112.7, "2025-06": 110.8}
    spec = {"transform": "yoy_from_index", "round": 1}
    assert (
        resolve_pending.intl_transformed_value(spec, series, "2026-06") == 1.7
    )


def test_intl_fact_rows_carry_country_geography_and_concept() -> None:
    spec = resolve_pending.INTL_ADAPTERS["statcan.cpi.allitems.yoy"]
    row = resolve_pending.generic_fact(
        "statcan.cpi.allitems.yoy.2026-05",
        spec,
        "month",
        "2026-05",
        3.2,
        __import__("datetime").date(2026, 6, 22),
        "https://www150.statcan.gc.ca/t1/wds/rest/example",
        spec["source_file"],
    )
    assert row["geography"]["id"] == "CA"
    assert row["geography"]["name"] == "Canada"
    assert row["measure"]["concept"] == "statcan.cpi.allitems.yoy.2026-05"
    assert row["measure"]["unit"] == "percent"

    flash_spec = resolve_pending.INTL_ADAPTERS["eurostat.ea.hicp.flash.yoy"]
    row = resolve_pending.generic_fact(
        "eurostat.hicp.all_items_annual_rate.euro_area.june_2026.flash",
        flash_spec,
        "month",
        "2026-06",
        2.8,
        __import__("datetime").date(2026, 7, 1),
        "https://ec.europa.eu/eurostat/api/example",
        flash_spec["source_file"],
    )
    assert row["geography"]["id"] == "EA21"
    # The euro area must use a level the ledger's arch fact schema admits
    # (the append gate rejected "area"; regression for PolicyEngine/ledger#90).
    assert row["geography"]["level"] == "region"
    # The print-kind suffix is stripped from the measure concept.
    assert row["measure"]["concept"] == (
        "eurostat.hicp.all_items_annual_rate.euro_area.june_2026"
    )
    # US adapters keep the existing geography.
    us_row = resolve_pending.generic_fact(
        "bls.cps.unemployment_rate.june_2026.first_print",
        resolve_pending.ALFRED_ADAPTERS["bls.cps.unemployment_rate"],
        "month",
        "2026-06",
        4.1,
        __import__("datetime").date(2026, 7, 2),
        "https://alfred.stlouisfed.org/example",
        "alfredgraph.csv",
    )
    assert us_row["geography"]["id"] == "0100000US"


def test_intl_dialects_share_one_spec_so_dialects_share_archives() -> None:
    adapters = resolve_pending.INTL_ADAPTERS
    assert adapters["statcan.cpi.all_items_annual_rate.canada"] is (
        adapters["statcan.cpi.allitems.yoy"]
    )
    assert adapters["eurostat.hicp.all_items_annual_rate.euro_area"] is (
        adapters["eurostat.ea.hicp.flash.yoy"]
    )
    assert adapters["abs.cpi.all_groups_annual_rate.australia"] is (
        adapters["abs.cpi_indicator.allgroups.yoy"]
    )
    assert adapters["statcan.gdp_by_industry.monthly_growth"] is (
        adapters[
            "statcan.36-10-0434-01.all_industries"
            ".month_to_month_percent_change"
        ]
    )


def test_custody_seal_accepts_xlsx_response_archives(tmp_path) -> None:
    """The e-Stat workbook is a first-class resolver response.

    Regression: the first international run failed custody verification
    because the response-name schema only admitted csv/html/json.
    """
    original_root = resolve_pending.ROOT
    resolve_pending.ROOT = tmp_path
    try:
        run_dir = tmp_path / "records" / "resolutions" / "run"
        raw = b"PK\x03\x04 not a real workbook, bytes are opaque here"
        archive = resolve_pending.archive_response(
            run_dir,
            series_id="estat-tokyo-cpi-table1-2",
            vintage="2026-06-26",
            raw=raw,
            extension="xlsx",
        )
        assert archive["path"].endswith(".xlsx.gz")
        manifest = resolve_pending.finalize_resolution_manifest(
            run_dir,
            {
                "schemaVersion": "thesis_resolution_run_v1",
                "retrievedAt": "2026-07-10T20:00:00Z",
                "ledgerRepo": "PolicyEngine/ledger",
                "ledgerBranch": "test",
                "ledgerRepoSha": "0" * 40,
                "facts": [
                    {
                        "dataPointId": (
                            "statjp.cpi.tokyo_all_items_annual_rate"
                            ".june_2026.preliminary"
                        ),
                        "sourceVintage": "2026-06-26",
                        "retrievedAt": "2026-07-10T20:00:00Z",
                        "responseArchive": archive,
                    }
                ],
            },
        )
        result = verify_run(run_dir)
        assert result.inventory_status == "complete"
        assert manifest["custodyInventoryVersion"] == 2
    finally:
        resolve_pending.ROOT = original_root
