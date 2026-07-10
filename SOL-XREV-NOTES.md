# SOL XREV cross-review fixes

## X2 — ledger-owned normalization scale

- Replaced forecast-authored history and primary-interval fallbacks with a
  per-`dataPointId` scale derived from `ledgerHistoryAtCutoff`, the same
  same-series, same-unit, deduplicated, ordered history used by F9 baselines.
- The cutoff is the target's `registeredAt`; legacy registrations fall back to
  the primary run seal. The scale is the sample standard deviation of successive
  ledger changes.
- Fewer than three pre-cutoff observations, missing cutoffs, and zero/non-finite
  dispersion now produce `normalizationScale: null` and
  `normalizationScaleSource: "unavailable"`. Raw CRPS, absolute error, coverage,
  PIT, and the score row remain public.
- Introduced `numeric_cdf_crps_v3_ledger_scale` so append-only SQL stores can add
  corrected scores beside historical v2 rows. The SQL migration adds nullable
  scale, normalized-error, and sharpness fields plus v3 consistency checks.
- Propagated nullable normalized values through Thesis Log, Brier reward rows,
  leaderboards, paired skill, calibration summaries, judge calibration,
  Strategy Lab, target-architecture projections, and SQL backfills. Normalized
  aggregates filter unavailable rows; raw aggregates remain available.

Exploit regressions in `site/src/__tests__/scoring-integrity.test.ts` verify:

1. changing `historicalContext` from honest values to a fabricated million-unit
   range changes nothing;
2. ledger values 10, 14, 12 produce the expected sample step-dispersion
   `sqrt(18)`, while a post-registration million-unit observation is excluded;
3. a two-point history publishes raw CRPS but has null nCRPS, normalized absolute
   error, sharpness, reward, leaderboard score count, and paired skill.

## X6 — retry-safe resolution publication

- The resolve workflow queries the current ledger branch SHA after every
  resolver invocation, independently of resolver skip text.
- It compares that SHA with `records/resolutions/latest.json`, which now denotes
  the last _successfully canaried_ ledger deployment. A mismatch or an append in
  the current run triggers marker, push, deploy-hook, and production-canary
  steps.
- The deployable non-skip commit writes `rebuild-request.json`. Only after the
  production canary reaches that site commit does a `[skip ci]` success-marker
  commit update `latest.json` with `ledgerBranchSha` and `siteCommitSha`. A
  failure between request, push, deploy, canary, or success-marker push therefore
  leaves the previous successful SHA in place and is retried next run.

## X7 + X8 — recorder deployment pinning and canary policy

- Site and forecast-API `/build.json` responses now expose `deploymentUrl`,
  `deploymentId`, and `branchUrl` alongside the commit.
- The recorder fetches both mutable-alias canaries before any other surface,
  validates immutable `*.vercel.app` deployment URLs, and fetches all site
  surfaces, Thesis Log chunks, and forecast SSE streams from those immutable
  deployments.
- Loop-dispatched runs accept `expected_sha` and require exact equality with the
  site canary. Scheduled runs retain ancestor tolerance and record the exact
  deployed-to-checkout ancestry distance.
- Both aliases are re-fetched byte-for-byte after collection. A rollover during
  collection fails the run. Snapshots archive both canaries and record canonical
  URLs, immutable fetched URLs, live deployment commits, deployment URLs,
  expected SHA, and ancestry distance.
- Roll and prospect workflows dispatch the recorder with their pushed SHA.
- `tests/test_record_integrity.py` verifies exact-SHA and pinned-deployment URL
  rejection independently of the workflow shell.

## X10 — post-rebase production validation

- Both docket publish jobs now run, after the final rebase and before push:
  `bun install --frozen-lockfile`, full Vitest, and `bun run build`.
- The validation step has a 30-minute bound inside the existing 60-minute publish
  job bound.

## X11 — robust template inversion and docket recovery

- Captured weekly dates, month names/month numbers, and quarters are semantically
  validated. Impossible values are warned and skipped.
- Repeated template tokens use one named capture plus regex backreferences, so
  templates cannot create duplicate named groups and repeated values must agree.
- `step_period` and `not_too_far_ahead` return safely with a printed warning for
  malformed periods.
- If the successor of the maximum published slug is beyond the allowed horizon,
  the roll scans from the last ledger-observed period and selects the earliest
  eligible unpublished gap before that maximum. This prevents a valid-looking
  far-future rogue slug from freezing a series.
- Adoption replaces concrete date/month/quarter/year fragments only at whole
  slug-token boundaries, preserving literals such as `may` inside `mayor`.
- `tests/test_roll_docket.py` covers repeated tokens, invalid ISO dates, invalid
  months and quarters, non-raising helpers, the far-future freeze recovery, and
  literal-month template corruption.

## Local verification

Passed without network:

```text
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/sol-xfix-mpl \
  XDG_CACHE_HOME=/tmp/sol-xfix-cache PYTHONPATH=. pytest -q
278 passed, 1 skipped

cd site
bunx vitest run \
  --exclude src/__tests__/forecast-catalog.test.ts \
  --exclude src/__tests__/migration.test.tsx
13 files passed, 195 tests passed

bunx tsc --noEmit --pretty false
Prettier check: clean
Ruff check and format check: clean
Workflow YAML parse: clean
```

The excluded Vitest files call the live GitHub-hosted ledger and fail under the
required no-network sandbox. No record, generated wave, or generated forecast
module was changed.

## Integrator reruns and live-fire checks

1. With network access, run `cd site && bun install --frozen-lockfile && bun run
test && bun run build` so the catalog and migration suites exercise the live
   ledger. Run the equivalent frozen install, typecheck, tests, and production
   build in `forecast-api/`.
2. Apply `20260709_ledger_normalization_scale.sql`, then generate/insert the v3
   backfill. Confirm old v2 score rows remain immutable and new v3 rows satisfy
   the availability constraint.
3. Deploy both Vercel projects. Confirm alias and immutable-deployment
   `/build.json` bodies agree and expose commit, deployment URL, and deployment
   ID (or branch URL).
4. Dispatch `record-forecasts.yml` with `expected_sha` equal to production and
   inspect the snapshot: all site/log/SSE `fetchedUrl` values must be immutable
   Vercel URLs, expected SHA must match, and ancestry distance must be zero.
   Repeat once with an intentionally wrong SHA and confirm fail-closed behavior.
5. Run the scheduled recorder path without `expected_sha` while production is an
   ancestor of main. Confirm it succeeds and records the nonzero ancestry
   distance. Move either alias during a test collection and confirm the mixed-
   deployment guard fails.
6. For resolution retry safety, run once with a ledger SHA different from the
   successful marker and interrupt after the rebuild-request push or before the
   success-marker push. Rerun and confirm marker, deploy, and canary repeat. Then
   complete the run and verify `latest.json` records both the deployed ledger SHA
   and canaried site SHA.
7. Manually dispatch each docket workflow with one safe target. Confirm the
   post-rebase frozen install, Vitest, and production build all complete before
   push, and that the recorder dispatch receives the pushed SHA.
