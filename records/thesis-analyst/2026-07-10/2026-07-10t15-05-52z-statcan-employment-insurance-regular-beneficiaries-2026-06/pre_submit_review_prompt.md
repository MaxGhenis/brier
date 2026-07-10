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
4bb21ef60fbeaf9f353b1eff38c9399b5c627ec62de6169f07c8e2945fda0def

# Draft forecast response
{"slug":"canada-ei-regular-beneficiaries-june-2026","country":"CA","type":"data","title":"Canada regular EI beneficiaries, June 2026","question":"Statistics Canada regular Employment Insurance beneficiaries for Canada, June 2026, seasonally adjusted, beneficiary detail total, sex total, age group total, first print","unit":"thousands","pointEstimate":557.33,"ciLow":541.67,"ciHigh":574.29,"confidence":0.8,"resolutionDate":"2026-08-20","resolutionSource":"Statistics Canada Table 14-10-0011-01 and The Daily Employment Insurance release","resolutionSourceUrl":"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101","resolutionRule":"Resolve to the first Statistics Canada publication for June 2026 regular Employment Insurance beneficiaries for Canada, seasonally adjusted, beneficiary detail total, sex total, age group total, from Table 14-10-0011-01 or the same first-print The Daily release. Convert persons to thousands by multiplying by 0.001. Use the first print only and ignore later revisions or corrections.","dataPointId":"statcan.employment_insurance.regular_beneficiaries.canada.june_2026.first_print","historicalContext":[{"label":"February 2026","value":542.11},{"label":"March 2026","value":548},{"label":"April 2026","value":544.44},{"label":"December 2025","value":569.11}],"drivers":["Recent level remains above 2025","April monthly decline","Lower May unemployment rate","Seasonal summer labour-market normalization"],"sourceContext":["https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101","https://www150.statcan.gc.ca/n1/daily-quotidien/260618/dq260618d-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260522/dq260522b-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260219/cg-b001-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm","https://www150.statcan.gc.ca/n1/dai-quo/cal3-eng.htm"],"runAt":"2026-07-10T00:00:00Z","thresholdLadder":{"thresholds":[535,540,545,550,555,560,565,570,575,580,585],"cumulativeProbabilities":[0.03,0.07,0.16,0.28,0.43,0.58,0.72,0.84,0.91,0.95,0.97]},"reasoning":[{"kind":"heading","text":"Canada regular EI beneficiaries, June 2026"},{"kind":"text","text":"The target is the first Statistics Canada print for Canada, seasonally adjusted, total beneficiary detail, both sexes, all ages, from Table 14-10-0011-01. The official release schedule and target registration identify 2026-08-20 as the June 2026 resolution date."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada Table 14-10-0011-01 and April 2026 The Daily release","result":"Fetched April 2026 Canada regular EI beneficiaries: 544,440 persons, or 544.44 thousands; the monthly change was -0.5% and the year-over-year change was +3.5%."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada February and March 2026 Employment Insurance releases","result":"Fetched February 2026 regular EI beneficiaries: 542,110 persons, or 542.11 thousands; fetched March 2026: 548,000 persons, or 548.00 thousands; March increased 2,300 persons, or 0.4%, from February."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada historical Employment Insurance series chart","result":"Fetched December 2025 regular EI beneficiaries: 569,110 persons, or 569.11 thousands; the same official series showed June 2025 at 547,700 persons, July 2025 at 555,090, and November 2025 at 566,640."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada Labour Force Survey, May 2026","result":"Fetched the May 2026 Canadian unemployment rate: 6.6%, down 0.3 percentage points from April and below the recent 7.1% high in August and September 2025."},{"kind":"text","text":"The base rate is a persistent level near the mid-500-thousand range: the 2025 June-to-November path was 547.70, 555.09, 555.27, 554.27, 561.48, and 566.64 thousand, while early 2026 moved from 554.83 in January to 542.11 in February, 548.00 in March, and 544.44 in April. The reference class favors a June print near the recent level, with some downward pressure from improved labour-market conditions."},{"kind":"text","text":"Level and momentum are mixed: the current level is still above June 2025, but the February-April sequence is below the late-2025 peak. The May unemployment improvement is a downside adjustment for beneficiary inflows, while seasonal summer normalization limits the expected decline."},{"kind":"text","text":"Prior/update/interval: model prior is a local-level persistence prior using the fetched December 2025-April 2026 observations plus the June-November 2025 seasonal reference class; the update is modestly downward for the 6.6% May unemployment rate and recent April decline; successive changes over the fetched level history have sigma = 7.84 thousand, giving a nominal 80% half-width of roughly 1.28*sigma = 10.04 thousand. The ladder-implied half-width is 16.31 thousand, widened to about 1.63 times the sigma width because May and June prints are not yet observed and the level series has shown several large month-to-month reversals."},{"kind":"math","text":"Ladder: P(X <= 535) = 0.03; P(X <= 540) = 0.07; P(X <= 545) = 0.16; P(X <= 550) = 0.28; P(X <= 555) = 0.43; P(X <= 560) = 0.58; P(X <= 565) = 0.72; P(X <= 570) = 0.84; P(X <= 575) = 0.91; P(X <= 580) = 0.95; P(X <= 585) = 0.97. Linear interpolation gives ciLow at 0.10 as 541.67, pointEstimate at 0.50 as 557.33, and ciHigh at 0.90 as 574.29, all in thousands and rounded to the table's 0.01-thousand precision."},{"kind":"text","text":"The upside risk is a renewed rise toward the late-2025 level, particularly if the lower unemployment rate reflects weaker participation rather than stronger hiring. The downside risk is a continuation of the February-April decline after improved employment conditions. A renewed labour-market shock or administrative change would be outside the interval and could land above 574.29 or below 541.67 thousand."},{"kind":"forecast","point":557.33,"ciLow":541.67,"ciHigh":574.29}]}
