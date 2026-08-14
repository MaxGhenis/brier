#!/usr/bin/env python3
"""Normalize spawn-agent JSON variants into the cell contract's step schema.

Agents occasionally drift on the reasoning-step shape. This maps the two
observed variants onto the contract (docs/cell-contract.md) WITHOUT inventing
content: tool/fetch steps keep their full detail as the result, the first
sentence doubles as the call description, and the final step is replaced by
the canonical forecast triple the cell already asserts.

Usage: normalize_spawn_json.py IN.json OUT.json
"""

from __future__ import annotations

import json
import re
import sys

# step types that represent a data retrieval → kind: tool
FETCH_TYPES = {"tool", "data_fetch", "cross_check", "external_anchor"}
# quantitative derivation steps → kind: math
MATH_TYPES = {
    "math",
    "volatility",
    "momentum",
    "synthesis",
    "mean_reversion",
    "seasonality",
    "trend_adjustment",
}
TEXT_TYPES = {
    "text",
    "heading",
    "base_rate",
    "counter_consideration",
    "reference-class",
    "reference_class",
}


CANON_STEP_KEYS = {
    "heading": ("kind", "text"),
    "text": ("kind", "text"),
    "math": ("kind", "text"),
    "tool": ("kind", "tool", "call", "result"),
    "forecast": ("kind", "point", "ciLow", "ciHigh"),
}


def norm_steps(cell: dict) -> list[dict]:
    out = []
    for s in cell["reasoning"]:
        if s.get("kind") in CANON_STEP_KEYS:
            # Contract-shaped kind, but agents decorate steps with extra
            # fields (a forecast step carrying commentary text broke the
            # typed publish build); keep only the contract's keys.
            allowed = CANON_STEP_KEYS[s["kind"]]
            out.append({k: s[k] for k in allowed if k in s})
            continue
        t = s.get("type") or s.get("kind") or "text"
        detail = s.get("detail", "")
        if t in FETCH_TYPES:
            dot = detail.find(". ")
            call = detail[: dot + 1] if dot > 0 else detail[:140]
            out.append(
                {
                    "kind": "tool",
                    "tool": s.get("tool", "data.fetch"),
                    "call": call if isinstance(call, str) else "data.fetch",
                    "result": detail,
                }
            )
        elif t in ("forecast", "final"):
            out.append(
                {
                    "kind": "forecast",
                    "point": cell["pointEstimate"],
                    "ciLow": cell["ciLow"],
                    "ciHigh": cell["ciHigh"],
                }
            )
        elif t in MATH_TYPES:
            out.append({"kind": "math", "text": detail})
        else:
            out.append(
                {"kind": "heading" if t == "heading" else "text", "text": detail}
            )
    return out


def parse_history_sentence(s: str) -> dict | None:
    """Extract {label, value} from prose like 'Nov 2025: 3.5%.' or
    'Bank Rate held at 3.75% on 19 March 2026 (...)'. Returns None if no
    confident match."""
    import re

    m = re.search(r"([A-Z][a-z]{2,9}\.? 20\d\d)\s*:?\s*(-?\d+(?:\.\d+)?)\s*%", s)
    if m:
        return {"label": m.group(1), "value": float(m.group(2))}
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*%\s+on\s+(\d{1,2} [A-Z][a-z]{2,9} 20\d\d)", s)
    if m:
        return {"label": m.group(2), "value": float(m.group(1))}
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*%\s+in\s+([A-Z][a-z]{2,9} 20\d\d)", s)
    if m:
        return {"label": m.group(2), "value": float(m.group(1))}
    return None


def to_number(value):
    if isinstance(value, (int, float)):
        return value
    s = str(value).strip().replace(",", "").replace("%", "")
    s = re.sub(r"\s*(thousand|thousands|million|millions|k)$", "", s, flags=re.I)
    if s.lower().endswith("k"):
        s = s[:-1]
    try:
        return round(float(s), 6)
    except ValueError:
        return None


def scrub_signed_zeros(value):
    """Recursively map IEEE -0.0 to +0.0 across a parsed JSON payload.

    Python's json keeps the sign ("-0.0") while JavaScript's JSON.stringify
    drops it ("0"), so a signed zero anywhere in a sealed cell splits the
    Python-written sidecars from the regenerated TS surfaces.
    """
    if isinstance(value, float):
        return value + 0.0
    if isinstance(value, dict):
        return {key: scrub_signed_zeros(item) for key, item in value.items()}
    if isinstance(value, list):
        return [scrub_signed_zeros(item) for item in value]
    return value


def main() -> int:
    cells = scrub_signed_zeros(json.load(open(sys.argv[1])))
    if not isinstance(cells, list) or not all(isinstance(c, dict) for c in cells):
        print(
            "REFUSING: spawn output is not a list of cell objects "
            f"(got {type(cells).__name__})",
            file=sys.stderr,
        )
        return 1
    # A schema-incomplete draft must become a diagnosable refusal, not a
    # KeyError traceback: the 2026-08-03 auto-roll recorded ok:false with
    # EMPTY validationErrors because a draft lacking `reasoning` crashed
    # this script before any check could name the gap.
    problems = []
    for index, c in enumerate(cells):
        missing = [key for key in ("reasoning", "historicalContext") if key not in c]
        if missing:
            problems.append(
                f"cell {index} ({c.get('dataPointId', 'no dataPointId')}) "
                f"missing required keys: {', '.join(missing)}"
            )
        else:
            for key in ("reasoning", "historicalContext"):
                if not isinstance(c[key], list):
                    problems.append(
                        f"cell {index} ({c.get('dataPointId', 'no dataPointId')}) "
                        f"{key} is {type(c[key]).__name__}, not a list"
                    )
    if problems:
        for line in problems:
            print(f"REFUSING: {line}", file=sys.stderr)
        return 1
    for c in cells:
        c["reasoning"] = norm_steps(c)
        c["sourceContext"] = [
            u if isinstance(u, str) else (u.get("url") or u.get("href") or "")
            for u in c.get("sourceContext", [])
        ]
        c["sourceContext"] = [u for u in c["sourceContext"] if u]
        rows = []
        for h in c["historicalContext"]:
            if isinstance(h, str):
                parsed = parse_history_sentence(h)
                if parsed:
                    rows.append(parsed)
            elif (v := to_number(h.get("value"))) is not None:
                row = {
                    "label": h.get("label") or str(h.get("period", "?")),
                    "value": v,
                }
                if "period" in h:
                    # Preserve the model's structured identity verbatim. The
                    # shared validator owns canonical-shape checks; this
                    # normalizer must neither discard nor infer authority.
                    row["period"] = h["period"]
                rows.append(row)
        c["historicalContext"] = rows
    json.dump(cells, open(sys.argv[2], "w"), indent=1)
    print(f"normalized {len(cells)} cells -> {sys.argv[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
