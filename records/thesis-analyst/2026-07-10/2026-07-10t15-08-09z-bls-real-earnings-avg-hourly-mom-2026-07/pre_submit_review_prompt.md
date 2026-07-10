# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.real_earnings.avg_hourly_mom
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-real-avg-hourly-earnings-mom-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.real_earnings.avg_hourly_mom.2026-07.first_print"
- resolutionDate: "2026-08-12"
- resolutionSource: "U.S. Bureau of Labor Statistics Real Earnings Table A-1"
- resolutionSourceUrl: "https://www.bls.gov/news.release/realer.t01.htm"
- resolutionRule: "Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-18", "start": "2026-08-10"}, "field": "bls.real_earnings.avg_hourly_mom", "releasePolicy": "first_print", "sourceSeriesId": "bls.real_earnings.avg_hourly_mom", "sourceUrl": "https://www.bls.gov/news.release/realer.t01.htm", "table": "U.S. Bureau of Labor Statistics Real Earnings Table A-1", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-8662209989befa5925d38419a847521e7a1076b91048aef177ca79c7544f4334.json"
- targetContentHash: "8662209989befa5925d38419a847521e7a1076b91048aef177ca79c7544f4334"
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
178d9f1ab50e659ec88db59c912ea8098ebd0f20cf29bd59c7761acedc749d7a

# Draft forecast response
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"U.S. Real Average Hourly Earnings, July 2026","question":"U.S. Bureau of Labor Statistics Real Earnings Table A-1, seasonally adjusted real average hourly earnings for all private nonfarm employees, July 2026 first-print over-the-month percent change","unit":"percent","pointEstimate":-0.1,"ciLow":-0.7,"ciHigh":0.8,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"2026-01","value":0.3},{"label":"2026-02","value":0.1},{"label":"2026-03","value":-0.6},{"label":"2026-04","value":-0.5},{"label":"2026-05","value":-0.1}],"drivers":["nominal hourly earnings growth","CPI-U inflation","recent negative real-earnings momentum","seasonally adjusted first-print volatility"],"sourceContext":["https://www.bls.gov/schedule/2026/08_sched.htm","https://www.bls.gov/ces/publications/news-release-schedule.htm","https://www.bls.gov/news.release/realer.htm","https://www.bls.gov/news.release/archives/realer_04102026.htm","https://www.bls.gov/news.release/archives/realer_03112026.htm"],"runAt":"2026-07-10T15:08:23Z","thresholdLadder":{"thresholds":[-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1,1.2],"cumulativeProbabilities":[0.08,0.15,0.28,0.42,0.58,0.68,0.77,0.85,0.9,0.95,0.97]},"reasoning":[{"kind":"heading","text":"Forecast of July 2026 first-print real average hourly earnings growth"},{"kind":"text","text":"The target is BLS CES series bls.real_earnings.avg_hourly_mom: Table A-1, all private nonfarm employees, seasonally adjusted, real average hourly earnings, over-the-month percent change, first printed for July 2026. The official calendar schedules the Real Earnings release for August 12, 2026."},{"kind":"tool","tool":"official.lookup","call":"BLS August 2026 release-calendar lookup","result":"Fetched official calendar values: July 2026 Real Earnings is scheduled for August 12, 2026 at 08:30 AM; the July Employment Situation is scheduled for August 7, 2026."},{"kind":"tool","tool":"official.lookup","call":"BLS May 2026 Real Earnings Table A-1 lookup","result":"Fetched same-variant seasonally adjusted Table A-1 values: real average hourly earnings over-the-month change was -0.6 percent in March 2026, -0.5 percent in April 2026, and -0.1 percent in May 2026; nominal average hourly earnings changes were 0.2, 0.2, and 0.3 percent, while CPI-U changes were 0.9, 0.6, and 0.5 percent."},{"kind":"tool","tool":"official.lookup","call":"BLS January-February 2026 archived Real Earnings lookup","result":"Fetched same-variant Table A-1 values: real average hourly earnings over-the-month change was 0.3 percent in January 2026 and 0.1 percent in February 2026; February nominal hourly earnings growth was 0.4 percent and CPI-U inflation was 0.3 percent."},{"kind":"text","text":"The recent official reference class is mixed but tilted negative: the five fetched monthly observations from January through May 2026 are 0.3, 0.1, -0.6, -0.5, and -0.1 percent. The mechanical relationship is nominal wage growth minus CPI-U inflation, with rounding and seasonal-adjustment noise affecting the printed one-decimal result."},{"kind":"text","text":"Base rate: use the five-observation recent reference class as the persistence prior, centered near -0.16 percent, then modestly pull toward zero because nominal wage growth has remained positive and the latest real change improved from -0.5 to -0.1 percent."},{"kind":"text","text":"Prior/update/interval: persistence prior is the January-May 2026 Table A-1 reference class; momentum adjustment is toward zero after -0.6, -0.5, -0.1; the nominal-wage-minus-CPI mechanism supplies the level adjustment; the interval uses the values themselves because this is a change series. With sample sigma = 0.385 percentage points, the standard 80% half-width is roughly 1.28*sigma = 0.49 points. The ladder-implied interval is -0.7 to 0.8, a 0.75-to-1.75-compatible rounded width around that benchmark, reflecting one-decimal first-print and inflation-volatility uncertainty."},{"kind":"math","text":"Ladder: P(X <= -0.8) = 0.08; P(X <= -0.6) = 0.15; P(X <= -0.4) = 0.28; P(X <= -0.2) = 0.42; P(X <= 0) = 0.58; P(X <= 0.2) = 0.68; P(X <= 0.4) = 0.77; P(X <= 0.6) = 0.85; P(X <= 0.8) = 0.90; P(X <= 1) = 0.95; P(X <= 1.2) = 0.97. Linear interpolation gives the 10th percentile -0.74, median -0.10, and 90th percentile 0.80, rounded to the one-decimal print precision as -0.7, -0.1, and 0.8."},{"kind":"text","text":"Downside risk is a renewed CPI spike with nominal wage growth near 0.2 percent, which would land below the interval if real earnings print at -0.8 percent or lower. Upside risk is CPI cooling to roughly 0.1 percent while wages hold near 0.3 percent, which would land above the interval at 0.9 percent or higher. A large seasonal-adjustment residual or benchmark revision would be outside the interval, but later revisions do not affect this first-print target."},{"kind":"forecast","point":-0.1,"ciLow":-0.7,"ciHigh":0.8}]}
