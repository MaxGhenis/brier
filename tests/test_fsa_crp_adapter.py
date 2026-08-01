from __future__ import annotations

import copy
import json
import pathlib
import subprocess
import sys
from types import SimpleNamespace

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import prospect_targets  # noqa: E402
import register_targets  # noqa: E402
import resolve_pending  # noqa: E402
from adopt_proven_series import SOURCE_BINDING_TEMPLATE_KEYS  # noqa: E402

SERIES = "usda.fsa.crp.enrolled_acres_total"
SPEC = resolve_pending.FSA_CRP_ADAPTERS[SERIES]
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "fsa_crp"


def test_fsa_crp_adapter_and_docket_share_the_exact_seven_key_binding() -> None:
    docket = json.loads(
        (ROOT / "scripts" / "docket_series.json").read_text()
    )
    entry = next(
        e for e in docket["series"] if e["series"] == SERIES
    )
    binding = entry["extras"]["sourceBinding"]

    assert "fsa-crp-monthly-summary" in register_targets.SOURCE_ADAPTERS
    assert prospect_targets._source_binding_errors(binding) == []
    assert set(binding) == SOURCE_BINDING_TEMPLATE_KEYS
    assert resolve_pending.fsa_crp_binding_template(SPEC) == binding
    assert resolve_pending.fsa_crp_binding_matches_spec(binding, SPEC)
    assert resolve_pending.fsa_crp_binding_matches_spec(
        {
            **binding,
            "allowedHosts": ["www.fsa.usda.gov"],
            "expectedReleaseWindow": {
                "start": "2026-07-01",
                "end": "2026-07-31",
            },
        },
        SPEC,
    )

    for key in SOURCE_BINDING_TEMPLATE_KEYS:
        tampered = copy.deepcopy(binding)
        if key == "transform":
            tampered[key]["factor"] = 2
        else:
            tampered[key] = f"{tampered[key]}-tampered"
        assert not resolve_pending.fsa_crp_binding_matches_spec(tampered, SPEC)
    assert not resolve_pending.fsa_crp_binding_matches_spec(
        {**binding, "unexpected": True}, SPEC
    )
    assert not resolve_pending.fsa_crp_binding_matches_spec(
        {**binding, "allowedHosts": ["example.com"]}, SPEC
    )


def test_fsa_crp_landing_page_selects_one_target_month_pdf() -> None:
    landing = b"""
    <html><body>
      <a href="/docs/crp-monthly-summary-may-2026.pdf">
        CRP Monthly Summary May 2026
      </a>
      <a href="/docs/crp-monthly-summary-june-2026.pdf">
        <span>CRP Monthly Summary</span> June 2026
      </a>
      <a href="/docs/crp-monthly-summary-june-2026.pdf">
        CRP Monthly Summary June 2026 duplicate navigation link
      </a>
      <a href="/docs/crp-monthly-summary-june-2026.xlsx">
        CRP Monthly Summary June 2026 spreadsheet
      </a>
    </body></html>
    """

    url, refusal = resolve_pending.fsa_crp_summary_pdf_url(
        landing,
        "2026-06",
        landing_url=SPEC["source_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )

    assert refusal is None
    assert url == "https://www.fsa.usda.gov/docs/crp-monthly-summary-june-2026.pdf"


def test_fsa_crp_landing_page_selection_fails_closed() -> None:
    ambiguous = b"""
    <a href="/docs/crp-monthly-summary-june-2026.pdf">
      CRP Monthly Summary June 2026
    </a>
    <a href="/archive/crp-monthly-summary-june-2026.pdf">
      CRP Monthly Summary June 2026
    </a>
    """
    url, refusal = resolve_pending.fsa_crp_summary_pdf_url(
        ambiguous,
        "2026-06",
        landing_url=SPEC["source_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert url is None and "found 2" in refusal

    off_host = b"""
    <a href="https://example.com/crp-monthly-summary-june-2026.pdf">
      CRP Monthly Summary June 2026
    </a>
    """
    url, refusal = resolve_pending.fsa_crp_summary_pdf_url(
        off_host,
        "2026-06",
        landing_url=SPEC["source_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert url is None and "not in adapter allowlist" in refusal

    url, refusal = resolve_pending.fsa_crp_summary_pdf_url(
        b'<a href="/docs/crp-monthly-summary-may-2026.pdf">May 2026</a>',
        "2026-06",
        landing_url=SPEC["source_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert (url, refusal) == (None, None)


def test_fsa_crp_text_fixture_parses_exact_total_acres() -> None:
    text = (FIXTURE_ROOT / "crp_monthly_summary_synthetic.txt").read_text()

    value, refusal = resolve_pending.fsa_crp_value_from_text(text, "2026-06")

    assert refusal is None
    assert value == 23_456_789


def test_fsa_crp_text_parser_refuses_wrong_identity_or_ambiguous_layout() -> None:
    text = (FIXTURE_ROOT / "crp_monthly_summary_synthetic.txt").read_text()

    value, refusal = resolve_pending.fsa_crp_value_from_text(text, "2026-05")
    assert value is None and "target month" in refusal

    duplicate = text + "\nTOTAL CRP  1  1  22,222,222  $1\n"
    value, refusal = resolve_pending.fsa_crp_value_from_text(duplicate, "2026-06")
    assert value is None and "found 2" in refusal

    missing_column = text.replace("Acres", "Hectares")
    value, refusal = resolve_pending.fsa_crp_value_from_text(missing_column, "2026-06")
    assert value is None and "Acres column" in refusal

    non_integer = text.replace("23,456,789", "23.5 million")
    value, refusal = resolve_pending.fsa_crp_value_from_text(non_integer, "2026-06")
    assert value is None and "not an integer" in refusal


def test_fsa_crp_pdf_extraction_is_external_and_fail_closed(monkeypatch) -> None:
    text, refusal = resolve_pending.fsa_crp_pdf_text(b"not a pdf")
    assert text is None and "not a PDF" in refusal

    monkeypatch.setattr(resolve_pending.shutil, "which", lambda _: None)
    text, refusal = resolve_pending.fsa_crp_pdf_text(b"%PDF-synthetic")
    assert text is None and "unavailable" in refusal

    monkeypatch.setattr(
        resolve_pending.shutil,
        "which",
        lambda _: "/usr/bin/pdftotext",
    )

    def fake_run(*args, **kwargs):
        assert args[0] == [
            "/usr/bin/pdftotext",
            "-layout",
            "-enc",
            "UTF-8",
            "-",
            "-",
        ]
        assert kwargs["input"] == b"%PDF-synthetic"
        return SimpleNamespace(returncode=0, stdout=b"layout text\n", stderr=b"")

    monkeypatch.setattr(resolve_pending.subprocess, "run", fake_run)
    text, refusal = resolve_pending.fsa_crp_pdf_text(b"%PDF-synthetic")
    assert (text, refusal) == ("layout text\n", None)

    def timed_out(*_args, **_kwargs):
        raise subprocess.TimeoutExpired("pdftotext", 60)

    monkeypatch.setattr(resolve_pending.subprocess, "run", timed_out)
    text, refusal = resolve_pending.fsa_crp_pdf_text(b"%PDF-synthetic")
    assert text is None and "failed" in refusal


def test_fsa_crp_fetch_path_archives_the_selected_pdf(monkeypatch) -> None:
    text = (FIXTURE_ROOT / "crp_monthly_summary_synthetic.txt").read_text()
    pdf_url = "https://www.fsa.usda.gov/docs/crp-monthly-summary-june-2026.pdf"
    landing = f'<a href="{pdf_url}">CRP Monthly Summary June 2026</a>'.encode()
    pdf = b"%PDF-synthetic"
    calls: list[str] = []

    def fake_get(url, *, allowed_hosts, timeout=120):
        assert allowed_hosts == SPEC["allowed_hosts"]
        assert timeout == 120
        calls.append(url)
        if url == SPEC["source_url"]:
            return landing, "2026-07-10T13:40:00Z", url
        assert url == pdf_url
        return pdf, "2026-07-10T13:40:01Z", url

    monkeypatch.setattr(resolve_pending, "http_get", fake_get)
    monkeypatch.setattr(resolve_pending, "fsa_crp_pdf_text", lambda _: (text, None))

    value, raw, source_url, retrieved_at, refusal = (
        resolve_pending.fsa_crp_fetch_period(SPEC, "2026-06")
    )

    assert calls == [SPEC["source_url"], pdf_url]
    assert value == 23_456_789
    assert raw == pdf
    assert source_url == pdf_url
    assert retrieved_at == "2026-07-10T13:40:01Z"
    assert refusal is None


def test_fsa_crp_anchor_admission_rejects_placeholders_and_bad_values() -> None:
    assert SPEC["anchor_status"] == "VERIFIED"
    assert resolve_pending.fsa_crp_verified_anchors(SPEC) == {
        "2025-11": 26317011,
        "2026-03": 26203615,
        "2026-04": 26182019,
    }
    tbv_spec = {
        **SPEC,
        "anchor_status": "ANCHOR_TBV",
        "anchors": {
            "ANCHOR_TBV_PERIOD_1": "ANCHOR_TBV",
            "ANCHOR_TBV_PERIOD_2": "ANCHOR_TBV",
            "ANCHOR_TBV_PERIOD_3": "ANCHOR_TBV",
        },
    }
    assert resolve_pending.fsa_crp_verified_anchors(tbv_spec) is None
    # Flipping the status alone must not arm placeholder anchors.
    assert (
        resolve_pending.fsa_crp_verified_anchors(
            {**tbv_spec, "anchor_status": "VERIFIED"}
        )
        is None
    )
    assert (
        resolve_pending.fsa_crp_verified_anchors(
            {**SPEC, "anchors": {"2026-01": 1, "2026-02": 2}}
        )
        is None
    )
    assert (
        resolve_pending.fsa_crp_verified_anchors(
            {**SPEC, "anchors": {**SPEC["anchors"], "2026-04": "not-a-number"}}
        )
        is None
    )

def test_fsa_crp_anchor_comparison_requires_three_exact_values() -> None:
    assert resolve_pending.fsa_crp_anchor_mismatches(
        {"2026-01": 1.0, "2026-02": 2.0},
        {"2026-01": 1.0, "2026-02": 2.0},
    ) == ["only 2 verified anchors; at least 3 required"]
    anchors = {"2026-01": 1.0, "2026-02": 2.0, "2026-03": 3.0}
    assert resolve_pending.fsa_crp_anchor_mismatches(anchors, anchors) == []
    assert resolve_pending.fsa_crp_anchor_mismatches(
        {**anchors, "2026-03": 4.0}, anchors
    ) == ["2026-03=4.0 (official 3.0)"]


def test_fsa_crp_target_routes_and_is_armed() -> None:
    ref = f"{SERIES}.june_2026.first_print"
    log = {
        "entries": [
            {
                "kind": "prediction_recorded",
                "forecastSlug": "crp-june",
                "resolutionDate": "2026-07-10",
                "unit": "count",
            }
        ],
        "resolutionLinks": [
            {
                "status": "pending",
                "forecastSlug": "crp-june",
                "targetFactRef": ref,
            }
        ],
    }

    todo = resolve_pending.pending_adapter_refs(log)

    assert len(todo) == 1
    _, kind, spec, period_type, period, release_date, forecast = todo[0]
    assert kind == "fsa_crp"
    assert (period_type, period) == ("month", "2026-06")
    assert release_date == "2026-07-10"
    assert spec["unit"] == forecast["unit"] == "count"
    anchors = resolve_pending.fsa_crp_verified_anchors(spec)
    assert anchors == {"2025-11": 26317011, "2026-03": 26203615, "2026-04": 26182019}
    assert (
        resolve_pending.binding_adapter_mismatch(
            kind,
            {"contract": {"sourceBinding": {"adapter": "fsa-crp-monthly-summary"}}},
        )
        is None
    )


def test_fsa_crp_spec_builds_a_level_fact_without_reusing_binding_transform() -> None:
    fact = resolve_pending.generic_fact(
        f"{SERIES}.june_2026.first_print",
        SPEC,
        "month",
        "2026-06",
        23_456_789,
        resolve_pending.dt.date(2026, 7, 10),
        SPEC["source_url"],
        "https://www.fsa.usda.gov/docs/crp-monthly-summary-june-2026.pdf",
    )

    assert "transform" not in SPEC
    assert fact["aggregation"] == {"method": "level"}
    assert fact["source_row_keys"] == ["2026-06"]
    assert fact["measure"]["concept"] == SERIES


def test_fsa_crp_published_anchor_fixtures_reproduce_values() -> None:
    if SPEC["anchor_status"] == "ANCHOR_TBV":
        pytest.skip(
            "ANCHOR_TBV: integrator must fetch three official summaries, "
            "record their values, and add period-named text fixtures"
        )
    anchors = resolve_pending.fsa_crp_verified_anchors(SPEC)
    assert anchors is not None
    for period, expected in anchors.items():
        text = (FIXTURE_ROOT / "anchors" / f"{period}.txt").read_text()
        got, refusal = resolve_pending.fsa_crp_value_from_text(text, period)
        assert refusal is None
        assert got == expected
