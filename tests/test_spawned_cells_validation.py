"""The converter's leakage and sigma gates must fire on FRESH cells.

Raw spawned cells carry the sealed runAt at the top level; predictionRun
only exists after the converter builds the TS. A predictionRun-only read
left run_at empty and silently skipped both gates until vitest bounced the
staged wave (live incident 2026-07-10: Canada June LFS forecast generated
on LFS release day survived generate and died in the publish gate).
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import replace_cells_in_place  # noqa: E402
import spawned_cells_to_ts  # noqa: E402
import verify_wave_reproducibility  # noqa: E402


def sealed_agent(version: str = "2.5.10") -> dict[str, str]:
    return {
        "agent": "thesis.analyst",
        "agentVersion": version,
        "promptHash": "a" * 64,
        "toolPolicyHash": "b" * 64,
    }


def successful_manifest(**overrides: object) -> dict:
    manifest: dict = {"ok": True, "agent": sealed_agent()}
    manifest.update(overrides)
    return manifest


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
                {
                    "period": {"type": "month", "value": f"2026-{index:02d}"},
                    "label": f"2026-{index:02d}",
                    "value": 17 + index,
                }
                for index in range(1, 7)
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


def test_million_cubic_feet_is_a_canonical_exploratory_unit() -> None:
    cell = probe_cell("2026-07-17")
    cell["unit"] = "million_cubic_feet"

    errors = spawned_cells_to_ts.validate(cell, set())

    assert not any("not allowed" in error for error in errors), errors


# The committed 2026-08-07 DoD registration whose immutable unit
# ("billions USD") is not an ALLOWED_UNITS member — the incident that
# motivated the registration-authenticated exemption.
DOD_REGISTRATION_PATH = (
    "records/targets/"
    "2026-08-07-59b334c6612eaf1c20be70ad587590901539f4fc2a11749e9f6a8f1ef2927907.json"
)
DOD_CONTENT_HASH = "59b334c6612eaf1c20be70ad587590901539f4fc2a11749e9f6a8f1ef2927907"


def registered_dod_context() -> dict:
    return {
        "catalogSlug": "us-dod-prime-award-obligations-fy2026",
        "targetUnit": "billions USD",
        "targetRegistrationPath": DOD_REGISTRATION_PATH,
        "targetContentHash": DOD_CONTENT_HASH,
    }


def test_registered_unit_is_exempt_from_the_exploratory_allowlist() -> None:
    # A registration-authenticated run passes by echoing the registered
    # targetUnit byte-for-byte; an unregistered run, a mismatched claim,
    # or an off-list unit with no registration stays refused.
    cell = probe_cell("2026-07-17")
    cell["unit"] = "billions USD"

    unregistered = spawned_cells_to_ts.validate(cell, set())
    assert any("not allowed" in error for error in unregistered), unregistered

    registered = spawned_cells_to_ts.validate(
        cell, set(), target_context=registered_dod_context()
    )
    assert not any("not allowed" in error for error in registered), registered

    mismatched_context = registered_dod_context()
    mismatched_context["targetUnit"] = "usd_billions"
    mismatched = spawned_cells_to_ts.validate(
        cell, set(), target_context=mismatched_context
    )
    assert any("not allowed" in error for error in mismatched), mismatched


def test_forged_contexts_cannot_buy_the_unit_exemption() -> None:
    # A bare claim, a wrong hash, a foreign slug, or an attacker-shaped
    # unit matching the cell must all fall back to the allowlist: the
    # exemption exists only for units the registration snapshot proves.
    cell = probe_cell("2026-07-17")

    cell["unit"] = "attacker-shaped unit"
    bare_claim = spawned_cells_to_ts.validate(
        cell, set(), target_context={"targetUnit": "attacker-shaped unit"}
    )
    assert any("not allowed" in error for error in bare_claim), bare_claim

    cell["unit"] = "billions USD"
    no_snapshot = spawned_cells_to_ts.validate(
        cell, set(), target_context={"targetUnit": "billions USD"}
    )
    assert any("not allowed" in error for error in no_snapshot), no_snapshot

    tampered = registered_dod_context()
    tampered["targetContentHash"] = "0" * 64
    wrong_hash = spawned_cells_to_ts.validate(cell, set(), target_context=tampered)
    assert any("not allowed" in error for error in wrong_hash), wrong_hash

    foreign = registered_dod_context()
    foreign["catalogSlug"] = "some-other-slug"
    wrong_slug = spawned_cells_to_ts.validate(cell, set(), target_context=foreign)
    assert any("not allowed" in error for error in wrong_slug), wrong_slug


def bounded_context(start: str = "2026-07-11") -> dict:
    return {
        "resolutionDateBasis": "resolve-by-bound",
        "sourceBinding": {
            "expectedReleaseWindow": {"start": start, "end": "2026-07-17"}
        },
    }


def ticket_context() -> dict:
    return {
        "ticketId": "2026-07-10-deadbeef",
        "ticketPath": ("records/tickets/2026-07-10/2026-07-10-deadbeef.json"),
        "nonceSha256": "a" * 64,
    }


def test_bounded_cell_requires_ticket_context_literally() -> None:
    cell = probe_cell("2026-07-17")
    cell["runStartedAt"] = "2026-07-10T04:00:00Z"

    errors = spawned_cells_to_ts.validate(cell, set(), target_context=bounded_context())

    assert "resolve-by-bound target requires generation ticket context" in errors
    ticketed = spawned_cells_to_ts.validate(
        cell,
        set(),
        target_context=bounded_context(),
        generation_ticket=ticket_context(),
    )
    assert "resolve-by-bound target requires generation ticket context" not in ticketed


def test_bounded_cell_rejects_incomplete_ticket_context_literally() -> None:
    cell = probe_cell("2026-07-17")
    cell["runStartedAt"] = "2026-07-10T04:00:00Z"

    errors = spawned_cells_to_ts.validate(
        cell,
        set(),
        target_context=bounded_context(),
        generation_ticket={"ticketId": "2026-07-10-deadbeef"},
    )

    assert "resolve-by-bound target requires generation ticket context" in errors


def test_shared_validator_rejects_unsupported_basis_literally() -> None:
    errors = spawned_cells_to_ts.validate(
        probe_cell("2026-07-17"),
        set(),
        target_context={"resolutionDateBasis": "deadline-ish"},
    )

    assert "unsupported target resolutionDateBasis 'deadline-ish'" in errors


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        (
            "runStartedAt",
            None,
            "resolve-by-bound cell is missing runStartedAt",
        ),
        (
            "runStartedAt",
            "not-an-instant",
            "resolve-by-bound cell runStartedAt is not ISO-8601",
        ),
        (
            "runStartedAt",
            "2026-07-10T04:00:00",
            "resolve-by-bound cell runStartedAt is not timezone-aware",
        ),
        (
            "runStartedAt",
            "2026-07-11T00:00:00Z",
            "runStartedAt 2026-07-11T00:00:00Z must precede "
            "expectedReleaseWindow.start 2026-07-11",
        ),
        (
            "runAt",
            "2026-07-11T00:00:00Z",
            "runAt 2026-07-11T00:00:00Z must precede "
            "expectedReleaseWindow.start 2026-07-11",
        ),
    ],
)
def test_bounded_run_and_seal_must_precede_window_literally(
    field: str, value: str | None, message: str
) -> None:
    cell = probe_cell("2026-07-17")
    cell["runStartedAt"] = "2026-07-10T04:00:00Z"
    if value is None:
        cell.pop(field, None)
    else:
        cell[field] = value

    errors = spawned_cells_to_ts.validate(
        cell,
        set(),
        target_context=bounded_context(),
        generation_ticket=ticket_context(),
    )

    assert message in errors


def test_bounded_context_requires_canonical_nested_window_start_literally() -> None:
    cell = probe_cell("2026-07-17")
    cell["runStartedAt"] = "2026-07-10T04:00:00Z"

    errors = spawned_cells_to_ts.validate(
        cell,
        set(),
        target_context=bounded_context("2026-7-11"),
        generation_ticket=ticket_context(),
    )

    assert (
        "resolve-by-bound target requires canonical "
        "sourceBinding.expectedReleaseWindow.start"
    ) in errors


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
        assert any("interval derivation" in error for error in errors), (mode, errors)


def converter_policy_cell(
    policy_step: str | None,
    *,
    prompt_mode: str = "full",
) -> dict:
    cell = probe_cell("2026-07-17")
    cell.update(
        {
            "type": "conditional",
            "conditionalOn": "A registered policy changes the measured outcome.",
            "promptMode": prompt_mode,
        }
    )
    if policy_step is not None:
        cell["reasoning"].append({"kind": "text", "text": policy_step})
    return cell


def converter_policy_step(precedent_url: str) -> str:
    return (
        "Policy chain: Touched population: a fetched count of 12,000 workers; "
        f"Propagation: the evaluation at {precedent_url} found a 0.3-point "
        "response per funded unit and implies a measured effect; Offsets: "
        "turnover could counteract it; Timing/lag: implementation lag leaves "
        "half the effect in the resolution period."
    )


def policy_chain_validation_errors(errors: list[str]) -> list[str]:
    return [error for error in errors if error.startswith("conditional policy chain:")]


def test_converter_enforces_current_conditional_policy_chain() -> None:
    errors = spawned_cells_to_ts.validate(
        converter_policy_cell(None),
        set(),
        agent_version="2.5.12",
    )

    assert policy_chain_validation_errors(errors) == [
        "conditional policy chain: missing reasoning step beginning exactly "
        "'Policy chain:'"
    ]


def test_converter_uses_sealed_target_context_for_precedent_exclusions() -> None:
    measure_url = "https://www.congress.gov/bill/119th-congress/house-bill/8800"
    conditional = f"The measure at {measure_url} is enacted before the deadline."
    cell = converter_policy_cell(converter_policy_step(measure_url))
    cell["conditionalOn"] = conditional
    cell["sourceContext"].append(measure_url)
    cell[spawned_cells_to_ts.SEALED_TARGET_CONTEXT_KEY] = {"conditional": conditional}

    errors = spawned_cells_to_ts.validate(
        cell,
        set(),
        agent_version="2.5.12",
    )

    assert policy_chain_validation_errors(errors) == [
        "conditional policy chain: precedent URL must be distinct from the "
        "conditional instrument and resolution source URLs"
    ]


def test_converter_grandfathers_pre_policy_chain_agent() -> None:
    errors = spawned_cells_to_ts.validate(
        converter_policy_cell(None),
        set(),
        agent_version="2.5.11",
    )

    assert policy_chain_validation_errors(errors) == []


def test_converter_grandfathers_pre_policy_chain_agent_with_sealed_mode() -> None:
    errors = spawned_cells_to_ts.validate(
        converter_policy_cell(None),
        set(),
        agent_version="2.5.11",
        prompt_mode="full",
    )

    assert policy_chain_validation_errors(errors) == []


@pytest.mark.parametrize("prompt_mode", ["ladder", "ladder_v2"])
def test_converter_exempts_current_ladder_modes(prompt_mode: str) -> None:
    errors = spawned_cells_to_ts.validate(
        converter_policy_cell(None, prompt_mode=prompt_mode),
        set(),
        agent_version="2.5.12",
    )

    assert policy_chain_validation_errors(errors) == []


def test_converter_accepts_complete_current_policy_chain() -> None:
    precedent_url = "https://example.gov/program-evaluation"
    cell = converter_policy_cell(converter_policy_step(precedent_url))
    cell["sourceContext"].append(precedent_url)

    errors = spawned_cells_to_ts.validate(
        cell,
        set(),
        agent_version="2.5.12",
    )

    assert policy_chain_validation_errors(errors) == []


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


def test_stamp_refuses_when_run_sealed_agent_is_absent() -> None:
    with pytest.raises(ValueError, match="lacks sealed agent metadata"):
        spawned_cells_to_ts.to_forecast_cell(stampable_cell())


def test_metadata_carrier_refuses_when_run_manifest_is_absent(
    tmp_path: pathlib.Path,
) -> None:
    with pytest.raises(ValueError, match="lacks manifest.json"):
        spawned_cells_to_ts.carry_sealed_run_metadata([stampable_cell()], tmp_path)


def test_explicit_ci_stamp_is_not_inferred() -> None:
    cell = stampable_cell()
    cell[spawned_cells_to_ts.SEALED_AGENT_KEY] = sealed_agent()
    run = spawned_cells_to_ts.to_forecast_cell(cell, provenance="ci")["predictionRun"]

    assert run["provenance"] == "ci"
    assert "generationTicket" not in run


def test_attested_stamp_carries_public_ticket_identity() -> None:
    cell = stampable_cell()
    cell[spawned_cells_to_ts.SEALED_AGENT_KEY] = sealed_agent()
    cell[spawned_cells_to_ts.SEALED_GENERATION_TICKET_KEY] = {
        "ticketId": "2030-01-11-deadbeef",
        "ticketPath": "records/tickets/2030-01-11/2030-01-11-deadbeef.json",
    }

    run = spawned_cells_to_ts.to_forecast_cell(
        cell, provenance="local_operator_attested"
    )["predictionRun"]

    assert run["provenance"] == "local_operator_attested"
    assert run["generationTicket"] == {
        "ticketId": "2030-01-11-deadbeef",
        "ticketPath": "records/tickets/2030-01-11/2030-01-11-deadbeef.json",
    }


def test_unsealed_cell_cannot_self_claim_attested_provenance() -> None:
    cell = stampable_cell()
    cell[spawned_cells_to_ts.SEALED_AGENT_KEY] = sealed_agent()
    cell["generationTicket"] = {
        "ticketId": "2030-01-11-deadbeef",
        "ticketPath": "records/tickets/2030-01-11/2030-01-11-deadbeef.json",
    }

    run = spawned_cells_to_ts.to_forecast_cell(cell)["predictionRun"]

    assert "provenance" not in run
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
    cell[spawned_cells_to_ts.SEALED_TARGET_CONTEXT_KEY] = bounded_context()
    cell[spawned_cells_to_ts.SEALED_VALIDATION_TICKET_KEY] = ticket_context()
    cells_path = tmp_path / "normalized_cells.json"
    cells_path.write_text(json.dumps([cell]))
    (tmp_path / "manifest.json").write_text(json.dumps(successful_manifest()))

    cells = [cell]
    spawned_cells_to_ts.carry_sealed_run_metadata(cells, tmp_path)
    loaded = cells[0]
    run = spawned_cells_to_ts.to_forecast_cell(loaded)["predictionRun"]

    assert "provenance" not in run
    assert "generationTicket" not in run
    assert run["agent"] != "spoofed.agent"
    assert spawned_cells_to_ts.SEALED_TARGET_CONTEXT_KEY not in loaded
    assert spawned_cells_to_ts.SEALED_VALIDATION_TICKET_KEY not in loaded


def test_converter_validation_uses_sealed_bounded_manifest_context(
    tmp_path: pathlib.Path,
) -> None:
    import json

    manifest = successful_manifest(
        **{
            "targetContext": bounded_context(),
            "generationTicket": ticket_context(),
        }
    )
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    cell = probe_cell("2026-07-17")
    cell["runStartedAt"] = "2026-07-01T03:55:00Z"
    cell["runAt"] = "2026-07-01T04:00:00Z"
    cells_path = tmp_path / "normalized_cells.json"
    cells_path.write_text(json.dumps([cell]))

    cells = [cell]
    spawned_cells_to_ts.carry_sealed_run_metadata(cells, tmp_path)
    loaded = cells[0]
    errors = spawned_cells_to_ts.validate(
        loaded,
        set(),
        agent_version=loaded[spawned_cells_to_ts.SEALED_AGENT_KEY]["agentVersion"],
    )

    assert "resolve-by-bound target requires generation ticket context" not in errors
    assert not any("expectedReleaseWindow.start" in error for error in errors)


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

    manifest = successful_manifest(
        **{
            "agent": sealed_agent("3.0.0"),
            "generationTicket": {
                "ticketId": "2030-01-11-deadbeef",
                "ticketPath": ("records/tickets/2030-01-11/2030-01-11-deadbeef.json"),
                "nonceSha256": "a" * 64,
            },
        }
    )
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    cell = stampable_cell()
    cell["runAt"] = "2026-07-01T00:00:00Z"
    cells_path = tmp_path / "normalized_cells.json"
    cells_path.write_text(json.dumps([cell]))

    cells = [cell]
    spawned_cells_to_ts.carry_sealed_run_metadata(cells, tmp_path)
    unlabeled = cells[0]
    unlabeled_run = spawned_cells_to_ts.to_forecast_cell(unlabeled)["predictionRun"]
    assert "provenance" not in unlabeled_run
    assert "generationTicket" not in unlabeled_run

    spawned_cells_to_ts.carry_sealed_run_metadata(
        cells, tmp_path, provenance="local_operator_attested"
    )
    loaded = cells[0]
    run = spawned_cells_to_ts.to_forecast_cell(
        loaded, provenance="local_operator_attested"
    )["predictionRun"]

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


def test_ci_conversion_refuses_ticketed_manifest_literally(
    tmp_path: pathlib.Path,
) -> None:
    import json

    (tmp_path / "manifest.json").write_text(
        json.dumps(successful_manifest(generationTicket={"untrusted": "shape"}))
    )
    cell = stampable_cell()
    cell["runAt"] = "2026-07-01T00:00:00Z"
    cells_path = tmp_path / "normalized_cells.json"
    cells_path.write_text(json.dumps([cell]))

    with pytest.raises(ValueError) as error:
        spawned_cells_to_ts.carry_sealed_run_metadata([cell], tmp_path, provenance="ci")

    assert str(error.value) == (
        "ticketed runs must be converted with --provenance local_operator_attested"
    )


def test_local_attested_conversion_requires_manifest_literally(
    tmp_path: pathlib.Path,
) -> None:
    import json

    cell = stampable_cell()
    cell["runAt"] = "2026-07-01T00:00:00Z"
    cells_path = tmp_path / "normalized_cells.json"
    cells_path.write_text(json.dumps([cell]))

    with pytest.raises(ValueError) as error:
        spawned_cells_to_ts.load_cells(
            cells_path,
            provenance="local_operator_attested",
        )

    assert str(error.value) == (f"cell input lacks manifest.json: {cells_path}")


def test_replacement_and_replay_preserve_existing_run_label() -> None:
    labeled = """
    {
      "predictionDistribution": {"provenance": "interval_seeded"},
      "predictionRun": {"kind": "recorded-agent-run", "provenance": "ci"}
    }
    """
    legacy = '{"predictionRun": {"kind": "recorded-agent-run"}}'

    assert replace_cells_in_place.existing_run_provenance(labeled) == "ci"
    assert replace_cells_in_place.existing_run_provenance(legacy) is None
    assert verify_wave_reproducibility.committed_run_provenance(labeled) == "ci"
    assert verify_wave_reproducibility.committed_run_provenance(legacy) is None
    assert (
        verify_wave_reproducibility.trusted_replay_provenance(
            labeled, [{"results": []}]
        )
        == "ci"
    )
    assert (
        verify_wave_reproducibility.trusted_replay_provenance(legacy, [{"results": []}])
        is None
    )

    mixed = labeled + "\n" + legacy
    with pytest.raises(
        ValueError,
        match="generated wave mixes predictionRun provenance labels",
    ):
        verify_wave_reproducibility.committed_run_provenance(mixed)

    with pytest.raises(
        ValueError,
        match=(
            "generated wave predictionRun provenance differs from its batch "
            "provenance: ci != local_operator_attested"
        ),
    ):
        verify_wave_reproducibility.trusted_replay_provenance(
            labeled,
            [{"results": [], "generationTicket": {"ticketId": "ticket"}}],
        )


def test_sealed_agent_meta_rejects_incomplete_manifest_identity(
    tmp_path: pathlib.Path,
) -> None:
    """A recorded half-filled agent block must fail, not fall back."""

    import json

    (tmp_path / "manifest.json").write_text(
        json.dumps(
            {
                "ok": True,
                "agent": {"agent": "thesis.analyst", "agentVersion": ""},
            }
        )
    )
    with pytest.raises(ValueError, match="agent metadata is incomplete"):
        spawned_cells_to_ts.sealed_agent_meta(tmp_path)
    assert spawned_cells_to_ts.sealed_agent_meta(tmp_path / "missing") is None


@pytest.mark.parametrize(
    "agent_version",
    [
        "fixture",
        "2.5",
        "02.5.9",
        "2.05.9",
        "2.5.09",
        "2.5.9+.",
        "2.5.9-..",
        "2.5.9-01",
        "２.５.９",
    ],
)
def test_promotion_rejects_malformed_sealed_agent_version(
    tmp_path: pathlib.Path, agent_version: str
) -> None:
    (tmp_path / "manifest.json").write_text(
        json.dumps(successful_manifest(agent=sealed_agent(agent_version)))
    )
    cells_path = tmp_path / "normalized_cells.json"
    cell = stampable_cell()
    cell["runAt"] = "2026-07-01T00:00:00Z"
    cells_path.write_text(json.dumps([cell]))

    with pytest.raises(ValueError, match="agentVersion is malformed"):
        spawned_cells_to_ts.load_cells(cells_path)


@pytest.mark.parametrize(
    "agent_version", ["2.5.9-alpha+build", "2.2.0+median3", "0.0.0"]
)
def test_sealed_agent_meta_accepts_strict_valid_semver(
    tmp_path: pathlib.Path, agent_version: str
) -> None:
    (tmp_path / "manifest.json").write_text(
        json.dumps(successful_manifest(agent=sealed_agent(agent_version)))
    )

    meta = spawned_cells_to_ts.sealed_agent_meta(tmp_path)

    assert meta is not None
    assert meta["agentVersion"] == agent_version


def test_promotion_refuses_handmade_pre_floor_manifest(
    tmp_path: pathlib.Path,
) -> None:
    cell = probe_cell("2026-07-17")
    cell["runAt"] = "2026-07-01T00:00:00Z"
    cell["historicalContext"] = cell["historicalContext"][:5]
    cells_path = tmp_path / "cells.with_activity.json"
    cells_path.write_text(json.dumps([cell]))
    (tmp_path / "manifest.json").write_text(
        json.dumps(
            successful_manifest(
                agent=sealed_agent("2.5.9"),
                cellsPath="records/thesis-analyst/forged/cells.with_activity.json",
            )
        )
    )

    with pytest.raises(ValueError, match="outside the repository records tree"):
        spawned_cells_to_ts.load_cells(cells_path)


def test_promotion_refuses_copied_real_legacy_manifest_with_other_cells(
    tmp_path: pathlib.Path,
) -> None:
    real_manifest = (
        ROOT
        / "records/thesis-analyst/2026-06-17"
        / "2026-06-17t02-04-41z-abs-labour-employment-change-2026-05"
        / "manifest.json"
    )
    (tmp_path / "manifest.json").write_bytes(real_manifest.read_bytes())
    cells_path = tmp_path / "cells.with_activity.json"
    cells_path.write_text(json.dumps([stampable_cell()]))

    with pytest.raises(ValueError, match="outside the repository records tree"):
        spawned_cells_to_ts.load_cells(cells_path)


def committed_legacy_fixture(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    declared_cells_path: str | None = None,
) -> tuple[pathlib.Path, pathlib.Path]:
    repo = tmp_path / "repo"
    run_relative = pathlib.Path(
        "records/thesis-analyst/2026-07-01/legacy-binding-fixture"
    )
    run_dir = repo / run_relative
    run_dir.mkdir(parents=True)
    cells_path = run_dir / "cells.with_activity.json"
    cells_path.write_text(json.dumps([stampable_cell()]))
    manifest_path = run_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            successful_manifest(
                agent=sealed_agent("2.0.0"),
                cellsPath=(
                    declared_cells_path
                    or (run_relative / "cells.with_activity.json").as_posix()
                ),
            )
        )
    )
    subprocess.run(["git", "init", "--quiet"], cwd=repo, check=True)
    subprocess.run(["git", "add", "records"], cwd=repo, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "core.hooksPath=/dev/null",
            "-c",
            "user.name=Legacy Fixture",
            "-c",
            "user.email=legacy-fixture@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "Commit legacy fixture",
        ],
        cwd=repo,
        check=True,
    )
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()
    monkeypatch.setattr(spawned_cells_to_ts, "ROOT", repo)
    monkeypatch.setattr(
        spawned_cells_to_ts,
        "LEGACY_HISTORY_RECORDS_COMMIT",
        commit,
    )
    return manifest_path, cells_path


@pytest.mark.parametrize("changed_artifact", ["manifest", "cells"])
def test_promotion_refuses_legacy_bytes_changed_after_known_commit(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    changed_artifact: str,
) -> None:
    manifest_path, cells_path = committed_legacy_fixture(tmp_path, monkeypatch)
    if changed_artifact == "manifest":
        manifest = json.loads(manifest_path.read_text())
        manifest["agent"]["promptHash"] = "c" * 64
        manifest_path.write_text(json.dumps(manifest))
    else:
        cells_path.write_bytes(cells_path.read_bytes() + b"\n")

    with pytest.raises(ValueError, match="bytes differ from the known committed"):
        spawned_cells_to_ts.load_cells(cells_path)


def test_promotion_refuses_committed_legacy_manifest_bound_to_other_cells(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _manifest_path, cells_path = committed_legacy_fixture(
        tmp_path,
        monkeypatch,
        declared_cells_path=(
            "records/thesis-analyst/2026-07-01/legacy-binding-fixture/other.json"
        ),
    )

    with pytest.raises(ValueError, match="cellsPath does not name converter input"):
        spawned_cells_to_ts.load_cells(cells_path)


def test_later_branch_commit_cannot_expand_known_legacy_records(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _manifest_path, cells_path = committed_legacy_fixture(tmp_path, monkeypatch)
    cells_path.write_bytes(cells_path.read_bytes() + b"\n")
    subprocess.run(["git", "add", "records"], cwd=tmp_path / "repo", check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "core.hooksPath=/dev/null",
            "-c",
            "user.name=Legacy Fixture",
            "-c",
            "user.email=legacy-fixture@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "Change legacy fixture after cutoff",
        ],
        cwd=tmp_path / "repo",
        check=True,
    )

    with pytest.raises(ValueError, match="bytes differ from the known committed"):
        spawned_cells_to_ts.load_cells(cells_path)


def reviewed_history_floor_fixture(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[pathlib.Path, str, dict]:
    repo = tmp_path / "reviewed-repo"
    scripts_dir = repo / "scripts"
    scripts_dir.mkdir(parents=True)
    authorization = {
        "targetPeriod": "2030-01",
        "status": "official_source_exposes_fewer_than_six_prints",
        "availablePrintCount": 4,
        "availablePeriods": [
            {"type": "month", "value": f"2029-{index:02d}"} for index in range(1, 5)
        ],
    }
    registry = {
        "series": [
            {
                "series": "test.reviewed_rate",
                "period": "2030-01",
                "extras": {"historyFloorAuthorization": authorization},
            }
        ]
    }
    (scripts_dir / "docket_series.json").write_text(json.dumps(registry) + "\n")
    subprocess.run(["git", "init", "--quiet"], cwd=repo, check=True)
    subprocess.run(["git", "add", "scripts/docket_series.json"], cwd=repo, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "core.hooksPath=/dev/null",
            "-c",
            "user.name=History Floor Fixture",
            "-c",
            "user.email=history-floor-fixture@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "Review short-history authorization",
        ],
        cwd=repo,
        check=True,
    )
    checkout_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()
    monkeypatch.setattr(spawned_cells_to_ts, "ROOT", repo)
    return repo, checkout_sha, authorization


def reviewed_four_print_cell() -> dict:
    cell = probe_cell("2030-01-15")
    cell.update(
        {
            "slug": "borrowed-history-authorization-probe",
            "dataPointId": "test.borrowed_history_authorization.2030-01",
            "drivers": ["four-print official history"],
            "runAt": "2026-07-01T04:00:00Z",
            "historicalContext": [
                {
                    "period": {"type": "month", "value": f"2029-{index:02d}"},
                    "label": f"2029-{index:02d}",
                    "value": 16 + index,
                }
                for index in range(1, 5)
            ],
            "historyAvailability": {
                "status": "official_source_exposes_fewer_than_six_prints",
                "availablePrintCount": 4,
                "detail": "The official source exposes exactly four prints.",
            },
            "reasoning": [
                {"kind": "heading", "text": "Short-history probe"},
                {
                    "kind": "text",
                    "text": "The reference class is the last 4 prints.",
                },
                {
                    "kind": "tool",
                    "tool": "official.history",
                    "call": "Fetch the official history",
                    "result": "Fetched 17, 18, 19, and 20.",
                },
                {
                    "kind": "tool",
                    "tool": "official.calendar",
                    "call": "Fetch the official release calendar",
                    "result": "Release date 2030-01-15.",
                },
                {
                    "kind": "tool",
                    "tool": "official.metadata",
                    "call": "Fetch the official series metadata",
                    "result": "The inventory contains 4 prints.",
                },
                {
                    "kind": "math",
                    "text": (
                        "Prior/update/interval: base rate 20; sigma = 7.8125, "
                        "so 1.28*sigma = 10 and the interval is [10, 30]."
                    ),
                },
                {
                    "kind": "text",
                    "text": "Outside the interval if the series breaks regime.",
                },
                {"kind": "forecast", "point": 20, "ciLow": 10, "ciHigh": 30},
            ],
        }
    )
    return cell


def test_backdated_current_run_cannot_borrow_reviewed_history_authorization(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, checkout_sha, authorization = reviewed_history_floor_fixture(
        tmp_path, monkeypatch
    )
    cell = reviewed_four_print_cell()
    resolved = spawned_cells_to_ts.reviewed_history_floor_authorization(
        repo,
        checkout_sha=checkout_sha,
        series="test.reviewed_rate",
        target_period="2030-01",
    )
    assert resolved == authorization
    assert (
        spawned_cells_to_ts.validate(
            cell,
            set(),
            agent_version="2.5.10",
            trusted_history_authorization=resolved,
        )
        == []
    )

    run_dir = repo / "records/thesis-analyst/2030-01-01/backdated-current-probe"
    run_dir.mkdir(parents=True)
    cells_path = run_dir / "cells.with_activity.json"
    cells_path.write_text(json.dumps([cell]))
    (run_dir / "manifest.json").write_text(
        json.dumps(
            successful_manifest(
                agent=sealed_agent("2.5.10"),
                checkoutSha=checkout_sha,
                series="test.reviewed_rate",
                period="2030-01",
                cellsPath=cells_path.relative_to(repo).as_posix(),
            )
        )
    )

    authorization_lookups = []

    def record_authorization_lookup(*args: object, **kwargs: object) -> dict:
        authorization_lookups.append((args, kwargs))
        return authorization

    monkeypatch.setattr(
        spawned_cells_to_ts,
        "reviewed_history_floor_authorization",
        record_authorization_lookup,
    )

    with pytest.raises(
        ValueError,
        match=r"agentVersion 2\.5\.10 requires custody_root\.json",
    ):
        spawned_cells_to_ts.load_cells(cells_path)
    assert authorization_lookups == []


def test_backdated_current_six_print_run_still_requires_custody(
    tmp_path: pathlib.Path,
) -> None:
    cell = probe_cell("2030-01-15")
    cell["runAt"] = "2026-07-01T04:00:00Z"
    cells_path = tmp_path / "normalized_cells.json"
    cells_path.write_text(json.dumps([cell]))
    (tmp_path / "manifest.json").write_text(
        json.dumps(successful_manifest(agent=sealed_agent("2.5.10")))
    )

    with pytest.raises(
        ValueError,
        match=r"agentVersion 2\.5\.10 requires custody_root\.json",
    ):
        spawned_cells_to_ts.load_cells(cells_path)


def test_history_authorization_lookup_follows_current_custody_authentication(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Unit-level call-order coverage: the real verifier is replaced so this
    # test isolates the exact verify -> sealed-identity lookup sequence. A
    # separate integration test exercises a genuine runner custody root.
    repo, checkout_sha, authorization = reviewed_history_floor_fixture(
        tmp_path, monkeypatch
    )
    run_dir = repo / "records/thesis-analyst/2030-01-01/rooted-current-probe"
    run_dir.mkdir(parents=True)
    cells_path = run_dir / "cells.with_activity.json"
    cells_path.write_text(json.dumps([reviewed_four_print_cell()]))
    (run_dir / "custody_root.json").write_text("{}\n")
    (run_dir / "manifest.json").write_text(
        json.dumps(
            successful_manifest(
                agent=sealed_agent("2.5.10"),
                checkoutSha=checkout_sha,
                series="test.reviewed_rate",
                period="2030-01",
                cellsPath=cells_path.relative_to(repo).as_posix(),
                custodyRootSha256="c" * 64,
            )
        )
    )

    import verify_custody

    events = []

    def verify_first(candidate: pathlib.Path) -> None:
        events.append(("verify", candidate))

    def authorize_second(
        repo_root: pathlib.Path,
        *,
        checkout_sha: object,
        series: object,
        target_period: object,
    ) -> dict:
        events.append(
            (
                "authorize",
                repo_root,
                checkout_sha,
                series,
                target_period,
            )
        )
        return authorization

    monkeypatch.setattr(verify_custody, "verify_run", verify_first)
    monkeypatch.setattr(
        spawned_cells_to_ts,
        "reviewed_history_floor_authorization",
        authorize_second,
    )

    [loaded] = spawned_cells_to_ts.load_cells(cells_path)

    assert events == [
        ("verify", run_dir),
        (
            "authorize",
            repo,
            checkout_sha,
            "test.reviewed_rate",
            "2030-01",
        ),
    ]
    assert loaded[spawned_cells_to_ts.SEALED_HISTORY_AUTHORIZATION_KEY] == authorization


def test_invalid_current_custody_refuses_before_history_authorization_lookup(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, checkout_sha, authorization = reviewed_history_floor_fixture(
        tmp_path, monkeypatch
    )
    run_dir = repo / "records/thesis-analyst/2030-01-01/invalid-current-root"
    run_dir.mkdir(parents=True)
    cells_path = run_dir / "cells.with_activity.json"
    cells_path.write_text(json.dumps([reviewed_four_print_cell()]))
    (run_dir / "custody_root.json").write_text("{}\n")
    (run_dir / "manifest.json").write_text(
        json.dumps(
            successful_manifest(
                agent=sealed_agent("2.5.10"),
                checkoutSha=checkout_sha,
                series="test.reviewed_rate",
                period="2030-01",
                cellsPath=cells_path.relative_to(repo).as_posix(),
                custodyRootSha256="c" * 64,
            )
        )
    )

    authorization_lookups = []

    def record_authorization_lookup(*args: object, **kwargs: object) -> dict:
        authorization_lookups.append((args, kwargs))
        return authorization

    monkeypatch.setattr(
        spawned_cells_to_ts,
        "reviewed_history_floor_authorization",
        record_authorization_lookup,
    )

    import verify_custody

    with pytest.raises(
        verify_custody.CustodyError,
        match="unsupported custody schema",
    ):
        spawned_cells_to_ts.load_cells(cells_path)
    assert authorization_lookups == []


def test_in_place_replacement_cannot_bypass_current_custody(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "target.ts"
    cell = probe_cell("2030-01-15")
    cell["runAt"] = "2026-07-01T04:00:00Z"
    target.write_text(f"export const CELLS = {json.dumps([cell])};\n")
    original = target.read_text()

    run_dir = tmp_path / "upgrade"
    run_dir.mkdir()
    upgrades_path = run_dir / "cells.with_activity.json"
    upgrades_path.write_text(json.dumps([cell]))
    (run_dir / "manifest.json").write_text(
        json.dumps(
            successful_manifest(
                agent=sealed_agent("2.5.10"),
                cellsPath=str(upgrades_path),
            )
        )
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["replace_cells_in_place.py", str(target), str(upgrades_path)],
    )

    with pytest.raises(
        ValueError,
        match=r"agentVersion 2\.5\.10 requires custody_root\.json",
    ):
        replace_cells_in_place.main()
    assert target.read_text() == original


@pytest.mark.parametrize(
    "period",
    [
        {"type": [], "value": "2026-01"},
        {"type": {}, "value": "2026-01"},
        {"type": "month", "value": []},
    ],
)
def test_shared_validation_refuses_unhashable_period_containers(
    period: dict[str, object],
) -> None:
    cell = probe_cell("2026-07-17")
    cell["historicalContext"][0]["period"] = period

    errors = spawned_cells_to_ts.validate(
        cell,
        set(),
        agent_version="2.5.10",
    )

    assert "historicalContext[0] has no valid canonical period identity" in errors


@pytest.mark.parametrize("row", [[], "row", 7, None])
def test_shared_validation_refuses_non_object_history_rows(
    row: object,
) -> None:
    cell = probe_cell("2026-07-17")
    cell["historicalContext"] = [row]

    errors = spawned_cells_to_ts.validate(
        cell,
        set(),
        agent_version="2.5.10",
    )

    assert "historicalContext[0] must be an object" in errors


@pytest.mark.parametrize("history", [None, "rows", 7, {}])
def test_shared_validation_refuses_non_list_history(
    history: object,
) -> None:
    cell = probe_cell("2026-07-17")
    cell["historicalContext"] = history

    errors = spawned_cells_to_ts.validate(
        cell,
        set(),
        agent_version="2.5.10",
    )

    assert "historicalContext must be a list" in errors


def test_promotion_keeps_valid_pre_floor_record_with_legacy_history() -> None:
    cells_path = (
        ROOT
        / "records/thesis-analyst/2026-08-12"
        / "2026-08-12t21-21-45z-us-dol-initial-claims-sa-week-2026-08-15"
        / "cells.with_activity.json"
    )

    [loaded] = spawned_cells_to_ts.load_cells(cells_path)
    assert all("period" not in row for row in loaded["historicalContext"])
    assert (
        spawned_cells_to_ts.validate(
            loaded,
            set(),
            agent_version=loaded[spawned_cells_to_ts.SEALED_AGENT_KEY]["agentVersion"],
        )
        == []
    )
    assert (
        spawned_cells_to_ts.to_forecast_cell(loaded)["predictionRun"]["agentVersion"]
        == "2.5.9"
    )


def test_all_committed_pre_floor_records_replay_through_promotion() -> None:
    manifests: list[tuple[pathlib.Path, dict, str]] = []
    for manifest_path in sorted(
        (ROOT / "records/thesis-analyst").rglob("manifest.json")
    ):
        manifest = json.loads(manifest_path.read_text())
        agent = manifest.get("agent") if isinstance(manifest, dict) else None
        version = agent.get("agentVersion") if isinstance(agent, dict) else None
        if (
            manifest.get("ok") is True
            and spawned_cells_to_ts.valid_agent_version(version)
            and not spawned_cells_to_ts.agent_version_enforces_history_floor(version)
        ):
            manifests.append((manifest_path, manifest, version))

    # The pre-floor corpus GROWS until the enforcing version ships:
    # every roll before this change publishes sub-2.5.10 records, so an
    # exact pin rots on the merge ref (509 at fix time, 510 one day
    # later). The floor proves discovery works; the sweep below proves
    # the universal property that actually matters.
    assert len(manifests) >= 509
    cell_count = 0
    history_row_count = 0
    rooted_count = 0
    for manifest_path, manifest, version in manifests:
        rooted_count += int((manifest_path.parent / "custody_root.json").is_file())
        cells_path = ROOT / manifest["cellsPath"]
        loaded = spawned_cells_to_ts.load_cells(cells_path)
        assert len(loaded) == 1, cells_path
        for cell in loaded:
            sealed_version = cell[spawned_cells_to_ts.SEALED_AGENT_KEY]["agentVersion"]
            assert sealed_version == version
            assert (
                spawned_cells_to_ts.history_floor_errors(
                    cell,
                    agent_version=sealed_version,
                )
                == []
            ), cells_path
            projected = spawned_cells_to_ts.to_forecast_cell(cell)
            assert projected["predictionRun"]["agentVersion"] == version
            cell_count += 1
            history_row_count += len(cell["historicalContext"])

    assert cell_count == len(manifests)
    assert history_row_count >= 2_637
    assert rooted_count >= 326
    assert len(manifests) - rooted_count == 183


def test_recorded_failed_manifest_never_promotes(tmp_path: pathlib.Path) -> None:
    manifest = successful_manifest()
    manifest["ok"] = False
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    cells_path = tmp_path / "cells.with_activity.json"
    cells_path.write_text(json.dumps([stampable_cell()]))

    with pytest.raises(ValueError, match="run manifest is not successful"):
        spawned_cells_to_ts.load_cells(cells_path)


@pytest.mark.parametrize(
    "filename", ["cells.with_activity.json", "normalized_cells.json"]
)
def test_cell_input_without_manifest_never_uses_live_fallback(
    tmp_path: pathlib.Path, filename: str
) -> None:
    cells_path = tmp_path / filename
    cells_path.write_text(json.dumps([stampable_cell()]))

    with pytest.raises(ValueError, match="lacks manifest.json"):
        spawned_cells_to_ts.load_cells(cells_path)


def test_reviewer_text_matching_the_screen_is_withheld() -> None:
    # Run 31613588748: a reviewer suggestion saying "attach the fetch
    # transcript" reached the public catalog and the private-source
    # backstop refused the whole publish. Reviewer wording is not
    # evidence: the projection withholds the matching string behind the
    # marker while the run record keeps the original.
    cell = stampable_cell()
    cell[spawned_cells_to_ts.SEALED_AGENT_KEY] = sealed_agent()
    cell["preSubmitReview"] = {
        "schemaVersion": "thesis_pre_submit_review_v1",
        "status": "completed",
        "summary": "Solid derivation overall.",
        "findings": [
            {
                "findingId": "review.suggestion.1",
                "severity": "info",
                "rubricItem": "optional_suggestion",
                "summary": (
                    "Consider attaching the underlying fetch transcript "
                    "or activity artifacts."
                ),
            }
        ],
        "dispositions": [],
    }
    run = spawned_cells_to_ts.to_forecast_cell(cell)["predictionRun"]
    review = run["preSubmitReview"]
    marker = spawned_cells_to_ts.PRIVATE_SOURCE_MARKER
    assert review["findings"][0]["summary"] == marker
    # Untainted reviewer text passes through verbatim, and structured
    # fields are untouched.
    assert review["summary"] == "Solid derivation overall."
    assert review["findings"][0]["severity"] == "info"
    assert not spawned_cells_to_ts.PRIVATE_SOURCE_RE.search(
        json.dumps(review, ensure_ascii=False)
    )
    # The screen only rewrites the review projection: the published
    # reasoning is the agent's verbatim.
    assert run is not None


def test_agent_text_matching_the_screen_still_refuses() -> None:
    # The withholding path is reviewer-only; the agent citing a private
    # source remains a validation failure, exactly as before.
    cell = stampable_cell()
    cell["reasoning"] = [
        {"kind": "text", "text": "Cross-checked against a Granola export."}
    ]
    hits = spawned_cells_to_ts.private_source_hits(cell)
    assert hits == ["reasoning"]


def test_agent_planted_review_dies_at_the_carrier(
    tmp_path: pathlib.Path,
) -> None:
    # Round-two screen review: an agent-supplied preSubmitReview survived
    # a no-review run, was excluded from private_source_hits, and was
    # then masked as if a reviewer wrote it. Review metadata is
    # runner-authored: only the sealed manifest may attach it.
    import json

    cell = stampable_cell()
    cell["runAt"] = "2026-07-01T04:00:00Z"  # pre-custody-enforcement: the
    # carrier boundary under test is date-independent
    cell["preSubmitReview"] = {
        "schemaVersion": "thesis_pre_submit_review_v1",
        "status": "completed",
        "summary": "planted: sourced from a Granola export",
        "findings": [],
        "dispositions": [],
    }
    cells_path = tmp_path / "normalized_cells.json"
    cells_path.write_text(json.dumps([cell]))
    (tmp_path / "manifest.json").write_text(json.dumps(successful_manifest()))

    # The successful manifest has no review: the planted review must not survive.
    cells = [cell]
    spawned_cells_to_ts.carry_sealed_run_metadata(cells, tmp_path)
    loaded = cells[0]
    assert "preSubmitReview" not in loaded
    run = spawned_cells_to_ts.to_forecast_cell(loaded)["predictionRun"]
    assert "preSubmitReview" not in run


def test_manifest_review_overrides_any_cell_claim(
    tmp_path: pathlib.Path,
) -> None:
    import json

    manifest = successful_manifest(
        preSubmitReview={
            "schemaVersion": "thesis_pre_submit_review_v1",
            "status": "completed",
            "summary": "Runner-sealed review.",
            "findings": [],
            "dispositions": [],
        }
    )
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    cell = stampable_cell()
    cell["runAt"] = "2026-07-01T04:00:00Z"
    cell["preSubmitReview"] = {"summary": "planted"}
    cells_path = tmp_path / "normalized_cells.json"
    cells_path.write_text(json.dumps([cell]))

    cells = [cell]
    spawned_cells_to_ts.carry_sealed_run_metadata(cells, tmp_path)
    loaded = cells[0]
    assert loaded["preSubmitReview"]["summary"] == "Runner-sealed review."
    run = spawned_cells_to_ts.to_forecast_cell(loaded)["predictionRun"]
    assert run["preSubmitReview"]["summary"] == "Runner-sealed review."


def test_brier_judge_review_is_manifest_only_and_screened() -> None:
    # Round-two screen review: the Brier-judge prompt builder fell back
    # to cell.preSubmitReview and compacted it unscreened.
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
    try:
        import run_brier_reasoning_judge as judge
    finally:
        sys.path.pop(0)
    marker = spawned_cells_to_ts.PRIVATE_SOURCE_MARKER
    screened = judge._screened_manifest_review(
        {
            "preSubmitReview": {
                "status": "completed",
                "summary": "Attach the fetch transcript next time.",
                "findings": [],
                "dispositions": [],
            }
        }
    )
    assert screened["summary"] == marker
    assert judge._screened_manifest_review({}) is None
    with pytest.raises(ValueError, match="preSubmitReview is invalid"):
        judge._screened_manifest_review({"preSubmitReview": ["not-a-dict"]})


def test_screen_engines_fold_ascii_only() -> None:
    # Python IGNORECASE is Unicode-aware; JavaScript's bare "i" flag is
    # not. The screen compiles ASCII so the engines agree: a long-s
    # "tranſcript" must NOT match in either engine.
    assert not spawned_cells_to_ts.PRIVATE_SOURCE_RE.search("a tranſcript here")
    assert spawned_cells_to_ts.PRIVATE_SOURCE_RE.search("a TRANSCRIPT here")


def test_judge_loader_screens_review_end_to_end(tmp_path: pathlib.Path) -> None:
    # Round-four screen review: the earlier regression tested only the
    # helper; a leaky loader stayed green. This drives load_batch_runs
    # over a real batch/manifest/cells fixture whose manifest review
    # hides a screened token inside a dict KEY.
    import json

    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
    try:
        import run_brier_reasoning_judge as judge
    finally:
        sys.path.pop(0)
    cells_path = tmp_path / "cells.json"
    cells_path.write_text(
        json.dumps(
            [
                {
                    "runAt": "2026-08-12T00:00:00Z",
                    "slug": "fixture-cell",
                    "title": "t",
                    "question": "q",
                    "unit": "percent",
                    "pointEstimate": 1.0,
                    "ciLow": 0.5,
                    "ciHigh": 1.5,
                    "resolutionDate": "2026-12-31",
                    "resolutionRule": "r",
                    "sourceContext": [],
                    "drivers": [],
                    "reasoning": [],
                    # Agent-planted: must never reach the judge prompt.
                    "preSubmitReview": {"summary": "planted Granola export"},
                }
            ]
        )
    )
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "cellsPath": str(cells_path),
                "preSubmitReview": {
                    "status": "completed",
                    "summary": "Fine run.",
                    "findings": [
                        {
                            "findingId": "review.finding.1",
                            "severity": "info",
                            "rubricItem": "review",
                            # Screened reviewer wording in a retained field.
                            "summary": "Consider attaching the fetch transcript.",
                        }
                    ],
                    "dispositions": [],
                },
            }
        )
    )
    batch_path = tmp_path / "batch.json"
    batch_path.write_text(
        json.dumps(
            {
                "results": [
                    {"ok": True, "manifestPath": str(manifest_path), "target": {}}
                ]
            }
        )
    )
    runs = judge.load_batch_runs([batch_path], max_runs=5)
    assert len(runs) == 1
    blob = json.dumps(runs, ensure_ascii=False)
    marker = spawned_cells_to_ts.PRIVATE_SOURCE_MARKER
    assert marker in blob
    assert "planted" not in blob
    assert not spawned_cells_to_ts.PRIVATE_SOURCE_RE.search(blob.replace(marker, ""))
    # A malformed dict where the summary string belongs refuses with a
    # typed error instead of smuggling content past compaction.
    manifest_path.write_text(
        json.dumps(
            {
                "cellsPath": str(cells_path),
                "preSubmitReview": {"summary": {"fetch transcript": "secret"}},
            }
        )
    )
    with pytest.raises(ValueError, match="summary must be a string"):
        judge.load_batch_runs([batch_path], max_runs=5)


def test_existing_slugs_sees_both_key_forms_and_rejects_lookalikes(
    tmp_path: pathlib.Path,
) -> None:
    # This script's own json.dumps output writes quoted keys; the scan
    # was blind to every auto-*.ts it generated until 2026-08-13 (PR
    # #181 review). It must see both forms, ignore suffix keys and
    # escaped JSON inside trace strings, and it remains a HEURISTIC:
    # dynamically constructed slugs are invisible, so publication
    # decisions use the evaluated catalog, never this scan.
    site_data = tmp_path
    (site_data / "forecast-examples").mkdir()
    # A commented-out literal still counts: the scan reads source text,
    # and over-matching only makes the collision guard more conservative.
    (site_data / "forecast-examples" / "a.ts").write_text(
        'export const A = [{ slug: "bare-one" }];\n// slug: "commented-four"\n'
    )
    (site_data / "forecast-examples" / "auto-b.ts").write_text(
        '[{ "slug": "quoted-two",'
        ' "trace": "{\\"slug\\": \\"escaped-never\\"}",'
        ' "myslug": "suffix-never", relatedSlug: "camel-never" }]\n'
    )
    (site_data / "forecast-cells.ts").write_text(
        'const CELLS = [{ slug: "cells-three" }];\n'
    )
    got = spawned_cells_to_ts.existing_slugs(site_data, site_data / "__none__.ts")
    assert got == {"bare-one", "quoted-two", "cells-three", "commented-four"}
