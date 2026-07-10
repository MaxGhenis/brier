# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: abs.cpi.all_groups.yoy
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "australia-cpi-annual-rate-july-2026"
- country: "AU"
- targetUnit: "percent"
- dataPointId: "abs.cpi.all_groups.yoy.2026-07.first_print"
- resolutionDate: "2026-08-26"
- resolutionSource: "Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release"
- resolutionSourceUrl: "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026"
- resolutionRule: "Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger sourceBinding URL appears to point to the ABS Consumer Price Index, Australia, June 2026 page rather than the July 2026 Monthly CPI Indicator page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and documents that discrepancy rather than changing the target identity."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-09-02", "start": "2026-08-25"}, "field": "abs.cpi.all_groups.yoy", "releasePolicy": "first_print", "sourceSeriesId": "abs.cpi.all_groups.yoy", "sourceUrl": "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/june-2026", "table": "Australian Bureau of Statistics Consumer Price Index, Australia, June 2026 release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-fc08c8b584fa0779c2421f4944d8c026e568b8990f2942968fad89cfb39c5530.json"
- targetContentHash: "fc08c8b584fa0779c2421f4944d8c026e568b8990f2942968fad89cfb39c5530"
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
7defca226e328eefaadbafcff27940e0b5a83f4fe682b90228a233dd179d1ea7

# Draft forecast response
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI annual rate, July 2026","question":"What will the Australian Bureau of Statistics first print for the July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, not seasonally adjusted, in percent rounded to one decimal?","unit":"percent","pointEstimate":4.3,"ciLow":3.5,"ciHigh":5.2,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger sourceBinding URL appears to point to the ABS Consumer Price Index, Australia, June 2026 page rather than the July 2026 Monthly CPI Indicator page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and documents that discrepancy rather than changing the target identity.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"2026-05 All groups CPI annual movement","value":4.0},{"label":"2026-04 All groups CPI annual movement","value":4.2},{"label":"2026-03 All groups CPI annual movement","value":4.6},{"label":"2026-02 All groups CPI annual movement","value":3.7}],"drivers":["Recent all-groups annual CPI is near 4 percent after a March fuel shock","July fuel-excise and oil-price pass-through can lift the annual rate again","Housing and rents remain sticky upside contributors","Monthly CPI indicator is partial-sample and prints to one decimal","First-print target ignores later corrections or quarterly-CPI replacement values"],"sourceContext":["https://www.abs.gov.au/release-calendar","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/april-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/march-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026"],"runAt":"2026-07-10T21:14:13Z","thresholdLadder":{"thresholds":[3.0,3.3,3.6,3.8,4.0,4.2,4.4,4.6,4.8,5.0,5.2,5.5,5.8],"cumulativeProbabilities":[0.03,0.07,0.12,0.20,0.31,0.43,0.54,0.65,0.75,0.83,0.90,0.96,0.98]},"reasoning":[{"kind":"heading","text":"Australia July 2026 monthly CPI indicator forecast"},{"kind":"text","text":"Framing: the resolver is the ABS Monthly Consumer Price Index Indicator, Australia, July 2026 release, All groups CPI annual movement, first print, in percent rounded to one decimal. I use the same monthly-indicator all-groups annual variant for anchors; I do not mix in quarterly CPI, seasonally adjusted variants, trimmed mean, or later revisions."},{"kind":"tool","tool":"official.lookup","call":"Check ABS release calendar and target page contract for the July 2026 Monthly Consumer Price Index Indicator release.","result":"ABS release calendar target is 26 August 2026 for the July 2026 Monthly CPI Indicator; the registered target window is 2026-08-25 to 2026-09-02 and the first-print value will be one decimal percent."},{"kind":"tool","tool":"official.lookup","call":"Read ABS Monthly Consumer Price Index Indicator, Australia, May 2026 release for the same All groups CPI annual movement variant and component context.","result":"Fetched May 2026 All groups CPI annual movement 4.0%; housing annual movement 5.2%; rents annual movement 7.4%; automotive fuel annual movement -5.1%."},{"kind":"tool","tool":"official.lookup","call":"Read ABS Monthly Consumer Price Index Indicator, Australia, April 2026 release for the same All groups CPI annual movement variant.","result":"Fetched April 2026 All groups CPI annual movement 4.2%; March 2026 comparison 4.6%; trimmed mean inflation 3.4%."},{"kind":"tool","tool":"official.lookup","call":"Read ABS Monthly Consumer Price Index Indicator, Australia, March 2026 release for the same All groups CPI annual movement variant and shock context.","result":"Fetched March 2026 All groups CPI annual movement 4.6%; February 2026 comparison 3.7%; automotive fuel annual movement 32.8%."},{"kind":"text","text":"Reference class and base rate: for near-term Australian monthly CPI indicator all-groups annual forecasts, the strongest public reference class is recent same-series persistence plus one- to three-month shock reversal. The fetched same-variant sequence 3.7%, 4.6%, 4.2%, 4.0% anchors the ladder span: most mass stays in the high-3s to high-4s, with a meaningful right tail if fuel or housing re-accelerates."},{"kind":"text","text":"Prior/update/interval: persistence prior is the recent same-series All groups CPI annual movement centered around the May 2026 4.0% print, using the February-May 2026 sample of 3.7%, 4.6%, 4.2%, and 4.0%; I update upward for the July fuel-excise/oil pass-through risk and sticky housing/rent pressure, partly offset by likely normalization from the March fuel spike and monthly-indicator sampling noise. The interval method is a threshold ladder grounded on the fetched 3.7%-4.6% recent range, widened for two unknown monthly prints before July and one-off fuel-policy effects; final implied bounds are 10th percentile 3.5, median 4.3, and 90th percentile 5.2."},{"kind":"math","text":"Ladder: P(X <= 3.0) = 0.03; P(X <= 3.3) = 0.07; P(X <= 3.6) = 0.12; P(X <= 3.8) = 0.20; P(X <= 4.0) = 0.31; P(X <= 4.2) = 0.43; P(X <= 4.4) = 0.54; P(X <= 4.6) = 0.65; P(X <= 4.8) = 0.75; P(X <= 5.0) = 0.83; P(X <= 5.2) = 0.90; P(X <= 5.5) = 0.96; P(X <= 5.8) = 0.98. Linear interpolation gives 10th percentile at 3.48, median at 4.33, and 90th percentile at 5.20; rounded to the ABS print precision this is 10th percentile at 3.5, median at 4.3, and 90th percentile at 5.2."},{"kind":"text","text":"Counter-considerations: upside risk is a larger July fuel rebound, rent acceleration, or supply shock that would land above the interval near 5.3% or higher. Downside risk is a sharper fuel reversal, energy subsidy effect, or broad goods disinflation that would land outside the interval below 3.5%. The central case keeps annual inflation above target but below the March shock peak."},{"kind":"forecast","point":4.3,"ciLow":3.5,"ciHigh":5.2}]}
