# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.housing.completions_saar
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-housing-completions-july-2026"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "census.housing.completions_saar.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-18", "start": "2026-08-18"}, "field": "COMPUTSA", "releasePolicy": "first_print", "sourceSeriesId": "COMPUTSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=COMPUTSA", "table": "New Residential Construction, seasonally adjusted annual rates", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-d575eb38110952504acebd0ba3e773df5327cd1eb860702d961a00d0b2d45a82.json"
- targetContentHash: "d575eb38110952504acebd0ba3e773df5327cd1eb860702d961a00d0b2d45a82"
- registrationCommit: "0249a6f266d1d202c43782056e77403612358765"
- registeredAtUtc: "2026-07-31T14:48:09Z"

# Source hints
- Use Census income, poverty, SPM, and health-insurance release pages, CPS ASEC historical tables, and the Census release calendar.
- For official-poverty targets, distinguish the official poverty measure from SPM and cite the exact Census table or report.
- For SPM targets, name the population group, calendar year, and whether taxes, credits, transfers, medical expenses, or housing adjustments matter for the forecast.
- For ACS table targets, fetch each history year's values from the keyless JSON endpoint https://data.census.gov/api/access/data/table?id=<PRODUCT><YEAR>.<TABLE>&g=010XX00US (for example ACSDT1Y2024.B28005) and read the cited variable columns from the returned JSON.
- api.census.gov requires an API key (keyless requests redirect to missing_key.html); never rely on it in keyless runs, and never present remembered values as fetched ones.
- ACS vintage discipline: never mix 5-year estimates into a 1-year series — the 5-year file is a five-year average, so its level trails the 1-year series; the product id in the fetch URL (ACSDT1Y vs ACSDT5Y) is the vintage authority.

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

Emit the final JSON object only. (agent thesis.analyst v2.4.0, prompt 7ef119647b35, tools 50a06b62f9be, promptMode fast)


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
{"slug":"us-housing-completions-july-2026","country":"US","type":"data","title":"US housing completions, July 2026","question":"What will the U.S. Census Bureau and HUD first report for privately-owned housing completions in July 2026, seasonally adjusted annual rate, in thousands of units?","unit":"thousands","pointEstimate":1390,"ciLow":1270,"ciHigh":1510,"confidence":0.8,"resolutionDate":"2026-08-18","resolutionSource":"U.S. Census Bureau and HUD New Residential Construction release, mirrored as ALFRED/FRED series COMPUTSA first print","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=COMPUTSA","resolutionRule":"Resolve to the first official July 2026 print for COMPUTSA, privately-owned housing completions at a seasonally adjusted annual rate in thousands of units, as released on August 18, 2026. Use the initial vintage/first print only; do not apply later revisions or same-day correction exceptions unless the registered sourceBinding changes.","dataPointId":"census.housing.completions_saar.2026_07.first_print","historicalContext":[{"label":"2026-06 preliminary SAAR","value":1392},{"label":"2026-05 revised SAAR","value":1347},{"label":"2026-04 revised SAAR","value":1454},{"label":"2026-03 SAAR","value":1373},{"label":"2026-02 SAAR","value":1324},{"label":"2026-01 SAAR","value":1439}],"drivers":["June completions near 1.39 million SAAR after a May dip","single-family completions strengthened to 964 thousand SAAR in June","five-or-more completions remained softer at 413 thousand SAAR","starts rebounded to 1,427 thousand SAAR in June, supporting near-term completions","not-seasonally-adjusted completions year to date were 9.5 percent below 2025"],"sourceContext":["https://www.census.gov/construction/nrc/current/index.html","https://www.census.gov/construction/nrc/pdf/newresconst.pdf","https://www.census.gov/construction/soc/schedule.html","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=COMPUTSA"],"runAt":"2026-07-31T14:51:46Z","reasoning":[{"kind":"heading","text":"US July 2026 housing completions SAAR first print"},{"kind":"text","text":"Framing and exact resolver: this forecasts Census/HUD New Residential Construction privately-owned housing completions, seasonally adjusted annual rate, total United States, July 2026, in thousands. The ledger resolver is ALFRED/FRED sourceSeriesId COMPUTSA under first_print policy; I use Census/HUD release tables as official public evidence and keep the final rule tied to the registered first-vintage COMPUTSA target."},{"kind":"tool","tool":"official.lookup","call":"Checked Census Survey of Construction release schedule for July 2026 New Residential Construction.","result":"Fetched schedule shows July 2026 New Residential Construction at 8:30 a.m. on August 18, 2026; the same schedule lists June 2026 on July 17, 2026 and August 2026 on September 17, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the June 2026 Census/HUD New Residential Construction current release summary for housing completions.","result":"Fetched June 2026 housing completions at 1,392 thousand SAAR, revised May at 1,347 thousand SAAR, June 2025 at 1,372 thousand SAAR, single-family completions at 964 thousand SAAR, and five-or-more completions at 413 thousand SAAR."},{"kind":"tool","tool":"official.lookup","call":"Read Census/HUD PDF Table 5a for recent total housing completions SAAR history.","result":"Fetched total completions SAAR values: January 2026 1,439, February 2026 1,324, March 2026 1,373, April 2026 1,454, May 2026 1,347, June 2026 1,392, all in thousands."},{"kind":"tool","tool":"official.lookup","call":"Read Census/HUD June release for leading construction indicators and completion composition.","result":"Fetched June 2026 building permits at 1,367 thousand SAAR, housing starts at 1,427 thousand SAAR, May starts at 1,199 thousand SAAR, and units under construction at 1,264 thousand SAAR."},{"kind":"tool","tool":"official.lookup","call":"Read Census/HUD PDF Table 5b for not-seasonally-adjusted year-to-date completions.","result":"Fetched not-seasonally-adjusted completions year to date at 434.5 thousand in 2026 versus 478.9 thousand in 2025, a -9.5 percent change; June 2026 NSA completions were 123.7 thousand."},{"kind":"text","text":"Reference class and base rate: for this same SAAR variant, the near-term reference class is month-to-month changes in recent total completions. A persistence base rate around the latest print, 1,392 thousand, is more informative than the 2025 July level because completions are volatile and the July first print is a one-month SAAR estimate."},{"kind":"math","text":"Prior/update/interval: persistence prior is June 2026 total completions SAAR = 1,392. Historical sample is the official January-June 2026 Census Table 5a sequence 1,439, 1,324, 1,373, 1,454, 1,347, 1,392, giving successive changes -115, +49, +81, -107, +45; sample sigma = 94 thousand. Adjustment components: -20 thousand for weak 2026 year-to-date NSA completions versus 2025, +10 thousand for high single-family completions, +8 thousand for June starts rebound and still-large under-construction stock, net about -2 thousand from persistence. Point = 1,390. 80% half-width = 1.28*sigma = 1.28*94 = 120 thousand, so bounds are 1,390 - 120 = 1,270 and 1,390 + 120 = 1,510."},{"kind":"text","text":"Counter-considerations: upside risk would come from June's 1,427 thousand starts rebound pulling through quickly or multifamily completions normalizing upward, which would land above the interval if the first print exceeds 1,510 thousand. Downside risk is a renewed multifamily completion drop or seasonal adjustment reversal after June's single-family strength, which would land below the interval if the first print is under 1,270 thousand."},{"kind":"forecast","point":1390,"ciLow":1270,"ciHigh":1510}]}

# Reviewer critique
{
  "summary": "Draft is publication-ready with no blocking issues; it states the registered resolver, first-print rule, prior, update, interval construction, tails, and coherent JSON fields.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider naming ALFRED as the registered mirror and Census/HUD as the official release more explicitly in the final resolver sentence to avoid any perceived source ambiguity.",
    "The volatility sample is very short; note that the 80% interval is based on January-June 2026 month-to-month moves if space allows."
  ]
}

Emit the final JSON object only.
