# SOL-F7 canonical hashing overhaul

## What changed

- Added `site/src/data/canonical-json.ts` as the single canonical JSON and
  SHA-256 implementation. It sorts object keys by UTF-16 code units, preserves
  array order, emits JSON without whitespace, uses JSON number formatting, and
  rejects non-finite numbers.
- Replaced the four 32-bit FNV-1a implementations in prediction specs, Thesis
  Log resolution events, target-architecture projections, and SQL backfill
  generation.
- Full payload-hash fields now contain lowercase 64-character SHA-256 digests.
  Content-derived public IDs retain their namespace shapes and use 16 hex
  characters when truncated.
- Run IDs commit to the point estimate, 80% interval, and full numeric CDF.
  Resolution payload hashes commit to the observed value and unit. Score IDs
  commit to the forecast payload, outcome payload, and
  `numeric_cdf_crps_v1` scorer version.
- Artifact projection deduplication now accepts only identical content digests.
  A truncated-ID collision throws and reports both full digests. Projection
  construction also checks every projected ID namespace for different-payload
  collisions.
- Added canonicalization, full-digest, payload-commitment, forced-collision,
  and real-catalog snapshot tests. Updated `docs/thesis-architecture.md` with
  the hashing contract.

## ID namespaces affected

Directly changed:

- `run.*`: appended a 16-hex forecast-output digest.
- `score.*`: appended a 16-hex digest over forecast, outcome, and scorer
  payloads.
- `artifact.<hex>`: changed from an 8-hex FNV reduction of a content hash to the
  first 16 hex characters of the full content SHA-256.
- `obs.history.*`: changed the suffix from 8 to 16 hex characters.
- `source_series.*`: changed the suffix from 8 to 16 hex characters.

Changed transitively because they embed or reference one of those IDs:

- `vintage.*` for generated historical observations.
- run tool-call IDs (`run.*.tool.*`).
- `run_pack.*`, `run_artifact.*`, `candidate.*`, `reasoning.*`, `review.*`, and
  generated-baseline artifact IDs that embed a run ID.
- resolution-judge IDs that embed a score ID.
- all run, score, artifact, source-series, and observation foreign keys in the
  target-architecture JSON and SQL exports.

Hash fields changed to full SHA-256 include spec, prompt, tool-policy,
input-bundle, idempotency, public-trace, tool request/response, pack prompt,
strategy prompt/tool policy, observation payload, normalized vintage payload,
resolution payload, score, and artifact content hashes.

## Consumers checked

- Searched `site/src/data`, app routes, pages, and components for run, score,
  resolution-event, source-series, observation, and artifact consumers.
- Checked Brier reward exports, Thesis Log exports, forecast judges,
  target-architecture runtime/manifest/chunk exports, and SQL backfill output.
- Public forecast URLs are slug-based; no public route is keyed by the changed
  content-derived IDs. No backward-compatible aliases were added because no
  consumer requires the old IDs.
- No Python implementation mirrors these hashes under `scripts/`.
- The Next.js production build completed, confirming `node:crypto` did not
  enter a browser bundle.

## Verification

- `bunx tsc --noEmit`: passed.
- Six offline Vitest files: 153 tests passed.
- Full `bun run test`: 178 tests passed; 11 ledger-backed tests failed and the
  47-test catalog suite stopped in setup because the sandbox cannot resolve
  `github.com` (`ENOTFOUND`). All failures came from the shared live-ledger
  fetch, not a test assertion.
- `bun run build`: passed; 1,346 static pages generated. A later repeat reached
  a Turbopack sandbox error when an internal CSS worker tried to bind a port,
  after the successful identical build.
- `git diff --check`: passed.

## Deliberately not changed

- Scoring calculations and CRPS semantics were not modified; only score ID and
  hash plumbing changed.
- Files under `records/`, generated forecast/ledger/wave modules,
  `.github/workflows/`, and `scripts/` were not modified.
- Locale-aware sorts used only for presentation ordering remain unchanged; all
  hash canonicalization uses the canonical JSON module and no `localeCompare`.
- Existing generated activity-artifact SHA-256 values are preserved as the full
  content digest; only the derived artifact reference ID changed.

## Environment limitations

- The work began from a clean checkout on the provided
  `sol/f7-canonical-hashing` branch, but the sandbox mounts `.git` read-only.
  `git fetch` cannot write
  `FETCH_HEAD`, and `git add` cannot create `.git/index.lock`, so this workspace
  could not create the requested local commits. The working-tree changes are
  complete and ready for the integrator to commit.
