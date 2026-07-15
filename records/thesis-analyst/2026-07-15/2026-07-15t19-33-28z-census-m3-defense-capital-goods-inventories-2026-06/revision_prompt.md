# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.m3.defense_capital_goods.inventories
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-defense-capital-goods-inventories-june-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "census.m3.defense_capital_goods.inventories.2026_06.first_print"
- resolutionSourceUrl: "https://www.census.gov/manufacturing/m3/adv/current/index.html"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.census.gov"], "expectedReleaseWindow": {"end": "2026-07-27", "start": "2026-07-27"}, "field": "Defense capital goods; Inventories; seasonally adjusted; preliminary June 2026 value", "releasePolicy": "first_print", "sourceSeriesId": "M3_ADV_TABLE2_DEFENSE_CAPITAL_GOODS_INVENTORY_SA", "sourceUrl": "https://www.census.gov/manufacturing/m3/adv/current/index.html", "table": "Monthly Advance Report on Durable Goods Manufacturers' Shipments, Inventories and Orders, Table 2 - Unfilled Orders and Inventory", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-15-8dd3078fe13d3af0a3b419b722d536b8642ab37d614e8373b70faea0c7284901.json"
- targetContentHash: "8dd3078fe13d3af0a3b419b722d536b8642ab37d614e8373b70faea0c7284901"
- registrationCommit: "05b56ed86beda8ccde0b2891912278d9ab065f09"
- registeredAtUtc: "2026-07-15T19:28:27Z"

# Source hints
- Use Census income, poverty, SPM, and health-insurance release pages, CPS ASEC historical tables, and the Census release calendar.
- For official-poverty targets, distinguish the official poverty measure from SPM and cite the exact Census table or report.
- For SPM targets, name the population group, calendar year, and whether taxes, credits, transfers, medical expenses, or housing adjustments matter for the forecast.

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
{"slug":"us-defense-capital-goods-inventories-june-2026","country":"US","type":"data","title":"US defense capital-goods inventories, June 2026","question":"What will the U.S. Census Bureau first report for seasonally adjusted defense capital goods total inventories in June 2026?","unit":"usd_billions","pointEstimate":28.35,"ciLow":28.22,"ciHigh":28.48,"confidence":0.8,"resolutionDate":"2026-07-27","resolutionSource":"U.S. Census Bureau Monthly Advance Report on Durable Goods Manufacturers' Shipments, Inventories and Orders","resolutionSourceUrl":"https://www.census.gov/manufacturing/m3/adv/current/index.html","resolutionRule":"Resolve to the preliminary June 2026 value for Defense capital goods; Total Inventories in Table 2 of the first U.S. Census Bureau June 2026 Advance Report, using the seasonally adjusted estimate in millions of dollars multiplied by 0.001 and rounded to three decimal places in USD billions. Ignore all later revisions and corrections not contained in that first print.","dataPointId":"census.m3.defense_capital_goods.inventories.2026_06.first_print","historicalContext":[{"label":"2026-01 first print, SA","value":27.82},{"label":"2026-02 first print, SA","value":27.877},{"label":"2026-03 first print, SA","value":28.088},{"label":"2026-04 first print, SA","value":28.121},{"label":"2026-05 first print, SA","value":28.257}],"drivers":["persistent nominal inventory accumulation","recent positive monthly momentum","defense aircraft and other long-cycle production inventories","survey and concurrent-seasonal-adjustment noise"],"sourceContext":["https://www.census.gov/manufacturing/m3/adv/current/index.html","https://www.census.gov/manufacturing/m3/adv/pdf/table2a.pdf","https://www.census.gov/manufacturing/m3/historical_data/pressreleases/adv/2026/jan26adv.pdf","https://www.census.gov/manufacturing/m3/historical_data/pressreleases/adv/2026/feb26adv.pdf","https://www.census.gov/manufacturing/m3/historical_data/pressreleases/adv/2026/mar26adv.pdf","https://www.census.gov/manufacturing/m3/historical_data/pressreleases/adv/2026/apr26adv.pdf","https://www.census.gov/economic-indicators/calendar-listview.html"],"runAt":"2026-07-15T19:34:10Z","reasoning":[{"kind":"heading","text":"June 2026 defense capital-goods inventories forecast"},{"kind":"text","text":"The resolver is Census M3 Advance Table 2 series M3_ADV_TABLE2_DEFENSE_CAPITAL_GOODS_INVENTORY_SA: preliminary June 2026 defense capital goods total inventories, seasonally adjusted, reported in millions and converted to USD billions. The first official print alone controls; later revisions do not."},{"kind":"text","text":"The Census economic-indicator calendar explicitly schedules the June 2026 Advance Report on Durable Goods for July 27, 2026 at 8:30 a.m. EDT, verifying the ledger resolution date rather than inferring it from monthly cadence."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest Census M3 May 2026 Advance Table 2 defense capital-goods inventory row.","result":"The official seasonally adjusted preliminary values were May 2026 28,257 million, revised April 2026 28,161 million, and March 2026 28,022 million; May rose 0.3%."},{"kind":"tool","tool":"official.lookup","call":"Fetch the Census January 2026 Advance Table 2 defense capital-goods inventory history.","result":"The official seasonally adjusted values shown were January 2026 27,820 million, December 2025 27,668 million, and November 2025 27,738 million."},{"kind":"tool","tool":"official.lookup","call":"Fetch first-print defense capital-goods inventories from the February, March, and April 2026 Census advance releases.","result":"The preliminary seasonally adjusted prints were February 2026 27,877 million, March 2026 28,088 million, and April 2026 28,121 million."},{"kind":"text","text":"Outside view/base rate: the seven-month first-print reference class from November 2025 through May 2026 is 27.738, 27.668, 27.820, 27.877, 28.088, 28.121, and 28.257 billion. Six monthly changes average +0.0865 billion and are positive in five of six months, favoring another moderate increase over pure level persistence."},{"kind":"text","text":"Level is anchored at May's 28.257 billion. Momentum contributes about +0.087 billion from the mean monthly change. No identified one-off warrants a large adjustment; the policy/production mechanism is gradual accumulation in long-cycle defense manufacturing, so the combined estimate is rounded to 28.350 billion."},{"kind":"math","text":"Prior/update/interval: persistence-plus-drift prior using the seven first-print observations from November 2025-May 2026; successive changes are -0.070, +0.152, +0.057, +0.211, +0.033, and +0.136 billion. Their mean is +0.0865 and sample sigma = 0.101 billion. Point = 28.257 + 0.0865 = 28.3435, rounded to 28.35. The normal 80% half-width is 1.28*sigma = 1.28*0.101 = 0.129 billion, giving 28.35 ± 0.13 = [28.22, 28.48]."},{"kind":"text","text":"Upside risk comes from unusually rapid accumulation tied to aircraft, missile, ship, or communications production and would land above the interval if June adds more than about 0.22 billion. Downside risk is a drawdown, delivery-driven liquidation, or noisy seasonal adjustment; a fall of more than about 0.04 billion from May would land below the interval. Either would be outside the interval and falsify the smooth-accumulation reference class."},{"kind":"forecast","point":28.35,"ciLow":28.22,"ciHigh":28.48}]}

# Reviewer critique
{"summary":"Draft is publishable with one minor coherence cleanup around rounding the computed point estimate.","requiredFixes":[{"rubricItem":"coherence","severity":"warning","summary":"The math step says 28.257 + 0.0865 = 28.3435, rounded to 28.35, but ordinary rounding to two decimals would give 28.34 and to three decimals 28.344.","actionRequested":"Either change the stated rounded point to 28.34/28.344 with matching interval fields, or explicitly justify the small discretionary upward rounding to 28.35."}],"optionalSuggestions":["Add the May 2026 advance release PDF explicitly to sourceContext if available, since the May value anchors the forecast.","Clarify that March/April values used in the historical sample are first-print values, distinct from any later revised values visible in the current table."]}

Emit the final JSON object only.
