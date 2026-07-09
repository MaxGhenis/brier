# SOL-F11: CI generation/publication trust boundary

## Trust-boundary diagram in words

For both docket loops, the data flow is:

1. A **generate** job checks out `main` without persisted credentials and with
   read-only repository permission.
2. Generate computes targets, runs Codex and the analyst batch, and copies only
   the allowlisted repository delta into a workflow artifact. Prospect may copy
   `records/**`; roll may copy `records/**` and
   `scripts/docket_series.json` so proven-series adoption still works. The
   batch manifest travels inside the records delta. The same high-confidence
   token scan runs before upload so an obvious leaked key does not enter the
   artifact service.
3. The workflow-artifact boundary is the trust boundary. Nothing in the
   generate checkout can push, open an issue, or dispatch another workflow.
4. A separate **publish** job starts from a fresh `main` checkout, also with
   `persist-credentials: false`, and downloads the artifact.
5. Before applying the delta, publish enforces the path and hash inventory,
   rejects symlinks and path traversal, replays the shared forecast-cell
   validator against every batch-declared `cells.with_activity.json`, checks
   that the replayed pass/fail status matches both manifests, verifies each
   run's custody root, and rejects unreferenced cell payloads. Failed traces
   may remain records only when the independent replay confirms they failed;
   `register_wave.py` can select only independently passing results.
6. Publish stages the records-first commit and scans the exact Git index bytes
   for common GitHub, OpenAI, AWS, and Slack token shapes and private keys.
   It repeats that scan for the generated publication commit.
7. Only explicit push steps receive the write token. Publication then keeps
   the F13 sequence: records-first push, content-hashed `register_wave` name,
   site test, commit, rebase, retest, push, production-build canary, and only
   then recorder dispatch. The shared `docket-writers` concurrency group is
   unchanged.

`resolve-and-rebuild.yml` remains a single trusted job because it does not run
the analyst. Its checkout no longer persists credentials, and only its push
step receives an explicit write token. Its non-skip resolution marker and
production-build canary remain in place. `record-forecasts.yml`, including its
canary-ancestry gate, is untouched.

## Secret visibility

- Roll `generate`: the `OPENAI_API_KEY` repository secret is present in the
  job environment because Codex and its review run need it. The checkout
  action gets the automatic token with `contents: read` internally, but does
  not persist it and no `GH_TOKEN` or `GITHUB_TOKEN` is exported to shell
  steps. No deploy hook is available.
- Prospect `generate`: identical to roll generate: `OPENAI_API_KEY`, plus an
  internal read-only checkout token that is not persisted. No write token,
  issue token, recorder-dispatch token, or deploy hook is exported.
- Roll and prospect `publish`: no `OPENAI_API_KEY`. The automatic
  `${{ github.token }}` is exported as `GH_TOKEN` only to each push step, the
  canary-gated recorder-dispatch step, and the failure-alert step. The
  `MANUAL_DEPLOY_HOOK_URL` secret is exported only to the canary/dispatch step.
  Checkout credentials are not persisted.
- Resolve job: `ARCH_DATA_TOKEN` is exported only while resolving official
  prints; `${{ github.token }}` is exported only to the marker push and failure
  alert; `VERCEL_DEPLOY_HOOK_URL` is referenced only by the rebuild step.
  Checkout credentials are not persisted.
- Record workflow: unchanged by F11.

The Codex install is pinned to `@openai/codex@0.144.0` in both generate jobs.
That is the exact version resolved by the operator's current Bun global install
when this change was prepared (`codex-cli 0.144.0`); no live registry lookup was
available in the offline sandbox.

## Residual risks

- `OPENAI_API_KEY` remains visible to the analyst process and to the Codex
  credential store inside generate. This is acceptable for now because the
  model call requires it and the job has no repository, issue, action-dispatch,
  or deploy authority. Key scoping, spend limits, and rotation remain the
  containment controls for abuse of the model account itself.
- The regex secret scan is deliberately dependency-free and high confidence.
  It can miss unknown, reformatted, encrypted, or split credentials. It is a
  backstop, not a replacement for provider-side secret scanning and rotation.
- Publish executes trusted repository validation and generation code against
  attacker-influenced JSON. Path allowlisting, regular-file checks, custody
  verification, and JSON parsing narrow that surface, but bugs in those trusted
  scripts remain a risk.
- Artifact hashes detect transfer corruption or inventory changes, but the
  hashes originate in generate. Trust comes from independent validator replay,
  custody verification, path restrictions, and secret scanning in publish,
  not from those hashes alone.
- Failed model traces remain publishable as failed records after independent
  validation, by design. They are public forensic data and are excluded from
  wave registration; the scanner still gates their committed bytes.

## Integrator live-fire checklist

Run these only after the branch lands on `main` and repository secrets are
available:

1. Dispatch roll once with a small cap:
   `gh workflow run roll-docket.yml --ref main -f max_targets=1`.
2. Confirm roll `generate` shows `contents: read`, produces exactly one named
   artifact, and has no credential in `.git/config`. Confirm `publish`
   downloads it, reports validator/custody and both secret-scan results, makes
   the records-first commit, and preserves the post-rebase site retest.
3. Dispatch prospect once with bounded work:
   `gh workflow run prospect-docket.yml --ref main -f count=1 -f mine_max=1 -f focus=health`.
4. Confirm the prospect command log contains an argv-style invocation (no
   `eval`), then verify the same artifact, validation, records-first,
   rebase/retest, push, and canary sequence.
5. For each docket run that publishes a cell, confirm the content-hashed wave
   name, production `build.json` SHA match, and a canary-gated
   `record-forecasts.yml` dispatch. Confirm the recorder's ancestry gate still
   passes; do not bypass it by dispatching before the canary.
6. Dispatch the resolver once:
   `gh workflow run resolve-and-rebuild.yml --ref main`. If it appends a fact,
   confirm the non-skip marker is pushed using only the explicit push-step
   token and that the deploy canary reaches the marker SHA. If there is no
   pending official print, confirm the no-op path exits cleanly.
7. Inspect both docket artifacts and the resulting commits: only the
   allowlisted record delta (plus roll's registry update), generated site data,
   and expected import/target wiring should appear. No scoring data or other
   site data should change.
