# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bea.private_nonresidential_fixed_investment
- period: 2026-Q3
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-private-nonresidential-fixed-investment-q3-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.private_nonresidential_fixed_investment.2026_q3.first_print"
- expectedReleaseWindow: {"end": "2026-10-29", "start": "2026-10-29"}
- sourceBinding: {"adapter": "bea-release", "allowedHosts": ["apps.bea.gov", "www.bea.gov"], "expectedReleaseWindow": {"end": "2026-10-29", "start": "2026-10-29"}, "field": "Line 2: Nonresidential", "releasePolicy": "first_print", "sourceSeriesId": "T50305:L2", "sourceUrl": "https://apps.bea.gov/iTable/?ReqID=19&step=3&isuri=1&nipa_table_list=145&categories=survey", "table": "Gross Domestic Product advance release, NIPA Table 5.3.5, line 2 (Nonresidential)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-17-78ab7e77198fa656ee058e98fa6d3e8743b3f9f24714b851883bee7fff4d2114.json"
- targetContentHash: "78ab7e77198fa656ee058e98fa6d3e8743b3f9f24714b851883bee7fff4d2114"
- registrationCommit: "f3a73cbcc701b9315d3ec1d35ea05889b2c07f95"
- registeredAtUtc: "2026-08-17T16:54:17Z"
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
49b9479eee00033071aa96bf9a7691697c71688733f47d4beef120b832f95c54

# Draft forecast response
{"slug":"us-private-nonresidential-fixed-investment-q3-2026","country":"US","type":"data","title":"US private nonresidential fixed investment, Q3 2026","question":"What will BEA report as the first-print nominal seasonally adjusted annual-rate value for private nonresidential fixed investment, NIPA Table 5.3.5 line 2, in 2026-Q3?","unit":"usd_billions","pointEstimate":4710,"ciLow":4630,"ciHigh":4790,"confidence":0.8,"resolutionDate":"2026-10-29","resolutionSource":"U.S. Bureau of Economic Analysis GDP advance release, NIPA Table 5.3.5 line 2","resolutionSourceUrl":"https://apps.bea.gov/iTable/?ReqID=19&step=3&isuri=1&nipa_table_list=145&categories=survey","resolutionRule":"Resolve to the first official BEA GDP advance-release print for 2026-Q3, NIPA Table 5.3.5, line 2 Nonresidential, nominal seasonally adjusted annual rate. Use the published table value transformed by multiplying the table's millions-of-dollars value by 0.001 to usd_billions. Do not use later second, third, annual-update, or comprehensive-revision values except insofar as BEA has already incorporated them into the first Q3 advance-release table on 2026-10-29.","dataPointId":"bea.private_nonresidential_fixed_investment.2026_q3.first_print","historicalContext":[{"period":{"type":"quarter","value":"2023-Q1"},"label":"2023-Q1","value":3756.575},{"period":{"type":"quarter","value":"2023-Q2"},"label":"2023-Q2","value":3854.267},{"period":{"type":"quarter","value":"2023-Q3"},"label":"2023-Q3","value":3871.644},{"period":{"type":"quarter","value":"2023-Q4"},"label":"2023-Q4","value":3941.343},{"period":{"type":"quarter","value":"2024-Q1"},"label":"2024-Q1","value":3963.752},{"period":{"type":"quarter","value":"2024-Q2"},"label":"2024-Q2","value":4012.411},{"period":{"type":"quarter","value":"2024-Q3"},"label":"2024-Q3","value":4069.186},{"period":{"type":"quarter","value":"2024-Q4"},"label":"2024-Q4","value":4046.39},{"period":{"type":"quarter","value":"2025-Q1"},"label":"2025-Q1","value":4137.819},{"period":{"type":"quarter","value":"2025-Q2"},"label":"2025-Q2","value":4207.512},{"period":{"type":"quarter","value":"2025-Q3"},"label":"2025-Q3","value":4293.474},{"period":{"type":"quarter","value":"2025-Q4"},"label":"2025-Q4","value":4364.412},{"period":{"type":"quarter","value":"2026-Q1"},"label":"2026-Q1","value":4490.516},{"period":{"type":"quarter","value":"2026-Q2"},"label":"2026-Q2","value":4623.657}],"drivers":["recent nominal PNFI level has risen for five straight quarters","Q2 advance release showed current-dollar GDP up 7.9 percent SAAR","BEA said Q2 investment growth reflected equipment and intellectual property gains partly offset by structures","September 2026 annual update can shift the level before the Q3 advance print","Q3 first print will include partial source data and BEA projections"],"sourceContext":["https://www.bea.gov/news/schedule/full","https://www.bea.gov/news/2026/gdp-advance-estimate-2nd-quarter-2026","https://fred.stlouisfed.org/series/PNFI","https://db.nomics.world/BEA/NIPA-T50305/A008RC-Q","https://apps.bea.gov/iTable/?ReqID=19&step=3&isuri=1&nipa_table_list=145&categories=survey"],"runAt":"2026-08-17T16:56:49Z","reasoning":[{"kind":"heading","text":"US private nonresidential fixed investment, 2026-Q3 first print"},{"kind":"text","text":"Resolver framing: this is BEA NIPA Table 5.3.5 line 2, Nonresidential, nominal seasonally adjusted annual rate. The ledger table value is in millions and the target unit is usd_billions, so resolution multiplies the official table value by 0.001."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA's 2026 release schedule for the GDP advance estimate covering 2026-Q3.","result":"BEA lists GDP (Advance Estimate), 3rd Quarter 2026 on October 29, 2026 at 8:30 AM; the same schedule page lists GDP (Advance Estimate), 2nd Quarter 2026 on July 30, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched current public BEA/FRED mirror history for PNFI, BEA account A008RC, quarterly SAAR billions of dollars.","result":"Recent fetched values were 2025-Q1 4137.819, 2025-Q2 4207.512, 2025-Q3 4293.474, 2025-Q4 4364.412, 2026-Q1 4490.516, and 2026-Q2 4623.657 usd_billions."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA's Q2 2026 advance GDP release for current-quarter macro context and source assumptions.","result":"The Q2 2026 advance release reported real GDP +1.5 percent SAAR, current-dollar GDP +7.9 percent SAAR, real final sales to private domestic purchasers +3.9 percent, and PCE price index +5.1 percent."},{"kind":"tool","tool":"official.lookup","call":"Checked the BEA-derived DBnomics NIPA-T50305 A008RC-Q page for table identity and latest line value scale.","result":"DBnomics identifies BEA NIPA Table 5.3.5 line 2 A008RC-Q as Nonresidential quarterly and shows 2026-Q2=4,623,657 in the BEA table's millions scale, equivalent to 4623.657 usd_billions after the registered 0.001 transform."},{"kind":"text","text":"Base rate/reference class: using the 2023-Q1 through 2026-Q2 quarterly level history, the outside-view one-quarter change averaged about 66.7 usd_billions. The recent five changes were stronger, about +69.7, +86.0, +70.9, +126.1, and +133.1, so pure persistence from 2026-Q2 would point somewhat above the long recent mean."},{"kind":"math","text":"Prior/update/interval: persistence prior is last observed PNFI level 4623.657 plus the 2023-Q1 to 2026-Q2 mean quarterly change of 66.7, giving 4690.4. I add about 20 for continued Q2 nominal momentum and equipment/IPP strength, while subtracting no explicit policy drag because financing-cost restraint is already visible in the recent level series, giving a point near 4710. For interval sizing, successive changes in the 2023-Q1 to 2026-Q2 fetched history have sigma = 43.5 usd_billions, so 1.28*sigma = 55.7. I widen to an 80 usd_billions half-width because the September 2026 annual update can shift the level before the Q3 first print and the advance estimate still uses partial source data plus projections; final 80 percent bounds are 4710-80=4630 and 4710+80=4790."},{"kind":"text","text":"Upside risk: a continuing AI/data-center equipment and software investment surge, stronger Q3 nominal GDP, or upward annual-update level revision would land above the interval. Downside risk: a pullback in nonresidential structures, weaker capital-goods imports/shipments, or a downward annual-update rebasing would land below the interval. An outside the interval outcome would most likely require both a large annual-update level shift and an unusually large Q3 source-data surprise."},{"kind":"forecast","point":4710,"ciLow":4630,"ciHigh":4790}]}
