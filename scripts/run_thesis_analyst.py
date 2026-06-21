#!/usr/bin/env python3
"""Run the versioned thesis.analyst agent and persist full run activity.

The runner is intentionally thin:

1. Build the prompt from agents/thesis-analyst/build_prompt.py, or use the
   inline fast prompt for high-volume release-series runs.
2. Execute a headless agent command, or read a saved response / mock cell.
3. Extract JSON, normalize the cell shape, and validate the spawned-cell
   contract.
4. Write every activity artifact: prompt, command, stdout, stderr, raw
   response, parsed cells, normalized cells, validation report, and manifest.

Usage:
  python3 scripts/run_thesis_analyst.py \
      --series ons.labour.unemployment_rate --period 2026-Q4 \
      --prompt-mode fast \
      --command "codex --search exec --ignore-user-config -m gpt-5.5 \
      -c 'service_tier=\"fast\"' \
      --sandbox read-only -C {repo_root} -"

  python3 scripts/run_thesis_analyst.py \
      --series ons.labour.unemployment_rate --period 2026-Q4 \
      --response-file /tmp/codex-output.txt

  python3 scripts/run_thesis_analyst.py \
      --series test.series --period 2030-01 --mock-cell
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import shlex
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
AGENT_ROOT = ROOT / "agents" / "thesis-analyst"
SCRIPTS = ROOT / "scripts"
DEFAULT_RECORD_ROOT = ROOT / "records" / "thesis-analyst"


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "run"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def repo_relative(path: pathlib.Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def write_artifact(
    out_dir: pathlib.Path,
    artifact_type: str,
    filename: str,
    content: str | bytes,
    created_at: str,
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    data = content.encode() if isinstance(content, str) else content
    path.write_bytes(data)
    return {
        "artifactType": artifact_type,
        "path": repo_relative(path),
        "sha256": sha256_bytes(data),
        "bytes": len(data),
        "createdAt": created_at,
    }


def load_prompt_builder():
    sys.path.insert(0, str(AGENT_ROOT))
    try:
        import build_prompt  # type: ignore

        return build_prompt
    finally:
        if sys.path[0] == str(AGENT_ROOT):
            sys.path.pop(0)


def build_prompt(series: str, period: str, conditional: str | None) -> tuple[str, dict]:
    builder = load_prompt_builder()
    return builder.build(series, period, conditional), builder.agent_meta()


def build_run_prompt(
    series: str,
    period: str,
    conditional: str | None,
    mode: str,
) -> tuple[str, dict]:
    prompt, meta = build_prompt(series, period, conditional)
    if mode == "full":
        return prompt, meta
    if mode == "fast":
        return build_fast_prompt(series, period, conditional, meta), meta
    raise ValueError(f"Unsupported prompt mode {mode!r}")


def build_fast_prompt(
    series: str,
    period: str,
    conditional: str | None,
    meta: dict[str, Any],
) -> str:
    """Compact prompt for scheduled public-release batches.

    The full prompt is better for one-off reasoning audits. This one is for
    scale: it inlines the contract and explicitly keeps the child agent away
    from local repo inspection.
    """

    schema = {
        "slug": "kebab-case-unique-vs-catalog",
        "country": "US|UK|CA|AU|EA|JP",
        "type": "data",
        "title": "Short display title",
        "question": "Exact agency series, period, adjustment, first print",
        "unit": (
            "percent|count|thousands|millions|usd|usd_billions|"
            "gbp_billions|ratio|percent_growth"
        ),
        "pointEstimate": 0,
        "ciLow": 0,
        "ciHigh": 0,
        "confidence": 0.8,
        "resolutionDate": "YYYY-MM-DD",
        "resolutionSource": "Official agency release",
        "resolutionSourceUrl": "https://official-source.example",
        "resolutionRule": "First-print rule with rounding and revision policy",
        "dataPointId": "agency.dataset.concept.period.first_print",
        "historicalContext": [{"label": "latest", "value": 0}],
        "drivers": ["short driver phrases"],
        "sourceContext": ["https://urls-actually-used"],
        "runAt": "date -u +%Y-%m-%dT%H:%M:%SZ",
        "reasoning": [
            {"kind": "heading", "text": "Forecast title"},
            {"kind": "text", "text": "Framing and exact resolver"},
            {
                "kind": "tool",
                "tool": "official.lookup",
                "call": "source lookup description",
                "result": "fetched numbers",
            },
            {"kind": "math", "text": "point and 80% interval calculation"},
            {"kind": "forecast", "point": 0, "ciLow": 0, "ciHigh": 0},
        ],
    }
    domain_notes = "\n".join(f"- {line}" for line in fast_domain_notes(series))
    conditional_line = (
        f"- conditional_on: {conditional}\n"
        if conditional
        else "- conditional_on: null\n"
    )
    return (
        "# Thesis analyst fast public-release run\n\n"
        "Return exactly one JSON object and no Markdown. Do not wrap it in a "
        "code fence.\n\n"
        "Hard scope: Do not inspect the local repository or workspace. Do not "
        "run ls, cat, sed, rg, find, git, or open local files. The schema is "
        "fully specified below. You may use web search, official public URLs, "
        "`date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands "
        "only.\n\n"
        "Goal: produce one auditable forecast for an automatically resolvable "
        "government/public statistical release. Resolve on the first official "
        "print unless the series itself is a policy decision level after an "
        "announcement.\n\n"
        "# Question spec\n"
        f"- series: {series}\n"
        f"- period: {period}\n"
        f"{conditional_line}\n"
        "# Source hints\n"
        f"{domain_notes}\n\n"
        "# Default promoted forecasting practices\n"
        "- Resolve the exact first-print target before inside-view evidence.\n"
        "- Fetch and state the recent official-source reference class.\n"
        "- Anchor on the outside-view base rate before current-release "
        "adjustments.\n"
        "- Separate level, momentum, one-off, and policy-mechanism effects "
        "before combining them.\n"
        "- Size the 80% interval from realized first-print dispersion, then "
        "widen or skew only for stated reasons.\n"
        "- Name concrete upside, downside, and outside-the-interval scenarios.\n\n"
        "# Required JSON shape\n"
        f"{json.dumps(schema, indent=2)}\n\n"
        "# Validation rules\n"
        "- Use confidence 0.8 exactly.\n"
        "- ciLow < pointEstimate < ciHigh, except discrete policy-rate "
        "targets may put the modal point at an interval edge if needed.\n"
        "- historicalContext must contain at least 3 numeric fetched points.\n"
        "- sourceContext must contain at least 2 source URLs actually used.\n"
        "- reasoning must contain at least 7 steps, at least 3 tool steps "
        "whose result strings include fetched numbers, one explicit base-rate "
        "or reference-class step, one math step, one counter-consideration, "
        "and a final forecast step whose numbers exactly match the cell.\n"
        "- Every tool step result must include at least one fetched numeric "
        "value. Put qualitative source notes in text steps instead.\n"
        "- resolutionDate must be verified from an official release calendar "
        "or announcement schedule this run. Do not infer it from cadence.\n"
        "- runAt must be the actual UTC date command output from this run.\n"
        "- Slug should be stable and descriptive; if the same target already "
        "exists, reuse the obvious canonical slug rather than inventing a "
        "near-duplicate.\n\n"
        "Emit the final JSON object only. "
        f"(agent {meta['agent']} v{meta['agentVersion']}, "
        f"prompt {meta['promptHash'][:12]}, "
        f"tools {meta['toolPolicyHash'][:12]}, promptMode fast)\n"
    )


def fast_domain_notes(series: str) -> list[str]:
    if series.startswith("boe."):
        return [
            "Use Bank of England MPC pages and monetary-policy summaries.",
            "Target is usually Bank Rate after the named MPC announcement.",
            "Resolution source should be the Bank of England announcement page.",
        ]
    if series.startswith("ons."):
        return [
            "Use ONS time-series pages, ONS API, and ONS release calendar.",
            "UK CPI/CPIH prints to one decimal; labour-market rates print to "
            "one decimal.",
            "Resolution source should be the relevant ONS release or time-series page.",
        ]
    if series.startswith("statcan."):
        return [
            "Use Statistics Canada The Daily and release schedule.",
            "Canada CPI annual rates print to one decimal.",
            "Resolution source should be the Statistics Canada release/table.",
        ]
    if series.startswith("estat."):
        return [
            "Use Statistics Bureau of Japan/e-Stat CPI pages and release schedule.",
            "Japan CPI annual rates print to one decimal.",
            "Resolution source should be the official CPI release/table.",
        ]
    if series.startswith("eurostat."):
        return [
            "Use Eurostat euro-indicators release calendar and official HICP/IP pages.",
            "Euro-area HICP rates print to one decimal.",
            "Resolution source should be the Eurostat release/data page.",
        ]
    if series.startswith("abs."):
        return [
            "Use ABS release calendar and official monthly CPI indicator pages.",
            "Australia CPI indicator rates print to one decimal.",
            "Resolution source should be the ABS release page.",
        ]
    if series.startswith(("bls.", "bea.", "census.", "dol.", "fed.", "us.")):
        return [
            "Use the official agency release calendar, not inferred cadence.",
            "FRED may be used as a history mirror, but resolution cites the agency.",
            "For FOMC targets, resolve to the target range upper bound after "
            "the announcement.",
            "For DOL claims, name the week-ending date and cite the release date.",
        ]
    return [
        "Use the official agency data page and release calendar.",
        "FRED or sanctioned mirrors may be used only for history, not final "
        "resolution.",
        "Match the agency's published rounding precision.",
    ]


def default_out_dir(series: str, period: str, run_at: str) -> pathlib.Path:
    date = run_at[:10]
    stamp = slugify(run_at.replace(":", "-"))
    return DEFAULT_RECORD_ROOT / date / f"{stamp}-{slugify(series)}-{slugify(period)}"


def run_agent_command(
    command: str,
    prompt: str,
    prompt_path: pathlib.Path,
    timeout_seconds: int,
) -> dict:
    rendered = command.format(prompt_path=str(prompt_path), repo_root=str(ROOT))
    argv = shlex.split(rendered)
    if not argv:
        raise SystemExit("--command resolved to an empty command")
    started_at = utc_now()
    try:
        completed = subprocess.run(
            argv,
            input=prompt,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
        finished_at = utc_now()
        return {
            "argv": argv,
            "startedAt": started_at,
            "finishedAt": finished_at,
            "returnCode": completed.returncode,
            "timedOut": False,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except subprocess.TimeoutExpired as exc:
        finished_at = utc_now()
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        stderr = (
            f"{stderr}\nagent command timed out after "
            f"{timeout_seconds} seconds\n"
        ).lstrip()
        return {
            "argv": argv,
            "startedAt": started_at,
            "finishedAt": finished_at,
            "returnCode": 124,
            "timedOut": True,
            "stdout": stdout,
            "stderr": stderr,
        }


def infer_command_model(command_result: dict[str, Any] | None) -> str | None:
    if not command_result:
        return None

    argv = command_result.get("argv") or []
    for index, arg in enumerate(argv):
        if arg in {"-m", "--model"} and index + 1 < len(argv):
            return str(argv[index + 1])
        if isinstance(arg, str) and arg.startswith("--model="):
            return arg.split("=", 1)[1]

    stderr = str(command_result.get("stderr") or "")
    match = re.search(r"(?im)^model:\s*(\S+)\s*$", stderr)
    return match.group(1) if match else None


def stamp_runtime_invocation(
    meta: dict[str, Any],
    command_result: dict[str, Any] | None,
) -> dict[str, Any]:
    runtime_meta = dict(meta)
    runtime_model = infer_command_model(command_result)
    if runtime_model and runtime_model != runtime_meta.get("model"):
        runtime_meta["configuredModel"] = runtime_meta.get("model")
        runtime_meta["model"] = runtime_model
    return runtime_meta


def write_failure_manifest(
    out_dir: pathlib.Path,
    run_at: str,
    args: argparse.Namespace,
    meta: dict[str, Any],
    refs: list[dict[str, Any]],
    phase: str,
    message: str,
    command_result: dict[str, Any] | None,
) -> dict[str, Any]:
    error = {
        "phase": phase,
        "message": message,
        "command": (
            {
                "returnCode": command_result["returnCode"],
                "timedOut": command_result.get("timedOut", False),
            }
            if command_result
            else None
        ),
    }
    refs.append(
        write_artifact(
            out_dir,
            "error",
            "error.json",
            json.dumps(error, indent=2),
            run_at,
        )
    )
    manifest = {
        "schemaVersion": "thesis_analyst_run_manifest_v1",
        "createdAt": run_at,
        "series": args.series,
        "period": args.period,
        "conditional": args.conditional,
        "promptMode": args.prompt_mode,
        "agent": meta,
        "ok": False,
        "cellsPath": None,
        "artifacts": refs,
        "validation": None,
        "error": error,
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
    return manifest


def extract_json_payload(text: str) -> list[dict]:
    stripped = text.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", stripped, flags=re.S)
    if fenced:
        stripped = fenced.group(1).strip()

    decoder = json.JSONDecoder()
    for index, char in enumerate(stripped):
        if char not in "[{":
            continue
        try:
            payload, _end = decoder.raw_decode(stripped[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return [payload]
        if isinstance(payload, list) and all(
            isinstance(item, dict) for item in payload
        ):
            return payload
    raise ValueError("No JSON object or array found in agent output")


def normalize_cells(parsed_path: pathlib.Path, normalized_path: pathlib.Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "normalize_spawn_json.py"),
            str(parsed_path),
            str(normalized_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "normalize_spawn_json.py failed:\n"
            f"stdout:\n{completed.stdout}\n\nstderr:\n{completed.stderr}"
        )


def validate_cells(
    cells: list[dict],
    allow_existing_slug: bool = False,
) -> dict[str, Any]:
    sys.path.insert(0, str(SCRIPTS))
    try:
        from spawned_cells_to_ts import existing_slugs, validate  # type: ignore
    finally:
        if sys.path[0] == str(SCRIPTS):
            sys.path.pop(0)

    taken = existing_slugs(ROOT / "site" / "src" / "data", ROOT / "__runner__.ts")
    seen: set[str] = set()
    rows = []
    ok = True
    for cell in cells:
        errors = validate(cell, taken | seen)
        if allow_existing_slug:
            errors = [error for error in errors if "slug collides" not in error]
        if errors:
            ok = False
        else:
            seen.add(cell["slug"])
        rows.append({"slug": cell.get("slug", "?"), "ok": not errors, "errors": errors})
    return {"ok": ok, "cells": rows}


def attach_activity_log(
    cells: list[dict],
    refs: list[dict],
    meta: dict[str, Any],
) -> list[dict]:
    return [
        {
            **cell,
            "model": cell.get("model", meta.get("model")),
            "activityLog": refs,
        }
        for cell in cells
    ]


def write_ts_module(
    cells_path: pathlib.Path,
    out_ts: pathlib.Path,
    const_name: str,
) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "spawned_cells_to_ts.py"),
            str(out_ts),
            const_name,
            str(cells_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "spawned_cells_to_ts.py failed:\n"
            f"stdout:\n{completed.stdout}\n\nstderr:\n{completed.stderr}"
        )


def mock_cell(series: str, period: str, run_at: str) -> dict[str, Any]:
    slug = f"{slugify(series)}-{slugify(period)}"
    country = "UK" if series.startswith(("ons.", "boe.")) else "US"
    resolution_date = (
        datetime.now(timezone.utc).date() + timedelta(days=90)
    ).isoformat()
    point = 5.1
    ci_low = 4.6
    ci_high = 5.8
    return {
        "slug": slug,
        "country": country,
        "type": "data",
        "title": f"{series} {period}",
        "question": (
            f"What will the first-print value of {series} be for {period}, "
            "as published by the official source?"
        ),
        "unit": "percent",
        "pointEstimate": point,
        "ciLow": ci_low,
        "ciHigh": ci_high,
        "confidence": 0.8,
        "resolutionDate": resolution_date,
        "resolutionSource": "Official statistical release",
        "resolutionSourceUrl": "https://www.ons.gov.uk/",
        "resolutionRule": (
            "Resolves to the first published official value for the target "
            "series and period; later revisions do not change the result."
        ),
        "dataPointId": f"{series}.{slugify(period)}.first_print",
        "historicalContext": [
            {"label": "t-3", "value": 5.0},
            {"label": "t-2", "value": 5.1},
            {"label": "t-1", "value": 5.2},
        ],
        "drivers": ["recent momentum", "release volatility", "labour-market slack"],
        "sourceContext": [
            "https://www.ons.gov.uk/",
            "https://www.nomisweb.co.uk/home/release_dates.asp",
        ],
        "runAt": run_at,
        "reasoning": [
            {"kind": "heading", "text": "Mock thesis.analyst dry run"},
            {
                "kind": "text",
                "text": (
                    "Reference class base rate from the last 3 prints is 5.1, "
                    "with recent values clustered between 5.0 and 5.2."
                ),
            },
            {
                "kind": "tool",
                "tool": "official.lookup",
                "call": f"official.lookup(series='{series}', period='{period}')",
                "result": "{t_minus_3: 5.0, t_minus_2: 5.1, t_minus_1: 5.2}",
            },
            {
                "kind": "tool",
                "tool": "calendar.lookup",
                "call": f"calendar.lookup(series='{series}', period='{period}')",
                "result": (
                    f"{{resolution_date: '{resolution_date}', first_print: true}}"
                ),
            },
            {
                "kind": "math",
                "text": (
                    "Point = recent center 5.1. Realized volatility plus "
                    "horizon uncertainty gives an 80% interval [4.6, 5.8]."
                ),
            },
            {
                "kind": "text",
                "text": (
                    "Outside the interval if hiring weakens abruptly or the "
                    "survey mean-reverts faster than the recent prints imply."
                ),
            },
            {"kind": "forecast", "point": point, "ciLow": ci_low, "ciHigh": ci_high},
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--series", required=True)
    parser.add_argument("--period", required=True)
    parser.add_argument("--conditional")
    parser.add_argument("--prompt-mode", choices=["full", "fast"], default="full")
    parser.add_argument("--out-dir")
    parser.add_argument("--command")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--response-file")
    parser.add_argument("--mock-cell", action="store_true")
    parser.add_argument("--print-prompt", action="store_true")
    parser.add_argument("--allow-existing-slug", action="store_true")
    parser.add_argument("--write-ts")
    parser.add_argument("--const-name", default="SPAWNED_FORECAST_CELLS")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_at = utc_now()
    prompt, meta = build_run_prompt(
        args.series,
        args.period,
        args.conditional,
        args.prompt_mode,
    )
    if args.print_prompt:
        print(prompt)
        return 0

    if (
        sum(bool(value) for value in [args.command, args.response_file, args.mock_cell])
        != 1
    ):
        raise SystemExit(
            "Choose exactly one of --command, --response-file, or --mock-cell"
        )

    out_dir = (
        pathlib.Path(args.out_dir)
        if args.out_dir
        else default_out_dir(args.series, args.period, run_at)
    )
    refs: list[dict[str, Any]] = []
    refs.append(write_artifact(out_dir, "prompt", "prompt.md", prompt, run_at))

    command_result: dict[str, Any] | None = None
    if args.command:
        command_result = run_agent_command(
            args.command,
            prompt,
            out_dir / "prompt.md",
            args.timeout_seconds,
        )
        refs.append(
            write_artifact(
                out_dir,
                "command",
                "command.json",
                json.dumps(
                    {
                        "argv": command_result["argv"],
                        "returnCode": command_result["returnCode"],
                        "timedOut": command_result.get("timedOut", False),
                        "startedAt": command_result["startedAt"],
                        "finishedAt": command_result["finishedAt"],
                    },
                    indent=2,
                ),
                run_at,
            )
        )
        refs.append(
            write_artifact(
                out_dir, "stdout", "stdout.txt", command_result["stdout"], run_at
            )
        )
        refs.append(
            write_artifact(
                out_dir, "stderr", "stderr.txt", command_result["stderr"], run_at
            )
        )
        raw_response = command_result["stdout"]
        if command_result["returnCode"] != 0:
            print(
                f"agent command exited {command_result['returnCode']}", file=sys.stderr
            )
    elif args.response_file:
        raw_response = pathlib.Path(args.response_file).read_text()
        refs.append(
            write_artifact(
                out_dir,
                "command",
                "command.json",
                json.dumps({"responseFile": args.response_file}, indent=2),
                run_at,
            )
        )
    else:
        raw_response = json.dumps(
            [mock_cell(args.series, args.period, run_at)], indent=2
        )
        refs.append(
            write_artifact(
                out_dir,
                "command",
                "command.json",
                json.dumps({"mockCell": True}, indent=2),
                run_at,
            )
        )

    runtime_meta = stamp_runtime_invocation(meta, command_result)

    refs.append(
        write_artifact(
            out_dir, "raw_response", "raw_response.txt", raw_response, run_at
        )
    )

    try:
        parsed_cells = extract_json_payload(raw_response)
    except ValueError as exc:
        manifest = write_failure_manifest(
            out_dir,
            run_at,
            args,
            runtime_meta,
            refs,
            "parse",
            str(exc),
            command_result,
        )
        print(json.dumps(manifest, indent=2))
        return 1
    parsed_path = out_dir / "parsed_cells.json"
    refs.append(
        write_artifact(
            out_dir,
            "parsed_cell",
            parsed_path.name,
            json.dumps(parsed_cells, indent=2),
            run_at,
        )
    )

    normalized_path = out_dir / "normalized_cells.json"
    normalize_cells(parsed_path, normalized_path)
    normalized_cells = json.loads(normalized_path.read_text())
    refs.append(
        {
            "artifactType": "normalized_cell",
            "path": repo_relative(normalized_path),
            "sha256": sha256_bytes(normalized_path.read_bytes()),
            "bytes": normalized_path.stat().st_size,
            "createdAt": run_at,
        }
    )

    validation = validate_cells(normalized_cells, args.allow_existing_slug)
    validation_ref = write_artifact(
        out_dir,
        "validation_report",
        "validation.json",
        json.dumps(validation, indent=2),
        run_at,
    )
    refs.append(validation_ref)

    cells_with_activity = attach_activity_log(normalized_cells, refs, runtime_meta)
    cells_path = out_dir / "cells.with_activity.json"
    cells_path.write_text(json.dumps(cells_with_activity, indent=2))

    manifest = {
        "schemaVersion": "thesis_analyst_run_manifest_v1",
        "createdAt": run_at,
        "series": args.series,
        "period": args.period,
        "conditional": args.conditional,
        "promptMode": args.prompt_mode,
        "agent": runtime_meta,
        "ok": validation["ok"]
        and (not command_result or command_result["returnCode"] == 0),
        "cellsPath": repo_relative(cells_path),
        "artifacts": refs,
        "validation": validation,
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

    if args.write_ts:
        write_ts_module(cells_path, pathlib.Path(args.write_ts), args.const_name)

    print(json.dumps(manifest, indent=2))
    return 0 if manifest["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
