# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.employed_people_by_occupation.office_administrative_support
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-office-admin-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.office_administrative_support.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Office and administrative support occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.office_administrative_support", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-148ed0329886292f905056a164baddd005c4f488016df31b37fd3083d7030d8e.json"
- targetContentHash: "148ed0329886292f905056a164baddd005c4f488016df31b37fd3083d7030d8e"
- registrationCommit: "36b3b6b19986083e354c0bd56b0090751cfaeba7"
- registeredAtUtc: "2026-07-21T01:00:49Z"
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
2300c245584077b6fa7e19d5745b7bc5cd48cb7a3f6843460af0c2b063cb2843

# Draft forecast response
{"slug":"cps-office-admin-employment-july-2026","country":"US","type":"data","title":"US office and administrative support employment, July 2026","question":"What will BLS first report for employed people in office and administrative support occupations in July 2026, not seasonally adjusted, in millions?","unit":"millions","pointEstimate":16.34,"ciLow":16.16,"ciHigh":16.52,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the July 2026 total employed value for “Office and administrative support occupations” in CPS Employment Situation Table A-19, not seasonally adjusted, as first published by BLS on August 7, 2026. Convert the reported thousands to millions by multiplying by 0.001 and retain three decimal places. Ignore subsequent revisions.","dataPointId":"bls.cps.employed_people_by_occupation.office_administrative_support.july_2026.first_print","historicalContext":[{"label":"January 2026 first print, NSA millions","value":16.355},{"label":"February 2026 first print, NSA millions","value":16.38},{"label":"March 2026 first print, NSA millions","value":16.563},{"label":"April 2026 first print, NSA millions","value":16.471},{"label":"May 2026 first print, NSA millions","value":16.335},{"label":"June 2026 first print, NSA millions","value":16.184},{"label":"July 2025 first print, NSA millions","value":16.565}],"drivers":["usual June-to-July seasonal increase in the unadjusted series","recent three-month decline in office-support employment","CPS sampling volatility","weak aggregate household employment momentum"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/schedule/news_release/empsit.htm","https://www.bls.gov/news.release/archives/empsit_07022026.pdf","https://www.bls.gov/news.release/archives/empsit_06052026.pdf","https://www.bls.gov/news.release/archives/empsit_05082026.pdf","https://www.bls.gov/news.release/archives/empsit_04032026.pdf","https://www.bls.gov/news.release/archives/empsit_03062026.pdf","https://www.bls.gov/news.release/archives/empsit_02112026.pdf","https://www.bls.gov/news.release/archives/empsit_08012025.pdf","https://www.bls.gov/news.release/archives/empsit_08022024.pdf","https://www.bls.gov/news.release/archives/empsit_07052024.pdf"],"runAt":"2026-07-21T01:10:37Z","reasoning":[{"kind":"heading","text":"July 2026 office and administrative support employment forecast"},{"kind":"text","text":"The target is the total employed count for Office and administrative support occupations in CPS Table A-19, not seasonally adjusted and reported in thousands, converted to millions. Resolution uses the first July 2026 print only. The official BLS calendar schedules it for August 7, 2026; this conflicts with the ledger sourceBinding window ending August 6, so the verified official date is used without changing the target."},{"kind":"tool","tool":"official.lookup","call":"Fetch the BLS Employment Situation release schedule for the July 2026 reference month.","result":"The official schedule lists July 2026 for release on 2026-08-07 at 8:30 AM ET."},{"kind":"tool","tool":"official.lookup","call":"Fetch first-published 2026 Table A-13/A-19 office and administrative support employment totals from BLS Employment Situation releases.","result":"Not-seasonally-adjusted employment was 16,355 thousand in January, 16,380 thousand in February, 16,563 thousand in March, 16,471 thousand in April, 16,335 thousand in May, and 16,184 thousand in June 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetch recent June and July reference-class values from archived BLS occupational employment tables.","result":"July employment was 15,814 thousand in 2024 and 16,565 thousand in 2025; June was 15,568 thousand in 2024 and 16,469 thousand in 2025, giving June-to-July changes of +246 thousand and +96 thousand."},{"kind":"text","text":"The outside-view base rate is the recent June-to-July reference class: the two observed increases average (+0.246 + 0.096)/2 = +0.171 million. Applied mechanically to June 2026's 16.184 million, that gives 16.355 million."},{"kind":"text","text":"Level is 16.184 million in June. Momentum is negative: the March-to-June path fell 0.379 million. The one-off seasonal mechanism points upward in July, while policy and aggregate labor-market effects are modestly negative because June household employment weakened. I therefore trim the seasonal prior by 0.015 million to 16.340 million."},{"kind":"math","text":"Prior/update/interval: persistence-plus-July-seasonality prior, using January-June 2026 first-print NSA levels and the 2024-2025 June-to-July reference class; adjustments are +0.171 million seasonal, -0.015 million for recent negative momentum, and 0.000 million for other mechanisms, yielding 16.184 + 0.171 - 0.015 = 16.340 million. Successive 2026 changes are +0.025, +0.183, -0.092, -0.136, and -0.151 million; their sample standard deviation is sigma = 0.140 million. The normal 80% half-width is 1.28*sigma = 1.28*0.140 = 0.179 million, implying 16.161 to 16.519 million, rounded outward to final bounds of 16.16 to 16.52 million."},{"kind":"text","text":"Upside risk comes from a July seasonal increase nearer 2024's +0.246 million, which could push the print toward the upper bound. Downside risk comes from continuation of the March-June contraction. An unusually large CPS sampling move or a decline exceeding about 0.024 million from June would land outside the interval below 16.16; a gain above about 0.336 million would land outside the interval above 16.52."},{"kind":"forecast","point":16.34,"ciLow":16.16,"ciHigh":16.52}]}
