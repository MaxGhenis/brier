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

import pytest

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


def stampable_cell() -> dict:
    """Minimal cell with the fields to_forecast_cell copies verbatim."""
    cell = {key: "?" for key in spawned_cells_to_ts.REQUIRED}
    cell.update(
        {
            "slug": "stamp-probe-cell",
            "pointEstimate": 1.0,
            "ciLow": 0.5,
            "ciHigh": 1.5,
            "confidence": 0.8,
            "historicalContext": [{"label": "t-1", "value": 1.0}],
            "drivers": ["driver"],
            "sourceContext": ["https://example.gov/series"],
            "runAt": "2026-07-24T14:57:47Z",
            "reasoning": [],
            "model": "gpt-5.5",
        }
    )
    return cell


def test_published_stamp_names_the_run_agent_not_the_working_tree() -> None:
    """A published cell must carry the agent that PRODUCED it.

    The stamp used to come from the live agent definition, so editing any
    skill silently restamped every previously published cell with a version
    that never generated it — and broke wave reproducibility until the wave
    was regenerated into that same untruth (2026-07-25).
    """

    sealed = {
        "agent": "thesis.analyst",
        "agentVersion": "2.3.0",
        "model": "gpt-5.5",
        "promptHash": "a" * 64,
        "toolPolicyHash": "b" * 64,
    }
    cell = stampable_cell()
    cell[spawned_cells_to_ts.SEALED_AGENT_KEY] = sealed

    run = spawned_cells_to_ts.to_forecast_cell(cell)["predictionRun"]

    assert run["agentVersion"] == "2.3.0"
    assert run["promptHash"] == "a" * 64
    assert run["toolPolicyHash"] == "b" * 64
    live = spawned_cells_to_ts.agent_stamp()
    assert live["agentVersion"] != "2.3.0", (
        "fixture must differ from the live agent, or this proves nothing"
    )
    # The private carrier key must never reach the published cell.
    assert spawned_cells_to_ts.SEALED_AGENT_KEY not in run


def test_stamp_falls_back_to_live_agent_when_run_sealed_none() -> None:
    """Pre-manifest inputs keep working: fall back, never crash."""

    run = spawned_cells_to_ts.to_forecast_cell(stampable_cell())["predictionRun"]
    assert run["agentVersion"] == spawned_cells_to_ts.agent_stamp()["agentVersion"]
    assert run["provenance"] == "ci"


def test_attested_stamp_carries_public_ticket_identity() -> None:
    cell = stampable_cell()
    cell[spawned_cells_to_ts.SEALED_GENERATION_TICKET_KEY] = {
        "ticketId": "2030-01-11-deadbeef",
        "ticketPath": "records/tickets/2030-01-11/2030-01-11-deadbeef.json",
    }

    run = spawned_cells_to_ts.to_forecast_cell(cell)["predictionRun"]

    assert run["provenance"] == "local_operator_attested"
    assert run["generationTicket"] == {
        "ticketId": "2030-01-11-deadbeef",
        "ticketPath": "records/tickets/2030-01-11/2030-01-11-deadbeef.json",
    }


def test_unsealed_cell_cannot_self_claim_attested_provenance() -> None:
    cell = stampable_cell()
    cell["generationTicket"] = {
        "ticketId": "2030-01-11-deadbeef",
        "ticketPath": "records/tickets/2030-01-11/2030-01-11-deadbeef.json",
    }

    run = spawned_cells_to_ts.to_forecast_cell(cell)["predictionRun"]

    assert run["provenance"] == "ci"
    assert "generationTicket" not in run


def test_loaded_cell_cannot_spoof_private_sealed_metadata(
    tmp_path: pathlib.Path,
) -> None:
    import json

    cell = stampable_cell()
    cell["runAt"] = "2026-07-01T00:00:00Z"
    cell[spawned_cells_to_ts.SEALED_GENERATION_TICKET_KEY] = {
        "ticketId": "2030-01-11-deadbeef",
        "ticketPath": "records/tickets/2030-01-11/2030-01-11-deadbeef.json",
    }
    cell[spawned_cells_to_ts.SEALED_AGENT_KEY] = {
        "agent": "spoofed.agent",
        "agentVersion": "999.0.0",
        "promptHash": "a" * 64,
        "toolPolicyHash": "b" * 64,
    }
    cells_path = tmp_path / "normalized_cells.json"
    cells_path.write_text(json.dumps([cell]))

    loaded = spawned_cells_to_ts.load_cells(cells_path)[0]
    run = spawned_cells_to_ts.to_forecast_cell(loaded)["predictionRun"]

    assert run["provenance"] == "ci"
    assert "generationTicket" not in run
    assert run["agent"] != "spoofed.agent"


def test_sealed_generation_ticket_reads_manifest_identity(
    tmp_path: pathlib.Path,
) -> None:
    import json

    manifest = {
        "generationTicket": {
            "ticketId": "2030-01-11-deadbeef",
            "ticketPath": "records/tickets/2030-01-11/2030-01-11-deadbeef.json",
            "nonceSha256": "a" * 64,
        }
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))

    assert spawned_cells_to_ts.sealed_generation_ticket(tmp_path) == {
        "ticketId": "2030-01-11-deadbeef",
        "ticketPath": "records/tickets/2030-01-11/2030-01-11-deadbeef.json",
    }


def test_loaded_manifest_ticket_reaches_published_prediction_run(
    tmp_path: pathlib.Path,
) -> None:
    import json

    manifest = {
        "agent": {
            "agent": "thesis.analyst",
            "agentVersion": "3.0.0",
            "promptHash": "b" * 64,
            "toolPolicyHash": "c" * 64,
        },
        "generationTicket": {
            "ticketId": "2030-01-11-deadbeef",
            "ticketPath": "records/tickets/2030-01-11/2030-01-11-deadbeef.json",
            "nonceSha256": "a" * 64,
        },
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    cell = stampable_cell()
    cell["runAt"] = "2026-07-01T00:00:00Z"
    cells_path = tmp_path / "normalized_cells.json"
    cells_path.write_text(json.dumps([cell]))

    loaded = spawned_cells_to_ts.load_cells(cells_path)[0]
    run = spawned_cells_to_ts.to_forecast_cell(loaded)["predictionRun"]

    assert run["agentVersion"] == "3.0.0"
    assert run["provenance"] == "local_operator_attested"
    assert run["generationTicket"] == {
        "ticketId": "2030-01-11-deadbeef",
        "ticketPath": "records/tickets/2030-01-11/2030-01-11-deadbeef.json",
    }


def test_sealed_generation_ticket_refuses_invalid_manifest_identity(
    tmp_path: pathlib.Path,
) -> None:
    import json

    (tmp_path / "manifest.json").write_text(
        json.dumps(
            {
                "generationTicket": {
                    "ticketId": "2030-01-11-deadbeef",
                    "ticketPath": "records/tickets/2030-01-11/ticket.json",
                    "nonceSha256": "not-a-hash",
                }
            }
        )
    )

    with pytest.raises(ValueError, match="nonceSha256 is invalid"):
        spawned_cells_to_ts.sealed_generation_ticket(tmp_path)


def test_legacy_replacement_module_omits_only_new_provenance_stamp(
    tmp_path: pathlib.Path,
) -> None:
    legacy = tmp_path / "legacy.ts"
    legacy.write_text('"predictionDistribution": {"provenance": "interval_seeded"}')
    current = tmp_path / "current.ts"
    current.write_text('"predictionRun": {"provenance": "ci"}')

    assert not spawned_cells_to_ts.replacement_has_run_provenance(str(legacy))
    assert spawned_cells_to_ts.replacement_has_run_provenance(str(current))
    assert spawned_cells_to_ts.replacement_has_run_provenance(None)
    legacy_run = spawned_cells_to_ts.to_forecast_cell(
        stampable_cell(), include_provenance=False
    )["predictionRun"]
    assert "provenance" not in legacy_run
    assert "generationTicket" not in legacy_run


def test_sealed_agent_meta_rejects_incomplete_manifest_identity(
    tmp_path: pathlib.Path,
) -> None:
    """A half-filled agent block must fall back, not publish blanks."""

    import json

    (tmp_path / "manifest.json").write_text(
        json.dumps({"agent": {"agent": "thesis.analyst", "agentVersion": ""}})
    )
    assert spawned_cells_to_ts.sealed_agent_meta(tmp_path) is None
    assert spawned_cells_to_ts.sealed_agent_meta(tmp_path / "missing") is None
