# Wave-2 bill-pair reachability audit

Audit date: 2026-08-02. This is an offline code-and-artifact audit; it makes no
claim that an endpoint was fetched during this work.

## Method

I ran the proposal-only mapper in `scripts/map_bill_metrics.py` against every
top-level `bills/*.json` artifact and the current
`scripts/docket_series.json`. I also swept all 28 `bills/stress-*.json`
artifacts directly from the already-fetched `origin/hack/stress-bills` Git
object (without checking out or copying its `records/**`). The stress corpus
itself reports only three non-null series hints; I confirmed those three
against the current docket.

Mapper reachability is necessary but not sufficient. For every apparent hit I
then checked:

1. the docket entry's exact `sourceBinding.adapter`;
2. that the adapter family is one of the user-authorized registered families;
3. the resolver's current series/period admission path in
   `scripts/resolve_pending.py`;
4. whether the bill still has an open legislative condition; and
5. whether the metric exists under both legal arms and has a release window
   after the condition deadline.

The mapper only accepts an exact hint or a dot-descendant of a hint
(`match_registered_series`, `scripts/map_bill_metrics.py`). Two known mappings
need explicit review rather than a mapper hit: the older Farm Bill artifact
has no `series_hint` on its CRP metric, and S.3596 uses the historical hint
`irs.soi.additional_child_tax_credit_returns` while the reviewed docket series
is `irs.actc.total_claims`.

## Adapter-reachable bill metrics today

| Bill | Metric | Registered series | Adapter / resolving code path | Pending legislation? | Pair disposition |
|---|---|---|---|---|---|
| Farm Bill 2.0 discussion draft | Total active CRP enrolled acres in the fixed September 30, 2027 monthly snapshot | `usda.fsa.crp.enrolled_acres_total` | `fsa-crp-monthly-summary`; `FSA_CRP_ADAPTERS`, `fsa_crp_fetch_period`, and the `fsa_crp` branch of `pending_adapter_refs` in `scripts/resolve_pending.py` | **Yes.** Artifact status is a Senate Agriculture Committee discussion draft; the condition remains open through 2027-09-30. | **Implemented in this branch.** Two non-complement arms, because enactment of a different FY2027–31 ceiling makes both exact premises false. |
| S.3596, Stronger Start for Working Families Act | IRS SOI Publication 1304 total ACTC claim count for TY2027 | `irs.actc.total_claims` | `irs-soi-pub1304`; `IRS_SOI_PUB1304_ADAPTERS`, `irs_soi_pub1304_fetch_year`, and the `irs_soi_pub1304` branch of `pending_adapter_refs` | **Yes.** Artifact status is introduced in Senate; the legal condition is open through 2027-12-31. | Already implemented by merged PR #114. Not a second wave-2 pair. |
| H.R.1 stress artifact | Department of Defense prime-award obligations | `usaspending.dod.prime_award_obligations` | `usaspending-api`; `USASPENDING_ADAPTERS` and the `usaspending` branch of `pending_adapter_refs` | **No.** The stress artifact analyzes House-engrossed H.R.1, and the repository context identifies H.R.1 as enacted. | Rejected: no open enactment condition. An unconditional target is outside this lane. |
| H.R.1 stress artifact | Unique Department of Defense prime-contract recipients | `usaspending.dod.unique_prime_contract_recipients` | `usaspending-api`; same registered family and resolver branch | **No.** Enacted legislation. | Rejected for the same reason. |

## Rejected near-matches and gaps

- The H.R.1 stress artifact also hints `fns.snap.total_persons`, but its docket
  binding is `generic-url`, which is not one of the authorized adapter families
  for this task. It is not counted as reachable today for this lane.
- The S.3596 child Supplemental Poverty Measure metric has no matching docket
  series or authorized adapter path. The already-recorded refusal also notes
  unresolved release-date/vintage problems; it is not a clean second pair.
- The FRONTIER Act artifact contains 38 metric hints, but none maps to a
  current docket series. Many describe bill-created or nonstandardized
  Commerce/IVO publications, so treating them as zero or as a nearby proxy
  would violate the symmetric, automatically resolvable pair requirement.
- Farm Bill 2.0 contains USAspending, QCEW, CMS, and other possible data-source
  prose, but no additional metric carries an exact registered series hint and
  a clean two-arm legal/measurement contract. Bill-created products that may
  exist only after enactment are asymmetric missing-data outcomes, not valid
  pairs.
- The remaining 27 stress artifacts have no registered-series hints. The
  corpus synthesis says the only three emitted hints are the SNAP and two DoD
  series on H.R.1, matching this sweep.

## Decision

No second pair is implemented. The only clean, still-open, newly actionable
candidate is the CRP pair shipped here. S.3596 is already registered, H.R.1 is
enacted, and every other apparent metric lacks an exact currently admitted
series, an authorized adapter, a symmetric observable outcome, or an open
condition.
