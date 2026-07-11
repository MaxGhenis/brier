# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: statcan.gdp_by_industry.monthly_growth
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "canada-monthly-gdp-growth-july-2026"
- country: "CA"
- targetUnit: "percent_growth"
- dataPointId: "statcan.36-10-0434-01.all_industries.month_to_month_percent_change.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-10-02", "start": "2026-09-24"}, "field": "v65201210", "releasePolicy": "first_print", "sourceSeriesId": "v65201210", "sourceUrl": "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange?vectorIds=65201210", "table": "Statistics Canada Table 36-10-0434-01, all industries, chained 2017 dollars SA at annual rates; MoM percent change computed from levels at the release vintage", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-11-53b3ddc1394061e51a22b42a373fc001da9ea7198bee88023eba70524e8fb945.json"
- targetContentHash: "53b3ddc1394061e51a22b42a373fc001da9ea7198bee88023eba70524e8fb945"
- registrationCommit: "464d182153273b99932d1049c8c2b2039b6a9eba"
- registeredAtUtc: "2026-07-11T01:30:29Z"

# Source hints
- Use Statistics Canada The Daily and release schedule.
- Canada CPI annual rates print to one decimal.
- Resolution source should be the Statistics Canada release/table.

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
{"slug":"canada-monthly-gdp-growth-july-2026","country":"CA","type":"data","title":"Canada monthly GDP growth, July 2026","question":"What will Statistics Canada first report for the July 2026 month-over-month percent change in real GDP by industry at basic prices, all industries, chained 2017 dollars, seasonally adjusted at annual rates?","unit":"percent_growth","pointEstimate":0.1,"ciLow":-0.26,"ciHigh":0.46,"confidence":0.8,"resolutionDate":"2026-09-29","resolutionSource":"Statistics Canada Table 36-10-0434-01","resolutionSourceUrl":"https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange?vectorIds=65201210","resolutionRule":"Resolve to the first Statistics Canada print for July 2026 using vector v65201210 in Table 36-10-0434-01, all industries, chained 2017 dollars, seasonally adjusted at annual rates. Compute the month-over-month percent change from the June and July levels at that release vintage; retain the computed value without substituting later revisions.","dataPointId":"statcan.36-10-0434-01.all_industries.month_to_month_percent_change.2026-07.first_print","historicalContext":[{"label":"2025-07 MoM","value":0.6},{"label":"2025-08 MoM","value":-0.1},{"label":"2025-09 MoM","value":0.2},{"label":"2025-10 MoM","value":-0.3},{"label":"2025-11 MoM","value":0},{"label":"2025-12 MoM","value":0.2},{"label":"2026-01 MoM","value":0},{"label":"2026-02 MoM","value":0.2},{"label":"2026-03 MoM","value":-0.1},{"label":"2026-04 MoM","value":0.5}],"drivers":["recent monthly-growth base rate near 0.1%","services-sector persistence","volatile mining and oil production","manufacturing and trade uncertainty","one-off maintenance and labour disruptions"],"sourceContext":["https://www150.statcan.gc.ca/n1/daily-quotidien/260630/dq260630a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260529/dq260529b-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260227/t001b-eng.htm","https://www150.statcan.gc.ca/n1/release-diffusion/2026-eng.pdf","https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorByReferencePeriodRange?vectorIds=65201210"],"runAt":"2026-07-11T01:31:50Z","reasoning":[{"kind":"heading","text":"Canada real GDP by industry, July 2026 first print"},{"kind":"text","text":"The target is the July 2026 month-over-month change in Statistics Canada vector v65201210, Table 36-10-0434-01: all industries, chained 2017 dollars, seasonally adjusted at annual rates. It resolves from the first release vintage, not a later revision."},{"kind":"tool","tool":"official.lookup","call":"Inspect Statistics Canada's 2026–2027 official release calendar for GDP by industry.","result":"The calendar lists September 29, 2026 as the release date for the July 2026 reference period; it also lists August 28 for June and October 30 for August."},{"kind":"tool","tool":"official.lookup","call":"Inspect Statistics Canada's December 2025 GDP release table for the recent official reference class.","result":"Official all-industries monthly changes for July–December 2025 were 0.6%, -0.1%, 0.2%, -0.3%, 0.0%, and 0.2%, respectively."},{"kind":"tool","tool":"official.lookup","call":"Inspect Statistics Canada's March and April 2026 GDP by industry releases.","result":"The official monthly changes were February +0.2%, March -0.1%, and April +0.5%; the June 30 release also gave a preliminary May advance estimate of +0.1%."},{"kind":"text","text":"The reference class is the ten official monthly observations from July 2025 through April 2026: 0.6, -0.1, 0.2, -0.3, 0.0, 0.2, 0.0, 0.2, -0.1, and 0.5 percent. Their mean is 0.12%, providing the base rate before release-specific adjustments."},{"kind":"text","text":"Level and momentum effects are mildly positive: the April rebound was broad and the preliminary May signal was +0.1%. One-off effects from energy maintenance and labour disruptions can reverse quickly. Policy and trade uncertainty restrain manufacturing, while steady services activity supports growth."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate model; historical sample = the 10 July 2025–April 2026 monthly growth values. Their mean is 0.12%. Adjustments are -0.01 point for fading April energy/reopening strength, -0.02 for manufacturing and trade uncertainty, and +0.01 for services persistence, giving 0.10%. For this change series, dispersion is computed from the values themselves: sample variance = 0.696/9 = 0.0773, so sigma = 0.278%. The normal 80% half-width is 1.28*sigma = 1.28*0.278 = 0.356%, implying 0.10 ± 0.356 = [-0.256%, 0.456%], reported as [-0.26%, 0.46%]."},{"kind":"text","text":"Upside risk comes from a synchronized oil, mining, manufacturing, and services expansion; growth above 0.46% would land outside the interval. Downside risk comes from shutdowns, wildfire or maintenance disruptions, or a sharp trade-related manufacturing contraction; growth below -0.26% would land outside the interval."},{"kind":"forecast","point":0.1,"ciLow":-0.26,"ciHigh":0.46}]}

# Reviewer critique
{"summary":"The draft is publishable; it matches the target contract and gives a coherent prior, update, interval, tails, and first-print resolver.","requiredFixes":[],"optionalSuggestions":["Consider noting that the May +0.1% figure is a preliminary advance estimate, not part of the 10-observation historical sample used for the variance.","If available in the trace, keep the release-calendar citation tied directly to the September 29, 2026 resolution date."]}

Emit the final JSON object only.
