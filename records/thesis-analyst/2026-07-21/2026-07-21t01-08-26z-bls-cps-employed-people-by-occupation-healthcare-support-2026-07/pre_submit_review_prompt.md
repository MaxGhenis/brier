# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.employed_people_by_occupation.healthcare_support
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-healthcare-support-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.healthcare_support.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Healthcare support occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.healthcare_support", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-e2043717570a339e4f9e280e31486229af547196d9c88d0ccdbf8936af8bb3f1.json"
- targetContentHash: "e2043717570a339e4f9e280e31486229af547196d9c88d0ccdbf8936af8bb3f1"
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
6566b221fe22c259b29d0559b3d0bbeda1e9634900343b34aaa8cc83d5b1413c

# Draft forecast response
{"slug":"cps-healthcare-support-employment-july-2026","country":"US","type":"data","title":"US healthcare support employment, July 2026","question":"What will BLS first report for July 2026 employed people age 16 and over in healthcare support occupations, not seasonally adjusted, in millions?","unit":"millions","pointEstimate":5.801,"ciLow":4.626,"ciHigh":6.976,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, CPS Table A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the first value published for July 2026 in BLS CPS Employment Situation Table A-19, row 'Healthcare support occupations,' Total, 16 years and over, not seasonally adjusted. Multiply the published thousands value by 0.001 and retain three decimal places in millions. Ignore all later revisions; no correction or release-day grace exception applies.","dataPointId":"bls.cps.employed_people_by_occupation.healthcare_support.july_2026.first_print","historicalContext":[{"label":"July 2023 NSA CPS healthcare support employment","value":4.911},{"label":"June 2025 NSA CPS healthcare support employment","value":5.95},{"label":"June 2026 NSA CPS healthcare support employment","value":5.691}],"drivers":["June 2026 level persistence","modest July seasonal uplift","long-run healthcare labor demand","high CPS subgroup sampling volatility"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/schedule/2026/home.htm","https://www.bls.gov/news.release/archives/empsit_07022026.pdf","https://www.bls.gov/news.release/conemp.t02.htm"],"runAt":"2026-07-21T01:09:11Z","reasoning":[{"kind":"heading","text":"July 2026 healthcare support employment forecast"},{"kind":"text","text":"The resolver is the first July 2026 print for Total employed people age 16 and over in 'Healthcare support occupations' in CPS Table A-19, measured in thousands and not seasonally adjusted, then multiplied by 0.001. All anchors below use that same CPS occupation/NSA variant. The ledger expectedReleaseWindow ending 2026-08-06 conflicts with the official August 7 release date; the forecast remains tied to the registered target and uses the verified official date."},{"kind":"tool","tool":"official.lookup","call":"Read current BLS CPS Employment Situation Table A-19 for the healthcare support occupations row.","result":"BLS Table A-19 reports 5,950 thousand for June 2025 and 5,691 thousand for June 2026, equivalent to 5.950 million and 5.691 million."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS July 2023 contingent-work table as an additional public CPS occupation-level reference observation.","result":"The BLS CPS table reports 4,911 thousand total employed people in healthcare support occupations in July 2023, equivalent to 4.911 million."},{"kind":"tool","tool":"official.calendar","call":"Verify the July 2026 Employment Situation publication date using the BLS 2026 release calendar and latest release announcement.","result":"The official calendar lists Employment Situation for July 2026 on Friday, August 7, 2026 at 8:30 AM ET; the June 2026 release repeats August 7, 2026."},{"kind":"text","text":"The outside-view base rate/reference class is persistence around the latest 5.691 million level, with substantial CPS subgroup noise. The sparse same-variant official history spans 4.911 million in July 2023, 5.950 million in June 2025, and 5.691 million in June 2026."},{"kind":"text","text":"Level contributes 5.691 million. Momentum is mixed: the latest year-over-year change is -0.259 million. A July calendar/seasonal adjustment contributes +0.080 million, while continuing structural demand for healthcare support labor contributes +0.030 million; no discrete policy or one-off shock is added."},{"kind":"math","text":"Prior/update/interval: persistence model prior = 5.691 million; historical sample = 4.911, 5.950, and 5.691 million. Successive changes are +1.039 and -0.259 million; their sample standard deviation gives sigma = sqrt(((1.039-0.390)^2+(-0.259-0.390)^2)/(2-1)) = 0.918 million. Updates are +0.080 July seasonality and +0.030 structural healthcare demand, so point = 5.691+0.080+0.030 = 5.801 million. The 80% half-width is 1.28*sigma = 1.28*0.918 = 1.175 million, implying 5.801-1.175 = 4.626 and 5.801+1.175 = 6.976 million."},{"kind":"text","text":"Upside risk comes from unusually strong household-survey sampling, labor-force entry, or faster caregiving hiring and would land above the interval at more than 6.976 million. Downside risk comes from a sharp participation decline, healthcare funding disruption, or an adverse CPS sampling swing and would land below the interval at less than 4.626 million. The wide interval reflects realized occupation-level dispersion rather than a rounded hedge."},{"kind":"forecast","point":5.801,"ciLow":4.626,"ciHigh":6.976}]}
