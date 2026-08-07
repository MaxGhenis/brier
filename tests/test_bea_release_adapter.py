from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import sys
from typing import Any

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import prospect_targets  # noqa: E402
import register_targets  # noqa: E402
import resolve_pending  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "ingestion_wave1" / "bea"
RELEASE_DAY = dt.date(2026, 7, 30)


def _docket_entry(series: str) -> dict[str, Any]:
    docket = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    return next(row for row in docket["series"] if row["series"] == series)


def _registration(
    series: str,
) -> tuple[str, dict[str, Any], dict[str, Any], dict[str, Any]]:
    entry = _docket_entry(series)
    target = {
        **entry["extras"],
        "series": series,
        "period": "2026-Q2",
        "catalogSlug": f"unit4-{series.replace('.', '-')}",
        "releaseCalendarUrl": entry["releaseCalendarUrl"],
        "expectedReleaseDate": RELEASE_DAY.isoformat(),
    }
    contract = register_targets.build_contract(target, dt.date(2026, 7, 1))
    ref = contract["dataPointId"]
    envelope = {
        "targetContentHash": "a" * 64,
        "contract": contract,
        "ledgerPin": None,
    }
    spec = resolve_pending.BEA_RELEASE_ADAPTERS[series]
    forecast = {
        "resolutionDate": RELEASE_DAY.isoformat(),
        "unit": spec["unit"],
    }
    return ref, envelope, spec, forecast


def test_real_bea_current_release_fixtures_are_hash_pinned_and_parse() -> None:
    release_raw = (FIXTURES / "gdp-advance-2026-q2.html").read_bytes()
    table_raw = (FIXTURES / "nipa-table-5-3-5-2026-q2.json").read_bytes()

    assert len(release_raw) == 52_640
    assert hashlib.sha256(release_raw).hexdigest() == (
        "4636dc341d7cd1a53196fdf0ad529143b0e8b2d0db874f6086ca9b8ebf23cf5d"
    )
    assert len(table_raw) == 46_905
    assert hashlib.sha256(table_raw).hexdigest() == (
        "59e5f1ab0eeaa76cdca566383c66eab7787214216ffcbe35aa4c1793a894750d"
    )
    assert (
        resolve_pending.bea_release_page_refusal(release_raw, "2026-04", RELEASE_DAY)
        is None
    )

    pnfi = resolve_pending.BEA_RELEASE_ADAPTERS[
        "bea.private_nonresidential_fixed_investment"
    ]
    research = resolve_pending.BEA_RELEASE_ADAPTERS[
        "bea.research_and_development_fixed_investment"
    ]
    assert resolve_pending.bea_itable_value(
        table_raw, pnfi, "2026-04", RELEASE_DAY
    ) == (4623.657, None)
    assert resolve_pending.bea_itable_value(
        table_raw, research, "2026-04", RELEASE_DAY
    ) == (937.772, None)


def test_bea_table_revision_stamp_must_equal_registered_release_day() -> None:
    raw = (FIXTURES / "nipa-table-5-3-5-2026-q2.json").read_bytes()
    response = json.loads(raw)
    # The raw fixture is the live double-encoded body: a JSON string
    # wrapping the response object. Unwrap it the way the parser does.
    if isinstance(response, str):
        response = json.loads(response)
    table_prompt = next(
        prompt for prompt in response["Prompts"] if prompt["Name"] == "TheTable"
    )
    prompt_data = json.loads(table_prompt["PromtData"])
    table = json.loads(prompt_data["Table"])
    table["Description"] = (
        "Last Revised on: August 26, 2026 - Next Release Date September 30, 2026"
    )
    prompt_data["Table"] = json.dumps(table, separators=(",", ":"))
    table_prompt["PromtData"] = json.dumps(prompt_data, separators=(",", ":"))
    mutated = json.dumps(response, separators=(",", ":")).encode()
    spec = resolve_pending.BEA_RELEASE_ADAPTERS[
        "bea.private_nonresidential_fixed_investment"
    ]

    value, refusal = resolve_pending.bea_itable_value(
        mutated, spec, "2026-04", RELEASE_DAY
    )

    assert value is None
    assert refusal == (
        "iTable revision stamp 'Last Revised on: August 26, 2026 - Next "
        "Release Date September 30, 2026' does not start with registered "
        "release stamp 'Last Revised on: July 30, 2026'"
    )


@pytest.mark.parametrize(
    ("series", "series_id", "field"),
    [
        (
            "bea.private_nonresidential_fixed_investment",
            "T50305:L2",
            "Line 2: Nonresidential",
        ),
        (
            "bea.research_and_development_fixed_investment",
            "T50305:L18",
            "Line 18: Research and development",
        ),
    ],
)
def test_bea_registry_binds_official_release_parser_and_keeps_alfred_as_mirror(
    series: str, series_id: str, field: str
) -> None:
    _ref, registration, spec, _forecast = _registration(series)
    binding = registration["contract"]["sourceBinding"]

    assert binding["adapter"] == "bea-release"
    assert binding["sourceUrl"] == resolve_pending.BEA_ITABLE_PAGE_URL
    assert binding["sourceSeriesId"] == series_id
    assert binding["field"] == field
    assert binding["transform"] == {"operation": "multiply", "factor": 0.001}
    assert binding["releasePolicy"] == "first_print"
    assert binding["expectedReleaseWindow"] == {
        "start": RELEASE_DAY.isoformat(),
        "end": RELEASE_DAY.isoformat(),
    }
    assert binding["allowedHosts"] == ["apps.bea.gov", "www.bea.gov"]
    assert resolve_pending.bea_release_binding_matches_spec(binding, spec)
    widened = {**binding, "allowedHosts": [*binding["allowedHosts"], "evil.example"]}
    duplicated = {
        **binding,
        "allowedHosts": [*binding["allowedHosts"], "www.bea.gov"],
    }
    assert not resolve_pending.bea_release_binding_matches_spec(widened, spec)
    assert not resolve_pending.bea_release_binding_matches_spec(duplicated, spec)
    assert (
        prospect_targets._source_binding_errors(
            resolve_pending.bea_release_binding_template(spec)
        )
        == []
    )
    assert spec["history_mirror"]["adapter"] == "alfred-fred"
    assert series in resolve_pending.ALFRED_HISTORY_MIRRORS
    assert series not in resolve_pending.ALFRED_ADAPTERS
    assert register_targets.is_calendar_gated_source("bea-release", series)


def test_pending_bea_series_route_only_to_official_release_family() -> None:
    registrations = [
        _registration("bea.private_nonresidential_fixed_investment"),
        _registration("bea.research_and_development_fixed_investment"),
    ]
    entries = []
    links = []
    for index, (ref, _registration_envelope, spec, forecast) in enumerate(
        registrations
    ):
        slug = f"bea-release-{index}"
        entries.append(
            {
                "kind": "prediction_recorded",
                "forecastSlug": slug,
                **forecast,
            }
        )
        links.append(
            {
                "status": "pending",
                "forecastSlug": slug,
                "targetFactRef": ref,
            }
        )

    routed = resolve_pending.pending_adapter_refs(
        {"entries": entries, "resolutionLinks": links}
    )

    assert len(routed) == 2
    assert {row[1] for row in routed} == {"bea_release"}
    assert {row[3:5] for row in routed} == {("quarter", "2026-04")}
    assert {row[2]["series_id"] for row in routed} == {
        "T50305:L2",
        "T50305:L18",
    }


def test_main_resolves_both_bea_series_from_real_official_fixtures(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    registrations = [
        _registration("bea.private_nonresidential_fixed_investment"),
        _registration("bea.research_and_development_fixed_investment"),
    ]
    contracts = {ref: envelope for ref, envelope, _spec, _forecast in registrations}
    entries = []
    links = []
    for index, (ref, _envelope, _spec, forecast) in enumerate(registrations):
        slug = f"bea-release-main-{index}"
        entries.append(
            {
                "kind": "prediction_recorded",
                "forecastSlug": slug,
                **forecast,
            }
        )
        links.append(
            {
                "status": "pending",
                "forecastSlug": slug,
                "targetFactRef": ref,
            }
        )
    log = {"entries": entries, "resolutionLinks": links}
    release_raw = (FIXTURES / "gdp-advance-2026-q2.html").read_bytes()
    table_raw = (FIXTURES / "nipa-table-5-3-5-2026-q2.json").read_bytes()
    calls = {"release": 0, "table": 0}

    class FixedDate(dt.date):
        @classmethod
        def today(cls) -> FixedDate:
            return cls(2026, 7, 30)

    expected_release_url = resolve_pending.bea_advance_release_url(
        "2026-04", RELEASE_DAY
    )
    expected_table_body = resolve_pending.bea_itable_request_body(
        registrations[0][2], "2026-04"
    )

    def fake_http_request(
        request: Any,
        *,
        allowed_hosts: list[str] | tuple[str, ...],
        timeout: int = 120,
    ) -> tuple[bytes, str, str]:
        assert tuple(allowed_hosts) == ("apps.bea.gov", "www.bea.gov")
        assert timeout == 120
        if request.full_url == expected_release_url:
            calls["release"] += 1
            assert request.get_method() == "GET"
            assert request.data is None
            return release_raw, "2026-07-30T12:30:01Z", expected_release_url
        assert request.full_url == resolve_pending.BEA_ITABLE_DATA_URL
        calls["table"] += 1
        assert request.get_method() == "POST"
        assert json.loads(request.data) == expected_table_body
        assert request.get_header("Content-type") == "application/json"
        return (
            table_raw,
            "2026-07-30T12:30:02Z",
            resolve_pending.BEA_ITABLE_DATA_URL,
        )

    monkeypatch.setattr(resolve_pending.dt, "date", FixedDate)
    monkeypatch.setattr(resolve_pending, "utc_now", lambda: "2026-07-30T12:30:03Z")
    monkeypatch.setattr(resolve_pending, "load_thesis_log", lambda _url: log)
    monkeypatch.setattr(
        resolve_pending, "ledger_state", lambda *_args: ("", "blob", "b" * 40)
    )
    monkeypatch.setattr(resolve_pending, "registration_contracts", lambda: contracts)
    monkeypatch.setattr(resolve_pending, "http_request", fake_http_request)
    monkeypatch.setattr(
        resolve_pending,
        "fred_vintage_series",
        lambda *_args: pytest.fail("BEA resolution must not call ALFRED"),
    )
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])

    assert resolve_pending.main() == 0

    output = capsys.readouterr().out
    assert "-> 4623.657 usd_billions" in output
    assert "-> 937.772 usd_billions" in output
    assert "dry-run: would append 2 row(s)" in output
    assert calls == {"release": 1, "table": 1}


def test_main_refuses_bea_current_table_after_registered_release_day_literal(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    ref, envelope, _spec, forecast = _registration(
        "bea.private_nonresidential_fixed_investment"
    )
    log = {
        "entries": [
            {
                "kind": "prediction_recorded",
                "forecastSlug": "late-bea-release",
                **forecast,
            }
        ],
        "resolutionLinks": [
            {
                "status": "pending",
                "forecastSlug": "late-bea-release",
                "targetFactRef": ref,
            }
        ],
    }

    class FixedDate(dt.date):
        @classmethod
        def today(cls) -> FixedDate:
            return cls(2026, 7, 31)

    monkeypatch.setattr(resolve_pending.dt, "date", FixedDate)
    monkeypatch.setattr(resolve_pending, "utc_now", lambda: "2026-07-31T00:00:00Z")
    monkeypatch.setattr(resolve_pending, "load_thesis_log", lambda _url: log)
    monkeypatch.setattr(
        resolve_pending, "ledger_state", lambda *_args: ("", "blob", "b" * 40)
    )
    monkeypatch.setattr(
        resolve_pending, "registration_contracts", lambda: {ref: envelope}
    )
    monkeypatch.setattr(
        resolve_pending,
        "fetch_bea_release_page",
        lambda *_args: pytest.fail("late capture must fail before any fetch"),
    )
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])

    assert resolve_pending.main() == 0

    output = capsys.readouterr().out
    assert (
        f"  FIRST-PRINT WINDOW MISSED (refusing): {ref} — "
        "registered release day was 2026-07-30"
    ) in output
    assert "nothing new to record" in output


def test_main_refuses_bea_fetch_that_crosses_utc_window_end_literal(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    ref, envelope, _spec, forecast = _registration(
        "bea.private_nonresidential_fixed_investment"
    )
    log = {
        "entries": [
            {
                "kind": "prediction_recorded",
                "forecastSlug": "straddled-bea-release",
                **forecast,
            }
        ],
        "resolutionLinks": [
            {
                "status": "pending",
                "forecastSlug": "straddled-bea-release",
                "targetFactRef": ref,
            }
        ],
    }
    release_raw = (FIXTURES / "gdp-advance-2026-q2.html").read_bytes()
    table_raw = (FIXTURES / "nipa-table-5-3-5-2026-q2.json").read_bytes()

    class FixedDate(dt.date):
        @classmethod
        def today(cls) -> FixedDate:
            return cls(2026, 7, 30)

    monkeypatch.setattr(resolve_pending.dt, "date", FixedDate)
    monkeypatch.setattr(resolve_pending, "utc_now", lambda: "2026-07-30T23:59:58Z")
    monkeypatch.setattr(resolve_pending, "load_thesis_log", lambda _url: log)
    monkeypatch.setattr(
        resolve_pending, "ledger_state", lambda *_args: ("", "blob", "b" * 40)
    )
    monkeypatch.setattr(
        resolve_pending, "registration_contracts", lambda: {ref: envelope}
    )
    monkeypatch.setattr(
        resolve_pending,
        "fetch_bea_release_page",
        lambda period, day: (
            release_raw,
            resolve_pending.bea_advance_release_url(period, day),
            "2026-07-30T23:59:59Z",
        ),
    )
    monkeypatch.setattr(
        resolve_pending,
        "fetch_bea_itable_table",
        lambda adapter, period: (
            table_raw,
            resolve_pending.BEA_ITABLE_DATA_URL,
            resolve_pending.bea_itable_request_body(adapter, period),
            "2026-07-31T00:00:01Z",
        ),
    )
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])

    assert resolve_pending.main() == 0

    output = capsys.readouterr().out
    assert (
        f"  FIRST-PRINT WINDOW MISSED (refusing): {ref} — capture completed "
        "2026-07-31 after registered release day 2026-07-30"
    ) in output
    assert "nothing new to record" in output
