"""Weighted population counts for ONE PolicyEngine variable under a reform,
run on Modal against a pinned Populace build — THROUGH the audited wrapper
(scripts/tools/policyengine.py).

Why this exists separately from modal_economy.py: some reforms reach an outcome
through a threshold rather than through the budget. Raising
``gov.dol.minimum_wage`` moves no dollars in a static model; it moves the income
bar inside ``medicaid_work_requirement_eligible``. app-v2 economy metrics cannot
see that, so the metric here is the variable itself, counted by the engine under
both arms.

Why Modal: a national PolicyEngine microsim OOMs a 16 GB laptop (every state's
EITC spawns a population branch-clone), and the certified stack for build P is
older than whatever is on the dev box. A 32 GB container with the certified
pins installed is the only place this number legitimately exists.

The counting rule (the part that must not be reimplemented by hand): weights
come off the MicroSeries the engine returns, never off the HDF5. A mask applied
to a raw ``weight`` column reproduces neither the variable's logic nor its
entity mapping — that is a spreadsheet wearing PolicyEngine's name.

Run:
    modal run scripts/tools/modal_population.py
    modal run scripts/tools/modal_population.py --value 17.0 --year 2027
(set PYTHONIOENCODING=utf-8 on Windows or the Modal CLI's checkmark crashes cp1252)

Output paths are __file__-anchored, never cwd-relative, and the full result JSON
prints before any file write — stdout is the recovery path.
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

DEFAULT_PARAMETER = "gov.dol.minimum_wage"
DEFAULT_VARIABLE = "medicaid_work_requirement_eligible"


def _drafts_dir() -> Path:
    # Resolved LAZILY at the local entrypoint only — the Modal container mounts
    # this file at a shallow path where .parents[2] raises IndexError at import.
    return Path(__file__).resolve().parents[2] / "drafts" / "pe-reform"


def minimum_wage_reform(value: float, year: int) -> dict:
    return {DEFAULT_PARAMETER: {f"{year}-01-01.{year}-12-31": value}}


image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        f"policyengine-us=={PE_US}",
        f"policyengine-core=={PE_CORE}",
        "microdf-python",
        "huggingface-hub",
    )
)

app = modal.App("thesis-population-buildp")


@app.function(image=image, memory=32768, timeout=3600, cpu=4.0)
def population(
    reform: dict,
    year: int,
    variable: str,
    map_to: str = "person",
    bootstrap: int = 400,
    seed: int = 0,
) -> dict:
    import warnings

    warnings.filterwarnings("ignore")
    import gc

    import numpy as np
    from policyengine_core.reforms import Reform
    from policyengine_us import Microsimulation

    def arm(sim):
        series = sim.calculate(variable, period=year, map_to=map_to)
        weights = getattr(series, "weights", None)
        if weights is None:
            raise RuntimeError(
                f"{variable} came back unweighted from the engine "
                f"(map_to={map_to!r}); refusing to substitute raw dataset weights"
            )
        return np.asarray(series.values), np.asarray(weights, dtype=float)

    def sigma(contrib, clusters):
        # Households are the survey's sampling unit; persons inside one share a
        # weight and are not independent draws. Inlined rather than imported:
        # the container mounts this file alone, not the repo.
        order = np.argsort(clusters, kind="stable")
        per_cluster = np.add.reduceat(
            np.asarray(contrib, dtype=float)[order],
            np.concatenate(([0], np.flatnonzero(np.diff(clusters[order])) + 1)),
        )
        n = len(per_cluster)
        if n < 2:
            return 0.0
        idx = np.random.default_rng(seed).integers(0, n, size=(bootstrap, n))
        return float(per_cluster[idx].sum(axis=1).std(ddof=1))

    base_sim = Microsimulation(dataset=DATASET)
    base_vals, weights = arm(base_sim)
    clusters = np.asarray(base_sim.calculate("household_id", period=year, map_to=map_to))
    del base_sim
    gc.collect()  # drop the baseline sim before building the reform arm
    ref_vals, _ = arm(
        Microsimulation(dataset=DATASET, reform=Reform.from_dict(reform, country_id="us"))
    )
    gc.collect()

    if base_vals.shape != ref_vals.shape:
        raise RuntimeError(
            f"arms disagree on record count ({base_vals.shape} vs {ref_vals.shape})"
        )

    base_true, ref_true = base_vals.astype(bool), ref_vals.astype(bool)
    return {
        "engine": "modal",
        "dataset": BUILD_P,
        "pe_us_version": PE_US,
        "pe_core_version": PE_CORE,
        "year": year,
        "reform": reform,
        "variable": variable,
        "entity": map_to,
        "records": int(base_true.size),
        "weighted_population": float(weights.sum()),
        "baseline_true_weighted": float(weights[base_true].sum()),
        "reform_true_weighted": float(weights[ref_true].sum()),
        # Both transitions, kept separate — a net change hides a reform that
        # moves people both ways, and the direction is the whole finding here.
        "became_false_weighted": float(weights[base_true & ~ref_true].sum()),
        "became_true_weighted": float(weights[~base_true & ref_true].sum()),
        "became_false_sigma": sigma(weights * (base_true & ~ref_true), clusters),
        "bootstrap_draws": bootstrap,
        "bootstrap_seed": seed,
    }


# --------------------------------------------------------------------------- #
# Wrapper routing at the entrypoint                                            #
# --------------------------------------------------------------------------- #
def _wrapper():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import policyengine as pe  # the audited call path (issue #45)

    return pe


def _record(pe, v, result: dict) -> "object":
    """Register the remote result in the wrapper's audit trail as an EconomyRun,
    so a Modal number and a local number are the same artifact to an auditor."""
    from datetime import datetime, timezone

    impact = {k: result[k] for k in (
        "variable", "entity", "records", "weighted_population",
        "baseline_true_weighted", "reform_true_weighted",
        "became_false_weighted", "became_true_weighted",
        "became_false_sigma", "bootstrap_draws", "bootstrap_seed",
    )}
    impact["net_change_weighted"] = (
        impact["reform_true_weighted"] - impact["baseline_true_weighted"]
    )
    run = pe.EconomyRun(
        "ok", result["year"], "us", "us", result["reform"], None, pe.baseline_id("us"),
        impact=impact, message="ok", engine="modal", dataset=result["dataset"],
        pe_us_version=result["pe_us_version"], param_source=v.param_source,
        checked_existence=v.checked_existence, variable=result["variable"],
        certification=pe.certification_note(result["dataset"], result["pe_us_version"]),
        computed_at=datetime.now(timezone.utc).isoformat(),
    )
    pe._log_call(run, pe.DEFAULT_LOG_DIR)
    return run


@app.local_entrypoint()
def main(value: float = 15.0, year: int = 2027, variable: str = DEFAULT_VARIABLE):
    pe = _wrapper()
    reform = minimum_wage_reform(value, year)

    # Both gates BEFORE a container starts: an uncertified pairing or an
    # unvalidated reform must not reach paid compute, let alone a slide.
    v = pe.validate_reform(reform)
    if not v.ok:
        raise SystemExit("reform failed validation:\n  - " + "\n  - ".join(v.problems))
    print(f"validated [{v.param_source}] checked_existence={v.checked_existence}")
    try:
        cert = pe.require_certification(BUILD_P, PE_US)
    except pe.UncertifiedPairing as exc:
        raise SystemExit(f"refusing to run: {exc}")
    print(f"certified {cert['certified_model_version']} against {BUILD_P}")

    result = population.remote(reform, year, variable)
    print(json.dumps(result, indent=2))

    run = _record(pe, v, result)
    out_dir = _drafts_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"buildP-population-{variable}-{year}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"wrote {path}")
    print(
        f"{result['became_false_weighted'] / 1e6:,.3f}M lost {variable}; "
        f"{result['became_true_weighted'] / 1e6:,.3f}M gained it "
        f"(certified={run.certification['certified']})"
    )
