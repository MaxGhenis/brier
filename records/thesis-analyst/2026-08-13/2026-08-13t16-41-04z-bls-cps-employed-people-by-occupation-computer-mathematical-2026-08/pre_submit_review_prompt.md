# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.employed_people_by_occupation.computer_mathematical
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-computer-math-employment-august-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.computer_mathematical.august_2026.first_print"
- expectedReleaseWindow: {"end": "2026-09-11", "start": "2026-09-03"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-09-11", "start": "2026-09-03"}, "field": "Computer and mathematical occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.computer_mathematical", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-13-83c7957c7a7a20d3b18b8babe138f2a1751bf02acd6f799a9246036fb456f038.json"
- targetContentHash: "83c7957c7a7a20d3b18b8babe138f2a1751bf02acd6f799a9246036fb456f038"
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
149ad43926e5768cf4270e2129b1c2bad68fd5ca8e4583d5b45dcf85a713b8e5

# Draft forecast response
{"slug":"cps-computer-math-employment-august-2026","country":"US","type":"data","title":"US computer and math employment, August 2026","question":"What will BLS first report for total employed people age 16 and over in Computer and mathematical occupations in August 2026 in CPS Employment Situation Table A-19, not seasonally adjusted, converted from thousands to millions?","unit":"millions","pointEstimate":6.97,"ciLow":6.44,"ciHigh":7.50,"confidence":0.8,"resolutionDate":"2026-09-11","resolutionSource":"CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the first BLS-published August 2026 value in CPS Employment Situation Table A-19, row 'Computer and mathematical occupations,' Total age 16 years and over, not seasonally adjusted, reported in thousands and multiplied by 0.001 to millions; retain three decimals and ignore all later revisions. The canonical ledger target fixes resolutionDate as 2026-09-11, although an archived official BLS 2026 schedule fetched this run lists the August 2026 Employment Situation release for Friday, September 4, 2026 at 08:30 ET.","dataPointId":"bls.cps.employed_people_by_occupation.computer_mathematical.august_2026.first_print","historicalContext":[{"label":"2021 annual average, millions","value":5.688},{"label":"2022 annual average, millions","value":6.171},{"label":"2023 annual average, millions","value":6.502},{"label":"2024 annual average, millions","value":6.386},{"label":"2025 annual average, millions","value":6.711},{"label":"June 2025 first-print row, millions","value":6.602},{"label":"June 2026 first-print row, millions","value":6.95}],"drivers":["June 2026 exact-row persistence","2021-2025 annual growth reference class","CPS occupational sampling volatility","no direct August-specific policy signal"],"sourceContext":["https://web.archive.org/web/20260710110509/https://www.bls.gov/web/empsit/cpseea19.htm","https://web.archive.org/web/20260812070739/https://www.bls.gov/schedule/2026/home.htm","https://app.thesisinstitute.org/specs.json"],"runAt":"2026-08-13T16:41:17Z","reasoning":[{"kind":"heading","text":"August 2026 CPS computer and mathematical employment forecast"},{"kind":"text","text":"The registered resolver is BLS CPS Employment Situation Table A-19, row 'Computer and mathematical occupations,' total age 16 years and over, not seasonally adjusted. The table is reported in thousands and the target unit is millions after multiplying by 0.001; the print policy is FIRST PRINT."},{"kind":"tool","tool":"official.lookup","call":"Fetch Wayback snapshot of BLS CPS Table A-19, 2026-07-10 capture of https://www.bls.gov/web/empsit/cpseea19.htm, using the repository A-19 parser.","result":"Fetched 116586 bytes; parser returned computer_mathematical = 6950.0 thousand, business_financial_operations = 9720.0 thousand, healthcare_support = 5691.0 thousand, office_administrative_support = 16184.0 thousand, production = 7759.0 thousand, transportation_material_moving = 12010.0 thousand. For the target row this is 6.950 million for June 2026."},{"kind":"tool","tool":"official.lookup","call":"Inspect public Thesis record records/thesis-analyst/2026-07-21/2026-07-21t01-06-13z-bls-cps-employed-people-by-occupation-computer-mathematical-2026-07/cells.with_activity.json for earlier official-source history fetched in that run.","result":"The public record's fetched history for this exact series lists 2021 annual average 5.688 million, 2022 6.171, 2023 6.502, 2024 6.386, 2025 6.711, June 2025 6.602, and June 2026 6.950."},{"kind":"tool","tool":"official.lookup","call":"Fetch archived BLS 2026 release schedule page for the August 2026 Employment Situation release date.","result":"The archived BLS schedule section for September 2026 lists Friday, September 4, 2026 at 08:30 AM for Employment Situation for August 2026; the same schedule lists Friday, September 11, 2026 at 08:30 AM for Consumer Price Index and Real Earnings for August 2026."},{"kind":"tool","tool":"catalog.lookup","call":"Fetch https://app.thesisinstitute.org/specs.json and inspect local generated ledger target for slug identity.","result":"The specs.json request returned HTTP 404 with content-length 11289, so no competing specs entry was fetched. Local ledger-targets.generated.ts contains the registered slug cps-computer-math-employment-august-2026 with dataPointId bls.cps.employed_people_by_occupation.computer_mathematical.august_2026.first_print and unit millions."},{"kind":"tool","tool":"model.candidates","call":"Compute thesis_model_candidate_v1 candidates from the inspected exact-series history.","result":"thesis_model_candidate_v1 persistence: point 6.950, p10 6.419, p50 6.950, p90 7.481, 80% interval 6.419-7.481, 90% interval 6.267-7.633, interval_method annual_change_plus_latest_gap_sigma, calibration_n 5, train_cutoff 2026-06, walk_forward_score unavailable. Drift candidate: point 6.971, p10 6.440, p50 6.971, p90 7.502, 80% interval 6.440-7.502, 90% interval 6.288-7.654, interval_method annual_change_plus_latest_gap_sigma, calibration_n 5, train_cutoff 2026-06, walk_forward_score unavailable."},{"kind":"text","text":"Base rate/reference class: the exact-row outside view is persistence near the latest fetched first-print level, 6.950 million in June 2026, with the public annual reference class rising from 5.688 million in 2021 to 6.711 million in 2025 and the June 2026 first print 0.348 million above June 2025. I did not find a witnessed July 2026 first-print observation in the local ledger, so I do not use July as evidence."},{"kind":"text","text":"Level, momentum, one-off, and policy effects: level anchor is 6.950 million. The longer annual trend implies about +0.021 million per month, but the available exact-row monthly evidence is thin and CPS occupational allocation is noisy. I found no direct August-specific policy, classification, or hiring signal strong enough to move materially away from the persistence/drift benchmark."},{"kind":"math","text":"Prior/update/interval: prior model = persistence at 6.950 million, with drift candidate point 6.971 million from mean 2021-2025 annual change of (6.711 - 5.688)/4 = 0.256 million per year, or +0.021 million per month. Historical sample = annual averages 5.688, 6.171, 6.502, 6.386, 6.711 plus June 2026 exact row 6.950. Annual changes are +0.483, +0.331, -0.116, and +0.325, giving trend RMS 0.340 million; add monthly sampling proxy abs(6.950 - 6.711) = 0.239 million, so sigma = sqrt(0.340^2 + 0.239^2) = 0.415 million. Update components: +0.021 drift, no one-off, no policy adjustment, so point = 6.950 + 0.021 = 6.971, rounded to 6.97. The 80% half-width is 1.28*sigma = 1.28*0.415 = 0.531 million, giving 6.44 to 7.50 after rounding."},{"kind":"text","text":"Upside risk: a strong August sample for professional services or a CPS occupation-allocation rebound would land above the interval. Downside risk: weaker technology hiring plus adverse CPS sampling or a reversal of the June year-over-year gain would land below the interval and outside the interval."},{"kind":"forecast","point":6.97,"ciLow":6.44,"ciHigh":7.50}]}
