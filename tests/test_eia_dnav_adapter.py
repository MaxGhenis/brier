"""EIA DNav annual-history adapter for natural-gas venting and flaring.

The fixtures are byte-for-byte official EIA responses fetched on 2026-08-13;
their retrieval metadata and hashes live beside them in
``tests/fixtures/eia_dnav/README.md``.  These tests keep the keyless DNav page
and its linked BIFF8 workbook one authenticated, archived resolution surface.
"""

from __future__ import annotations

import base64
import copy
import datetime as dt
import hashlib
import json
import pathlib
import struct
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import prospect_targets  # noqa: E402
import register_targets  # noqa: E402
import resolve_pending  # noqa: E402
import roll_docket  # noqa: E402
from adopt_proven_series import SOURCE_BINDING_TEMPLATE_KEYS  # noqa: E402

SERIES = "eia.ng.vented_flared.us.annual"
REF = f"{SERIES}.2025.first_print"
SPEC = resolve_pending.EIA_DNAV_ADAPTERS[SERIES]
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "eia_dnav"
PAGE = FIXTURE_ROOT / "n9040us2a.html"
WORKBOOK = FIXTURE_ROOT / "N9040US2a.xls"
FIXTURE_PINS = {
    "n9040us2a.html": (
        7_615,
        "00b6c41be70b9f52463fd4536344372e50dcf96b25b0b58078e989bbf6362e6a",
    ),
    "N9040US2a.xls": (
        31_232,
        "2097906a434f257678ed09ab34cb1a5bb6bd070b9430e0edfed3a32b738b3a92",
    ),
    "natural-gas-annual.html": (
        114_290,
        "1ca09dbac466614e868819999454d38f85c5699eea1e20a739c5d3f9976b022f",
    ),
    "natural-gas-annual-summary.html": (
        59_307,
        "19990844a4f4b1b961292eaed8e59e87e2a8b3b4d065db691eb1e74f23f9eb9a",
    ),
    "upcoming-reports.html": (
        75_148,
        "08abcd52aa620b33ab3170f95b964df9162438e9edf5a93021f8545e8f682e3c",
    ),
    "api-no-key.json": (
        163,
        "b71fb384d31b5e7ccc66d279785c9e6cd51fa51f07820a3363c849034b9608bd",
    ),
}


def docket_entry() -> dict:
    docket = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    return next(entry for entry in docket["series"] if entry["series"] == SERIES)


def registered_target(
    registration_date: dt.date = dt.date(2026, 8, 13),
) -> tuple[dict, dict]:
    entry = docket_entry()
    target = roll_docket.bounded_annual_first_print_seed_target(
        entry, set(), registration_date
    )
    assert target is not None
    return target, register_targets.build_contract(target, registration_date)


def _replace_nth(raw: bytes, old: bytes, new: bytes, occurrence: int = 0) -> bytes:
    assert len(old) == len(new)
    positions = []
    cursor = 0
    while True:
        cursor = raw.find(old, cursor)
        if cursor < 0:
            break
        positions.append(cursor)
        cursor += len(old)
    assert occurrence < len(positions), (old, positions)
    position = positions[occurrence]
    return raw[:position] + new + raw[position + len(old) :]


def _rk_double(value: float) -> bytes:
    """Return BIFF's four-byte RK spelling for an exactly representable value."""

    bits = struct.unpack("<Q", struct.pack("<d", value))[0]
    return struct.pack("<I", (bits >> 32) & 0xFFFFFFFC)


def capture_envelope(
    *, period: str = "2024", value: float = 335_163.0
) -> bytes:
    return resolve_pending.eia_dnav_capture_envelope(
        page_url=SPEC["source_url"],
        page_raw=PAGE.read_bytes(),
        page_retrieved_at="2026-08-13T18:53:10Z",
        workbook_url=SPEC["workbook_url"],
        workbook_raw=WORKBOOK.read_bytes(),
        workbook_retrieved_at="2026-08-13T18:53:11Z",
        period=period,
        value=value,
        source_series_id=SPEC["series_id"],
        unit=SPEC["unit"],
    )


@pytest.mark.parametrize("name", sorted(FIXTURE_PINS))
def test_official_fixture_bytes_match_reviewed_pins(name: str) -> None:
    raw = (FIXTURE_ROOT / name).read_bytes()
    expected_bytes, expected_sha256 = FIXTURE_PINS[name]

    assert len(raw) == expected_bytes
    assert hashlib.sha256(raw).hexdigest() == expected_sha256


def test_api_fixture_proves_the_official_route_is_not_keyless() -> None:
    payload = json.loads((FIXTURE_ROOT / "api-no-key.json").read_bytes())

    assert payload["error"]["code"] == "API_KEY_MISSING"


def test_real_workbook_authenticates_identity_and_exact_annual_anchors() -> None:
    values, refusal = resolve_pending.eia_dnav_values_from_xls(
        WORKBOOK.read_bytes(), SPEC
    )

    assert refusal is None
    assert values is not None
    assert values["2022"] == 271_682
    assert values["2023"] == 324_207
    assert values["2024"] == 335_163
    assert max(values) == "2024"
    assert resolve_pending.eia_dnav_verified_anchors(SPEC) == {
        "2022": 271_682.0,
        "2023": 324_207.0,
        "2024": 335_163.0,
    }
    assert resolve_pending.eia_dnav_anchor_mismatches(
        values, resolve_pending.eia_dnav_verified_anchors(SPEC) or {}
    ) == []


def test_official_annual_schedule_is_bound_to_the_n9040us2_series() -> None:
    annual = (FIXTURE_ROOT / "natural-gas-annual.html").read_text()
    summary = (FIXTURE_ROOT / "natural-gas-annual-summary.html").read_text()
    upcoming = (FIXTURE_ROOT / "upcoming-reports.html").read_text()

    assert "With Data for 2024" in annual
    assert "Next Release:</strong> October 2026" in annual
    assert 'href="/dnav/ng/ng_sum_lsum_dcu_nus_a.htm"' in annual
    assert "Vented and Flared" in summary
    assert 'href="./hist/n9040us2a.htm"' in summary
    assert "271,682" in summary
    assert "324,207" in summary
    assert "335,163" in summary
    october = upcoming.index("<h2>October 2026</h2>")
    november = upcoming.index("<h2>November 2026</h2>", october)
    assert "Natural Gas Annual" in upcoming[october:november]


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (
            lambda raw: _replace_nth(raw, b"Sourcekey", b"Sourcekez"),
            "expected 'Sourcekey'",
        ),
        (
            lambda raw: _replace_nth(raw, b"N9040US2", b"N9040US3"),
            "expected 'N9040US2'",
        ),
        (
            lambda raw: _replace_nth(raw, b"Date", b"Data", 2),
            "expected 'Date'",
        ),
        (
            lambda raw: _replace_nth(raw, b"Data 1", b"Data X"),
            "expected exact EIA sheet inventory",
        ),
        (
            lambda raw: _replace_nth(
                raw, b"Vented and Flared", b"Ventee and Flared"
            ),
            "workbook identity mismatch",
        ),
        (
            lambda raw: raw.replace(b"(MMcf)", b"(Mcf )"),
            "workbook identity mismatch",
        ),
        (
            lambda raw: _replace_nth(raw, b"Annual", b"Monthl"),
            "expected 'Annual'",
        ),
        (
            lambda raw: _replace_nth(
                raw, b"n9040us2a.xls", b"n9040us3a.xls"
            ),
            "expected 'n9040us2a.xls'",
        ),
    ],
    ids=[
        "wrong-sourcekey-header",
        "wrong-sourcekey",
        "wrong-date-header",
        "wrong-sheet",
        "wrong-title",
        "wrong-unit",
        "wrong-frequency",
        "wrong-filename",
    ],
)
def test_workbook_identity_drift_fails_closed(mutation, expected: str) -> None:
    values, refusal = resolve_pending.eia_dnav_values_from_xls(
        mutation(WORKBOOK.read_bytes()), SPEC
    )

    assert values is None
    assert refusal is not None
    assert expected in refusal


def test_workbook_parser_refuses_a_duplicate_annual_target_row() -> None:
    raw = WORKBOOK.read_bytes()
    # Turn the terminal 2024-06-30 row into a second 2023-06-30 row without
    # otherwise changing the official BIFF workbook.
    duplicate = _replace_nth(raw, _rk_double(45_473.0), _rk_double(45_107.0))

    values, refusal = resolve_pending.eia_dnav_values_from_xls(duplicate, SPEC)

    assert values is None
    assert refusal is not None
    assert "not contiguous" in refusal or "duplicate" in refusal


@pytest.mark.parametrize(
    ("replacement_date", "expected"),
    [
        (45_474.0, "is not dated June 30"),
        (45_838.0, "not contiguous at 2025"),
    ],
    ids=["wrong-period-day", "missing-2024-row"],
)
def test_workbook_parser_refuses_wrong_or_missing_annual_period(
    replacement_date: float, expected: str
) -> None:
    raw = _replace_nth(
        WORKBOOK.read_bytes(), _rk_double(45_473.0), _rk_double(replacement_date)
    )

    values, refusal = resolve_pending.eia_dnav_values_from_xls(raw, SPEC)

    assert values is None
    assert refusal is not None and expected in refusal


def test_workbook_parser_refuses_bad_bytes_and_invalid_anchor_declarations() -> None:
    values, refusal = resolve_pending.eia_dnav_values_from_xls(b"not an xls", SPEC)
    assert values is None
    assert refusal is not None and "workbook parse failed" in refusal

    assert (
        resolve_pending.eia_dnav_verified_anchors(
            {**SPEC, "anchor_status": "ANCHOR_TBV"}
        )
        is None
    )
    assert (
        resolve_pending.eia_dnav_verified_anchors(
            {**SPEC, "anchors": {"2023": 1, "2024": 2}}
        )
        is None
    )
    assert (
        resolve_pending.eia_dnav_verified_anchors(
            {**SPEC, "anchors": {**SPEC["anchors"], "2024": 1.5}}
        )
        is None
    )


def test_workbook_parser_refuses_truncated_leading_history() -> None:
    values, refusal = resolve_pending.eia_dnav_values_from_xls(
        WORKBOOK.read_bytes(), {**SPEC, "first_year": 1935}
    )

    assert values is None
    assert refusal == "EIA first annual row changed from 1935 to 1936"


def test_page_authenticates_the_exact_title_and_workbook_link() -> None:
    assert (
        resolve_pending.eia_dnav_workbook_link(PAGE.read_bytes(), SPEC)
        == SPEC["workbook_url"]
    )


@pytest.mark.parametrize(
    "html",
    [
        lambda raw: raw.replace(b"Million Cubic Feet", b"Thousand Cubic Feet"),
        lambda raw: raw.replace(b"../hist_xls/", b"../hist_csv/"),
        lambda raw: raw.replace(b"N9040US2a.xls", b"N9040US3a.xls"),
        lambda raw: raw.replace(
            b"</body>",
            b"<a href='../hist_xls/N9040US2a.xls'>duplicate</a></body>",
        ),
        lambda _raw: b"\xff\xfe\xfd",
    ],
    ids=["wrong-title", "wrong-path", "wrong-link", "duplicate-link", "bad-text"],
)
def test_page_identity_or_link_drift_fails_closed(html) -> None:
    assert resolve_pending.eia_dnav_workbook_link(html(PAGE.read_bytes()), SPEC) is None


def test_adapter_and_docket_share_an_exact_seven_key_binding() -> None:
    entry = docket_entry()
    template = entry["extras"]["sourceBinding"]
    target, contract = registered_target()
    binding = contract["sourceBinding"]

    assert "eia-dnav-xls" in register_targets.SOURCE_ADAPTERS
    assert prospect_targets._source_binding_errors(template) == []
    assert set(template) == SOURCE_BINDING_TEMPLATE_KEYS
    assert template == resolve_pending.eia_dnav_binding_template(SPEC)
    assert set(binding) == {
        *SOURCE_BINDING_TEMPLATE_KEYS,
        "allowedHosts",
        "expectedReleaseWindow",
    }
    assert binding["allowedHosts"] == ["www.eia.gov"]
    assert binding["expectedReleaseWindow"] == target["expectedReleaseWindow"]
    assert resolve_pending.eia_dnav_binding_matches_spec(binding, SPEC)


@pytest.mark.parametrize("key", sorted(SOURCE_BINDING_TEMPLATE_KEYS))
def test_binding_refuses_drift_in_every_template_key(key: str) -> None:
    _, contract = registered_target()
    binding = copy.deepcopy(contract["sourceBinding"])
    if key == "transform":
        binding[key]["factor"] = 2
    else:
        binding[key] = f"{binding[key]}-tampered"

    assert not resolve_pending.eia_dnav_binding_matches_spec(binding, SPEC)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("sourceUrl", "https://www.eia.gov/dnav/ng/hist/n9040us2m.htm"),
        ("sourceUrl", "https://www.eia.gov/dnav/ng/hist/n9040us2a.htm?x=1"),
        ("sourceUrl", "https://example.com/dnav/ng/hist/n9040us2a.htm"),
        ("allowedHosts", ["example.com"]),
        ("allowedHosts", ["www.eia.gov", "api.eia.gov"]),
        ("unexpected", True),
    ],
    ids=[
        "same-host-wrong-path",
        "same-path-query",
        "wrong-host",
        "host-substitution",
        "host-widening",
        "extra-key",
    ],
)
def test_binding_host_path_and_shape_are_fail_closed(key: str, value: object) -> None:
    _, contract = registered_target()
    binding = copy.deepcopy(contract["sourceBinding"])
    binding[key] = value

    assert not resolve_pending.eia_dnav_binding_matches_spec(binding, SPEC)


def test_live_docket_seed_rolls_to_the_exact_bounded_contract() -> None:
    entry = docket_entry()
    target, contract = registered_target(dt.date(2026, 8, 13))

    assert target == {
        "series": SERIES,
        "period": "2025",
        "seedPeriod": "2025",
        "catalogSlug": "us-natural-gas-vented-flared-2025",
        **entry["extras"],
    }
    assert contract == {
        "series": SERIES,
        "period": "2025",
        "catalogSlug": "us-natural-gas-vented-flared-2025",
        "dataPointId": REF,
        "country": "US",
        "unit": "million_cubic_feet",
        "valueScale": 1.0,
        "sourceBinding": {
            **entry["extras"]["sourceBinding"],
            "expectedReleaseWindow": {
                "start": "2026-10-01",
                "end": "2026-10-31",
            },
            "allowedHosts": ["www.eia.gov"],
        },
        "resolutionDateBasis": "resolve-by-bound",
        "resolutionDate": "2026-10-31",
        "seedPeriod": "2025",
    }
    assert target["anchors"] == SPEC["anchors"]
    register_targets.validate_native_calendar_contract(contract, target, entry)
    register_targets.require_seed_docket_template(
        contract,
        [entry],
        "2026-08-13T00:00:00Z",
        batch_target={
            **target,
            "country": contract["country"],
            "dataPointId": contract["dataPointId"],
        },
    )


def test_bounded_seed_stops_when_its_window_opens() -> None:
    entry = docket_entry()

    assert roll_docket.bounded_annual_first_print_seed_target(
        entry, set(), dt.date(2026, 9, 30)
    ) is not None
    assert (
        roll_docket.bounded_annual_first_print_seed_target(
            entry, set(), dt.date(2026, 10, 1)
        )
        is None
    )


def test_pending_reference_routes_to_the_eia_family() -> None:
    log = {
        "entries": [
            {
                "kind": "prediction_recorded",
                "forecastSlug": "eia-vented-flared-2025",
                "resolutionDate": "2026-10-31",
                "unit": "million_cubic_feet",
            }
        ],
        "resolutionLinks": [
            {
                "status": "pending",
                "forecastSlug": "eia-vented-flared-2025",
                "targetFactRef": REF,
            },
            {
                "status": "resolved",
                "forecastSlug": "eia-vented-flared-2025",
                "targetFactRef": REF,
            },
        ],
    }

    todo = resolve_pending.pending_adapter_refs(log)

    assert len(todo) == 1
    ref, kind, spec, period_type, period, release_date, forecast = todo[0]
    assert ref == REF
    assert kind == "eia_dnav"
    assert spec is SPEC
    assert (period_type, period, release_date) == (
        "year",
        "2025",
        "2026-10-31",
    )
    assert forecast["unit"] == SPEC["unit"]


def test_malformed_eia_period_does_not_route() -> None:
    log = {
        "entries": [
            {
                "kind": "prediction_recorded",
                "forecastSlug": "bad-period",
                "resolutionDate": "2026-10-31",
                "unit": SPEC["unit"],
            }
        ],
        "resolutionLinks": [
            {
                "status": "pending",
                "forecastSlug": "bad-period",
                "targetFactRef": f"{SERIES}.2025-Q4.first_print",
            }
        ],
    }

    assert resolve_pending.pending_adapter_refs(log) == []


def test_capture_envelope_binds_both_exact_artifacts_and_derived_value() -> None:
    raw = capture_envelope()
    envelope = json.loads(raw)
    page_raw = PAGE.read_bytes()
    workbook_raw = WORKBOOK.read_bytes()

    assert envelope["schemaVersion"] == resolve_pending.EIA_DNAV_ENVELOPE_SCHEMA
    assert envelope["page"] == {
        "url": SPEC["source_url"],
        "retrievedAt": "2026-08-13T18:53:10Z",
        "bytes": len(page_raw),
        "sha256": hashlib.sha256(page_raw).hexdigest(),
        "bodyBase64": base64.b64encode(page_raw).decode(),
    }
    assert envelope["workbook"] == {
        "url": SPEC["workbook_url"],
        "retrievedAt": "2026-08-13T18:53:11Z",
        "bytes": len(workbook_raw),
        "sha256": hashlib.sha256(workbook_raw).hexdigest(),
        "bodyBase64": base64.b64encode(workbook_raw).decode(),
    }
    assert envelope["derived"] == {
        "sourceSeriesId": "N9040US2",
        "period": "2024",
        "unit": "million_cubic_feet",
        "value": 335_163.0,
    }
    assert raw == resolve_pending.canonical_bytes(envelope)


def test_eia_http_get_timestamps_the_completed_response_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_http_get(url: str, *, allowed_hosts):
        assert url == SPEC["workbook_url"]
        assert allowed_hosts == SPEC["allowed_hosts"]
        return b"workbook bytes", "2026-10-31T23:59:58Z", url

    monkeypatch.setattr(resolve_pending, "http_get", fake_http_get)
    monkeypatch.setattr(
        resolve_pending, "utc_now", lambda: "2026-11-01T00:00:01Z"
    )

    assert resolve_pending.eia_dnav_http_get(
        SPEC["workbook_url"], allowed_hosts=SPEC["allowed_hosts"]
    ) == (
        b"workbook bytes",
        "2026-11-01T00:00:01Z",
        SPEC["workbook_url"],
    )


def test_fetch_authenticates_page_then_archives_the_linked_workbook(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    def fake_get(url: str, *, allowed_hosts) -> tuple[bytes, str, str]:
        assert allowed_hosts == SPEC["allowed_hosts"]
        calls.append(url)
        if url == SPEC["source_url"]:
            return PAGE.read_bytes(), "2026-08-13T18:53:10Z", url
        assert url == SPEC["workbook_url"]
        return WORKBOOK.read_bytes(), "2026-08-13T18:53:11Z", url

    monkeypatch.setattr(resolve_pending, "eia_dnav_http_get", fake_get)

    value, raw, fetched_url, retrieved_at, refusal = (
        resolve_pending.eia_dnav_fetch_year(SPEC, "2024")
    )

    assert calls == [SPEC["source_url"], SPEC["workbook_url"]]
    assert value == 335_163
    assert raw is not None
    assert json.loads(raw)["workbook"]["sha256"] == FIXTURE_PINS[
        "N9040US2a.xls"
    ][1]
    assert fetched_url == SPEC["workbook_url"]
    assert retrieved_at == "2026-08-13T18:53:11Z"
    assert refusal is None


def test_fetch_leaves_a_missing_target_year_pending_without_archiving(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_get(url: str, *, allowed_hosts) -> tuple[bytes, str, str]:
        assert allowed_hosts == SPEC["allowed_hosts"]
        raw = PAGE.read_bytes() if url == SPEC["source_url"] else WORKBOOK.read_bytes()
        return raw, "2026-08-13T18:53:10Z", url

    monkeypatch.setattr(resolve_pending, "eia_dnav_http_get", fake_get)

    value, raw, fetched_url, _retrieved_at, refusal = (
        resolve_pending.eia_dnav_fetch_year(SPEC, "2025")
    )

    assert value is None
    assert raw is None
    assert fetched_url == SPEC["workbook_url"]
    assert refusal is None


def test_fetch_rejects_a_non_year_period_without_network(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        resolve_pending,
        "eia_dnav_http_get",
        lambda *_args, **_kwargs: pytest.fail("invalid period reached the network"),
    )

    value, raw, fetched_url, _retrieved_at, refusal = (
        resolve_pending.eia_dnav_fetch_year(SPEC, "2025-Q4")
    )

    assert value is None and raw is None
    assert fetched_url == SPEC["source_url"]
    assert refusal == "period must be YYYY"


@pytest.mark.parametrize("redirect", ["page", "workbook"])
def test_fetch_refuses_same_host_nonexact_redirects(
    monkeypatch: pytest.MonkeyPatch, redirect: str
) -> None:
    def fake_get(url: str, *, allowed_hosts) -> tuple[bytes, str, str]:
        assert allowed_hosts == SPEC["allowed_hosts"]
        if url == SPEC["source_url"]:
            final = f"{url}?download=1" if redirect == "page" else url
            return PAGE.read_bytes(), "2026-08-13T18:53:10Z", final
        final = f"{url}?download=1" if redirect == "workbook" else url
        return WORKBOOK.read_bytes(), "2026-08-13T18:53:11Z", final

    monkeypatch.setattr(resolve_pending, "eia_dnav_http_get", fake_get)

    value, _raw, _fetched_url, _retrieved_at, refusal = (
        resolve_pending.eia_dnav_fetch_year(SPEC, "2024")
    )

    assert value is None
    assert refusal is not None and "redirected away" in refusal


def test_fetch_does_not_request_a_workbook_from_an_unauthenticated_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def fake_get(url: str, *, allowed_hosts) -> tuple[bytes, str, str]:
        nonlocal calls
        assert allowed_hosts == SPEC["allowed_hosts"]
        calls += 1
        return b"<html>wrong page</html>", "2026-08-13T18:53:10Z", url

    monkeypatch.setattr(resolve_pending, "eia_dnav_http_get", fake_get)

    value, _raw, _fetched_url, _retrieved_at, refusal = (
        resolve_pending.eia_dnav_fetch_year(SPEC, "2024")
    )

    assert calls == 1
    assert value is None
    assert refusal == (
        "EIA DNav page did not authenticate the exact N9040US2 XLS sibling"
    )


@pytest.mark.parametrize(
    ("day", "state", "message"),
    [
        (
            dt.date(2026, 9, 30),
            "pending",
            f"  RELEASE WINDOW NOT OPEN (deferring): {REF} — opens 2026-10-01",
        ),
        (dt.date(2026, 10, 1), "open", None),
        (dt.date(2026, 10, 31), "open", None),
        (
            dt.date(2026, 11, 1),
            "missed",
            f"  FIRST-PRINT WINDOW MISSED (refusing): {REF} — registered window "
            "closed 2026-10-31; no release-time witnessed or versioned "
            "first-print custody is registered",
        ),
    ],
)
def test_bounded_window_pre_open_and_post_verdicts(
    day: dt.date, state: str, message: str | None
) -> None:
    assert resolve_pending.bounded_resolution_window_gate(
        REF,
        day,
        {"start": "2026-10-01", "end": "2026-10-31"},
    ) == (state, message)


def _run_main(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    *,
    now,
    fetch,
    spec: dict | None = None,
    contract_mutation=None,
) -> str:
    active_spec = spec or SPEC
    _, contract = registered_target()
    if contract_mutation is not None:
        contract_mutation(contract)
    registration = {
        "targetContentHash": "a" * 64,
        "contract": contract,
        "ledgerPin": None,
    }
    forecast = {"resolutionDate": "2026-10-31", "unit": SPEC["unit"]}
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
                REF,
                "eia_dnav",
                active_spec,
                "year",
                "2025",
                "2026-10-31",
                forecast,
            )
        ],
    )
    monkeypatch.setattr(
        resolve_pending, "ledger_state", lambda *_args: ("", "blob", "b" * 40)
    )
    monkeypatch.setattr(
        resolve_pending, "registration_contracts", lambda: {REF: registration}
    )
    monkeypatch.setattr(
        resolve_pending, "utc_now", now if callable(now) else lambda: now
    )
    monkeypatch.setattr(resolve_pending, "eia_dnav_fetch_year", fetch)
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])

    assert resolve_pending.main() == 0
    return capsys.readouterr().out


@pytest.mark.parametrize(
    ("now", "expected"),
    [
        (
            "2026-09-30T23:59:59Z",
            f"RELEASE WINDOW NOT OPEN (deferring): {REF}",
        ),
        (
            "2026-11-01T00:00:00Z",
            f"FIRST-PRINT WINDOW MISSED (refusing): {REF}",
        ),
    ],
)
def test_resolver_defers_or_refuses_without_fetching_outside_window(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    now: str,
    expected: str,
) -> None:
    def unexpected_fetch(*_args, **_kwargs):
        raise AssertionError("EIA fetch ran outside the registered window")

    output = _run_main(
        monkeypatch, capsys, now=now, fetch=unexpected_fetch
    )

    assert expected in output
    assert f"resolve {REF}" not in output
    assert "nothing new to record" in output


def test_resolver_open_window_reparses_envelope_checks_anchors_and_resolves(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    real_parser = resolve_pending.eia_dnav_values_from_xls

    def future_parser(raw: bytes, spec: dict):
        values, refusal = real_parser(raw, spec)
        assert refusal is None and values is not None
        return {**values, "2025": 335_163.0}, None

    monkeypatch.setattr(resolve_pending, "eia_dnav_values_from_xls", future_parser)

    def fake_fetch(spec: dict, year: str):
        assert spec is SPEC
        assert year == "2025"
        return (
            335_163.0,
            capture_envelope(period="2025", value=335_163.0),
            SPEC["workbook_url"],
            "2026-10-15T12:00:00Z",
            None,
        )

    output = _run_main(
        monkeypatch,
        capsys,
        now="2026-10-15T12:00:01Z",
        fetch=fake_fetch,
    )

    assert f"resolve {REF} -> 335163.0 million_cubic_feet" in output
    assert "dry-run: would append 1 row(s)" in output


def test_resolver_refuses_a_capture_that_crosses_the_window_end(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    moments = iter(["2026-10-31T23:59:59Z", "2026-11-01T00:00:01Z"])
    fetches: list[str] = []

    def fake_fetch(_spec: dict, year: str):
        fetches.append(year)
        return (
            335_163.0,
            capture_envelope(period="2025", value=335_163.0),
            SPEC["workbook_url"],
            "2026-10-31T23:59:59Z",
            None,
        )

    output = _run_main(
        monkeypatch,
        capsys,
        now=lambda: next(moments, "2026-11-01T00:00:01Z"),
        fetch=fake_fetch,
    )

    assert fetches == ["2025"]
    assert f"FIRST-PRINT WINDOW MISSED (refusing): {REF}" in output
    assert f"resolve {REF}" not in output


def test_resolver_refuses_binding_drift_before_fetch(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def mutate(contract: dict) -> None:
        contract["sourceBinding"]["sourceSeriesId"] = "N9040US3"

    def unexpected_fetch(*_args, **_kwargs):
        raise AssertionError("EIA fetch ran before binding authentication")

    output = _run_main(
        monkeypatch,
        capsys,
        now="2026-10-15T12:00:00Z",
        fetch=unexpected_fetch,
        contract_mutation=mutate,
    )

    assert "BINDING/ADAPTER MISMATCH" in output
    assert f"resolve {REF}" not in output


def test_resolver_refuses_anchor_mismatch_in_the_archived_workbook(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    drifted_spec = {**SPEC, "anchors": {**SPEC["anchors"], "2024": 1}}

    def fake_fetch(_spec: dict, _year: str):
        return (
            335_163.0,
            capture_envelope(period="2025", value=335_163.0),
            SPEC["workbook_url"],
            "2026-10-15T12:00:00Z",
            None,
        )

    output = _run_main(
        monkeypatch,
        capsys,
        now="2026-10-15T12:00:01Z",
        fetch=fake_fetch,
        spec=drifted_spec,
    )

    assert "ANCHOR MISMATCH (refusing, wrong EIA series?)" in output
    assert "2024=335163.0 (official 1.0)" in output
    assert f"resolve {REF}" not in output


def test_eia_fact_projects_onto_the_registered_source_binding() -> None:
    _, contract = registered_target()
    raw = capture_envelope(period="2025", value=335_163.0)
    row = resolve_pending.generic_fact(
        REF,
        SPEC,
        "year",
        "2025",
        335_163.0,
        dt.date(2026, 10, 15),
        SPEC["source_url"],
        SPEC["workbook_url"],
    )
    registration = {
        "targetContentHash": "a" * 64,
        "contract": contract,
        "ledgerPin": None,
    }

    projection = resolve_pending.source_binding_projection(registration, row, raw)

    assert row["measure"]["concept"] == SERIES
    assert row["measure"]["unit"] == "million_cubic_feet"
    assert row["source"]["source_file"] == SPEC["workbook_url"]
    assert row["source_row_keys"] == ["2025"]
    assert row["source_cell_keys"] == ["N9040US2"]
    assert projection == {
        "series": SERIES,
        "concept": SERIES,
        "period": "2025",
        "releasePolicy": "first_print",
        "table": SPEC["source_table"],
        "field": "annual_value_mmcf",
        "transform": {"operation": "identity", "factor": 1},
        "unit": "million_cubic_feet",
        "sourceUrl": SPEC["source_url"],
        "responseSha256": hashlib.sha256(raw).hexdigest(),
    }

    wrong_host = copy.deepcopy(row)
    wrong_host["source"]["url"] = "https://example.com/n9040us2a.htm"
    with pytest.raises(ValueError, match="not in the registered allowedHosts"):
        resolve_pending.source_binding_projection(registration, wrong_host, raw)
