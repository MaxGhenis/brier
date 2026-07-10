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
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US real hourly earnings, July 2026","question":"What will the first BLS print show for the July 2026 seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls?","unit":"percent","pointEstimate":0.1,"ciLow":-0.4,"ciHigh":0.6,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"January 2026 first print","value":0.3},{"label":"February 2026 first print","value":0.2},{"label":"March 2026 first print","value":-0.6},{"label":"April 2026 first print","value":-0.5},{"label":"May 2026 first print","value":-0.1}],"drivers":["Nominal hourly-pay growth near 0.3 percent","Monthly CPI-U inflation determines the real-wage subtraction","Recent first prints have unusually wide dispersion","One-decimal BLS publication rounding"],"sourceContext":["https://www.bls.gov/schedule/2026/08_sched.htm","https://www.bls.gov/news.release/archives/realer_02132026.htm","https://www.bls.gov/news.release/archives/realer_03112026.htm","https://www.bls.gov/news.release/archives/realer_04102026.htm","https://www.bls.gov/news.release/archives/realer_05122026.htm","https://www.bls.gov/news.release/archives/realer_06102026.htm","https://www.bls.gov/news.release/archives/empsit_07022026.htm"],"runAt":"2026-07-10T17:13:17Z","reasoning":[{"kind":"heading","text":"July 2026 real average hourly earnings forecast"},{"kind":"text","text":"The target is the first-print, one-decimal value in BLS Real Earnings Table A-1 for all employees on private nonfarm payrolls: seasonally adjusted real average hourly earnings over the month. Table A-1 uses CPI-U to deflate nominal earnings; no later revision replaces the first print."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS August 2026 release calendar.","result":"The official calendar schedules July 2026 Real Earnings for August 12, 2026 at 8:30 a.m. ET, alongside July CPI."},{"kind":"tool","tool":"official.lookup","call":"Read archived BLS Real Earnings Table A-1 releases for January through March 2026.","result":"First-printed monthly real average hourly earnings changes were January 0.3%, February 0.2%, and March -0.6%; the corresponding first-print CPI-U changes were 0.2%, 0.3%, and 0.9%."},{"kind":"tool","tool":"official.lookup","call":"Read archived BLS Real Earnings Table A-1 releases for April and May 2026.","result":"First-printed real hourly earnings changes were April -0.5% and May -0.1%; nominal hourly earnings changed 0.2% and 0.3%, while CPI-U changed 0.6% and 0.5%."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS June 2026 Employment Situation earnings data.","result":"June average hourly earnings for all private employees rose 0.3% to $37.64, following a May level of $37.51; the 12-month increase was 3.5%."},{"kind":"text","text":"The outside-view base rate/reference class is the six available first-print monthly observations from December 2025 through May 2026: 0.0%, 0.3%, 0.2%, -0.6%, -0.5%, and -0.1%. Their mean is -0.12% and median is -0.05%. Recent negative prints largely reflect temporarily elevated CPI-U rather than collapsing nominal wages."},{"kind":"text","text":"Mechanisms: the level of nominal hourly earnings remains high and its momentum is about 0.3% monthly; CPI-U is the principal subtraction and recent 0.5%-0.9% readings created the negative one-offs. A normalization of monthly inflation toward roughly 0.2%-0.3%, combined with wage growth around 0.3%, shifts the July real change toward zero or slightly positive."},{"kind":"math","text":"Prior/update/interval: Start from a persistence/reference-class prior near the six-print median of -0.05%. Using the change-series values themselves [0.0, 0.3, 0.2, -0.6, -0.5, -0.1], the sample standard deviation is sigma = 0.37 percentage point, so 1.28*sigma = 0.47 point. Update by about +0.15 point for persistent 0.3% nominal wage growth and anticipated CPI normalization, yielding a 0.1% center. The ladder implies an 80% interval of -0.4% to 0.6%, a 0.50-point half-width, close to the 0.47-point empirical width."},{"kind":"math","text":"Ladder: P(X <= -0.5) = 0.06; P(X <= -0.4) = 0.10; P(X <= -0.3) = 0.18; P(X <= -0.2) = 0.27; P(X <= -0.1) = 0.38; P(X <= 0.0) = 0.46; P(X <= 0.1) = 0.50; P(X <= 0.2) = 0.61; P(X <= 0.3) = 0.71; P(X <= 0.4) = 0.79; P(X <= 0.5) = 0.85; P(X <= 0.6) = 0.90; P(X <= 0.7) = 0.95. Linear interpolation places the 10th, 50th, and 90th percentiles exactly at -0.4%, 0.1%, and 0.6%, respectively."},{"kind":"text","text":"Upside risk comes from July CPI-U near zero while nominal hourly pay rises at least 0.4%; that could land above the interval. Downside risk comes from another energy- or tariff-related CPI jump near 0.8% with weak wage growth; that would land below the interval. Composition-driven hourly-pay volatility is an additional outside-the-interval mechanism."},{"kind":"forecast","point":0.1,"ciLow":-0.4,"ciHigh":0.6}],"thresholdLadder":{"thresholds":[-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7],"cumulativeProbabilities":[0.06,0.1,0.18,0.27,0.38,0.46,0.5,0.61,0.71,0.79,0.85,0.9,0.95]}}
