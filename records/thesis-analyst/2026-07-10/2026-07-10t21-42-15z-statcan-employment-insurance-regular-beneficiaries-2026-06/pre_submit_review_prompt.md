# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: statcan.employment_insurance.regular_beneficiaries
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "canada-ei-regular-beneficiaries-june-2026"
- country: "CA"
- targetUnit: "thousands"
- dataPointId: "statcan.employment_insurance.regular_beneficiaries.canada.june_2026.first_print"
- resolutionDate: "2026-08-20"
- resolutionSource: "Statistics Canada Table 14-10-0011-01 and The Daily Employment Insurance release"
- resolutionSourceUrl: "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101"
- resolutionRule: "Resolve to the first Statistics Canada publication for June 2026 regular Employment Insurance beneficiaries for Canada, seasonally adjusted, beneficiary detail total, sex total, age group total, from Table 14-10-0011-01 or the same first-print The Daily release. Convert persons to thousands by multiplying by 0.001. Use the first print only; ignore later revisions or table corrections unless the first-print rule itself is changed by Statistics Canada before release."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-08-27", "start": "2026-08-19"}, "field": "statcan.employment_insurance.regular_beneficiaries", "releasePolicy": "first_print", "sourceSeriesId": "statcan.employment_insurance.regular_beneficiaries", "sourceUrl": "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101", "table": "Statistics Canada Employment Insurance Statistics, Table 14-10-0011-01 and The Daily release for May 2026", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-2071f24c9311aaa43cd5bf3d2af243438c9d0aa1124763f0d51d599364e0d06b.json"
- targetContentHash: "2071f24c9311aaa43cd5bf3d2af243438c9d0aa1124763f0d51d599364e0d06b"
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
af40066e19803db6294008112435a93cf29920294ed9fe536ca494b8a7c0a22a

# Draft forecast response
{"slug":"canada-ei-regular-beneficiaries-june-2026","country":"CA","type":"data","title":"Canada regular EI beneficiaries, June 2026","question":"What will Statistics Canada first report for Canada regular Employment Insurance beneficiaries in June 2026, seasonally adjusted, beneficiary detail total, sex total, age group total?","unit":"thousands","pointEstimate":549.58,"ciLow":527.5,"ciHigh":573.57,"confidence":0.8,"resolutionDate":"2026-08-20","resolutionSource":"Statistics Canada Table 14-10-0011-01 and The Daily Employment Insurance release","resolutionSourceUrl":"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101","resolutionRule":"Resolve to the first Statistics Canada publication for June 2026 regular Employment Insurance beneficiaries for Canada, seasonally adjusted, beneficiary detail total, sex total, age group total, from Table 14-10-0011-01 or the same first-print The Daily release. Convert persons to thousands by multiplying by 0.001. Use the first print only; ignore later revisions or table corrections unless the first-print rule itself is changed by Statistics Canada before release.","dataPointId":"statcan.employment_insurance.regular_beneficiaries.canada.june_2026.first_print","historicalContext":[{"label":"February 2026 first print","value":542.11},{"label":"March 2026 first print","value":548},{"label":"April 2026 first print","value":544.44}],"drivers":["April level near 544 thousand","June unemployment rate of 6.5%","May employment gain limits near-term inflows","EI administrative eligibility and processing lags","Temporary EI measures support beneficiary duration"],"sourceContext":["https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101","https://www150.statcan.gc.ca/n1/daily-quotidien/260618/dq260618d-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260522/dq260522b-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260423/dq260423c-eng.htm","https://www150.statcan.gc.ca/n1/release-diffusion/2026-eng.pdf","https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm"],"runAt":"2026-07-10T21:42:36Z","thresholdLadder":{"thresholds":[515,520,525,530,535,540,545,550,555,560,565,570,575,580],"cumulativeProbabilities":[0.03,0.05,0.08,0.12,0.18,0.27,0.39,0.51,0.62,0.72,0.79,0.85,0.92,0.96]},"reasoning":[{"kind":"heading","text":"Canada regular EI beneficiaries, June 2026 first print"},{"kind":"text","text":"The target is the first Statistics Canada print for June 2026 in Table 14-10-0011-01: Canada, seasonally adjusted, regular benefits, beneficiary detail total, sex total, and age group total. Table values are persons and are converted to thousands by multiplying by 0.001. Later revisions are excluded."},{"kind":"tool","tool":"official.lookup","call":"Read Statistics Canada The Daily Employment Insurance release for April 2026 and Table 14-10-0011-01.","result":"Fetched Canada regular EI beneficiaries of 544,440 persons in April 2026, a monthly change of -0.5% and a 12-month change of +3.5%."},{"kind":"tool","tool":"official.lookup","call":"Read Statistics Canada The Daily Employment Insurance releases for February and March 2026.","result":"Fetched 542,110 persons for February 2026 and 548,000 persons for March 2026; March rose by 2,300 persons or 0.4%, while February had fallen by 8,700 or 1.6%."},{"kind":"tool","tool":"official.lookup","call":"Read Statistics Canada Labour Force Survey release for May 2026.","result":"Fetched May 2026 employment growth of 88,000 or 0.4%, unemployment of 6.6%, and a January-to-April employment decline of 112,000."},{"kind":"tool","tool":"official.lookup","call":"Check Statistics Canada's official 2026-2027 release-date publication for Employment Insurance.","result":"The official schedule lists Employment Insurance for reference period June 2026 on August 19, 2026; the supplied ledger instead fixes resolutionDate at August 20, 2026, a discrepancy of 1 day."},{"kind":"text","text":"The ledger date is retained to keep this forecast tied to the registered target, but its August 20 date conflicts with the official Statistics Canada schedule, which currently shows August 19. The exact-series stable source is Table 14-10-0011-01."},{"kind":"text","text":"The outside-view reference class is the same-variant first-print sequence: 542.11 thousand in February, 548.00 thousand in March, and 544.44 thousand in April. Its range of 5.89 thousand anchors the central rungs, while the broader 515–580 thousand span allows for two months of administrative inflows, exits, and revisions to seasonal factors."},{"kind":"math","text":"Prior/update/interval: A level-persistence model starts from April's 544.44 thousand. The historical sample is the February-April first-print sequence of 542.11, 548.00, and 544.44 thousand. Adjustments are approximately +5 thousand for lagged softness and temporary EI-policy support, partly offset by May's 88,000 employment gain and unemployment easing to 6.6%. The reference-class range anchors the dense central rungs from 540 to 550, while administrative lag, eligibility, exhaustion, and labour-market uncertainty widen the elicited ladder to 515–580. The interval method is direct threshold-ladder inversion, implying final 80% bounds of 527.50 to 573.57 thousand."},{"kind":"math","text":"Ladder: P(X <= 515) = 0.03; P(X <= 520) = 0.05; P(X <= 525) = 0.08; P(X <= 530) = 0.12; P(X <= 535) = 0.18; P(X <= 540) = 0.27; P(X <= 545) = 0.39; P(X <= 550) = 0.51; P(X <= 555) = 0.62; P(X <= 560) = 0.72; P(X <= 565) = 0.79; P(X <= 570) = 0.85; P(X <= 575) = 0.92; P(X <= 580) = 0.96. Linear interpolation gives the 10th percentile at 527.50, median at 549.58, and 90th percentile at 573.57."},{"kind":"text","text":"Upside risk comes from delayed claims following early-2026 employment weakness, longer benefit duration under temporary EI measures, or concentrated manufacturing losses; an abrupt deterioration would land above the interval. Downside risk comes from sustained job gains, rapid claimant re-employment, or benefit exhaustion; a sharp normalization would land below the interval. The principal outside the interval scenario is a large administrative or policy-driven discontinuity."},{"kind":"forecast","point":549.58,"ciLow":527.5,"ciHigh":573.57}]}
