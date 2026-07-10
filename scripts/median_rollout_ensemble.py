#!/usr/bin/env python3
"""Build median-of-rollouts derived runs from rollout batch manifests.

Median prediction sampling — run K independent rollouts of the same
question and publish the pointwise median of their CDFs — is the
inference-time aggregation validated in Turtel et al. 2025
(arXiv:2505.17989). Each rollout here is a normal recorded thesis.analyst
fast run; this script derives one `thesis.analyst.median3` run per target
from their published intervals and records it with references to every
constituent manifest. No new model call happens: the derived run is a
deterministic function of already-recorded artifacts.

Usage:
    python3 scripts/median_rollout_ensemble.py \
        --batch records/thesis-analyst/batches/....json \
        --batch records/thesis-analyst/batches/....json \
        --batch records/thesis-analyst/batches/....json \
        [--out-list /tmp/median-manifests.txt] [--dry-run]
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import pathlib
import sys
from typing import Any

from canonical_json import canonical_bytes, canonical_sha256
from verify_custody import CustodyError, verify_run

ROOT = pathlib.Path(__file__).resolve().parents[1]

POINT_COUNT = 201
REQUIRED_ROLLOUTS = 3
AGGREGATION_ALGORITHM_VERSION = "pointwise_median_cdf_v1"
CUSTODY_INVENTORY_VERSION = 2
MANIFEST_HASH_MODE = (
    "canonical-json-v1; exclude artifacts where artifactType=manifest and "
    "exclude custodyRootSha256"
)


def utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .strftime("%Y-%m-%dT%H:%M:%SZ")
    )


def repo_path(path: str | pathlib.Path) -> pathlib.Path:
    candidate = pathlib.Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def repo_relative(path: pathlib.Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def interval_knots(cell: dict[str, Any]) -> list[tuple[float, float]]:
    """The same five CDF anchors the site derives from an 80% interval
    (site/src/data/prediction-distribution.ts buildNumericCdfFromInterval)."""
    point = float(cell["pointEstimate"])
    ci_low = float(cell["ciLow"])
    ci_high = float(cell["ciHigh"])
    lower_spread = max(abs(point - ci_low), 1e-9)
    upper_spread = max(abs(ci_high - point), 1e-9)
    return [
        (ci_low - lower_spread * 1.5, 0.0),
        (ci_low, 0.1),
        (point, 0.5),
        (ci_high, 0.9),
        (ci_high + upper_spread * 1.5, 1.0),
    ]


def cdf_at(knots: list[tuple[float, float]], value: float) -> float:
    if value <= knots[0][0]:
        return knots[0][1]
    for index in range(1, len(knots)):
        prev_value, prev_prob = knots[index - 1]
        knot_value, knot_prob = knots[index]
        if value <= knot_value:
            width = knot_value - prev_value
            if width <= 0:
                return knot_prob
            ratio = (value - prev_value) / width
            return prev_prob + ratio * (knot_prob - prev_prob)
    return knots[-1][1]


def quantile_from_points(points: list[dict[str, float]], q: float) -> float:
    for index in range(1, len(points)):
        prev, current = points[index - 1], points[index]
        if current["probability"] >= q:
            span = current["probability"] - prev["probability"]
            if span <= 0:
                return current["value"]
            ratio = (q - prev["probability"]) / span
            return prev["value"] + ratio * (current["value"] - prev["value"])
    return points[-1]["value"]


def decimal_places(value: Any) -> int:
    text = repr(float(value))
    if "e" in text or "E" in text:
        return 6
    if "." not in text:
        return 0
    return min(len(text.split(".")[1].rstrip("0")), 6)


def median(values: list[float]) -> float:
    ordered = sorted(values)
    count = len(ordered)
    middle = count // 2
    if count % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def median_distribution(cells: list[dict[str, Any]]) -> dict[str, Any]:
    knot_sets = [interval_knots(cell) for cell in cells]
    support_lower = min(knots[0][0] for knots in knot_sets)
    support_upper = max(knots[-1][0] for knots in knot_sets)
    step = (support_upper - support_lower) / (POINT_COUNT - 1)
    points = []
    for index in range(POINT_COUNT):
        value = (
            support_upper if index == POINT_COUNT - 1 else support_lower + step * index
        )
        probability = median([cdf_at(knots, value) for knots in knot_sets])
        points.append(
            {
                "value": round(value, 10),
                "probability": round(probability, 10),
            }
        )
    return {
        "format": "numeric_cdf_v1",
        "pointCount": POINT_COUNT,
        "support": {
            "lower": round(support_lower, 10),
            "upper": round(support_upper, 10),
        },
        "points": points,
    }


def collect_rollouts(
    batch_paths: list[pathlib.Path],
) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for batch_path in batch_paths:
        batch = json.loads(batch_path.read_text())
        for result in batch.get("results", []):
            if not result.get("ok"):
                continue
            target = result.get("target") or {}
            slug = target.get("catalogSlug")
            cells_path = result.get("cellsPath")
            manifest_path = result.get("manifestPath")
            if not slug or not cells_path or not manifest_path:
                continue
            cells = json.loads(repo_path(cells_path).read_text())
            if not cells:
                continue
            groups.setdefault(slug, []).append(
                {
                    "target": target,
                    "cell": cells[0],
                    "cellsPath": cells_path,
                    "manifestPath": manifest_path,
                }
            )
    return groups


def validate_constituent_rollouts(
    rollouts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Require exactly three distinct runs whose custody roots verify."""
    if len(rollouts) != REQUIRED_ROLLOUTS:
        raise ValueError(
            f"median3 requires exactly 3 constituent runs; received {len(rollouts)}"
        )

    references: list[dict[str, Any]] = []
    canonical_target: bytes | None = None
    for rollout in rollouts:
        manifest_path = repo_path(rollout["manifestPath"])
        try:
            verification = verify_run(manifest_path.parent)
        except CustodyError as exc:
            raise ValueError(
                f"constituent custody verification failed: {manifest_path}: {exc}"
            ) from exc
        manifest = json.loads(manifest_path.read_text())
        custody_root = manifest.get("custodyRootSha256")
        run_at = rollout["cell"].get("runAt")
        if not custody_root or not run_at:
            raise ValueError(
                f"constituent lacks custody root or runAt: {manifest_path}"
            )
        # Tests may replace verify_run with a no-op to exercise only the
        # distinct-reference rule. Real runs must be complete, successful
        # analyst inventories.
        if verification is not None:
            if (
                verification.run_mode != "analyst"
                or verification.inventory_status != "complete"
                or not verification.run_succeeded
            ):
                raise ValueError(
                    "median3 constituents must be successful complete-v2 "
                    f"analyst runs: {manifest_path}"
                )
            if (
                manifest.get("schemaVersion") != "thesis_analyst_run_manifest_v1"
                or manifest.get("promptMode") != "fast"
                or manifest.get("ok") is not True
            ):
                raise ValueError(
                    f"median3 constituent is not a successful fast run: {manifest_path}"
                )
            target = rollout.get("target")
            if not isinstance(target, dict) or canonical_bytes(
                manifest.get("targetContext")
            ) != canonical_bytes(target):
                raise ValueError(
                    f"median3 constituent target context mismatch: {manifest_path}"
                )
            encoded_target = canonical_bytes(target)
            if canonical_target is None:
                canonical_target = encoded_target
            elif encoded_target != canonical_target:
                raise ValueError("median3 constituents do not share one target")
        manifest_raw = manifest_path.read_bytes()
        references.append(
            {
                "manifestPath": (
                    repo_relative(manifest_path)
                    if manifest_path.is_relative_to(ROOT)
                    else str(manifest_path)
                ),
                "manifestSha256": hashlib.sha256(manifest_raw).hexdigest(),
                "manifestBytes": len(manifest_raw),
                "custodyRootSha256": str(custody_root),
                "runAt": str(run_at),
            }
        )

    roots = {reference["custodyRootSha256"] for reference in references}
    manifests = {reference["manifestPath"] for reference in references}
    if len(roots) != REQUIRED_ROLLOUTS or len(manifests) != REQUIRED_ROLLOUTS:
        raise ValueError(
            "median3 requires exactly 3 distinct custody-verifiable run references"
        )
    return references


def build_derived_run(
    slug: str,
    rollouts: list[dict[str, Any]],
    run_at: str,
    *,
    sealed_at: str | None = None,
) -> tuple[dict[str, Any], pathlib.Path]:
    rollouts = sorted(
        rollouts,
        key=lambda row: (row["cell"].get("runAt", ""), row["manifestPath"]),
    )
    constituent_runs = validate_constituent_rollouts(rollouts)
    cells = [rollout["cell"] for rollout in rollouts]
    target = rollouts[0]["target"]
    manifest_source = json.loads(repo_path(rollouts[0]["manifestPath"]).read_text())
    agent_meta = manifest_source.get("agent", {})

    distribution = median_distribution(cells)
    precision = max(
        max(
            decimal_places(cell["pointEstimate"]),
            decimal_places(cell["ciLow"]),
            decimal_places(cell["ciHigh"]),
        )
        for cell in cells
    )
    q10 = round(quantile_from_points(distribution["points"], 0.10), precision)
    q50 = round(quantile_from_points(distribution["points"], 0.50), precision)
    q90 = round(quantile_from_points(distribution["points"], 0.90), precision)
    distribution["summary"] = {
        "pointEstimate": q50,
        "median": q50,
        "interval80": {"lower": q10, "upper": q90},
    }
    distribution["provenance"] = "agent_reported"

    nearest = min(cells, key=lambda cell: abs(cell["pointEstimate"] - q50))
    run_ats = [cell.get("runAt", "?") for cell in cells]
    rollout_points = [cell["pointEstimate"] for cell in cells]
    widths = [round(cell["ciHigh"] - cell["ciLow"], precision + 2) for cell in cells]
    source_context: list[str] = []
    for cell in cells:
        for url in cell.get("sourceContext", []):
            if url not in source_context:
                source_context.append(url)

    derived_cell = {
        key: nearest[key]
        for key in [
            "slug",
            "country",
            "type",
            "title",
            "question",
            "unit",
            "resolutionDate",
            "resolutionSource",
            "resolutionSourceUrl",
            "resolutionRule",
            "dataPointId",
            "historicalContext",
        ]
        if key in nearest
    }
    derived_cell.update(
        {
            "pointEstimate": q50,
            "ciLow": q10,
            "ciHigh": q90,
            "confidence": 0.8,
            "drivers": nearest.get("drivers", []),
            "sourceContext": source_context[:8],
            "reasoning": [
                {"kind": "heading", "text": "Median-of-3 rollout ensemble"},
                {
                    "kind": "text",
                    "text": (
                        "Derived run: the pointwise median of the CDFs of "
                        f"{len(cells)} independent thesis.analyst fast "
                        "rollouts on this target — median prediction "
                        "sampling per Turtel et al. 2025 "
                        "(arXiv:2505.17989). No new model call; this run is "
                        "a deterministic aggregate of the recorded "
                        f"rollouts at {', '.join(run_ats)}. Drivers and "
                        "resolver fields mirror the rollout closest to the "
                        "median."
                    ),
                },
                {
                    "kind": "tool",
                    "tool": "ensemble.median",
                    "call": (f"ensemble.median({{rollouts: {json.dumps(run_ats)}}})"),
                    "result": (
                        f"{{rollout_points: {json.dumps(rollout_points)}, "
                        f"rollout_widths: {json.dumps(widths)}, "
                        f"q10: {q10}, q50: {q50}, q90: {q90}}}"
                    ),
                },
                {
                    "kind": "math",
                    "text": (
                        "Median CDF quantiles: q10 = "
                        f"{q10}, q50 = {q50}, q90 = {q90}. Constituent "
                        f"points {json.dumps(rollout_points)} with 80% "
                        f"widths {json.dumps(widths)}; the median interval "
                        "inherits the central rollout mass rather than "
                        "averaging tails."
                    ),
                },
                {
                    "kind": "forecast",
                    "point": q50,
                    "ciLow": q10,
                    "ciHigh": q90,
                },
            ],
        }
    )

    day = run_at[:10]
    stamp = run_at.lower().replace(":", "-").replace("+00-00", "z")
    out_dir = ROOT / "records" / "thesis-analyst" / day / f"{stamp}-median3-{slug}"
    if out_dir.exists() and any(out_dir.iterdir()):
        raise ValueError(f"derived run directory already exists: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    cells_path = out_dir / "cells.with_activity.json"
    distribution_path = out_dir / "distribution.json"

    def artifact_ref(artifact_type: str, path: str) -> dict[str, Any]:
        data = repo_path(path).read_bytes()
        ref = {
            "artifactType": artifact_type,
            "path": path,
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "createdAt": run_at,
        }
        return ref

    distribution_path.write_text(json.dumps(distribution, indent=1) + "\n")
    distribution_ref = artifact_ref(
        "derived_distribution", repo_relative(distribution_path)
    )
    sealed_at = sealed_at or utc_now()
    if sealed_at < run_at:
        raise ValueError("derived seal time predates run start")
    derived_cell["runStartedAt"] = run_at
    derived_cell["runAt"] = sealed_at
    for field in (
        "registrationCommit",
        "targetContentHash",
        "targetRegistrationPath",
        "registeredAtUtc",
    ):
        if target.get(field) not in (None, ""):
            derived_cell[field] = target[field]

    parent_activity = [
        {
            "artifactType": "constituent_manifest",
            "path": reference["manifestPath"],
            "sha256": reference["manifestSha256"],
            "bytes": reference["manifestBytes"],
            "custodyRootSha256": reference["custodyRootSha256"],
            "createdAt": run_at,
        }
        for reference in constituent_runs
    ]

    manifest = {
        "schemaVersion": "thesis_derived_ensemble_manifest_v1",
        "createdAt": run_at,
        "runStartedAt": run_at,
        "custodyInventoryVersion": CUSTODY_INVENTORY_VERSION,
        "runMode": "derived_ensemble",
        "manifestHashSemantics": MANIFEST_HASH_MODE,
        "series": manifest_source.get("series"),
        "period": manifest_source.get("period"),
        "targetContext": target,
        "promptMode": "median3",
        "aggregationAlgorithmVersion": AGGREGATION_ALGORITHM_VERSION,
        "agent": {
            "agent": "thesis.analyst.median3",
            "model": agent_meta.get("model"),
            "agentVersion": f"{agent_meta.get('agentVersion', '?')}+median3",
            "promptHash": agent_meta.get("promptHash"),
            "toolPolicyHash": agent_meta.get("toolPolicyHash"),
            "aggregationAlgorithmVersion": AGGREGATION_ALGORITHM_VERSION,
        },
        "ok": True,
        "cellsPath": None,  # set after writing cells
        "constituentRuns": constituent_runs,
        "constituentManifests": [
            reference["manifestPath"] for reference in constituent_runs
        ],
        "artifacts": [],
    }
    for field in (
        "registrationCommit",
        "targetContentHash",
        "targetRegistrationPath",
        "registeredAtUtc",
    ):
        if target.get(field) not in (None, ""):
            manifest[field] = target[field]

    cell_with_activity = {
        **derived_cell,
        "model": agent_meta.get("model"),
        "aggregationAlgorithmVersion": AGGREGATION_ALGORITHM_VERSION,
        "constituentRuns": constituent_runs,
        "activityLog": [*parent_activity, distribution_ref],
    }
    cells_path.write_text(json.dumps([cell_with_activity], indent=2) + "\n")
    manifest["cellsPath"] = repo_relative(cells_path)
    cells_ref = artifact_ref("cells_with_activity", repo_relative(cells_path))
    local_refs = [distribution_ref, cells_ref]

    manifest_path = out_dir / "manifest.json"
    self_payload = copy.deepcopy(manifest)
    self_payload["artifacts"] = local_refs
    self_bytes = canonical_bytes(self_payload)
    manifest_ref = {
        "artifactType": "manifest",
        "path": repo_relative(manifest_path),
        "sha256": hashlib.sha256(self_bytes).hexdigest(),
        "bytes": len(self_bytes),
        "createdAt": run_at,
        "hashMode": MANIFEST_HASH_MODE,
    }
    manifest["artifacts"] = [*local_refs, manifest_ref]
    custody_entries = []
    for ref in local_refs:
        path = repo_path(ref["path"])
        raw = path.read_bytes()
        entry = {
            "artifactType": ref["artifactType"],
            "path": path.name,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
        if path.suffix == ".json":
            entry["canonicalJsonSha256"] = canonical_sha256(json.loads(raw))
        custody_entries.append(entry)
    custody_root = {
        "schemaVersion": "thesis_custody_root_v1",
        "custodyInventoryVersion": CUSTODY_INVENTORY_VERSION,
        "runMode": "derived_ensemble",
        "hashAlgorithm": "sha256",
        "canonicalJson": (
            "UTF-16 code-unit key order; ECMAScript JSON number/string encoding"
        ),
        "artifacts": custody_entries,
        "constituentCustodyRoots": constituent_runs,
        "manifestWithoutCustodyRoot": {
            "path": "manifest.json",
            "excludedField": "custodyRootSha256",
            "canonicalJsonSha256": canonical_sha256(manifest),
        },
    }
    (out_dir / "custody_root.json").write_text(
        json.dumps(custody_root, indent=2) + "\n"
    )
    manifest["custodyRootSha256"] = canonical_sha256(custody_root)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest, manifest_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", action="append", required=True, type=pathlib.Path)
    parser.add_argument("--out-list")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    groups = collect_rollouts([repo_path(path) for path in args.batch])
    written = []
    for slug, rollouts in sorted(groups.items()):
        try:
            validate_constituent_rollouts(rollouts)
        except ValueError as exc:
            print(f"  fail {slug}: {exc}", file=sys.stderr)
            return 1
        if args.dry_run:
            points = [r["cell"]["pointEstimate"] for r in rollouts]
            print(f"  would derive {slug} from points {points}")
            continue
        manifest, manifest_path = build_derived_run(slug, rollouts, utc_now())
        summary = json.loads((manifest_path.parent / "distribution.json").read_text())[
            "summary"
        ]
        print(
            f"  {slug}: median {summary['pointEstimate']} "
            f"[{summary['interval80']['lower']}, "
            f"{summary['interval80']['upper']}] "
            f"from {len(rollouts)} rollouts -> {repo_relative(manifest_path)}"
        )
        written.append(repo_relative(manifest_path))
    if args.out_list and written:
        pathlib.Path(args.out_list).write_text("\n".join(written) + "\n")
    print(f"{len(written)} derived runs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
