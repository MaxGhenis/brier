#!/usr/bin/env python3
"""Resolve pending forecast cells whose official numbers have published.

Adapter-based: each adapter claims a family of targetFactRefs from the live
catalog's resolutionLinks, checks whether the official first print exists
yet, and emits a PolicyEngine-Ledger fact row (the JSONL schema the site's
build fetches and joins on source_record_id == targetFactRef). Appending a
row is what resolves a cell: the next site build scores it.

First adapters: DOL UI weekly claims (initial + continued, seasonally
adjusted), read from FRED's ICSA/CCSA series — the advance vintage named by
the cells' own resolver rules. BLS CES detailed-industry cells (the defense
batch) resolve straight from the BLS Public Data API v2 series their
resolutionSourceUrls bind, under a temporal first-print gate and runtime
anchor verification (see BLS_API_ADAPTERS).

Usage:
    python3 scripts/resolve_pending.py [--dry-run]
        [--ledger-repo PolicyEngine/ledger]
        [--ledger-branch codex/thesis-ledger-facts]
        [--ledger-path ledger/official_observations.jsonl]

Requires `gh` auth with write access to the ledger repo unless --dry-run.
Idempotent: refs already present in the ledger are skipped.
"""

from __future__ import annotations

import argparse
import base64
import copy
import csv
import datetime as dt
import gzip
import hashlib
import http.client
import io
import json
import math
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote, urlparse

from canonical_json import canonical_bytes, canonical_sha256
from ledger_release_chain import (
    DEFAULT_CLOCK_SKEW_SECONDS,
    LEDGER_RELATIVE,
    MANIFEST_RELATIVE,
    PREFIX_RELATIVE,
    SCHEMA_VERSION,
    ChainVerification,
    jsonl_line_offsets,
    manifest_filename,
    producer_signature_path_for_manifest,
    receipt_paths_for_manifest,
    sha256_bytes,
    validate_manifest_schema,
    verify_producer_signature_bytes,
    verify_release_chain,
)
from register_targets import RegistrationError, registration_content_hash
from thesis_log_client import load_thesis_log
from verify_custody import verify_run

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOG_URL = "https://app.thesisinstitute.org/log.json"
# ALFRED with a vintage date pins the ADVANCE print (what the resolver rules
# name); plain FRED would silently hand back revised values on backfills.
FRED_CSV = (
    "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
    "?id={series}&vintage_date={vintage}"
)

MAX_TIMESTAMP_TOKEN_BYTES = 1024 * 1024
DEFAULT_TIMESTAMP_TIMEOUT_SECONDS = 45.0
PRODUCER_SIGNING_KEY_ENV = "LEDGER_PRODUCER_SIGNING_KEY"
TSA_ENDPOINTS = {
    "freetsa": "https://freetsa.org/tsr",
    # DigiCert's documented RFC 3161 endpoint is plain HTTP (its TLS endpoint
    # does not answer timestamp queries). The signed token is verified against
    # the separately pinned trust anchor before the proposal branch exists.
    "digicert": "http://timestamp.digicert.com",
}
TimestampRequester = Callable[[str, bytes, float], bytes]


class LedgerProposalError(RuntimeError):
    """A witnessed ledger proposal could not be constructed or published."""


@dataclass(frozen=True)
class RepositoryTree:
    tree_sha: str
    files: dict[str, bytes]
    modes: dict[str, str]
    blob_shas: dict[str, str]


def _validate_timestamp_timeout(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LedgerProposalError(
            "timeout_seconds must be a finite positive number"
        )
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise LedgerProposalError(
            "timeout_seconds must be a finite positive number"
        )
    return result


def request_timestamp(endpoint: str, query: bytes, timeout_seconds: float) -> bytes:
    """POST one DER RFC 3161 query and return a size-bounded response."""

    if endpoint not in TSA_ENDPOINTS.values():
        raise LedgerProposalError(f"refusing unapproved TSA endpoint: {endpoint!r}")
    if type(query) is not bytes or not query:
        raise LedgerProposalError("RFC 3161 query must be non-empty bytes")
    timeout = _validate_timestamp_timeout(timeout_seconds)
    request = urllib.request.Request(
        endpoint,
        data=query,
        headers={
            "Content-Type": "application/timestamp-query",
            "User-Agent": "Thesis-Ledger-Release-Witness/1",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        token = response.read(MAX_TIMESTAMP_TOKEN_BYTES + 1)
    if not token:
        raise LedgerProposalError(f"TSA returned an empty response: {endpoint}")
    if len(token) > MAX_TIMESTAMP_TOKEN_BYTES:
        raise LedgerProposalError(
            f"TSA response exceeds the one-megabyte limit: {endpoint}"
        )
    return token


def _build_timestamp_query(manifest: bytes, timeout_seconds: float) -> bytes:
    """Build the DER query whose SHA-256 imprint covers exact manifest bytes."""

    with tempfile.TemporaryDirectory(prefix="thesis-release-query-") as name:
        temporary = pathlib.Path(name)
        manifest_path = temporary / "manifest.json"
        query_path = temporary / "request.tsq"
        manifest_path.write_bytes(manifest)
        try:
            completed = subprocess.run(
                [
                    "openssl",
                    "ts",
                    "-query",
                    "-config",
                    "/dev/null",
                    "-data",
                    str(manifest_path),
                    "-sha256",
                    "-cert",
                    "-out",
                    str(query_path),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env={**os.environ, "LC_ALL": "C", "OPENSSL_CONF": "/dev/null"},
            )
        except FileNotFoundError as exc:
            raise LedgerProposalError(
                "openssl is required to construct the RFC 3161 query"
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise LedgerProposalError(
                "OpenSSL timestamp-query construction timed out"
            ) from exc
        if completed.returncode != 0:
            diagnostic = (completed.stderr or completed.stdout).strip()
            raise LedgerProposalError(
                "OpenSSL timestamp-query construction failed: "
                f"{diagnostic[-1000:] or 'no diagnostic'}"
            )
        try:
            query = query_path.read_bytes()
        except FileNotFoundError as exc:
            raise LedgerProposalError(
                "OpenSSL did not produce the RFC 3161 query"
            ) from exc
    if not query or len(query) > MAX_TIMESTAMP_TOKEN_BYTES:
        raise LedgerProposalError("OpenSSL produced an invalid-sized RFC 3161 query")
    return query


def _sign_release_manifest(
    manifest: bytes,
    signing_key: str | None,
    timeout_seconds: float,
) -> bytes:
    """Materialize the PEM for OpenSSL without parsing or logging its contents."""

    if type(manifest) is not bytes:
        raise LedgerProposalError("producer-signed manifest payload must be bytes")
    if type(signing_key) is not str or not signing_key.strip():
        raise LedgerProposalError(
            f"{PRODUCER_SIGNING_KEY_ENV} must contain a non-empty PEM private key"
        )
    timeout = _validate_timestamp_timeout(timeout_seconds)

    with tempfile.TemporaryDirectory(prefix="thesis-release-signature-") as name:
        temporary = pathlib.Path(name)
        # TemporaryDirectory is private by default; make that property explicit
        # before materializing secret bytes and use exclusive creation below.
        temporary.chmod(0o700)
        key_path = temporary / "producer-private.pem"
        manifest_path = temporary / "manifest.json"
        signature_path = temporary / "producer.sig"
        descriptor = -1
        try:
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            descriptor = os.open(key_path, flags, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
                descriptor = -1
                stream.write(signing_key)

            manifest_path.write_bytes(manifest)
            environment = os.environ.copy()
            environment.pop(PRODUCER_SIGNING_KEY_ENV, None)
            environment.update({"LC_ALL": "C", "OPENSSL_CONF": "/dev/null"})
            try:
                completed = subprocess.run(
                    [
                        "openssl",
                        "pkeyutl",
                        "-sign",
                        "-inkey",
                        str(key_path),
                        "-rawin",
                        "-in",
                        str(manifest_path),
                        "-out",
                        str(signature_path),
                    ],
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=timeout,
                    env=environment,
                )
            except FileNotFoundError as exc:
                raise LedgerProposalError(
                    "OpenSSL 3 is required for Ed25519 producer signing"
                ) from exc
            except subprocess.TimeoutExpired:
                raise LedgerProposalError(
                    "OpenSSL producer signing timed out"
                ) from None
            if completed.returncode != 0:
                raise LedgerProposalError(
                    "OpenSSL producer signing failed "
                    f"with exit code {completed.returncode}"
                )
            try:
                signature = signature_path.read_bytes()
            except FileNotFoundError as exc:
                raise LedgerProposalError(
                    "OpenSSL producer signing did not emit a signature"
                ) from exc
        finally:
            if descriptor >= 0:
                os.close(descriptor)
            # Do not rely only on TemporaryDirectory cleanup for key erasure:
            # unlink as soon as OpenSSL is done, including every failure path.
            try:
                key_path.unlink()
            except FileNotFoundError:
                pass
    if len(signature) != 64:
        raise LedgerProposalError(
            "OpenSSL producer signing did not emit a 64-byte raw Ed25519 signature"
        )
    return signature


def _request_timestamp_receipts(
    query: bytes,
    *,
    requester: TimestampRequester,
    timeout_seconds: float,
) -> dict[str, bytes]:
    receipts: dict[str, bytes] = {}
    for tsa, endpoint in TSA_ENDPOINTS.items():
        try:
            token = requester(endpoint, query, timeout_seconds)
        except (
            http.client.HTTPException,
            OSError,
            LedgerProposalError,
            urllib.error.URLError,
        ) as exc:
            raise LedgerProposalError(f"{tsa} timestamp request failed: {exc}") from exc
        except Exception as exc:
            raise LedgerProposalError(f"{tsa} timestamp request failed: {exc}") from exc
        if type(token) is not bytes or not token:
            raise LedgerProposalError(f"{tsa} TSA must return non-empty bytes")
        if len(token) > MAX_TIMESTAMP_TOKEN_BYTES:
            raise LedgerProposalError(
                f"{tsa} TSA response exceeds the one-megabyte limit"
            )
        receipts[tsa] = token
    return receipts


def utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def fred_advance_value(
    series_id: str, week: str, vintage: str
) -> tuple[float | None, bytes | None, str, str]:
    """The series value for `week` as printed on `vintage` (advance print)."""
    url = FRED_CSV.format(series=series_id, vintage=vintage)
    retrieved_at = utc_now()
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            raw = r.read()
    except urllib.error.HTTPError:
        return None, None, url, retrieved_at
    text = raw.decode()
    for row in csv.DictReader(io.StringIO(text)):
        date = row.get("observation_date") or row.get("DATE")
        value = row.get(f"{series_id}_{vintage.replace('-', '')}") or row.get(series_id)
        if date == week and value not in (None, "", "."):
            return float(value), raw, url, retrieved_at
    return None, raw, url, retrieved_at


def fred_vintage_series(
    series_id: str, vintage: str
) -> tuple[dict[str, float], bytes | None, str, str]:
    """Every dated value of `series_id` as printed on `vintage`."""
    url = FRED_CSV.format(series=series_id, vintage=vintage)
    retrieved_at = utc_now()
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            raw = r.read()
    except urllib.error.HTTPError:
        return {}, None, url, retrieved_at
    rows: dict[str, float] = {}
    for row in csv.DictReader(io.StringIO(raw.decode())):
        date = row.get("observation_date") or row.get("DATE")
        value = row.get(f"{series_id}_{vintage.replace('-', '')}") or row.get(
            series_id
        )
        if date and value not in (None, "", "."):
            rows[date] = float(value)
    return rows, raw, url, retrieved_at


# Generic ALFRED adapters for monthly/quarterly first prints, one entry per
# dataPointId series stem. Every mapping was verified against the cell's own
# published history at each anchor's FIRST-PRINT vintage before being added
# (2026-07-10; e.g. all six BEA April anchors matched to the 0.1 at the
# 2026-06-05 vintage) — a candidate series that cannot reproduce the cell's
# recorded history must never resolve it. Transforms:
#   level         — the period's value as printed
#   mom_diff      — period minus prior period, same vintage (payroll change
#                   as BLS headlines it)
#   pct_change_1d — percent change from prior period, one decimal (how BEA
#                   headlines PCE price changes)
ALFRED_ADAPTERS: dict[str, dict[str, Any]] = {
    "bls.ces.total_nonfarm_payroll_change": {
        "fred": "PAYEMS",
        "transform": "mom_diff",
        "unit": "thousands",
        "label": "US nonfarm payroll change",
        "source_name": "bls_ces",
        "source_table": "Employment Situation, Table B-1 (total nonfarm)",
        "concept_authority": "bls",
    },
    "bls.cps.unemployment_rate": {
        "fred": "UNRATE",
        "transform": "level",
        "unit": "percent",
        "label": "US unemployment rate",
        "source_name": "bls_cps",
        "source_table": "Employment Situation, Table A-1",
        "concept_authority": "bls",
    },
    "bls.jolts.job_openings_total": {
        "fred": "JTSJOL",
        "transform": "level",
        "unit": "thousands",
        "label": "US job openings, total nonfarm",
        "source_name": "bls_jolts",
        "source_table": "JOLTS news release, Table 1",
        "concept_authority": "bls",
    },
    "bls.jolts.job_openings": {
        "fred": "JTSJOL",
        "transform": "level",
        "unit": "millions",
        "scale": 0.001,
        "round": 3,
        "label": "US job openings, total nonfarm",
        "source_name": "bls_jolts",
        "source_table": "JOLTS news release, Table 1",
        "concept_authority": "bls",
    },
    "bls.cpi.u.core_mom": {
        "fred": "CPILFESL",
        "transform": "pct_change_1d",
        "unit": "percent_growth",
        "label": "US core CPI-U, monthly change",
        "source_name": "bls_cpi",
        "source_table": "Consumer Price Index news release",
        "concept_authority": "bls",
    },
    "bls.cpi.u.headline_mom": {
        "fred": "CPIAUCSL",
        "transform": "pct_change_1d",
        "unit": "percent_growth",
        "label": "US CPI-U all items, monthly change",
        "source_name": "bls_cpi",
        "source_table": "Consumer Price Index news release",
        "concept_authority": "bls",
    },
    "bea.pce.core_mom": {
        "fred": "PCEPILFE",
        "transform": "pct_change_1d",
        "unit": "percent_growth",
        "label": "US core PCE price index, monthly change",
        "source_name": "bea",
        "source_table": "Personal Income and Outlays",
        "concept_authority": "bea",
    },
    "us.bea.core_pce.mom_sa": {
        "fred": "PCEPILFE",
        "transform": "pct_change_1d",
        "unit": "percent_growth",
        "label": "US core PCE price index, monthly change",
        "source_name": "bea",
        "source_table": "Personal Income and Outlays",
        "concept_authority": "bea",
    },
    "bea.pce_price_index.monthly_change": {
        "fred": "PCEPI",
        "transform": "pct_change_1d",
        "unit": "percent_growth",
        "label": "US PCE price index, monthly change",
        "source_name": "bea",
        "source_table": "Personal Income and Outlays",
        "concept_authority": "bea",
    },
    "bea.real_gdp.saar": {
        "fred": "A191RL1Q225SBEA",
        "transform": "level",
        "unit": "percent_growth",
        "label": "US real GDP, SAAR percent change",
        "source_name": "bea",
        "source_table": "Gross Domestic Product news release",
        "concept_authority": "bea",
    },
    "bea.disposable_personal_income.level": {
        "fred": "DSPI",
        "transform": "level",
        "unit": "usd_billions",
        "label": "US disposable personal income, SAAR level",
        "source_name": "bea",
        "source_table": "Personal Income and Outlays, Table 1",
        "concept_authority": "bea",
    },
    "bea.government_social_benefits.level": {
        "fred": "A063RC1",
        "transform": "level",
        "unit": "usd_billions",
        "label": "US government social benefits to persons, SAAR level",
        "source_name": "bea",
        "source_table": "Personal Income and Outlays, Table 1",
        "concept_authority": "bea",
    },
    "bea.government_social_benefits.social_security": {
        "fred": "W823RC1",
        "transform": "level",
        "unit": "usd_billions",
        "label": "US social security benefits, SAAR level",
        "source_name": "bea",
        "source_table": "Personal Income and Outlays, Table 1",
        "concept_authority": "bea",
    },
    "bea.government_social_benefits.medicare": {
        "fred": "W824RC1",
        "transform": "level",
        "unit": "usd_billions",
        "label": "US Medicare benefits, SAAR level",
        "source_name": "bea",
        "source_table": "Personal Income and Outlays, Table 1",
        "concept_authority": "bea",
    },
    "bea.government_social_benefits.medicaid": {
        "fred": "W729RC1",
        "transform": "level",
        "unit": "usd_billions",
        "label": "US Medicaid benefits, SAAR level",
        "source_name": "bea",
        "source_table": "Personal Income and Outlays, Table 1",
        "concept_authority": "bea",
    },
    "bea.wages_and_salaries.level": {
        "fred": "A576RC1",
        "transform": "level",
        "unit": "usd_billions",
        "label": "US wages and salaries, SAAR level",
        "source_name": "bea",
        "source_table": "Personal Income and Outlays, Table 1",
        "concept_authority": "bea",
    },
    "bea.personal_current_taxes.level": {
        "fred": "W055RC1",
        "transform": "level",
        "unit": "usd_billions",
        "label": "US personal current taxes, SAAR level",
        "source_name": "bea",
        "source_table": "Personal Income and Outlays, Table 1",
        "concept_authority": "bea",
    },
}

# CPS Table A-19 detail rows have no FRED mirror, so they resolve from an
# immutable Wayback Machine snapshot of the cells' OWN bound source page
# (bls.gov blocks non-browser fetches; web.archive.org serves the exact
# bytes and independently timestamps them). One snapshot per data month,
# captured right after the Employment Situation release. The three rows
# that DO have FRED mirrors (office/admin, production, transport) were
# cross-checked against ALFRED at the release vintage and matched exactly.
A19_SNAPSHOT_URLS: dict[str, str] = {
    "2026-06": (
        "https://web.archive.org/web/20260710110509/"
        "https://www.bls.gov/web/empsit/cpseea19.htm"
    ),
}
A19_ROW_LABELS: dict[str, str] = {
    "business_financial_operations": "Business and financial operations occupations",
    "computer_mathematical": "Computer and mathematical occupations",
    "healthcare_support": "Healthcare support occupations",
    "office_administrative_support": (
        "Office and administrative support occupations"
    ),
    "production": "Production occupations",
    "transportation_material_moving": (
        "Transportation and material moving occupations"
    ),
}
A19_STEM = "bls.cps.employed_people_by_occupation"

# BLS CES detailed-industry cells (defense batch: aerospace product and
# parts, ship and boat building, federal Department of Defense) resolve
# directly from the BLS Public Data API v2 series their resolutionSourceUrls
# bind — two of the three have no FRED mirror. The API serves CURRENT
# estimates only (no ALFRED-style vintage archive), so first-print
# discipline is temporal: a period is captured only while it is still the
# series' latest published month AND still carries BLS's preliminary "P"
# footnote — the window between the Employment Situation release that first
# prints it and the next one (~4 weeks; the daily resolver cron lands on
# day one). A period found outside that window has been revised and is
# refused rather than recorded as a first print.
#
# Detailed industries print one month behind headline CES: June 2026 was
# not in the 2026-07-02 release the cells' resolutionDate names (verified
# live 2026-07-10: May 2026 was the latest print), so the adapter defers
# ("not yet published") until it lands — expected with the 2026-08-07
# Employment Situation.
#
# Anchors are the cells' own recorded history, i.e. FIRST prints, while the
# API returns current estimates, so anchor equality is tolerance-based:
# CES monthly recalculations move detailed first prints by a few tenths of
# a percent (observed while wiring this adapter: DoD April 2026 printed
# 474.9, read 476.6 at the 2026-07-10 vintage, +0.36%), and annual
# benchmarking can move levels by low single digits. 2% relative slack is
# publication-appropriate and still orders of magnitude tighter than the
# wrong-series/wrong-unit failures the gate exists to catch; if a later
# benchmark pushes an anchor past it, the refusal forces manual review
# rather than silently resolving from a redefined series.
BLS_API_URL = (
    "https://api.bls.gov/publicAPI/v2/timeseries/data/{series}"
    "?startyear={start}&endyear={end}"
)
BLS_ANCHOR_TOLERANCE = 0.02
BLS_API_ADAPTERS: dict[str, dict[str, Any]] = {
    "bls.ces.aerospace_product_and_parts_employment": {
        "series_id": "CES3133640001",
        "unit": "thousands",
        "label": "US aerospace product and parts employment (SA)",
        "source_name": "bls_ces",
        "source_table": (
            "Current Employment Statistics, all employees, aerospace "
            "product and parts manufacturing (SA)"
        ),
        "concept_authority": "bls",
        "source_concept": "CES3133640001",
        "anchor_start_year": 2025,
        "anchors": {
            "2025-06": 566.8,
            "2025-12": 577.6,
            "2026-02": 579.9,
            "2026-04": 585.4,
        },
    },
    "bls.ces.ship_and_boat_building_employment": {
        "series_id": "CES3133660001",
        "unit": "thousands",
        "label": "US ship and boat building employment (SA)",
        "source_name": "bls_ces",
        "source_table": (
            "Current Employment Statistics, all employees, ship and boat "
            "building (SA)"
        ),
        "concept_authority": "bls",
        "source_concept": "CES3133660001",
        "anchor_start_year": 2024,
        "anchors": {
            "2024-06": 153.2,
            "2025-06": 149.4,
            "2025-12": 148.8,
            "2026-04": 148.5,
        },
    },
    "bls.ces.federal_department_of_defense_employment": {
        "series_id": "CES9091911001",
        "unit": "thousands",
        "label": "US federal Department of Defense employment (SA)",
        "source_name": "bls_ces",
        "source_table": (
            "Current Employment Statistics, all employees, federal "
            "government, Department of Defense (SA)"
        ),
        "concept_authority": "bls",
        "source_concept": "CES9091911001",
        "anchor_start_year": 2025,
        "anchors": {
            "2025-06": 560.0,
            "2025-12": 490.1,
            "2026-02": 478.2,
            "2026-04": 474.9,
        },
    },
}
for _spec in BLS_API_ADAPTERS.values():
    _spec["evidence_notes"] = (
        "First print for {period} captured from {source_url} (BLS Public "
        "Data API v2, current estimates only) inside the first-print "
        "window: at capture the value was still the series' latest "
        "published month and still carried BLS's preliminary footnote."
    )

# ---------------------------------------------------------------------------
# CMS provider-data (Care Compare) adapters (2026-07-20). Each monthly
# refresh REPLACES the published CSV in place, so the first print for a
# refresh is only capturable while that refresh is the live file. The
# metastore item is the release ledger: `modified` stamps the refresh's
# processing vintage (the first of the refresh month) and the distribution
# URL rotates per refresh, so the adapter reads the metastore first, gates
# on the modified month matching the cell's period, and only then downloads
# the CSV. A capture attempted after the next refresh replaces the file
# fails closed ("window missed") rather than resolving a later vintage.
CMS_PROVIDER_DATA_ADAPTERS: dict[str, dict[str, Any]] = {
    "cms.nursing_home_compare.reported_total_nurse_staffing_hprd_us": {
        "metastore_url": (
            "https://data.cms.gov/provider-data/api/1/metastore/schemas/"
            "dataset/items/xcdc-v8bm"
        ),
        "state_row": "NATION",
        "row_column": "State or Nation",
        "value_column": (
            "Reported Total Nurse Staffing Hours per Resident per Day"
        ),
        "processing_date_column": "Processing Date",
        "unit": "ratio",
        "round": 3,
        "label": (
            "US nursing home reported total nurse staffing hours per "
            "resident per day (Care Compare national average)"
        ),
        "source_name": "cms_provider_data",
        "source_table": (
            "Nursing home Care Compare provider data, State US Averages "
            "(NH_StateUSAverages)"
        ),
        "concept_authority": "cms",
        "source_concept": (
            "Reported Total Nurse Staffing Hours per Resident per Day"
        ),
        # Fail-closed sanity range: reported national total nurse staffing
        # HPRD has printed in the high-3s for years; anything outside this
        # band is a wrong column, wrong row, or upstream restructuring.
        "sanity_range": (2.0, 6.0),
        "evidence_notes": (
            "First print for {period} captured from {source_url}: the CMS "
            "provider-data metastore's modified date placed the live "
            "NH_StateUSAverages file inside the {period} refresh window at "
            "capture, and the file's own Processing Date column agreed."
        ),
    },
    # Computed metric: national occupancy = sum(residents/day) over
    # sum(certified beds) across every facility row in the Provider
    # Information file — one division over one official file, per the
    # cell's registered resolution rule.
    "cms.care_compare.nursing_home_occupancy_pct": {
        "metastore_url": (
            "https://data.cms.gov/provider-data/api/1/metastore/schemas/"
            "dataset/items/4pq5-n9py"
        ),
        "aggregate": {
            "numerator_column": "Average Number of Residents per Day",
            "denominator_column": "Number of Certified Beds",
            "scale": 100.0,
            # A truncated download would silently bias a sum ratio; the
            # file has carried ~14k-15k certified facilities for years.
            "min_rows": 10000,
        },
        "processing_date_column": "Processing Date",
        "unit": "percent",
        "round": 2,
        "label": (
            "US nursing home occupancy, average residents per day as a "
            "share of certified beds (Care Compare provider file)"
        ),
        "source_name": "cms_provider_data",
        "source_table": (
            "Nursing home Care Compare provider data, Provider Information "
            "(NH_ProviderInfo)"
        ),
        "concept_authority": "cms",
        "source_concept": (
            "Average Number of Residents per Day / Number of Certified Beds"
        ),
        "sanity_range": (60.0, 95.0),
        "evidence_notes": (
            "First print for {period} captured from {source_url}: the CMS "
            "provider-data metastore's modified date placed the live "
            "NH_ProviderInfo file inside the {period} refresh window at "
            "capture; occupancy computed as sum of Average Number of "
            "Residents per Day over sum of Number of Certified Beds across "
            "all facility rows with both fields populated."
        ),
    },
}


def cms_provider_data_metastore(
    spec: dict[str, Any],
) -> tuple[str, str, str]:
    """(modified_date, download_url, retrieved_at) from the metastore item."""
    request = urllib.request.Request(
        spec["metastore_url"],
        headers={"User-Agent": INTL_USER_AGENT},
    )
    retrieved_at = utc_now()
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = json.loads(response.read().decode())
    modified = str(payload.get("modified") or "")
    distributions = payload.get("distribution") or []
    download_url = ""
    for distribution in distributions:
        candidate = str(distribution.get("downloadURL") or "")
        if candidate.lower().endswith(".csv"):
            download_url = candidate
            break
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", modified) or not download_url:
        raise ValueError(
            f"metastore item missing modified/downloadURL: {spec['metastore_url']}"
        )
    return modified, download_url, retrieved_at


def cms_provider_data_gate(period: str, modified: str) -> str | None:
    """None when `modified` is inside the period's refresh window, else the
    reason the capture must defer ("pending") or refuse ("missed")."""
    window_start = f"{period}-01"
    year, month = int(period[:4]), int(period[5:7])
    if month == 12:
        year, month = year + 1, 1
    else:
        month += 1
    window_end = f"{year}-{month:02d}-01"
    if modified < window_start:
        return (
            f"pending: metastore modified {modified} still before the "
            f"{period} refresh window"
        )
    if modified >= window_end:
        return (
            f"missed: metastore modified {modified} is past the {period} "
            f"refresh window; the first print is no longer the live file"
        )
    return None


def cms_provider_data_value(
    csv_bytes: bytes, spec: dict[str, Any], modified: str
) -> tuple[float | None, str | None]:
    """(value, refusal_reason) for the spec's metric in the live CSV.

    Two modes: a single row/column read (`state_row` + `value_column`), or
    an `aggregate` sum-ratio across every row (numerator over denominator,
    rows with either field unparseable skipped). Both cross-check the
    file's Processing Date against the metastore vintage and fail closed
    on restructured columns or out-of-band results.
    """
    reader = csv.DictReader(io.StringIO(csv_bytes.decode("utf-8-sig")))
    fieldnames = reader.fieldnames or []
    processing_column = spec.get("processing_date_column")

    def processing_date_mismatch(row: dict[str, Any]) -> str | None:
        if processing_column and row.get(processing_column) not in (
            None,
            "",
            modified,
        ):
            return (
                f"file Processing Date {row.get(processing_column)!r} "
                f"disagrees with metastore modified {modified!r}"
            )
        return None

    aggregate = spec.get("aggregate")
    if aggregate:
        numerator_column = aggregate["numerator_column"]
        denominator_column = aggregate["denominator_column"]
        if numerator_column not in fieldnames or (
            denominator_column not in fieldnames
        ):
            return None, (
                f"columns {numerator_column!r}/{denominator_column!r} not "
                "both present; upstream file restructured"
            )
        numerator_total = 0.0
        denominator_total = 0.0
        rows_used = 0
        first_row_checked = False
        for row in reader:
            if not first_row_checked:
                first_row_checked = True
                mismatch = processing_date_mismatch(row)
                if mismatch:
                    return None, mismatch
            try:
                numerator = float((row.get(numerator_column) or "").strip())
                denominator = float(
                    (row.get(denominator_column) or "").strip()
                )
            except ValueError:
                continue
            numerator_total += numerator
            denominator_total += denominator
            rows_used += 1
        min_rows = aggregate.get("min_rows", 1)
        if rows_used < min_rows:
            return None, (
                f"only {rows_used} usable rows (< {min_rows}); truncated "
                "download or upstream restructuring"
            )
        if denominator_total <= 0:
            return None, "denominator sum is not positive"
        value = (
            numerator_total / denominator_total * aggregate.get("scale", 1.0)
        )
    else:
        row_column = spec["row_column"]
        value_column = spec["value_column"]
        if row_column not in fieldnames or value_column not in fieldnames:
            return None, (
                f"columns {row_column!r}/{value_column!r} not both present; "
                "upstream file restructured"
            )
        target_row = next(
            (
                row
                for row in reader
                if row.get(row_column) == spec["state_row"]
            ),
            None,
        )
        if target_row is None:
            return None, f"row {spec['state_row']!r} not found"
        mismatch = processing_date_mismatch(target_row)
        if mismatch:
            return None, mismatch
        raw_value = (target_row.get(value_column) or "").strip()
        try:
            value = float(raw_value)
        except ValueError:
            return None, f"non-numeric value {raw_value!r} in {value_column!r}"
    low, high = spec["sanity_range"]
    if not (low <= value <= high):
        return None, (
            f"value {value} outside sanity range [{low}, {high}]; wrong "
            "row/column or upstream restructuring"
        )
    return round(value, spec.get("round", 4)), None

MONTH_NUMBERS = {
    name: number
    for number, name in enumerate(
        "january february march april may june july august september "
        "october november december".split(),
        start=1,
    )
}

# ---------------------------------------------------------------------------
# International native-source adapters (2026-07-10). ALFRED has no vintage
# coverage for these series, so each adapter binds the official national
# source the cells' resolver rules name. Every mapping below reproduced the
# cells' OWN recorded historicalContext anchors before being added, and the
# same anchor set is re-verified at fetch time (`anchors` on each spec) so a
# wrong series, wrong unit, or upstream restructuring fails closed instead
# of resolving a wrong fact. Where a recorded anchor and the official record
# disagreed, the official release-day artifact adjudicated; the evidence is
# documented inline per source.
#
# First-print discipline per source (anchors are FIRST prints; live APIs
# serve revised values on backfills):
#   - Sources whose published series are not revised (StatCan CPI, ABS
#     monthly CPI original, e-Stat CPI indexes) resolve from the current
#     value fetched between releases: that value IS the first print when
#     captured before the next release (the exact response bytes plus
#     retrievedAt are archived, so the vintage claim is auditable).
#   - Revision-prone series (LFS-style surveys, monthly GDP, EI counts)
#     additionally carry `first_print_window_days`: they resolve only while
#     the fetch instant is provably inside the window between the naming
#     release and the next one; after that the first print is no longer
#     retrievable from the live endpoint and the cell defers loudly.
#   - Series whose first prints are replaced on the SAME endpoint within
#     days (Eurostat retail benchmark revisions, ABS Building Approvals'
#     two-releases-per-month cycle) resolve only from immutable Wayback
#     snapshots of the month's own release page, pinned per period like
#     A19_SNAPSHOT_URLS. Eurostat HICP flash additionally requires the
#     target period to still carry its provisional/estimated status flag,
#     so a post-final fetch can never masquerade as the flash print.
INTL_USER_AGENT = "Mozilla/5.0 (compatible; thesis-resolver/1.0; +https://app.thesisinstitute.org)"

US_GEOGRAPHY = {
    "level": "country",
    "id": "0100000US",
    "vintage": "current",
    "name": "United States",
}
INTL_GEOGRAPHY = {
    "CA": {"level": "country", "id": "CA", "vintage": "current", "name": "Canada"},
    "AU": {"level": "country", "id": "AU", "vintage": "current", "name": "Australia"},
    "JP": {"level": "country", "id": "JP", "vintage": "current", "name": "Japan"},
    # "region" is the arch fact schema's level for supranational scopes
    # (ALLOWED_GEOGRAPHY_LEVELS in PolicyEngine/ledger arch/core.py).
    "EA": {
        "level": "region",
        "id": "EA21",
        "vintage": "current",
        "name": "Euro area",
    },
}

STATCAN_WDS_RANGE = (
    "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange"
    "?vectorIds={vector}&startRefPeriod={start}&endReferencePeriod={end}"
)
ABS_DATA_URL = (
    "https://data.api.abs.gov.au/rest/data/{flow}/{key}"
    "?lastNObservations={last_n}&format=jsondata"
)
EUROSTAT_DATA_URL = (
    "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{dataset}/{key}"
    "?format=JSON&startPeriod={start}"
)

# Cells whose recorded historicalContext contradicts the official series are
# never auto-resolved, even after their release date: resolving them would
# grade a target whose own registration evidence is unreliable. Each entry
# documents the contradiction; clearing one requires a human/analyst pass.
INTL_RESOLUTION_HOLDS = {
    "statjp.cpi.tokyo_all_items_annual_rate.july_2026.preliminary": (
        "the July-wave run recorded Tokyo anchors 2.9/2.9/3.5/3.4/3.4 "
        "(Feb-Jun 2026), but the official 2020-base Tokyo ku-area series "
        "prints 1.5/1.4/1.5/1.4/1.7 (Statistics Bureau kubu.pdf published "
        "2026-06-26 and e-Stat table 1-2); the recorded context appears to "
        "be a different vintage/series and must be reviewed before this "
        "cell may resolve"
    ),
}

# Pinned immutable snapshots per data month, one URL list per period tried
# in order (same custody model as A19_SNAPSHOT_URLS: web.archive.org serves
# exact bytes and independently timestamps them).
#
# Eurostat retail trade (euro area, volume, MoM SCA): the live sts_trtu_m /
# ei_isrr_m endpoints already serve benchmark-revised back months (Feb/Mar/
# Apr 2026 first prints 0.3/-0.1/-0.4 now read -0.4/0.8/-0.3), so only the
# release-day page witnesses the first print. Verified 2026-07-10: the
# 2026-06-04 release page headlines April at -0.4 (exact anchor match) and
# itself shows March already revised to 0.8, matching today's API; the
# 2026-07-06 release-day snapshot headlines May at +0.2, which the API
# still serves unrevised.
EUROSTAT_RETAIL_SNAPSHOT_URLS: dict[str, list[str]] = {
    "2026-05": [
        "https://web.archive.org/web/20260706201910/"
        "https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/4-06072026-bp",
    ],
}

# ABS Building Approvals (total dwellings, MoM % SA): the national SA
# series is not carried by the ABS Data API (BA_GCCSA serves Original
# only), and since May 2026 each month gets a first release then an update
# ~7 days later on the same page slug, so first prints must come from the
# release-day snapshot. Verified 2026-07-10: the apr-2026 page (released
# 2026-06-02) says "Total dwellings approved fell 3.4%, to 16,710" (exact
# anchor match) and the may-2026 release-day snapshot (2026-07-01, before
# the 7/08 update) says "Total dwellings approved fell 1.1% to 17,019".
ABS_BA_SNAPSHOT_URLS: dict[str, list[str]] = {
    "2026-05": [
        "https://web.archive.org/web/20260701030516/"
        "https://www.abs.gov.au/statistics/industry/building-and-construction/"
        "building-approvals-australia/may-2026",
    ],
}

# Statistics Bureau of Japan artifacts, pinned per period. The Tokyo ku-area
# CPI preliminary exists in machine-readable form only as the e-Stat table
# 1-2 workbook; each release mints a new immutable statInfId, so the pinned
# URL is itself a vintage artifact (keyless download, no e-Stat appId
# required). The LFS and household-spending pages are the release pages
# themselves; the parser refuses any artifact whose own printed reference
# month differs from the target period, so a rolled-over live page can
# never resolve an older cell (the trailing Wayback URL keeps the period
# resolvable after rollover).
JP_TOKYO_CPI_XLSX_URLS: dict[str, list[str]] = {
    "2026-06": [
        "https://www.e-stat.go.jp/stat-search/file-download"
        "?statInfId=000040461676&fileKind=0",
        "https://web.archive.org/web/20260710/https://www.e-stat.go.jp/stat-search/"
        "file-download?statInfId=000040461676&fileKind=0",
    ],
}
JP_LFS_LIVE_URLS = [
    "https://www.stat.go.jp/data/roudou/sokuhou/tsuki/index.html",
]
JP_LFS_PAGE_URLS: dict[str, list[str]] = {
    "2026-05": [
        "https://web.archive.org/web/20260710/https://www.stat.go.jp/data/roudou/"
        "sokuhou/tsuki/index.html",
    ],
}
JP_KAKEI_LIVE_URLS = [
    "https://www.stat.go.jp/data/kakei/sokuhou/tsuki/index.html",
]
JP_KAKEI_PAGE_URLS: dict[str, list[str]] = {
    "2026-05": [
        "https://web.archive.org/web/20260710/https://www.stat.go.jp/data/kakei/"
        "sokuhou/tsuki/index.html",
    ],
}

# One spec per dataPointId stem; dataPointId dialects of the same fact share
# a spec dict (and therefore one cached fetch and one archived response).
# `anchors` are the cells' recorded first prints re-checked at fetch time;
# `anchor_tolerance` encodes each source's documented revision behavior.
_STATCAN_CPI_SPEC = {
    "kind": "statcan",
    "series_id": "statcan-v41690973",
    "source_file": "getDataFromVectorByReferencePeriodRange (WDS JSON)",
    "extension": "json",
    "vector": 41690973,
    "product": "18-10-0004-01",
    "transform": "yoy_from_index",
    "round": 1,
    "unit": "percent",
    "label": "Canada CPI all-items, 12-month change (NSA)",
    "source_name": "statcan",
    "source_table": "Consumer Price Index, Table 18-10-0004-01 (all-items, Canada)",
    "concept_authority": "statcan",
    "source_concept": "v41690973",
    "country": "CA",
    # StatCan CPI indexes are not revised after publication (corrections
    # only), and the published 12-month change is computed from rounded
    # index values — verified 2026-07-10: computed YoY reproduced all six
    # recorded anchors exactly (Nov25 2.2, Dec25 2.4, Jan 2.3, Feb 1.8,
    # Mar 2.4, Apr 2.8). May 2026 was released 2026-06-22 on the updated
    # basket (weights effective 2026-06-15), which chain-links within the
    # same index series.
    "anchors": {"2026-01": 2.3, "2026-02": 1.8, "2026-03": 2.4, "2026-04": 2.8},
    "anchor_tolerance": 0.1,
}
_STATCAN_GDP_SPEC = {
    "kind": "statcan",
    "series_id": "statcan-v65201210",
    "source_file": "getDataFromVectorByReferencePeriodRange (WDS JSON)",
    "extension": "json",
    "vector": 65201210,
    "product": "36-10-0434-01",
    "transform": "mom_pct",
    "round": 1,
    "unit": "percent_growth",
    "label": "Canada real GDP by industry, all industries, MoM change (SA)",
    "source_name": "statcan",
    "source_table": (
        "GDP by industry, Table 36-10-0434-01 (all industries, chained "
        "2017 dollars, SA at annual rates)"
    ),
    "concept_authority": "statcan",
    "source_concept": "v65201210",
    "country": "CA",
    # Monthly GDP levels are revised at each release, moving back-month MoM
    # changes by ~0.1pp per step (recorded first prints Nov25 0.0, Dec25
    # 0.2, Jan 0.1 currently read 0.1, 0.1, -0.0). The three most recent
    # published months reproduced their recorded first prints exactly on
    # 2026-07-10 (Feb 0.2, Mar -0.1, Apr 0.5); the tolerance absorbs one
    # revision step while still refusing transform mistakes (April YoY
    # would read ~1.5, a 1.0pp miss).
    "anchors": {"2026-02": 0.2, "2026-03": -0.1, "2026-04": 0.5},
    "anchor_tolerance": 0.25,
    # The next monthly GDP release (~31 days later) revises the target
    # month itself, so the first print is only retrievable live until then.
    "first_print_window_days": 24,
}
_STATCAN_EI_SPEC = {
    "kind": "statcan",
    "series_id": "statcan-v64549350",
    "source_file": "getDataFromVectorByReferencePeriodRange (WDS JSON)",
    "extension": "json",
    "vector": 64549350,
    "product": "14-10-0011-01",
    "transform": "level",
    "scale": 0.001,
    "round": 2,
    "unit": "thousands",
    "label": "Canada EI regular beneficiaries (SA)",
    "source_name": "statcan",
    "source_table": (
        "Employment insurance beneficiaries, Table 14-10-0011-01 "
        "(regular benefits, Canada, SA)"
    ),
    "concept_authority": "statcan",
    "source_concept": "v64549350",
    "country": "CA",
    "entity": {"name": "person", "role": "ei_beneficiary"},
    # EI counts are administrative and re-seasonally-adjusted each release:
    # the latest month held exactly (Apr 544.44 recorded = 544.44 today),
    # the prior month drifted 0.56k in one release (Mar first print 548.0
    # -> 547.44), and February drifted ~8k over three releases, so only
    # the two freshest anchors are checked, at a tolerance wide enough for
    # documented SA refits but far below any wrong-series miss.
    "anchors": {"2026-03": 548.0, "2026-04": 544.44},
    "anchor_tolerance": 2.5,
    "first_print_window_days": 24,
}
_ABS_CPI_SPEC = {
    "kind": "abs",
    "series_id": "abs-cpi-allgroups-yoy",
    "source_file": "ABS Data API SDMX-JSON",
    "extension": "json",
    "flow": "CPI",
    "key": "3.10001.10.50.M",
    "transform": "level",
    "round": 1,
    "unit": "percent",
    "label": "Australia monthly CPI, all groups, annual change",
    "source_name": "abs",
    "source_table": (
        "Monthly Consumer Price Index (complete monthly CPI, dataflow CPI: "
        "annual change, all groups, original, weighted average of eight "
        "capital cities)"
    ),
    "concept_authority": "abs",
    "source_concept": "CPI/3.10001.10.50.M",
    "country": "AU",
    # Australia moved from the CPI_M indicator (final observation 2025-09)
    # to the complete monthly CPI published under dataflow CPI with
    # FREQ=M; the recorded anchors match the complete CPI exactly and
    # differ from the retired indicator (2025-09: 3.6 vs 3.5), so the
    # cells' series is the complete CPI. Original-series annual rates are
    # not revised; verified 2026-07-10 with six exact anchor matches
    # (Nov25 3.4, Dec25 3.8, Jan 3.8, Feb 3.7, Mar 4.6, Apr 4.2).
    "anchors": {"2026-02": 3.7, "2026-03": 4.6, "2026-04": 4.2},
    "anchor_tolerance": 0.1,
}
_ABS_UR_SPEC = {
    "kind": "abs",
    "series_id": "abs-lf-unemployment-rate",
    "source_file": "ABS Data API SDMX-JSON",
    "extension": "json",
    "flow": "LF",
    "key": "M13.3.1599.20.AUS.M",
    "transform": "level",
    "round": 1,
    "unit": "percent",
    "label": "Australia unemployment rate (SA)",
    "source_name": "abs",
    "source_table": (
        "Labour Force, Australia (dataflow LF: unemployment rate, persons, "
        "total age, seasonally adjusted, Australia)"
    ),
    "concept_authority": "abs",
    "source_concept": "LF/M13.3.1599.20.AUS.M",
    "country": "AU",
    # The Data API serves unrounded rates; rounding to one decimal (as ABS
    # headlines) reproduced every recorded first print on 2026-07-10
    # (Mar 4.278->4.3, Apr 4.481->4.5, May 4.356->4.4, the May release-day
    # page confirming "decreased by 0.1ppts to 4.4%"). SA rates revise by
    # ~0.1pp at later releases, hence the window and tolerance.
    "anchors": {"2026-03": 4.3, "2026-04": 4.5},
    "anchor_tolerance": 0.15,
    "first_print_window_days": 18,
}
_ABS_EMP_SPEC = {
    "kind": "abs",
    "series_id": "abs-lf-employed-persons",
    "source_file": "ABS Data API SDMX-JSON",
    "extension": "json",
    "flow": "LF",
    "key": "M3.3.1599.20.AUS.M",
    "transform": "mom_diff",
    "round": 1,
    "unit": "thousands",
    "label": "Australia employment change (SA)",
    "source_name": "abs",
    "source_table": (
        "Labour Force, Australia (dataflow LF: employed persons, seasonally "
        "adjusted, Australia; month-over-month change)"
    ),
    "concept_authority": "abs",
    "source_concept": "LF/M3.3.1599.20.AUS.M",
    "country": "AU",
    "entity": {"name": "person", "role": "employed"},
    # ABS headlines the SA change against the prior month AS REVISED IN THE
    # SAME RELEASE, so the first print equals the level diff only at the
    # release's own vintage (the 2026-06-25 release page prints 14,698,500
    # -> 14,738,800 = +40,300, matching the live diff on 2026-07-10).
    # Historical level anchors are useless here — LFS rebenchmarks moved
    # the recorded April level (14,737.4) to 14,698.5 in one release — so
    # the anchor pins the latest release's own level, and the window keeps
    # the fetch inside the vintage that headlined the target change.
    "anchor_transform": "raw_level",
    "anchors": {"2026-05": 14738.8},
    "anchor_tolerance": 60.0,
    "first_print_window_days": 18,
}
_ABS_BA_SPEC = {
    "kind": "abs_ba_release",
    "series_id": "abs-building-approvals-release",
    "source_file": "building-approvals-australia release page (Wayback snapshot)",
    "extension": "html",
    "snapshots": ABS_BA_SNAPSHOT_URLS,
    "unit": "percent_growth",
    "label": "Australia building approvals, total dwellings, MoM change (SA)",
    "source_name": "abs",
    "source_table": "Building Approvals, Australia (release page, key statistics)",
    "concept_authority": "abs",
    "source_concept": "building-approvals-australia release page",
    "country": "AU",
    "anchors": {},
    "anchor_tolerance": 0.0,
}
_STATJP_TOKYO_SPEC = {
    "kind": "estat_xlsx",
    "series_id": "estat-tokyo-cpi-table1-2",
    "source_file": "e-Stat table 1-2 workbook (Tokyo ku-area, release vintage)",
    "extension": "xlsx",
    "snapshots": JP_TOKYO_CPI_XLSX_URLS,
    "transform": "yoy_from_index",
    "round": 1,
    "unit": "percent",
    "label": "Japan Tokyo ku-area CPI all items, annual change (preliminary)",
    "source_name": "stat_jp",
    "source_table": (
        "2020-base CPI, Tokyo ku-area mid-month preliminary, e-Stat table "
        "1-2 (all items index)"
    ),
    "concept_authority": "stat_jp",
    "source_concept": "e-Stat statInfId 000040461676 (series 0001, all items)",
    "country": "JP",
    # The Statistics Bureau publishes the Tokyo preliminary YoY only in the
    # release PDF (CID-encoded, not machine-readable) and the e-Stat table
    # workbook; YoY computed from the workbook's rounded index reproduces
    # every published rate (kubu.pdf, 2026-06-26: Jan 1.5, Feb 1.5, Mar
    # 1.4, Apr 1.5, May 1.4, Jun 1.7), including both anchors this cell's
    # origin wave recorded (Apr 1.5, May 1.4). CPI indexes are unrevised;
    # the pinned statInfId is itself an immutable release vintage.
    "anchors": {"2026-04": 1.5, "2026-05": 1.4},
    "anchor_tolerance": 0.1,
}
_STATJP_LFS_SPEC = {
    "kind": "jp_lfs_page",
    "series_id": "statjp-lfs-monthly-page",
    "source_file": "stat.go.jp LFS monthly summary page",
    "extension": "html",
    "snapshots": JP_LFS_PAGE_URLS,
    "unit": "percent",
    "label": "Japan unemployment rate (SA)",
    "source_name": "stat_jp",
    "source_table": "Labour Force Survey, monthly summary page (SA rate table)",
    "concept_authority": "stat_jp",
    "source_concept": "stat.go.jp roudou sokuhou monthly page",
    "country": "JP",
    # The release page's own SA table carries the recent months, so one
    # fetch both anchors and resolves; verified 2026-07-10 against the
    # 2026-06-30 release (Feb 2.6, Mar 2.7, Apr 2.5 exact; May prints
    # 2.5). A misaligned parse fails the anchor check rather than
    # resolving a neighboring month.
    "anchors": {"2026-02": 2.6, "2026-03": 2.7, "2026-04": 2.5},
    "anchor_tolerance": 0.05,
}
_STATJP_KAKEI_SPEC = {
    "kind": "jp_kakei_page",
    "series_id": "statjp-kakei-monthly-page",
    "source_file": "stat.go.jp kakei monthly summary page",
    "extension": "html",
    "snapshots": JP_KAKEI_PAGE_URLS,
    "unit": "percent_growth",
    "label": (
        "Japan household spending, real YoY change "
        "(two-or-more-person households)"
    ),
    "source_name": "stat_jp",
    "source_table": (
        "Family Income and Expenditure Survey, monthly summary page "
        "(two-or-more-person households, real consumption expenditure)"
    ),
    "concept_authority": "stat_jp",
    "source_concept": "stat.go.jp kakei sokuhou monthly page",
    "country": "JP",
    # Kakei YoY figures are not revised across monthly releases (Feb -1.8
    # identical across the 2026-04, 2026-05-12 and 2026-07-07 vintages).
    # The cell's recorded March anchor (-0.5) is refuted by the official
    # record — the 2026-05-12 release printed March at -2.9 (Wayback
    # 2026-05-20 capture) and it still reads -2.9 today — so March is a
    # transcription error in the origin wave and is excluded; February and
    # April verify the row/column alignment instead.
    "anchors": {"2026-02": -1.8, "2026-04": -0.5},
    "anchor_tolerance": 0.05,
}
_EUROSTAT_HICP_SPEC = {
    "kind": "eurostat",
    "series_id": "eurostat-prc-hicp-minr-ea",
    "source_file": "Eurostat dissemination API JSON-stat",
    "extension": "json",
    "dataset": "prc_hicp_minr",
    "key": "M.RCH_A.TOTAL.EA21",
    "require_flag": True,
    "unit": "percent",
    "label": "Euro area HICP all-items flash estimate, annual rate",
    "source_name": "eurostat",
    "source_table": (
        "HICP (ECOICOP ver.2) monthly rates, prc_hicp_minr (all-items "
        "annual rate, euro area)"
    ),
    "concept_authority": "eurostat",
    "source_concept": "prc_hicp_minr/M.RCH_A.TOTAL.EA21",
    "country": "EA",
    # Eurostat loads the euro-area flash into prc_hicp_minr on release
    # morning flagged as an estimate; finals (~2 weeks later) replace the
    # value and drop the flag, so `require_flag` refuses any fetch that
    # can no longer see the flash vintage. Verified 2026-07-10: seven
    # exact anchor matches (Nov25 2.1 ... May26 3.2) and 2026-06 = 2.8
    # still flagged, matching the 2026-07-01 release headline "Euro area
    # annual inflation down to 2.8%". The pre-2026 dataset (prc_hicp_manr)
    # was frozen at 2025-12 by the ECOICOP-2 migration.
    "anchors": {"2026-03": 2.6, "2026-04": 3.0, "2026-05": 3.2},
    "anchor_tolerance": 0.1,
}
_EUROSTAT_UNEMP_SPEC = {
    "kind": "eurostat",
    "series_id": "eurostat-une-rt-m-ea",
    "source_file": "Eurostat dissemination API JSON-stat",
    "extension": "json",
    "dataset": "une_rt_m",
    "key": "M.SA.TOTAL.PC_ACT.T.EA21",
    "require_flag": False,
    "unit": "percent",
    "label": "Euro area unemployment rate (SA)",
    "source_name": "eurostat",
    "source_table": "Unemployment by sex and age, une_rt_m (euro area, SA, total)",
    "concept_authority": "eurostat",
    "source_concept": "une_rt_m/M.SA.TOTAL.PC_ACT.T.EA21",
    "country": "EA",
    # une_rt_m updates only on its monthly release day and revises back
    # months by <=0.2pp (ei_lm_m_vtg carries the documented vintages).
    # Verified 2026-07-10: the four freshest recorded first prints match
    # exactly (Feb 6.4, Mar 6.3, Apr 6.2, May 6.2; dataset updated
    # 2026-07-02, the May release day). An older recorded January anchor
    # (6.1) now reads 6.3 — documented revision drift, excluded.
    "anchors": {"2026-03": 6.3, "2026-04": 6.2},
    "anchor_tolerance": 0.2,
    "first_print_window_days": 21,
}
_EUROSTAT_RETAIL_SPEC = {
    "kind": "eurostat_release",
    "series_id": "eurostat-retail-trade-release",
    "source_file": "Euro indicators news release page (Wayback snapshot)",
    "extension": "html",
    "snapshots": EUROSTAT_RETAIL_SNAPSHOT_URLS,
    "unit": "percent_growth",
    "label": "Euro area retail trade volume, MoM change (SCA)",
    "source_name": "eurostat",
    "source_table": "Euro indicators news release, volume of retail trade",
    "concept_authority": "eurostat",
    "source_concept": "products-euro-indicators release page (euro area headline)",
    "country": "EA",
    "anchors": {},
    "anchor_tolerance": 0.0,
}

USASPENDING_API_ROOT = "https://api.usaspending.gov/api/v2"

# Registered-query snapshot family: USAspending revises continuously, so a
# target's outcome is the value its pinned query returns on the registered
# capture date (expectedReleaseWindow.start), never a source first print.
# Each spec mirrors the series' committed 7-key template in
# scripts/docket_series.json; the executor refuses on any drift between the
# registered binding and this table.
USASPENDING_ADAPTERS: dict[str, dict[str, Any]] = {
    "usaspending.dod.prime_award_obligations": {
        "url_template": (
            f"{USASPENDING_API_ROOT}/agency/097/awards/"
            "?fiscal_year={fiscal_year}"
        ),
        "field": "obligations",
        "series_id": "usaspending.agency.097.awards.obligations",
        "label": "US DoD prime award obligations, fiscal year to date",
        "unit": "billions USD",
        "scale": 1e-9,
        "round": 1,
        "source_name": "usaspending_api",
        "source_table": "USAspending API v2, agency 097 (DoD) award summary",
        "concept_authority": "usaspending",
        "source_concept": "obligations",
    },
    "usaspending.dod.prime_contract_obligations": {
        "url_template": (
            f"{USASPENDING_API_ROOT}/agency/097/obligations_by_award_category/"
            "?fiscal_year={fiscal_year}"
        ),
        "field": "results[category=contracts].aggregated_amount",
        "series_id": (
            "usaspending.agency.097.obligations_by_award_category.contracts"
        ),
        "label": "US DoD prime contract obligations, fiscal year to date",
        "unit": "billions USD",
        "scale": 1e-9,
        "round": 1,
        "source_name": "usaspending_api",
        "source_table": (
            "USAspending API v2, agency 097 (DoD) obligations by award "
            "category, contracts row"
        ),
        "concept_authority": "usaspending",
        "source_concept": "results[category=contracts].aggregated_amount",
    },
    "usaspending.dod.new_prime_awards": {
        "url_template": (
            f"{USASPENDING_API_ROOT}/agency/097/awards/new/count/"
            "?fiscal_year={fiscal_year}"
        ),
        "field": "new_award_count",
        "series_id": "usaspending.agency.097.awards.new_award_count",
        "label": "US DoD new prime awards, fiscal year to date",
        "unit": "millions",
        "scale": 1e-6,
        "round": 3,
        "source_name": "usaspending_api",
        "source_table": "USAspending API v2, agency 097 (DoD) new award count",
        "concept_authority": "usaspending",
        "source_concept": "new_award_count",
    },
    "usaspending.dod.prime_award_transactions": {
        "url_template": (
            f"{USASPENDING_API_ROOT}/agency/097/awards/"
            "?fiscal_year={fiscal_year}"
        ),
        "field": "transaction_count",
        "series_id": "usaspending.agency.097.awards.transaction_count",
        "label": "US DoD prime award transactions, fiscal year to date",
        "unit": "millions",
        "scale": 1e-6,
        "round": 3,
        "source_name": "usaspending_api",
        "source_table": "USAspending API v2, agency 097 (DoD) award summary",
        "concept_authority": "usaspending",
        "source_concept": "transaction_count",
    },
}
for _spec in USASPENDING_ADAPTERS.values():
    _spec["evidence_notes"] = (
        "Registered-query snapshot for {period} captured from {source_url} "
        "inside the preregistered snapshot window. USAspending revises "
        "continuously, so the outcome is defined as the value the pinned "
        "query returned on the registered capture date; the full response "
        "bytes are archived as evidence."
    )


def extract_json_field(payload: Any, selector: str) -> float | None:
    """Resolve a dotted selector with [key=value] list matches to a number.

    "results[category=contracts].aggregated_amount" walks payload["results"],
    picks the item whose "category" equals "contracts", then reads
    "aggregated_amount". Returns None when any hop is missing or the leaf is
    not a plain number, so the caller refuses instead of guessing.
    """
    current: Any = payload
    for segment in selector.split("."):
        match = re.fullmatch(r"([A-Za-z_]\w*)\[(\w+)=([^\]]+)\]", segment)
        if match:
            name, key, expected = match.groups()
            if not isinstance(current, dict):
                return None
            items = current.get(name)
            if not isinstance(items, list):
                return None
            current = next(
                (
                    item
                    for item in items
                    if isinstance(item, dict) and str(item.get(key)) == expected
                ),
                None,
            )
        else:
            if not isinstance(current, dict):
                return None
            current = current.get(segment)
        if current is None:
            return None
    if isinstance(current, bool) or not isinstance(current, (int, float)):
        return None
    return float(current)


def snapshot_window_state(today: dt.date, window: Any) -> str:
    """"pending" | "open" | "missed" | "invalid" for a snapshot window."""
    if not isinstance(window, dict):
        return "invalid"
    try:
        start = dt.date.fromisoformat(str(window.get("start")))
        end = dt.date.fromisoformat(str(window.get("end")))
    except (TypeError, ValueError):
        return "invalid"
    if start > end:
        return "invalid"
    if today < start:
        return "pending"
    if today > end:
        return "missed"
    return "open"


INTL_ADAPTERS: dict[str, dict[str, Any]] = {
    # Canada (two CPI dataPointId dialects name the same fact)
    "statcan.cpi.all_items_annual_rate.canada": _STATCAN_CPI_SPEC,
    "statcan.cpi.allitems.yoy": _STATCAN_CPI_SPEC,
    "statcan.gdp_by_industry.monthly_growth": _STATCAN_GDP_SPEC,
    "statcan.36-10-0434-01.all_industries.month_to_month_percent_change": (
        _STATCAN_GDP_SPEC
    ),
    "statcan.employment_insurance.regular_beneficiaries.canada": _STATCAN_EI_SPEC,
    # Australia (three CPI dialects: recorded wave, live-comparison, docket)
    "abs.cpi.all_groups_annual_rate.australia": _ABS_CPI_SPEC,
    "abs.cpi_indicator.allgroups.yoy": _ABS_CPI_SPEC,
    "abs.cpi.all_groups.yoy": _ABS_CPI_SPEC,
    "abs.labour.unemployment_rate.australia": _ABS_UR_SPEC,
    "abs.labour.employment_change.australia": _ABS_EMP_SPEC,
    "abs.building_approvals.total_dwellings_mom.australia": _ABS_BA_SPEC,
    # Japan
    "statjp.cpi.tokyo_all_items_annual_rate": _STATJP_TOKYO_SPEC,
    "statjp.lfs.unemployment_rate.japan": _STATJP_LFS_SPEC,
    "statjp.household_spending.real_yoy.two_or_more_person_households": (
        _STATJP_KAKEI_SPEC
    ),
    # Euro area (two flash HICP dialects name the same fact)
    "eurostat.hicp.all_items_annual_rate.euro_area": _EUROSTAT_HICP_SPEC,
    "eurostat.ea.hicp.flash.yoy": _EUROSTAT_HICP_SPEC,
    "eurostat.unemployment_rate.euro_area": _EUROSTAT_UNEMP_SPEC,
    "eurostat.retail_trade.volume_mom.euro_area": _EUROSTAT_RETAIL_SPEC,
}


def http_get(url: str, timeout: int = 120) -> tuple[bytes, str]:
    """Fetch raw bytes with the resolver UA; returns (bytes, retrievedAt)."""
    request = urllib.request.Request(url, headers={"User-Agent": INTL_USER_AGENT})
    retrieved_at = utc_now()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(), retrieved_at


def fetch_first(urls: list[str]) -> tuple[bytes, str, str]:
    """Try pinned URLs in order; returns (bytes, url, retrievedAt)."""
    last_error: Exception | None = None
    for url in urls:
        try:
            raw, retrieved_at = http_get(url)
            return raw, url, retrieved_at
        except Exception as exc:  # noqa: BLE001 - next pin is the fallback
            last_error = exc
    raise RuntimeError(f"all pinned URLs failed (last: {last_error})")


def statcan_series(vector: int) -> tuple[dict[str, float], bytes, str, str]:
    """StatCan WDS values keyed YYYY-MM (range covers YoY-12 + anchors)."""
    today = dt.date.today()
    url = STATCAN_WDS_RANGE.format(
        vector=vector,
        start=f"{today.year - 3}-01-01",
        end=today.isoformat(),
    )
    raw, retrieved_at = http_get(url)
    payload = json.loads(raw.decode())
    if not payload or payload[0].get("status") != "SUCCESS":
        raise ValueError(f"WDS status not SUCCESS for vector {vector}")
    points = payload[0]["object"]["vectorDataPoint"]
    series = {
        str(p["refPer"])[:7]: float(p["value"])
        for p in points
        if p.get("value") is not None
    }
    return series, raw, url, retrieved_at


def abs_series(flow: str, key: str) -> tuple[dict[str, float], bytes, str, str]:
    """ABS Data API (SDMX-JSON 2.0) single-series values keyed YYYY-MM."""
    url = ABS_DATA_URL.format(flow=flow, key=key, last_n=30)
    raw, retrieved_at = http_get(url)
    payload = json.loads(raw.decode())
    data = payload["data"]
    structure = data["structures"][0]
    times = [
        v["id"]
        for dim in structure["dimensions"]["observation"]
        if dim["id"] == "TIME_PERIOD"
        for v in dim["values"]
    ]
    all_series = data["dataSets"][0]["series"]
    if len(all_series) != 1:
        raise ValueError(f"ABS key {flow}/{key} matched {len(all_series)} series")
    observations = next(iter(all_series.values()))["observations"]
    series = {
        times[int(index)]: float(values[0])
        for index, values in observations.items()
        if values and values[0] is not None
    }
    return series, raw, url, retrieved_at


def eurostat_series(
    dataset: str, key: str
) -> tuple[dict[str, float], dict[str, str], bytes, str, str]:
    """Eurostat JSON-stat values + per-period status flags, keyed YYYY-MM."""
    today = dt.date.today()
    url = EUROSTAT_DATA_URL.format(
        dataset=dataset, key=key, start=f"{today.year - 2}-{today.month:02d}"
    )
    raw, retrieved_at = http_get(url)
    payload = json.loads(raw.decode())
    if "dimension" not in payload:
        raise ValueError(f"eurostat {dataset}/{key}: {str(payload)[:160]}")
    index_to_period = {
        v: k for k, v in payload["dimension"]["time"]["category"]["index"].items()
    }
    series = {
        index_to_period[int(flat)]: float(value)
        for flat, value in payload["value"].items()
    }
    status = payload.get("status")
    flags: dict[str, str] = {}
    if isinstance(status, dict):
        flags = {
            index_to_period[int(flat)]: str(flag)
            for flat, flag in status.items()
            if int(flat) in index_to_period
        }
    return series, flags, raw, url, retrieved_at


def estat_xlsx_index_series(raw: bytes) -> dict[str, float]:
    """All-items index by YYYY-MM from an e-Stat CPI table 1-x workbook.

    Cells map by column letter (recent rows are sparse, so document order
    lies); the all-items column is the one whose header row carries item
    code 0001.
    """
    import zipfile
    from xml.etree import ElementTree

    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    archive = zipfile.ZipFile(io.BytesIO(raw))
    shared: list[str] = []
    for item in ElementTree.fromstring(
        archive.read("xl/sharedStrings.xml")
    ).iter(f"{ns}si"):
        shared.append("".join(t.text or "" for t in item.iter(f"{ns}t")))
    rows: list[dict[str, str]] = []
    for row in ElementTree.fromstring(
        archive.read("xl/worksheets/sheet1.xml")
    ).iter(f"{ns}row"):
        cells: dict[str, str] = {}
        for cell in row.iter(f"{ns}c"):
            value = cell.find(f"{ns}v")
            column = re.match(r"([A-Z]+)", cell.get("r", ""))
            if value is None or column is None:
                continue
            cells[column.group(1)] = (
                shared[int(value.text)] if cell.get("t") == "s" else value.text
            )
        rows.append(cells)
    code_row = next(r for r in rows if any(v == "0001" for v in r.values()))
    items_column = next(c for c, v in code_row.items() if v == "0001")
    series: dict[str, float] = {}
    for row in rows:
        month = next(
            (
                v.strip()
                for v in row.values()
                if isinstance(v, str) and re.fullmatch(r"(19|20)\d{4}\s*", v)
            ),
            None,
        )
        if month and items_column in row:
            try:
                series[f"{month[:4]}-{month[4:6]}"] = float(row[items_column])
            except ValueError:
                continue
    return series


def decode_jp(raw: bytes) -> str:
    for encoding in ("shift_jis", "cp932", "utf-8"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("shift_jis", errors="replace")


def _jp_month_labels(text: str) -> list[str]:
    """YYYY-MM labels for a stat.go.jp monthly table header segment.

    Headers run like '2026年2月 3月 4月 5月': bare months inherit the last
    seen year.
    """
    labels: list[str] = []
    year = None
    for match in re.finditer(r"(\d{4})年(\d{1,2})月|(?<![年\d])(\d{1,2})月", text):
        if match.group(1):
            year = int(match.group(1))
            labels.append(f"{year}-{int(match.group(2)):02d}")
        elif year is not None:
            labels.append(f"{year}-{int(match.group(3)):02d}")
    return labels


def jp_lfs_unemployment_series(raw: bytes) -> dict[str, float]:
    """SA unemployment rates by month from the LFS monthly summary page."""
    text = re.sub(r"<[^>]+>", " ", decode_jp(raw))
    text = text.replace("&nbsp;", " ").replace("&#160;", " ")
    text = re.sub(r"[\s　]+", " ", text)
    segment = re.search(
        r"月次（季節調整値）(.{0,240}?)完全失業率((?:\s*[\d.]+%)+)", text
    )
    if not segment:
        raise ValueError("LFS page: SA table not found")
    labels = _jp_month_labels(segment.group(1))
    values = [float(v) for v in re.findall(r"([\d.]+)%", segment.group(2))]
    # The value row leads with calendar-year averages (one per bare year
    # label); the monthly values are the trailing ones matching the month
    # labels.
    if len(values) < len(labels):
        raise ValueError("LFS page: fewer rate values than month labels")
    return dict(zip(labels, values[len(values) - len(labels) :]))


def jp_kakei_real_yoy_series(raw: bytes) -> dict[str, float]:
    """Real YoY spending changes (two-or-more-person households) by month."""
    text = re.sub(r"<[^>]+>", "|", decode_jp(raw))
    text = text.replace("&nbsp;", " ").replace("&#160;", " ")
    text = re.sub(r"[ \t　]+", " ", text)
    flat = re.sub(r"[|\s]+", " ", text)
    header = re.search(r"月次（前年同月比(.{0,200}?)【二人以上の世帯】", flat)
    if not header:
        raise ValueError("kakei page: monthly header not found")
    labels = _jp_month_labels(header.group(1))
    row = re.search(
        r"【二人以上の世帯】\s*消費支出（実質）(.*?)(?:≪|実収入|【単身世帯】)",
        flat,
    )
    if not row:
        raise ValueError("kakei page: real consumption row not found")
    # YoY values are the bare numbers; bracketed 【..】 values are the MoM
    # SA series and are dropped. ▲ marks negatives.
    yoy: list[float] = []
    for token in re.finditer(r"(【[^】]*】)|(▲?\d+(?:\.\d+)?)", row.group(1)):
        if token.group(1):
            continue
        yoy.append(float(token.group(2).replace("▲", "-")))
    # The row leads with calendar-year averages; monthly values trail.
    if len(yoy) < len(labels):
        raise ValueError("kakei page: fewer YoY values than month labels")
    return dict(zip(labels, yoy[len(yoy) - len(labels) :]))


def jp_page_reference_period(raw: bytes) -> str | None:
    """The page's own printed reference month ('2026年(令和8年)5月分')."""
    text = re.sub(r"[\s　]+", "", decode_jp(raw))
    match = re.search(r"(\d{4})年（令和\d+年）(\d{1,2})月分", text)
    if not match:
        return None
    return f"{match.group(1)}-{int(match.group(2)):02d}"


MONTH_NAMES = {number: name.capitalize() for name, number in MONTH_NUMBERS.items()}


def eurostat_retail_headline(raw: bytes, period: str) -> float | None:
    """Signed euro-area MoM % from a retail-trade release page snapshot."""
    text = re.sub(r"<[^>]+>", " ", raw.decode("utf-8", errors="replace"))
    text = re.sub(r"(&nbsp;|&#160;|\s)+", " ", text)
    month_label = f"{MONTH_NAMES[int(period[5:7])]} {period[:4]}"
    match = re.search(
        rf"In {month_label}, compared with [A-Za-z]+ \d{{4}},? the seasonally "
        rf"adjusted retail trade volume (increased|decreased) by ([\d.]+)% "
        rf"in the euro area",
        text,
    )
    if not match:
        return None
    value = float(match.group(2))
    return value if match.group(1) == "increased" else -value


def abs_ba_headline(raw: bytes, period: str) -> float | None:
    """Signed SA total-dwellings MoM % from an ABS approvals release page."""
    text = re.sub(r"<[^>]+>", " ", raw.decode("utf-8", errors="replace"))
    text = re.sub(r"(&nbsp;|&#160;|\s)+", " ", text)
    month_label = f"{MONTH_NAMES[int(period[5:7])]} {period[:4]}"
    match = re.search(
        rf"The {month_label} seasonally adjusted estimate:?\s*Total dwellings "
        rf"approved (rose|fell) ([\d.]+)%",
        text,
    )
    if not match:
        return None
    value = float(match.group(2))
    return value if match.group(1) == "rose" else -value


def intl_transformed_value(
    spec: dict[str, Any], series: dict[str, float], period: str
) -> float | None:
    """Apply the spec's transform at `period` over a YYYY-MM keyed series."""
    transform = spec.get("transform", "level")
    if period not in series:
        return None
    if transform == "level":
        value = series[period]
    elif transform == "mom_diff":
        prior = prior_period_date(period, "month")
        if prior not in series:
            return None
        value = series[period] - series[prior]
    elif transform == "mom_pct":
        prior = prior_period_date(period, "month")
        if prior not in series or not series[prior]:
            return None
        value = (series[period] / series[prior] - 1) * 100
    elif transform == "yoy_from_index":
        prior = f"{int(period[:4]) - 1}-{period[5:7]}"
        if prior not in series or not series[prior]:
            return None
        value = (series[period] / series[prior] - 1) * 100
    else:
        raise ValueError(f"unknown intl transform {transform!r}")
    value *= spec.get("scale", 1)
    digits = spec.get("round")
    if digits is not None:
        value = round(value, digits)
    # IEEE -0.0 survives round() and splits Python's json ("-0.0") from
    # JSON.stringify ("0") downstream; normalize before the value enters
    # any ledger row (same guard as the spawn intake).
    return round(value, 4) + 0.0


def intl_anchor_failures(
    spec: dict[str, Any], series: dict[str, float]
) -> list[str]:
    """Anchor periods whose recorded first prints the fetch cannot reproduce.

    Failing closed here is the core safety property: a candidate series that
    cannot reproduce the cell's own recorded history must never resolve it.
    """
    failures = []
    for anchor_period, expected in (spec.get("anchors") or {}).items():
        if spec.get("anchor_transform") == "raw_level":
            # Anchors stated on the fetched series itself (used where the
            # published headline is a same-release diff whose historical
            # values are not stable enough to anchor on).
            actual = series.get(anchor_period)
        else:
            actual = intl_transformed_value(spec, series, anchor_period)
        if actual is None or abs(actual - expected) > spec["anchor_tolerance"]:
            failures.append(f"{anchor_period}: expected {expected}, got {actual}")
    return failures


def flash_vintage_missing(
    spec: dict[str, Any], flags: dict[str, str], period: str
) -> bool:
    """True when a flash-print spec can no longer see the flash vintage.

    Eurostat drops the provisional/estimated flag when finals replace the
    flash value on the same endpoint; resolving past that point would record
    the final as if it were the flash first print.
    """
    return bool(spec.get("require_flag")) and period not in flags


def intl_fetch(
    spec: dict[str, Any],
    period: str,
    cache: dict[Any, tuple],
) -> tuple[dict[str, float], dict[str, str], bytes, str, str]:
    """Fetch + parse one adapter artifact, cached so dialects share bytes.

    Returns (series keyed YYYY-MM, status flags, raw bytes, url,
    retrievedAt). For single-print page artifacts the series carries just
    the periods the page itself prints.
    """
    kind = spec["kind"]
    if kind == "statcan":
        cache_key = ("statcan", spec["vector"])
        if cache_key not in cache:
            series, raw, url, retrieved_at = statcan_series(spec["vector"])
            cache[cache_key] = (series, {}, raw, url, retrieved_at)
    elif kind == "abs":
        cache_key = ("abs", spec["flow"], spec["key"])
        if cache_key not in cache:
            series, raw, url, retrieved_at = abs_series(spec["flow"], spec["key"])
            cache[cache_key] = (series, {}, raw, url, retrieved_at)
    elif kind == "eurostat":
        cache_key = ("eurostat", spec["dataset"], spec["key"])
        if cache_key not in cache:
            series, flags, raw, url, retrieved_at = eurostat_series(
                spec["dataset"], spec["key"]
            )
            cache[cache_key] = (series, flags, raw, url, retrieved_at)
    elif kind in ("estat_xlsx", "jp_lfs_page", "jp_kakei_page",
                  "eurostat_release", "abs_ba_release"):
        # JP release pages replace their content monthly with no interim
        # revision, so the live page is tried first (this is how future
        # months resolve on release day without a new pin) and the parse's
        # own reference-month check rejects a rolled-over or stale page.
        # Snapshot-only kinds (approvals' two-release cycle, retail's
        # numbered release slugs) resolve exclusively from pinned URLs.
        urls = list(spec.get("live_urls") or []) + list(
            spec["snapshots"].get(period) or []
        )
        if not urls:
            raise LookupError(f"no pinned artifact registered for {period}")
        cache_key = (kind, spec["series_id"], period)
        if cache_key not in cache:
            failures: list[str] = []
            for url in urls:
                try:
                    raw, retrieved_at = http_get(url)
                    if kind == "estat_xlsx":
                        series = estat_xlsx_index_series(raw)
                        # The workbook is one release vintage; its newest
                        # month must be the target, else wrong vintage.
                        if not series or max(series) != period:
                            raise ValueError(
                                f"workbook's latest month is not {period}"
                            )
                    elif kind in ("jp_lfs_page", "jp_kakei_page"):
                        reference = jp_page_reference_period(raw)
                        if reference != period:
                            raise ValueError(
                                f"page reference month {reference} is not "
                                f"the target {period}"
                            )
                        series = (
                            jp_lfs_unemployment_series(raw)
                            if kind == "jp_lfs_page"
                            else jp_kakei_real_yoy_series(raw)
                        )
                    elif kind == "eurostat_release":
                        value = eurostat_retail_headline(raw, period)
                        series = {} if value is None else {period: value}
                    else:
                        value = abs_ba_headline(raw, period)
                        series = {} if value is None else {period: value}
                    cache[cache_key] = (series, {}, raw, url, retrieved_at)
                    break
                except Exception as exc:  # noqa: BLE001 - try the next pin
                    failures.append(f"{url}: {exc}")
            if cache_key not in cache:
                raise ValueError(
                    "no pinned artifact parsed cleanly: " + "; ".join(failures)
                )
    else:
        raise ValueError(f"unknown intl adapter kind {kind!r}")
    return cache[cache_key]


def parse_ref_period(ref: str, stem: str) -> tuple[str, str] | None:
    """(period_type, YYYY-MM) parsed from a dataPointId's period tail."""
    tail = ref[len(stem) + 1 :]
    tail = re.sub(
        r"\.(first_print|registered_query_snapshot|advance|second|third|flash"
        r"|preliminary)_?(estimate)?$",
        "",
        tail,
    )
    m = re.fullmatch(r"([a-z]+)_(\d{4})", tail)
    if m and m.group(1) in MONTH_NUMBERS:
        return "month", f"{m.group(2)}-{MONTH_NUMBERS[m.group(1)]:02d}"
    m = re.fullmatch(r"(\d{4})-(\d{2})", tail)
    if m:
        return "month", f"{m.group(1)}-{m.group(2)}"
    m = re.fullmatch(r"q([1-4])_(\d{4})", tail)
    if m:
        return "quarter", f"{m.group(2)}-{(int(m.group(1)) - 1) * 3 + 1:02d}"
    m = re.fullmatch(r"(\d{4})_q([1-4])", tail)
    if m:
        return "quarter", f"{m.group(1)}-{(int(m.group(2)) - 1) * 3 + 1:02d}"
    m = re.fullmatch(r"fy_?(\d{4})", tail)
    if m:
        return "fiscal_year", m.group(1)
    return None


def prior_period_date(period_date: str, period_type: str) -> str:
    year, month = int(period_date[:4]), int(period_date[5:7])
    step = 3 if period_type == "quarter" else 1
    month -= step
    if month < 1:
        month += 12
        year -= 1
    return f"{year}-{month:02d}"


def apply_transform(
    rows: dict[str, float], spec: dict[str, Any], period_type: str, period: str
) -> float | None:
    key = f"{period}-01"
    prior_key = f"{prior_period_date(period, period_type)}-01"
    if rows.get(key) is None:
        return None
    transform = spec["transform"]
    if transform == "level":
        value = rows[key]
    elif transform == "mom_diff":
        if rows.get(prior_key) is None:
            return None
        value = rows[key] - rows[prior_key]
    elif transform == "pct_change_1d":
        if rows.get(prior_key) is None:
            return None
        value = round((rows[key] / rows[prior_key] - 1) * 100, 1)
    else:
        raise ValueError(f"unknown transform {transform!r}")
    value *= spec.get("scale", 1)
    digits = spec.get("round")
    if digits is not None:
        value = round(value, digits)
    # IEEE -0.0 survives round() and splits Python's json ("-0.0") from
    # JSON.stringify ("0") downstream; normalize before the value enters
    # any ledger row (same guard as the spawn intake).
    return round(value, 4) + 0.0


def value_plausible(
    value: float, forecast_entry: dict[str, Any] | None
) -> bool:
    """Bounded unit-scale gate: a fetched value wildly outside the cell's
    own interval means a wrong series or transform (thousands-vs-millions
    class), never a legitimate outcome. Bounded at 4 interval-widths so a
    genuine surprise still resolves and grades."""
    interval = (forecast_entry or {}).get("interval80") or {}
    lower, upper = interval.get("lower"), interval.get("upper")
    if lower is None or upper is None:
        return True
    width = max(upper - lower, abs(upper) * 0.05, 1e-9)
    return (lower - 4 * width) <= value <= (upper + 4 * width)


def generic_fact(
    ref: str,
    spec: dict[str, Any],
    period_type: str,
    period: str,
    value: float,
    release_day: dt.date,
    source_url: str,
    source_file: str,
) -> dict:
    return {
        "source_record_id": ref,
        "label": f"{spec['label']}, {period}",
        "value": value,
        "observed_at": release_day.isoformat(),
        "period": {"type": period_type, "value": period},
        "domain": spec.get("domain", "economy"),
        "geography": INTL_GEOGRAPHY.get(spec.get("country", ""), US_GEOGRAPHY),
        "entity": spec.get("entity", {"name": "economy", "role": "aggregate"}),
        "measure": {
            "concept": re.sub(
            r"\.(first_print|registered_query_snapshot|flash|preliminary)$",
            "",
            ref,
        ),
            "unit": spec["unit"],
            "source_concept": spec.get("fred", spec.get("source_concept", "")),
            "concept_relation": "source_label",
            "concept_authority": spec["concept_authority"],
            "concept_evidence_url": source_url,
            "concept_evidence_notes": spec.get(
                "evidence_notes",
                "First print for {period} captured from {source_url} on the "
                "official release date named by the cell's resolver.",
            ).format(period=period, source_url=source_url),
        },
        "aggregation": {"method": "level"},
        "filters": {},
        "source": {
            "source_name": spec["source_name"],
            "source_table": spec["source_table"],
            "source_file": source_file,
            "url": source_url,
            "vintage": "first_print",
            "extracted_at": dt.date.today().isoformat(),
            "extraction_method": (
                "Automated first-print capture by scripts/resolve_pending.py "
                "(anchor-verified adapter)"
            ),
        },
        "source_row_keys": [period],
        "source_cell_keys": [spec.get("fred", spec.get("source_concept", ""))],
    }


def a19_values_from_html(html: str) -> dict[str, float]:
    """June-style A-19 parse: each row label followed by year-ago then
    current-month totals; the CURRENT month (second number) is the print."""
    text = re.sub(r"<[^>]+>", "|", html)
    text = re.sub(r"[\s|]+", " ", text)
    out: dict[str, float] = {}
    for key, label in A19_ROW_LABELS.items():
        m = re.search(re.escape(label) + r"\s+([0-9,]+)\s+([0-9,]+)", text)
        if m:
            out[key] = float(m.group(2).replace(",", ""))
    return out


def bls_rows_from_payload(raw: bytes, series_id: str) -> dict[str, dict[str, Any]]:
    """Monthly rows keyed YYYY-MM with the latest/preliminary markers the
    temporal first-print gate needs. Only a successful response for exactly
    `series_id` yields rows; anything else fails closed to empty."""
    try:
        payload = json.loads(raw.decode())
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}
    if payload.get("status") != "REQUEST_SUCCEEDED":
        return {}
    rows: dict[str, dict[str, Any]] = {}
    for series in (payload.get("Results") or {}).get("series") or []:
        if series.get("seriesID") != series_id:
            continue
        for row in series.get("data") or []:
            match = re.fullmatch(r"M(0[1-9]|1[0-2])", str(row.get("period")))
            if not match:
                continue
            try:
                value = float(row["value"])
            except (KeyError, TypeError, ValueError):
                continue
            rows[f"{row.get('year')}-{match.group(1)}"] = {
                "value": value,
                "latest": str(row.get("latest", "")).lower() == "true",
                "preliminary": any(
                    footnote.get("code") == "P"
                    for footnote in row.get("footnotes") or []
                    if isinstance(footnote, dict)
                ),
            }
    return rows


def bls_series_rows(
    series_id: str, start_year: int, end_year: int
) -> tuple[dict[str, dict[str, Any]], bytes | None, str, str]:
    """Every monthly value of `series_id` as the BLS API currently serves it,
    fetched keylessly from the cell's own bound resolutionSourceUrl."""
    url = BLS_API_URL.format(series=series_id, start=start_year, end=end_year)
    retrieved_at = utc_now()
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            raw = r.read()
    except urllib.error.HTTPError:
        return {}, None, url, retrieved_at
    rows = bls_rows_from_payload(raw, series_id)
    if not rows:
        # An error payload (rate limit, unknown series) must not archive as
        # if it were a print; surface it as a failed fetch instead.
        return {}, None, url, retrieved_at
    return rows, raw, url, retrieved_at


def bls_anchor_mismatches(
    rows: dict[str, dict[str, Any]], anchors: dict[str, float]
) -> list[str]:
    """Anchor periods whose fetched values cannot reproduce the cell's own
    recorded history within BLS_ANCHOR_TOLERANCE (see the adapter note on
    first prints vs current estimates)."""
    problems = []
    for anchor_period, expected in sorted(anchors.items()):
        state = rows.get(anchor_period)
        if state is None:
            problems.append(f"{anchor_period}=missing (recorded {expected})")
            continue
        if abs(state["value"] - expected) > BLS_ANCHOR_TOLERANCE * abs(expected):
            problems.append(
                f"{anchor_period}={state['value']} (recorded first print "
                f"{expected})"
            )
    return problems


def bls_first_print(
    rows: dict[str, dict[str, Any]], period: str
) -> tuple[float | None, str | None]:
    """(value, refusal): a value only while `period` is still the series'
    latest preliminary print; a present-but-revised period is refused, an
    absent one defers."""
    state = rows.get(period)
    if state is None:
        return None, None
    if not (state["latest"] and state["preliminary"]):
        return None, (
            f"{period} is published but no longer the latest preliminary "
            "print; the first-print window was missed — resolve manually "
            "from an archived vintage"
        )
    return state["value"], None


def claims_fact(
    ref: str, week: str, raw: float, kind: str, release_day: dt.date
) -> dict:
    """Build a ledger fact row for a weekly claims first print."""
    if kind == "initial":
        value, unit = round(raw / 1_000, 1), "thousands"
        concept = "us.dol.initial_claims.sa"
        fred_id, label = "ICSA", "US initial claims (SA, advance)"
    else:
        value, unit = round(raw / 1_000_000, 3), "millions"
        concept = "dol.eta.continued_claims.sa"
        fred_id, label = "CCSA", "US insured unemployment (SA, advance)"
    source_url = FRED_CSV.format(series=fred_id, vintage=release_day.isoformat())
    return {
        "source_record_id": ref,
        "label": f"{label}, week ending {week}",
        "value": value,
        "observed_at": release_day.isoformat(),
        "period": {"type": "week_ending", "value": week},
        "domain": "labor",
        "geography": {
            "level": "country",
            "id": "0100000US",
            "vintage": "current",
            "name": "United States",
        },
        "entity": {"name": "person", "role": "ui_claimant"},
        "measure": {
            "concept": concept,
            "unit": unit,
            "source_concept": fred_id,
            "concept_relation": "source_label",
            "concept_authority": "dol_eta",
            "concept_evidence_url": source_url,
            "concept_evidence_notes": (
                f"DOL ETA UI Weekly Claims news release, advance seasonally "
                f"adjusted figure for the week ending {week}, read from FRED "
                f"{fred_id} (advance vintage) as the cell's resolver names."
            ),
        },
        "aggregation": {"method": "level"},
        "filters": {},
        "source": {
            "source_name": "dol_eta",
            "source_table": "Unemployment Insurance Weekly Claims (advance)",
            "source_file": "fredgraph.csv",
            "url": source_url,
            "vintage": "advance",
            "extracted_at": dt.date.today().isoformat(),
            "extraction_method": (
                "Automated first-print capture via FRED series "
                f"{fred_id} by scripts/resolve_pending.py"
            ),
        },
        "source_row_keys": [week],
        "source_cell_keys": [fred_id],
    }


def pending_claims_refs(log: dict) -> list[tuple[str, str, str, str]]:
    """(ref, week, kind, verified release date) for pending claims cells."""
    forecasts = {
        entry["forecastSlug"]: entry
        for entry in log.get("entries", [])
        if entry.get("kind") == "prediction_recorded"
        and entry.get("forecastSlug")
        and entry.get("resolutionDate")
    }
    out = []
    for link in log["resolutionLinks"]:
        if link.get("status") != "pending":
            continue
        ref = link.get("targetFactRef")
        if not ref:
            continue
        forecast = forecasts.get(link.get("forecastSlug"))
        if not forecast:
            raise ValueError(
                f"pending target {ref} has no recorded, verified resolutionDate"
            )
        release_date = str(forecast["resolutionDate"])
        dt.date.fromisoformat(release_date)
        m = re.match(r"us\.dol\.initial_claims\.sa\.week_(\d{4}-\d{2}-\d{2})$", ref)
        if m:
            out.append((ref, m.group(1), "initial", release_date))
            continue
        m = re.match(
            r"dol\.eta\.continued_claims\.sa\.week_(\d{4}-\d{2}-\d{2})(\.first_print)?$",
            ref,
        )
        if m:
            out.append((ref, m.group(1), "continued", release_date))
    return out


def pending_adapter_refs(
    log: dict,
) -> list[tuple[str, str, dict[str, Any], str, str, str, dict[str, Any]]]:
    """(ref, kind, spec, period_type, period, release_date, forecast_entry)
    for pending cells covered by the generic adapters."""
    forecasts = {
        entry["forecastSlug"]: entry
        for entry in log.get("entries", [])
        if entry.get("kind") == "prediction_recorded" and entry.get("forecastSlug")
    }
    out = []
    for link in log["resolutionLinks"]:
        if link.get("status") != "pending":
            continue
        ref = link.get("targetFactRef")
        if not ref:
            continue
        forecast = forecasts.get(link.get("forecastSlug")) or {}
        release_date = str(forecast.get("resolutionDate") or "")
        if not release_date:
            continue
        intl_stem = next(
            (
                stem
                for stem in INTL_ADAPTERS
                if ref.startswith(stem + ".")
            ),
            None,
        )
        if intl_stem:
            parsed = parse_ref_period(ref, intl_stem)
            if parsed and parsed[0] == "month":
                out.append(
                    (
                        ref,
                        "intl",
                        INTL_ADAPTERS[intl_stem],
                        parsed[0],
                        parsed[1],
                        release_date,
                        forecast,
                    )
                )
            continue
        usaspending_stem = next(
            (
                stem
                for stem in USASPENDING_ADAPTERS
                if ref.startswith(stem + ".")
            ),
            None,
        )
        if usaspending_stem:
            parsed = parse_ref_period(ref, usaspending_stem)
            if parsed and parsed[0] == "fiscal_year":
                out.append(
                    (
                        ref,
                        "usaspending",
                        USASPENDING_ADAPTERS[usaspending_stem],
                        parsed[0],
                        parsed[1],
                        release_date,
                        forecast,
                    )
                )
            continue
        if ref.startswith(A19_STEM + "."):
            occupation = ref[len(A19_STEM) + 1 :].split(".")[0]
            parsed = parse_ref_period(ref, f"{A19_STEM}.{occupation}")
            if occupation in A19_ROW_LABELS and parsed:
                spec = {
                    "label": f"CPS employed, {A19_ROW_LABELS[occupation]}",
                    "unit": "thousands",
                    "source_name": "bls_cps",
                    "source_table": "Employment Situation, Table A-19",
                    "concept_authority": "bls",
                    "source_concept": A19_ROW_LABELS[occupation],
                    "a19_row": occupation,
                }
                out.append(
                    (ref, "a19", spec, parsed[0], parsed[1], release_date, forecast)
                )
            continue
        bls_stem = next(
            (
                stem
                for stem in BLS_API_ADAPTERS
                if ref.startswith(stem + ".")
            ),
            None,
        )
        if bls_stem:
            parsed = parse_ref_period(ref, bls_stem)
            if parsed:
                out.append(
                    (
                        ref,
                        "bls_api",
                        BLS_API_ADAPTERS[bls_stem],
                        parsed[0],
                        parsed[1],
                        release_date,
                        forecast,
                    )
                )
            continue
        cms_stem = next(
            (
                stem
                for stem in CMS_PROVIDER_DATA_ADAPTERS
                if ref.startswith(stem + ".")
            ),
            None,
        )
        if cms_stem:
            parsed = parse_ref_period(ref, cms_stem)
            if parsed and parsed[0] == "month":
                out.append(
                    (
                        ref,
                        "cms_provider_data",
                        CMS_PROVIDER_DATA_ADAPTERS[cms_stem],
                        parsed[0],
                        parsed[1],
                        release_date,
                        forecast,
                    )
                )
            continue
        for stem, spec in ALFRED_ADAPTERS.items():
            if not ref.startswith(stem + "."):
                continue
            parsed = parse_ref_period(ref, stem)
            if parsed:
                out.append(
                    (
                        ref,
                        "alfred",
                        spec,
                        parsed[0],
                        parsed[1],
                        release_date,
                        forecast,
                    )
                )
            break
    return out


def _created_at_utc(now: dt.datetime | None) -> str:
    current = now or dt.datetime.now(dt.timezone.utc)
    if (
        not isinstance(current, dt.datetime)
        or current.tzinfo is None
        or current.utcoffset() is None
    ):
        raise LedgerProposalError("now must be a timezone-aware datetime")
    try:
        current_utc = current.astimezone(dt.timezone.utc)
    except (OverflowError, ValueError) as exc:
        raise LedgerProposalError("now cannot be represented as UTC") from exc
    return current_utc.isoformat(timespec="seconds").replace("+00:00", "Z")


def _build_next_release_manifest(
    ledger: bytes,
    immutable_prefix: bytes,
    existing: ChainVerification,
    *,
    now: dt.datetime | None,
) -> tuple[dict[str, Any], bytes]:
    """Construct the exact next non-genesis manifest from a verified base."""

    head = existing.head
    if head is None:
        raise LedgerProposalError("cannot build a release before witnessed genesis")
    offsets = jsonl_line_offsets(ledger, LEDGER_RELATIVE.as_posix())
    line_count = len(offsets) - 1
    previous_count = head.manifest["state"]["lineCount"]
    if previous_count >= line_count:
        raise LedgerProposalError(
            "proposed ledger has no rows after the witnessed base HEAD"
        )
    witnessed_prefix = ledger[: offsets[previous_count]]
    if sha256_bytes(witnessed_prefix) != head.manifest["state"]["jsonlSha256"]:
        raise LedgerProposalError(
            "proposed ledger does not begin with the exact state committed by "
            "the witnessed base HEAD"
        )
    immutable_digest = sha256_bytes(immutable_prefix)
    if immutable_digest != head.manifest["state"]["immutablePrefixSha256"]:
        raise LedgerProposalError(
            "ledger/immutable_prefix.json differs from the witnessed base HEAD"
        )
    suffix = ledger[offsets[previous_count] :]
    manifest: dict[str, Any] = {
        "schemaVersion": SCHEMA_VERSION,
        "releaseIndex": head.release_index + 1,
        "previousManifestSha256": head.sha256,
        "state": {
            "path": LEDGER_RELATIVE.as_posix(),
            "jsonlSha256": sha256_bytes(ledger),
            "lineCount": line_count,
            "immutablePrefixSha256": immutable_digest,
        },
        "append": {
            "previousLineCount": previous_count,
            "appendedRowCount": line_count - previous_count,
            "appendedBytesSha256": sha256_bytes(suffix),
        },
        "createdAtUtc": _created_at_utc(now),
        "producer": {
            "repo": "PolicyEngine/ledger",
            "branch": "codex/thesis-ledger-facts",
        },
    }
    validate_manifest_schema(manifest)
    return manifest, canonical_bytes(manifest) + b"\n"


def _validated_repository_path(value: str) -> pathlib.PurePosixPath:
    if type(value) is not str or not value or value.startswith("/"):
        raise LedgerProposalError(f"invalid repository path: {value!r}")
    path = pathlib.PurePosixPath(value)
    if path.as_posix() != value or any(part in {"", ".", ".."} for part in path.parts):
        raise LedgerProposalError(f"invalid repository path: {value!r}")
    return path


def _materialize_repository_tree(
    root: pathlib.Path,
    tree: RepositoryTree,
) -> None:
    for relative, payload in tree.files.items():
        path = _validated_repository_path(relative)
        mode = tree.modes.get(relative)
        if mode not in {"100644", "100755"}:
            raise LedgerProposalError(
                f"base tree entry has non-regular mode {mode}: {relative}"
            )
        output = root / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(payload)
        output.chmod(0o755 if mode == "100755" else 0o644)


def _base_has_release_chain(tree: RepositoryTree) -> bool:
    prefix = MANIFEST_RELATIVE.as_posix() + "/"
    return any(relative.startswith(prefix) for relative in tree.files)


def _prepare_release_files(
    tree: RepositoryTree,
    *,
    path: str,
    candidate_ledger: bytes,
    added: int,
    requester: TimestampRequester,
    timeout_seconds: float,
    clock_skew_seconds: int,
    anchor_dir: pathlib.Path | None,
    now: dt.datetime | None,
    producer_signing_key: str | None,
) -> dict[str, bytes]:
    """Build and locally verify the release files before any visible push."""

    base_ledger = tree.files.get(path)
    if base_ledger is None:
        raise LedgerProposalError(f"base commit is missing ledger file {path}")
    base_offsets = jsonl_line_offsets(base_ledger, path)
    candidate_offsets = jsonl_line_offsets(candidate_ledger, path)
    if not candidate_ledger.startswith(base_ledger):
        raise LedgerProposalError(
            "proposed ledger is not an exact byte append to the base commit"
        )
    row_delta = len(candidate_offsets) - len(base_offsets)
    if row_delta <= 0:
        raise LedgerProposalError("proposed ledger does not append any rows")
    if type(added) is not int or added != row_delta:
        raise LedgerProposalError(
            f"proposal row delta is {row_delta}, but added={added!r}"
        )

    # Until the ledger's separately reviewed genesis lands, preserve the
    # existing legacy append path. In particular, the automated consumer must
    # not race that migration by inventing genesis itself.
    if not _base_has_release_chain(tree):
        return {}
    if path != LEDGER_RELATIVE.as_posix():
        raise LedgerProposalError(
            f"witnessed releases require ledger path {LEDGER_RELATIVE.as_posix()}"
        )
    prefix_path = PREFIX_RELATIVE.as_posix()
    immutable_prefix = tree.files.get(prefix_path)
    if immutable_prefix is None:
        raise LedgerProposalError(
            f"base commit is missing immutable-prefix file {prefix_path}"
        )

    timeout = _validate_timestamp_timeout(timeout_seconds)
    if type(clock_skew_seconds) is not int or clock_skew_seconds < 0:
        raise LedgerProposalError(
            "clock_skew_seconds must be a non-negative integer"
        )
    with tempfile.TemporaryDirectory(prefix="thesis-ledger-proposal-") as name:
        stage = pathlib.Path(name)
        _materialize_repository_tree(stage, tree)
        selected_anchors = anchor_dir or (stage / "releases" / "anchors")
        enforce_production_pins = anchor_dir is None

        # The base is verified strictly, with HEAD required to witness its
        # entire JSONL. Allowing a pending append here would permit a proposer
        # to advance an already-unwitnessed state.
        base_verification = verify_release_chain(
            stage,
            anchor_dir=selected_anchors,
            require_chain=True,
            verify_state=True,
            enforce_production_pins=enforce_production_pins,
            clock_skew_seconds=clock_skew_seconds,
        )
        manifest, manifest_raw = _build_next_release_manifest(
            candidate_ledger,
            immutable_prefix,
            base_verification,
            now=now,
        )
        filename = manifest_filename(manifest["releaseIndex"], manifest_raw)
        manifest_path = stage / MANIFEST_RELATIVE / filename
        if manifest_path.exists():
            raise LedgerProposalError(
                f"refusing to overwrite release manifest {manifest_path.name}"
            )
        producer_signature_path = producer_signature_path_for_manifest(manifest_path)
        producer_signature = _sign_release_manifest(
            manifest_raw,
            producer_signing_key,
            timeout,
        )
        # Verify against the public key materialized from the immutable base
        # tree (or the explicit test-only anchor override), never this checkout.
        verify_producer_signature_bytes(
            manifest_raw,
            producer_signature,
            anchor_dir=selected_anchors,
            enforce_production_pin=enforce_production_pins,
            label=producer_signature_path.name,
        )
        query = _build_timestamp_query(manifest_raw, timeout)
        receipts = _request_timestamp_receipts(
            query,
            requester=requester,
            timeout_seconds=timeout,
        )

        (stage / LEDGER_RELATIVE).write_bytes(candidate_ledger)
        manifest_path.write_bytes(manifest_raw)
        receipt_paths = receipt_paths_for_manifest(manifest_path)
        for tsa, token in receipts.items():
            receipt_paths[tsa].write_bytes(token)
        producer_signature_path.write_bytes(producer_signature)
        verify_release_chain(
            stage,
            anchor_dir=selected_anchors,
            require_chain=True,
            verify_state=True,
            enforce_production_pins=enforce_production_pins,
            clock_skew_seconds=clock_skew_seconds,
        )
        return {
            (stage_path.relative_to(stage).as_posix()): stage_path.read_bytes()
            for stage_path in (
                manifest_path,
                *receipt_paths.values(),
                producer_signature_path,
            )
        }


def ledger_state(repo: str, branch: str, path: str) -> tuple[str, str, str]:
    """Return (content, blob_sha, repository HEAD sha) for the ledger."""
    repo_sha = subprocess.run(
        ["gh", "api", f"repos/{repo}/commits/{branch}", "--jq", ".sha"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    raw = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{repo}/contents/{path}?ref={repo_sha}",
            "--jq",
            "{sha: .sha, content: .content}",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    payload = json.loads(raw)
    import base64

    return base64.b64decode(payload["content"]).decode(), payload["sha"], repo_sha


def _gh_api(*args: str, input_body: dict[str, Any] | None = None) -> str:
    # Without `--input -` gh ignores stdin and sends an empty request body
    # (GitHub answers 422 "nil is not an object"); the flag precedes the
    # endpoint so callers' path arguments stay the trailing tokens.
    body_flags = ["--input", "-"] if input_body is not None else []
    command = ["gh", "api", *body_flags, *args]
    completed = subprocess.run(
        command,
        input=json.dumps(input_body) if input_body is not None else None,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"gh api {' '.join(args)} failed: {completed.stderr.strip()[:500]}"
        )
    return completed.stdout


def _git_object_sha(value: Any, label: str) -> str:
    if type(value) is not str or re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise LedgerProposalError(f"GitHub returned an invalid {label}: {value!r}")
    return value


def _fetch_git_blob(repo: str, sha: str) -> bytes:
    sha = _git_object_sha(sha, "requested blob SHA")
    payload = json.loads(_gh_api(f"repos/{repo}/git/blobs/{sha}"))
    response_sha = _git_object_sha(payload.get("sha"), "returned blob SHA")
    if response_sha != sha:
        raise LedgerProposalError(
            f"GitHub returned blob {response_sha} for requested blob {sha}"
        )
    if payload.get("encoding") != "base64" or type(payload.get("content")) is not str:
        raise LedgerProposalError(f"GitHub blob {sha} is not base64 encoded")
    try:
        encoded = "".join(payload["content"].split())
        raw = base64.b64decode(encoded, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise LedgerProposalError(f"GitHub blob {sha} has invalid base64") from exc
    size = payload.get("size")
    if type(size) is not int or size != len(raw):
        raise LedgerProposalError(
            f"GitHub blob {sha} size mismatch: reported={size!r}, actual={len(raw)}"
        )
    header = f"blob {len(raw)}\0".encode("ascii")
    actual_sha = hashlib.sha1(
        header + raw,
        usedforsecurity=False,
    ).hexdigest()
    if actual_sha != sha:
        raise LedgerProposalError(
            f"GitHub blob bytes do not match tree object {sha}: {actual_sha}"
        )
    return raw


def _git_tree_object_sha(entries: list[dict[str, str]]) -> str:
    body = bytearray()
    for entry in entries:
        mode = entry["mode"].lstrip("0") or "0"
        body.extend(f"{mode} {entry['path']}\0".encode("utf-8"))
        body.extend(bytes.fromhex(entry["sha"]))
    header = f"tree {len(body)}\0".encode("ascii")
    return hashlib.sha1(header + body, usedforsecurity=False).hexdigest()


def _fetch_git_tree(
    repo: str,
    tree_sha: str,
    cache: dict[str, dict[str, dict[str, str]]],
) -> dict[str, dict[str, str]]:
    tree_sha = _git_object_sha(tree_sha, "requested tree SHA")
    if tree_sha in cache:
        return cache[tree_sha]
    payload = json.loads(_gh_api(f"repos/{repo}/git/trees/{tree_sha}"))
    if type(payload) is not dict:
        raise LedgerProposalError(f"GitHub tree {tree_sha} response is not an object")
    response_sha = _git_object_sha(payload.get("sha"), "returned tree SHA")
    if response_sha != tree_sha:
        raise LedgerProposalError(
            f"GitHub returned tree {response_sha} for requested tree {tree_sha}"
        )
    if payload.get("truncated") is not False:
        raise LedgerProposalError(
            f"GitHub returned a truncated tree for object {tree_sha}"
        )
    raw_entries = payload.get("tree")
    if type(raw_entries) is not list:
        raise LedgerProposalError(f"GitHub tree {tree_sha} has no entry list")
    entries: dict[str, dict[str, str]] = {}
    ordered: list[dict[str, str]] = []
    for raw_entry in raw_entries:
        if type(raw_entry) is not dict:
            raise LedgerProposalError(f"GitHub tree {tree_sha} has a malformed entry")
        path = raw_entry.get("path")
        mode = raw_entry.get("mode")
        object_type = raw_entry.get("type")
        if (
            type(path) is not str
            or not path
            or "/" in path
            or path in {".", ".."}
            or "\0" in path
            or type(mode) is not str
            or type(object_type) is not str
        ):
            raise LedgerProposalError(
                f"GitHub tree {tree_sha} has an unsafe direct entry"
            )
        valid_kind = (
            (object_type == "tree" and mode == "040000")
            or (object_type == "blob" and mode in {"100644", "100755", "120000"})
            or (object_type == "commit" and mode == "160000")
        )
        if not valid_kind:
            raise LedgerProposalError(
                f"GitHub tree {tree_sha} has invalid type/mode for {path}: "
                f"{object_type}/{mode}"
            )
        if path in entries:
            raise LedgerProposalError(
                f"GitHub tree {tree_sha} contains duplicate path {path!r}"
            )
        entry = {
            "path": path,
            "mode": mode,
            "type": object_type,
            "sha": _git_object_sha(raw_entry.get("sha"), f"object SHA for {path}"),
        }
        entries[path] = entry
        ordered.append(entry)
    computed_sha = _git_tree_object_sha(ordered)
    if computed_sha != tree_sha:
        raise LedgerProposalError(
            f"GitHub tree entries hash to {computed_sha}, expected {tree_sha}; "
            "refusing partial base state"
        )
    cache[tree_sha] = entries
    return entries


def _repository_blob_at_path(
    repo: str,
    root_entries: dict[str, dict[str, str]],
    path: str,
    cache: dict[str, dict[str, dict[str, str]]],
    *,
    required: bool,
) -> tuple[bytes, str, str] | None:
    relative = _validated_repository_path(path)
    entries = root_entries
    for component in relative.parts[:-1]:
        entry = entries.get(component)
        if entry is None:
            if required:
                raise LedgerProposalError(f"base commit is missing {path}")
            return None
        if entry["type"] != "tree" or entry["mode"] != "040000":
            raise LedgerProposalError(
                f"base path component is not a regular tree: {component}"
            )
        entries = _fetch_git_tree(repo, entry["sha"], cache)
    entry = entries.get(relative.name)
    if entry is None:
        if required:
            raise LedgerProposalError(f"base commit is missing {path}")
        return None
    if entry["type"] != "blob" or entry["mode"] not in {"100644", "100755"}:
        raise LedgerProposalError(f"base tree entry is not a regular file: {path}")
    return _fetch_git_blob(repo, entry["sha"]), entry["mode"], entry["sha"]


def _collect_release_tree_files(
    repo: str,
    tree_sha: str,
    prefix: pathlib.PurePosixPath,
    cache: dict[str, dict[str, dict[str, str]]],
    files: dict[str, bytes],
    modes: dict[str, str],
    blob_shas: dict[str, str],
) -> None:
    entries = _fetch_git_tree(repo, tree_sha, cache)
    for name, entry in entries.items():
        relative = prefix / name
        if entry["type"] == "tree":
            _collect_release_tree_files(
                repo,
                entry["sha"],
                relative,
                cache,
                files,
                modes,
                blob_shas,
            )
            continue
        if entry["type"] != "blob" or entry["mode"] not in {"100644", "100755"}:
            raise LedgerProposalError(
                f"base release entry is not a regular file: {relative}"
            )
        path = _validated_repository_path(relative.as_posix()).as_posix()
        files[path] = _fetch_git_blob(repo, entry["sha"])
        modes[path] = entry["mode"]
        blob_shas[path] = entry["sha"]


def _fetch_repository_tree(
    repo: str, commit_sha: str, ledger_path: str
) -> RepositoryTree:
    """Fetch the exact ledger/release subset from one immutable commit tree."""

    commit_sha = _git_object_sha(commit_sha, "commit SHA")
    commit = json.loads(_gh_api(f"repos/{repo}/git/commits/{commit_sha}"))
    if type(commit) is not dict:
        raise LedgerProposalError(
            f"GitHub commit {commit_sha} response is not an object"
        )
    response_sha = _git_object_sha(commit.get("sha"), "returned commit SHA")
    if response_sha != commit_sha:
        raise LedgerProposalError(
            f"GitHub returned commit {response_sha} for requested commit {commit_sha}"
        )
    tree_payload = commit.get("tree")
    if type(tree_payload) is not dict:
        raise LedgerProposalError(f"GitHub commit {commit_sha} has no tree")
    tree_sha = _git_object_sha(tree_payload.get("sha"), "tree SHA")
    cache: dict[str, dict[str, dict[str, str]]] = {}
    root_entries = _fetch_git_tree(repo, tree_sha, cache)
    files: dict[str, bytes] = {}
    modes: dict[str, str] = {}
    blob_shas: dict[str, str] = {}
    for wanted, required in (
        (ledger_path, True),
        (PREFIX_RELATIVE.as_posix(), False),
    ):
        blob = _repository_blob_at_path(
            repo, root_entries, wanted, cache, required=required
        )
        if blob is not None:
            payload, mode, blob_sha = blob
            files[wanted] = payload
            modes[wanted] = mode
            blob_shas[wanted] = blob_sha
    releases = root_entries.get("releases")
    if releases is not None:
        if releases["type"] != "tree" or releases["mode"] != "040000":
            raise LedgerProposalError("base releases path is not a regular tree")
        _collect_release_tree_files(
            repo,
            releases["sha"],
            pathlib.PurePosixPath("releases"),
            cache,
            files,
            modes,
            blob_shas,
        )
    return RepositoryTree(
        tree_sha=tree_sha,
        files=files,
        modes=modes,
        blob_shas=blob_shas,
    )


def _upload_git_blob(repo: str, payload: bytes) -> str:
    response = json.loads(
        _gh_api(
            "-X",
            "POST",
            f"repos/{repo}/git/blobs",
            input_body={
                "content": base64.b64encode(payload).decode("ascii"),
                "encoding": "base64",
            },
        )
    )
    return _git_object_sha(response.get("sha"), "created blob SHA")


def _publish_proposal_commit(
    repo: str,
    *,
    base_sha: str,
    base_tree_sha: str,
    message: str,
    changes: Mapping[str, bytes],
) -> str:
    """Create one unreferenced commit containing every proposal change."""

    if not changes:
        raise LedgerProposalError("proposal commit has no changes")
    tree_entries: list[dict[str, str]] = []
    for relative, payload in sorted(changes.items()):
        relative = _validated_repository_path(relative).as_posix()
        if type(payload) is not bytes:
            raise LedgerProposalError(f"proposal payload is not bytes: {relative}")
        tree_entries.append(
            {
                "path": relative,
                "mode": "100644",
                "type": "blob",
                "sha": _upload_git_blob(repo, payload),
            }
        )
    tree_response = json.loads(
        _gh_api(
            "-X",
            "POST",
            f"repos/{repo}/git/trees",
            input_body={"base_tree": base_tree_sha, "tree": tree_entries},
        )
    )
    candidate_tree_sha = _git_object_sha(
        tree_response.get("sha"), "created tree SHA"
    )
    commit_response = json.loads(
        _gh_api(
            "-X",
            "POST",
            f"repos/{repo}/git/commits",
            input_body={
                "message": message,
                "tree": candidate_tree_sha,
                "parents": [base_sha],
            },
        )
    )
    return _git_object_sha(commit_response.get("sha"), "proposal commit SHA")


def _branch_head(repo: str, branch: str) -> str:
    value = _gh_api(f"repos/{repo}/commits/{branch}", "--jq", ".sha").strip()
    return _git_object_sha(value, f"{branch} branch HEAD")


def _is_github_not_found(error: Exception) -> bool:
    diagnostic = str(error).lower()
    return "http 404" in diagnostic or "(404)" in diagnostic


def _proposal_ref_sha(repo: str, proposal: str) -> str | None:
    try:
        payload = json.loads(
            _gh_api(f"repos/{repo}/git/ref/heads/{proposal}")
        )
    except RuntimeError as exc:
        if _is_github_not_found(exc):
            return None
        raise
    target = payload.get("object")
    if type(target) is not dict:
        raise LedgerProposalError(f"proposal ref {proposal} has no target object")
    return _git_object_sha(target.get("sha"), f"target of proposal ref {proposal}")


def _find_open_proposal_pr(repo: str, proposal: str) -> int | None:
    owner, separator, _name = repo.partition("/")
    if not separator or not owner:
        raise LedgerProposalError(f"invalid GitHub repository name: {repo!r}")
    head = quote(f"{owner}:{proposal}", safe="")
    payload = json.loads(
        _gh_api(f"repos/{repo}/pulls?state=open&head={head}&per_page=10")
    )
    if type(payload) is not list:
        raise LedgerProposalError("GitHub open-PR recovery response is not a list")
    numbers = [entry.get("number") for entry in payload if type(entry) is dict]
    if any(type(number) is not int for number in numbers):
        raise LedgerProposalError("GitHub open-PR recovery returned an invalid number")
    if len(numbers) > 1:
        raise LedgerProposalError(
            f"multiple open PRs unexpectedly use proposal branch {proposal}"
        )
    return numbers[0] if numbers else None


def _proposal_pr_identity(
    repo: str,
    pr_number: int,
    *,
    expected_head_sha: str,
    expected_base: str,
    expected_base_sha: str | None = None,
) -> dict[str, Any]:
    payload = json.loads(_gh_api(f"repos/{repo}/pulls/{pr_number}"))
    if type(payload) is not dict:
        raise LedgerProposalError("GitHub pull-request response is not an object")
    head = payload.get("head")
    base = payload.get("base")
    matches = (
        type(head) is dict
        and head.get("sha") == expected_head_sha
        and type(base) is dict
        and base.get("ref") == expected_base
    )
    if expected_base_sha is not None:
        matches = matches and base.get("sha") == expected_base_sha
    if not matches:
        raise LedgerProposalError(
            "pull request no longer has the expected proposal head and base"
        )
    return payload


def _merged_proposal_sha(
    repo: str,
    pr_number: int,
    *,
    expected_head_sha: str,
    expected_base: str,
) -> str | None:
    """Recover a merge that may have succeeded despite a lost response."""

    payload = _proposal_pr_identity(
        repo,
        pr_number,
        expected_head_sha=expected_head_sha,
        expected_base=expected_base,
    )
    if payload.get("merged") is not True:
        return None
    return _git_object_sha(
        payload.get("merge_commit_sha"),
        f"merged commit SHA for pull request {pr_number}",
    )


def _cleanup_proposal(
    repo: str,
    proposal: str,
    *,
    ref_created: bool,
    ref_creation_attempted: bool,
    proposal_commit: str,
    pr_number: int | None,
    pr_creation_attempted: bool,
    merged: bool,
) -> list[str]:
    failures: list[str] = []
    if pr_number is None and pr_creation_attempted and not merged:
        try:
            pr_number = _find_open_proposal_pr(repo, proposal)
        except Exception as exc:
            failures.append(f"locate possibly-created PR: {exc}")
    if pr_number is not None and not merged:
        try:
            _gh_api(
                "-X",
                "PATCH",
                f"repos/{repo}/pulls/{pr_number}",
                input_body={"state": "closed"},
            )
        except Exception as exc:
            failures.append(f"close PR #{pr_number}: {exc}")
    should_delete_ref = ref_created
    if not ref_created and ref_creation_attempted:
        try:
            recovered_sha = _proposal_ref_sha(repo, proposal)
            if recovered_sha is not None and recovered_sha != proposal_commit:
                failures.append(
                    f"ref {proposal} points to unexpected commit {recovered_sha}; "
                    "refusing to delete it"
                )
            else:
                should_delete_ref = recovered_sha is not None
        except Exception as exc:
            failures.append(f"locate possibly-created branch {proposal}: {exc}")
    if should_delete_ref:
        try:
            _gh_api("-X", "DELETE", f"repos/{repo}/git/refs/heads/{proposal}")
        except Exception as exc:
            failures.append(f"delete branch {proposal}: {exc}")
    return failures


def _verify_remote_proposal_state(
    repo: str,
    commit_sha: str,
    *,
    path: str,
    candidate_ledger: bytes,
    release_files: Mapping[str, bytes],
    clock_skew_seconds: int,
    anchor_dir: pathlib.Path | None,
) -> None:
    """Re-fetch and fully verify the exact merged repository state."""

    tree = _fetch_repository_tree(repo, commit_sha, path)
    if tree.files.get(path) != candidate_ledger:
        raise LedgerProposalError(
            "merged commit ledger bytes do not equal the verified proposal"
        )
    for relative, expected in release_files.items():
        if tree.files.get(relative) != expected:
            raise LedgerProposalError(
                f"merged commit release bytes differ from proposal: {relative}"
            )
    with tempfile.TemporaryDirectory(prefix="thesis-ledger-merged-") as name:
        stage = pathlib.Path(name)
        _materialize_repository_tree(stage, tree)
        has_chain = _base_has_release_chain(tree)
        selected_anchors = anchor_dir or (stage / "releases" / "anchors")
        verification = verify_release_chain(
            stage,
            anchor_dir=selected_anchors,
            require_chain=has_chain,
            verify_state=True,
            enforce_production_pins=anchor_dir is None,
            clock_skew_seconds=clock_skew_seconds,
        )
        if release_files and verification.head is None:
            raise LedgerProposalError("merged release chain unexpectedly has no HEAD")


def append_gate_verdict(gate_runs: list[dict]) -> bool:
    """True when the append gate genuinely passed on a proposal head.

    The gate workflow fires on several events, so the same head carries one
    real "Append gate" run per delivering event plus skipped twins from the
    events whose job-level condition did not match. A skipped twin is not a
    verdict: the gate passed when at least one run concluded success and
    none concluded against the proposal.
    """
    conclusions = [run.get("conclusion") for run in gate_runs]
    if any(c not in ("success", "skipped", "neutral") for c in conclusions):
        return False
    return "success" in conclusions


def propose_ledger_append(
    repo: str,
    branch: str,
    path: str,
    content: str,
    blob_sha: str,
    base_sha: str,
    added: int,
    *,
    poll_seconds: int = 20,
    poll_attempts: int = 30,
    timestamp_requester: TimestampRequester | None = None,
    timestamp_timeout_seconds: float = DEFAULT_TIMESTAMP_TIMEOUT_SECONDS,
    clock_skew_seconds: int = DEFAULT_CLOCK_SKEW_SECONDS,
    release_anchor_dir: pathlib.Path | None = None,
    release_now: dt.datetime | None = None,
    producer_signing_key: str | None = None,
) -> str:
    """Publish one fully witnessed commit through the reviewed append gate."""

    environment_signing_key = os.environ.pop(PRODUCER_SIGNING_KEY_ENV, None)
    if producer_signing_key is None:
        producer_signing_key = environment_signing_key
    candidate_ledger = content.encode("utf-8")
    base_tree = _fetch_repository_tree(repo, base_sha, path)
    if base_tree.blob_shas.get(path) != blob_sha:
        raise LedgerProposalError(
            "base ledger blob differs from the state used to build the append"
        )
    release_files = _prepare_release_files(
        base_tree,
        path=path,
        candidate_ledger=candidate_ledger,
        added=added,
        requester=timestamp_requester or request_timestamp,
        timeout_seconds=timestamp_timeout_seconds,
        clock_skew_seconds=clock_skew_seconds,
        anchor_dir=release_anchor_dir,
        now=release_now,
        producer_signing_key=producer_signing_key,
    )
    message = f"Record {added} first-print observation(s) via resolve_pending.py"
    changes = {path: candidate_ledger, **release_files}
    proposal_commit = _publish_proposal_commit(
        repo,
        base_sha=base_sha,
        base_tree_sha=base_tree.tree_sha,
        message=message,
        changes=changes,
    )
    current_base = _branch_head(repo, branch)
    if current_base != base_sha:
        raise LedgerProposalError(
            f"ledger branch moved while proposal was prepared: {base_sha} -> "
            f"{current_base}; retry against the new trusted state"
        )

    stamp = utc_now().lower().replace(":", "-").replace("t", "-")
    proposal = f"thesis-facts-append/{stamp}-{time.time_ns():x}"
    ref_created = False
    ref_creation_attempted = False
    pr_number: int | None = None
    pr_creation_attempted = False
    merged = False
    try:
        ref_creation_attempted = True
        _gh_api(
            "-X",
            "POST",
            f"repos/{repo}/git/refs",
            input_body={
                "ref": f"refs/heads/{proposal}",
                "sha": proposal_commit,
            },
        )
        ref_created = True
        pr_creation_attempted = True
        pr = json.loads(
            _gh_api(
                "-X",
                "POST",
                f"repos/{repo}/pulls",
                input_body={
                    "title": message,
                    "head": proposal,
                    "base": branch,
                    "body": (
                        "Automated witnessed append proposal from "
                        f"resolve_pending.py: {added} first-print observation(s) "
                        f"built against {base_sha}. The proposal commit contains "
                        "the ledger append and its complete four-sibling release, "
                        "and "
                        "merges only after the thesis-facts append gate passes."
                    ),
                },
            )
        )
        if type(pr.get("number")) is not int:
            raise LedgerProposalError("GitHub did not return a pull-request number")
        pr_number = pr["number"]

        gate_passed = False
        for _ in range(poll_attempts):
            runs = json.loads(
                _gh_api(f"repos/{repo}/commits/{proposal_commit}/check-runs")
            ).get("check_runs", [])
            gate_runs = [run for run in runs if run.get("name") == "Append gate"]
            if gate_runs and all(
                run.get("status") == "completed" for run in gate_runs
            ):
                gate_passed = append_gate_verdict(gate_runs)
                break
            time.sleep(poll_seconds)
        if not gate_passed:
            raise LedgerProposalError(
                f"append gate did not pass for {repo}#{pr_number}; refusing to "
                "leave a failed proposal branch or PR"
            )

        current_base = _branch_head(repo, branch)
        if current_base != base_sha:
            raise LedgerProposalError(
                f"ledger branch moved while proposal awaited the append gate: "
                f"{base_sha} -> {current_base}; refusing to rebase a release "
                "built against stale state"
            )

        pr_state = _proposal_pr_identity(
            repo,
            pr_number,
            expected_head_sha=proposal_commit,
            expected_base=branch,
            expected_base_sha=base_sha,
        )
        if pr_state.get("merged") is True:
            raise LedgerProposalError(
                f"pull request {repo}#{pr_number} merged before the controlled merge"
            )

        ambiguous_merge_error: BaseException | None = None
        merge_response: Any = None
        try:
            merge_raw = _gh_api(
                "-X",
                "PUT",
                f"repos/{repo}/pulls/{pr_number}/merge",
                input_body={
                    "merge_method": "rebase",
                    "sha": proposal_commit,
                },
            )
        except RuntimeError as exc:
            ambiguous_merge_error = exc
        else:
            try:
                merge_response = json.loads(merge_raw)
            except json.JSONDecodeError as exc:
                ambiguous_merge_error = exc
            if type(merge_response) is not dict:
                ambiguous_merge_error = LedgerProposalError(
                    "GitHub merge response is not an object"
                )

        if ambiguous_merge_error is not None:
            recovered_sha = _merged_proposal_sha(
                repo,
                pr_number,
                expected_head_sha=proposal_commit,
                expected_base=branch,
            )
            if recovered_sha is None:
                raise ambiguous_merge_error
            merged_sha = recovered_sha
        else:
            assert isinstance(merge_response, dict)
            if merge_response.get("merged") is not True:
                raise LedgerProposalError(
                    f"GitHub did not merge {repo}#{pr_number}: "
                    f"{merge_response.get('message', 'no diagnostic')}"
                )
            response_merged_sha = _git_object_sha(
                merge_response.get("sha"), "merged commit SHA"
            )
            confirmed_sha = _merged_proposal_sha(
                repo,
                pr_number,
                expected_head_sha=proposal_commit,
                expected_base=branch,
            )
            if confirmed_sha is None:
                raise LedgerProposalError(
                    "GitHub merge response was not confirmed by pull-request state"
                )
            if confirmed_sha != response_merged_sha:
                raise LedgerProposalError(
                    "GitHub merge response SHA disagrees with pull-request state: "
                    f"{response_merged_sha} != {confirmed_sha}"
                )
            merged_sha = confirmed_sha
        merged = True
        _verify_remote_proposal_state(
            repo,
            merged_sha,
            path=path,
            candidate_ledger=candidate_ledger,
            release_files=release_files,
            clock_skew_seconds=clock_skew_seconds,
            anchor_dir=release_anchor_dir,
        )
        _gh_api("-X", "DELETE", f"repos/{repo}/git/refs/heads/{proposal}")
        ref_created = False
        return merged_sha
    except BaseException as exc:
        cleanup_failures = _cleanup_proposal(
            repo,
            proposal,
            ref_created=ref_created,
            ref_creation_attempted=ref_creation_attempted,
            proposal_commit=proposal_commit,
            pr_number=pr_number,
            pr_creation_attempted=pr_creation_attempted,
            merged=merged,
        )
        if cleanup_failures:
            raise LedgerProposalError(
                f"proposal failed ({exc}); cleanup also failed: "
                + "; ".join(cleanup_failures)
            ) from exc
        raise


def registration_contracts(
    records_dir: pathlib.Path | None = None,
) -> dict[str, dict[str, Any]]:
    """Map preregistered dataPointIds to their verified contracts.

    Snapshot content hashes deliberately exclude the operational
    ``registeredAtUtc`` (v2+), so verification must use the schema-aware
    ``registration_content_hash``, never a whole-file canonical hash.
    """
    records_dir = records_dir or ROOT / "records" / "targets"
    contracts: dict[str, dict[str, Any]] = {}
    unresolved_published: set[str] = set()
    if not records_dir.exists():
        return contracts
    for path in sorted(records_dir.glob("*.json")):
        match = re.fullmatch(r"\d{4}-\d{2}-\d{2}-([0-9a-f]{64})\.json", path.name)
        if not match:
            continue
        try:
            snapshot = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        try:
            content_hash = registration_content_hash(snapshot)
        except RegistrationError as exc:
            raise ValueError(f"invalid target registration {path}: {exc}") from exc
        if content_hash != match.group(1):
            raise ValueError(f"target registration hash mismatch: {path}")
        for target in snapshot.get("targets", []):
            data_point_id = target.get("dataPointId")
            if not data_point_id:
                continue
            key = str(data_point_id)
            entry = {
                "targetContentHash": content_hash,
                "contract": target,
                "ledgerPin": snapshot.get("ledgerPin"),
            }
            existing = contracts.get(key)
            if existing is None:
                contracts[key] = entry
                continue
            # A dataPointId can be registered in more than one snapshot (a
            # per-target snapshot plus a later batch set). Lexicographic file
            # order used to silently pick whichever sorted last, so an
            # appended fact could carry a valid-but-wrong contract hash and
            # then be excluded by the site's target-hash check (finding 9).
            # Resolve to whichever registration the PUBLISHED target actually
            # committed; identical duplicates are fine; a conflict the
            # published set does not disambiguate fails closed.
            if existing["targetContentHash"] == content_hash and (
                canonical_bytes(existing["contract"]) == canonical_bytes(target)
            ):
                continue
            published = published_target_hashes().get(key)
            if published is None:
                # An unpublished (prospect/registered-not-yet-scored)
                # dataPointId is never looked up during resolution — the
                # resolver only appends to published pending cells — so a
                # duplicate here cannot mis-score. Pick deterministically by
                # the freshest registration rather than lexical file order.
                if _registered_at(target) >= _registered_at(existing["contract"]):
                    contracts[key] = entry
                continue
            # For a PUBLISHED target the fact must carry the exact hash its
            # cell committed, or the site excludes the score. Resolve to the
            # published registration; a conflict the published set does not
            # contain fails closed (finding 9).
            if content_hash == published:
                contracts[key] = entry
                unresolved_published.discard(key)
            elif existing["targetContentHash"] != published:
                # Neither candidate seen so far matches the published hash.
                # Supersede history retains every snapshot for a dataPointId,
                # and file order is date-lexicographic, so the matching
                # snapshot may simply not have been scanned yet. Defer the
                # fail-closed decision to the end of the scan.
                unresolved_published.add(key)
    for key in sorted(unresolved_published):
        published = published_target_hashes().get(key)
        if contracts[key]["targetContentHash"] != published:
            raise ValueError(
                f"neither registration for published dataPointId {key} "
                f"matches its target hash {(published or '')[:16]}…; resolve "
                "the duplicate before appending"
            )
    return contracts


def _registered_at(contract: dict[str, Any]) -> str:
    return str(contract.get("registeredAtUtc") or contract.get("registeredAt") or "")


_PUBLISHED_TARGET_HASHES: dict[str, str] | None = None


def published_target_hashes(
    generated_path: pathlib.Path | None = None,
) -> dict[str, str]:
    """Map each published dataPointId to the target hash its cell committed.

    The generated target module is what the site actually scores against, so
    it is the authority for which registration a duplicate dataPointId
    resolves to.
    """
    global _PUBLISHED_TARGET_HASHES
    if _PUBLISHED_TARGET_HASHES is not None and generated_path is None:
        return _PUBLISHED_TARGET_HASHES
    path = generated_path or (
        ROOT / "site" / "src" / "data" / "ledger-targets.generated.ts"
    )
    mapping: dict[str, str] = {}
    if path.exists():
        # Each entry names its dataPointId before its targetContentHash; only
        # preregistered v2/v3 targets carry a hash (the hardcoded legacy
        # targets do not), so map each hash to the nearest preceding id.
        current: str | None = None
        for line in path.read_text().splitlines():
            dpid = re.search(r'dataPointId:\s*"([^"]+)"', line)
            if dpid:
                current = dpid.group(1)
                continue
            thash = re.search(r'targetContentHash:\s*"([0-9a-f]{64})"', line)
            if thash and current is not None:
                mapping[current] = thash.group(1)
    if generated_path is None:
        _PUBLISHED_TARGET_HASHES = mapping
    return mapping


ASSERTION_CONTENT_KEYS = (
    "source_record_id",
    "value",
    "observed_at",
    "period",
    "geography",
    "entity",
    "aggregation",
    "filters",
    "domain",
)


def assertion_version_projection(row: dict[str, Any]) -> dict[str, Any]:
    """The canonical projection that content-addresses an assertion (av2).

    Committed to everything that changes what the assertion MEANS —
    identity, value, timing, population, the FULL measure (concept mapping
    and authority, not just concept/unit), exact publisher provenance
    including source file and byte digest, source row/cell lineage, and the
    archived response digest. Two assertions that differ in any of these
    get different IDs; a correction must supersede explicitly (finding 3).
    Kept byte-identical with the ledger append gate's recomputation.
    """
    measure = row.get("measure") or {}
    source = row.get("source") or {}
    projection = {key: row.get(key) for key in ASSERTION_CONTENT_KEYS}
    projection["measure"] = {
        "concept": measure.get("concept"),
        "unit": measure.get("unit"),
        "source_concept": measure.get("source_concept"),
        "concept_relation": measure.get("concept_relation"),
        "concept_authority": measure.get("concept_authority"),
        "legal_vintage": measure.get("legal_vintage"),
    }
    projection["source"] = {
        "source_name": source.get("source_name"),
        "source_table": source.get("source_table"),
        "source_file": source.get("source_file"),
        "url": source.get("url"),
        "vintage": source.get("vintage"),
        "source_sha256": source.get("source_sha256"),
    }
    projection["lineage"] = {
        "source_row_keys": row.get("source_row_keys"),
        "source_cell_keys": row.get("source_cell_keys"),
    }
    projection["responseArchiveSha256"] = (row.get("responseArchive") or {}).get(
        "sha256"
    )
    return projection


def assertion_version(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"av2:{canonical_sha256(assertion_version_projection(row))}",
        "supersedes": None,
    }


def source_binding_projection(
    registration: dict[str, Any], row: dict[str, Any], raw: bytes
) -> dict[str, Any]:
    """Bind the appended fact to the registered resolver contract.

    The projection is derived from the ROW's own content, then each derived
    field is checked against the registration; a mismatch fails the append.
    Copying the registration's fields wholesale would make the site's
    contract check tautological — a row from a different publisher, period,
    or concept would still "match". Deriving from the row and rejecting on
    mismatch is what actually binds the appended fact to its target
    (finding 1). The archived-response digest binds the bytes; a trusted
    parse proof that the value came FROM those bytes is the resolver's job
    (it built both row and archive from the same fetch) and remains the
    step-5 hardening for an untrusted writer.
    """
    contract = registration["contract"]
    binding = contract.get("sourceBinding") or {}
    measure = row.get("measure") or {}
    row_source = row.get("source") or {}
    record_id = row.get("source_record_id")

    row_unit = measure.get("unit")
    row_concept = measure.get("concept")
    # Direct field equalities that need no fragile period re-tokenization: a
    # row from a different publisher carries a different measure concept, and
    # the registration lookup already keyed on the row's source_record_id, so
    # the period is pinned by identity. unit + concept + publisher host close
    # the "unrelated row scores as contract_bound" hole (finding 1).
    if row_unit != contract.get("unit"):
        raise ValueError(
            f"fact unit {row_unit!r} does not match registered unit "
            f"{contract.get('unit')!r} for {record_id}"
        )
    registered_series = contract.get("series")
    if registered_series is not None and row_concept != registered_series:
        raise ValueError(
            f"fact measure concept {row_concept!r} does not match the "
            f"registered series {registered_series!r} for {record_id}"
        )
    allowed_hosts = binding.get("allowedHosts")
    row_url = row_source.get("url") or measure.get("concept_evidence_url")
    if allowed_hosts and row_url:
        host = urlparse(str(row_url)).hostname
        if host not in allowed_hosts:
            raise ValueError(
                f"fact source host {host!r} is not in the registered "
                f"allowedHosts {allowed_hosts} for {record_id}"
            )
    return {
        "series": registered_series,
        "concept": row_concept,
        "period": contract.get("period"),
        "releasePolicy": binding.get("releasePolicy"),
        "table": binding.get("table"),
        "field": binding.get("field"),
        "transform": binding.get("transform"),
        "unit": row_unit,
        "sourceUrl": str(row_url) if row_url else None,
        "responseSha256": hashlib.sha256(raw).hexdigest(),
    }


def archive_response(
    run_dir: pathlib.Path,
    *,
    series_id: str,
    vintage: str,
    raw: bytes,
    extension: str = "csv",
) -> dict[str, Any]:
    """Write one deterministic gzip archive and return its hash reference."""
    raw_sha256 = hashlib.sha256(raw).hexdigest()
    compressed = gzip.compress(raw, mtime=0)
    gzip_sha256 = hashlib.sha256(compressed).hexdigest()
    name = f"{series_id.lower()}-{vintage}-{raw_sha256[:16]}.{extension}.gz"
    path = run_dir / "responses" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(compressed)
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": raw_sha256,
        "bytes": len(raw),
        "gzipSha256": gzip_sha256,
        "gzipBytes": len(compressed),
        "contentEncoding": "gzip",
    }


def attach_resolution_provenance(
    row: dict[str, Any],
    *,
    run_dir: pathlib.Path,
    series_id: str,
    vintage: str,
    raw: bytes,
    retrieved_at: str,
    ledger_repo_sha: str,
    target_contracts: dict[str, dict[str, Any]],
    extension: str = "csv",
) -> dict[str, Any]:
    # Archive first so the assertion version can bind the response digest;
    # computing it before archiving would leave the bytes out of identity.
    response_archive = archive_response(
        run_dir,
        series_id=series_id,
        vintage=vintage,
        raw=raw,
        extension=extension,
    )
    output = {
        **row,
        "ledgerRepoSha": ledger_repo_sha,
        "sourceVintage": vintage,
        "retrievedAt": retrieved_at,
        "responseArchive": response_archive,
    }
    output["assertionVersion"] = assertion_version(output)
    registration = target_contracts.get(str(row["source_record_id"]))
    if registration:
        output["targetContentHash"] = registration["targetContentHash"]
        output["sourceBindingProjection"] = source_binding_projection(
            registration, row, raw
        )
    return output


def resolution_run_dir(retrieved_at: str) -> pathlib.Path:
    stamp = retrieved_at.lower().replace(":", "-")
    return (
        ROOT
        / "records"
        / "resolutions"
        / retrieved_at[:10]
        / f"{stamp}-resolve-pending"
    )


def finalize_resolution_manifest(
    run_dir: pathlib.Path, manifest: dict[str, Any]
) -> dict[str, Any]:
    """Seal the exact resolver-response inventory and verify it immediately."""

    created_at = str(manifest["retrievedAt"])
    repository = ROOT.resolve()
    refs: list[dict[str, Any]] = []
    rooted: list[dict[str, Any]] = []
    seen_paths: set[str] = set()
    for fact in manifest["facts"]:
        archive = fact["responseArchive"]
        path = repository / archive["path"]
        relative = path.resolve().relative_to(run_dir.resolve()).as_posix()
        ref = {
            "artifactType": "resolver_response",
            "path": path.resolve().relative_to(repository).as_posix(),
            "sha256": archive["gzipSha256"],
            "bytes": archive["gzipBytes"],
            "createdAt": created_at,
        }
        # Several facts can legitimately share one archived response (two
        # dataPointId dialects of the same series resolve from the same
        # vintage bytes); the inventory lists each archive exactly once.
        if ref["path"] in seen_paths:
            continue
        seen_paths.add(ref["path"])
        refs.append(ref)
        rooted.append({**ref, "path": relative})
    manifest.update(
        {
            "custodyInventoryVersion": 2,
            "runMode": "resolver",
            "ok": True,
            "manifestHashSemantics": (
                "canonical-json-v1; exclude artifacts where "
                "artifactType=manifest and exclude custodyRootSha256"
            ),
            "artifacts": refs,
        }
    )
    self_payload = copy.deepcopy(manifest)
    self_payload.pop("custodyRootSha256", None)
    self_bytes = canonical_bytes(self_payload)
    manifest_ref = {
        "artifactType": "manifest",
        "path": (run_dir / "manifest.json")
        .resolve()
        .relative_to(repository)
        .as_posix(),
        "sha256": hashlib.sha256(self_bytes).hexdigest(),
        "bytes": len(self_bytes),
        "createdAt": created_at,
        "hashMode": manifest["manifestHashSemantics"],
    }
    manifest["artifacts"] = [*refs, manifest_ref]
    custody = {
        "schemaVersion": "thesis_custody_root_v1",
        "custodyInventoryVersion": 2,
        "runMode": "resolver",
        "hashAlgorithm": "sha256",
        "canonicalJson": (
            "UTF-16 code-unit key order; ECMAScript JSON number/string encoding"
        ),
        "artifacts": rooted,
        "manifestWithoutCustodyRoot": {
            "path": "manifest.json",
            "excludedField": "custodyRootSha256",
            "canonicalJsonSha256": canonical_sha256(manifest),
        },
    }
    (run_dir / "custody_root.json").write_text(json.dumps(custody, indent=2) + "\n")
    manifest["custodyRootSha256"] = canonical_sha256(custody)
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    verify_run(run_dir)
    return manifest


def main() -> int:
    # Remove the secret before any network client or subprocess can inherit it.
    # The value remains only as an in-memory string until proposal signing.
    producer_signing_key = os.environ.pop(PRODUCER_SIGNING_KEY_ENV, None)
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--ledger-repo", default="PolicyEngine/ledger")
    parser.add_argument("--ledger-branch", default="codex/thesis-ledger-facts")
    parser.add_argument("--ledger-path", default="ledger/official_observations.jsonl")
    args = parser.parse_args()

    log = load_thesis_log(LOG_URL)
    todo = pending_claims_refs(log)
    adapter_todo = pending_adapter_refs(log)
    if not todo and not adapter_todo:
        print("no pending adapter-covered cells")
        return 0

    content, sha, ledger_repo_sha = ledger_state(
        args.ledger_repo, args.ledger_branch, args.ledger_path
    )
    existing_ids = {
        json.loads(line)["source_record_id"]
        for line in content.splitlines()
        if line.strip()
    }

    fetched_rows: list[tuple[dict[str, Any], str, str, bytes, str, str]] = []
    today = dt.date.today()
    for ref, week, kind, source_vintage in todo:
        if ref in existing_ids:
            print(f"  already recorded: {ref}")
            continue
        release_day = dt.date.fromisoformat(source_vintage)
        if release_day > today:
            print(f"  release {release_day} not reached: {ref}")
            continue
        series_id = "ICSA" if kind == "initial" else "CCSA"
        value, raw, _source_url, retrieved_at = fred_advance_value(
            series_id, week, release_day.isoformat()
        )
        if value is None or raw is None:
            print(f"  not yet published: {ref}")
            continue
        row = claims_fact(ref, week, value, kind, release_day)
        fetched_rows.append(
            (row, series_id, release_day.isoformat(), raw, retrieved_at, "csv")
        )
        print(f"  resolve {ref} -> {row['value']} {row['measure']['unit']}")

    # Generic adapters: ALFRED vintage series, BLS API series, A-19
    # snapshot rows, and the international native-source adapters. FRED
    # fetches are cached per (series, vintage); BLS fetches per (series,
    # year range); A-19 snapshots per month; international artifacts per
    # source key so dataPointId dialects share one archived response.
    alfred_cache: dict[tuple[str, str], tuple[dict, bytes | None, str, str]] = {}
    usaspending_cache: dict[str, tuple[Any, bytes | None, str, str]] = {}
    usaspending_contracts: dict[str, dict[str, Any]] | None = None
    bls_cache: dict[
        tuple[str, int, int], tuple[dict, bytes | None, str, str]
    ] = {}
    a19_cache: dict[str, tuple[dict[str, float], bytes | None, str, str]] = {}
    intl_cache: dict[Any, tuple] = {}
    # CMS provider-data: one metastore read per dataset item and one CSV
    # download per distribution URL, shared across cells on the same file.
    cms_metastore_cache: dict[str, tuple[str, str, str] | None] = {}
    cms_csv_cache: dict[str, bytes | None] = {}
    for ref, kind, spec, period_type, period, source_vintage, forecast in (
        adapter_todo
    ):
        if ref in existing_ids:
            print(f"  already recorded: {ref}")
            continue
        release_day = dt.date.fromisoformat(source_vintage)
        if release_day > today:
            print(f"  release {release_day} not reached: {ref}")
            continue
        unit = (forecast or {}).get("unit")
        if unit and unit != spec["unit"]:
            print(
                f"  UNIT MISMATCH (refusing): {ref} cell={unit!r} "
                f"adapter={spec['unit']!r}"
            )
            continue
        if kind == "intl":
            hold_reason = INTL_RESOLUTION_HOLDS.get(ref)
            if hold_reason:
                print(f"  ON HOLD (not resolving): {ref} — {hold_reason}")
                continue
            window = spec.get("first_print_window_days")
            if window is not None and today > release_day + dt.timedelta(
                days=window
            ):
                print(
                    f"  FIRST-PRINT WINDOW ELAPSED (deferring, needs a "
                    f"pinned vintage): {ref} released {release_day}, "
                    f"window {window}d"
                )
                continue
            try:
                series, flags, raw, source_url, retrieved_at = intl_fetch(
                    spec, period, intl_cache
                )
            except LookupError as exc:
                print(f"  {exc}: {ref}")
                continue
            except Exception as exc:  # noqa: BLE001 - defer, don't crash run
                print(f"  fetch/parse failed (deferring): {ref} — {exc}")
                continue
            anchor_failures = intl_anchor_failures(spec, series)
            if anchor_failures:
                print(
                    f"  ANCHOR MISMATCH (refusing, wrong series/vintage?): "
                    f"{ref} — {'; '.join(anchor_failures)}"
                )
                continue
            if flash_vintage_missing(spec, flags, period):
                print(
                    f"  FLASH VINTAGE NO LONGER SERVED (deferring): {ref} — "
                    f"{period} carries no provisional flag, finals likely "
                    f"published"
                )
                continue
            value = intl_transformed_value(spec, series, period)
            series_id = spec["series_id"]
            source_file = spec["source_file"]
            extension = spec["extension"]
        elif kind == "alfred":
            cache_key = (spec["fred"], release_day.isoformat())
            if cache_key not in alfred_cache:
                alfred_cache[cache_key] = fred_vintage_series(*cache_key)
            rows, raw, source_url, retrieved_at = alfred_cache[cache_key]
            value = apply_transform(rows, spec, period_type, period)
            series_id = spec["fred"]
            source_file = "alfredgraph.csv"
            extension = "csv"
        elif kind == "bls_api":
            series_id = spec["series_id"]
            bls_key = (series_id, spec["anchor_start_year"], int(period[:4]))
            if bls_key not in bls_cache:
                bls_cache[bls_key] = bls_series_rows(*bls_key)
            rows, raw, source_url, retrieved_at = bls_cache[bls_key]
            if raw is None:
                print(f"  BLS API fetch failed: {ref}")
                continue
            mismatches = bls_anchor_mismatches(rows, spec["anchors"])
            if mismatches:
                print(
                    f"  ANCHOR MISMATCH (refusing, wrong series?): {ref} "
                    + "; ".join(mismatches)
                )
                continue
            value, refusal = bls_first_print(rows, period)
            if refusal:
                print(f"  FIRST-PRINT WINDOW MISSED (refusing): {ref} — {refusal}")
                continue
            # The API has no vintage archive, so the capture day IS the
            # source vintage; the latest+preliminary gate above bounds it
            # inside the first-print window.
            release_day = dt.date.fromisoformat(retrieved_at[:10])
            source_file = "timeseries/data (BLS Public Data API v2)"
            extension = "json"
        elif kind == "cms_provider_data":
            metastore_key = spec["metastore_url"]
            if metastore_key not in cms_metastore_cache:
                try:
                    cms_metastore_cache[metastore_key] = (
                        cms_provider_data_metastore(spec)
                    )
                except Exception as exc:  # noqa: BLE001 - defer, don't crash
                    print(f"  CMS metastore fetch failed (deferring): {ref} — {exc}")
                    cms_metastore_cache[metastore_key] = None
            metastore = cms_metastore_cache[metastore_key]
            if metastore is None:
                continue
            modified, download_url, retrieved_at = metastore
            gate = cms_provider_data_gate(period, modified)
            if gate:
                if gate.startswith("missed"):
                    print(f"  FIRST-PRINT WINDOW MISSED (refusing): {ref} — {gate}")
                else:
                    print(f"  refresh not posted yet (deferring): {ref} — {gate}")
                continue
            if download_url not in cms_csv_cache:
                request = urllib.request.Request(
                    download_url, headers={"User-Agent": INTL_USER_AGENT}
                )
                try:
                    with urllib.request.urlopen(request, timeout=300) as r:
                        cms_csv_cache[download_url] = r.read()
                except Exception as exc:  # noqa: BLE001 - defer, don't crash
                    print(f"  CMS CSV fetch failed (deferring): {ref} — {exc}")
                    cms_csv_cache[download_url] = None
            raw = cms_csv_cache[download_url]
            if raw is None:
                continue
            value, refusal = cms_provider_data_value(raw, spec, modified)
            if refusal:
                print(f"  CMS PARSE REFUSAL (refusing): {ref} — {refusal}")
                continue
            # The live file IS the refresh's first print while the gate
            # holds; the capture day is the source vintage.
            release_day = dt.date.fromisoformat(retrieved_at[:10])
            source_url = download_url
            series_id = spec.get("state_row", "ALL_FACILITIES")
            source_file = download_url.rsplit("/", 1)[-1]
            extension = "csv"
        elif kind == "usaspending":
            if usaspending_contracts is None:
                usaspending_contracts = registration_contracts()
            contract = usaspending_contracts.get(ref)
            binding = (contract or {}).get("sourceBinding") or {}
            window_state = snapshot_window_state(
                dt.date.fromisoformat(utc_now()[:10]),
                binding.get("expectedReleaseWindow"),
            )
            if contract is None or window_state == "invalid":
                print(f"  NO REGISTERED SNAPSHOT WINDOW (refusing): {ref}")
                continue
            if window_state == "pending":
                print(
                    f"  SNAPSHOT WINDOW NOT OPEN (deferring): {ref} — opens "
                    f"{binding['expectedReleaseWindow']['start']}"
                )
                continue
            if window_state == "missed":
                print(
                    f"  SNAPSHOT WINDOW MISSED (refusing): {ref} — closed "
                    f"{binding['expectedReleaseWindow']['end']}"
                )
                continue
            if (
                binding.get("sourceUrl") != spec["url_template"]
                or binding.get("field") != spec["field"]
            ):
                print(
                    f"  BINDING/ADAPTER MISMATCH (refusing, registry drift?): "
                    f"{ref}"
                )
                continue
            snapshot_url = spec["url_template"].format(fiscal_year=period)
            allowed = binding.get("allowedHosts") or []
            host = urllib.parse.urlparse(snapshot_url).hostname
            if host not in allowed:
                print(
                    f"  HOST NOT IN REGISTERED ALLOWLIST (refusing): {ref} — "
                    f"{host}"
                )
                continue
            if snapshot_url not in usaspending_cache:
                retrieved_at = utc_now()
                request = urllib.request.Request(
                    snapshot_url,
                    headers={
                        "User-Agent": "thesis-resolver/1 "
                        "(app.thesisinstitute.org)"
                    },
                )
                try:
                    with urllib.request.urlopen(request, timeout=120) as r:
                        raw_body = r.read()
                    usaspending_cache[snapshot_url] = (
                        json.loads(raw_body.decode()),
                        raw_body,
                        snapshot_url,
                        retrieved_at,
                    )
                except (
                    urllib.error.URLError,
                    json.JSONDecodeError,
                    UnicodeDecodeError,
                ) as exc:
                    print(f"  USAspending fetch failed ({exc}): {ref}")
                    usaspending_cache[snapshot_url] = (
                        None,
                        None,
                        snapshot_url,
                        retrieved_at,
                    )
            payload, raw, source_url, retrieved_at = usaspending_cache[
                snapshot_url
            ]
            if raw is None:
                continue
            raw_value = extract_json_field(payload, spec["field"])
            if raw_value is None:
                print(
                    f"  FIELD NOT FOUND IN RESPONSE (refusing): {ref} — "
                    f"{spec['field']}"
                )
                continue
            value = round(raw_value * spec.get("scale", 1), spec.get("round", 4))
            # The registered capture day IS the outcome's vintage: the
            # window gate above bounds it inside the preregistered
            # snapshot window.
            release_day = dt.date.fromisoformat(retrieved_at[:10])
            series_id = spec["series_id"]
            source_file = (
                "registered query snapshot (USAspending API v2)"
            )
            extension = "json"
        else:
            snapshot_url = A19_SNAPSHOT_URLS.get(period)
            if not snapshot_url:
                print(f"  no A-19 snapshot registered for {period}: {ref}")
                continue
            if period not in a19_cache:
                retrieved_at = utc_now()
                try:
                    with urllib.request.urlopen(snapshot_url, timeout=120) as r:
                        raw_html = r.read()
                    a19_cache[period] = (
                        a19_values_from_html(raw_html.decode()),
                        raw_html,
                        snapshot_url,
                        retrieved_at,
                    )
                except urllib.error.HTTPError as exc:
                    print(f"  A-19 snapshot fetch failed ({exc}): {ref}")
                    a19_cache[period] = ({}, None, snapshot_url, retrieved_at)
            values, raw, source_url, retrieved_at = a19_cache[period]
            value = values.get(spec["a19_row"])
            series_id = f"cpseea19-{spec['a19_row']}"
            source_file = "cpseea19.htm (Wayback snapshot)"
            extension = "html"
        if value is None or raw is None:
            print(f"  not yet published: {ref}")
            continue
        if not value_plausible(value, forecast):
            print(
                f"  IMPLAUSIBLE VALUE (refusing, wrong series/transform?): "
                f"{ref} -> {value}"
            )
            continue
        row = generic_fact(
            ref, spec, period_type, period, value, release_day,
            source_url, source_file,
        )
        fetched_rows.append(
            (row, series_id, release_day.isoformat(), raw, retrieved_at, extension)
        )
        print(f"  resolve {ref} -> {row['value']} {row['measure']['unit']}")

    if not fetched_rows:
        print("nothing new to record")
        return 0
    if args.dry_run:
        print(f"dry-run: would append {len(fetched_rows)} row(s)")
        for row, *_ in fetched_rows:
            print(json.dumps(row)[:200])
        return 0

    run_retrieved_at = min(item[4] for item in fetched_rows)
    run_dir = resolution_run_dir(run_retrieved_at)
    run_dir.mkdir(parents=True, exist_ok=False)
    target_contracts = registration_contracts()
    new_rows = [
        attach_resolution_provenance(
            row,
            run_dir=run_dir,
            series_id=series_id,
            vintage=vintage,
            raw=raw,
            retrieved_at=retrieved_at,
            ledger_repo_sha=ledger_repo_sha,
            target_contracts=target_contracts,
            extension=extension,
        )
        for row, series_id, vintage, raw, retrieved_at, extension in fetched_rows
    ]

    updated = (
        content.rstrip("\n")
        + "\n"
        + "\n".join(json.dumps(row, separators=(",", ":")) for row in new_rows)
        + "\n"
    )
    finalize_resolution_manifest(
        run_dir,
        {
            "schemaVersion": "thesis_resolution_run_v1",
            "retrievedAt": run_retrieved_at,
            "ledgerRepo": args.ledger_repo,
            "ledgerBranch": args.ledger_branch,
            "ledgerRepoSha": ledger_repo_sha,
            "facts": [
                {
                    "dataPointId": row["source_record_id"],
                    "sourceVintage": row["sourceVintage"],
                    "retrievedAt": row["retrievedAt"],
                    "targetContentHash": row.get("targetContentHash"),
                    "responseArchive": row["responseArchive"],
                }
                for row in new_rows
            ],
        },
    )
    merged_sha = propose_ledger_append(
        args.ledger_repo,
        args.ledger_branch,
        args.ledger_path,
        updated,
        sha,
        ledger_repo_sha,
        len(new_rows),
        producer_signing_key=producer_signing_key,
    )
    print(
        f"appended {len(new_rows)} observation(s) to "
        f"{args.ledger_repo}@{args.ledger_branch}:{args.ledger_path} "
        f"via reviewed proposal (merged at {merged_sha})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
