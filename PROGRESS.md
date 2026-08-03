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
3. **PASS — `stress-119hr5595ih.json` → `remit-act-hr5595-119.json`.** JSON parsed; destination bytes identical (SHA-256 `fc32c9e899f7bcb107f790939eb9db2c64ac72e383fc44af01d19f245b3b0d51`); all six required bill info fields present with exemplar-compatible types; 1 provision and 3 metrics have the contract shapes; all stance goal indexes are in range; no nonempty `series_hint` values required registry lookup.
4. **PASS — `stress-119s1082is.json` → `safeguarding-medicaid-s1082-119.json`.** JSON parsed; destination bytes identical (SHA-256 `c3cc444c9aa30cee0eb334d345fa5d60d3a8fa62301d2c98a76d172a692df4ea`); all six required bill info fields present with exemplar-compatible types; 3 provisions and 8 metrics have the contract shapes; all stance goal indexes are in range; no nonempty `series_hint` values required registry lookup.
5. **PASS — `stress-119s2718is.json` → `cdfi-fund-s2718-119.json`.** JSON parsed; destination bytes identical (SHA-256 `5f3eacbde985968e05cfc33157965a98be0320e8ae5816689c3a9d5f82221250`); all six required bill info fields present with exemplar-compatible types; 1 provision and 3 metrics have the contract shapes; all stance goal indexes are in range; no nonempty `series_hint` values required registry lookup.
6. **PASS — `stress-119hr978ih.json` → `superior-national-forest-hr978-119.json`.** JSON parsed; destination bytes identical (SHA-256 `a11fdc25d099e3e3722714d0298d020f21525bed848bf885a53cc8d8e1af3b19`); all six required bill info fields present with exemplar-compatible types; 3 provisions and 7 metrics have the contract shapes; all stance goal indexes are in range; no nonempty `series_hint` values required registry lookup.
7. **PASS — `stress-119s767is.json` → `hidta-enhancement-s767-119.json`.** JSON parsed; destination bytes identical (SHA-256 `90d38926f476921fa276b1882501bbf68c75e64ca81d375c7018f430ac6e6562`); all six required bill info fields present with exemplar-compatible types; 3 provisions and 7 metrics have the contract shapes; all stance goal indexes are in range; no nonempty `series_hint` values required registry lookup.
