#!/usr/bin/env python3
"""Capture the rolling SBA Loan Program Performance PDF bundle.

Every expected source outcome is sealed as an immutable custody run. The
capture time is diagnostic only; the recorder chain and its RFC 3161 witness
provide the admissible clock.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import gzip
import hashlib
import http.client
import io
import json
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Callable, Mapping

from canonical_json import canonical_bytes, canonical_sha256
from sba_loan_performance import (
    CHARGE_OFF_AMOUNT_SERIES,
    CHARGE_OFF_RATE_SERIES,
    POST_CHARGE_OFF_RECOVERY_SERIES,
    parse_sba_loan_performance_pdf,
)

ENTRY_URL = (
    "https://www.sba.gov/document/"
    "report-small-business-administration-loan-program-performance"
)
ALLOWED_HOSTS = ("legacy.sba.gov", "www.sba.gov")
RUN_SCHEMA = "thesis_sba_pdf_witness_run_v1"
FETCH_EVENT_SCHEMA = "thesis_sba_pdf_fetch_event_v1"
RUN_MODE = "sba_pdf_witness"
CAPTURE_REFUSAL = "SBA CAPTURE FAILED (refusing):"
PARSER_CONTRACT = "scripts/sba_loan_performance.py:SBA_REPORT_SPECS:v2"

MAX_LANDING_BYTES = 5 * 1024 * 1024
MAX_BUNDLE_BYTES = 50 * 1024 * 1024
MAX_ZIP_MEMBERS = 1_000
MAX_UNCOMPRESSED_BYTES = 100 * 1024 * 1024
MAX_REDIRECTS = 10

_BUNDLE_RE = re.compile(r"WebsiteReports_FY(?P<year>\d{2})Q(?P<quarter>[1-4])\.zip")
_RUN_RE = re.compile(r"\d{8}T\d{6}Z-sba-pdf-witness")
_RETAINED_HEADERS = {
    "date": "Date",
    "location": "Location",
    "content-type": "Content-Type",
    "content-length": "Content-Length",
    "etag": "ETag",
    "last-modified": "Last-Modified",
}
_REDIRECT_STATUSES = {301, 302, 303, 307, 308}
_REPORT_PREFIXES = {
    CHARGE_OFF_AMOUNT_SERIES: "WDS_ChargeOffAmount_Report_",
    CHARGE_OFF_RATE_SERIES: "WDS_ChargeOffRates_Report_",
    POST_CHARGE_OFF_RECOVERY_SERIES: "WDS_PostChargeOffRecovery_Report_",
}


class SbaCaptureError(ValueError):
    """Expected official-source or bundle-contract refusal."""


@dataclass(frozen=True)
class BundleIdentity:
    label: str
    fiscal_year: int
    quarter: int
    linked_url: str


@dataclass(frozen=True)
class FetchAttempt:
    requested_url: str
    redirects: tuple[dict[str, Any], ...]
    final_url: str | None
    status: int | None
    headers: dict[str, str]
    body: bytes | None
    error: str | None

    @property
    def succeeded(self) -> bool:
        return self.status == 200 and self.body is not None and self.error is None

    def event(self) -> dict[str, Any]:
        return {
            "requestedUrl": self.requested_url,
            "redirects": list(self.redirects),
            "finalUrl": self.final_url,
            "status": self.status,
            "contentType": self.headers.get("Content-Type"),
            "headers": self.headers,
            "outcome": "success" if self.succeeded else "failed",
            "bodySha256": (
                hashlib.sha256(self.body).hexdigest() if self.body is not None else None
            ),
            "bodyBytes": len(self.body) if self.body is not None else None,
            "error": self.error,
        }


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(  # type: ignore[override]
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Mapping[str, str],
        newurl: str,
    ) -> None:
        return None


class _HrefCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for name, value in attrs:
            if name.lower() == "href" and value is not None:
                self.hrefs.append(value)


def utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _retained_headers(headers: Mapping[str, str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for name, value in headers.items():
        canonical = _RETAINED_HEADERS.get(name.lower())
        if canonical is not None:
            values[canonical] = str(value)
    return values


def _official_url(url: str, *, label: str) -> urllib.parse.SplitResult:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https":
        raise SbaCaptureError(f"{label} must use HTTPS")
    if parsed.username is not None or parsed.password is not None or parsed.port:
        raise SbaCaptureError(f"{label} contains forbidden URL authority fields")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise SbaCaptureError(
            f"{label} host {parsed.hostname!r} is outside the SBA allowlist"
        )
    return parsed


def _read_bounded(response: Any, maximum: int) -> bytes:
    raw = response.read(maximum + 1)
    if len(raw) > maximum:
        raise SbaCaptureError(f"response exceeds the {maximum}-byte capture limit")
    return raw


def _fetch_url(url: str, *, timeout_seconds: float, max_bytes: int) -> FetchAttempt:
    """Fetch one official URL while recording and policing each redirect."""

    requested_url = url
    redirects: list[dict[str, Any]] = []
    current = url
    opener = urllib.request.build_opener(_NoRedirect())
    for _ in range(MAX_REDIRECTS + 1):
        try:
            _official_url(current, label="fetch URL")
        except SbaCaptureError as exc:
            return FetchAttempt(
                requested_url,
                tuple(redirects),
                current,
                None,
                {},
                None,
                str(exc),
            )
        request = urllib.request.Request(
            current,
            headers={"User-Agent": "Thesis-SBA-custody-witness/1"},
        )
        try:
            response = opener.open(request, timeout=timeout_seconds)
        except urllib.error.HTTPError as exc:
            headers = _retained_headers(exc.headers)
            if exc.code in _REDIRECT_STATUSES:
                location = exc.headers.get("Location")
                if not location:
                    return FetchAttempt(
                        requested_url,
                        tuple(redirects),
                        current,
                        exc.code,
                        headers,
                        None,
                        "redirect response lacks Location",
                    )
                if len(redirects) >= MAX_REDIRECTS:
                    return FetchAttempt(
                        requested_url,
                        tuple(redirects),
                        current,
                        exc.code,
                        headers,
                        None,
                        f"redirect chain exceeds {MAX_REDIRECTS} hops",
                    )
                target = urllib.parse.urljoin(current, location)
                try:
                    _official_url(target, label="redirect target")
                except SbaCaptureError as refusal:
                    return FetchAttempt(
                        requested_url,
                        tuple(
                            [
                                *redirects,
                                {
                                    "sourceUrl": current,
                                    "status": exc.code,
                                    "location": location,
                                    "targetUrl": target,
                                    "headers": headers,
                                },
                            ]
                        ),
                        target,
                        None,
                        {},
                        None,
                        str(refusal),
                    )
                redirects.append(
                    {
                        "sourceUrl": current,
                        "status": exc.code,
                        "location": location,
                        "targetUrl": target,
                        "headers": headers,
                    }
                )
                current = target
                continue
            try:
                body = _read_bounded(exc, max_bytes)
            except (http.client.HTTPException, OSError, SbaCaptureError) as refusal:
                body = None
                error = f"response read failed: {refusal}"
            else:
                error = f"HTTP status {exc.code}"
            return FetchAttempt(
                requested_url,
                tuple(redirects),
                current,
                exc.code,
                headers,
                body,
                error,
            )
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return FetchAttempt(
                requested_url,
                tuple(redirects),
                current,
                None,
                {},
                None,
                f"network fetch failed: {type(exc).__name__}",
            )
        headers: dict[str, str] = {}
        status: int | None = None
        final_url = current
        try:
            with response:
                # Preserve metadata before reading the body. A truncated,
                # oversized, or otherwise unreadable response is still useful
                # custody evidence even though it cannot be admitted.
                headers = _retained_headers(response.headers)
                status = int(response.status)
                final_url = str(response.geturl())
                body = _read_bounded(response, max_bytes)
        except (http.client.HTTPException, OSError, SbaCaptureError) as exc:
            return FetchAttempt(
                requested_url,
                tuple(redirects),
                final_url,
                status,
                headers,
                None,
                f"response read failed: {exc}",
            )
        try:
            _official_url(final_url, label="final response URL")
        except SbaCaptureError as exc:
            return FetchAttempt(
                requested_url,
                tuple(redirects),
                final_url,
                status,
                headers,
                body,
                str(exc),
            )
        return FetchAttempt(
            requested_url,
            tuple(redirects),
            final_url,
            status,
            headers,
            body,
            None if status == 200 else f"HTTP status {status}",
        )
    return FetchAttempt(
        requested_url,
        tuple(redirects),
        current,
        None,
        {},
        None,
        f"redirect chain exceeds {MAX_REDIRECTS} hops",
    )


def _require_success(attempt: FetchAttempt, *, stage: str) -> bytes:
    if not attempt.succeeded:
        reason = attempt.error or f"HTTP status {attempt.status}"
        raise SbaCaptureError(f"{stage}: {reason}")
    assert attempt.body is not None
    return attempt.body


def _bundle_identity_from_url(url: str) -> BundleIdentity:
    parsed = _official_url(url, label="linked asset URL")
    if parsed.query or parsed.fragment:
        raise SbaCaptureError("linked asset URL must not contain query or fragment")
    name = pathlib.PurePosixPath(parsed.path).name
    match = _BUNDLE_RE.fullmatch(name)
    if match is None:
        raise SbaCaptureError(f"unrecognized SBA bundle filename {name!r}")
    fiscal_year = 2000 + int(match.group("year"))
    quarter = int(match.group("quarter"))
    return BundleIdentity(
        label=f"FY{match.group('year')}Q{quarter}",
        fiscal_year=fiscal_year,
        quarter=quarter,
        linked_url=url,
    )


def _linked_bundle(landing: bytes, *, page_url: str) -> BundleIdentity:
    try:
        text = landing.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SbaCaptureError("landing page is not valid UTF-8") from exc
    parser = _HrefCollector()
    try:
        parser.feed(text)
        parser.close()
    except Exception as exc:
        raise SbaCaptureError("landing page HTML parsing failed") from exc
    candidates: list[BundleIdentity] = []
    for href in parser.hrefs:
        resolved = urllib.parse.urljoin(page_url, href)
        try:
            identity = _bundle_identity_from_url(resolved)
        except SbaCaptureError:
            continue
        candidates.append(identity)
    if len(candidates) != 1:
        raise SbaCaptureError(
            "landing page must link exactly one recognized bundle, found "
            f"{len(candidates)}"
        )
    return candidates[0]


def _safe_zip_member(name: str) -> pathlib.PurePosixPath:
    if not name or "\\" in name or "\x00" in name or name.startswith("/"):
        raise SbaCaptureError(f"unsafe ZIP member path {name!r}")
    path = pathlib.PurePosixPath(name)
    if not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise SbaCaptureError(f"unsafe ZIP member path {name!r}")
    canonical = path.as_posix() + ("/" if name.endswith("/") else "")
    if name != canonical:
        raise SbaCaptureError(f"unsafe ZIP member path {name!r} is not canonical")
    return path


def _expected_as_of(identity: BundleIdentity) -> dt.date:
    if identity.quarter == 1:
        return dt.date(identity.fiscal_year - 1, 12, 31)
    month_day = {2: (3, 31), 3: (6, 30), 4: (9, 30)}[identity.quarter]
    return dt.date(identity.fiscal_year, *month_day)


def _period_coverage(identity: BundleIdentity) -> dict[str, Any]:
    """Derive the ten displayed years before inspecting any report PDF."""

    displayed = list(range(identity.fiscal_year - 9, identity.fiscal_year + 1))
    completed_stop = (
        identity.fiscal_year + 1 if identity.quarter == 4 else identity.fiscal_year
    )
    return {
        "periodType": "fiscal_year",
        "displayedFiscalYears": displayed,
        "possibleCompletedFiscalYears": list(
            range(identity.fiscal_year - 9, completed_stop)
        ),
    }


def _captured_bundle(raw: bytes, *, identity: BundleIdentity) -> dict[str, Any]:
    """Bind fetched bytes to their page-derived identity before PDF parsing."""

    return {
        "label": identity.label,
        "fiscalYear": identity.fiscal_year,
        "quarter": identity.quarter,
        "assetUrl": identity.linked_url,
        "rawSha256": _sha256(raw),
        "rawBytes": len(raw),
        "periodCoverage": _period_coverage(identity),
        "parserContract": PARSER_CONTRACT,
    }


def _inspect_bundle(raw: bytes, *, identity: BundleIdentity) -> dict[str, Any]:
    """Replay ZIP structure and the three reviewed report parsers."""

    if not raw.startswith(b"PK"):
        raise SbaCaptureError("asset response does not have a ZIP signature")
    try:
        archive = zipfile.ZipFile(io.BytesIO(raw))
    except (zipfile.BadZipFile, zipfile.LargeZipFile) as exc:
        raise SbaCaptureError("asset is not a valid ZIP archive") from exc

    root = f"WebsiteReports_{identity.label}"
    inventory: list[dict[str, Any]] = []
    bodies: dict[str, bytes] = {}
    seen: set[str] = set()
    total_size = 0
    try:
        infos = archive.infolist()
        if not infos or len(infos) > MAX_ZIP_MEMBERS:
            raise SbaCaptureError(
                f"ZIP member count {len(infos)} is outside the reviewed limit"
            )
        for info in infos:
            path = _safe_zip_member(info.filename)
            normalized_path = path.as_posix()
            if normalized_path in seen:
                raise SbaCaptureError(f"duplicate ZIP member path {info.filename!r}")
            seen.add(normalized_path)
            if path.parts[0] != root:
                raise SbaCaptureError(
                    f"ZIP member {info.filename!r} is outside expected root {root!r}"
                )
            if info.flag_bits & 0x1:
                raise SbaCaptureError(f"encrypted ZIP member {info.filename!r}")
            unix_type = (info.external_attr >> 16) & 0o170000
            if unix_type == 0o120000:
                raise SbaCaptureError(f"symlink ZIP member {info.filename!r}")
            total_size += info.file_size
            if total_size > MAX_UNCOMPRESSED_BYTES:
                raise SbaCaptureError("ZIP uncompressed size exceeds reviewed limit")
            try:
                member = archive.read(info)
            except (
                NotImplementedError,
                OSError,
                RuntimeError,
                ValueError,
                zipfile.BadZipFile,
            ) as exc:
                raise SbaCaptureError(
                    f"ZIP member {info.filename!r} cannot be replayed"
                ) from exc
            if len(member) != info.file_size:
                raise SbaCaptureError(
                    f"ZIP member {info.filename!r} size changed during replay"
                )
            bodies[info.filename] = member
            inventory.append(
                {
                    "path": info.filename,
                    "bytes": len(member),
                    "sha256": _sha256(member),
                }
            )
    finally:
        archive.close()

    parsed_year = identity.fiscal_year - 1
    expected_as_of = _expected_as_of(identity)
    reports: list[dict[str, Any]] = []
    observed_dates: set[dt.date] = set()
    for series, prefix in _REPORT_PREFIXES.items():
        pattern = re.compile(
            rf"{re.escape(root)}/{re.escape(prefix)}(?P<date>\d{{8}})\.pdf"
        )
        matches = [name for name in bodies if pattern.fullmatch(name)]
        if len(matches) != 1:
            raise SbaCaptureError(
                f"required report {prefix!r} must occur once, found {len(matches)}"
            )
        member_path = matches[0]
        match = pattern.fullmatch(member_path)
        assert match is not None
        try:
            filename_date = dt.datetime.strptime(match.group("date"), "%Y%m%d").date()
        except ValueError as exc:
            raise SbaCaptureError(
                f"required report {member_path!r} has an invalid date"
            ) from exc
        member = bodies[member_path]
        cell, refusal = parse_sba_loan_performance_pdf(
            member,
            series=series,
            fiscal_year=parsed_year,
        )
        if refusal is not None:
            raise SbaCaptureError(f"{member_path}: {refusal}")
        assert cell is not None
        report_as_of = dt.date.fromisoformat(cell.report_as_of)
        if filename_date != report_as_of:
            raise SbaCaptureError(
                f"required report {member_path!r} filename date disagrees with content"
            )
        if report_as_of != expected_as_of:
            raise SbaCaptureError(
                f"required report {member_path!r} as-of date does not match "
                f"{identity.label}"
            )
        if cell.partial_fiscal_year != identity.fiscal_year:
            raise SbaCaptureError(
                f"required report {member_path!r} fiscal year disagrees with bundle"
            )
        observed_dates.add(report_as_of)
        reports.append(
            {
                "series": series,
                "memberPath": member_path,
                "memberSha256": _sha256(member),
                "memberBytes": len(member),
                "tableTitle": cell.table_title,
                "reportAsOf": cell.report_as_of,
                "partialFiscalYear": cell.partial_fiscal_year,
                "headerYears": list(cell.header_years),
                "parsedFiscalYear": cell.fiscal_year,
                "printedValue": cell.printed_value,
                "value": cell.value,
                "unit": cell.unit,
                "pdfSha256": cell.pdf_sha256,
            }
        )
    if observed_dates != {expected_as_of}:
        raise SbaCaptureError("required reports do not share one reviewed as-of date")

    return {
        **_captured_bundle(raw, identity=identity),
        "reportAsOf": expected_as_of.isoformat(),
        "memberInventory": inventory,
        "reports": reports,
    }


def _json_object(path: pathlib.Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def _previous_complete(records: pathlib.Path) -> dict[str, Any] | None:
    """Return the latest repository-path complete capture after verification."""

    candidates: list[tuple[str, pathlib.Path, dict[str, Any]]] = []
    for path in records.rglob("manifest.json"):
        if path.is_symlink() or path.parent.is_symlink():
            continue
        try:
            manifest = _json_object(path)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        if manifest.get("schemaVersion") != RUN_SCHEMA or manifest.get(
            "outcome"
        ) not in {"bootstrap", "changed"}:
            continue
        relative = path.parent.relative_to(records.parent).as_posix()
        candidates.append((relative, path.parent, manifest))
    if not candidates:
        return None
    _, run_dir, manifest = max(candidates, key=lambda item: item[0])
    from verify_custody import verify_run

    verified = verify_run(run_dir)
    bundle = manifest.get("bundle")
    if not isinstance(bundle, dict):
        raise ValueError(f"complete SBA capture lacks bundle object: {run_dir}")
    return {
        "runDirectory": run_dir.relative_to(records.parent).as_posix(),
        "custodyRootPath": (run_dir / "custody_root.json")
        .relative_to(records.parent)
        .as_posix(),
        "custodyRootSha256": verified.custody_root_sha256,
        "bundleSha256": bundle["rawSha256"],
        "bundleBytes": bundle["rawBytes"],
        "bundleLabel": bundle["label"],
        "reportAsOf": bundle["reportAsOf"],
    }


def _write_exclusive(path: pathlib.Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)


def _write_json_exclusive(path: pathlib.Path, value: Any) -> None:
    _write_exclusive(path, (json.dumps(value, indent=2) + "\n").encode())


def _artifact_ref(
    *,
    artifact_type: str,
    path: pathlib.Path,
    run_dir: pathlib.Path,
    repository: pathlib.Path,
    created_at: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = path.read_bytes()
    manifest_ref: dict[str, Any] = {
        "artifactType": artifact_type,
        "path": path.relative_to(repository).as_posix(),
        "sha256": _sha256(raw),
        "bytes": len(raw),
        "createdAt": created_at,
    }
    if path.suffix == ".json":
        manifest_ref["canonicalJsonSha256"] = canonical_sha256(json.loads(raw))
    root_ref = {
        **manifest_ref,
        "path": path.relative_to(run_dir).as_posix(),
    }
    return manifest_ref, root_ref


def _seal_run(
    *,
    records: pathlib.Path,
    retrieved_at: str,
    outcome: str,
    landing: FetchAttempt,
    asset: FetchAttempt | None,
    bundle: dict[str, Any] | None,
    previous: dict[str, Any] | None,
    failure_stage: str | None,
    failure_reason: str | None,
) -> pathlib.Path:
    instant = dt.datetime.fromisoformat(retrieved_at.replace("Z", "+00:00"))
    stamp = instant.astimezone(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if _RUN_RE.fullmatch(f"{stamp}-sba-pdf-witness") is None:
        raise ValueError("invalid SBA witness run timestamp")
    run_dir = records / instant.date().isoformat() / f"{stamp}-sba-pdf-witness"
    run_dir.mkdir(parents=True, exist_ok=False)

    failure = (
        {"stage": failure_stage, "reason": failure_reason}
        if failure_stage is not None and failure_reason is not None
        else None
    )
    fetch_event = {
        "schemaVersion": FETCH_EVENT_SCHEMA,
        "attemptedAt": retrieved_at,
        "outcome": outcome,
        "landing": landing.event(),
        "asset": asset.event() if asset is not None else None,
        "failure": failure,
    }
    fetch_path = run_dir / "fetch_event.json"
    _write_json_exclusive(fetch_path, fetch_event)

    archive_paths: list[tuple[str, pathlib.Path]] = []
    landing_path: pathlib.Path | None = None
    landing_gzip: bytes | None = None
    if landing.body is not None:
        landing_gzip = gzip.compress(landing.body, mtime=0)
        landing_path = run_dir / "upstream" / "landing-page.html.gz"
        _write_exclusive(landing_path, landing_gzip)
        archive_paths.append(("landing_archive", landing_path))

    archive_bundle = outcome in {"bootstrap", "changed"} or (
        outcome == "failed" and bundle is not None
    )
    if archive_bundle:
        assert (
            landing.body is not None
            and landing_path is not None
            and landing_gzip is not None
            and asset is not None
            and asset.body is not None
        )
        bundle_gzip = gzip.compress(asset.body, mtime=0)
        bundle_path = run_dir / "upstream" / "loan-program-performance.zip.gz"
        _write_exclusive(bundle_path, bundle_gzip)
        archive_paths.append(("bundle_archive", bundle_path))
        assert bundle is not None
        bundle["landingArchive"] = {
            "path": landing_path.relative_to(run_dir).as_posix(),
            "rawSha256": _sha256(landing.body),
            "rawBytes": len(landing.body),
            "gzipSha256": _sha256(landing_gzip),
            "gzipBytes": len(landing_gzip),
            "contentEncoding": "gzip",
        }
        bundle["zipArchive"] = {
            "path": bundle_path.relative_to(run_dir).as_posix(),
            "rawSha256": _sha256(asset.body),
            "rawBytes": len(asset.body),
            "gzipSha256": _sha256(bundle_gzip),
            "gzipBytes": len(bundle_gzip),
            "contentEncoding": "gzip",
        }

    repository = records.parent.resolve()
    manifest_refs: list[dict[str, Any]] = []
    rooted_refs: list[dict[str, Any]] = []
    for artifact_type, path in [("fetch_event", fetch_path), *archive_paths]:
        manifest_ref, rooted_ref = _artifact_ref(
            artifact_type=artifact_type,
            path=path,
            run_dir=run_dir,
            repository=repository,
            created_at=retrieved_at,
        )
        manifest_refs.append(manifest_ref)
        rooted_refs.append(rooted_ref)

    manifest: dict[str, Any] = {
        "schemaVersion": RUN_SCHEMA,
        "retrievedAt": retrieved_at,
        "source": {
            "entryUrl": ENTRY_URL,
            "allowedHosts": list(ALLOWED_HOSTS),
            "requiredSeries": list(_REPORT_PREFIXES),
            "parserContract": PARSER_CONTRACT,
        },
        "outcome": outcome,
        "ok": outcome != "failed",
        "fetchEventPath": "fetch_event.json",
        "bundle": bundle,
        "previousCompleteCapture": previous,
        "failure": failure,
        "custodyInventoryVersion": 2,
        "runMode": RUN_MODE,
        "manifestHashSemantics": (
            "canonical-json-v1; exclude artifacts where "
            "artifactType=manifest and exclude custodyRootSha256"
        ),
        "artifacts": manifest_refs,
    }
    self_payload = copy.deepcopy(manifest)
    self_payload.pop("custodyRootSha256", None)
    self_bytes = canonical_bytes(self_payload)
    manifest_ref = {
        "artifactType": "manifest",
        "path": (run_dir / "manifest.json").relative_to(repository).as_posix(),
        "sha256": _sha256(self_bytes),
        "bytes": len(self_bytes),
        "createdAt": retrieved_at,
        "hashMode": manifest["manifestHashSemantics"],
    }
    manifest["artifacts"] = [*manifest_refs, manifest_ref]
    custody = {
        "schemaVersion": "thesis_custody_root_v1",
        "custodyInventoryVersion": 2,
        "runMode": RUN_MODE,
        "hashAlgorithm": "sha256",
        "canonicalJson": (
            "UTF-16 code-unit key order; ECMAScript JSON number/string encoding"
        ),
        "artifacts": rooted_refs,
        "manifestWithoutCustodyRoot": {
            "path": "manifest.json",
            "excludedField": "custodyRootSha256",
            "canonicalJsonSha256": canonical_sha256(manifest),
        },
    }
    _write_json_exclusive(run_dir / "custody_root.json", custody)
    manifest["custodyRootSha256"] = canonical_sha256(custody)
    _write_json_exclusive(run_dir / "manifest.json", manifest)

    from verify_custody import verify_run

    verify_run(run_dir)
    return run_dir / "manifest.json"


FetchFunction = Callable[..., FetchAttempt]


def capture_sba_pdf(
    records: pathlib.Path,
    *,
    retrieved_at: str | None = None,
    timeout_seconds: float = 60,
    fetcher: FetchFunction = _fetch_url,
) -> pathlib.Path:
    """Capture one source attempt and return its sealed manifest path."""

    records = records.resolve()
    records.mkdir(parents=True, exist_ok=True)
    retrieved_at = retrieved_at or utc_now()
    previous = _previous_complete(records)

    landing = fetcher(
        ENTRY_URL,
        timeout_seconds=timeout_seconds,
        max_bytes=MAX_LANDING_BYTES,
    )
    asset: FetchAttempt | None = None
    bundle: dict[str, Any] | None = None
    outcome = "failed"
    failure_stage: str | None = None
    failure_reason: str | None = None
    previous_reference: dict[str, Any] | None = None
    active_stage = "landing fetch"
    try:
        landing_raw = _require_success(landing, stage=active_stage)
        active_stage = "landing validation"
        if landing.final_url is None:
            raise SbaCaptureError("final URL is absent")
        content_type = landing.headers.get("Content-Type", "").lower()
        if not content_type.startswith("text/html"):
            raise SbaCaptureError(f"content type {content_type!r} is not HTML")
        identity = _linked_bundle(landing_raw, page_url=landing.final_url)
        active_stage = "asset fetch"
        asset = fetcher(
            identity.linked_url,
            timeout_seconds=timeout_seconds,
            max_bytes=MAX_BUNDLE_BYTES,
        )
        asset_raw = _require_success(asset, stage=active_stage)
        active_stage = "asset validation"
        asset_type = asset.headers.get("Content-Type", "").split(";", 1)[0].lower()
        if asset_type != "application/zip":
            raise SbaCaptureError(f"content type {asset_type!r} is not application/zip")
        raw_sha = _sha256(asset_raw)
        bundle = _captured_bundle(asset_raw, identity=identity)
        if (
            previous is not None
            and previous["bundleSha256"] == raw_sha
            and previous["bundleBytes"] == len(asset_raw)
            and previous["bundleLabel"] == identity.label
        ):
            outcome = "unchanged"
            bundle = {
                "label": identity.label,
                "fiscalYear": identity.fiscal_year,
                "quarter": identity.quarter,
                "assetUrl": identity.linked_url,
                "rawSha256": raw_sha,
                "rawBytes": len(asset_raw),
                "periodCoverage": _period_coverage(identity),
                "reportAsOf": previous["reportAsOf"],
                "parserContract": PARSER_CONTRACT,
            }
            previous_reference = previous
        else:
            active_stage = "bundle validation"
            bundle = _inspect_bundle(asset_raw, identity=identity)
            outcome = "bootstrap" if previous is None else "changed"
    except SbaCaptureError as exc:
        reason = str(exc)
        prefix = f"{active_stage}: "
        detail = reason.removeprefix(prefix)
        failure_stage = active_stage
        failure_reason = f"{CAPTURE_REFUSAL} {detail}"
        if active_stage != "bundle validation":
            bundle = None
        previous_reference = None

    return _seal_run(
        records=records,
        retrieved_at=retrieved_at,
        outcome=outcome,
        landing=landing,
        asset=asset,
        bundle=bundle,
        previous=previous_reference,
        failure_stage=failure_stage,
        failure_reason=failure_reason,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=pathlib.Path, default=pathlib.Path("records"))
    parser.add_argument("--timeout-seconds", type=float, default=60)
    args = parser.parse_args()
    manifest = capture_sba_pdf(
        args.records,
        timeout_seconds=args.timeout_seconds,
    )
    try:
        printable = manifest.relative_to(pathlib.Path.cwd())
    except ValueError:
        printable = manifest
    print(printable.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
