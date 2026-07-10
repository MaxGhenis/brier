# SOL-F5 — independent resolver binding

## What changed

- Both docket generate jobs now run `scripts/register_targets.py` after target
  computation and before `run_thesis_batch.py`.
- Each registration is canonical-JSON hashed and written as a new immutable
  `records/targets/YYYY-MM-DD-<sha256>.json` snapshot. The batch target context
  carries the snapshot path/hash and the full contract.
- The generated target ledger receives a `registrationState: "preregistered"`
  entry immediately. Publication verifies the forecast against that entry and
  finalizes it as `published`; legacy entries with no state remain implicitly
  published.
- Preregistered targets may lack a forecast for seven days. Published targets,
  malformed preregistrations, and preregistrations older than seven days remain
  test failures.
- `resolve_pending.py` archives each successful ALFRED response byte-for-byte
  as deterministic gzip under `records/resolutions/<date>/<run>/responses/`.
  Appended ledger facts include the archive hashes plus `targetContentHash`,
  the pre-append `ledgerRepoSha`, `sourceVintage`, and `retrievedAt`.
- Site/scoring resolution now selects the earliest `observedAt` for a
  `dataPointId`, so a later revision cannot change the score.

The F11 generate/publish trust split remains in place. Registration artifacts
cross the existing unprivileged publication bundle and the snapshot lands in
the records-first commit. F13's deployable marker and `/build.json` canary flow
are unchanged.

## Local verification completed

```bash
ruff check scripts/register_targets.py scripts/roll_docket.py \
  scripts/prospect_series.py scripts/mine_ledger_gaps.py \
  scripts/generate_ledger_targets.py scripts/run_thesis_analyst.py \
  scripts/resolve_pending.py scripts/docket_publication.py \
  tests/test_register_targets.py tests/test_resolve_pending.py \
  tests/test_thesis_analyst_runner.py

pytest -q tests/test_register_targets.py tests/test_resolve_pending.py \
  tests/test_thesis_analyst_runner.py tests/test_docket_publication.py

cd site
bun run test -- src/__tests__/independent-resolver-binding.test.ts
bunx tsc --noEmit
```

The full Python suite also passes offline when its existing paper environment
is supplied (`243 passed, 1 skipped` excluding figures; `17 passed` for the
figure suite). The sandbox cannot fetch the live PolicyEngine ledger used by
the broader Vitest/build path, so the integrator must rerun `bun run test` and
`bun run build` with network access.

## Integrator live-fire: one roll dispatch

Run this after merging/committing F5 to `main`, because both docket workflows
intentionally check out `main` inside their jobs.

```bash
gh workflow run roll-docket.yml --ref main \
  -f max_targets=1 \
  -f cadence=weekly

RUN_ID=$(gh run list --workflow roll-docket.yml --limit 1 --json databaseId \
  --jq '.[0].databaseId')
gh run watch "$RUN_ID" --exit-status
gh run view "$RUN_ID" --log > /tmp/sol-f5-roll.log
rg -n "Preregister targets before forecasting|Run the analyst batch|Commit run records|Publish passing cells" \
  /tmp/sol-f5-roll.log
```

Then pull `main` and verify the records-first boundary and hash:

```bash
git pull --ff-only origin main
git log --oneline -6
REG=$(ls -t records/targets/*.json | head -1)
python3 - "$REG" <<'PY'
import json, pathlib, re, sys
sys.path.insert(0, "scripts")
from canonical_json import canonical_sha256

path = pathlib.Path(sys.argv[1])
payload = json.loads(path.read_text())
digest = canonical_sha256(payload)
assert re.search(rf"-{digest}\.json$", path.name), (path, digest)
target = payload["targets"][0]
required = {"series", "period", "catalogSlug", "dataPointId", "unit", "valueScale", "sourceBinding"}
assert required <= target.keys()
assert {"adapter", "sourceSeriesId", "field", "table", "transform", "releasePolicy", "expectedReleaseWindow"} <= target["sourceBinding"].keys()
print(path, digest, target["dataPointId"])
PY
```

Inspect the batch manifest and generated target entry. The batch target's
`targetContentHash`, `dataPointId`, unit, and `sourceBinding` must match the
snapshot exactly. If the forecast passed, its generated target must be
`registrationState: "published"`; if the analyst failed, the entry must remain
`preregistered` and the catalog orphan test must permit it only through day 7.

Finally rerun the network-backed gates and confirm the existing F13 canary:

```bash
(cd site && bun run test && bun run build)
SHA=$(git rev-parse origin/main)
test "$(curl -sf https://app.thesisinstitute.org/build.json | \
  python3 -c 'import json,sys; print(json.load(sys.stdin)["commit"])')" = "$SHA"
```

On the next claims release, dispatch `resolve-and-rebuild.yml` once and verify
that the new `records/resolutions/<date>/<run>/manifest.json` archive references
match the gzip files and that the appended ledger row carries all four F5
provenance fields. This is network-only and was not attempted in the sandbox.
