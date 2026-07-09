# F12 handoff: generated-site sharding and size budgets

> **External contract change:** `/log.json` is now `thesis_log_v3`. It is a
> manifest, not a self-contained v2 body. Consumers must follow and verify the
> four chunk collections or use `scripts/thesis_log_client.py`. The external
> `verify.sh` marker lives outside this repository and must change from
> `thesis_log_v2` to `thesis_log_v3` when this work is integrated.

## Consumer inventory

All Python consumers under `scripts/` were searched for `log.json` and the v2
heavy fields.

- `mine_ledger_gaps.py`: reads slim `resolutionLinks`; now uses the shared
  loader so it works across v2/v3 rollovers.
- `adopt_proven_series.py`: reads chunked `scores`; now uses the shared loader.
- `prospect_series.py`: reads slim `resolutionLinks`; now uses the shared
  loader.
- `roll_docket.py`: reads slim `resolutionLinks`; now uses the shared loader.
- `resolve_pending.py`: additional consumer found by the audit; reads slim
  `resolutionLinks` and now uses the shared loader.
- `record_forecast_snapshot.py`: reads `entries`; now hydrates through the
  shared loader and archives the manifest plus every referenced chunk.
- `thesis_records_to_comparisons.py` and `strategy_comparisons.py`: audited as
  requested; neither reads `log.json` or any v2 log field in the current base,
  so no loader call was added.

The recorder workflow downloads the v3 manifest and chunks with
`scripts/thesis_log_client.py` before constructing the immutable snapshot.

## Thesis Log v3 chunk map

`/log.json` retains `schemaVersion`, `source`, `counts`, slim
`resolutionLinks`, `resolutionEvents`, `resolutionQueue`, and `judgeResults`.
The formerly inline heavy arrays are reachable through `collections`:

| Collection | Route                       | Contents                                                                      |
| ---------- | --------------------------- | ----------------------------------------------------------------------------- |
| `entries`  | `/log/entries/{index}.json` | every v2 prediction-recorded and prediction-resolved entry                    |
| `specs`    | `/log/specs/{index}.json`   | every v2 prediction spec                                                      |
| `runs`     | `/log/runs/{index}.json`    | every v2 slim run record; 201-point CDFs remain in target-architecture chunks |
| `scores`   | `/log/scores/{index}.json`  | every v2 score, including chronology flags                                    |

Each collection manifest records total count and chunk count. Each chunk
reference records index, row count, URL, and the SHA-256 of the complete chunk
body serialized with the repository's canonical-JSON helper. The Python
client verifies shape, count, ordering, and canonical hash before hydrating.

## Integrator reruns

Run these from a network-enabled checkout after integration:

```bash
cd site
bun install
bunx tsc -b
bun run test
bun run build
bun run check:size-budgets
cd ..
uv run pytest tests/ -q
```

The live-ledger Vitest suites fail in this sandbox with `ENOTFOUND github.com`;
the integrator must rerun them with network access. A production webpack build
did complete here and measured `forecasts.html` at 3,421,198 bytes and
`log.json.body` at 784,244 bytes. The default Turbopack build completed once,
then a repeat hit the sandbox's `binding to a port: Operation not permitted`
restriction while evaluating PostCSS. Rerun the default `bun run build` in CI
and confirm both the CI budgets (`forecasts.html` <= 12 MiB, `log.json.body` <=
8 MiB) and today's F12 targets (`forecasts.html` < 6 MB, `log.json.body` < 4
MB).

Also rerun the external deployment verifier after changing its expected marker
from `thesis_log_v2` to `thesis_log_v3`. That `verify.sh` is outside this repo
and is intentionally not modified here.

Finally, inspect `/forecasts`, one section anchor, and one per-cell link in a
local browser. This sandbox rejected `next start` with `listen EPERM` and
reported no available in-app browser, so visual localhost verification could
not run here; the static HTML structure and link targets were inspected from
the successful build output instead.

No `records/`, generated wave module, or scoring-semantic file is changed by
this work package.
