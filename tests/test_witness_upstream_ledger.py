from __future__ import annotations

import gzip
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import witness_upstream_ledger as wul  # noqa: E402
from verify_custody import CustodyError, verify_run  # noqa: E402


def _jsonl_bytes(rows: list[dict]) -> bytes:
    return b"".join(
        json.dumps(row, separators=(",", ":")).encode() + b"\n" for row in rows
    )


def _witness_run(tmp_path: pathlib.Path, monkeypatch) -> pathlib.Path:
    monkeypatch.setattr(wul, "ROOT", tmp_path)
    run_dir = tmp_path / "records" / "2030-01-01" / "run-ledger-witness"
    run_dir.mkdir(parents=True)
    jsonl_raw = _jsonl_bytes(
        [
            {"source_record_id": "series.a.2030", "value": 1},
            {"source_record_id": "series.b.2030", "value": 2},
        ]
    )
    commit_raw = json.dumps({"sha": "b" * 40}).encode()
    upstream = [
        wul._archive(
            run_dir,
            "official-observations.jsonl",
            jsonl_raw,
            role="official_observations_jsonl",
            url="https://example.test/observations.jsonl",
        ),
        wul._archive(
            run_dir,
            "ledger-branch-commit.json",
            commit_raw,
            role="ledger_branch_commit_api",
            url="https://example.test/commit",
        ),
    ]
    manifest = {
        "schemaVersion": "thesis_ledger_witness_run_v1",
        "retrievedAt": "2030-01-01T00:00:00Z",
        "ledgerRepo": "PolicyEngine/ledger",
        "ledgerBranch": "codex/thesis-ledger-facts",
        "ledgerBranchSha": "b" * 40,
        "ledgerMainSha": "c" * 40,
        "jsonl": wul._validate_jsonl(jsonl_raw),
        "upstream": upstream,
    }
    wul._seal(run_dir, manifest)
    return run_dir


def test_witness_run_seals_and_verifies(tmp_path, monkeypatch) -> None:
    run_dir = _witness_run(tmp_path, monkeypatch)

    result = verify_run(run_dir)

    assert result.run_mode == "ledger_witness"
    assert result.inventory_status == "complete"
    assert result.headline_eligible is False
    manifest = json.loads((run_dir / "manifest.json").read_text())
    assert manifest["jsonl"]["lineCount"] == 2
    assert manifest["jsonl"]["sourceRecordIdCount"] == 2


def test_witness_run_detects_tampered_archive(tmp_path, monkeypatch) -> None:
    run_dir = _witness_run(tmp_path, monkeypatch)
    archive = run_dir / "upstream" / "official-observations.jsonl.gz"
    tampered = _jsonl_bytes(
        [
            {"source_record_id": "series.a.2030", "value": 999},
            {"source_record_id": "series.b.2030", "value": 2},
        ]
    )
    archive.write_bytes(gzip.compress(tampered, mtime=0))

    with pytest.raises(CustodyError):
        verify_run(run_dir)


def test_witness_run_requires_the_observations_archive(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setattr(wul, "ROOT", tmp_path)
    run_dir = tmp_path / "records" / "2030-01-01" / "run-ledger-witness"
    run_dir.mkdir(parents=True)
    jsonl_raw = _jsonl_bytes([{"source_record_id": "series.a.2030", "value": 1}])
    upstream = [
        wul._archive(
            run_dir,
            "ledger-branch-commit.json",
            json.dumps({"sha": "b" * 40}).encode(),
            role="ledger_branch_commit_api",
            url="https://example.test/commit",
        )
    ]
    manifest = {
        "schemaVersion": "thesis_ledger_witness_run_v1",
        "retrievedAt": "2030-01-01T00:00:00Z",
        "ledgerRepo": "PolicyEngine/ledger",
        "ledgerBranch": "codex/thesis-ledger-facts",
        "ledgerBranchSha": "b" * 40,
        "ledgerMainSha": "c" * 40,
        "jsonl": wul._validate_jsonl(jsonl_raw),
        "upstream": upstream,
    }

    with pytest.raises(CustodyError):
        wul._seal(run_dir, manifest)


def test_witness_run_detects_wrong_line_count_commitment(
    tmp_path, monkeypatch
) -> None:
    run_dir = _witness_run(tmp_path, monkeypatch)
    manifest_path = run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["jsonl"]["lineCount"] = 3

    # Rewriting the commitment invalidates the sealed manifest hashes first;
    # both failures are CustodyError and both fail closed.
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    with pytest.raises(CustodyError):
        verify_run(run_dir)
