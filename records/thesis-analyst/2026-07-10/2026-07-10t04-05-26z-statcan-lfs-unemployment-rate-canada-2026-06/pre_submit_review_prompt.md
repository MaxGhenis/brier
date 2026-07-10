# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: statcan.lfs.unemployment_rate.canada
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "statcan-lfs-unemployment-rate-canada-june-2026"
- targetUnit: "percent"
- dataPointId: "statcan.lfs.unemployment_rate.canada.june_2026.first_print"
- resolutionSourceUrl: "https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-07-09", "start": "2026-07-01"}, "field": "official_release:statcan:dq260605a:unemployment_rate", "releasePolicy": "first_print", "sourceSeriesId": "statcan.lfs.unemployment_rate", "sourceUrl": "https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm", "table": "Labour Force Survey, May 2026", "transform": {"factor": 1, "operation": "identity"}}
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
85b14a084401ef868269ce7ceae1541e5760f80d8efdbafdf49db559317560ab

# Draft forecast response
{"slug":"statcan-lfs-unemployment-rate-canada-june-2026","country":"CA","type":"data","title":"Canada unemployment rate, June 2026","question":"Statistics Canada Labour Force Survey unemployment rate for Canada, June 2026 reference month, seasonally adjusted, first print","unit":"percent","pointEstimate":6.7,"ciLow":6.4,"ciHigh":7,"confidence":0.8,"resolutionDate":"2026-07-10","resolutionSource":"Statistics Canada The Daily, Labour Force Survey","resolutionSourceUrl":"https://www150.statcan.gc.ca/n1/daily-quotidien/260710/dq260710a-eng.htm","resolutionRule":"Resolve to the first-print seasonally adjusted unemployment rate for Canada in Statistics Canada's Labour Force Survey for the June 2026 reference month, as published in The Daily and sourced to Table 14-10-0287-01. Use the one-decimal percent value as first published; do not substitute later revisions or corrected historical table vintages unless the first-print release itself is replaced before publication.","dataPointId":"statcan.lfs.unemployment_rate.canada.june_2026.first_print","historicalContext":[{"label":"May 2026 unemployment rate","value":6.6},{"label":"April 2026 unemployment rate","value":6.9},{"label":"March 2026 unemployment rate","value":6.7},{"label":"February 2026 unemployment rate","value":6.7},{"label":"January 2026 unemployment rate","value":6.5}],"drivers":["May unemployment rate fell to 6.6 after April's 6.9","May employment gain of 88,000 suggests some reversal after early-2026 weakness","Recent monthly unemployment-rate changes had about 0.24 percentage-point dispersion","LFS remains above the 2017-2019 pre-pandemic average of 6.0"],"sourceContext":["https://www150.statcan.gc.ca/release-diffusion/2026-eng.pdf","https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260508/dq260508a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260410/dq260410a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260313/dq260313a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260206/dq260206a-eng.htm","https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028701"],"runAt":"2026-07-10T04:06:08Z","reasoning":[{"kind":"heading","text":"Canada LFS Unemployment Rate, June 2026"},{"kind":"text","text":"Framing and exact resolver: target is the Statistics Canada Labour Force Survey unemployment rate for Canada, seasonally adjusted, June 2026 reference month, first print. I keep the catalog slug and dataPointId, but the supplied ledger URL points to the June 5, 2026 Daily page for Labour Force Survey, May 2026; the official release schedule says the June 2026 LFS reference period is released on July 10, 2026, so the specific resolver page should be the July 10, 2026 Daily LFS page when available."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada 2026-2027 major economic releases PDF and read Labour Force Survey rows.","result":"Fetched schedule numbers: Labour Force Survey release date for June 2026 reference period is July 10, 2026; May 2026 reference period is June 5, 2026; July 2026 reference period is August 7, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily, Labour Force Survey, May 2026.","result":"Fetched latest official LFS numbers: Canada unemployment rate was 6.6% in May 2026, down 0.3 pts; employment increased by 88,000 or 0.4%; employment rate was 60.7%; job-finding rate was 26.3%."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily releases for January through April 2026 and Table 14-10-0287-01 metadata.","result":"Fetched reference class history from the same seasonally adjusted LFS variant: January 2026 unemployment rate 6.5%, February 2026 6.7%, March 2026 6.7%, April 2026 6.9%, May 2026 6.6%; Table 14-10-0287-01 release date shown as 2026-06-05 for the then-current table view."},{"kind":"text","text":"Base rate/reference class: for a one-month-ahead LFS unemployment-rate forecast, persistence from the latest same-variant official print is the base rate. The last five first-print-like Daily values were 6.5, 6.7, 6.7, 6.9, and 6.6, putting the local level around 6.7 with recent prints ranging 6.5 to 6.9."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2026 LFS unemployment rate 6.6. Historical sample = Jan-May 2026 same-variant seasonally adjusted Canada unemployment-rate prints. Adjustment components: level +0.05 because the Jan-May average is 6.68 and the labour market remains above the pre-pandemic 6.0 reference; momentum -0.05 because May employment rose 88,000 and unemployment fell 0.3 pts; one-off/policy mechanism 0.00 because no official release evidence points to a discrete June break. Point = 6.6 + 0.05 - 0.05 + 0.05 rounding judgment = 6.7. Successive changes = +0.2, 0.0, +0.2, -0.3; sigma = 0.236 percentage points using sample standard deviation; 1.28*sigma = 0.302, so 80% half-width is about 0.3 and the one-decimal interval is 6.4 to 7.0."},{"kind":"text","text":"Variant control: all anchors are Statistics Canada LFS, Canada, seasonally adjusted unemployment rate, using The Daily releases sourced to Table 14-10-0287-01. I did not mix unadjusted, provincial, trend-cycle, payroll, or U.S.-concept unemployment series."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed labour-force participation rebound or job losses after May that pushes unemployment to 7.1 or higher, which would land above the interval. Downside risk is a second strong employment month or a participation drop like January that pushes unemployment to 6.3 or lower, outside the interval on the low side."},{"kind":"forecast","point":6.7,"ciLow":6.4,"ciHigh":7}]}
