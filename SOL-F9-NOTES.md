# SOL-F9 notes — fair paired baselines

## Implemented

- Persistence baselines now enter during ledger enrichment, after the site
  fetches the PolicyEngine Ledger. They are no longer synthesized from a
  forecast cell's `historicalContext` or restricted to selected agent-name
  prefixes.
- Every chronology-verified scored primary target gets a baseline coverage
  record. Two or more pre-cutoff same-series ledger observations produce a
  baseline; otherwise the record is explicitly `unavailable` with a reason.
- Available baseline artifacts embed the exact observation IDs, data-point
  IDs, periods, values, units, and `observedAt` timestamps used. The artifact
  SHA-256 and byte count commit to canonical JSON; no `generated://` or
  zero-byte placeholder is used.
- Reward exports include baseline coverage, overall target-paired skill, and
  target-paired win rate. Agent leaderboard rows expose paired target count,
  mean paired skill (`agent nCRPS - baseline nCRPS`), and win rate; legacy
  descriptive means are renamed as unpaired.
- The calibration baseline tile and both leaderboard tables now foreground
  paired skill and win rate.
- Scoring v2 chronology gates, target-scale normalization, condition gates,
  distribution transforms, and exact CRPS were left unchanged; agent and
  baseline scores share the existing per-target normalization scale.
- Median-rollout derivation requires exactly three distinct constituent
  manifests whose custody roots verify. Derived metadata records the three
  manifest/custody references and `pointwise_median_cdf_v1`; strategy label
  generation validates those fields before using “Median of 3 rollouts.”

## Local verification

- `bunx vitest run src/__tests__/fair-baselines.test.ts`: 4 passed.
- `ruff check scripts/median_rollout_ensemble.py scripts/strategy_comparisons.py scripts/thesis_records_to_comparisons.py tests/test_thesis_analyst_runner.py`: passed.
- `pytest tests/test_thesis_analyst_runner.py -q`: 18 passed.
- `pytest -q --ignore=tests/test_figures.py` with sandbox-safe Python cache
  settings: 224 passed, 1 skipped.
- `bunx vitest run --exclude src/__tests__/forecast-catalog.test.ts --exclude
  src/__tests__/migration.test.tsx`: 182 passed.
- `bunx tsc --noEmit`: passed.
- `git diff --check`: passed.

The full site catalog suite and `bun run build` fetch the live ledger from
GitHub. This sandbox has no network, so the catalog run stops in `beforeAll`
with `getaddrinfo ENOTFOUND github.com`; the integrator should rerun `cd site &&
bun run test && bun run build` with the normal ledger fixture/mock or network
access. The first attempted `uv run` also could not initialize the external uv
cache under the filesystem sandbox; system `ruff` and `pytest` were used for
the offline checks above. The unrelated figure suite also aborts while
Matplotlib builds its font cache in this restricted macOS sandbox; all 224
non-figure Python tests pass.
