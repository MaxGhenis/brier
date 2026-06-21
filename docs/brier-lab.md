# Brier Lab

Brier is the forecast-accuracy agent trained and evaluated on Thesis records.
Thesis supplies the environment: generated public-data forecast specs,
agent-only runs, immutable activity artifacts, automatic first-print
resolution, and proper scores.

Read [`docs/thesis-vision.md`](thesis-vision.md) for the strategic contract:
Thesis is the agent-only, open-source, autoresolving public-data lab; Brier is
the agent optimized inside it for forecast accuracy.

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
- provenance hashes and activity-artifact count

Higher reward is better because normalized CRPS is negated. Unresolved rows
have `reward.value = null` until the first-print resolver records an official
fact.

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
