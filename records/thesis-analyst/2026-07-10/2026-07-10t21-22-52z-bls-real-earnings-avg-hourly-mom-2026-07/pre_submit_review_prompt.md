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
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US real hourly earnings MoM, July 2026","question":"What will the first-print BLS Real Earnings Table A-1 seasonally adjusted over-the-month percent change be for real average hourly earnings of all employees on private nonfarm payrolls in July 2026?","unit":"percent","pointEstimate":-0.1,"ciLow":-0.5,"ciHigh":0.3,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"2026-05 real average hourly earnings MoM SA first available table value","value":-0.1},{"label":"2026-04 real average hourly earnings MoM SA table value","value":-0.5},{"label":"2026-03 real average hourly earnings MoM SA table value","value":-0.6},{"label":"2025-05 real average hourly earnings MoM SA table value","value":0.4}],"drivers":["Real hourly earnings mechanically combine nominal private average hourly earnings and CPI-U inflation","Recent BLS real hourly prints were negative as CPI-U rose faster than nominal wages","June nominal average hourly earnings growth was steady near 0.3 percent","May CPI-U inflation was elevated by energy but core inflation was lower","July energy prices remain the main upside inflation risk to the deflator"],"sourceContext":["https://www.bls.gov/schedule/news_release/realer.htm","https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/news.release/empsit.t19.htm","https://www.bls.gov/news.release/cpi.nr0.htm"],"runAt":"2026-07-10T21:23:27Z","thresholdLadder":{"thresholds":[-0.9,-0.7,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.5,0.7],"cumulativeProbabilities":[0.02,0.06,0.1,0.17,0.26,0.38,0.52,0.65,0.76,0.84,0.9,0.97,0.99]},"reasoning":[{"kind":"heading","text":"Forecast for July 2026 BLS real average hourly earnings MoM"},{"kind":"text","text":"Framing and exact resolver: this forecast is for BLS Real Earnings Table A-1, all employees on private nonfarm payrolls, seasonally adjusted, real average hourly earnings over-the-month percent change for July 2026. The target resolves to the one-decimal first print on the BLS official release page, with no later revision used."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Real Earnings release schedule for the reference month and release date.","result":"BLS schedule lists June 2026 Real Earnings for Jul. 14, 2026 at 08:30 AM and July 2026 Real Earnings for Aug. 12, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Read BLS Real Earnings Table A-1 current release for same-variant real average hourly earnings and component values.","result":"Table A-1 shows real average hourly earnings over-the-month percent changes of 0.4 for May 2025, -0.6 for Mar. 2026, -0.5 for Apr. 2026, and -0.1 for May 2026; the same row levels are $11.32, $11.31, $11.25, and $11.24."},{"kind":"tool","tool":"official.lookup","call":"Read BLS Employment Situation Table B-3 for the latest nominal average hourly earnings anchor.","result":"BLS Table B-3 shows total private average hourly earnings of $37.41 in Apr. 2026, $37.51 in May 2026, and $37.64 in June 2026, with average weekly earnings of $1283.16, $1286.59, and $1291.05."},{"kind":"tool","tool":"official.lookup","call":"Read BLS CPI summary for the latest CPI-U inflation reference class and deflator pressure.","result":"BLS CPI summary shows CPI-U seasonally adjusted all-items changes of 0.9 in Mar. 2026, 0.6 in Apr. 2026, and 0.5 in May 2026; energy rose 10.9 in Mar., 3.8 in Apr., and 3.9 in May, while core CPI rose 0.2 in May."},{"kind":"text","text":"The same-variant rule matters: all anchors above refer either directly to BLS Table A-1 real average hourly earnings for all employees on private nonfarm payrolls, seasonally adjusted, or to its BLS-published nominal AHE and CPI-U inputs. I am not using FRED or local catalog estimates as evidence."},{"kind":"text","text":"Reference class and base rate: recent Table A-1 real hourly MoM prints centered below zero, with Mar.-May 2026 at -0.6, -0.5, and -0.1 after CPI-U rose 0.9, 0.6, and 0.5. A persistence prior from this reference class points negative, but the latest nominal wage input, June AHE at $37.64 after $37.51 in May, argues against another extreme negative unless July CPI-U reaccelerates."},{"kind":"text","text":"Prior/update/interval: starting from a persistence prior near the recent Table A-1 average of about -0.4 for Mar.-May 2026, I add +0.2 because June nominal AHE momentum was still about 0.3 percent, add +0.1 because May core CPI was only 0.2 despite headline energy pressure, and subtract -0.1 for July energy/geopolitical inflation risk. The threshold span is anchored by fetched real AHE rungs of -0.6, -0.5, -0.1, and +0.4, so the elicited 80 percent interval spans a negative repeat through a modest positive rebound."},{"kind":"math","text":"Ladder: P(X <= -0.9) = 0.02; P(X <= -0.7) = 0.06; P(X <= -0.5) = 0.10; P(X <= -0.4) = 0.17; P(X <= -0.3) = 0.26; P(X <= -0.2) = 0.38; P(X <= -0.1) = 0.52; P(X <= 0.0) = 0.65; P(X <= 0.1) = 0.76; P(X <= 0.2) = 0.84; P(X <= 0.3) = 0.90; P(X <= 0.5) = 0.97; P(X <= 0.7) = 0.99. Linear interpolation gives 10th percentile at -0.5, median at -0.1142857142857143, and 90th percentile at 0.3; rounded to BLS one-decimal print precision, the forecast is point -0.1 with 80 percent interval [-0.5, 0.3]."},{"kind":"text","text":"Upside risk: if July CPI-U cools sharply while nominal AHE keeps a 0.3 percent or better monthly pace, the real hourly print would land above the interval. Downside risk: renewed energy-price pressure or weak July AHE could put the deflator well above nominal wage growth and would land below the interval. An outside the interval outcome is most likely from an energy shock, a gasoline reversal, or an unusually large July payroll wage surprise."},{"kind":"forecast","point":-0.1,"ciLow":-0.5,"ciHigh":0.3}]}
