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
4c4eb9fec241655f9e048f127ca41a35afc0cbde3c602de7cfa70b292d69ac9d

# Draft forecast response
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC total participation, May 2026","question":"What will USDA FNS first report for national WIC Total Participants in May 2026, in millions of participants?","unit":"millions","pointEstimate":6.85,"ciLow":6.73,"ciHigh":6.97,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Convert the displayed whole participant count to millions by dividing by 1,000,000 and round to 0.001 million. Use the first posted May 2026 value only; ignore later preliminary, final, or annual-summary revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"FY 2025 annual average total participants","value":6.866},{"label":"May 2025 total participants","value":6.895},{"label":"October 2025 preliminary total participants","value":6.909},{"label":"November 2025 initial total participants","value":6.752},{"label":"May 2024 total participants","value":6.764}],"drivers":["Recent WIC participation was near 6.8-6.9 million before the November 2025 initial drop","May normally sits above winter participation in the recent official monthly reference class","First-print risk is larger than final-vintage trend risk because November 2025 initial data showed a large one-month fall","No variant adjustment: all anchors use USDA FNS national monthly WIC Total Participants, not annual summaries for resolution"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-2.pdf","https://www.fns.usda.gov/sites/default/files/resource-files/27wilatest-2.pdf"],"runAt":"2026-07-10T16:16:18Z","thresholdLadder":{"thresholds":[6.64,6.68,6.71,6.73,6.76,6.79,6.82,6.85,6.88,6.91,6.94,6.97,7.01],"cumulativeProbabilities":[0.03,0.06,0.085,0.1,0.17,0.27,0.39,0.5,0.62,0.73,0.83,0.9,0.96]},"reasoning":[{"kind":"heading","text":"US WIC May 2026 total participation forecast"},{"kind":"text","text":"Framing and exact resolver: this is the USDA FNS national monthly WIC Total Participants series for May 2026, first official print only, converted from whole persons to millions. I use the WIC Data Tables page and the national monthly WIC Participation and Costs table for the same national monthly variant; annual summaries are context only, not the resolution vintage."},{"kind":"tool","tool":"official.lookup","call":"Open USDA FNS WIC Data Tables page and identify the official monthly WIC data materials and latest-month materials.","result":"The WIC Data Tables page lists Monthly Data - National Level FY 2022 through November 2025 and Latest Available Month materials; page updated February 24, 2026, with FY 2026 preliminary data available."},{"kind":"tool","tool":"official.lookup","call":"Read USDA FNS national monthly WIC Participation and Costs PDF, data as of February 13, 2026.","result":"Fetched national total participants: May 2023 = 6,696,739; May 2024 = 6,763,710; May 2025 = 6,894,610; FY 2025 annual average = 6,866,095; October 2025 = 6,909,050; November 2025 = 6,752,138."},{"kind":"tool","tool":"official.lookup","call":"Read USDA FNS latest-month WIC Total Participation PDF for state-level cross-check of latest national total.","result":"Fetched latest-month national TOTAL row: November 2024 = 6,829,321; October 2025 preliminary = 6,909,050; November 2025 initial = 6,752,138; month-to-month change = -2.3%; year-over-year change = -1.1%."},{"kind":"text","text":"Reference class and base rate: recent same-variant May totals rose from 6.697 million in May 2023 to 6.764 million in May 2024 to 6.895 million in May 2025, but the latest first-print official observation, November 2025 at 6.752 million, was 1.1% below November 2024. A simple base rate is therefore May 2025 adjusted down roughly 0.5%-1.0%, with partial recovery from the low November initial print."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2025 level of 6.895 million, historical sample = monthly USDA FNS national WIC totals from Oct 2022 through Nov 2025, adjustment components = -0.060 million for weaker latest year-over-year level, +0.015 million for typical winter-to-May seasonal lift after a low initial November, giving 6.850 million. Using successive monthly changes from the fetched history, sigma = 0.054 million, so 1.28*sigma = 0.069 million. I widen to a ladder-implied 80% half-width of 0.120 million, 1.74x the one-step half-width, because the target is six months beyond the latest available first print and November 2025 showed an unusually large -0.157 million one-month change."},{"kind":"math","text":"Ladder: P(X <= 6.640) = 0.03; P(X <= 6.680) = 0.06; P(X <= 6.710) = 0.085; P(X <= 6.730) = 0.10; P(X <= 6.760) = 0.17; P(X <= 6.790) = 0.27; P(X <= 6.820) = 0.39; P(X <= 6.850) = 0.50; P(X <= 6.880) = 0.62; P(X <= 6.910) = 0.73; P(X <= 6.940) = 0.83; P(X <= 6.970) = 0.90; P(X <= 7.010) = 0.96. Linear interpolation gives the 10th percentile 6.730, median 6.850, and 90th percentile 6.970 million."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound from the unusually low November 2025 initial print plus normal spring enrollment strength, which would land above the interval if May 2026 prints above 6.970 million. Downside risk is that the November drop reflects a durable eligibility, outreach, or reporting decline; a continuation below roughly 6.730 million would land outside the interval on the low side."},{"kind":"forecast","point":6.85,"ciLow":6.73,"ciHigh":6.97}]}
