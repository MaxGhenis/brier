import json
import re
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REQUEST_ROOT = ROOT / "drafts" / "ledger-ingestion"
SBA_WORKFLOW = ".github/workflows/witness-sba-pdf.yml"
SBA_REQUESTS = (
    (
        "sba-disaster-loan-program-charge-off-amount.json",
        299_971_326,
        "usd",
    ),
    (
        "sba-disaster-loan-program-charge-off-rate-upb.json",
        3.06,
        "percent",
    ),
    (
        "sba-disaster-loan-program-post-charge-off-recovery.json",
        126_510_000,
        "usd",
    ),
)


@pytest.mark.parametrize(
    (
        "request_name",
        "adapter_family",
        "artifact_sha256",
        "artifact_byte_length",
        "page_field",
        "page",
        "fetched_value",
        "normalized_value",
        "normalized_unit",
    ),
    [
        (
            "irs-soi-credit-25e-total-claims.json",
            "irs-soi-pub4801-line-item-pdf",
            "49686f6c909452bc775bed40f10a633629e8ce486d7f47ee131cb093d1d04d81",
            4_228_018,
            "pdfPage",
            31,
            31_992,
            31_992,
            "count",
        ),
        (
            "irs-soi-credit-25e-total-credit-amount.json",
            "irs-soi-pub4801-line-item-pdf",
            "49686f6c909452bc775bed40f10a633629e8ce486d7f47ee131cb093d1d04d81",
            4_228_018,
            "pdfPage",
            32,
            96_013,
            96.013,
            "usd_millions",
        ),
        (
            "irs-soi-credit-45x-total-claims.json",
            "irs-soi-pub5108-line-item-pdf",
            "0c7516d5a784a24f51522bd3cf5358bbed735c031e54ba56c87bad831a873855",
            4_639_023,
            "pdfPage",
            167,
            9,
            9,
            "count",
        ),
        (
            "irs-soi-credit-45x-total-credit-amount.json",
            "irs-soi-pub5108-line-item-pdf",
            "0c7516d5a784a24f51522bd3cf5358bbed735c031e54ba56c87bad831a873855",
            4_639_023,
            "pdfPage",
            168,
            317_505,
            317.505,
            "usd_millions",
        ),
    ],
)
def test_deferred_pdf_requests_record_discovered_evidence_and_open_work(
    request_name: str,
    adapter_family: str,
    artifact_sha256: str,
    artifact_byte_length: int,
    page_field: str,
    page: int,
    fetched_value: int,
    normalized_value: int | float,
    normalized_unit: str,
) -> None:
    request = json.loads((REQUEST_ROOT / request_name).read_text())
    serialized = json.dumps(request)

    assert request["status"] == "proposed"
    assert request["adapterFamily"] == adapter_family
    assert "UNVERIFIED" not in serialized

    verification = request["verification"]
    assert verification["outcome"] == "proposed"
    assert verification["firstPrint"]["status"] == "not_authenticated"
    assert "custody" in " ".join(verification["requiredWork"]).lower()
    assert "parser" in " ".join(verification["requiredWork"]).lower()

    artifact = verification["artifact"]
    assert artifact["sha256"] == artifact_sha256
    assert artifact["byteLength"] == artifact_byte_length
    assert artifact[page_field] == page
    assert artifact["fetchedValue"] == fetched_value
    assert artifact["normalizedValue"] == normalized_value
    assert artifact["normalizedUnit"] == normalized_unit


@pytest.mark.parametrize(
    ("request_name", "normalized_value", "normalized_unit"),
    SBA_REQUESTS,
)
def test_sba_requests_match_the_implemented_custody_lane(
    request_name: str,
    normalized_value: int | float,
    normalized_unit: str,
) -> None:
    request = json.loads((REQUEST_ROOT / request_name).read_text())
    serialized = json.dumps(request).lower()
    verification = request["verification"]

    assert request["status"] == "proposed"
    assert request["adapterFamily"] == "sba-loan-program-performance-pdf"
    assert verification["outcome"] == "proposed"
    assert verification["firstPrint"]["status"] == "not_authenticated"
    assert verification["artifact"]["normalizedValue"] == normalized_value
    assert verification["artifact"]["normalizedUnit"] == normalized_unit

    assert SBA_WORKFLOW in request["note"]
    assert SBA_WORKFLOW in verification["firstPrint"]["blocker"]
    assert SBA_WORKFLOW in " ".join(verification["requiredWork"])
    assert "irs-soi-pub1304" not in serialized
    assert "resolve-and-rebuild" not in serialized
    assert "implement and review an sba" not in serialized
    assert "requires a new sba" not in serialized


def test_wave1_report_matches_all_30_request_outcomes() -> None:
    report = (REQUEST_ROOT / "WAVE1-REPORT.md").read_text()
    request_names = re.findall(
        r"^\|.*?`([^`]+\.json)`.*\|$",
        report,
        flags=re.MULTILINE,
    )
    outcomes = Counter(
        json.loads((REQUEST_ROOT / request_name).read_text())["status"]
        for request_name in request_names
    )

    assert len(request_names) == 30
    assert outcomes == Counter({"verified": 5, "rejected": 4, "proposed": 21})
    assert "Five requests verified cleanly, four received a" in report
    assert "and 21 remain proposals" in report
    assert SBA_WORKFLOW in report
    assert "resolve-and-rebuild" not in report
    assert "~~Add reviewed SBA PDF parsing" not in report

    for request_name, _, _ in SBA_REQUESTS:
        assert re.search(
            rf"^\| \d+ \| `{re.escape(request_name)}` \| Proposed;",
            report,
            flags=re.MULTILINE,
        )


def test_sba_recovery_request_pins_the_discovered_pdf_member() -> None:
    request = json.loads(
        (
            REQUEST_ROOT
            / "sba-disaster-loan-program-post-charge-off-recovery.json"
        ).read_text()
    )
    artifact = request["verification"]["artifact"]

    assert artifact["memberPath"] == (
        "WebsiteReports_FY25Q3/"
        "WDS_PostChargeOffRecovery_Report_20250630.pdf"
    )
    assert artifact["memberSha256"] == (
        "09616e8af327a6ea8e3bbc340e44392bbead98e581a9f85a7de99ef8b81e380f"
    )
    assert artifact["memberByteLength"] == 109_817
    assert artifact["column"] == "Fiscal Year 2024"
