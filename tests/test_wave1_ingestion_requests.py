import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REQUEST_ROOT = ROOT / "drafts" / "ledger-ingestion"


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
        (
            "sba-disaster-loan-program-post-charge-off-recovery.json",
            "sba-loan-program-performance-pdf",
            "51d5571d03d028d5efd4b8b9c8d7984f55285d36202eb8f67afe8a3476bb1242",
            1_296_419,
            "page",
            1,
            126_510_000,
            126_510_000,
            "usd",
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
