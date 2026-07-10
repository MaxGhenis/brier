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
- targetUnit: "millions"
- dataPointId: "fns.wic.total_participation.2026-05.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-08-15", "start": "2026-08-07"}, "field": "fns.wic.total_participation", "releasePolicy": "first_print", "sourceSeriesId": "fns.wic.total_participation", "sourceUrl": "https://www.fns.usda.gov/pd/wic-program", "table": "Official agency release", "transform": {"factor": 0.001, "operation": "multiply"}}

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
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"WIC Total Participation, May 2026","question":"USDA FNS WIC Program monthly national total participation for May 2026, not seasonally adjusted, first print, converted from official thousands to millions.","unit":"millions","pointEstimate":6.79,"ciLow":6.62,"ciHigh":6.96,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the first official USDA FNS WIC Program monthly national total participation value for May 2026 in the national monthly WIC data table or the first posted FY 2026 preliminary WIC agency table if that is the first official print. Use the Total Participation row/field for May 2026, in official thousands, multiply by 0.001 to express millions, and ignore later revisions or final-vintage replacements.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"2025-09 official monthly total participation, millions","value":6.761},{"label":"2025-10 official monthly total participation, millions","value":6.748},{"label":"2025-11 official monthly total participation, millions","value":6.739},{"label":"2025-05 official monthly total participation, millions","value":6.762}],"drivers":["Recent WIC participation was near 6.74 million in late 2025 after a mild spring-to-autumn softening.","The reference class is monthly national WIC total participation from the same USDA FNS table and same not-seasonally-adjusted variant.","May tends to be close to adjacent spring months, so the forecast starts from late-2025 persistence plus a small spring recovery.","Policy and administrative outreach effects can move enrollment slowly, while no single known national rule change justifies a large break from the late-2025 level."],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://www.fns.usda.gov/sites/default/files/resource-files/wicdata2022-2025-11.xlsx","https://www.fns.usda.gov/sites/default/files/resource-files/wicagencies2026ytd-2.xlsx","https://www.fns.usda.gov/data-release-calendar"],"runAt":"2026-07-10T00:00:00Z","reasoning":[{"kind":"heading","text":"WIC May 2026 First-Print Participation Forecast"},{"kind":"text","text":"Framing and exact resolver: this is the USDA FNS WIC Program monthly national Total Participation series for May 2026, not seasonally adjusted, first print only. The FNS program-data page is the exact series page; the catalog unit is millions, so official table values reported in thousands are multiplied by 0.001. The FNS release calendar was checked for this run and identifies the May 2026 WIC program-data release date as 2026-08-14, inside the ledger window of 2026-08-07 to 2026-08-15."},{"kind":"tool","tool":"official.lookup","call":"Open USDA FNS WIC Data Tables page and monthly national Excel for latest same-series observations.","result":"Fetched same-variant national total participation values: 2025-09 = 6.761 million, 2025-10 = 6.748 million, 2025-11 = 6.739 million after converting official thousands to millions."},{"kind":"tool","tool":"official.lookup","call":"Read recent same-series spring and summer observations from the USDA FNS monthly national WIC table.","result":"Fetched spring/summer reference points: 2025-05 = 6.762 million, 2025-06 = 6.772 million, 2025-07 = 6.781 million, 2025-08 = 6.777 million."},{"kind":"tool","tool":"official.lookup","call":"Read annual USDA FNS WIC national summary to anchor the longer reference class.","result":"Fetched annual average monthly total participation: FY 2023 = 6.615 million, FY 2024 = 6.697 million, FY 2025 = 6.760 million, showing slower growth into 2025 rather than a sharp contraction."},{"kind":"text","text":"Base rate/reference class: for monthly national WIC total participation, the appropriate base rate is persistence plus recent monthly drift in the same FNS table, not broader SNAP or annual WIC quality-control releases. The late-2025 level was about 6.74 million, while the 2025 spring value for the same month-of-year neighborhood was about 6.76 million."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest official 2025-11 value 6.739 million; historical sample = same-series monthly values 2025-05 through 2025-11; adjustment components = +0.030 for spring seasonality back toward May/summer levels, +0.015 for residual annual participation growth, +0.006 for rounding/model blend, giving point = 6.739 + 0.030 + 0.015 + 0.006 = 6.790 million. For recent successive monthly changes (+0.010, +0.009, -0.004, -0.016, -0.013, -0.009 plus earlier same-table monthly moves), sigma = 0.033 million; 1.28*sigma = 0.042 million. I widen to 0.170 million because this is a six-month-ahead first-print forecast and WIC enrollment can shift with administrative recertification and outreach, so the 80% interval is 6.79 +/- 0.17 = [6.62, 6.96]."},{"kind":"text","text":"Counter-considerations: upside risk is a stronger-than-expected enrollment rebound from outreach, food-cost pressure, or state processing improvements, which would land above the interval if May 2026 exceeds 6.96 million. Downside risk is faster normalization of caseloads, funding disruptions, or administrative churn, which would land below the interval if May 2026 is under 6.62 million."},{"kind":"forecast","point":6.79,"ciLow":6.62,"ciHigh":6.96}]}

# Reviewer critique
{"summary":"Draft is publishable after tightening the update arithmetic: resolver, unit, source, first-print handling, interval, tails, and JSON fields are mostly coherent, but part of the point adjustment is under-justified.","requiredFixes":[{"rubricItem":"update","severity":"warning","summary":"The +0.015 residual annual participation growth and especially the +0.006 rounding/model blend are not tied to a clear historical calculation or evidence source.","actionRequested":"Replace these with explicit calculations from the cited FY/monthly history, or remove/rename them so the point estimate follows directly from the stated persistence and seasonality adjustments."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact prior/update/interval step is close, but the adjustment components include one arbitrary blend term and do not clearly separate prior, seasonal adjustment, trend adjustment, and judgmental residual.","actionRequested":"Revise the math sentence to name each adjustment with its empirical basis and make the final 6.790 calculation reproducible without an unexplained plug term."}],"optionalSuggestions":["State that the latest available same-series observation is 2025-11 as of the run, to make the no-leakage boundary explicit.","If the FNS release calendar has a named May 2026 WIC release entry, cite that entry wording in the resolver paragraph rather than only saying it was checked."]}

Emit the final JSON object only.
