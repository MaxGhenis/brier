# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.m3.durable_goods_new_orders_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-durable-goods-orders-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "census.m3.durable_goods_new_orders_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-31", "start": "2026-08-23"}, "field": "DGORDER", "releasePolicy": "first_print", "sourceSeriesId": "DGORDER", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGORDER", "table": "Advance Report on Durable Goods Manufacturers' Shipments, Inventories, and Orders", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-d6f28095537ab7cb8796d55dd43d50e385eeed4b422bded333bedb06d0e4f3b7.json"
- targetContentHash: "d6f28095537ab7cb8796d55dd43d50e385eeed4b422bded333bedb06d0e4f3b7"
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
{"slug":"us-durable-goods-orders-mom-july-2026","country":"US","type":"data","title":"US durable goods orders MoM, July 2026","question":"What will the U.S. Census Bureau first print report for July 2026 seasonally adjusted durable goods manufacturers' new orders month-over-month percent change?","unit":"percent_growth","pointEstimate":0.4,"ciLow":-5.2,"ciHigh":6,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"U.S. Census Bureau M3 Advance Report / ALFRED DGORDER first vintage","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGORDER","resolutionRule":"Resolve to the first-print month-over-month percent change for seasonally adjusted Total Durable Goods New Orders for July 2026 in the U.S. Census Bureau Advance Report on Durable Goods Manufacturers' Shipments, Inventories, and Orders, mirrored as DGORDER original vintage. Use the one-decimal percentage-point value as first published on 2026-08-26; ignore later revisions, full-report updates, and annual benchmark changes.","dataPointId":"census.m3.durable_goods_new_orders_mom.2026_07.first_print","historicalContext":[{"label":"2026-06 headline new orders MoM first print","value":0.3},{"label":"2026-05 headline new orders MoM revised in June advance","value":-4},{"label":"2026-04 headline new orders MoM revised in June advance","value":8.5},{"label":"2026-06 excluding transportation new orders MoM","value":0.6},{"label":"2026-06 nondefense capital goods excluding aircraft new orders MoM","value":0.9}],"drivers":["June headline stabilized after May aircraft-led reversal","Ex-transportation orders still positive","Aircraft and defense orders create wide month-to-month dispersion","Core capital-goods orders point to ongoing equipment demand"],"sourceContext":["https://www.census.gov/manufacturing/m3/release_schedule.html","https://www.census.gov/manufacturing/m3/adv/current/index.html","https://www.census.gov/manufacturing/m3/adv/pdf/table1a.pdf","https://www.census.gov/manufacturing/m3/historical_data/pressreleases/adv/2026/may26adv.pdf","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGORDER"],"runAt":"2026-07-31T15:00:45Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 durable goods new orders MoM"},{"kind":"text","text":"Framing and exact resolver: this targets the seasonally adjusted Total Durable Goods New Orders month-over-month percent change, not the not-seasonally-adjusted level, not ex-transportation, and not the later full-report revision. The ledger uses DGORDER with first_print policy; I keep that resolver and use Census M3 advance-table evidence for the same variant."},{"kind":"tool","tool":"official.lookup","call":"Checked the Census M3 release schedule for the July 2026 survey month.","result":"The official schedule lists June 2026 advance release on 7/27/2026, July 2026 advance release on 8/26/2026, and August 2026 advance release on 9/25/2026."},{"kind":"tool","tool":"official.lookup","call":"Read the current June 2026 Census advance press release and Table 1 for durable goods new orders.","result":"June 2026 durable goods new orders increased $1.1 billion or 0.3% to $334.8 billion; Table 1 shows Total New Orders 334,772 million, May 333,706 million, April 347,767 million, with monthly changes 0.3%, -4.0%, and 8.5%."},{"kind":"tool","tool":"official.lookup","call":"Read the June 2026 component detail in Census advance Table 1.","result":"June 2026 excluding transportation new orders rose 0.6% to 220,940 million; excluding defense rose 0.3% to 308,542 million; computers and electronic products rose 3.1% to 31,099 million; transportation equipment fell 0.2% to 113,832 million."},{"kind":"tool","tool":"official.lookup","call":"Read the May 2026 historical Census advance release for the recent reference-class path and volatility.","result":"The May 2026 release reported May new orders -4.5% to $332.1 billion after April +8.5%; its 2025-2026 chart gave monthly changes including Jun-25 -9.4%, Jul-25 -2.8%, Aug-25 3.0%, Sep-25 0.6%, Oct-25 -2.1%, Nov-25 5.4%, Dec-25 -0.9%, Jan-26 -0.4%, Feb-26 -1.2%, Mar-26 1.3%, Apr-26 8.5%, and May-26 -4.5%."},{"kind":"text","text":"Base rate / reference class: durable-goods headline MoM is a high-variance flow series because aircraft and defense orders can swing the aggregate. The recent official reference class is centered near zero: the Jun-25 through Jun-26 values average about -0.17 percentage points, while the non-transport June reading at +0.6% and core capital-goods excluding aircraft at +0.9% argue against treating the May drop as persistent weakness."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class prior is the recent headline mean, using official Jun-25 through Jun-26 monthly changes [-9.4, -2.8, 3.0, 0.6, -2.1, 5.4, -0.9, -0.4, -1.2, 1.3, 8.5, -4.5, 0.3], mean = -0.17. Updates: +0.3 pp for June headline stabilization, +0.2 pp for ex-transport/core-capital strength, and +0.1 pp for partial mean reversion after the May/April aircraft whipsaw, giving point = 0.4. For a change/flow target I size dispersion from the values themselves: sample sigma = 4.4 percentage points, so 1.28*sigma = 5.6; point 0.4 +/- 5.6 gives an 80% interval of -5.2 to 6.0."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed aircraft or defense-order surge like April 2026, which would land above the interval if transportation orders jump sharply. Downside risk is another aircraft cancellation or broad transportation reversal like May 2026, which would land below the interval. Outside the interval would require a move larger than the recent non-aircraft trend can explain, so it would most likely be transportation/aircraft-specific rather than broad manufacturing momentum."},{"kind":"forecast","point":0.4,"ciLow":-5.2,"ciHigh":6}]}

# Reviewer critique
{"summary":"The draft is publishable with no blocking issues; it names the first-print resolver, uses a recent official reference-class prior, and keeps point/interval/JSON fields coherent.","requiredFixes":[],"optionalSuggestions":["Clarify that ALFRED DGORDER is the mirror used for the ledger resolver while Census is the official origin source.","Consider noting why the volatility sample mixes or prefers first-print values, since May appears as -4.5 in the interval sample but -4.0 in the revised historical context."]}

Emit the final JSON object only.
