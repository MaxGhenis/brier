# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: statcan.lfs.unemployment_rate.canada
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "statcan-lfs-unemployment-rate-canada-june-2026"
- targetUnit: "percent"
- dataPointId: "statcan.lfs.unemployment_rate.canada.june_2026.first_print"
- resolutionSourceUrl: "https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www150.statcan.gc.ca"], "expectedReleaseWindow": {"end": "2026-07-09", "start": "2026-07-01"}, "field": "official_release:statcan:dq260605a:unemployment_rate", "releasePolicy": "first_print", "sourceSeriesId": "statcan.lfs.unemployment_rate", "sourceUrl": "https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm", "table": "Labour Force Survey, May 2026", "transform": {"factor": 1, "operation": "identity"}}

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
{"slug":"statcan-lfs-unemployment-rate-canada-june-2026","country":"CA","type":"data","title":"Canada unemployment rate, June 2026","question":"Statistics Canada Labour Force Survey unemployment rate for Canada, June 2026 reference month, seasonally adjusted, first print","unit":"percent","pointEstimate":6.7,"ciLow":6.4,"ciHigh":7,"confidence":0.8,"resolutionDate":"2026-07-10","resolutionSource":"Statistics Canada The Daily, Labour Force Survey","resolutionSourceUrl":"https://www150.statcan.gc.ca/n1/daily-quotidien/260710/dq260710a-eng.htm","resolutionRule":"Resolve to the first-print seasonally adjusted unemployment rate for Canada in Statistics Canada's Labour Force Survey for the June 2026 reference month, as published in The Daily and sourced to Table 14-10-0287-01. Use the one-decimal percent value as first published; do not substitute later revisions or corrected historical table vintages unless the first-print release itself is replaced before publication.","dataPointId":"statcan.lfs.unemployment_rate.canada.june_2026.first_print","historicalContext":[{"label":"May 2026 unemployment rate","value":6.6},{"label":"April 2026 unemployment rate","value":6.9},{"label":"March 2026 unemployment rate","value":6.7},{"label":"February 2026 unemployment rate","value":6.7},{"label":"January 2026 unemployment rate","value":6.5}],"drivers":["May unemployment rate fell to 6.6 after April's 6.9","May employment gain of 88,000 suggests some reversal after early-2026 weakness","Recent monthly unemployment-rate changes had about 0.24 percentage-point dispersion","LFS remains above the 2017-2019 pre-pandemic average of 6.0"],"sourceContext":["https://www150.statcan.gc.ca/release-diffusion/2026-eng.pdf","https://www150.statcan.gc.ca/n1/daily-quotidien/260605/dq260605a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260508/dq260508a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260410/dq260410a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260313/dq260313a-eng.htm","https://www150.statcan.gc.ca/n1/daily-quotidien/260206/dq260206a-eng.htm","https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028701"],"runAt":"2026-07-10T04:06:08Z","reasoning":[{"kind":"heading","text":"Canada LFS Unemployment Rate, June 2026"},{"kind":"text","text":"Framing and exact resolver: target is the Statistics Canada Labour Force Survey unemployment rate for Canada, seasonally adjusted, June 2026 reference month, first print. I keep the catalog slug and dataPointId, but the supplied ledger URL points to the June 5, 2026 Daily page for Labour Force Survey, May 2026; the official release schedule says the June 2026 LFS reference period is released on July 10, 2026, so the specific resolver page should be the July 10, 2026 Daily LFS page when available."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada 2026-2027 major economic releases PDF and read Labour Force Survey rows.","result":"Fetched schedule numbers: Labour Force Survey release date for June 2026 reference period is July 10, 2026; May 2026 reference period is June 5, 2026; July 2026 reference period is August 7, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily, Labour Force Survey, May 2026.","result":"Fetched latest official LFS numbers: Canada unemployment rate was 6.6% in May 2026, down 0.3 pts; employment increased by 88,000 or 0.4%; employment rate was 60.7%; job-finding rate was 26.3%."},{"kind":"tool","tool":"official.lookup","call":"Opened Statistics Canada The Daily releases for January through April 2026 and Table 14-10-0287-01 metadata.","result":"Fetched reference class history from the same seasonally adjusted LFS variant: January 2026 unemployment rate 6.5%, February 2026 6.7%, March 2026 6.7%, April 2026 6.9%, May 2026 6.6%; Table 14-10-0287-01 release date shown as 2026-06-05 for the then-current table view."},{"kind":"text","text":"Base rate/reference class: for a one-month-ahead LFS unemployment-rate forecast, persistence from the latest same-variant official print is the base rate. The last five first-print-like Daily values were 6.5, 6.7, 6.7, 6.9, and 6.6, putting the local level around 6.7 with recent prints ranging 6.5 to 6.9."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2026 LFS unemployment rate 6.6. Historical sample = Jan-May 2026 same-variant seasonally adjusted Canada unemployment-rate prints. Adjustment components: level +0.05 because the Jan-May average is 6.68 and the labour market remains above the pre-pandemic 6.0 reference; momentum -0.05 because May employment rose 88,000 and unemployment fell 0.3 pts; one-off/policy mechanism 0.00 because no official release evidence points to a discrete June break. Point = 6.6 + 0.05 - 0.05 + 0.05 rounding judgment = 6.7. Successive changes = +0.2, 0.0, +0.2, -0.3; sigma = 0.236 percentage points using sample standard deviation; 1.28*sigma = 0.302, so 80% half-width is about 0.3 and the one-decimal interval is 6.4 to 7.0."},{"kind":"text","text":"Variant control: all anchors are Statistics Canada LFS, Canada, seasonally adjusted unemployment rate, using The Daily releases sourced to Table 14-10-0287-01. I did not mix unadjusted, provincial, trend-cycle, payroll, or U.S.-concept unemployment series."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed labour-force participation rebound or job losses after May that pushes unemployment to 7.1 or higher, which would land above the interval. Downside risk is a second strong employment month or a participation drop like January that pushes unemployment to 6.3 or lower, outside the interval on the low side."},{"kind":"forecast","point":6.7,"ciLow":6.4,"ciHigh":7}]}

# Reviewer critique
{"summary":"Draft is mostly coherent, but it must not publish with resolver fields that diverge from the canonical ledger contract without an explicit review decision.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft changes resolutionDate to 2026-07-10 and resolutionSourceUrl to the July 10 Daily page, while the canonical ledger contract specifies resolutionDate/source URL fields tied to dq260605a and the expected release window ending 2026-07-09.","actionRequested":"Either align the JSON resolver fields to the canonical ledger contract, or explicitly flag this as a ledger discrepancy for human catalog correction before publication; do not silently publish mismatched resolver fields."},{"rubricItem":"update","severity":"warning","summary":"The move from the 6.6 persistence prior to a 6.7 point estimate rests on a vague '+0.05 rounding judgment' after stated adjustment components net to zero.","actionRequested":"Replace the rounding judgment with a concrete stated update, or keep the point at the rounded persistence-implied value if no material update is justified."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is based on only four Jan-May 2026 monthly changes, which is a very small realized-volatility sample.","actionRequested":"Use a longer same-series monthly change sample if available, or explicitly justify why the short 2026 sample is sufficient for the interval width."}],"optionalSuggestions":["State whether the forecast was made before the July 10, 2026 release time to remove any leakage concern.","Keep the reasoning discrepancy note, but mirror the final decision consistently in the top-level JSON fields."]}

Emit the final JSON object only.
