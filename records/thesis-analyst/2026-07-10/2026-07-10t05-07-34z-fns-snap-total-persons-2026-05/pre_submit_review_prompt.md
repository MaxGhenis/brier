# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fns.snap.total_persons
- period: 2026-05
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "snap-participation-may-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "usda.fns.snap.persons.may_2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-10-04", "start": "2026-09-26"}, "field": "Persons", "releasePolicy": "first_print", "sourceSeriesId": "fns.snap.total_persons", "sourceUrl": "https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap", "table": "FNS SNAP data tables, national monthly participation (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-ce991f6991d220d23c0e726215dd851d2dc220fecb76c58a8a740d915a0eeacd.json"
- targetContentHash: "ce991f6991d220d23c0e726215dd851d2dc220fecb76c58a8a740d915a0eeacd"
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
d1f0fc44052a6e6632b0d53839f25a322259ec070397fb6997d0e4ba172d3894

# Draft forecast response
{"slug":"snap-participation-may-2026","country":"US","type":"data","title":"SNAP participation, May 2026","question":"USDA FNS SNAP national monthly participation, Persons, May 2026, not seasonally adjusted, first print, converted from the FNS table's thousands of persons to millions of persons.","unit":"millions","pointEstimate":41.62,"ciLow":40.9,"ciHigh":42.34,"confidence":0.8,"resolutionDate":"2026-09-30","resolutionSource":"USDA Food and Nutrition Service SNAP Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","resolutionRule":"Resolve to the first official USDA FNS SNAP data-table print for national monthly participation, table Persons, May 2026. Use the reported national Persons value in thousands and multiply by 0.001 to express millions. Do not use later revisions or same-day corrected files unless the first print itself is withdrawn before publication as an official file.","dataPointId":"usda.fns.snap.persons.may_2026","historicalContext":[{"label":"latest_nov_2025","value":42.311},{"label":"oct_2025","value":42.284},{"label":"may_2025","value":42.19},{"label":"may_2024","value":41.73}],"drivers":["Recent FNS national participation is near 42.3 million persons","May seasonal movement from the prior November is usually modest","2026 eligibility and administrative-policy tightening creates downside risk versus persistence","Labor-market deterioration or delayed policy implementation would keep participation closer to the recent level"],"sourceContext":["https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","https://www.fns.usda.gov/pd/data-release-calendar"],"runAt":"2026-07-10T05:10:00Z","reasoning":[{"kind":"heading","text":"Forecast for USDA FNS SNAP Persons, May 2026"},{"kind":"text","text":"Framing and exact resolver: this target is the USDA Food and Nutrition Service national SNAP monthly participation table, Persons, not seasonally adjusted. The FNS file reports persons in thousands, and this cell reports millions using the ledger transform factor 0.001."},{"kind":"tool","tool":"official.lookup","call":"Checked USDA FNS SNAP Data Tables page for the current official monthly SNAP participation table and latest available period.","result":"FNS page identifies the national monthly Persons, Households, Benefits table and shows Latest Available Month: November 2025; extracted recent national Persons values were September 2025 = 42.239 million, October 2025 = 42.284 million, and November 2025 = 42.311 million after converting thousands to millions."},{"kind":"tool","tool":"official.lookup","call":"Checked USDA FNS release calendar for the first-print timing of the May 2026 SNAP monthly participation table.","result":"The official release schedule places the May 2026 SNAP monthly data release on 2026-09-30, inside the registered expected window 2026-09-26 to 2026-10-04; the page also listed monthly SNAP releases with a 2026 schedule year."},{"kind":"tool","tool":"official.lookup","call":"Pulled same-series FNS national Persons history for recent May reference points and near-current months.","result":"Same variant and unit after conversion: May 2023 = 42.083 million, May 2024 = 41.730 million, May 2025 = 42.190 million, October 2025 = 42.284 million, November 2025 = 42.311 million."},{"kind":"text","text":"Base rate/reference class: the recent official-source reference class is a high-level, slow-moving national caseload around 41.7 to 42.3 million persons, with May-to-May moves of -0.353 million from 2023 to 2024 and +0.460 million from 2024 to 2025 rather than a clear trend."},{"kind":"text","text":"Level, momentum, and mechanism: level starts from the latest FNS November 2025 value of 42.311 million. Momentum is near flat, because September to November 2025 rose only 0.072 million. The main inside-view adjustment is a negative policy/administrative effect in early 2026, partially offset by normal churn and any weaker labor-market conditions."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest official November 2025 Persons, 42.311 million; historical sample = recent FNS Nov-to-May and May-to-May movements from the same national monthly Persons series; adjustment components = -0.04 million seasonal Nov-to-May base drift and -0.65 million for 2026 eligibility/administrative tightening, so point = 42.311 - 0.04 - 0.65 = 41.621 million, rounded to 41.62. Interval method = realized dispersion of comparable six-month level changes; sigma = 0.52 million, so 1.28*sigma = 0.666 million. I widen slightly to 0.72 million for policy timing uncertainty, giving 41.62 - 0.72 = 40.90 and 41.62 + 0.72 = 42.34."},{"kind":"text","text":"Counter-considerations: upside risk is that eligibility changes bite faster than assumed or states accelerate removals, which would land below the interval near or under 40.9 million. Downside risk to a low-participation forecast is that policy effects are delayed, litigation/implementation frictions slow terminations, or the labor market weakens; that would land above the interval near or above 42.34 million. Outside the interval would require either a broad administrative drop exceeding roughly 1.4 million from November or a near-complete absence of 2026 policy effects plus renewed caseload growth."},{"kind":"forecast","point":41.62,"ciLow":40.9,"ciHigh":42.34}]}
