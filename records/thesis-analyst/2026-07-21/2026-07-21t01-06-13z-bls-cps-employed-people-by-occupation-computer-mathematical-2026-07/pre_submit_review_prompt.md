# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.employed_people_by_occupation.computer_mathematical
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-computer-math-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.computer_mathematical.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Computer and mathematical occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.computer_mathematical", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-9008e5bd3c60b6d015f5989bcf403009c9ea1156c41007faec60f49194626eca.json"
- targetContentHash: "9008e5bd3c60b6d015f5989bcf403009c9ea1156c41007faec60f49194626eca"
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
57638133d4b1d943c129802e4101100baed29ea4dc406c6b55f7cc2e6f61655c

# Draft forecast response
{"slug":"cps-computer-math-employment-july-2026","country":"US","type":"data","title":"US computer and math employment, July 2026","question":"How many people were employed in computer and mathematical occupations in July 2026, not seasonally adjusted, in the BLS CPS first print?","unit":"millions","pointEstimate":6.98,"ciLow":6.68,"ciHigh":7.28,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, CPS Table A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the total number of employed people age 16 and over in the 'Computer and mathematical occupations' row of CPS Employment Situation Table A-19 for July 2026, not seasonally adjusted, as first published by BLS on August 7, 2026. Convert thousands to millions by multiplying by 0.001 and retain three decimal places. Ignore subsequent revisions. The registered source window ending August 6 conflicts with the official BLS calendar and June release notice, both of which specify August 7.","dataPointId":"bls.cps.employed_people_by_occupation.computer_mathematical.july_2026.first_print","historicalContext":[{"label":"2021 annual average","value":5.688},{"label":"2022 annual average","value":6.171},{"label":"2023 annual average","value":6.502},{"label":"2024 annual average","value":6.386},{"label":"2025 annual average","value":6.711},{"label":"June 2025","value":6.602},{"label":"June 2026","value":6.95}],"drivers":["June 2026 level of 6.950 million","positive longer-run occupational employment trend","CPS sampling volatility","weak tech hiring versus resilient incumbent employment"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/cps/cpsaat09.htm","https://www.bls.gov/cps/data/aa2023/cpsaat09.htm","https://www.bls.gov/cps/aa2022/cpsaat09.htm","https://www.bls.gov/cps/publications/release-calendar.htm","https://www.bls.gov/news.release/archives/empsit_07022026.pdf"],"runAt":"2026-07-21T01:06:38Z","reasoning":[{"kind":"heading","text":"July 2026 computer and mathematical employment forecast"},{"kind":"text","text":"The target is the total, age 16 and over, for Computer and mathematical occupations in CPS Table A-19, reported in thousands and not seasonally adjusted. Resolution uses the strict August 7 first print and the table's 0.001 conversion to millions."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest BLS CPS Table A-19 observation and matched year-earlier value.","result":"BLS Table A-19 reports 6,950 thousand employed in June 2026 and 6,602 thousand in June 2025 for Computer and mathematical occupations."},{"kind":"tool","tool":"official.lookup","call":"Fetch recent BLS annual-average occupation levels from CPS Table 9.","result":"BLS CPS Table 9 reports 6,386 thousand in 2024 and 6,711 thousand in 2025; the 2025 figure is an 11-month average because October data were not collected."},{"kind":"tool","tool":"official.lookup","call":"Fetch earlier official CPS annual-average reference-class observations.","result":"Official CPS Table 9 archives report 5,688 thousand in 2021, 6,171 thousand in 2022, and 6,502 thousand in 2023."},{"kind":"tool","tool":"official.lookup","call":"Verify the official release date from the BLS CPS calendar and latest Employment Situation notice.","result":"The BLS calendar lists the July 2026 Employment Situation for August 7, 2026, and the June release specifies August 7, 2026 at 8:30 a.m. ET; this is 1 day after the registered expected window end."},{"kind":"text","text":"The outside-view base rate is gradual growth with substantial CPS noise: annual-average employment rose from 5.688 million in 2021 to 6.711 million in 2025, while June 2026 was 0.348 million above June 2025."},{"kind":"text","text":"Level, momentum, one-off, and mechanism effects: the 6.950 million June level supplies the persistence anchor; positive multi-year growth adds 0.05 million; weak technology hiring subtracts 0.02 million; no identified July-specific policy or classification change warrants another adjustment."},{"kind":"math","text":"Prior/update/interval: persistence model prior = June 2026's 6.950 million; historical sample = 2021-2025 annual averages of 5.688, 6.171, 6.502, 6.386, and 6.711 million; successive changes are +0.483, +0.331, -0.116, and +0.325 million, giving sigma = 0.236 million. Adjustments are +0.050 million for longer-run momentum and -0.020 million for soft hiring, yielding 6.950 + 0.050 - 0.020 = 6.980 million. The normal 80% half-width is 1.28*sigma = 1.28*0.236 = 0.302 million, implying 6.678 to 7.282 million, rounded to 6.68 to 7.28 million."},{"kind":"text","text":"Upside risk comes from faster AI-related hiring, labor-force re-entry, or favorable CPS sampling and would land above the interval if employment exceeds 7.28 million. Downside risk comes from layoffs, weak hiring, or adverse sampling and would land below the interval if employment is under 6.68 million; either outcome would be outside the interval."},{"kind":"forecast","point":6.98,"ciLow":6.68,"ciHigh":7.28}]}
