# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.dod.prime_award_obligations
- period: FY2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-prime-award-obligations-fy2026"
- country: "US"
- targetUnit: "billions USD"
- dataPointId: "usaspending.dod.prime_award_obligations.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "obligations", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.agency.097.awards.obligations", "sourceUrl": "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year={fiscal_year}", "table": "USAspending API v2, agency 097 (DoD) award summary, prime award obligations, fiscal year to date", "transform": {"factor": 1e-09, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-07-59b334c6612eaf1c20be70ad587590901539f4fc2a11749e9f6a8f1ef2927907.json"
- targetContentHash: "59b334c6612eaf1c20be70ad587590901539f4fc2a11749e9f6a8f1ef2927907"
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
9c35d4aa7ad7fbf3abbb68eb3593d88ea701d6ce49c4d75ff30f764afcf2939f

# Draft forecast response
{"slug":"us-dod-prime-award-obligations-fy2026","country":"US","type":"data","title":"US DoD prime award obligations FY2026","question":"What will USAspending API v2 report as Department of Defense agency 097 prime award obligations for fiscal year 2026 in the first registered query snapshot?","unit":"usd_billions","pointEstimate":532,"ciLow":493,"ciHigh":571,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"USAspending API v2 agency 097 awards endpoint","resolutionSourceUrl":"https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2026","resolutionRule":"Resolve to the first official USAspending API v2 response for /api/v2/agency/097/awards/?fiscal_year=2026 after the FY2026 period-12 Data Broker publication window, using the obligations field for agency 097 prime award obligations, multiplied by 1e-09 and rounded to the nearest 0.1 billion USD. Do not revise for later USAspending updates or corrections.","dataPointId":"usaspending.dod.prime_award_obligations.fy2026.registered_query_snapshot","historicalContext":[{"label":"FY2023 first-print comparable USAspending agency 097 awards obligations","value":463.8},{"label":"FY2024 first-print comparable USAspending agency 097 awards obligations","value":454.6},{"label":"FY2025 first-print comparable USAspending agency 097 awards obligations","value":505.2},{"label":"FY2026 current fiscal-year-to-date check as of run date","value":500.6}],"drivers":["FY2025 DoD prime award obligations were near $505B on the same USAspending agency-awards basis","FY2026 defense budget authority and procurement/RDT&E support a moderate nominal increase","DoD procurement reporting lag makes late-year catch-up important for the first post-period snapshot","The range is sized from realized annual flow dispersion rather than a hand-rounded band"],"sourceContext":["https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2023","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2024","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2025","https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2026","https://tfx.treasury.gov/data-transparency/resources","https://files.gao.gov/multimedia/Federal_Government_Contracting-FY2025/index.html"],"runAt":"2026-08-07T18:20:00Z","reasoning":[{"kind":"heading","text":"US DoD prime award obligations FY2026"},{"kind":"text","text":"Framing and exact resolver: this is the USAspending API v2 agency 097 awards endpoint, fiscal_year=2026, obligations field, transformed from USD to billions USD. I keep the ledger target's 2026-10-22 resolution date and first-print snapshot rule."},{"kind":"tool","tool":"official.lookup","call":"Checked Treasury TFX resources page for Data Broker Reporting Submission Dates FY26 and the USAspending publication timing note.","result":"TFX listed Data Broker Reporting Submission Dates FY26 as a 37.42 KB official document; for FY2026 period 12 the target period ends 2026-09-30, the registered public window is 2026-10-15 to 2026-10-22, and the resolver uses 2026-10-22."},{"kind":"tool","tool":"official.lookup","call":"Fetched USAspending API v2 agency 097 awards endpoint for recent full fiscal years on the same obligations field and 1e-09 transform.","result":"Fetched comparable obligations: FY2021 421.5 billion USD, FY2022 447.2 billion USD, FY2023 463.8 billion USD, FY2024 454.6 billion USD, FY2025 505.2 billion USD."},{"kind":"tool","tool":"official.lookup","call":"Checked USAspending/official procurement context for the current FY2026 and reporting lag context.","result":"The current FY2026 public context showed about 500.6 billion USD in DoD award/contract spending already visible before final period-12 publication, while USAspending notes DoD contract data can have a 90-day publication lag."},{"kind":"tool","tool":"official.lookup","call":"Checked GAO FY2025 governmentwide contracting snapshot for an official outside benchmark on defense-agency contract obligations.","result":"GAO reported FY2025 governmentwide contract obligations of 793 billion USD and defense-agency products plus services of 253 + 238 = 491 billion USD, excluding small missing/other categories and excluding other transaction agreements of 18.2 billion USD."},{"kind":"text","text":"Base rate / reference class: the same-variant USAspending agency 097 prime-award obligations history is a steadily rising but noisy annual flow. The base rate from FY2021-FY2025 is centered in the high-$450B range, with FY2025 stepping up to just above $500B."},{"kind":"text","text":"Variant control: anchors are DoD agency 097 prime award obligations or the nearest official defense-agency contract-obligation cross-check; the resolution itself remains the USAspending agency-awards obligations field, not budgetary resources, outlays, FRED, or news."},{"kind":"math","text":"Prior/update/interval: persistence prior = FY2025 same-endpoint value 505.2; historical sample = FY2021-FY2025 values 421.5, 447.2, 463.8, 454.6, 505.2; adjustment components = +14.0 for nominal defense topline/inflation, +8.0 for procurement and RDT&E mix, +4.8 for late DoD reporting catch-up and FY2026 current run-rate, giving point 532.0. For the flow-series interval I used the values themselves: sample sigma = 30.5, so 80% half-width = 1.28*sigma = 1.28*30.5 = 39.0; point 532.0 +/- 39.0 gives 493.0 to 571.0."},{"kind":"text","text":"Counter-considerations: upside risk is a stronger late-September procurement closeout, supplemental defense funds, or faster DoD reporting that would land above the interval; downside risk is continuing-resolution friction, delayed award reporting, or deobligation cleanup that would land below the interval. A material accounting or API classification change would be outside the interval risk in either direction."},{"kind":"forecast","point":532,"ciLow":493,"ciHigh":571}]}
