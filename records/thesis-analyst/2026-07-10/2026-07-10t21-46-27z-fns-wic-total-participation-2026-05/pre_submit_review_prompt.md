# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fns.wic.total_participation
- period: 2026-05
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "wic-participation-may-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "fns.wic.total_participation.2026-05.first_print"
- resolutionDate: "2026-08-14"
- resolutionSource: "Official agency release"
- resolutionSourceUrl: "https://www.fns.usda.gov/pd/wic-program"
- resolutionRule: "Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. The expected displayed FNS monthly table value is a whole participant count, as in 6,894,610 for May 2025; convert that displayed person count to millions by dividing by 1,000,000 and round to 0.001 million for the cell. If the ledger adapter instead extracts an intermediate value expressed in thousands of participants, its listed factor 0.001 produces the same final unit of millions. Use the first posted May 2026 value only; ignore later preliminary/final revisions or annual-summary revisions."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-08-15", "start": "2026-08-07"}, "field": "fns.wic.total_participation", "releasePolicy": "first_print", "sourceSeriesId": "fns.wic.total_participation", "sourceUrl": "https://www.fns.usda.gov/pd/wic-program", "table": "Official agency release", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-d9f0f26436f4322b04c9deeec1745f166dd46dbeec72d9ec676b1e2cf86ae6a9.json"
- targetContentHash: "d9f0f26436f4322b04c9deeec1745f166dd46dbeec72d9ec676b1e2cf86ae6a9"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"
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
63b5071f47ba9db650de78217132d81d4758f445b4850e1c7c6ea5458a1ee46e

# Draft forecast response
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC participation, May 2026","question":"What will USDA FNS first report as national WIC Total Participants for May 2026, in millions of people?","unit":"millions","pointEstimate":6.78,"ciLow":6.65,"ciHigh":6.9,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Divide the displayed whole-person count by 1,000,000 and round to 0.001 million. Use only the first posted value and ignore later preliminary, final, or annual-summary revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"March 2023","value":6.621311},{"label":"May 2023","value":6.696739},{"label":"March 2024","value":6.680974},{"label":"May 2024","value":6.76371},{"label":"March 2025","value":6.850836},{"label":"May 2025","value":6.89461},{"label":"March 2026 preliminary","value":6.701661}],"drivers":["Recent year-over-year participation decline","Typical March-to-May seasonal increase","Children remain the largest participant category","Preliminary-data reporting variation"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-6.pdf","https://fns-prod.azureedge.us/pd/overview"],"runAt":"2026-07-10T21:47:18Z","reasoning":[{"kind":"heading","text":"May 2026 national WIC participation forecast"},{"kind":"text","text":"The target is the first USDA FNS national monthly-table print of Total Participants for May 2026, not an annual average, eligibility estimate, revised value, or state-only measure. The official table has no separate seasonal adjustment. The displayed person count is converted to millions and rounded to 0.001."},{"kind":"tool","tool":"official.lookup","call":"Fetched the USDA WIC national monthly participation table and read recent March and May totals.","result":"Total participation was 6,621,311 in March 2023 and 6,696,739 in May 2023; 6,680,974 in March 2024 and 6,763,710 in May 2024; 6,850,836 in March 2025 and 6,894,610 in May 2025."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest available FY 2026 observations from the USDA WIC national monthly table.","result":"Total participation was 6,696,300 in January 2026, 6,664,580 in February 2026, and 6,701,661 in March 2026; the table says FY 2026 data are preliminary and data are as of June 12, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched category detail for the latest month and annual reference values from the official USDA table.","result":"March 2026 comprised 1,458,253 women, 1,419,036 infants, and 3,824,372 children, totaling 6,701,661. FY 2024 averaged 6,704,329 and FY 2025 averaged 6,867,417 participants."},{"kind":"tool","tool":"official.calendar_lookup","call":"Checked the official program-data schedule associated with the registered release window for the May 2026 posting.","result":"The official expected release window is August 7 through August 15, 2026, with the ledger target dated August 14, 2026; the target therefore resolves on 2026-08-14 rather than on a cadence-inferred date."},{"kind":"text","text":"The reference class is the same-series March-to-May movement: +75,428 in 2023, +82,736 in 2024, and +43,774 in 2025. Its median increase is 75,428. Applying that base rate to March 2026 gives 6,777,089, while the May year-over-year decline implied by that anchor is about 1.7%."},{"kind":"text","text":"Prior/update/interval: The persistence prior is March 2026 participation of 6.701661 million, with the historical sample consisting of the fetched 2023-2025 March-to-May changes. I add the median seasonal change of 0.075428 million, make no separate level adjustment because the latest year-over-year weakness is already embedded in March, and allow for reporting and policy-mechanism uncertainty through the elicited threshold ladder. The ladder interpolation implies final 80% bounds of 6.650 to 6.900 million."},{"kind":"text","text":"An upside risk is a stronger spring enrollment rebound, outreach effect, or delayed state reporting that would push participation toward or above 6.900 million. A downside risk is continued caseload attrition or incomplete first-print state submissions; an unusually broad decline would land below the interval at 6.650 million."},{"kind":"math","text":"Ladder: P(X <= 6.58) = 0.03; P(X <= 6.62) = 0.06; P(X <= 6.65) = 0.10; P(X <= 6.68) = 0.16; P(X <= 6.71) = 0.24; P(X <= 6.74) = 0.34; P(X <= 6.78) = 0.50; P(X <= 6.81) = 0.62; P(X <= 6.84) = 0.73; P(X <= 6.87) = 0.82; P(X <= 6.90) = 0.90; P(X <= 6.94) = 0.95; P(X <= 6.98) = 0.98. Linear interpolation gives the 10th percentile at 6.650, median at 6.780, and 90th percentile at 6.900."},{"kind":"forecast","point":6.78,"ciLow":6.65,"ciHigh":6.9}],"thresholdLadder":{"thresholds":[6.58,6.62,6.65,6.68,6.71,6.74,6.78,6.81,6.84,6.87,6.9,6.94,6.98],"cumulativeProbabilities":[0.03,0.06,0.1,0.16,0.24,0.34,0.5,0.62,0.73,0.82,0.9,0.95,0.98]}}
