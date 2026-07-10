#!/usr/bin/env python3
"""Verify versioned, complete artifact custody for Thesis run modes."""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
import re
import stat
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from canonical_json import canonical_bytes, canonical_sha256

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INVENTORY_VERSION = 2
INVENTORY_STATUS_COMPLETE = "complete"
INVENTORY_STATUS_LEGACY = "legacy-incomplete"
DERIVED_ENSEMBLE_SCHEMA = "thesis_derived_ensemble_manifest_v1"
DERIVED_ENSEMBLE_ALGORITHM = "pointwise_median_cdf_v1"
LEGACY_DERIVED_AT = "2026-07-08T03:03:42Z"
LEGACY_DERIVED_DIRS = {
    "bls-ppi-final-demand-monthly-change-june-2026-median3-2026-07-08t03-03-42z",
    "census-housing-starts-saar-june-2026-median3-2026-07-08t03-03-42z",
    "continued-claims-week-2026-06-27-median3-2026-07-08t03-03-42z",
    "initial-claims-week-2026-07-04-median3-2026-07-08t03-03-42z",
    "us-core-cpi-mom-june-2026-median3-2026-07-08t03-03-42z",
    "us-cpi-u-mom-june-2026-median3-2026-07-08t03-03-42z",
}

ANALYST_COMPLETED_INVENTORY = {
    "prompt.md": "prompt",
    "raw_response.txt": "raw_response",
    "parsed_cells.json": "parsed_cell",
    "normalized_cells.json": "normalized_cell",
    "distribution.json": "run_distribution",
    "validation.json": "validation_report",
    "cells.with_activity.json": "cells_with_activity",
}
CODEX_STAGE_INVENTORY = {
    "codex_stdout.jsonl": "codex_stdout_jsonl",
    "codex_stderr.log": "codex_stderr_log",
    "codex_events.jsonl": "codex_events_jsonl",
    "codex_last_message.txt": "codex_last_message",
    "codex_trace.json": "codex_trace",
}
REVIEWED_STAGE_INVENTORY = {
    "pre_submit_review_prompt.md": "review_prompt",
    "revision_prompt.md": "revision_prompt",
}
RESOLVER_RESPONSE_RE = re.compile(
    # One archived source response per fetched document: a lowercase series
    # or page identifier, the first-print vintage date, and a content-hash
    # prefix. CSV for ALFRED vintage fetches, HTML for archived source
    # pages (e.g. the Wayback snapshot of BLS Table A-19).
    r"responses/[a-z0-9._-]+-\d{4}-\d{2}-\d{2}-[0-9a-f]{16}\.(?:csv|html)\.gz"
)
LEDGER_WITNESS_ARCHIVE_RE = re.compile(r"upstream/[a-z0-9][a-z0-9._-]*\.gz")
RECORDER_REQUIRED_SURFACES = {
    "log": "log.json.gz",
    "ledger": "ledger.json.gz",
    "targets": "targets.json.gz",
    "reward": "reward.json.gz",
    "build": "build.json.gz",
    "apiBuild": "api-build.json.gz",
    "ledgerCommitApi": "ledger-commit.json.gz",
}
RECORDER_REQUIRED_LIVE = {
    "spm-child-poverty-2025": "live/spm-child-poverty-2025.json.gz",
    "cpi-u-annual-2026": "live/cpi-u-annual-2026.json.gz",
    "ctc-expansion-cost-ty2026": "live/ctc-expansion-cost-ty2026.json.gz",
    "ctc-current-law-outlays-ty2026": "live/ctc-current-law-outlays-ty2026.json.gz",
}


class CustodyError(ValueError):
    pass


@dataclass(frozen=True)
class CustodyVerification:
    run_mode: str
    custody_inventory_version: int
    inventory_status: str
    custody_root_sha256: str
    artifact_count: int
    run_succeeded: bool

    @property
    def headline_eligible(self) -> bool:
        return (
            self.run_mode == "analyst"
            and self.inventory_status == INVENTORY_STATUS_COMPLETE
            and self.run_succeeded
        )


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CustodyError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CustodyError(f"JSON record must be an object: {path}")
    return value


def _safe_relative(value: str) -> PurePosixPath:
    if not value or "\\" in value:
        raise CustodyError(f"invalid artifact path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise CustodyError(f"unsafe artifact path: {value!r}")
    if path.as_posix() != value:
        raise CustodyError(f"non-normalized artifact path: {value!r}")
    return path


def _safe_artifact_path(run_dir: Path, relative: str) -> Path:
    logical = _safe_relative(relative)
    path = run_dir.joinpath(*logical.parts)
    try:
        path.resolve().relative_to(run_dir.resolve())
    except ValueError as exc:
        raise CustodyError(f"artifact path escapes run directory: {relative}") from exc
    return path


def _manifest_relative(run_dir: Path, value: str, *, legacy: bool) -> str:
    segments = value.split("/")
    if (
        not value
        or "\\" in value
        or value.endswith("/")
        or any(segment in {".", ".."} for segment in segments)
        or any(not segment for segment in segments[1:])
    ):
        raise CustodyError(f"unsafe manifest artifact path: {value!r}")
    source = Path(value)
    candidates = []
    if source.is_absolute():
        candidates.append(source)
    else:
        candidates.extend([Path.cwd() / source, REPOSITORY_ROOT / source])
        candidates.extend(
            ancestor.parent / source
            for ancestor in run_dir.parents
            if ancestor.name == "records"
        )
        if not source.parts or source.parts[0] != "records":
            candidates.append(run_dir / source)
    for candidate in candidates:
        try:
            relative = candidate.resolve().relative_to(run_dir.resolve())
        except ValueError:
            continue
        return _safe_relative(relative.as_posix()).as_posix()
    if legacy:
        for index, part in enumerate(source.parts):
            if part != run_dir.name or index + 1 >= len(source.parts):
                continue
            relative = PurePosixPath(*source.parts[index + 1 :])
            candidate = run_dir.joinpath(*relative.parts)
            if candidate.exists():
                return _safe_relative(relative.as_posix()).as_posix()
        return _safe_relative(source.name).as_posix()
    raise CustodyError(f"manifest artifact path does not resolve inside run: {value!r}")


def _self_hash_payload(manifest: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(manifest)
    payload.pop("custodyRootSha256", None)
    payload["artifacts"] = [
        artifact
        for artifact in payload.get("artifacts", [])
        if artifact.get("artifactType") != "manifest"
    ]
    return payload


def _regular_files(root: Path) -> set[str]:
    discovered: set[str] = set()
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode) or path.is_symlink():
            raise CustodyError(f"run contains a symlink or special file: {relative}")
        discovered.add(relative)
    return discovered


def _repository_artifact_path(run_dir: Path, value: str) -> Path:
    """Resolve a repository-relative cross-run reference beside ``run_dir``."""

    logical = _safe_relative(value)
    candidates = [REPOSITORY_ROOT.joinpath(*logical.parts)]
    candidates.extend(
        ancestor.parent.joinpath(*logical.parts)
        for ancestor in run_dir.parents
        if ancestor.name == "records"
    )
    for candidate in candidates:
        if candidate.is_file() and not candidate.is_symlink():
            return candidate
    raise CustodyError(f"referenced repository artifact is missing: {value}")


def _instant(value: Any, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise CustodyError(f"invalid {label}: {value!r}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise CustodyError(f"{label} lacks a UTC offset: {value!r}")
    return parsed.astimezone(timezone.utc)


def _required(entries: list[dict[str, Any]], required: dict[str, str]) -> None:
    actual = {(str(entry["path"]), str(entry["artifactType"])) for entry in entries}
    absent = [
        f"{path} ({artifact_type})"
        for path, artifact_type in required.items()
        if (path, artifact_type) not in actual
    ]
    if absent:
        raise CustodyError(
            "run is missing required inventory artifacts: " + ", ".join(absent)
        )


def _command_backend(run_dir: Path, prefix: str = "") -> str:
    command = _load_object(run_dir / f"{prefix}command.json")
    backend = command.get("backend")
    if backend not in {"codex", "external_command", "response_file", "mock"}:
        raise CustodyError(f"v2 analyst command.json has invalid backend: {backend!r}")
    return str(backend)


def _prefixed(inventory: dict[str, str], prefix: str) -> dict[str, str]:
    return {
        f"{prefix}{path}": artifact_type for path, artifact_type in inventory.items()
    }


def _require_invocation_stage(
    run_dir: Path,
    entries: list[dict[str, Any]],
    *,
    prefix: str,
    stdout_artifact_type: str,
) -> set[str]:
    base = {
        f"{prefix}command.json": "command",
        f"{prefix}stdout.txt": stdout_artifact_type,
        f"{prefix}stderr.txt": "stderr",
    }
    _required(entries, base)
    codex = _prefixed(CODEX_STAGE_INVENTORY, prefix)
    paths = {str(entry["path"]) for entry in entries}
    if _command_backend(run_dir, prefix) == "codex":
        _required(entries, codex)
        return {*base, *codex}
    unexpected_codex = sorted(paths & set(codex))
    if unexpected_codex:
        raise CustodyError(
            "non-Codex invocation contains Codex trace artifacts: "
            + ", ".join(unexpected_codex)
        )
    return set(base)


def _verify_invocation_stages(
    run_dir: Path,
    manifest: dict[str, Any],
    entries: list[dict[str, Any]],
) -> set[str]:
    paths = {str(entry["path"]) for entry in entries}
    stage_suffixes = {
        "command.json",
        "stdout.txt",
        "stderr.txt",
        *CODEX_STAGE_INVENTORY,
    }

    def has_stage(prefix: str) -> bool:
        return any(f"{prefix}{suffix}" in paths for suffix in stage_suffixes)

    has_draft = has_stage("draft_")
    has_review = has_stage("pre_submit_review_")
    has_final = has_stage("")
    if not any((has_draft, has_review, has_final)):
        raise CustodyError("analyst inventory contains no invocation stage")
    if has_review and not has_draft:
        raise CustodyError("reviewed inventory has reviewer stage without draft")
    if has_draft and has_final and not has_review:
        raise CustodyError("reviewed inventory has final stage without reviewer")
    allowed: set[str] = set()
    if has_draft:
        allowed.update(
            _require_invocation_stage(
                run_dir,
                entries,
                prefix="draft_",
                stdout_artifact_type="draft_forecast",
            )
        )
    if has_review:
        _required(entries, {"pre_submit_review_prompt.md": "review_prompt"})
        allowed.add("pre_submit_review_prompt.md")
        allowed.update(
            _require_invocation_stage(
                run_dir,
                entries,
                prefix="pre_submit_review_",
                stdout_artifact_type="pre_submit_review",
            )
        )
    if has_final:
        allowed.update(
            _require_invocation_stage(
                run_dir,
                entries,
                prefix="",
                stdout_artifact_type="stdout",
            )
        )
    if has_review and has_final:
        _required(entries, {"revision_prompt.md": "revision_prompt"})
        allowed.add("revision_prompt.md")
    if "pre_submit_review_prompt.md" in paths and not has_review:
        raise CustodyError("review prompt exists without a reviewer invocation")
    if "revision_prompt.md" in paths and not (has_review and has_final):
        raise CustodyError(
            "revision prompt exists without review and final invocations"
        )
    review = manifest.get("preSubmitReview")
    if isinstance(review, dict):
        status = review.get("status")
        expected = {
            "draft_failed": (True, False, False),
            "review_failed": (True, True, False),
            "revision_failed": (True, True, True),
            "completed": (True, True, True),
        }.get(status)
        if expected is None:
            raise CustodyError(f"unknown pre-submit review status: {status!r}")
        if (has_draft, has_review, has_final) != expected:
            raise CustodyError(
                f"pre-submit review stages disagree with status {status!r}"
            )
        if status in {"revision_failed", "completed"}:
            _required(entries, REVIEWED_STAGE_INVENTORY)
    # Parse-failure manifests are sealed before compact review metadata is
    # built; when metadata is absent, the rooted stage filenames are the
    # authoritative record of how far the invocation progressed.
    return allowed


def _verify_cells_activity(
    run_dir: Path, manifest_entries: list[dict[str, Any]], entries: list[dict[str, Any]]
) -> None:
    cells_path = run_dir / "cells.with_activity.json"
    try:
        cells = json.loads(cells_path.read_bytes())
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CustodyError(f"invalid cells.with_activity.json: {exc}") from exc
    if not isinstance(cells, list) or not cells:
        raise CustodyError("cells.with_activity.json must be a nonempty list")
    expected = [
        ref
        for ref in manifest_entries
        if ref.get("artifactType") not in {"cells_with_activity", "manifest"}
    ]
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict) or cell.get("activityLog") != expected:
            raise CustodyError(
                f"cells.with_activity.json cell {index} does not expose the "
                "complete rooted activity prefix"
            )
    entry_paths = {str(entry["path"]) for entry in entries}
    if "cells.with_activity.json" not in entry_paths:
        raise CustodyError("cells.with_activity.json is not in the custody root")


def _verify_analyst_v2(
    run_dir: Path,
    manifest: dict[str, Any],
    manifest_entries: list[dict[str, Any]],
    entries: list[dict[str, Any]],
) -> None:
    if manifest.get("schemaVersion") != "thesis_analyst_run_manifest_v1":
        raise CustodyError("analyst custody mode has the wrong manifest schema")
    parse_failed = (
        isinstance(manifest.get("error"), dict)
        and manifest["error"].get("phase") == "parse"
    )
    if parse_failed:
        base = {
            "prompt.md": "prompt",
            "raw_response.txt": "raw_response",
            "error.json": "error",
        }
        _required(entries, base)
        forbidden = {
            "parsed_cells.json",
            "normalized_cells.json",
            "distribution.json",
            "validation.json",
            "cells.with_activity.json",
        }
        present = {str(entry["path"]) for entry in entries}
        if forbidden & present:
            raise CustodyError("parse-failure inventory contains post-parse artifacts")
        allowed = {*base, *_verify_invocation_stages(run_dir, manifest, entries)}
        unexpected = sorted(present - allowed)
        if unexpected:
            raise CustodyError(
                "parse-failure inventory contains unexpected artifacts: "
                + ", ".join(unexpected)
            )
        return

    if manifest.get("validation") is None:
        raise CustodyError(
            "analyst v2 run is neither parse-failed nor validation-complete"
        )
    _required(entries, ANALYST_COMPLETED_INVENTORY)
    allowed = {
        *ANALYST_COMPLETED_INVENTORY,
        *_verify_invocation_stages(run_dir, manifest, entries),
    }
    review = manifest.get("preSubmitReview")
    if isinstance(review, dict) and review.get("status") == "completed":
        _required(entries, REVIEWED_STAGE_INVENTORY)
    if (
        manifest.get("ok")
        and isinstance(review, dict)
        and review.get("status") != "completed"
    ):
        raise CustodyError(
            "successful reviewed analyst run lacks a completed review inventory"
        )
    unexpected = sorted({str(entry["path"]) for entry in entries} - allowed)
    if unexpected:
        raise CustodyError(
            "completed analyst inventory contains unexpected artifacts: "
            + ", ".join(unexpected)
        )
    _verify_cells_activity(run_dir, manifest_entries, entries)


def _verify_resolver_v2(
    run_dir: Path, manifest: dict[str, Any], entries: list[dict[str, Any]]
) -> None:
    if manifest.get("schemaVersion") != "thesis_resolution_run_v1":
        raise CustodyError("resolver custody mode has the wrong manifest schema")
    facts = manifest.get("facts")
    if not isinstance(facts, list) or not facts:
        raise CustodyError("resolver inventory requires at least one fact")
    rooted_responses = {
        str(entry["path"])
        for entry in entries
        if RESOLVER_RESPONSE_RE.fullmatch(str(entry["path"]))
    }
    invalid_entries = [
        f"{entry['artifactType']}:{entry['path']}"
        for entry in entries
        if entry["artifactType"] != "resolver_response"
        or not RESOLVER_RESPONSE_RE.fullmatch(str(entry["path"]))
    ]
    if invalid_entries:
        raise CustodyError(
            "resolver inventory contains non-response artifacts: "
            + ", ".join(invalid_entries)
        )
    manifest_responses: set[str] = set()
    manifest_response_claims: dict[str, tuple] = {}
    for fact in facts:
        archive = fact.get("responseArchive") if isinstance(fact, dict) else None
        if not isinstance(archive, dict):
            raise CustodyError("resolver fact lacks responseArchive")
        declared = str(archive.get("path", ""))
        relative = _manifest_relative(run_dir, declared, legacy=False)
        if not RESOLVER_RESPONSE_RE.fullmatch(relative):
            raise CustodyError(
                "invalid resolver response archive path: "
                f"declared={declared!r}, resolved={relative!r}"
            )
        if relative in manifest_responses:
            # Several facts may share one archived response (two dataPointId
            # dialects of the same series resolve from the same vintage
            # bytes) — but every reference must declare identical hashes.
            prior = manifest_response_claims.get(relative)
            claim = (
                archive.get("sha256"),
                archive.get("gzipSha256"),
                archive.get("bytes"),
                archive.get("gzipBytes"),
            )
            if prior != claim:
                raise CustodyError(
                    f"conflicting resolver response declarations: {relative}"
                )
            continue
        if archive.get("contentEncoding") != "gzip":
            raise CustodyError(f"resolver response is not declared gzip: {relative}")
        path = _safe_artifact_path(run_dir, relative)
        compressed = path.read_bytes()
        if _sha256(compressed) != archive.get("gzipSha256") or len(
            compressed
        ) != archive.get("gzipBytes"):
            raise CustodyError(f"resolver compressed response mismatch: {relative}")
        try:
            raw = gzip.decompress(compressed)
        except (OSError, EOFError) as exc:
            raise CustodyError(
                f"invalid resolver gzip response {relative}: {exc}"
            ) from exc
        if _sha256(raw) != archive.get("sha256") or len(raw) != archive.get("bytes"):
            raise CustodyError(f"resolver decompressed response mismatch: {relative}")
        manifest_responses.add(relative)
        manifest_response_claims[relative] = (
            archive.get("sha256"),
            archive.get("gzipSha256"),
            archive.get("bytes"),
            archive.get("gzipBytes"),
        )
    if rooted_responses != manifest_responses:
        raise CustodyError(
            "resolver response inventory mismatch: "
            f"rooted={sorted(rooted_responses)}, "
            f"manifest={sorted(manifest_responses)}"
        )


def _verify_ledger_witness_v2(
    run_dir: Path, manifest: dict[str, Any], entries: list[dict[str, Any]]
) -> None:
    if manifest.get("schemaVersion") != "thesis_ledger_witness_run_v1":
        raise CustodyError("ledger witness custody mode has the wrong manifest schema")
    upstream = manifest.get("upstream")
    if not isinstance(upstream, list) or not upstream:
        raise CustodyError("ledger witness inventory requires an upstream archive")
    invalid_entries = [
        f"{entry['artifactType']}:{entry['path']}"
        for entry in entries
        if entry["artifactType"] != "upstream_archive"
        or not LEDGER_WITNESS_ARCHIVE_RE.fullmatch(str(entry["path"]))
    ]
    if invalid_entries:
        raise CustodyError(
            "ledger witness inventory contains non-upstream artifacts: "
            + ", ".join(invalid_entries)
        )
    rooted_archives = {str(entry["path"]) for entry in entries}
    jsonl_claim = manifest.get("jsonl")
    if not isinstance(jsonl_claim, dict):
        raise CustodyError("ledger witness manifest lacks a jsonl commitment")
    manifest_archives: set[str] = set()
    observations_witnessed = False
    for record in upstream:
        archive = record.get("archive") if isinstance(record, dict) else None
        if not isinstance(archive, dict):
            raise CustodyError("ledger witness record lacks an archive")
        declared = str(archive.get("path", ""))
        relative = _manifest_relative(run_dir, declared, legacy=False)
        if not LEDGER_WITNESS_ARCHIVE_RE.fullmatch(relative):
            raise CustodyError(
                "invalid ledger witness archive path: "
                f"declared={declared!r}, resolved={relative!r}"
            )
        if relative in manifest_archives:
            raise CustodyError(f"duplicate ledger witness archive: {relative}")
        if archive.get("contentEncoding") != "gzip":
            raise CustodyError(
                f"ledger witness archive is not declared gzip: {relative}"
            )
        path = _safe_artifact_path(run_dir, relative)
        compressed = path.read_bytes()
        if _sha256(compressed) != archive.get("gzipSha256") or len(
            compressed
        ) != archive.get("gzipBytes"):
            raise CustodyError(
                f"ledger witness compressed archive mismatch: {relative}"
            )
        try:
            raw = gzip.decompress(compressed)
        except (OSError, EOFError) as exc:
            raise CustodyError(
                f"invalid ledger witness gzip archive {relative}: {exc}"
            ) from exc
        if _sha256(raw) != archive.get("sha256") or len(raw) != archive.get("bytes"):
            raise CustodyError(
                f"ledger witness decompressed archive mismatch: {relative}"
            )
        if record.get("role") == "official_observations_jsonl":
            observations_witnessed = True
            lines = [line for line in raw.decode("utf-8").splitlines() if line.strip()]
            if len(lines) != jsonl_claim.get("lineCount"):
                raise CustodyError(
                    "ledger witness jsonl line count mismatch: "
                    f"expected {jsonl_claim.get('lineCount')}, got {len(lines)}"
                )
            if _sha256(raw) != jsonl_claim.get("sha256"):
                raise CustodyError("ledger witness jsonl commitment hash mismatch")
            seen_ids: set[str] = set()
            for number, line in enumerate(lines, start=1):
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise CustodyError(
                        f"ledger witness jsonl line {number} is invalid: {exc}"
                    ) from exc
                record_id = (
                row.get("source_record_id") if isinstance(row, dict) else None
            )
                if not record_id:
                    raise CustodyError(
                        f"ledger witness jsonl line {number} lacks source_record_id"
                    )
                seen_ids.add(str(record_id))
            if len(seen_ids) != jsonl_claim.get("sourceRecordIdCount"):
                raise CustodyError(
                    "ledger witness jsonl source_record_id count mismatch: "
                    f"expected {jsonl_claim.get('sourceRecordIdCount')}, "
                    f"got {len(seen_ids)}"
                )
        manifest_archives.add(relative)
    if not observations_witnessed:
        raise CustodyError(
            "ledger witness run does not witness official_observations.jsonl"
        )
    if rooted_archives != manifest_archives:
        raise CustodyError(
            "ledger witness archive inventory mismatch: "
            f"rooted={sorted(rooted_archives)}, "
            f"manifest={sorted(manifest_archives)}"
        )


def _verified_constituent_runs(
    run_dir: Path,
    manifest: dict[str, Any],
    references: Any,
    *,
    require_complete: bool,
) -> list[dict[str, Any]]:
    if (
        not isinstance(references, list)
        or len(references) != 3
        or not all(isinstance(reference, dict) for reference in references)
    ):
        raise CustodyError("derived ensemble requires exactly 3 constituent runs")
    paths: set[str] = set()
    roots: set[str] = set()
    normalized: list[dict[str, Any]] = []
    target = manifest.get("targetContext")
    for reference in references:
        logical = _safe_relative(str(reference.get("manifestPath") or "")).as_posix()
        root_sha = str(reference.get("custodyRootSha256") or "")
        manifest_sha = str(reference.get("manifestSha256") or "")
        manifest_bytes = reference.get("manifestBytes")
        if (
            logical in paths
            or root_sha in roots
            or not re.fullmatch(r"[0-9a-f]{64}", root_sha)
            or not re.fullmatch(r"[0-9a-f]{64}", manifest_sha)
            or type(manifest_bytes) is not int
            or manifest_bytes < 1
        ):
            raise CustodyError(
                "derived ensemble requires 3 distinct, fully hashed constituent roots"
            )
        parent_path = _repository_artifact_path(run_dir, logical)
        raw = parent_path.read_bytes()
        if _sha256(raw) != manifest_sha or len(raw) != manifest_bytes:
            raise CustodyError(f"constituent manifest integrity mismatch: {logical}")
        parent = _load_object(parent_path)
        if parent.get("custodyRootSha256") != root_sha:
            raise CustodyError(f"constituent custody root mismatch: {logical}")
        verification = verify_run(parent_path.parent)
        if verification.run_mode != "analyst" or not verification.run_succeeded:
            raise CustodyError(
                f"constituent is not a successful analyst run: {logical}"
            )
        if (
            require_complete
            and verification.inventory_status != INVENTORY_STATUS_COMPLETE
        ):
            raise CustodyError(f"constituent is not a complete v2 run: {logical}")
        if parent.get("promptMode") != "fast" or canonical_bytes(
            parent.get("targetContext")
        ) != canonical_bytes(target):
            raise CustodyError(f"constituent target or prompt mode mismatch: {logical}")
        parent_cells_path = _repository_artifact_path(
            run_dir, str(parent.get("cellsPath") or "")
        )
        try:
            parent_cells = json.loads(parent_cells_path.read_bytes())
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise CustodyError(f"invalid constituent cells: {logical}: {exc}") from exc
        if not isinstance(parent_cells, list) or len(parent_cells) != 1:
            raise CustodyError(f"constituent must contain exactly one cell: {logical}")
        parent_run_at = str(parent_cells[0].get("runAt") or "")
        if reference.get("runAt") != parent_run_at:
            raise CustodyError(f"constituent runAt mismatch: {logical}")
        paths.add(logical)
        roots.add(root_sha)
        normalized.append({**reference, "manifestPath": logical})
    return normalized


def _verify_derived_ensemble_v2(
    run_dir: Path,
    manifest: dict[str, Any],
    entries: list[dict[str, Any]],
    custody: dict[str, Any],
) -> None:
    if (
        manifest.get("schemaVersion") != DERIVED_ENSEMBLE_SCHEMA
        or manifest.get("aggregationAlgorithmVersion") != DERIVED_ENSEMBLE_ALGORITHM
        or manifest.get("promptMode") != "median3"
        or manifest.get("ok") is not True
    ):
        raise CustodyError("invalid derived ensemble manifest contract")
    if manifest.get("createdAt") != manifest.get("runStartedAt"):
        raise CustodyError("derived manifest createdAt/runStartedAt mismatch")
    target = manifest.get("targetContext")
    if not isinstance(target, dict) or any(
        canonical_bytes(manifest.get(field)) != canonical_bytes(target.get(field))
        for field in ("series", "period")
    ):
        raise CustodyError("derived manifest target identity mismatch")
    if (
        _manifest_relative(
            run_dir, str(manifest.get("cellsPath") or ""), legacy=False
        )
        != "cells.with_activity.json"
    ):
        raise CustodyError("derived manifest cellsPath is outside its run")
    actual_inventory = [
        (str(entry["artifactType"]), str(entry["path"])) for entry in entries
    ]
    if actual_inventory != [
        ("derived_distribution", "distribution.json"),
        ("cells_with_activity", "cells.with_activity.json"),
    ]:
        raise CustodyError("derived ensemble has an invalid local artifact inventory")

    references = _verified_constituent_runs(
        run_dir,
        manifest,
        manifest.get("constituentRuns"),
        require_complete=True,
    )
    if canonical_bytes(custody.get("constituentCustodyRoots")) != canonical_bytes(
        references
    ):
        raise CustodyError("custody root constituent chain differs from manifest")
    if manifest.get("constituentManifests") != [
        reference["manifestPath"] for reference in references
    ]:
        raise CustodyError("derived constituent manifest list is inconsistent")

    start = _instant(manifest.get("runStartedAt"), "derived runStartedAt")
    for reference in references:
        if _instant(reference.get("runAt"), "constituent runAt") > start:
            raise CustodyError("derived run starts before a constituent was sealed")

    cells_path = run_dir / "cells.with_activity.json"
    distribution_path = run_dir / "distribution.json"
    try:
        cells = json.loads(cells_path.read_bytes())
        distribution = json.loads(distribution_path.read_bytes())
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CustodyError(f"invalid derived JSON artifact: {exc}") from exc
    if not isinstance(cells, list) or len(cells) != 1 or not isinstance(cells[0], dict):
        raise CustodyError("derived cells payload must contain exactly one cell")
    cell = cells[0]
    if (
        cell.get("runStartedAt") != manifest.get("runStartedAt")
        or _instant(cell.get("runAt"), "derived cell runAt") < start
        or cell.get("aggregationAlgorithmVersion") != DERIVED_ENSEMBLE_ALGORITHM
        or canonical_bytes(cell.get("constituentRuns")) != canonical_bytes(references)
        or cell.get("slug") != (manifest.get("targetContext") or {}).get("catalogSlug")
    ):
        raise CustodyError("derived cell metadata differs from its manifest")
    for field in (
        "registrationCommit",
        "targetContentHash",
        "targetRegistrationPath",
        "registeredAtUtc",
    ):
        target_value = (manifest.get("targetContext") or {}).get(field)
        if target_value not in (None, "") and (
            manifest.get(field) != target_value or cell.get(field) != target_value
        ):
            raise CustodyError(f"derived registration binding mismatch: {field}")

    summary = distribution.get("summary") if isinstance(distribution, dict) else None
    interval = summary.get("interval80") if isinstance(summary, dict) else None
    if (
        distribution.get("format") != "numeric_cdf_v1"
        or not isinstance(interval, dict)
        or canonical_bytes(summary.get("pointEstimate"))
        != canonical_bytes(cell.get("pointEstimate"))
        or canonical_bytes(interval.get("lower")) != canonical_bytes(cell.get("ciLow"))
        or canonical_bytes(interval.get("upper")) != canonical_bytes(cell.get("ciHigh"))
    ):
        raise CustodyError("derived distribution summary differs from its cell")

    activity = cell.get("activityLog")
    if not isinstance(activity, list) or len(activity) != 4:
        raise CustodyError(
            "derived activity log must expose 3 parents and distribution"
        )
    for activity_ref, reference in zip(activity[:3], references):
        expected = {
            "artifactType": "constituent_manifest",
            "path": reference["manifestPath"],
            "sha256": reference["manifestSha256"],
            "bytes": reference["manifestBytes"],
            "custodyRootSha256": reference["custodyRootSha256"],
            "createdAt": manifest["runStartedAt"],
        }
        if canonical_bytes(activity_ref) != canonical_bytes(expected):
            raise CustodyError("derived activity log has a mismatched constituent")
    distribution_ref = next(
        ref
        for ref in manifest["artifacts"]
        if ref.get("artifactType") == "derived_distribution"
    )
    if canonical_bytes(activity[3]) != canonical_bytes(distribution_ref):
        raise CustodyError("derived activity log has a mismatched distribution")


def _verify_legacy_derived_without_root(
    run_dir: Path, manifest: dict[str, Any]
) -> CustodyVerification:
    """Verify the six immutable July-8 median runs as incomplete legacy data."""

    if (
        manifest.get("schemaVersion") != DERIVED_ENSEMBLE_SCHEMA
        or manifest.get("createdAt") != LEGACY_DERIVED_AT
        or manifest.get("promptMode") != "median3"
        or manifest.get("aggregationAlgorithmVersion")
        not in {None, DERIVED_ENSEMBLE_ALGORITHM}
        or manifest.get("ok") is not True
        or manifest.get("runMode") is not None
        or manifest.get("custodyInventoryVersion") is not None
        or manifest.get("custodyRootSha256") is not None
        or run_dir.parent.name != "2026-07-08"
        or run_dir.name not in LEGACY_DERIVED_DIRS
    ):
        raise CustodyError(f"missing custody root: {run_dir / 'custody_root.json'}")
    discovered = _regular_files(run_dir)
    expected_files = {"cells.with_activity.json", "distribution.json", "manifest.json"}
    if discovered != expected_files:
        raise CustodyError("legacy derived run has an unexpected file inventory")
    references = manifest.get("constituentManifests")
    artifacts = manifest.get("artifacts")
    if (
        not isinstance(references, list)
        or len(references) != 3
        or len(set(references)) != 3
        or not isinstance(artifacts, list)
        or len(artifacts) != 4
    ):
        raise CustodyError("legacy derived run has an invalid constituent inventory")
    parent_entries = [
        entry
        for entry in artifacts
        if isinstance(entry, dict)
        and entry.get("artifactType") == "constituent_manifest"
    ]
    distribution_entries = [
        entry
        for entry in artifacts
        if isinstance(entry, dict)
        and entry.get("artifactType") == "derived_distribution"
    ]
    if [entry.get("path") for entry in parent_entries] != references or len(
        distribution_entries
    ) != 1:
        raise CustodyError("legacy derived artifacts do not match constituent list")
    parent_hashes: set[str] = set()
    for entry in parent_entries:
        parent_path = _repository_artifact_path(run_dir, str(entry["path"]))
        raw = parent_path.read_bytes()
        if _sha256(raw) != entry.get("sha256") or len(raw) != entry.get("bytes"):
            raise CustodyError("legacy constituent manifest integrity mismatch")
        parent_hashes.add(str(entry.get("sha256")))
    if len(parent_hashes) != 3:
        raise CustodyError("legacy derived run lacks 3 distinct constituent manifests")
    distribution_path = _repository_artifact_path(
        run_dir, str(distribution_entries[0]["path"])
    )
    raw_distribution = distribution_path.read_bytes()
    if (
        distribution_path.parent != run_dir
        or _sha256(raw_distribution) != distribution_entries[0].get("sha256")
        or len(raw_distribution) != distribution_entries[0].get("bytes")
    ):
        raise CustodyError("legacy derived distribution integrity mismatch")
    cells_path = _repository_artifact_path(
        run_dir, str(manifest.get("cellsPath") or "")
    )
    try:
        cells = json.loads(cells_path.read_bytes())
        distribution = json.loads(raw_distribution)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CustodyError(f"invalid legacy derived JSON: {exc}") from exc
    if not isinstance(cells, list) or len(cells) != 1:
        raise CustodyError("legacy derived cells must contain exactly one cell")
    summary = distribution.get("summary") or {}
    interval = summary.get("interval80") or {}
    cell = cells[0]
    if (
        cell.get("runAt") != LEGACY_DERIVED_AT
        or cell.get("aggregationAlgorithmVersion")
        not in {None, DERIVED_ENSEMBLE_ALGORITHM}
        or canonical_bytes(cell.get("pointEstimate"))
        != canonical_bytes(summary.get("pointEstimate"))
        or canonical_bytes(cell.get("ciLow")) != canonical_bytes(interval.get("lower"))
        or canonical_bytes(cell.get("ciHigh")) != canonical_bytes(interval.get("upper"))
    ):
        raise CustodyError("legacy derived cells differ from distribution")
    return CustodyVerification(
        run_mode="derived_ensemble",
        custody_inventory_version=1,
        inventory_status=INVENTORY_STATUS_LEGACY,
        custody_root_sha256=_sha256((run_dir / "manifest.json").read_bytes()),
        artifact_count=len(artifacts),
        run_succeeded=True,
    )


def verify_run(run_dir: Path) -> CustodyVerification:
    run_dir = run_dir.resolve()
    root_path = run_dir / "custody_root.json"
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file():
        raise CustodyError(f"missing manifest: {manifest_path}")
    manifest = _load_object(manifest_path)
    if not root_path.is_file():
        return _verify_legacy_derived_without_root(run_dir, manifest)
    custody = _load_object(root_path)
    if custody.get("schemaVersion") != "thesis_custody_root_v1":
        raise CustodyError(
            f"unsupported custody schema: {custody.get('schemaVersion')!r}"
        )

    custody_version = custody.get("custodyInventoryVersion")
    manifest_version = manifest.get("custodyInventoryVersion")
    legacy = custody_version is None and manifest_version is None
    if legacy:
        version = 1
        run_mode = (
            "analyst"
            if manifest.get("schemaVersion") == "thesis_analyst_run_manifest_v1"
            else "unknown"
        )
    else:
        if (
            custody_version != INVENTORY_VERSION
            or manifest_version != INVENTORY_VERSION
        ):
            raise CustodyError(
                "custody inventory version mismatch: "
                f"root={custody_version!r}, manifest={manifest_version!r}"
            )
        version = INVENTORY_VERSION
        run_mode = str(custody.get("runMode"))
        if run_mode != manifest.get("runMode") or run_mode not in {
            "analyst",
            "resolver",
            "derived_ensemble",
            "ledger_witness",
        }:
            raise CustodyError(
                "custody run mode mismatch: "
                f"root={run_mode!r}, manifest={manifest.get('runMode')!r}"
            )

    entries = custody.get("artifacts")
    if not isinstance(entries, list):
        raise CustodyError("custody_root.json artifacts must be a list")
    seen_identities: set[tuple[str, str]] = set()
    seen_paths: set[str] = set()
    normalized_entries: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise CustodyError("custody artifact entry is not an object")
        artifact_type = str(entry.get("artifactType"))
        relative = _safe_relative(str(entry.get("path"))).as_posix()
        if relative in {"manifest.json", "custody_root.json"}:
            raise CustodyError(
                f"control file appears as ordinary custody artifact: {relative}"
            )
        identity = (artifact_type, relative)
        if identity in seen_identities or relative in seen_paths:
            raise CustodyError(
                f"duplicate custody artifact path: {artifact_type} {relative}"
            )
        seen_identities.add(identity)
        seen_paths.add(relative)
        path = _safe_artifact_path(run_dir, relative)
        if not path.is_file() or path.is_symlink():
            raise CustodyError(
                f"missing or non-regular artifact {artifact_type}: {relative}"
            )
        raw = path.read_bytes()
        actual_sha = _sha256(raw)
        if actual_sha != entry.get("sha256"):
            raise CustodyError(
                f"raw SHA-256 mismatch for {artifact_type} {relative}: "
                f"expected {entry.get('sha256')}, got {actual_sha}"
            )
        if len(raw) != entry.get("bytes"):
            raise CustodyError(
                f"byte-count mismatch for {artifact_type} {relative}: "
                f"expected {entry.get('bytes')}, got {len(raw)}"
            )
        if not legacy and path.suffix == ".json" and "canonicalJsonSha256" not in entry:
            raise CustodyError(
                f"v2 JSON custody artifact lacks canonical hash: {relative}"
            )
        if "canonicalJsonSha256" in entry:
            try:
                value = json.loads(raw)
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise CustodyError(
                    f"artifact marked as JSON is invalid: {relative}: {exc}"
                ) from exc
            actual_canonical = canonical_sha256(value)
            if actual_canonical != entry["canonicalJsonSha256"]:
                raise CustodyError(
                    "canonical JSON SHA-256 mismatch for "
                    f"{artifact_type} {relative}: "
                    f"expected {entry['canonicalJsonSha256']}, "
                    f"got {actual_canonical}"
                )
        normalized_entries.append(
            {**entry, "artifactType": artifact_type, "path": relative}
        )

    manifest_entries = manifest.get("artifacts")
    if not isinstance(manifest_entries, list):
        raise CustodyError("manifest artifacts must be a list")
    normalized_manifest: list[tuple[str, str]] = []
    normalized_manifest_refs: list[dict[str, Any]] = []
    manifest_paths: set[str] = set()
    for ref in manifest_entries:
        if not isinstance(ref, dict):
            raise CustodyError("manifest artifact entry is not an object")
        artifact_type = str(ref.get("artifactType"))
        relative = _manifest_relative(run_dir, str(ref.get("path")), legacy=legacy)
        if relative in manifest_paths:
            raise CustodyError(
                f"manifest references an artifact path more than once: {relative}"
            )
        manifest_paths.add(relative)
        normalized_manifest.append((artifact_type, relative))
        normalized_manifest_refs.append(
            {**ref, "artifactType": artifact_type, "path": relative}
        )
    rooted_order = [
        (str(entry["artifactType"]), str(entry["path"])) for entry in normalized_entries
    ]
    referenced_without_manifest = [
        item for item in normalized_manifest if item[0] != "manifest"
    ]
    if legacy:
        if set(rooted_order) != set(referenced_without_manifest):
            raise CustodyError(
                "custody artifact coverage mismatch: "
                f"rooted={sorted(rooted_order)}, "
                f"referenced={sorted(referenced_without_manifest)}"
            )
    elif rooted_order != referenced_without_manifest:
        raise CustodyError(
            "v2 custody artifacts must match manifest artifacts one-to-one and in order"
        )
    if not legacy:
        nonself_refs = [
            ref for ref in normalized_manifest_refs if ref["artifactType"] != "manifest"
        ]
        for ref, entry in zip(nonself_refs, normalized_entries):
            for field in ("sha256", "bytes"):
                if ref.get(field) != entry.get(field):
                    raise CustodyError(
                        "manifest/custody integrity mismatch for "
                        f"{entry['path']} field {field}: "
                        f"manifest={ref.get(field)!r}, custody={entry.get(field)!r}"
                    )
            if "canonicalJsonSha256" in ref and ref["canonicalJsonSha256"] != entry.get(
                "canonicalJsonSha256"
            ):
                raise CustodyError(
                    f"manifest/custody canonical JSON mismatch for {entry['path']}"
                )

    if legacy and manifest.get("ok"):
        required_types = {"prompt", "command", "normalized_cell", "cells_with_activity"}
        present_types = {artifact_type for artifact_type, _ in rooted_order}
        absent = sorted(required_types - present_types)
        if absent:
            raise CustodyError(
                "successful legacy run is missing required custody artifact types: "
                + ", ".join(absent)
            )

    manifest_without_root = copy.deepcopy(manifest)
    manifest_without_root.pop("custodyRootSha256", None)
    manifest_commitment = custody.get("manifestWithoutCustodyRoot") or {}
    actual_manifest_sha = canonical_sha256(manifest_without_root)
    if actual_manifest_sha != manifest_commitment.get("canonicalJsonSha256"):
        raise CustodyError(
            "manifest-without-root canonical SHA-256 mismatch: expected "
            f"{manifest_commitment.get('canonicalJsonSha256')}, "
            f"got {actual_manifest_sha}"
        )
    self_refs = [
        ref for ref in manifest_entries if ref.get("artifactType") == "manifest"
    ]
    if len(self_refs) != 1:
        raise CustodyError(
            "manifest must contain exactly one self artifact entry, "
            f"got {len(self_refs)}"
        )
    if (
        _manifest_relative(run_dir, str(self_refs[0].get("path")), legacy=legacy)
        != "manifest.json"
    ):
        raise CustodyError("manifest self artifact does not point to manifest.json")
    self_bytes = canonical_bytes(_self_hash_payload(manifest))
    self_sha = _sha256(self_bytes)
    if self_sha != self_refs[0].get("sha256"):
        raise CustodyError(
            "manifest self-entry SHA-256 mismatch: "
            f"expected {self_refs[0].get('sha256')}, got {self_sha}"
        )
    if len(self_bytes) != self_refs[0].get("bytes"):
        raise CustodyError(
            "manifest self-entry byte-count mismatch: "
            f"expected {self_refs[0].get('bytes')}, got {len(self_bytes)}"
        )
    actual_root_sha = canonical_sha256(custody)
    if actual_root_sha != manifest.get("custodyRootSha256"):
        raise CustodyError(
            "custody root SHA-256 mismatch: "
            f"expected {manifest.get('custodyRootSha256')}, got {actual_root_sha}"
        )

    if not legacy:
        discovered = _regular_files(run_dir)
        expected_files = {*manifest_paths, "custody_root.json"}
        if discovered != expected_files:
            raise CustodyError(
                "v2 run directory inventory mismatch: "
                f"unreferenced={sorted(discovered - expected_files)}, "
                f"missing={sorted(expected_files - discovered)}"
            )
        if run_mode == "analyst":
            _verify_analyst_v2(run_dir, manifest, manifest_entries, normalized_entries)
        elif run_mode == "resolver":
            _verify_resolver_v2(run_dir, manifest, normalized_entries)
        elif run_mode == "ledger_witness":
            _verify_ledger_witness_v2(run_dir, manifest, normalized_entries)
        elif run_mode == "derived_ensemble":
            _verify_derived_ensemble_v2(run_dir, manifest, normalized_entries, custody)
        else:
            raise CustodyError(f"unsupported custody run mode: {run_mode}")

    return CustodyVerification(
        run_mode=run_mode,
        custody_inventory_version=version,
        inventory_status=INVENTORY_STATUS_LEGACY
        if legacy
        else INVENTORY_STATUS_COMPLETE,
        custody_root_sha256=actual_root_sha,
        artifact_count=len(entries),
        run_succeeded=(
            (
                run_mode == "analyst"
                and manifest.get("ok") is True
                and isinstance(manifest.get("validation"), dict)
                and manifest["validation"].get("ok") is True
            )
            or (run_mode == "derived_ensemble" and manifest.get("ok") is True)
        ),
    )


def _recorder_archive(
    records_root: Path, record: dict[str, Any], expected_body_root: Path
) -> tuple[str, Any]:
    logical = str(record.get("archivePath", ""))
    if not logical.startswith("records/"):
        raise CustodyError(f"recorder archive path is not logical: {logical!r}")
    relative = _safe_relative(logical).parts[1:]
    path = records_root.joinpath(*relative)
    try:
        body_relative = (
            path.resolve().relative_to(expected_body_root.resolve()).as_posix()
        )
    except ValueError as exc:
        raise CustodyError(
            f"recorder archive escapes its body directory: {logical}"
        ) from exc
    if not path.is_file() or path.is_symlink():
        raise CustodyError(f"recorder archive is missing: {logical}")
    compressed = path.read_bytes()
    if _sha256(compressed) != record.get("archiveSha256") or len(
        compressed
    ) != record.get("archiveBytes"):
        raise CustodyError(f"recorder compressed archive mismatch: {logical}")
    try:
        raw = gzip.decompress(compressed)
        payload = json.loads(raw)
    except (OSError, EOFError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CustodyError(
            f"invalid recorder JSON gzip archive {logical}: {exc}"
        ) from exc
    if _sha256(raw) != record.get("sha256") or len(raw) != record.get("bytes"):
        raise CustodyError(f"recorder decompressed archive mismatch: {logical}")
    return body_relative, payload


def verify_recorder_snapshot(snapshot_path: Path) -> CustodyVerification:
    snapshot_path = snapshot_path.resolve()
    payload = _load_object(snapshot_path)
    if (
        payload.get("schemaVersion") != "thesis_record_snapshot_v2"
        or payload.get("snapshotKind") != "recorder_run"
    ):
        raise CustodyError("file is not a recorder snapshot")
    version = payload.get("custodyInventoryVersion")
    legacy = version is None
    if not legacy and (
        version != INVENTORY_VERSION or payload.get("runMode") != "recorder"
    ):
        raise CustodyError("unsupported recorder custody inventory version or mode")
    records_root = snapshot_path.parents[1]
    run_id = str(payload.get("runId", ""))
    body_root = snapshot_path.parent / f"bodies-{run_id}"
    referenced: set[str] = set()
    surfaces = payload.get("surfaces")
    if not isinstance(surfaces, dict):
        raise CustodyError("recorder snapshot lacks surfaces")
    if not legacy:
        missing_surfaces = sorted(set(RECORDER_REQUIRED_SURFACES) - set(surfaces))
        if missing_surfaces:
            raise CustodyError(
                "recorder is missing required surfaces: " + ", ".join(missing_surfaces)
            )
    surface_payloads: dict[str, Any] = {}
    for key, record in surfaces.items():
        if not isinstance(record, dict):
            raise CustodyError(f"recorder surface {key} is not an object")
        relative, archive_payload = _recorder_archive(records_root, record, body_root)
        surface_payloads[str(key)] = archive_payload
        if not legacy and RECORDER_REQUIRED_SURFACES.get(str(key)) != relative:
            raise CustodyError(
                f"recorder surface {key} has unexpected archive path {relative}"
            )
        if relative in referenced:
            raise CustodyError(f"duplicate recorder archive path: {relative}")
        referenced.add(relative)
    live = payload.get("liveForecasts") or {}
    if not isinstance(live, dict):
        raise CustodyError("recorder liveForecasts must be an object")
    if not legacy and set(live) != set(RECORDER_REQUIRED_LIVE):
        raise CustodyError(
            "recorder live forecast inventory is not the required exact set"
        )
    for key, record in live.items():
        relative, _archive_payload = _recorder_archive(records_root, record, body_root)
        if not legacy and RECORDER_REQUIRED_LIVE.get(str(key)) != relative:
            raise CustodyError(
                f"recorder live forecast {key} has unexpected archive path {relative}"
            )
        if relative in referenced:
            raise CustodyError(f"duplicate recorder archive path: {relative}")
        referenced.add(relative)
    chunks = payload.get("logChunks") or {}
    if not isinstance(chunks, dict):
        raise CustodyError("recorder logChunks must be an object")
    chunk_payloads: dict[str, Any] = {}
    chunk_relatives: dict[str, str] = {}
    for key, record in chunks.items():
        relative, archive_payload = _recorder_archive(records_root, record, body_root)
        chunk_payloads[str(key)] = archive_payload
        chunk_relatives[str(key)] = relative
        if relative in referenced:
            raise CustodyError(f"duplicate recorder archive path: {relative}")
        referenced.add(relative)
    if not legacy:
        log_manifest = surface_payloads["log"]
        if log_manifest.get("schemaVersion") == "thesis_log_v3":
            expected_chunks: dict[str, dict[str, Any]] = {}
            collections = log_manifest.get("collections")
            if not isinstance(collections, dict):
                raise CustodyError("recorder v3 log manifest lacks collections")
            for collection, collection_manifest in collections.items():
                references = (
                    collection_manifest.get("chunks")
                    if isinstance(collection_manifest, dict)
                    else None
                )
                if not isinstance(references, list):
                    raise CustodyError(
                        f"recorder v3 log collection {collection} lacks chunks"
                    )
                for expected_index, reference in enumerate(references):
                    if (
                        not isinstance(reference, dict)
                        or reference.get("index") != expected_index
                    ):
                        raise CustodyError(
                            f"recorder v3 {collection} chunk indexes are invalid"
                        )
                    expected_chunks[f"{collection}:{expected_index}"] = reference
            if set(chunks) != set(expected_chunks):
                raise CustodyError(
                    "recorder v3 log chunk inventory differs from its manifest"
                )
            for key, reference in expected_chunks.items():
                record = chunks[key]
                chunk = chunk_payloads[key]
                expected_collection, expected_index_text = key.split(":", 1)
                expected_index = int(expected_index_text)
                expected_url = f"/log/{expected_collection}/{expected_index}.json"
                if reference.get("url") != expected_url:
                    raise CustodyError(
                        f"recorder v3 chunk {key} has invalid manifest URL"
                    )
                expected_relative = f"{expected_url.lstrip('/')}.gz"
                if chunk_relatives[key] != expected_relative:
                    raise CustodyError(
                        f"recorder v3 chunk {key} archive path mismatch: "
                        f"expected {expected_relative}, got {chunk_relatives[key]}"
                    )
                if record.get("manifestSha256") != reference.get("sha256"):
                    raise CustodyError(
                        f"recorder v3 chunk {key} manifest hash link mismatch"
                    )
                expected_fields = {
                    "schemaVersion": "thesis_log_chunk_v1",
                    "logSchemaVersion": "thesis_log_v3",
                    "collection": expected_collection,
                    "chunkIndex": expected_index,
                    "count": reference.get("count"),
                }
                if any(
                    chunk.get(name) != value for name, value in expected_fields.items()
                ):
                    raise CustodyError(f"recorder v3 chunk {key} metadata mismatch")
                if len(chunk.get("rows", [])) != reference.get("count"):
                    raise CustodyError(f"recorder v3 chunk {key} row count mismatch")
                if canonical_sha256(chunk) != reference.get("sha256"):
                    raise CustodyError(
                        f"recorder v3 chunk {key} canonical hash mismatch"
                    )
        elif chunks:
            raise CustodyError("non-v3 recorder log unexpectedly has log chunks")
        discovered = _regular_files(body_root)
        if discovered != referenced:
            raise CustodyError(
                "recorder body inventory mismatch: "
                f"unreferenced={sorted(discovered - referenced)}, "
                f"missing={sorted(referenced - discovered)}"
            )
    return CustodyVerification(
        run_mode="recorder",
        custody_inventory_version=1 if legacy else INVENTORY_VERSION,
        inventory_status=INVENTORY_STATUS_LEGACY
        if legacy
        else INVENTORY_STATUS_COMPLETE,
        custody_root_sha256=_sha256(snapshot_path.read_bytes()),
        artifact_count=len(referenced) + 1,
        run_succeeded=False,
    )


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: verify_custody.py <run-dir|recorder-digest.json>", file=sys.stderr
        )
        return 2
    target = Path(sys.argv[1])
    try:
        result = (
            verify_run(target) if target.is_dir() else verify_recorder_snapshot(target)
        )
    except CustodyError as exc:
        print(f"CUSTODY BROKEN: {exc}", file=sys.stderr)
        return 1
    print(
        f"custody OK: {target} mode={result.run_mode} "
        f"inventory=v{result.custody_inventory_version} "
        f"status={result.inventory_status} artifacts={result.artifact_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
