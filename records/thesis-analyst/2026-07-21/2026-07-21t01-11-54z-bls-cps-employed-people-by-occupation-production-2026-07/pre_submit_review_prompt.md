# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.employed_people_by_occupation.production
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-production-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.production.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Production occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.production", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-e6122e1a77edbc28a7204a5b63f7b17fc1f4147009df5e69f180e83c7894b601.json"
- targetContentHash: "e6122e1a77edbc28a7204a5b63f7b17fc1f4147009df5e69f180e83c7894b601"
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
3fc3c2231bbe8a531505b4ffc42430e4426f1773512f5238df0a15a33d578f4b

# Draft forecast response
{"slug":"cps-production-employment-july-2026","country":"US","type":"data","title":"US production employment, July 2026","question":"What will BLS first report for people employed in production occupations in July 2026, not seasonally adjusted, in millions?","unit":"millions","pointEstimate":7.559,"ciLow":7.368,"ciHigh":7.75,"confidence":0.8,"resolutionDate":"2026-08-06","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-13/A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the first BLS-published July 2026 total employed value for Production occupations in CPS Employment Situation Table A-13/A-19, not seasonally adjusted, reported in thousands and multiplied by 0.001 to millions. Preserve the first print despite later revisions; round to three decimal places. The registered 2026-08-06 resolutionDate conflicts with the official BLS calendar and June release, which schedule publication for 2026-08-07; the forecast remains tied to the registered target date.","dataPointId":"bls.cps.employed_people_by_occupation.production.july_2026.first_print","historicalContext":[{"label":"January 2026 first print","value":7.905},{"label":"February 2026 first print","value":7.742},{"label":"March 2026 first print","value":7.685},{"label":"April 2026 first print","value":7.883},{"label":"May 2026 first print","value":7.912},{"label":"June 2026 first print","value":7.759},{"label":"July 2025 first print","value":7.662}],"drivers":["Recent CPS production-employment level","Typical July seasonal decline in NSA data","Household-survey sampling volatility","Soft year-over-year production employment"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/news.release/archives/empsit_07022026.pdf","https://www.bls.gov/news.release/archives/empsit_06052026.htm","https://www.bls.gov/news.release/archives/empsit_05082026.htm","https://www.bls.gov/news.release/archives/empsit_08012025.pdf","https://www.bls.gov/schedule/2026/home.htm"],"runAt":"2026-07-21T01:12:14Z","reasoning":[{"kind":"heading","text":"July 2026 CPS production-occupation employment forecast"},{"kind":"text","text":"The target is the first BLS print for total people employed in Production occupations, July 2026, not seasonally adjusted, from CPS Employment Situation Table A-13/A-19. BLS reports thousands; the resolver multiplies by 0.001. Later revisions do not replace the first print."},{"kind":"tool","tool":"official.lookup","call":"Read BLS archived Employment Situation releases for January through March 2026, Table A-13.","result":"Fetched first-print production-occupation employment of 7,905 thousand in January 2026, 7,742 thousand in February, and 7,685 thousand in March."},{"kind":"tool","tool":"official.lookup","call":"Read BLS archived Employment Situation releases for April through June 2026, Table A-13.","result":"Fetched first-print production-occupation employment of 7,883 thousand in April 2026, 7,912 thousand in May, and 7,759 thousand in June."},{"kind":"tool","tool":"official.lookup","call":"Read the archived July 2025 Employment Situation, Table A-13, for a same-month seasonal comparison.","result":"Fetched July production-occupation employment of 7,889 thousand in 2024 and 7,662 thousand in 2025; the June 2025 official table value was 7,938 thousand, implying a 276-thousand June-to-July decline in 2025."},{"kind":"tool","tool":"official.lookup","call":"Verify the July 2026 Employment Situation publication date using the official BLS release calendar and June 2026 release.","result":"The official calendar lists Friday, August 7, 2026 at 8:30 AM ET, and the June release repeats August 7, 2026; this is 1 day after the ledger resolutionDate of August 6."},{"kind":"text","text":"The reference class/base rate is persistence around the latest NSA CPS occupation level with a negative July seasonal update. The January-June sequence is choppy but centered near 7.8 million, while July 2025 fell 0.276 million from June and remained 0.227 million below July 2024."},{"kind":"math","text":"Prior/update/interval: persistence prior = June 2026 first print of 7.759 million; historical sample = January-June 2026 first prints [7.905, 7.742, 7.685, 7.883, 7.912, 7.759]. Successive changes are [-0.163, -0.057, +0.198, +0.029, -0.153] million, whose sample standard deviation is sigma = 0.149 million. Apply a -0.200 million update for July seasonality and weak year-over-year level momentum, with no separate policy adjustment: 7.759 - 0.200 = 7.559. The normal 80% half-width is 1.28*sigma = 1.28*0.149 = 0.191 million, implying bounds 7.559 +/- 0.191 = [7.368, 7.750]."},{"kind":"text","text":"Upside risk is an abrupt rebound like April 2026, which could put the print above 7.750 million. Downside risk is a July seasonal drop materially larger than 2025's 0.276 million or renewed manufacturing weakness; a decline exceeding 0.391 million from June would land below the interval. Either outcome would be outside the interval."},{"kind":"forecast","point":7.559,"ciLow":7.368,"ciHigh":7.75}]}
