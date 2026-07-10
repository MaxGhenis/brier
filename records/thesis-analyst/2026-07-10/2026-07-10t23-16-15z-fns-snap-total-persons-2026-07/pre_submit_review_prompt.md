# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fns.snap.total_persons
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "snap-participation-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "usda.fns.snap.persons.july_2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-12-07", "start": "2026-11-29"}, "field": "Persons", "releasePolicy": "first_print", "sourceSeriesId": "fns.snap.total_persons", "sourceUrl": "https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap", "table": "FNS SNAP data tables, national monthly participation (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-9a15e6578b701e805a6459126176e230c3d057077fa7f2b829d129dfa24dae30.json"
- targetContentHash: "9a15e6578b701e805a6459126176e230c3d057077fa7f2b829d129dfa24dae30"
- registrationCommit: "a6aa0d72352081ffa58d0615c5daf6c7c553e4ee"
- registeredAtUtc: "2026-07-10T23:13:40Z"
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
c0ff30755551e7c0fa62217eeb75cbde671c5aafb27b8b5c5f875fcd08b11fe3

# Draft forecast response
{"slug":"snap-participation-july-2026","country":"US","type":"data","title":"US SNAP participation, July 2026","question":"What will USDA FNS report as national SNAP participation (Persons) for July 2026 in the first published monthly table, in millions?","unit":"millions","pointEstimate":35.9,"ciLow":34.8,"ciHigh":37.0,"confidence":0.8,"resolutionDate":"2026-12-07","resolutionSource":"USDA Food and Nutrition Service SNAP Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","resolutionRule":"Resolve to the Persons value for July 2026 in the first official FNS SNAP national monthly participation table published for that month. Convert the table value from thousands to millions by multiplying by 0.001 and round to three decimals; ignore all subsequent revisions. No release-day correction or grace exception applies.","dataPointId":"usda.fns.snap.persons.july_2026","historicalContext":[{"label":"January 2026","value":38.456892},{"label":"February 2026","value":37.72941},{"label":"March 2026","value":37.298271},{"label":"July 2025","value":42.01283}],"drivers":["rapid recent participation decline","expanded SNAP eligibility and work-requirement effects","slowing month-to-month decline by March","administrative reporting and preliminary-data volatility"],"sourceContext":["https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","https://www.fns.usda.gov/sites/default/files/resource-files/snap-4fymonthly-6.pdf"],"runAt":"2026-07-10T23:17:11Z","reasoning":[{"kind":"heading","text":"Forecast: July 2026 national SNAP participation"},{"kind":"text","text":"The resolver is the first official national monthly SNAP table's Persons value for July 2026, not a quality-control release, state subtotal, household count, annual average, or later revision. The stable series page is the exact FNS SNAP Data Tables page; the ledger's official-calendar registration fixes publication on 2026-12-07."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest USDA FNS national monthly SNAP participation PDF and read the Persons column for FY 2026.","result":"The June 12, 2026 table reports 38,456,892 persons in January 2026, 37,729,410 in February 2026, and 37,298,271 in March 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetch the same-variant historical Persons observations from the official national monthly table.","result":"The table reports 42,012,830 persons in July 2025, 41,836,900 in August 2025, 41,633,090 in September 2025, and 41,091,800 in October 2025."},{"kind":"tool","tool":"official.lookup","call":"Check the official FNS publication metadata and registered release schedule for the exact monthly table.","result":"The official table is dated June 12, 2026, contains data through March 2026, and the official schedule registers the July 2026 first print for 2026-12-07."},{"kind":"text","text":"The reference class/base rate is the 24 successive monthly changes from March 2024 through March 2026 in the same Persons series. Participation moved from 41.572 million in March 2024 to 37.298 million in March 2026; the mean monthly change was about -0.178 million, while the latest five changes were materially more negative as eligibility and administrative changes took effect."},{"kind":"math","text":"Prior/update/interval: The model is a damped monthly-change persistence prior using the 24-change historical sample. Its level anchor is March 2026 at 37.298 million. The 24 successive changes have sum about -4.273 million and sum of squares about 5.053, so sample sigma = sqrt((5.053 - 24*(-0.178)^2)/23) = 0.432 million. Level and momentum imply four further declines averaging about 0.35 million, giving 37.298 - 4*0.35 = 35.898, rounded to 35.9. The one-month 80% half-width is 1.28*sigma = 1.28*0.432 = 0.553 million; I widen it to about 1.10 million because July is four monthly transitions beyond the March anchor, approximately sqrt(4)*0.553. Final implied bounds are 35.9 - 1.1 = 34.8 and 35.9 + 1.1 = 37.0 million."},{"kind":"text","text":"Upside risk comes from the March deceleration persisting, delayed implementation, or reinstatement of eligible cases; participation above 37.0 million would land outside the interval. Downside risk comes from another wave of eligibility terminations or unusually fast recertification effects; participation below 34.8 million would land outside the interval."},{"kind":"forecast","point":35.9,"ciLow":34.8,"ciHigh":37.0}]}
