# Skill: US fiscal data — Treasury, SNAP/FNS, program administration

## Monthly Treasury Statement (MTS)
- Schedule: `https://fiscal.treasury.gov/reports-statements/mts/` — typically
  the 8th business day of the following month.
- The resolvable number: total deficit/surplus for the month, first print,
  USD billions. FRED mirror for history: MTSDS133FMS.
- Seasonality dominates (April surpluses, June often surplus from mid-June
  corporate taxes; outlay timing shifts when the 1st falls on a weekend) —
  the base rate is the same-calendar-month distribution, not adjacent months.

## USDA FNS (SNAP)
- Quality control payment error rates: annual, published ~end of June for
  the prior fiscal year at
  `https://www.fns.usda.gov/snap/qc/per` (state + national, combined over-
  and underpayment, first print). FY2024 rates published June 30, 2025.
- Participation/benefit data: monthly tables at
  `https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap`
  (lags ~3 months).
- Post-2025 reconciliation law, state cost-share keys off error rates —
  expect state behavioral responses (QC staffing, arbitration) in the
  inside view.

## Social Security / IRS
- SSA monthly statistical snapshot for benefit levels; IRS SOI for filing
  aggregates (long lags — prefer cells with clean scheduled prints).
