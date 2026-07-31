"""The reform -> draft cell loop (#65), after the certification fix.

Two properties carry this file. First, the loop cannot write outside ``drafts/``
— a draft that can land in ``examples/`` is a draft that gets cited as one.
Second, it cannot emit a cell from an uncertified or unfinished run, because the
figure it would carry was never priced by PolicyEngine. The last test is a
regression guard on the original defect: the population count must not be
recoverable by reading the dataset's weight column.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "tools"))

pytest.importorskip("numpy", reason="the cell builder derives its interval with numpy")
cell_mod = importlib.import_module("pe_reform_cell")
pe = importlib.import_module("policyengine")

CERTIFIED = {
    "build": "populace-us-2024-buildp-test",
    "certified_model_version": "1.764.6",
    "running_model_version": "1.764.6",
    "certified": True,
    "warning": None,
}
UNCERTIFIED = {
    "build": "populace-us-2024-buildp-test",
    "certified_model_version": "1.764.6",
    "running_model_version": "1.784.3",
    "certified": False,
    "warning": "UNCERTIFIED PAIRING: build certifies policyengine-us==1.764.6, running 1.784.3.",
}


def artifact(**overrides) -> dict:
    base = {
        "engine": "modal",
        "dataset": "populace-us-2024-buildp-test",
        "pe_us_version": "1.764.6",
        "year": 2027,
        "variable": "medicaid_work_requirement_eligible",
        "entity": "person",
        "records": 1_200_000,
        "weighted_population": 331_000_000.0,
        "baseline_true_weighted": 21_000_000.0,
        "reform_true_weighted": 17_500_000.0,
        "became_false_weighted": 3_600_000.0,
        "became_true_weighted": 100_000.0,
        "became_false_sigma": 164_000.0,
        "bootstrap_draws": 400,
        "bootstrap_seed": 20260731,
    }
    base.update(overrides)
    return base


# --------------------------------------------------------------------------- #
# drafts confinement                                                           #
# --------------------------------------------------------------------------- #
def test_paths_under_drafts_are_accepted():
    target = cell_mod.DRAFTS_ROOT / "pe-reform" / "cell.json"
    assert cell_mod.in_drafts(target) == target.resolve()


def test_nested_paths_under_drafts_are_accepted():
    target = cell_mod.DRAFTS_ROOT / "a" / "b" / "c.json"
    assert cell_mod.in_drafts(target) == target.resolve()


@pytest.mark.parametrize(
    "relative",
    [
        "examples/pe-reform/cell.json",
        "site/src/data/forecast-examples/cell.ts",
        "draft_cells.json",
        "records/targets/cell.json",
    ],
)
def test_paths_outside_drafts_are_refused(relative):
    with pytest.raises(SystemExit) as excinfo:
        cell_mod.in_drafts(ROOT / relative)
    assert "drafts only" in str(excinfo.value)


def test_traversal_out_of_drafts_is_refused():
    with pytest.raises(SystemExit):
        cell_mod.in_drafts(cell_mod.DRAFTS_ROOT / ".." / "examples" / "cell.json")


def test_a_sibling_named_like_drafts_is_not_drafts():
    with pytest.raises(SystemExit):
        cell_mod.in_drafts(cell_mod.DRAFTS_ROOT.parent / "drafts-published" / "cell.json")


# --------------------------------------------------------------------------- #
# the emission gate                                                            #
# --------------------------------------------------------------------------- #
def test_certified_run_passes_the_gate():
    assert cell_mod.require_certified({"certification": CERTIFIED}) is CERTIFIED


def test_uncertified_run_emits_nothing():
    with pytest.raises(SystemExit) as excinfo:
        cell_mod.require_certified({"certification": UNCERTIFIED})
    assert "refusing to emit a cell" in str(excinfo.value)
    assert "UNCERTIFIED PAIRING" in str(excinfo.value)


def test_missing_certification_emits_nothing():
    """Absence of a verdict is not a pass."""
    with pytest.raises(SystemExit) as excinfo:
        cell_mod.require_certified({})
    assert "refusing to emit a cell" in str(excinfo.value)


def test_refused_population_run_stops_the_loop(monkeypatch):
    refused = pe.EconomyRun(
        "error", 2027, "us", "us", {}, None, 2, engine="local",
        dataset="build", message="UNCERTIFIED PAIRING: ...",
    )
    monkeypatch.setattr(pe, "population_impact_local", lambda *a, **k: refused)
    args = cell_mod.parse_args([])
    with pytest.raises(SystemExit) as excinfo:
        cell_mod.population_run(args)
    assert "Emitting nothing" in str(excinfo.value)


# --------------------------------------------------------------------------- #
# recorded run artifacts are data, not authorities                             #
# --------------------------------------------------------------------------- #
def test_recorded_run_is_recertified_from_its_own_pairing(tmp_path, monkeypatch):
    """An artifact asserting its own innocence does not get to."""
    monkeypatch.setattr(pe, "certified_model_version", lambda build=None: "1.764.6")
    path = tmp_path / "run.json"
    path.write_text(json.dumps(artifact(pe_us_version="1.784.3", certified=True)), encoding="utf-8")

    recorded = cell_mod.load_recorded_run(path)

    assert recorded["certification"]["certified"] is False
    with pytest.raises(SystemExit):
        cell_mod.require_certified(recorded)


def test_recorded_run_certifies_on_a_matching_pairing(tmp_path, monkeypatch):
    monkeypatch.setattr(pe, "certified_model_version", lambda build=None: "1.764.6")
    path = tmp_path / "run.json"
    path.write_text(json.dumps(artifact()), encoding="utf-8")

    recorded = cell_mod.load_recorded_run(path)

    assert recorded["certification"]["certified"] is True
    assert recorded["engine"] == "modal"


def test_non_artifact_json_is_refused(tmp_path):
    path = tmp_path / "run.json"
    path.write_text(json.dumps({"exposed_millions": 4.49}), encoding="utf-8")
    with pytest.raises(SystemExit) as excinfo:
        cell_mod.load_recorded_run(path)
    assert "not a population run artifact" in str(excinfo.value)


@pytest.mark.parametrize("dropped", ["became_false_sigma", "weighted_population", "dataset"])
def test_artifact_missing_a_required_field_is_refused(tmp_path, dropped):
    payload = artifact()
    del payload[dropped]
    path = tmp_path / "run.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(SystemExit) as excinfo:
        cell_mod.load_recorded_run(path)
    assert dropped in str(excinfo.value)


# --------------------------------------------------------------------------- #
# the cell the loop builds                                                     #
# --------------------------------------------------------------------------- #
def synthetic_facts() -> dict:
    a = artifact()
    exposed = a["became_false_weighted"]
    sigma_sampling = a["became_false_sigma"]
    sigma_drift = exposed * 0.25
    import numpy as np

    return {
        "run_at": "2026-07-31T18:00:00Z",
        "engine": "modal",
        "policyengine_version": "1.764.6",
        "dataset": a["dataset"],
        "certification": CERTIFIED,
        "entity": "person",
        "records": a["records"],
        "weighted_population": a["weighted_population"],
        "baseline_wage": 7.25,
        "reform_wage": 15.0,
        "baseline_bar": 6960.0,
        "reform_bar": 14400.0,
        "baseline_true": a["baseline_true_weighted"],
        "reform_true": a["reform_true_weighted"],
        "net_change": a["reform_true_weighted"] - a["baseline_true_weighted"],
        "became_true": a["became_true_weighted"],
        "exposed": exposed,
        "sigma_sampling": sigma_sampling,
        "sigma_drift": sigma_drift,
        "drift_sigma_frac": 0.25,
        "bootstrap_draws": 400,
        "bootstrap_seed": 20260731,
        "mechanism": {
            "earnings": [3_000, 10_000, 20_000],
            "baseline": {"minimum_wage": 7.25, "annual_bar": 6960.0,
                         "eligible": [False, True, True]},
            "reform": {"minimum_wage": 15.0, "annual_bar": 14400.0,
                       "eligible": [False, False, True]},
            "flipped": [False, True, False],
        },
        "memory_trace": [],
        "peak_commit_mb": 0,
        "sigma_total": float(np.hypot(sigma_sampling, sigma_drift)),
    }


@pytest.fixture
def built_cell():
    return cell_mod.build_cell(cell_mod.parse_args([]), synthetic_facts())


def test_cell_point_and_interval_are_derived_from_the_run(built_cell):
    assert built_cell["pointEstimate"] == 3.60
    assert built_cell["ciLow"] < built_cell["pointEstimate"] < built_cell["ciHigh"]
    assert built_cell["confidence"] == 0.8


def test_cell_meets_the_trace_depth_rubric(built_cell):
    steps = built_cell["reasoning"]
    assert len(steps) >= 7
    assert sum(1 for s in steps if s["kind"] == "tool") >= 3
    assert any(s["kind"] == "math" for s in steps)
    assert any(s["kind"] == "forecast" for s in steps)


def test_math_step_shows_the_80_percent_multiplier(built_cell):
    math = next(s for s in built_cell["reasoning"] if s["kind"] == "math")
    assert "1.28" in math["text"]
    assert "sqrt(" in math["text"]


def test_math_step_names_the_drift_term_as_the_weak_input(built_cell):
    """The old cell asserted a 25% scope sigma with no provenance."""
    math = next(s for s in built_cell["reasoning"] if s["kind"] == "math")
    assert "weakest input" in math["text"]
    assert "build O to build P" in math["text"]


def test_cell_credits_the_engine_with_the_exemptions(built_cell):
    """The proxy-rule cell called itself an upper bound because it dropped them."""
    blob = json.dumps(built_cell)
    assert "applied by the engine rather than approximated here" in blob
    assert "upper bound" not in blob


def test_tool_steps_name_the_microsimulation_not_the_microdata(built_cell):
    tools = [s["tool"] for s in built_cell["reasoning"] if s["kind"] == "tool"]
    assert "policyengine.microsimulation" in tools
    assert "policyengine.microdata" not in tools


def test_resolution_rule_resolves_by_rerunning_the_engine(built_cell):
    rule = built_cell["resolutionRule"]
    assert "national microsimulation" in rule
    assert "weights the engine returns" in rule
    assert "certifies" in rule
    # The hand-written screens the old rule published as the resolution contract.
    assert "imputed monthly hours" not in rule
    assert "full-time students" not in rule


def test_cell_records_the_pairing_it_was_priced_on(built_cell):
    rule = built_cell["resolutionRule"]
    assert "1.764.6" in rule
    assert "populace-us-2024-buildp-test" in rule


# --------------------------------------------------------------------------- #
# regression: the raw-weights path must not come back                          #
# --------------------------------------------------------------------------- #
def test_the_loop_cannot_read_the_dataset_directly():
    """The original defect, pinned shut.

    4.49M was produced by h5py-ing the Populace file, reading its ``weight``
    column and multiplying by a hand-written approximation of the variable.
    Nothing in this module may do that again.
    """
    source = (ROOT / "scripts" / "pe_reform_cell.py").read_text(encoding="utf-8")
    code = "\n".join(
        line for line in source.splitlines() if not line.strip().startswith("#")
    )
    body = code.split('"""', 2)[-1]  # drop the module docstring, which discusses it
    for banned in ("h5py", "populace_us_", '["weight"]', "huggingface"):
        assert banned not in body, f"{banned!r} is back in the population path"


def test_the_loop_routes_through_the_audited_wrapper():
    source = (ROOT / "scripts" / "pe_reform_cell.py").read_text(encoding="utf-8")
    assert "import policyengine as pe" in source
    assert "pe.population_impact_local" in source
    assert "require_certified" in source
