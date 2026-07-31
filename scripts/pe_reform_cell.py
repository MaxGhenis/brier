#!/usr/bin/env python3
"""Minimal reform -> PolicyEngine -> outcome metric -> draft forecast cell.

The smallest end-to-end path through the lab for a *policy* target: change ONE
PolicyEngine-US parameter, recompute a population outcome under baseline and
reform, size an 80% interval from the microdata itself, and emit a draft cell
that satisfies docs/cell-contract.md.

Worked example (the defaults): raise the federal minimum wage
(``gov.dol.minimum_wage``) from $7.25 to $15.00 and measure how many working-age
adults are newly exposed to failing the OBBBA Medicaid community-engagement
("work") requirement through its income route in 2027.

MODELING CAVEAT — read before citing any number this produces.
PolicyEngine-US is a STATIC tax-benefit model. Raising the minimum wage does not
raise anybody's earnings in it. Across the whole US model the parameter is read
by exactly four variables, and in every one it is a THRESHOLD, never a wage
floor:

    medicaid_work_requirement_eligible   (national)
    nm_cdcc_eligible                     (New Mexico)
    ok_ccs_activity_eligible             (Oklahoma)
    sd_cca_parent_in_eligible_activity   (South Dakota)

In the Medicaid variable it sets
``monthly_income_threshold = minimum_wage * monthly_hours_threshold`` (80h). So
a higher minimum wage RAISES the income bar for passing the work requirement
through the income route while earnings are held fixed, and modelled
eligibility goes DOWN. That is the threshold-indexation channel. It is NOT an
estimate of the labour-market effect of a wage floor.

TWO-STAGE DESIGN (and why).
Running ``Microsimulation.calculate("medicaid_work_requirement_eligible")`` over
the national dataset costs ~13 GB of commit — the cost is the VARIABLE GRAPH,
not the data. On an 8 GB box that thrashes the pagefile rather than computing.
``Simulation.subsample()`` does not help: it materialises the whole dataset via
``to_input_dataframe()`` before sampling, so its peak is roughly flat in n
(measured: 0.97 GB -> 5.46 GB just to build at n=2500).

So the pipeline splits the work:

  Stage 1 (mechanism)  A tiny Simulation over a handful of synthetic households
                       runs the REAL Reform through the REAL variable and shows
                       the eligibility flip. Cheap, exact, proves the plumbing.
  Stage 2 (population) The exposed population is counted by reading the
                       microdata columns directly out of the HDF5 and applying
                       the threshold rule the variable implements. Bounded
                       memory, real weights, national scope.

Stage 2 is a rule-applied-to-microdata estimate, not a full variable-graph
computation, and the emitted cell says so.

Usage:
    python scripts/pe_reform_cell.py --out draft_cells.json

Requires policyengine-us (see docs/policyengine-reform-loop.md).
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone

import numpy as np

# 80% interval => +/- 1.28 sigma. Named because the contract's validator greps
# the math step for this multiplier.
Z_80 = 1.28

# Hard ceiling on this process's commit. The national variable-graph path wants
# ~13 GB on a 7.4 GB box; abort loudly instead of thrashing the pagefile.
COMMIT_GUARD_MB = 3_500

SOURCE_CONTEXT = [
    "https://github.com/PolicyEngine/policyengine-us",
    "https://www.law.cornell.edu/uscode/text/29/206",
    "https://www.congress.gov/bill/119th-congress/house-bill/1/text",
    "https://www.medicaid.gov/federal-policy-guidance/downloads/cib12082025.pdf",
]

# Read straight out of policyengine_us/parameters/gov/dol/minimum_wage.yaml.
MINIMUM_WAGE_HISTORY = [
    {"label": "2007-07-24 federal minimum wage", "value": 5.85},
    {"label": "2008-07-24 federal minimum wage", "value": 6.55},
    {"label": "2009-07-24 federal minimum wage", "value": 7.25},
]

MONTHS = 12


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--parameter", default="gov.dol.minimum_wage")
    p.add_argument("--value", type=float, default=15.00)
    p.add_argument("--period", type=int, default=2027)
    p.add_argument("--metric", default="medicaid_work_requirement_eligible")
    p.add_argument("--out", type=pathlib.Path, default=pathlib.Path("draft_cells.json"))
    p.add_argument("--run-json", type=pathlib.Path, default=None)
    p.add_argument("--bootstrap", type=int, default=400)
    p.add_argument("--seed", type=int, default=20260731)
    p.add_argument(
        "--dataset",
        type=pathlib.Path,
        default=None,
        help="populace_us_*.h5; defaults to the newest in the HF cache",
    )
    p.add_argument(
        "--slug",
        default="us-adults-newly-exposed-medicaid-work-requirement-2027",
    )
    return p.parse_args(argv)


def report_memory(stage: str) -> dict:
    """Print commit + free RAM for a stage, and abort if commit runs away.

    Working set is the misleading metric here: once Windows starts paging, RSS
    *falls* while the process is actually in trouble. Commit (private bytes) is
    what tracks real demand, so that is what gets printed and guarded on.
    """
    try:
        import psutil
    except ImportError:
        return {}
    proc = psutil.Process()
    commit_mb = proc.memory_info().private / 1024**2
    free_mb = psutil.virtual_memory().available / 1024**2
    print(
        f"[mem] {stage}: commit={commit_mb:,.0f}MB free={free_mb:,.0f}MB",
        file=sys.stderr,
        flush=True,
    )
    if commit_mb > COMMIT_GUARD_MB:
        raise MemoryError(
            f"commit {commit_mb:,.0f}MB exceeded the {COMMIT_GUARD_MB:,}MB guard "
            f"at stage {stage!r} — aborting rather than thrashing the pagefile"
        )
    return {"stage": stage, "commit_mb": commit_mb, "free_mb": free_mb}


def find_dataset(explicit: pathlib.Path | None) -> pathlib.Path:
    if explicit:
        return explicit
    cache = pathlib.Path.home() / ".cache/huggingface/hub"
    candidates = sorted(cache.glob("**/populace_us_*.h5"))
    if not candidates:
        raise FileNotFoundError(
            "no populace_us_*.h5 in the HuggingFace cache; run a Microsimulation "
            "once to download it, or pass --dataset"
        )
    return candidates[-1]


# --------------------------------------------------------------------------
# Stage 1: mechanism. Real Reform, real variable, a handful of households.
# --------------------------------------------------------------------------


def run_mechanism_check(args) -> dict:
    from policyengine_core.reforms import Reform
    from policyengine_us import Simulation

    year = str(args.period)
    reform = Reform.from_dict(
        {args.parameter: {f"{args.period}-01-01.{args.period}-12-31": args.value}},
        country_id="us",
    )

    # Earnings chosen to straddle both bars: below baseline, between the two,
    # and above reform. Zero weekly hours so the 80-hour activity route cannot
    # mask the income route we are testing.
    earnings = [3_000, 10_000, 20_000]
    people = {
        f"p{i}": {
            "age": {year: 30},
            "employment_income": {year: e},
            "weekly_hours_worked": {year: 0},
        }
        for i, e in enumerate(earnings)
    }
    members = list(people)
    situation = {
        "people": people,
        "tax_units": {f"tu{i}": {"members": [m]} for i, m in enumerate(members)},
        "families": {f"f{i}": {"members": [m]} for i, m in enumerate(members)},
        "spm_units": {f"s{i}": {"members": [m]} for i, m in enumerate(members)},
        "marital_units": {f"m{i}": {"members": [m]} for i, m in enumerate(members)},
        "households": {
            f"h{i}": {"members": [m], "state_name": {year: "TX"}}
            for i, m in enumerate(members)
        },
    }

    out = {"earnings": earnings}
    for label, ref in (("baseline", None), ("reform", reform)):
        sim = Simulation(situation=situation, reform=ref) if ref else Simulation(
            situation=situation
        )
        node = sim.tax_benefit_system.parameters(f"{args.period}-06-01")
        for part in args.parameter.split("."):
            node = getattr(node, part)
        wage = float(node)
        eligible = sim.calculate(args.metric, args.period)
        out[label] = {
            "minimum_wage": wage,
            "annual_bar": wage * 80 * MONTHS,
            "eligible": [bool(x) for x in eligible],
        }
        del sim
    out["flipped"] = [
        b and not r
        for b, r in zip(out["baseline"]["eligible"], out["reform"]["eligible"])
    ]
    return out


# --------------------------------------------------------------------------
# Stage 2: population. Direct columnar read of the microdata.
# --------------------------------------------------------------------------


def load_microdata(path: pathlib.Path) -> dict[str, np.ndarray]:
    import h5py

    cols = (
        "age",
        "employment_income",
        "self_employment_income",
        "weight",
        "person_household_id",
        "is_disabled",
        "is_full_time_college_student",
        "hourly_wage",
    )
    with h5py.File(path, "r") as f:
        table = f["person"]["table"]
        # Read the columns we need one at a time; reading the whole compound
        # row set would pull all 250 fields into memory for nothing.
        data = {c: np.asarray(table[c]) for c in cols}
    return data


def exposed_mask(data: dict[str, np.ndarray], base_bar: float, reform_bar: float):
    """People newly failing the INCOME route who cannot fall back on hours.

    Deliberately an upper bound on newly-exposed adults: the real variable
    exempts many more groups (pregnancy, caretakers of children <=13, medically
    frail, AIAN, incarcerated, veterans, former foster youth, Medicare) that the
    microdata columns here cannot identify.
    """
    earnings = data["employment_income"] + data["self_employment_income"]
    age = data["age"]

    working_age = (age >= 19) & (age < 65)
    in_band = (earnings >= base_bar) & (earnings < reform_bar)

    # The 80h/month activity route: anyone plausibly clearing it is not exposed.
    wage = np.where(data["hourly_wage"] > 0, data["hourly_wage"], np.nan)
    implied_monthly_hours = np.divide(
        earnings, wage * MONTHS, out=np.zeros_like(earnings), where=~np.isnan(wage)
    )
    fails_hours = implied_monthly_hours < 80

    observable_exempt = (data["is_disabled"] > 0) | (
        data["is_full_time_college_student"] > 0
    )

    return working_age & in_band & fails_hours & ~observable_exempt, {
        "working_age": working_age,
        "in_band": in_band,
        "fails_hours": fails_hours,
        "observable_exempt": observable_exempt,
    }


def cluster_bootstrap_sigma(
    contrib: np.ndarray, clusters: np.ndarray, draws: int, seed: int
) -> float:
    """Sampling sigma of a weighted count, resampling households."""
    rng = np.random.default_rng(seed)
    order = np.argsort(clusters, kind="stable")
    sorted_ids, sorted_contrib = clusters[order], contrib[order]
    starts = np.concatenate(([0], np.flatnonzero(np.diff(sorted_ids)) + 1))
    per_cluster = np.add.reduceat(sorted_contrib, starts)
    n = len(per_cluster)
    if n == 0:
        return 0.0
    idx = rng.integers(0, n, size=(draws, n))
    return float(per_cluster[idx].sum(axis=1).std(ddof=1))


def build_cell(args, facts: dict) -> dict:
    point = round(facts["exposed"] / 1e6, 2)
    sigma_m = facts["sigma_total"] / 1e6
    ci_low = round(point - Z_80 * sigma_m, 2)
    ci_high = round(point + Z_80 * sigma_m, 2)
    if ci_low >= point:
        ci_low = round(point - 0.01, 2)
    if ci_high <= point:
        ci_high = round(point + 0.01, 2)

    mech = facts["mechanism"]
    flipped_at = [
        e for e, f in zip(mech["earnings"], mech["flipped"]) if f
    ]

    reasoning = [
        {
            "kind": "heading",
            "text": (
                f"US adults newly exposed to the Medicaid work requirement in "
                f"{args.period} under a ${args.value:.2f} federal minimum wage"
            ),
        },
        {
            "kind": "text",
            "text": (
                f"One-parameter counterfactual: {args.parameter} moves from "
                f"${facts['baseline_wage']:.2f} to ${args.value:.2f} for "
                f"{args.period}; nothing else changes. PolicyEngine-US is a "
                "static model, so no earnings rise. The parameter reaches the "
                "outcome only as a threshold — monthly_income_threshold = "
                "minimum_wage x 80 hours inside "
                "medicaid_work_requirement_eligible — so raising the floor "
                "raises the bar for passing the requirement via the income "
                "route while earnings are held fixed. This is threshold "
                "indexation, not a labour-market effect."
            ),
        },
        {
            "kind": "tool",
            "tool": "policyengine.simulation",
            "call": (
                "Mechanism check: ran the real Reform through the real "
                f"{args.metric} variable on {len(mech['earnings'])} synthetic "
                "single-adult households with zero weekly hours."
            ),
            "result": (
                f"Annual income bar moves ${mech['baseline']['annual_bar']:,.0f} "
                f"-> ${mech['reform']['annual_bar']:,.0f}. Earnings "
                f"{mech['earnings']} give baseline eligibility "
                f"{mech['baseline']['eligible']} and reform eligibility "
                f"{mech['reform']['eligible']}; the $"
                f"{flipped_at[0]:,} case flips, confirming the parameter "
                "propagates to the outcome variable."
            ),
        },
        {
            "kind": "tool",
            "tool": "policyengine.microdata",
            "call": (
                f"Read {facts['n_records']:,} person records from "
                f"{facts['dataset_name']} and applied the threshold rule."
            ),
            "result": (
                f"Weighted population {facts['weighted_population'] / 1e6:,.1f} "
                f"million; {facts['in_band_weighted'] / 1e6:.2f} million people "
                f"have earnings in the newly exposed band "
                f"${facts['baseline_bar']:,.0f}-${facts['reform_bar']:,.0f}."
            ),
        },
        {
            "kind": "tool",
            "tool": "policyengine.microdata",
            "call": (
                "Filtered that band to working-age adults who cannot fall back "
                "on the 80-hour activity route and are not observably exempt."
            ),
            "result": (
                f"{facts['exposed']:,.0f} people ({point:.2f} million) remain "
                f"exposed, {facts['exposed'] / facts['in_band_weighted'] * 100:.1f} "
                "percent of the raw band after the age, hours and exemption "
                "screens."
            ),
        },
        {
            "kind": "text",
            "text": (
                "Base rate for the interval: the federal minimum wage has moved "
                "only three times since 2007 (5.85, 6.55, 7.25) and has been "
                "frozen at $7.25 since 2009-07-24, so the historical range of "
                "the parameter itself is narrow and essentially all uncertainty "
                "here is survey and model uncertainty rather than "
                "parameter-path uncertainty."
            ),
        },
        {
            "kind": "math",
            "text": (
                f"Point = {point:.2f} million exposed. sigma_sampling = "
                f"{facts['sigma_sampling'] / 1e6:.3f}M from a {args.bootstrap}-draw "
                "household-clustered bootstrap of the weighted count. "
                f"sigma_scope = {facts['sigma_scope'] / 1e6:.3f}M, taken as a "
                "quarter of the exposed count, reflecting that unobservable "
                "exemptions can only reduce it and the hours proxy is "
                "imputed. Combining independently: sigma = sqrt("
                f"{facts['sigma_sampling'] / 1e6:.3f}^2 + "
                f"{facts['sigma_scope'] / 1e6:.3f}^2) = {sigma_m:.3f}M. "
                f"80% interval = {point:.2f} +/- 1.28 * {sigma_m:.3f} = "
                f"[{ci_low:.2f}, {ci_high:.2f}] million."
            ),
        },
        {
            "kind": "text",
            "text": (
                "What would land outside the interval: this is an upper bound "
                "on newly exposed adults, because the real variable exempts "
                "pregnancy, caretakers of children 13 and under, the medically "
                "frail, AIAN members, veterans, former foster youth and "
                "Medicare enrollees, none of which these microdata columns "
                "identify. Downside risk therefore dominates — a full "
                "variable-graph run would land below this figure. Upside risk "
                "is narrower: it needs the hourly-wage imputation to overstate "
                "how many people clear the 80-hour route."
            ),
        },
        {"kind": "forecast", "point": point, "ciLow": ci_low, "ciHigh": ci_high},
    ]

    return {
        "slug": args.slug,
        "country": "US",
        "type": "policy",
        "title": (
            f"US adults newly exposed to Medicaid work requirement, "
            f"{args.period}, ${args.value:.0f} minimum wage"
        ),
        "question": (
            "Under a counterfactual in which the federal minimum wage "
            f"(gov.dol.minimum_wage) is ${args.value:.2f} for {args.period}, how "
            "many US working-age adults have earnings in the band that newly "
            "fails the Medicaid community-engagement income route and cannot "
            "fall back on the 80-hour activity route, in millions?"
        ),
        "unit": "millions",
        "pointEstimate": point,
        "ciLow": ci_low,
        "ciHigh": ci_high,
        "confidence": 0.8,
        "resolutionDate": f"{args.period}-01-04",
        "resolutionSource": "PolicyEngine-US model recomputation",
        "resolutionSourceUrl": "https://github.com/PolicyEngine/policyengine-us",
        "resolutionRule": (
            "Resolve by recomputation with the latest policyengine-us release "
            "available on the resolution date, using that release's default US "
            f"microdata. Apply the single-parameter reform {args.parameter} = "
            f"{args.value:.2f} for {args.period}. Count weighted persons aged "
            "19-64 whose employment plus self-employment income falls in "
            "[baseline bar, reform bar) where each bar is minimum_wage x 80 x "
            "12, whose imputed monthly hours are under 80, and who are neither "
            "disabled nor full-time students. Report in millions to 2 decimals. "
            "The forecast is against the THEN-CURRENT release, not a pinned "
            "one: model and dataset drift are part of what is forecast. "
            f"Baseline was policyengine-us {facts['policyengine_version']} on "
            f"{facts['dataset_name']}."
        ),
        "dataPointId": (
            f"policyengine.us.medicaid_work_requirement_exposed.{args.period}."
            f"reform_min_wage_{int(args.value)}"
        ),
        "conditionalOn": (
            f"PolicyEngine-US parameter {args.parameter} set to ${args.value:.2f} "
            f"for {args.period}; all other parameters at released values."
        ),
        "historicalContext": MINIMUM_WAGE_HISTORY,
        "drivers": [
            "Minimum wage enters the model only as an 80-hour income threshold, never as a wage floor",
            f"Annual income bar rises from ${facts['baseline_bar']:,.0f} to ${facts['reform_bar']:,.0f}",
            "Static model holds earnings fixed, so a higher floor strictly tightens the income route",
            "OBBBA work requirement only switches on 2027-01-01",
            "Unobservable exemptions make this an upper bound on newly exposed adults",
        ],
        "sourceContext": SOURCE_CONTEXT,
        "runAt": facts["run_at"],
        "reasoning": reasoning,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    mem_trace = [report_memory("start")]

    try:
        import policyengine_us  # noqa: F401
    except ImportError as exc:
        print(f"policyengine-us is not importable: {exc}", file=sys.stderr)
        return 2

    run_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    print("stage 1: mechanism check (real reform, real variable)...", file=sys.stderr)
    mechanism = run_mechanism_check(args)
    mem_trace.append(report_memory("mechanism checked"))
    if not any(mechanism["flipped"]):
        print(
            "mechanism check found no eligibility flip — the parameter does not "
            "propagate to the metric; refusing to emit a cell",
            file=sys.stderr,
        )
        return 3

    dataset = find_dataset(args.dataset)
    print(f"stage 2: reading microdata {dataset.name}...", file=sys.stderr)
    data = load_microdata(dataset)
    mem_trace.append(report_memory("microdata loaded"))

    base_bar = mechanism["baseline"]["annual_bar"]
    reform_bar = mechanism["reform"]["annual_bar"]
    mask, parts = exposed_mask(data, base_bar, reform_bar)

    weights = data["weight"]
    exposed = float((mask * weights).sum())
    in_band_weighted = float((parts["in_band"] & parts["working_age"]) @ weights)

    sigma_sampling = cluster_bootstrap_sigma(
        mask * weights, data["person_household_id"], args.bootstrap, args.seed
    )
    mem_trace.append(report_memory("metric computed"))

    facts = {
        "run_at": run_at,
        "policyengine_version": getattr(policyengine_us, "__version__", "unknown"),
        "dataset_name": dataset.name,
        "n_records": len(weights),
        "weighted_population": float(weights.sum()),
        "baseline_wage": mechanism["baseline"]["minimum_wage"],
        "reform_wage": mechanism["reform"]["minimum_wage"],
        "baseline_bar": base_bar,
        "reform_bar": reform_bar,
        "in_band_weighted": in_band_weighted,
        "exposed": exposed,
        "sigma_sampling": sigma_sampling,
        "sigma_scope": exposed * 0.25,
        "mechanism": mechanism,
        "memory_trace": mem_trace,
        "peak_commit_mb": max((m.get("commit_mb", 0) for m in mem_trace), default=0),
    }
    facts["sigma_total"] = float(np.hypot(facts["sigma_sampling"], facts["sigma_scope"]))

    cell = build_cell(args, facts)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps([cell], indent=1), encoding="utf-8")
    print(f"wrote draft cell -> {args.out}")

    run_json = args.run_json or args.out.with_name(args.out.stem + ".run.json")
    run_json.write_text(
        json.dumps(
            {
                "reform": {
                    "parameter": args.parameter,
                    "value": args.value,
                    "period": args.period,
                },
                "metric": args.metric,
                "facts": facts,
            },
            indent=1,
            default=str,
        ),
        encoding="utf-8",
    )
    print(f"wrote run record -> {run_json}")
    print(
        json.dumps(
            {
                "exposed_millions": round(exposed / 1e6, 3),
                "point": cell["pointEstimate"],
                "ciLow": cell["ciLow"],
                "ciHigh": cell["ciHigh"],
                "peak_commit_mb": round(facts["peak_commit_mb"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
