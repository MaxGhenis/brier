#!/usr/bin/env python3
"""Minimal reform -> PolicyEngine -> outcome metric -> draft forecast cell.

The smallest end-to-end path through the lab for a *policy* target: change ONE
PolicyEngine-US parameter, have the engine recompute a population outcome under
baseline and reform, size an 80% interval from the run itself, and emit a draft
cell that satisfies docs/cell-contract.md.

Worked example (the defaults): raise the federal minimum wage
(``gov.dol.minimum_wage``) from $7.25 to $15.00 and measure how many people lose
``medicaid_work_requirement_eligible`` in 2027.

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

HOW THE NUMBER IS PRODUCED (and how it used to be, which was wrong).
An earlier revision of this script counted the exposed population by opening the
Populace HDF5 with h5py, reading the ``weight`` column, and multiplying it by a
hand-written approximation of the variable's rule — an income band, an imputed
hours proxy, and two of the variable's many exemptions. That is not a
PolicyEngine number. It reproduces neither the variable's logic nor its entity
mapping, it silently drops every exemption the columns cannot see, and it is
unfalsifiable against the model it claims to be running. House doctrine: never
touch the weights directly, always go through the microsimulation.

Both stages now run through the audited wrapper (``scripts/tools/policyengine.py``,
POLICYENGINE.md):

  Stage 1 (mechanism)   A tiny Simulation over synthetic households runs the real
                        Reform through the real variable and shows the eligibility
                        flip. No dataset, so no certification question; it proves
                        the parameter reaches the outcome, nothing more.
  Stage 2 (population)  ``pe.population_impact_local`` (or a Modal run recorded by
                        ``scripts/tools/modal_population.py``) has the ENGINE
                        compute the variable under both arms on a pinned Populace
                        build, and counts transitions with the engine's own
                        weights.

Stage 2 is certification-gated and fail-closed. A national microsim needs a
big-memory box and the build's certified model version; on anything else this
script refuses and emits nothing rather than producing a figure that was never
priced by PolicyEngine.

Usage:
    python scripts/pe_reform_cell.py                        # local certified run
    modal run scripts/tools/modal_population.py             # produce a run artifact
    python scripts/pe_reform_cell.py --from-run drafts/pe-reform/<artifact>.json

Output is confined to drafts/ — this loop stops at a draft cell and never
publishes: the converter requires a custody envelope that only a recorded
run_thesis_analyst.py agent run legitimately produces.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "tools"))
import policyengine as pe  # noqa: E402  the audited call path (issue #45)

ROOT = pathlib.Path(__file__).resolve().parents[1]
# Everything this loop writes lands here. The result is a draft, not a
# publication: it has no custody envelope, no recorded agent run and no
# pre-registration, so it must not sit anywhere that reads as blessed output.
DRAFTS_ROOT = ROOT / "drafts"

# 80% interval => +/- 1.28 sigma. Named because the contract's validator greps
# the math step for this multiplier.
Z_80 = 1.28

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
    p.add_argument(
        "--out",
        type=pathlib.Path,
        default=DRAFTS_ROOT / "pe-reform" / "minwage-15-draft-cell.json",
        help="draft cell path; must be under drafts/",
    )
    p.add_argument("--run-json", type=pathlib.Path, default=None)
    p.add_argument(
        "--from-run",
        type=pathlib.Path,
        default=None,
        help="consume a recorded run artifact (e.g. from modal_population.py) "
        "instead of computing locally",
    )
    p.add_argument("--build", default=pe.POPULACE_BUILD)
    p.add_argument("--bootstrap", type=int, default=400)
    p.add_argument("--seed", type=int, default=20260731)
    p.add_argument(
        "--drift-sigma-frac",
        type=float,
        default=0.25,
        help="model/dataset drift sigma as a fraction of the point estimate; "
        "see the math step for what this is and why it is the weak input",
    )
    p.add_argument(
        "--slug",
        default="us-adults-losing-medicaid-work-requirement-eligibility-2027",
    )
    return p.parse_args(argv)


def in_drafts(path: pathlib.Path) -> pathlib.Path:
    """Resolve ``path`` and refuse anything outside drafts/.

    A draft that can be written to examples/ is a draft that ends up cited as an
    example. The confinement is enforced here rather than left to the caller's
    ``--out``, because the caller is usually a shell history line.
    """
    resolved = (path if path.is_absolute() else pathlib.Path.cwd() / path).resolve()
    try:
        resolved.relative_to(DRAFTS_ROOT.resolve())
    except ValueError:
        raise SystemExit(
            f"refusing to write {resolved}: this loop emits drafts only, and "
            f"drafts live under {DRAFTS_ROOT}"
        )
    return resolved


def report_memory(stage: str) -> dict:
    """Print commit + free RAM for a stage.

    Working set is the misleading metric here: once Windows starts paging, RSS
    *falls* while the process is actually in trouble. Commit (private bytes) is
    what tracks real demand, so that is what gets printed.
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
    return {"stage": stage, "commit_mb": commit_mb, "free_mb": free_mb}


def reform_dict(args) -> dict:
    return {args.parameter: {f"{args.period}-01-01.{args.period}-12-31": args.value}}


# --------------------------------------------------------------------------
# Stage 1: mechanism. Real Reform, real variable, a handful of households.
# --------------------------------------------------------------------------


def run_mechanism_check(args) -> dict:
    """Household point-check: does the parameter reach the outcome at all?

    No dataset is involved, so this is the one leg with no certification
    question (POLICYENGINE.md 0.1: household checks are fast and datasetless).
    It cannot produce a population number and is not asked to.
    """
    from policyengine_core.reforms import Reform
    from policyengine_us import Simulation

    year = str(args.period)
    reform = Reform.from_dict(reform_dict(args), country_id="us")

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
# Stage 2: population, computed BY the engine on a pinned build.
# --------------------------------------------------------------------------

RUN_ARTIFACT_KEYS = {
    "variable",
    "dataset",
    "pe_us_version",
    "records",
    "weighted_population",
    "baseline_true_weighted",
    "reform_true_weighted",
    "became_false_weighted",
    "became_true_weighted",
    "became_false_sigma",
}


def load_recorded_run(path: pathlib.Path) -> dict:
    """Adapt a modal_population.py artifact to the shape the cell builder wants."""
    result = json.loads(path.read_text(encoding="utf-8"))
    missing = RUN_ARTIFACT_KEYS - set(result)
    if missing:
        raise SystemExit(
            f"{path} is not a population run artifact (missing {sorted(missing)})"
        )
    # Re-derive certification from the artifact's own recorded pairing rather
    # than trusting a flag inside it: the artifact is data, not an authority.
    return {
        "result": result,
        "certification": pe.certification_note(result["dataset"], result["pe_us_version"]),
        "engine": result.get("engine", "modal"),
    }


def population_run(args) -> dict:
    if args.from_run:
        return load_recorded_run(args.from_run)

    run = pe.population_impact_local(
        reform_dict(args),
        year=args.period,
        variable=args.metric,
        build=args.build,
        bootstrap=args.bootstrap,
        seed=args.seed,
    )
    if run.status != "ok":
        raise SystemExit(
            f"population run did not complete ({run.status}): {run.message}\n"
            "Emitting nothing - a cell built on a refused run would carry a "
            "number PolicyEngine never produced."
        )
    return {
        "result": {
            **run.impact,
            "dataset": run.dataset,
            "pe_us_version": run.pe_us_version,
        },
        "certification": run.certification,
        "engine": run.engine,
    }


def require_certified(recorded: dict) -> dict:
    """The last gate before a number becomes a quotable cell."""
    cert = recorded.get("certification") or {}
    if not cert.get("certified"):
        raise SystemExit(
            f"refusing to emit a cell: {cert.get('warning', 'certification missing')}\n"
            "A quotable figure must come from a model version the data build "
            "certifies. Install the certified stack "
            "(scripts/tools/requirements-tax.txt) or use the Modal path "
            "(scripts/tools/modal_population.py)."
        )
    return cert


# --------------------------------------------------------------------------
# Cell
# --------------------------------------------------------------------------


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
    flipped_at = [e for e, f in zip(mech["earnings"], mech["flipped"]) if f]

    reasoning = [
        {
            "kind": "heading",
            "text": (
                f"US people losing {args.metric} in {args.period} under a "
                f"${args.value:.2f} federal minimum wage"
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
                "Mechanism point-check: ran the real Reform through the real "
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
            "tool": "policyengine.microsimulation",
            "call": (
                "Ran the national microsimulation on Populace build "
                f"{facts['dataset']} under baseline and reform with "
                f"policyengine-us {facts['policyengine_version']} (a pairing the "
                "build certifies), and had the engine compute "
                f"{args.metric} for all {facts['records']:,} "
                f"{facts['entity']} records in each arm."
            ),
            "result": (
                f"Weighted population {facts['weighted_population'] / 1e6:,.1f} "
                f"million. Baseline eligibility "
                f"{facts['baseline_true'] / 1e6:,.2f} million, reform "
                f"{facts['reform_true'] / 1e6:,.2f} million — a net change of "
                f"{facts['net_change'] / 1e6:+,.2f} million."
            ),
        },
        {
            "kind": "tool",
            "tool": "policyengine.microsimulation",
            "call": (
                "Counted the per-record transitions between the two arms using "
                "the weights the engine returned with the variable, never the "
                "dataset's raw weight column."
            ),
            "result": (
                f"{facts['exposed']:,.0f} people ({point:.2f} million) hold the "
                "eligibility at baseline and lose it under the reform; "
                f"{facts['became_true'] / 1e6:,.2f} million move the other way. "
                "Every exemption the variable encodes — pregnancy, caretakers "
                "of children 13 and under, the medically frail, AIAN members, "
                "veterans, former foster youth, Medicare enrollees — is applied "
                "by the engine rather than approximated here."
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
                f"Point = {point:.2f} million losing eligibility. "
                f"sigma_sampling = {facts['sigma_sampling'] / 1e6:.3f}M from a "
                f"{facts['bootstrap_draws']}-draw household-clustered bootstrap "
                "of the weighted transition count, resampling households "
                "because persons inside one share a survey weight. "
                f"sigma_drift = {facts['sigma_drift'] / 1e6:.3f}M "
                f"({args.drift_sigma_frac:.0%} of the point), covering model and "
                "dataset movement between now and resolution, since this "
                "resolves against the then-current release rather than a pinned "
                "one. That fraction is the weakest input in this cell: the only "
                "in-repo measurement of build-to-build drift is the build O to "
                "build P refresh, which moved a comparable static-microsim "
                "budget line by +14% while roughly tripling its child-poverty "
                "line, so one figure is being asked to cover a two-order spread "
                "and is chosen wide on purpose. Combining independently: "
                f"sigma = sqrt({facts['sigma_sampling'] / 1e6:.3f}^2 + "
                f"{facts['sigma_drift'] / 1e6:.3f}^2) = {sigma_m:.3f}M. "
                f"80% interval = {point:.2f} +/- 1.28 * {sigma_m:.3f} = "
                f"[{ci_low:.2f}, {ci_high:.2f}] million."
            ),
        },
        {
            "kind": "text",
            "text": (
                "What would land outside the interval: the count is exact given "
                "this model and this build, so error comes from what changes "
                "before resolution rather than from what the run approximated. "
                "A Populace rebuild that reweights the low-earnings tail moves "
                "it most; a policyengine-us release that revises the work "
                "requirement's exemptions or its income route moves it "
                "discontinuously and in either direction. A resolver pinning "
                "the build used here would instead find this number "
                "reproducible to the record."
            ),
        },
        {"kind": "forecast", "point": point, "ciLow": ci_low, "ciHigh": ci_high},
    ]

    return {
        "slug": args.slug,
        "country": "US",
        "type": "policy",
        "title": (
            f"US people losing Medicaid work-requirement eligibility, "
            f"{args.period}, ${args.value:.0f} minimum wage"
        ),
        "question": (
            "Under a counterfactual in which the federal minimum wage "
            f"(gov.dol.minimum_wage) is ${args.value:.2f} for {args.period}, how "
            f"many US people hold {args.metric} under current law and lose it "
            "under the reform, in millions?"
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
            "available on the resolution date, paired with the Populace build "
            "that release certifies. Apply the single-parameter reform "
            f"{args.parameter} = {args.value:.2f} for {args.period}. Run the "
            "national microsimulation under both arms, have the engine compute "
            f"{args.metric} per {facts['entity']}, and report the weighted count "
            "of records true under baseline and false under reform, using the "
            "weights the engine returns with the variable. Report in millions "
            "to 2 decimals. The forecast is against the THEN-CURRENT certified "
            "pairing, not a pinned one: model and dataset drift are part of "
            "what is forecast. Baseline was policyengine-us "
            f"{facts['policyengine_version']} on {facts['dataset']}."
        ),
        "dataPointId": (
            f"policyengine.us.medicaid_work_requirement_lost.{args.period}."
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
            "Resolution is against the then-current certified pairing, so model and data drift are forecast too",
        ],
        "sourceContext": SOURCE_CONTEXT,
        "runAt": facts["run_at"],
        "reasoning": reasoning,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    out_path = in_drafts(args.out)
    run_json = in_drafts(args.run_json) if args.run_json else out_path.with_name(
        out_path.stem + ".run.json"
    )
    mem_trace = [report_memory("start")]

    try:
        import policyengine_us  # noqa: F401
    except ImportError as exc:
        print(f"policyengine-us is not importable: {exc}", file=sys.stderr)
        return 2

    run_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    print("stage 1: mechanism point-check (real reform, real variable)...", file=sys.stderr)
    mechanism = run_mechanism_check(args)
    mem_trace.append(report_memory("mechanism checked"))
    if not any(mechanism["flipped"]):
        print(
            "mechanism check found no eligibility flip — the parameter does not "
            "propagate to the metric; refusing to emit a cell",
            file=sys.stderr,
        )
        return 3

    print("stage 2: national microsimulation through the engine...", file=sys.stderr)
    recorded = population_run(args)
    certification = require_certified(recorded)
    result = recorded["result"]
    mem_trace.append(report_memory("population computed"))

    exposed = float(result["became_false_weighted"])
    sigma_sampling = float(result["became_false_sigma"])
    sigma_drift = exposed * args.drift_sigma_frac
    baseline_true = float(result["baseline_true_weighted"])
    reform_true = float(result["reform_true_weighted"])

    facts = {
        "run_at": run_at,
        "engine": recorded["engine"],
        "policyengine_version": result["pe_us_version"],
        "dataset": result["dataset"],
        "certification": certification,
        "entity": result.get("entity", "person"),
        "records": int(result["records"]),
        "weighted_population": float(result["weighted_population"]),
        "baseline_wage": mechanism["baseline"]["minimum_wage"],
        "reform_wage": mechanism["reform"]["minimum_wage"],
        "baseline_bar": mechanism["baseline"]["annual_bar"],
        "reform_bar": mechanism["reform"]["annual_bar"],
        "baseline_true": baseline_true,
        "reform_true": reform_true,
        "net_change": float(result.get("net_change_weighted", reform_true - baseline_true)),
        "became_true": float(result["became_true_weighted"]),
        "exposed": exposed,
        "sigma_sampling": sigma_sampling,
        "sigma_drift": sigma_drift,
        "drift_sigma_frac": args.drift_sigma_frac,
        "bootstrap_draws": int(result.get("bootstrap_draws", args.bootstrap)),
        "bootstrap_seed": int(result.get("bootstrap_seed", args.seed)),
        "mechanism": mechanism,
        "memory_trace": mem_trace,
        "peak_commit_mb": max((m.get("commit_mb", 0) for m in mem_trace), default=0),
    }
    facts["sigma_total"] = float(np.hypot(sigma_sampling, sigma_drift))

    cell = build_cell(args, facts)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps([cell], indent=1), encoding="utf-8")
    print(f"wrote draft cell -> {out_path}")

    run_json.write_text(
        json.dumps(
            {
                "reform": reform_dict(args),
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
                "certified": certification.get("certified"),
                "peak_commit_mb": round(facts["peak_commit_mb"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
