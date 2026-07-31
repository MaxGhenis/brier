"""Ablation harness for bill-conditioned forecasting (Leg B).

Design is frozen in PREREGISTRATION.md. This module only *runs* the grid; it
holds no analysis logic and it does not modify any existing repo scoring code.

Every configuration dimension is a pure function of the config dict, so a run
record is fully reproducible from (unit, config, seed) plus the frozen corpus.
"""
from __future__ import annotations

import json
import os
import random
import re
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Optional

HERE = Path(__file__).parent
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
TRANSPORT = "anthropic_api"

# ---------------------------------------------------------------------------
# transport
# ---------------------------------------------------------------------------


def _load_anthropic_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    env = Path.home() / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("ANTHROPIC_API_KEY"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("ANTHROPIC_API_KEY not found in env or ~/.env")


_KEY: Optional[str] = None
_KEY_LOCK = threading.Lock()


def _key() -> str:
    global _KEY
    with _KEY_LOCK:
        if _KEY is None:
            _KEY = _load_anthropic_key()
    return _KEY


@dataclass
class CallResult:
    text: str
    ok: bool
    duration_s: float
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    error: Optional[str] = None


def call_model(
    prompt: str,
    model: str,
    temperature: float = 1.0,
    max_tokens: int = 2000,
    timeout: float = 180.0,
    retries: int = 4,
) -> CallResult:
    """One completion through the Anthropic Messages API. Errors returned, not raised."""
    body = json.dumps(
        {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode()
    start = time.time()
    last = ""
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                ANTHROPIC_URL,
                data=body,
                headers={
                    "x-api-key": _key(),
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                payload = json.loads(r.read().decode())
            blocks = payload.get("content") or []
            text = "".join(b.get("text", "") for b in blocks if b.get("type") == "text")
            usage = payload.get("usage") or {}
            return CallResult(
                text=text,
                ok=True,
                duration_s=time.time() - start,
                prompt_tokens=usage.get("input_tokens"),
                completion_tokens=usage.get("output_tokens"),
            )
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode()[:300]
            except Exception:  # noqa: BLE001
                pass
            last = f"HTTP {e.code}: {detail}"
            if e.code in (400, 401, 403, 404):
                break
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
        time.sleep(min(2.0 * (2**attempt), 20.0) * (0.5 + random.random()))
    return CallResult(text="", ok=False, duration_s=time.time() - start, error=last)


# ---------------------------------------------------------------------------
# D5 — magnitude perturbation (contamination arm)
# ---------------------------------------------------------------------------

MAGNITUDE_SUBSTITUTIONS = {
    "actual": [],
    # Age caps pushed far DOWN: many more adults become subject to the work
    # requirement, so participation should fall much harder.
    "severe": [
        ("over 51 years of age", "over 31 years of age"),
        ("over 53 years of age", "over 33 years of age"),
        ("over 55 years of age", "over 35 years of age"),
    ],
    # Age caps pushed far UP: almost nobody is newly subject, so the provision
    # should be close to inert.
    "inert": [
        ("over 51 years of age", "over 71 years of age"),
        ("over 53 years of age", "over 73 years of age"),
        ("over 55 years of age", "over 75 years of age"),
    ],
}


def apply_magnitude(text: str, magnitude: str) -> tuple[str, int]:
    subs = MAGNITUDE_SUBSTITUTIONS[magnitude]
    n = 0
    for old, new in subs:
        text, k = re.subn(re.escape(old), new, text)
        n += k
    return text, n


# ---------------------------------------------------------------------------
# D1 — policy context
# ---------------------------------------------------------------------------

OPERATIONAL_SUMMARY = (
    "A federal statute enacted on 3 June 2023 modifies the work-requirement "
    "rules for the Supplemental Nutrition Assistance Program. It raises the "
    "upper age bound of the age-based exemption from the able-bodied-adults-"
    "without-dependents time limit in annual steps over fiscal years 2023-2025, "
    "adds categorical exemptions for homeless individuals, veterans, and people "
    "aged 24 or under who were in foster care at 18, and reduces the share of "
    "its caseload a state may exempt at discretion. The new exemption rules "
    "apply to applications for initial certification or recertification "
    "received starting 90 days after enactment."
)


def build_policy_context(provisions: dict[str, str], level: str, magnitude: str) -> tuple[str, dict]:
    """Return (context_block, provenance) for a D1 level."""
    meta = {"level": level, "magnitude": magnitude, "substitutions": 0}
    if level == "none":
        return "", meta
    if level == "summary":
        return (
            "POLICY CONTEXT (operational description):\n" + OPERATIONAL_SUMMARY,
            meta,
        )

    operative_keys = ["sec311_operative", "sec312_operative", "sec314_transparency"]
    purpose_keys = ["sec313_purpose"]
    if level == "operative_only":
        keys = operative_keys
    elif level == "purpose_only":
        keys = purpose_keys
    elif level == "operative_plus_purpose":
        keys = operative_keys + purpose_keys
    else:
        raise ValueError(f"unknown policy_context level: {level}")

    parts = []
    total_subs = 0
    for k in keys:
        text = provisions[k]
        if k == "sec311_operative":
            text, n = apply_magnitude(text, magnitude)
            total_subs += n
        parts.append(text)
    meta["substitutions"] = total_subs
    meta["provisions"] = keys
    header = (
        "POLICY CONTEXT (verbatim statutory text, Fiscal Responsibility Act of "
        "2023, Pub. L. 118-5, enacted 3 June 2023):"
    )
    return header + "\n\n" + "\n\n".join(parts), meta


# ---------------------------------------------------------------------------
# D2 — elicitation format
# ---------------------------------------------------------------------------

BASE_TASK = """You are forecasting a US public-benefit program indicator.

TARGET
  Series: monthly count of SNAP (Supplemental Nutrition Assistance Program) recipients in {state_name} ({state}).
  Units: persons.
  Target month: {target_month_label}.

WHAT YOU KNOW
  The published history of this series, as it stood at the forecast origin, is
  given below. Nothing after the last row was available at the origin.
  Forecast origin: {origin_label}.

HISTORY (month, persons)
{history_block}
"""

ELICITATION_INSTRUCTIONS = {
    "point_ci_json": """Give your forecast for the target month.

Respond with ONLY a JSON object, no prose before or after:
{"point": <number of persons>, "ci_low": <number>, "ci_high": <number>, "rationale": "<one sentence>"}
where [ci_low, ci_high] is your 80% central credible interval.""",
    "free_text": """Give your forecast for the target month in plain prose. State your
central estimate and your 80% credible interval explicitly, in persons. Do not
use JSON, bullet points, or headings — write it as a short paragraph.""",
    "cot_then_json": """Think through the forecast step by step first: establish the base rate from
the history, note the trend and seasonality, then consider any adjustment.
Write your reasoning, then on the FINAL line emit only a JSON object:
{"point": <number of persons>, "ci_low": <number>, "ci_high": <number>, "rationale": "<one sentence>"}
where [ci_low, ci_high] is your 80% central credible interval.""",
    "forced_choice_bins": """Choose exactly one bin for the target month's value, and give an 80% interval
consistent with your choice.

BINS (persons, relative to the last observed value L in the history):
  A: below 0.90 x L
  B: 0.90 x L to 0.95 x L
  C: 0.95 x L to 1.00 x L
  D: 1.00 x L to 1.05 x L
  E: 1.05 x L to 1.10 x L
  F: above 1.10 x L

Respond with ONLY a JSON object:
{"bin": "<A-F>", "point": <number of persons>, "ci_low": <number>, "ci_high": <number>, "rationale": "<one sentence>"}""",
}

STATE_NAMES = {
    "CA": "California", "FL": "Florida", "NY": "New York",
    "TX": "Texas", "PA": "Pennsylvania", "OH": "Ohio",
}

MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]


def month_label(iso: str) -> str:
    y, m, _ = iso.split("-")
    return f"{MONTH_NAMES[int(m) - 1]} {y}"


def format_history(history: list[dict], max_rows: int = 60) -> str:
    rows = history[-max_rows:]
    return "\n".join(f"  {r['month'][:7]}  {int(r['value']):,}" for r in rows)


def build_prompt(unit: dict, provisions: dict, config: dict) -> tuple[str, dict]:
    ctx, ctx_meta = build_policy_context(
        provisions, config["policy_context"], config.get("magnitude", "actual")
    )
    base = BASE_TASK.format(
        state=unit["state"],
        state_name=STATE_NAMES[unit["state"]],
        target_month_label=month_label(unit["target_month"]),
        origin_label=month_label(unit["origin_vintage"]),
        history_block=format_history(unit["history"]),
    )
    parts = [base]
    if ctx:
        parts.append(ctx)
    parts.append(ELICITATION_INSTRUCTIONS[config["elicitation"]])
    return "\n\n".join(parts), ctx_meta


# ---------------------------------------------------------------------------
# parsing
# ---------------------------------------------------------------------------


def _first_json_object(text: str) -> Optional[dict]:
    """Extract the last balanced top-level JSON object in the text."""
    candidates = []
    depth = 0
    start = -1
    in_str = False
    esc = False
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
                candidates.append(text[start : i + 1])
    for blob in reversed(candidates):
        try:
            obj = json.loads(blob)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "point" in obj:
            return obj
    return None


_NUM = r"[-+]?\$?\s*\d[\d,]*(?:\.\d+)?\s*(?:million|thousand|billion|m|k)?"


def _to_float(raw: Any) -> Optional[float]:
    if isinstance(raw, (int, float)):
        return float(raw)
    if not isinstance(raw, str):
        return None
    s = raw.strip().lower().replace("$", "").replace(",", "").replace("persons", "").strip()
    mult = 1.0
    for suffix, factor in (("billion", 1e9), ("million", 1e6), ("thousand", 1e3), ("m", 1e6), ("k", 1e3)):
        if s.endswith(suffix):
            s = s[: -len(suffix)].strip()
            mult = factor
            break
    try:
        return float(s) * mult
    except ValueError:
        return None


def parse_forecast(text: str, elicitation: str) -> dict:
    """Return {point, ci_low, ci_high, parse_mode} or {'parse_error': ...}."""
    obj = _first_json_object(text)
    if obj is not None:
        point = _to_float(obj.get("point"))
        lo = _to_float(obj.get("ci_low"))
        hi = _to_float(obj.get("ci_high"))
        if point is not None and lo is not None and hi is not None:
            if lo > hi:
                lo, hi = hi, lo
            out = {"point": point, "ci_low": lo, "ci_high": hi, "parse_mode": "json"}
            if "bin" in obj:
                out["bin"] = obj.get("bin")
            return out

    # free-text fallback: central estimate + interval
    nums = [
        _to_float(m.group(0))
        for m in re.finditer(_NUM, text.replace("\n", " "), re.I)
    ]
    nums = [n for n in nums if n is not None and n > 1000]
    if len(nums) >= 3:
        # heuristic: an 80% interval brackets the point estimate
        for i in range(len(nums) - 2):
            a, b, c = nums[i], nums[i + 1], nums[i + 2]
            if b <= a <= c or c <= a <= b:
                lo, hi = sorted((b, c))
                return {"point": a, "ci_low": lo, "ci_high": hi, "parse_mode": "prose_triple"}
            if a <= b <= c:
                return {"point": b, "ci_low": a, "ci_high": c, "parse_mode": "prose_ordered"}
    if nums:
        return {"parse_error": "no_interval", "point_candidate": nums[0], "parse_mode": "failed"}
    return {"parse_error": "no_numbers", "parse_mode": "failed"}


# ---------------------------------------------------------------------------
# D3 — pipeline
# ---------------------------------------------------------------------------

SKEPTIC_TEMPLATE = """Below is a forecasting task and a draft forecast produced by another analyst.

=== TASK ===
{prompt}

=== DRAFT FORECAST ===
{draft}

You are the SKEPTIC. Your job is to attack this forecast. Identify, specifically:
- any number asserted that the history does not support;
- any claim about the policy that is not supported verbatim by the text supplied
  (quote the text you are relying on, or say the claim is unsupported);
- whether the interval is too narrow for the stated horizon.
Be concrete and brief. Do not produce your own forecast."""

VERIFIER_TEMPLATE = """You are the VERIFIER. Below is a forecasting task, a draft forecast, and a
skeptic's critique.

=== TASK ===
{prompt}

=== DRAFT FORECAST ===
{draft}

=== SKEPTIC ===
{critique}

For each of the skeptic's points, state whether it is CORRECT or INCORRECT and
why, checking against the history and the supplied policy text only. Be brief."""

JUDGE_TEMPLATE = """You are the JUDGE. Below is a forecasting task, a draft forecast, a skeptic's
critique, and a verifier's assessment.

=== TASK ===
{prompt}

=== DRAFT ===
{draft}

=== SKEPTIC ===
{critique}

=== VERIFIER ===
{verification}

Produce the final forecast. Respond with ONLY a JSON object, no prose:
{{"point": <number of persons>, "ci_low": <number>, "ci_high": <number>, "rationale": "<one sentence>"}}
where [ci_low, ci_high] is your 80% central credible interval."""


def run_single(unit: dict, provisions: dict, config: dict) -> dict:
    prompt, ctx_meta = build_prompt(unit, provisions, config)
    model = config["model"]
    temp = config.get("temperature", 1.0)
    record: dict[str, Any] = {
        "unit_id": unit["unit_id"],
        "config": dict(config),
        "context_meta": ctx_meta,
        "prompt_chars": len(prompt),
        "calls": [],
    }

    # Caps raised 2026-07-31 14:05 EDT after 5/1753 runs truncated exactly at the
    # cap and lost their JSON. Truncation correlated with elicitation verbosity —
    # i.e. with a measured dimension — so it was a confound, not just data loss.
    max_tokens = 6000 if config["elicitation"] == "cot_then_json" else 4000
    first = call_model(prompt, model, temperature=temp, max_tokens=max_tokens)
    record["calls"].append(
        {"role": "draft", "ok": first.ok, "duration_s": round(first.duration_s, 2),
         "prompt_tokens": first.prompt_tokens, "completion_tokens": first.completion_tokens,
         "error": first.error}
    )
    if not first.ok:
        record["error"] = first.error
        return record
    record["draft_text"] = first.text

    if config["pipeline"] == "single_pass":
        record["final_text"] = first.text
        record["forecast"] = parse_forecast(first.text, config["elicitation"])
        return record

    # debate
    critique = call_model(
        SKEPTIC_TEMPLATE.format(prompt=prompt, draft=first.text),
        model, temperature=temp, max_tokens=2500,
    )
    record["calls"].append({"role": "skeptic", "ok": critique.ok,
                            "duration_s": round(critique.duration_s, 2),
                            "completion_tokens": critique.completion_tokens,
                            "error": critique.error})
    if not critique.ok:
        record["error"] = f"skeptic: {critique.error}"
        return record

    verification = call_model(
        VERIFIER_TEMPLATE.format(prompt=prompt, draft=first.text, critique=critique.text),
        model, temperature=temp, max_tokens=2500,
    )
    record["calls"].append({"role": "verifier", "ok": verification.ok,
                            "duration_s": round(verification.duration_s, 2),
                            "completion_tokens": verification.completion_tokens,
                            "error": verification.error})
    if not verification.ok:
        record["error"] = f"verifier: {verification.error}"
        return record

    judged = call_model(
        JUDGE_TEMPLATE.format(prompt=prompt, draft=first.text,
                              critique=critique.text, verification=verification.text),
        model, temperature=temp, max_tokens=2500,
    )
    record["calls"].append({"role": "judge", "ok": judged.ok,
                            "duration_s": round(judged.duration_s, 2),
                            "completion_tokens": judged.completion_tokens,
                            "error": judged.error})
    if not judged.ok:
        record["error"] = f"judge: {judged.error}"
        return record

    record["skeptic_text"] = critique.text
    record["verifier_text"] = verification.text
    record["final_text"] = judged.text
    record["forecast"] = parse_forecast(judged.text, "point_ci_json")
    return record
