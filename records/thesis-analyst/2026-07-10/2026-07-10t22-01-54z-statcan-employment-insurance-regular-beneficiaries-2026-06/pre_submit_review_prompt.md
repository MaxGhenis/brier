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
{"slug":"canada-ei-regular-beneficiaries-june-2026","country":"CA","type":"data","title":"Canada regular EI beneficiaries, June 2026","question":"Statistics Canada regular Employment Insurance beneficiaries, Canada, both sexes, age 15 years and over, seasonally adjusted, June 2026 first print","unit":"thousands","pointEstimate":542.75,"ciLow":529.17,"ciHigh":561,"confidence":0.8,"resolutionDate":"2026-08-20","resolutionSource":"Statistics Canada Table 14-10-0011-01 and The Daily Employment Insurance release","resolutionSourceUrl":"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101","resolutionRule":"Resolve to the first Statistics Canada publication for June 2026 regular Employment Insurance beneficiaries for Canada, seasonally adjusted, beneficiary detail total, sex total, age group total, from Table 14-10-0011-01 or the same first-print The Daily release. Convert persons to thousands by multiplying by 0.001. Use the first print only; ignore later revisions or table corrections unless the first-print rule itself is changed by Statistics Canada before release.","dataPointId":"statcan.employment_insurance.regular_beneficiaries.canada.june_2026.first_print","historicalContext":[{"label":"December 2025","value":567.62},{"label":"January 2026","value":559.02},{"label":"February 2026","value":550.35},{"label":"March 2026","value":547.44},{"label":"April 2026","value":544.44}],"drivers":["Recent seasonally adjusted beneficiary level and four-month decline","May labour-market improvement, with unemployment rate at 6.6%","Normal monthly administrative and seasonal-adjustment noise"],"sourceContext":["https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101","https://www150.statcan.gc.ca/n1/daily-quotidien/260618/dq260618d-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm","https://www150.statcan.gc.ca/n1/release-diffusion/2026-eng.pdf"],"runAt":"2026-07-10T22:02:04Z","thresholdLadder":{"thresholds":[520,525,530,535,540,545,550,555,560,565,570,575,580],"cumulativeProbabilities":[0.03,0.06,0.11,0.2,0.39,0.59,0.68,0.8,0.88,0.93,0.96,0.98,0.99]},"reasoning":[{"kind":"heading","text":"Canada regular EI beneficiaries: June 2026 first print"},{"kind":"text","text":"The resolver is Table 14-10-0011-01, series variant regular benefits, Canada, both sexes, age 15 years and over, seasonally adjusted; all anchors below use that same variant. The table is in persons and the target converts it to thousands. The ledger specifies 2026-08-20, while Statistics Canada's 2026 release-calendar PDF lists Employment Insurance for June on August 21; this is a concrete date discrepancy retained against the supplied target contract rather than silently changing it."},{"kind":"tool","tool":"official.lookup","call":"Fetched Statistics Canada Table 14-10-0011-01 for Canada, regular benefits, both sexes, age 15 years and over, seasonally adjusted.","result":"Fetched persons: December 2025 567,620; January 2026 559,020; February 2026 550,350; March 2026 547,440; April 2026 544,440, equivalent to 567.62, 559.02, 550.35, 547.44, and 544.44 thousands."},{"kind":"tool","tool":"official.lookup","call":"Fetched Statistics Canada The Daily Employment Insurance release for April 2026.","result":"Fetched April 2026 regular EI beneficiaries of 544,440 for Canada; the April level was 3,000 lower than March's 547,440 in the seasonally adjusted series."},{"kind":"tool","tool":"official.lookup","call":"Fetched Statistics Canada The Daily Labour Force Survey release for May 2026 as current labour-market context.","result":"Fetched May 2026 Canadian unemployment rate of 6.6%, down from the recent 7.1% high in August and September 2025; youth unemployment was 13.4% in May 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched Statistics Canada's 2026-2027 release-date calendar for Employment Insurance.","result":"Fetched calendar entries showing Employment Insurance reference April 2026 on June 19, May 2026 on July 23, and June 2026 on August 21, 2026."},{"kind":"text","text":"Prior/update/interval: The persistence-with-recent-trend prior uses the fetched December-to-April reference class (567.62, 559.02, 550.35, 547.44, 544.44 thousand), whose decline decelerated into March-April. I update modestly lower for the May 6.6% unemployment rate, but retain substantial administrative/seasonal-adjustment uncertainty. The elicited ladder spans 520 to 580 thousand; its 10th and 90th interpolations set the 80% interval."},{"kind":"math","text":"Ladder: P(X <= 520) = 0.03; P(X <= 525) = 0.06; P(X <= 530) = 0.11; P(X <= 535) = 0.20; P(X <= 540) = 0.39; P(X <= 545) = 0.59; P(X <= 550) = 0.68; P(X <= 555) = 0.80; P(X <= 560) = 0.88; P(X <= 565) = 0.93; P(X <= 570) = 0.96; P(X <= 575) = 0.98; P(X <= 580) = 0.99. Linear interpolation gives 10th percentile at 529.17, median at 542.75, and 90th percentile at 561.00 thousand."},{"kind":"text","text":"Upside risk: a renewed rise in job separations or weaker June hiring would lift beneficiaries above the central estimate. Downside risk: continued re-employment and fewer new claims would reduce the level. Outside the interval: a broad labour-market deterioration would land above 561.00 thousand, while an unusually sharp benefit exit/claim decline would land below 529.17 thousand."},{"kind":"forecast","point":542.75,"ciLow":529.17,"ciHigh":561}]}
