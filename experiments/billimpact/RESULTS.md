# RESULTS — Harness sensitivity of bill-conditioned forecasting

**2026-07-31, Hacking the Think Tank II (FAI/IFP, Washington DC).** David Gringras.

Design frozen in [`PREREGISTRATION.md`](PREREGISTRATION.md), committed 09:59 EDT
(`f95c4b6c`) **before the first model call**. Extensions in
[`PREREG-AMENDMENT-1.md`](PREREG-AMENDMENT-1.md) and
[`PREREG-AMENDMENT-2.md`](PREREG-AMENDMENT-2.md), each committed before its own
first run. Adversarial audit of our own constructions:
[`RED_TEAM.md`](RED_TEAM.md) — its corrections are **applied here**, not hidden.
Scope: **Leg B (conditional forecast) plus the S.3596 mechanical arm**; the
team's extraction leg is out of scope and nothing here merges the two.

**Totals: ~5,100 scored runs** — 2,520 (corpus A grid) + 720 (amendment arms
H/I/J/K) + 180 (arm P) + ~1,400 (CTC arm) + 260 quarantined-and-rerun — across
**20 retrospective units (5 enacted laws, 5 programs)** and **14
PolicyEngine-verified household cases**. All first prints frozen before any
model ran; zero API errors; every failed run quarantined, none silently cleaned.

---

## 1 · The dispersion (corpus A: SNAP under Pub. L. 118-5 §§311–314)

12 units = 6 states × 2 target months; forecaster sees the series as published
2023-06 (pre-effect vintage), scored on first prints (zero revisions) with the
house CDF + exact CRPS + PIT; the Python scorer is pinned against
`site/src/data/prediction-distribution.ts` by an executable cross-artefact test.

| Dim | What varies | Spread | Naïve ratio | **Corrected inference** (RED_TEAM) |
|---|---|---|---|---|
| D4 | model tier | 9.3% | 4.65 [2.11, 6.46] | **12.4× its permutation null; survives Bonferroni + state clustering. The most defensible number in the study.** |
| D1 | policy context shown | 3.5% | 1.81 [1.11, 2.65] | 4.1× its permutation null (p<0.0003) — but the effect is **carried by the purpose-clause arm** (see §2); statutory-text-only levels alone are null |
| D2 | elicitation format | 8.1% | 1.73 [1.17, 2.92] | 4.8× its permutation null, but **fragile to state clustering** (clustered CI spans 1); report as suggestive |
| D3 | debate pipeline | 1.0% | 0.35 → "null" | **Wrong as originally stated**: no magnitude effect, but debate shifts forecasts *up* in 8/9 moving units (p=0.039) and inflates within-cell variance 5.4× |
| D5 | statutory magnitude | 2.1% | 1.17 → corrected **0.97** | Null (the 1.17 excluded the most insensitive unit because its noise floor was 0 — a denominator selection RED_TEAM caught) |

The original "ratio > 1" threshold was **wrong**: under a true null the
expected ratio is 0.12–0.52, not 1 (numerator ranges over medians-of-5,
denominator over single draws). The permutation-based restatement above is the
honest test — and it *strengthens* the headline. Both constructions are
reported; nothing was re-run to get there.

**Calibration, the sharpest accuracy statement in the study:** adding bill text
made intervals **narrower in 12/12 units (p=0.0005) while coverage fell**
(0.50 → 0.33 against a nominal 0.80). Bill context bought confidence, not
accuracy. No policy-context level improved CRPS over the unconditioned
baseline (all four point estimates worse; every CI spans 0).

## 2 · The purpose-clause effect is *named-statute recall*, not preamble sycophancy

FRA §313 is a real enacted purpose clause with zero mechanical content. Shown
*only* this clause (statute named in the header), forecasts fell in 10/12
units, median −2.65% (p=0.002) — **more** than the operative sections
themselves (−0.69%). Amendment 2 decomposed the mechanism:

| Arm | Construction | Median shift | Sign test |
|---|---|---|---|
| `purpose_only` | clause + **statute named** | −2.65% | p=0.002 |
| `purpose_unnamed` | name redacted | −0.35% | p=0.29 |
| `purpose_complete` | + "this is the complete bill" | 0.00% | p=0.45 |
| `purpose_synthetic_expand` | pro-enrollment clause, complete framing | 0.00% (no sign flip) | p=0.45 |

**The name of the law does the work.** Strip it and the effect collapses;
assert completeness and it vanishes; an access-*expanding* clause fails to push
forecasts up. What looked like sycophancy is the model recognising
"Pub. L. 118-5" and pricing in what it remembers that law doing — direct,
mechanism-level evidence of backtest contamination, caught because the test
was built to be decomposable. (N=12 non-independent units; one reference
config.)

## 3 · Counterfactual statutory forecasting is recall-dominated — at every tier tested

Three escape routes for the "it's just the pipeline" objection were closed in
turn:

- **Not elicitation.** Decomposed elicitation (arm K) elicits the policy delta
  as its own number. Models produce a plausible-magnitude delta (−8k to −20k
  persons) — which then **fails to track the statute**: severe-vs-inert in the
  expected direction in only 3/12 units across a 40-year rewrite of the ABAWD
  age caps. The delta is a prior about "SNAP work-requirement bills", not a
  reading of this one.
- **Not effect size.** The FPUC arm (arm J) rewrites a $300/week supplement to
  $100 / $900 — a first-order, dollar-denominated effect on UI outlays.
  **Dose-response monotone in 0/6 (unit × model × elicitation) cells.**
- **Not the model tier.** Fable-5 fails it too, and diagnostically: its
  forecasts hug the *realised* Jan/Mar-2021 trajectory regardless of dose —
  recall-anchoring on a period deep inside training data.

Corpus A's version of the same finding: 6/12 units returned *identical*
forecasts under a 20-year-stricter and a 20-year-looser rewrite while being
displaced from the unmodified statute — the models react to the *existence* of
an amendment, not its *content*.

## 4 · The control: mechanical statutory analysis works — and tools close the tier gap

S.3596 (Stronger Start for Working Families Act; CTC phase-in threshold
$2,500 → $1) against 14 PolicyEngine-verified household cases (zero-delta and
partial-delta traps included). Exact-answer rates (±$1):

| Condition | haiku-4.5 | sonnet-5 | opus-5 / fable-5 |
|---|---|---|---|
| full bill, no tools | **4%** | 74% | 100% |
| full bill + PolicyEngine tool | **100%** | 100% | 100% |
| §2(a) only (conforming amendment withheld), no tools | — | **60%** (31% on partial-delta) | 100% |
| plain-English summary, no tools | — | 98% | 100% |

Three demo-grade facts: **the tool converts every model to 100%** (haiku
4→100); the **statutory trap works** — verbatim-but-incomplete statute is
*worse* input than a plain description for mid-tier models; and **tools fix
arithmetic, not extraction** — opus with the tool but the incomplete excerpt
dips to 86%, feeding a mis-extracted threshold into a correct calculator.

Put §3 and §4 together and the architecture writes itself: **compute the
statutory leg mechanically (PolicyEngine, full text), never inside the
forecast — the LLM demonstrably substitutes memory for derivation exactly
there.** (PolicyEngine is used here as the reference implementation of the
statutory arithmetic; per house convention it remains a model input, never
ground truth for behaviour.)

## 5 · Out-of-sample bake-off (amendment-frozen selection; corpus B)

Config selected on corpus A (fable-5 · operative_only · point_ci_json), frozen
in Amendment 1 **before any corpus-B run**, then evaluated on 8 fresh units
across 4 other laws/programs (3–14-month horizons, heavily-revised BEA series
scored on first prints) against mechanical baselines:

| Arm | mean nCRPS | median | 80% coverage |
|---|---|---|---|
| fable + bill (selected) | 0.242 | 0.154 | 0.70 |
| fable, no bill | 0.229 | 0.169 | 0.72 |
| sonnet + bill | 0.518 | 0.460 | 0.35 |
| persistence | 0.362 | 0.194 | 0.62 |
| drift | 0.382 | 0.281 | 0.38 |

The selected config **beats persistence in 6/8 units** (ΔnCRPS −0.120
[−0.362, +0.092]; directional, not significant at N=8), with the largest wins
exactly where a bill-reader should win — the FPUC shock, where persistence
scores 0.87/0.72 and fable 0.12/0.17. Model tier again dominates: sonnet+bill
*loses* to persistence. Bill-vs-no-bill remains a wash (4/8) — noting the
no-bill arm is contaminated in the model's favour on historical events, which
biases against finding conditioning value. The forward-registration pack
(below) is the uncontaminated version of this comparison.

## 6 · Forward registration — making it a live experiment

Retrospective validation is the rehearsal; the lab's own machinery is the real
instrument. `forward/` (in progress at time of writing) registers per-config
lanes on already-registered, near-resolving Thesis targets, so harness
sensitivity resolves *mechanically, out of training distribution*, under the
lab's chronology verification, over the coming weeks and months.

## 7 · Instrumentation defects caught and corrected (all documented, none silent)

1. **max_tokens truncation** correlated with elicitation verbosity (a measured
   dimension) — 9 runs quarantined and re-run.
2. **The prose parser read calendar years as forecasts** — 214 runs, 70% of
   free-text; corrected *offline* from stored responses (`reparse.py`), v1
   parses preserved; caught by the scorer pin looking for something else.
3. **Thinking-budget exhaustion** produced empty responses on the CTC arm (157
   quarantined, re-run at raised caps).
4. **A backwards direction comment** on the perturbation arm and a wrong
   commit-time claim in an earlier draft of this file — both recorded in
   Amendment 1 §F.
5. RED_TEAM's corrections to our own statistics (§1).

Each of 1–3 was non-random with respect to a measured dimension — precisely
the class of artefact this study exists to detect, caught by its own
machinery.

## 8 · What none of this supports

N = 20 retrospective units across 5 laws; 12 of them are 6 states × 2 months
and not independent; every dimension is measured at one reference config;
retrospective accuracy on in-training-window targets is an upper bound;
D2 is clustering-fragile; the bake-off is N=8. No claim generalises beyond the
programs tested without further corpora. State N. Always.

---

## The three sentences

> We backtested the forecasting leg against five enacted laws with frozen
> first-print ground truth, pre-registered before the first run — then held
> the bills fixed and changed only the scaffolding nobody reports: model
> choice moves the forecast twelve times its sampling noise, and showing the
> model the bill made it *more confident and less calibrated* in twelve of
> twelve units.

> When we rewrote a statute's operative numbers — a forty-year swing in a
> work-requirement age cap, a tripled unemployment supplement — the forecasts
> didn't track the change at any model tier, while the same models computed a
> bill's household tax effect to the dollar once PolicyEngine was in the loop;
> the models derive mechanics but recall forecasts.

> So the architecture conclusion is: compute the statutory leg mechanically,
> never inside the forecast, report your harness with your number — and we've
> started registering per-config forward forecasts in the lab so this measures
> itself, contamination-free, from here on.
