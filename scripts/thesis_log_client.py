#!/usr/bin/env python3
"""Load the chunked Thesis Log v3 manifest as the former hydrated shape."""

from __future__ import annotations

import argparse
import json
import pathlib
import urllib.parse
import urllib.request
from collections.abc import Callable
from typing import Any

from canonical_json import canonical_sha256

LOG_URL = "https://app.thesisinstitute.org/log.json"
CHUNKED_COLLECTIONS = ("entries", "specs", "runs", "scores")

JsonLoader = Callable[[str], dict[str, Any]]


def fetch_json(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=120) as response:
        return json.load(response)


def fetch_json_bytes(url: str) -> tuple[bytes, dict[str, Any]]:
    with urllib.request.urlopen(url, timeout=120) as response:
        raw = response.read()
    return raw, json.loads(raw)


def load_thesis_log(
    url: str = LOG_URL,
    *,
    manifest: dict[str, Any] | None = None,
    loader: JsonLoader = fetch_json,
) -> dict[str, Any]:
    """Fetch a v3 manifest and all chunks, returning v2-compatible arrays.

    A v2 response is returned unchanged during deployment rollovers. V3 chunks
    are canonical-hash checked before any consumer sees their rows.
    """

    manifest = manifest or loader(url)
    if manifest.get("schemaVersion") == "thesis_log_v2":
        return manifest
    if manifest.get("schemaVersion") != "thesis_log_v3":
        raise ValueError(
            f"unsupported Thesis Log schema: {manifest.get('schemaVersion')!r}"
        )

    hydrated = dict(manifest)
    collections = manifest.get("collections")
    if not isinstance(collections, dict):
        raise ValueError("thesis_log_v3 is missing collections")

    for collection in CHUNKED_COLLECTIONS:
        collection_manifest = collections.get(collection)
        if not isinstance(collection_manifest, dict):
            raise ValueError(f"thesis_log_v3 is missing {collection} manifest")
        rows: list[Any] = []
        chunks = collection_manifest.get("chunks")
        if not isinstance(chunks, list):
            raise ValueError(f"{collection} manifest is missing chunks")
        for expected_index, reference in enumerate(chunks):
            if reference.get("index") != expected_index:
                raise ValueError(f"{collection} chunk indexes are not contiguous")
            chunk_url = urllib.parse.urljoin(url, reference["url"])
            chunk = loader(chunk_url)
            _verify_chunk(collection, reference, chunk)
            rows.extend(chunk["rows"])
        if len(rows) != collection_manifest.get("count"):
            raise ValueError(
                f"{collection} row count mismatch: expected "
                f"{collection_manifest.get('count')}, got {len(rows)}"
            )
        hydrated[collection] = rows
    return hydrated


def load_thesis_log_from_directory(source_dir: pathlib.Path) -> dict[str, Any]:
    manifest_path = source_dir / "log.json"
    manifest = json.loads(manifest_path.read_text())

    def load_local(url: str) -> dict[str, Any]:
        path = source_dir / urllib.parse.urlparse(url).path.lstrip("/")
        return json.loads(path.read_text())

    return load_thesis_log(
        "https://app.thesisinstitute.org/log.json",
        manifest=manifest,
        loader=load_local,
    )


def download_thesis_log(url: str, output_dir: pathlib.Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_raw, manifest = fetch_json_bytes(url)
    _write_bytes(output_dir / "log.json", manifest_raw)
    if manifest.get("schemaVersion") != "thesis_log_v3":
        return load_thesis_log(url, manifest=manifest)

    downloaded: dict[str, dict[str, Any]] = {}
    for collection_manifest in manifest["collections"].values():
        for reference in collection_manifest["chunks"]:
            chunk_url = urllib.parse.urljoin(url, reference["url"])
            chunk_raw, chunk = fetch_json_bytes(chunk_url)
            destination = output_dir / urllib.parse.urlparse(chunk_url).path.lstrip("/")
            _write_bytes(destination, chunk_raw)
            downloaded[chunk_url] = chunk

    return load_thesis_log(
        url,
        manifest=manifest,
        loader=lambda chunk_url: downloaded[chunk_url],
    )


def _verify_chunk(
    collection: str,
    reference: dict[str, Any],
    chunk: dict[str, Any],
) -> None:
    expected = {
        "schemaVersion": "thesis_log_chunk_v1",
        "logSchemaVersion": "thesis_log_v3",
        "collection": collection,
        "chunkIndex": reference["index"],
        "count": reference["count"],
    }
    for key, value in expected.items():
        if chunk.get(key) != value:
            raise ValueError(
                f"{collection} chunk {reference['index']} has invalid {key}: "
                f"expected {value!r}, got {chunk.get(key)!r}"
            )
    if len(chunk.get("rows", [])) != reference["count"]:
        raise ValueError(f"{collection} chunk {reference['index']} row count mismatch")
    actual_sha256 = canonical_sha256(chunk)
    if actual_sha256 != reference.get("sha256"):
        raise ValueError(
            f"{collection} chunk {reference['index']} sha256 mismatch: "
            f"expected {reference.get('sha256')}, got {actual_sha256}"
        )


def _write_bytes(path: pathlib.Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=LOG_URL)
    parser.add_argument("--output-dir", type=pathlib.Path)
    args = parser.parse_args()
    log = (
        download_thesis_log(args.url, args.output_dir)
        if args.output_dir
        else load_thesis_log(args.url)
    )
    print(
        json.dumps(
            {
                "schemaVersion": log["schemaVersion"],
                "counts": log["counts"],
                "collections": {name: len(log[name]) for name in CHUNKED_COLLECTIONS},
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
