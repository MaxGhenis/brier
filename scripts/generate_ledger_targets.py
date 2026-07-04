#!/usr/bin/env python3
"""Append target registrations for spawned cells to ledger-targets.generated.ts.

Every published forecast must have a Thesis target ledger entry for its
dataPointId (requireLedgerTarget throws at build time otherwise). Hand-authored
entries live in ledger-targets.ts; everything spawned by the thesis.analyst
pipeline registers here, derived from the recorded cell's own resolver fields.

Usage:
  python3 scripts/generate_ledger_targets.py CELLS1.json [CELLS2.json ...]

Idempotent: dataPointIds already registered in either ledger file are skipped.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
GENERATED = ROOT / "site" / "src" / "data" / "ledger-targets.generated.ts"
HAND_AUTHORED = ROOT / "site" / "src" / "data" / "ledger-targets.ts"


def registered_data_point_ids() -> set[str]:
    ids = set()
    for path in (GENERATED, HAND_AUTHORED):
        ids.update(
            re.findall(r'dataPointId:\s*\n?\s*"([^"]+)"', path.read_text())
        )
    return ids


def entry_for(cell: dict) -> dict:
    entry = {
        "kind": "target_registered",
        "dataPointId": cell["dataPointId"],
        "observationId": f"obs.{cell['dataPointId']}",
        "country": cell["country"],
        "periodLabel": cell["resolutionDate"],
        "unit": cell["unit"],
        "resolutionDate": cell["resolutionDate"],
        "resolutionSource": cell["resolutionSource"],
        "resolutionSourceUrl": cell.get("resolutionSourceUrl"),
        "resolutionRule": cell["resolutionRule"],
        "resolutionPolicy": "first_print",
        "sourceKind": "official_release",
        "source": cell["resolutionSource"],
        "sourceUrl": cell.get("resolutionSourceUrl"),
        "note": (
            "Target registration generated from the recorded thesis.analyst "
            f"run for {cell['title']}."
        ),
    }
    return {k: v for k, v in entry.items() if v is not None}


def ts_literal(entry: dict) -> str:
    lines = ["  {"]
    for key, value in entry.items():
        lines.append(f"    {key}: {json.dumps(value, ensure_ascii=False)},")
    lines.append("  },")
    return "\n".join(lines)


def main() -> int:
    cells = []
    for path in sys.argv[1:]:
        cells.extend(json.load(open(path)))
    existing = registered_data_point_ids()
    new_entries = []
    for cell in cells:
        if cell["dataPointId"] in existing:
            continue
        existing.add(cell["dataPointId"])
        new_entries.append(entry_for(cell))
    if not new_entries:
        print("nothing to register")
        return 0
    source = GENERATED.read_text()
    closer = "] satisfies" if "] satisfies" in source else "];"
    idx = source.rindex(closer)
    block = "\n".join(ts_literal(entry) for entry in new_entries) + "\n"
    GENERATED.write_text(source[:idx] + block + source[idx:])
    print(f"registered {len(new_entries)} targets -> {GENERATED}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
