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
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US real average hourly earnings, July 2026","question":"U.S. BLS Table A-1 seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, July 2026 first print","unit":"percent","pointEstimate":-0.1,"ciLow":-0.5,"ciHigh":0.3,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"2025-12 first print","value":-0.3},{"label":"2026-01 first print","value":0.3},{"label":"2026-02 first print","value":0.2},{"label":"2026-03 first print","value":-0.6},{"label":"2026-04 first print","value":-0.5},{"label":"2026-05 first print","value":-0.1}],"drivers":["Recent real-hourly-earnings prints have been mostly negative after inflation deflation","June nominal private average hourly earnings rose 0.3 percent","July CPI inflation relative to nominal earnings is the dominant unresolved offset"],"sourceContext":["https://www.bls.gov/schedule/2026/08_sched.htm","https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/news.release/archives/realer_02132026.htm","https://www.bls.gov/news.release/archives/realer_03112026.htm","https://www.bls.gov/news.release/archives/realer_04102026.htm","https://www.bls.gov/news.release/archives/empsit_07022026.htm"],"runAt":"2026-07-10T15:35:05Z","reasoning":[{"kind":"heading","text":"July 2026 real average hourly earnings first-print forecast"},{"kind":"text","text":"The resolver is BLS Real Earnings Table A-1: the seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls. Table A-1 uses CPI-U to deflate this all-employees series; all anchors below use that same SA Table A-1 variant. The official BLS August 2026 calendar schedules Real Earnings for July 2026 on August 12 at 08:30 Eastern, verifying the 2026-08-12 resolution date."},{"kind":"tool","tool":"official.lookup","call":"Fetch BLS Real Earnings Table A-1 for the latest available official release.","result":"BLS Table A-1 fetched real average hourly earnings over-the-month changes of 0.4 percent in May 2025, -0.6 percent in March 2026, -0.5 percent in April 2026, and -0.1 percent in May 2026; the associated May 2026 CPI-U change was 0.5 percent and nominal average-hourly-earnings change was 0.3 percent."},{"kind":"tool","tool":"official.lookup","call":"Fetch the BLS archived January 2026 Real Earnings release, Table A-1.","result":"The BLS January 2026 Table A-1 release fetched a -0.3 percent December 2025 real average hourly earnings change and a 0.3 percent January 2026 change; January real average hourly earnings were $11.38."},{"kind":"tool","tool":"official.lookup","call":"Fetch the BLS archived February and March 2026 Real Earnings releases, Table A-1.","result":"The BLS February release fetched a 0.2 percent February 2026 real average hourly earnings change and $11.40 level; the March release fetched a -0.6 percent March 2026 change and $11.32 level."},{"kind":"tool","tool":"official.lookup","call":"Fetch the BLS June 2026 Employment Situation release for the latest nominal earnings signal.","result":"The BLS June Employment Situation fetched total-private average hourly earnings of $37.51 in May and $37.64 in June, a $0.13 or 0.3 percent increase; total-private average weekly hours were 34.3 in both months."},{"kind":"text","text":"Reference class/base rate: the six December-to-May first-print Table A-1 changes (-0.3, 0.3, 0.2, -0.6, -0.5, -0.1 percent) average -0.17 percent. The latest -0.1 percent is less negative than March and April but does not establish a sustained positive-real-pay regime."},{"kind":"text","text":"The June nominal 0.3 percent hourly-earnings increase is a modest positive adjustment versus the negative recent real-pay base rate. It is not enough to project a positive July real print without knowing July CPI-U, so the combined point remains -0.1 percent."},{"kind":"math","text":"Prior/update/interval: persistence/mean-reversion prior is the six first-print SA Table A-1 values from December-May, with mean -0.17 percent; adjustments are +0.1 percentage point for June's 0.3 percent nominal wage momentum, offset by unresolved July CPI-U deflation risk. For this change series, using the values themselves gives sample sigma = 0.37 percentage point; 1.28*sigma = 0.47 percentage point. A one-decimal 80% interval centered near the adjusted -0.1 point is -0.5 to 0.3 percent, half-width 0.40 percentage point, or 0.86 times the dispersion-based width."},{"kind":"text","text":"upside risk: a soft July CPI-U print combined with another roughly 0.3 percent nominal wage gain would land above the interval. downside risk: CPI-U acceleration with flat nominal hourly earnings would land below the interval; a large energy or goods-price move is the principal outside the interval scenario."},{"kind":"forecast","point":-0.1,"ciLow":-0.5,"ciHigh":0.3}]}
