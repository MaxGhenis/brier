"""The certification gate, and the engine-computed population path (#65 fix).

``certification_note`` already failed closed as a *report*, but a report binds
only a caller that reads it and it was consulted in exactly one place —
``compute_block``, i.e. after the number already existed. These tests pin the
gate as a gate: nothing that touches microdata may return a figure on an
uncertified pairing, and the population count must come off the engine's own
weighted series rather than the dataset's weight column.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "tools"))
pe = importlib.import_module("policyengine")

CTC_THRESHOLD = "gov.irs.credits.ctc.refundable.phase_in.threshold"
GOOD_REFORM = {CTC_THRESHOLD: {"2026-01-01.2100-12-31": 0}}
BUILD = "populace-us-2024-buildp-test"

# The tool is deliberately stdlib-only so plain `uv sync` stays fast; the array
# helpers import numpy lazily. CI runs --all-extras, so these run there.
requires_numpy = pytest.mark.skipif(
    importlib.util.find_spec("numpy") is None,
    reason="numpy lives in the experiments extra; the tool itself is stdlib-only",
)


@pytest.fixture
def params(monkeypatch):
    monkeypatch.setattr(
        pe, "known_parameters", lambda country="us": ({CTC_THRESHOLD}, "policyengine-us@test")
    )


@pytest.fixture
def certifies(monkeypatch):
    """Build certifies 1.764.6; the caller picks what is 'installed'."""
    monkeypatch.setattr(pe, "certified_model_version", lambda build=None: "1.764.6")

    def running(version):
        monkeypatch.setattr(pe, "policyengine_us_version", lambda: version)

    return running


# --------------------------------------------------------------------------- #
# require_certification — the gate itself                                      #
# --------------------------------------------------------------------------- #
def test_require_certification_passes_on_exact_match(certifies):
    certifies("1.764.6")
    note = pe.require_certification(BUILD, "1.764.6")
    assert note["certified"] is True
    assert note["warning"] is None


def test_require_certification_raises_on_mismatch(certifies):
    certifies("1.784.3")
    with pytest.raises(pe.UncertifiedPairing) as excinfo:
        pe.require_certification(BUILD, "1.784.3")
    assert "UNCERTIFIED PAIRING" in str(excinfo.value)
    # The refusal carries the structured note, so a caller can record WHY.
    assert excinfo.value.note["certified"] is False
    assert excinfo.value.note["certified_model_version"] == "1.764.6"


def test_require_certification_raises_when_manifest_unreachable(monkeypatch):
    monkeypatch.setattr(pe, "certified_model_version", lambda build=None: None)
    with pytest.raises(pe.UncertifiedPairing) as excinfo:
        pe.require_certification(BUILD, "1.764.6")
    assert "CANNOT CERTIFY" in str(excinfo.value)


def test_require_certification_raises_when_running_version_unknown(certifies):
    with pytest.raises(pe.UncertifiedPairing) as excinfo:
        pe.require_certification(BUILD, None)
    assert "CANNOT CERTIFY" in str(excinfo.value)


def test_uncertified_pairing_is_a_policyengine_error():
    assert issubclass(pe.UncertifiedPairing, pe.PolicyEngineError)


# --------------------------------------------------------------------------- #
# the gate is reached BEFORE the microdata                                     #
# --------------------------------------------------------------------------- #
def _explode_if_imported(monkeypatch):
    """Make any attempt to build a Microsimulation an unmistakable failure."""
    import builtins

    real_import = builtins.__import__

    def guard(name, *a, **kw):
        if name.startswith("policyengine_us"):
            raise AssertionError(f"reached the engine ({name}) on an uncertified pairing")
        return real_import(name, *a, **kw)

    monkeypatch.setattr(builtins, "__import__", guard)


def test_economy_local_refuses_before_touching_the_engine(params, certifies, monkeypatch, tmp_path):
    certifies("1.784.3")
    _explode_if_imported(monkeypatch)
    run = pe.economy_local(GOOD_REFORM, 2026, build=BUILD, log_dir=tmp_path)
    assert run.status == "error"
    assert "UNCERTIFIED PAIRING" in run.message
    assert run.impact == {}
    assert run.certification["certified"] is False


def test_population_local_refuses_before_touching_the_engine(
    params, certifies, monkeypatch, tmp_path
):
    certifies("1.784.3")
    _explode_if_imported(monkeypatch)
    run = pe.population_impact_local(
        GOOD_REFORM, 2027, "medicaid_work_requirement_eligible",
        build=BUILD, log_dir=tmp_path,
    )
    assert run.status == "error"
    assert "UNCERTIFIED PAIRING" in run.message
    assert run.impact == {}


def test_refused_run_is_still_written_to_the_audit_log(params, certifies, tmp_path):
    certifies("1.784.3")
    pe.population_impact_local(
        GOOD_REFORM, 2027, "medicaid_work_requirement_eligible",
        build=BUILD, log_dir=tmp_path,
    )
    logged = list(tmp_path.glob("*.json"))
    assert len(logged) == 1, "a refusal is a run that happened; it must be auditable"


def test_validation_failure_still_precedes_certification(params, certifies, tmp_path):
    """A bad reform is rejected on its own terms, not blamed on the pairing."""
    certifies("1.784.3")
    run = pe.population_impact_local(
        {"gov.not.a.real.parameter": {"2027-01-01.2027-12-31": 1}},
        2027, "medicaid_work_requirement_eligible", build=BUILD, log_dir=tmp_path,
    )
    assert run.status == "error"
    assert "failed validation" in run.message


# --------------------------------------------------------------------------- #
# compute_block prefers the verdict the run actually reached                   #
# --------------------------------------------------------------------------- #
def test_compute_block_uses_the_runs_recorded_certification(monkeypatch):
    # If the manifest moved after the run, recomputing here would certify a run
    # that was refused. The recorded verdict wins.
    monkeypatch.setattr(pe, "certified_model_version", lambda build=None: "1.999.9")
    recorded = {"build": BUILD, "certified_model_version": "1.764.6",
                "running_model_version": "1.764.6", "certified": True, "warning": None}
    run = pe.EconomyRun("ok", 2026, "us", "us", GOOD_REFORM, None, 2, engine="local",
                        dataset=BUILD, pe_us_version="1.764.6", certification=recorded)
    assert pe.compute_block(run)["certification"] is recorded


def test_compute_block_still_computes_when_the_run_recorded_nothing(monkeypatch):
    monkeypatch.setattr(pe, "certified_model_version", lambda build=None: "1.764.6")
    run = pe.EconomyRun("ok", 2026, "us", "us", GOOD_REFORM, None, 2, engine="modal",
                        dataset=BUILD, pe_us_version="1.764.6")
    assert pe.compute_block(run)["certification"]["certified"] is True


# --------------------------------------------------------------------------- #
# weights come off the engine, never the dataset                               #
# --------------------------------------------------------------------------- #
class _Series:
    def __init__(self, values, weights):
        self.values = values
        self.weights = weights


class _Sim:
    def __init__(self, series):
        self._series = series

    def calculate(self, variable, period=None, map_to=None):
        return self._series


@requires_numpy
def test_engine_series_takes_values_and_weights_from_the_engine():
    values, weights = pe._engine_series(
        _Sim(_Series([True, False], [10.0, 20.0])), "v", 2027, "person"
    )
    assert list(values) == [True, False]
    assert list(weights) == [10.0, 20.0]


@requires_numpy
def test_engine_series_refuses_an_unweighted_result():
    """The defect this replaces: reaching for the raw weight column instead."""
    with pytest.raises(pe.PolicyEngineError) as excinfo:
        pe._engine_series(_Sim(_Series([True], None)), "v", 2027, "person")
    assert "refusing to substitute raw dataset weights" in str(excinfo.value)


# --------------------------------------------------------------------------- #
# the bootstrap resamples households, not persons                              #
# --------------------------------------------------------------------------- #
@requires_numpy
def test_bootstrap_sigma_is_zero_without_variation():
    sigma = pe.cluster_bootstrap_sigma([5.0, 5.0, 5.0, 5.0], [1, 2, 3, 4], draws=50, seed=1)
    assert sigma == pytest.approx(0.0, abs=1e-9)


@requires_numpy
def test_bootstrap_sigma_is_positive_with_variation():
    contrib = [0.0] * 50 + [100.0] * 50
    clusters = list(range(100))
    assert pe.cluster_bootstrap_sigma(contrib, clusters, draws=200, seed=1) > 0


@requires_numpy
def test_bootstrap_clusters_persons_into_households():
    """Four persons in one household are one draw, not four.

    Clustering must widen the spread relative to treating persons as
    independent; if the two agreed, the clustering would not be doing anything.
    """
    contrib = [25.0] * 4 + [0.0] * 4
    by_household = pe.cluster_bootstrap_sigma(contrib, [1, 1, 1, 1, 2, 2, 2, 2], draws=400, seed=7)
    by_person = pe.cluster_bootstrap_sigma(contrib, list(range(8)), draws=400, seed=7)
    assert by_household > by_person


@requires_numpy
def test_bootstrap_sigma_of_a_single_cluster_is_zero():
    assert pe.cluster_bootstrap_sigma([1.0, 2.0], [4, 4], draws=10, seed=1) == 0.0


@requires_numpy
def test_bootstrap_sigma_is_seed_reproducible():
    contrib = [float(i % 7) for i in range(200)]
    clusters = [i // 2 for i in range(200)]
    a = pe.cluster_bootstrap_sigma(contrib, clusters, draws=100, seed=3)
    b = pe.cluster_bootstrap_sigma(contrib, clusters, draws=100, seed=3)
    assert a == b
