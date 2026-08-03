# Stress corpus promotion progress

## State

- Branch: `promote/stress-substantive` (from `origin/main`).
- Input: `.lane-input/bills/` (untracked; must remain untracked).
- Scope: validate and promote exactly the 11 requested substantive stress artifacts, in the requested order.
- Artifact contents must remain byte-for-byte identical; only destination filenames change.

## Done

- Confirmed `PROGRESS.md` did not previously exist.
- Confirmed the worktree began clean apart from untracked `.lane-input/`.
- Inspected the tracked contract exemplar `bills/farm-bill-2-0.json` and series registry `scripts/docket_series.json`.

## Next

- Build a temporary offline structural checker under `scratch/`.
- For each requested artifact in order: copy byte-for-byte, run and record every required check, and commit it if all checks pass.
- Delete the temporary checker, add a final landed/failed/integrator summary, and commit the completed ledger.

## Per-file checks

Results will be appended here in promotion order.
