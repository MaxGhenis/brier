# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.m3.durable_goods_shipments_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-durable-goods-shipments-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "census.m3.durable_goods_shipments_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-31", "start": "2026-08-23"}, "field": "AMDMVS", "releasePolicy": "first_print", "sourceSeriesId": "AMDMVS", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=AMDMVS", "table": "Advance Report on Durable Goods Manufacturers' Shipments, Inventories, and Orders", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-c41517a667d8f0263c9113e0c85438385b4bddf98a8e86427e6946fb916edb17.json"
- targetContentHash: "c41517a667d8f0263c9113e0c85438385b4bddf98a8e86427e6946fb916edb17"
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
{"slug":"us-durable-goods-shipments-mom-july-2026","country":"US","type":"data","title":"US durable goods shipments MoM, July 2026","question":"What will the U.S. Census Bureau first report for July 2026 seasonally adjusted manufacturers' value of shipments: durable goods (AMDMVS), month-over-month percent growth, in the Advance Report on Durable Goods Manufacturers' Shipments, Inventories, and Orders?","unit":"percent_growth","pointEstimate":0.4,"ciLow":-0.3,"ciHigh":1.1,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"ALFRED/FRED mirror of the U.S. Census Bureau M3 Advance Report first print for AMDMVS","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=AMDMVS","resolutionRule":"Resolve to the first vintage value for 2026-07-01 in AMDMVS, the seasonally adjusted U.S. Census Bureau Manufacturers' Value of Shipments: Durable Goods series, converted to month-over-month percent growth from the prior first-available monthly level and rounded to one decimal percentage point as reported in the Census advance table. Later revisions, full-report updates, benchmark revisions, and same-day corrections not represented in the first posted vintage do not change resolution.","dataPointId":"census.m3.durable_goods_shipments_mom.2026_07.first_print","historicalContext":[{"label":"2026-06 advance durable goods shipments MoM","value":0.7},{"label":"2026-05 revised durable goods shipments MoM in June advance table","value":1.1},{"label":"2026-04 durable goods shipments MoM in June advance table","value":0.7},{"label":"2026-06 SA shipments level, millions of dollars","value":330685},{"label":"2026-05 SA shipments level, millions of dollars","value":328239}],"drivers":["Recent shipments momentum is positive: June +0.7%, May +1.1%, April +0.7%.","New orders slowed to +0.3% in June, limiting evidence for another large shipments gain.","Transportation shipments were only +0.2% in June after +1.4% in May, so July aircraft and vehicle mix can move the headline.","Core durable shipments excluding transportation were firmer at +1.0% in June."],"sourceContext":["https://www.census.gov/manufacturing/m3/adv/current/index.html","https://www.census.gov/manufacturing/m3/adv/pdf/table1a.pdf","https://www.census.gov/manufacturing/m3/release_schedule.html","https://www.census.gov/economic-indicators/calendar-listview.html","https://fred.stlouisfed.org/series/AMDMVS","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=AMDMVS"],"runAt":"2026-07-31T15:03:55Z","reasoning":[{"kind":"heading","text":"July 2026 durable goods shipments MoM forecast"},{"kind":"text","text":"Framing and exact resolver: this forecast is for Census M3 durable goods manufacturers' shipments, seasonally adjusted, total durable goods, first print for July 2026. The ledger resolver is AMDMVS through ALFRED/FRED; the underlying official publication is the Census Advance Report on Durable Goods Manufacturers' Shipments, Inventories, and Orders. I am keeping the ledger target unchanged even though Census is the official agency source and ALFRED is the resolver mirror."},{"kind":"tool","tool":"official.lookup","call":"Checked Census M3 release schedule and 2026 economic-indicator calendar for the July 2026 advance report date.","result":"Fetched release-date numbers: Census M3 schedule lists July 2026 survey month Advance Report on 8/26/2026 and Full Report on 9/2/2026; the Census 2026 economic-indicator calendar also lists the Advance Report on Durable Goods for July 2026 at 8:30 AM on August 26, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened the latest Census June 2026 Advance Report landing page and Table 1 for shipments and new orders.","result":"Fetched current advance-table numbers: total durable goods shipments were 330,685 million dollars in Jun 2026, 328,239 million in May 2026 revised, and 324,768 million in Apr 2026; monthly percent changes were +0.7 for Jun-May, +1.1 for May-Apr, and +0.7 for Apr-Mar."},{"kind":"tool","tool":"official.lookup","call":"Read Table 1 component rows for transportation, excluding transportation, excluding defense, and orders as same-variant Census advance evidence.","result":"Fetched component numbers: durable goods new orders were 334,772 million dollars in Jun 2026 and +0.3% m/m; shipments excluding transportation were 220,903 million and +1.0%; transportation shipments were 109,782 million and +0.2%; shipments excluding defense were 308,180 million and +0.5%."},{"kind":"tool","tool":"history.lookup","call":"Checked public FRED/ALFRED AMDMVS history mirror for recent seasonally adjusted shipment levels before the latest advance-table revision.","result":"Fetched AMDMVS history numbers: May 2026 was 328,030 million dollars, Apr 2026 324,768, Mar 2026 322,562, Feb 2026 320,023, and Jan 2026 315,099, all seasonally adjusted millions of dollars."},{"kind":"text","text":"Reference class and base rate: the closest base rate is monthly percent growth in the same SA durable-goods shipments series. The recent 2026 reference class is unusually firm: implied Feb-Jan +1.6%, Mar-Feb +0.8%, Apr-Mar +0.7%, then the Census advance table has May-Apr +1.1% and Jun-May +0.7%. I anchor below that near-term average because shipments are a level flow with mean reversion and because June new orders were only +0.3%."},{"kind":"math","text":"Prior/update/interval: persistence prior starts from the recent same-series average, (1.6 + 0.8 + 0.7 + 1.1 + 0.7) / 5 = 1.0%, then I subtract 0.4 percentage point for mean reversion from an unusually strong first half of 2026, subtract 0.1 for June new-orders softness, and add 0.0 to 0.1 for still-firm core shipments, giving a rounded point of +0.4%. For dispersion, using fetched recent monthly percent changes [1.6, 0.8, 0.7, 1.1, 0.7], sigma = 0.36 percentage point, so 1.28*sigma = 0.46 percentage point. I widen to a 0.7 point half-width, about 1.5x the recent-sample half-width, because July first-print transportation and aircraft shipments can be lumpy and the five-month sample is quiet. Rounded 80% interval: 0.4 - 0.7 = -0.3 and 0.4 + 0.7 = 1.1."},{"kind":"text","text":"Variant discipline: every quantitative anchor above is for seasonally adjusted durable-goods manufacturers' shipments or same-table SA durable components from the Census M3 Advance Report/Table 1, not not-seasonally-adjusted shipments, full-report revisions, or durable-goods new orders as the target variable."},{"kind":"text","text":"Counter-considerations: upside risk is a July catch-up in transportation or aircraft shipments plus continued strong core capital-goods shipments, which would land above the interval if total shipments rose more than +1.1%. Downside risk is a vehicle/aircraft reversal or weaker tariff-related factory throughput, which would land below the interval if total shipments fell more than -0.3%. Outside the interval would most likely require a transportation-led swing rather than normal month-to-month drift in nontransport durable categories."},{"kind":"forecast","point":0.4,"ciLow":-0.3,"ciHigh":1.1}]}

# Reviewer critique
{"summary":"The draft is publishable on the main resolver/date/unit/coherence checks, with only minor strengthening needed around the breadth of the prior and volatility basis.","requiredFixes":[],"optionalSuggestions":["Broaden or explicitly contextualize the five-month persistence sample with a longer same-series base rate so the mean-reversion adjustment is better grounded.","Clarify that the July MoM calculation should use the July first-print vintage and the prior-month level available in that same first-print release if that is the resolver convention."]}

Emit the final JSON object only.
