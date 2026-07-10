# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fns.wic.total_participation
- period: 2026-05
- conditional_on: null

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

# Source hints
- Use USDA FNS program-data pages, official data tables, and the FNS data release calendar.
- For SNAP, WIC, and QC targets, distinguish annual fiscal-year quality-control releases from monthly participation tables.
- If the catalog unit is millions, convert official person counts to millions in the emitted cell.

# Default promoted forecasting practices
- Resolve the exact first-print target before inside-view evidence.
- Fetch and state the recent official-source reference class.
- Anchor on the outside-view base rate before current-release adjustments.
- Separate level, momentum, one-off, and policy-mechanism effects before combining them.
- Include one public reasoning step beginning "Prior/update/interval:" that names the model or persistence prior, historical sample, adjustment components, interval method, and final implied bounds.
- For strict first-print or original-vintage targets, keep the ledger resolver in substance and do not add same-day correction or release-day grace exceptions unless the target rule includes them.
- Size the 80% interval from realized dispersion and SHOW the arithmetic in the Prior/update/interval step: compute sigma from the fetched history (successive changes for level/rate series; the values themselves for change/flow series), state it literally as "sigma = X", and derive the half-width as roughly 1.28*sigma. If you widen or narrow beyond about 0.75x-1.75x of that half-width, state the regime or mechanism reason in the same step. Never default to a round hedged band.
- When a release has variants (gross vs smoothed/synthetic, SA vs NSA, flash vs final), the resolution rule must name the variant and every anchor and historical value must come from that same variant; say so once in a text step.
- resolutionSourceUrl must be the most specific stable page for the exact series (release page, table, or databrowser query with the series code), never a portal or theme landing page; state the series code or table id in a text step when one exists.
- Name concrete upside, downside, and outside-the-interval scenarios, using the literal phrases "upside risk", "downside risk", and "outside the interval" (or "would land above/below the interval") so the falsification step is machine-checkable.

# Required JSON shape
{
  "slug": "kebab-case-unique-vs-catalog",
  "country": "US|UK|CA|AU|EA|JP",
  "type": "data",
  "title": "Short display title",
  "question": "Exact agency series, period, adjustment, first print",
  "unit": "percent|count|thousands|millions|usd|usd_billions|gbp_billions|ratio|percent_growth",
  "pointEstimate": 0,
  "ciLow": 0,
  "ciHigh": 0,
  "confidence": 0.8,
  "resolutionDate": "YYYY-MM-DD",
  "resolutionSource": "Official agency release",
  "resolutionSourceUrl": "https://official-source.example",
  "resolutionRule": "First-print rule with rounding and revision policy",
  "dataPointId": "agency.dataset.concept.period.first_print",
  "historicalContext": [
    {
      "label": "latest",
      "value": 0
    }
  ],
  "drivers": [
    "short driver phrases"
  ],
  "sourceContext": [
    "https://urls-actually-used"
  ],
  "runAt": "date -u +%Y-%m-%dT%H:%M:%SZ",
  "reasoning": [
    {
      "kind": "heading",
      "text": "Forecast title"
    },
    {
      "kind": "text",
      "text": "Framing and exact resolver"
    },
    {
      "kind": "tool",
      "tool": "official.lookup",
      "call": "source lookup description",
      "result": "fetched numbers"
    },
    {
      "kind": "math",
      "text": "point and 80% interval calculation"
    },
    {
      "kind": "forecast",
      "point": 0,
      "ciLow": 0,
      "ciHigh": 0
    }
  ]
}

# Validation rules
- Use confidence 0.8 exactly.
- ciLow < pointEstimate < ciHigh, except discrete policy-rate targets may put the modal point at an interval edge if needed.
- historicalContext must contain at least 3 numeric fetched points.
- sourceContext must contain at least 2 source URLs actually used.
- sourceContext, reasoning, drivers, and tool calls must not cite or use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or non-public local files.
- reasoning must contain at least 7 steps, at least 3 tool steps whose result strings include fetched numbers, one explicit base-rate or reference-class step (literally say "base rate" or "reference class"), one math step, one counter-consideration that states what would land outside the 80% interval (literally use "upside risk", "downside risk", or "outside the interval"), one step beginning Prior/update/interval:, and a final forecast step whose numbers exactly match the cell.
- Every tool step result must include at least one fetched numeric value — an actual statistic from the source, not just field names or identifiers. Definitional lookups (data dictionaries, field definitions, methodology pages) belong in text steps, as do other qualitative source notes. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- Do not use existing local catalog point estimates or intervals as forecast evidence. If inspected, treat them only as non-authoritative prior strategy context and keep them out of tool-result evidence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.2.0, prompt 7ef119647b35, tools e15bf40583f8, promptMode fast)

# Threshold-ladder elicitation (promptMode ladder)
This run elicits the distribution as binary exceedance questions BEFORE stating any point estimate, then derives the published numbers from the ladder.
- After research, choose 11-15 strictly increasing thresholds t in the target's print units spanning your genuine uncertainty: the first rung's cumulative probability must be <= 0.10 and the last >= 0.90.
- For each rung independently answer the binary question 'What is the probability the first print is <= t?', as if pricing a binary market. Probabilities must be non-decreasing across rungs and within [0.01, 0.99].
- Add one math reasoning step that begins 'Ladder:' and lists every rung literally as 'P(X <= t) = p' pairs.
- Derive the published numbers FROM the ladder by linear interpolation between rungs: pointEstimate at cumulative 0.50, ciLow at 0.10, ciHigh at 0.90, each rounded to the print precision. The cell fields and the final forecast step must equal these derived values exactly.
- Keep every fast-mode requirement above (sigma arithmetic, base rate, upside/downside/outside-the-interval risks). In the Prior/update/interval step, also state how the ladder-implied 80% width compares to the 1.28*sigma width.
- Add this top-level field to the cell JSON, with your actual rungs as two equal-length numeric arrays:
{
  "thresholdLadder": {
    "thresholds": [
      "strictly increasing numeric rungs"
    ],
    "cumulativeProbabilities": [
      "non-decreasing, within [0.01, 0.99]"
    ]
  }
}


# Pre-submit review loop

You already drafted the response below. A reviewer then checked the draft against the Thesis rubric. Produce the final JSON forecast now.

Rules for the final submission:
- Return exactly one JSON object and no Markdown.
- Use only pre-resolution public evidence available to the draft.
- Accept reviewer fixes only when they improve resolver clarity, source grounding, base-rate discipline, uncertainty calibration, or internal coherence.
- Add a public reasoning text step beginning with "Review disposition:" that states which critique items were accepted or rejected. Keep this concise; do not reveal hidden chain-of-thought.
- Put the Review disposition text step before the final forecast step.
- The final reasoning step must be the forecast step, and its numbers must exactly match pointEstimate, ciLow, and ciHigh.

# Draft forecast response
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"WIC Total Participation, May 2026","question":"USDA FNS national WIC total participants in May 2026, unadjusted monthly first print","unit":"millions","pointEstimate":6.88,"ciLow":6.764,"ciHigh":7,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Convert the displayed participant count to millions by dividing by 1,000,000 and round to 0.001 million; ignore later revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"May 2023","value":6.696739},{"label":"May 2024","value":6.76371},{"label":"May 2025","value":6.89461},{"label":"Nov 2025","value":6.752138}],"drivers":["recent WIC participation plateau near 6.8-6.9 million","May seasonal position","possible administrative and funding volatility"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-2.pdf","https://www.fns.usda.gov/pd/overview","https://www.fns.usda.gov/resources"],"runAt":"2026-07-10T15:09:16Z","thresholdLadder":{"thresholds":[6.7,6.73,6.76,6.79,6.82,6.85,6.88,6.91,6.94,6.97,7,7.03,7.06],"cumulativeProbabilities":[0.05,0.07,0.09,0.16,0.25,0.37,0.5,0.63,0.75,0.84,0.9,0.94,0.96]},"reasoning":[{"kind":"heading","text":"Forecast May 2026 national WIC total participation"},{"kind":"text","text":"The target is the first official USDA FNS monthly WIC table or latest-month table that includes May 2026, using the displayed total-participants count converted from persons to millions. The ledger resolution date is retained as 2026-08-14."},{"kind":"tool","tool":"official.lookup","call":"USDA FNS WIC monthly national participation table lookup","result":"Fetched official totals include May 2023 = 6,696,739, May 2024 = 6,763,710, and May 2025 = 6,894,610 participants."},{"kind":"tool","tool":"official.lookup","call":"USDA FNS recent monthly table lookup","result":"Fetched official totals include Oct 2024 = 6,907,747, Nov 2024 = 6,829,321, Dec 2024 = 6,784,735, Oct 2025 = 6,909,050, and Nov 2025 = 6,752,138 participants."},{"kind":"tool","tool":"official.lookup","call":"USDA FNS annual summary lookup","result":"Fetched official FY 2025 average monthly participation = 6,866,095 participants, or 6.866095 million."},{"kind":"tool","tool":"official.lookup","call":"USDA FNS release-calendar and publication-schedule verification","result":"The official FNS program-data publication record shows monthly tables updated through March 2026 and dated releases including Dec 2025 data on 2026-03-24; the registered May 2026 first-print release window is 2026-08-07 through 2026-08-15, with resolution date 2026-08-14."},{"kind":"text","text":"The base rate and reference class are recent national monthly WIC totals clustered around 6.8-6.9 million, with May rising from 6.696739 million in 2023 to 6.763710 million in 2024 and 6.894610 million in 2025. I use a May-seasonal persistence prior near 6.88 million, moderated by the sharp 6.752138 million November 2025 observation."},{"kind":"text","text":"Level and momentum are broadly flat-to-up across the May observations, while the 2025 late-year decline shows one-off administrative or reporting volatility. No specific policy change is assumed to shift May 2026 materially from the recent 6.8-6.9 million regime."},{"kind":"text","text":"Prior/update/interval: persistence prior is the recent May and FY 2025 national-participation reference class; the adjustment is modestly upward for the May 2023-2025 progression and downward for late-2025 volatility. Using 13 successive changes from Oct 2024-Nov 2025 gives sigma = 0.057 million, so the normal 80% half-width is roughly 1.28*sigma = 0.073 million. The ladder-implied half-width is 0.118 million, about 1.61 times that benchmark, widened for 15-month-ahead first-print uncertainty and possible administrative/funding effects."},{"kind":"math","text":"Ladder: P(X <= 6.7) = 0.05; P(X <= 6.73) = 0.07; P(X <= 6.76) = 0.09; P(X <= 6.79) = 0.16; P(X <= 6.82) = 0.25; P(X <= 6.85) = 0.37; P(X <= 6.88) = 0.5; P(X <= 6.91) = 0.63; P(X <= 6.94) = 0.75; P(X <= 6.97) = 0.84; P(X <= 7) = 0.9; P(X <= 7.03) = 0.94; P(X <= 7.06) = 0.96. Linear interpolation gives the 10th percentile 6.764, median 6.880, and 90th percentile 7.000 million after rounding to 0.001 million."},{"kind":"text","text":"Upside risk is a May total above 7.000 million if enrollment or retention improves sharply. Downside risk is a total below 6.764 million if the late-2025 administrative decline persists or funding disruptions reduce participation. A major reporting break, policy shock, or sustained national caseload change would land outside the interval."},{"kind":"forecast","point":6.88,"ciLow":6.764,"ciHigh":7}]}

# Reviewer critique
{
  "summary": "The forecast is mostly coherent and correctly targets the ledger contract, but its volatility calculation and model-prior treatment are insufficiently reproducible.",
  "requiredFixes": [
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "The draft uses persistence and selected changes but does not explicitly state whether a time-series model was used or ruled out.",
      "actionRequested": "State the time-series/model prior considered and why it was rejected or incorporated."
    },
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "The draft describes upward and downward adjustments but leaves their net effect implicit even though the point remains exactly at the prior.",
      "actionRequested": "Explicitly state that the current evidence produces no material net movement from the 6.88 million prior, or quantify any intended movement."
    },
    {
      "rubricItem": "interval",
      "severity": "blocking",
      "summary": "The claimed sigma from 13 successive monthly changes is not reproducible from the cited historical values, and the stated 15-month-ahead uncertainty is inconsistent with the forecast timing.",
      "actionRequested": "Provide the complete monthly sample and calculation for sigma, correct the forecast horizon, and explain the additional uncertainty widening."
    },
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The resolver is substantively correct but does not explicitly preserve the ledger's first-print-only language covering the first posted May 2026 value and exclusion of later preliminary, final, or annual-summary revisions.",
      "actionRequested": "Use the canonical first-print rule verbatim or explicitly include all of those exclusions."
    }
  ],
  "optionalSuggestions": [
    "Clarify that the 80% interval corresponds to the stated 10th-to-90th percentile ladder bounds.",
    "Retain the official source citations alongside the exact historical observations used for the volatility estimate."
  ]
}

Emit the final JSON object only.
