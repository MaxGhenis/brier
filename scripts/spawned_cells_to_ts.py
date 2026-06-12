#!/usr/bin/env python3
"""Convert spawned-forecast JSON (from thesis.analyst agent runs) into a
ForecastCell TS module, validating the trace-depth contract on the way in.

Usage:
  python3 scripts/spawned_cells_to_ts.py OUT_TS CONST_NAME IN1.json [IN2.json ...]
"""

import json
import pathlib
import re
import sys
from datetime import datetime, timezone

ALLOWED_UNITS = {
    "count", "percent", "gbp_billions", "usd", "usd_billions", "usd_monthly",
    "thousands", "millions", "per_1000_live_births", "ratio", "percent_growth",
}
ALLOWED_COUNTRIES = {"US", "UK", "CA", "AU", "EA", "JP"}
ALLOWED_TYPES = {"data", "policy", "conditional"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED = [
    "slug", "country", "type", "title", "question", "unit", "pointEstimate",
    "ciLow", "ciHigh", "confidence", "resolutionDate", "resolutionSource",
    "resolutionSourceUrl", "resolutionRule", "dataPointId",
    "historicalContext", "drivers", "sourceContext", "runAt", "reasoning",
]


def existing_slugs(site_data: pathlib.Path) -> set[str]:
    slugs = set()
    for f in list(site_data.glob("almanac-examples/*.ts")) + [site_data / "forecast-cells.ts"]:
        slugs |= set(re.findall(r'slug:\s*"([^"]+)"', f.read_text()))
    return slugs


def validate(cell: dict, taken: set[str]) -> list[str]:
    errs = []
    for k in REQUIRED:
        if k not in cell:
            errs.append(f"missing {k}")
    if errs:
        return errs
    if not SLUG_RE.match(cell["slug"]):
        errs.append("bad slug format")
    if cell["slug"] in taken:
        errs.append("slug collides with existing catalog")
    if cell["unit"] not in ALLOWED_UNITS:
        errs.append(f"unit {cell['unit']!r} not allowed")
    if cell["country"] not in ALLOWED_COUNTRIES:
        errs.append(f"country {cell['country']!r} not allowed")
    if cell["type"] not in ALLOWED_TYPES:
        errs.append(f"type {cell['type']!r} not allowed")
    if not cell["ciLow"] < cell["pointEstimate"] < cell["ciHigh"]:
        errs.append("CI does not bracket point estimate")
    if cell["confidence"] != 0.8:
        errs.append("confidence must be 0.8")
    for key in ("resolutionDate",):
        try:
            datetime.strptime(cell[key], "%Y-%m-%d")
        except ValueError:
            errs.append(f"{key} not YYYY-MM-DD")
    try:
        run_at = datetime.fromisoformat(cell["runAt"].replace("Z", "+00:00"))
        if run_at > datetime.now(timezone.utc):
            errs.append("runAt is in the future")
        if run_at < datetime(2026, 6, 1, tzinfo=timezone.utc):
            errs.append("runAt predates the pipeline")
    except ValueError:
        errs.append("runAt not ISO-8601")
    if not str(cell["resolutionSourceUrl"]).startswith("https://"):
        errs.append("resolutionSourceUrl not https")
    if len(cell["historicalContext"]) < 3:
        errs.append("needs >=3 historical points")
    if len(cell["sourceContext"]) < 2:
        errs.append("needs >=2 source URLs")

    steps = cell["reasoning"]
    if len(steps) < 7:
        errs.append(f"only {len(steps)} reasoning steps (need >=7)")
    tools = [s for s in steps if s.get("kind") == "tool"]
    if len(tools) < 3:
        errs.append(f"only {len(tools)} tool steps (need >=3)")
    for t in tools:
        if not re.search(r"\d", str(t.get("result", ""))):
            errs.append(f"tool step without numeric result: {t.get('tool')}")
    if not any(s.get("kind") == "math" for s in steps):
        errs.append("no math step")
    last = steps[-1]
    if last.get("kind") != "forecast":
        errs.append("last step is not the forecast")
    elif (last.get("point"), last.get("ciLow"), last.get("ciHigh")) != (
        cell["pointEstimate"], cell["ciLow"], cell["ciHigh"],
    ):
        errs.append("forecast step numbers do not match cell numbers")
    return errs


def to_forecast_cell(cell: dict) -> dict:
    out = {k: cell[k] for k in (
        "slug", "country", "type", "title", "question", "unit",
        "pointEstimate", "ciLow", "ciHigh", "confidence", "resolutionDate",
        "resolutionSource", "resolutionSourceUrl", "resolutionRule",
        "dataPointId", "historicalContext", "drivers",
    )}
    if cell.get("conditionalOn"):
        out["conditionalOn"] = cell["conditionalOn"]
    out["predictionRun"] = {
        "kind": "recorded-agent-run",
        "runAt": cell["runAt"],
        "agent": cell.get("agent", "thesis.analyst.v2"),
        "model": cell.get("model", "claude-fable-5"),
        "sourceContext": cell["sourceContext"],
    }
    out["reasoning"] = cell["reasoning"]
    return out


def main() -> int:
    out_ts, const_name, *inputs = sys.argv[1:]
    site_data = pathlib.Path(__file__).resolve().parents[1] / "site/src/data"
    taken = existing_slugs(site_data)
    cells, failed = [], []
    seen = set()
    for path in inputs:
        for cell in json.load(open(path)):
            errs = validate(cell, taken | seen)
            if errs:
                failed.append((cell.get("slug", "?"), errs))
            else:
                seen.add(cell["slug"])
                cells.append(to_forecast_cell(cell))
    cells.sort(key=lambda c: c["resolutionDate"])

    body = ",\n".join(
        "  " + json.dumps(c, indent=2, ensure_ascii=False).replace("\n", "\n  ")
        for c in cells
    )
    header = (
        "// Generated by scripts/spawned_cells_to_ts.py from recorded\n"
        "// thesis.analyst agent runs. Every tool-step result was fetched from\n"
        "// the named source at predictionRun.runAt; regenerate, don't hand-edit.\n"
        'import type { ForecastCell } from "../forecast-cells";\n\n'
        f"export const {const_name}: ForecastCell[] = [\n{body},\n];\n"
    )
    pathlib.Path(out_ts).write_text(header)
    print(f"wrote {len(cells)} cells -> {out_ts}")
    for slug, errs in failed:
        print(f"REJECTED {slug}: {'; '.join(errs)}")
    return 1 if failed and not cells else 0


if __name__ == "__main__":
    sys.exit(main())
