# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: eurostat.construction.production_index
- period: 2026-05
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "euro-area-construction-production-index-may-2026"
- country: "EA"
- targetUnit: "index_points"
- dataPointId: "eurostat.construction.production_index.2026_05.first_print"
- resolutionSourceUrl: "https://ec.europa.eu/eurostat/databrowser/view/sts_copr_m/default/table?lang=en"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["ec.europa.eu"], "expectedReleaseWindow": {"end": "2026-07-20", "start": "2026-07-20"}, "field": "freq=M, unit=I21, s_adj=SCA, indic_bt=PRD, nace_r2=F, geo=EA20", "releasePolicy": "first_print", "sourceSeriesId": "sts_copr_m.M.I21.SCA.PRD.F.EA20", "sourceUrl": "https://ec.europa.eu/eurostat/databrowser/view/sts_copr_m/default/table?lang=en", "table": "sts_copr_m: Production in construction - monthly data", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-11-88e510f907520fe3734008853e5f0f83c6b6296c6f9c0dd7d76a6a9c8f0bee49.json"
- targetContentHash: "88e510f907520fe3734008853e5f0f83c6b6296c6f9c0dd7d76a6a9c8f0bee49"
- registrationCommit: "357f4e8477327d91775a345ece531f3eb42fa3b7"
- registeredAtUtc: "2026-07-11T18:10:24Z"

# Source hints
- Use Eurostat euro-indicators release calendar and official HICP/IP pages.
- Euro-area HICP rates print to one decimal.
- Resolution source should be the Eurostat release/data page.

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
{"slug":"euro-area-construction-production-index-may-2026","country":"EA","type":"data","title":"Euro-area construction production, May 2026","question":"What will Eurostat first report for the May 2026 euro-area production-in-construction index, calendar and seasonally adjusted, 2021=100, series sts_copr_m.M.I21.SCA.PRD.F.EA20?","unit":"index_points","pointEstimate":105.7,"ciLow":104.4,"ciHigh":107.1,"confidence":0.8,"resolutionDate":"2026-07-20","resolutionSource":"Eurostat Production in construction release and sts_copr_m data table","resolutionSourceUrl":"https://ec.europa.eu/eurostat/databrowser/view/sts_copr_m/default/table?lang=en","resolutionRule":"Resolve to the first value Eurostat publishes on 20 July 2026 for May 2026 in sts_copr_m, series freq=M, unit=I21, s_adj=SCA, indic_bt=PRD, nace_r2=F, geo=EA20. Use the calendar-and-seasonally-adjusted production-in-construction index, 2021=100, as printed to one decimal. Do not substitute monthly growth, calendar-adjusted data, EU data, or a later revision. The ledger unit is index_points, although that value is absent from the prompt's enumerated unit examples.","dataPointId":"eurostat.construction.production_index.2026_05.first_print","historicalContext":[{"label":"November 2025","value":104.3},{"label":"December 2025","value":104.6},{"label":"January 2026","value":103.6},{"label":"February 2026","value":103.1},{"label":"March 2026","value":104.9},{"label":"April 2026","value":105.5}],"drivers":["April level of 105.5 index points","six-month mean monthly change of 0.24 points","March-April rebound after January-February weakness","weak buildings but stronger civil engineering and specialised construction"],"sourceContext":["https://ec.europa.eu/eurostat/web/products-euro-indicators/w/4-18062026-ap","https://ec.europa.eu/eurostat/web/main/news/euro-indicators/release-calendar","https://ec.europa.eu/eurostat/databrowser/view/sts_copr_m/default/table?lang=en"],"runAt":"2026-07-11T18:16:38Z","reasoning":[{"kind":"heading","text":"Euro-area construction production index for May 2026"},{"kind":"text","text":"The target is Eurostat table sts_copr_m, exact series sts_copr_m.M.I21.SCA.PRD.F.EA20: total construction for EA20, calendar and seasonally adjusted, 2021=100. The resolver is the May 2026 first print, not a growth rate or later revision."},{"kind":"tool","tool":"official.lookup","call":"Read the monthly index table in Eurostat's 18 June 2026 Production in construction release.","result":"Euro-area SCA index values were 104.3 in November 2025, 104.6 in December, 103.6 in January 2026, 103.1 in February, 104.9 in March, and 105.5 in April."},{"kind":"tool","tool":"official.lookup","call":"Read Eurostat's month-on-month total-construction reference class from the same official release.","result":"Euro-area monthly changes from November 2025 through April 2026 were -0.9%, +0.3%, -1.0%, -0.5%, +1.7%, and +0.6%, respectively."},{"kind":"tool","tool":"official.lookup","call":"Read Eurostat's April annual and sector detail to assess the composition of momentum.","result":"April 2026 total construction was 0.9% above April 2025; buildings fell 5.2% year over year, while civil engineering rose 4.4% and specialised construction rose 1.7%."},{"kind":"text","text":"The outside-view base rate is short-run level persistence: the six official index levels fluctuate around 104-105, while the five successive level changes average +0.24 points. Level is therefore anchored at April's 105.5, with only a small positive continuation."},{"kind":"text","text":"Current-release adjustments are approximately net zero beyond the persistence prior: recent momentum is positive, the March-April rebound may partly reverse as a one-off, weak building activity offsets stronger civil engineering and specialised work, and no specific policy mechanism warrants a further adjustment."},{"kind":"text","text":"Eurostat's official release states that the next Production in construction release is 20 July 2026, matching the official Euro-indicators calendar and verifying the ledger resolution date rather than inferring it from monthly cadence."},{"kind":"math","text":"Prior/update/interval: The model is a persistence-plus-mean-change prior using the six November-April official index observations. Successive changes are +0.3, -1.0, -0.5, +1.8, and +0.6 points; their mean is +0.24 and sample sigma = 1.08 points. Starting from 105.5 gives 105.5 + 0.24 = 105.74, rounded to 105.7. The empirical 80% half-width is 1.28*sigma = 1.28*1.08 = 1.38 points, implying 105.74 ± 1.38 = 104.36 to 107.12, rounded to 104.4-107.1."},{"kind":"text","text":"Upside risk comes from another broad rebound like March, which would land above the interval. Downside risk comes from renewed building-sector weakness or reversal of the March-April surge; a monthly fall exceeding roughly 1.1 points would land below the interval. Either outcome would be outside the interval and falsify the central persistence view."},{"kind":"forecast","point":105.7,"ciLow":104.4,"ciHigh":107.1}]}

# Reviewer critique
{"summary":"The draft satisfies the review rubric and is publication-ready, with only minor wording cleanup suggested.","requiredFixes":[],"optionalSuggestions":["Clarify the driver phrase \"six-month mean monthly change\" as \"mean of the five successive Nov-Apr level changes\" to avoid ambiguity.","Consider naming the April 2026 release as the latest available official observation in the reasoning, since the May first print is still pending."]}

Emit the final JSON object only.
