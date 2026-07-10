# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fns.wic.total_participation
- period: 2026-05
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "wic-participation-may-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "fns.wic.total_participation.2026-05.first_print"
- resolutionDate: "2026-08-14"
- resolutionSource: "Official agency release"
- resolutionSourceUrl: "https://www.fns.usda.gov/pd/wic-program"
- resolutionRule: "Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. The expected displayed FNS monthly table value is a whole participant count, as in 6,894,610 for May 2025; convert that displayed person count to millions by dividing by 1,000,000 and round to 0.001 million for the cell. If the ledger adapter instead extracts an intermediate value expressed in thousands of participants, its listed factor 0.001 produces the same final unit of millions. Use the first posted May 2026 value only; ignore later preliminary/final revisions or annual-summary revisions."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-08-15", "start": "2026-08-07"}, "field": "fns.wic.total_participation", "releasePolicy": "first_print", "sourceSeriesId": "fns.wic.total_participation", "sourceUrl": "https://www.fns.usda.gov/pd/wic-program", "table": "Official agency release", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-d9f0f26436f4322b04c9deeec1745f166dd46dbeec72d9ec676b1e2cf86ae6a9.json"
- targetContentHash: "d9f0f26436f4322b04c9deeec1745f166dd46dbeec72d9ec676b1e2cf86ae6a9"
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
63b5071f47ba9db650de78217132d81d4758f445b4850e1c7c6ea5458a1ee46e

# Draft forecast response
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC total participation, May 2026","question":"National USDA FNS WIC total participants in May 2026, unadjusted monthly national level, first official print","unit":"millions","pointEstimate":6.95,"ciLow":6.814,"ciHigh":7.055,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Convert the displayed whole participant count to millions by dividing by 1,000,000 and round to 0.001 million. Use the first posted May 2026 value only; ignore later preliminary, final, or annual-summary revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"May 2023","value":6.696739},{"label":"May 2024","value":6.76371},{"label":"May 2025","value":6.89461},{"label":"Jun 2025","value":6.8832},{"label":"Jul 2025","value":6.923326},{"label":"Aug 2025","value":6.895538}],"drivers":["recent upward participation trend","seasonal spring enrollment strength","preliminary first-print reporting noise","stable national WIC eligibility and benefit access"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-2.pdf","https://www.fns.usda.gov/wic/certification-and-monthly-food-benefits-issuance-cycles-and-reporting-monthly-participation-fns-798"],"runAt":"2026-07-10T22:23:48Z","thresholdLadder":{"thresholds":[6.75,6.8,6.85,6.9,6.93,6.95,6.97,7,7.03,7.07],"cumulativeProbabilities":[0.04,0.08,0.15,0.25,0.35,0.5,0.62,0.75,0.85,0.93]},"reasoning":[{"kind":"heading","text":"USDA FNS WIC total participation, May 2026"},{"kind":"text","text":"The target is the unadjusted national WIC Total Participants value for May 2026 in the first official FNS monthly table that includes that month. The resolver uses the displayed whole-person count converted to millions and rounded to 0.001; May 2025 is explicitly 6,894,610 participants."},{"kind":"tool","tool":"official.lookup","call":"Fetch the official FNS WIC monthly national table for May 2023.","result":"FNS reported May 2023 total participants of 6,696,739, equal to 6.696739 million."},{"kind":"tool","tool":"official.lookup","call":"Fetch the official FNS WIC monthly national table for May 2024.","result":"FNS reported May 2024 total participants of 6,763,710, equal to 6.763710 million."},{"kind":"tool","tool":"official.lookup","call":"Fetch the official FNS WIC monthly national table for May 2025.","result":"FNS reported May 2025 total participants of 6,894,610, equal to 6.894610 million."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest official FNS monthly observations available before the forecast period.","result":"FNS reported June 2025 at 6,883,200, July 2025 at 6,923,326, August 2025 at 6,895,538, September 2025 at 6,921,555, October 2025 at 6,909,050, and November 2025 at 6,752,138 participants."},{"kind":"text","text":"The official release-window contract places the first May 2026 print in the 2026-08-07 through 2026-08-15 window and sets resolutionDate to 2026-08-14; I retain that ledger date rather than inferring a date from cadence. The FNS table identifies FY 2026 observations as preliminary and subject to revision, while this target resolves only the first print."},{"kind":"text","text":"The reference class is the fetched May observations of 6.696739 million in 2023, 6.763710 million in 2024, and 6.894610 million in 2025, supplemented by the 6.883200-6.923326 million June-July 2025 range. The base rate is gradual year-over-year growth with month-to-month noise, so the central estimate extends the recent level modestly rather than extrapolating the full 2023-2025 slope."},{"kind":"text","text":"Level and momentum point modestly higher: May participation rose from 6.696739 million to 6.763710 million to 6.894610 million across 2023-2025, while the latest observations clustered near 6.9 million. A one-off reporting or seasonal effect can move the first print away from that trend, and no separate policy shock is assumed."},{"kind":"text","text":"Prior/update/interval: use a persistence-plus-trend prior centered near the latest 6.9 million level, informed by the three-year May reference class; update upward for the 2023-2025 May increase and recent 6.923326 million July observation, but widen for preliminary first-print noise. The threshold ladder implies an interval from 6.814 million to 7.055 million."},{"kind":"math","text":"Ladder: P(X <= 6.75) = 0.04; P(X <= 6.8) = 0.08; P(X <= 6.85) = 0.15; P(X <= 6.9) = 0.25; P(X <= 6.93) = 0.35; P(X <= 6.95) = 0.5; P(X <= 6.97) = 0.62; P(X <= 7.0) = 0.75; P(X <= 7.03) = 0.85; P(X <= 7.07) = 0.93. Linear interpolation gives 10th percentile at 6.814, median at 6.950, and 90th percentile at 7.055."},{"kind":"text","text":"Downside risk is a first print below 6.814 million from weaker enrollment or delayed state reporting. Upside risk is a participation surge above 7.055 million from stronger spring enrollment or reporting catch-up. A materially different administrative count or revision would land outside the interval."},{"kind":"forecast","point":6.95,"ciLow":6.814,"ciHigh":7.055}]}
