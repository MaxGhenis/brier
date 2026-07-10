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
import copy
import csv
import datetime as dt
import gzip
import hashlib
import io
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.request
from typing import Any
from urllib.parse import urlparse

from canonical_json import canonical_bytes, canonical_sha256
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
    "EA": {"level": "area", "id": "EA21", "vintage": "current", "name": "Euro area"},
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
    return round(value, 4)


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
        r"\.(first_print|advance|second|third|flash|preliminary)_?(estimate)?$",
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
    return round(value, 4)


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
            "concept": re.sub(r"\.(first_print|flash|preliminary)$", "", ref),
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
    command = ["gh", "api", *args]
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
) -> str:
    """Append through a reviewed proposal, never by writing the branch.

    The accepted branch only advances through a pull request whose append
    gate (schema, immutable prefix, append-only diff, contract bindings,
    supersede semantics) has passed. The proposal branches from the exact
    state the rows were built against; a merge without a passing gate, or
    with no gate at all, fails closed and leaves the proposal open for
    humans (review finding 5).
    """
    import base64

    stamp = utc_now().lower().replace(":", "-").replace("t", "-")
    proposal = f"thesis-facts-append/{stamp}"
    _gh_api(
        "-X",
        "POST",
        f"repos/{repo}/git/refs",
        input_body={"ref": f"refs/heads/{proposal}", "sha": base_sha},
    )
    message = f"Record {added} first-print observation(s) via resolve_pending.py"
    put_response = json.loads(
        _gh_api(
            "-X",
            "PUT",
            f"repos/{repo}/contents/{path}",
            input_body={
                "message": message,
                "content": base64.b64encode(content.encode()).decode(),
                "sha": blob_sha,
                "branch": proposal,
            },
        )
    )
    head_sha = str(put_response["commit"]["sha"])
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
                    f"Automated append proposal from resolve_pending.py: "
                    f"{added} first-print observation(s) built against "
                    f"{base_sha}. Merges only after the thesis-facts append "
                    "gate passes."
                ),
            },
        )
    )
    pr_number = int(pr["number"])

    gate_passed = False
    for _ in range(poll_attempts):
        runs = json.loads(
            _gh_api(f"repos/{repo}/commits/{head_sha}/check-runs")
        ).get("check_runs", [])
        gate_runs = [run for run in runs if run.get("name") == "Append gate"]
        if gate_runs and all(
            run.get("status") == "completed" for run in gate_runs
        ):
            if all(run.get("conclusion") == "success" for run in gate_runs):
                gate_passed = True
            break
        time.sleep(poll_seconds)
    if not gate_passed:
        raise RuntimeError(
            f"append gate did not pass for {repo}#{pr_number}; leaving the "
            "proposal open for review instead of merging unreviewed rows"
        )

    _gh_api(
        "-X",
        "PUT",
        f"repos/{repo}/pulls/{pr_number}/merge",
        input_body={"merge_method": "rebase"},
    )
    _gh_api("-X", "DELETE", f"repos/{repo}/git/refs/heads/{proposal}")

    merged_sha = _gh_api(
        f"repos/{repo}/commits/{branch}", "--jq", ".sha"
    ).strip()
    merged_lines = _fetch_branch_lines(repo, merged_sha, path)
    expected_lines = [line for line in content.split("\n") if line.strip()]
    if merged_lines[: len(expected_lines)] != expected_lines:
        raise RuntimeError(
            "merged ledger does not extend the proposed append; investigate "
            f"{repo}@{merged_sha} before trusting new resolutions"
        )
    return merged_sha


def _fetch_branch_lines(repo: str, ref: str, path: str) -> list[str]:
    import base64

    payload = json.loads(
        _gh_api(
            f"repos/{repo}/contents/{path}?ref={ref}",
            "--jq",
            "{content: .content}",
        )
    )
    text = base64.b64decode(payload["content"]).decode()
    return [line for line in text.split("\n") if line.strip()]


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
            elif existing["targetContentHash"] != published:
                raise ValueError(
                    f"neither registration for published dataPointId {key} "
                    f"matches its target hash {published[:16]}…; resolve the "
                    "duplicate before appending"
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
    bls_cache: dict[
        tuple[str, int, int], tuple[dict, bytes | None, str, str]
    ] = {}
    a19_cache: dict[str, tuple[dict[str, float], bytes | None, str, str]] = {}
    intl_cache: dict[Any, tuple] = {}
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
    )
    print(
        f"appended {len(new_rows)} observation(s) to "
        f"{args.ledger_repo}@{args.ledger_branch}:{args.ledger_path} "
        f"via reviewed proposal (merged at {merged_sha})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
