# Wave-2 bill-conditional pairs progress

## State

CRP pair implemented and locally Python-verified; offline reachability sweep
in progress.

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
  coupling coverage. `ruff` passes and 78 focused Python tests pass.

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

- Sweep bill artifacts (and the offline stress branch if present) for other
  adapter-reachable, still-open candidates; commit `PAIRS-CANDIDATES.md`.
- Run broader available checks; site dependencies are currently absent, so
  `bun run test -- conditions.test.ts` cannot find `vitest` without a network
  install, which standing orders prohibit.
