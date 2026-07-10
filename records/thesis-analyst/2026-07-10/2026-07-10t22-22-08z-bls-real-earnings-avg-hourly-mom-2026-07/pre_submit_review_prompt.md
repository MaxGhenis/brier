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
a1a8ebf69a502af791531d4acf3951d2590434e388824b33ad85e75800da812b

# Draft forecast response
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US Real Average Hourly Earnings MoM — July 2026","question":"What will the first-print July 2026 seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls be in BLS Real Earnings Table A-1?","unit":"percent","pointEstimate":-0.1,"ciLow":-0.7,"ciHigh":0.5,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"2026-01","value":0.3},{"label":"2026-02","value":0.1},{"label":"2026-03","value":-0.6},{"label":"2026-04","value":-0.5},{"label":"2026-05","value":-0.1}],"drivers":["moderating nominal wage growth","CPI-U deflator volatility","recent negative real-earnings momentum","seasonal-adjustment noise"],"sourceContext":["https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/news.release/archives/realer_04102026.htm","https://www.bls.gov/schedule/2026/08_sched_list.htm","https://www.bls.gov/schedule/2026/07_sched_list.htm"],"runAt":"2026-07-10T22:22:19Z","thresholdLadder":{"thresholds":[-1,-0.7,-0.5,-0.3,-0.1,0,0.1,0.3,0.5,0.7,1],"cumulativeProbabilities":[0.05,0.1,0.2,0.32,0.46,0.56,0.68,0.8,0.89,0.95,0.98]},"reasoning":[{"kind":"heading","text":"US real average hourly earnings, July 2026 first print"},{"kind":"text","text":"The target is the BLS CES series bls.real_earnings.avg_hourly_mom, specifically Table A-1 for all employees on private nonfarm payrolls, seasonally adjusted, and resolved at the first official July 2026 print without later revisions."},{"kind":"tool","tool":"official.lookup","call":"BLS official release calendar lookup for the target release date","result":"The BLS August 2026 release schedule lists Real Earnings for July 2026 at 08:30 a.m. ET on August 12, 2026, verifying the resolution date rather than inferring it from cadence."},{"kind":"tool","tool":"official.lookup","call":"BLS Real Earnings Table A-1 recent-series lookup","result":"The official Table A-1 page reports the recent seasonally adjusted over-the-month real average hourly earnings changes as March 2026 -0.6 percent, April 2026 -0.5 percent, and May 2026 -0.1 percent."},{"kind":"tool","tool":"official.lookup","call":"BLS archived Real Earnings history lookup","result":"The official March 2026 archive reports January 2026 at 0.3 percent and February 2026 at 0.1 percent for the same Table A-1 seasonally adjusted series."},{"kind":"text","text":"The base rate/reference class is the five fetched 2026 observations: 0.3, 0.1, -0.6, -0.5, and -0.1 percent. Their median is -0.1 percent, with four of five values between -0.6 and 0.3."},{"kind":"text","text":"The exact variant is the gross all-employee, private nonfarm payrolls, seasonally adjusted real average hourly earnings series in BLS Table A-1, deflated with CPI-U; no production-and-nonsupervisory, NSA, weekly-earnings, or revised-vintage values are mixed in."},{"kind":"text","text":"Prior/update/interval: A persistence prior centered near the five-observation median of -0.1 percent is adjusted modestly for recent negative momentum, while CPI-U and nominal hourly-pay surprises create two-sided monthly noise; the fetched reference class anchors the rung span from -0.6 to 0.3 percent, producing an elicited 80% interval from -0.7 to 0.5 percent."},{"kind":"math","text":"Ladder: P(X <= -1) = 0.05; P(X <= -0.7) = 0.1; P(X <= -0.5) = 0.2; P(X <= -0.3) = 0.32; P(X <= -0.1) = 0.46; P(X <= 0) = 0.56; P(X <= 0.1) = 0.68; P(X <= 0.3) = 0.8; P(X <= 0.5) = 0.89; P(X <= 0.7) = 0.95; P(X <= 1) = 0.98. Linear interpolation gives 10th percentile at -0.7, median at -0.06, and 90th percentile at 0.53; rounding to BLS one-decimal print precision gives 10th percentile at -0.7, median at -0.1, and 90th percentile at 0.5."},{"kind":"text","text":"Downside risk is a renewed CPI acceleration with nominal pay below trend, which would land below the interval; upside risk is softer CPI alongside firm nominal wage growth, which would land above the interval. An unusually large seasonal-adjustment change or release-month data shock would be outside the interval."},{"kind":"forecast","point":-0.1,"ciLow":-0.7,"ciHigh":0.5}]}
