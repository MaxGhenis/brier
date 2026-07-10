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
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC total participants, May 2026","question":"USDA FNS national WIC Total Participants for calendar May 2026, unadjusted monthly administrative count, first print","unit":"millions","pointEstimate":6.98,"ciLow":6.913,"ciHigh":7.047,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-2.pdf","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Convert the displayed whole-person count to millions by dividing by 1,000,000 and round to 0.001 million. Use the first posted May 2026 value only; ignore later preliminary, final, or annual-summary revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"May 2023 official total participants","value":6.697},{"label":"May 2024 official total participants","value":6.764},{"label":"May 2025 official total participants","value":6.895},{"label":"November 2025 official total participants","value":6.752}],"drivers":["year-over-year participation growth through May 2025","normal spring rise from winter participation levels","slower late-2025 comparable participation level","calendar-month, unadjusted administrative reporting"],"sourceContext":["https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-2.pdf","https://www.fns.usda.gov/pd/overview"],"runAt":"2026-07-10T00:00:00Z","reasoning":[{"kind":"heading","text":"US WIC May 2026 total participation forecast"},{"kind":"text","text":"The target is the FNS monthly national Total Participants series, a calendar-month unadjusted administrative count. The resolver uses the first official May 2026 print, converts persons to millions, and the FNS release calendar specifies the August 14, 2026 release date; no revision or later annual-summary value is eligible."},{"kind":"tool","tool":"official.lookup","call":"Fetched the official FNS WIC monthly table, series table 37wic-monthly.","result":"The official table reports Total Participants of 6,696,739 in May 2023, 6,763,710 in May 2024, and 6,894,610 in May 2025; these equal 6.697, 6.764, and 6.895 million."},{"kind":"tool","tool":"official.lookup","call":"Fetched the later portion of the same official FNS monthly table for the latest available FY 2026 comparable observations.","result":"The table reports 6,909,050 total participants in October 2025 and 6,752,138 in November 2025, versus 6,907,747 and 6,829,321 in October and November 2024."},{"kind":"tool","tool":"official.lookup","call":"Fetched the official FNS Program Data Overview and annual totals for reference-class context.","result":"FNS reports FY 2023 average total participants of 6,575,977, FY 2024 of 6,704,329, and FY 2025 of 6,866,095; the overview states that current numbers are preliminary and subject to revision."},{"kind":"text","text":"The base rate is continued growth in the same official monthly reference class: May increased 0.067 million from 2023 to 2024 and 0.131 million from 2024 to 2025. The level effect is the 6.895 million May 2025 anchor; momentum supports another increase, while the softer November 2025 year-over-year comparison restrains extrapolation. There is no seasonal-adjustment variant: every anchor is the same unadjusted national Total Participants table."},{"kind":"math","text":"Prior/update/interval: Persistence-plus-year-over-year-growth prior uses the May 2025 level of 6.895 million and a restrained +0.085 million update from prior May growth, partially offset by the November comparable slowdown, giving 6.980 million. From the official monthly level history, successive monthly changes have sigma = 0.052 million; 1.28*sigma = 0.067 million. The 80% half-width is 0.067 million, so implied bounds are 6.980 - 0.067 = 6.913 and 6.980 + 0.067 = 7.047 million."},{"kind":"text","text":"upside risk is a renewed participation acceleration from improved access or enrollment, which could put May above 7.047 million. downside risk is a broader continuation of the late-2025 comparable weakness, which could put May below 6.913 million. A policy or reporting disruption large enough to move the print outside the interval would falsify the persistence-and-momentum model."},{"kind":"forecast","point":6.98,"ciLow":6.913,"ciHigh":7.047}]}

# Reviewer critique
{"summary":"The forecast is methodologically coherent, but its resolver source URL conflicts with the ledger’s bound official source and its interval provenance needs to be more explicit.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft sets resolutionSourceUrl to an Azure Edge PDF host, while the canonical target binds resolution to https://www.fns.usda.gov/pd/wic-program with allowed host www.fns.usda.gov.","actionRequested":"Set the forecast resolutionSourceUrl to the canonical FNS WIC Program page and retain the first-posted-May-2026 rule; cite an official calendar or release placeholder supporting August 14 if available."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The interval cites a monthly-change sigma of 0.052 million but does not identify the historical window, number of changes, or treatment of revisions used to calculate it.","actionRequested":"Name the exact first-print monthly sample and observation count used for sigma, and state that the calculation uses the target’s unadjusted persons-to-millions series."}],"optionalSuggestions":["Make the upside and downside scenarios more operational by naming a concrete WIC enrollment/access or reporting mechanism and the size of movement needed to breach each bound."]}

Emit the final JSON object only.
