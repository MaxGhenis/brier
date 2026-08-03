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
| `superior-national-forest-hr978-119.json` | 7 | 0 | 7 | 0 | complete |
| `hidta-enhancement-s767-119.json` | 7 | 4 | 4 | 0 | complete |
| `future-networks-hr2449-119.json` | 2 | 0 | 2 | 0 | complete |
| `flraa-medevac-s2075-119.json` | 3 | 1 | 2 | 0 | complete |
| `sba-disaster-fairness-hr1021-119.json` | 8 | 5 | 6 | 0 | complete |
| `flare-act-s1188-119.json` | 2 | 1 | 1 | 0 | complete |

## Wave-1 admission gate

**Result: zero new docket entries admitted.** This is a fail-closed outcome,
not an omitted implementation step.

- 51 request files say `adapterFamily: NONE-existing` because the current
  resolver has no compatible parser/spec for the named official product.
- Four ALFRED candidates (`bea.ita.personal_transfer_payments`, BEA private
  nonresidential investment, BEA R&D investment, and EIA vented/flared gas)
  have neither an exact current `ALFRED_ADAPTERS` stem nor an offline-verified
  FRED ID/transform/first-print history.
- Four USAspending candidates are not among the six reviewed
  `USASPENDING_ADAPTERS` stems. Their agency/account/program filters are still
  `UNVERIFIED`; the DoD parser must not be generalized by name similarity.
- Five workbook candidates require new table-specific parsing. The current
  IRS Publication 1304 executor is hard-coded to `irs.actc.total_claims` and
  cannot parse other IRS tables or SBA workbooks today.
- The current CMS executor covers only two Care Compare nursing-home datasets;
  it cannot parse CMS-64, Medicaid Data API, PERM, or future statutory reports.
- The H.R. 1 mappings to `usaspending.dod.prime_award_obligations`,
  `usaspending.dod.unique_prime_contract_recipients`, and the child-credit
  portion of `irs.actc.total_claims` are already admitted/executable, so no
  duplicate entries were authored. `fns.snap.total_persons` is already in the
  docket but remains bound to `generic-url` with no resolver executor; that is
  an explicit integrator work item, not a claimed admission.

Because no request cleared exact adapter identity and an executable source
binding, this phase makes no changes to `scripts/docket_series.json`,
`docs/anchor-verifications.md`, or registry/prospect binding tests. Anchors
also remain unverified, but they could have been omitted under the task's
admission rule and were not treated as the deciding gate. There are no new rows
for those surfaces to describe or validate, and no target may roll from this
wave until a later reviewed admission supplies them.

## Final per-bill metric map

This table accounts for all 88 substantive metrics in the 11 promoted bill
artifacts. Request and no-series filenames are relative to
`drafts/ledger-ingestion/`. A request is worklist evidence only: none of the
request rows below is admitted. Where a metric names several outcomes but only
one has a plausible recurring product, the request note preserves that partial
coverage rather than implying that the concept resolves the whole metric.

### One Big Beautiful Bill Act (H.R. 1)

| Metric | Proposed series | Adapter family | Request / admission / no-series state |
|---|---|---|---|
| Direct participation | `fns.snap.total_persons` | `generic-url` (no executor) | Existing docket entry; needs a reviewed executor before any roll |
| Fiscal delivery | `fns.snap.total_benefits`; `fns.snap.average_benefit_per_person` | `NONE-existing` | `fns-snap-total-benefits.json`; `fns-snap-average-benefit-per-person.json` |
| Statutory trigger and payment accuracy | `fns.snap.total_payment_error_rate` | `NONE-existing` | `fns-snap-total-payment-error-rate.json`; cost-share tiers remain a derived concept |
| Agricultural program inputs | `usda.fsa.arc_plc.additional_base_acres_allocated`; `usaspending.usda.selected_rural_program_obligations` | `NONE-existing`; `usaspending-api` | `usda-fsa-arc-plc-additional-base-acres-allocated.json`; `usaspending-usda-selected-rural-program-obligations.json` |
| Honest employment gap | — | — | `no-series.ndjson` |
| Federal contract obligations | `usaspending.dod.prime_award_obligations` | `usaspending-api` | Existing admitted and executable docket entry; no duplicate authored |
| Supplier-base breadth | `usaspending.dod.unique_prime_contract_recipients` | `usaspending-api` | Existing admitted and executable docket entry; no duplicate authored |
| Honest capability gap | — | — | `no-series.ndjson` |
| Direct Loan volume by type | `ed.fsa.direct_loan.disbursement_volume_by_type` | `NONE-existing` | `ed-fsa-direct-loan-disbursement-volume-by-type.json`; borrower counts require a separate count-unit concept if verified |
| Repayment performance | `ed.fsa.direct_loan.portfolio_by_repayment_plan_status` | `NONE-existing` | `ed-fsa-direct-loan-portfolio-by-repayment-plan-status.json` |
| Pell recipients and outlays | `ed.pell.recipients`; `ed.pell.outlays` | `NONE-existing` | `ed-pell-recipients.json`; `ed-pell-outlays.json` |
| Institutional reimbursements | — | — | `no-series.ndjson` |
| Program rescissions and obligations | `usaspending.energy_commerce.title_iv.named_account_obligations` | `usaspending-api` | `usaspending-energy-commerce-title-iv-named-account-obligations.json`; rescissions and auction receipts are explicitly outside this concept |
| Energy and vehicle outcomes | `epa.automotive_trends.new_vehicle_co2_rate`; `nhtsa.cafe.actual_fleet_fuel_economy`; `eia.electric_power.net_generation_by_source` | `NONE-existing` | `epa-automotive-trends-new-vehicle-co2-rate.json`; `nhtsa-cafe-actual-fleet-fuel-economy.json`; `eia-electric-power-net-generation-by-source.json` |
| Coverage participation | `cms.medicaid_chip.total_enrollment` | `NONE-existing` | `cms-medicaid-chip-total-enrollment.json` |
| Federal Medicaid outlays | `cms.medicaid.cms64.federal_share_net_expenditures` | `NONE-existing` | `cms-medicaid-cms64-federal-share-net-expenditures.json` |
| Renewal burden and procedural loss | `cms.medicaid_pi.procedural_disenrollment_share` | `NONE-existing` | `cms-medicaid-pi-procedural-disenrollment-share.json` |
| Exchange verification | — | — | `no-series.ndjson` |
| Appropriation execution | `usaspending.dhs.title_vi.named_account_obligations_outlays` | `usaspending-api` | `usaspending-dhs-title-vi-named-account-obligations-outlays.json` |
| Delivery and operations gap | — | — | `no-series.ndjson` |
| Immigration-court capacity | `doj.eoir.immigration_judges_onboard`; `doj.eoir.case_completions`; `doj.eoir.pending_caseload` | `NONE-existing` | `doj-eoir-immigration-judges-onboard.json`; `doj-eoir-case-completions.json`; `doj-eoir-pending-caseload.json` |
| Detention and removal operations | `ice.detention.average_daily_population`; `ice.ero.removals` | `NONE-existing` | `ice-detention-average-daily-population.json`; `ice-ero-removals.json` |
| Applications and fee receipts | `uscis.i589.receipts`; `uscis.i765.c08.receipts` | `NONE-existing` | `uscis-i589-receipts.json`; `uscis-i765-c08-receipts.json`; fee receipts remain outside these concepts |
| Unaccompanied-child operations | `acf.orr.unaccompanied_children.releases_to_sponsors`; `acf.orr.unaccompanied_children.average_length_of_care` | `NONE-existing` | `acf-orr-unaccompanied-children-releases-to-sponsors.json`; `acf-orr-unaccompanied-children-average-length-of-care.json` |
| Lease and timber-sale delivery | `blm.oil_gas.lease_sale_acres_sold`; `blm.oil_gas.lease_sale_bonus_bids`; `usfs.timber.volume_sold` | `NONE-existing` | `blm-oil-gas-lease-sale-acres-sold.json`; `blm-oil-gas-lease-sale-bonus-bids.json`; `usfs-timber-volume-sold.json` |
| Production, receipts, and capacity | `onrr.federal_oil.production_volume`; `onrr.federal_minerals.royalty_revenue` | `NONE-existing` | `onrr-federal-oil-production-volume.json`; `onrr-federal-minerals-royalty-revenue.json`; project-specific Reclamation capacity is not represented |
| Asset and staffing delivery | `faa.air_traffic_controller.certified_professional_count` | `NONE-existing` | `faa-air-traffic-controller-certified-professional-count.json`; Coast Guard acquisitions remain program-specific reports, not this series |
| Vehicle-fee collection | `doe.afdc.electric_vehicle_registrations` | `NONE-existing` | `doe-afdc-electric-vehicle-registrations.json`; fees and Highway Trust Fund remittances are not represented |
| Tax-return claims | `irs.actc.total_claims`; `irs.soi.hr1_individual_deduction_claims` | Existing `irs-soi-pub1304`; new workbook parser required | Existing ACTC docket entry plus `irs-soi-hr1-individual-deduction-claims.json` |
| Individual receipts | `treasury.mts.individual_income_tax` | `NONE-existing` | `treasury-mts-individual-income-tax.json` |
| Business investment and research | `bea.private_nonresidential_fixed_investment`; `bea.research_and_development_fixed_investment`; `treasury.mts.corporation_income_tax_receipts` | `alfred-fred`; `NONE-existing` | `bea-private-nonresidential-fixed-investment.json`; `bea-research-and-development-fixed-investment.json`; `treasury-mts-corporation-income-tax-receipts.json` |
| Honest distribution gap | — | — | `no-series.ndjson` |
| Clean-credit claims | `irs.soi.clean_energy_credit_claims` | Workbook parser required | `irs-soi-clean-energy-credit-claims.json` |
| Clean-energy deployment | `doe.anl.light_duty_electric_drive_vehicle_sales`; `eia.electric_generator.capacity_additions_by_source`; `eia.electric_power.net_generation_by_source` | `NONE-existing` | `doe-anl-light-duty-electric-drive-vehicle-sales.json`; `eia-electric-generator-capacity-additions-by-source.json`; `eia-electric-power-net-generation-by-source.json` |
| Medicare improper-payment recoupment | `cms.medicare.improper_payments_recouped_1899d` | `NONE-existing` | `cms-medicare-improper-payments-recouped-1899d.json` |
| Debt subject to limit | `treasury.mspd.debt_subject_to_limit` | `NONE-existing` | `treasury-mspd-debt-subject-to-limit.json` |

### COVER Now Act (H.R. 608)

| Metric | Proposed series | Adapter family | Request / admission / no-series state |
|---|---|---|---|
| Bill-created demonstration enrollment | — | — | `no-series.ndjson` |
| Demonstration expenditures and matching payments | `cms.medicaid.section_1902_uu.medical_assistance_expenditures`; `cms.medicaid.section_1902_uu.federal_matching_payments` | `NONE-existing` | `cms-medicaid-section-1902-uu-medical-assistance-expenditures.json`; `cms-medicaid-section-1902-uu-federal-matching-payments.json` |
| State-transition coverage continuity | — | — | `no-series.ndjson` |
| Rulemaking and application-decision milestones | — | — | `no-series.ndjson` |
| Project and locality participation structure | — | — | `no-series.ndjson` |
| Confirmed prohibited State actions | — | — | `no-series.ndjson` |
| Federal withholding enforcement | — | — | `no-series.ndjson` |
| One-time congressional report | — | — | `no-series.ndjson` |
| State administrative-match implementation | `cms.medicaid.section_1903_a_8.administrative_matching_percentage`; `cms.medicaid.section_1903_a_8.incremental_federal_payment` | `NONE-existing` | `cms-medicaid-section-1903-a-8-administrative-matching-percentage.json`; `cms-medicaid-section-1903-a-8-incremental-federal-payment.json` |

### REMIT Act (H.R. 5595)

| Metric | Proposed series | Adapter family | Request / admission / no-series state |
|---|---|---|---|
| Gross remittance-tax liability | — | — | `no-series.ndjson` |
| Citizen and national relief take-up | — | — | `no-series.ndjson` |
| Broad personal-transfer proxy | `bea.ita.personal_transfer_payments` | `alfred-fred` | `bea-ita-personal-transfer-payments.json` |

### Safeguarding Medicaid Act (S. 1082)

| Metric | Proposed series | Adapter family | Request / admission / no-series state |
|---|---|---|---|
| State plan and program implementation | — | — | `no-series.ndjson` |
| Asset-check coverage | `cms.medicaid_asset_verification.application_asset_checks`; `cms.medicaid_asset_verification.renewal_asset_checks` | `NONE-existing` | `cms-medicaid-asset-verification-application-asset-checks.json`; `cms-medicaid-asset-verification-renewal-asset-checks.json` |
| Resource-test implementation | — | — | `no-series.ndjson` |
| Post-check application eligibility | `cms.medicaid_asset_verification.applicants_determined_eligible_after_check` | `NONE-existing` | `cms-medicaid-asset-verification-applicants-determined-eligible-after-check.json` |
| Honest access and safeguard gap | — | — | `no-series.ndjson` |
| Bill-created federal savings estimate | — | — | `no-series.ndjson` |
| Public State eligibility-processing reports | `cms.medicaid_asset_verification.eligibility_renewals_initiated`; `cms.medicaid_asset_verification.renewal_asset_checks`; `cms.medicaid_asset_verification.new_applications_initiated`; `cms.medicaid_asset_verification.application_asset_checks`; `cms.medicaid_asset_verification.applicants_determined_eligible_after_check` | `NONE-existing` | The five corresponding `cms-medicaid-asset-verification-*.json` requests; fields and publication are future and UNVERIFIED |
| Corrective-action implementation | — | — | `no-series.ndjson` |

### CDFI Fund capitalization assistance (S. 2718)

| Metric | Proposed series | Adapter family | Request / admission / no-series state |
|---|---|---|---|
| Annual report delivery and assistance totals | — | — | `no-series.ndjson` |
| Mandated competitiveness and liquidity assessment | — | — | `no-series.ndjson` |
| Honest origination, reach, concentration, and risk gap | — | — | `no-series.ndjson` |

### Superior National Forest Restoration Act (H.R. 978)

| Metric | Proposed series | Adapter family | Request / admission / no-series state |
|---|---|---|---|
| One-time withdrawal-order legal state | — | — | `no-series.ndjson` |
| Initial-review deadline compliance | — | — | `no-series.ndjson` |
| Supplemental-review deadline compliance | — | — | `no-series.ndjson` |
| Post-approval permit deadline compliance | — | — | `no-series.ndjson` |
| Canceled-instrument reissuance completion | — | — | `no-series.ndjson` |
| Five-day preference-lease grant compliance | — | — | `no-series.ndjson` |
| Discretionary surface-permit issuance | — | — | `no-series.ndjson` |

### HIDTA Enhancement Act (S. 767)

| Metric | Proposed series | Adapter family | Request / admission / no-series state |
|---|---|---|---|
| Direct fentanyl-reporting output | — | — | `no-series.ndjson` |
| Program enforcement output | `ondcp.hidta.fentanyl_removed.weight`; `ondcp.hidta.fentanyl_removed.dosage_units` | `NONE-existing` | `ondcp-hidta-fentanyl-removed-weight.json`; `ondcp-hidta-fentanyl-removed-dosage-units.json` |
| Direct limitations-and-recommendations disclosure | — | — | `no-series.ndjson` |
| Direct fiscal implementation | `ondcp.hidta.enacted_budget_authority` | `NONE-existing` | `ondcp-hidta-enacted-budget-authority.json` |
| Supplemental-grant use | `usaspending.ondcp.hidta_supplemental_grant_obligations` | `usaspending-api` | `usaspending-ondcp-hidta-supplemental-grant-obligations.json` |
| Request-process establishment milestone | — | — | `no-series.ndjson` |
| Temporary-reassignment use | — | — | `no-series.ndjson` |

### FUTURE Networks Act (H.R. 2449)

| Metric | Proposed series | Adapter family | Request / admission / no-series state |
|---|---|---|---|
| Draft-report publication and public-comment milestone | — | — | `no-series.ndjson` |
| Final-report publication and required-content milestone | — | — | `no-series.ndjson` |

### FLRAA MEDEVAC and special-operations procurement (S. 2075)

| Metric | Proposed series | Adapter family | Request / admission / no-series state |
|---|---|---|---|
| Variant-development budget and activity proxy | `army.rdte.pe0605241a.dg5.flraa_medevac_planned_program` | `NONE-existing` | `army-rdte-pe0605241a-dg5-flraa-medevac-planned-program.json` |
| One-time statutory reporting milestone | — | — | `no-series.ndjson` |
| Honest capability and life-cycle-cost gap | — | — | `no-series.ndjson` |

### Small Business Disaster Damage Fairness Act (H.R. 1021)

| Metric | Proposed series | Adapter family | Request / admission / no-series state |
|---|---|---|---|
| Regulatory and guidance implementation | — | — | `no-series.ndjson` |
| Loan participation proxy | `sba.disaster.physical_loans.approved_count_14001_50000`; `sba.disaster.physical_loans.approved_amount_14001_50000` | `NONE-existing` | `sba-disaster-physical-loans-approved-count-14001-50000.json`; `sba-disaster-physical-loans-approved-amount-14001-50000.json`; cadence is deliberately `null` until the integrator verifies the Open Data refresh schedule |
| Aggregate credit-performance context | `sba.disaster.loan_program.charge_off_amount`; `sba.disaster.loan_program.charge_off_rate_upb`; `sba.disaster.loan_program.post_charge_off_recovery` | Workbook parser required | `sba-disaster-loan-program-charge-off-amount.json`; `sba-disaster-loan-program-charge-off-rate-upb.json`; `sba-disaster-loan-program-post-charge-off-recovery.json` |
| One-time report delivery | — | — | `no-series.ndjson` |
| Bill-created loan-performance measure | — | — | `no-series.ndjson` |
| Outreach-plan implementation | — | — | `no-series.ndjson` |
| Rural access outcome | — | — | `no-series.ndjson` |
| Honest awareness and unmet-need gap | — | — | `no-series.ndjson` |

### FLARE Act (S. 1188)

| Metric | Proposed series | Adapter family | Request / admission / no-series state |
|---|---|---|---|
| Aggregate flaring-and-venting outcome | `eia.natural_gas.vented_flared.us_annual` | `alfred-fred` | `eia-natural-gas-vented-flared-us-annual.json` |
| Honest tax-uptake and eligibility gap | — | — | `no-series.ndjson` |

## Integrator morning checklist

1. Start with source identity and first-print evidence. For each request, fetch
   the exact official product at the URL in its `verification` field; pin the
   field/table identity, unit, cadence, release calendar, revision behavior,
   and at least three first-print observations. Do not turn a likely URL
   pattern into a `sourceBinding` without that evidence.
2. Prioritize reusable missing executors: an official FNS SNAP table parser
   (including the already-docketed `fns.snap.total_persons`), a Medicaid Data
   API/CMS-64 family distinct from Care Compare, then exact ALFRED IDs and
   transforms for the four candidates. Future statutory CMS fields must wait
   for actual publications rather than being inferred from the bill.
3. Verify every proposed USAspending query by immutable agency, account,
   program-activity, award-type, action-date, and snapshot filters. The current
   six hard-coded DoD stems are not authority for the USDA, DHS, Energy /
   Commerce, or ONDCP requests.
4. Build table-specific workbook parsers for the two new IRS requests and the
   three SBA Loan Program Performance requests. The Publication 1304 ACTC
   parser is an implementation pattern, not a generic workbook executor.
5. Only after an executor and anchors pass review: add the recurring docket
   entry, replace the documentation stub with pinned values and retrieval
   dates, extend registry/prospect coupling tests, run the focused suites, and
   then roll a target. Keep all 45 no-series rows open until a stable public
   numeric product with a resolvable release policy appears.

## Verification record

- The required `uv run --extra dev pytest tests/test_roll_docket.py
  tests/test_register_targets.py tests/test_prospect_targets.py -q` invocation
  was attempted with a writable temporary uv cache. It stopped before test
  collection because the isolated cache lacked the build requirements
  `setuptools>=61.0` and `wheel`, and network resolution was disabled. No
  dependency was fetched.
- The same three test files were then run without installation through the
  repository's existing Python and read-only cached pytest runtime: **167
  passed in 223.05 seconds**.
- `tests/test_map_bill_metrics.py`: **14 passed in 0.19 seconds** through the
  same offline runtime.
- Corpus checks require all 64 JSON requests and all 45 NDJSON rows to parse,
  all requested base and added fields to be present, every verification block
  to begin with `UNVERIFIED` and contain an exact HTTPS URL, and all 64
  proposed concepts to be unique.
