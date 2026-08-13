# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.employed_people_by_occupation.business_financial_operations
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-business-financial-employment-august-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.business_financial_operations.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-09-11", "start": "2026-09-03"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-11", "start": "2026-09-03"}, "field": "Business and financial operations occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.business_financial_operations", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-13-7f9e2805bbd169b63cf804785f639e8a770a559cb5b29578b6467da0e454c6cd.json"
- targetContentHash: "7f9e2805bbd169b63cf804785f639e8a770a559cb5b29578b6467da0e454c6cd"
- registrationCommit: "448b17e91d8ee0fa53f512a75460719c172b1358"
- registeredAtUtc: "2026-08-13T06:52:40Z"
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
722f3056520fc3138e2fa34e4a1a4a14d038cab2e3f040c318376cbc402e1af1

# Draft forecast response
{"slug":"cps-business-financial-employment-august-2026","country":"US","type":"data","title":"US business and financial operations employment, August 2026","question":"What will the U.S. Bureau of Labor Statistics first report in CPS Employment Situation Table A-19 for employed people in Business and financial operations occupations, total age 16 years and over, not seasonally adjusted, for August 2026, in millions?","unit":"millions","pointEstimate":9.835,"ciLow":9.608,"ciHigh":10.062,"confidence":0.8,"resolutionDate":"2026-09-11","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the first value published by BLS for August 2026 in CPS Employment Situation Table A-19, row 'Business and financial operations occupations,' Total age 16 years and over, not seasonally adjusted, reported in thousands and multiplied by 0.001 to millions. Use the first official print without later revisions. The official BLS Employment Situation schedule fetched this run lists August 2026 for Sep. 04, 2026, while the registered Thesis target contract sets resolutionDate to 2026-09-11; this cell preserves the registered target date and records the discrepancy.","dataPointId":"bls.cps.employed_people_by_occupation.business_financial_operations.august_2026.first_print","historicalContext":[{"label":"January 2026 first-print Table A-19 NSA","value":10.291},{"label":"March 2026 first-print Table A-19 NSA","value":10.195},{"label":"May 2026 first-print Table A-19 NSA","value":10.033},{"label":"June 2026 first-print Table A-19 NSA","value":9.72},{"label":"July 2026 current BLS Table A-19 NSA","value":9.835}],"drivers":["last-print persistence from July 2026","same-row A-19 history drifted lower through June","July rebound argues against extending the June drop mechanically","CPS occupation-cell sampling volatility dominates short-horizon signal"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/schedule/news_release/empsit.htm","https://web.archive.org/web/20260218113618/https://www.bls.gov/web/empsit/cpseea19.htm","https://web.archive.org/web/20260502095151/https://www.bls.gov/web/empsit/cpseea19.htm","https://web.archive.org/web/20260613101041/https://www.bls.gov/web/empsit/cpseea19.htm","https://web.archive.org/web/20260710110509/https://www.bls.gov/web/empsit/cpseea19.htm","https://app.thesisinstitute.org/specs.json"],"runAt":"2026-08-13T16:40:10Z","reasoning":[{"kind":"heading","text":"BLS CPS A-19 occupation employment forecast"},{"kind":"text","text":"The target is the BLS CPS Employment Situation Table A-19 row 'Business and financial operations occupations,' total age 16 years and over, not seasonally adjusted, for August 2026, first print, transformed from thousands to millions. The canonical Thesis target fixes slug, unit, dataPointId, source URL, and resolutionDate."},{"kind":"tool","tool":"web.open","call":"Open https://www.bls.gov/schedule/news_release/empsit.htm / BLS schedule result for Employment Situation","result":"BLS Employment Situation schedule result: July 2026 release Aug. 07, 2026 at 08:30 AM; August 2026 release Sep. 04, 2026 at 08:30 AM; September 2026 release Oct. 02, 2026 at 08:30 AM. This conflicts with the registered target resolutionDate 2026-09-11, so I keep 2026-09-11 as the target contract and state the discrepancy."},{"kind":"tool","tool":"web.open","call":"Open https://www.bls.gov/web/empsit/cpseea19.htm","result":"Current BLS Table A-19, Last Modified Date August 07, 2026: Business and financial operations occupations row has July 2025 total 10,298 thousand and July 2026 total 9,835 thousand; men 4,618 thousand and women 5,217 thousand for July 2026."},{"kind":"tool","tool":"curl+parser","call":"Fetch Wayback snapshots of the BLS Table A-19 page for same-row history","result":"Parsed same-row BLS Table A-19 snapshots: Feb. 11, 2026 page current value 10,291 thousand; Apr. 03, 2026 page current value 10,195 thousand; Jun. 05, 2026 page current value 10,033 thousand; Jul. 02, 2026 page current value 9,720 thousand. Values are transformed by 0.001 to 10.291, 10.195, 10.033, and 9.720 million."},{"kind":"tool","tool":"python","call":"PYTHONPATH=. python3 scripts/run_time_series_models.py --target-id bls.cps.employed_people_by_occupation.business_financial_operations.august_2026.first_print --target-period 2026-08 --history-json ... --models persistence --round-increment 0.001","result":"thesis_model_candidate_v1 persistence.last_print: trainCutoff 2026-07, pointEstimate 9.835, p10 9.567, p50 9.835, p90 9.887, interval80 lower 9.567 upper 9.887, calibrationN 4, walk_forward_1_step rows 4, meanAbsoluteError 0.1715."},{"kind":"tool","tool":"curl","call":"curl -L -sS https://app.thesisinstitute.org/specs.json | rg -n cps-business-financial-employment-august-2026 -C 1","result":"Slug check against fetched specs.json returned no match for cps-business-financial-employment-august-2026 (rg exit 1). Local registered target remains records/targets/2026-08-13-7f9e2805bbd169b63cf804785f639e8a770a559cb5b29578b6467da0e454c6cd.json."},{"kind":"text","text":"Base rate / reference class: the same-row recent level history available this run is 10.291, 10.195, 10.033, 9.720, and 9.835 million. The trailing observed range is 9.720-10.291 million, and last-print persistence from July 2026 is 9.835 million. No direct August-specific official signal was fetched that clears the update test, so persistence is the prior and the forecast point."},{"kind":"math","text":"Prior/update/interval: prior = persistence.last_print from July 2026 = 9.835 million; historical sample = same-row A-19 levels 2026-01, 2026-03, 2026-05, 2026-06, 2026-07; successive changes = -0.096, -0.162, -0.313, +0.115 million, so sigma = 0.178 million using sample standard deviation. Update components = 0.000 million because no release-specific current signal justifies moving more than one rounding unit from persistence. Interval method = realized successive-change sigma; 80% half-width = 1.28*sigma = 1.28*0.178 = 0.227 million, giving 9.835 - 0.227 = 9.608 and 9.835 + 0.227 = 10.062."},{"kind":"text","text":"Counter-consideration: downside risk outside the interval would come from another occupation-cell drop like the May-to-June move plus broader household employment weakness, which would land below 9.608 million. Upside risk outside the interval would come from a reversal of the June drop plus stronger white-collar hiring or classification mix, which would land above 10.062 million."},{"kind":"forecast","point":9.835,"ciLow":9.608,"ciHigh":10.062}]}
