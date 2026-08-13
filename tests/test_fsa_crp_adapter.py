from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import subprocess
import sys
import urllib.request
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
RECOVERY_ROOT = FIXTURE_ROOT / "recovery_2026_08_13"
RECOVERY_FIXTURE_PINS = {
    "stale-statistics-301.html": (
        470,
        "4187ac28fa28499314920d3beb9cd5774b51727bbbefa888a972328c96616a91",
    ),
    "crp-statistics.html": (
        121_040,
        "f0e572b484359368042634d7413937acd174d53434667f55b092382b8a73c181",
    ),
    "april-2026-document.html": (
        62_639,
        "6b076bd7e94e13bc3d32ddf9663c80201c2c94f6a1c3eebf6ce4a5ce064df695",
    ),
    "CRPMonthlyApril2026WithPageNumbers.pdf": (
        5_356_828,
        "03ac66bd80f263cdaa221295eb17963fbb9be0574b846fd11f6024ca0ee4e373",
    ),
}

APRIL_DOCUMENT_URL = "https://www.fsa.usda.gov/documents/april-2026-crp-monthly-summary"
APRIL_PDF_URL = (
    "https://www.fsa.usda.gov/sites/default/files/2026-07/"
    "CRPMonthlyApril2026WithPageNumbers.pdf"
)


def test_fsa_crp_adapter_and_docket_share_the_exact_seven_key_binding() -> None:
    docket = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    entry = next(e for e in docket["series"] if e["series"] == SERIES)
    binding = entry["extras"]["sourceBinding"]

    assert "fsa-crp-monthly-summary" in register_targets.SOURCE_ADAPTERS
    assert prospect_targets._source_binding_errors(binding) == []
    assert set(binding) == SOURCE_BINDING_TEMPLATE_KEYS
    assert SPEC["source_url"] == resolve_pending.FSA_CRP_LANDING_URL
    assert binding["sourceUrl"] == (
        "https://www.fsa.usda.gov/tools/informational/reports/"
        "conservation-statistics/crp"
    )
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
    assert not resolve_pending.fsa_crp_binding_matches_spec(
        {
            **binding,
            "sourceUrl": resolve_pending.FSA_CRP_STALE_LANDING_URL,
        },
        SPEC,
    )


def _monthly_summaries_table(
    *,
    june_summary: str = "/documents/june-2026-crp-monthly-summary",
    extra_june_summary: str | None = None,
    duplicate_june_row: bool = False,
) -> bytes:
    extra_link = (
        f'<a href="{extra_june_summary}">duplicate summary</a>'
        if extra_june_summary
        else ""
    )
    duplicate_row = (
        """
        <tr>
          <th>June 2026</th>
          <td><a href="/documents/june-2026-crp-monthly-summary-copy">PDF</a></td>
          <td><a href="/documents/june-2026-crp-monthly-onepager-copy">PDF</a></td>
        </tr>
        """
        if duplicate_june_row
        else ""
    )
    return f"""
    <html><body>
      <table>
        <thead><tr>
          <th>Month/Year</th><th>Summary</th><th>One-pager</th>
        </tr></thead>
        <tbody>
          <tr>
            <th>May 2026</th>
            <td><a href="/documents/may-2026-crp-monthly-summary">PDF</a></td>
            <td><a href="/documents/may-2026-crp-monthly-onepager">PDF</a></td>
          </tr>
          <tr>
            <th>June 2026</th>
            <td><a href="{june_summary}">PDF</a>{extra_link}</td>
            <td><a href="/documents/june-2026-crp-monthly-onepager">PDF</a></td>
          </tr>
          {duplicate_row}
        </tbody>
      </table>
    </body></html>
    """.encode()


def _june_document_page(*artifact_urls: str) -> bytes:
    links = "".join(f'<a href="{url}">Download</a>' for url in artifact_urls)
    return f"<html><body>{links}</body></html>".encode()


def test_fsa_crp_structurally_selects_summary_document_then_pdf() -> None:
    document_url, refusal = resolve_pending.fsa_crp_summary_document_url(
        _monthly_summaries_table(),
        "2026-06",
        landing_url=SPEC["source_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )

    assert refusal is None
    assert document_url == (
        "https://www.fsa.usda.gov/documents/june-2026-crp-monthly-summary"
    )

    pdf_url = (
        "https://www.fsa.usda.gov/sites/default/files/2026-07/"
        "CRPMonthlyJune2026WithPageNumbers.pdf"
    )
    url, refusal = resolve_pending.fsa_crp_document_pdf_url(
        _june_document_page(pdf_url, pdf_url),
        "2026-06",
        document_url=document_url,
        allowed_hosts=SPEC["allowed_hosts"],
    )

    assert refusal is None
    assert url == pdf_url


@pytest.mark.parametrize(
    ("url", "kind", "message"),
    [
        (
            resolve_pending.FSA_CRP_STALE_LANDING_URL,
            "landing",
            "exact reviewed path",
        ),
        (
            f"{resolve_pending.FSA_CRP_LANDING_URL}/",
            "landing",
            "empty or dot segments",
        ),
        # 2026-08-13 review probes: noncanonical shapes must refuse
        # BEFORE any decode — a second decoder downstream must never be
        # able to reveal traversal or separators validation did not see.
        (
            "https://www.fsa.usda.gov/sites/default/files/2026-07/"
            "%252e%252e%252fdocuments%252fCRPMonthlyApril2026.pdf",
            "artifact",
            "canonical form",
        ),
        (
            "https://www.fsa.usda.gov/sites/default/files/2026-07/"
            "CRPMonthlyApril2026%252f..%252fsecret.pdf",
            "artifact",
            "canonical form",
        ),
        (
            "https://www.fsa.usda.gov/SITES/DEFAULT/FILES/2026-07/"
            "CRPMonthlyApril2026WithPageNumbers.pdf",
            "artifact",
            "outside the reviewed class",
        ),
        (
            "https://www.fsa.usda.gov/tools/informational/reports/"
            "conservation-statistics/crp;download",
            "landing",
            "canonical form",
        ),
        (
            "https://www.fsa.usda.gov/sites/default/files/2026-07/"
            "CRPMonthly%41pril2026.pdf",
            "artifact",
            "canonical form",
        ),
        (
            "https://www.fsa.usda.gov/sites/default/files/2026-07/..%2fsecret.pdf",
            "artifact",
            "canonical form",
        ),
        (
            "https://www.fsa.usda.gov/sites/default/files/2026-07/"
            "CRPMonthly\\April2026.pdf",
            "artifact",
            "canonical form",
        ),
        (
            "https://www.fsa.usda.gov/sites/default/files/2026-07/../"
            "2026-08/CRPMonthlyApril2026.pdf",
            "artifact",
            "empty or dot segments",
        ),
        (
            "https://www.fsa.usda.gov/sites//default/files/2026-07/"
            "CRPMonthlyApril2026.pdf",
            "artifact",
            "empty or dot segments",
        ),
        (
            "https://www.fsa.usda.gov/documents/APRIL-2026-document",
            "document",
            "outside the reviewed class",
        ),
        (
            "https://www.fsa.usda.gov/sites/default/files/2026-07/"
            "CRPMonthlyApril2026.PDF",
            "artifact",
            "outside the reviewed class",
        ),
        (
            f"{resolve_pending.FSA_CRP_LANDING_URL}?download=1",
            "landing",
            "canonical form",
        ),
        (
            "http://www.fsa.usda.gov/tools/informational/reports/"
            "conservation-statistics/crp",
            "landing",
            "canonical form",
        ),
        (
            "https://example.com/tools/informational/reports/"
            "conservation-statistics/crp",
            "landing",
            "allowlist",
        ),
        (
            "https://www.fsa.usda.gov:443/tools/informational/reports/"
            "conservation-statistics/crp",
            "landing",
            "port",
        ),
        (
            "https://www.fsa.usda.gov/sites/default/files/2026-07/"
            "CRPMonthlyApril2026WithPageNumbers.pdf",
            "document",
            "document path",
        ),
        (
            "https://www.fsa.usda.gov/sites/default/files/documents/"
            "CRPMonthlyApril2026WithPageNumbers.pdf",
            "artifact",
            "artifact path",
        ),
        (
            "https://www.fsa.usda.gov/sites/default/files/2026-07/nested/"
            "CRPMonthlyApril2026WithPageNumbers.pdf",
            "artifact",
            "artifact path",
        ),
    ],
)
def test_fsa_crp_url_kind_allowlist_rejects_unreviewed_urls(
    url: str, kind: str, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        resolve_pending._require_fsa_crp_url_kind(
            url,
            kind,
            SPEC["allowed_hosts"],
        )


@pytest.mark.parametrize(
    ("url", "kind"),
    [
        (resolve_pending.FSA_CRP_LANDING_URL, "landing"),
        (APRIL_DOCUMENT_URL, "document"),
        (APRIL_PDF_URL, "artifact"),
    ],
)
def test_fsa_crp_url_kind_allowlist_accepts_reviewed_classes(
    url: str, kind: str
) -> None:
    resolve_pending._require_fsa_crp_url_kind(
        url,
        kind,
        SPEC["allowed_hosts"],
    )


def test_fsa_crp_redirect_handler_refuses_every_redirect() -> None:
    request = urllib.request.Request(resolve_pending.FSA_CRP_LANDING_URL)
    handler = resolve_pending._FsaCrpNoRedirectHandler(
        "landing",
        SPEC["allowed_hosts"],
    )

    with pytest.raises(ValueError, match="redirects are not allowed"):
        handler.redirect_request(
            request,
            None,
            301,
            "Moved Permanently",
            {},
            resolve_pending.FSA_CRP_LANDING_URL,
        )

    with pytest.raises(ValueError, match="exact reviewed path"):
        handler.redirect_request(
            request,
            None,
            301,
            "Moved Permanently",
            {},
            resolve_pending.FSA_CRP_STALE_LANDING_URL,
        )


def test_fsa_crp_landing_selection_fails_closed() -> None:
    document_url, refusal = resolve_pending.fsa_crp_summary_document_url(
        _monthly_summaries_table(
            extra_june_summary="/documents/june-2026-crp-monthly-summary-copy"
        ),
        "2026-06",
        landing_url=SPEC["source_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert document_url is None and "found 2" in refusal

    document_url, refusal = resolve_pending.fsa_crp_summary_document_url(
        _monthly_summaries_table(duplicate_june_row=True),
        "2026-06",
        landing_url=SPEC["source_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert document_url is None and "found 2" in refusal

    document_url, refusal = resolve_pending.fsa_crp_summary_document_url(
        _monthly_summaries_table(
            june_summary=("https://example.com/documents/june-2026-crp-monthly-summary")
        ),
        "2026-06",
        landing_url=SPEC["source_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert document_url is None and "not in adapter allowlist" in refusal

    document_url, refusal = resolve_pending.fsa_crp_summary_document_url(
        _monthly_summaries_table(
            june_summary="/documents/june-2026-crp-monthly-onepager"
        ),
        "2026-06",
        landing_url=SPEC["source_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert document_url is None and "does not authenticate" in refusal

    document_url, refusal = resolve_pending.fsa_crp_summary_document_url(
        _monthly_summaries_table(),
        "2026-07",
        landing_url=SPEC["source_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert (document_url, refusal) == (None, None)


def test_fsa_crp_document_selection_fails_closed() -> None:
    document_url = "https://www.fsa.usda.gov/documents/june-2026-crp-monthly-summary"
    pdf_url = (
        "https://www.fsa.usda.gov/sites/default/files/2026-07/"
        "CRPMonthlyJune2026WithPageNumbers.pdf"
    )
    second_pdf_url = (
        "https://www.fsa.usda.gov/sites/default/files/2026-08/"
        "CRPMonthlyJune2026WithPageNumbers.pdf"
    )
    url, refusal = resolve_pending.fsa_crp_document_pdf_url(
        _june_document_page(pdf_url, second_pdf_url),
        "2026-06",
        document_url=document_url,
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert url is None and "found 2" in refusal

    off_host = pdf_url.replace("www.fsa.usda.gov", "example.com")
    url, refusal = resolve_pending.fsa_crp_document_pdf_url(
        _june_document_page(off_host),
        "2026-06",
        document_url=document_url,
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert url is None and "not in adapter allowlist" in refusal

    legacy_path = pdf_url.replace("/2026-07/", "/documents/")
    url, refusal = resolve_pending.fsa_crp_document_pdf_url(
        _june_document_page(legacy_path),
        "2026-06",
        document_url=document_url,
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert url is None and "outside the reviewed class" in refusal

    one_pager = pdf_url.replace("WithPageNumbers.pdf", "CRPOnePager.pdf")
    url, refusal = resolve_pending.fsa_crp_document_pdf_url(
        _june_document_page(one_pager),
        "2026-06",
        document_url=document_url,
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert url is None and "found 0" in refusal


def test_fsa_crp_recovery_fixtures_are_byte_and_hash_pinned() -> None:
    for name, (expected_size, expected_sha256) in RECOVERY_FIXTURE_PINS.items():
        raw = (RECOVERY_ROOT / name).read_bytes()
        assert len(raw) == expected_size
        assert hashlib.sha256(raw).hexdigest() == expected_sha256


def test_fsa_crp_recovery_fixtures_replay_through_real_pdf_parser() -> None:
    document_url, refusal = resolve_pending.fsa_crp_summary_document_url(
        (RECOVERY_ROOT / "crp-statistics.html").read_bytes(),
        "2026-04",
        landing_url=SPEC["source_url"],
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert (document_url, refusal) == (APRIL_DOCUMENT_URL, None)

    pdf_url, refusal = resolve_pending.fsa_crp_document_pdf_url(
        (RECOVERY_ROOT / "april-2026-document.html").read_bytes(),
        "2026-04",
        document_url=document_url,
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert (pdf_url, refusal) == (APRIL_PDF_URL, None)

    text, refusal = resolve_pending.fsa_crp_pdf_text(
        (RECOVERY_ROOT / "CRPMonthlyApril2026WithPageNumbers.pdf").read_bytes()
    )
    assert refusal is None
    assert text is not None
    value, refusal = resolve_pending.fsa_crp_value_from_text(text, "2026-04")
    assert (value, refusal) == (26_182_019, None)


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
    document_url = "https://www.fsa.usda.gov/documents/june-2026-crp-monthly-summary"
    pdf_url = (
        "https://www.fsa.usda.gov/sites/default/files/2026-07/"
        "CRPMonthlyJune2026WithPageNumbers.pdf"
    )
    landing = _monthly_summaries_table()
    document = _june_document_page(pdf_url)
    pdf = b"%PDF-synthetic"
    calls: list[tuple[str, str]] = []

    def fake_get(url, *, kind, allowed_hosts, timeout=120):
        assert allowed_hosts == SPEC["allowed_hosts"]
        assert timeout == 120
        calls.append((kind, url))
        if url == SPEC["source_url"]:
            return landing, "2026-07-10T13:40:00Z", url
        if url == document_url:
            return document, "2026-07-10T13:40:01Z", url
        assert url == pdf_url
        return pdf, "2026-07-10T13:40:02Z", url

    monkeypatch.setattr(resolve_pending, "fsa_crp_http_get", fake_get)
    monkeypatch.setattr(resolve_pending, "fsa_crp_pdf_text", lambda _: (text, None))

    value, raw, source_url, retrieved_at, refusal = (
        resolve_pending.fsa_crp_fetch_period(SPEC, "2026-06")
    )

    assert calls == [
        ("landing", SPEC["source_url"]),
        ("document", document_url),
        ("artifact", pdf_url),
    ]
    assert value == 23_456_789
    assert raw == pdf
    assert source_url == pdf_url
    assert retrieved_at == "2026-07-10T13:40:02Z"
    assert refusal is None


def test_fsa_crp_stale_landing_refuses_before_network(monkeypatch) -> None:
    calls: list[str] = []

    def unexpected_get(url, **_kwargs):
        calls.append(url)
        raise AssertionError("stale URL must refuse before network access")

    monkeypatch.setattr(resolve_pending, "fsa_crp_http_get", unexpected_get)
    stale_spec = {
        **SPEC,
        "source_url": resolve_pending.FSA_CRP_STALE_LANDING_URL,
    }

    value, raw, source_url, _retrieved_at, refusal = (
        resolve_pending.fsa_crp_fetch_period(stale_spec, "2026-06")
    )

    assert (value, raw) == (None, None)
    assert source_url == resolve_pending.FSA_CRP_STALE_LANDING_URL
    assert "landing fetch failed" in refusal
    assert "exact reviewed path" in refusal
    assert calls == []


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


def test_fsa_crp_conditional_pair_arms_route_to_one_monthly_print() -> None:
    refs = [
        (
            f"{SERIES}.2027_09.first_print."
            "ceiling_27_million_source_recovered_2026_08_13"
        ),
        (
            f"{SERIES}.2027_09.first_print."
            "no_fy2027_31_ceiling_source_recovered_2026_08_13"
        ),
    ]
    docket = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    entry = next(e for e in docket["series"] if e["series"] == SERIES)
    assert [arm["dataPointId"] for arm in entry["conditionalPair"]["arms"]] == refs
    assert all(ref.endswith("_source_recovered_2026_08_13") for ref in refs)
    log = {
        "entries": [
            {
                "kind": "prediction_recorded",
                "forecastSlug": f"crp-arm-{index}",
                "resolutionDate": "2027-12-31",
                "unit": "count",
            }
            for index in range(2)
        ],
        "resolutionLinks": [
            {
                "status": "pending",
                "forecastSlug": f"crp-arm-{index}",
                "targetFactRef": ref,
            }
            for index, ref in enumerate(refs)
        ],
    }

    todo = resolve_pending.pending_adapter_refs(log)

    assert [row[0] for row in todo] == refs
    assert {(row[1], row[3], row[4]) for row in todo} == {
        ("fsa_crp", "month", "2027-09")
    }


def test_fsa_crp_spec_builds_a_level_fact_without_reusing_binding_transform() -> None:
    fact = resolve_pending.generic_fact(
        f"{SERIES}.june_2026.first_print",
        SPEC,
        "month",
        "2026-06",
        23_456_789,
        resolve_pending.dt.date(2026, 7, 10),
        SPEC["source_url"],
        (
            "https://www.fsa.usda.gov/sites/default/files/2026-07/"
            "CRPMonthlyJune2026WithPageNumbers.pdf"
        ),
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


@pytest.mark.parametrize(
    "url",
    [
        "https://www.fsa.usda.gov/tools/informational/reports/"
        "conservation\t-statistics/crp",
        "https://www.fsa.usda.gov/tools/informational/reports/"
        "conservation\n-statistics/crp",
        "https://www.fsa.usda.gov/tools/informational/reports/"
        "conservation\r-statistics/crp",
        "https://www.fsa.usda.gov/tools/informational/reports/"
        "conservation-statistics/crp;",
        "https://www.fsa.usda.gov/tools/informational/reports/"
        "conservation-statistics/crp?",
        "https://www.fsa.usda.gov/tools/informational/reports/"
        "conservation-statistics/crp#",
        "https://www.fsa.usda.gov:/tools/informational/reports/"
        "conservation-statistics/crp",
    ],
)
def test_lossy_parse_shapes_refuse_before_transport(
    url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Round-2 review: urlparse strips embedded TAB/LF/CR and tolerates
    # bare ;/?/#/port components, so post-parse checks validated a
    # different string than the transport used — TAB, LF, and CR probes
    # reached the mocked opener. The raw-string guard must refuse
    # BEFORE any parser or socket: the tripwire below detonates if the
    # transport is ever reached.
    def tripwire(*args: object, **kwargs: object) -> object:
        raise AssertionError("transport reached for a noncanonical URL")

    monkeypatch.setattr(resolve_pending.urllib.request, "build_opener", tripwire)
    with pytest.raises(ValueError, match="canonical form"):
        resolve_pending.fsa_crp_http_get(
            url, kind="landing", allowed_hosts=SPEC["allowed_hosts"]
        )


@pytest.mark.parametrize(
    ("href", "message"),
    [
        ("../sites/default/files/2026-07/CRPMonthlyApril2026.pdf", "canonical form"),
        ("/documents/../sites/x.pdf", "empty or dot segments"),
        ("//evil.example/sites/default/files/2026-07/x.pdf", "empty or dot segments"),
        ("/documents/april\t-2026", "canonical form"),
        ("documents/april-2026-crp-monthly-summary", "canonical form"),
        ("https://www.fsa.usda.gov/documents/./april-2026", "empty or dot segments"),
    ],
)
def test_raw_hrefs_refuse_before_urljoin_normalizes(href: str, message: str) -> None:
    # urljoin resolves dot segments and strips TAB/LF/CR, so a hostile
    # href can normalize into a clean URL that passes every post-join
    # check without ever being the reviewed link shape.
    with pytest.raises(ValueError, match=message):
        resolve_pending._require_fsa_crp_raw_href(href, "document")


def test_malformed_unrelated_link_is_ignored_not_crashed() -> None:
    # Round-3 review: an unrelated navigation href like "https://[broken"
    # reached urljoin before any filter or guard and raised an
    # unstructured "Invalid IPv6 URL" ValueError outside the refusal
    # envelope. Unrelated links must be filtered out untouched by any
    # parser, and selection on the REAL recovery page must still succeed.
    real_page = (RECOVERY_ROOT / "april-2026-document.html").read_bytes()
    poisoned = b'<a href="https://[broken">nav</a>' + real_page
    url, refusal = resolve_pending.fsa_crp_document_pdf_url(
        poisoned,
        "2026-04",
        document_url=APRIL_DOCUMENT_URL,
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert refusal is None
    assert url == APRIL_PDF_URL


def test_malformed_candidate_link_refuses_structurally() -> None:
    # A CRP-monthly-labeled hostile candidate must produce a STRUCTURED
    # refusal (None + message), never an unstructured exception.
    poisoned = _june_document_page(
        "../CRPMonthlyApril2026.pdf",
    )
    url, refusal = resolve_pending.fsa_crp_document_pdf_url(
        poisoned,
        "2026-04",
        document_url=APRIL_DOCUMENT_URL,
        allowed_hosts=SPEC["allowed_hosts"],
    )
    assert url is None
    assert refusal is not None and "canonical form" in refusal
