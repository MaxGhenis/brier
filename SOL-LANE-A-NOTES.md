# Lane A — publication trust boundary

## What changed

This lane closes re-audit findings N2, N3, and N4 on the scheduled roll
pipeline.

- `scripts/docket_publication.py` now derives authority from the exact batch
  manifest rather than caller-provided path prefixes. A bundle may contain only
  the exact batch file, canonical target snapshots named by its targets, and
  data files beneath the exact run directories named by its results.
- Publication is append-only. A path already present in `HEAD` or in the
  publisher checkout may be restated only when the bytes are identical.
  Different bytes fail before semantic validation and are checked again at
  apply time.
- Chain state, resolution markers, workflow/control paths, source-code
  extensions, executable modes, symlinks, un-inventoried files, and paths
  outside the invocation are rejected. A new run's `custody_root.json` is the
  one custody-root exception because the publisher must verify that run; prior
  custody roots cannot enter another invocation's exact run scope.
- Bundle files are data only (`.json`, `.jsonl`, `.log`, `.md`, `.txt`). The
  publisher recreates/verifies preregistration TypeScript from canonical target
  snapshots, then runs trusted `spawned_cells_to_ts.py` and
  `generate_ledger_targets.py` through `register_wave.py`. The existing
  `allowedHosts ∪ sourceUrl host` check remains unchanged.
- Target registration is now `thesis_target_registration_v2`, one immutable
  snapshot per target. `registeredAtUtc` is a real second-precision UTC instant
  inside the snapshot. `targetContentHash` covers `{schemaVersion, targets}`
  and intentionally excludes that operational timestamp.
- Retries locate the existing snapshot by content hash, require its canonical
  bytes and either the exact preregistration block or the deterministic
  published block to match, and reuse its original timestamp/path. Mixed
  batches can therefore combine retried targets with new targets without
  changing a prior target's hash. Empty target sets write nothing.
- After the privileged push, each ephemeral target is stamped with the commit
  that introduced its snapshot. Successful cells, failed manifests, successful
  manifests, and batch results retain `registrationCommit`,
  `targetContentHash`, `targetRegistrationPath`, `registeredAtUtc`, and the
  harness `runStartedAt` where applicable.
- Publisher validation compares the untrusted batch against a separately
  downloaded privileged target artifact. It requires the registration commit
  to have introduced the exact snapshot, be an ancestor of publisher `HEAD`,
  have both author and committer instants contemporaneous with
  `registeredAtUtc`, and strictly predate the run start. Canonical JSON
  comparisons prevent Python's `true == 1` behavior from confusing trusted
  numeric contracts with untrusted booleans.
- Each run directory must exactly equal its manifest artifact inventory plus
  `custody_root.json`; extra unreferenced data is rejected. Wave module names
  use the full batch SHA-256, and trusted generation goes through a temporary
  candidate that can only create a new module or restate an identical one.
  It never overwrites a prior wave.
- Finalized ledger-target TypeScript is regenerated from the canonical target
  snapshot and validated cell JSON. A retry accepts it only when the full
  generated block is deterministic and byte-identical; the existing
  `allowedHosts ∪ sourceUrl host` contract check still runs unchanged.
- The old early records push is gone. Records and trusted generated TypeScript
  are committed and pushed together only after bundle validation, application,
  complete chain/custody verification, and site gates. Every rebase reruns the
  trusted generators and requires a clean diff, then reruns the bundle, chain,
  custody, test, and build checks before a bounded push retry.
- Producer jobs expose their exact artifact names, so GitHub's "re-run failed
  jobs" behavior does not accidentally look for the new attempt number. A
  byte-identical already-published retry is an idempotent success and can
  resume a failed deployment canary or recorder dispatch.

## Exact workflow graph

```text
register (contents:write; trusted checked-in scripts only)
  checkout main with full history
  → adopt registry entries
  → compute roll targets
  → capture registeredAtUtc
  → write canonical per-target snapshots + preregistration TS
  → commit
  → clean-tree rebase
  → global chain+custody verification and complete registration binding under
    that rebased HEAD
  → push (max 3) / compare local SHA with git ls-remote
  → promote the already-verified candidate binding metadata
  → upload privileged targets JSON

generate (contents:read; untrusted analyst/Codex job)
  needs register
  → checkout the exact remotely verified source SHA
  → independently verify privileged target bindings
  → run analyst batch
  → stage exact-scope data-only bundle
  → upload bundle

publish (contents:write)
  needs register + generate, always evaluates failures/no-op
  → checkout current main with full history
  → independently download privileged targets and untrusted bundle
  → validate entire bundle before applying any file
  → append-only apply
  → verify full record chain and every custody root
  → regenerate publication TS using publisher-checkout code
  → site test + build
  → commit records + generated TS
  → clean-tree rebase / trusted regeneration + clean-diff check / revalidate
    bundle / reverify chain+custody / retest + rebuild / push (max 3)
  → verify remote SHA through the existing deployment canary and dispatch the
    RFC 3161-backed record workflow; failed-only batches dispatch the
    recorder's ancestor-safe path without waiting for a nonexistent new live
    forecast deployment
```

The batch path now includes both `github.run_id` and `github.run_attempt`, so a
workflow retry cannot collide with the earlier attempt under append-only rules.

## No-target and retry behavior

- No new targets: `register` reports `count=0`; it creates no snapshot, commit,
  or artifact. `generate` is skipped and `publish` succeeds as a no-op.
- Exact retry: the existing snapshot and TypeScript must be byte-identical. No
  registration commit is created; the target binds to the original snapshot's
  introducing commit while generation checks out the current verified `main`.
- Retry plus new target: each target carries its own snapshot/hash/introducing
  commit, while the job also exposes a canonical registration-set hash.
- Any partial/mismatched retry fails closed. The workflow never repairs or
  rewrites a prior registration.

## Integrator / live-fire notes

- No new secret is required. The jobs use the existing `github.token`,
  `OPENAI_API_KEY`, and deployment/recording configuration.
- Keep force-pushes disabled and branch protection enabled on `main`; the
  pushed registration commit is the timing witness. The later record workflow's
  RFC 3161 witness supplies the external upper bound that Git itself lacks.
- The workflow token must retain permission to push the trusted registration
  commit and the later publication commit directly to protected `main`, as the
  existing workflow already did.
- First live run caveat: legacy v1 snapshots do not contain `registeredAtUtc`.
  A target with no conflicting preregistration block receives a fresh v2
  registration. If a legacy v1 preregistration block already exists for the
  same unpublished `dataPointId`, the new code deliberately fails instead of
  rewriting it; inspect that target manually and advance to a fresh target
  period.
- The near-duplicate `prospect-docket.yml` now inherits the strict data-only,
  exact-scope, append-only bundle policy and trusted snapshot-to-TS
  materialization through the shared scripts. It does **not** yet have the new
  pre-analyst privileged registration commit; a separate prospect workflow
  migration is still needed to give prospect-created targets the full N4 Git
  timing guarantee.
- Workflow YAML was parsed locally and passes `actionlint`, but cannot be
  executed end to end without GitHub/network access. The first live fire should
  confirm protected-branch token behavior, producer-bound artifact/job-output
  wiring across "re-run failed jobs," post-push stamp recovery, and the
  failed-only recorder dispatch.

## Verification performed

- Required focused tests under installed Python 3.12: `47 passed`, including
  overwrite, chain-file, TypeScript, outside-scope, identical-restatement,
  executable-mode, Git ancestry/chronology, backdating, retry, no-op, and
  snapshot-to-TypeScript regeneration cases.
- Focused tests including runner binding/collision regressions: `68 passed`.
- Full non-figure Python suite: `285 passed, 1 skipped`.
- Full Python suite with writable Matplotlib/cache directories and the `Agg`
  backend: `302 passed, 1 skipped`.
- `ruff`, `actionlint`, `git diff --check`, the complete record-chain verifier,
  and all eight current custody roots pass.
- The exact requested `uv --with pytest` command cannot run in this networkless
  sandbox: the default cache is read-only, and a writable cache then attempts to
  fetch pytest from PyPI. The equivalent already-installed Python 3.12 pytest
  invocation was used instead.
- Site dependencies are not installed in this networkless clone, so the local
  site test/build was not repeated; both remain mandatory before every publish
  push in the workflow.

## Residual risk

The boundary still relies on trusted code and protected-branch administration.
An administrator who can alter the workflow/token policy can subvert the
privileged registrar, and Git commit metadata is not independently timestamped
until the subsequent record run. The design makes ordinary analyst output
incapable of doing so and makes operator backdating require changing protected
trusted history or the privileged workflow rather than editing an artifact.
Bundle file-count and byte-size caps remain a resource-exhaustion hardening
opportunity (integrity policy is fail-closed), and the workflow's third-party
actions remain version-tagged rather than pinned to immutable action SHAs.
