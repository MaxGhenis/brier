# RESULTS — Harness sensitivity of bill-conditioned forecasts

**2026-07-31, Hacking the Think Tank II (FAI/IFP, Washington DC).**
David Gringras. Design frozen in [`PREREGISTRATION.md`](PREREGISTRATION.md),
committed at 11:38 EDT — **before the first model call** (commit `f95c4b6c`).

Canonical analysis outputs: [`results/`](results/). Figure for the demo:
[`results/demo_dispersion.png`](results/demo_dispersion.png).

---

## Scope, stated once and plainly

This covers **Leg B only — the conditional forecast**. The extraction leg (did
the tool read the bill correctly) is owned by other team members and is not
scored here. The two are never merged into one accuracy number.

**N = 12 units, one policy event, one program, 2520 runs.** Every number below
is conditional on that. Nothing here generalises to other programs or other
bills without a further corpus.

---

## What was tested

**Policy event.** Fiscal Responsibility Act of 2023, Pub. L. 118-5, §§311–314
(SNAP work requirements), enacted 2023-06-03. Verbatim text from govinfo
`PLAW-118publ5`, sliced into [`provisions.json`](provisions.json) with SHA-256
prefixes recorded in the preregistration. §311 raises the ABAWD age-exemption
ceiling in annual steps (FY2023 over 51, FY2024 over 53, FY2025+ over 55) and
adds exemptions for homeless individuals, veterans and former foster youth ≤24;
§312 cuts the state discretionary exemption pool to 8%; §313 is a **pure
statement-of-purpose amendment** — a real preamble in the same title as the
operative restriction, which is what makes the stated-purpose test genuine
rather than synthetic.

**Indicator.** State monthly SNAP recipients (Census/USDA-FNS series
`BR<ST><FIPS>M647NCEN`) for CA, FL, NY, TX, PA, OH, at target months 2023-12
and 2024-03 — 3 and 6 months after the §311 phase-in.

**Ground truth.** First prints only, discovered empirically by walking ALFRED
vintages forward and taking the earliest carrying a non-missing value. All 12
resolved at vintage 2026-02-01; **revision from first print to today is 0.0 for
every unit**. Frozen in [`ground_truth.json`](ground_truth.json) before any
model ran. ALFRED is used strictly as a history mirror, per AGENTS.md — it is
not presented as a resolution source of record.

**Scoring.** The house rule, not a substitute: point + 80% interval → the
existing `interval_anchor_v1` transform (`scripts/run_thesis_analyst.py`,
itself a port of `site/src/data/prediction-distribution.ts`) → 201-point
`numeric_cdf_v1` CDF → exact-integral **CRPS** + **PIT**. No existing repo
scoring code was modified. The Python scorer is pinned against the TypeScript
original by [`pin_against_typescript.py`](pin_against_typescript.py), which
executes the real `.ts` file under Node and hashes it to prevent substitution.

---

## Headline: the dispersion

Every dimension is compared against a **noise floor** — the spread across 5
repeats of the *same* configuration at fixed temperature. A dimension whose
bootstrap CI on the ratio includes 1 is reported as NULL. This threshold was
pre-registered.

| Dim | What changes | Spread | Noise floor | Ratio | 95% CI | Verdict |
|---|---|---|---|---|---|---|
| **D4** | model tier | 9.31% | 2.00% | **4.65** | [2.11, 6.46] | EXCEEDS |
| **D2** | elicitation format | 8.40% | 5.49% | **1.53** | [1.06, 2.29] | EXCEEDS |
| **D1** | policy context | 3.54% | 1.96% | **1.81** | [1.11, 2.65] | EXCEEDS |
| D3 | single-pass vs debate | 1.04% | 2.97% | 0.35 | [0.10, 0.76] | **NULL** |
| D5 | perturbed statute | 2.13% | 1.82% | 1.17 | [0.34, 1.94] | **NULL** |

N = 12 units for every row (11 for D5). 5 repeats per cell. 2520/2520 cells run
(100% grid completion), 0 API errors, 4 unparseable responses (0.16%).

**Ratios are not comparable across dimensions** — the range statistic grows
with the number of levels (D1 has 5, D3 has 2). Compare each against 1, never
against each other.

### Pre-registered primary analyses

- **P1 — policy context.** EXCEEDS (1.81×). Which portion of the bill the model
  sees moves the forecast by more than sampling noise.
- **P2 — elicitation format.** EXCEEDS (1.53×). Replicates, in a policy-analysis
  setting, the axis from arXiv:2603.10044.
- **P3 — the sycophancy test.** 6 of 7 non-tied unit-pairs show `purpose_only`
  shifting the forecast in the *same direction* as `operative_only` relative to
  `none`; 5 pairs tied; sign test p = 0.125. **Directionally suggestive, not
  significant at N=12.** Reported as inconclusive.
- **P4 — magnitude elasticity.** Median **0.000**, CI [0.000, 0.016] → the
  pre-registered **memorisation signal**.

### P4 is the sharpest result

We rewrote §311's age ceilings from "over 51/53/55" to "over 31/33/35"
(`severe`) and "over 71/73/75" (`inert`) — a 40-year swing in how many adults
lose benefits. The substitution is verified applied in the run records
(`context_meta.substitutions = 3`), so the model demonstrably saw different
statutory text.

**The forecast did not move.** A tool that *derived* its answer from the statute
would have to move. This is consistent with the model recalling a remembered
caseload trajectory rather than reasoning from the provision in front of it.

### Debate did not replicate

The *LegalHalluLens* result — a 45% reduction in fabricated findings from a
Skeptic/Verifier/Judge pipeline — has not, to our knowledge, been tested on
statutes. Here it is **NULL**: debate moved the forecast *less* than run-to-run
noise (0.35×). This is a failed replication in a new domain, reported as such.
It is not evidence that debate is useless; it is evidence that it does not move
*this* quantity on *this* corpus.

### Conditioning on the bill did not improve accuracy

`skill_vs_unconditioned` = CRPS(conditioned) − CRPS(`none`), bootstrap CI:

| policy_context | skill | 95% CI | verdict |
|---|---|---|---|
| summary | 0.306 | [−0.067, 0.731] | no detectable skill |
| operative_only | 0.221 | [−0.069, 0.591] | no detectable skill |
| purpose_only | 0.199 | [−0.120, 0.539] | no detectable skill |
| operative_plus_purpose | 0.463 | [−0.079, 1.111] | no detectable skill |

Every CI includes zero. **Showing the model the bill did not make the forecast
better.** The pre-registration required this be reported if it occurred. It
occurred.

---

## Two harness defects found and corrected — both would have biased a result

Recorded because they are the kind of thing this experiment exists to catch,
and because both were *non-random with respect to a measured dimension*.

**1. Truncation (9 runs).** Five runs hit `max_tokens` exactly and lost their
trailing JSON. Truncation correlates with elicitation verbosity — i.e. with D2 —
so silently dropping them would have biased D2. Caps were raised, the failed
traces were **quarantined rather than deleted**
([`runs_api.quarantined.jsonl`](runs_api.quarantined.jsonl), per AGENTS.md), and
the cells were re-run. All 9 succeeded.

**2. The parser read calendar years as forecasts (214 runs).** The original
prose parser took any number above 1,000 as a candidate, so against a series in
the millions it accepted "December 2023" as a point estimate of 2023 people.
**210 of 300 free-text runs (70%)** were affected — and free text is a *level of
D2*. Left in place this would have made free-text elicitation look catastrophic
for reasons having nothing to do with elicitation, manufacturing exactly the
artefact this study exists to detect.

Because every response was stored, the correction was **offline** — no model was
re-called, no run discarded. [`reparse.py`](reparse.py) re-extracts with a scale
band of [0.2×, 5×] the last observed value; original parses are preserved as
`forecast_v1` so the correction is auditable. This was caught by the
cross-artefact scorer pin, which was looking for something else entirely.

---

## What this does not support

- **N = 12 units, one law, one program.** No claim generalises beyond SNAP
  participation without another corpus.
- **The two target months of a state are not independent** — 12 units are really
  6 states × 2 horizons, so the bootstrap over units likely overstates precision.
  D1 and D2 have CI lower bounds of 1.11 and 1.06; they are the marginal results
  and would be the first to fall under a stricter dependence model or any
  multiple-comparison correction. No correction is applied.
- **The horizon is 30–33 months**, because this Census series publishes with a
  ~2-year lag in annual bulk updates: at the 2023-06 vintage it carried data only
  through 2021-06. The policy signal is therefore a small share of total forecast
  error. This biases the accuracy leg toward pessimism and D1 toward the null —
  the effects reported were found *despite* it.
- **Every dimension is measured at one reference configuration.** Interactions
  are unmeasured.
- **PolicyEngine framing.** Used here as the *reference implementation of the
  statutory arithmetic* — exact for what the formula computes — while remaining
  a model input for anything behavioural, per
  `agents/thesis-analyst/skills/policyengine.md`. It is not called ground truth
  for behaviour.

---

## Three sentences to say out loud

> We backtested the forecasting leg against a real enacted law — the SNAP work-requirement title of the Fiscal Responsibility Act — scored against first prints, pre-registered before the first run.

> Then we held the bill fixed and changed only the harness: model choice moves the forecast 4.65× run-to-run noise, elicitation format 1.53×, and which part of the bill you show it 1.81× — and multi-agent debate didn't help at all, which is a failed replication of the one result people cite for it.

> When we rewrote the statute's age threshold by forty years, the forecast didn't move — so on this corpus the tool is recalling a caseload, not deriving from the provision, and conditioning on the bill didn't beat the unconditioned baseline either.
