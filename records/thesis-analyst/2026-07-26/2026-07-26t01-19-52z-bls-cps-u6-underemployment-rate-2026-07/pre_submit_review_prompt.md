# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.u6_underemployment_rate
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "u6-underemployment-rate-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.cps.u6_underemployment_rate.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-07", "start": "2026-08-07"}, "field": "U6RATE", "releasePolicy": "first_print", "sourceSeriesId": "U6RATE", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=U6RATE", "table": "Employment Situation, Table A-15", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-512ba8158233c1abf89904f08899c08d8a4638f56115874fc1f508cdce11cbb4.json"
- targetContentHash: "512ba8158233c1abf89904f08899c08d8a4638f56115874fc1f508cdce11cbb4"
- registrationCommit: "145f6612f225710a4621f124b13bf5d5ae5d97ac"
- registeredAtUtc: "2026-07-26T00:55:04Z"
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
f7381e7184ba0e3c5342f3f1da5afaa23cfcd51c0d7029e961efe71aa913fe5e

# Draft forecast response
{"slug":"u6-underemployment-rate-july-2026","country":"US","type":"data","title":"US U-6 Underemployment Rate, July 2026","question":"What will the U.S. Bureau of Labor Statistics first report for the seasonally adjusted U-6 underemployment rate in Employment Situation Table A-15 for July 2026?","unit":"percent","pointEstimate":8.0,"ciLow":7.7,"ciHigh":8.2,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-15","resolutionSourceUrl":"https://www.bls.gov/news.release/empsit.t15.htm","resolutionRule":"Resolve to the first BLS Employment Situation print for July 2026, Table A-15, seasonally adjusted U-6 rate, series LNS13327709/U6RATE, in percent rounded to one decimal. Do not use later revisions or FRED/ALFRED updates except as a vintage mirror of the first print.","dataPointId":"bls.cps.u6_underemployment_rate.2026_07.first_print","historicalContext":[{"label":"2026-06 U-6 SA","value":7.9},{"label":"2026-05 U-6 SA","value":8.1},{"label":"2026-04 U-6 SA","value":8.2},{"label":"2026-03 U-6 SA","value":8.0},{"label":"2026-02 U-6 SA","value":7.9}],"drivers":["June U-6 fell to 7.9 after May 8.1 and April 8.2","U-3 unemployment rate eased to 4.2 in June but remained near recent 4.3 prints","June payroll growth slowed to 57,000 with prior-month downward revisions","Part-time for economic reasons and marginal attachment remained elevated enough to keep U-6 near 8 percent"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm?categoryId=1&orient=1","https://www.bls.gov/cps/publications/release-calendar.htm","https://www.bls.gov/news.release/archives/empsit_07022026.htm","https://fred.stlouisfed.org/series/U6RATE"],"runAt":"2026-07-26T01:20:21Z","reasoning":[{"kind":"heading","text":"July 2026 U-6 first-print forecast"},{"kind":"text","text":"Framing and exact resolver: this targets BLS CPS Table A-15, seasonally adjusted U-6, series LNS13327709/U6RATE, for July 2026. The ledger uses ALFRED as the vintage adapter, but the economic object and resolution source are the BLS Employment Situation first print."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Employment Situation release schedule for the July 2026 reference month.","result":"BLS schedule lists July 2026 Employment Situation release on 2026-08-07 at 08:30 AM; June 2026 was released 2026-07-02 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Read BLS archived Employment Situation for June 2026, Table A-15, seasonally adjusted alternative measures.","result":"Fetched U-6 values: Feb 2026 7.9, Mar 2026 8.0, Apr 2026 8.2, May 2026 8.1, Jun 2026 7.9; June 2025 was 8.1."},{"kind":"tool","tool":"official.lookup","call":"Read BLS June 2026 Employment Situation summary and household detail for labor-market context.","result":"Fetched June 2026 unemployment rate 4.2 percent, nonfarm payroll employment +57,000, labor force participation rate 61.5 percent, part time for economic reasons 4.7 million, marginally attached 1.8 million, discouraged workers 477,000."},{"kind":"tool","tool":"public.mirror.lookup","call":"Checked FRED U6RATE mirror for latest vintage context and next-release metadata.","result":"FRED showed Jun 2026 U6RATE 7.9 percent, May 2026 8.1, Apr 2026 8.2, Mar 2026 8.0, Feb 2026 7.9, updated 2026-07-02 8:31 AM CDT, next release date 2026-08-07."},{"kind":"text","text":"Base rate/reference class: recent one-month moves in this level rate are small and mean-reverting around roughly 8.0. The reference class used here is the last four official month-to-month changes in the same seasonally adjusted U-6 series: +0.1, +0.2, -0.1, and -0.2 percentage point."},{"kind":"math","text":"Prior/update/interval: persistence prior is June U-6 = 7.9; historical sample is Feb-Jun 2026 BLS Table A-15 values 7.9, 8.0, 8.2, 8.1, 7.9. Adjustment components: +0.03 for weaker payroll growth and downward revisions, +0.02 because U-6 was still near its recent 8.02 five-month average, and 0.00 for no clear July-specific policy or one-off shock, giving 7.9 + 0.05 = 7.95, rounded to point 8.0. For the interval, successive changes are +0.1, +0.2, -0.1, -0.2, so sigma = 0.183 percentage point and 1.28*sigma = 0.234; 7.95 +/- 0.234 gives 7.72 to 8.18, rounded to an 80% interval of 7.7 to 8.2."},{"kind":"text","text":"Counter-considerations: upside risk is a July jump in involuntary part-time work or marginal attachment that would land above the interval, especially if the June payroll weakness was the start of a broader deterioration. Downside risk is a rebound in full-time employment and lower marginal attachment that would land below the interval. Outside the interval would most likely require a broad household-survey swing rather than ordinary month-to-month noise."},{"kind":"forecast","point":8.0,"ciLow":7.7,"ciHigh":8.2}]}
