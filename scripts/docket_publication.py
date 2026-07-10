#!/usr/bin/env python3
"""Move unprivileged docket output across the publication trust boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
from typing import Any

from canonical_json import canonical_sha256

ROOT = pathlib.Path(__file__).resolve().parents[1]

SECRET_PATTERNS = {
    "GitHub token": re.compile(
        rb"(?:gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{80,255})"
    ),
    "OpenAI API key": re.compile(rb"sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    "AWS access key": re.compile(rb"(?:AKIA|ASIA)[A-Z0-9]{16}"),
    "Slack token": re.compile(rb"xox[baprs]-[A-Za-z0-9-]{20,}"),
    "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


class PublicationError(ValueError):
    """The generated publication bundle failed a trust-boundary check."""


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_repo_path(value: str) -> pathlib.PurePosixPath:
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise PublicationError(f"unsafe repository path: {value!r}")
    return path


def path_allowed(path: pathlib.PurePosixPath, allowed: list[str]) -> bool:
    for value in allowed:
        candidate = relative_repo_path(value)
        if path == candidate or candidate in path.parents:
            return True
    return False


def safe_join(root: pathlib.Path, relative: pathlib.PurePosixPath) -> pathlib.Path:
    root = root.resolve()
    path = root.joinpath(*relative.parts)
    try:
        path.resolve().relative_to(root)
    except ValueError as exc:
        raise PublicationError(f"path escapes through a symlink: {relative}") from exc
    current = path
    while current != root:
        if current.is_symlink():
            raise PublicationError(f"symlink is not allowed in bundle path: {relative}")
        current = current.parent
    return path


def changed_paths(allowed: list[str]) -> list[pathlib.PurePosixPath]:
    command = [
        "git",
        "ls-files",
        "--modified",
        "--others",
        "--exclude-standard",
        "--",
        *allowed,
    ]
    output = subprocess.check_output(command, cwd=ROOT, text=True)
    paths = sorted({relative_repo_path(line) for line in output.splitlines() if line})
    deleted = subprocess.check_output(
        ["git", "diff", "--name-only", "--diff-filter=D", "--", *allowed],
        cwd=ROOT,
        text=True,
    ).splitlines()
    if deleted:
        raise PublicationError(
            "docket generation may not delete publication files: " + ", ".join(deleted)
        )
    return paths


def stage(args: argparse.Namespace) -> None:
    bundle = pathlib.Path(args.bundle_dir).resolve()
    if bundle.exists():
        shutil.rmtree(bundle)
    repo = bundle / "repo"
    repo.mkdir(parents=True)

    paths = changed_paths(args.allow_path)
    batch = relative_repo_path(args.batch)
    if batch not in paths:
        raise PublicationError(f"batch manifest is not in the delta: {batch}")

    entries = []
    for relative in paths:
        if not path_allowed(relative, args.allow_path):
            raise PublicationError(
                f"path is outside the publication allowlist: {relative}"
            )
        source = safe_join(ROOT, relative)
        if source.is_symlink() or not source.is_file():
            raise PublicationError(
                f"publication artifact must be a regular file: {relative}"
            )
        secret_hits = scan_bytes(source.read_bytes())
        if secret_hits:
            raise PublicationError(
                f"refusing to upload {relative}: possible " + ", ".join(secret_hits)
            )
        destination = repo.joinpath(*relative.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        entries.append(
            {
                "path": str(relative),
                "bytes": source.stat().st_size,
                "sha256": sha256(source),
            }
        )

    manifest = {
        "schemaVersion": "thesis_docket_publication_bundle_v1",
        "batchManifest": str(batch),
        "files": entries,
    }
    (bundle / "bundle_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"staged {len(entries)} files in {bundle}")


def load_bundle(
    bundle: pathlib.Path, batch: str, allowed: list[str]
) -> tuple[pathlib.Path, dict[str, Any]]:
    bundle = bundle.resolve()
    repo = bundle / "repo"
    manifest_path = bundle / "bundle_manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PublicationError(f"invalid bundle manifest: {exc}") from exc
    if manifest.get("schemaVersion") != "thesis_docket_publication_bundle_v1":
        raise PublicationError("unsupported publication bundle schema")
    if manifest.get("batchManifest") != batch:
        raise PublicationError("bundle does not contain the expected batch manifest")

    expected: set[pathlib.PurePosixPath] = set()
    for entry in manifest.get("files", []):
        relative = relative_repo_path(str(entry.get("path", "")))
        if relative in expected:
            raise PublicationError(f"duplicate bundle path: {relative}")
        if not path_allowed(relative, allowed):
            raise PublicationError(
                f"path is outside the publication allowlist: {relative}"
            )
        expected.add(relative)
        path = safe_join(repo, relative)
        if path.is_symlink() or not path.is_file():
            raise PublicationError(f"bundle entry is not a regular file: {relative}")
        if path.stat().st_size != entry.get("bytes") or sha256(path) != entry.get(
            "sha256"
        ):
            raise PublicationError(f"bundle hash mismatch: {relative}")

    actual = {
        pathlib.PurePosixPath(path.relative_to(repo).as_posix())
        for path in repo.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if actual != expected:
        raise PublicationError(
            f"bundle file inventory mismatch: missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )
    return repo, manifest


def load_json(path: pathlib.Path, label: str) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PublicationError(f"invalid {label} {path}: {exc}") from exc


def validate_target_registration(repo: pathlib.Path, target: dict[str, Any]) -> None:
    path_value = target.get("targetRegistrationPath")
    content_hash = target.get("targetContentHash")
    if not path_value or not re.fullmatch(r"[0-9a-f]{64}", str(content_hash or "")):
        raise PublicationError("batch target lacks a hashed registration snapshot")
    relative = relative_repo_path(str(path_value))
    if pathlib.PurePosixPath("records/targets") not in relative.parents:
        raise PublicationError(
            f"target registration is outside records/targets: {relative}"
        )
    snapshot = load_json(safe_join(repo, relative), "target registration")
    if snapshot.get("schemaVersion") != "thesis_target_registration_v1":
        raise PublicationError("unsupported target registration schema")
    if canonical_sha256(snapshot) != content_hash or not relative.name.endswith(
        f"-{content_hash}.json"
    ):
        raise PublicationError(f"target registration hash mismatch: {relative}")
    contract = next(
        (
            row
            for row in snapshot.get("targets", [])
            if row.get("catalogSlug") == target.get("catalogSlug")
        ),
        None,
    )
    if not contract:
        raise PublicationError(
            f"target registration has no contract for {target.get('catalogSlug')}"
        )
    expected = {
        "series": target.get("series"),
        "period": target.get("period"),
        "catalogSlug": target.get("catalogSlug"),
        "dataPointId": target.get("dataPointId"),
        "unit": target.get("targetUnit"),
        "valueScale": target.get("valueScale"),
        "sourceBinding": target.get("sourceBinding"),
    }
    for key, value in expected.items():
        if contract.get(key) != value:
            raise PublicationError(
                f"target registration contract mismatch for {key}: "
                f"snapshot={contract.get(key)!r}, batch={value!r}"
            )


def validate_cells(repo: pathlib.Path, batch_relative: str) -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from run_thesis_analyst import validate_cells as shared_validate_cells
        from verify_custody import CustodyError, verify_run
    finally:
        sys.path.pop(0)

    batch_path = safe_join(repo, relative_repo_path(batch_relative))
    batch = load_json(batch_path, "batch manifest")
    if batch.get("schemaVersion") != "thesis_batch_manifest_v1":
        raise PublicationError("unsupported batch manifest schema")
    prompt_mode = str(batch.get("promptMode", "full"))
    referenced_payloads: set[pathlib.PurePosixPath] = set()
    referenced_manifests: set[pathlib.PurePosixPath] = set()

    for index, result in enumerate(batch.get("results", [])):
        cells_value = result.get("cellsPath")
        manifest_value = result.get("manifestPath")
        expected_ok = result.get("ok") is True
        if expected_ok and (not cells_value or not manifest_value):
            raise PublicationError(
                f"passing result {index} lacks cells or manifest path"
            )
        target = result.get("target")
        if not isinstance(target, dict):
            raise PublicationError(f"result {index} has no target context")
        validate_target_registration(repo, target)
        if manifest_value:
            manifest_relative = relative_repo_path(str(manifest_value))
            if manifest_relative in referenced_manifests:
                raise PublicationError(f"duplicate run manifest: {manifest_relative}")
            referenced_manifests.add(manifest_relative)
            manifest_path = safe_join(repo, manifest_relative)
            manifest = load_json(manifest_path, "run manifest")
            if bool(manifest.get("ok")) != expected_ok:
                raise PublicationError(
                    f"run manifest status mismatch: {manifest_relative}"
                )
            try:
                verify_run(manifest_path.parent)
            except CustodyError as exc:
                raise PublicationError(f"custody verification failed: {exc}") from exc
        if not cells_value:
            continue

        cells_relative = relative_repo_path(str(cells_value))
        if cells_relative in referenced_payloads:
            raise PublicationError(f"duplicate cells payload: {cells_relative}")
        referenced_payloads.add(cells_relative)
        cells_path = safe_join(repo, cells_relative)
        cells = load_json(cells_path, "cells payload")
        if not isinstance(cells, list) or not all(
            isinstance(cell, dict) for cell in cells
        ):
            raise PublicationError(
                f"cells payload is not an object list: {cells_relative}"
            )

        report = shared_validate_cells(
            cells,
            target_context=target,
            prompt_mode=prompt_mode,
        )
        if bool(report.get("ok")) != expected_ok:
            raise PublicationError(
                f"validator status mismatch for {cells_relative}: "
                f"batch ok={expected_ok}, replay={report}"
            )

        if not manifest_value:
            raise PublicationError(
                f"cells payload has no run manifest: {cells_relative}"
            )
        print(
            f"validated {cells_relative} "
            f"({'passing' if expected_ok else 'retained failed trace'})"
        )

    bundled_payloads = {
        pathlib.PurePosixPath(path.relative_to(repo).as_posix())
        for path in repo.rglob("cells.with_activity.json")
    }
    if bundled_payloads != referenced_payloads:
        raise PublicationError(
            "batch/cell inventory mismatch: "
            f"unreferenced={sorted(bundled_payloads - referenced_payloads)}, "
            f"missing={sorted(referenced_payloads - bundled_payloads)}"
        )
    bundled_manifests = {
        pathlib.PurePosixPath(path.relative_to(repo).as_posix())
        for path in repo.glob("records/thesis-analyst/*/*/manifest.json")
    }
    if bundled_manifests != referenced_manifests:
        raise PublicationError(
            "batch/run-manifest inventory mismatch: "
            f"unreferenced={sorted(bundled_manifests - referenced_manifests)}, "
            f"missing={sorted(referenced_manifests - bundled_manifests)}"
        )


def apply_bundle(repo: pathlib.Path, manifest: dict[str, Any]) -> None:
    for entry in manifest["files"]:
        relative = relative_repo_path(entry["path"])
        source = safe_join(repo, relative)
        destination = safe_join(ROOT, relative)
        if destination.exists() and destination.read_bytes() == source.read_bytes():
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def validate(args: argparse.Namespace) -> None:
    bundle = pathlib.Path(args.bundle_dir)
    repo, manifest = load_bundle(bundle, args.batch, args.allow_path)
    validate_cells(repo, args.batch)
    if args.apply:
        apply_bundle(repo, manifest)
        print("validated publication bundle applied to checkout")


def scan_bytes(data: bytes) -> list[str]:
    return [name for name, pattern in SECRET_PATTERNS.items() if pattern.search(data)]


def scan_staged(_: argparse.Namespace) -> None:
    output = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
        cwd=ROOT,
    )
    paths = [path.decode() for path in output.split(b"\0") if path]
    findings = []
    for path in paths:
        data = subprocess.check_output(["git", "show", f":{path}"], cwd=ROOT)
        for kind in scan_bytes(data):
            findings.append(f"{path}: possible {kind}")
    if findings:
        raise PublicationError("secret scan failed:\n" + "\n".join(findings))
    print(f"secret scan passed for {len(paths)} staged files")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    stage_parser = subparsers.add_parser("stage")
    stage_parser.add_argument("--bundle-dir", required=True)
    stage_parser.add_argument("--batch", required=True)
    stage_parser.add_argument("--allow-path", action="append", required=True)
    stage_parser.set_defaults(func=stage)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--bundle-dir", required=True)
    validate_parser.add_argument("--batch", required=True)
    validate_parser.add_argument("--allow-path", action="append", required=True)
    validate_parser.add_argument("--apply", action="store_true")
    validate_parser.set_defaults(func=validate)

    scan_parser = subparsers.add_parser("scan-staged")
    scan_parser.set_defaults(func=scan_staged)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        args.func(args)
    except (PublicationError, subprocess.CalledProcessError) as exc:
        print(f"PUBLICATION BLOCKED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
