"""Port the Farm Bill 2.0 analysis from ThesisInstitute/implementation-analysis.

One-off migration: the standalone site's analysis.json is the direct
ancestor of the bill.json contract (issue #43), so this is a recorded
passthrough, not a rewrite. Fields the contract doesn't (yet) name —
provisions[].context and metrics[].registry (the frozen analysis-day
badge) — are carried through: the site's registry seam uses the frozen
badge as fallback until the live registry mapper computes status at
build time, at which point the frozen field is ignorable.

Usage:
  uv run --extra bills scripts/bills/port_farm_bill.py
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx

SOURCE = (
    "https://raw.githubusercontent.com/ThesisInstitute/implementation-analysis/"
    "main/site/analysis.json"
)
REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "bills" / "farm-bill-2-0.json"


def main() -> None:
    analysis = httpx.get(SOURCE, timeout=60, follow_redirects=True).json()
    analysis["bill"]["slug"] = "farm-bill-2-0"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    n_metrics = sum(len(p["metrics"]) for p in analysis["provisions"])
    print(
        f"wrote {OUT.relative_to(REPO_ROOT)} "
        f"({len(analysis['provisions'])} provisions, {n_metrics} metrics)"
    )


if __name__ == "__main__":
    main()
