#!/usr/bin/env python3
"""Assemble a thesis.analyst run prompt from a question spec, and emit the
version/hash metadata that prediction runs record.

Usage:
  # full prompt for an agent run
  python3 agents/thesis-analyst/build_prompt.py \
      --series bls.cps.unemployment_rate --period 2026-06 \
      [--conditional "axiom:reconciliation-2025/sec-71119 deadline in effect"]

  # just the version/hash metadata (used by spawned_cells_to_ts.py)
  python3 agents/thesis-analyst/build_prompt.py --metadata
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent

# Which skills attach for which series namespaces; calibration,
# resolution-rules always attach (the method is universal).
ALWAYS = ["calibration.md", "resolution-rules.md"]
DOMAIN = {
    r"^(bls|bea|census|fred|dol|fed)\.": ["us-data.md"],
    r"^(ons|boe|statcan|estat|eurostat|abs)\.": ["intl-data.md"],
    r"^(cms|medicaid)\.": ["cms-medicaid.md", "us-data.md"],
    r"^(treasury|fns|snap|ssa|irs)\.": ["treasury-fiscal.md", "us-data.md"],
    r"^(policyengine|pe)\.": ["policyengine.md"],
}
CONDITIONAL_SKILLS = ["policyengine.md", "axiom.md"]


def agent_meta() -> dict:
    yaml_text = (ROOT / "agent.yaml").read_text()
    version = re.search(r"^version:\s*(\S+)", yaml_text, re.M).group(1)
    model = re.search(r"^model:\s*(\S+)", yaml_text, re.M).group(1)
    prompt_hash = hashlib.sha256((ROOT / "system.md").read_bytes()).hexdigest()
    skills = sorted((ROOT / "skills").glob("*.md"))
    tool_policy = hashlib.sha256(
        b"".join(p.read_bytes() for p in skills)
    ).hexdigest()
    return {
        "agent": "thesis.analyst",
        "agentVersion": version,
        "model": model,
        "promptHash": prompt_hash,
        "toolPolicyHash": tool_policy,
        "skills": [p.name for p in skills],
    }


def select_skills(series: str, conditional: str | None) -> list[str]:
    names = list(ALWAYS)
    for pattern, skill_names in DOMAIN.items():
        if re.search(pattern, series):
            names += skill_names
    if conditional:
        names += CONDITIONAL_SKILLS
    if len(names) == len(ALWAYS):  # unknown namespace: attach both data skills
        names += ["us-data.md", "intl-data.md"]
    seen, ordered = set(), []
    for n in names:
        if n not in seen:
            seen.add(n)
            ordered.append(n)
    return ordered


def build(series: str, period: str, conditional: str | None) -> str:
    meta = agent_meta()
    parts = [
        (ROOT / "system.md").read_text(),
        "\n\n# Attached skills\n",
    ]
    for name in select_skills(series, conditional):
        parts.append(f"\n---\n{(ROOT / 'skills' / name).read_text()}")
    parts.append(
        "\n---\n# Question spec\n"
        f"- series: {series}\n- period: {period}\n"
        f"- conditional_on: {conditional or 'null'}\n\n"
        "Produce one JSON cell per docs/cell-contract.md. "
        f"(agent {meta['agent']} v{meta['agentVersion']}, "
        f"prompt {meta['promptHash'][:12]}, "
        f"tools {meta['toolPolicyHash'][:12]})\n"
    )
    return "".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--series")
    ap.add_argument("--period")
    ap.add_argument("--conditional")
    ap.add_argument("--metadata", action="store_true")
    args = ap.parse_args()
    if args.metadata:
        print(json.dumps(agent_meta(), indent=1))
        return 0
    if not (args.series and args.period):
        ap.error("--series and --period required (or --metadata)")
    print(build(args.series, args.period, args.conditional))
    return 0


if __name__ == "__main__":
    sys.exit(main())
