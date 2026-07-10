"""The converter's leakage and sigma gates must fire on FRESH cells.

Raw spawned cells carry the sealed runAt at the top level; predictionRun
only exists after the converter builds the TS. A predictionRun-only read
left run_at empty and silently skipped both gates until vitest bounced the
staged wave (live incident 2026-07-10: Canada June LFS forecast generated
on LFS release day survived generate and died in the publish gate).
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import spawned_cells_to_ts  # noqa: E402


def probe_cell(resolution_date: str) -> dict:
    cell = {key: "?" for key in spawned_cells_to_ts.REQUIRED}
    cell.update(
        {
            "slug": "leakage-probe-cell",
            "title": "Leakage probe",
            "question": "?",
            "type": "data",
            "country": "CA",
            "unit": "thousands",
            "pointEstimate": 20,
            "ciLow": 10,
            "ciHigh": 30,
            "confidence": 0.8,
            "resolutionDate": resolution_date,
            "resolutionSource": "Test",
            "resolutionRule": "Test",
            "resolutionSourceUrl": "https://example.gov/data",
            "runAt": "2026-07-10T04:05:26Z",
            "historicalContext": [
                {"label": "t-2", "value": 18},
                {"label": "t-1", "value": 19},
            ],
            "sourceContext": [
                "https://example.gov/a",
                "https://example.gov/b",
            ],
            "reasoning": [],
        }
    )
    return cell


def test_leakage_gate_fires_on_fresh_cells_with_top_level_run_at() -> None:
    errors = spawned_cells_to_ts.validate(probe_cell("2026-07-10"), set())
    assert any("leakage" in error for error in errors), errors

    errors_ok = spawned_cells_to_ts.validate(probe_cell("2026-07-17"), set())
    assert not any("leakage" in error for error in errors_ok), errors_ok


def test_sigma_gate_fires_on_fresh_cells_with_top_level_run_at() -> None:
    # No math step showing sigma/1.28: the derivation gate must complain for
    # a fresh post-2026-07-05 cell, which it silently skipped before the fix.
    errors = spawned_cells_to_ts.validate(probe_cell("2026-07-17"), set())
    assert any("interval derivation" in error for error in errors), errors


def ladder_v2_cell(math_text: str) -> dict:
    cell = probe_cell("2026-07-17")
    cell["promptMode"] = "ladder_v2"
    cell["reasoning"] = [{"kind": "math", "text": math_text}]
    return cell


def test_ladder_v2_derivation_gate_accepts_quantile_inversion() -> None:
    # The pre-registered ladder_v2 contract: rungs plus the interpolated tail
    # percentiles stated literally satisfy the derivation gate with no sigma.
    compliant = ladder_v2_cell(
        "Ladder: P(X <= 18) = 0.05; P(X <= 19) = 0.30; P(X <= 20) = 0.55; "
        "P(X <= 21) = 0.85; P(X <= 22) = 0.95. Linear interpolation gives "
        "the 10th percentile at 18.2, median at 19.8, and 90th percentile "
        "at 21.3."
    )
    errors = spawned_cells_to_ts.validate(compliant, set())
    assert not any("derivation" in error for error in errors), errors
    assert not any("ladder_v2 math step" in error for error in errors), errors


def test_ladder_v2_derivation_gate_rejects_missing_percentiles() -> None:
    # Rungs alone are elicitation, not derivation: the interpolated tail
    # percentiles must be stated.
    rungs_only = ladder_v2_cell(
        "Ladder: P(X <= 18) = 0.05; P(X <= 19) = 0.30; P(X <= 20) = 0.55; "
        "P(X <= 21) = 0.85; P(X <= 22) = 0.95."
    )
    errors = spawned_cells_to_ts.validate(rungs_only, set())
    assert any("ladder_v2 math step" in error for error in errors), errors

    # And percentile prose without the elicited rungs fails too.
    percentiles_only = ladder_v2_cell(
        "10th percentile at 18.2 and 90th percentile at 21.3, trust me."
    )
    errors = spawned_cells_to_ts.validate(percentiles_only, set())
    assert any("ladder_v2 math step" in error for error in errors), errors


def test_sigma_gate_still_binds_every_other_prompt_mode() -> None:
    # ladder_v2 is an explicit opt-in: fast/ladder/full cells (and cells with
    # no promptMode at all) still owe the sigma/1.28 derivation.
    for mode in ("fast", "ladder", "full", None):
        cell = probe_cell("2026-07-17")
        if mode is not None:
            cell["promptMode"] = mode
        cell["reasoning"] = [
            {
                "kind": "math",
                "text": "Ladder: P(X <= 18) = 0.05; P(X <= 22) = 0.95; "
                "P(X <= 20) = 0.5; 10th percentile at 18.2, 90th "
                "percentile at 21.3.",
            }
        ]
        errors = spawned_cells_to_ts.validate(cell, set())
        assert any(
            "interval derivation" in error for error in errors
        ), (mode, errors)
