# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.core_pce.mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-core-pce-mom-july-2026"
- targetUnit: "percent_growth"
- dataPointId: "us.bea.core_pce.mom_sa.2026-07"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bea.gov"], "expectedReleaseWindow": {"end": "2026-09-03", "start": "2026-08-26"}, "field": "bea.core_pce.mom", "releasePolicy": "first_print", "sourceSeriesId": "bea.core_pce.mom", "sourceUrl": "https://www.bea.gov/data/personal-consumption-expenditures-price-index-excluding-food-and-energy", "table": "U.S. Bureau of Economic Analysis, Personal Income and Outlays", "transform": {"factor": 1.0, "operation": "multiply"}}

# Source hints
- Use the official agency release calendar, not inferred cadence.
- FRED may be used as a history mirror, but resolution cites the agency.
- For FOMC targets, resolve to the target range upper bound after the announcement.
- For DOL claims, name the week-ending date and cite the release date.

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
{"slug":"us-core-pce-mom-july-2026","country":"US","type":"data","title":"US Core PCE MoM, July 2026","question":"What will the U.S. Bureau of Economic Analysis first report as the seasonally adjusted month-over-month percent change in the PCE price index excluding food and energy for July 2026?","unit":"percent_growth","pointEstimate":0.3,"ciLow":0.18,"ciHigh":0.42,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"U.S. Bureau of Economic Analysis, Personal Income and Outlays","resolutionSourceUrl":"https://www.bea.gov/data/personal-consumption-expenditures-price-index-excluding-food-and-energy","resolutionRule":"Resolve to BEA's first reported seasonally adjusted month-over-month percent change for the PCE price index excluding food and energy for July 2026 in Personal Income and Outlays, Table 2.8.7 / release text. Use the value as first printed and rounded by BEA to one decimal percentage point in the August 26, 2026 release; ignore later revisions, data-archive updates, and the September 30, 2026 annual update.","dataPointId":"us.bea.core_pce.mom_sa.2026-07","historicalContext":[{"label":"2026-05 first print core PCE m/m","value":0.3},{"label":"2026-04 first print core PCE m/m","value":0.2},{"label":"2026-03 first print core PCE m/m","value":0.3},{"label":"2026-02 first print core PCE m/m","value":0.4},{"label":"2026-01 first print core PCE m/m","value":0.4},{"label":"2025-12 first print core PCE m/m","value":0.4},{"label":"2025-11 value shown in December release table","value":0.2},{"label":"2025-09 first print core PCE m/m","value":0.2}],"drivers":["Recent first-print core PCE clustered around 0.3 percent m/m","May 2026 core PCE was 0.3 percent m/m and 3.4 percent y/y","Services-price persistence keeps upside pressure above a 0.2-only baseline","July 2026 CPI and PPI source components were not yet available at run time","Annual-update revisions begin after this first-print target"],"sourceContext":["https://www.bea.gov/news/schedule","https://www.bea.gov/data/personal-consumption-expenditures-price-index-excluding-food-and-energy","https://www.bea.gov/news/2026/personal-income-and-outlays-may-2026","https://www.bea.gov/news/2026/personal-income-and-outlays-april-2026","https://www.bea.gov/news/2026/personal-income-and-outlays-march-2026","https://www.bea.gov/news/2026/personal-income-and-outlays-february-2026","https://www.bea.gov/news/2026/personal-income-and-outlays-january-2026","https://www.bea.gov/news/2026/personal-income-and-outlays-december-2025","https://www.bea.gov/news/2025/personal-income-and-outlays-september-2025","https://fred.stlouisfed.org/series/PCEPILFE"],"runAt":"2026-07-10T04:33:42Z","reasoning":[{"kind":"heading","text":"US Core PCE MoM July 2026 First Print"},{"kind":"text","text":"Resolver framing: this is the BEA seasonally adjusted PCE price index excluding food and energy, month-over-month percent change for July 2026, first print. The ledger window allowed 2026-08-26 through 2026-09-03, but the official BEA schedule this run shows the July 2026 Personal Income and Outlays release on 2026-08-26 at 8:30 AM, so I use 2026-08-26 while keeping the same catalog target."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA release schedule for Personal Income and Outlays July 2026.","result":"BEA schedule fetched: Personal Income and Outlays, July 2026 is listed for August 26, 2026 at 8:30 AM; the same schedule page also lists June 2026 on July 30, 2026 and August 2026 on September 30, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA exact core PCE data page and current-release status.","result":"BEA core PCE page fetched: May 2026 y/y +3.4%, April 2026 y/y +3.3%, March 2026 y/y +3.3%, February 2026 y/y +3.0%; current release June 25, 2026 and next release July 30, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read BEA Personal Income and Outlays May 2026 release for latest first-print monthly core inflation and related demand context.","result":"May 2026 release fetched: core PCE price index increased 0.3% m/m; headline PCE price index increased 0.4% m/m; core PCE increased 3.4% y/y; current-dollar PCE increased $156.1 billion and real PCE increased 0.3% m/m."},{"kind":"tool","tool":"official.lookup","call":"Read prior BEA first-print releases for the same SA monthly core PCE variant and the same release family.","result":"Fetched first-print monthly core PCE values: January 2026 0.4%, February 2026 0.4%, March 2026 0.3%, April 2026 0.2%, May 2026 0.3%, December 2025 0.4%, November 2025 0.2% from the December release table, and September 2025 0.2%."},{"kind":"tool","tool":"fred.lookup","call":"Checked FRED mirror for the BEA core PCE chain-type price index to cross-check latest level and source code context, not for final resolution.","result":"FRED PCEPILFE mirror fetched: May 2026 index 130.082, April 2026 129.667, March 2026 129.343, February 2026 128.961, January 2026 128.455; FRED notes BEA Account Code DPCCRG, monthly seasonally adjusted."},{"kind":"text","text":"Reference class/base rate: for this first-print forecast I anchor on the same BEA Personal Income and Outlays monthly core PCE first-print/release-table values because the target is a rounded monthly change, not the revised index level. The recent reference class mean is 0.30 percent across the eight fetched monthly values."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent official first-print reference class [0.2, 0.2, 0.4, 0.4, 0.4, 0.3, 0.2, 0.3], mean = 2.4/8 = 0.30. Adjustment components: +0.01 because May y/y core PCE at 3.4% indicates above-target persistence; -0.01 because July CPI/PPI component evidence is not yet available and two monthly releases remain before July; final point remains 0.30. Interval method uses realized dispersion of the change values themselves: sample sigma = 0.093, half-width = 1.28*sigma = 0.119, so 0.30 +/- 0.119 gives 0.181 to 0.419, rounded to 0.18 to 0.42."},{"kind":"text","text":"Mechanisms: level pressure is still firm because core y/y is 3.4%, momentum is centered at 0.3% after May's 0.3% and April's first-print 0.2%, and no one-off July source component has been observed yet. BEA's annual update is scheduled after this August first print, so it should not change the first-print resolution rule."},{"kind":"text","text":"Counter-considerations: upside risk is a broad July services or tariff-sensitive goods acceleration that would land above the interval, roughly a BEA print of 0.5% or higher. Downside risk is a broad softening in rents, portfolio-management, medical, and goods components that would land below the interval, roughly a BEA print of 0.1% or lower. A shutdown-style delay could move publication mechanics, but the release-date forecast is tied to the official schedule fetched this run."},{"kind":"forecast","point":0.3,"ciLow":0.18,"ciHigh":0.42}]}

# Reviewer critique
{
  "summary": "Draft is publishable with no blocking issues; it clearly ties the forecast to the BEA first-print July 2026 core PCE MoM target and gives a compact prior/update/interval rationale.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider noting that the interval is based on a very small recent eight-observation rounded first-print sample, so it is a heuristic dispersion interval rather than a calibrated forecast-error interval.",
    "Consider explaining why the historical sample skips October 2025 if the cited first-print sequence is meant to be consecutive."
  ]
}

Emit the final JSON object only.
