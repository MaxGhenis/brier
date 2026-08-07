# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.dod.prime_award_transactions
- period: FY2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-prime-award-transactions-fy2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "usaspending.dod.prime_award_transactions.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "transaction_count", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.agency.097.awards.transaction_count", "sourceUrl": "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year={fiscal_year}", "table": "USAspending API v2, agency 097 (DoD) award summary, transaction count, fiscal year to date", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-07-41dd79f388ca4e5be3ffe71c6c375afc0cc75e0393ae1cb4d6347241b5637d8c.json"
- targetContentHash: "41dd79f388ca4e5be3ffe71c6c375afc0cc75e0393ae1cb4d6347241b5637d8c"
- registrationCommit: "a6991688486115b857a52f29c370ed8f884457e3"
- registeredAtUtc: "2026-08-07T17:54:06Z"
# Rubric
Check these items and name concrete fixes when needed:
1. Exact resolver, source, first-print rule, and resolution date.
2. Base-rate or persistence prior stated before inside-view updates.
3. Time-series/model prior used or explicitly ruled out.
4. Current evidence justifies material movement from the prior.
5. Interval size comes from realized volatility or explicit uncertainty.
6. A compact Prior/update/interval step names the prior, historical sample, adjustment components, interval method, and implied bounds.
7. Tail scenarios are concrete and tied to the target.
8. Point, interval, final forecast step, and JSON fields are coherent.
9. No leakage, catalog point/interval circularity, subjective resolver, or unit ambiguity.

# Required response
Return JSON only, with this shape:
{
  "summary": "one sentence",
  "requiredFixes": [
    {
      "rubricItem": "resolver|base_rate|model_prior|update|interval|prior_update_interval|tails|coherence|leakage",
      "severity": "warning|blocking",
      "summary": "specific issue",
      "actionRequested": "specific change requested"
    }
  ],
  "optionalSuggestions": ["short suggestions"]
}

# Original forecaster prompt hash material
d6c45939a99e940dd6005e004565e9bd4fd46b39a981d99387a211dbda9fd982

# Draft forecast response
{"slug":"us-dod-prime-award-transactions-fy2026","country":"US","type":"data","title":"DoD Prime Award Transactions FY2026","question":"What will the USAspending API v2 agency 097 awards transaction_count be for Department of Defense prime awards in FY2026, in millions, in the first registered query snapshot?","unit":"millions","pointEstimate":3.86,"ciLow":3.47,"ciHigh":4.25,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"USAspending API v2 agency award summary","resolutionSourceUrl":"https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2026","resolutionRule":"Resolve from the first official USAspending API v2 registered query snapshot for agency 097 with fiscal_year=2026 in the registered release window, using the transaction_count field multiplied by 0.000001 and rounded to millions; do not revise for later API updates or corrections.","dataPointId":"usaspending.dod.prime_award_transactions.fy2026.registered_query_snapshot","historicalContext":[{"label":"FY2021 official API transaction_count, millions","value":4.566},{"label":"FY2022 official API transaction_count, millions","value":4.318},{"label":"FY2023 official API transaction_count, millions","value":4.084},{"label":"FY2024 official API transaction_count, millions","value":3.965},{"label":"FY2025 official API transaction_count, millions","value":3.786}],"drivers":["FY2026 DoD award flow is tracking close to recent years but below FY2021-FY2022 highs","DoD procurement and operations funding remains large enough to support a near-flat transaction count","Administrative reporting and late fiscal-year modification volume can move the final count materially","First registered USAspending API snapshot may miss some lagged procurement corrections"],"sourceContext":["https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2021","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2022","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2023","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2024","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2025","https://api.usaspending.gov/api/v2/references/submission_periods/","https://api.usaspending.gov/docs/endpoints"],"runAt":"2026-08-07T19:16:36Z","reasoning":[{"kind":"heading","text":"Forecast DoD FY2026 Prime Award Transactions"},{"kind":"text","text":"Framing and exact resolver: this is the USAspending API v2 agency 097 awards endpoint, fiscal_year=2026, field transaction_count, transformed to millions. The registered target uses a resolve-by-bound window ending 2026-10-22; the official submission-period endpoint visible this run lists recent reveal and certification dates but not yet the future FY2026 fiscal-month-12 row, so I keep the ledger resolutionDate and note that the exact future reveal row was not observable yet."},{"kind":"tool","tool":"official.lookup","call":"Fetched USAspending agency 097 awards endpoint for completed fiscal years 2021 and 2022, reading transaction_count and converting by 1e-6.","result":"Fetched FY2021 transaction_count 4566000 = 4.566 million; FY2022 transaction_count 4318000 = 4.318 million."},{"kind":"tool","tool":"official.lookup","call":"Fetched USAspending agency 097 awards endpoint for completed fiscal years 2023 and 2024, same agency 097 and same transaction_count field.","result":"Fetched FY2023 transaction_count 4084000 = 4.084 million; FY2024 transaction_count 3965000 = 3.965 million."},{"kind":"tool","tool":"official.lookup","call":"Fetched USAspending agency 097 awards endpoint for FY2025 and the public submission-period schedule context.","result":"Fetched FY2025 transaction_count 3786000 = 3.786 million; submission_periods showed FY2026 fiscal_month 9 and FY2025 fiscal_month 12 entries, with FY2025 fiscal_month 12 submission_reveal_date 2025-12-06T02:57:27Z."},{"kind":"text","text":"Base rate/reference class: the same-source annual flow reference class is FY2021-FY2025 DoD prime award transaction counts, ranging from 3.786 million to 4.566 million, with a mean of 4.144 million and a downward drift of about 0.195 million per year over the last four year-to-year steps."},{"kind":"text","text":"Level and momentum: the downtrend from 4.566 million in FY2021 to 3.786 million in FY2025 argues against returning to the early-period level; however, FY2025 to FY2026 should not mechanically extend the full decline because transaction reporting appears to be settling near a high-3-million annual run rate."},{"kind":"text","text":"Policy and mechanism adjustment: FY2026 defense spending remains large, so the main policy effect is on composition and timing rather than a collapse in transaction activity. I add a small +0.07 million adjustment versus pure recent-trend persistence for late-year modifications and awards tied to ongoing defense procurement activity."},{"kind":"math","text":"Prior/update/interval: persistence prior is FY2025 at 3.786 million; historical sample is FY2021-FY2025 same USAspending API annual values of 4.566, 4.318, 4.084, 3.965, and 3.786 million; adjustment components are +0.04 million for stabilization after the FY2021-FY2025 decline and +0.03 million for FY2026 late-year defense award/modification flow, giving point 3.786 + 0.074 = 3.860 million. For the flow-series interval I use dispersion of the annual values themselves: sigma = 0.305 million, so 80% half-width is about 1.28*sigma = 1.28*0.305 = 0.390 million, implying 3.860 +/- 0.390 = 3.470 to 4.250 million."},{"kind":"text","text":"Counter-considerations: upside risk is a heavier-than-usual late FY2026 modification surge or delayed FY2025-FY2026 procurement data clearing into the first snapshot, which would land above the interval if the count exceeds 4.25 million. Downside risk is a reporting lag, shutdown-related processing disruption, or sustained simplification of award actions, which would land below the interval if the count is under 3.47 million."},{"kind":"forecast","point":3.86,"ciLow":3.47,"ciHigh":4.25}]}
