from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

ingest = importlib.import_module("ingest_target_architecture")


PARITY_ROW = {
    "alpha": 1,
    "items": [True, None, 1e-7],
    "nested": {"😀": "astral", "\uffff": "bmp"},
    "timestamp": "2026-07-09T12:34:56Z",
}
PARITY_DIGEST = "e199cead09a282ee400e6dc9c5ab8b4c12822b75d25bc2fc84bc1a6652528402"


def test_row_digest_matches_typescript_parity_vector() -> None:
    assert ingest.row_digest(PARITY_ROW) == PARITY_DIGEST


def test_chunk_hash_excludes_only_the_root_reference() -> None:
    chunk = {
        "schemaVersion": ingest.CHUNK_SCHEMA,
        "projectionSchemaVersion": "thesis_target_architecture_projection_v1",
        "generatedAt": "2026-06-29T00:00:00+00:00",
        "projectionRootSha256": "a" * 64,
        "table": "targets",
        "chunkIndex": 0,
        "chunkSize": 10_000,
        "rowCount": 1,
        "rows": [PARITY_ROW],
    }

    first = ingest.canonical_sha256(ingest.chunk_hash_payload(chunk))
    chunk["projectionRootSha256"] = "b" * 64
    assert ingest.canonical_sha256(ingest.chunk_hash_payload(chunk)) == first
    chunk["rows"][0]["alpha"] = 2
    assert ingest.canonical_sha256(ingest.chunk_hash_payload(chunk)) != first


def test_dry_run_rejects_a_mixed_generation(tmp_path: Path) -> None:
    table_entries = []
    chunks = {}
    for table in ingest.TABLES:
        chunk = {
            "schemaVersion": ingest.CHUNK_SCHEMA,
            "projectionSchemaVersion": "thesis_target_architecture_projection_v1",
            "generatedAt": "2026-06-29T00:00:00+00:00",
            "projectionRootSha256": "0" * 64,
            "table": table,
            "chunkIndex": 0,
            "chunkSize": 10_000,
            "rowCount": 0,
            "rows": [],
        }
        reference = {
            "index": 0,
            "rowCount": 0,
            "url": f"/forecasts/targets/{table}/0.json",
            "sha256": ingest.canonical_sha256(ingest.chunk_hash_payload(chunk)),
        }
        table_payload = {
            "table": table,
            "rowCount": 0,
            "url": f"/forecasts/targets/{table}/manifest.json",
            "chunkCount": 1,
            "chunks": [reference],
        }
        table_entries.append(
            {
                **table_payload,
                "sha256": ingest.canonical_sha256(table_payload),
            }
        )
        chunks[table] = chunk

    manifest_payload = {
        "schemaVersion": ingest.MANIFEST_SCHEMA,
        "projectionSchemaVersion": "thesis_target_architecture_projection_v1",
        "generatedAt": "2026-06-29T00:00:00+00:00",
        "source": {"records": "forecast_cells"},
        "sourceCommit": "0123456789abcdef0123456789abcdef01234567",
        "builderVersion": "thesis_target_architecture_builder_v2",
        "hashAlgorithm": "sha256",
        "hashCanonicalization": "canonical_json_v1",
        "chunkHashSemantics": "canonical_chunk_without_projection_root_v1",
        "counts": {
            (
                "forecastDistributionPoints"
                if table == "forecastDistributions"
                else table
            ): 0
            for table in ingest.TABLES
        },
        "chunkSize": 10_000,
        "tables": table_entries,
    }
    root = ingest.canonical_sha256(manifest_payload)
    manifest = {**manifest_payload, "projectionRootSha256": root}
    for chunk in chunks.values():
        chunk["projectionRootSha256"] = root

    (tmp_path / "targets.json").write_text(json.dumps(manifest))
    for table, chunk in chunks.items():
        path = tmp_path / "forecasts" / "targets" / table / "0.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(chunk))

    snapshot = ingest.download_snapshot("https://example.test", tmp_path)
    assert snapshot.root == root
    assert set(snapshot.rows) == set(ingest.TABLES)

    chunks["targets"]["projectionRootSha256"] = "f" * 64
    target_path = tmp_path / "forecasts" / "targets" / "targets" / "0.json"
    target_path.write_text(json.dumps(chunks["targets"]))

    with pytest.raises(ingest.SnapshotError, match="mixed projection root"):
        ingest.download_snapshot("https://example.test", tmp_path)
