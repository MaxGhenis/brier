#!/usr/bin/env python3
"""Strict parser for SBA Loan Program Performance Disaster cells.

The parser fixtures exercise source layout only. Resolution must additionally
select the earliest witnessed, custody-verified capture; see the SBA custody
family design note.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import io
import re
from dataclasses import dataclass, replace

LAYOUT_REFUSAL = "SBA PDF LAYOUT DRIFT (refusing):"
PARTIAL_REFUSAL = "SBA PERIOD PARTIAL (refusing):"
PARSER_REFUSAL = "SBA PDF PARSER UNAVAILABLE (refusing):"

CHARGE_OFF_AMOUNT_SERIES = "sba.disaster.loan_program.charge_off_amount"
CHARGE_OFF_RATE_SERIES = "sba.disaster.loan_program.charge_off_rate_upb"
POST_CHARGE_OFF_RECOVERY_SERIES = "sba.disaster.loan_program.post_charge_off_recovery"


@dataclass(frozen=True)
class SbaReportSpec:
    title: str
    page_count: int
    unit: str
    footer_lead: str
    definition_marker: str
    revision_marker: str


@dataclass(frozen=True)
class SbaLoanPerformanceCell:
    series: str
    fiscal_year: int
    value: int | float
    unit: str
    printed_value: str
    table_title: str
    report_as_of: str
    partial_fiscal_year: int
    header_years: tuple[int, ...]
    pdf_sha256: str | None = None


SBA_REPORT_SPECS = {
    CHARGE_OFF_AMOUNT_SERIES: SbaReportSpec(
        title="Table 5 - Charge Off Amount by Program",
        page_count=2,
        unit="USD",
        footer_lead=(
            "This table displays the total charge off amount by program as of "
            "the end of each fiscal year."
        ),
        definition_marker=(
            "Charge off amount is defined as the total dollar amount of principal "
            "and interest outstanding at the time that the loan is charged off."
        ),
        revision_marker=(
            "Charge off amounts for a given fiscal year may be adjusted due to "
            "data updates."
        ),
    ),
    CHARGE_OFF_RATE_SERIES: SbaReportSpec(
        title=(
            "Table 9 - Charge Off Rates as a Percent of Unpaid Principal "
            "Balance (UPB) Amount by Program"
        ),
        page_count=1,
        unit="percent",
        footer_lead=(
            "This table displays the charge off rates by program for each given "
            "fiscal year."
        ),
        definition_marker=(
            "Charge off rates are defined as the charge off amount during the "
            "fiscal year as a percent of UPB at fiscal year end."
        ),
        revision_marker=(
            "Charge off rates for previous fiscal years are updated to reflect "
            "changes to charge off amounts."
        ),
    ),
    POST_CHARGE_OFF_RECOVERY_SERIES: SbaReportSpec(
        title="Table 7 - Post-Charge Off Recovery Amount by Program",
        page_count=2,
        unit="USD",
        footer_lead=(
            "This table displays the total post-charge off recovery amount by "
            "program as of the end of each fiscal year."
        ),
        definition_marker=(
            "Post-charge off recovery amount is typically defined as the dollar "
            "amount recovered via the Treasury Cross Servicing program after a "
            "loan has been charged off, however not all these recoveries are due "
            "to Treasury efforts."
        ),
        revision_marker=(
            "Post-charge off recovery amounts for a given fiscal year may be "
            "adjusted due to data updates."
        ),
    ),
}

_HEADER_RE = re.compile(r"Program((?:\s+\d{4}){10})")
_USD_RE = re.compile(r"\$-?(?:0|[1-9]\d{0,2}(?:,\d{3})*)")
_PERCENT_RE = re.compile(r"(?:0|[1-9]\d*)(?:\.\d{2})%")
_PARTIAL_TAIL_RE = re.compile(
    r" Since data are not available through the end of the most recent fiscal "
    r"year, the data displayed in (?P<year>\d{4}) are as of "
    r"(?P<date>\d{2}/\d{2}/\d{4})\."
)
_EXPECTED_MEDIA_BOX = (1008.0, 612.0)
_QUARTER_ENDS = {(3, 31), (6, 30), (9, 30), (12, 31)}


def _spec(series: str) -> SbaReportSpec:
    try:
        return SBA_REPORT_SPECS[series]
    except KeyError as exc:
        raise ValueError(f"unsupported SBA Loan Performance series {series!r}") from exc


def _layout_refusal(reason: str) -> tuple[None, str]:
    return None, f"{LAYOUT_REFUSAL} {reason}"


def _normalized_lines(text: str) -> list[str]:
    return [
        normalized
        for line in text.replace("\r\n", "\n").replace("\r", "\n").splitlines()
        if (normalized := " ".join(line.split()))
    ]


def sba_pdf_text(raw: bytes, *, series: str) -> tuple[str | None, str | None]:
    """Extract page-one layout text while enforcing the reviewed PDF shape."""

    spec = _spec(series)
    if not raw.startswith(b"%PDF-"):
        return _layout_refusal("response does not start with %PDF-")
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError:
        return None, f"{PARSER_REFUSAL} pypdf is not installed"

    try:
        reader = PdfReader(io.BytesIO(raw), strict=True)
        if reader.is_encrypted:
            return _layout_refusal("PDF is encrypted")
        page_count = len(reader.pages)
        if page_count != spec.page_count:
            return _layout_refusal(
                f"expected {spec.page_count} pages for {series}, found {page_count}"
            )
        page = reader.pages[0]
        if (page.rotation or 0) != 0:
            return _layout_refusal("page 1 rotation changed")
        media_box = (
            round(float(page.mediabox.width), 3),
            round(float(page.mediabox.height), 3),
        )
        if media_box != _EXPECTED_MEDIA_BOX:
            return _layout_refusal("page 1 media box must remain 1008x612 points")
        text = page.extract_text(extraction_mode="layout")
    except Exception:
        return _layout_refusal("strict PDF parsing failed")
    if not text or not text.strip():
        return _layout_refusal("page 1 has no extractable text")
    return text, None


def parse_sba_loan_performance_text(
    text: str, *, series: str, fiscal_year: int
) -> tuple[SbaLoanPerformanceCell | None, str | None]:
    """Parse one completed Disaster fiscal-year cell from page-one text."""

    if type(fiscal_year) is not int:
        raise TypeError("fiscal_year must be an integer")
    spec = _spec(series)
    lines = _normalized_lines(text)
    collapsed = " ".join(text.split())

    title_count = lines.count(spec.title)
    if title_count != 1:
        return _layout_refusal(
            f"expected one exact title {spec.title!r}, found {title_count}"
        )

    headers = [match for line in lines if (match := _HEADER_RE.fullmatch(line))]
    if len(headers) != 1:
        return _layout_refusal(
            f"expected one ten-year Program header, found {len(headers)}"
        )
    fiscal_year_label_count = lines.count("Fiscal Year")
    if fiscal_year_label_count != 1:
        return _layout_refusal(
            f"expected one exact 'Fiscal Year' label, found {fiscal_year_label_count}"
        )
    years = tuple(int(value) for value in headers[0].group(1).split())
    if years != tuple(range(years[0], years[0] + 10)):
        return _layout_refusal("fiscal-year header is not ten consecutive years")
    header_line = f"Program {' '.join(str(year) for year in years)}"
    if lines[:3] != [spec.title, "Fiscal Year", header_line]:
        return _layout_refusal(
            "title, Fiscal Year label, and Program header are not in the reviewed order"
        )

    section_indexes = [index for index, line in enumerate(lines) if line == "Disaster"]
    row_indexes = [
        index for index, line in enumerate(lines) if line.startswith("Disaster ")
    ]
    if len(section_indexes) != 1 or len(row_indexes) != 1:
        return _layout_refusal(
            "expected one Disaster section and one Disaster row, found "
            f"{len(section_indexes)} and {len(row_indexes)}"
        )
    if row_indexes[0] != section_indexes[0] + 1:
        return _layout_refusal("Disaster row does not immediately follow its section")

    row = lines[row_indexes[0]].split()
    values = row[1:]
    if len(values) != len(years):
        return _layout_refusal(
            f"Disaster row has {len(values)} values for {len(years)} headers"
        )
    value_re = _USD_RE if spec.unit == "USD" else _PERCENT_RE
    invalid = next((value for value in values if not value_re.fullmatch(value)), None)
    if invalid is not None:
        return _layout_refusal(
            f"Disaster {spec.unit} row contains invalid token {invalid!r}"
        )

    for label, marker in (
        ("unit definition", spec.definition_marker),
        ("revision", spec.revision_marker),
    ):
        marker_count = collapsed.count(marker)
        if marker_count != 1:
            return _layout_refusal(
                f"expected one exact {label} statement, found {marker_count}"
            )

    partial_re = re.compile(re.escape(spec.footer_lead) + _PARTIAL_TAIL_RE.pattern)
    partial_matches = list(partial_re.finditer(collapsed))
    if len(partial_matches) != 1:
        return _layout_refusal(
            "expected one exact quarter-to-date fiscal-year statement, found "
            f"{len(partial_matches)}"
        )
    partial_year = int(partial_matches[0].group("year"))
    date_text = partial_matches[0].group("date")
    try:
        report_as_of = dt.datetime.strptime(date_text, "%m/%d/%Y").date()
    except ValueError:
        return _layout_refusal("quarter-to-date statement has an invalid date")
    if (report_as_of.month, report_as_of.day) not in _QUARTER_ENDS:
        return _layout_refusal("report as-of date is not a quarter end")
    as_of_fiscal_year = report_as_of.year + (report_as_of.month >= 10)
    if partial_year != as_of_fiscal_year or partial_year != years[-1]:
        return _layout_refusal(
            "quarter-to-date fiscal year does not match the report as-of date "
            "and final header"
        )

    if fiscal_year not in years:
        return _layout_refusal(
            f"fiscal year {fiscal_year} is absent from the ten-year header"
        )
    if fiscal_year == partial_year:
        return (
            None,
            f"{PARTIAL_REFUSAL} fiscal year {fiscal_year} is quarter-to-date "
            f"as of {report_as_of.isoformat()}",
        )

    printed_value = values[years.index(fiscal_year)]
    if spec.unit == "USD":
        parsed_value: int | float = int(printed_value[1:].replace(",", ""))
    else:
        parsed_value = float(printed_value[:-1])
    return (
        SbaLoanPerformanceCell(
            series=series,
            fiscal_year=fiscal_year,
            value=parsed_value,
            unit=spec.unit,
            printed_value=printed_value,
            table_title=spec.title,
            report_as_of=report_as_of.isoformat(),
            partial_fiscal_year=partial_year,
            header_years=years,
        ),
        None,
    )


def parse_sba_loan_performance_pdf(
    raw: bytes, *, series: str, fiscal_year: int
) -> tuple[SbaLoanPerformanceCell | None, str | None]:
    """Parse an official PDF and bind the result to the member-byte hash."""

    text, refusal = sba_pdf_text(raw, series=series)
    if refusal is not None:
        return None, refusal
    assert text is not None
    cell, refusal = parse_sba_loan_performance_text(
        text, series=series, fiscal_year=fiscal_year
    )
    if refusal is not None:
        return None, refusal
    assert cell is not None
    return replace(cell, pdf_sha256=hashlib.sha256(raw).hexdigest()), None
