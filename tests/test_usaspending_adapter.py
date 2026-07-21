from __future__ import annotations

import datetime as dt
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
    assert len(entries) == 4
    for entry in entries:
        binding = entry["extras"]["sourceBinding"]
        assert set(binding) == SOURCE_BINDING_TEMPLATE_KEYS, entry["series"]
        assert not (set(binding) & SOURCE_BINDING_DERIVED_KEYS)
        assert binding["adapter"] == "usaspending-api"
        assert binding["releasePolicy"] == "registered_query_snapshot"
        assert binding["sourceUrl"].startswith(
            "https://api.usaspending.gov/api/v2/"
        )
        # One template spans fiscal years: the query pins everything except
        # the year token the resolver substitutes from the target period.
        assert "{fiscal_year}" in binding["sourceUrl"]
        transform = binding["transform"]
        assert transform["operation"] == "multiply"
        assert 0 < float(transform["factor"]) <= 1


def test_each_template_has_a_matching_resolver_spec() -> None:
    for entry in apel_templates():
        spec = resolve_pending.USASPENDING_ADAPTERS[entry["series"]]
        binding = entry["extras"]["sourceBinding"]
        # The executor refuses on drift, so the committed template and the
        # resolver table must agree byte-for-byte on the query and field.
        assert spec["url_template"] == binding["sourceUrl"], entry["series"]
        assert spec["field"] == binding["field"], entry["series"]
        assert spec["series_id"] == binding["sourceSeriesId"], entry["series"]
        assert spec["scale"] == float(binding["transform"]["factor"])


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
