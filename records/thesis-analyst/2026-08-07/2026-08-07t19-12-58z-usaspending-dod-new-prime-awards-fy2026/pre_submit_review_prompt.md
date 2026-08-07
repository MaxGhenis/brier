# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.dod.new_prime_awards
- period: FY2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-new-prime-awards-fy2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "usaspending.dod.new_prime_awards.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "new_award_count", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.agency.097.awards.new_award_count", "sourceUrl": "https://api.usaspending.gov/api/v2/agency/097/awards/new/count/?fiscal_year={fiscal_year}", "table": "USAspending API v2, agency 097 (DoD) new award count, fiscal year to date", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-07-e6964d48e8a09276874f5990a6155deca11583fde07f94e731a8355b70cb4f47.json"
- targetContentHash: "e6964d48e8a09276874f5990a6155deca11583fde07f94e731a8355b70cb4f47"
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
9144c28c88bc6e0e4fb39e840ded9e49ea1d9f47b7848154ba504b346d84519a

# Draft forecast response
{"slug":"us-dod-new-prime-awards-fy2026","country":"US","type":"data","title":"DoD New Prime Awards FY2026","question":"What will USAspending API v2 report as Department of Defense agency 097 new_award_count for fiscal_year=2026, in millions of new prime awards, in the first registered query snapshot on 2026-10-22?","unit":"millions","pointEstimate":1.43,"ciLow":1.18,"ciHigh":1.68,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"USAspending API v2, agency 097 awards new count","resolutionSourceUrl":"https://api.usaspending.gov/api/v2/agency/097/awards/new/count/?fiscal_year=2026","resolutionRule":"On 2026-10-22, query the official USAspending API v2 endpoint /api/v2/agency/097/awards/new/count/?fiscal_year=2026 and read new_award_count for toptier_code 097, agency_type awarding, award_type_codes null. Convert to millions by multiplying by 1e-6 and round to the agency/API integer precision before conversion. Use the first registered query snapshot only; do not apply later revisions or same-day correction grace unless the registered target is changed.","dataPointId":"usaspending.dod.new_prime_awards.fy2026.registered_query_snapshot","historicalContext":[{"label":"FY2021 official API new_award_count, millions","value":1.765},{"label":"FY2022 official API new_award_count, millions","value":1.285},{"label":"FY2023 official API new_award_count, millions","value":1.332},{"label":"FY2024 official API new_award_count, millions","value":1.505},{"label":"FY2025 official API new_award_count, millions","value":1.588},{"label":"FY2026 current official API new_award_count, millions","value":1.068328}],"drivers":["Current FY2026 official API count is 1.068328 million before the fiscal-year closeout snapshot","DoD award data have a published 90-day contract and IDV display delay, making late backfill material","FY2021-FY2025 reference class clusters around roughly 1.3 million to 1.8 million","DLA transaction-heavy award flow dominates count volatility","FY2026 defense budget and operating tempo argue for persistence rather than a regime break"],"sourceContext":["https://api.usaspending.gov/api/v2/agency/097/awards/new/count/?fiscal_year=2026","https://api.usaspending.gov/api/v2/agency/097/awards/","https://api.usaspending.gov/api/v2/agency/097/","https://api.usaspending.gov/api/v2/references/submission_periods/","https://api.usaspending.gov/api/v2/awards/last_updated/"],"runAt":"2026-08-07T19:13:07Z","reasoning":[{"kind":"heading","text":"DoD FY2026 New Prime Awards Forecast"},{"kind":"text","text":"Framing and exact resolver: the target is USAspending API v2 agency 097, field new_award_count, fiscal_year=2026, transformed to millions. The official agency overview identifies toptier_code 097 as Department of Defense and states that DoD contract and IDV data are subject to a 90-day publication delay while other DoD data are not; that matters because the 2026-10-22 registered snapshot may still be a policy-defined snapshot rather than a fully final all-contract vintage."},{"kind":"tool","tool":"official.lookup","call":"GET https://api.usaspending.gov/api/v2/agency/097/awards/new/count/","result":"Fetched official current FY2026 response: toptier_code=097, fiscal_year=2026, agency_type=awarding, award_type_codes=null, new_award_count=1068328, equal to 1.068328 million after the registered factor 1e-6."},{"kind":"tool","tool":"official.lookup","call":"GET https://api.usaspending.gov/api/v2/agency/097/awards/","result":"Fetched official FY2026 agency-awards context: fiscal_year=2026, latest_action_date=2026-07-10, transaction_count=2205913, obligations=245063144206.58 dollars."},{"kind":"tool","tool":"official.lookup","call":"GET https://api.usaspending.gov/api/v2/references/submission_periods/ and GET https://api.usaspending.gov/api/v2/awards/last_updated/","result":"Fetched official schedule/update context: awards last_updated=08/07/2026; FY2026 fiscal month 9 submission_due_date=2026-07-31 and certification_due_date=2026-08-15; FY2025 fiscal month 12 had submission_start_date=2025-10-21, certification_due_date=2025-11-18, and submission_reveal_date=2025-12-06T02:57:27.169269Z. I found no official future FY2026 period-12 exact reveal date in the available endpoint, so I keep the ledger-registered resolve-by-bound date 2026-10-22 and state this discrepancy rather than changing the target."},{"kind":"tool","tool":"official.lookup","call":"USAspending API v2 agency 097 awards new count historical fiscal-year pulls for FY2021-FY2025","result":"Fetched official reference class in raw counts: FY2021=1765000, FY2022=1285000, FY2023=1332000, FY2024=1505000, FY2025=1588000; transformed to millions these are 1.765, 1.285, 1.332, 1.505, and 1.588."},{"kind":"text","text":"Base rate and reference class: the FY2021-FY2025 annual level prior is centered near 1.495 million, with FY2024-FY2025 closer to 1.55 million. The current FY2026 count of 1.068328 million is through a latest_action_date of 2026-07-10, so a simple elapsed-year annualization gives about 1.38 million before allowing for end-year and reporting-window backfill."},{"kind":"math","text":"Prior/update/interval: persistence prior = FY2021-FY2025 official annual new_award_count values in millions [1.765, 1.285, 1.332, 1.505, 1.588], mean = 1.495. Current-release update = 1.068328 / about 0.775 of the fiscal year = 1.379 annualized, plus +0.05 million for late-fiscal-year/backfill flow and no separate policy shock, giving point = 1.43. Interval method = sample dispersion of the five annual flow values; sigma = 0.195 million, so 1.28*sigma = 0.250 million, yielding 1.43 +/- 0.25 = [1.18, 1.68]."},{"kind":"text","text":"Counter-considerations: upside risk is a larger-than-usual DoD/DLA late-year contract and assistance backfill, which would land above the interval if the 2026-10-22 snapshot exceeds 1.68 million. Downside risk is continued missing delayed procurement records or weaker DLA micro-award volume, which would land below the interval if the snapshot remains under 1.18 million. Outside the interval would mainly signal either a release-policy/backfill timing surprise or an actual count-regime break, not ordinary year-to-year noise."},{"kind":"forecast","point":1.43,"ciLow":1.18,"ciHigh":1.68}]}
