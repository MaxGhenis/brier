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

1. **PASS — `stress-119hr1eh.json` → `one-big-beautiful-bill-hr1-119.json`.** JSON parsed; destination bytes identical (SHA-256 `d6860df7665fe48cb53b96ce0b80c53d4ca9666e3b5c7413125a16d5c17ee377`); all six required bill info fields present with exemplar-compatible types; 13 provisions and 36 metrics have the contract shapes; all stance goal indexes are in range; all 3 nonempty `series_hint` values occur in `scripts/docket_series.json`.
2. **PASS — `stress-119hr608ih.json` → `cover-act-hr608-119.json`.** JSON parsed; destination bytes identical (SHA-256 `b3bd86e7f700be90c6e793b65c3d5567cac5d3947cf5d02fe1a812caa6850e50`); all six required bill info fields present with exemplar-compatible types; 3 provisions and 9 metrics have the contract shapes; all stance goal indexes are in range; no nonempty `series_hint` values required registry lookup.
