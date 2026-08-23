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

- Pending local commits after the implementation audit.

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

- Pending implementation, verification, and the required real run.
