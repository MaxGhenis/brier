"""Correctness tests for the PolicyEngine tool (issue #45).

Three tiers, so repo CI stays offline and fast:
  - offline: structural validation, result normalization, compute-block shape
    (parameter source is monkeypatched — no network, no model).
  - local-model: real parameter existence checks (skipped unless policyengine-us
    is importable, i.e. the `tax` group is installed).
  - live-API: policy creation + household calc (skipped unless PE_LIVE=1).
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "tools"))
pe = importlib.import_module("policyengine")

CTC_THRESHOLD = "gov.irs.credits.ctc.refundable.phase_in.threshold"
GOOD_REFORM = {CTC_THRESHOLD: {"2026-01-01.2100-12-31": 0}}


# --------------------------------------------------------------------------- #
# offline: validation is structural + existence, existence source mocked       #
# --------------------------------------------------------------------------- #
@pytest.fixture
def mock_params(monkeypatch):
    known = {CTC_THRESHOLD, "gov.irs.credits.eitc.max"}
    monkeypatch.setattr(pe, "known_parameters", lambda country="us": (known, "policyengine-us@test"))
    return known


def test_base_param_strips_bracket():
    assert pe._base_param("gov.irs.credits.eitc.max[0].amount") == "gov.irs.credits.eitc.max"
    assert pe._base_param("gov.irs.credits.ctc.refundable.phase_in.threshold") == CTC_THRESHOLD


def test_valid_reform_passes(mock_params):
    r = pe.validate_reform(GOOD_REFORM)
    assert r.ok and not [p for p in r.problems if not p.startswith("WARNING")]
    assert r.checked_existence and r.param_source == "policyengine-us@test"


def test_unknown_parameter_flagged(mock_params):
    r = pe.validate_reform({"gov.irs.credits.ctc.made_up": {"2026-01-01.2026-12-31": 1}})
    assert not r.ok
    assert any("unknown parameter" in p for p in r.problems)


def test_bad_date_and_string_value_flagged(mock_params):
    r = pe.validate_reform({CTC_THRESHOLD: {"2026": "lots"}})
    assert not r.ok
    assert any("bad date range" in p for p in r.problems)
    assert any("value must be number/bool" in p for p in r.problems)


def test_boolean_value_allowed(mock_params, monkeypatch):
    monkeypatch.setattr(pe, "known_parameters",
                        lambda country="us": ({"gov.contrib.x.in_effect"}, "policyengine-us@test"))
    r = pe.validate_reform({"gov.contrib.x.in_effect": {"2026-01-01.2100-12-31": True}})
    assert r.ok


def test_empty_reform_rejected():
    assert not pe.validate_reform({}).ok


def test_structural_only_warns_when_source_unavailable(monkeypatch):
    monkeypatch.setattr(pe, "known_parameters", lambda country="us": (None, "structural-only"))
    r = pe.validate_reform(GOOD_REFORM)
    # structurally fine, but existence unverified -> ok True with a loud WARNING
    assert r.ok and not r.checked_existence
    assert any(p.startswith("WARNING") for p in r.problems)


# --------------------------------------------------------------------------- #
# offline: result normalization + compute block                                #
# --------------------------------------------------------------------------- #
RAW = {
    "budget": {"budgetary_impact": -1.6e9, "tax_revenue_impact": -1.6e9,
               "benefit_spending_impact": 0.0, "households": 1.3e8},
    "poverty": {
        "poverty": {"all": {"baseline": 0.10, "reform": 0.099},
                    "child": {"baseline": 0.20, "reform": 0.199}},
        "deep_poverty": {"child": {"baseline": 0.05, "reform": 0.0499}},
    },
    "decile": {"average": {str(i): i * 10.0 for i in range(1, 11)}, "relative": {}},
    "intra_decile": {"all": {"Gain more than 5%": 0.06}},
}


def test_normalize_economy_shape_and_pct_change():
    n = pe.normalize_economy(RAW)
    assert n["budgetary_impact"] == -1.6e9
    assert n["poverty"]["child"]["baseline"] == 0.20
    # -0.5% child poverty change from 0.20 -> 0.199
    assert n["poverty"]["child"]["pct_change"] == pytest.approx(-0.005, rel=1e-6)
    assert n["decile_average_change"]["10"] == 100.0
    assert n["winners_losers"] == {"Gain more than 5%": 0.06}


def test_normalize_tolerates_missing_keys():
    n = pe.normalize_economy({})  # empty result must not raise
    assert n["budgetary_impact"] is None
    assert n["poverty"]["child"]["pct_change"] is None


def test_compute_block_ok():
    run = pe.EconomyRun("ok", 2026, "us", "us", GOOD_REFORM, 85587, 2,
                        impact=pe.normalize_economy(RAW))
    block = pe.compute_block(run, provision_title="strike $2,500 -> $1")
    assert block["model"] == "policyengine-us"
    assert block["reform"] == GOOD_REFORM
    assert block["budgetary_impact"] == -1.6e9
    assert "budgetary impact" in block["result_summary"]
    assert block["provision_title"] == "strike $2,500 -> $1"


def test_compute_block_pending_widens():
    run = pe.EconomyRun("pending", 2026, "us", "us", GOOD_REFORM, 85587, 2,
                        message="still computing")
    block = pe.compute_block(run)
    assert block["status"] == "pending"
    assert "pending" in block["result_summary"]


# --------------------------------------------------------------------------- #
# local-model: real parameter existence (needs the certified stack)            #
# --------------------------------------------------------------------------- #
_HAS_MODEL = importlib.util.find_spec("policyengine_us") is not None
local_only = pytest.mark.skipif(not _HAS_MODEL, reason="policyengine-us not installed (see scripts/tools/requirements-tax.txt)")


@local_only
def test_local_parameters_include_ctc_threshold():
    params, source = pe.known_parameters("us")
    assert params is not None and CTC_THRESHOLD in params
    assert source.startswith("policyengine-us@")


@local_only
def test_real_reform_validates_and_garbage_fails():
    assert pe.validate_reform(GOOD_REFORM).ok
    assert not pe.validate_reform({"gov.irs.credits.ctc.not_real": {"2026-01-01.2026-12-31": 0}}).ok


# --------------------------------------------------------------------------- #
# live-API: policy + household (needs network; opt in with PE_LIVE=1)           #
# --------------------------------------------------------------------------- #
live_only = pytest.mark.skipif(not os.environ.get("PE_LIVE"), reason="set PE_LIVE=1 for live API tests")


@live_only
def test_create_policy_returns_id():
    pid = pe.create_policy(GOOD_REFORM, validate=True)
    assert isinstance(pid, int) and pid > 0


@live_only
def test_household_ctc_phase_in_point_check():
    # A single parent, 1 child, $2,000 earnings. Baseline CTC phase-in starts at
    # $2,500 of earnings, so refundable CTC is ~$0; striking the threshold to $0
    # phases in from the first dollar -> refundable CTC > baseline.
    hh = {
        "people": {"a": {"age": {"2026": 30}, "employment_income": {"2026": 2000}},
                   "c": {"age": {"2026": 4}}},
        # /calculate only returns variables present in the payload — request the
        # output by seeding it null.
        "tax_units": {"t": {"members": ["a", "c"], "refundable_ctc": {"2026": None}}},
        "spm_units": {"s": {"members": ["a", "c"]}},
        "households": {"h": {"members": ["a", "c"], "state_name": {"2026": "TX"}}},
    }
    base = pe.household_under(hh, None, baseline=True)
    reform = pe.household_under(hh, GOOD_REFORM)
    b = base["tax_units"]["t"]["refundable_ctc"]["2026"]
    r = reform["tax_units"]["t"]["refundable_ctc"]["2026"]
    assert r > b  # phasing in from the first dollar raises the refundable CTC
