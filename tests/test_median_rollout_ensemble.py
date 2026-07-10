from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import docket_publication  # noqa: E402
import median_rollout_ensemble as median  # noqa: E402
import run_thesis_analyst as analyst  # noqa: E402
import verify_custody  # noqa: E402
from canonical_json import canonical_bytes, canonical_sha256  # noqa: E402
from verify_custody import CustodyError, verify_run  # noqa: E402


def target_context() -> dict:
    return {
        "series": "agency.test.rate",
        "period": "2030-01",
        "catalogSlug": "agency-test-rate-january-2030",
        "country": "US",
        "dataPointId": "agency.test.rate.2030_01.first_print",
        "targetUnit": "percent",
        "valueScale": 1,
        "sourceBinding": {
            "adapter": "generic-url",
            "sourceUrl": "https://agency.example/rate",
            "allowedHosts": ["agency.example"],
        },
        "resolutionDate": "2030-02-15",
        "resolutionSource": "Agency",
        "resolutionSourceUrl": "https://agency.example/rate",
        "resolutionRule": "Use the first official print only.",
        "resolutionPolicy": "first_print",
        "registeredAtUtc": "2030-01-01T00:00:00Z",
        "registrationCommit": "a" * 40,
        "targetContentHash": "b" * 64,
        "targetRegistrationPath": f"records/targets/2030-01-01-{'b' * 64}.json",
        "comparisonTarget": True,
    }


def parent_cell(index: int, run_at: str) -> dict:
    point = 10 + index
    target = target_context()
    return {
        "slug": target["catalogSlug"],
        "country": target["country"],
        "type": "data",
        "title": "Agency rate",
        "question": "What will the agency rate be?",
        "unit": target["targetUnit"],
        "resolutionDate": target["resolutionDate"],
        "resolutionSource": target["resolutionSource"],
        "resolutionSourceUrl": target["resolutionSourceUrl"],
        "resolutionRule": target["resolutionRule"],
        "resolutionPolicy": target["resolutionPolicy"],
        "dataPointId": target["dataPointId"],
        "historicalContext": [],
        "pointEstimate": point,
        "ciLow": point - 2,
        "ciHigh": point + 2,
        "confidence": 0.8,
        "drivers": ["fixture"],
        "sourceContext": [target["resolutionSourceUrl"]],
        "reasoning": [
            {"kind": "heading", "text": "Fixture"},
            {
                "kind": "forecast",
                "point": point,
                "ciLow": point - 2,
                "ciHigh": point + 2,
            },
        ],
        "runStartedAt": run_at,
        "runAt": run_at,
        **{
            field: target[field]
            for field in (
                "registrationCommit",
                "targetContentHash",
                "targetRegistrationPath",
                "registeredAtUtc",
            )
        },
    }


def write_parent(repo: pathlib.Path, index: int, run_at: str) -> dict:
    stamp = run_at.lower().replace(":", "-")
    run_dir = (
        repo / "records" / "thesis-analyst" / run_at[:10] / f"{stamp}-parent-{index}"
    )
    cell = parent_cell(index, run_at)
    refs = [
        analyst.write_artifact(run_dir, "prompt", "prompt.md", "prompt\n", run_at),
        analyst.write_artifact(
            run_dir,
            "command",
            "command.json",
            json.dumps({"backend": "mock", "argv": []}),
            run_at,
        ),
        analyst.write_artifact(run_dir, "stdout", "stdout.txt", "{}\n", run_at),
        analyst.write_artifact(run_dir, "stderr", "stderr.txt", "", run_at),
        analyst.write_artifact(
            run_dir, "raw_response", "raw_response.txt", "{}\n", run_at
        ),
        analyst.write_artifact(
            run_dir, "parsed_cell", "parsed_cells.json", json.dumps([cell]), run_at
        ),
        analyst.write_artifact(
            run_dir,
            "normalized_cell",
            "normalized_cells.json",
            json.dumps([cell]),
            run_at,
        ),
        analyst.write_artifact(
            run_dir,
            "run_distribution",
            "distribution.json",
            json.dumps(analyst.interval_distribution(cell)),
            run_at,
        ),
        analyst.write_artifact(
            run_dir,
            "validation_report",
            "validation.json",
            json.dumps({"ok": True, "cells": []}),
            run_at,
        ),
    ]
    cell["activityLog"] = list(refs)
    refs.append(
        analyst.write_artifact(
            run_dir,
            "cells_with_activity",
            "cells.with_activity.json",
            json.dumps([cell]),
            run_at,
        )
    )
    manifest = {
        "schemaVersion": "thesis_analyst_run_manifest_v1",
        "createdAt": run_at,
        "runStartedAt": run_at,
        "series": target_context()["series"],
        "period": target_context()["period"],
        "conditional": None,
        "targetContext": target_context(),
        "promptMode": "fast",
        "agent": {
            "agent": "thesis.analyst",
            "model": "fixture",
            "agentVersion": "fixture",
        },
        "preSubmitReview": None,
        "ok": True,
        "cellsPath": analyst.repo_relative(run_dir / "cells.with_activity.json"),
        "artifacts": refs,
        "validation": {"ok": True, "cells": []},
        **{
            field: target_context()[field]
            for field in (
                "registrationCommit",
                "targetContentHash",
                "targetRegistrationPath",
                "registeredAtUtc",
            )
        },
    }
    analyst.finalize_manifest(run_dir, run_at, manifest, refs)
    return {
        "target": target_context(),
        "cell": cell,
        "manifestPath": analyst.repo_relative(run_dir / "manifest.json"),
        "cellsPath": analyst.repo_relative(run_dir / "cells.with_activity.json"),
    }


@pytest.fixture
def derived_run(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    monkeypatch.setattr(analyst, "ROOT", repo)
    monkeypatch.setattr(median, "ROOT", repo)
    monkeypatch.setattr(verify_custody, "REPOSITORY_ROOT", repo)
    parents = [
        write_parent(repo, 1, "2030-01-10T12:00:01Z"),
        write_parent(repo, 2, "2030-01-10T12:00:02Z"),
        write_parent(repo, 3, "2030-01-10T12:00:03Z"),
    ]
    manifest, manifest_path = median.build_derived_run(
        target_context()["catalogSlug"],
        list(reversed(parents)),
        "2030-01-10T12:01:00Z",
        sealed_at="2030-01-10T12:01:01Z",
    )
    return repo, parents, manifest, manifest_path


def test_median_writer_emits_timestamp_first_complete_v2_custody(derived_run):
    repo, parents, manifest, manifest_path = derived_run
    assert docket_publication.RUN_MANIFEST_RE.fullmatch(
        manifest_path.relative_to(repo).as_posix()
    )
    verification = verify_run(manifest_path.parent)
    assert verification.run_mode == "derived_ensemble"
    assert verification.inventory_status == "complete"
    assert verification.run_succeeded is True
    assert manifest["runStartedAt"] == "2030-01-10T12:01:00Z"
    assert len({row["custodyRootSha256"] for row in manifest["constituentRuns"]}) == 3
    assert [row["runAt"] for row in manifest["constituentRuns"]] == sorted(
        parent["cell"]["runAt"] for parent in parents
    )


def test_new_median_missing_root_is_not_grandfathered(derived_run):
    _, _, _, manifest_path = derived_run
    (manifest_path.parent / "custody_root.json").unlink()
    with pytest.raises(CustodyError, match="missing custody root"):
        verify_run(manifest_path.parent)


def test_new_median_cells_path_cannot_alias_a_parent(derived_run):
    _, parents, _, manifest_path = derived_run
    manifest = json.loads(manifest_path.read_text())
    custody_path = manifest_path.parent / "custody_root.json"
    custody = json.loads(custody_path.read_text())
    manifest["cellsPath"] = parents[0]["cellsPath"]

    manifest.pop("custodyRootSha256")
    self_ref = next(
        ref for ref in manifest["artifacts"] if ref["artifactType"] == "manifest"
    )
    self_bytes = canonical_bytes(verify_custody._self_hash_payload(manifest))
    self_ref["sha256"] = verify_custody._sha256(self_bytes)
    self_ref["bytes"] = len(self_bytes)
    custody["manifestWithoutCustodyRoot"]["canonicalJsonSha256"] = canonical_sha256(
        manifest
    )
    custody_path.write_text(json.dumps(custody, indent=2) + "\n")
    manifest["custodyRootSha256"] = canonical_sha256(custody)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    with pytest.raises(CustodyError, match="resolve inside run|outside its run"):
        verify_run(manifest_path.parent)


def test_median_rejects_duplicate_constituent_roots(derived_run):
    _, parents, _, _ = derived_run
    duplicate = [parents[0], parents[0], parents[2]]
    with pytest.raises(ValueError, match="3 distinct custody-verifiable"):
        median.validate_constituent_rollouts(duplicate)


def test_median_rejects_fewer_than_three_constituent_roots(derived_run):
    _, parents, _, _ = derived_run
    with pytest.raises(ValueError, match="exactly 3 constituent"):
        median.validate_constituent_rollouts(parents[:2])


def test_derived_custody_rechecks_parent_manifest_bytes(derived_run):
    repo, parents, _, manifest_path = derived_run
    parent_manifest = repo / parents[0]["manifestPath"]
    parent_manifest.write_text(parent_manifest.read_text() + "\n")
    with pytest.raises(CustodyError, match="constituent manifest integrity"):
        verify_run(manifest_path.parent)


def test_all_published_july8_medians_are_narrow_legacy_records():
    run_dirs = sorted((ROOT / "records/thesis-analyst/2026-07-08").glob("*-median3-*"))
    assert len(run_dirs) == 6
    assert {run_dir.name for run_dir in run_dirs} == verify_custody.LEGACY_DERIVED_DIRS
    for run_dir in run_dirs:
        verification = verify_run(run_dir)
        assert verification.run_mode == "derived_ensemble"
        assert verification.inventory_status == "legacy-incomplete"
        assert verification.headline_eligible is False
