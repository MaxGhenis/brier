# Thesis Vision

Thesis is an open-source, agent-only forecasting lab for public data series
that can resolve automatically. Brier is the forecast-accuracy agent trained
and evaluated inside that lab.

For the concrete rebuild blueprint, read
[`docs/thesis-architecture.md`](thesis-architecture.md). This page is the
strategic contract; the architecture page turns it into system boundaries,
schemas, runners, adapters, UI, and build order. Current-codebase migration
lives in [`docs/thesis-migration.md`](thesis-migration.md).

The point is not to build another human prediction market. The point is to
make millions of small, checkable forecasts over official series, publish the
full agent trace for each one, resolve them mechanically from official sources,
and use proper scores to improve the agents.

## Mission

Thesis exists to turn public decision-making into an empirical, auditable
forecasting problem:

1. Generate many forecast specs over official public data.
2. Run AI agents only; no human forecasters, hidden priors, or private edits.
3. Publish the prompt, command, stdout/stderr, fetched-source trace, normalized
   forecast, validation report, resolution event, and score.
4. Resolve from official first prints or explicitly defined policy states.
5. Train and compare agents by forecast accuracy, not by preference ratings.

The long-run Brier goal is an open-source AI forecasting agent optimized
directly for accuracy under proper scoring rules. In the ideal version, Brier
learns policies for source selection, base-rate construction, pack use,
distribution sizing, and final forecasts from scored Thesis runs. The reward is
forecast accuracy. Humans still choose their goals and values; the agent's job
is to give the best available predictions.

## Scope

Thesis prioritizes targets that are:

- published by government or similarly authoritative public institutions;
- numeric, dated, and repeatedly released;
- resolvable from a stable official source URL or release calendar;
- suitable for first-print rules, fixed-vintage rules, or exact policy-state
  checks;
- high volume enough to create a training/evaluation environment.

Good targets include labor-market releases, CPI and PCE releases, GDP and
income releases, Treasury and fiscal tables, administrative performance
series, central-bank policy settings, and clean international statistical
agency releases.

Lower-priority targets include one-off news events, private-company outcomes,
questions requiring subjective judging, questions whose source can disappear,
and questions where resolution needs a human committee.

## Non-Goals

Thesis is not:

- a place for humans to enter forecasts;
- a Manifold/Metaculus clone;
- a general chat assistant;
- a collection of plausible mock traces;
- a dashboard whose data can be hand-edited after the fact;
- an RLHF preference benchmark.

Human review can improve code, schemas, and source coverage, but the forecasts
themselves should be produced by recorded agents and scored against official
outcomes.

## Forecast Cell Contract

Every forecast cell must answer four questions:

- What exactly is being forecast?
- When and where does it resolve?
- What did the agent fetch and compute this run?
- How should it be scored later?

That means every real forecast needs:

- a stable `dataPointId`;
- a `resolutionDate` verified from an official calendar or schedule;
- a `resolutionSourceUrl` pointing to the official resolving source;
- a first-print, fixed-vintage, or policy-state `resolutionRule`;
- point estimate, 80% interval, and distribution;
- trace steps with fetched numbers, base rate, math, counter-consideration,
  and final forecast;
- immutable activity artifacts.

If a target cannot be resolved mechanically, it should not enter the core
Thesis training environment.

## Activity Trace Requirement

The trace is the scientific record. A highlighted reasoning summary is not
enough.

A production run should preserve:

- prompt;
- command and model invocation;
- stdout and stderr;
- raw Codex/agent event streams, last assistant message, and usage metadata
  when the backend exposes them;
- draft response, reviewer critique, revision prompt, and public disposition
  when pre-submit review is enabled;
- raw response;
- parsed and normalized forecast JSON;
- validation report;
- manifest;
- later resolution event and score.

Runs that cannot satisfy the trace-depth rubric should remain as failed
records, not be silently cleaned up into successful forecasts.

The app can display a simplified public reasoning trace, but the underlying
record should preserve the complete machine trace needed to replay, audit, and
score the run.

## Packs

Packs are experimental forecasting interventions, not generic markdown skills.

A pack should encode a reusable forecasting move such as release-vintage
calibration, base-rate construction, component decomposition, source
selection, policy-mechanism decomposition, or known agency-specific resolution
rules. Packs matter because they let Thesis compare agents and runs with and
without the intervention on the same target family.

Pack pages should show what the pack changes in the forecast process and where
it is used. They should not repeat a generic definition of what packs are on
every page.

## Promoting Pack Insights

When a pack consistently improves held-out forecast accuracy, its general
forecasting lesson should stop being optional. Promote it into the default
Brier/thesis.analyst system prompt, a universal skill, or the tool policy, then
bump the agent version so future runs are attributable to the new default.

Promotion is reserved for portable practices such as treating the base rate as
the prior forecast, frequent updates when new official information arrives,
explicit decomposition, benchmark competition against naive persistence, and
realized-volatility interval sizing. Domain-specific sources and priors should
usually remain packs or skills so they can still be ablated.

The promotion gate is documented in
[`docs/pack-promotion.md`](pack-promotion.md). Old runs remain valid; prompt
hashes, tool-policy hashes, pack labels, and agent versions separate the
experimental regime from the promoted default.

## Prioritization

When choosing what to build or forecast next, prefer:

1. More automatically resolvable official-series targets.
2. Targets resolving soon enough to score the loop.
3. Families with repeated releases and many comparable targets.
4. Runs that compare agent versions, prompt modes, or pack sets.
5. Infrastructure that reduces hand-editing and preserves full traces.
6. UI that makes run comparison, resolution, and scoring legible.

Do not prioritize novelty over autoresolution. A boring weekly government
series that resolves cleanly is more valuable than an interesting bespoke
question that cannot become training data.

## Scoring and Brier

The Brier Lab export is the bridge from Thesis records to agent training:

- rows are forecast runs;
- unresolved rows carry no reward until the official fact lands;
- resolved rows receive proper scores, currently normalized CRPS;
- split assignment is by `resolutionDate`, not run order;
- training must avoid leakage from future official outcomes.

This makes Thesis a dataset and evaluation loop for Brier. Prompt experiments,
pack ablations, tool policies, and eventually RL policies should be judged by
held-out forecast accuracy.

## Agent Operating Rule

When a future agent is unsure what to do, the default answer should be:

1. Add or improve automatically resolvable public-data forecasts.
2. Preserve or improve full activity traces.
3. Make comparison across agents, prompt modes, and pack sets easier.
4. Make resolution and scoring more automatic.
5. Keep the project open-source and reproducible.

Everything else is secondary.
