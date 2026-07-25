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
    assert set(registry) == set(specs) == APEL_SERIES

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
