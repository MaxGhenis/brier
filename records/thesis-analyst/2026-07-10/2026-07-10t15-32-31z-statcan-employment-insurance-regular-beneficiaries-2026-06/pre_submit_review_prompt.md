# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: statcan.employment_insurance.regular_beneficiaries
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "canada-ei-regular-beneficiaries-june-2026"
- country: "CA"
- targetUnit: "thousands"
- dataPointId: "statcan.employment_insurance.regular_beneficiaries.canada.june_2026.first_print"
- resolutionDate: "2026-08-20"
- resolutionSource: "Statistics Canada Table 14-10-0011-01 and The Daily Employment Insurance release"
- resolutionSourceUrl: "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101"
- resolutionRule: "Resolve to the first Statistics Canada publication for June 2026 regular Employment Insurance beneficiaries for Canada, seasonally adjusted, beneficiary detail total, sex total, age group total, from Table 14-10-0011-01 or the same first-print The Daily release. Convert persons to thousands by multiplying by 0.001. Use the first print only; ignore later revisions or table corrections unless the first-print rule itself is changed by Statistics Canada before release."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-08-27", "start": "2026-08-19"}, "field": "statcan.employment_insurance.regular_beneficiaries", "releasePolicy": "first_print", "sourceSeriesId": "statcan.employment_insurance.regular_beneficiaries", "sourceUrl": "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101", "table": "Statistics Canada Employment Insurance Statistics, Table 14-10-0011-01 and The Daily release for May 2026", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-2071f24c9311aaa43cd5bf3d2af243438c9d0aa1124763f0d51d599364e0d06b.json"
- targetContentHash: "2071f24c9311aaa43cd5bf3d2af243438c9d0aa1124763f0d51d599364e0d06b"
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
4bb21ef60fbeaf9f353b1eff38c9399b5c627ec62de6169f07c8e2945fda0def

# Draft forecast response
{"slug":"canada-ei-regular-beneficiaries-june-2026","country":"CA","type":"data","title":"Canada regular EI beneficiaries, June 2026","question":"Statistics Canada regular Employment Insurance beneficiaries for Canada, seasonally adjusted, beneficiary detail total, both sexes, age 15 years and over, June 2026 first print","unit":"thousands","pointEstimate":537.5,"ciLow":531.8,"ciHigh":543.2,"confidence":0.8,"resolutionDate":"2026-08-20","resolutionSource":"Statistics Canada Table 14-10-0011-01 and The Daily Employment Insurance release","resolutionSourceUrl":"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101&request_locale=en","resolutionRule":"Resolve to the first Statistics Canada publication for June 2026 regular Employment Insurance beneficiaries for Canada, seasonally adjusted, beneficiary detail total, sex total, age group total, from Table 14-10-0011-01 or the same first-print The Daily release. Convert persons to thousands by multiplying by 0.001. Use the first print only; ignore later revisions or table corrections unless the first-print rule itself is changed by Statistics Canada before release.","dataPointId":"statcan.employment_insurance.regular_beneficiaries.canada.june_2026.first_print","historicalContext":[{"label":"December 2025","value":567.62},{"label":"January 2026","value":559.02},{"label":"February 2026","value":550.35},{"label":"March 2026","value":547.44},{"label":"April 2026","value":544.44}],"drivers":["Recent seasonally adjusted beneficiary decline","May employment gain and lower unemployment rate","Two-month forecast horizon from latest EI print","EI eligibility and claims timing may diverge from Labour Force Survey"],"sourceContext":["https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410001101&request_locale=en","https://www150.statcan.gc.ca/n1/daily-quotidien/260618/dq260618d-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm","https://www150.statcan.gc.ca/n1/release-diffusion/2026-eng.pdf"],"runAt":"2026-07-10T15:32:50Z","reasoning":[{"kind":"heading","text":"Canada regular EI beneficiaries: June 2026 first print"},{"kind":"text","text":"The resolver is the Canada, seasonally adjusted, Regular benefits, both-sexes, age-15-and-over variant in Statistics Canada Table 14-10-0011-01; all anchors below use that variant and are converted from persons to thousands. The ledger resolutionDate is 2026-08-20, but the official 2026-2027 release calendar places Employment Insurance for June 2026 on November 19, 2026; this is a concrete target-registration discrepancy, so this cell remains tied to the supplied ledger target and its first-print rule rather than silently changing it."},{"kind":"tool","tool":"official.lookup","call":"Fetched Statistics Canada Table 14-10-0011-01, Canada, Regular benefits, both sexes, age 15 years and over, seasonally adjusted.","result":"Fetched 567,620 persons in December 2025, 559,020 in January 2026, 550,350 in February, 547,440 in March, and 544,440 in April; converted values are 567.62, 559.02, 550.35, 547.44, and 544.44 thousands."},{"kind":"tool","tool":"official.lookup","call":"Fetched Statistics Canada The Daily Employment Insurance release for April 2026.","result":"The April release reports 544,440 regular EI beneficiaries in Canada, a monthly decrease of 0.5% and a 12-month increase of 3.5%; it states that May 2026 EI data will be released July 23."},{"kind":"tool","tool":"official.lookup","call":"Fetched Statistics Canada Labour Force Survey release for May 2026 as a current labour-market cross-check.","result":"May employment increased by 88,000 to 21,122,000, while the unemployment rate fell 0.3 percentage points to 6.6%; the April unemployment rate was 6.9%."},{"kind":"tool","tool":"official.lookup","call":"Fetched Statistics Canada 2026-2027 major-release calendar to verify the target's publication timing.","result":"The calendar lists Employment Insurance for May 2026 on July 23, Employment Insurance for June 2026 on November 19, and August 20 as the date for July industrial product and raw-material price indexes, not June Employment Insurance."},{"kind":"text","text":"Reference class/base rate: the immediate five-print reference class is a declining seasonally adjusted regular-beneficiary level, falling 23.18 thousand from December to April. The May labour-market improvement is a modest additional downward adjustment, but it is not mechanically the same population or timing as EI beneficiaries."},{"kind":"text","text":"Level and momentum point toward another modest decline after April; the May LFS employment gain and lower unemployment rate reinforce that direction. Offsetting this, EI receipt depends on eligibility, benefit duration, and claims timing, so the LFS signal is used only as a small adjustment."},{"kind":"math","text":"Prior/update/interval: persistence-with-recent-momentum prior uses the five fetched levels 567.62, 559.02, 550.35, 547.44, 544.44 and successive changes -8.60, -8.67, -2.91, -3.00 thousand; their sample standard deviation is sigma = 3.28 thousand, so 1.28*sigma = 4.20 thousand. A two-month horizon from the latest April EI print plus eligibility/timing uncertainty widens the half-width to 5.70 thousand (1.36x the one-step width). Starting from 544.44, recent persistence implies a low-540s May and a further modest June decline; the LFS adjustment yields 537.50, with 531.80 to 543.20."},{"kind":"text","text":"Counter-consideration: upside risk is a renewed rise in layoffs or faster claims conversion, which would lift beneficiaries above 543.20 thousand. Downside risk is that the May employment improvement persists and claims exhaust or decline faster than expected; a much stronger labour-market improvement or administrative shift would land below the interval."},{"kind":"forecast","point":537.5,"ciLow":531.8,"ciHigh":543.2}]}
