# Wave-2 bill-conditional pairs progress

## State

Implementation and offline reachability audit complete; final broad checks in
progress.

## Done

- Confirmed the worktree is clean and `PROGRESS.md` did not already exist.
- Read the repository forecasting, registration, resolution, scoring, and
  analyst-method operating documents required by `AGENTS.md`.
- Located the merged S.3596 conditional-pair pattern, the CRP docket entry,
  the farm-bill artifact, the condition registry/tests, and the offline bill
  metric mapper.
- Registered a two-arm target for the September 2027 CRP Monthly Summary and
  wired it to the farm-bill page as pending (no forecast wave is claimed).
- Extended conditional-pair seeding/reauthentication to the CRP adapter's
  canonical monthly `YYYY-MM` period and taught the existing FSA resolver
  route to accept the pair's condition-token suffix. No adapter definition or
  `ADAPTERS` registry was added or modified.
- Added roll-docket, resolver-routing, condition-registry, and docket/registry
  coupling coverage. `ruff` passes and 85 focused mapper, roll-docket, and FSA
  adapter Python tests pass.
- Swept all three branch bill artifacts and all 28 artifacts on the fetched
  `origin/hack/stress-bills` branch with the merged mapper plus manual adapter
  admission checks. Results and rejections are in `PAIRS-CANDIDATES.md`.
- Rejected a second pair: S.3596 is already registered; H.R.1's two authorized
  USAspending hits are enacted/unconditional; SNAP uses an unauthorized
  `generic-url` binding; all remaining metrics lack an exact admitted series,
  an open condition, or a symmetric observable outcome.

### CRP period and release-window decision

The bill artifact itself says to forecast “FSA active CRP enrolled acres at
September 30 in FY2027–31” and separately warns that 27 million acres is a
ceiling, not a target (`bills/farm-bill-2-0.json`, first provision). The first
period the proposed FY2027–31 ceiling bears on is therefore the September 2027
monthly snapshot (`2027-09`), not calendar year 2027 and not an annual
aggregate. The registered resolver is month-only: `pending_adapter_refs` in
`scripts/resolve_pending.py` admits the FSA family only as `period_type ==
"month"`, and its PDF selector/parser require `YYYY-MM`.

The expected release window is 2027-12-01 through 2027-12-31, strictly after
the 2027-09-30 legal-condition deadline. This uses the repository's verified
publication evidence in `docs/anchor-verifications.md`: the April 2026
summary was posted under FSA's July 2026 files path and the integrator recorded
the real lag as approximately three months. The by-date is the window end; no
exact release day is invented.

### CRP arm design

The arms are deliberately **not** declared complements. A farm bill could set
an FY2027–31 ceiling other than exactly 27,000,000 acres. In that intermediate
legal state, both “27 million enacted” and “no FY2027–31 ceiling enacted” are
false, so neither forecast should score. `conditions.ts` records that
rationale and tests assert both `complementOf` fields are absent.

## Next

- Ran the available broader Python checks. Site dependencies are currently absent, so
  `bun run test -- conditions.test.ts` cannot find `vitest` without a network
  install, which standing orders prohibit.
- Final handoff: report the shipped/rejected set and verification limits.

# Series-ingestion wave 1 progress

The Wave-2 log above was inherited from the mapper branch and is retained
verbatim. This is the fresh progress section for thesis#123; it does not
rewrite or erase the earlier lane's record.

## State

- Branch: `feat/series-ingestion-wave1`, based on the mapper branch at
  `3cca0795`.
- Evidence boundary: repository artifacts only. Network access was not used.
- Every proposed product, URL pattern, cadence, unit, field, and query that was
  not already proved by repository material is marked `UNVERIFIED` with an
  integrator procedure.
- Adapter eligibility is exact-stem based. A parser for a different dataset
  from the same publisher does not make a request admission-ready.
- The inherited `PROGRESS.md` made a fresh root file impossible without
  clobbering prior work, so this additive section is the task-owned log.

## Worklist commits

| Bill artifact | Metrics | Request files | No-series rows | Existing admitted mappings | State |
|---|---:|---:|---:|---:|---|
| `one-big-beautiful-bill-hr1-119.json` | 36 | 43 | 6 | 4 (one lacks an executor) | complete |
| `cover-act-hr608-119.json` | 9 | 4 | 7 | 0 | complete |
| `remit-act-hr5595-119.json` | 3 | 1 | 2 | 0 | complete |
| `safeguarding-medicaid-s1082-119.json` | 8 | 5 | 5 | 0 | complete |
| `cdfi-fund-s2718-119.json` | 3 | 0 | 3 | 0 | complete |
