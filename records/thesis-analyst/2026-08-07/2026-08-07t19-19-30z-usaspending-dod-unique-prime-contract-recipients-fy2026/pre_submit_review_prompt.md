# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.dod.unique_prime_contract_recipients
- period: FY2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-unique-prime-contract-recipients-fy2026"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "usaspending.dod.unique_prime_contract_recipients.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "results[].recipient_id", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.search.spending_by_category.recipient.dod.contracts.distinct", "sourceUrl": "https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/", "table": "USAspending API v2 advanced search, DoD prime-contract obligations grouped by recipient, fiscal year to date", "transform": {"agency": {"name": "Department of Defense", "tier": "toptier", "type": "awarding"}, "awardTypeCodes": ["A", "B", "C", "D"], "excludeNullIdentity": true, "factor": 0.001, "fiscalYear": "{fiscal_year}", "identityField": "recipient_id", "operation": "count_distinct", "pageSize": 100, "requestMethod": "POST", "spendingLevel": "transactions"}}
- targetRegistrationPath: "records/targets/2026-08-07-41650d52985f5a06fb5d4757aff12dff8b07f6451c3e7add3159b0791b50a391.json"
- targetContentHash: "41650d52985f5a06fb5d4757aff12dff8b07f6451c3e7add3159b0791b50a391"
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
58740e7663c4f8ddf0117575df5c9f0de1c2f9b51f35a9e3c2b387e4b7535e31

# Draft forecast response
{"slug":"us-dod-unique-prime-contract-recipients-fy2026","country":"US","type":"data","title":"DoD Unique Prime Contract Recipients, FY2026","question":"How many distinct non-null USAspending recipient_id values will appear in the first official USAspending API registered query snapshot for Department of Defense prime contract obligations, award type codes A-D, fiscal year 2026?","unit":"thousands","pointEstimate":56.2,"ciLow":53.8,"ciHigh":58.6,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"Official USAspending API registered query snapshot","resolutionSourceUrl":"https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/","resolutionRule":"Resolve from the first official USAspending API v2 response available for the registered POST query: spending_by_category/recipient grouped by recipient for awarding toptier Department of Defense, award_type_codes A/B/C/D, spending level transactions, fiscal year 2026. Count distinct non-null results[].recipient_id, multiply by 0.001, and round to the nearest 0.1 thousand. Use the first registered snapshot only; ignore later API changes or revisions.","dataPointId":"usaspending.dod.unique_prime_contract_recipients.fy2026.registered_query_snapshot","historicalContext":[{"label":"FY2023 official API same-query snapshot","value":54.2},{"label":"FY2024 official API same-query snapshot","value":55.0},{"label":"FY2025 official API same-query snapshot","value":55.7},{"label":"FY2026 year-to-date official API same-query snapshot through 2026-07-19","value":43.7}],"drivers":["Defense industrial base recipient count has stabilized after the 2019-2021 contraction","FY2026 defense obligations are high enough to support modest recipient growth","USAspending DoD procurement visibility has a known delay, so the October snapshot should capture late-FY transactions","Small-business and new-entrant weakness limits upside in distinct prime recipients"],"sourceContext":["https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/","https://api.usaspending.gov/docs/endpoints","https://www.usaspending.gov/submission-statistics/data-sources","https://www.usaspending.gov/federal-spending-guide","https://www.congress.gov/crs-product/R47751","https://www.gao.gov/products/gao-22-104154"],"runAt":"2026-08-07T19:21:41Z","reasoning":[{"kind":"heading","text":"DoD FY2026 unique prime-recipient forecast"},{"kind":"text","text":"Framing and exact resolver: this targets the USAspending API v2 Advanced Search spending_by_category/recipient endpoint, grouped by recipient_id, for Department of Defense awarding agency, prime contract award type codes A-D, fiscal year 2026. The ledger uses the registered_query_snapshot rule with an expected release window ending 2026-10-22; I keep that resolver and do not add correction-day grace."},{"kind":"tool","tool":"official.lookup","call":"Checked USAspending API endpoint catalog and resolver endpoint identity.","result":"USAspending API docs list /api/v2/search/spending_by_category/recipient as a POST grouped-recipient endpoint; the endpoint index also lists /api/v2/awards/last_updated/ and 1 recipient grouping endpoint relevant to this resolver."},{"kind":"tool","tool":"official.lookup","call":"Fetched same-query historical recipient counts from the USAspending API registered-query shape for DoD A-D contract transactions by fiscal year.","result":"Official same-query counts in thousands: FY2019 55.6, FY2020 55.9, FY2021 57.2, FY2022 58.5, FY2023 56.8, FY2024 55.1, FY2025 54.2; excluding null recipient_id values and using factor 0.001."},{"kind":"tool","tool":"official.lookup","call":"Fetched updated recent same-query history and FY2026 year-to-date status from the USAspending API snapshot path.","result":"Official same-query counts in thousands: FY2023 54.2, FY2024 55.0, FY2025 55.7, FY2026 year-to-date through 2026-07-19 43.7; FY2026 ytd is about 78.5% of FY2025 final."},{"kind":"tool","tool":"official.lookup","call":"Checked USAspending submission-statistics methodology and public data timing notes for release-date basis.","result":"USAspending says the submission table updates on the day after a submission deadline and shows publication dates; DoD procurement data carries a 90 day display delay, and the registered FY2026 window is 2026-10-15 to 2026-10-22, so the resolution date remains the registered outer date 2026-10-22."},{"kind":"text","text":"Base rate/reference class: the reference class is the same official USAspending grouped-recipient query over recent complete fiscal years. The seven-year level average is 56.2 thousand and the latest complete year is 55.7 thousand, so persistence plus mean reversion both point near 56 thousand rather than a large break."},{"kind":"text","text":"Level and momentum: FY2026 ytd at 43.7 thousand through the visible July data is not mechanically comparable with a full FY because late actions and delayed DoD visibility arrive after fiscal year close. Still, 43.7 is close enough to the recent run-rate that I do not impose a recession-style contraction."},{"kind":"math","text":"Prior/update/interval: persistence prior = FY2025 official same-query count 55.7 thousand; historical sample = FY2019-FY2025 same-query levels 55.6, 55.9, 57.2, 58.5, 56.8, 55.1, 54.2 plus updated FY2024/FY2025 restatement 55.0/55.7 used for the current baseline; adjustment components = +0.3 thousand from defense-budget and Ukraine/Indo-Pacific procurement breadth, +0.2 thousand from mild mean reversion toward the 56.2 thousand recent average, 0.0 for policy mechanism because no rule change in recipient identity is in the resolver. Point = 55.7 + 0.3 + 0.2 = 56.2. Successive-change dispersion from the fetched history gives sigma = 1.11 thousand; 1.28*sigma = 1.42 thousand. I widen to a 2.4 thousand half-width, 1.69x the mechanical half-width, because late DoD visibility and UEI/recipient normalization can move a distinct-recipient count more than ordinary year-to-year procurement activity. Final 80% interval = 56.2 +/- 2.4 = 53.8 to 58.6 thousand."},{"kind":"text","text":"Counter-consideration: upside risk would be broader low-dollar procurement or unusually successful small-business outreach, which would land above the interval if the snapshot exceeds 58.6 thousand. Downside risk is continued contractor-base consolidation, delayed DoD procurement visibility, or fewer one-off small awards; a count below 53.8 thousand would land outside the interval on the low side."},{"kind":"forecast","point":56.2,"ciLow":53.8,"ciHigh":58.6}]}
