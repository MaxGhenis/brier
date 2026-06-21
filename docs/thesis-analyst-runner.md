# Thesis analyst runner

`scripts/run_thesis_analyst.py` is the local Axiom-style runner for forecast
cells. It turns a target spec into a complete run directory, then feeds the
validated cell into the existing spawned-cell converter.

Before changing the runner, read [`docs/thesis-vision.md`](thesis-vision.md).
The runner exists to make agent-only public-data forecasts reproducible:
prompt, command, stdout/stderr, raw response, normalized forecast, validation,
manifest, and later score should remain linked.

## Headless Codex run

```bash
python3 scripts/run_thesis_analyst.py \
  --series ons.labour.unemployment_rate \
  --period 2026-Q4 \
  --command "codex --search exec --ignore-user-config -m gpt-5.5 -c 'service_tier=\"fast\"' --sandbox read-only -C {repo_root} -"
```

The prompt is sent on stdin. The command may also reference `{prompt_path}` and
`{repo_root}`:

```bash
python3 scripts/run_thesis_analyst.py \
  --series ons.labour.unemployment_rate \
  --period 2026-Q4 \
  --command "codex exec -C {repo_root} -"
```

Agent commands default to a 600 second timeout. Use `--timeout-seconds` to make
smoke tests shorter or longer. A timeout writes `command.json`, `stdout.txt`,
`stderr.txt`, `raw_response.txt`, `error.json`, and `manifest.json` with
`ok: false`.

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

## Activity artifacts

Every run writes a directory under `records/thesis-analyst/YYYY-MM-DD/` with:

- `prompt.md`
- `command.json`
- `stdout.txt` and `stderr.txt` when a command is used
- `raw_response.txt`
- `parsed_cells.json`
- `normalized_cells.json`
- `validation.json`
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
  --command "codex --search exec --ignore-user-config -m gpt-5.5 -c 'service_tier=\"fast\"' --sandbox read-only -C {repo_root} -" \
  --write-ts site/src/data/almanac-examples/generated-thesis-agent.ts \
  --const-name GENERATED_THESIS_AGENT_CELLS
```

Generated modules should be imported into `site/src/data/forecast-cells.ts`
only after review. Do not hand-edit generated modules; rerun the agent or
replace the source artifact.
