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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI annual rate, July 2026","question":"What will the first ABS-published All groups CPI, Australia annual movement for July 2026 be, in original terms and rounded to one decimal?","unit":"percent","pointEstimate":4.0,"ciLow":3.2,"ciHigh":4.8,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger sourceBinding URL appears to point to the ABS Consumer Price Index, Australia, June 2026 page rather than the July 2026 Monthly CPI Indicator page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and documents that discrepancy rather than changing the target identity.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"March 2026 annual CPI","value":4.6},{"label":"April 2026 annual CPI","value":4.2},{"label":"May 2026 annual CPI","value":4.0},{"label":"July 2025 annual CPI","value":3.0}],"drivers":["May annual CPI momentum eased to 4.0%","services and non-tradables inflation remained firm","electricity-rebate effects elevated housing inflation","July 2025 electricity and headline CPI base effects roll out","higher fuel prices create near-term upside risk"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/april-2026","https://www.abs.gov.au/release-calendar/future-releases-calendar/202608","https://www.rba.gov.au/publications/smp/2026/may/overview.html"],"runAt":"2026-07-10T21:39:23Z","thresholdLadder":{"thresholds":[2.8,3.0,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.6,4.8,5.0,5.2],"cumulativeProbabilities":[0.04,0.07,0.11,0.18,0.28,0.4,0.52,0.64,0.75,0.84,0.91,0.95,0.97]},"reasoning":[{"kind":"heading","text":"Australia All groups CPI annual movement, July 2026 first print"},{"kind":"text","text":"The target is the original, not seasonally adjusted, All groups CPI annual movement for July 2026, printed to one decimal by ABS. It resolves only to the first print. The ledger calls the release the Monthly CPI Indicator and supplies a sourceBinding for the June CPI page, while the current ABS calendar labels the July publication Consumer Price Index, Australia; I preserve the registered dataPointId and resolver and document this discrepancy rather than changing target identity."},{"kind":"tool","tool":"official.lookup","call":"Fetch the ABS May 2026 Consumer Price Index release and its All groups CPI history.","result":"ABS reported annual All groups CPI of 4.6% in March 2026, 4.2% in April, and 4.0% in May; monthly original CPI was 1.1%, 0.4%, and -0.7%, respectively. July 2025 annual CPI was 3.0% and its monthly movement was 1.3%."},{"kind":"tool","tool":"official.lookup","call":"Fetch ABS May 2026 component and analytical-series movements.","result":"In May 2026, Housing inflation was 6.5%, Transport 3.3%, Food 3.3%, trimmed mean 3.6%, non-tradables 4.7%, and tradables 2.5%. Electricity rose 21.1% annually but only 3.9% excluding government-rebate effects."},{"kind":"tool","tool":"official.lookup","call":"Fetch the RBA May 2026 Statement on Monetary Policy inflation projections.","result":"The RBA projected year-ended CPI inflation of 4.8% for June 2026 and 4.0% for December 2026, with trimmed mean inflation of 3.8% and 3.5%, respectively."},{"kind":"tool","tool":"official.lookup","call":"Verify the July 2026 CPI release date in the ABS August 2026 future-release calendar.","result":"The official ABS calendar places Consumer Price Index, Australia July 2026 on 26 August 2026 at 11:30am, verifying resolutionDate 2026-08-26 rather than inferring it from monthly cadence."},{"kind":"text","text":"Reference class/base rate: the fetched annual sequence from July 2025 through May 2026 was 3.0%, 3.2%, 3.6%, 3.8%, 3.4%, 3.8%, 3.8%, 3.7%, 4.6%, 4.2%, and 4.0%. Persistence near the latest 4.0% is the outside-view anchor, while the observed range of 3.0% to 4.6% anchors the central ladder span."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms point in different directions. The 4.0% May level and 3.6% trimmed mean show persistent underlying pressure; headline momentum eased from March. Expiring electricity rebates raised measured housing inflation, while the unusually large 13.5% July 2025 electricity increase and 1.3% headline monthly increase become adverse base effects when they roll out. Higher fuel costs can offset part of that decline."},{"kind":"math","text":"Ladder: P(X <= 2.8) = 0.04; P(X <= 3.0) = 0.07; P(X <= 3.2) = 0.11; P(X <= 3.4) = 0.18; P(X <= 3.6) = 0.28; P(X <= 3.8) = 0.40; P(X <= 4.0) = 0.52; P(X <= 4.2) = 0.64; P(X <= 4.4) = 0.75; P(X <= 4.6) = 0.84; P(X <= 4.8) = 0.91; P(X <= 5.0) = 0.95; P(X <= 5.2) = 0.97. Linear interpolation gives the 10th percentile at 3.15, median at 3.97, and 90th percentile at 4.77; rounded to the ABS print precision these are 3.2, 4.0, and 4.8."},{"kind":"text","text":"Prior/update/interval: A latest-value persistence model uses the July 2025-May 2026 reference-class sample (3.0%-4.6%) and starts from May's 4.0%. Updates comprise sticky services/non-tradables and fuel pressure upward, offset by recent headline slowing and the July 2025 electricity/headline base effects. The interval method is direct threshold-ladder quantile inversion, yielding final implied 80% bounds of 3.2% to 4.8% and a 4.0% median."},{"kind":"text","text":"Upside risk: a larger fuel shock, renewed electricity-price increases, or broader pass-through into goods and services would land above the interval. Downside risk: a sharp fuel reversal plus a stronger-than-expected electricity base-effect unwind would land below the interval. An outcome outside the interval would therefore require a materially larger one-off price move than embedded in the recent ABS reference class."},{"kind":"forecast","point":4.0,"ciLow":3.2,"ciHigh":4.8}]}
