from __future__ import annotations

import gzip
import hashlib
import io
import json
import pathlib
import sys
import zipfile
from collections.abc import Callable, Mapping
from dataclasses import replace

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import resolve_pending  # noqa: E402
import witness_sba_pdf as witness  # noqa: E402
from sba_loan_performance import (  # noqa: E402
    CHARGE_OFF_AMOUNT_SERIES,
    CHARGE_OFF_RATE_SERIES,
    LAYOUT_REFUSAL,
    PARTIAL_REFUSAL,
    POST_CHARGE_OFF_RECOVERY_SERIES,
)
from verify_custody import verify_run  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "sba_loan_performance"
ASSET_URL = (
    "https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip"
)
LANDING_URL = (
    "https://legacy.sba.gov/document/"
    "report-small-business-administration-loan-program-performance"
)
REPORTS = {
    CHARGE_OFF_AMOUNT_SERIES: "WDS_ChargeOffAmount_Report_20250630.pdf",
    CHARGE_OFF_RATE_SERIES: "WDS_ChargeOffRates_Report_20250630.pdf",
    POST_CHARGE_OFF_RECOVERY_SERIES: ("WDS_PostChargeOffRecovery_Report_20250630.pdf"),
}
EXPECTED = {
    CHARGE_OFF_AMOUNT_SERIES: (299_971_326, "usd", "$299,971,326"),
    CHARGE_OFF_RATE_SERIES: (3.06, "percent", "3.06%"),
    POST_CHARGE_OFF_RECOVERY_SERIES: (126_510_000, "usd", "$126,510,000"),
}
ABSENT = "SBA CUSTODY ABSENT (refusing):"
UNWITNESSED = "SBA CUSTODY UNWITNESSED (refusing):"
INVALID = "SBA CUSTODY INVALID (refusing):"
AMBIGUOUS = "SBA EARLIEST CAPTURE AMBIGUOUS (refusing):"


def _bundle_bytes(
    *,
    marker: str | None = None,
    overrides: Mapping[str, bytes] | None = None,
) -> bytes:
    output = io.BytesIO()
    overrides = overrides or {}
    root = "WebsiteReports_FY25Q3"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in REPORTS.values():
            archive.writestr(
                f"{root}/{name}",
                overrides.get(name, (FIXTURES / name).read_bytes()),
            )
        if marker is not None:
            archive.writestr(f"{root}/{marker}.txt", marker.encode())
    return output.getvalue()


def _success(url: str, body: bytes, content_type: str) -> witness.FetchAttempt:
    return witness.FetchAttempt(
        requested_url=url,
        redirects=(),
        final_url=url,
        status=200,
        headers={
            "Content-Type": content_type,
            "Content-Length": str(len(body)),
        },
        body=body,
        error=None,
    )


def _landing_success() -> witness.FetchAttempt:
    body = f'<a href="{ASSET_URL}">download</a>'.encode()
    return witness.FetchAttempt(
        requested_url=witness.ENTRY_URL,
        redirects=(
            {
                "sourceUrl": witness.ENTRY_URL,
                "status": 302,
                "location": LANDING_URL,
                "targetUrl": LANDING_URL,
                "headers": {"Location": LANDING_URL},
            },
        ),
        final_url=LANDING_URL,
        status=200,
        headers={
            "Content-Type": "text/html; charset=utf-8",
            "Content-Length": str(len(body)),
        },
        body=body,
        error=None,
    )


def _fetcher(
    *attempts: witness.FetchAttempt,
) -> Callable[..., witness.FetchAttempt]:
    pending = iter(attempts)

    def fetch(
        url: str, *, timeout_seconds: float, max_bytes: int
    ) -> witness.FetchAttempt:
        del timeout_seconds, max_bytes
        attempt = next(pending)
        assert attempt.requested_url == url
        return attempt

    return fetch


def _capture(
    records: pathlib.Path,
    *,
    retrieved_at: str,
    bundle: bytes,
) -> pathlib.Path:
    return witness.capture_sba_pdf(
        records,
        retrieved_at=retrieved_at,
        fetcher=_fetcher(
            _landing_success(),
            _success(ASSET_URL, bundle, "application/zip"),
        ),
    )


def _manifest(path: pathlib.Path) -> dict[str, object]:
    value = json.loads(path.read_bytes())
    assert isinstance(value, dict)
    return value


def _proof(
    records: pathlib.Path,
    manifest_path: pathlib.Path,
    witnessed_at: str,
) -> tuple[str, str, dict[str, object], dict[str, str]]:
    manifest = _manifest(manifest_path)
    root_hash = str(manifest["custodyRootSha256"])
    run = manifest_path.parent.relative_to(records.parent.resolve()).as_posix()
    core = {
        "earliestWitnessedAt": witnessed_at,
        "witnessDigest": f"records/witness-snapshots/{root_hash[:12]}.json",
        "tsaGenTime": witnessed_at,
        "coverage": "direct",
    }
    root_proof: dict[str, object] = {
        **core,
        "custodyInventoryVersion": 2,
        "inventoryStatus": "complete",
        "headlineEligible": True,
    }
    return root_hash, run, root_proof, core


def _timeline(
    records: pathlib.Path,
    *entries: tuple[pathlib.Path, str],
) -> dict[str, object]:
    roots: dict[str, dict[str, object]] = {}
    runs: dict[str, dict[str, str]] = {}
    for manifest_path, witnessed_at in entries:
        root_hash, run, root_proof, run_proof = _proof(
            records, manifest_path, witnessed_at
        )
        roots[root_hash] = root_proof
        runs[run] = run_proof
    return {
        "schemaVersion": "thesis_witnessed_timeline_v1",
        "custodyRoots": roots,
        "runs": runs,
        "registrationSnapshots": {},
    }


def _install_timeline(
    monkeypatch: pytest.MonkeyPatch,
    timeline: dict[str, object],
) -> None:
    monkeypatch.setattr(resolve_pending, "extract_timeline", lambda _records: timeline)


def test_refuses_when_no_sba_capture_exists(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = tmp_path / "records"
    records.mkdir()
    _install_timeline(monkeypatch, _timeline(records))

    resolution, refusal = resolve_pending.resolve_sba_pdf_first_print(
        records,
        series=CHARGE_OFF_AMOUNT_SERIES,
        fiscal_year=2024,
    )

    assert resolution is None
    assert refusal is not None and refusal.startswith(ABSENT)


def test_refuses_valid_capture_without_witness_proof(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = tmp_path / "records"
    _capture(
        records,
        retrieved_at="2026-08-07T12:00:00Z",
        bundle=_bundle_bytes(),
    )
    _install_timeline(monkeypatch, _timeline(records))

    resolution, refusal = resolve_pending.resolve_sba_pdf_first_print(
        records,
        series=CHARGE_OFF_AMOUNT_SERIES,
        fiscal_year=2024,
    )

    assert resolution is None
    assert refusal is not None and refusal.startswith(UNWITNESSED)


@pytest.mark.parametrize("series", tuple(REPORTS))
def test_resolves_each_series_from_real_witnessed_zip_and_pdf(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    series: str,
) -> None:
    records = tmp_path / "records"
    bundle = _bundle_bytes()
    manifest_path = _capture(
        records,
        retrieved_at="2026-08-07T12:00:00Z",
        bundle=bundle,
    )
    timeline = _timeline(records, (manifest_path, "2026-08-07T13:00:00Z"))
    _install_timeline(monkeypatch, timeline)

    resolution, refusal = resolve_pending.resolve_sba_pdf_first_print(
        records,
        series=series,
        fiscal_year=2024,
    )

    assert refusal is None
    assert resolution is not None
    expected_value, expected_unit, printed_value = EXPECTED[series]
    assert (resolution.value, resolution.unit) == (expected_value, expected_unit)
    assert resolution.raw_bundle == bundle
    assert (
        resolution.run_directory
        == manifest_path.parent.relative_to(records.parent.resolve()).as_posix()
    )
    assert resolution.source_url == ASSET_URL
    expected_member = f"WebsiteReports_FY25Q3/{REPORTS[series]}"
    assert resolution.member_path == expected_member

    manifest = _manifest(manifest_path)
    root_hash, _, root_proof, _ = _proof(records, manifest_path, "2026-08-07T13:00:00Z")
    required_provenance = {
        "custodyMode",
        "runDirectory",
        "landingUrl",
        "assetUrl",
        "zipSha256",
        "memberPath",
        "memberSha256",
        "custodyRootSha256",
        "witnessDigest",
        "earliestWitnessedAt",
        "tsaGenTime",
        "witnessCoverage",
        "tableTitle",
        "section",
        "row",
        "fiscalYear",
        "printedValue",
        "unit",
        "parserContract",
    }
    provenance = resolution.provenance
    assert required_provenance <= provenance.keys()
    assert provenance["custodyMode"]
    assert provenance["runDirectory"] == resolution.run_directory
    assert provenance["landingUrl"] == witness.ENTRY_URL
    assert provenance["landingFinalUrl"] == LANDING_URL
    assert provenance["assetUrl"] == ASSET_URL
    assert provenance["zipSha256"] == hashlib.sha256(bundle).hexdigest()
    assert provenance["memberPath"] == expected_member
    assert (
        provenance["memberSha256"]
        == hashlib.sha256((FIXTURES / REPORTS[series]).read_bytes()).hexdigest()
    )
    assert provenance["custodyRootSha256"] == root_hash
    assert provenance["witnessDigest"] == root_proof["witnessDigest"]
    assert provenance["earliestWitnessedAt"] == "2026-08-07T13:00:00Z"
    assert provenance["tsaGenTime"] == "2026-08-07T13:00:00Z"
    assert provenance["witnessCoverage"] == "direct"
    assert provenance["section"] == "Disaster"
    assert provenance["row"] == "Disaster"
    assert provenance["fiscalYear"] == 2024
    assert provenance["printedValue"] == printed_value
    assert provenance["unit"] == expected_unit
    assert provenance["parserContract"] == manifest["bundle"]["parserContract"]  # type: ignore[index]

    spec = resolve_pending.SBA_PDF_ADAPTERS[series]
    ref = f"{series}.fy_2024.first_print"
    fact = resolve_pending.sba_pdf_fact(ref, spec, "2024", resolution)
    assert fact["observed_at"] == "2026-08-07"
    assert fact["source"]["vintage"] == "earliest_witnessed_capture"
    assert fact["source"]["source_file"] == "WebsiteReports_FY25Q3.zip"
    assert fact["source"]["source_sha256"] == provenance["zipSha256"]
    assert fact["custodyProvenance"] == provenance


def test_sba_zip_response_archive_passes_resolution_custody_verification(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = tmp_path / "records"
    bundle = _bundle_bytes()
    manifest_path = _capture(
        records,
        retrieved_at="2026-08-07T12:00:00Z",
        bundle=bundle,
    )
    _install_timeline(
        monkeypatch,
        _timeline(records, (manifest_path, "2026-08-07T13:00:00Z")),
    )
    resolution, refusal = resolve_pending.resolve_sba_pdf_first_print(
        records,
        series=CHARGE_OFF_AMOUNT_SERIES,
        fiscal_year=2024,
    )
    assert refusal is None
    assert resolution is not None

    spec = resolve_pending.SBA_PDF_ADAPTERS[CHARGE_OFF_AMOUNT_SERIES]
    ref = f"{CHARGE_OFF_AMOUNT_SERIES}.fy_2024.first_print"
    row = resolve_pending.sba_pdf_fact(ref, spec, "2024", resolution)
    registration = {
        "targetContentHash": "f" * 64,
        "contract": {
            "series": CHARGE_OFF_AMOUNT_SERIES,
            "unit": "usd",
            "period": {"type": "fiscal_year", "value": "2024"},
            "sourceBinding": {
                **resolve_pending.sba_pdf_binding_template(spec),
                "allowedHosts": ["legacy.sba.gov", "www.sba.gov"],
                "expectedReleaseWindow": {
                    "start": "2026-07-01",
                    "end": "2026-09-30",
                },
            },
        },
    }
    monkeypatch.setattr(resolve_pending, "ROOT", tmp_path)
    run_dir = tmp_path / "records" / "resolutions" / "run"
    enriched = resolve_pending.attach_resolution_provenance(
        row,
        run_dir=run_dir,
        series_id=resolve_pending.SBA_ARCHIVE_SERIES_ID,
        vintage="2026-08-07",
        raw=resolution.raw_bundle,
        retrieved_at="2026-08-07T13:40:00Z",
        ledger_repo_sha="0" * 40,
        target_contracts={ref: registration},
        extension="zip",
    )
    response = enriched["responseArchive"]
    assert response["path"].endswith(".zip.gz")
    assert response["sha256"] == hashlib.sha256(bundle).hexdigest()
    assert gzip.decompress((tmp_path / response["path"]).read_bytes()) == bundle
    assert enriched["source"]["source_file"] == "WebsiteReports_FY25Q3.zip"
    assert enriched["source"]["source_sha256"] == response["sha256"]
    assert enriched["sourceBindingProjection"]["responseSha256"] == response["sha256"]
    assert enriched["custodyProvenance"]["memberPath"] == resolution.member_path

    manifest = resolve_pending.finalize_resolution_manifest(
        run_dir,
        {
            "schemaVersion": "thesis_resolution_run_v1",
            "retrievedAt": "2026-08-07T13:40:00Z",
            "ledgerRepo": "PolicyEngine/ledger",
            "ledgerBranch": "test",
            "ledgerRepoSha": "0" * 40,
            "facts": [
                {
                    "dataPointId": ref,
                    "sourceVintage": enriched["sourceVintage"],
                    "retrievedAt": enriched["retrievedAt"],
                    "targetContentHash": enriched["targetContentHash"],
                    "responseArchive": response,
                }
            ],
        },
    )
    assert manifest["ok"] is True
    assert verify_run(run_dir).inventory_status == "complete"


def test_refuses_tampered_witnessed_archive_as_invalid_custody(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = tmp_path / "records"
    manifest_path = _capture(
        records,
        retrieved_at="2026-08-07T12:00:00Z",
        bundle=_bundle_bytes(),
    )
    manifest = _manifest(manifest_path)
    bundle_info = manifest["bundle"]
    assert isinstance(bundle_info, dict)
    archive_info = bundle_info["zipArchive"]
    assert isinstance(archive_info, dict)
    archive_path = manifest_path.parent / str(archive_info["path"])
    archive_path.write_bytes(archive_path.read_bytes() + b"tampered")
    _install_timeline(
        monkeypatch,
        _timeline(records, (manifest_path, "2026-08-07T13:00:00Z")),
    )

    resolution, refusal = resolve_pending.resolve_sba_pdf_first_print(
        records,
        series=CHARGE_OFF_AMOUNT_SERIES,
        fiscal_year=2024,
    )

    assert resolution is None
    assert refusal is not None and refusal.startswith(INVALID)


def test_refuses_partial_fiscal_year_from_witnessed_capture(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = tmp_path / "records"
    manifest_path = _capture(
        records,
        retrieved_at="2026-08-07T12:00:00Z",
        bundle=_bundle_bytes(),
    )
    _install_timeline(
        monkeypatch,
        _timeline(records, (manifest_path, "2026-08-07T13:00:00Z")),
    )

    resolution, refusal = resolve_pending.resolve_sba_pdf_first_print(
        records,
        series=CHARGE_OFF_AMOUNT_SERIES,
        fiscal_year=2025,
    )

    assert resolution is None
    assert refusal is not None and refusal.startswith(PARTIAL_REFUSAL)


def test_propagates_strict_parser_layout_refusal(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = tmp_path / "records"
    manifest_path = _capture(
        records,
        retrieved_at="2026-08-07T12:00:00Z",
        bundle=_bundle_bytes(),
    )
    _install_timeline(
        monkeypatch,
        _timeline(records, (manifest_path, "2026-08-07T13:00:00Z")),
    )
    refusal_message = f"{LAYOUT_REFUSAL} synthetic reviewed-layout change"
    monkeypatch.setattr(
        resolve_pending,
        "parse_sba_loan_performance_pdf",
        lambda _raw, *, series, fiscal_year: (None, refusal_message),
    )

    resolution, refusal = resolve_pending.resolve_sba_pdf_first_print(
        records,
        series=CHARGE_OFF_AMOUNT_SERIES,
        fiscal_year=2024,
    )

    assert resolution is None
    assert refusal == refusal_message


def test_selects_by_earliest_witness_not_claimed_retrieval_time(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = tmp_path / "records"
    first_bundle = _bundle_bytes(marker="first")
    first = _capture(
        records,
        retrieved_at="2026-08-07T12:00:00Z",
        bundle=first_bundle,
    )
    second_bundle = _bundle_bytes(marker="second")
    second = _capture(
        records,
        retrieved_at="2026-08-08T12:00:00Z",
        bundle=second_bundle,
    )
    _install_timeline(
        monkeypatch,
        _timeline(
            records,
            (first, "2026-08-10T13:00:00Z"),
            (second, "2026-08-09T13:00:00Z"),
        ),
    )

    resolution, refusal = resolve_pending.resolve_sba_pdf_first_print(
        records,
        series=CHARGE_OFF_AMOUNT_SERIES,
        fiscal_year=2024,
    )

    assert refusal is None
    assert resolution is not None
    assert resolution.raw_bundle == second_bundle
    assert (
        resolution.run_directory
        == second.parent.relative_to(records.parent.resolve()).as_posix()
    )


def test_accepts_equal_values_tied_at_earliest_witness(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = tmp_path / "records"
    bundles = (_bundle_bytes(marker="one"), _bundle_bytes(marker="two"))
    manifests = (
        _capture(
            records,
            retrieved_at="2026-08-07T12:00:00Z",
            bundle=bundles[0],
        ),
        _capture(
            records,
            retrieved_at="2026-08-08T12:00:00Z",
            bundle=bundles[1],
        ),
    )
    witnessed_at = "2026-08-09T13:00:00Z"
    _install_timeline(
        monkeypatch,
        _timeline(records, *((path, witnessed_at) for path in manifests)),
    )

    resolution, refusal = resolve_pending.resolve_sba_pdf_first_print(
        records,
        series=CHARGE_OFF_AMOUNT_SERIES,
        fiscal_year=2024,
    )

    assert refusal is None
    assert resolution is not None
    assert (resolution.value, resolution.unit) == (299_971_326, "usd")
    assert resolution.raw_bundle in bundles


def test_refuses_unequal_values_tied_at_earliest_witness(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records = tmp_path / "records"
    report_name = REPORTS[CHARGE_OFF_AMOUNT_SERIES]
    original_pdf = (FIXTURES / report_name).read_bytes()
    variant_pdf = original_pdf + b"\n% byte-distinct tie variant\n"
    bundles = (
        _bundle_bytes(marker="one"),
        _bundle_bytes(overrides={report_name: variant_pdf}),
    )
    manifests = (
        _capture(
            records,
            retrieved_at="2026-08-07T12:00:00Z",
            bundle=bundles[0],
        ),
        _capture(
            records,
            retrieved_at="2026-08-08T12:00:00Z",
            bundle=bundles[1],
        ),
    )
    witnessed_at = "2026-08-09T13:00:00Z"
    _install_timeline(
        monkeypatch,
        _timeline(records, *((path, witnessed_at) for path in manifests)),
    )
    real_parser = resolve_pending.parse_sba_loan_performance_pdf
    variant_hash = hashlib.sha256(variant_pdf).hexdigest()

    def disagreeing_parser(raw: bytes, *, series: str, fiscal_year: int):
        cell, refusal = real_parser(raw, series=series, fiscal_year=fiscal_year)
        if cell is not None and hashlib.sha256(raw).hexdigest() == variant_hash:
            cell = replace(
                cell,
                value=int(cell.value) + 1,
                printed_value="$299,971,327",
            )
        return cell, refusal

    monkeypatch.setattr(
        resolve_pending,
        "parse_sba_loan_performance_pdf",
        disagreeing_parser,
    )

    resolution, refusal = resolve_pending.resolve_sba_pdf_first_print(
        records,
        series=CHARGE_OFF_AMOUNT_SERIES,
        fiscal_year=2024,
    )

    assert resolution is None
    assert refusal is not None and refusal.startswith(AMBIGUOUS)


def test_pending_adapter_refs_routes_sba_fiscal_year() -> None:
    ref = f"{CHARGE_OFF_AMOUNT_SERIES}.fy_2024.first_print"
    forecast = {
        "kind": "prediction_recorded",
        "forecastSlug": "sba-charge-offs-fy2024",
        "resolutionDate": "2026-12-31",
        "unit": "usd",
    }
    log = {
        "entries": [forecast],
        "resolutionLinks": [
            {
                "forecastSlug": forecast["forecastSlug"],
                "targetFactRef": ref,
                "status": "pending",
            }
        ],
    }

    assert resolve_pending.pending_adapter_refs(log) == [
        (
            ref,
            "sba_pdf",
            resolve_pending.SBA_PDF_ADAPTERS[CHARGE_OFF_AMOUNT_SERIES],
            "fiscal_year",
            "2024",
            "2026-12-31",
            forecast,
        )
    ]


def test_resolution_workflow_installs_the_sba_pdf_parser() -> None:
    workflow = (ROOT / ".github/workflows/resolve-and-rebuild.yml").read_text()
    assert "pip install --user xlrd==2.0.1 pypdf==6.14.2" in workflow


def test_main_allows_closed_bound_only_to_reach_witnessed_custody(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    ref = f"{CHARGE_OFF_AMOUNT_SERIES}.fy_2024.first_print"
    spec = resolve_pending.SBA_PDF_ADAPTERS[CHARGE_OFF_AMOUNT_SERIES]
    forecast = {"resolutionDate": "2020-12-31", "unit": "usd"}
    binding = {
        **resolve_pending.sba_pdf_binding_template(spec),
        "allowedHosts": ["legacy.sba.gov", "www.sba.gov"],
        "expectedReleaseWindow": {"start": "2020-10-01", "end": "2020-12-31"},
    }
    registration = {
        "contract": {
            "resolutionDateBasis": "resolve-by-bound",
            "sourceBinding": binding,
        }
    }
    calls: list[tuple[pathlib.Path, str, int]] = []

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
                "sba_pdf",
                spec,
                "fiscal_year",
                "2024",
                "2020-12-31",
                forecast,
            )
        ],
    )
    monkeypatch.setattr(
        resolve_pending, "ledger_state", lambda *_args: ("", "blob", "a" * 40)
    )
    monkeypatch.setattr(
        resolve_pending, "registration_contracts", lambda: {ref: registration}
    )
    monkeypatch.setattr(
        resolve_pending, "utc_now", lambda: "2026-08-07T12:00:00Z"
    )
    monkeypatch.setattr(
        resolve_pending,
        "extract_timeline",
        lambda _records: {"runs": {}, "custodyRoots": {}},
    )

    def custody_only(
        records: pathlib.Path,
        *,
        series: str,
        fiscal_year: int,
        timeline: Mapping[str, object],
    ) -> tuple[None, str]:
        assert timeline == {"runs": {}, "custodyRoots": {}}
        calls.append((records, series, fiscal_year))
        return None, (
            f"{resolve_pending.SBA_CUSTODY_ABSENT} no witnessed capture in test"
        )

    def unexpected_network(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("SBA resolver attempted a live network fetch")

    monkeypatch.setattr(
        resolve_pending, "resolve_sba_pdf_first_print", custody_only
    )
    monkeypatch.setattr(resolve_pending.urllib.request, "urlopen", unexpected_network)
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])

    assert resolve_pending.main() == 0
    assert calls == [(ROOT / "records", CHARGE_OFF_AMOUNT_SERIES, 2024)]
    output = capsys.readouterr().out
    assert resolve_pending.SBA_CUSTODY_ABSENT in output
    assert "nothing new to record" in output
