from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import docket_publication  # noqa: E402
from docket_publication import PublicationError  # noqa: E402


def git(repo: pathlib.Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def test_stage_copies_only_allowlisted_delta(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    (repo / "records").mkdir()
    (repo / "records" / "base.json").write_text("{}\n")
    git(repo, "add", "records/base.json")
    git(
        repo,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-m",
        "base",
    )

    batch = pathlib.Path("records/batches/run.json")
    batch_path = repo / batch
    batch_path.parent.mkdir()
    batch_path.write_text('{"schemaVersion":"thesis_batch_manifest_v1"}\n')
    (repo / "not-allowed.txt").write_text("do not publish\n")
    monkeypatch.setattr(docket_publication, "ROOT", repo)

    bundle = tmp_path / "bundle"
    docket_publication.stage(
        argparse.Namespace(
            bundle_dir=str(bundle),
            batch=str(batch),
            allow_path=["records"],
        )
    )

    manifest = json.loads((bundle / "bundle_manifest.json").read_text())
    assert [entry["path"] for entry in manifest["files"]] == [str(batch)]
    assert not (bundle / "repo" / "not-allowed.txt").exists()


def test_load_bundle_rejects_uninventoried_file(tmp_path: pathlib.Path) -> None:
    bundle = tmp_path / "bundle"
    repo = bundle / "repo"
    payload = repo / "records" / "batch.json"
    payload.parent.mkdir(parents=True)
    payload.write_text("{}\n")
    (repo / "records" / "extra.json").write_text("{}\n")
    (bundle / "bundle_manifest.json").write_text(
        json.dumps(
            {
                "schemaVersion": "thesis_docket_publication_bundle_v1",
                "batchManifest": "records/batch.json",
                "files": [
                    {
                        "path": "records/batch.json",
                        "bytes": payload.stat().st_size,
                        "sha256": docket_publication.sha256(payload),
                    }
                ],
            }
        )
    )

    with pytest.raises(PublicationError, match="inventory mismatch"):
        docket_publication.load_bundle(bundle, "records/batch.json", ["records"])


@pytest.mark.parametrize(
    "sample, expected",
    [
        (b"ghp_" + b"a" * 36, "GitHub token"),
        (b"sk-proj-" + b"a" * 24, "OpenAI API key"),
        (b"AKIA" + b"A" * 16, "AWS access key"),
        (b"xoxb-" + b"a" * 24, "Slack token"),
        (b"-----BEGIN PRIVATE KEY-----", "private key"),
    ],
)
def test_secret_scanner_detects_common_token_shapes(
    sample: bytes, expected: str
) -> None:
    assert expected in docket_publication.scan_bytes(sample)


def test_scan_staged_rejects_secret(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    (repo / "records").mkdir()
    (repo / "records" / "leak.txt").write_bytes(b"ghp_" + b"a" * 36)
    git(repo, "add", "records/leak.txt")
    monkeypatch.setattr(docket_publication, "ROOT", repo)

    with pytest.raises(PublicationError, match="possible GitHub token"):
        docket_publication.scan_staged(argparse.Namespace())
