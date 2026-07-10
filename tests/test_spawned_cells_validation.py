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
