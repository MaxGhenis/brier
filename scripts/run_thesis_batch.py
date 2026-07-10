#!/usr/bin/env python3
"""Run a finite queue of thesis.analyst forecasts.

This is intentionally a loop, not a daemon. It records every child run under
`records/thesis-analyst/` through `run_thesis_analyst.py`, then writes a batch
manifest summarizing successes, validation failures, and record paths.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_thesis_analyst.py"
DEFAULT_CODEX_MODEL = "gpt-5.5"

DEFAULT_TARGETS: list[dict[str, Any]] = [
    {
        "series": "statcan.employment_insurance.regular_beneficiaries",
        "period": "2026-04",
        "catalogSlug": "canada-ei-regular-beneficiaries-april-2026",
        "valueScale": 0.001,
        "targetUnit": "thousands",
    },
    {
        "series": "abs.cpi.all_groups.yoy",
        "period": "2026-05",
        "catalogSlug": "australia-cpi-annual-rate-may-2026",
    },
    {
        "series": "abs.labour.unemployment_rate",
        "period": "2026-05",
        "catalogSlug": "australia-unemployment-rate-may-2026",
    },
    {
        "series": "abs.labour.employment_change",
        "period": "2026-05",
        "catalogSlug": "australia-employment-change-may-2026",
    },
    {
        "series": "statcan.gdp_by_industry.monthly_growth",
        "period": "2026-04",
        "catalogSlug": "canada-monthly-gdp-growth-april-2026",
    },
    {
        "series": "statjp.cpi.tokyo_all_items_yoy",
        "period": "2026-06",
        "catalogSlug": "japan-tokyo-cpi-annual-rate-june-2026-prelim",
    },
    {
        "series": "statjp.lfs.unemployment_rate",
        "period": "2026-05",
        "catalogSlug": "japan-unemployment-rate-may-2026",
    },
    {
        "series": "eurostat.hicp.flash.yoy",
        "period": "2026-06",
        "catalogSlug": "euro-flash-hicp-june-2026",
    },
    {
        "series": "eurostat.unemployment_rate",
        "period": "2026-05",
        "catalogSlug": "euro-area-unemployment-rate-may-2026",
    },
    {
        "series": "eurostat.retail_trade.volume_mom",
        "period": "2026-05",
        "catalogSlug": "euro-area-retail-trade-volume-growth-may-2026",
    },
    {
        "series": "bea.core_pce.mom",
        "period": "2026-05",
        "catalogSlug": "us-core-pce-mom-may-2026",
    },
    {
        "series": "bls.jolts.job_openings",
        "period": "2026-05",
        "catalogSlug": "jolts-openings-may-2026",
        "valueScale": 0.001,
        "targetUnit": "millions",
    },
    {
        "series": "bls.ces.nonfarm_payrolls.change",
        "period": "2026-06",
        "catalogSlug": "nonfarm-payrolls-june-2026",
    },
    {
        "series": "bls.cps.unemployment_rate",
        "period": "2026-06",
        "catalogSlug": "unemployment-rate-june-2026",
    },
    {
        "series": "treasury.mts.monthly_deficit",
        "period": "2026-06",
        "catalogSlug": "us-mts-deficit-june-2026",
    },
    {
        "series": "bls.cpi.u.headline_mom",
        "period": "2026-06",
        "catalogSlug": "us-cpi-u-mom-june-2026",
    },
    {
        "series": "bls.cpi.u.core_mom",
        "period": "2026-06",
        "catalogSlug": "us-core-cpi-mom-june-2026",
    },
    {
        "series": "us.dol.initial_claims.sa",
        "period": "week_2026-06-20",
        "catalogSlug": "initial-claims-week-2026-06-20",
        "valueScale": 0.001,
        "targetUnit": "thousands",
    },
    {
        "series": "bea.government_social_benefits.level",
        "period": "2026-05",
        "catalogSlug": "us-government-social-benefits-may-2026",
    },
    {
        "series": "bea.government_social_benefits.social_security",
        "period": "2026-05",
        "catalogSlug": "us-social-security-benefits-may-2026",
    },
    {
        "series": "bea.government_social_benefits.medicare",
        "period": "2026-05",
        "catalogSlug": "us-medicare-benefits-may-2026",
    },
    {
        "series": "bea.government_social_benefits.medicaid",
        "period": "2026-05",
        "catalogSlug": "us-medicaid-benefits-may-2026",
    },
    {
        "series": "bea.wages_and_salaries.level",
        "period": "2026-05",
        "catalogSlug": "us-wages-and-salaries-may-2026",
    },
]


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def slug_time(value: str) -> str:
    return value.lower().replace(":", "-").replace("+00-00", "z")


def parse_target(value: str) -> dict[str, str]:
    parts = value.split(":", 2)
    if len(parts) not in {2, 3}:
        raise argparse.ArgumentTypeError(
            "targets must be SERIES:PERIOD or SERIES:PERIOD:CATALOG_SLUG"
        )
    target = {"series": parts[0], "period": parts[1]}
    if len(parts) == 3:
        target["catalogSlug"] = parts[2]
    return target


def load_targets(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.targets_file:
        data = json.loads(pathlib.Path(args.targets_file).read_text())
        targets = data["targets"] if isinstance(data, dict) else data
    elif args.target:
        targets = args.target
    else:
        targets = DEFAULT_TARGETS
    if args.skip:
        targets = targets[args.skip :]
    if args.max_targets is not None:
        targets = targets[: args.max_targets]
    return targets


def run_one(
    target: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    command = args.command or os.environ.get("THESIS_AGENT_COMMAND")
    codex_model = (
        args.codex_model
        or os.environ.get("THESIS_CODEX_MODEL")
        or DEFAULT_CODEX_MODEL
    )
    argv = [
        sys.executable,
        str(RUNNER),
        "--series",
        target["series"],
        "--period",
        target["period"],
        "--prompt-mode",
        args.prompt_mode,
        "--timeout-seconds",
        str(args.timeout_seconds),
        "--allow-existing-slug",
        "--target-context-json",
        json.dumps(target, sort_keys=True),
    ]
    if target.get("conditional"):
        argv.extend(["--conditional", target["conditional"]])
    if command:
        argv.extend(["--command", command])
    else:
        argv.extend(["--codex-model", codex_model])
        if args.no_codex_search:
            argv.append("--no-codex-search")
        if args.codex_reasoning_effort:
            argv.extend(["--codex-reasoning-effort", args.codex_reasoning_effort])
    if args.no_pre_submit_review:
        pass
    elif args.pre_submit_review_codex_model:
        argv.extend(
            [
                "--pre-submit-review-codex-model",
                args.pre_submit_review_codex_model,
            ]
        )
        if args.pre_submit_review_codex_search:
            argv.append("--pre-submit-review-codex-search")
    started_at = utc_now()
    completed = subprocess.run(
        argv,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    finished_at = utc_now()
    manifest = None
    try:
        manifest = json.loads(completed.stdout)
    except json.JSONDecodeError:
        manifest = None
    validation_errors = []
    if manifest and manifest.get("validation"):
        for cell in manifest["validation"].get("cells", []):
            validation_errors.extend(cell.get("errors", []))
    return {
        "target": target,
        "startedAt": started_at,
        "finishedAt": finished_at,
        "returnCode": completed.returncode,
        "ok": completed.returncode == 0 and bool(manifest and manifest.get("ok")),
        "manifestPath": manifest_path(manifest) if manifest else None,
        "cellsPath": manifest.get("cellsPath") if manifest else None,
        "stdoutTail": completed.stdout[-2000:],
        "stderrTail": completed.stderr[-2000:],
        "validationErrors": validation_errors,
    }


def manifest_path(manifest: dict[str, Any]) -> str | None:
    for artifact in manifest.get("artifacts", []):
        if artifact.get("artifactType") == "manifest":
            return artifact.get("path")
    return None


def write_batch_manifest(
    out_path: pathlib.Path,
    started_at: str,
    finished_at: str,
    args: argparse.Namespace,
    results: list[dict[str, Any]],
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schemaVersion": "thesis_batch_manifest_v1",
        "startedAt": started_at,
        "finishedAt": finished_at,
        "promptMode": args.prompt_mode,
        "timeoutSeconds": args.timeout_seconds,
        "targets": len(results),
        "ok": sum(1 for result in results if result["ok"]),
        "failed": sum(1 for result in results if not result["ok"]),
        "results": results,
    }
    out_path.write_text(json.dumps(manifest, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", action="append", type=parse_target)
    parser.add_argument("--targets-file")
    parser.add_argument("--max-targets", type=int)
    parser.add_argument("--skip", type=int, default=0)
    parser.add_argument(
        "--prompt-mode", choices=["full", "fast", "ladder", "ladder_v2"], default="fast"
    )
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--max-failures", type=int, default=999)
    parser.add_argument("--command")
    parser.add_argument("--codex-model")
    parser.add_argument("--codex-reasoning-effort", default="low")
    parser.add_argument("--no-codex-search", action="store_true")
    # Review is on by default: the reviewer rubric (interval-from-realized-
    # volatility, resolver exactness, variant pinning) is exactly the failure
    # profile of unreviewed fast-mode runs. --no-pre-submit-review to opt out.
    parser.add_argument("--pre-submit-review-codex-model", default="gpt-5.5")
    parser.add_argument("--no-pre-submit-review", action="store_true")
    parser.add_argument("--pre-submit-review-codex-search", action="store_true")
    parser.add_argument("--out")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    targets = load_targets(args)
    started_at = utc_now()
    out = (
        pathlib.Path(args.out)
        if args.out
        else ROOT
        / "records"
        / "thesis-analyst"
        / "batches"
        / f"{slug_time(started_at)}.json"
    )
    results = []
    failures = 0
    for index, target in enumerate(targets, start=1):
        print(
            f"[{index}/{len(targets)}] {target['series']} {target['period']}",
            flush=True,
        )
        result = run_one(target, args)
        results.append(result)
        print(
            json.dumps(
                {
                    "ok": result["ok"],
                    "manifestPath": result["manifestPath"],
                    "validationErrors": result["validationErrors"],
                }
            ),
            flush=True,
        )
        write_batch_manifest(out, started_at, utc_now(), args, results)
        if not result["ok"]:
            failures += 1
            if failures >= args.max_failures:
                break
    write_batch_manifest(out, started_at, utc_now(), args, results)
    print(f"batch manifest: {out}")
    return 0 if all(result["ok"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
