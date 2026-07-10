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


def _proposal_api_stub(gate_conclusion: str, calls: list[list[str]]):
    import base64 as _base64
    import json as _json

    payload = _json.dumps(
        {"source_record_id": "test.series.2030", "value": 1}
    )

    def fake_run(command, **_kwargs):
        calls.append(command)
        joined = " ".join(command)
        if "/git/refs" in joined and "-X POST" in joined:
            return SimpleNamespace(returncode=0, stdout="{}", stderr="")
        if "/contents/" in joined and "-X PUT" in joined:
            return SimpleNamespace(
                returncode=0,
                stdout=_json.dumps({"commit": {"sha": "h" * 40}}),
                stderr="",
            )
        if joined.endswith("/pulls") and "-X POST" in joined:
            return SimpleNamespace(
                returncode=0, stdout=_json.dumps({"number": 7}), stderr=""
            )
        if "/check-runs" in joined:
            return SimpleNamespace(
                returncode=0,
                stdout=_json.dumps(
                    {
                        "check_runs": [
                            {
                                "name": "Append gate",
                                "status": "completed",
                                "conclusion": gate_conclusion,
                            }
                        ]
                    }
                ),
                stderr="",
            )
        if "/merge" in joined:
            return SimpleNamespace(returncode=0, stdout="{}", stderr="")
        if "-X DELETE" in joined:
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        if "/commits/" in joined:
            return SimpleNamespace(returncode=0, stdout="m" * 40 + "\n", stderr="")
        if "/contents/" in joined:
            return SimpleNamespace(
                returncode=0,
                stdout=_json.dumps(
                    {
                        "content": _base64.b64encode(
                            (payload + "\n").encode()
                        ).decode()
                    }
                ),
                stderr="",
            )
        raise AssertionError(f"unexpected gh call: {joined}")

    return fake_run, payload


def test_append_proposal_merges_only_after_the_gate_passes(monkeypatch) -> None:
    calls: list[list[str]] = []
    fake_run, payload = _proposal_api_stub("success", calls)
    monkeypatch.setattr(resolve_pending.subprocess, "run", fake_run)

    merged = resolve_pending.propose_ledger_append(
        "PolicyEngine/ledger",
        "codex/thesis-ledger-facts",
        "ledger/official_observations.jsonl",
        payload + "\n",
        "blob-sha",
        "b" * 40,
        1,
        poll_seconds=0,
        poll_attempts=1,
    )

    assert merged == "m" * 40
    assert any("/merge" in " ".join(c) for c in calls)


def test_append_proposal_refuses_to_merge_on_gate_failure(monkeypatch) -> None:
    calls: list[list[str]] = []
    fake_run, payload = _proposal_api_stub("failure", calls)
    monkeypatch.setattr(resolve_pending.subprocess, "run", fake_run)

    try:
        resolve_pending.propose_ledger_append(
            "PolicyEngine/ledger",
            "codex/thesis-ledger-facts",
            "ledger/official_observations.jsonl",
            payload + "\n",
            "blob-sha",
            "b" * 40,
            1,
            poll_seconds=0,
            poll_attempts=1,
        )
    except RuntimeError as error:
        assert "append gate did not pass" in str(error)
    else:
        raise AssertionError("gate failure did not block the merge")
    assert not any("/merge" in " ".join(c) for c in calls)


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
