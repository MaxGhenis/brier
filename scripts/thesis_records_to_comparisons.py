#!/usr/bin/env python3
"""Generate ForecastComparisonRun augments from thesis.analyst record manifests.

Usage:
  python3 scripts/thesis_records_to_comparisons.py \
      site/src/data/thesis-analyst-live-comparisons.ts \
      RECORDED_THESIS_ANALYST_COMPARISON_RUN_AUGMENTS \
      records/thesis-analyst/2026-06-16/.../manifest.json \
      --batch-manifest records/thesis-analyst/batches/....json
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]

CANONICAL_TARGETS: dict[str, dict[str, Any]] = {
    "boe-bank-rate-2026-06-18": {
        "targetSlug": "boe-bank-rate-june-2026",
        "valueScale": 1,
    },
    "statcan-ei-regular-beneficiaries-2026-04": {
        "targetSlug": "canada-ei-regular-beneficiaries-april-2026",
        # The live agent forecasted persons; the catalog target is thousands.
        "valueScale": 0.001,
    },
    "canada-cpi-all-items-yoy-2026-05": {
        "targetSlug": "canada-cpi-yoy-may-2026",
        "valueScale": 1,
    },
    "jp-core-cpi-exfreshfood-yoy-2026-05": {
        "targetSlug": "japan-core-cpi-yoy-may-2026",
        "valueScale": 1,
    },
    "us-dol-initial-claims-sa-week-2026-06-13-first-print": {
        "targetSlug": "initial-claims-week-2026-06-13",
        # The live agent forecasted persons; the catalog target is thousands.
        "valueScale": 0.001,
    },
    "bls-jolts-job-openings-2026-05": {
        "targetSlug": "jolts-openings-may-2026",
        # The live agent forecasted thousands; the catalog target is millions.
        "valueScale": 0.001,
    },
}

CATALOG_TARGET_UNITS: dict[str, str] = {
    "canada-ei-regular-beneficiaries-april-2026": "thousands",
    "initial-claims-week-2026-06-13": "thousands",
    "initial-claims-week-2026-06-20": "thousands",
    "jolts-openings-may-2026": "millions",
}


def repo_path(path: str | pathlib.Path) -> pathlib.Path:
    candidate = pathlib.Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def repo_path_key(path: str | pathlib.Path) -> str:
    return str(repo_path(path).resolve())


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def scaled(value: int | float, scale: int | float) -> int | float:
    output = float(value) * float(scale)
    if output.is_integer():
        return int(output)
    return round(output, 6)


def effective_scale(
    cell: dict[str, Any],
    scale: int | float,
    target_unit: str | None,
) -> int | float:
    if target_unit and cell.get("unit") == target_unit:
        return 1
    return scale


def scale_reasoning(steps: list[dict[str, Any]], scale: int | float) -> list[dict]:
    if scale == 1:
        return steps
    output = []
    for step in steps:
        if step.get("kind") != "forecast":
            output.append(step)
            continue
        output.append(
            {
                **step,
                "point": scaled(step["point"], scale),
                "ciLow": scaled(step["ciLow"], scale),
                "ciHigh": scaled(step["ciHigh"], scale),
            }
        )
    return output


def infer_runtime_model(manifest: dict[str, Any]) -> str | None:
    for artifact in manifest.get("artifacts", []):
        if artifact.get("artifactType") != "command":
            continue
        command_path = repo_path(artifact["path"])
        if not command_path.exists():
            continue
        command = json.loads(command_path.read_text())
        argv = command.get("argv") or []
        for index, arg in enumerate(argv):
            if arg in {"-m", "--model"} and index + 1 < len(argv):
                return argv[index + 1]
            if isinstance(arg, str) and arg.startswith("--model="):
                return arg.split("=", 1)[1]
    return None


def comparison_run(
    cell: dict[str, Any],
    manifest: dict[str, Any],
    target_slug: str,
    scale: int | float,
    target_unit: str | None = None,
) -> dict[str, Any]:
    agent = manifest["agent"]
    prompt_mode = manifest.get("promptMode", "full")
    run_at = cell["runAt"]
    label = f"Thesis analyst {prompt_mode} run"
    scale = effective_scale(cell, scale, target_unit)
    value_note = (
        " Values converted to the catalog target unit."
        if scale != 1
        else ""
    )
    return {
        "variantId": (
            f"{target_slug}-thesis-analyst-{slugify(prompt_mode)}-"
            f"{slugify(run_at)}"
        ),
        "label": label,
        "description": (
            "Validated live Codex-backed thesis.analyst run with prompt, "
            "command, stdout/stderr, parsed cell, normalized cell, validation, "
            f"and manifest artifacts captured. Prompt mode: {prompt_mode}."
            f"{value_note}"
        ),
        "pointEstimate": scaled(cell["pointEstimate"], scale),
        "ciLow": scaled(cell["ciLow"], scale),
        "ciHigh": scaled(cell["ciHigh"], scale),
        "confidence": cell["confidence"],
        "drivers": cell["drivers"],
        "predictionRun": {
            "kind": "recorded-agent-run",
            "runAt": run_at,
            "agent": agent["agent"],
            "model": infer_runtime_model(manifest) or agent["model"],
            "agentVersion": agent.get("agentVersion"),
            "promptHash": agent.get("promptHash"),
            "toolPolicyHash": agent.get("toolPolicyHash"),
            "promptMode": prompt_mode,
            "runLabel": label,
            "runDescription": (
                "Live thesis.analyst run promoted from the recorded manifest."
            ),
            "sourceContext": cell["sourceContext"],
            "activityLog": manifest.get("artifacts", cell.get("activityLog", [])),
        },
        "reasoning": scale_reasoning(cell["reasoning"], scale),
    }


def load_runs(
    manifest_paths: list[pathlib.Path],
    include_unmapped: bool,
    batch_targets: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    augments: dict[str, list[dict[str, Any]]] = {}
    for manifest_path in manifest_paths:
        manifest = json.loads(manifest_path.read_text())
        if not manifest.get("ok"):
            continue
        batch_mapping = batch_targets.get(repo_path_key(manifest_path))
        cells_path = repo_path(manifest["cellsPath"])
        for cell in json.loads(cells_path.read_text()):
            mapping = CANONICAL_TARGETS.get(cell["slug"])
            if not mapping and batch_mapping:
                mapping = batch_mapping
            if mapping:
                target_slug = mapping["targetSlug"]
                scale = mapping.get("valueScale", 1)
                target_unit = mapping.get("targetUnit") or CATALOG_TARGET_UNITS.get(
                    target_slug
                )
            elif include_unmapped:
                target_slug = cell["slug"]
                scale = 1
                target_unit = None
            else:
                continue
            augments.setdefault(target_slug, []).append(
                comparison_run(cell, manifest, target_slug, scale, target_unit)
            )
    for runs in augments.values():
        runs.sort(key=lambda run: run["predictionRun"]["runAt"])
    return dict(sorted(augments.items()))


def load_batch_targets(
    batch_manifest_paths: list[pathlib.Path],
) -> dict[str, dict[str, Any]]:
    targets: dict[str, dict[str, Any]] = {}
    for batch_manifest_path in batch_manifest_paths:
        batch = json.loads(batch_manifest_path.read_text())
        for result in batch.get("results", []):
            manifest_path = result.get("manifestPath")
            target = result.get("target") or {}
            catalog_slug = target.get("catalogSlug")
            if not manifest_path or not catalog_slug:
                continue
            targets[repo_path_key(manifest_path)] = {
                "targetSlug": catalog_slug,
                "valueScale": target.get("valueScale", 1),
                "targetUnit": target.get("targetUnit")
                or CATALOG_TARGET_UNITS.get(catalog_slug),
            }
    return targets


def write_ts(out_path: pathlib.Path, const_name: str, augments: dict) -> None:
    body = json.dumps(augments, indent=2, ensure_ascii=True)
    out_path.write_text(
        "// Generated by scripts/thesis_records_to_comparisons.py from\n"
        "// recorded thesis.analyst manifests. Regenerate; do not hand-edit.\n"
        'import type { ForecastComparisonRun } from "./forecast-cells";\n\n'
        f"export const {const_name}: Record<string, ForecastComparisonRun[]> = "
        f"{body};\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("out_ts")
    parser.add_argument("const_name")
    parser.add_argument("manifests", nargs="+", type=pathlib.Path)
    parser.add_argument("--batch-manifest", action="append", type=pathlib.Path)
    parser.add_argument("--include-unmapped", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_paths = [repo_path(path) for path in args.manifests]
    batch_targets = load_batch_targets(
        [repo_path(path) for path in args.batch_manifest or []]
    )
    augments = load_runs(manifest_paths, args.include_unmapped, batch_targets)
    write_ts(repo_path(args.out_ts), args.const_name, augments)
    print(f"wrote {sum(len(runs) for runs in augments.values())} runs -> {args.out_ts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
