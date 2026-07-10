# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: statcan.gdp_by_industry.monthly_growth
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "canada-monthly-gdp-growth-june-2026"
- targetUnit: "percent_growth"
- dataPointId: "statcan.36-10-0434-01.all_industries.month_to_month_percent_change.2026-06.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-09-04", "start": "2026-08-27"}, "field": "statcan.gdp_by_industry.monthly_growth", "releasePolicy": "first_print", "sourceSeriesId": "statcan.gdp_by_industry.monthly_growth", "sourceUrl": "https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610043401", "table": "Statistics Canada The Daily release and Table 36-10-0434-01", "transform": {"factor": 1.0, "operation": "multiply"}}

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
{"slug":"canada-monthly-gdp-growth-june-2026","country":"CA","type":"data","title":"Canada Monthly GDP Growth, June 2026","question":"What will Statistics Canada first report for real gross domestic product by industry, all industries, seasonally adjusted monthly percent change, June 2026?","unit":"percent_growth","pointEstimate":0.1,"ciLow":-0.2,"ciHigh":0.4,"confidence":0.8,"resolutionDate":"2026-08-28","resolutionSource":"Statistics Canada The Daily release and Table 36-10-0434-01","resolutionSourceUrl":"https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610043401","resolutionRule":"Resolve to the first Statistics Canada print for June 2026 real GDP by industry, all industries, seasonally adjusted monthly change, as published in The Daily and Table 36-10-0434-01. Use the first-published monthly percent change rounded to one decimal percentage point; ignore later revisions.","dataPointId":"statcan.36-10-0434-01.all_industries.month_to_month_percent_change.2026-06.first_print","historicalContext":[{"label":"2026-05 advance estimate","value":0.1},{"label":"2026-04 official","value":0.5},{"label":"2026-03 official","value":-0.1},{"label":"2026-02 official","value":0.2},{"label":"2026-01 official","value":0.1},{"label":"2025-12 official","value":0.2},{"label":"2025-11 official","value":0},{"label":"2025-10 official","value":-0.3}],"drivers":["May advance GDP was modestly positive at 0.1%","April official GDP rebound was 0.5% after March -0.1%","May goods exports rose 0.9% but real export volumes were essentially unchanged","Services and finance/real estate momentum partly offset goods-sector volatility","Energy and mining swings keep one-month dispersion wide"],"sourceContext":["https://www150.statcan.gc.ca/release-diffusion/2026-eng.pdf","https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610043401","https://www150.statcan.gc.ca/n1/daily-quotidien/260630/dq260630a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260529/dq260529b-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260430/dq260430a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260707/dq260707a-eng.htm"],"runAt":"2026-07-10T04:20:18Z","reasoning":[{"kind":"heading","text":"Canada June 2026 Monthly GDP Growth Forecast"},{"kind":"text","text":"Framing and exact resolver: target is Statistics Canada's real gross domestic product by industry for all industries, seasonally adjusted, monthly percent change for June 2026, first print. The ledger points to Table 36-10-0434-01; the same Daily releases report the monthly change from that table, while the related growth-rates view is Table 36-10-0434-02. I keep the ledger target unchanged and resolve on the first print only."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada 2026-2027 major economic release calendar for Gross domestic product by industry","result":"Fetched release calendar shows Gross domestic product by industry: April 2026 released June 30, 2026; May 2026 scheduled July 31, 2026; June 2026 scheduled August 28, 2026."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada Daily release for GDP by industry, April 2026","result":"Fetched latest official GDP print: April 2026 real GDP by industry monthly change was +0.5%; March 2026 was -0.1%; advance information indicated May 2026 increased +0.1%; 14 of 20 sectors grew in April."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada Daily releases for prior GDP by industry months","result":"Fetched recent same-variant history: March 2026 -0.1%, February 2026 +0.2%, January 2026 +0.1%, December 2025 +0.2%, November 2025 0.0%, October 2025 -0.3% monthly change."},{"kind":"tool","tool":"official.lookup","call":"Statistics Canada Daily release for Canadian international merchandise trade, May 2026","result":"Fetched May 2026 trade context: exports +0.9% to $77.1 billion, imports -0.2% to $72.9 billion, goods surplus $4.2 billion, real total export volumes essentially unchanged, real total import volumes +0.4%."},{"kind":"text","text":"Reference class and base rate: for this flow/change target I use the recent same-variant monthly GDP changes themselves, not level changes. The 8-point reference class from October 2025 through the May 2026 advance is -0.3, 0.0, 0.2, 0.1, 0.2, -0.1, 0.5, 0.1, giving a base rate mean of 0.0875% before judgmental adjustment."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class prior is the 8-point recent same-variant monthly GDP sample (-0.3, 0.0, 0.2, 0.1, 0.2, -0.1, 0.5, 0.1), mean = 0.0875. Adjustment components: +0.02 for still-positive May advance and services momentum, -0.01 for April's one-off rebound risk fading, +0.00 for trade because nominal exports rose but real export volumes were essentially unchanged. Final point rounds to 0.1. Interval method uses realized dispersion of the values themselves: sigma = 0.236, half-width = 1.28*sigma = 0.302, so 0.1 +/- 0.3 gives an 80% interval of -0.2 to 0.4 after one-decimal rounding."},{"kind":"text","text":"Upside risk: June would land above the interval if mining/oil output and manufacturing both rebound again while services continue growing around April-May rates. Downside risk: June would land below the interval if energy maintenance, tariffs-sensitive manufacturing, or wholesale/retail weakness turn the May advance into a short-lived bounce. Outside the interval likely requires a broad goods-sector shock rather than normal monthly noise."},{"kind":"forecast","point":0.1,"ciLow":-0.2,"ciHigh":0.4}]}

# Reviewer critique
{
  "summary": "The draft is publication-ready aside from a minor clarity issue around separating the prior from the May advance update.",
  "requiredFixes": [
    {
      "rubricItem": "base_rate",
      "severity": "warning",
      "summary": "The stated 8-point base-rate sample includes the 2026-05 advance estimate, then the update also adds a positive adjustment for the same May advance/services momentum, which could read as partial double-counting rather than a clean prior-before-update structure.",
      "actionRequested": "Clarify whether the May advance is part of the prior sample or an inside-view update; preferably state an official-history prior excluding the May advance, then apply the May advance as an update, or explicitly say the update is only for information not already captured by the sample."
    }
  ],
  "optionalSuggestions": [
    "Keep the resolver text as written; it matches the ledger slug, unit, dataPointId, first-print rule, and August 28, 2026 release date.",
    "The interval method is acceptable, but note that the realized-volatility sample is small if you want to make the uncertainty caveat explicit.",
    "The Table 36-10-0434-02 aside is useful but slightly distracting; ensure it cannot be read as changing the canonical Table 36-10-0434-01 resolver."
  ]
}

Emit the final JSON object only.
