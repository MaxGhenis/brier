# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fns.wic.total_participation
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "wic-participation-june-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "fns.wic.total_participation.2026-06.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-09-18", "start": "2026-09-10"}, "field": "fns.wic.total_participation", "releasePolicy": "first_print", "sourceSeriesId": "fns.wic.total_participation", "sourceUrl": "https://www.fns.usda.gov/pd/wic-program", "table": "Official agency release", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-de8d99ce467a695f4b235a8da2d9fb8973d60a0cd95e9791f53dc8f3e7bb81fb.json"
- targetContentHash: "de8d99ce467a695f4b235a8da2d9fb8973d60a0cd95e9791f53dc8f3e7bb81fb"
- registrationCommit: "79e7796ea8cde8d3c263a226250346d3aa2c88d9"
- registeredAtUtc: "2026-07-10T17:47:41Z"

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
{"slug":"wic-participation-june-2026","country":"US","type":"data","title":"US WIC Participation, June 2026","question":"What will USDA FNA report as total WIC participation for June 2026, in millions, in the first official print?","unit":"millions","pointEstimate":6.75,"ciLow":6.686,"ciHigh":6.814,"confidence":0.8,"resolutionDate":"2026-09-18","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the total participants value for June 2026 in the first official USDA FNA WIC monthly national-level table published on the WIC Data Tables page, multiplied by 0.001 to convert thousands to millions. Use that first print without incorporating later revisions or corrections, and round only the resolved millions value to six decimal places.","dataPointId":"fns.wic.total_participation.2026-06.first_print","historicalContext":[{"label":"December 2025","value":6.712611},{"label":"January 2026","value":6.6963},{"label":"February 2026","value":6.66458},{"label":"March 2026","value":6.701661},{"label":"June 2025","value":6.8832}],"drivers":["recent March rebound after winter declines","typical March-to-June seasonal increase","lower FY2026 participation level than FY2025","preliminary reporting volatility"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-6.pdf","https://www.fns.usda.gov/pd/overview","https://www.fns.usda.gov/pd/data-release-schedule"],"runAt":"2026-07-10T17:49:31Z","reasoning":[{"kind":"heading","text":"June 2026 WIC participation forecast"},{"kind":"text","text":"The target is national total WIC participants for June 2026, not an annual fiscal-year measure or a participant-category subtotal. It resolves from the first official monthly national-level print. The official release calendar schedules this target for 2026-09-18; the ledger window of 2026-09-10 through 2026-09-18 is consistent with that date."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest USDA FNA WIC monthly national-level table and read total participants for December 2025 through March 2026.","result":"The official table reports 6,712,611 participants in Dec 2025, 6,696,300 in Jan 2026, 6,664,580 in Feb 2026, and 6,701,661 in Mar 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetch same-variant historical March and June national total-participation observations from the official WIC monthly table.","result":"Total participants were 6,621,311 in Mar 2023 and 6,732,424 in Jun 2023; 6,680,974 in Mar 2024 and 6,736,885 in Jun 2024; 6,850,836 in Mar 2025 and 6,883,200 in Jun 2025."},{"kind":"tool","tool":"official.lookup","call":"Fetch the recent FY2026 level transition from the official national monthly WIC table.","result":"Total participation fell from 6,909,938 in Oct 2025 to 6,771,734 in Nov 2025 and 6,712,611 in Dec 2025 before reaching 6,701,661 in Mar 2026."},{"kind":"text","text":"The reference class is the three prior March-to-June changes in the same official total-participation series: +0.111113 million in 2023, +0.055911 million in 2024, and +0.032364 million in 2025. Their base-rate mean is +0.066463 million."},{"kind":"text","text":"Level is anchored at March's 6.701661 million. Momentum improved in March by 0.037081 million after four monthly declines, while the one-off October-to-November drop and continued lower FY2026 level argue against applying the full seasonal base rate. Policy mechanisms such as eligibility-guideline and food-package changes are unlikely to reverse the level break fully by June."},{"kind":"math","text":"Prior/update/interval: persistence-plus-seasonality prior using the official Oct 2024-Mar 2026 monthly history; historical sample is the 13 successive changes from Mar 2025 through Mar 2026. The mean prior adds the three-year March-to-June base rate of 0.066463 million to 6.701661, then applies a -0.018124 million momentum/policy-level adjustment: 6.701661 + 0.066463 - 0.018124 = 6.750000. The sample dispersion of those successive monthly changes gives sigma = 0.050 million, so the 80% half-width is approximately 1.28*sigma = 1.28*0.050 = 0.064 million, implying bounds 6.750-0.064=6.686 and 6.750+0.064=6.814."},{"kind":"text","text":"Upside risk comes from a stronger normal spring enrollment rebound and would land above the interval if participation exceeds 6.814 million. Downside risk comes from renewed attrition comparable to the late-2025 decline and would land below the interval if participation falls under 6.686 million. These are the concrete outside-the-interval scenarios."},{"kind":"forecast","point":6.75,"ciLow":6.686,"ciHigh":6.814}]}

# Reviewer critique
{
  "summary": "Draft is mostly publication-ready, but the interval-method description has a concrete sample-count inconsistency and the inside-view adjustment needs a more explicit basis.",
  "requiredFixes": [
    {
      "rubricItem": "interval",
      "severity": "blocking",
      "summary": "The interval says it uses 13 successive monthly changes from Mar 2025 through Mar 2026, but that endpoint span implies 12 month-to-month changes; it also does not explain why one-month volatility is appropriate for a March-to-June target.",
      "actionRequested": "Correct the historical sample definition/count and state whether the 0.050 sigma is for one-month changes, March-to-June changes, or an explicitly scaled three-month horizon."
    },
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "The -0.018124 million momentum/policy-level adjustment is directionally justified but numerically under-specified.",
      "actionRequested": "Break the adjustment into named components or state that it is a judgmental shrinkage from the three-year March-to-June base rate, with the reason for the approximate size."
    },
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The question text says USDA FNA, while the canonical agency/source is USDA FNS.",
      "actionRequested": "Change USDA FNA to USDA FNS in display text while keeping the same slug, source URL, dataPointId, first-print rule, and 2026-09-18 resolution date."
    }
  ],
  "optionalSuggestions": [
    "State the implied prior before adjustment as 6.768124 million to make the update step easier to audit.",
    "Mention that the unit conversion is from participants in thousands to millions under the ledger transform factor 0.001.",
    "Consider adding one concrete downside example tied to the late-2025 monthly drop magnitude rather than only naming renewed attrition."
  ]
}

Emit the final JSON object only.
