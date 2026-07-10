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
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC participation, May 2026","question":"USDA FNS WIC national Total Participants for May 2026, first official monthly program-data print, converted from persons to millions","unit":"millions","pointEstimate":6.79,"ciLow":6.583,"ciHigh":7.01,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Use the whole participant count displayed by FNS, divide by 1,000,000, and round to 0.001 million. Use the first posted May 2026 value only; ignore later preliminary, final, annual-summary, or other revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"Nov 2024 latest-month comparison","value":6.829321},{"label":"Oct 2025 preliminary","value":6.90905},{"label":"Nov 2025 initial","value":6.752138},{"label":"May 2025 same-month anchor","value":6.89461}],"drivers":["Nov 2025 initial print was 1.1% below Nov 2024","May 2025 same-month anchor was 6.895 million participants","monthly first prints can move sharply because latest-month state reporting is preliminary","WIC eligibility and infant/child population trends point to mild drift rather than a regime jump","possible FY2026 funding or administrative disruption widens downside risk"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://www.fns.usda.gov/sites/default/files/resource-files/27wilatest-2.pdf","https://www.fns.usda.gov/data-release-calendar"],"runAt":"2026-07-10T00:00:00Z","thresholdLadder":{"thresholds":[6.5,6.6,6.65,6.7,6.75,6.8,6.85,6.9,6.95,7,7.05,7.15],"cumulativeProbabilities":[0.05,0.11,0.18,0.3,0.42,0.52,0.63,0.73,0.82,0.89,0.94,0.98]},"reasoning":[{"kind":"heading","text":"USDA FNS WIC total participation, May 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the national USDA FNS WIC Total Participants monthly table value for May 2026, not annual fiscal-year WIC participation and not a quality-control release. The target unit is millions, so the FNS person count is divided by 1,000,000 and rounded to 0.001 million. I keep the strict first-print policy and do not add a same-day correction or revision grace rule."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA FNS WIC Data Tables page and checked the available monthly materials and page metadata.","result":"FNS WIC Data Tables listed Monthly Data - National Level FY 2022 through November 2025, Monthly Data - State Level Participation FY 2026 preliminary, Latest Available Month materials, and page updated February 24, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA FNS WIC Latest Month Participation PDF for the latest national first-print/state-level reference point.","result":"The latest-month PDF showed TOTAL participation of 6,829,321 for November 2024, 6,909,050 for October 2025 preliminary, and 6,752,138 for November 2025 initial."},{"kind":"tool","tool":"official.lookup","call":"Checked the official FNS data-release calendar for the registered May 2026 WIC monthly-data release date and cross-checked the WIC series page.","result":"The target contract's official-calendar release date is 2026-08-14 for May 2026 WIC monthly data; the same FNS WIC series page currently exposes November 2025 as the latest month and 6,752,138 as the latest initial TOTAL reference value."},{"kind":"tool","tool":"official.lookup","call":"Used the ledger-provided official-source same-month anchor from the FNS monthly table example for May 2025.","result":"The May 2025 WIC Total Participants example is 6,894,610 persons, equal to 6.894610 million after dividing by 1,000,000."},{"kind":"text","text":"Reference class and base rate: the most relevant reference class is recent national WIC monthly first prints on the same FNS WIC table. The Nov 2025 initial count was 1.1% below Nov 2024, while May 2025 was 6.895 million; applying roughly the recent year-over-year softness to the May seasonal anchor gives an outside-view base rate near 6.82 million before current-policy adjustments."},{"kind":"text","text":"Level, momentum, and mechanism: the level anchor is May 2025 at 6.895 million, the latest observed initial level is lower at 6.752 million in November 2025, and the six-month seasonal path from November to May is usually not a large structural break. I make a modest downward update for reported year-over-year softness and administrative/funding uncertainty, partly offset by normal eligibility continuity and the tendency for WIC caseloads to be sticky month to month."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2025 same-month value of 6.894610 million; historical sample = fetched FNS latest-month totals of 6.829321 million for Nov 2024, 6.909050 million for Oct 2025 preliminary, and 6.752138 million for Nov 2025 initial; adjustment components = about -0.075 million for recent year-over-year softness, -0.020 million for funding/administrative risk, and -0.010 million for first-print noise/momentum, implying a center near 6.79 million. The interval method is the threshold ladder below, with rung span anchored by the fetched 6.752138 latest initial, 6.909050 prior-month preliminary, and 6.894610 May same-month values plus allowance for first-print and policy disruption."},{"kind":"math","text":"Ladder: P(X <= 6.500) = 0.05; P(X <= 6.600) = 0.11; P(X <= 6.650) = 0.18; P(X <= 6.700) = 0.30; P(X <= 6.750) = 0.42; P(X <= 6.800) = 0.52; P(X <= 6.850) = 0.63; P(X <= 6.900) = 0.73; P(X <= 6.950) = 0.82; P(X <= 7.000) = 0.89; P(X <= 7.050) = 0.94; P(X <= 7.150) = 0.98. Linear interpolation gives 10th percentile at 6.583, median at 6.790, and 90th percentile at 7.010."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in certification or state reporting that puts May 2026 back near or above 7.05 million, which would land above the interval. Downside risk is a funding, enrollment, or administrative shock that keeps caseload near 6.5 million or below; that would land outside the interval on the low side."},{"kind":"forecast","point":6.79,"ciLow":6.583,"ciHigh":7.01}]}
