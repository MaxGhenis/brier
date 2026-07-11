# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: abs.labour.unemployment_rate
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "australia-unemployment-rate-july-2026"
- country: "AU"
- targetUnit: "percent"
- dataPointId: "abs.labour.unemployment_rate.australia.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["data.api.abs.gov.au", "www.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-08-27", "start": "2026-08-19"}, "field": "M13", "releasePolicy": "first_print", "sourceSeriesId": "LF/M13.3.1599.20.AUS.M", "sourceUrl": "https://data.api.abs.gov.au/rest/data/LF/M13.3.1599.20.AUS.M?format=jsondata", "table": "Labour Force, Australia (dataflow LF): unemployment rate, persons, seasonally adjusted; first print captured on release day", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-11-cf3a2f76bb15d9f5eb9f5ae19d2e96b55111cf6842a1c8c8412b915ae614a85b.json"
- targetContentHash: "cf3a2f76bb15d9f5eb9f5ae19d2e96b55111cf6842a1c8c8412b915ae614a85b"
- registrationCommit: "acccfc0a6925ff3385b5c0e29b544fb6310a3f73"
- registeredAtUtc: "2026-07-11T00:23:25Z"

# Source hints
- Use ABS release calendar and official monthly CPI indicator pages.
- Australia CPI indicator rates print to one decimal.
- Resolution source should be the ABS release page.

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
{"slug":"australia-unemployment-rate-july-2026","country":"AU","type":"data","title":"Australia unemployment rate, July 2026","question":"What will the ABS first-print seasonally adjusted unemployment rate for Australia be for July 2026?","unit":"percent","pointEstimate":4.4,"ciLow":4.1,"ciHigh":4.7,"confidence":0.8,"resolutionDate":"2026-08-20","resolutionSource":"Australian Bureau of Statistics, Labour Force, Australia","resolutionSourceUrl":"https://data.api.abs.gov.au/rest/data/LF/M13.3.1599.20.AUS.M?format=jsondata","resolutionRule":"Resolve to the unemployment rate for persons, Australia, seasonally adjusted, series LF/M13.3.1599.20.AUS.M (field M13), for July 2026 in the first ABS Labour Force, Australia print released on 20 August 2026. Use the value as published to one decimal place; ignore all subsequent revisions.","dataPointId":"abs.labour.unemployment_rate.australia.july_2026.first_print","historicalContext":[{"label":"January 2026 unemployment rate, seasonally adjusted","value":4.1},{"label":"February 2026 unemployment rate, seasonally adjusted","value":4.3},{"label":"March 2026 unemployment rate, seasonally adjusted","value":4.3},{"label":"April 2026 unemployment rate, seasonally adjusted","value":4.5},{"label":"May 2026 unemployment rate, seasonally adjusted","value":4.4}],"drivers":["Recent unemployment-rate persistence near 4.4 percent","May employment increased by 40000 while unemployment fell by 18300","Employment-to-population ratio remained high at 63.8 percent","Restrictive 4.35 percent cash rate may gradually soften labour demand","Two unreleased monthly transitions add sampling and cyclical uncertainty"],"sourceContext":["https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia","https://www.abs.gov.au/release-calendar/future-releases-calendar/202608/rcc_labour","https://www.abs.gov.au/media-centre/media-releases/unemployment-rate-falls-44-may","https://www.abs.gov.au/media-centre/media-releases/unemployment-rate-rises-45-april","https://www.abs.gov.au/media-centre/media-releases/unemployment-rate-remains-43-march","https://www.abs.gov.au/media-centre/media-releases/unemployment-rate-rises-43-february","https://www.rba.gov.au/cash-rate-target-overview.html","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/may-2026"],"runAt":"2026-07-11T00:27:57Z","reasoning":[{"kind":"heading","text":"Australia July 2026 unemployment-rate forecast"},{"kind":"text","text":"The target is the first-print July 2026 Australian unemployment rate for persons, seasonally adjusted—not trend or unadjusted—from ABS dataflow LF, series M13.3.1599.20.AUS.M. Resolution uses the first official print without later revisions."},{"kind":"tool","tool":"official.lookup","call":"Fetched the ABS Labour Force release calendar and series release page for the July 2026 reference period.","result":"ABS schedules Labour Force, Australia, July 2026 for 20 August 2026 at 11:30am AEST; the preceding June 2026 release is scheduled for 23 July 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent ABS Labour Force releases for the national seasonally adjusted unemployment-rate reference class.","result":"The first reported rates were 4.1% in January 2026, 4.3% in February, 4.3% in March, 4.5% in April, and 4.4% in May."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest ABS Labour Force release for level and momentum indicators.","result":"In May 2026 employment rose by 40000, unemployed persons fell by 18300 to 671300, the unemployment rate fell 0.1 point to 4.4%, and the employment-to-population ratio rose 0.1 point to 63.8%."},{"kind":"tool","tool":"official.lookup","call":"Fetched current official inflation and monetary-policy settings relevant to labour demand.","result":"ABS reported May 2026 annual CPI inflation of 4.0%, while the RBA cash-rate target was 4.35% effective 17 June 2026."},{"kind":"text","text":"The outside-view base rate is persistence: this reference class has stayed within 4.1% to 4.5% across the five available 2026 prints, with a five-month mean of 4.32%. A 4.4% anchor gives more weight to the latest level while allowing mild mean reversion."},{"kind":"text","text":"Level is 4.4%; momentum is mixed because April's rise reversed partly in May; the May waiting-to-start-job backlog unwind is a potentially one-off downward effect; and the policy mechanism from a 4.35% cash rate creates gradual upward pressure through softer labour demand rather than a sharp immediate jump."},{"kind":"math","text":"Prior/update/interval: The model is a latest-level persistence prior anchored at 4.4%, using the January-May 2026 historical sample [4.1, 4.3, 4.3, 4.5, 4.4]. Successive changes are [+0.2, 0.0, +0.2, -0.1] percentage points; their sample standard deviation is sigma = 0.15 percentage points. The one-step 80% half-width is 1.28*sigma = 1.28*0.15 = 0.19. Because July is two monthly transitions beyond the latest May print, scale by sqrt(2): 0.19*1.414 = 0.27, rounded to the release precision as 0.3. The persistence prior plus a roughly neutral net update gives 4.4%, with final implied bounds 4.4-0.3 = 4.1% and 4.4+0.3 = 4.7%."},{"kind":"text","text":"Upside risk comes from restrictive policy producing faster hiring weakness or participation rebounding while employment stalls; a print of 4.8% or higher would land above the interval. Downside risk comes from continued strong employment growth or another unwind in people waiting to start jobs; 4.0% or lower would land below the interval. These are the concrete scenarios outside the interval."},{"kind":"forecast","point":4.4,"ciLow":4.1,"ciHigh":4.7}]}

# Reviewer critique
{"summary":"Draft is publishable: resolver, first-print rule, prior, update logic, interval math, tails, and JSON fields are coherent with the ledger target.","requiredFixes":[],"optionalSuggestions":["Consider noting that the volatility estimate uses only four month-to-month changes, so the interval is mechanically transparent but sample-limited.","If space allows, cite the ABS calendar line that fixes 20 August 2026 as the July 2026 Labour Force release date."]}

Emit the final JSON object only.
