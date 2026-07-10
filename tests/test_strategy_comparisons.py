from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import strategy_comparisons as strategy  # noqa: E402


def run(variant_id: str, run_at: str = "2030-01-01T00:00:00Z") -> dict:
    return {
        "variantId": variant_id,
        "predictionRun": {"runAt": run_at},
    }


def test_legacy_all_record_regeneration_is_byte_identical(
    tmp_path: pathlib.Path,
) -> None:
    output = tmp_path / "strategy.ts"
    augments = strategy.all_record_augments(
        legacy_index=strategy.LEGACY_INDEX,
        suites_root=tmp_path / "no-suites",
    )
    strategy.write_strategy_ts(output, augments)

    assert output.read_bytes() == (
        ROOT / "site/src/data/thesis-strategy-comparisons.ts"
    ).read_bytes()
    assert sum(map(len, augments.values())) == 30


def test_cli_always_regenerates_whole_corpus_and_rejects_partial_inputs(
    tmp_path: pathlib.Path,
) -> None:
    output = tmp_path / "strategy.ts"
    result = subprocess.run(
        [sys.executable, str(strategy.__file__), "--out", str(output)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert output.read_bytes() == (
        ROOT / "site/src/data/thesis-strategy-comparisons.ts"
    ).read_bytes()

    partial = subprocess.run(
        [
            sys.executable,
            str(strategy.__file__),
            "--ladder-batch",
            "records/example.json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert partial.returncode != 0
    assert "unrecognized arguments: --ladder-batch" in partial.stderr

    override = subprocess.run(
        [sys.executable, str(strategy.__file__), "--suites-root", str(tmp_path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert override.returncode != 0
    assert "unrecognized arguments: --suites-root" in override.stderr


def test_indexed_rollout_labels_are_fixed_within_each_suite(monkeypatch) -> None:
    target = {
        "catalogSlug": "example-target",
        "valueScale": 1,
        "targetUnit": "percent",
    }

    def results(paths):
        index = int(pathlib.Path(paths[0]).stem[-1])
        manifest = {
            "promptMode": "fast",
            "artifacts": [],
            "agent": {"agent": "thesis.analyst", "model": "fixture"},
        }
        cell = {
            "runAt": f"2030-01-01T00:00:0{index}Z",
            "sourceContext": [],
            "pointEstimate": index,
            "ciLow": index - 1,
            "ciHigh": index + 1,
            "confidence": 0.8,
            "drivers": [],
            "reasoning": [],
        }
        yield target, manifest, cell

    monkeypatch.setattr(strategy, "batch_results", results)
    first = strategy.indexed_rollout_augments(
        [
            (1, pathlib.Path("rollout-1")),
            (2, pathlib.Path("rollout-2")),
            (3, pathlib.Path("rollout-3")),
        ]
    )
    second = strategy.indexed_rollout_augments(
        [
            (1, pathlib.Path("second-1")),
            (2, pathlib.Path("second-2")),
            (3, pathlib.Path("second-3")),
        ]
    )

    assert [row["label"] for row in first["example-target"]] == [
        "Fast rollout 1 of 3",
        "Fast rollout 2 of 3",
        "Fast rollout 3 of 3",
    ]
    assert [row["label"] for row in second["example-target"]] == [
        "Fast rollout 1 of 3",
        "Fast rollout 2 of 3",
        "Fast rollout 3 of 3",
    ]


def test_suite_scanner_requires_exact_lane_shape(tmp_path: pathlib.Path) -> None:
    root = tmp_path / "strategy-suites"
    path = root / "2030-01-01" / "strategy-123-a1.json"
    path.parent.mkdir(parents=True)
    payload = {
        "schemaVersion": "thesis_strategy_suite_v1",
        "sourceSha": "a" * 40,
        "selectionPath": "records/selection.json",
        "selectionSha256": "b" * 64,
        "selectionSetHash": "c" * 64,
        "suite": "both",
        "createdAt": "2030-01-01T00:00:00Z",
        "lanes": {
            "ladder": {"batchManifest": "records/ladder.json"},
            "rollouts": [
                {"index": index, "batchManifest": f"records/rollout-{index}.json"}
                for index in range(1, 4)
            ],
            "median3": [
                {
                    "catalogSlug": "target",
                    "ok": False,
                    "manifestPath": None,
                    "error": "constituent failure",
                }
            ],
        },
    }
    path.write_text(json.dumps(payload))

    waves = strategy.load_suite_waves(root)
    assert [index for index, _path in waves[0]["rolloutBatches"]] == [1, 2, 3]

    payload["lanes"]["rollouts"].pop()
    path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="rollout lane cardinality"):
        strategy.load_suite_waves(root)

    payload["lanes"]["rollouts"] = [
        {"index": index, "batchManifest": f"records/rollout-{index}.json"}
        for index in range(1, 4)
    ]
    payload["suite"] = "median3"
    path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="median3-only suite has a ladder"):
        strategy.load_suite_waves(root)


def test_new_median_projects_verified_parent_activity(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    distribution_path = tmp_path / "distribution.json"
    distribution_path.write_text(
        json.dumps(
            {
                "format": "numeric_cdf_v1",
                "pointCount": 2,
                "support": {"lower": 0, "upper": 1},
                "points": [
                    {"value": 0, "probability": 0},
                    {"value": 1, "probability": 1},
                ],
                "summary": {
                    "pointEstimate": 0.5,
                    "median": 0.5,
                    "interval80": {"lower": 0.1, "upper": 0.9},
                },
                "provenance": "agent_reported",
            }
        )
    )
    parent_activity = [
        {"artifactType": "constituent_manifest", "path": f"parent-{index}.json"}
        for index in range(1, 4)
    ] + [{"artifactType": "derived_distribution", "path": str(distribution_path)}]
    cells_path = tmp_path / "cells.json"
    cells_path.write_text(
        json.dumps(
            [
                {
                    "unit": "percent",
                    "pointEstimate": 0.5,
                    "ciLow": 0.1,
                    "ciHigh": 0.9,
                    "activityLog": parent_activity,
                }
            ]
        )
    )
    constituent_runs = [
        {
            "manifestPath": f"parent-{index}.json",
            "custodyRootSha256": str(index) * 64,
        }
        for index in range(1, 4)
    ]
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "ok": True,
                "targetContext": {
                    "catalogSlug": "example-target",
                    "targetUnit": "percent",
                    "valueScale": 1,
                },
                "cellsPath": str(cells_path),
                "aggregationAlgorithmVersion": "pointwise_median_cdf_v1",
                "constituentRuns": constituent_runs,
                "artifacts": [
                    {
                        "artifactType": "derived_distribution",
                        "path": str(distribution_path),
                    }
                ],
            }
        )
    )
    monkeypatch.setattr(
        strategy,
        "comparison_run",
        lambda *_args, **_kwargs: {
            "description": "fixture",
            "predictionRun": {"activityLog": ["local-only"]},
        },
    )

    augments = strategy.median_augments([manifest_path])

    assert (
        augments["example-target"][0]["predictionRun"]["activityLog"]
        == parent_activity
    )
    assert (
        augments["example-target"][0]["predictionRun"]["constituentRuns"]
        == constituent_runs
    )


def test_strategy_custody_provenance_fields_are_typed() -> None:
    source = (ROOT / "site/src/data/forecast-cells.ts").read_text()

    assert "hashMode?: string;" in source
    assert "manifestSha256?: string;" in source
    assert "manifestBytes?: number;" in source


def test_merge_rejects_duplicate_variant_ids() -> None:
    with pytest.raises(ValueError, match="duplicate or missing strategy variantId"):
        strategy.merge(
            {"first": [run("duplicate")]},
            {"second": [run("duplicate", "2030-01-02T00:00:00Z")]},
        )
