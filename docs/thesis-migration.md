# Thesis Clean Migration Plan

This document tracks the implementation path into the clean target architecture
in [`docs/thesis-architecture.md`](thesis-architecture.md). There is no legacy
database compatibility layer: a fresh Thesis database should be created from
`site/supabase/migrations/20260629_thesis_target_architecture.sql`, then loaded
from the generated target-architecture backfill.

## Current State

The live site is still generated from git-tracked forecast cells, ledger rows,
analyst records, judge artifacts, pack definitions, score exports, and static
TypeScript projections. The clean database schema and deterministic backfill now
exist as repo artifacts, but they are not yet the operational writer/read path.

The source-of-truth model should be:

- append-only database tables are the primary query store;
- artifact records are the reproducible evidence store;
- static TypeScript and JSON exports are generated site views.

Until the cutover, git records can remain operationally primary, but database
rows generated from them must be treated as derived views. Do not let git
records and database rows diverge as independent sources of truth.

## Clean Schema

The committed migration defines the target architecture directly:

- target contracts: `targets`, `target_versions`;
- source evidence: `source_series`, `observations`, `observation_vintages`,
  `target_observation_bindings`;
- model priors: `baseline_candidates`;
- strategy and pack metadata: `forecast_strategies`, `strategy_versions`,
  `packs`, `pack_versions`;
- forecast records: `forecast_runs`, `forecast_distributions`,
  `run_pack_versions`, `run_artifact_refs`;
- public activity records: `reasoning_events`, `tool_calls`,
  `artifact_refs`;
- review and judge diagnostics: `review_runs`, `judge_runs`;
- resolution and learning records: `resolution_events`, `scores`;
- integrity records: `audit_events`.

The migration is append-only by default, enables public read policies with
artifact visibility checks, and records insert audit events for public-state
tables.

## Generated Backfill

`scripts/write_target_architecture_projection.ts` writes both:

- a JSON projection for inspection and static export; and
- a SQL backfill for the clean target schema.

The backfill intentionally does not write old prediction/spec tables or alias
columns. Internally, the code can still use existing TypeScript builders to
normalize forecast cells, but the database surface is target-first.

## Landing Pieces

- Clean target records are generated in
  `site/src/data/thesis-target-architecture.ts`.
- `/forecasts/targets.json` and `/targets.json` expose a small manifest.
- `/log.json` exposes the `thesis_log_v3` manifest; the complete entries,
  specs, runs, and scores are canonical-hashed chunks under `/log/{table}/`.
- Per-table exports are available under `/forecasts/targets/{table}.json`.
- Large tables are chunked under `/forecasts/targets/{table}/{chunk}.json`.
- `site/src/data/thesis-target-architecture-sql.ts` generates the SQL backfill.

## Cutover Steps

1. Pick or create the Thesis Supabase project and link the repo to that project.
2. Apply `site/supabase/migrations/20260629_thesis_target_architecture.sql`.
3. Generate the current projection and backfill SQL from forecast cells and
   ledger records.
4. Load the SQL backfill into the linked database.
5. Verify table counts against the projection manifest.
6. Cut new forecast, review, judge, resolution, and score writers over to
   append to the database and artifact store first.
7. Generate site TypeScript and JSON exports from the database/artifact records.
8. Stop hand-editing static forecast data as the primary forecast state.

## Guardrails

- Keep every new prediction ledger-first.
- Prefer `target` and `target_version` vocabulary for new work.
- Preserve the 201-point CDF output contract until a deliberate scoring
  migration replaces it.
- Add source adapters and observation vintages before scaling more
  first-print-resolved target families.
- Promote repeated reviewer findings into deterministic validators.
- Keep LLM judges as process diagnostics, not reward signals.
