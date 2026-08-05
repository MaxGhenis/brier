from __future__ import annotations

import copy
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
                "start": "2027-09-01",
                "end": "2027-12-31",
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


def test_spm_pair_current_template_is_rejected_by_strict_chronology(
    capsys: pytest.CaptureFixture[str],
) -> None:
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
    assert [
        (arm["conditionId"], arm["conditional"])
        for arm in entry["conditionalPair"]["arms"]
    ] == [
        (arm["conditionId"], arm["conditional"])
        for arm in irs_entry["conditionalPair"]["arms"]
    ]

    targets = roll_docket.conditional_pair_seed_targets(
        entry, set(), roll_docket.dt.date(2026, 8, 4)
    )
    assert targets == []
    assert capsys.readouterr().err == (
        "  warning: skip census.spm.child_poverty_rate: conditional pair "
        "release window must open after the condition deadline\n"
    )


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
    assert url is None and "first-print window was missed" in refusal

    url, refusal = resolve_pending.census_spm_report_url(
        b'<a href="https://example.com/library/publications/2025/demo/'
        b'p60-287.html">'
        b"Poverty in the United States: 2024</a>",
        "2024",
        publications_url=SPEC["publications_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert url is None and "not in adapter allowlist" in refusal


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
    assert url is None and "no reviewed Table B-2 XLSX" in refusal

    wrong_report_number = report.replace(b"/p60/287/", b"/p60/999/")
    url, refusal = resolve_pending.census_spm_table_url(
        wrong_report_number,
        "2024",
        report_url=report_url,
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert url is None and "not the reviewed" in refusal


def test_report_publication_date_and_first_print_window_fail_closed() -> None:
    report = b"""
      <h1>Poverty in the United States: 2024</h1>
      <p>September <strong>09</strong>, 2025</p>
      <footer>Page Last Revised - August 13, 2025</footer>
    """
    publication_day, refusal = (
        resolve_pending.census_spm_report_publication_date(report, "2024")
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
    assert "missed the 21-day first-print window" in refusal


def test_real_table_orientation_and_merged_headers_parse_exact_child_rate() -> None:
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


def test_table_parser_fails_closed_on_wrong_identity_and_ambiguity() -> None:
    grid, refusal = resolve_pending.census_spm_xlsx_grid(
        synthetic_workbook(), SPEC
    )
    assert refusal is None

    _, refusal = resolve_pending.census_spm_rate_from_grid(grid, "2023", SPEC)
    assert "ending in report year 2023" in refusal

    duplicate_column = copy.deepcopy(grid)
    duplicate_column[3][10] = "Under 18 years"
    duplicate_column[4][10] = "Below Poverty"
    duplicate_column[5][10] = "Percent"
    _, refusal = resolve_pending.census_spm_rate_from_grid(
        duplicate_column, "2024", SPEC
    )
    assert "found 2" in refusal

    duplicate_year = copy.deepcopy(grid)
    duplicate_year.insert(10, [2024.0, *("" for _ in range(8)), 99.0])
    _, refusal = resolve_pending.census_spm_rate_from_grid(
        duplicate_year, "2024", SPEC
    )
    assert "inside ALL RACES, found 2" in refusal

    bad_value = copy.deepcopy(grid)
    bad_value[7][9] = "13.4 percent"
    _, refusal = resolve_pending.census_spm_rate_from_grid(
        bad_value, "2024", SPEC
    )
    assert "not in [0, 100]" in refusal

    bad_arithmetic = copy.deepcopy(grid)
    bad_arithmetic[7][7] = 5000.0
    _, refusal = resolve_pending.census_spm_rate_from_grid(
        bad_arithmetic, "2024", SPEC
    )
    assert "arithmetic cross-check" in refusal

    _, refusal = resolve_pending.census_spm_xlsx_grid(
        synthetic_workbook(sheet_name="Table B-3"), SPEC
    )
    assert "exactly one Table B-2 sheet" in refusal


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
    assert "redirected away from the exact indexed P60 artifact" in refusal

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
    assert "missed the 21-day first-print window" in refusal


def test_revised_anchor_admission_and_exact_comparison() -> None:
    assert "anchors" not in SPEC
    assert resolve_pending.census_spm_verified_anchors(SPEC) is None
    verified = {
        **SPEC,
        "anchor_status": "VERIFIED_REVISED_METHODOLOGY",
        # Synthetic values only. The pre-correction 13.4% 2024 print must
        # never be mistaken for a revised-methodology anchor.
        "anchors": {"2022": 10.1, "2023": 10.2, "2024": 10.3},
    }
    anchors = resolve_pending.census_spm_verified_anchors(verified)
    assert anchors == {"2022": 10.1, "2023": 10.2, "2024": 10.3}
    assert resolve_pending.census_spm_anchor_mismatches(anchors, anchors) == []
    assert resolve_pending.census_spm_anchor_mismatches(
        {**anchors, "2024": 10.4}, anchors
    ) == ["2024=10.4 (official 10.3)"]
    for bad in (
        {**verified, "anchor_status": "VERIFIED"},
        {**verified, "anchors": {"2023": 10.2, "2024": 10.3}},
        {
            **verified,
            "anchors": {"2018": 10.0, "2023": 10.2, "2024": 10.3},
        },
        {
            **verified,
            "anchors": {"2022": 10.1, "2023": 10.2, "2024": True},
        },
    ):
        assert resolve_pending.census_spm_verified_anchors(bad) is None


def test_both_condition_arms_route_to_one_annual_print() -> None:
    refs = [
        f"{SERIES}.2026.first_print.threshold_one_dollar",
        f"{SERIES}.2026.first_print.current_law",
    ]
    log = {
        "entries": [
            {
                "kind": "prediction_recorded",
                "forecastSlug": f"spm-arm-{index}",
                "resolutionDate": "2027-12-31",
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
        ("census_spm", "year", "2026")
    }


def test_unverified_adapter_refuses_before_any_network_call(
    monkeypatch, capsys
) -> None:
    ref = f"{SERIES}.2026.first_print.current_law"
    forecast = {"resolutionDate": "2027-12-31", "unit": "percent"}
    registration = {
        "contract": {
            "resolutionDateBasis": "resolve-by-bound",
            "sourceBinding": {
                **resolve_pending.census_spm_binding_template(SPEC),
                "allowedHosts": ["www.census.gov", "www2.census.gov"],
                "expectedReleaseWindow": {
                    "start": "2027-09-01",
                    "end": "2027-12-31",
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
            (ref, "census_spm", SPEC, "year", "2026", "2027-12-31", forecast)
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
        resolve_pending, "utc_now", lambda: "2027-09-01T12:00:00Z"
    )

    def unexpected_fetch(*_args, **_kwargs):
        raise AssertionError("unverified Census SPM adapter made a network call")

    monkeypatch.setattr(resolve_pending, "http_get", unexpected_fetch)
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])

    assert resolve_pending.main() == 0
    output = capsys.readouterr().out
    assert "CENSUS SPM ADAPTER UNVERIFIED" in output
    assert "nothing new to record" in output


def test_absent_basis_census_contract_cannot_inherit_bounded_adapter() -> None:
    ref = f"{SERIES}.2026.first_print.current_law"
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


def test_mutable_census_adapter_cannot_claim_immutable_late_capture() -> None:
    ref = f"{SERIES}.2026.first_print.current_law"
    window = {"start": "2027-09-01", "end": "2027-12-31"}
    registration = {
        "contract": {
            "sourceBinding": {
                **resolve_pending.census_spm_binding_template(SPEC),
                "allowedHosts": ["www.census.gov", "www2.census.gov"],
                "expectedReleaseWindow": window,
            }
        }
    }
    spoofed = {
        **SPEC,
        "late_capture_capability": (
            resolve_pending.IMMUTABLE_ARTIFACT_LATE_CAPTURE
        ),
    }

    assert not resolve_pending.authenticated_late_capture_capability(
        registration, spoofed
    )
    assert resolve_pending.bounded_resolution_window_gate(
        ref,
        resolve_pending.dt.date(2028, 1, 1),
        window,
        registration=registration,
        spec=spoofed,
    ) == (
        "missed",
        f"  FIRST-PRINT WINDOW MISSED (refusing): {ref} — registered window "
        "closed 2027-12-31; adapter has no authenticated immutable-artifact "
        "late-capture capability",
    )


@pytest.mark.parametrize("timing", ["open", "crosses-window-end", "missed"])
def test_verified_adapter_applies_mutable_window_to_both_arms(
    monkeypatch, capsys, timing
) -> None:
    refs = [
        f"{SERIES}.2026.first_print.threshold_one_dollar",
        f"{SERIES}.2026.first_print.current_law",
    ]
    armed_spec = {
        **SPEC,
        "anchor_status": "VERIFIED_REVISED_METHODOLOGY",
        "anchors": {"2022": 10.1, "2023": 10.2, "2024": 10.3},
    }
    binding = {
        **resolve_pending.census_spm_binding_template(armed_spec),
        "allowedHosts": ["www.census.gov", "www2.census.gov"],
        "expectedReleaseWindow": {
            "start": "2027-09-01",
            "end": "2027-12-31",
        },
    }
    registrations = {
        ref: {
            "contract": {
                "series": SERIES,
                "period": "2026",
                "resolutionDateBasis": "resolve-by-bound",
                "sourceBinding": binding,
            },
            "targetContentHash": str(index) * 64,
        }
        for index, ref in enumerate(refs, start=1)
    }
    forecasts = [
        {"resolutionDate": "2027-12-31", "unit": "percent"}
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
            (ref, "census_spm", armed_spec, "year", "2026", "2027-12-31", forecast)
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
            ["2027-12-31T23:59:59Z", "2028-01-01T00:00:01Z"]
        )
        monkeypatch.setattr(
            resolve_pending,
            "utc_now",
            lambda: next(moments, "2028-01-01T00:00:01Z"),
        )
    elif timing == "missed":
        monkeypatch.setattr(
            resolve_pending, "utc_now", lambda: "2028-01-01T00:00:01Z"
        )
    else:
        monkeypatch.setattr(
            resolve_pending, "utc_now", lambda: "2027-09-15T12:00:00Z"
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
            "2027-09-15T12:00:02Z",
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
        [] if timing == "missed" else [("2026", True)]
    )
    output = capsys.readouterr().out
    if timing != "open":
        message = (
            "  FIRST-PRINT WINDOW MISSED (refusing): "
            f"{SERIES}.2026.first_print.current_law — registered window "
            "closed 2027-12-31; adapter has no authenticated immutable-"
            "artifact late-capture capability"
        )
        assert message in output
        assert output.count("FIRST-PRINT WINDOW MISSED (refusing)") == 2
        assert "LATE FIRST-PRINT CAPTURE (recording)" not in output
        assert "nothing new to record" in output
    else:
        assert output.count("resolve census.spm.child_poverty_rate.2026") == 2
        assert "dry-run: would append 2 row(s)" in output


def test_spec_builds_a_percent_fact_bound_to_the_announcement() -> None:
    ref = f"{SERIES}.2026.first_print.current_law"
    table_url = (
        "https://www2.census.gov/programs-surveys/demo/tables/p60/300/"
        "tableB-2.xlsx"
    )
    fact = resolve_pending.generic_fact(
        ref,
        SPEC,
        "year",
        "2026",
        13.4,
        resolve_pending.dt.date(2027, 9, 15),
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
