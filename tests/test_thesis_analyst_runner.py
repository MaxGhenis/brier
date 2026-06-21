from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_thesis_analyst.py"
COMPARISON_GENERATOR = ROOT / "scripts" / "thesis_records_to_comparisons.py"


def test_print_prompt_contains_question_spec():
    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--series",
            "ons.labour.unemployment_rate",
            "--period",
            "2026-Q4",
            "--print-prompt",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "# Question spec" in result.stdout
    assert "- series: ons.labour.unemployment_rate" in result.stdout
    assert "- period: 2026-Q4" in result.stdout
    assert "Produce one JSON cell per docs/cell-contract.md" in result.stdout
    assert "Default promoted practices" in result.stdout
    assert "outside-view base rate before current-news adjustments" in result.stdout


def test_fast_prompt_inlines_contract_and_forbids_repo_reads():
    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--series",
            "boe.bank_rate",
            "--period",
            "2026-06-18",
            "--prompt-mode",
            "fast",
            "--print-prompt",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "# Thesis analyst fast public-release run" in result.stdout
    assert "Do not inspect the local repository" in result.stdout
    assert "# Default promoted forecasting practices" in result.stdout
    assert "Anchor on the outside-view base rate before current-release" in (
        result.stdout
    )
    assert '"resolutionDate": "YYYY-MM-DD"' in result.stdout
    assert "Every tool step result must include at least one fetched numeric" in (
        result.stdout
    )
    assert "- series: boe.bank_rate" in result.stdout
    assert "Bank of England MPC" in result.stdout
    assert "docs/cell-contract.md" not in result.stdout


def test_mock_run_writes_activity_artifacts(tmp_path):
    out_dir = tmp_path / "run"

    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--series",
            "test.synthetic_rate",
            "--period",
            "2030-01",
            "--mock-cell",
            "--out-dir",
            str(out_dir),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    manifest = json.loads((out_dir / "manifest.json").read_text())
    printed_manifest = json.loads(result.stdout)
    assert manifest["schemaVersion"] == "thesis_analyst_run_manifest_v1"
    assert printed_manifest["ok"] is True
    assert manifest["ok"] is True
    assert manifest["series"] == "test.synthetic_rate"
    assert manifest["period"] == "2030-01"
    assert manifest["promptMode"] == "full"

    artifact_types = {artifact["artifactType"] for artifact in manifest["artifacts"]}
    assert {
        "prompt",
        "command",
        "raw_response",
        "parsed_cell",
        "normalized_cell",
        "validation_report",
        "manifest",
    }.issubset(artifact_types)

    for artifact in manifest["artifacts"]:
        path = ROOT / artifact["path"]
        if not path.exists():
            path = Path(artifact["path"])
        assert path.exists()
        assert artifact["sha256"]
        assert artifact["bytes"] > 0

    cells = json.loads((out_dir / "cells.with_activity.json").read_text())
    assert len(cells) == 1
    cell = cells[0]
    assert cell["slug"] == "test-synthetic-rate-2030-01"
    assert cell["activityLog"]
    activity_types = {artifact["artifactType"] for artifact in cell["activityLog"]}
    assert {"prompt", "raw_response", "validation_report"}.issubset(activity_types)
    assert manifest["validation"]["cells"][0]["ok"] is True


def test_fast_mock_run_records_prompt_mode(tmp_path):
    out_dir = tmp_path / "fast-run"

    subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--series",
            "boe.bank_rate",
            "--period",
            "2026-06-18",
            "--prompt-mode",
            "fast",
            "--mock-cell",
            "--out-dir",
            str(out_dir),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    manifest = json.loads((out_dir / "manifest.json").read_text())
    prompt = (out_dir / "prompt.md").read_text()

    assert manifest["promptMode"] == "fast"
    assert "Do not inspect the local repository" in prompt


def test_command_model_override_is_stamped_in_manifest_and_cells(tmp_path):
    out_dir = tmp_path / "model-run"
    response_path = tmp_path / "response.json"
    response_path.write_text(
        json.dumps(
            [
                {
                    "slug": "test-runtime-model-2030-01",
                    "country": "US",
                    "type": "data",
                    "title": "Runtime model test forecast",
                    "question": (
                        "What will the first-print value of the synthetic "
                        "runtime-model test series be for January 2030?"
                    ),
                    "unit": "percent",
                    "pointEstimate": 5.1,
                    "ciLow": 4.7,
                    "ciHigh": 5.8,
                    "confidence": 0.8,
                    "resolutionDate": "2030-01-15",
                    "resolutionSource": "Official synthetic release",
                    "resolutionSourceUrl": "https://example.com/runtime-model",
                    "resolutionRule": (
                        "Resolves to the first official synthetic release "
                        "value for January 2030; later revisions do not count."
                    ),
                    "dataPointId": "test.runtime_model.january_2030.first_print",
                    "historicalContext": [
                        {"label": "t-3", "value": 4.9},
                        {"label": "t-2", "value": 5.0},
                        {"label": "t-1", "value": 5.2},
                    ],
                    "drivers": [
                        "recent reference class",
                        "stable monthly series",
                        "synthetic release volatility",
                    ],
                    "sourceContext": [
                        "https://example.com/runtime-model",
                        "https://example.com/runtime-model-calendar",
                    ],
                    "runAt": "2026-06-17T10:00:00Z",
                    "reasoning": [
                        {"kind": "heading", "text": "Runtime model forecast"},
                        {
                            "kind": "text",
                            "text": (
                                "The base-rate reference class is the last "
                                "three synthetic prints around 5.0 percent."
                            ),
                        },
                        {
                            "kind": "tool",
                            "tool": "official.lookup",
                            "call": "lookup synthetic latest values",
                            "result": "Fetched t-3 4.9, t-2 5.0, t-1 5.2.",
                        },
                        {
                            "kind": "tool",
                            "tool": "calendar.lookup",
                            "call": "lookup synthetic release date",
                            "result": "Fetched release date 2030-01-15.",
                        },
                        {
                            "kind": "math",
                            "text": (
                                "Center on the 5.1 recent mean and use an "
                                "80% interval from 4.7 to 5.8."
                            ),
                        },
                        {
                            "kind": "text",
                            "text": (
                                "Outside the interval if the synthetic series "
                                "breaks from its recent stable pattern."
                            ),
                        },
                        {
                            "kind": "forecast",
                            "point": 5.1,
                            "ciLow": 4.7,
                            "ciHigh": 5.8,
                        },
                    ],
                }
            ]
        )
    )

    subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--series",
            "test.runtime_model",
            "--period",
            "2030-01",
            "--command",
            (
                f"{sys.executable} -c 'import pathlib, sys; "
                "print(pathlib.Path(sys.argv[1]).read_text())' "
                f"{response_path} --model gpt-5.5-mini"
            ),
            "--out-dir",
            str(out_dir),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    manifest = json.loads((out_dir / "manifest.json").read_text())
    cells = json.loads((out_dir / "cells.with_activity.json").read_text())

    assert manifest["agent"]["model"] == "gpt-5.5-mini"
    assert manifest["agent"]["configuredModel"] == "claude-fable-5"
    assert cells[0]["model"] == "gpt-5.5-mini"


def test_command_timeout_writes_failure_manifest(tmp_path):
    out_dir = tmp_path / "timeout-run"

    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--series",
            "test.synthetic_rate",
            "--period",
            "2030-01",
            "--command",
            f"{sys.executable} -c 'import time; time.sleep(2)'",
            "--timeout-seconds",
            "1",
            "--out-dir",
            str(out_dir),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    command = json.loads((out_dir / "command.json").read_text())
    manifest = json.loads((out_dir / "manifest.json").read_text())
    error = json.loads((out_dir / "error.json").read_text())

    assert command["returnCode"] == 124
    assert command["timedOut"] is True
    assert manifest["ok"] is False
    assert manifest["error"]["phase"] == "parse"
    assert error["command"]["timedOut"] is True


def test_comparison_generator_maps_and_scales_claims_record(tmp_path):
    record_dir = tmp_path / "record"
    record_dir.mkdir()
    cells_path = record_dir / "cells.with_activity.json"
    command_path = record_dir / "command.json"
    manifest_path = record_dir / "manifest.json"
    out_ts = tmp_path / "live-comparisons.ts"

    command_path.write_text(
        json.dumps({"argv": ["codex", "exec", "-m", "gpt-5.5", "-"]})
    )
    cells_path.write_text(
        json.dumps(
            [
                {
                    "slug": (
                        "us-dol-initial-claims-sa-week-2026-06-13-first-print"
                    ),
                    "pointEstimate": 225000,
                    "ciLow": 209000,
                    "ciHigh": 243000,
                    "confidence": 0.8,
                    "drivers": ["latest print rose to 229000"],
                    "sourceContext": ["https://www.dol.gov/ui/data.pdf"],
                    "runAt": "2026-06-16T12:33:22Z",
                    "reasoning": [
                        {"kind": "heading", "text": "Claims"},
                        {
                            "kind": "forecast",
                            "point": 225000,
                            "ciLow": 209000,
                            "ciHigh": 243000,
                        },
                    ],
                }
            ]
        )
    )
    manifest_path.write_text(
        json.dumps(
            {
                "ok": True,
                "promptMode": "fast",
                "cellsPath": str(cells_path),
                "agent": {
                    "agent": "thesis.analyst",
                    "model": "claude-fable-5",
                    "agentVersion": "2.0.0",
                    "promptHash": "prompt-hash",
                    "toolPolicyHash": "tool-hash",
                },
                "artifacts": [
                    {
                        "artifactType": "command",
                        "path": str(command_path),
                        "sha256": "abc",
                        "bytes": 1,
                        "createdAt": "2026-06-16T12:33:11Z",
                    }
                ],
            }
        )
    )

    subprocess.run(
        [
            sys.executable,
            str(COMPARISON_GENERATOR),
            str(out_ts),
            "LIVE_RUNS",
            str(manifest_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    output = out_ts.read_text()
    assert '"initial-claims-week-2026-06-13"' in output
    assert '"pointEstimate": 225' in output
    assert '"ciLow": 209' in output
    assert '"model": "gpt-5.5"' in output
    assert '"promptMode": "fast"' in output


def test_comparison_generator_uses_batch_manifest_catalog_slug(tmp_path):
    record_dir = tmp_path / "record"
    record_dir.mkdir()
    cells_path = record_dir / "cells.with_activity.json"
    command_path = record_dir / "command.json"
    manifest_path = record_dir / "manifest.json"
    batch_manifest_path = tmp_path / "batch.json"
    out_ts = tmp_path / "live-comparisons.ts"

    command_path.write_text(
        json.dumps({"argv": ["codex", "exec", "-m", "gpt-5.5", "-"]})
    )
    cells_path.write_text(
        json.dumps(
            [
                {
                    "slug": "agent-emitted-near-duplicate-slug",
                    "pointEstimate": 4.2,
                    "ciLow": 3.6,
                    "ciHigh": 4.8,
                    "confidence": 0.8,
                    "drivers": ["official monthly indicator is noisy"],
                    "sourceContext": ["https://www.abs.gov.au/statistics"],
                    "runAt": "2026-06-17T02:10:00Z",
                    "reasoning": [
                        {"kind": "heading", "text": "ABS CPI"},
                        {
                            "kind": "forecast",
                            "point": 4.2,
                            "ciLow": 3.6,
                            "ciHigh": 4.8,
                        },
                    ],
                }
            ]
        )
    )
    manifest_path.write_text(
        json.dumps(
            {
                "ok": True,
                "promptMode": "fast",
                "cellsPath": str(cells_path),
                "agent": {
                    "agent": "thesis.analyst",
                    "model": "claude-fable-5",
                    "agentVersion": "2.0.0",
                    "promptHash": "prompt-hash",
                    "toolPolicyHash": "tool-hash",
                },
                "artifacts": [
                    {
                        "artifactType": "command",
                        "path": str(command_path),
                        "sha256": "abc",
                        "bytes": 1,
                        "createdAt": "2026-06-17T02:10:00Z",
                    }
                ],
            }
        )
    )
    batch_manifest_path.write_text(
        json.dumps(
            {
                "schemaVersion": "thesis_batch_manifest_v1",
                "results": [
                    {
                        "ok": True,
                        "manifestPath": str(manifest_path),
                        "target": {
                            "series": "abs.cpi.all_groups.yoy",
                            "period": "2026-05",
                            "catalogSlug": "australia-cpi-annual-rate-may-2026",
                        },
                    }
                ],
            }
        )
    )

    subprocess.run(
        [
            sys.executable,
            str(COMPARISON_GENERATOR),
            str(out_ts),
            "LIVE_RUNS",
            str(manifest_path),
            "--batch-manifest",
            str(batch_manifest_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    output = out_ts.read_text()
    assert '"australia-cpi-annual-rate-may-2026"' in output
    assert '"agent-emitted-near-duplicate-slug"' not in output
    assert '"pointEstimate": 4.2' in output


def test_comparison_generator_does_not_rescale_matching_target_unit(tmp_path):
    record_dir = tmp_path / "record"
    record_dir.mkdir()
    cells_path = record_dir / "cells.with_activity.json"
    command_path = record_dir / "command.json"
    manifest_path = record_dir / "manifest.json"
    batch_manifest_path = tmp_path / "batch.json"
    out_ts = tmp_path / "live-comparisons.ts"

    command_path.write_text(
        json.dumps({"argv": ["codex", "exec", "-m", "gpt-5.5", "-"]})
    )
    cells_path.write_text(
        json.dumps(
            [
                {
                    "slug": "us-dol-initial-claims-sa-week-2026-06-20",
                    "unit": "thousands",
                    "pointEstimate": 225,
                    "ciLow": 208,
                    "ciHigh": 243,
                    "confidence": 0.8,
                    "drivers": ["latest print was 245 thousand"],
                    "sourceContext": ["https://www.dol.gov/ui/data.pdf"],
                    "runAt": "2026-06-21T15:11:54Z",
                    "reasoning": [
                        {"kind": "heading", "text": "Claims"},
                        {
                            "kind": "forecast",
                            "point": 225,
                            "ciLow": 208,
                            "ciHigh": 243,
                        },
                    ],
                }
            ]
        )
    )
    manifest_path.write_text(
        json.dumps(
            {
                "ok": True,
                "promptMode": "fast",
                "cellsPath": str(cells_path),
                "agent": {
                    "agent": "thesis.analyst",
                    "model": "gpt-5.5",
                    "agentVersion": "2.0.0",
                    "promptHash": "prompt-hash",
                    "toolPolicyHash": "tool-hash",
                },
                "artifacts": [
                    {
                        "artifactType": "command",
                        "path": str(command_path),
                        "sha256": "abc",
                        "bytes": 1,
                        "createdAt": "2026-06-21T15:11:48Z",
                    }
                ],
            }
        )
    )
    batch_manifest_path.write_text(
        json.dumps(
            {
                "schemaVersion": "thesis_batch_manifest_v1",
                "results": [
                    {
                        "ok": True,
                        "manifestPath": str(manifest_path),
                        "target": {
                            "series": "us.dol.initial_claims.sa",
                            "period": "week_2026-06-20",
                            "catalogSlug": "initial-claims-week-2026-06-20",
                            "valueScale": 0.001,
                            "targetUnit": "thousands",
                        },
                    }
                ],
            }
        )
    )

    subprocess.run(
        [
            sys.executable,
            str(COMPARISON_GENERATOR),
            str(out_ts),
            "LIVE_RUNS",
            str(manifest_path),
            "--batch-manifest",
            str(batch_manifest_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    output = out_ts.read_text()
    assert '"initial-claims-week-2026-06-20"' in output
    assert '"pointEstimate": 225' in output
    assert '"ciLow": 208' in output
    assert '"pointEstimate": 0.225' not in output
