#!/usr/bin/env python3
"""Report per-run token usage and list-price cost from sealed custody traces.

Every analyst invocation retains its codex usage payload in the run's
``*codex_trace.json`` artifact (draft, pre-submit review, and final phases),
so cost telemetry is read straight out of the immutable record — no separate
metering system. Coverage begins with the 2026-06-28 custody regime; earlier
runs predate artifact retention.

Usage: usage_report.py [--records records/thesis-analyst] [--json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import statistics
from collections import defaultdict
from typing import Any

# $/M tokens (input, cached input, output), provider list prices.
# Mirrors the pinned table in Max's usage-tracker extract.py.
LIST_PRICES: dict[str, tuple[float, float, float]] = {
    "gpt-5.6-sol": (5.0, 0.50, 30.0),
    "gpt-5.6-terra": (2.5, 0.25, 15.0),
    "gpt-5.6-luna": (1.0, 0.10, 6.0),
    "gpt-5.6": (5.0, 0.50, 30.0),
    "gpt-5.5": (5.0, 0.50, 30.0),
}
FALLBACK_PRICE = (5.0, 0.50, 30.0)


def invocation_cost(model: str, usage: dict[str, Any]) -> float:
    p_in, p_cached, p_out = LIST_PRICES.get(model, FALLBACK_PRICE)
    tokens_in = usage.get("input_tokens", 0)
    cached = usage.get("cached_input_tokens", 0)
    out = usage.get("output_tokens", 0)
    return (max(tokens_in - cached, 0) * p_in + cached * p_cached + out * p_out) / 1e6


def phase_of(name: str) -> str:
    if "pre_submit_review" in name:
        return "review"
    if name.startswith("draft_"):
        return "draft"
    return "final"


def collect(records_root: pathlib.Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    missing_usage = 0
    for trace_path in sorted(records_root.rglob("*codex_trace.json")):
        trace = json.loads(trace_path.read_text())
        usage = trace.get("usage")
        if not usage:
            missing_usage += 1
            continue
        run_dir = trace_path.parent
        date = next((p for p in run_dir.parts if p.startswith("20")), "?")[:10]
        model = trace.get("model") or "?"
        rows.append(
            {
                "dir": str(run_dir),
                "date": date,
                "phase": phase_of(trace_path.name),
                "model": model,
                "input": usage.get("input_tokens", 0),
                "cached": usage.get("cached_input_tokens", 0),
                "output": usage.get("output_tokens", 0),
                "cost": invocation_cost(model, usage),
            }
        )
    return {"rows": rows, "missing_usage": missing_usage}


def summarize(data: dict[str, Any]) -> dict[str, Any]:
    rows = data["rows"]
    by_dir: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"cost": 0.0, "models": set(), "date": ""}
    )
    for row in rows:
        entry = by_dir[row["dir"]]
        entry["cost"] += row["cost"]
        entry["models"].add(row["model"])
        entry["date"] = row["date"]

    per_event = sorted(entry["cost"] for entry in by_dir.values())
    total = sum(row["cost"] for row in rows)

    by_model: dict[str, dict[str, float]] = defaultdict(lambda: {"n": 0, "cost": 0.0})
    for row in rows:
        by_model[row["model"]]["n"] += 1
        by_model[row["model"]]["cost"] += row["cost"]

    by_phase: dict[str, float] = defaultdict(float)
    for row in rows:
        by_phase[row["phase"]] += row["cost"]

    by_month: dict[str, list[float]] = defaultdict(list)
    for entry in by_dir.values():
        by_month[entry["date"][:7]].append(entry["cost"])

    def dist(values: list[float]) -> dict[str, float]:
        if not values:
            return {}
        ordered = sorted(values)
        return {
            "n": len(ordered),
            "median": statistics.median(ordered),
            "mean": statistics.mean(ordered),
            "p10": ordered[len(ordered) // 10],
            "p90": ordered[9 * len(ordered) // 10],
            "max": ordered[-1],
        }

    return {
        "invocations": len(rows),
        "missingUsage": data["missing_usage"],
        "generationEvents": len(by_dir),
        "totalListCost": round(total, 2),
        "perEvent": {k: round(v, 3) for k, v in dist(per_event).items()},
        "byModel": {
            model: {"invocations": int(v["n"]), "cost": round(v["cost"], 2)}
            for model, v in sorted(by_model.items(), key=lambda x: -x[1]["cost"])
        },
        "byPhaseShare": {
            phase: round(cost / total, 3) if total else 0.0
            for phase, cost in sorted(by_phase.items(), key=lambda x: -x[1])
        },
        "perEventByMonth": {
            month: {k: round(v, 3) for k, v in dist(values).items()}
            for month, values in sorted(by_month.items())
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", default="records/thesis-analyst")
    parser.add_argument("--json", action="store_true", help="emit JSON only")
    args = parser.parse_args()

    summary = summarize(collect(pathlib.Path(args.records)))
    if args.json:
        print(json.dumps(summary, indent=2))
        return 0

    print(
        f"invocations: {summary['invocations']} "
        f"(missing usage: {summary['missingUsage']})"
    )
    print(f"generation events: {summary['generationEvents']}")
    print(f"total list-price cost: ${summary['totalListCost']:,.2f}")
    pe = summary["perEvent"]
    print(
        f"per generation event: median ${pe['median']:.3f} "
        f"(p10 ${pe['p10']:.3f} / p90 ${pe['p90']:.3f} / max ${pe['max']:.2f})"
    )
    print("by model:")
    for model, v in summary["byModel"].items():
        print(f"  {model:14s} {v['invocations']:4d} runs  ${v['cost']:8.2f}")
    print("phase share of spend:")
    for phase, share in summary["byPhaseShare"].items():
        print(f"  {phase:8s} {share:.0%}")
    print("per event by month:")
    for month, v in summary["perEventByMonth"].items():
        print(f"  {month}: n={v['n']:.0f} median ${v['median']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
