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
                "Federal aggregation (income_tax minus measured-zero benefits; state "
                "spillover of ~$0.35M/yr itemized separately). Gains concentrate in "
                "the lowest income deciles (decile 1 averages "
                "+$32/yr vs +$0.30 for decile 10); Gini falls 0.02%. The annual cost "
                "declines from $1.86B to $1.53B across the window as earnings growth "
                "lifts families past the old $2,500 floor."
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
            "budgetary_impact": -1826050568.80,
            "ten_year_budgetary_impact": -17069142980.93,
            "ten_year_window": "2026-2035",
            "poverty_child_pct_change": -0.0115527,
            "beneficiaries_share": 0.0648,
            "note": (
                "Statute sets the threshold to $1; PolicyEngine policy 85587 models "
                "$0 — economically identical, recorded per the audit. Static microsim, "
                "one evidence stream with its own error bars. Anchors: PolicyEngine "
                "-$1.6B/yr on an older data build; Tax Policy Center ~$1.0B/yr."
            ),
            "source": (
                "Audited call path scripts/tools/policyengine.py per POLICYENGINE.md; "
                "run scripts/tools/modal_economy.py 2026-07-31 on the certified stack; "
                "full artifacts bills/stronger-start-working-families-act/"
                "buildP-economy-2026.json and buildP-sweep-2026-2035.json "
                "(sum-checked; PR #64)."
            ),
        }
    ],
}


# Run artifacts that ground the registry rows (land via PR #64). When present,
# attach VERIFIES the registry numbers against them and dies loudly on drift —
# a hand-transcribed number that no longer matches its source run must never
# ship silently (that is how the published -$1.6B went stale).
ARTIFACT_DIR = BILLS_DIR / "stronger-start-working-families-act"
GROUNDING = {
    ("s3596-119", 0): {
        "economy": ARTIFACT_DIR / "buildP-economy-2026.json",
        "sweep": ARTIFACT_DIR / "buildP-sweep-2026-2035.json",
    },
}


def _verify_against_artifacts(slug: str, provision_index: int, rows: list[dict]) -> None:
    ground = GROUNDING.get((slug, provision_index))
    if not ground:
        return
    row = rows[0]
    checks: list[tuple[str, float, float]] = []
    econ_path, sweep_path = ground["economy"], ground["sweep"]
    if econ_path.exists():
        econ = json.loads(econ_path.read_text(encoding="utf-8"))
        checks.append(("budgetary_impact", row["budgetary_impact"],
                       econ["budget"]["budgetary_impact"]))
        checks.append(("poverty_child_pct_change", row["poverty_child_pct_change"],
                       econ["poverty"]["child"]["pct_change"]))
        if econ.get("dataset") != row.get("dataset"):
            raise SystemExit(f"DRIFT: dataset {row.get('dataset')} != artifact {econ.get('dataset')}")
    if sweep_path.exists():
        sweep = json.loads(sweep_path.read_text(encoding="utf-8"))
        checks.append(("ten_year_budgetary_impact", row["ten_year_budgetary_impact"],
                       sweep["ten_year_budgetary_impact"]))
    verified = []
    for name, registry_val, artifact_val in checks:
        tol = max(abs(artifact_val) * 1e-4, 1e-6)  # transcriptions are rounded
        if abs(registry_val - artifact_val) > tol:
            raise SystemExit(f"DRIFT in {name}: registry {registry_val} != artifact {artifact_val} "
                             f"— re-transcribe from the run artifact before attaching")
        verified.append(name)
    if verified:
        print(f"verified against run artifacts: {', '.join(verified)}")
    else:
        print("note: run artifacts not present on this branch — registry values unverified "
              "(they verify automatically once PR #64's artifacts land)")


def _row_key(row: dict) -> tuple:
    return (
        row.get("model"),
        json.dumps(row.get("reform", {}), sort_keys=True),
        row.get("year"),
        row.get("dataset"),
    )


def attach(slug: str, provision_index: int, rows: list[dict]) -> Path:
    _verify_against_artifacts(slug, provision_index, rows)
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
