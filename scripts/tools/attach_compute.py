"""Attach an audited PolicyEngine compute row to a bill.json provision.

The compute block is the #45 leg of the bill.json contract (plan #43): model
runs attached to the provisions they price. Extraction regens (ingest_bill.py)
rewrite bills/<slug>.json WITHOUT compute rows — re-run this after any regen to
re-attach them. Idempotent: matching rows (same model+reform+year+dataset) are
replaced in place, never duplicated.

Usage:
    python scripts/tools/attach_compute.py <slug> [--provision 0] [--row path.json]

Without --row, uses the row registry below (checked in next to the runs that
produced it). Row provenance should come from the audited call path
(scripts/tools/policyengine.py compute_block / modal_economy.py output).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BILLS_DIR = Path(__file__).resolve().parents[2] / "bills"

# Registry of audited compute rows, keyed by (slug, provision index).
# S.3596 row: certified build-P run, Modal, 2026-07-31 — full artifact at
# bills/stronger-start-working-families-act/buildP-economy-2026.json.
ROWS: dict[tuple[str, int], list[dict]] = {
    ("s3596-119", 0): [
        {
            "model": "policyengine-us",
            "reform": {
                "gov.irs.credits.ctc.refundable.phase_in.threshold": {
                    "2026-01-01.2100-12-31": 0
                }
            },
            "result_summary": (
                "2026: budgetary impact -$1.83B; SPM child poverty -1.2% (17.02% to "
                "16.82%); 6.5% of people gain, concentrated in the lowest income "
                "deciles (decile-1 average +$32/yr vs decile-10 +$0.30); Gini -0.02%."
            ),
            "engine": "modal",
            "pe_us_version": "1.764.6",
            "pe_core_version": "3.26.11",
            "dataset": "populace-us-2024-buildp-sparse-rmloss100-cae8640-20260728T011454Z",
            "certification": {
                "certified_model_version": "1.764.6",
                "running_model_version": "1.764.6",
                "certified": True,
            },
            "year": 2026,
            "region": "us",
            "status": "ok",
            "budgetary_impact": -1826396338.82,
            "poverty_child_pct_change": -0.0115527,
            "note": (
                "The statute sets the threshold to $1; PolicyEngine policy 85587 "
                "models $0 — economically identical, recorded per the audit. Static "
                "microsim, one evidence stream with its own error bars; anchors: "
                "previously published PolicyEngine figure -$1.6B on an older data "
                "build, Tax Policy Center about $1.0B per year."
            ),
            "source": (
                "Audited call path scripts/tools/policyengine.py per POLICYENGINE.md; "
                "run scripts/tools/modal_economy.py 2026-07-31 on the certified stack; "
                "full artifact bills/stronger-start-working-families-act/"
                "buildP-economy-2026.json (PR #64)."
            ),
        }
    ],
}


def _row_key(row: dict) -> tuple:
    return (
        row.get("model"),
        json.dumps(row.get("reform", {}), sort_keys=True),
        row.get("year"),
        row.get("dataset"),
    )


def attach(slug: str, provision_index: int, rows: list[dict]) -> Path:
    path = BILLS_DIR / f"{slug}.json"
    artifact = json.loads(path.read_text(encoding="utf-8"))
    provisions = artifact["provisions"]
    if provision_index >= len(provisions):
        raise SystemExit(f"{slug}: provision {provision_index} out of range ({len(provisions)})")
    existing = provisions[provision_index].get("compute") or []
    keep = [r for r in existing if _row_key(r) not in {_row_key(n) for n in rows}]
    provisions[provision_index]["compute"] = keep + rows
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(artifact, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Attach audited compute rows to bill.json")
    ap.add_argument("slug")
    ap.add_argument("--provision", type=int, default=0)
    ap.add_argument("--row", help="path to a JSON file holding one compute row (or a list)")
    args = ap.parse_args(argv)

    if args.row:
        loaded = json.loads(Path(args.row).read_text(encoding="utf-8"))
        rows = loaded if isinstance(loaded, list) else [loaded]
    else:
        rows = ROWS.get((args.slug, args.provision))
        if not rows:
            print(f"no registered rows for ({args.slug}, {args.provision}); pass --row", file=sys.stderr)
            return 1
    path = attach(args.slug, args.provision, rows)
    print(f"attached {len(rows)} compute row(s) -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
