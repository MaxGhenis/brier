"""Quarantine truncated runs and queue them for re-execution.

AGENTS.md forbids silently cleaning failed runs into successful ones, so the
failed traces are MOVED to a quarantine file rather than deleted, and the
re-run is recorded. The defect being corrected: five runs hit the max_tokens
cap exactly and lost their trailing JSON. That loss correlated with elicitation
verbosity — a measured dimension — so leaving it in place would bias the very
comparison the experiment exists to make.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=Path, default=HERE / "runs_api.jsonl")
    ap.add_argument("--quarantine", type=Path, default=HERE / "runs_api.quarantined.jsonl")
    ap.add_argument("--apply", action="store_true", help="actually rewrite the runs file")
    args = ap.parse_args()

    kept: list[str] = []
    dropped: list[dict] = []
    for line in args.runs.read_text().splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            kept.append(line)
            continue
        forecast = rec.get("forecast") or rec.get("answer") or {}
        failed = bool(rec.get("error")) or "parse_error" in forecast
        if failed:
            dropped.append(rec)
        else:
            kept.append(line)

    print(f"total={len(kept) + len(dropped)} keep={len(kept)} quarantine={len(dropped)}")
    for rec in dropped:
        cfg = rec.get("config", {})
        print(
            f"  {rec.get('cell_key')}  elicitation={cfg.get('elicitation')} "
            f"pipeline={cfg.get('pipeline')} "
            f"reason={rec.get('error') or (rec.get('forecast') or {}).get('parse_error')}"
        )

    if not args.apply:
        print("\n(dry run — pass --apply to rewrite; then re-run sweep.py to regenerate these cells)")
        return

    with args.quarantine.open("a") as fh:
        for rec in dropped:
            rec["_quarantined_reason"] = "max_tokens truncation; re-run with raised cap"
            fh.write(json.dumps(rec) + "\n")
    args.runs.write_text("\n".join(kept) + ("\n" if kept else ""))
    print(f"\nquarantined {len(dropped)} -> {args.quarantine}")
    print("now re-run: python3 experiments/billimpact/sweep.py --out experiments/billimpact/runs_api.jsonl")


if __name__ == "__main__":
    main()
