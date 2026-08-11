# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fns.snap.total_persons
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "snap-participation-august-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "usda.fns.snap.persons.august_2026"
- expectedReleaseWindow: {"end": "2027-01-11", "start": "2027-01-03"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2027-01-11", "start": "2027-01-03"}, "field": "Persons", "releasePolicy": "first_print", "sourceSeriesId": "fns.snap.total_persons", "sourceUrl": "https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap", "table": "FNS SNAP data tables, national monthly participation (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-bc941c534dcbaf1f13d1b9ba88a016f9cf51fde91019bc90beea1873ced2f0a2.json"
- targetContentHash: "bc941c534dcbaf1f13d1b9ba88a016f9cf51fde91019bc90beea1873ced2f0a2"
- registrationCommit: "e8c13ea71f583ab7105a64de5fe4c8594cfcb6d0"
- registeredAtUtc: "2026-08-11T12:50:27Z"
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
7db8336cdd5be13aabc3c2b82e0efd06c44335ae270893b313bb696fcb11228f

# Draft forecast response
{"slug":"snap-participation-august-2026","country":"US","type":"data","title":"US SNAP participation, August 2026","question":"What will USDA FNS first report for national SNAP participation, Persons, in August 2026, converted from persons to millions?","unit":"millions","pointEstimate":35.81,"ciLow":35.08,"ciHigh":36.55,"confidence":0.8,"resolutionDate":"2027-01-11","resolutionSource":"USDA Food and Nutrition Service SNAP Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","resolutionRule":"Resolve to the first official USDA FNS SNAP Data Tables national monthly Participation Persons value for August 2026, using the national monthly table 'Persons, Households, Benefits, and Average Monthly Benefit per Person & Household'; convert the official persons count to millions by multiplying by 0.000001, equivalent to the registered thousands-to-millions transform when the table is read in thousands. Use the first print only; do not substitute later revisions.","dataPointId":"usda.fns.snap.persons.august_2026","historicalContext":[{"label":"Apr 2026 latest preliminary","value":37.011096},{"label":"Mar 2026 preliminary","value":37.438048},{"label":"Feb 2026 preliminary","value":37.875833},{"label":"Aug 2025","value":41.841272}],"drivers":["Recent official SNAP participation decline through April 2026","FY 2026 benefit and eligibility standards already in force for the target month","Policy implementation risk from 2025 SNAP eligibility and work-rule changes","Seasonal August participation is not enough to offset current downtrend"],"sourceContext":["https://fns-prod.azureedge.us/pd/supplemental-nutrition-assistance-program-snap","https://fns-prod.azureedge.us/sites/default/files/resource-files/snap-4fymonthly7.pdf","https://fns-prod.azureedge.us/snap/allotment/cola"],"runAt":"2026-08-11T13:22:50Z","reasoning":[{"kind":"heading","text":"SNAP national participation forecast for August 2026"},{"kind":"text","text":"Framing and exact resolver: the target is the USDA FNS national SNAP monthly table, Participation Persons, for August 2026, first print, converted to millions. The registered contract sets a resolve-by-bound resolution date of 2027-01-11 within the expected 2027-01-03 to 2027-01-11 release window; the FNA data page itself showed the monthly table and latest-data timestamp but I did not find a separate date-specific public release calendar page in this run."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA/FNA SNAP Data Tables page and identified the national monthly participation table and latest data vintage.","result":"Fetched page showed Latest Available Month = April 2026, Page updated = August 06, 2026, and the national monthly table link FY 23 through FY 26; this confirms the exact series family and a July 2026 public update."},{"kind":"tool","tool":"official.lookup","call":"Opened the USDA/FNA national SNAP monthly PDF table for FY 2023 through FY 2026 and read recent Persons values.","result":"Fetched Persons values: Aug 2025 = 41,841,272; Sep 2025 = 41,637,114; Oct 2025 = 41,096,660; Nov 2025 = 39,999,890; Dec 2025 = 39,207,898; Jan 2026 = 38,476,351; Feb 2026 = 37,875,833; Mar 2026 = 37,438,048; Apr 2026 = 37,011,096."},{"kind":"tool","tool":"official.lookup","call":"Read the USDA/FNA Program Data overview context for vintage and preliminary-status handling.","result":"Fetched overview values: latest month April 2026, data as of July 10, 2026, annual state-level data cover 2020-2025, and the page says most current numbers are preliminary and subject to revision."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA/FNA FY 2026 SNAP COLA policy page to check target-month benefit/eligibility setting.","result":"Fetched FY 2026 standards effective Oct. 1, 2025 through Sept. 30, 2026; 48-state gross monthly income limit for household size 4 = $3,483; maximum monthly allotment for household size 4 in the 48 states and DC = $994; minimum allotment for 1-2 person households = $24."},{"kind":"text","text":"Reference class/base rate: for an official-source level series with monthly administrative reporting, I start from persistence plus recent monthly change, not from the long pandemic/disaster period. The cleanest recent reference class is FY 2025 through FY 2026 national monthly Persons, with special caution that FY 2023 included unusually high and volatile values such as Aug 2023 = 53.518725 million."},{"kind":"text","text":"Level and momentum: Apr 2026 was 37.011096 million. Recent sequential changes were -0.540454, -1.096770, -0.791992, -0.731547, -0.600518, -0.437785, and -0.426952 million from Sep 2025-Apr 2026, so the decline was still large but easing by March-April."},{"kind":"text","text":"Policy and one-off effects: FY 2026 eligibility and allotment settings are already in force for August 2026, so I do not add a mechanical October COLA break. I do keep a negative adjustment because 2025-2026 policy memoranda and work-rule/eligibility implementation risk plausibly continue trimming caseloads before August, while the November 2025 disruption is partly a one-off and should not be linearly extrapolated."},{"kind":"math","text":"Prior/update/interval: persistence prior = Apr 2026 official Persons of 37.011096 million; historical sample = recent official monthly changes from Sep 2025 through Apr 2026; adjustment components = -0.25 million/month underlying caseload normalization, -0.05 million/month policy/friction drag, and no positive August seasonal offset because 2025 Apr-to-Aug was -0.515774 million. Point = 37.011096 + 4*(-0.30) = 35.811096, rounded to 35.81. Monthly change dispersion from the seven fetched changes is about 0.249 million; four-month propagated sigma = sqrt(4)*0.249 = 0.498 million, widened for policy uncertainty to sigma = 0.574 million; 1.28*sigma = 0.735 million, giving 35.811096 +/- 0.735 = [35.08, 36.55]."},{"kind":"text","text":"Counter-consideration: upside risk is a faster-than-expected halt in recertification losses or disaster-assistance additions, which would land above the interval if August participation stays above 36.55 million. Downside risk is broader eligibility/work-rule implementation or administrative churn, which would land below the interval if August participation falls below 35.08 million. A major reporting reclassification would also be outside the interval but should still resolve on the same first-print Persons field."},{"kind":"forecast","point":35.81,"ciLow":35.08,"ciHigh":36.55}]}
