# Gemini CLI backend lane notes

Branch: `feat/gemini-cli-backend` (no pushes)

## 2026-08-23 — contract and implementation reconnaissance

- Read `AGENTS.md`, `docs/thesis-vision.md`, `docs/cell-contract.md`,
  `docs/thesis-analyst-runner.md`, `docs/brier-lab.md`, and
  `agents/thesis-analyst/system.md` before changing the runner.
- Confirmed the worktree started clean at `1be3a5bc`, matching `origin/main`.
- Inspected the installed Gemini CLI 0.36.0 stream formatter after a live smoke
  attempt. The CLI emitted `init` and user `message` events before the sandboxed
  network request failed. The installed formatter confirms that assistant text
  is emitted as `message` events with `role: "assistant"`, `content`, and
  `delta: true`; the terminal `result` event carries `status` and simplified
  `stats`, including a `models` mapping.
- The live smoke attempt did not reach a model response because this execution
  sandbox blocks the Gemini API request (`TypeError: fetch failed`). The parent
  shell already contains `GEMINI_API_KEY`; no key value was printed or written.
- Implementation decision: pass the forecast prompt directly as the `-p`
  argument. The runner records `<prompt>` in `command.json`, so the prompt is
  retained only in `prompt.md`/the normal activity artifacts and command-line
  length remains comfortably below the platform limit for current Thesis
  prompts.
- Implementation decision: Gemini runs always use a temporary `HOME` with only
  the API-key auth selector and a separate temporary working directory. This
  prevents real-home OAuth selection and workspace settings from overriding
  auth; the v1 tradeoff is that Gemini cannot inspect repository files.
- Compatibility finding: `scripts/verify_custody.py` currently recognizes only
  Codex trace inventories. It must learn the Gemini inventory and allow mixed
  Gemini-forecaster/Codex-reviewer runs. Ticket replay remains Codex-only.
- Constraint note: the site activity-log TypeScript union lives under the
  explicitly excluded `site/src/data/**` tree. This lane will not edit that
  path; the runner/custody/docs contract will carry the new Gemini artifact
  types, and any later catalog-promotion type update must be a separately
  authorized change.

## Commits

- `673a45db` — Add Gemini CLI analyst backend.
- `69000e4e` — Pass Gemini models through analyst batches.
- `fbb34661` — Document Gemini CLI analyst runs.
- This final verification report is committed as the last coherent lane step;
  its hash is available in `git log` after the commit is created.

## 2026-08-23 — implementation and regression verification

- Added the native `gemini_cli` runner with direct `-p` prompt delivery,
  `--approval-mode plan`, `stream-json`, temporary API-key-selected `HOME`, and
  a separate temporary working directory.
- Added a Gemini stream parser that concatenates assistant message deltas,
  retains raw stdout, selects only `tool_use`/`tool_result` events for the
  normalized event stream, and carries terminal stats/model keys into the
  trace.
- Added exact-value key redaction in addition to the existing credential-shape
  redaction. `GEMINI_API_KEY` is added only to the Gemini child environment;
  `GOOGLE_API_KEY` and unrelated parent credentials are not inherited.
- Strengthened the workspace snapshot with a hash of `git diff HEAD` plus
  untracked file contents, excluding the run directory, so already-dirty files
  cannot be changed invisibly during a guarded stage.
- Added Gemini artifact custody and prefix-local backend selection, preserving
  mixed Gemini forecast/Codex review inventories while leaving ticket replay
  Codex-only.
- Added batch `--gemini-model`/`THESIS_GEMINI_MODEL` selection with ambiguity
  refusal and existing Codex fallback when no backend is selected.
- Added runner, parser, auth, OAuth-prompt, missing-binary, backend-exclusion,
  mutation, custody, batch, and credential-hygiene regressions.
- Verification: direct Ruff passed; Python compilation passed; `git diff
  --check` passed; `python3 -m pytest tests/test_thesis_analyst_runner.py
  tests/test_thesis_analyst_env_hygiene.py tests/test_ticket_mode.py` passed
  266 tests in 66.83 seconds.
- The prescribed `uv run --extra dev` wrapper could not initialize the
  protected user cache; an isolated offline cache then lacked the ruff wheel.
  The already-installed project tools were invoked directly instead.

## Final report

### Files touched

- `scripts/run_thesis_analyst.py:85-92,1556-1562,1788-1866,1987-2054,
  2344-2548,2655-2681,2960-2986,3900-3974,4139-4174` — Gemini binary/auth
  preflight, stream parser, strengthened workspace fingerprint, native runner,
  artifact sealing, runtime metadata, CLI selection, and ticket refusal.
- `scripts/run_thesis_batch.py:367-449,539-553` — non-ticket backend
  resolution, `THESIS_GEMINI_MODEL`, and Gemini flag pass-through without
  forwarding Codex-only options.
- `scripts/verify_custody.py:37-58,391-455` — required Gemini stage inventory,
  `gemini_cli` backend recognition, and cross-backend artifact refusal.
- `docs/thesis-analyst-runner.md:80-128,189-217,328-339` — invocation, auth,
  temporary `HOME`/cwd pitfalls, safety, batch behavior, runtime metadata,
  credential hygiene, and artifact documentation.
- `docs/cell-contract.md:31-52` — Gemini activity-artifact types in the public
  cell contract.
- `tests/test_thesis_analyst_runner.py:2019-2298,2624-2672,2813-2875` — fake
  CLI E2E, missing auth/binary, OAuth refusal, backend mutual exclusion,
  workspace mutation, custody, and parser coverage.
- `tests/test_thesis_analyst_env_hygiene.py:348-472` — backend-only key
  inheritance, temporary auth settings/cwd, exact-value redaction, and sealed
  artifact assertions.
- `tests/test_ticket_mode.py:406-448` — batch flag/environment pass-through and
  ambiguous-backend refusal; the existing ticket-policy tests also assert that
  Gemini cannot enter the attested Codex lane.
- `_LANE-NOTES.md` — implementation journal and this final report.

No files under `records/**`, `scripts/docket_series.json`,
`site/src/data/**`, `drafts/ledger-entries/**`, or `.github/workflows/**` were
changed.

### Interface and artifact result

- `scripts/run_thesis_analyst.py --gemini-model MODEL` is now one of the five
  exactly-one forecast sources alongside `--command`, `--codex-model`,
  `--response-file`, and `--mock-cell`.
- `scripts/run_thesis_batch.py --gemini-model MODEL` and
  `THESIS_GEMINI_MODEL=MODEL` select the same backend for non-ticket batches.
- `THESIS_GEMINI_BIN` overrides `PATH` lookup. `GEMINI_API_KEY` must be present
  in the parent environment and is added only to Gemini's child environment.
- The executed argv is `gemini -m MODEL --approval-mode plan -o stream-json -p
  PROMPT`; `command.json` replaces the prompt bytes with `<prompt>`, contains no
  environment values, and records environment variable names only.
- Gemini runs add `gemini_stdout.jsonl`, `gemini_events.jsonl`,
  `gemini_last_message.txt`, and `gemini_trace.json`. Tool-use and tool-result
  records land in `gemini_events.jsonl`; the untouched redacted stream remains
  in `gemini_stdout.jsonl`.
- Successful manifests record `agent.backend: "gemini_cli"`, the requested
  `agent.model`, and `agent.runtimeModel` from the `stats.models` key when the
  CLI supplies one.
- No `--pre-submit-review-gemini-model` was added. Pre-submit review remains on
  the existing Codex/custom reviewer paths; custody explicitly supports a
  Gemini forecast followed by a Codex review.

### Verification

- `ruff check scripts/run_thesis_analyst.py scripts/run_thesis_batch.py
  scripts/verify_custody.py scripts/thesis_records_to_comparisons.py
  tests/test_thesis_analyst_runner.py
  tests/test_thesis_analyst_env_hygiene.py tests/test_ticket_mode.py` — passed.
- `python3 -m py_compile scripts/run_thesis_analyst.py
  scripts/run_thesis_batch.py scripts/verify_custody.py` — passed.
- `python3 -m pytest tests/test_thesis_analyst_runner.py
  tests/test_thesis_analyst_env_hygiene.py tests/test_ticket_mode.py` — **266
  passed in 66.83 seconds**.
- `python3 -m pytest tests/test_record_integrity.py` — 25 passed; the three
  live-record tests failed before their assertions because optional pinned
  dependency `receipt==0.5.1` is not installed in this sandbox. The prescribed
  `uv --extra` path cannot populate it because the user uv cache is protected
  and outbound package access is disabled.
- `git diff --check origin/main` — passed.

New named regressions include:

- `test_gemini_model_run_captures_full_gemini_trace`
- `test_gemini_model_requires_api_key_with_exact_error`
- `test_gemini_model_requires_cli_binary_with_clear_error`
- `test_gemini_oauth_prompt_fails_closed_despite_valid_result`
- `test_gemini_model_is_mutually_exclusive_with_other_backends`
- `test_gemini_run_fails_closed_on_workspace_mutation`
- `test_parse_gemini_jsonl_concatenates_deltas_and_keeps_tool_events`
- `test_gemini_stage_gets_only_its_key_and_seals_redacted`
- `test_non_ticket_run_one_passes_gemini_model_from_flag_or_env`
- `test_non_ticket_batch_refuses_ambiguous_backend_selection`

### Real E2E result

The requested command was first invoked with its exact destination:

```text
/Users/maxghenis/ThesisInstitute/_gdm-experiments/2026-08-21/16-naep-2026-gemini-flash
```

This managed execution environment rejected directory creation there with
`PermissionError: [Errno 1] Operation not permitted` because that path is
outside its writable roots. The run was then repeated with every requested
forecast input unchanged and only `--out-dir` replaced by the writable:

```text
/private/tmp/16-naep-2026-gemini-flash
```

The parent `GEMINI_API_KEY`, real `/opt/homebrew/bin/gemini` 0.36.0, requested
`gemini-3.7-flash`, NAEP series/period, fast prompt, 900-second timeout, and the
exact supplied target-context JSON were used. The target context still reads,
verbatim, `"anchors": {"2024": 274}`; it was not edited.

The runner launched and sealed the real Gemini process, but this execution
sandbox blocks its outbound API request. Gemini returned `resultStatus:
"error"`, zero tokens/tool calls, and:

```text
[API Error: exception TypeError: fetch failed sending request]
```

The process therefore produced no assistant forecast JSON. The runner failed
honestly in the parse phase rather than manufacturing a cell or reaching the
anchor gate. `error.json` is, verbatim:

```json
{
  "phase": "parse",
  "message": "No JSON object or array found in agent output",
  "command": {
    "returnCode": 1,
    "timedOut": false
  }
}
```

There is no `validation.json` to quote because validation was never reached.
The requested validation report, verbatim as an existence result, is:

```text
validation.json
NOT CREATED
```

The failed-run trace is nevertheless complete and useful: `gemini_trace.json`
records `backend: "gemini_cli"`, requested/runtime model
`gemini-3.7-flash`, `approvalMode: "plan"`, `oauthPromptDetected: false`, and
`workspaceMutations: []` is recorded in `command.json`. A direct custody check
returned:

```text
custody OK: /private/tmp/16-naep-2026-gemini-flash mode=analyst inventory=v2 status=complete artifacts=10
```

All 12 files in that real run directory were scanned against the in-memory API
key; the result was `secret_hits=[]`. No secret value was printed, journaled,
or committed. Nothing was pushed.

STOP
