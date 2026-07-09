from __future__ import annotations

import copy
import pathlib
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from canonical_json import canonical_sha256  # noqa: E402
from thesis_log_client import load_thesis_log  # noqa: E402


def chunk(collection: str, index: int, rows: list[dict]) -> dict:
    return {
        "schemaVersion": "thesis_log_chunk_v1",
        "logSchemaVersion": "thesis_log_v3",
        "collection": collection,
        "chunkIndex": index,
        "count": len(rows),
        "rows": rows,
    }


def manifest_and_payloads() -> tuple[dict, dict[str, dict]]:
    payloads = {
        f"https://example.test/log/{name}/0.json": chunk(
            name, 0, [{"collection": name}]
        )
        for name in ("entries", "specs", "runs", "scores")
    }
    collections = {}
    for name in ("entries", "specs", "runs", "scores"):
        payload = payloads[f"https://example.test/log/{name}/0.json"]
        collections[name] = {
            "count": 1,
            "chunkCount": 1,
            "chunks": [
                {
                    "index": 0,
                    "count": 1,
                    "url": f"/log/{name}/0.json",
                    "sha256": canonical_sha256(payload),
                }
            ],
        }
    return (
        {
            "schemaVersion": "thesis_log_v3",
            "source": {},
            "counts": {},
            "collections": collections,
            "resolutionLinks": [],
        },
        payloads,
    )


def test_hydrates_every_v3_collection_and_preserves_manifest() -> None:
    manifest, payloads = manifest_and_payloads()
    hydrated = load_thesis_log(
        "https://example.test/log.json",
        manifest=manifest,
        loader=payloads.__getitem__,
    )

    assert hydrated["schemaVersion"] == "thesis_log_v3"
    assert hydrated["resolutionLinks"] == []
    for name in ("entries", "specs", "runs", "scores"):
        assert hydrated[name] == [{"collection": name}]
        assert hydrated["collections"][name]["count"] == 1


def test_rejects_a_chunk_that_does_not_match_its_canonical_hash() -> None:
    manifest, payloads = manifest_and_payloads()
    tampered = copy.deepcopy(payloads)
    tampered["https://example.test/log/runs/0.json"]["rows"][0]["tampered"] = True

    with pytest.raises(ValueError, match="runs chunk 0 sha256 mismatch"):
        load_thesis_log(
            "https://example.test/log.json",
            manifest=manifest,
            loader=tampered.__getitem__,
        )


def test_accepts_v2_during_a_rolling_deployment() -> None:
    legacy = {"schemaVersion": "thesis_log_v2", "entries": []}
    assert load_thesis_log(manifest=legacy) is legacy
