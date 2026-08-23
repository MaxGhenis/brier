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
POLICY_CONTRACT_START = "For fast and full conditional runs, one reasoning step"
POLICY_CONTRACT_END = "Base-rate provenance: fetch `historicalContext`"
LEGACY_2_5_11_POLICY_CONTRACT = """For fast and full conditional runs, one reasoning \
step beginning exactly
`Policy chain:` must decompose the touched population (with a fetched count),
propagation to the measured quantity, offsetting responses, and timing/lag.
The pre-submit reviewer checks those four components and whether the policy
effect's direction and size are consistent with its cited precedent. The
runner's literal evidence gate is specified below.

Machine-checked requirements (CI-validated literally, not approximately;
a trace missing any is rejected):

- the base-rate step must use explicit reference-class wording — literally
  say "base rate" or "reference class", or a trailing-N range/
  distribution statement;
- the falsification step must use one of the literal phrasings
  "upside risk", "downside risk", "outside the interval", or
  "would land above/below the interval";
- fast and full conditional cells must include a reasoning step whose text
  begins exactly `Policy chain:` and either cites at least one fetched
  precedent URL that also appears exactly in `sourceContext`, or contains the
  exact phrase `no fetched precedent`, states a numeric policy-term bound, and
  labels that term `low-confidence`. The runner applies this gate only to
  fast/full runs; the dispatch-only `ladder` and `ladder_v2` contracts and
  validators remain sealed;
- one math step must begin "Prior/update/interval:" and SHOW the interval
  arithmetic: compute sigma from the fetched history (successive changes
  for level/rate series; the values themselves for change/flow series),
  state it literally as "sigma = X", and derive the half-width as roughly
  1.28*sigma — stating a regime or mechanism reason in the same step if
  you widen or narrow beyond about 0.75x–1.75x of that;
- confidence is 0.8 exactly; ciLow < pointEstimate < ciHigh;
- every tool step's result string includes at least one fetched numeric
  value; resolutionDate follows the applicable calendar/default or bounded
  branch above and is never inferred from cadence; runAt is the actual UTC
  date command output from this run.

"""


def agent_meta() -> dict:
    yaml_text = (ROOT / "agent.yaml").read_text()
    version = re.search(r"^version:\s*(\S+)", yaml_text, re.M).group(1)
    model = re.search(r"^model:\s*(\S+)", yaml_text, re.M).group(1)
    prompt_hash = hashlib.sha256((ROOT / "system.md").read_bytes()).hexdigest()
    skills = sorted((ROOT / "skills").glob("*.md"))
    tool_policy = hashlib.sha256(b"".join(p.read_bytes() for p in skills)).hexdigest()
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


def contract_for_prompt(
    conditional: str | None,
    *,
    contract_override: str | None = None,
    legacy_policy_chain: bool = False,
) -> str:
    """Select current conditional bytes or the frozen 2.5.11 projection."""

    if contract_override is not None:
        return contract_override
    contract = (ROOT.parent.parent / "docs" / "cell-contract.md").read_text()
    if conditional and not legacy_policy_chain:
        return contract
    try:
        start = contract.index(POLICY_CONTRACT_START)
        end = contract.index(POLICY_CONTRACT_END, start)
    except ValueError as exc:
        raise RuntimeError(
            "cell contract policy-chain section anchors are missing"
        ) from exc
    return contract[:start] + LEGACY_2_5_11_POLICY_CONTRACT + contract[end:]


def build(
    series: str,
    period: str,
    conditional: str | None,
    *,
    contract_override: str | None = None,
    legacy_policy_chain: bool = False,
) -> str:
    meta = agent_meta()
    parts = [
        (ROOT / "system.md").read_text(),
        "\n\n# Attached skills\n",
    ]
    for name in select_skills(series, conditional):
        parts.append(f"\n---\n{(ROOT / 'skills' / name).read_text()}")
    # The selected cell contract is embedded verbatim, not referenced: four CI waves
    # on 2026-08-03 produced substantively sound drafts with invented field
    # names (catalogSlug, pointEstimate, a snake-case conditional key)
    # because the schema lived behind a "per docs/cell-contract.md" pointer that only
    # repo-reading local runs actually followed (thesis#115). The contract
    # file stays the current source of truth. Unconditional 2.5.11 prompts use
    # the pre-policy-chain projection so conditional-only contract changes do
    # not silently alter their bytes; attested replay may supply the exact
    # contract from its authenticated historical checkout.
    contract = contract_for_prompt(
        conditional,
        contract_override=contract_override,
        legacy_policy_chain=legacy_policy_chain,
    )
    conditional_block = (
        "- conditionalOn: null\n"
        if not conditional
        else (
            f"- conditionalOn: {conditional}\n"
            "  The published cell's `conditionalOn` field must repeat the\n"
            "  text above byte-for-byte — the registry gates on the exact\n"
            "  string, and any paraphrase fails validation.\n"
        )
    )
    parts.append(
        "\n---\n# Cell contract (verbatim — your output must use exactly "
        "these field names)\n"
        f"{contract}\n"
        "\n---\n# Question spec\n"
        f"- series: {series}\n- period: {period}\n"
        f"{conditional_block}\n"
        "Produce one JSON cell per the contract above. "
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
