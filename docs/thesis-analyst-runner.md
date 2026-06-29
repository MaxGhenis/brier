# Thesis analyst runner

`scripts/run_thesis_analyst.py` is the local Axiom-style runner for forecast
cells. It turns a target spec into a complete run directory, then feeds the
validated cell into the existing spawned-cell converter.

Before changing the runner, read [`docs/thesis-vision.md`](thesis-vision.md).
The runner exists to make agent-only public-data forecasts reproducible:
prompt, command, stdout/stderr, raw response, normalized forecast, validation,
manifest, and later score should remain linked.

## Subscription-backed Codex run

Use the native Codex path for local GPT-family runs. It follows the same
pattern as Axiom Encode: prefer the Desktop-bundled Codex CLI, create a
temporary `CODEX_HOME` with subscription auth symlinked in, ignore user config,
run `codex exec --json`, capture the last assistant message, and persist the
full JSONL event stream as activity artifacts.

```bash
python3 scripts/run_thesis_analyst.py \
  --series ons.labour.unemployment_rate \
  --period 2026-Q4 \
  --codex-model gpt-5.5
```

Use `--no-codex-search` for reviewer-like runs that should not fetch new
evidence, `--codex-sandbox` to change the execution sandbox, and
`--codex-reasoning-effort` to change the Codex reasoning-effort config.
Codex runs default to the read-only sandbox and may inspect local repo context
when useful, including prior run manifests, activity artifacts, generated
comparison data, prediction packs, ledger targets, docs, and tests. The prompt
treats that context as optional: agents should use it when it improves an
update or resolver, but they are not required to inspect prior traces for every
target.

`--command` remains available for non-Codex agents or custom experiments. The
command may reference `{prompt_path}` and `{repo_root}` and receives the prompt
on stdin:

```bash
python3 scripts/run_thesis_analyst.py \
  --series ons.labour.unemployment_rate \
  --period 2026-Q4 \
  --command "codex exec -C {repo_root} -"
```

Agent commands default to a 600 second timeout. Use `--timeout-seconds` to make
smoke tests shorter or longer. A timeout writes `command.json`, `stdout.txt`,
`stderr.txt`, `raw_response.txt`, `error.json`, and `manifest.json` with
`ok: false`. Codex runs additionally write `codex_stdout.jsonl`,
`codex_stderr.log`, `codex_events.jsonl`, `codex_last_message.txt`, and
`codex_trace.json`.

When the command names a model with `-m`, `--model`, or `--model=...`, the
runner records that runtime model in `manifest.json` and in generated cell
metadata. If it differs from the agent default in `agent.yaml`, the manifest
also keeps `configuredModel` for comparison.

## Saved-response and dry-run modes

Use a saved response when a model run happened elsewhere:

```bash
python3 scripts/run_thesis_analyst.py \
  --series ons.labour.unemployment_rate \
  --period 2026-Q4 \
  --response-file /tmp/codex-output.txt
```

Use the deterministic mock mode to test plumbing without calling an agent:

```bash
python3 scripts/run_thesis_analyst.py \
  --series test.synthetic_rate \
  --period 2030-01 \
  --mock-cell
```

## Pre-submit review loop

Use `--pre-submit-review-codex-model` or `--pre-submit-review-command` to run a
reviewer subagent between the draft and final forecast:

```bash
python3 scripts/run_thesis_analyst.py \
  --series ons.labour.unemployment_rate \
  --period 2026-Q4 \
  --codex-model gpt-5.5 \
  --pre-submit-review-codex-model gpt-5.5
```

The runner first saves the draft response, then asks the reviewer to critique
resolver clarity, base-rate discipline, time-series/model prior use, update
justification, interval calibration, tail scenarios, coherence, and leakage.
The forecaster is then rerun with the draft and critique and must include a
public `Review disposition:` reasoning step in the final JSON. The draft,
review prompt, reviewer output, revision prompt, final response, parsed cells,
validation, and manifest are all activity artifacts. Only the final forecast is
scored; the review loop is a workflow variant that can be compared against
unreviewed runs later.

The reviewer Codex path does not enable web search by default; add
`--pre-submit-review-codex-search` only when the review should fetch additional
public context. The normal review mode should judge the draft, cited evidence,
and target spec.

## Time-series model-candidate preflight

For repeated numeric public series, run model candidates before asking the
agent to make an inside-view update. The shared schema is
`thesis_model_candidate_v1`: every candidate carries point, p10/p50/p90, 80%
and 90% intervals, interval method, train cutoff, calibration_n, history, and
walk-forward score metadata when enough history exists.

```bash
python3 scripts/run_time_series_models.py \
  --target-id fns.snap.overpayment_payment_error_rate.us.fy2026 \
  --target-period FY2026 \
  --history-json '[{"period":"2024","value":9.26},{"period":"2025","value":9.28}]' \
  --models persistence \
  --round-increment 0.1
```

With enough history and the Python `experiments` extra installed, include the
first open-source adapter:

```bash
uv run --extra experiments python scripts/run_time_series_models.py \
  --target-id example.series.2026 \
  --target-period 2026 \
  --history-file /tmp/history.json \
  --models persistence,statsmodels-local-level
```

`statsmodels-local-level` uses statsmodels SARIMAX(0,1,0) with drift and
native state-space prediction intervals. If a future adapter cannot produce
native intervals, it must wrap the point forecast with conformal, residual,
panel, or fallback-prior intervals and label `intervalMethod` accordingly.

## Activity artifacts

Every run writes a directory under `records/thesis-analyst/YYYY-MM-DD/` with:

- `prompt.md`
- `command.json`
- `stdout.txt` and `stderr.txt` when a command is used
- `codex_stdout.jsonl`, `codex_stderr.log`, `codex_events.jsonl`,
  `codex_last_message.txt`, and `codex_trace.json` when `--codex-model` or
  `--pre-submit-review-codex-model` is used
- `raw_response.txt`
- `draft_stdout.txt`, `pre_submit_review_stdout.txt`, and `revision_prompt.md`
  when pre-submit review is enabled
- `parsed_cells.json`
- `normalized_cells.json`
- `validation.json`
- model-candidate JSON from `scripts/run_time_series_models.py` when a
  repeated numeric series preflight is run
- `cells.with_activity.json`
- `manifest.json`

`cells.with_activity.json` carries `activityLog` refs for the prompt, raw
response, parsed/normalized cells, and validation report. When that file is
converted with `scripts/spawned_cells_to_ts.py`, the refs land in
`predictionRun.activityLog`, then in Thesis Log run records and `/log.json`.

## Convert to a generated catalog module

```bash
python3 scripts/run_thesis_analyst.py \
  --series ons.labour.unemployment_rate \
  --period 2026-Q4 \
  --codex-model gpt-5.5 \
  --write-ts site/src/data/almanac-examples/generated-thesis-agent.ts \
  --const-name GENERATED_THESIS_AGENT_CELLS
```

Generated modules should be imported into `site/src/data/forecast-cells.ts`
only after review. Do not hand-edit generated modules; rerun the agent or
replace the source artifact.
