# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.bed.private_gross_job_gains.opening_establishments
- period: 2025-Q4
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bls-bed-opening-establishment-gross-job-gains-q4-2025"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "bls.bed.private_gross_job_gains.opening_establishments.2025_q4.first_print"
- resolutionSourceUrl: "https://www.bls.gov/news.release/cewbd.toc.htm"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-29"}, "field": "Gross job gains at opening establishments; private sector; seasonally adjusted", "releasePolicy": "first_print", "sourceSeriesId": "BLS BED Table 1", "sourceUrl": "https://www.bls.gov/news.release/cewbd.toc.htm", "table": "Business Employment Dynamics, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-15-0da8b2bfeb748c0bd47c8b30aed2a4ac58581d3c578ffd0c870928a8c55d9740.json"
- targetContentHash: "0da8b2bfeb748c0bd47c8b30aed2a4ac58581d3c578ffd0c870928a8c55d9740"
- registrationCommit: "4ca8bf2478e8cea37b8112b8821dc9865efdce9c"
- registeredAtUtc: "2026-07-15T21:20:34Z"
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
8b80c2db2f36957b3a36181929ef6e90e2cacded423e94fdfb6fb046fd14c624

# Draft forecast response
{"slug":"bls-bed-opening-establishment-gross-job-gains-q4-2025","country":"US","type":"data","title":"US opening-establishment job gains, Q4 2025","question":"What will BLS first report for private-sector gross job gains at opening establishments in 2025 Q4, seasonally adjusted, in thousands?","unit":"thousands","pointEstimate":1635,"ciLow":1583,"ciHigh":1687,"confidence":0.8,"resolutionDate":"2026-07-29","resolutionSource":"U.S. Bureau of Labor Statistics Business Employment Dynamics release","resolutionSourceUrl":"https://www.bls.gov/news.release/cewbd.toc.htm","resolutionRule":"Resolve to the first value published for 2025 Q4 in BLS Business Employment Dynamics Table 1, Gross job gains—Opening establishments—Total private, seasonally adjusted, in thousands. Use the displayed integer value, equivalent to rounding to the nearest thousand jobs, and ignore all subsequent revisions.","dataPointId":"bls.bed.private_gross_job_gains.opening_establishments.2025_q4.first_print","historicalContext":[{"label":"2023-Q1","value":1570},{"label":"2023-Q2","value":1608},{"label":"2023-Q3","value":1586},{"label":"2023-Q4","value":1637},{"label":"2024-Q1","value":1531},{"label":"2024-Q2","value":1561},{"label":"2024-Q3","value":1564},{"label":"2024-Q4","value":1660},{"label":"2025-Q1","value":1589},{"label":"2025-Q2","value":1527},{"label":"2025-Q3","value":1597}],"drivers":["Recent rebound from 1,527 thousand to 1,597 thousand","Recent Q4 prints of 1,637 thousand and 1,660 thousand","Soft 2025 gross-job-gain environment","Opening-establishment volatility around a stable 1.6 million level"],"sourceContext":["https://www.bls.gov/news.release/cewbd.t01.htm","https://www.bls.gov/schedule/news_release/cewbd.htm","https://www.bls.gov/news.release/archives/cewbd_02262026.pdf"],"runAt":"2026-07-15T21:22:05Z","reasoning":[{"kind":"heading","text":"BLS opening-establishment gross job gains, 2025 Q4"},{"kind":"text","text":"The target is BLS BED Table 1, total-private gross job gains at opening establishments, seasonally adjusted and measured in thousands—not the opening-firm series or an unadjusted variant. Resolution uses the strict first 2025-Q4 print without correction-day or revision exceptions."},{"kind":"tool","tool":"official.lookup","call":"Fetch recent observations from BLS BED Table 1.","result":"BLS reports opening-establishment gross job gains of 1,589 thousand in 2025 Q1, 1,527 thousand in Q2, and 1,597 thousand in Q3, seasonally adjusted."},{"kind":"tool","tool":"official.lookup","call":"Fetch the pre-2025 reference class from BLS BED Table 1.","result":"The 2024 quarterly values were 1,531, 1,561, 1,564, and 1,660 thousand; the 2023 values were 1,570, 1,608, 1,586, and 1,637 thousand."},{"kind":"tool","tool":"official.lookup","call":"Check related total gross job gains and the official release schedule.","result":"Total private gross job gains were 7,448 thousand in 2025 Q1, 7,585 thousand in Q2, and 7,475 thousand in Q3; the BLS calendar schedules the 2025 Q4 BED release for July 29, 2026 at 10:00 AM."},{"kind":"text","text":"The outside-view base rate is the recent 2023-Q1 through 2025-Q3 reference class: opening-establishment gains have centered near 1.585 million, while the two latest Q4 observations were higher at 1.637 million and 1.660 million."},{"kind":"text","text":"Level and momentum point in different directions: the series remains near 1.6 million and rebounded 70 thousand in Q3, but total gross gains eased from 7.585 million to 7.475 million. Recent Q4 strength supports an elevated anchor, while the softer 2025 labor-flow backdrop warrants a modest downward adjustment. No discrete policy or identifiable one-off mechanism justifies a larger shift."},{"kind":"math","text":"Prior/update/interval: A recent-Q4 persistence model uses the 2023-Q4 and 2024-Q4 average, (1,637 + 1,660) / 2 = 1,648.5 thousand, based on the 11-quarter 2023-Q1–2025-Q3 historical sample. Apply a -13.5 thousand adjustment for softer 2025 total gross gains, giving 1,635.0. Because this is a flow series, dispersion is computed from the values themselves: sample sigma = 40.7 thousand. The normal 80% half-width is 1.28*sigma = 1.28*40.7 = 52.1 thousand, implying 1,635 ± 52, or final bounds of 1,583 to 1,687 thousand."},{"kind":"text","text":"Upside risk comes from another Q4 opening surge comparable to or stronger than 2024 and would land above the interval if the first print exceeds 1,687 thousand. Downside risk comes from broad-based establishment-formation weakness or reversal of the Q3 rebound and would land below the interval if the print is under 1,583 thousand."},{"kind":"forecast","point":1635,"ciLow":1583,"ciHigh":1687}]}
