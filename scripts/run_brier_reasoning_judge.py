#!/usr/bin/env python3
"""Run a model-generated judge over forecast reasoning traces.

This is an auxiliary process-eval, not a reward signal. It reviews recent
forecast traces and suggests improvements to Brier prompts, packs, validators,
UI, or scheduling.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
try:
    from private_source_screen import (  # type: ignore
        screen_pre_submit_review,
    )
    from run_thesis_analyst import (  # type: ignore
        append_command_artifacts,
        extract_json_payload,
        repo_relative,
        run_codex_agent_command,
        utc_now,
        write_artifact,
    )
finally:
    if sys.path[0] == str(SCRIPTS):
        sys.path.pop(0)


def default_out_dir(run_at: str) -> pathlib.Path:
    date = run_at[:10]
    stamp = run_at.lower().replace(":", "-").replace("+00-00", "z")
    return ROOT / "records" / "brier-judges" / date / f"{stamp}-reasoning-judge"


def load_batch_runs(
    batch_paths: list[pathlib.Path],
    max_runs: int,
) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for batch_path in batch_paths:
        batch = json.loads((ROOT / batch_path).read_text())
        for result in batch.get("results", []):
            if not result.get("ok"):
                continue
            manifest_path = ROOT / result["manifestPath"]
            manifest = json.loads(manifest_path.read_text())
            cells = json.loads((ROOT / manifest["cellsPath"]).read_text())
            for cell in cells:
                runs.append(
                    {
                        "target": result.get("target", {}),
                        "manifestPath": repo_relative(manifest_path),
                        "runAt": cell.get("runAt"),
                        "slug": cell.get("slug"),
                        "title": cell.get("title"),
                        "question": cell.get("question"),
                        "unit": cell.get("unit"),
                        "pointEstimate": cell.get("pointEstimate"),
                        "ciLow": cell.get("ciLow"),
                        "ciHigh": cell.get("ciHigh"),
                        "resolutionDate": cell.get("resolutionDate"),
                        "resolutionRule": cell.get("resolutionRule"),
                        "sourceContext": cell.get("sourceContext", []),
                        "drivers": cell.get("drivers", []),
                        "reasoning": compact_reasoning(cell.get("reasoning", [])),
                        # Runner-authored only, and screened: a
                        # cell-supplied review never reaches the judge
                        # prompt, and reviewer wording that matches the
                        # private-source screen is withheld here exactly
                        # as in every other projection.
                        "preSubmitReview": compact_review(
                            _screened_manifest_review(manifest)
                        ),
                    }
                )
    return runs[-max_runs:]


def compact_reasoning(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    for step in steps:
        if not isinstance(step, dict):
            continue
        kind = step.get("kind")
        row: dict[str, Any] = {"kind": kind}
        if kind == "tool":
            row["tool"] = step.get("tool")
            row["call"] = truncate(str(step.get("call") or ""), 500)
            row["result"] = truncate(str(step.get("result") or ""), 700)
        elif kind == "forecast":
            row["point"] = step.get("point")
            row["ciLow"] = step.get("ciLow")
            row["ciHigh"] = step.get("ciHigh")
        else:
            row["text"] = truncate(str(step.get("text") or ""), 800)
        compact.append(row)
    return compact


def _screened_manifest_review(
    manifest: dict[str, Any],
) -> dict[str, Any] | None:
    review = manifest.get("preSubmitReview")
    if review is None:
        return None
    if not isinstance(review, dict):
        raise ValueError("manifest preSubmitReview is invalid")
    # The judge prompt retains specific fields; enforce their types so a
    # malformed manifest cannot smuggle content through an unexpected
    # shape (e.g. a dict where a summary string belongs).
    if "summary" in review and not isinstance(review["summary"], str):
        raise ValueError("manifest preSubmitReview.summary must be a string")
    if "status" in review and not isinstance(review["status"], str):
        raise ValueError("manifest preSubmitReview.status must be a string")
    for field in ("findings", "dispositions"):
        if field in review and not isinstance(review[field], list):
            raise ValueError(
                f"manifest preSubmitReview.{field} must be a list"
            )
    return screen_pre_submit_review(review)


def compact_review(review: dict[str, Any] | None) -> dict[str, Any] | None:
    if not review:
        return None
    return {
        "status": review.get("status"),
        "summary": review.get("summary"),
        "findings": [
            {
                "severity": finding.get("severity"),
                "rubricItem": finding.get("rubricItem"),
                "summary": finding.get("summary"),
                "actionRequested": finding.get("actionRequested"),
            }
            for finding in review.get("findings", [])
        ],
    }


def truncate(value: str, limit: int) -> str:
    return value if len(value) <= limit else value[: limit - 3] + "..."


def build_prompt(runs: list[dict[str, Any]]) -> str:
    schema = {
        "schemaVersion": "brier_reasoning_judge_v1",
        "summary": "one paragraph",
        "reviewedRunCount": len(runs),
        "strengths": ["specific observed strengths"],
        "systemIssues": [
            {
                "issueId": "short_snake_case",
                "severity": "low|medium|high",
                "area": "prompt|pack|validator|ui|scheduler|scoring|data_adapter",
                "summary": "specific weakness",
                "evidenceRunSlugs": ["slug"],
            }
        ],
        "recommendations": [
            {
                "priority": "now|next|later",
                "area": "prompt|pack|validator|ui|scheduler|scoring|data_adapter",
                "summary": "change to Brier",
                "rationale": (
                    "why this should improve forecast accuracy or auditability"
                ),
                "proposedChange": "concrete implementation",
                "expectedImpact": "short expected effect",
                "risk": "failure mode or tradeoff",
                "evidenceRunSlugs": ["slug"],
            }
        ],
        "promptPatchCandidates": [
            {
                "file": "path or prompt surface",
                "patchSummary": "specific text or behavior to add",
            }
        ],
    }
    return (
        "# Brier reasoning judge\n\n"
        "You are an LLM judge reviewing public forecast reasoning traces to "
        "suggest improvements to Brier. This is an auxiliary process review, "
        "not a reward signal and not an outcome score. Do not reward forecasts "
        "for matching unknown future outcomes. Do not rewrite the forecasts. "
        "Review the traces for process weaknesses that could be fixed in the "
        "Brier system prompt, validators, packs, source adapters, scheduling, "
        "or UI.\n\n"
        "Prefer concrete system changes over generic advice. If a target type "
        "looks mismatched to the fast public-release prompt, say so. If prior "
        "traces are useful but not structured enough, suggest a concrete "
        "strategy-track/update representation. If reviewer findings repeat, "
        "suggest a validator or prompt change.\n\n"
        "# Required JSON shape\n"
        f"{json.dumps(schema, indent=2)}\n\n"
        "# Forecast runs to review\n"
        f"{json.dumps(runs, indent=2)}\n\n"
        "Return exactly one JSON object and no Markdown."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-manifest", action="append", required=True)
    parser.add_argument("--model", default="gpt-5.5")
    parser.add_argument("--timeout-seconds", type=int, default=700)
    parser.add_argument("--max-runs", type=int, default=12)
    parser.add_argument("--out-dir")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_at = utc_now()
    out_dir = pathlib.Path(args.out_dir) if args.out_dir else default_out_dir(run_at)
    refs: list[dict[str, Any]] = []
    batch_paths = [pathlib.Path(path) for path in args.batch_manifest]
    runs = load_batch_runs(batch_paths, args.max_runs)
    prompt = build_prompt(runs)
    refs.append(write_artifact(out_dir, "prompt", "prompt.md", prompt, run_at))
    command_result = run_codex_agent_command(
        prompt=prompt,
        timeout_seconds=args.timeout_seconds,
        model=args.model,
        out_dir=out_dir,
        prefix="",
        search=False,
        sandbox="read-only",
        reasoning_effort="low",
    )
    append_command_artifacts(
        refs,
        out_dir,
        prefix="",
        command_result=command_result,
        created_at=run_at,
        stdout_artifact_type="raw_response",
    )
    raw_response = command_result["stdout"]
    ok = command_result["returnCode"] == 0
    parsed: dict[str, Any] | None = None
    parse_error: str | None = None
    if ok:
        try:
            parsed = extract_json_payload(raw_response)[0]
            refs.append(
                write_artifact(
                    out_dir,
                    "parsed_cell",
                    "judge.json",
                    json.dumps(parsed, indent=2),
                    run_at,
                )
            )
        except Exception as exc:  # noqa: BLE001
            ok = False
            parse_error = str(exc)
    manifest = {
        "schemaVersion": "brier_reasoning_judge_run_manifest_v1",
        "createdAt": run_at,
        "ok": ok,
        "judge": {
            "agent": "brier.reasoning_judge",
            "model": args.model,
            "promptVersion": "brier-reasoning-judge-v0.1",
            "rewardEligible": False,
        },
        "inputBatchManifests": [str(path) for path in batch_paths],
        "reviewedRunCount": len(runs),
        "judgePath": repo_relative(out_dir / "judge.json") if parsed else None,
        "parseError": parse_error,
        "artifacts": refs,
    }
    manifest_ref = write_artifact(
        out_dir,
        "manifest",
        "manifest.json",
        json.dumps(manifest, indent=2),
        run_at,
    )
    manifest["artifacts"].append(manifest_ref)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
