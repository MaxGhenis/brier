# F8: materialized distributions and exact CRPS

## What changed

- Replaced trapezoid CRPS scoring with exact integration of each
  piecewise-linear CDF segment. Scoring now rejects malformed distributions:
  fewer than two points, non-finite values, non-increasing support values,
  decreasing/out-of-range probabilities, or endpoint probabilities outside
  `0 +/- 1e-9` and `1 +/- 1e-9`.
- Added `distributionProvenance` and `transformVersion` to resolved scores,
  reward rows, strategy score/summary rows, log summaries, target-architecture
  distribution/score projections, and SQL backfill rows. The calibration and
  strategy tables expose the elicitation population without changing ranking.
- Versioned the interval transform as `interval_anchor_v1` and agent-authored
  CDFs as `agent_cdf_v1`. `transformVersion` is part of the canonical score-ID
  payload. Existing checked-in agent CDFs resolve to `agent_cdf_v1` without
  editing generated wave modules.
- Added the distribution-provenance schema migration. Historical append-only
  database rows remain nullable until reprojected from their immutable run
  payload; new backfill rows carry the exact classification and version.
- The thesis analyst runner now materializes a 201-point distribution after
  normalization, writes `distribution.json` as a `run_distribution` artifact
  with SHA-256/byte/time metadata, includes it in the manifest/activity log,
  and carries the exact distribution through the generated TypeScript cell.
  Interval runs use the TypeScript five-anchor math; ladder runs match
  `strategy_comparisons.py::ladder_distribution` at scale 1.

## Exact CRPS derivation

For a segment `[a, b]` on which the observation indicator is constant `c`,
the error `e(x) = F(x) - c` is linear. If its endpoint errors are `e0` and
`e1` and `w = b - a`, the implemented closed form is:

```text
integral_a^b e(x)^2 dx = w * (e0^2 + e0*e1 + e1^2) / 3
```

When `y` lies inside a segment, the code linearly evaluates `F(y)` and splits
the segment at `y`: the left piece uses `c = 0`, and the right piece uses
`c = 1`. With valid CDF endpoints, an observation below support contributes
the exact lower tail `lower - y`; one above support contributes `y - upper`.
Golden tests cover the uniform `[0,1]` result `1/12` at `y = 0.5`, a near-step,
both outside-support directions, and a hand-derived asymmetric result `13/48`.
The asymmetric test also verifies PIT interpolation (`0.625`).

## TypeScript/Python parity fixture

`tests/fixtures/interval_anchor_v1_distribution.json` was generated directly
from `buildNumericCdfFromInterval` with point `5.1`, p10 `4.6`, and p90 `5.8`.
It records all 201 TypeScript points as fixed 10-decimal strings and names the
builder in its `source` field. The Python test materializes the same inputs,
formats its points to 10 decimals, and compares the full array. A separate
test compares runner ladder points/support directly with the existing strategy
builder.

## Verification performed

- Offline site subset: 8 files, 171 tests passed.
- Focused exact-CRPS/hashing tests: 17 passed.
- Python runner suite via installed system pytest: 16 passed.
- Python Ruff checks passed.
- `bunx tsc --noEmit` passed.
- `git diff --check` passed.

The full `bun run test` reached 196 passing tests, then the live-ledger suites
failed with `getaddrinfo ENOTFOUND github.com` (`forecast-catalog.test.ts` and
11 ledger-dependent tests in `migration.test.tsx`), as expected without
network. `bun run build` reached Next.js compilation but Turbopack could not
bind its CSS worker port in this sandbox (`Operation not permitted`). The exact
requested uv pytest wrapper also could not fetch uncached pytest from PyPI;
the same test file passed through the already-installed system pytest.

## Integrator reruns

In a networked environment that permits local build worker ports, rerun:

```bash
cd site
bun run test
bun run build

cd ..
uv run --quiet --with pytest python -m pytest tests/test_thesis_analyst_runner.py -q
```
