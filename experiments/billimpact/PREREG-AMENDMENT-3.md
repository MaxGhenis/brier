# Amendment 3 — the causal test of recall-anchoring (period-moved dose-response)

**Written 2026-07-31 ~12:20 EDT, committed before its first run.** Post-hoc
amendment; every rule below frozen before any Amendment-3 model call.

## Motivation

Arms J/K/P established that forecasts fail to track statutory content on
*retrospective* targets (FPUC dose-response 0/6 monotone; SNAP deltas
non-tracking; the purpose effect name-driven). All of those targets sit inside
training data, so two explanations remain entangled:

- **Recall-anchoring** — the model predicts the remembered realized world and
  ignores the counterfactual text;
- **Derivation failure** — the model cannot propagate a statutory parameter
  into a quantitative forecast at all.

Moving the *same statute* to a period with **no realized trajectory to recall**
separates them.

## Design

**Stimulus.** The verbatim FPUC provision (Pub. L. 116-260 div. N §203) with
exactly four labelled substitutions: the three operative dates moved to a
2026 window (supplement in force for weeks beginning after 2026-09-04 and
ending on or before 2026-12-26) and the inserted rate set per dose. Presented
as "the text of a bill now pending before Congress; assume it is enacted and
in force through the target month." Text is otherwise identical to the retro
arm, so the only differences between arms are the period and the existence of
a memory.

**Periods.** `retro2021` — the real unit `fpuc300.us.2021-01` exactly as in
arm J (history at the 2020-12 origin vintage). `future2026` — target
**November 2026**, history = last 60 months of `W825RC1` at today's vintage
(through 2026-06, level ≈ 35–36). No truth exists for the future arm and none
is ever scored; the measurand is **dose-response only**.

**Doses.** $100 / $300 / $900 weekly (same substitution machinery as arm J).

**Grid.** period {retro2021, future2026} × dose {third, actual, tripled} ×
model {sonnet-5, opus-5, fable-5} × elicitation {point_ci_json,
derivation_json} × 5 reps = **360 runs**.

**New elicitation `derivation_json`** (the maximal-structure arm): the model
must state, as separate JSON fields, the weekly supplement rate it read from
the text, its estimate of eligible weekly claimant volume, the computed
mechanical contribution in the series' units, the no-policy baseline, and
point + 80% CI. Tests whether explicitly-directed derivation rescues
dose-tracking.

## Metrics (per period × model × elicitation)

1. **Monotonicity**: median(third) < median(actual) < median(tripled).
2. **Dose spread**: range of dose medians ÷ within-cell repeat range (the same
   noise-floor construction as the main grid, with its known conservatism).
3. **The causal contrast (primary)**: dose spread in `future2026` minus dose
   spread in `retro2021`, per model × elicitation.
4. For `derivation_json`: does the *stated* supplement rate equal the dose
   ($100/300/900), and does the *computed contribution* scale with it — i.e.
   where exactly does the chain break, extraction or composition?

## Registered predictions

- **Recall-anchoring** ⇒ future2026 shows monotone dose-response with
  first-order spread while retro2021 stays flat (replicating J).
- **Derivation failure** ⇒ flat in both periods, including under
  `derivation_json`.
- **Elicitation rescue** ⇒ `derivation_json` monotone in both periods while
  `point_ci_json` is flat — the failure was elicitation all along.
- Mixtures reported as observed. The future arm is never scored for accuracy;
  no realized value exists and none will be claimed.

## Null

No dose spread anywhere above the repeat noise floor.

---

## Deconfound arm (appended ~15:10 EDT, committed before its runs; responds to the #61 review)

The review is correct that the original arms differ in statute-name visibility
as well as period: the retro header names Pub. L. 116-260, the future header
does not — and §2 of this study shows the name alone moves forecasts. New arm:
retro2021, identical dose machinery, with the header anonymized to match the
future arm's framing ("verbatim text of a statute; assume it is in force
through the target month"; no law name, no public-law number). opus-5 and
fable-5 × 3 doses × {point+CI, directed derivation} × 5 reps. Registered
predictions: if recall-anchoring is period-driven, unnamed-retro stays flat
under point+CI (matching named-retro) and derivation still restores tracking;
if the original flatness was name-driven, unnamed-retro shows dose-response
and the period claim must be withdrawn in favor of a name claim. Either
outcome is reported.
