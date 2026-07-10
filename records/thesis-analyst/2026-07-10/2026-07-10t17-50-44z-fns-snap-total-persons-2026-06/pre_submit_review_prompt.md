# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fns.snap.total_persons
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "snap-participation-june-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "usda.fns.snap.persons.june_2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-11-03", "start": "2026-10-26"}, "field": "Persons", "releasePolicy": "first_print", "sourceSeriesId": "fns.snap.total_persons", "sourceUrl": "https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap", "table": "FNS SNAP data tables, national monthly participation (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-fa0d017e2d4445b343793d95ea532622f4da9946c9dc0ce333ef7298be904a6d.json"
- targetContentHash: "fa0d017e2d4445b343793d95ea532622f4da9946c9dc0ce333ef7298be904a6d"
- registrationCommit: "79e7796ea8cde8d3c263a226250346d3aa2c88d9"
- registeredAtUtc: "2026-07-10T17:47:41Z"
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
2d880a721404c5df2c09cffa82a2998ea83a51ecf0a36c4628825effe483987e

# Draft forecast response
{"slug":"snap-participation-june-2026","country":"US","type":"data","title":"US SNAP Participation, June 2026","question":"What will USDA FNA first report for total persons participating in SNAP nationally in June 2026, unadjusted, in millions?","unit":"millions","pointEstimate":35.55,"ciLow":34.71,"ciHigh":36.39,"confidence":0.8,"resolutionDate":"2026-11-03","resolutionSource":"USDA Food and Nutrition Administration SNAP Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","resolutionRule":"Resolve to the first value published for Persons for June 2026 in the USDA FNA SNAP national monthly participation table, reported in thousands and multiplied by 0.001 to millions. Use the first print available on the specified SNAP Data Tables page; disregard later revisions. Round the resolved value to three decimal places in millions.","dataPointId":"usda.fns.snap.persons.june_2026","historicalContext":[{"label":"January 2026 first available official table value","value":38.456892},{"label":"February 2026 first available official table value","value":37.72941},{"label":"March 2026 latest official table value","value":37.298271},{"label":"June 2025 official table value","value":42.08488}],"drivers":["Strong FY2026 participation downtrend","Recent monthly decline beginning to moderate","Tighter eligibility and work-requirement environment","Administrative reporting volatility"],"sourceContext":["https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","https://fns-prod.azureedge.us/sites/default/files/resource-files/snap-4fymonthly-6.pdf","https://fns-prod.azureedge.us/pd/overview","https://www.fns.usda.gov/snap/recipient/eligibility"],"runAt":"2026-07-10T17:51:47Z","reasoning":[{"kind":"heading","text":"June 2026 national SNAP participation forecast"},{"kind":"text","text":"The resolver is the unadjusted national Persons field for June 2026 in the FNS/FNA SNAP monthly participation table, not an annual quality-control measure. The official table reports persons in thousands; the cell converts that figure to millions. The first print is binding, with no correction-day grace period."},{"kind":"tool","tool":"official.lookup","call":"Fetch the USDA FNA SNAP national monthly participation table and read the latest FY2026 Persons observations.","result":"The table dated June 12, 2026 reports 38,456,892 persons in January 2026, 37,729,410 in February 2026, and 37,298,271 in March 2026, equivalent to 38.456892, 37.729410, and 37.298271 million."},{"kind":"tool","tool":"official.lookup","call":"Fetch the same official SNAP table's recent reference-class history.","result":"Official Persons values were 42,180,523 in February 2025, 42,193,855 in March, 42,353,149 in April, 42,248,301 in May, 42,084,880 in June, 42,012,830 in July, 41,836,900 in August, and 41,633,090 in September."},{"kind":"tool","tool":"official.lookup","call":"Check the official SNAP table's FY2026 transition and annual summaries.","result":"Persons fell from 41,091,800 in October 2025 to 39,997,940 in November and 39,205,146 in December; USDA reports FY2025 average participation of 42,383,194 and the preliminary FY2026-to-date average of 38,963,243."},{"kind":"tool","tool":"official.lookup","call":"Verify the release timing against the official FNA program-data schedule and target release window.","result":"The official schedule places the June 2026 SNAP monthly-table release on 2026-11-03; the latest table available during this run covered March 2026 and was dated 2026-06-12."},{"kind":"text","text":"The outside-view base rate is persistence with drift for a slowly moving administrative caseload. The 13 monthly changes from February 2025 through March 2026 average -0.376 million, but the FY2026 decline is much steeper: October-to-March participation fell 3.794 million. Level is therefore anchored at March's 37.298 million; momentum remains negative, while the shrinking March decline supplies a moderating adjustment."},{"kind":"text","text":"Mechanisms are separated as follows: level 37.298 million; momentum approximately -0.58 million per month over April-June; moderation adds about 0.10 million per month relative to the latest FY2026 trend; tighter eligibility and work rules retain a negative policy adjustment. These components imply about 35.55 million rather than simple flat persistence."},{"kind":"math","text":"Prior/update/interval: persistence-with-drift prior; historical sample is the 13 successive monthly changes from February 2025 through March 2026. Their sample standard deviation is sigma = 0.376 million, so the one-step 80% half-width is 1.28*sigma = 1.28*0.376 = 0.482 million. For a three-month horizon, scale by sqrt(3): 0.482*1.732 = 0.835, rounded to 0.84 million. Point = 37.298 - 1.748 = 35.550; bounds = 35.550 +/- 0.840 = [34.710, 36.390]."},{"kind":"text","text":"Upside risk: faster stabilization in enrollment or delayed implementation of tighter eligibility rules would land above 36.39 million. Downside risk: continued declines near the November-January pace, broad recertification losses, or unusually aggressive enforcement would land below 34.71 million, outside the interval."},{"kind":"forecast","point":35.55,"ciLow":34.71,"ciHigh":36.39}]}
