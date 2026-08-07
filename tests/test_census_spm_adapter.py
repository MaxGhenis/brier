from __future__ import annotations

import copy
import hashlib
import io
import json
import pathlib
import sys
import zipfile
from xml.sax.saxutils import escape

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import prospect_targets  # noqa: E402
import register_targets  # noqa: E402
import resolve_pending  # noqa: E402
import roll_docket  # noqa: E402
from adopt_proven_series import SOURCE_BINDING_TEMPLATE_KEYS  # noqa: E402

SERIES = "census.spm.child_poverty_rate"
SPEC = resolve_pending.CENSUS_SPM_ADAPTERS[SERIES]
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "census_spm"


def corrected_anchor_fixture() -> dict[str, float]:
    """Synthetic future values that cannot match either legacy transition."""

    return {
        "2019": 12.1,
        "2020": 9.3,
        "2021": 5.1,
        "2022": 12.3,
        "2023": 13.6,
        "2024": 13.2,
    }


def invalid_anchor_specs() -> list[tuple[str, dict]]:
    corrected = corrected_anchor_fixture()
    verified = {
        **SPEC,
        "anchor_status": "VERIFIED_REVISED_METHODOLOGY",
        "anchors": corrected,
    }
    cases = [
        ("wrong-status", {**verified, "anchor_status": "VERIFIED"}),
        (
            "boolean-2024",
            {**verified, "anchors": {**corrected, "2024": True}},
        ),
        (
            "legacy-2019-12.5",
            {**verified, "anchors": {**corrected, "2019": 12.5}},
        ),
        (
            "legacy-2019-12.6",
            {**verified, "anchors": {**corrected, "2019": 12.6}},
        ),
        (
            "legacy-2020-9.7",
            {**verified, "anchors": {**corrected, "2020": 9.7}},
        ),
        (
            "full-legacy-vector",
            {
                **verified,
                "anchors": {
                    "2019": 12.6,
                    "2020": 9.7,
                    "2021": 5.2,
                    "2022": 12.4,
                    "2023": 13.7,
                    "2024": 13.4,
                },
            },
        ),
    ]
    for missing_year in corrected:
        cases.append(
            (
                f"missing-{missing_year}",
                {
                    **verified,
                    "anchors": {
                        year: value
                        for year, value in corrected.items()
                        if year != missing_year
                    },
                },
            )
        )
    for extra_year in ("2018", "2025"):
        cases.append(
            (
                f"extra-{extra_year}",
                {
                    **verified,
                    "anchors": {**corrected, extra_year: 10.0},
                },
            )
        )
    return cases


def docket_entry() -> dict:
    docket = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    return next(entry for entry in docket["series"] if entry["series"] == SERIES)


def inline_cell(reference: str, value: str) -> str:
    return (
        f'<c r="{reference}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'
    )


def number_cell(reference: str, value: float | int) -> str:
    return f'<c r="{reference}"><v>{value}</v></c>'


def synthetic_workbook(*, sheet_name: str = "TableB-2") -> bytes:
    rows = {
        2: [
            inline_cell(
                "A2",
                "Table B-2. Number and Percentage of People in Poverty Using "
                "the Supplemental Poverty Measure by Age, Race, and Hispanic "
                "Origin: 2009 to 2024",
            )
        ],
        4: [
            inline_cell("A4", "Race, Hispanic origin, and year"),
            inline_cell("B4", "All People"),
            inline_cell("G4", "Under 18 years"),
        ],
        5: [
            inline_cell("C5", "Below Poverty"),
            inline_cell("H5", "Below Poverty"),
        ],
        6: [
            inline_cell("B6", "Total"),
            inline_cell("C6", "Number"),
            inline_cell("D6", "Margin of error"),
            inline_cell("E6", "Percent"),
            inline_cell("F6", "Margin of error"),
            inline_cell("G6", "Total"),
            inline_cell("H6", "Number"),
            inline_cell("I6", "Margin of error"),
            inline_cell("J6", "Percent"),
            inline_cell("K6", "Margin of error"),
        ],
        7: [inline_cell("A7", "ALL RACES")],
        # Match the real rich-text cell: the footnote run is flattened after
        # the year by the OOXML reader.
        8: [
            '<c r="A8" t="inlineStr"><is><r><t>2024</t></r>'
            '<r><t>3</t></r></is></c>',
            number_cell("G8", 72980),
            number_cell("H8", 9744),
            number_cell("J8", 13.4),
        ],
        9: [
            number_cell("A9", 2023),
            number_cell("G9", 1000),
            number_cell("H9", 137),
            number_cell("J9", 13.7),
        ],
        10: [
            number_cell("A10", 2022),
            number_cell("G10", 1000),
            number_cell("H10", 124),
            number_cell("J10", 12.4),
        ],
        11: [inline_cell("A11", "White alone")],
        # A repeated year in another race section must never make ALL RACES
        # ambiguous.
        12: [number_cell("A12", 2024), number_cell("J12", 8.1)],
    }
    row_xml = "".join(
        f'<row r="{row}">{"".join(cells)}</row>'
        for row, cells in sorted(rows.items())
    )
    merges = (
        '<mergeCell ref="A4:A6"/>'
        '<mergeCell ref="B4:F4"/>'
        '<mergeCell ref="G4:K4"/>'
        '<mergeCell ref="C5:F5"/>'
        '<mergeCell ref="H5:K5"/>'
        # The official 2024 workbook merges the section label A7:U7.
        '<mergeCell ref="A7:U7"/>'
    )
    worksheet = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/'
        'spreadsheetml/2006/main">'
        f"<sheetData>{row_xml}</sheetData>"
        f'<mergeCells count="6">{merges}</mergeCells>'
        "</worksheet>"
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/'
        'spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships"><sheets>'
        f'<sheet name="{escape(sheet_name)}" sheetId="1" r:id="rId1"/>'
        "</sheets></workbook>"
    )
    relationships = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/'
        '2006/relationships"><Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("xl/workbook.xml", workbook)
        archive.writestr("xl/_rels/workbook.xml.rels", relationships)
        archive.writestr("xl/worksheets/sheet1.xml", worksheet)
    return output.getvalue()


def test_adapter_and_docket_share_the_exact_seven_key_binding() -> None:
    binding = docket_entry()["extras"]["sourceBinding"]

    assert "census-spm-annual-report" in register_targets.SOURCE_ADAPTERS
    assert binding["sourceUrl"] == (
        "https://www.census.gov/newsroom/press-releases/2026/"
        "statement-on-supplemental-poverty-measure.html"
    )
    assert SPEC["publications_url"] == (
        "https://www.census.gov/topics/income-poverty/library/"
        "publications.html"
    )
    assert "expectedReleaseWindow" not in SPEC
    assert "resolutionDate" not in SPEC
    assert binding["field"] == "under_18_percent_in_poverty"
    assert "revised-methodology" in binding["table"]
    assert "Table B-2" in binding["table"]
    assert prospect_targets._source_binding_errors(binding) == []
    assert set(binding) == SOURCE_BINDING_TEMPLATE_KEYS
    assert resolve_pending.census_spm_binding_template(SPEC) == binding
    assert resolve_pending.census_spm_binding_matches_spec(binding, SPEC)
    assert resolve_pending.census_spm_binding_matches_spec(
        {
            **binding,
            "allowedHosts": ["www.census.gov", "www2.census.gov"],
            "expectedReleaseWindow": {
                "start": "2028-08-01",
                "end": "2028-12-31",
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
        assert not resolve_pending.census_spm_binding_matches_spec(tampered, SPEC)
    assert not resolve_pending.census_spm_binding_matches_spec(
        {**binding, "unexpected": True}, SPEC
    )
    assert not resolve_pending.census_spm_binding_matches_spec(
        {**binding, "allowedHosts": ["www.census.gov"]}, SPEC
    )
    assert not resolve_pending.census_spm_binding_matches_spec(
        {**binding, "allowedHosts": ["example.com", "www.census.gov"]}, SPEC
    )


def test_spm_pair_targets_cy2027_after_ty2027_policy_and_before_release() -> None:
    entry = docket_entry()
    irs_entry = next(
        candidate
        for candidate in json.loads(
            (ROOT / "scripts" / "docket_series.json").read_text()
        )["series"]
        if candidate["series"] == "irs.actc.total_claims"
    )
    assert "anchors" not in entry["extras"]
    assert "September 2026" in entry["comment"]
    assert entry["period"] == "2027"
    assert entry["conditionalPair"]["conditionDeadline"] == "2027-12-31"
    assert entry["extras"]["resolutionDate"] == "2028-12-31"
    assert entry["extras"]["expectedReleaseWindow"] == {
        "start": "2028-08-01",
        "end": "2028-12-31",
    }
    assert "methodology announcement (identity)" in entry["extras"][
        "resolutionSource"
    ]
    assert "Table B-2 (resolving artifact)" in entry["extras"][
        "resolutionSource"
    ]
    assert "Thesis lab commitments" in entry["extras"]["resolutionRule"]
    assert "announcement does not establish either timing value" in entry[
        "extras"
    ]["resolutionRule"]
    assert [arm["conditionId"] for arm in entry["conditionalPair"]["arms"]] == [
        arm["conditionId"] for arm in irs_entry["conditionalPair"]["arms"]
    ]
    assert [arm["conditional"] for arm in entry["conditionalPair"]["arms"]] != [
        arm["conditional"] for arm in irs_entry["conditionalPair"]["arms"]
    ]
    assert all(
        conditional.startswith(
            "For the CY2027 Census Supplemental Poverty Measure "
            "child-poverty outcome,"
        )
        and "tax year 2027" in conditional
        for conditional in (
            arm["conditional"] for arm in entry["conditionalPair"]["arms"]
        )
    )

    targets = roll_docket.conditional_pair_seed_targets(
        entry, set(), roll_docket.dt.date(2026, 8, 4)
    )
    assert [target["catalogSlug"] for target in targets] == [
        "spm-child-poverty-rate-cy2027-threshold-one-dollar",
        "spm-child-poverty-rate-cy2027-current-law",
    ]
    assert [target["dataPointId"] for target in targets] == [
        f"{SERIES}.2027.first_print.threshold_one_dollar",
        f"{SERIES}.2027.first_print.current_law",
    ]
    for target in targets:
        contract = register_targets.build_contract(
            target, roll_docket.dt.date(2026, 8, 4)
        )
        assert contract["resolutionDate"] == "2028-12-31"
        assert contract["sourceBinding"]["expectedReleaseWindow"] == {
            "start": "2028-08-01",
            "end": "2028-12-31",
        }


def test_publication_index_selects_exact_report_and_enforces_first_print() -> None:
    target = "/library/publications/2025/demo/p60-287.html"
    index = f"""
      <a href="/library/publications/2024/demo/p60-285.html">
        Poverty in the United States: 2023
      </a>
      <a href="{target}">Poverty in the United States: 2024</a>
      <a href="{target}">duplicate navigation link</a>
    """.encode()
    url, refusal = resolve_pending.census_spm_report_url(
        index,
        "2024",
        publications_url=SPEC["publications_url"],
        allowed_hosts=SPEC["allowed_hosts"],
        require_latest=True,
    )
    assert refusal is None
    assert url == f"https://www.census.gov{target}"

    later = index + b"""
      <a href="/library/publications/2026/demo/p60-290.html">
        Poverty in the United States: 2025
      </a>
    """
    url, refusal = resolve_pending.census_spm_report_url(
        later,
        "2024",
        publications_url=SPEC["publications_url"],
        allowed_hosts=SPEC["allowed_hosts"],
        require_latest=True,
    )
    assert (url, refusal) == (
        None,
        "Census report for 2024 is no longer the latest annual print (found "
        "2025); the first-print window was missed",
    )

    url, refusal = resolve_pending.census_spm_report_url(
        b'<a href="https://example.com/library/publications/2025/demo/'
        b'p60-287.html">'
        b"Poverty in the United States: 2024</a>",
        "2024",
        publications_url=SPEC["publications_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert (url, refusal) == (
        None,
        "source host 'example.com' is not in adapter allowlist "
        "['www.census.gov', 'www2.census.gov']",
    )

    early_url = (
        "https://www.census.gov/library/publications/2024/demo/p60-287.html"
    )
    url, refusal = resolve_pending.census_spm_report_url(
        (
            f'<a href="{early_url}">'
            "Poverty in the United States: 2024</a>"
        ).encode(),
        "2024",
        publications_url=SPEC["publications_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert url is None
    assert refusal == (
        "Census annual report link does not match the reviewed P60 "
        "publication path for 2024: report URL publication year 2024 "
        "predates the earliest valid year 2025 for the 2024 outcome: "
        f"{early_url!r}"
    )


def test_report_page_selects_one_table_b2_and_refuses_layout_drift() -> None:
    report_url = "https://www.census.gov/library/publications/2025/demo/p60-287.html"
    table_url = (
        "https://www2.census.gov/programs-surveys/demo/tables/p60/287/"
        "tableB-2.xlsx"
    )
    report = f"""
      <h1>Poverty in the United States: 2024</h1>
      <p>September 09, 2025</p>
      <a href="{table_url}">Table B-2</a>
    """.encode()
    url, refusal = resolve_pending.census_spm_table_url(
        report,
        "2024",
        report_url=report_url,
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert (url, refusal) == (table_url, None)

    missing = b"<h1>Poverty in the United States: 2024</h1>"
    url, refusal = resolve_pending.census_spm_table_url(
        missing,
        "2024",
        report_url=report_url,
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert (url, refusal) == (
        None,
        "Census annual report page has no reviewed Table B-2 XLSX link; the "
        "publication is incomplete or its layout changed",
    )

    wrong_report_number = report.replace(b"/p60/287/", b"/p60/999/")
    url, refusal = resolve_pending.census_spm_table_url(
        wrong_report_number,
        "2024",
        report_url=report_url,
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert (url, refusal) == (
        None,
        "Census published a Table B-2 link but not the reviewed "
        "'tableB-2.xlsx' artifact; extend the adapter",
    )


def test_report_publication_date_and_first_print_window_fail_closed() -> None:
    report_url = (
        "https://www.census.gov/library/publications/2025/demo/p60-287.html"
    )
    report = b"""
      <h1>Poverty in the United States: 2024</h1>
      <p>September <strong>09</strong>, 2025</p>
      <footer>Page Last Revised - August 13, 2025</footer>
    """
    publication_day, refusal = (
        resolve_pending.census_spm_report_publication_date(
            report, "2024", report_url=report_url
        )
    )
    assert (publication_day, refusal) == (
        resolve_pending.dt.date(2025, 9, 9),
        None,
    )
    assert (
        resolve_pending.census_spm_first_print_gate(
            publication_day,
            resolve_pending.dt.date(2025, 9, 30),
            SPEC["first_print_window_days"],
        )
        is None
    )
    refusal = resolve_pending.census_spm_first_print_gate(
        publication_day,
        resolve_pending.dt.date(2025, 10, 1),
        SPEC["first_print_window_days"],
    )
    assert refusal == (
        "report published 2025-09-09, but capture 2025-10-01 missed the "
        "21-day first-print window ending 2025-09-30"
    )


def test_later_publication_year_keeps_title_latest_and_first_print_checks(
    monkeypatch,
) -> None:
    report_url = (
        "https://www.census.gov/library/publications/2028/demo/p60-300.html"
    )
    table_url = (
        "https://www2.census.gov/programs-surveys/demo/tables/p60/300/"
        "tableB-2.xlsx"
    )
    index = (
        f'<a href="{report_url}">Poverty in the United States: 2026</a>'
    ).encode()
    report = (
        "<h1>Poverty in the United States: 2026</h1>"
        "<p>January 12, 2028</p>"
        f'<a href="{table_url}">Table B-2</a>'
    ).encode()
    workbook = b"delayed-cy2026-workbook"

    def fake_get(url, *, allowed_hosts, timeout=120):
        assert allowed_hosts == SPEC["allowed_hosts"]
        if url == SPEC["publications_url"]:
            return index, "2028-01-12T12:00:00Z", url
        if url == report_url:
            return report, "2028-01-12T12:00:01Z", url
        assert url == table_url
        return workbook, "2028-01-12T12:00:02Z", url

    monkeypatch.setattr(resolve_pending, "http_get", fake_get)
    monkeypatch.setattr(
        resolve_pending, "utc_now", lambda: "2028-01-12T12:00:03Z"
    )
    monkeypatch.setattr(
        resolve_pending,
        "census_spm_xlsx_grid",
        lambda raw, spec: ([raw, spec], None),
    )
    monkeypatch.setattr(
        resolve_pending,
        "census_spm_rate_from_grid",
        lambda grid, year, spec: (11.2, None),
    )

    assert resolve_pending.census_spm_fetch_year(
        SPEC, "2026", require_latest=True
    ) == (
        11.2,
        workbook,
        table_url,
        "2028-01-12T12:00:02Z",
        None,
    )

    mismatched_date = report.replace(
        b"January 12, 2028", b"January 12, 2027"
    )
    publication_day, refusal = (
        resolve_pending.census_spm_report_publication_date(
            mismatched_date, "2026", report_url=report_url
        )
    )
    assert publication_day is None
    assert refusal == (
        "Census report publication date year 2027 does not match P60 URL "
        "publication year 2028: "
        "'https://www.census.gov/library/publications/2028/demo/p60-300.html'"
    )


def test_synthetic_table_orientation_and_merged_headers_parse_exact_rate() -> None:
    grid, refusal = resolve_pending.census_spm_xlsx_grid(
        synthetic_workbook(), SPEC
    )
    assert refusal is None
    # J's propagated ancestry is exactly the official header path.
    assert grid[3][9] == "Under 18 years"
    assert grid[4][9] == "Below Poverty"
    assert grid[5][9] == "Percent"
    assert grid[6][20] == "ALL RACES"

    value, refusal = resolve_pending.census_spm_rate_from_grid(
        grid, "2024", SPEC
    )
    assert (value, refusal) == (13.4, None)
    historical, refusal = resolve_pending.census_spm_rate_from_grid(
        grid, "2023", SPEC, report_year="2024"
    )
    assert (historical, refusal) == (13.7, None)


@pytest.mark.parametrize(
    ("filename", "byte_count", "digest", "report_year", "expected"),
    (
        (
            "p60-283-tableB-2.xlsx",
            41_756,
            "c5938c06302e547583d35fc8d1480b6b726b288501c46b99d5965f517b4a245e",
            "2023",
            {
                "2019": 12.6,
                "2020": 9.7,
                "2021": 5.2,
                "2022": 12.4,
                "2023": 13.7,
            },
        ),
        (
            "p60-287-tableB-2.xlsx",
            43_484,
            "8cdb688380c543c1bd3bc47e2124ec6872511eff8c03c8340b1adacdbd1525fe",
            "2024",
            {
                "2019": 12.6,
                "2020": 9.7,
                "2021": 5.2,
                "2022": 12.4,
                "2023": 13.7,
                "2024": 13.4,
            },
        ),
    ),
)
def test_official_workbook_vintages_are_hash_pinned_and_parse_legacy_series(
    filename, byte_count, digest, report_year, expected
) -> None:
    raw = (FIXTURE_ROOT / filename).read_bytes()
    assert len(raw) == byte_count
    assert hashlib.sha256(raw).hexdigest() == digest
    grid, refusal = resolve_pending.census_spm_xlsx_grid(raw, SPEC)
    assert refusal is None

    actual = {}
    for year in expected:
        value, refusal = resolve_pending.census_spm_rate_from_grid(
            grid, year, SPEC, report_year=report_year
        )
        assert refusal is None
        actual[year] = value
    assert actual == expected


def test_table_parser_fails_closed_on_wrong_identity_and_ambiguity() -> None:
    grid, refusal = resolve_pending.census_spm_xlsx_grid(
        synthetic_workbook(), SPEC
    )
    assert refusal is None

    _, refusal = resolve_pending.census_spm_rate_from_grid(grid, "2023", SPEC)
    assert refusal == (
        "Table B-2 title is not the Supplemental Poverty Measure range ending "
        "in report year 2023; wrong or later workbook"
    )

    duplicate_column = copy.deepcopy(grid)
    duplicate_column[3][10] = "Under 18 years"
    duplicate_column[4][10] = "Below Poverty"
    duplicate_column[5][10] = "Percent"
    _, refusal = resolve_pending.census_spm_rate_from_grid(
        duplicate_column, "2024", SPEC
    )
    assert refusal == (
        "expected exactly one Under 18 years / Below Poverty / Percent "
        "column, found 2 at [9, 10]"
    )

    duplicate_year = copy.deepcopy(grid)
    duplicate_year.insert(10, [2024.0, *("" for _ in range(8)), 99.0])
    _, refusal = resolve_pending.census_spm_rate_from_grid(
        duplicate_year, "2024", SPEC
    )
    assert refusal == (
        "expected exactly one 2024 row inside ALL RACES, found 2; duplicate "
        "transition rows require exactly one row carrying an authenticated "
        "revised-methodology footnote, found 0"
    )

    legacy_grid, refusal = resolve_pending.census_spm_xlsx_grid(
        (FIXTURE_ROOT / "p60-287-tableB-2.xlsx").read_bytes(), SPEC
    )
    assert refusal is None
    footnote_tamper = copy.deepcopy(legacy_grid)
    for row in footnote_tamper:
        for column, cell in enumerate(row):
            if isinstance(cell, str) and (
                "revised Supplemental Poverty Measure methodology" in cell
            ):
                row[column] = cell.replace("revised", "unreviewed")
    _, refusal = resolve_pending.census_spm_rate_from_grid(
        footnote_tamper, "2019", SPEC, report_year="2024"
    )
    assert refusal == (
        "expected exactly one 2019 row inside ALL RACES, found 2; duplicate "
        "transition rows require exactly one row carrying an authenticated "
        "revised-methodology footnote, found 0"
    )

    bad_value = copy.deepcopy(grid)
    bad_value[7][9] = "13.4 percent"
    _, refusal = resolve_pending.census_spm_rate_from_grid(
        bad_value, "2024", SPEC
    )
    assert refusal == (
        "child SPM percent cell is not in [0, 100]: '13.4 percent'"
    )

    bad_arithmetic = copy.deepcopy(grid)
    bad_arithmetic[7][7] = 5000.0
    _, refusal = resolve_pending.census_spm_rate_from_grid(
        bad_arithmetic, "2024", SPEC
    )
    assert refusal == (
        "child SPM percent fails the Table B-2 arithmetic cross-check: "
        "published 13.4, implied 6.85119 from 5000/72980"
    )

    _, refusal = resolve_pending.census_spm_xlsx_grid(
        synthetic_workbook(sheet_name="Table B-3"), SPEC
    )
    assert refusal == (
        "expected exactly one Table B-2 sheet, found 0 (sheets: "
        "['Table B-3']); extend the adapter"
    )


def test_fetch_year_discovers_and_archives_the_exact_xlsx(monkeypatch) -> None:
    report_url = "https://www.census.gov/library/publications/2025/demo/p60-287.html"
    table_url = (
        "https://www2.census.gov/programs-surveys/demo/tables/p60/287/"
        "tableB-2.xlsx"
    )
    index = (
        f'<a href="{report_url}">Poverty in the United States: 2024</a>'
    ).encode()
    report = (
        f"<h1>Poverty in the United States: 2024</h1>"
        "<p>September 09, 2025</p>"
        f'<a href="{table_url}">Table B-2</a>'
    ).encode()
    workbook = synthetic_workbook()
    calls: list[str] = []

    def fake_get(url, *, allowed_hosts, timeout=120):
        assert allowed_hosts == SPEC["allowed_hosts"]
        calls.append(url)
        if url == SPEC["publications_url"]:
            return index, "2025-09-09T12:00:00Z", url
        if url == report_url:
            return report, "2025-09-09T12:00:01Z", url
        assert url == table_url
        return workbook, "2025-09-09T12:00:02Z", url

    monkeypatch.setattr(resolve_pending, "http_get", fake_get)
    monkeypatch.setattr(
        resolve_pending, "utc_now", lambda: "2025-09-09T12:00:03Z"
    )
    value, raw, url, retrieved_at, refusal = resolve_pending.census_spm_fetch_year(
        SPEC, "2024", require_latest=True
    )

    assert calls == [SPEC["publications_url"], report_url, table_url]
    assert (value, raw, url, retrieved_at, refusal) == (
        13.4,
        workbook,
        table_url,
        "2025-09-09T12:00:02Z",
        None,
    )


def test_fetch_year_refuses_report_redirect_and_late_capture(monkeypatch) -> None:
    report_url = "https://www.census.gov/library/publications/2025/demo/p60-287.html"
    redirected_url = (
        "https://www.census.gov/library/publications/2025/demo/p60-999.html"
    )
    index = (
        f'<a href="{report_url}">Poverty in the United States: 2024</a>'
    ).encode()
    report = b"""
      <h1>Poverty in the United States: 2024</h1>
      <p>September 09, 2025</p>
    """

    def redirected_get(url, *, allowed_hosts, timeout=120):
        if url == SPEC["publications_url"]:
            return index, "2025-09-09T12:00:00Z", url
        assert url == report_url
        return report, "2025-09-09T12:00:01Z", redirected_url

    monkeypatch.setattr(resolve_pending, "http_get", redirected_get)
    *_, refusal = resolve_pending.census_spm_fetch_year(SPEC, "2024")
    assert refusal == (
        "Census annual report fetch redirected away from the exact indexed "
        "P60 artifact: "
        "'https://www.census.gov/library/publications/2025/demo/p60-287.html' "
        "-> "
        "'https://www.census.gov/library/publications/2025/demo/p60-999.html'"
    )

    def late_get(url, *, allowed_hosts, timeout=120):
        if url == SPEC["publications_url"]:
            return index, "2025-09-30T23:59:58Z", url
        assert url == report_url
        return report, "2025-09-30T23:59:59Z", url

    monkeypatch.setattr(resolve_pending, "http_get", late_get)
    # The report request began on the last admissible day, but the decision
    # happened after midnight. The post-response day must win.
    monkeypatch.setattr(
        resolve_pending, "utc_now", lambda: "2025-10-01T00:00:01Z"
    )
    *_, refusal = resolve_pending.census_spm_fetch_year(SPEC, "2024")
    assert refusal == (
        "report published 2025-09-09, but capture 2025-10-01 missed the "
        "21-day first-print window ending 2025-09-30"
    )


def test_revised_anchor_admission_and_exact_comparison() -> None:
    assert "anchors" not in SPEC
    assert resolve_pending.census_spm_verified_anchors(SPEC) is None
    corrected = corrected_anchor_fixture()
    verified = {
        **SPEC,
        "anchor_status": "VERIFIED_REVISED_METHODOLOGY",
        # Synthetic future values only. The real legacy workbook values below
        # must never arm the corrected-methodology adapter.
        "anchors": corrected,
    }
    anchors = resolve_pending.census_spm_verified_anchors(verified)
    assert anchors == corrected
    assert resolve_pending.census_spm_anchor_mismatches(anchors, anchors) == []
    assert resolve_pending.census_spm_anchor_mismatches(
        {**anchors, "2024": 13.3}, anchors
    ) == ["2024=13.3 (official 13.2)"]
    incomplete = {
        year: value for year, value in anchors.items() if year != "2019"
    }
    assert resolve_pending.census_spm_anchor_mismatches(
        incomplete, incomplete
    ) == [
        "verified anchors must cover exactly 2019-2024; got "
        "['2020', '2021', '2022', '2023', '2024']"
    ]
    for _case, bad in invalid_anchor_specs():
        assert resolve_pending.census_spm_verified_anchors(bad) is None


def test_both_condition_arms_route_to_one_annual_print() -> None:
    refs = [
        f"{SERIES}.2027.first_print.threshold_one_dollar",
        f"{SERIES}.2027.first_print.current_law",
    ]
    log = {
        "entries": [
            {
                "kind": "prediction_recorded",
                "forecastSlug": f"spm-arm-{index}",
                "resolutionDate": "2028-12-31",
                "unit": "percent",
            }
            for index in range(2)
        ],
        "resolutionLinks": [
            {
                "status": "pending",
                "forecastSlug": f"spm-arm-{index}",
                "targetFactRef": ref,
            }
            for index, ref in enumerate(refs)
        ],
    }

    todo = resolve_pending.pending_adapter_refs(log)
    assert [row[0] for row in todo] == refs
    assert {(row[1], row[3], row[4]) for row in todo} == {
        ("census_spm", "year", "2027")
    }


@pytest.mark.parametrize(
    ("case", "adapter_spec"),
    [("pending", SPEC), *invalid_anchor_specs()],
    ids=lambda value: value if isinstance(value, str) else None,
)
def test_unverified_adapter_refuses_before_any_network_call(
    monkeypatch, capsys, case, adapter_spec
) -> None:
    ref = f"{SERIES}.2027.first_print.current_law"
    forecast = {"resolutionDate": "2028-12-31", "unit": "percent"}
    registration = {
        "contract": {
            "resolutionDateBasis": "resolve-by-bound",
            "sourceBinding": {
                **resolve_pending.census_spm_binding_template(SPEC),
                "allowedHosts": ["www.census.gov", "www2.census.gov"],
                "expectedReleaseWindow": {
                    "start": "2028-08-01",
                    "end": "2028-12-31",
                },
            },
        }
    }
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
                "census_spm",
                adapter_spec,
                "year",
                "2027",
                "2028-12-31",
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
        resolve_pending, "registration_contracts", lambda: {ref: registration}
    )
    monkeypatch.setattr(
        resolve_pending, "utc_now", lambda: "2028-08-01T12:00:00Z"
    )

    def unexpected_fetch(*_args, **_kwargs):
        raise AssertionError("unverified Census SPM adapter made a network call")

    monkeypatch.setattr(resolve_pending, "http_get", unexpected_fetch)
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])

    assert resolve_pending.main() == 0
    output = capsys.readouterr().out
    message = (
        "  CENSUS SPM ADAPTER UNVERIFIED (refusing): "
        f"{ref} — all six 2019-2024 official-source anchors, with "
        "transition-discriminating 2019 and 2020 values, are required"
    )
    assert message in output.splitlines(), case
    assert "nothing new to record" in output


def test_absent_basis_census_contract_cannot_inherit_bounded_adapter() -> None:
    ref = f"{SERIES}.2027.first_print.current_law"
    registration = {
        "contract": {
            "dataPointId": ref,
            "sourceBinding": {"adapter": "census-spm-annual-report"},
        }
    }

    assert resolve_pending.effective_resolution_date_basis(
        ref, registration, SPEC
    ) == (
        None,
        "absent registered basis defaults to 'release-calendar'; adapter "
        "basis 'resolve-by-bound' may be inherited only by the two legacy "
        "IRS-SOI targets with adapter 'irs-soi-pub1304': "
        f"{ref}",
    )


def test_mutable_census_adapter_has_no_late_capture_bypass() -> None:
    ref = f"{SERIES}.2027.first_print.current_law"
    window = {"start": "2028-08-01", "end": "2028-12-31"}

    assert resolve_pending.bounded_resolution_window_gate(
        ref,
        resolve_pending.dt.date(2029, 1, 1),
        window,
    ) == (
        "missed",
        f"  FIRST-PRINT WINDOW MISSED (refusing): {ref} — registered window "
        "closed 2028-12-31; no release-time witnessed or versioned "
        "first-print custody is registered",
    )


@pytest.mark.parametrize("timing", ["open", "crosses-window-end", "missed"])
def test_verified_adapter_applies_mutable_window_to_both_arms(
    monkeypatch, capsys, timing
) -> None:
    refs = [
        f"{SERIES}.2027.first_print.threshold_one_dollar",
        f"{SERIES}.2027.first_print.current_law",
    ]
    armed_spec = {
        **SPEC,
        "anchor_status": "VERIFIED_REVISED_METHODOLOGY",
        "anchors": corrected_anchor_fixture(),
    }
    binding = {
        **resolve_pending.census_spm_binding_template(armed_spec),
        "allowedHosts": ["www.census.gov", "www2.census.gov"],
        "expectedReleaseWindow": {
            "start": "2028-08-01",
            "end": "2028-12-31",
        },
    }
    registrations = {
        ref: {
            "contract": {
                "series": SERIES,
                "period": "2027",
                "resolutionDateBasis": "resolve-by-bound",
                "sourceBinding": binding,
            },
            "targetContentHash": str(index) * 64,
        }
        for index, ref in enumerate(refs, start=1)
    }
    forecasts = [
        {"resolutionDate": "2028-12-31", "unit": "percent"}
        for _ref in refs
    ]
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
            (ref, "census_spm", armed_spec, "year", "2027", "2028-12-31", forecast)
            for ref, forecast in zip(refs, forecasts)
        ],
    )
    monkeypatch.setattr(
        resolve_pending,
        "ledger_state",
        lambda *_args: ("", "blob", "a" * 40),
    )
    monkeypatch.setattr(
        resolve_pending, "registration_contracts", lambda: registrations
    )
    if timing == "crosses-window-end":
        moments = iter(
            ["2028-12-31T23:59:59Z", "2029-01-01T00:00:01Z"]
        )
        monkeypatch.setattr(
            resolve_pending,
            "utc_now",
            lambda: next(moments, "2029-01-01T00:00:01Z"),
        )
    elif timing == "missed":
        monkeypatch.setattr(
            resolve_pending, "utc_now", lambda: "2029-01-01T00:00:01Z"
        )
    else:
        monkeypatch.setattr(
            resolve_pending, "utc_now", lambda: "2028-09-15T12:00:00Z"
        )
    fetches: list[tuple[str, bool]] = []

    def fake_fetch(spec, year, *, require_latest=False):
        assert spec is armed_spec
        fetches.append((year, require_latest))
        return (
            11.0,
            b"authenticated-workbook",
            "https://www2.census.gov/programs-surveys/demo/tables/p60/300/"
            "tableB-2.xlsx",
            "2028-09-15T12:00:02Z",
            None,
        )

    monkeypatch.setattr(resolve_pending, "census_spm_fetch_year", fake_fetch)
    monkeypatch.setattr(
        resolve_pending,
        "census_spm_xlsx_grid",
        lambda raw, spec: ([raw, spec], None),
    )
    anchor_values = armed_spec["anchors"]
    monkeypatch.setattr(
        resolve_pending,
        "census_spm_rate_from_grid",
        lambda _grid, year, _spec, *, report_year=None: (
            anchor_values[year],
            None,
        ),
    )
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])

    assert resolve_pending.main() == 0
    assert fetches == (
        [] if timing == "missed" else [("2027", True)]
    )
    output = capsys.readouterr().out
    if timing != "open":
        refusals = {
            line
            for line in output.splitlines()
            if line.startswith("  FIRST-PRINT WINDOW MISSED (refusing):")
        }
        assert refusals == {
            "  FIRST-PRINT WINDOW MISSED (refusing): "
            f"{SERIES}.2027.first_print.threshold_one_dollar — registered "
            "window closed 2028-12-31; no release-time witnessed or "
            "versioned first-print custody is registered",
            "  FIRST-PRINT WINDOW MISSED (refusing): "
            f"{SERIES}.2027.first_print.current_law — registered window "
            "closed 2028-12-31; no release-time witnessed or versioned "
            "first-print custody is registered",
        }
        assert "LATE FIRST-PRINT CAPTURE (recording)" not in output
        assert "nothing new to record" in output
    else:
        assert output.count("resolve census.spm.child_poverty_rate.2027") == 2
        assert "dry-run: would append 2 row(s)" in output


def test_fact_separates_methodology_announcement_from_observed_workbook() -> None:
    ref = f"{SERIES}.2027.first_print.current_law"
    table_url = (
        "https://www2.census.gov/programs-surveys/demo/tables/p60/300/"
        "tableB-2.xlsx"
    )
    fact = resolve_pending.generic_fact(
        ref,
        SPEC,
        "year",
        "2027",
        13.4,
        resolve_pending.dt.date(2028, 9, 15),
        SPEC["source_url"],
        table_url,
    )

    assert fact["measure"]["concept"] == SERIES
    assert fact["measure"]["unit"] == "percent"
    assert fact["source"]["url"] == SPEC["source_url"]
    assert fact["source"]["source_file"] == table_url
    assert fact["value"] == 13.4
    assert (
        resolve_pending.binding_adapter_mismatch(
            "census_spm",
            {
                "contract": {
                    "sourceBinding": {"adapter": "census-spm-annual-report"}
                }
            },
        )
        is None
    )
    assert (
        resolve_pending.binding_adapter_mismatch(
            "census_spm",
            {"contract": {"sourceBinding": {"adapter": "generic-url"}}},
        )
        == "generic-url"
    )
