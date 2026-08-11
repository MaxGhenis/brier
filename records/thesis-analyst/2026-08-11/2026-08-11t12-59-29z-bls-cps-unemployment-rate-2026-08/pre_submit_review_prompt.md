# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.unemployment_rate
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "unemployment-rate-august-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.cps.unemployment_rate.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-09-11", "start": "2026-09-03"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-11", "start": "2026-09-03"}, "field": "bls.cps.unemployment_rate", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.unemployment_rate", "sourceUrl": "https://www.bls.gov/news.release/empsit.nr0.htm", "table": "U.S. Bureau of Labor Statistics, Employment Situation (Current Population Survey)", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-ee40ca45dbbd92d41117ea4d5d678fe815ae3a21d5db698050b009e0f27fa0e4.json"
- targetContentHash: "ee40ca45dbbd92d41117ea4d5d678fe815ae3a21d5db698050b009e0f27fa0e4"
- registrationCommit: "e8c13ea71f583ab7105a64de5fe4c8594cfcb6d0"
- registeredAtUtc: "2026-08-11T12:50:27Z"
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
88810f15b36fbac69dfe76e45c17491d00f359cb366a770606026603a5b275ac

# Draft forecast response
{"slug":"unemployment-rate-august-2026","country":"US","type":"data","title":"US unemployment rate, August 2026","question":"What will the BLS Current Population Survey U-3 unemployment rate, seasonally adjusted, be for August 2026 in the first Employment Situation print?","unit":"percent","pointEstimate":4.2,"ciLow":4,"ciHigh":4.3,"confidence":0.8,"resolutionDate":"2026-09-04","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/empsit.t01.htm","resolutionRule":"Resolve to the first-print BLS Employment Situation Table A-1 total unemployment rate, seasonally adjusted, for August 2026, reported in percent to one decimal place. Use the initial release value only; do not use later monthly revisions, annual population-control revisions, or corrected values unless the first posted release itself is replaced before ordinary public access.","dataPointId":"bls.cps.unemployment_rate.august_2026.first_print","historicalContext":[{"label":"July 2026","value":4.1},{"label":"June 2026","value":4.2},{"label":"May 2026","value":4.3},{"label":"April 2026","value":4.3},{"label":"March 2026","value":4.3}],"drivers":["July unemployment rate was 4.1 percent after a falling labor force participation rate","Recent CPS rate changes are small, with 2026 readings clustered between 4.1 and 4.4 percent","July payroll employment fell by 23,000, a soft-labor-market signal that offsets pure downward unemployment momentum","Initial claims remained low near 199,000 in the latest public report, limiting the case for a sharp August unemployment jump"],"sourceContext":["https://www.bls.gov/news.release/empsit.nr0.htm","https://www.bls.gov/news.release/empsit.t01.htm","https://www.bls.gov/charts/employment-situation/civilian-unemployment-rate.htm","https://www.bls.gov/schedule/news_release/empsit.htm?categoryId=1&orient=1"],"runAt":"2026-08-11T12:59:56Z","reasoning":[{"kind":"heading","text":"US CPS unemployment rate forecast for August 2026"},{"kind":"text","text":"Resolver framing: this targets the BLS Current Population Survey total U-3 unemployment rate, seasonally adjusted, series LNS14000000 as displayed in Employment Situation Table A-1 for August 2026, first print only."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Employment Situation release schedule for the August 2026 reference month.","result":"BLS lists August 2026 Employment Situation release date Sep. 04, 2026 at 08:30 AM; the same schedule lists July 2026 on Aug. 07, 2026 and September 2026 on Oct. 02, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the current BLS Employment Situation Summary for July 2026.","result":"The July 2026 summary reports nonfarm payroll employment -23,000, unemployment rate 4.1 percent, unemployed people 6.9 million, labor force participation rate 61.4 percent, and prior May/June payroll revisions totaling -103,000."},{"kind":"tool","tool":"official.lookup","call":"Read BLS Table A-1 for the seasonally adjusted total unemployment rate and labor-force details.","result":"Table A-1 reports total unemployment rate 4.3 in Mar. 2026, 4.3 in Apr. 2026, 4.3 in May 2026, 4.2 in June 2026, and 4.1 in July 2026; it also reports July 2026 labor force 169,094 thousand, employed 162,177 thousand, unemployed 6,916 thousand, and participation rate 61.4."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS civilian unemployment rate chart table for recent reference-class history.","result":"The BLS chart shows seasonally adjusted total unemployment rates of Jan. 2026 4.3, Feb. 2026 4.4, Mar. 2026 4.3, Apr. 2026 4.3, May 2026 4.3, June 2026 4.2, and July 2026 4.1; it also shows June 2025 4.1, July 2025 4.3, Aug. 2025 4.3, Sept. 2025 4.4, Nov. 2025 4.5, and Dec. 2025 4.4."},{"kind":"text","text":"Base rate/reference class: for a one-month-ahead level forecast of a rounded unemployment rate, the strongest base rate is persistence plus the empirical monthly-change distribution. Recent values have sat in a narrow 4.1 to 4.4 percent range in 2026, so large moves are possible but not the central case."},{"kind":"math","text":"Prior/update/interval: persistence prior is July 2026 unemployment rate 4.1. Historical sample is monthly changes from the BLS chart from Jan. 2024 through July 2026, skipping the missing Oct. 2025 observation; sigma = 0.11 percentage point from successive monthly changes. Update components: +0.06 for weak July payrolls and downward payroll revisions, +0.03 for the participation-rate decline being unlikely to keep lowering U-3 at the same pace, and -0.04 for still-low claims/no layoff surge context, giving an unrounded mean near 4.15. Interval method: 80 percent half-width is roughly 1.28*sigma = 1.28*0.11 = 0.14, so 4.15 +/- 0.14 gives about 4.01 to 4.29, rounded to the target display as 4.0 to 4.3 with point 4.2."},{"kind":"text","text":"Counter-considerations: upside risk is an August household-survey employment drop or rebound in participation that would push unemployment to 4.4 or higher, outside the interval. Downside risk is another participation decline or noisy drop in unemployed workers that would keep the rate at 3.9 or below, also outside the interval."},{"kind":"forecast","point":4.2,"ciLow":4,"ciHigh":4.3}]}
