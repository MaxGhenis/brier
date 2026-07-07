#!/usr/bin/env python3
"""Publish a batch's winning cells as a wave module in one step.

Wraps the by-hand publish flow: pick the latest passing run per slug from
batch manifests, convert them with spawned_cells_to_ts.py, register their
ledger targets, and wire the module into forecast-cells.ts (idempotent —
existing import lines are left alone).

Usage:
    python3 scripts/register_wave.py --name auto-2026-07-10 \
        --batch records/thesis-analyst/batches/2026-07-10/roll.json
        [--allow-missing]

The module lands at site/src/data/forecast-examples/{name}.ts exporting
{NAME}_WAVE. Exits 2 when the batch produced no publishable cells (callers
treat that as "nothing to do"), 1 on missing slugs without --allow-missing.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CELLS_TS = ROOT / "site" / "src" / "data" / "forecast-cells.ts"
EXAMPLES = ROOT / "site" / "src" / "data" / "forecast-examples"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--batch", action="append", required=True)
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()

    winners: dict[str, str] = {}
    wanted: set[str] = set()
    for path in args.batch:
        batch = json.loads(pathlib.Path(path).read_text())
        for result in batch["results"]:
            slug = result["target"]["catalogSlug"]
            wanted.add(slug)
            if result["ok"] and result.get("cellsPath"):
                winners[slug] = result["cellsPath"]

    missing = sorted(wanted - set(winners))
    if missing:
        print(f"no passing run for: {', '.join(missing)}", file=sys.stderr)
        if not args.allow_missing:
            return 1
    if not winners:
        print("no publishable cells", file=sys.stderr)
        return 2

    const = re.sub(r"[^A-Z0-9]+", "_", args.name.upper()).strip("_") + "_WAVE"
    module = EXAMPLES / f"{args.name}.ts"
    run_files = sorted(set(winners.values()))

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "spawned_cells_to_ts.py"),
         str(module), const, *run_files],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_ledger_targets.py"),
         *run_files],
        check=True,
    )

    source = CELLS_TS.read_text()
    import_line = (
        f'import {{ {const} }} from "./forecast-examples/{args.name}";'
    )
    if import_line not in source:
        anchor = re.search(r'^import \{ [A-Z0-9_]+ \} from "\./forecast-examples/[^"]+";$',
                           source, re.MULTILINE)
        assert anchor, "no forecast-examples import anchor found"
        source = source.replace(anchor.group(0), anchor.group(0) + "\n" + import_line, 1)
        spread = re.search(r"^  \.\.\.[A-Z0-9_]+,$", source, re.MULTILINE)
        assert spread, "no wave spread anchor found"
        source = source.replace(spread.group(0), spread.group(0) + f"\n  ...{const},", 1)
        CELLS_TS.write_text(source)
        print(f"registered {const} in forecast-cells.ts")
    print(f"published {len(winners)} cells -> {module.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
