# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.employed_people_by_occupation.business_financial_operations
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-business-financial-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.business_financial_operations.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Business and financial operations occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.business_financial_operations", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-1eb4254c92a69ec666207bbfc46826262f2310402f51a2e107c50cca573945da.json"
- targetContentHash: "1eb4254c92a69ec666207bbfc46826262f2310402f51a2e107c50cca573945da"
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
0c5c882a800ba3a0db6a90bf901794faba1cd40bfbaa2c8c37ca00b5118bdb8e

# Draft forecast response
{"slug":"cps-business-financial-employment-july-2026","country":"US","type":"data","title":"US business and financial operations employment, July 2026","question":"What will BLS first report for employed people in business and financial operations occupations in July 2026, not seasonally adjusted, in millions?","unit":"millions","pointEstimate":9.69,"ciLow":9.35,"ciHigh":10.03,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the first value published by BLS for July 2026 in CPS Employment Situation Table A-19, row 'Business and financial operations occupations,' Total age 16 years and over, not seasonally adjusted, reported in thousands and multiplied by 0.001 to millions. Use the first official print without later revisions. The official BLS calendar schedules the July release for August 7, 2026; this conflicts with the registered sourceBinding window ending August 6 but does not change the target.","dataPointId":"bls.cps.employed_people_by_occupation.business_financial_operations.july_2026.first_print","historicalContext":[{"label":"June 2025 NSA","value":10.205},{"label":"April 2026 NSA","value":9.857},{"label":"June 2026 NSA","value":9.72},{"label":"2024 annual average","value":9.945}],"drivers":["June 2026 level persistence","recent weakness in financial activities employment","CPS occupational sampling volatility","July seasonal composition"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/schedule/2026/home.htm","https://www.bls.gov/cps/publications/release-calendar.htm","https://www.bls.gov/web/empsit/cpseea44.pdf","https://www.bls.gov/opub/reports/womens-databook/"],"runAt":"2026-07-21T01:05:05Z","reasoning":[{"kind":"heading","text":"July 2026 business and financial operations employment forecast"},{"kind":"text","text":"The resolver is the first July 2026 print in BLS CPS Table A-19 for Business and financial operations occupations, total age 16 years and over, not seasonally adjusted. Table values are thousands and are converted to millions by multiplying by 0.001."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest BLS CPS Employment Situation Table A-19 values for the exact NSA occupational row.","result":"BLS Table A-19 reports 9,720 thousand in June 2026 and 10,205 thousand in June 2025, equal to 9.720 million and 10.205 million."},{"kind":"tool","tool":"official.lookup","call":"Fetch an earlier exact-row observation from BLS CPS occupational tables.","result":"BLS Table A-44 reports 9,857 thousand people in Business and financial operations occupations in April 2026, equal to 9.857 million."},{"kind":"tool","tool":"official.lookup","call":"Fetch the BLS annual occupation reference value.","result":"The BLS Women in the Labor Force occupation table reports 9,945 thousand employed in Business and financial operations occupations for the 2024 annual average, equal to 9.945 million."},{"kind":"tool","tool":"official.lookup","call":"Verify the July 2026 Employment Situation publication date on official BLS calendars.","result":"The BLS 2026 release schedule and CPS calendar both list the July 2026 Employment Situation for August 7, 2026 at 8:30 a.m. ET; the registered expected window ends August 6, one day too early."},{"kind":"text","text":"The reference class and base rate are persistence around the latest exact-series level, with substantial CPS sampling noise. The official observations show a lower June 2026 level than June 2025, while the 2024 annual average was 9.945 million."},{"kind":"text","text":"Level effect: anchor at June's 9.720 million. Momentum effect: the observed sequence from 10.205 to 9.857 to 9.720 is negative. One-off effect: noisy CPS occupational allocation argues against extrapolating the full decline. Policy mechanism: no discrete policy change identified, while weak financial-activities payroll evidence supports only a small negative adjustment."},{"kind":"math","text":"Prior/update/interval: persistence model prior = 9.720 million; historical sample = 10.205, 9.857, and 9.720 million. Successive observed changes are -0.348 and -0.137 million, giving RMS sigma = sqrt((0.348^2 + 0.137^2)/2) = 0.264 million. Apply a -0.030 million momentum/financial-activities adjustment and no separate one-off or policy adjustment, yielding 9.690 million. The 80% half-width is approximately 1.28*sigma = 1.28*0.264 = 0.338 million, rounded to 0.34, implying 9.35 to 10.03 million."},{"kind":"text","text":"Upside risk is a rebound in sampled professional hiring or July occupational reclassification, which would land above 10.03 million. Downside risk is continued finance-sector weakness combined with adverse CPS sampling, which would land below 9.35 million and outside the interval."},{"kind":"forecast","point":9.69,"ciLow":9.35,"ciHigh":10.03}]}
