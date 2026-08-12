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

import prospect_targets  # noqa: E402
import register_targets  # noqa: E402
import resolve_pending  # noqa: E402
import roll_docket  # noqa: E402

SERIES = "bls.qcew.child_day_care_services.annual_avg_employment"
FIXTURE = (
    ROOT
    / "tests"
    / "fixtures"
    / "qcew"
    / "child_day_care_services_2025_annual.csv"
)
SPEC = resolve_pending.QCEW_ADAPTERS[SERIES]


def docket_entry() -> dict:
    docket = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    return next(row for row in docket["series"] if row["series"] == SERIES)


def _replace_once(raw: bytes, old: bytes, new: bytes) -> bytes:
    assert raw.count(old) == 1
    return raw.replace(old, new, 1)


def test_live_official_2025_fixture_selects_exact_annual_private_us_row() -> None:
    # Live official fetch on 2026-08-12; provenance, byte count, and endpoint
    # are committed beside the fixture in tests/fixtures/qcew/README.md.
    raw = FIXTURE.read_bytes()
    assert len(raw) == 537503
    assert hashlib.sha256(raw).hexdigest() == (
        "a4ebb81ec1159b1c3faa1670a32dc77598cf51178d9e17c630cb289ea568c3a9"
    )

    value, refusal = resolve_pending.qcew_value_from_csv(raw, SPEC, "2025")

    assert refusal is None
    assert value == 991735
    assert resolve_pending.qcew_api_url(SPEC, "2025") == (
        "https://data.bls.gov/cew/data/api/2025/a/industry/624410.csv"
    )
    assert resolve_pending.qcew_source_series_id(SPEC, "2025") == (
        "area_fips=US000;own_code=5;industry_code=624410;agglvl_code=18;"
        "size_code=0;qtr=A"
    )


@pytest.mark.parametrize(
    ("old", "new"),
    [
        (
            b'"US000","5","624410","18","0","2025","A"',
            b'"US000","3","624410","18","0","2025","A"',
        ),
        (
            b'"US000","5","624410","18","0","2025","A"',
            b'"01000","5","624410","18","0","2025","A"',
        ),
    ],
    ids=["wrong-ownership", "wrong-area"],
)
def test_annual_parser_refuses_wrong_selector_rows(old: bytes, new: bytes) -> None:
    raw = _replace_once(FIXTURE.read_bytes(), old, new)

    value, refusal = resolve_pending.qcew_value_from_csv(raw, SPEC, "2025")

    assert value is None
    assert refusal == "expected one exact QCEW row, found 0"


def test_annual_parser_refuses_missing_measure_field() -> None:
    raw = _replace_once(
        FIXTURE.read_bytes(),
        b'"annual_avg_emplvl"',
        b'"annual_avg_emplvX"',
    )

    value, refusal = resolve_pending.qcew_value_from_csv(raw, SPEC, "2025")

    assert value is None
    assert refusal == "QCEW CSV is missing required columns"


def test_annual_parser_refuses_truncated_row_even_with_terminal_newline() -> None:
    raw = FIXTURE.read_bytes()
    cutoff = raw.index(b",991735") + len(b",991735")
    truncated = raw[:cutoff] + b"\r\n"

    value, refusal = resolve_pending.qcew_value_from_csv(
        truncated, SPEC, "2025"
    )

    assert value is None
    assert refusal is not None
    assert "truncated or malformed response" in refusal


def test_annual_spec_and_docket_share_live_verified_anchors() -> None:
    entry = docket_entry()

    assert resolve_pending.qcew_adapter_verified(SPEC)
    assert SPEC["period_type"] == "year"
    assert SPEC["anchors"] == {"2023": 954796, "2024": 983412, "2025": 991735}
    assert entry["extras"]["anchors"] == SPEC["anchors"]
    assert entry["extras"]["country"] == "US"
    assert entry["extras"]["targetUnit"] == "count"
    assert entry["ledger"] == {
        "uuid": "c6c98b8b-55f6-4543-b057-96726c38a2bf",
        "concept": SERIES,
    }


def test_annual_target_maps_to_qcew_family() -> None:
    ref = f"{SERIES}.2025.first_print"
    log = {
        "entries": [
            {
                "kind": "prediction_recorded",
                "forecastSlug": "qcew-child-care-2025",
                "resolutionDate": "2026-06-02",
                "unit": "count",
            }
        ],
        "resolutionLinks": [
            {
                "status": "pending",
                "forecastSlug": "qcew-child-care-2025",
                "targetFactRef": ref,
            }
        ],
    }

    todo = resolve_pending.pending_adapter_refs(log)

    assert len(todo) == 1
    got_ref, kind, spec, period_type, period, release_date, _forecast = todo[0]
    assert got_ref == ref
    assert kind == "qcew"
    assert spec is SPEC
    assert (period_type, period, release_date) == (
        "year",
        "2025",
        "2026-06-02",
    )


def test_annual_release_seed_is_bound_to_the_official_q4_calendar_slot() -> None:
    entry = docket_entry()
    assert entry["releaseCalendarUrl"] == (
        "https://www.bls.gov/cew/release-calendar.htm"
    )
    assert entry["releaseDates"] == {"2025": "2026-06-02"}

    assert entry["period"] == entry["seedPeriod"] == "2026"
    # BLS has not dated Q4 2026. Replay the authenticated historical slot to
    # test exact release-date derivation without making it the live seed.
    historical = copy.deepcopy(entry)
    historical["period"] = historical["seedPeriod"] = "2025"
    target = roll_docket.recurring_seed_target(
        historical, set(), dt.date(2026, 6, 1)
    )
    assert target is not None
    assert target["period"] == "2025"
    assert target["expectedReleaseDate"] == "2026-06-02"
    contract = register_targets.build_contract(target, dt.date(2026, 6, 1))
    register_targets.validate_native_calendar_contract(
        contract, target, historical
    )

    binding = contract["sourceBinding"]
    assert binding["allowedHosts"] == ["data.bls.gov", "www.bls.gov"]
    assert binding["expectedReleaseWindow"] == {
        "start": "2026-06-02",
        "end": "2026-06-02",
    }
    assert resolve_pending.qcew_binding_matches_spec(
        binding, SPEC, "2025", dt.date(2026, 6, 2)
    )


def test_annual_release_seed_refuses_post_release_and_undated_next_year(
    capsys: pytest.CaptureFixture[str],
) -> None:
    entry = docket_entry()
    assert (
        roll_docket.recurring_seed_target(entry, set(), dt.date(2026, 8, 12))
        is None
    )
    assert "requires an explicit ISO releaseDates['2026']" in capsys.readouterr().err


def test_published_annual_seed_rolls_only_with_a_dated_successor() -> None:
    entry = docket_entry()
    entry["releaseDates"]["2026"] = "2027-06-02"
    published_slug = roll_docket.format_slug(entry["slug"], "2025", "annual")

    assert roll_docket.next_roll_period(
        entry, {published_slug}, {published_slug}, dt.date(2026, 12, 1)
    ) == ("2026", published_slug)
    extras = roll_docket.target_extras_for_period(entry, "2026")
    assert extras is not None
    target = {
        "series": SERIES,
        "period": "2026",
        "catalogSlug": roll_docket.format_slug(entry["slug"], "2026", "annual"),
        **extras,
    }
    contract = register_targets.build_contract(target, dt.date(2026, 12, 1))
    binding = contract["sourceBinding"]

    assert contract["dataPointId"] == f"{SERIES}.2026.first_print"
    assert resolve_pending.qcew_binding_matches_spec(
        binding, SPEC, "2026", dt.date(2027, 6, 2)
    )


def test_qcew_postfetch_gate_refuses_a_midnight_straddle() -> None:
    release_day = dt.date(2027, 6, 2)

    assert (
        resolve_pending.qcew_postfetch_window_refusal(
            "2027-06-02T23:59:59Z", release_day, "2027-06-02T23:59:59Z"
        )
        is None
    )
    assert resolve_pending.qcew_postfetch_window_refusal(
        "2027-06-03T00:00:01Z", release_day, "2027-06-03T00:00:01Z"
    ) == (
        "QCEW response completed on 2027-06-03, after registered release day "
        "2027-06-02"
    )


def test_annual_fact_sources_the_exact_fetched_csv() -> None:
    fetched_url = resolve_pending.qcew_api_url(SPEC, "2025")
    row = resolve_pending.generic_fact(
        f"{SERIES}.2025.first_print",
        SPEC,
        "year",
        "2025",
        991735,
        dt.date(2026, 6, 2),
        fetched_url,
        fetched_url,
    )

    assert row["source"]["url"] == fetched_url
    assert row["source"]["source_file"] == fetched_url
    assert row["measure"]["concept_evidence_url"] == fetched_url
    assert fetched_url in row["measure"]["concept_evidence_notes"]


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("adapter", "generic-url"),
        (
            "sourceSeriesId",
            "area_fips=US000;own_code=3;industry_code=624410;agglvl_code=18;"
            "size_code=0;qtr=A",
        ),
        ("field", "qtrly_estabs"),
        ("allowedHosts", ["www.bls.gov"]),
    ],
)
def test_annual_binding_refuses_any_registered_selector_drift(
    key: str, value: object
) -> None:
    entry = copy.deepcopy(docket_entry())
    entry["period"] = entry["seedPeriod"] = "2025"
    target = roll_docket.recurring_seed_target(entry, set(), dt.date(2026, 6, 1))
    assert target is not None
    binding = register_targets.build_contract(
        target, dt.date(2026, 6, 1)
    )["sourceBinding"]
    binding[key] = value

    assert not resolve_pending.qcew_binding_matches_spec(
        binding, SPEC, "2025", dt.date(2026, 6, 2)
    )


def test_annual_variant_is_consumed_by_registration_roll_and_prospect() -> None:
    assert "bls-qcew" in register_targets.SOURCE_ADAPTERS
    assert register_targets.SOURCE_ADAPTER_ALLOWED_HOSTS["bls-qcew"] == {
        "data.bls.gov",
        "www.bls.gov",
    }
    assert "bls-qcew" in register_targets.CALENDAR_GATED_SOURCE_ADAPTERS
    assert "bls-qcew" in roll_docket.OFFICIAL_CALENDAR_ADAPTERS
    assert prospect_targets._period_error("2025") is None
    assert prospect_targets._source_binding_errors(
        docket_entry()["extras"]["sourceBinding"]
    ) == []

    assert roll_docket.period_key("2025", "annual") == (2025,)
    assert roll_docket.step_period("2025", "annual") == "2026"
    assert (
        roll_docket.format_slug(
            "us-private-child-care-{year}", "2025", "annual"
        )
        == "us-private-child-care-2025"
    )
