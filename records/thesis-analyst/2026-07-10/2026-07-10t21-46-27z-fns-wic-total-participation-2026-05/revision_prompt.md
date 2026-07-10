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
- Size the 80% interval by reading it off your elicited threshold ladder, and SHOW the derivation in the 'Ladder:' math step: state the interpolated values literally as '10th percentile at X', 'median at Y', and '90th percentile at Z'. Ground the rung placement in the fetched reference-class history (state which fetched values anchored the rung span in the Prior/update/interval step). Never default to a round hedged band.
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

Emit the final JSON object only. (agent thesis.analyst v2.2.0, prompt 7ef119647b35, tools e15bf40583f8, promptMode ladder_v2)

# Threshold-ladder elicitation (promptMode ladder_v2)
This run elicits the distribution as binary exceedance questions BEFORE stating any point estimate, then derives the published numbers from the ladder.
- After research, choose 11-15 strictly increasing thresholds t in the target's print units spanning your genuine uncertainty: the first rung's cumulative probability must be <= 0.10 and the last >= 0.90.
- For each rung independently answer the binary question 'What is the probability the first print is <= t?', as if pricing a binary market. Probabilities must be non-decreasing across rungs and within [0.01, 0.99].
- Add one math reasoning step that begins 'Ladder:' and lists every rung literally as 'P(X <= t) = p' pairs, then states the interpolated '10th percentile at X', 'median at Y', and '90th percentile at Z' in the same step.
- Derive the published numbers FROM the ladder by linear interpolation between rungs: pointEstimate at cumulative 0.50, ciLow at 0.10, ciHigh at 0.90, each rounded to the print precision. The cell fields and the final forecast step must equal these derived values exactly.
- Keep every other requirement above (base rate, upside/downside/outside-the-interval risks, Prior/update/interval step).
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
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC participation, May 2026","question":"What will USDA FNS first report as national WIC Total Participants for May 2026, in millions of people?","unit":"millions","pointEstimate":6.78,"ciLow":6.65,"ciHigh":6.9,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Divide the displayed whole-person count by 1,000,000 and round to 0.001 million. Use only the first posted value and ignore later preliminary, final, or annual-summary revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"March 2023","value":6.621311},{"label":"May 2023","value":6.696739},{"label":"March 2024","value":6.680974},{"label":"May 2024","value":6.76371},{"label":"March 2025","value":6.850836},{"label":"May 2025","value":6.89461},{"label":"March 2026 preliminary","value":6.701661}],"drivers":["Recent year-over-year participation decline","Typical March-to-May seasonal increase","Children remain the largest participant category","Preliminary-data reporting variation"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-6.pdf","https://fns-prod.azureedge.us/pd/overview"],"runAt":"2026-07-10T21:47:18Z","reasoning":[{"kind":"heading","text":"May 2026 national WIC participation forecast"},{"kind":"text","text":"The target is the first USDA FNS national monthly-table print of Total Participants for May 2026, not an annual average, eligibility estimate, revised value, or state-only measure. The official table has no separate seasonal adjustment. The displayed person count is converted to millions and rounded to 0.001."},{"kind":"tool","tool":"official.lookup","call":"Fetched the USDA WIC national monthly participation table and read recent March and May totals.","result":"Total participation was 6,621,311 in March 2023 and 6,696,739 in May 2023; 6,680,974 in March 2024 and 6,763,710 in May 2024; 6,850,836 in March 2025 and 6,894,610 in May 2025."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest available FY 2026 observations from the USDA WIC national monthly table.","result":"Total participation was 6,696,300 in January 2026, 6,664,580 in February 2026, and 6,701,661 in March 2026; the table says FY 2026 data are preliminary and data are as of June 12, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched category detail for the latest month and annual reference values from the official USDA table.","result":"March 2026 comprised 1,458,253 women, 1,419,036 infants, and 3,824,372 children, totaling 6,701,661. FY 2024 averaged 6,704,329 and FY 2025 averaged 6,867,417 participants."},{"kind":"tool","tool":"official.calendar_lookup","call":"Checked the official program-data schedule associated with the registered release window for the May 2026 posting.","result":"The official expected release window is August 7 through August 15, 2026, with the ledger target dated August 14, 2026; the target therefore resolves on 2026-08-14 rather than on a cadence-inferred date."},{"kind":"text","text":"The reference class is the same-series March-to-May movement: +75,428 in 2023, +82,736 in 2024, and +43,774 in 2025. Its median increase is 75,428. Applying that base rate to March 2026 gives 6,777,089, while the May year-over-year decline implied by that anchor is about 1.7%."},{"kind":"text","text":"Prior/update/interval: The persistence prior is March 2026 participation of 6.701661 million, with the historical sample consisting of the fetched 2023-2025 March-to-May changes. I add the median seasonal change of 0.075428 million, make no separate level adjustment because the latest year-over-year weakness is already embedded in March, and allow for reporting and policy-mechanism uncertainty through the elicited threshold ladder. The ladder interpolation implies final 80% bounds of 6.650 to 6.900 million."},{"kind":"text","text":"An upside risk is a stronger spring enrollment rebound, outreach effect, or delayed state reporting that would push participation toward or above 6.900 million. A downside risk is continued caseload attrition or incomplete first-print state submissions; an unusually broad decline would land below the interval at 6.650 million."},{"kind":"math","text":"Ladder: P(X <= 6.58) = 0.03; P(X <= 6.62) = 0.06; P(X <= 6.65) = 0.10; P(X <= 6.68) = 0.16; P(X <= 6.71) = 0.24; P(X <= 6.74) = 0.34; P(X <= 6.78) = 0.50; P(X <= 6.81) = 0.62; P(X <= 6.84) = 0.73; P(X <= 6.87) = 0.82; P(X <= 6.90) = 0.90; P(X <= 6.94) = 0.95; P(X <= 6.98) = 0.98. Linear interpolation gives the 10th percentile at 6.650, median at 6.780, and 90th percentile at 6.900."},{"kind":"forecast","point":6.78,"ciLow":6.65,"ciHigh":6.9}],"thresholdLadder":{"thresholds":[6.58,6.62,6.65,6.68,6.71,6.74,6.78,6.81,6.84,6.87,6.9,6.94,6.98],"cumulativeProbabilities":[0.03,0.06,0.1,0.16,0.24,0.34,0.5,0.62,0.73,0.82,0.9,0.95,0.98]}}

# Reviewer critique
{"summary":"The resolver and forecast trace are strong, but the model-prior treatment and small point-estimate discrepancy need clarification before publication.","requiredFixes":[{"rubricItem":"model_prior","severity":"blocking","summary":"No time-series or statistical model prior is used or explicitly ruled out.","actionRequested":"State why the short or preliminary series makes a formal model unsuitable, or report the model prior and how it informed the forecast."},{"rubricItem":"coherence","severity":"warning","summary":"The seasonal calculation gives 6.777089 million, while the ladder median and point estimate are 6.780 million without explaining the difference.","actionRequested":"Explain the approximately 0.003 million adjustment or rounding that connects the calculated prior to the final point estimate."}],"optionalSuggestions":["Briefly explain how reporting and policy uncertainty informed the chosen ladder width."]}

Emit the final JSON object only.
