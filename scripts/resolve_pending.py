#!/usr/bin/env python3
"""Resolve pending forecast cells whose official numbers have published.

Adapter-based: each adapter claims a family of targetFactRefs from the live
catalog's resolutionLinks, checks whether the official first print exists
yet, and emits a PolicyEngine-Ledger fact row (the JSONL schema the site's
build fetches and joins on source_record_id == targetFactRef). Appending a
row is what resolves a cell: the next site build scores it.

First adapters: DOL UI weekly claims (initial + continued, seasonally
adjusted), read from FRED's ICSA/CCSA series — the advance vintage named by
the cells' own resolver rules.

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
import urllib.request
from typing import Any

from canonical_json import canonical_bytes, canonical_sha256
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

MONTH_NUMBERS = {
    name: number
    for number, name in enumerate(
        "january february march april may june july august september "
        "october november december".split(),
        start=1,
    )
}


def parse_ref_period(ref: str, stem: str) -> tuple[str, str] | None:
    """(period_type, YYYY-MM) parsed from a dataPointId's period tail."""
    tail = ref[len(stem) + 1 :]
    tail = re.sub(r"\.(first_print|advance|second|third)_?(estimate)?$", "", tail)
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
        "geography": {
            "level": "country",
            "id": "0100000US",
            "vintage": "current",
            "name": "United States",
        },
        "entity": spec.get("entity", {"name": "economy", "role": "aggregate"}),
        "measure": {
            "concept": ref.rsplit(".", 1)[0]
            if ref.endswith("first_print")
            else ref,
            "unit": spec["unit"],
            "source_concept": spec.get("fred", spec.get("source_concept", "")),
            "concept_relation": "source_label",
            "concept_authority": spec["concept_authority"],
            "concept_evidence_url": source_url,
            "concept_evidence_notes": (
                f"First print for {period} captured from {source_url} on the "
                "official release date named by the cell's resolver."
            ),
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


def push_ledger(
    repo: str, branch: str, path: str, content: str, sha: str, added: int
) -> None:
    import base64

    body = {
        "message": f"Record {added} first-print observation(s) via resolve_pending.py",
        "content": base64.b64encode(content.encode()).decode(),
        "sha": sha,
        "branch": branch,
    }
    completed = subprocess.run(
        ["gh", "api", "-X", "PUT", f"repos/{repo}/contents/{path}", "--input", "-"],
        input=json.dumps(body),
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"ledger push failed: {completed.stderr.strip()[:500]}")


def registration_hashes(
    records_dir: pathlib.Path | None = None,
) -> dict[str, str]:
    """Map preregistered dataPointIds to verified snapshot hashes."""
    records_dir = records_dir or ROOT / "records" / "targets"
    hashes: dict[str, str] = {}
    if not records_dir.exists():
        return hashes
    for path in sorted(records_dir.glob("*.json")):
        match = re.fullmatch(r"\d{4}-\d{2}-\d{2}-([0-9a-f]{64})\.json", path.name)
        if not match:
            continue
        try:
            snapshot = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        # v2 per-target snapshots deliberately exclude registeredAtUtc from
        # their filename hash (the pushed registration commit witnesses that
        # instant); v1 day-batch snapshots hash the whole payload. Accept
        # whichever commitment the filename actually carries.
        accepted = {canonical_sha256(snapshot)}
        try:
            from register_targets import registration_content_hash

            accepted.add(registration_content_hash(snapshot))
        except Exception:
            pass
        if match.group(1) not in accepted:
            raise ValueError(f"target registration hash mismatch: {path}")
        content_hash = match.group(1)
        for target in snapshot.get("targets", []):
            data_point_id = target.get("dataPointId")
            if data_point_id:
                hashes[str(data_point_id)] = content_hash
    return hashes


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
    target_hashes: dict[str, str],
    extension: str = "csv",
) -> dict[str, Any]:
    output = {
        **row,
        "ledgerRepoSha": ledger_repo_sha,
        "sourceVintage": vintage,
        "retrievedAt": retrieved_at,
        "responseArchive": archive_response(
            run_dir,
            series_id=series_id,
            vintage=vintage,
            raw=raw,
            extension=extension,
        ),
    }
    target_hash = target_hashes.get(str(row["source_record_id"]))
    if target_hash:
        output["targetContentHash"] = target_hash
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

    # Generic adapters: ALFRED vintage series and A-19 snapshot rows. FRED
    # fetches are cached per (series, vintage); A-19 snapshots per month.
    alfred_cache: dict[tuple[str, str], tuple[dict, bytes | None, str, str]] = {}
    a19_cache: dict[str, tuple[dict[str, float], bytes | None, str, str]] = {}
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
        if kind == "alfred":
            cache_key = (spec["fred"], release_day.isoformat())
            if cache_key not in alfred_cache:
                alfred_cache[cache_key] = fred_vintage_series(*cache_key)
            rows, raw, source_url, retrieved_at = alfred_cache[cache_key]
            value = apply_transform(rows, spec, period_type, period)
            series_id = spec["fred"]
            source_file = "alfredgraph.csv"
            extension = "csv"
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
    target_hashes = registration_hashes()
    new_rows = [
        attach_resolution_provenance(
            row,
            run_dir=run_dir,
            series_id=series_id,
            vintage=vintage,
            raw=raw,
            retrieved_at=retrieved_at,
            ledger_repo_sha=ledger_repo_sha,
            target_hashes=target_hashes,
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
    push_ledger(
        args.ledger_repo,
        args.ledger_branch,
        args.ledger_path,
        updated,
        sha,
        len(new_rows),
    )
    print(
        f"appended {len(new_rows)} observation(s) to "
        f"{args.ledger_repo}@{args.ledger_branch}:{args.ledger_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
