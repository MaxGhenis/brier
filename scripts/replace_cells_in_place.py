#!/usr/bin/env python3
"""Replace existing catalog cells with upgraded agent-run versions, in place.

For upgrades to ALREADY-PUBLISHED cells (same slug): published spec fields
(slug, question, unit, type, resolutionDate, resolutionRule, conditionalOn)
must match the existing cell exactly — only evidence, reasoning, drivers,
historicalContext, the numeric forecast, resolutionSourceUrl, and the
predictionRun stamp may change. Aborts loudly on any spec drift.

Usage: replace_cells_in_place.py TARGET_TS UPGRADES.json
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

SPEC_FIELDS = ["slug", "question", "unit", "type", "resolutionDate", "conditionalOn"]


def find_cell_block(src: str, slug: str) -> tuple[int, int]:
    """Return (start, end) of the {...} object literal whose slug matches."""
    # Generated modules quote keys ("slug":) while hand-wired ones may not
    # (slug:); accept both so drift checks can never silently skip a cell.
    m = re.search(rf'"?slug"?:\s*"{re.escape(slug)}"', src)
    if not m:
        raise SystemExit(f"slug {slug} not found in target file")
    start = src.rfind("{", 0, m.start())
    depth, in_str, esc, quote = 0, False, False, ""
    i = start
    while i < len(src):
        ch = src[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                in_str = False
        else:
            if ch in "\"'`":
                in_str, quote = True, ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return start, i + 1
        i += 1
    raise SystemExit(f"unbalanced braces hunting {slug}")


def main() -> int:
    target, upgrades_path = sys.argv[1], sys.argv[2]
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from spawned_cells_to_ts import agent_stamp, to_forecast_cell, validate

    src = pathlib.Path(target).read_text()
    upgrades = json.load(open(upgrades_path))
    for cell in upgrades:
        slug = cell["slug"]
        start, end = find_cell_block(src, slug)
        old = src[start:end]
        for f in SPEC_FIELDS:
            old_val = re.search(rf'"?{f}"?:\s*"((?:[^"\\]|\\.)*)"', old)
            if f in cell and not old_val:
                raise SystemExit(
                    f"{slug}: published spec field {f!r} not found in the "
                    "existing cell block — refusing to replace without a "
                    "drift check"
                )
            if f in cell and old_val and old_val.group(1) != str(cell[f]):
                raise SystemExit(
                    f"{slug}: published spec field {f!r} drifted —\n"
                    f"  existing: {old_val.group(1)[:120]}\n"
                    f"  upgrade:  {str(cell[f])[:120]}"
                )
        # resolutionSource: the published text is the ledger's canonical
        # resolver identity. Target contexts may enrich it with fetch
        # instructions (e.g. the VINTAGE DISCIPLINE suffix) that the agent
        # echoes back; keep the published identity and drop the suffix,
        # loudly. Anything other than a pure suffix extension aborts.
        pub_src = re.search(r'"?resolutionSource"?:\s*"((?:[^"\\]|\\.)*)"', old)
        if pub_src and "resolutionSource" in cell:
            published = json.loads(f'"{pub_src.group(1)}"')
            upgraded = str(cell["resolutionSource"])
            if upgraded != published:
                if not upgraded.startswith(published):
                    raise SystemExit(
                        f"{slug}: resolutionSource drifted beyond an "
                        "instruction-suffix extension —\n"
                        f"  existing: {published[:120]}\n"
                        f"  upgrade:  {upgraded[:120]}"
                    )
                print(
                    f"{slug}: keeping published resolutionSource; upgrade "
                    "carried an instruction-enriched variant "
                    f"({len(upgraded) - len(published)} suffix chars dropped)"
                )
                cell = {**cell, "resolutionSource": published}
        errs = [e for e in validate(cell, set()) if "collide" not in e and "dataPointId" not in e]
        if errs:
            raise SystemExit(f"{slug}: upgrade fails contract: {'; '.join(errs)}")
        new = to_forecast_cell(cell)
        # carry forward fields the upgrade may not restate
        for f in ("dataPointId", "policyParameter"):
            kept = re.search(rf'"?{f}"?:\s*"((?:[^"\\]|\\.)*)"', old)
            if kept and f not in new:
                new[f] = kept.group(1)
        block = json.dumps(new, indent=2, ensure_ascii=False)
        indent = " " * (len(src[:start].split("\n")[-1]))
        block = block.replace("\n", "\n" + indent)
        src = src[:start] + block + src[end:]
        print(f"replaced {slug}")
    pathlib.Path(target).write_text(src)
    return 0


if __name__ == "__main__":
    sys.exit(main())
