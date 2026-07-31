"""Full app-v2 economy metrics on a pinned Populace build, run on Modal.

Why Modal: a national PolicyEngine microsim OOMs a 16 GB laptop (every state's
EITC spawns a population branch-clone). Modal gives a 32 GB box, so both arms
run. We pin the CERTIFIED stack for the build (policyengine-us==1.764.6 +
core==3.26.11 for build P) — running an uncertified model/data pair is exactly
what the #45 audit exists to prevent.

Run:  modal run scripts/tools/modal_economy.py
Output: prints JSON metrics; the local entrypoint also writes it under bills/.
"""

import json
import modal

# Certified stack for build P (per the build's release_manifest.json).
PE_US = "1.764.6"
PE_CORE = "3.26.11"
BUILD_P = "populace-us-2024-buildp-sparse-rmloss100-cae8640-20260728T011454Z"
DATASET = f"hf://datasets/policyengine/populace-us/populace_us_2024.h5@{BUILD_P}"

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

    b_net = baseline.calculate("household_net_income", year)
    r_net = reformed.calculate("household_net_income", year)
    budgetary_impact = float((b_net - r_net).sum())  # negative = cost to government

    def agg(sim, var):
        try:
            return float(sim.calculate(var, year).sum())
        except Exception:
            return None

    # budget decomposition
    b_tax, r_tax = agg(baseline, "household_tax"), agg(reformed, "household_tax")
    b_ben, r_ben = agg(baseline, "household_benefits"), agg(reformed, "household_benefits")

    # poverty by group (SPM), + deep child
    def pov(sim, var, child=False):
        p = sim.calculate(var, period=year, map_to="person")
        if child:
            age = sim.calculate("age", year)
            return float(p[age < 18].mean())
        return float(p.mean())

    def block(bfun, rfun):
        b, r = bfun, rfun
        return {"baseline": b, "reform": r, "change": r - b,
                "pct_change": ((r - b) / b) if b else None}

    poverty = {
        "all": block(pov(baseline, "in_poverty"), pov(reformed, "in_poverty")),
        "child": block(pov(baseline, "in_poverty", True), pov(reformed, "in_poverty", True)),
        "deep_child": block(pov(baseline, "in_deep_poverty", True), pov(reformed, "in_deep_poverty", True)),
    }

    # decile impacts (grouped by BASELINE income decile)
    decile = baseline.calculate("household_income_decile", year)
    change = r_net - b_net
    avg = change.groupby(decile).mean()
    rel = change.groupby(decile).sum() / b_net.groupby(decile).sum()
    decile_avg = {int(k): float(v) for k, v in avg.to_dict().items() if k and k > 0}
    decile_rel = {int(k): float(v) for k, v in rel.to_dict().items() if k and k > 0}

    # winners / losers (share of people by relative household net-income change)
    person_decile = baseline.calculate("household_net_income", year)  # placeholder to get weights
    rel_change = np.where(np.array(b_net) != 0, np.array(r_net - b_net) / np.array(b_net), 0.0)
    w = b_net.weights
    hh_people = baseline.calculate("household_count_people", year)
    pw = np.array(w) * np.array(hh_people)
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

    # inequality
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
            "tax_revenue_impact": (r_tax - b_tax) if (b_tax is not None and r_tax is not None) else None,
            "benefit_spending_impact": (r_ben - b_ben) if (b_ben is not None and r_ben is not None) else None,
            "baseline_net_income": float(b_net.sum()),
            "households": float(b_net.weights.sum()),
        },
        "poverty": poverty,
        "decile": {"average": decile_avg, "relative": decile_rel},
        "intra_decile": {"all": winners_losers},
        "inequality": inequality,
    }


@app.local_entrypoint()
def main():
    reform = {"gov.irs.credits.ctc.refundable.phase_in.threshold": {"2026-01-01.2100-12-31": 0}}
    result = economy.remote(reform, 2026)
    print(json.dumps(result, indent=2))
    with open("bills/stronger-start-working-families-act/buildP-economy-2026.json", "w") as f:
        json.dump(result, f, indent=2)
