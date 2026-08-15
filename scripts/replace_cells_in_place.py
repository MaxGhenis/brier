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
RUN_PROVENANCES = {"ci", "local_operator_attested"}


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


def existing_run_provenance(cell_block: str) -> str | None:
    """Read the existing predictionRun label without inferring a new one."""

    match = re.search(r'"?predictionRun"?\s*:\s*\{', cell_block)
    if match is None:
        return None
    start = cell_block.find("{", match.start())
    depth = 0
    in_string = False
    escaped = False
    end = None
    for index in range(start, len(cell_block)):
        char = cell_block[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end = index + 1
                break
    if end is None:
        raise SystemExit("unbalanced predictionRun block in existing cell")
    run_block = cell_block[start:end]
    matches = re.findall(r'"?provenance"?\s*:\s*"([^"]+)"', run_block)
    if not matches:
        return None
    if len(matches) != 1 or matches[0] not in RUN_PROVENANCES:
        raise SystemExit(
            f"existing predictionRun has invalid provenance labels: {matches}"
        )
    return matches[0]


def main() -> int:
    target, upgrades_path = sys.argv[1], sys.argv[2]
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from spawned_cells_to_ts import (
        SEALED_AGENT_KEY,
        SEALED_HISTORY_AUTHORIZATION_KEY,
        load_cells,
        to_forecast_cell,
        validate,
    )

    src = pathlib.Path(target).read_text()
    raw_upgrades = json.load(open(upgrades_path))
    provenances = []
    for cell in raw_upgrades:
        slug = cell["slug"]
        start, end = find_cell_block(src, slug)
        old = src[start:end]
        provenances.append(existing_run_provenance(old))

    # Authenticate the exact upgrades file through the same custody/legacy
    # boundary as ordinary generated-module promotion. Loading once per public
    # label preserves the existing cell's provenance without letting this
    # replacement path bypass current-version custody.
    loaded_by_provenance: dict[str | None, list[dict]] = {}
    for provenance in provenances:
        if provenance not in loaded_by_provenance:
            loaded_by_provenance[provenance] = load_cells(
                pathlib.Path(upgrades_path), provenance=provenance
            )

    for index, provenance in enumerate(provenances):
        cell = loaded_by_provenance[provenance][index]
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
        sealed_agent = cell.get(SEALED_AGENT_KEY)
        sealed_authorization = cell.get(SEALED_HISTORY_AUTHORIZATION_KEY)
        errs = [
            e
            for e in validate(
                cell,
                set(),
                agent_version=(
                    sealed_agent.get("agentVersion")
                    if isinstance(sealed_agent, dict)
                    else None
                ),
                trusted_history_authorization=(
                    sealed_authorization
                    if isinstance(sealed_authorization, dict)
                    else None
                ),
            )
            if "collide" not in e and "dataPointId" not in e
        ]
        if errs:
            raise SystemExit(f"{slug}: upgrade fails contract: {'; '.join(errs)}")
        new = to_forecast_cell(cell, provenance=provenance)
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
