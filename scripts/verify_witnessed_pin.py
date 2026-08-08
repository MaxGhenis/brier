#!/usr/bin/env python3
"""Verify that one sealed ledger witness is the exact committed pin state."""

from __future__ import annotations

import datetime as dt
import gzip
import json
import pathlib
import re
import subprocess
import sys
import tempfile
from typing import Any

from ledger_release_chain import (
    MANIFEST_RE,
    PRODUCER_SIGNATURE_RE,
    RECEIPT_RE,
    ReleaseChainError,
    _openssl_environment,
    _parse_receipt_text,
    load_manifest,
)
from verify_custody import CustodyError, same_ledger_repo, verify_run

ROOT = pathlib.Path(__file__).resolve().parents[1]
PIN_SCHEMA = "thesis_ledger_pin_v1"
WITNESS_SCHEMA = "thesis_ledger_witness_run_v2"
RELEASE_DIRECTORY = "releases/manifests"
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
GIT_SHA_RE = re.compile(r"[0-9a-f]{40}\Z")
STRICT_UTC_RE = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:"
    r"[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?Z\Z"
)
RELEASE_HEAD_KEYS = {
    "index",
    "manifestSha256",
    "freetsaGenTimeUtc",
    "digicertGenTimeUtc",
}
PIN_KEYS = {
    "schemaVersion",
    "repo",
    "branch",
    "sha",
    "jsonlSha256",
    "jsonlBytes",
    "lineCount",
    "pinnedAtUtc",
    "releaseHead",
}
PIN_CATALOG_KEYS = {"catalogSha256", "catalogBytes"}


class WitnessedPinError(ValueError):
    """The witness bundle and pin do not identify one exact ledger state."""


def _object(path: pathlib.Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise WitnessedPinError(f"cannot read {label} {path}: {exc}") from exc
    if type(value) is not dict:
        raise WitnessedPinError(f"{label} must be a JSON object: {path}")
    return value


def _inside_root(path: pathlib.Path, label: str) -> pathlib.Path:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise WitnessedPinError(f"{label} escapes the repository: {path}") from exc


def _strict_utc(value: Any, label: str) -> None:
    if type(value) is not str or STRICT_UTC_RE.fullmatch(value) is None:
        raise WitnessedPinError(f"{label} must be a strict UTC timestamp ending in Z")
    try:
        dt.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise WitnessedPinError(f"{label} is not a real UTC time: {value!r}") from exc


def _release_file_bytes(
    manifest: dict[str, Any], release_files: list[Any]
) -> dict[str, bytes]:
    upstream = manifest.get("upstream")
    if type(upstream) is not list:
        raise WitnessedPinError("witness manifest lacks its upstream archive list")
    by_name = {
        record.get("name"): record
        for record in upstream
        if type(record) is dict and record.get("role") == "ledger_release_file"
    }
    result: dict[str, bytes] = {}
    for item in release_files:
        if type(item) is not dict:
            raise WitnessedPinError("release-file inventory contains a non-object")
        source_path = item.get("path")
        archive_name = item.get("archiveName")
        record = by_name.get(archive_name)
        archive = record.get("archive") if type(record) is dict else None
        archive_path = archive.get("path") if type(archive) is dict else None
        if type(source_path) is not str or type(archive_path) is not str:
            raise WitnessedPinError(
                f"release-file inventory cannot resolve archive {archive_name!r}"
            )
        relative = _inside_root(ROOT / archive_path, f"release archive {source_path}")
        try:
            result[source_path] = gzip.decompress((ROOT / relative).read_bytes())
        except (OSError, EOFError) as exc:
            raise WitnessedPinError(
                f"cannot read release archive {source_path}: {exc}"
            ) from exc
    return result


def _receipt_gen_time(raw: bytes, label: str) -> str:
    """Read the signed TSTInfo genTime from already authenticated receipt bytes."""

    with tempfile.TemporaryDirectory(prefix="thesis-witnessed-pin-tsa-") as name:
        temporary = pathlib.Path(name)
        receipt = temporary / pathlib.PurePosixPath(label).name
        receipt.write_bytes(raw)
        empty_ca = temporary / "empty-ca"
        empty_ca.mkdir()
        environment = _openssl_environment(empty_ca)
        try:
            completed = subprocess.run(
                [
                    "openssl",
                    "ts",
                    "-reply",
                    "-config",
                    "/dev/null",
                    "-in",
                    str(receipt),
                    "-text",
                ],
                check=False,
                capture_output=True,
                text=True,
                env=environment,
            )
        except FileNotFoundError as exc:
            raise WitnessedPinError(
                "openssl is required to bind witnessed receipt genTimes"
            ) from exc
        if completed.returncode != 0:
            diagnostic = (completed.stderr or completed.stdout).strip()[-1000:]
            raise WitnessedPinError(
                f"cannot inspect witnessed receipt {label}: {diagnostic}"
            )
        try:
            gen_time, _policy = _parse_receipt_text(completed.stdout, receipt)
        except ReleaseChainError as exc:
            raise WitnessedPinError(
                f"cannot parse witnessed receipt {label}: {exc}"
            ) from exc
    return gen_time.isoformat().replace("+00:00", "Z")


def _load_manifest(raw: bytes, basename: str) -> tuple[dict[str, Any], str]:
    with tempfile.TemporaryDirectory(prefix="thesis-witnessed-pin-manifest-") as name:
        path = pathlib.Path(name) / basename
        path.write_bytes(raw)
        try:
            payload, _raw, digest = load_manifest(path)
        except ReleaseChainError as exc:
            raise WitnessedPinError(
                f"archived release manifest {basename} is invalid: {exc}"
            ) from exc
    return payload, digest


def _release_inventory(
    release_files: list[Any],
) -> tuple[dict[int, dict[str, Any]], dict[str, dict[str, dict[str, Any]]]]:
    manifests: dict[int, dict[str, Any]] = {}
    receipts: dict[str, dict[str, dict[str, Any]]] = {}
    producer_signatures: dict[str, dict[str, Any]] = {}
    prefix = f"{RELEASE_DIRECTORY}/"
    for item in release_files:
        if type(item) is not dict or type(item.get("path")) is not str:
            raise WitnessedPinError("release-file inventory contains a malformed item")
        path = item["path"]
        if not path.startswith(prefix) or "/" in path.removeprefix(prefix):
            raise WitnessedPinError(f"non-canonical release archive path {path!r}")
        basename = path.removeprefix(prefix)
        manifest_match = MANIFEST_RE.fullmatch(basename)
        if manifest_match is not None:
            index = int(manifest_match.group("index"))
            if index in manifests:
                raise WitnessedPinError(f"duplicate archived release index {index}")
            manifests[index] = item
            continue
        signature_match = PRODUCER_SIGNATURE_RE.fullmatch(basename)
        if signature_match is not None:
            stem = signature_match.group("stem")
            if stem in producer_signatures:
                raise WitnessedPinError(
                    f"duplicate archived producer signature for {stem}"
                )
            producer_signatures[stem] = item
            continue
        receipt_match = RECEIPT_RE.fullmatch(basename)
        if receipt_match is None:
            raise WitnessedPinError(
                f"unknown file in archived release manifest directory: {basename}"
            )
        receipts.setdefault(receipt_match.group("stem"), {})[
            receipt_match.group("tsa")
        ] = item
    if not manifests:
        raise WitnessedPinError(
            "release archive has artifacts but no valid genesis manifest"
        )
    indices = sorted(manifests)
    if indices != list(range(indices[-1] + 1)):
        raise WitnessedPinError(
            f"archived release indices are not contiguous from genesis: {indices}"
        )
    stems = {pathlib.PurePosixPath(item["path"]).stem for item in manifests.values()}
    if set(receipts) != stems:
        raise WitnessedPinError(
            "archived release receipts do not correspond exactly to manifests"
        )
    if set(producer_signatures) != stems:
        raise WitnessedPinError(
            "archived release producer signatures do not correspond exactly "
            "to manifests"
        )
    for stem in stems:
        if set(receipts[stem]) != {"freetsa", "digicert"}:
            raise WitnessedPinError(
                f"archived release {stem} lacks exactly two receipt providers"
            )
    return manifests, receipts


def verify_witnessed_pin(
    witness_manifest_path: pathlib.Path,
    pin_path: pathlib.Path,
) -> pathlib.Path:
    """Return the witness run directory after custody and pin-link checks."""

    witness_relative = _inside_root(witness_manifest_path, "witness manifest")
    pin_relative = _inside_root(pin_path, "ledger pin")
    witness_path = ROOT / witness_relative
    selected_pin_path = ROOT / pin_relative
    if witness_path.name != "manifest.json" or witness_relative.parts[:1] != (
        "records",
    ):
        raise WitnessedPinError(
            f"invalid witness manifest path: {witness_relative.as_posix()}"
        )
    try:
        verification = verify_run(witness_path.parent)
    except CustodyError as exc:
        raise WitnessedPinError(f"witness custody verification failed: {exc}") from exc
    if verification.run_mode != "ledger_witness":
        raise WitnessedPinError(
            f"witness run has unexpected custody mode {verification.run_mode!r}"
        )

    manifest = _object(witness_path, "witness manifest")
    pin = _object(selected_pin_path, "ledger pin")
    if manifest.get("schemaVersion") != WITNESS_SCHEMA:
        raise WitnessedPinError(f"witness schema must be exactly {WITNESS_SCHEMA!r}")
    if pin.get("schemaVersion") != PIN_SCHEMA:
        raise WitnessedPinError(f"pin schema must be exactly {PIN_SCHEMA!r}")
    pin_keys = set(pin)
    allowed_pin_keys = PIN_KEYS | PIN_CATALOG_KEYS
    if not PIN_KEYS.issubset(pin_keys) or not pin_keys.issubset(allowed_pin_keys):
        raise WitnessedPinError(
            "pin keys are not closed-world: "
            f"missing={sorted(PIN_KEYS - pin_keys)}, "
            f"unknown={sorted(pin_keys - allowed_pin_keys)}"
        )
    catalog_pin_keys = pin_keys & PIN_CATALOG_KEYS
    if catalog_pin_keys and catalog_pin_keys != PIN_CATALOG_KEYS:
        raise WitnessedPinError(
            "pin catalog commitment must contain catalogSha256 and "
            "catalogBytes together"
        )
    if type(pin.get("repo")) is not str or type(pin.get("branch")) is not str:
        raise WitnessedPinError("pin repo and branch must be strings")
    if type(pin.get("sha")) is not str or GIT_SHA_RE.fullmatch(pin["sha"]) is None:
        raise WitnessedPinError("pin sha must be a lowercase 40-character Git SHA")
    if (
        type(pin.get("jsonlSha256")) is not str
        or SHA256_RE.fullmatch(pin["jsonlSha256"]) is None
    ):
        raise WitnessedPinError("pin jsonlSha256 must be a SHA-256 digest")
    for key in ("jsonlBytes", "lineCount"):
        if type(pin.get(key)) is not int or pin[key] < 0:
            raise WitnessedPinError(f"pin {key} must be a non-negative integer")
    catalog_pinned = catalog_pin_keys == PIN_CATALOG_KEYS
    if catalog_pinned:
        if (
            type(pin.get("catalogSha256")) is not str
            or SHA256_RE.fullmatch(pin["catalogSha256"]) is None
        ):
            raise WitnessedPinError("pin catalogSha256 must be a SHA-256 digest")
        if type(pin.get("catalogBytes")) is not int or pin["catalogBytes"] < 0:
            raise WitnessedPinError("pin catalogBytes must be a non-negative integer")
    _strict_utc(pin.get("pinnedAtUtc"), "pin pinnedAtUtc")
    expected_identity = {
        "ledgerRepo": pin.get("repo"),
        "ledgerBranch": pin.get("branch"),
        "ledgerBranchSha": pin.get("sha"),
    }
    mismatches = {
        key: (manifest.get(key), expected)
        for key, expected in expected_identity.items()
        if not (
            # The repo slug unifies across the documented rename; every
            # other identity field stays a literal comparison.
            same_ledger_repo(manifest.get(key), expected)
            if key == "ledgerRepo"
            else manifest.get(key) == expected
        )
    }
    jsonl = manifest.get("jsonl")
    if type(jsonl) is not dict:
        raise WitnessedPinError("witness manifest lacks its JSONL commitment")
    if jsonl.get("sha256") != pin.get("jsonlSha256"):
        mismatches["jsonl.sha256"] = (
            jsonl.get("sha256"),
            pin.get("jsonlSha256"),
        )
    if jsonl.get("lineCount") != pin.get("lineCount"):
        mismatches["jsonl.lineCount"] = (
            jsonl.get("lineCount"),
            pin.get("lineCount"),
        )
    if jsonl.get("bytes") != pin.get("jsonlBytes"):
        mismatches["jsonl.bytes"] = (
            jsonl.get("bytes"),
            pin.get("jsonlBytes"),
        )
    catalog = manifest.get("catalog")
    if catalog_pinned:
        if type(catalog) is not dict:
            mismatches["catalog"] = (catalog, "catalog commitment")
        else:
            if catalog.get("sha256") != pin.get("catalogSha256"):
                mismatches["catalog.sha256"] = (
                    catalog.get("sha256"),
                    pin.get("catalogSha256"),
                )
            if catalog.get("bytes") != pin.get("catalogBytes"):
                mismatches["catalog.bytes"] = (
                    catalog.get("bytes"),
                    pin.get("catalogBytes"),
                )
    elif catalog is not None:
        mismatches["catalog"] = ("archived catalog commitment", None)

    release_archive = manifest.get("releaseArchive")
    if (
        type(release_archive) is not dict
        or type(release_archive.get("files")) is not list
    ):
        raise WitnessedPinError("witness manifest lacks its release-file inventory")
    release_files = release_archive["files"]
    head = pin.get("releaseHead")
    if head is None:
        if release_files:
            mismatches["releaseHead"] = ("archived release artifacts", None)
    elif type(head) is not dict:
        mismatches["releaseHead"] = (head, "object or null")
    else:
        if set(head) != RELEASE_HEAD_KEYS:
            mismatches["releaseHead.keys"] = (
                sorted(head),
                sorted(RELEASE_HEAD_KEYS),
            )
        index = head.get("index")
        digest = head.get("manifestSha256")
        if (
            type(index) is not int
            or index < 0
            or index > 9_999
            or type(digest) is not str
            or SHA256_RE.fullmatch(digest) is None
            or any(
                type(head.get(key)) is not str
                or STRICT_UTC_RE.fullmatch(head[key]) is None
                for key in ("freetsaGenTimeUtc", "digicertGenTimeUtc")
            )
        ):
            mismatches["releaseHead"] = (
                head,
                "closed valid index, digest, and strict UTC genTimes",
            )
        else:
            _strict_utc(head["freetsaGenTimeUtc"], "releaseHead.freetsaGenTimeUtc")
            _strict_utc(head["digicertGenTimeUtc"], "releaseHead.digicertGenTimeUtc")
            manifests, receipts = _release_inventory(release_files)
            terminal_index = max(manifests)
            if index != terminal_index:
                mismatches["releaseHead.index"] = (index, terminal_index)
            stem = f"{index:04d}-{digest[:16]}"
            manifest_path = f"{RELEASE_DIRECTORY}/{stem}.json"
            terminal = manifests.get(index)
            if (
                terminal is None
                or terminal.get("path") != manifest_path
                or terminal.get("sha256") != digest
            ):
                mismatches["releaseHead"] = (
                    terminal,
                    head,
                )
            else:
                archived = _release_file_bytes(manifest, release_files)
                payload, actual_digest = _load_manifest(
                    archived[manifest_path], pathlib.PurePosixPath(manifest_path).name
                )
                if actual_digest != digest:
                    mismatches["releaseHead.manifestSha256"] = (
                        actual_digest,
                        digest,
                    )
                state = payload["state"]
                if payload["releaseIndex"] != index:
                    mismatches["releaseHead.manifestIndex"] = (
                        payload["releaseIndex"],
                        index,
                    )
                if state["jsonlSha256"] != pin.get("jsonlSha256"):
                    mismatches["releaseHead.state.jsonlSha256"] = (
                        state["jsonlSha256"],
                        pin.get("jsonlSha256"),
                    )
                if state["lineCount"] != pin.get("lineCount"):
                    mismatches["releaseHead.state.lineCount"] = (
                        state["lineCount"],
                        pin.get("lineCount"),
                    )
                for tsa, key in (
                    ("freetsa", "freetsaGenTimeUtc"),
                    ("digicert", "digicertGenTimeUtc"),
                ):
                    receipt_path = receipts[stem][tsa]["path"]
                    actual_time = _receipt_gen_time(
                        archived[receipt_path], receipt_path
                    )
                    if actual_time != head[key]:
                        mismatches[f"releaseHead.{key}"] = (
                            actual_time,
                            head[key],
                        )
    if mismatches:
        raise WitnessedPinError(f"witness does not match pin: {mismatches}")
    return witness_path.parent


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: verify_witnessed_pin.py WITNESS_MANIFEST LEDGER_PIN",
            file=sys.stderr,
        )
        return 2
    try:
        run_dir = verify_witnessed_pin(
            pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
        )
    except WitnessedPinError as exc:
        print(f"WITNESSED PIN BROKEN: {exc}", file=sys.stderr)
        return 1
    print(run_dir.resolve().relative_to(ROOT.resolve()).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
