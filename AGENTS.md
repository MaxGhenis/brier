# Agent Instructions

This repository contains Brier and the Thesis forecasting app. Future agents
should treat this file as the operating entrypoint.

## Read First

Before changing forecast-generation, pack, resolution, scoring, or agent-run
surfaces, read these in order:

1. `docs/thesis-vision.md` - mission, scope, non-goals, prioritization.
2. `docs/cell-contract.md` - forecast-cell schema and trace-depth bar.
3. `docs/thesis-analyst-runner.md` - how live agent runs become records.
4. `docs/brier-lab.md` - reward export, splits, and scoring loop.
5. `agents/thesis-analyst/system.md` - analyst method and honesty rules.

For UI work, also inspect the existing page/component before editing; preserve
the utilitarian forecast-lab feel.

## North Star

Thesis is an open-source, agent-only forecasting lab for automatically
resolvable public-data series. Brier is the forecast-accuracy agent trained and
evaluated on Thesis records.

Optimize for:

- more official-series forecasts that resolve mechanically;
- complete public activity traces;
- run comparison across agents, prompt modes, and pack sets;
- automatic resolution and proper scoring;
- reproducibility over hand-authored polish.

## Hard Constraints

- Do not turn Thesis into a human prediction market.
- Do not add forecasts that require subjective adjudication unless they are
  outside the core Brier training loop.
- Do not hand-edit generated forecast modules except to wire generated output
  into the catalog after review.
- Do not collapse full activity into a summary. Preserve prompt, command,
  stdout/stderr, raw response, parsed/normalized cells, validation, manifest,
  resolution event, and score where available.
- Do not infer `resolutionDate` from cadence. Verify it from an official
  calendar, schedule, release placeholder, or policy-state rule.
- Do not use FRED or news as the final resolution source when an official
  agency source exists. FRED can be a history mirror.
- Do not silently clean failed agent runs into successful ones. Failed traces
  are useful records.

## Common Tasks

### Add Or Run Forecasts

Use the thesis analyst runner:

```bash
uv run --extra dev python scripts/run_thesis_analyst.py \
  --series ons.labour.unemployment_rate \
  --period 2026-Q4 \
  --prompt-mode fast \
  --command "/Users/maxghenis/.bun/bin/codex --search exec --ignore-user-config -m gpt-5.5 -c 'service_tier=\"fast\"' --sandbox read-only -C {repo_root} -"
```

Use `--prompt-mode fast` for high-volume public-release batches. Use full
prompt mode when auditing or improving the agent method.

After a successful run:

1. Inspect `manifest.json`, `validation.json`, and `normalized_cells.json`.
2. Keep failed runs in `records/thesis-analyst/...`.
3. Promote successful runs through a generator, not by hand-pasting JSON.
4. Verify the detail page, log page, and Brier reward export if the run is
   wired into the UI.

### Add Comparison Runs

Prefer generated comparison augments:

```bash
uv run python scripts/thesis_records_to_comparisons.py \
  site/src/data/thesis-analyst-live-comparisons.ts \
  RECORDED_THESIS_ANALYST_COMPARISON_RUN_AUGMENTS \
  records/thesis-analyst/YYYY-MM-DD/.../manifest.json
```

If units differ between the live cell and the catalog target, encode the
conversion in the generator mapping so comparisons render in the catalog unit.

### Add Or Change Packs

Packs are forecasting interventions, not generic markdown skills. A pack page
should explain what the pack changes in the forecast process and show where it
is used. Do not repeat a meta-definition of packs on every individual pack
page.

Useful pack comparisons show at least:

- no-pack/control run;
- pack-enabled run;
- point and interval shift;
- trace or reasoning difference;
- eventual score difference when resolved.

### Work On Resolution Or Scoring

Resolution and scoring code should preserve these invariants:

- splits are by `resolutionDate`, not run order;
- unresolved rows have null reward;
- resolved rows link to official observations;
- training cannot see future official outcomes;
- reward rows include provenance hashes and activity-artifact count.

## Verification

For Python runner changes:

```bash
uv run --extra dev ruff check scripts/run_thesis_analyst.py scripts/thesis_records_to_comparisons.py tests/test_thesis_analyst_runner.py
uv run --extra dev pytest tests/test_thesis_analyst_runner.py
```

For site changes:

```bash
cd site
bun run test
bun run build
```

After meaningful frontend changes, verify the affected localhost pages in the
in-app browser.

For docs-only changes, at minimum run:

```bash
git diff --check
```

## Definition Of Done

A change is not done until:

- the relevant docs or generated artifacts are updated;
- validation catches bad cells rather than allowing weak traces through;
- the UI shows the new run/comparison/resolution where appropriate;
- the Brier reward export still builds;
- tests or a clear reason for not running tests are reported.

When in doubt, choose the path that increases the number of automatically
resolvable, fully traced, scored public-data forecasts.
