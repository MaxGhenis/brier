from __future__ import annotations

import hashlib
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sba_loan_performance as sba  # noqa: E402

FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "sba_loan_performance"
FIXTURES = {
    sba.CHARGE_OFF_AMOUNT_SERIES: (
        "WDS_ChargeOffAmount_Report_20250630.pdf",
        107_076,
        "b3f352425adcc3304cbcc406d63a2ced149bc8224f3b604c2b47403edc9070f3",
        299_971_326,
        "USD",
        "$299,971,326",
    ),
    sba.CHARGE_OFF_RATE_SERIES: (
        "WDS_ChargeOffRates_Report_20250630.pdf",
        167_134,
        "23ab3dc1d37dc08be200b8076d07371b1ac901730e1828a697278bf279a1d762",
        3.06,
        "percent",
        "3.06%",
    ),
    sba.POST_CHARGE_OFF_RECOVERY_SERIES: (
        "WDS_PostChargeOffRecovery_Report_20250630.pdf",
        109_817,
        "09616e8af327a6ea8e3bbc340e44392bbead98e581a9f85a7de99ef8b81e380f",
        126_510_000,
        "USD",
        "$126,510,000",
    ),
}


def fixture_bytes(series: str) -> bytes:
    return (FIXTURE_ROOT / FIXTURES[series][0]).read_bytes()


@pytest.mark.parametrize("series", FIXTURES)
def test_official_pdf_fixture_bytes_match_reviewed_pins(series: str) -> None:
    _, expected_size, expected_sha256, *_ = FIXTURES[series]
    raw = fixture_bytes(series)

    assert len(raw) == expected_size
    assert hashlib.sha256(raw).hexdigest() == expected_sha256


@pytest.mark.parametrize("series", FIXTURES)
def test_real_official_pdf_parses_exact_disaster_fy2024_cell(series: str) -> None:
    _, _, expected_sha256, expected_value, expected_unit, printed = FIXTURES[series]

    cell, refusal = sba.parse_sba_loan_performance_pdf(
        fixture_bytes(series), series=series, fiscal_year=2024
    )

    assert refusal is None
    assert cell is not None
    assert cell.value == expected_value
    assert cell.unit == expected_unit
    assert cell.printed_value == printed
    assert cell.report_as_of == "2025-06-30"
    assert cell.partial_fiscal_year == 2025
    assert cell.header_years == tuple(range(2016, 2026))
    assert cell.pdf_sha256 == expected_sha256


def test_real_pdf_refuses_current_partial_year_with_literal_message() -> None:
    cell, refusal = sba.parse_sba_loan_performance_pdf(
        fixture_bytes(sba.CHARGE_OFF_AMOUNT_SERIES),
        series=sba.CHARGE_OFF_AMOUNT_SERIES,
        fiscal_year=2025,
    )

    assert cell is None
    assert refusal == (
        "SBA PERIOD PARTIAL (refusing): fiscal year 2025 is quarter-to-date "
        "as of 2025-06-30"
    )


def test_real_pdf_refuses_wrong_table_identity_with_literal_message() -> None:
    cell, refusal = sba.parse_sba_loan_performance_pdf(
        fixture_bytes(sba.CHARGE_OFF_AMOUNT_SERIES),
        series=sba.POST_CHARGE_OFF_RECOVERY_SERIES,
        fiscal_year=2024,
    )

    assert cell is None
    assert refusal == (
        "SBA PDF LAYOUT DRIFT (refusing): expected one exact title "
        "'Table 7 - Post-Charge Off Recovery Amount by Program', found 0"
    )


def test_non_pdf_refusal_is_literal() -> None:
    cell, refusal = sba.parse_sba_loan_performance_pdf(
        b"not a PDF",
        series=sba.CHARGE_OFF_AMOUNT_SERIES,
        fiscal_year=2024,
    )

    assert cell is None
    assert refusal == (
        "SBA PDF LAYOUT DRIFT (refusing): response does not start with %PDF-"
    )


def test_text_parser_refuses_duplicate_header_with_literal_message() -> None:
    text, refusal = sba.sba_pdf_text(
        fixture_bytes(sba.CHARGE_OFF_RATE_SERIES),
        series=sba.CHARGE_OFF_RATE_SERIES,
    )
    assert refusal is None and text is not None
    text += "\nProgram 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025\n"

    cell, refusal = sba.parse_sba_loan_performance_text(
        text, series=sba.CHARGE_OFF_RATE_SERIES, fiscal_year=2024
    )

    assert cell is None
    assert refusal == (
        "SBA PDF LAYOUT DRIFT (refusing): expected one ten-year Program header, found 2"
    )


def test_text_parser_refuses_renamed_fiscal_year_label() -> None:
    text, refusal = sba.sba_pdf_text(
        fixture_bytes(sba.CHARGE_OFF_RATE_SERIES),
        series=sba.CHARGE_OFF_RATE_SERIES,
    )
    assert refusal is None and text is not None
    text = text.replace("Fiscal Year", "Calendar Year", 1)

    cell, refusal = sba.parse_sba_loan_performance_text(
        text, series=sba.CHARGE_OFF_RATE_SERIES, fiscal_year=2024
    )

    assert cell is None
    assert refusal == (
        "SBA PDF LAYOUT DRIFT (refusing): expected one exact 'Fiscal Year' "
        "label, found 0"
    )


def test_text_parser_refuses_title_moved_below_table() -> None:
    series = sba.CHARGE_OFF_RATE_SERIES
    title = sba.SBA_REPORT_SPECS[series].title
    text, refusal = sba.sba_pdf_text(fixture_bytes(series), series=series)
    assert refusal is None and text is not None
    text = text.replace(title, "", 1) + f"\n{title}\n"

    cell, refusal = sba.parse_sba_loan_performance_text(
        text, series=series, fiscal_year=2024
    )

    assert cell is None
    assert refusal == (
        "SBA PDF LAYOUT DRIFT (refusing): title, Fiscal Year label, and Program "
        "header are not in the reviewed order"
    )


def test_text_parser_refuses_invalid_unit_token_with_literal_message() -> None:
    text, refusal = sba.sba_pdf_text(
        fixture_bytes(sba.CHARGE_OFF_AMOUNT_SERIES),
        series=sba.CHARGE_OFF_AMOUNT_SERIES,
    )
    assert refusal is None and text is not None
    text = text.replace("$299,971,326", "299971326", 1)

    cell, refusal = sba.parse_sba_loan_performance_text(
        text, series=sba.CHARGE_OFF_AMOUNT_SERIES, fiscal_year=2024
    )

    assert cell is None
    assert refusal == (
        "SBA PDF LAYOUT DRIFT (refusing): Disaster USD row contains invalid "
        "token '299971326'"
    )


def test_text_parser_refuses_missing_completed_year_marker() -> None:
    text, refusal = sba.sba_pdf_text(
        fixture_bytes(sba.POST_CHARGE_OFF_RECOVERY_SERIES),
        series=sba.POST_CHARGE_OFF_RECOVERY_SERIES,
    )
    assert refusal is None and text is not None
    text = text.replace("as of the end of each fiscal year", "year to date", 1)

    cell, refusal = sba.parse_sba_loan_performance_text(
        text, series=sba.POST_CHARGE_OFF_RECOVERY_SERIES, fiscal_year=2024
    )

    assert cell is None
    assert refusal == (
        "SBA PDF LAYOUT DRIFT (refusing): expected one exact quarter-to-date "
        "fiscal-year statement, found 0"
    )


def test_text_parser_refuses_changed_recovery_definition() -> None:
    series = sba.POST_CHARGE_OFF_RECOVERY_SERIES
    text, refusal = sba.sba_pdf_text(fixture_bytes(series), series=series)
    assert refusal is None and text is not None
    text = text.replace(
        "after a loan has been charged off",
        "before a loan has been charged off",
        1,
    )

    cell, refusal = sba.parse_sba_loan_performance_text(
        text, series=series, fiscal_year=2024
    )

    assert cell is None
    assert refusal == (
        "SBA PDF LAYOUT DRIFT (refusing): expected one exact unit definition "
        "statement, found 0"
    )
