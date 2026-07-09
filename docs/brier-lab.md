# Brier Lab

Brier is the forecast-accuracy agent trained and evaluated on Thesis records.
Thesis supplies the environment: generated public-data forecast specs,
agent-only runs, immutable activity artifacts, configured official resolution,
and proper scores.

Read [`docs/thesis-vision.md`](thesis-vision.md) for the strategic contract:
Thesis is the agent-only, open-source, autoresolving public-data lab; Brier is
the agent optimized inside it for forecast accuracy.

Read [`docs/thesis-architecture.md`](thesis-architecture.md) for the rebuild
blueprint: ledger-first targets, typed source adapters, benchmark priors,
strategy runs, review/judge separation, append-only storage, and Brier reward
exports.

Read [`docs/thesis-migration.md`](thesis-migration.md) for the current schema
mapping and source-of-truth cutover path.

## Reward

The first reward export is `/brier/reward.json`.

Each row is one recorded forecast run:

- `runId`, `predictionId`, `specId`, and `specVersionId`
- agent/model/run label metadata
- deterministic split
- resolution date and run horizon
- reward value, currently `-normalizedCrps`
- score components: CRPS, normalized CRPS, absolute error, 80% interval
  coverage
- distribution provenance (`agent_reported` or `interval_seeded`) and the
  immutable transform version used to materialize the scored CDF
- provenance hashes and activity-artifact count

Higher reward is better because normalized CRPS is negated. Unresolved rows
have `reward.value = null` until the configured official resolver records an
official fact.

## LLM Judges

The Thesis Log carries judge summary counts and a link to the full judge export.
`/forecasts/judges.json` and the Brier reward export carry the auxiliary judge
records:

- trace-quality judges score public reasoning for base rates, source
  grounding, resolution clarity, uncertainty calibration, mechanisms,
  counterarguments, and forecast coherence
- pairwise judges compare two runs on the same target, such as primary vs
  pack-informed or prior-informed runs
- post-resolution judges tag likely failure modes after official facts arrive

These records are explicitly `rewardEligible: false`. They are process
diagnostics for triage and prompt/pack iteration. Before any judge signal can
guide training, it must be checked against held-out proper scores; the reward
objective remains resolved forecast accuracy.

## Pre-submit Review

Some runs can use an explicit draft-review-revise workflow before publication.
The reviewer sees only the draft, target contract, and pre-resolution public
evidence; it cannot silently edit the forecast. The forecaster may revise the
final submission, but the draft response, reviewer critique, revision prompt,
and public disposition are all preserved as activity artifacts and compact
`preSubmitReview` metadata.

Only the final forecast receives reward. Review status is exported so Brier can
compare reviewed and unreviewed workflows by held-out CRPS before making review
part of the default agent policy.

## Splits

Rows are split by `resolutionDate`, not by creation time:

- `train`: resolved before 2026-07-01
- `validation`: resolved from 2026-07-01 through 2026-12-31
- `test`: resolved on or after 2027-01-01
- `unresolved`: no official fact yet

Training code may use only rows whose official resolution was known before the
evaluation cutoff. That keeps Brier from learning from future observations.

## What This Enables

The export is deliberately simple enough for:

- offline prompt and pack ablations
- supervised traces-to-forecast experiments
- RL policies that choose tools, packs, source weighting, and distributions
- agent leaderboards by domain, horizon, agency, or pack set
- leakage audits before any model-training run

The public trace is the scientific record: prompts, tool calls, fetched data,
raw response, normalized forecast, validation, resolution, and score.

## From Pack to Default

Pack ablations are the test harness for forecasting practices. If an
intervention reliably improves held-out reward and survives leakage/robustness
checks, its portable lesson should be promoted into the default Brier or
thesis.analyst policy. The pack then becomes historical evidence or a
domain-specific optional source, while the promoted rule is tracked by the next
agent version and prompt/tool-policy hashes.

See [`docs/pack-promotion.md`](pack-promotion.md) for the promotion gate.
