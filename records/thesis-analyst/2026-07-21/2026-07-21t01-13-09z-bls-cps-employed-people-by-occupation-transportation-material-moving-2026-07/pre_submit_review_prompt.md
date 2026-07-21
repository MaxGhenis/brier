# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.employed_people_by_occupation.transportation_material_moving
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-transport-material-moving-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.transportation_material_moving.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Transportation and material moving occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.transportation_material_moving", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-c022dea86383a42504a748b91016eb3303bf77dbb7184ffbce6566046bcacbbe.json"
- targetContentHash: "c022dea86383a42504a748b91016eb3303bf77dbb7184ffbce6566046bcacbbe"
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
4cf47410a482e372f47b04842deb9d8803cf725f9dfd782d7aeb32db4fac56d7

# Draft forecast response
{"slug":"cps-transport-material-moving-employment-july-2026","country":"US","type":"data","title":"US transportation and material-moving employment, July 2026","question":"What will BLS first report for July 2026 employment in transportation and material moving occupations, total age 16+, not seasonally adjusted, in CPS Table A-19?","unit":"millions","pointEstimate":12.01,"ciLow":11.83,"ciHigh":12.19,"confidence":0.8,"resolutionDate":"2026-08-06","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, CPS Table A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the first value published for July 2026 in BLS CPS Employment Situation Table A-19, row 'Transportation and material moving occupations,' Total, 16 years and over, not seasonally adjusted, reported in thousands and multiplied by 0.001 to millions. Retain that first print despite later revisions. The registered resolutionDate is 2026-08-06, but the official BLS calendar now schedules the July release for 2026-08-07; this ledger discrepancy should be corrected without changing the target identity.","dataPointId":"bls.cps.employed_people_by_occupation.transportation_material_moving.july_2026.first_print","historicalContext":[{"label":"March 2026 first print","value":12.214},{"label":"April 2026 first print","value":12.127},{"label":"May 2026 first print","value":12.12},{"label":"June 2026 first print","value":12.01},{"label":"June 2025","value":11.619}],"drivers":["June-level persistence","recent NSA monthly declines","positive year-over-year level","CPS sampling volatility","weak transportation payroll momentum"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/news.release/archives/empsit_04032026.pdf","https://www.bls.gov/news.release/archives/empsit_05082026.pdf","https://www.bls.gov/news.release/archives/empsit_06052026.pdf","https://www.bls.gov/news.release/archives/empsit_07022026.pdf","https://www.bls.gov/schedule/news_release/empsit.htm?categoryId=1&orient=1"],"runAt":"2026-07-21T01:13:26Z","reasoning":[{"kind":"heading","text":"July 2026 CPS transportation and material-moving employment forecast"},{"kind":"text","text":"The resolver is BLS CPS Table A-19, Transportation and material moving occupations, Total age 16+, not seasonally adjusted, first July 2026 print in thousands converted to millions. This is distinct from seasonally adjusted establishment-survey transportation and warehousing payrolls."},{"kind":"tool","tool":"official.lookup","call":"Read the current BLS CPS Table A-19 and June 2026 Employment Situation archive.","result":"BLS reports 12,010 thousand transportation and material-moving workers in June 2026 versus 11,619 thousand in June 2025; total CPS employment was 162,722 thousand in June 2026."},{"kind":"tool","tool":"official.lookup","call":"Read archived March and April 2026 Employment Situation occupation tables.","result":"The first-print transportation and material-moving employment values were 12,214 thousand in March 2026 and 12,127 thousand in April 2026; the corresponding prior-year values were 11,958 thousand and 12,059 thousand."},{"kind":"tool","tool":"official.lookup","call":"Read the archived May 2026 Employment Situation occupation table.","result":"The May 2026 first print was 12,120 thousand, compared with 11,742 thousand in May 2025; BLS also reported May transportation-and-warehousing payroll employment changed by +1,000."},{"kind":"tool","tool":"official.lookup","call":"Verify the July 2026 Employment Situation date on the official BLS release calendar and June release notice.","result":"Both official BLS sources schedule the July 2026 Employment Situation for August 7, 2026 at 8:30 a.m. ET; this is 1 day later than the registered 2026-08-06 resolutionDate."},{"kind":"text","text":"The reference class and base rate are short-horizon forecasts of this noisy NSA CPS occupation level. March-June 2026 declined 12.214 to 12.127 to 12.120 to 12.010 million, while June remained 0.391 million above June 2025. Persistence therefore deserves more weight than extrapolating the latest decline."},{"kind":"math","text":"Prior/update/interval: The model is level persistence at June's 12.010 million. Historical sample uses six successive March-to-June changes from the fetched 2025 and 2026 sequences: +0.101, -0.317, -0.123, -0.087, -0.007, and -0.110 million. Their sample dispersion is sigma = 0.139 million. The recent downward momentum adjustment (-0.04) is offset by positive year-over-year level and mean reversion (+0.04), leaving 12.010 million. The normal 80% half-width is 1.28*sigma = 1.28*0.139 = 0.178 million, rounded to 0.18, implying 11.83 to 12.19 million."},{"kind":"text","text":"A stronger-than-normal summer expansion in delivery, warehousing, or passenger transport is the upside risk and would land above the interval. Broad household-employment weakness, accelerated logistics layoffs, or an adverse CPS sampling swing is the downside risk and could land below the interval; either outcome would be outside the interval."},{"kind":"forecast","point":12.01,"ciLow":11.83,"ciHigh":12.19}]}
