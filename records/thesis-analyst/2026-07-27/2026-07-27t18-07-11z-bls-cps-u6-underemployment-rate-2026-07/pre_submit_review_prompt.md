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
- targetRegistrationPath: "records/targets/2026-07-27-20ec6a3c168e40892ebc5fe44743cf49c5940add207def0313de53d7f7cb8ed7.json"
- targetContentHash: "20ec6a3c168e40892ebc5fe44743cf49c5940add207def0313de53d7f7cb8ed7"
- registrationCommit: "e494ebc7a9b410a6fcffab9e5439408ff3d09413"
- registeredAtUtc: "2026-07-27T18:01:44Z"
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
efea07351f76995f159890f1288b1eb230ba9b4876c2b08bacc8ac39a1eff203

# Draft forecast response
{"slug":"u6-underemployment-rate-july-2026","country":"US","type":"data","title":"U-6 Underemployment Rate, July 2026","question":"What will the BLS first-print seasonally adjusted U-6 alternative labor underutilization rate be for July 2026 in Employment Situation Table A-15?","unit":"percent","pointEstimate":7.9,"ciLow":7.7,"ciHigh":8.1,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-15","resolutionSourceUrl":"https://www.bls.gov/news.release/empsit.t15.htm","resolutionRule":"Resolve to the first BLS-published July 2026 seasonally adjusted U-6 value in Employment Situation Table A-15, in percent, as released on August 7, 2026. Use the first print rounded to one decimal place; do not apply later revisions or same-day correction exceptions unless BLS explicitly republishes the first release before normal public access.","dataPointId":"bls.cps.u6_underemployment_rate.2026_07.first_print","historicalContext":[{"label":"2026-06 U-6 SA","value":7.9},{"label":"2026-05 U-6 SA","value":8.1},{"label":"2026-04 U-6 SA","value":8.2},{"label":"2026-03 U-6 SA","value":8.0},{"label":"2026-02 U-6 SA","value":7.9},{"label":"2026-01 U-6 SA","value":8.1}],"drivers":["June 2026 U-6 first print was 7.9 percent after May 8.1 and April 8.2","recent seasonally adjusted U-6 moves are small, with five 2026 monthly changes of -0.2, +0.1, +0.2, -0.1, and -0.2 percentage points","June official U-3 unemployment was 4.2 percent, down from 4.3 percent in May, limiting near-term U-6 upside","July first print resolves on the August 7, 2026 Employment Situation release"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm","https://www.bls.gov/cps/publications/release-calendar.htm","https://www.bls.gov/news.release/empsit.t15.htm?source=news_body_link","https://fred.stlouisfed.org/series/U6RATE","https://alfred.stlouisfed.org/series?seid=U6RATE"],"runAt":"2026-07-27T18:07:25Z","reasoning":[{"kind":"heading","text":"Forecast for BLS July 2026 U-6 first print"},{"kind":"text","text":"Framing and exact resolver: this targets the BLS CPS household-survey U-6 alternative labor underutilization rate, seasonally adjusted, Table A-15, source code LNS13327709 mirrored by FRED/ALFRED as U6RATE. The ledger uses ALFRED for first-print capture, but the substantive resolver is the BLS Employment Situation Table A-15 first print."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Schedule of Releases for the Employment Situation for the July 2026 reference month.","result":"BLS lists July 2026 Employment Situation release date as Aug. 07, 2026 at 08:30 AM; the same schedule lists June 2026 on Jul. 02, 2026 and August 2026 on Sep. 04, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS CPS release calendar for the July 2026 reference period.","result":"BLS CPS calendar lists Aug. 07, 2026 for July 2026 Employment Situation, with nearby entries Jul. 02, 2026 for June 2026 and Sep. 04, 2026 for August 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched the current official BLS Employment Situation Table A-15 for recent seasonally adjusted U-6 values.","result":"BLS Table A-15 reports U-6 seasonally adjusted values of Feb. 2026 7.9, Mar. 2026 8.0, Apr. 2026 8.2, May 2026 8.1, and June 2026 7.9; the same table reports June 2025 seasonally adjusted U-6 at 7.7."},{"kind":"tool","tool":"fred.lookup","call":"Checked FRED/ALFRED U6RATE as a public history mirror for the same BLS series LNS13327709.","result":"FRED/ALFRED U6RATE shows Jun 2026 7.9, May 2026 8.1, Apr 2026 8.2, Mar 2026 8.0, and Feb 2026 7.9, updated Jul 2, 2026 at 8:31 AM CDT, with next release date Aug 7, 2026."},{"kind":"text","text":"Base rate/reference class: for a monthly labor-underutilization rate already near 8 percent, the strongest reference class is persistence plus small one-month CPS sampling and composition movement. The 2026 official/mirror history gives recent one-month moves of -0.2, +0.1, +0.2, -0.1, and -0.2 percentage points from Jan through Jun, so unchanged or a one-tenth move is the modal case."},{"kind":"text","text":"Level, momentum, and mechanism: the latest level is 7.9 percent, down from 8.2 in April and 8.1 in May, while June U-3 in the same Table A-15 was 4.2 after 4.3 in May. That argues against a sharp U-6 rise, but U-6 is broader than U-3 and can move with marginal attachment and part-time-for-economic-reasons even when unemployment is steady."},{"kind":"math","text":"Prior/update/interval: persistence prior = June 2026 U-6 at 7.9 percent; historical sample = Jan-Jun 2026 seasonally adjusted U-6 values 8.1, 7.9, 8.0, 8.2, 8.1, 7.9, with successive changes -0.2, +0.1, +0.2, -0.1, -0.2. Sample sigma = 0.18 percentage point. 80% normal half-width is about 1.28*sigma = 1.28*0.18 = 0.23 percentage point. Adjustment components: level 0.00, recent downward momentum -0.05, mean-reversion from June drop +0.05, policy/mechanism one-off 0.00, leaving point 7.9. Implied continuous 80% bounds are 7.9 +/- 0.23 = 7.67 to 8.13, rounded to 7.7 to 8.1 for the printed one-decimal series."},{"kind":"text","text":"Counter-considerations: upside risk is a July jump in part-time-for-economic-reasons or marginal attachment that lifts U-6 to 8.2 or higher, which would land above the 80% interval. Downside risk is a broad household-survey improvement that pushes U-6 to 7.6 or lower, which would land below the interval. Outside the interval would most likely require a larger-than-recent move in the broader underemployment components rather than just a small U-3 change."},{"kind":"forecast","point":7.9,"ciLow":7.7,"ciHigh":8.1}]}
