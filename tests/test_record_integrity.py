from __future__ import annotations

import hashlib
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from canonical_json import canonical_stringify  # noqa: E402
from run_thesis_analyst import finalize_manifest, write_artifact  # noqa: E402
from verify_custody import CustodyError, verify_run  # noqa: E402
from verify_record_chain import ChainError, verify_records  # noqa: E402


def write_json(path: pathlib.Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def add_witness(snapshot: pathlib.Path) -> None:
    write_json(
        snapshot.with_suffix(".witness.json"),
        {
            "schemaVersion": "thesis_rfc3161_witness_v1",
            "status": "unavailable",
            "digestSha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
            "reason": "synthetic test fixture",
        },
    )


@pytest.fixture
def synthetic_chain(tmp_path: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]:
    records = tmp_path / "records"
    legacy = records / "2026-01-01" / "digest.json"
    write_json(legacy, {"legacy": True})
    first = records / "2026-01-02" / "digest-genesis.json"
    write_json(
        first,
        {
            "schemaVersion": "thesis_record_snapshot_v2",
            "snapshotKind": "chain_genesis_cutover",
            "runId": "genesis",
            "recordedAt": "2026-01-02T00:00:00Z",
        },
    )
    add_witness(first)
    second = records / "2026-01-03" / "digest-100.json"
    write_json(
        second,
        {
            "schemaVersion": "thesis_record_snapshot_v2",
            "snapshotKind": "recorder_run",
            "runId": "100",
            "recordedAt": "2026-01-03T00:00:00Z",
            "chain": {
                "prevDigestPath": "records/2026-01-02/digest-genesis.json",
                "prevDigestSha256": hashlib.sha256(first.read_bytes()).hexdigest(),
            },
        },
    )
    add_witness(second)
    write_json(
        records / "CHAIN_GENESIS.json",
        {
            "schemaVersion": "thesis_record_chain_genesis_v1",
            "firstSnapshot": "records/2026-01-02/digest-genesis.json",
            "legacyDigests": [
                {
                    "path": "records/2026-01-01/digest.json",
                    "sha256": hashlib.sha256(legacy.read_bytes()).hexdigest(),
                }
            ],
        },
    )
    write_json(
        records / "CHAIN_HEAD.json",
        {
            "schemaVersion": "thesis_record_chain_head_v1",
            "snapshotPath": "records/2026-01-03/digest-100.json",
            "snapshotSha256": hashlib.sha256(second.read_bytes()).hexdigest(),
        },
    )
    return records, second


def test_record_chain_fails_when_a_post_genesis_link_is_deleted(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path],
) -> None:
    records, second = synthetic_chain
    assert len(verify_records(records)) == 2

    payload = json.loads(second.read_text())
    del payload["chain"]
    write_json(second, payload)

    with pytest.raises(ChainError, match="missing chain block after genesis"):
        verify_records(records)


def test_record_chain_fails_when_a_linked_snapshot_is_missing(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path],
) -> None:
    records, second = synthetic_chain
    third = records / "2026-01-04" / "digest-101.json"
    write_json(
        third,
        {
            "schemaVersion": "thesis_record_snapshot_v2",
            "snapshotKind": "recorder_run",
            "runId": "101",
            "recordedAt": "2026-01-04T00:00:00Z",
            "chain": {
                "prevDigestPath": "records/2026-01-03/digest-100.json",
                "prevDigestSha256": hashlib.sha256(second.read_bytes()).hexdigest(),
            },
        },
    )
    add_witness(third)
    write_json(
        records / "CHAIN_HEAD.json",
        {
            "schemaVersion": "thesis_record_chain_head_v1",
            "snapshotPath": "records/2026-01-04/digest-101.json",
            "snapshotSha256": hashlib.sha256(third.read_bytes()).hexdigest(),
        },
    )
    second.unlink()
    second.with_suffix(".witness.json").unlink()

    with pytest.raises(ChainError, match="missing predecessor"):
        verify_records(records)


def test_record_chain_head_detects_deleted_tail(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path],
) -> None:
    records, second = synthetic_chain
    second.unlink()
    second.with_suffix(".witness.json").unlink()

    with pytest.raises(ChainError, match="chain head path mismatch"):
        verify_records(records)


@pytest.fixture
def synthetic_custody_run(tmp_path: pathlib.Path) -> pathlib.Path:
    run_dir = tmp_path / "run"
    created_at = "2026-01-01T00:00:00Z"
    refs = [
        write_artifact(run_dir, "prompt", "prompt.md", "forecast prompt\n", created_at),
        write_artifact(
            run_dir,
            "command",
            "command.json",
            json.dumps({"argv": ["agent"]}, indent=2),
            created_at,
        ),
        write_artifact(
            run_dir,
            "normalized_cell",
            "normalized_cells.json",
            json.dumps([{"slug": "synthetic", "pointEstimate": 1.5}], indent=2),
            created_at,
        ),
        write_artifact(
            run_dir,
            "cells_with_activity",
            "cells.with_activity.json",
            json.dumps([{"slug": "synthetic", "pointEstimate": 1.5}], indent=2),
            created_at,
        ),
    ]
    manifest = {
        "schemaVersion": "thesis_analyst_run_manifest_v1",
        "createdAt": created_at,
        "ok": True,
        "cellsPath": str(run_dir / "cells.with_activity.json"),
        "artifacts": refs,
    }
    finalize_manifest(run_dir, created_at, manifest, refs)
    return run_dir


def test_custody_verifier_accepts_fixture_and_rejects_changed_scored_cells(
    synthetic_custody_run: pathlib.Path,
) -> None:
    verify_run(synthetic_custody_run)
    cells = synthetic_custody_run / "cells.with_activity.json"
    cells.write_text(cells.read_text().replace("1.5", "9.5"))

    with pytest.raises(CustodyError, match="raw SHA-256 mismatch"):
        verify_run(synthetic_custody_run)


def test_python_canonical_json_uses_true_utf16_key_order() -> None:
    value = {"\ue000": 3, "😀": 2, "\ud7ff": 1, "nested": {"z": -0.0, "a": 1e-7}}
    assert canonical_stringify(value) == (
        '{"nested":{"a":1e-7,"z":0},"\ud7ff":1,"😀":2,"\ue000":3}'
    )
