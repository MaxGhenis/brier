# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.productivity.nonfarm_qoq_prelim
- period: 2026-Q3
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-nonfarm-productivity-q3-2026-prelim"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.productivity.nonfarm_qoq_prelim.2026_q3.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-11-13", "start": "2026-10-30"}, "field": "bls.productivity.nonfarm_qoq_prelim", "releasePolicy": "first_print", "sourceSeriesId": "bls.productivity.nonfarm_qoq_prelim", "sourceUrl": "https://www.bls.gov/news.release/prod2.t02.htm", "table": "U.S. Bureau of Labor Statistics Productivity and Costs news release, Table 2", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-305e7cc4fb0cea02fc06d094b277fc0b19edb85507cbcefe73e0b64e7d6e02df.json"
- targetContentHash: "305e7cc4fb0cea02fc06d094b277fc0b19edb85507cbcefe73e0b64e7d6e02df"
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
a5f82f6f99aa2d4b13c7ef70e61474f0058363e80e872400ed595985a2300bcf

# Draft forecast response
{"slug":"us-nonfarm-productivity-q3-2026-prelim","country":"US","type":"data","title":"US Nonfarm Productivity Q3 2026 Preliminary","question":"What will BLS first report for nonfarm business sector labor productivity, seasonally adjusted percent change from previous quarter at annual rate, in 2026 Q3 preliminary Table 2?","unit":"percent_growth","pointEstimate":1.7,"ciLow":-1.7,"ciHigh":5.1,"confidence":0.8,"resolutionDate":"2026-11-05","resolutionSource":"U.S. Bureau of Labor Statistics Productivity and Costs news release, Table 2","resolutionSourceUrl":"https://www.bls.gov/news.release/prod2.t02.htm","resolutionRule":"Resolve to the first BLS Productivity and Costs preliminary release for Third Quarter 2026, Table 2, Nonfarm business sector, row 2026 III, Labor productivity, seasonally adjusted percent change from previous quarter at annual rate. Use the one-decimal value printed in the first official release on 2026-11-05 and do not apply later revised releases.","dataPointId":"bls.productivity.nonfarm_qoq_prelim.2026_q3.first_print","historicalContext":[{"label":"2026 Q1 revised, BLS/FRED PRS85006092","value":0.3},{"label":"2025 Q4 revised, BLS/FRED PRS85006092","value":1.6},{"label":"2025 Q3 revised, BLS/FRED PRS85006092","value":5.2},{"label":"2025 Q2 revised, BLS/FRED PRS85006092","value":4.2},{"label":"2021Q1-2026Q1 revised-history sigma used for interval","value":2.64}],"drivers":["Recent revised productivity slowed to 0.3 percent in 2026 Q1 after strong 2025 readings","Post-2021 reference class remains volatile but centered near 1.5 percent annualized","Q3 first print will depend on early GDP/output and hours estimates available to BLS in November","AI/capital-deepening narrative supports a modest positive trend but not a large near-term jump"],"sourceContext":["https://www.bls.gov/schedule/news_release/prod2.htm","https://www.bls.gov/news.release/prod2.t02.htm","https://fred.stlouisfed.org/series/PRS85006092","https://fred.stlouisfed.org/data/PRS85006092"],"runAt":"2026-07-10T05:42:00Z","reasoning":[{"kind":"heading","text":"US nonfarm business labor productivity, 2026 Q3 preliminary first print"},{"kind":"text","text":"Framing and exact resolver: target is BLS Productivity and Costs Table 2, nonfarm business sector Labor productivity, seasonally adjusted percent change from previous quarter at an annual rate, for 2026 Q3 preliminary. The FRED/BLS series code used for history is PRS85006092; resolution remains the BLS first-print Table 2, not FRED."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Productivity and Costs release schedule for the Third Quarter 2026 preliminary release.","result":"BLS schedule lists Third Quarter 2026 (P) on Nov. 05, 2026 at 08:30 AM and Third Quarter 2026 (R) on Dec. 08, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Fetched current BLS Productivity and Costs Table 2 for nonfarm business sector labor productivity and components.","result":"BLS Table 2 shows 2026 Q1 labor productivity 0.3, output 1.0, hours worked 0.7; 2025 Q4 labor productivity 1.6, 2025 Q3 5.2, 2025 Q2 4.2, 2025 Q1 -0.9."},{"kind":"tool","tool":"history.lookup","call":"Fetched FRED mirror of BLS PRS85006092, Percent Change at Annual Rate, Seasonally Adjusted, quarterly.","result":"FRED PRS85006092 reports Q1 2026 0.3, Q4 2025 1.6, Q3 2025 5.2, Q2 2025 4.2, Q1 2025 -0.9; the date range is 1947-04-01 to 2026-01-01 and last updated 2026-06-04 7:41 AM CDT."},{"kind":"tool","tool":"history.lookup","call":"Read recent BLS/FRED history for the post-2020 reference class used to size uncertainty.","result":"For 2021Q1-2026Q1 PRS85006092 values are 2.9, 0.8, -2.4, 2.3, -4.9, -2.9, 0.2, 2.3, 0.9, 4.1, 5.1, 3.9, 0.2, 3.7, 3.7, 1.4, -0.9, 4.2, 5.2, 1.6, 0.3."},{"kind":"text","text":"Base rate/reference class: the post-2020 nonfarm business productivity values average about 1.5 percent annualized, while the 2023-2025 subset is stronger at about 2.8 percent. I put more weight on the broader post-2020 base rate because quarterly productivity first prints are noisy and 2025 likely included tariff and inventory timing effects."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class prior is the 2021Q1-2026Q1 PRS85006092 mean, 31.7/21 = 1.51. I add +0.2 for moderate trend productivity and likely normalization after the weak 2026 Q1 print, giving point = 1.7. For this change-rate series I compute sigma from the fetched values themselves: squared deviations from 1.51 sum to about 146.4, variance = 146.4/21 = 6.97, sigma = 2.64. The 80 percent normal half-width is roughly 1.28*sigma = 1.28*2.64 = 3.38, so 1.7 +/- 3.4 gives -1.7 to 5.1 after one-decimal rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a Q3 output rebound with flat or falling hours, which would land above the interval if productivity prints above 5.1. Downside risk is weak real output with continued hours growth, which would land below the interval if productivity prints below -1.7. A large inventory/tariff timing swing or a recession-style hours adjustment is the main outside the interval scenario."},{"kind":"forecast","point":1.7,"ciLow":-1.7,"ciHigh":5.1}]}
