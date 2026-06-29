from __future__ import annotations

import json
import subprocess
import sys
from importlib.util import find_spec
from pathlib import Path

import pytest

from brier.timeseries import (
    SCHEMA_VERSION,
    build_candidate_set,
    build_persistence_candidate,
    build_statsmodels_local_level_candidate,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_time_series_models.py"


SAMPLE_HISTORY = [
    {"period": "2020", "value": 100},
    {"period": "2021", "value": 103},
    {"period": "2022", "value": 107},
    {"period": "2023", "value": 110},
    {"period": "2024", "value": 114},
    {"period": "2025", "value": 119},
]


def test_persistence_candidate_has_required_interval_schema():
    candidate = build_persistence_candidate(
        target_data_point_id="test.series.2026",
        target_period="2026",
        history=SAMPLE_HISTORY,
        generated_at="2026-06-26T00:00:00Z",
        round_increment=0.1,
    ).as_dict()

    assert candidate["schemaVersion"] == SCHEMA_VERSION
    assert candidate["library"] == "brier"
    assert candidate["modelName"] == "persistence.last_print"
    assert candidate["pointEstimate"] == 119
    assert candidate["interval80"]["lower"] < candidate["pointEstimate"]
    assert candidate["interval80"]["upper"] > candidate["pointEstimate"]
    assert candidate["interval90"]["level"] == 0.9
    assert candidate["quantiles"]["p10"] == candidate["interval80"]["lower"]
    assert candidate["quantiles"]["p90"] == candidate["interval80"]["upper"]
    assert candidate["intervalMethod"] == "residual_quantile"
    assert candidate["backtestScore"]["rows"] == len(SAMPLE_HISTORY) - 1


@pytest.mark.skipif(
    find_spec("statsmodels") is None, reason="statsmodels extra missing"
)
def test_statsmodels_candidate_uses_native_interval_metadata():
    candidate = build_statsmodels_local_level_candidate(
        target_data_point_id="test.series.2026",
        target_period="2026",
        history=SAMPLE_HISTORY,
        generated_at="2026-06-26T00:00:00Z",
        round_increment=0.1,
    ).as_dict()

    assert candidate["library"] == "statsmodels"
    assert candidate["libraryVersion"] != "not_installed"
    assert candidate["modelName"] == "sarimax_local_level_drift"
    assert candidate["intervalMethod"] == "native_state_space"
    assert candidate["interval80"]["lower"] < candidate["pointEstimate"]
    assert candidate["interval80"]["upper"] > candidate["pointEstimate"]
    assert candidate["calibrationN"] == len(SAMPLE_HISTORY) - 1
    assert candidate["backtestScore"]["method"] == "walk_forward_1_step"


def test_candidate_set_can_emit_persistence_without_optional_extras():
    candidate_set = build_candidate_set(
        target_data_point_id="test.series.2026",
        target_period="2026",
        history=SAMPLE_HISTORY[:2],
        models=["persistence"],
        generated_at="2026-06-26T00:00:00Z",
    )

    assert candidate_set["schemaVersion"] == "thesis_model_candidate_set_v1"
    assert candidate_set["candidateCount"] == 1
    assert candidate_set["candidates"][0]["intervalMethod"] == "fallback_prior"


def test_time_series_model_script_outputs_candidate_json():
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--target-id",
            "test.series.2026",
            "--target-period",
            "2026",
            "--history-json",
            json.dumps(SAMPLE_HISTORY[:2]),
            "--models",
            "persistence",
            "--generated-at",
            "2026-06-26T00:00:00Z",
            "--round-increment",
            "0.1",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert payload["schemaVersion"] == "thesis_model_candidate_set_v1"
    assert payload["targetDataPointId"] == "test.series.2026"
    assert payload["candidates"][0]["schemaVersion"] == SCHEMA_VERSION
