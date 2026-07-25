# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.trade.goods_services_deficit
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-goods-services-trade-deficit-july-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.trade.goods_services_deficit.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.bea.gov"], "expectedReleaseWindow": {"end": "2026-09-08", "start": "2026-08-31"}, "field": "BOPGSTB", "releasePolicy": "first_print", "sourceSeriesId": "BOPGSTB", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BOPGSTB", "table": "U.S. International Trade in Goods and Services, Exhibit 1", "transform": {"factor": -0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-25-406ea378939f61f263dd2ddc4e3ffd7534f5b5e6e0e8c94a228cbbeb28e7c8ac.json"
- targetContentHash: "406ea378939f61f263dd2ddc4e3ffd7534f5b5e6e0e8c94a228cbbeb28e7c8ac"
- registrationCommit: "add78fbd9af9ca9b0c7389a9a44a7ec839f2f4af"
- registeredAtUtc: "2026-07-25T15:18:08Z"

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

Emit the final JSON object only. (agent thesis.analyst v2.3.0, prompt 7ef119647b35, tools 5d0da8127872, promptMode fast)


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
{"slug":"us-goods-services-trade-deficit-july-2026","country":"US","type":"data","title":"US goods and services trade deficit, July 2026","question":"What will the first-print U.S. Census Bureau and BEA seasonally adjusted goods and services trade deficit be for July 2026, balance of payments basis, in billions of U.S. dollars?","unit":"usd_billions","pointEstimate":69,"ciLow":56.1,"ciHigh":81.9,"confidence":0.8,"resolutionDate":"2026-09-03","resolutionSource":"U.S. Census Bureau and U.S. Bureau of Economic Analysis, U.S. International Trade in Goods and Services","resolutionSourceUrl":"https://www.bea.gov/news/2026/us-international-trade-goods-and-services-july-2026","resolutionRule":"Resolve to the first-print seasonally adjusted goods and services balance in Exhibit 1 of the U.S. International Trade in Goods and Services release for July 2026, balance of payments basis, converted to a positive deficit in usd_billions and rounded to one decimal place. Use the initially released July 2026 value only; ignore later monthly, annual, benchmark, or same-series revisions.","dataPointId":"bea.trade.goods_services_deficit.2026_07.first_print","historicalContext":[{"label":"May 2026 deficit, latest FRED BOPGSTB mirror","value":77.585},{"label":"April 2026 deficit, revised in May release","value":54.57},{"label":"March 2026 deficit, FRED BOPGSTB mirror","value":56.585},{"label":"February 2026 deficit, FRED BOPGSTB mirror","value":54.98},{"label":"January 2026 deficit, FRED BOPGSTB mirror","value":54.185}],"drivers":["May goods deficit jumped to 106.5 while the services surplus was 28.9","Recent 2026 deficits before May clustered near 54-57 billion","May exports fell 10.5 and imports rose 12.5, so the latest level is partly a broad import/export shock","Nonmonetary gold and capital-goods components were unusually visible in the May movement","Two-month-ahead July forecast allows partial mean reversion but keeps a wider-than-normal deficit bias"],"sourceContext":["https://www.bea.gov/news/schedule/","https://www.bea.gov/node/42997","https://www.bea.gov/news/2026/us-international-trade-goods-and-services-may-2026","https://fred.stlouisfed.org/series/BOPGSTB","https://www.bea.gov/data/intl-trade-investment/international-trade-goods-and-services"],"runAt":"2026-07-25T16:06:12Z","reasoning":[{"kind":"heading","text":"Forecast: July 2026 U.S. goods and services trade deficit"},{"kind":"text","text":"Framing and exact resolver: this targets the July 2026 first print of the U.S. International Trade in Goods and Services headline goods-and-services balance, seasonally adjusted and on a balance of payments basis, reported in Exhibit 1. The ledger transform turns BOPGSTB's negative millions-of-dollars balance into a positive usd_billions deficit; the agency first print is authoritative over later revisions."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA 2026 release schedule and the BEA scheduled-release node for U.S. International Trade in Goods and Services, July 2026.","result":"BEA schedule lists U.S. International Trade in Goods and Services, July 2026 on September 3, 2026 at 8:30 a.m.; BEA node 42997 also shows Scheduled Date September 3 08:30 and Release Title July 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest official BEA/Census release for May 2026 to anchor the same variant and near-term components.","result":"May 2026 goods and services deficit was 77.6 billion, up 23.0 billion from April's revised 54.6 billion; exports were 317.7 billion and imports were 395.3 billion."},{"kind":"tool","tool":"official.lookup","call":"Read May 2026 release detail for goods/services decomposition and one-off movement clues.","result":"The May goods deficit increased 23.6 billion to 106.5 billion, the services surplus increased 0.6 billion to 28.9 billion, exports of goods decreased 11.3 billion to 210.6 billion, and imports of goods increased 12.3 billion to 317.0 billion."},{"kind":"tool","tool":"alfred_fred.lookup","call":"Fetched the public FRED mirror for BOPGSTB recent monthly observations, using it only as a history mirror while retaining BEA/Census as the resolution source.","result":"BOPGSTB observations were May 2026 -77,585 million, April 2026 -54,570 million, March 2026 -56,585 million, February 2026 -54,980 million, and January 2026 -54,185 million; converted positive deficits are 77.585, 54.570, 56.585, 54.980, and 54.185 usd_billions."},{"kind":"text","text":"Reference class and base rate: the same-variant 2026 monthly first/latest-reference sample after the annual-revision release context has a positive-deficit mean of about 59.6 billion, but May's 77.6 billion print says the immediate trade-flow regime is above that base rate. I use the recent 2026 base rate as the outside-view anchor and pull the two-month-ahead July point partway from May toward the January-April cluster."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2026 deficit 77.6; historical sample = Jan-May 2026 positive BOPGSTB deficits of 54.185, 54.980, 56.585, 54.570, 77.585; adjustment components = -6.0 for partial reversal of May's goods shock and gold/export weakness, -2.5 for import normalization toward the January-April cluster, -0.1 for a roughly stable services surplus near 28.9, giving 77.6 - 8.6 = 69.0. For this flow series I size dispersion from the values themselves: sample sigma = 10.1 usd_billions, so 80% half-width is about 1.28*sigma = 1.28*10.1 = 12.9; final bounds are 69.0 - 12.9 = 56.1 and 69.0 + 12.9 = 81.9."},{"kind":"text","text":"Counter-considerations: upside risk for a larger positive deficit would be another July import surge in consumer goods, autos, semiconductors, crude oil, or a further export slump, which would land above the interval if the deficit exceeds 81.9 billion. Downside risk would be a quick reversal of May's import jump, a rebound in goods exports, or weaker domestic demand for imported goods, which would land below the interval if the deficit is under 56.1 billion."},{"kind":"forecast","point":69,"ciLow":56.1,"ciHigh":81.9}]}

# Reviewer critique
{"summary":"Draft is publishable after clarifying the prior/update framing; resolver, unit, first-print rule, date, interval arithmetic, and JSON fields are otherwise coherent.","requiredFixes":[{"rubricItem":"base_rate","severity":"warning","summary":"The reasoning states a 2026 Jan-May mean base rate of about 59.6, but the compact math step switches to a May persistence prior of 77.6, so the outside-view prior is not consistently stated before updates.","actionRequested":"Revise the prior/update text to name one primary prior, or explicitly separate the base-rate prior from the persistence prior and show the bridge from 59.6 or 77.6 to the 69.0 point estimate."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact step includes the requested components, but the adjustment components are framed as inside-view movements from May while the preceding paragraph says the outside-view anchor is the recent 2026 base rate.","actionRequested":"Make the compact step internally consistent by listing: base-rate sample, chosen prior, why that prior dominates, update components, interval method, and bounds in the same order."}],"optionalSuggestions":["Consider saying the 5-month level sigma is a short-sample uncertainty proxy rather than realized forecast-error volatility.","The future BEA URL is plausible, but the reasoning should rely on the schedule/node and Exhibit 1 resolver rather than assuming the exact URL will resolve before publication."]}

Emit the final JSON object only.
