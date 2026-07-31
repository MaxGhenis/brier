"""Re-parse stored model responses with a corrected prose parser.

WHY THIS EXISTS. The first parser extracted any number above 1,000 from prose
and looked for a bracketing triple. Applied to forecasts of SNAP recipient
counts (1.3-5.4 million), that happily accepted a YEAR — "mid-2021", "December
2023" — as a point estimate. 183 of 265 parsed free-text runs came back with a
point in [1900, 2100].

That is not a model failure, it is a harness failure, and it is not random: it
fires only on prose, which is one of the levels of a measured dimension
(elicitation format). Left in place it would have made free text look
catastrophically worse than JSON for reasons having nothing to do with
elicitation — manufacturing the exact kind of artefact this experiment exists
to detect.

Because every response was stored, the correction is offline: no model is
re-called and no run is discarded. Original parses are preserved as
`forecast_v1` so the correction is auditable.

The scale band is deliberately a SCALE filter, not an accuracy filter: it
rejects "2023" against a series in the millions, and accepts any forecast
within a factor of five of the last observed value in either direction. A model
that forecast a 3x collapse would still be parsed, and scored badly on merit.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Optional

HERE = Path(__file__).parent

SCALE_WORDS = {
    "million": 1e6, "millions": 1e6, "m": 1e6,
    "thousand": 1e3, "thousands": 1e3, "k": 1e3,
    "billion": 1e9, "billions": 1e9,
}

# number, optionally followed by a scale word
NUM_RE = re.compile(
    r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*(million|millions|thousand|thousands|billion|billions)?\b",
    re.I,
)

POINT_CUES = re.compile(
    r"(estimate|forecast|central|point|expect|project|approximately|about|around|will be)",
    re.I,
)
INTERVAL_CUES = re.compile(
    r"(80%|80 percent|credible interval|confidence interval|interval|range|between|from)",
    re.I,
)


def extract_candidates(text: str, anchor: float) -> list[tuple[float, int]]:
    """Return [(value, char_offset)] of numbers plausibly on the series' scale.

    `anchor` is the last observed value in the unit's own supplied history.
    """
    lo, hi = anchor * 0.2, anchor * 5.0
    out: list[tuple[float, int]] = []
    for m in NUM_RE.finditer(text):
        raw, scale = m.group(1), (m.group(2) or "").lower()
        try:
            val = float(raw.replace(",", ""))
        except ValueError:
            continue
        if scale:
            val *= SCALE_WORDS[scale]
        elif 1900 <= val <= 2100 and float(val).is_integer() and "," not in raw:
            # bare four-digit integer with no scale word: a year, not a count
            continue
        if lo <= val <= hi:
            out.append((val, m.start()))
    return out


def parse_prose(text: str, anchor: float) -> dict:
    cands = extract_candidates(text, anchor)
    if not cands:
        return {"parse_error": "no_scale_candidates", "parse_mode": "failed_v2"}

    values = [v for v, _ in cands]
    uniq = sorted(set(values))

    # Preferred shape: a point followed by a bracketing low/high pair.
    for i in range(len(cands) - 2):
        a, b, c = cands[i][0], cands[i + 1][0], cands[i + 2][0]
        if b < a < c or c < a < b:
            lo, hi = sorted((b, c))
            return {"point": a, "ci_low": lo, "ci_high": hi, "parse_mode": "prose_bracketed_v2"}
        if a < b < c:
            return {"point": b, "ci_low": a, "ci_high": c, "parse_mode": "prose_ordered_v2"}

    if len(uniq) >= 3:
        lo, mid, hi = uniq[0], uniq[len(uniq) // 2], uniq[-1]
        return {"point": mid, "ci_low": lo, "ci_high": hi, "parse_mode": "prose_spread_v2"}
    if len(uniq) == 2:
        lo, hi = uniq
        return {"point": (lo + hi) / 2, "ci_low": lo, "ci_high": hi,
                "parse_mode": "prose_pair_v2"}
    return {"parse_error": "single_value_no_interval", "point_candidate": uniq[0],
            "parse_mode": "failed_v2"}


def _first_json(text: str) -> Optional[dict]:
    blobs, depth, start, in_str, esc = [], 0, -1, False, False
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start >= 0:
                blobs.append(text[start:i + 1])
    for blob in reversed(blobs):
        try:
            obj = json.loads(blob)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "point" in obj:
            return obj
    return None


def _num(raw) -> Optional[float]:
    if isinstance(raw, (int, float)):
        return float(raw)
    if not isinstance(raw, str):
        return None
    s = raw.strip().lower().replace("$", "").replace(",", "").replace("persons", "").strip()
    mult = 1.0
    for suffix, factor in SCALE_WORDS.items():
        if s.endswith(" " + suffix) or s.endswith(suffix) and not s[:-len(suffix)].strip().endswith("e"):
            cut = s[: -len(suffix)].strip()
            try:
                float(cut)
            except ValueError:
                continue
            s, mult = cut, factor
            break
    try:
        return float(s) * mult
    except ValueError:
        return None


def reparse_one(text: str, anchor: float) -> dict:
    obj = _first_json(text)
    if obj is not None:
        p, lo, hi = _num(obj.get("point")), _num(obj.get("ci_low")), _num(obj.get("ci_high"))
        if p is not None and lo is not None and hi is not None:
            if lo > hi:
                lo, hi = hi, lo
            out = {"point": p, "ci_low": lo, "ci_high": hi, "parse_mode": "json_v2"}
            if "bin" in obj:
                out["bin"] = obj["bin"]
            return out
    return parse_prose(text, anchor)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=Path, default=HERE / "runs_api.jsonl")
    ap.add_argument("--ground-truth", type=Path, default=HERE / "ground_truth.json")
    ap.add_argument("--out", type=Path, default=HERE / "runs_api.reparsed.jsonl")
    args = ap.parse_args()

    gt = {u["unit_id"]: u for u in json.loads(args.ground_truth.read_text())}
    anchors = {uid: u["history"][-1]["value"] for uid, u in gt.items() if u.get("history")}

    stats = {"total": 0, "changed": 0, "was_year": 0, "now_ok": 0, "still_failed": 0,
             "rescued": 0, "lost": 0}
    by_elic: dict[str, dict[str, int]] = {}

    with args.out.open("w") as fh:
        for line in args.runs.read_text().splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            stats["total"] += 1
            elic = rec.get("config", {}).get("elicitation", "?")
            b = by_elic.setdefault(elic, {"n": 0, "v1_ok": 0, "v2_ok": 0, "year_v1": 0})
            b["n"] += 1

            old = rec.get("forecast") or {}
            if old.get("point") is not None:
                b["v1_ok"] += 1
                if 1900 <= old["point"] <= 2100:
                    stats["was_year"] += 1
                    b["year_v1"] += 1

            text = rec.get("final_text") or ""
            anchor = anchors.get(rec.get("unit_id"))
            if text and anchor:
                new = reparse_one(text, anchor)
            else:
                new = {"parse_error": "no_text_or_anchor", "parse_mode": "failed_v2"}

            rec["forecast_v1"] = old
            rec["forecast"] = new
            if new.get("point") is not None:
                b["v2_ok"] += 1
                stats["now_ok"] += 1
                if old.get("point") is None:
                    stats["rescued"] += 1
            else:
                stats["still_failed"] += 1
                if old.get("point") is not None:
                    stats["lost"] += 1
            if old.get("point") != new.get("point"):
                stats["changed"] += 1
            fh.write(json.dumps(rec) + "\n")

    print(json.dumps(stats, indent=2))
    print("\nby elicitation:")
    for k, v in sorted(by_elic.items()):
        print(f"  {k:20s} n={v['n']:5d} v1_parsed={v['v1_ok']:5d} "
              f"(year-shaped {v['year_v1']:4d})  v2_parsed={v['v2_ok']:5d}")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
