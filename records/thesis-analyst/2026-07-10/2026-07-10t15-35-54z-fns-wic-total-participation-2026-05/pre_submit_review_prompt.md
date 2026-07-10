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
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC total participants, May 2026","question":"USDA FNS national WIC Total Participants for calendar May 2026, unadjusted monthly administrative count, first print","unit":"millions","pointEstimate":6.98,"ciLow":6.913,"ciHigh":7.047,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-2.pdf","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Convert the displayed whole-person count to millions by dividing by 1,000,000 and round to 0.001 million. Use the first posted May 2026 value only; ignore later preliminary, final, or annual-summary revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"May 2023 official total participants","value":6.697},{"label":"May 2024 official total participants","value":6.764},{"label":"May 2025 official total participants","value":6.895},{"label":"November 2025 official total participants","value":6.752}],"drivers":["year-over-year participation growth through May 2025","normal spring rise from winter participation levels","slower late-2025 comparable participation level","calendar-month, unadjusted administrative reporting"],"sourceContext":["https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-2.pdf","https://www.fns.usda.gov/pd/overview"],"runAt":"2026-07-10T00:00:00Z","reasoning":[{"kind":"heading","text":"US WIC May 2026 total participation forecast"},{"kind":"text","text":"The target is the FNS monthly national Total Participants series, a calendar-month unadjusted administrative count. The resolver uses the first official May 2026 print, converts persons to millions, and the FNS release calendar specifies the August 14, 2026 release date; no revision or later annual-summary value is eligible."},{"kind":"tool","tool":"official.lookup","call":"Fetched the official FNS WIC monthly table, series table 37wic-monthly.","result":"The official table reports Total Participants of 6,696,739 in May 2023, 6,763,710 in May 2024, and 6,894,610 in May 2025; these equal 6.697, 6.764, and 6.895 million."},{"kind":"tool","tool":"official.lookup","call":"Fetched the later portion of the same official FNS monthly table for the latest available FY 2026 comparable observations.","result":"The table reports 6,909,050 total participants in October 2025 and 6,752,138 in November 2025, versus 6,907,747 and 6,829,321 in October and November 2024."},{"kind":"tool","tool":"official.lookup","call":"Fetched the official FNS Program Data Overview and annual totals for reference-class context.","result":"FNS reports FY 2023 average total participants of 6,575,977, FY 2024 of 6,704,329, and FY 2025 of 6,866,095; the overview states that current numbers are preliminary and subject to revision."},{"kind":"text","text":"The base rate is continued growth in the same official monthly reference class: May increased 0.067 million from 2023 to 2024 and 0.131 million from 2024 to 2025. The level effect is the 6.895 million May 2025 anchor; momentum supports another increase, while the softer November 2025 year-over-year comparison restrains extrapolation. There is no seasonal-adjustment variant: every anchor is the same unadjusted national Total Participants table."},{"kind":"math","text":"Prior/update/interval: Persistence-plus-year-over-year-growth prior uses the May 2025 level of 6.895 million and a restrained +0.085 million update from prior May growth, partially offset by the November comparable slowdown, giving 6.980 million. From the official monthly level history, successive monthly changes have sigma = 0.052 million; 1.28*sigma = 0.067 million. The 80% half-width is 0.067 million, so implied bounds are 6.980 - 0.067 = 6.913 and 6.980 + 0.067 = 7.047 million."},{"kind":"text","text":"upside risk is a renewed participation acceleration from improved access or enrollment, which could put May above 7.047 million. downside risk is a broader continuation of the late-2025 comparable weakness, which could put May below 6.913 million. A policy or reporting disruption large enough to move the print outside the interval would falsify the persistence-and-momentum model."},{"kind":"forecast","point":6.98,"ciLow":6.913,"ciHigh":7.047}]}
