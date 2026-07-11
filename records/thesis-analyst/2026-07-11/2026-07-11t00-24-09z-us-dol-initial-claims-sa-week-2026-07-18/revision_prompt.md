# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: us.dol.initial_claims.sa
- period: week_2026-07-18
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-18"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "us.dol.initial_claims.sa.week_2026-07-18"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-25", "start": "2026-07-21"}, "field": "ICSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "ICSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA", "table": "ALFRED graph CSV", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-11-744098c1b345176f966ba181700538215eeef034556de85c3664a099ad0ebe9f.json"
- targetContentHash: "744098c1b345176f966ba181700538215eeef034556de85c3664a099ad0ebe9f"
- registrationCommit: "acccfc0a6925ff3385b5c0e29b544fb6310a3f73"
- registeredAtUtc: "2026-07-11T00:23:25Z"

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
{"slug":"initial-claims-week-2026-07-18","country":"US","type":"data","title":"US initial claims, week ending July 18","question":"What will the advance first-print number of US seasonally adjusted initial unemployment insurance claims be for the week ending July 18, 2026?","unit":"thousands","pointEstimate":216,"ciLow":203,"ciHigh":229,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor Unemployment Insurance Weekly Claims release","resolutionSourceUrl":"https://www.dol.gov/agencies/eta/ui-claims","resolutionRule":"Resolve to the advance first-print seasonally adjusted US initial claims figure for the week ending July 18, 2026, in the DOL release scheduled for July 23, 2026, expressed in thousands and rounded to the nearest thousand. Ignore all subsequent revisions.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-18","historicalContext":[{"label":"week ending 2026-07-04 advance SA","value":215},{"label":"week ending 2026-06-27 comparison SA","value":217},{"label":"week ending 2026-06-20 comparison SA","value":216},{"label":"week ending 2026-06-13 comparison SA","value":227},{"label":"week ending 2025-07-19 SA reference","value":218}],"drivers":["recent claims level near 215 thousand","four-week average declining to 218.75 thousand","stable low insured-unemployment rate","July seasonal-adjustment volatility"],"sourceContext":["https://www.dol.gov/newsroom/releases/eta/eta20260709","https://www.dol.gov/sites/dolgov/files/OPA/newsreleases/ui-claims/20261132.pdf","https://www.dol.gov/newsroom/releases?agency=39&page=0&state=All&topic=132&year=all","https://www.dol.gov/agencies/eta/ui-claims"],"runAt":"2026-07-11T00:24:33Z","reasoning":[{"kind":"heading","text":"Advance US initial claims for the week ending July 18, 2026"},{"kind":"text","text":"The target is the DOL advance first print for US initial claims, seasonally adjusted, for the week ending July 18, 2026. The DOL schedule verifies release on Thursday, July 23, 2026. Resolution uses the advance SA figure only, not NSA claims, the four-week average, or a revised vintage; the series is ICSA and the release table is UNEMPLOYMENT INSURANCE DATA FOR REGULAR STATE PROGRAMS."},{"kind":"tool","tool":"official.lookup","call":"Read the July 9, 2026 DOL Weekly Claims release and its regular-state-program table.","result":"DOL reported advance SA initial claims of 215 thousand for July 4, 2026; the comparison levels were 217 thousand for June 27 and 216 thousand for June 20, while the four-week average was 218.75 thousand."},{"kind":"tool","tool":"official.lookup","call":"Read recent DOL Weekly Claims releases for the same seasonally adjusted initial-claims variant.","result":"The same-variant sequence for May 30 through July 4 was 225, 230, 227, 216, 217, and 215 thousand; the latest weekly change was -2 thousand."},{"kind":"tool","tool":"official.lookup","call":"Read the historical table embedded in the July 9 DOL release for the comparable July period and recent 2026 changes.","result":"The historical table shows 2025 SA claims of 228 thousand on July 5, 221 thousand on July 12, and 218 thousand on July 19; its 27 weekly changes from January 3 through July 4, 2026 range from -25 to +19 thousand."},{"kind":"text","text":"The reference class and base rate are low-volatility weekly claims observations outside recession: the latest six same-variant readings center near 218 thousand, while the comparable July 2025 sequence declined from 228 to 218 thousand. Persistence therefore anchors the forecast near 215-218 thousand."},{"kind":"text","text":"Level is about 215 thousand and recent momentum is mildly downward; one-off holiday and auto-retooling seasonality can create July noise even after adjustment. No official release evidence indicates a policy mechanism or broad layoffs requiring a large directional shift, so the net update is +1 thousand from the latest advance level."},{"kind":"math","text":"Prior/update/interval: The model is persistence around the latest 215 thousand observation, checked against the six-reading recent historical sample of 225, 230, 227, 216, 217, and 215. Adjustments are +1 thousand for mean reversion, 0 for weak downward momentum, 0 for policy, and 0 net for July one-offs, giving 216. For interval sizing, the 27 successive weekly changes from January 3 through July 4 have sum 12 and sum of squares 2748, so sample sigma = sqrt((2748 - 12^2/27)/(27-1)) = 10.27 thousand. The normal 80% half-width is 1.28*sigma = 13.15 thousand; 216 ± 13.15 rounds to final implied bounds of 203 and 229 thousand."},{"kind":"text","text":"Upside risk comes from concentrated auto-sector or other temporary layoffs and would land above the interval if the first print exceeds 229 thousand. Downside risk comes from unusually favorable seasonal adjustment or fewer filings and would land below the interval if the first print is under 203 thousand. Either outcome would be outside the interval and falsify the assumed calm-regime persistence model."},{"kind":"forecast","point":216,"ciLow":203,"ciHigh":229}]}

# Reviewer critique
{
  "summary": "Draft is publication-ready on resolver, prior, update, interval construction, tails, and JSON coherence.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider naming the ALFRED ICSA advance-vintage binding alongside the DOL release in the resolver text if the catalog display depends on that source binding.",
    "The interval method is acceptable, but noting that the 27-change volatility sample is same-series SA weekly changes would make the provenance slightly clearer."
  ]
}

Emit the final JSON object only.
