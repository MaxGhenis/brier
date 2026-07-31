"""Full app-v2 economy metrics on a pinned Populace build, run on Modal —
THROUGH the audited wrapper (scripts/tools/policyengine.py).

Why Modal: a national PolicyEngine microsim OOMs a 16 GB laptop (every state's
EITC spawns a population branch-clone). Modal gives a 32 GB box, so both arms
run. We pin the CERTIFIED stack for the build (policyengine-us==1.764.6 +
core==3.26.11 for build P) — running an uncertified model/data pair is exactly
what the #45 audit exists to prevent.

Wrapper routing (review finding, #64 — the audit artifact must not bypass the
wrapper it audits): the local entrypoint validates the reform FAIL-CLOSED via
pe.validate_reform before submitting, and every completed run is recorded as a
pe.EconomyRun -> pe._log_call (bills/compute-log audit trail) with the bill.json
row produced by pe.compute_block. The remote function only computes.

Budget aggregation (review finding, #64): federal = engine's own federal
variables — income_tax (federal 1040 net liability incl. refundable credits)
minus household_benefits delta — NEVER the household_net_income proxy, which
lumps state tax spillover into a "federal" number. State spillover is reported
separately; the net-income delta is carried as a labeled cross-check only.

Run:
    modal run scripts/tools/modal_economy.py            # single year (2026)
    modal run scripts/tools/modal_economy.py::sweep     # ten-year sweep, parallel
(set PYTHONIOENCODING=utf-8 on Windows or the Modal CLI's checkmark crashes cp1252)

Output paths are __file__-anchored, never cwd-relative, and the full result
JSON prints before any file write — stdout is the recovery path.
"""

import json
import sys
from pathlib import Path

import modal

# Certified stack for build P (per the build's release_manifest.json).
PE_US = "1.764.6"
PE_CORE = "3.26.11"
BUILD_P = "populace-us-2024-buildp-sparse-rmloss100-cae8640-20260728T011454Z"
DATASET = f"hf://datasets/policyengine/populace-us/populace_us_2024.h5@{BUILD_P}"

def _out_dir() -> Path:
    # Resolved LAZILY at the local entrypoint only — the Modal container mounts
    # this file at a shallow path where .parents[2] raises IndexError at import.
    return Path(__file__).resolve().parents[2] / "bills" / "stronger-start-working-families-act"

STRONGER_START = {"gov.irs.credits.ctc.refundable.phase_in.threshold": {"2026-01-01.2100-12-31": 0}}

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        f"policyengine-us=={PE_US}",
        f"policyengine-core=={PE_CORE}",
        "microdf-python",
        "huggingface-hub",
    )
)

app = modal.App("stronger-start-buildp-economy")


@app.function(image=image, memory=32768, timeout=3600, cpu=4.0)
def economy(reform: dict, year: int) -> dict:
    import warnings
    warnings.filterwarnings("ignore")
    import numpy as np
    from policyengine_us import Microsimulation
    from policyengine_core.reforms import Reform

    baseline = Microsimulation(dataset=DATASET)
    reformed = Microsimulation(dataset=DATASET, reform=Reform.from_dict(reform, country_id="us"))

    # ---- federal budget, through the engine's own federal variables ----
    b_fed = float(baseline.calculate("income_tax", year).sum())
    r_fed = float(reformed.calculate("income_tax", year).sum())
    tax_revenue_impact = r_fed - b_fed  # negative = federal revenue falls

    b_ben = float(baseline.calculate("household_benefits", year).sum())
    r_ben = float(reformed.calculate("household_benefits", year).sum())
    benefit_spending_impact = r_ben - b_ben  # positive = spending rises

    budgetary_impact = tax_revenue_impact - benefit_spending_impact  # negative = cost

    def _try_sum(sim, var):
        try:
            return float(sim.calculate(var, year).sum())
        except Exception:
            return None

    b_state = _try_sum(baseline, "state_income_tax")
    r_state = _try_sum(reformed, "state_income_tax")
    state_tax_revenue_impact = (r_state - b_state) if (b_state is not None and r_state is not None) else None

    # cross-check only — includes state spillover by construction
    b_net = baseline.calculate("household_net_income", year)
    r_net = reformed.calculate("household_net_income", year)
    household_net_income_delta = float((r_net - b_net).sum())

    # ---- poverty by group (SPM) ----
    def pov(sim, var, child=False):
        p = sim.calculate(var, period=year, map_to="person")
        if child:
            age = sim.calculate("age", year)
            return float(p[age < 18].mean())
        return float(p.mean())

    def block(b, r):
        return {"baseline": b, "reform": r, "change": r - b,
                "pct_change": ((r - b) / b) if b else None}

    poverty = {
        "all": block(pov(baseline, "in_poverty"), pov(reformed, "in_poverty")),
        "child": block(pov(baseline, "in_poverty", True), pov(reformed, "in_poverty", True)),
        "deep_child": block(pov(baseline, "in_deep_poverty", True), pov(reformed, "in_deep_poverty", True)),
    }

    # ---- decile impacts (baseline income decile; net-income change) ----
    decile = baseline.calculate("household_income_decile", year)
    change = r_net - b_net
    avg = change.groupby(decile).mean()
    rel = change.groupby(decile).sum() / b_net.groupby(decile).sum()
    decile_avg = {int(k): float(v) for k, v in avg.to_dict().items() if k and k > 0}
    decile_rel = {int(k): float(v) for k, v in rel.to_dict().items() if k and k > 0}

    # ---- winners/losers (person-weighted) ----
    rel_change = np.where(np.array(b_net) != 0, np.array(r_net - b_net) / np.array(b_net), 0.0)
    hh_people = baseline.calculate("household_count_people", year)
    pw = np.array(b_net.weights) * np.array(hh_people)
    total = pw.sum()

    def share(mask):
        return float(pw[mask].sum() / total)

    winners_losers = {
        "gain_more_5pct": share(rel_change > 0.05),
        "gain_less_5pct": share((rel_change > 1e-3) & (rel_change <= 0.05)),
        "no_change": share(np.abs(rel_change) <= 1e-3),
        "lose_less_5pct": share((rel_change < -1e-3) & (rel_change >= -0.05)),
        "lose_more_5pct": share(rel_change < -0.05),
    }

    # ---- inequality ----
    try:
        gini_b, gini_r = float(b_net.gini()), float(r_net.gini())
        inequality = {"gini": {"baseline": gini_b, "reform": gini_r,
                               "pct_change": (gini_r - gini_b) / gini_b if gini_b else None}}
    except Exception:
        inequality = {}

    return {
        "engine": "modal",
        "dataset": BUILD_P,
        "pe_us_version": PE_US,
        "pe_core_version": PE_CORE,
        "year": year,
        "reform": reform,
        "budget": {
            "budgetary_impact": budgetary_impact,
            "tax_revenue_impact": tax_revenue_impact,
            "benefit_spending_impact": benefit_spending_impact,
            "state_tax_revenue_impact": state_tax_revenue_impact,
            "household_net_income_delta": household_net_income_delta,
            "baseline_net_income": float(b_net.sum()),
            "households": float(b_net.weights.sum()),
        },
        "poverty": poverty,
        "decile": {"average": decile_avg, "relative": decile_rel},
        "intra_decile": {"all": winners_losers},
        "inequality": inequality,
    }


# --------------------------------------------------------------------------- #
# Wrapper routing at the entrypoints                                           #
# --------------------------------------------------------------------------- #
def _wrapper():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import policyengine as pe  # the audited call path (issue #45)
    return pe


def _validate_or_die(pe, reform: dict):
    v = pe.validate_reform(reform)  # FAIL-CLOSED: refuses if existence unverifiable
    if not v.ok:
        raise SystemExit("reform failed validation:\n  - " + "\n  - ".join(v.problems))
    print(f"validated [{v.param_source}] checked_existence={v.checked_existence}")
    return v


def _certify_or_die(pe):
    """Check the pinned stack against the build BEFORE a container starts.

    The image pins PE_US and the run pins BUILD_P, so the pairing is decided at
    edit time; catching a mismatch here costs nothing, while catching it in
    compute_block costs a 32 GB container and yields a number somebody will
    quote before reading the warning."""
    try:
        cert = pe.require_certification(BUILD_P, PE_US)
    except pe.UncertifiedPairing as exc:
        raise SystemExit(f"refusing to run: {exc}")
    print(f"certified {cert['certified_model_version']} against {BUILD_P}")
    return cert


def _record(pe, v, result: dict, provision: str) -> dict:
    """Register the remote result in the wrapper's audit trail and emit the
    bill.json compute row via pe.compute_block — the artifact goes through the
    wrapper, never around it."""
    from datetime import datetime, timezone

    imp = {
        "budgetary_impact": result["budget"]["budgetary_impact"],
        "tax_revenue_impact": result["budget"]["tax_revenue_impact"],
        "benefit_spending_impact": result["budget"]["benefit_spending_impact"],
        "state_tax_revenue_impact": result["budget"].get("state_tax_revenue_impact"),
        "household_net_income_delta": result["budget"].get("household_net_income_delta"),
        "poverty": {"all": result["poverty"]["all"], "child": result["poverty"]["child"]},
        "deep_poverty": {"child": result["poverty"]["deep_child"]},
    }
    run = pe.EconomyRun(
        "ok", result["year"], "us", "us", result["reform"], None, pe.baseline_id("us"),
        impact=imp, message="ok", engine="modal", dataset=result["dataset"],
        pe_us_version=result["pe_us_version"], param_source=v.param_source,
        checked_existence=v.checked_existence,
        certification=pe.certification_note(result["dataset"], result["pe_us_version"]),
        computed_at=datetime.now(timezone.utc).isoformat(),
    )
    pe._log_call(run, pe.DEFAULT_LOG_DIR)
    return pe.compute_block(run, provision)


@app.local_entrypoint()
def main():
    pe = _wrapper()
    v = _validate_or_die(pe, STRONGER_START)
    _certify_or_die(pe)
    result = economy.remote(STRONGER_START, 2026)
    print(json.dumps(result, indent=2))
    block = _record(pe, v, result,
                    "Sec. 2 — strike refundable CTC earnings threshold ($2,500 -> $1)")
    print(json.dumps(block, indent=2))
    with open(_out_dir() / "buildP-economy-2026.json", "w") as f:
        json.dump(result, f, indent=2)
    with open(_out_dir() / "compute-row-2026.json", "w") as f:
        json.dump(block, f, indent=2)


@app.local_entrypoint()
def sweep(start: int = 2026, end: int = 2035):
    """Ten-year sweep, one container per year in parallel:
    modal run scripts/tools/modal_economy.py::sweep"""
    pe = _wrapper()
    v = _validate_or_die(pe, STRONGER_START)
    _certify_or_die(pe)
    years = list(range(start, end + 1))
    rows = []
    for res in economy.map([STRONGER_START] * len(years), years):
        rows.append({
            "year": res["year"],
            "budgetary_impact": res["budget"]["budgetary_impact"],
            "tax_revenue_impact": res["budget"]["tax_revenue_impact"],
            "benefit_spending_impact": res["budget"]["benefit_spending_impact"],
            "state_tax_revenue_impact": res["budget"].get("state_tax_revenue_impact"),
            "child_poverty_baseline": res["poverty"]["child"]["baseline"],
            "child_poverty_reform": res["poverty"]["child"]["reform"],
        })
    rows.sort(key=lambda r: r["year"])
    total = sum(r["budgetary_impact"] for r in rows)
    out = {"dataset": BUILD_P, "pe_us_version": PE_US, "pe_core_version": PE_CORE,
           "engine": "modal", "reform": STRONGER_START,
           "validation": {"param_source": v.param_source, "checked_existence": v.checked_existence},
           "years": rows, "ten_year_budgetary_impact": total}
    print(json.dumps(out, indent=2))
    with open(_out_dir() / f"buildP-sweep-{start}-{end}.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"TOTAL {start}-{end}: ${total/1e9:,.1f}B")
