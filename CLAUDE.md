# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Brier is a decision-making framework that reframes subjective questions ("Should I...?") into forecasting problems with explicit KPIs, confidence intervals, and calibration tracking. The core thesis: making numeric predictions forces mechanism thinking, creates accountability, and reduces sycophancy.

## Commands

### Python Package

```bash
# Install for development
pip install -e ".[dev,experiments]"

# Run tests
pytest

# Run single test file
pytest tests/test_framework.py

# Run with coverage
pytest --cov=brier

# Format code
black brier tests
ruff check brier tests
```

### CLI

```bash
brier new "question"    # Create a new decision
brier new "q" --context "details"  # With context
brier list              # List all decisions
brier list --pending    # Decisions past review date
brier show <id>         # Show decision details (supports prefix match)
brier score [id]        # Score a decision's actual outcomes (interactive)
brier calibration       # Show calibration statistics
brier pending           # Alias for list --pending
brier forecast-draft <id-or-question>  # Draft a forecast/market pack (alias: market-draft)
brier setup {claude,codex}    # Install the skill + register the MCP server
brier doctor {claude,codex}   # Check skill/MCP installation health
brier uninstall {claude,codex}  # Remove skill + MCP registration
brier install-skill {claude,codex}  # Install just the packaged SKILL.md
```

### Site (Next.js)

```bash
cd site
bun install
bun run dev      # Development server
bun run build    # Build for production (standard Vercel SSG, not a static export)
bun run test     # Run vitest tests
```

Production deploys of the site and forecast-api go ONLY through the
self-verifying scripts in `~/thesis-institute` (`deploy-app.sh`); never run a
bare `vercel --prod` from a checkout or worktree.

### Paper

```bash
python3 paper/render_paper.py  # Generate figures, render HTML, sync preemptive_rigor.md and site/public/paper-raw
python3 paper/run_strongest_validation.py  # Strongest reviewer-facing validation across Claude Opus 4.6 and GPT-5.2
python3 paper/run_study1_rerun.py --models gpt-5.4  # Original Study 1 rerun with legacy prompt wording
python3 -m brier.experiments stability --strongest-validation --model gpt-5.2  # Single-model strongest validation
```

## Architecture

### Python Package (`brier/`)

- **framework.py**: Core dataclasses (`Decision`, `KPI`, `Option`, `Forecast`) with serialization. `Option.expected_value()` computes weighted expected values across KPIs. `Decision.best_option()` and `sensitivity_analysis()` for analysis.
- **storage.py**: `DecisionStore` persists decisions to `~/.brier/decisions.jsonl` in JSONL format. Supports CRUD and filtered queries (unscored, pending review, scored).
- **calibration.py**: `CalibrationTracker` computes forecast accuracy metrics: coverage (% of actuals in CIs), calibration error (coverage vs stated confidence), MAE, MRE, Brier scores.
- **cli.py**: Argparse CLI wrapping the above modules.

### Claude Code Plugin (`claude-plugin/`)

- **commands/decide.md**: Full structured decision analysis workflow (KPIs → options → forecasts → logging)
- **commands/score.md**: Score past decisions against actual outcomes
- **skills/decision-framework/SKILL.md**: Skill that detects advice-seeking patterns and reframes as forecasting problems

### Spawning new forecast cells (the thesis.analyst pipeline)

New cells are generated as recorded agent runs, never hand-authored mocks:
an agent researches the question with REAL fetches from official sources
(release calendars for resolutionDate, series history for the base rate),
derives point + 80% CI from the data, and emits JSON with a full trace and
`runAt` = actual generation time. Convert with
`python3 scripts/spawned_cells_to_ts.py site/src/data/almanac-examples/<name>.ts CONST_NAME in.json`,
which enforces the same trace-depth rubric CI does
(`site/src/__tests__/trace-depth.test.ts`): >=7 steps, >=3 real tool steps,
math derivation, base rate, disconfirming consideration. Resolved outcomes
are recorded as observations in PolicyEngine/arch-data
(`ledger/official_observations.jsonl`, branch `codex/thesis-ledger-facts`),
which the site fetches at build time. Deploy strictly via
`~/thesis-institute/deploy-app.sh`; run the recorder workflow
(`gh workflow run record-forecasts.yml --ref main`) right after deploying
new predictions so their pre-registration timestamp is tight.

### Site (`site/`)

Next.js App Router site with Tailwind CSS v4, deployed to Vercel as the
`brier-almanac` project behind app.thesisinstitute.org (standard SSG build —
all forecast pages prerender from `src/data/markets.ts`; four live cells
stream from forecast-api at runtime).

## Key Design Decisions

- Forecasts require both point estimates and confidence intervals
- Confidence levels are explicit (default 80%)
- Base rates and inside-view adjustments are first-class fields for outside/inside view reasoning
- Fermi decomposition supported via `Forecast.components` dict
- Decisions are append-only to JSONL; updates rewrite the file
