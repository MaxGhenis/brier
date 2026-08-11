from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import register_targets  # noqa: E402
import resolve_pending  # noqa: E402
from adopt_proven_series import (  # noqa: E402
    SOURCE_BINDING_DERIVED_KEYS,
    SOURCE_BINDING_TEMPLATE_KEYS,
)
from canonical_json import canonical_bytes  # noqa: E402

APEL_SERIES = {
    "usaspending.dod.prime_award_obligations",
    "usaspending.dod.prime_contract_obligations",
    "usaspending.dod.new_prime_awards",
    "usaspending.dod.prime_award_transactions",
    "usaspending.dod.unique_prime_contract_recipients",
    "usaspending.dod.small_business_contract_obligation_share",
    "usaspending.dhs.title_vi.award_transaction_obligations",
}
WAVE_B1_SPEC_ONLY_SERIES = {
    "usaspending.cdfi.assistance_transaction_obligations",
    "usaspending.ondcp.hidta_al95001_obligations",
    "usaspending.ntia.broadband_al11038_obligations",
    "usaspending.usfs.minnesota_place_of_performance_obligations",
}


def apel_templates() -> list[dict]:
    doc = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    return [
        entry
        for entry in doc["series"]
        if entry["series"].startswith("usaspending.")
    ]


def test_registrar_admits_the_new_policy_and_adapter() -> None:
    assert "registered_query_snapshot" in register_targets.RELEASE_POLICIES
    assert "usaspending-api" in register_targets.SOURCE_ADAPTERS


def test_apel_templates_carry_exactly_the_template_keys() -> None:
    entries = apel_templates()
    assert {entry["series"] for entry in entries} == APEL_SERIES
    for entry in entries:
        binding = entry["extras"]["sourceBinding"]
        assert set(binding) == SOURCE_BINDING_TEMPLATE_KEYS, entry["series"]
        assert not (set(binding) & SOURCE_BINDING_DERIVED_KEYS)
        assert binding["adapter"] == "usaspending-api"
        assert binding["releasePolicy"] == "registered_query_snapshot"
        assert binding["sourceUrl"].startswith(
            "https://api.usaspending.gov/api/v2/"
        )
        transform = binding["transform"]
        assert transform["operation"] in {
            "multiply",
            "count_distinct",
            "ratio_percent",
        }
        # GET URLs carry the fiscal-year token directly. The POST query plans
        # carry it in the reviewed transform that is part of the seven-key
        # binding.
        assert (
            "{fiscal_year}" in binding["sourceUrl"]
            or transform["fiscalYear"] == "{fiscal_year}"
        )
        assert 0 < float(transform["factor"]) <= 1


def test_registry_and_resolver_specs_match_bidirectionally_on_all_seven_keys() -> None:
    registry = {entry["series"]: entry for entry in apel_templates()}
    specs = resolve_pending.USASPENDING_ADAPTERS
    assert set(registry) == APEL_SERIES
    assert set(specs) == APEL_SERIES | WAVE_B1_SPEC_ONLY_SERIES

    for series, entry in registry.items():
        spec = specs[series]
        binding = entry["extras"]["sourceBinding"]
        assert resolve_pending.usaspending_binding_template(spec) == binding
        assert resolve_pending.usaspending_binding_matches_spec(binding, spec)

        derived_binding = {
            **binding,
            "allowedHosts": ["api.usaspending.gov"],
            "expectedReleaseWindow": entry["extras"]["expectedReleaseWindow"],
        }
        assert resolve_pending.usaspending_binding_matches_spec(
            derived_binding,
            spec,
        )
        assert spec["scale"] == float(binding["transform"]["factor"])

        for key in SOURCE_BINDING_TEMPLATE_KEYS:
            tampered = copy.deepcopy(binding)
            if key == "transform":
                tampered[key]["factor"] = float(tampered[key]["factor"]) + 1
            else:
                tampered[key] = f"{tampered[key]}-tampered"
            assert not resolve_pending.usaspending_binding_matches_spec(
                tampered,
                spec,
            ), f"{series} accepted drift in {key}"

        missing = copy.deepcopy(binding)
        missing.pop("field")
        assert not resolve_pending.usaspending_binding_matches_spec(missing, spec)
        assert not resolve_pending.usaspending_binding_matches_spec(
            {**binding, "unreviewedQueryOption": True},
            spec,
        )


def recipient_transform() -> dict:
    return resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.dod.unique_prime_contract_recipients"
    ]["transform"]


def share_transform() -> dict:
    return resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.dod.small_business_contract_obligation_share"
    ]["transform"]


def dhs_award_transaction_transform() -> dict:
    return resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.dhs.title_vi.award_transaction_obligations"
    ]["transform"]


def cdfi_program_transform() -> dict:
    return resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.cdfi.assistance_transaction_obligations"
    ]["transform"]


def hidta_program_transform() -> dict:
    return resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.ondcp.hidta_al95001_obligations"
    ]["transform"]


def ntia_broadband_program_transform() -> dict:
    return resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.ntia.broadband_al11038_obligations"
    ]["transform"]


def usfs_minnesota_transform() -> dict:
    return resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.usfs.minnesota_place_of_performance_obligations"
    ]["transform"]


def test_recipient_post_body_is_the_exact_registered_fy2026_query() -> None:
    expected = {
        "category": "recipient",
        "filters": {
            "agencies": [
                {
                    "type": "awarding",
                    "tier": "toptier",
                    "name": "Department of Defense",
                }
            ],
            "award_type_codes": ["A", "B", "C", "D"],
            "time_period": [
                {"end_date": "2026-09-30", "start_date": "2025-10-01"}
            ],
        },
        "limit": 100,
        "page": 2,
        "spending_level": "transactions",
    }
    body = resolve_pending.usaspending_recipient_page_body(
        "2026",
        recipient_transform(),
        2,
    )

    assert body == expected
    assert canonical_bytes(body) == canonical_bytes(expected)
    assert body == resolve_pending.usaspending_recipient_page_body(
        "2026",
        recipient_transform(),
        2,
    )


def test_recipient_post_body_rejects_boolean_pagination_values() -> None:
    with pytest.raises(ValueError, match="query plan"):
        resolve_pending.usaspending_recipient_page_body(
            "2026",
            recipient_transform(),
            True,
        )

    transform = copy.deepcopy(recipient_transform())
    transform["pageSize"] = True
    with pytest.raises(ValueError, match="query plan"):
        resolve_pending.usaspending_recipient_page_body("2026", transform, 1)


def test_share_post_bodies_only_differ_by_registered_filter() -> None:
    denominator, numerator = resolve_pending.usaspending_share_bodies(
        "2026",
        share_transform(),
    )
    base_filters = {
        "agencies": [
            {
                "type": "awarding",
                "tier": "toptier",
                "name": "Department of Defense",
            }
        ],
        "award_type_codes": ["A", "B", "C", "D"],
        "time_period": [
            {"end_date": "2026-09-30", "start_date": "2025-10-01"}
        ],
    }
    assert denominator == {
        "filters": base_filters,
        "group": "fiscal_year",
        "spending_level": "transactions",
    }
    assert numerator == {
        "filters": {
            **base_filters,
            "recipient_type_names": ["small_business"],
        },
        "group": "fiscal_year",
        "spending_level": "transactions",
    }
    assert "recipient_type_names" not in denominator["filters"]
    assert canonical_bytes(denominator) != canonical_bytes(numerator)


def test_dhs_post_body_is_the_exact_award_transaction_query() -> None:
    actual = resolve_pending.usaspending_fiscal_year_post_body(
        "2026",
        dhs_award_transaction_transform(),
    )
    assert actual["group"] == "fiscal_year"
    assert actual["spending_level"] == "transactions"
    assert actual["filters"]["time_period"] == [
        {"end_date": "2026-09-30", "start_date": "2025-10-01"}
    ]
    assert actual["filters"]["award_type_codes"] == [
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "A",
        "B",
        "C",
        "D",
        "IDV_A",
        "IDV_B",
        "IDV_B_A",
        "IDV_B_B",
        "IDV_B_C",
        "IDV_C",
        "IDV_D",
        "IDV_E",
    ]
    assert actual["filters"]["treasury_account_components"] == [
        {
            "aid": "070",
            "bpoa": "2025",
            "epoa": "2029",
            "main": "0530",
            "sub": "000",
        },
        {
            "aid": "070",
            "bpoa": "2025",
            "epoa": "2029",
            "main": "0532",
            "sub": "000",
        },
        {
            "aid": "070",
            "bpoa": "2025",
            "epoa": "2029",
            "main": "0509",
            "sub": "000",
        },
        {
            "aid": "070",
            "bpoa": "2025",
            "epoa": "2029",
            "main": "0510",
            "sub": "000",
        },
        {
            "aid": "070",
            "bpoa": "2025",
            "epoa": "2029",
            "main": "0413",
            "sub": "000",
        },
        {"aid": "070", "main": "0722"},
    ]
    assert hashlib.sha256(canonical_bytes(actual)).hexdigest() == (
        "340c6f761a86878475118a2dea32711986652d2d019c6cbd4bed2c2efdb3fb56"
    )


def test_cdfi_post_body_byte_matches_wave_a_capture_and_anchor() -> None:
    request = json.loads(
        (
            ROOT
            / "drafts"
            / "ledger-ingestion"
            / "usaspending-cdfi-fund-program-obligations.json"
        ).read_text()
    )
    query = request["verification"]["query"]
    spec = resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.cdfi.assistance_transaction_obligations"
    ]
    actual = resolve_pending.usaspending_fiscal_year_post_body(
        "2025",
        cdfi_program_transform(),
    )

    assert query["method"] == "POST"
    assert query["endpoint"] == spec["url_template"]
    assert query["field"] == spec["field"].format(fiscal_year="2025")
    assert actual == query["body"]
    assert canonical_bytes(actual) == canonical_bytes(query["body"])
    assert len(canonical_bytes(actual)) == 315
    assert hashlib.sha256(canonical_bytes(actual)).hexdigest() == (
        "55b613d18a2f4763b68355f01d37a02f07700c0330320b658f2bd676a22b1543"
    )

    evidence = request["verification"]["fetchedEvidence"]
    assert evidence["responseSha256"] == (
        "ed1225baa11ce0e294590cab40927060f62ebea1df9ea094909b797a0f06f0f1"
    )
    assert evidence["responseByteLength"] == 1_137
    assert resolve_pending.usaspending_fiscal_year_amount(
        {"results": evidence["resultRows"]},
        "2025",
    ) == 319_455_176.0


def test_cdfi_spec_preserves_the_wave_a_scope_caveats() -> None:
    spec = resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.cdfi.assistance_transaction_obligations"
    ]
    assert spec["label"] == (
        "CDFI Fund financial-assistance award-transaction obligations, "
        "fiscal year total"
    )
    assert "signed net federal_action_obligation" in spec["source_concept"]
    assert "non-award financial-account obligations and outlays" in spec[
        "evidence_notes"
    ]
    assert "bill-specific amended-section-113 activity" in spec["evidence_notes"]


def test_hidta_post_body_byte_matches_wave_a_capture_and_anchor() -> None:
    request = json.loads(
        (
            ROOT
            / "drafts"
            / "ledger-ingestion"
            / "usaspending-ondcp-hidta-program-obligations.json"
        ).read_text()
    )
    query = request["verification"]["query"]
    spec = resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.ondcp.hidta_al95001_obligations"
    ]
    actual = resolve_pending.usaspending_fiscal_year_post_body(
        "2025",
        hidta_program_transform(),
    )

    assert query["method"] == "POST"
    assert query["endpoint"] == spec["url_template"]
    assert query["field"] == spec["field"].format(fiscal_year="2025")
    assert actual == query["body"]
    assert canonical_bytes(actual) == canonical_bytes(query["body"])
    assert len(canonical_bytes(actual)) == 235
    assert hashlib.sha256(canonical_bytes(actual)).hexdigest() == (
        "df29835ff171f2649aaf7f33b4e6f2fc41f3efca5f8e92ae5e9e2ee16dec2c67"
    )

    evidence = request["verification"]["fetchedEvidence"]
    assert evidence["responseSha256"] == (
        "5caa8207b4160327a16411454468ccf7383dbde16f47312e311ac7a798898b95"
    )
    assert evidence["responseByteLength"] == 1_130
    assert resolve_pending.usaspending_fiscal_year_amount(
        {"results": evidence["resultRows"]},
        "2025",
    ) == 271_657_675.6


def test_hidta_spec_preserves_the_wave_a_scope_caveats() -> None:
    spec = resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.ondcp.hidta_al95001_obligations"
    ]
    assert spec["label"] == (
        "HIDTA Assistance Listing 95.001 financial-assistance "
        "award-transaction obligations, fiscal year total"
    )
    assert spec["transform"]["programNumbers"] == ["95.001"]
    assert "agency" not in spec["transform"]
    assert "whole Assistance Listing 95.001" in spec["evidence_notes"]
    assert "section 707(s) supplemental competitive grants" in spec[
        "evidence_notes"
    ]
    assert "all HIDTA financial-account obligations, outlays" in spec[
        "evidence_notes"
    ]
    assert "bill-caused spending" in spec["evidence_notes"]


def test_ntia_broadband_post_body_byte_matches_wave_a_capture_and_anchor() -> None:
    request = json.loads(
        (
            ROOT
            / "drafts"
            / "ledger-ingestion"
            / "usaspending-ntia-broadband-program-obligations.json"
        ).read_text()
    )
    query = request["verification"]["query"]
    spec = resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.ntia.broadband_al11038_obligations"
    ]
    actual = resolve_pending.usaspending_fiscal_year_post_body(
        "2025",
        ntia_broadband_program_transform(),
    )

    assert query["method"] == "POST"
    assert query["endpoint"] == spec["url_template"]
    assert query["field"] == spec["field"].format(fiscal_year="2025")
    assert actual == query["body"]
    assert canonical_bytes(actual) == canonical_bytes(query["body"])
    assert len(canonical_bytes(actual)) == 235
    assert hashlib.sha256(canonical_bytes(actual)).hexdigest() == (
        "232ff1c92f7ee2a962a8e54cc1779b1bee1e46976551fc71664b81a9dee5f205"
    )

    evidence = request["verification"]["fetchedEvidence"]
    assert evidence["responseSha256"] == (
        "bcda917cb217ca7fb442ff3b32aa291e11696326043d3a33205b66b9ef13cf64"
    )
    assert evidence["responseByteLength"] == 1_132
    assert resolve_pending.usaspending_fiscal_year_amount(
        {"results": evidence["resultRows"]},
        "2025",
    ) == 409_852_406.47


def test_ntia_broadband_spec_preserves_the_wave_a_scope_caveats() -> None:
    spec = resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.ntia.broadband_al11038_obligations"
    ]
    assert spec["label"] == (
        "Assistance Listing 11.038 Public Wireless Supply Chain Innovation "
        "Fund financial-assistance award-transaction obligations, fiscal year total"
    )
    assert spec["transform"]["programNumbers"] == ["11.038"]
    assert "agency" not in spec["transform"]
    assert "treasuryAccountComponents" not in spec["transform"]
    assert "signed net federal_action_obligation" in spec["source_concept"]
    assert "whole Assistance Listing 11.038" in spec["evidence_notes"]
    assert "no awarding-agency, awarding-subagency" in spec["evidence_notes"]
    assert "outcomes of the proposed 6G Task Force" in spec["evidence_notes"]
    assert "spending caused or authorized by H.R. 2449" in spec["evidence_notes"]
    assert "all NTIA, NIST, Commerce, or FCC obligations" in spec["evidence_notes"]
    assert "all obligations or outlays of federal account 013-0565" in spec[
        "evidence_notes"
    ]


def test_usfs_minnesota_post_body_byte_matches_wave_a_capture_and_anchor() -> None:
    request = json.loads(
        (
            ROOT
            / "drafts"
            / "ledger-ingestion"
            / "usaspending-usfs-superior-nf-obligations.json"
        ).read_text()
    )
    query = request["verification"]["query"]
    spec = resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.usfs.minnesota_place_of_performance_obligations"
    ]
    actual = resolve_pending.usaspending_fiscal_year_post_body(
        "2025",
        usfs_minnesota_transform(),
    )

    assert query["method"] == "POST"
    assert query["endpoint"] == spec["url_template"]
    assert query["field"] == spec["field"].format(fiscal_year="2025")
    assert actual == query["body"]
    assert canonical_bytes(actual) == canonical_bytes(query["body"])
    assert len(canonical_bytes(actual)) == 475
    assert hashlib.sha256(canonical_bytes(actual)).hexdigest() == (
        "59c5a37d550b6d3cbff5a845d3e2b0f994056e81c7c506d71fcf81c55faa6f2a"
    )

    evidence = request["verification"]["fetchedEvidence"]
    assert evidence["responseSha256"] == (
        "685c55dd28dc9824d018ce6ebb960d612e3a1d66fb9beb77862b381b47282f20"
    )
    assert evidence["responseByteLength"] == 1_150
    assert (
        resolve_pending.usaspending_fiscal_year_amount(
            {"results": evidence["resultRows"]},
            "2025",
        )
        == 46_832_556.79
    )


def test_usfs_minnesota_spec_preserves_the_wave_a_scope_caveats() -> None:
    spec = resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.usfs.minnesota_place_of_performance_obligations"
    ]
    assert spec["label"] == (
        "Minnesota-wide Forest Service award-transaction obligations "
        "(context only), fiscal year total"
    )
    assert "Superior National Forest" not in spec["label"]
    assert spec["transform"]["agency"] == {
        "name": "Forest Service",
        "tier": "subtier",
        "toptier_name": "Department of Agriculture",
        "type": "awarding",
    }
    assert spec["transform"]["placeOfPerformanceLocations"] == [
        {"country": "USA", "state": "MN"}
    ]
    assert "signed net federal_action_obligation" in spec["source_concept"]
    assert "Minnesota-wide spending context only" in spec["evidence_notes"]
    assert "not Superior National Forest obligations" in spec["evidence_notes"]
    assert "No value is attributed to H.R. 978" in spec["evidence_notes"]
    assert "mine-plan reviews, permits, mineral leases" in spec["evidence_notes"]
    assert "financial-account obligations, appropriations" in spec["evidence_notes"]
    assert "bill-caused spending" in spec["evidence_notes"]


def test_fiscal_year_post_body_rejects_mixed_or_malformed_scope_filters() -> None:
    mixed = copy.deepcopy(cdfi_program_transform())
    mixed["treasuryAccountComponents"] = copy.deepcopy(
        dhs_award_transaction_transform()["treasuryAccountComponents"]
    )
    with pytest.raises(ValueError, match="fiscal-year POST plan"):
        resolve_pending.usaspending_fiscal_year_post_body("2025", mixed)

    malformed = copy.deepcopy(cdfi_program_transform())
    malformed["agency"]["tier"] = "toptier"
    with pytest.raises(ValueError, match="awarding-subtier"):
        resolve_pending.usaspending_fiscal_year_post_body("2025", malformed)

    mixed_program = copy.deepcopy(hidta_program_transform())
    mixed_program["agency"] = copy.deepcopy(cdfi_program_transform()["agency"])
    with pytest.raises(ValueError, match="fiscal-year POST plan"):
        resolve_pending.usaspending_fiscal_year_post_body("2025", mixed_program)

    for bad_program_numbers in ([], ["95.1"], ["95.001", "95.001"], [95.001]):
        malformed_program = copy.deepcopy(hidta_program_transform())
        malformed_program["programNumbers"] = bad_program_numbers
        with pytest.raises(ValueError, match="program numbers"):
            resolve_pending.usaspending_fiscal_year_post_body(
                "2025",
                malformed_program,
            )

    malformed_toptier = copy.deepcopy(usfs_minnesota_transform())
    malformed_toptier["agency"]["toptier_name"] = ""
    with pytest.raises(ValueError, match="awarding-subtier"):
        resolve_pending.usaspending_fiscal_year_post_body(
            "2025",
            malformed_toptier,
        )

    for bad_locations in (
        [],
        [{"country": "USA"}],
        [{"country": "US", "state": "MN"}],
        [{"country": "USA", "state": "Minnesota"}],
        [
            {"country": "USA", "state": "MN"},
            {"country": "USA", "state": "MN"},
        ],
    ):
        malformed_location = copy.deepcopy(usfs_minnesota_transform())
        malformed_location["placeOfPerformanceLocations"] = bad_locations
        with pytest.raises(ValueError, match="place-of-performance"):
            resolve_pending.usaspending_fiscal_year_post_body(
                "2025",
                malformed_location,
            )

    unpaired_location = copy.deepcopy(hidta_program_transform())
    unpaired_location["placeOfPerformanceLocations"] = [
        {"country": "USA", "state": "MN"}
    ]
    with pytest.raises(ValueError, match="fiscal-year POST plan"):
        resolve_pending.usaspending_fiscal_year_post_body(
            "2025",
            unpaired_location,
        )


def test_dhs_series_is_narrow_and_account_obligations_request_stays_open() -> None:
    series = "usaspending.dhs.title_vi.award_transaction_obligations"
    old_series = "usaspending.dhs.title_vi.named_account_obligations"
    registry = {entry["series"]: entry for entry in apel_templates()}

    assert old_series not in registry
    assert old_series not in resolve_pending.USASPENDING_ADAPTERS
    entry = registry[series]
    assert entry["slug"] == (
        "us-dhs-title-vi-award-transaction-obligations-{period}"
    )
    binding = entry["extras"]["sourceBinding"]
    assert binding["sourceSeriesId"] == (
        "usaspending.search.spending_over_time.dhs.title_vi."
        "award_transaction_obligations"
    )
    assert binding["table"] == (
        "USAspending API v2 advanced search, DHS Title VI award transactions "
        "filtered to named Treasury accounts, obligations by fiscal year"
    )

    spec = resolve_pending.USASPENDING_ADAPTERS[series]
    assert spec["label"] == (
        "DHS Title VI award-transaction obligations, fiscal year total"
    )
    assert spec["source_concept"].startswith(
        "aggregated_amount of award transactions"
    )

    request = json.loads(
        (
            ROOT
            / "drafts"
            / "ledger-ingestion"
            / "usaspending-dhs-title-vi-named-account-obligations.json"
        ).read_text()
    )
    assert request["proposed_concept"] == old_series
    assert request["status"] == "proposed"
    assert request["verification"]["outcome"] == "proposed"
    assert request["likelyUrlPattern"] == (
        "https://api.usaspending.gov/api/v2/download/accounts/"
    )
    assert "financial-account submission/TAS path" in request["note"]
    assert series in request["note"]


def test_usda_aftpp_request_stays_proposed_pending_isolation() -> None:
    request = json.loads(
        (
            ROOT
            / "drafts"
            / "ledger-ingestion"
            / "usaspending-usda-selected-rural-program-obligations.json"
        ).read_text()
    )

    assert request["status"] == "proposed"
    assert request["verification"]["outcome"] == "proposed"
    identity = request["verification"]["implementationIdentityEvidence"]
    assert identity == {
        "sourceUrl": (
            "https://simpler.grants.gov/opportunity/"
            "06f0ec84-e04b-4258-bc33-1634d1209b42"
        ),
        "publisher": "USDA Foreign Agricultural Service",
        "opportunityTitle": "2026 America First Trade Promotion Program",
        "opportunityNumber": "USDA-FAS-AFTPP-2026",
        "assistanceListingNumber": "10.618",
        "programFunding": 285_000_000,
    }
    current = request["verification"]["currentUsaspendingState"]
    assert current["assistanceListingLookup"]["matchedRow"] == {
        "programNumber": "10.618",
        "programTitle": "Regional Agricultural Promotion Program",
        "popularName": "Regional Agricultural Promotion Program",
    }
    assert current["exactNameSpendingQuery"]["resultRow"] == {
        "fiscalYear": "2026",
        "aggregatedAmount": 0,
    }
    assert "award isolation and reporting lag remain open" in request["note"]
    assert "reporting lag" in request["verification"]["reason"]

    report = (ROOT / "drafts" / "ledger-ingestion" / "WAVE1-REPORT.md").read_text()
    assert "Five requests verified cleanly, four received a" in report
    assert "and 21 remain proposals" in report
    assert (
        "| `usaspending-usda-selected-rural-program-obligations.json` "
        "| Proposed |" in report
    )
    assert (
        "| `usaspending-usda-selected-rural-program-obligations.json` "
        "| Rejected |" not in report
    )


def test_dhs_post_body_refuses_malformed_or_duplicate_tas_components() -> None:
    malformed = copy.deepcopy(dhs_award_transaction_transform())
    malformed["treasuryAccountComponents"][0].pop("sub")
    with pytest.raises(
        ValueError,
        match="^registered USAspending TAS component is malformed$",
    ):
        resolve_pending.usaspending_fiscal_year_post_body("2026", malformed)

    duplicated = copy.deepcopy(dhs_award_transaction_transform())
    duplicated["treasuryAccountComponents"].append(
        copy.deepcopy(duplicated["treasuryAccountComponents"][0])
    )
    with pytest.raises(
        ValueError,
        match="^registered USAspending TAS plan repeats a component$",
    ):
        resolve_pending.usaspending_fiscal_year_post_body("2026", duplicated)


def test_dhs_fixture_is_hash_pinned_and_parses_the_verified_amount() -> None:
    fixture = (
        ROOT
        / "tests"
        / "fixtures"
        / "ingestion_wave1"
        / "usaspending"
        / "dhs-title-vi-fy2026.json"
    )
    raw = fixture.read_bytes()
    assert len(raw) == 1_146
    assert not raw.endswith(b"\n")
    assert hashlib.sha256(raw).hexdigest() == (
        "dd51e2eb947fc8b302fe9c33297c85989b542c933801dcb0729edf39ba157720"
    )
    payload = json.loads(raw)
    assert resolve_pending.usaspending_fiscal_year_amount(payload, "2026") == (
        32_171_899_636.26
    )


def test_usaspending_fetch_caps_each_network_request_at_20_seconds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: dict[str, object] = {}

    class Response:
        def __enter__(self) -> Response:
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return b'{"results":[]}'

    def fake_urlopen(request: object, timeout: int) -> Response:
        observed["request"] = request
        observed["timeout"] = timeout
        return Response()

    monkeypatch.setattr(resolve_pending.urllib.request, "urlopen", fake_urlopen)
    payload, raw, retrieved_at = resolve_pending.fetch_usaspending_json(
        "https://api.usaspending.gov/api/v2/search/spending_over_time/",
        {"group": "fiscal_year"},
    )
    assert observed["timeout"] == 20
    assert payload == {"results": []}
    assert raw == b'{"results":[]}'
    assert retrieved_at.endswith("Z")


def test_main_reads_usaspending_binding_from_real_registration_envelope(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    ref = (
        "usaspending.dod.prime_award_obligations.fy2026."
        "registered_query_snapshot"
    )
    registration = resolve_pending.registration_contracts()[ref]
    assert set(registration) == {"targetContentHash", "contract", "ledgerPin"}
    assert registration["contract"]["dataPointId"] == ref

    spec = resolve_pending.USASPENDING_ADAPTERS[
        "usaspending.dod.prime_award_obligations"
    ]
    forecast = {"resolutionDate": "2026-10-15", "unit": spec["unit"]}

    class FixedDate(dt.date):
        @classmethod
        def today(cls) -> FixedDate:
            return cls(2026, 10, 15)

    monkeypatch.setattr(resolve_pending.dt, "date", FixedDate)
    monkeypatch.setattr(
        resolve_pending,
        "load_thesis_log",
        lambda _url: {"entries": [], "resolutionLinks": []},
    )
    monkeypatch.setattr(resolve_pending, "pending_claims_refs", lambda _log: [])
    monkeypatch.setattr(
        resolve_pending,
        "pending_adapter_refs",
        lambda _log: [
            (
                ref,
                "usaspending",
                spec,
                "fiscal_year",
                "2026",
                "2026-10-15",
                forecast,
            )
        ],
    )
    monkeypatch.setattr(
        resolve_pending,
        "ledger_state",
        lambda *_args: ("", "blob", "a" * 40),
    )
    monkeypatch.setattr(
        resolve_pending,
        "registration_contracts",
        lambda: {ref: registration},
    )
    monkeypatch.setattr(
        resolve_pending,
        "utc_now",
        lambda: "2026-10-15T12:00:00Z",
    )

    requests: list[tuple[str, dict | None]] = []

    def fake_fetch(source_url: str, body: dict | None = None):
        requests.append((source_url, body))
        raw = b'{"obligations":250495914182.67}'
        return json.loads(raw), raw, "2026-10-15T12:00:00Z"

    monkeypatch.setattr(resolve_pending, "fetch_usaspending_json", fake_fetch)
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])

    assert resolve_pending.main() == 0
    output = capsys.readouterr().out
    assert requests == [
        (
            "https://api.usaspending.gov/api/v2/agency/097/awards/"
            "?fiscal_year=2026",
            None,
        )
    ]
    assert f"  resolve {ref} -> 250.5 billions USD" in output.splitlines()
    assert "dry-run: would append 1 row(s)" in output
    assert "NO REGISTERED SNAPSHOT WINDOW" not in output


def recipient_page(
    page: int,
    has_next: bool,
    identities: list[object],
) -> dict:
    return {
        "results": [{"recipient_id": identity} for identity in identities],
        "page_metadata": {"page": page, "hasNext": has_next},
    }


def test_distinct_recipient_count_deduplicates_across_complete_pages() -> None:
    pages = [
        recipient_page(1, True, ["A", "B", None]),
        recipient_page(2, False, ["B", "C"]),
    ]
    assert resolve_pending.usaspending_distinct_recipient_count(
        pages,
        recipient_transform(),
    ) == 3


def test_distinct_recipient_count_fails_closed_on_incomplete_or_bad_pages() -> None:
    valid = recipient_page(1, False, ["A"])
    invalid_page_sets = [
        [],
        [{"results": [], "page_metadata": {}}],
        [recipient_page(2, False, ["A"])],
        [recipient_page(True, False, ["A"])],
        [recipient_page(1, True, ["A"])],
        [
            recipient_page(1, False, ["A"]),
            recipient_page(2, False, ["B"]),
        ],
        [{**valid, "results": [{}]}],
        [{**valid, "results": [{"recipient_id": ""}]}],
        [{**valid, "results": [{"recipient_id": 123}]}],
    ]

    for pages in invalid_page_sets:
        assert (
            resolve_pending.usaspending_distinct_recipient_count(
                pages,
                recipient_transform(),
            )
            is None
        ), pages


def spending_payload(fiscal_year: object, amount: object) -> dict:
    return {
        "results": [
            {
                "time_period": {"fiscal_year": fiscal_year},
                "aggregated_amount": amount,
            }
        ]
    }


def test_fiscal_year_amount_requires_one_finite_matching_result() -> None:
    payload = {
        "results": [
            {
                "time_period": {"fiscal_year": 2025},
                "aggregated_amount": 999,
            },
            {
                "time_period": {"fiscal_year": 2026},
                "aggregated_amount": 80,
            },
        ]
    }
    assert resolve_pending.usaspending_fiscal_year_amount(payload, "2026") == 80
    assert (
        resolve_pending.usaspending_fiscal_year_amount(
            spending_payload(2025, 80),
            "2026",
        )
        is None
    )
    assert (
        resolve_pending.usaspending_fiscal_year_amount(
            {"results": payload["results"] + [payload["results"][1]]},
            "2026",
        )
        is None
    )
    assert (
        resolve_pending.usaspending_fiscal_year_amount(
            spending_payload(2026, True),
            "2026",
        )
        is None
    )
    assert (
        resolve_pending.usaspending_fiscal_year_amount(
            spending_payload(2026, float("inf")),
            "2026",
        )
        is None
    )


def test_fy_ratio_handles_zero_and_refuses_missing_or_impossible_amounts() -> None:
    ratio = resolve_pending.usaspending_ratio_percent
    denominator = spending_payload(2026, 80)

    assert ratio(spending_payload(2026, 20), denominator, "2026") == 25
    assert ratio(spending_payload(2026, 0), denominator, "2026") == 0
    assert (
        ratio(
            spending_payload(2026, 20),
            spending_payload(2026, 0),
            "2026",
        )
        is None
    )
    assert ratio(spending_payload(2025, 20), denominator, "2026") is None
    assert (
        ratio(
            spending_payload(2026, 20),
            spending_payload(2025, 80),
            "2026",
        )
        is None
    )
    assert ratio(spending_payload(2026, -1), denominator, "2026") is None
    assert ratio(spending_payload(2026, 81), denominator, "2026") is None


def test_snapshot_evidence_envelope_preserves_every_exchange_and_derivation() -> None:
    source_url = (
        "https://api.usaspending.gov/api/v2/search/spending_over_time/"
    )
    denominator, numerator = resolve_pending.usaspending_share_bodies(
        "2026",
        share_transform(),
    )
    denominator_raw = b'{ "results": [{"aggregated_amount": 80}] }\\n'
    numerator_raw = '{"message":"caf\u00e9","amount":20}\n'.encode()
    derived = {
        "operation": "ratio_percent",
        "fiscalYear": "2026",
        "numeratorObligations": 20,
        "denominatorObligations": 80,
        "percent": 25,
    }
    archived = resolve_pending.usaspending_snapshot_envelope(
        source_url,
        [
            (denominator, denominator_raw, "2026-10-15T12:00:00Z"),
            (numerator, numerator_raw, "2026-10-15T12:00:01Z"),
        ],
        derived,
    )
    evidence = json.loads(archived)

    assert archived.endswith(b"\n")
    assert canonical_bytes(evidence) + b"\n" == archived
    assert evidence["schemaVersion"] == (
        "usaspending_registered_query_snapshot_v1"
    )
    assert evidence["sourceUrl"] == source_url
    assert evidence["derived"] == derived
    assert [row["requestBody"] for row in evidence["exchanges"]] == [
        denominator,
        numerator,
    ]
    assert [row["retrievedAt"] for row in evidence["exchanges"]] == [
        "2026-10-15T12:00:00Z",
        "2026-10-15T12:00:01Z",
    ]
    assert [row["responseBodyUtf8"] for row in evidence["exchanges"]] == [
        denominator_raw.decode(),
        numerator_raw.decode(),
    ]
    assert [row["responseSha256"] for row in evidence["exchanges"]] == [
        hashlib.sha256(denominator_raw).hexdigest(),
        hashlib.sha256(numerator_raw).hexdigest(),
    ]
    assert {row["method"] for row in evidence["exchanges"]} == {"POST"}


def snapshot_target(window: dict | None) -> dict:
    target = {
        "series": "usaspending.dod.prime_award_obligations",
        "period": "FY2026",
        "catalogSlug": "us-dod-prime-award-obligations-fy2026",
        "targetUnit": "billions USD",
        "valueScale": 1e-9,
        "resolutionSourceUrl": (
            "https://api.usaspending.gov/api/v2/agency/097/awards/"
            "?fiscal_year={fiscal_year}"
        ),
        "sourceBinding": {
            "adapter": "usaspending-api",
            "releasePolicy": "registered_query_snapshot",
            "sourceUrl": (
                "https://api.usaspending.gov/api/v2/agency/097/awards/"
                "?fiscal_year={fiscal_year}"
            ),
            "sourceSeriesId": "usaspending.agency.097.awards.obligations",
            "field": "obligations",
            "table": "USAspending API v2, agency 097 (DoD) award summary",
            "transform": {"operation": "multiply", "factor": 1e-9},
        },
    }
    if window is not None:
        target["expectedReleaseWindow"] = window
    return target


def test_snapshot_registration_requires_an_explicit_window() -> None:
    registration_date = dt.date(2026, 7, 16)
    with pytest.raises(register_targets.RegistrationError, match="explicit"):
        register_targets.build_contract(snapshot_target(None), registration_date)

    contract = register_targets.build_contract(
        snapshot_target({"start": "2026-10-15", "end": "2026-10-22"}),
        registration_date,
    )
    binding = contract["sourceBinding"]
    assert binding["releasePolicy"] == "registered_query_snapshot"
    assert binding["expectedReleaseWindow"] == {
        "start": "2026-10-15",
        "end": "2026-10-22",
    }
    # Snapshot semantics are stamped into the id so graders and readers can
    # never mistake the outcome for a source first print.
    assert contract["dataPointId"] == (
        "usaspending.dod.prime_award_obligations.fy2026."
        "registered_query_snapshot"
    )


def test_parse_ref_period_handles_fiscal_year_snapshot_ids() -> None:
    parsed = resolve_pending.parse_ref_period(
        "usaspending.dod.prime_award_obligations.fy2026."
        "registered_query_snapshot",
        "usaspending.dod.prime_award_obligations",
    )
    assert parsed == ("fiscal_year", "2026")
    # Monthly and quarterly parsing is untouched.
    assert resolve_pending.parse_ref_period(
        "bea.pce_price_index.monthly_change.june_2026.first_print",
        "bea.pce_price_index.monthly_change",
    ) == ("month", "2026-06")


def test_extract_json_field_walks_paths_and_list_matches() -> None:
    payload = {
        "obligations": 250495914182.67,
        "results": [
            {"category": "grants", "aggregated_amount": 5814535628.2},
            {"category": "contracts", "aggregated_amount": 244049978285.78},
        ],
        "messages": ["informational"],
    }
    extract = resolve_pending.extract_json_field
    assert extract(payload, "obligations") == pytest.approx(250495914182.67)
    assert extract(
        payload, "results[category=contracts].aggregated_amount"
    ) == pytest.approx(244049978285.78)
    assert extract(payload, "results[category=loans].aggregated_amount") is None
    assert extract(payload, "missing") is None
    assert extract(payload, "messages") is None  # non-numeric leaf
    assert extract({"flag": True}, "flag") is None  # bools are not values


def test_snapshot_window_state_gates_by_date() -> None:
    state = resolve_pending.snapshot_window_state
    window = {"start": "2026-10-15", "end": "2026-10-22"}
    assert state(dt.date(2026, 10, 14), window) == "pending"
    assert state(dt.date(2026, 10, 15), window) == "open"
    assert state(dt.date(2026, 10, 22), window) == "open"
    assert state(dt.date(2026, 10, 23), window) == "missed"
    assert state(dt.date(2026, 10, 16), None) == "invalid"
    assert state(dt.date(2026, 10, 16), {"start": "2026-10-22"}) == "invalid"
    assert (
        state(dt.date(2026, 10, 16), {"start": "2026-10-22", "end": "2026-10-15"})
        == "invalid"
    )


def test_first_print_registration_flow_is_unchanged() -> None:
    target = snapshot_target(None)
    target["sourceBinding"]["releasePolicy"] = "first_print"
    target["expectedReleaseDate"] = "2026-10-15"
    contract = register_targets.build_contract(target, dt.date(2026, 7, 16))
    assert contract["dataPointId"].endswith(".first_print")
    assert contract["sourceBinding"]["releasePolicy"] == "first_print"


def test_append_gate_verdict_ignores_skipped_twins() -> None:
    verdict = resolve_pending.append_gate_verdict
    # The multi-event gate workflow leaves skipped twins on the same head;
    # they are non-verdicts, not failures (the 2026-07-18 outage tail).
    assert verdict(
        [{"conclusion": "success"}, {"conclusion": "skipped"}]
    ) is True
    assert verdict([{"conclusion": "success"}]) is True
    # A real adverse conclusion always refuses, whatever else passed.
    assert verdict(
        [{"conclusion": "success"}, {"conclusion": "failure"}]
    ) is False
    assert verdict(
        [{"conclusion": "skipped"}, {"conclusion": "cancelled"}]
    ) is False
    # All-skipped means the gate never judged the proposal: refuse.
    assert verdict([{"conclusion": "skipped"}]) is False
    assert verdict([]) is False


def test_every_registry_binding_template_conforms() -> None:
    # The 7-key rule holds registry-wide, not just for USAspending: any
    # template carrying derived keys could never authorize a binding.
    doc = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    checked = 0
    for entry in doc["series"]:
        binding = (entry.get("extras") or {}).get("sourceBinding")
        if binding is None:
            continue
        checked += 1
        assert set(binding) == SOURCE_BINDING_TEMPLATE_KEYS, entry["series"]
        assert binding["adapter"] in register_targets.SOURCE_ADAPTERS
        assert binding["releasePolicy"] in register_targets.RELEASE_POLICIES
    assert checked > 0
