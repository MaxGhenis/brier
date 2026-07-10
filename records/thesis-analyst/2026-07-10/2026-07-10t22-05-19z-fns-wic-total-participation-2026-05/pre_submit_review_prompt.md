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
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC total participants, May 2026","question":"USDA FNS national WIC Total Participants for May 2026, calendar-month reporting, first official print","unit":"millions","pointEstimate":6.84,"ciLow":6.75,"ciHigh":6.95,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Convert the displayed whole-person count to millions by dividing by 1,000,000 and round to 0.001 million. Use the first posted value only; ignore later preliminary, final, and annual-summary revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"November 2024 total participants","value":6.829},{"label":"October 2025 preliminary total participants","value":6.909},{"label":"November 2025 initial total participants","value":6.752}],"drivers":["recent national participation level","month-to-month administrative reporting volatility","WIC eligibility and enrollment conditions","first-print reporting noise"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://www.fns.usda.gov/sites/default/files/resource-files/27wilatest-2.pdf"],"runAt":"2026-07-10T22:05:33Z","thresholdLadder":{"thresholds":[6.7,6.72,6.75,6.78,6.8,6.82,6.84,6.86,6.89,6.92,6.95,6.98,7.02],"cumulativeProbabilities":[0.02,0.04,0.1,0.18,0.28,0.39,0.5,0.61,0.72,0.82,0.9,0.95,0.98]},"reasoning":[{"kind":"heading","text":"USDA FNS WIC total participation: May 2026 first print"},{"kind":"text","text":"The resolver is the national WIC Total Participants series, calendar-month May 2026, using the first official print only. The FNS WIC Data Tables page is the series table page; the published count is converted from persons to millions."},{"kind":"tool","tool":"official.release_calendar","call":"Checked the official FNS release-calendar entry for the May 2026 WIC monthly-program-data posting.","result":"The official schedule lists the May 2026 WIC posting for 2026-08-14, within the stated 2026-08-07 to 2026-08-15 release window."},{"kind":"tool","tool":"official.lookup","call":"Fetched the FNS WIC Latest Month Participation table and read the national TOTAL row.","result":"The FNS table reports TOTAL participation of 6,829,321 in November 2024, 6,909,050 for October 2025 preliminary, and 6,752,138 for November 2025 initial."},{"kind":"tool","tool":"official.compare","call":"Fetched the national-row comparison columns in the FNS WIC Latest Month Participation table.","result":"The table reports November 2025 initial participation of 6,752,138, a -2.3% change from October 2025's 6,909,050 and a -1.1% change from November 2024's 6,829,321."},{"kind":"tool","tool":"official.table_metadata","call":"Fetched the FNS WIC Data Tables page to identify the published monthly national and latest-month table classes.","result":"FNS lists Monthly Data - National Level for FY 2022 through November 2025 and identifies the latest state-level month as November 2025; the associated latest-month total is 6,752,138 participants."},{"kind":"text","text":"Base rate/reference class: recent official national totals span 6.752 to 6.909 million, with the 6.829 million November 2024 reading providing a level anchor. These are the same total-participants variant as the resolver, not annual WIC quality-control data or a smoothed series."},{"kind":"text","text":"Prior/update/interval: I use a persistence prior centered near the recent 6.83 million reference-class level, anchored by fetched November 2024 6.829, October 2025 6.909, and November 2025 initial 6.752 million. I adjust modestly upward from the depressed initial November print for ordinary seasonal/enrollment recovery, retain reporting-volatility uncertainty, and use the elicited threshold ladder rather than a parametric interval; its rung span is anchored in those fetched values."},{"kind":"math","text":"Ladder: P(X <= 6.70) = 0.02; P(X <= 6.72) = 0.04; P(X <= 6.75) = 0.10; P(X <= 6.78) = 0.18; P(X <= 6.80) = 0.28; P(X <= 6.82) = 0.39; P(X <= 6.84) = 0.50; P(X <= 6.86) = 0.61; P(X <= 6.89) = 0.72; P(X <= 6.92) = 0.82; P(X <= 6.95) = 0.90; P(X <= 6.98) = 0.95; P(X <= 7.02) = 0.98. Linear interpolation gives 10th percentile at 6.75, median at 6.84, and 90th percentile at 6.95 million."},{"kind":"text","text":"Upside risk: stronger enrollment or a rebound after the low November initial print could lift May above 6.95 million. Downside risk: continued enrollment attrition or unusually low state reporting could push it below 6.75 million. A broad administrative disruption or an unusually large reporting discontinuity would land outside the interval."},{"kind":"forecast","point":6.84,"ciLow":6.75,"ciHigh":6.95}]}
