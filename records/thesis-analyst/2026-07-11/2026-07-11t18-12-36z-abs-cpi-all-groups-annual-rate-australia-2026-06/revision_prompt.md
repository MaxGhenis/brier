# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: abs.cpi.all_groups_annual_rate.australia
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "abs-cpi-all-groups-annual-rate-australia-june-2026"
- country: "AU"
- targetUnit: "percent"
- dataPointId: "abs.cpi.all_groups_annual_rate.australia.june_2026.first_print"
- resolutionSourceUrl: "https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["data.api.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-07-28", "start": "2026-07-20"}, "field": "CPI/3.10001.10.50.M", "releasePolicy": "first_print", "sourceSeriesId": "CPI/3.10001.10.50.M", "sourceUrl": "https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata", "table": "Monthly Consumer Price Index (complete monthly CPI, dataflow CPI: annual change, all groups, original, weighted average of eight capital cities)", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-11-27a452d7e21646679c3fb7aaa3ae1761853c56d8fd4f34d9fcdd30adf7c9ab13.json"
- targetContentHash: "27a452d7e21646679c3fb7aaa3ae1761853c56d8fd4f34d9fcdd30adf7c9ab13"
- registrationCommit: "357f4e8477327d91775a345ece531f3eb42fa3b7"
- registeredAtUtc: "2026-07-11T18:10:24Z"

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
{"slug":"abs-cpi-all-groups-annual-rate-australia-june-2026","country":"AU","type":"data","title":"Australia CPI annual rate, June 2026","question":"What will the ABS first print for the annual percentage change in the original All groups CPI, weighted average of eight capital cities, for June 2026?","unit":"percent","pointEstimate":4.2,"ciLow":3.6,"ciHigh":4.8,"confidence":0.8,"resolutionDate":"2026-07-29","resolutionSource":"Australian Bureau of Statistics Consumer Price Index, Australia release and Data API","resolutionSourceUrl":"https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata","resolutionRule":"Resolve to the first value published by the Australian Bureau of Statistics for June 2026 annual change in the original All groups CPI, weighted average of eight capital cities, series CPI/3.10001.10.50.M. Use the first print as displayed to one decimal percentage point; later revisions do not change resolution.","dataPointId":"abs.cpi.all_groups_annual_rate.australia.june_2026.first_print","historicalContext":[{"label":"December 2025 annual CPI","value":3.8},{"label":"January 2026 annual CPI","value":3.8},{"label":"February 2026 annual CPI","value":3.7},{"label":"March 2026 annual CPI","value":4.6},{"label":"April 2026 annual CPI","value":4.2},{"label":"May 2026 annual CPI","value":4.0}],"drivers":["Persistence near May's 4.0% annual rate","Sticky housing inflation","Reversal of May transport and travel price falls","Food and tobacco inflation remain firm","Favorable but diminishing transport base effects"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/may-2026","https://www.abs.gov.au/release-calendar/future-releases-calendar/202607","https://data.api.abs.gov.au/rest/data/CPI/3.10001.10.50.M?lastNObservations=30&format=jsondata"],"runAt":"2026-07-11T18:12:53Z","reasoning":[{"kind":"heading","text":"Australia June 2026 annual CPI forecast"},{"kind":"text","text":"The target is the first-print June 2026 annual change in the original, not seasonally adjusted, All groups CPI for the weighted average of eight capital cities. Resolution uses ABS series CPI/3.10001.10.50.M and retains the first published one-decimal value without revision grace."},{"kind":"tool","tool":"official.lookup","call":"Fetch the ABS May 2026 Consumer Price Index release and its All groups annual history.","result":"ABS reported annual All groups CPI of 3.8% in December 2025, 3.8% in January 2026, 3.7% in February, 4.6% in March, 4.2% in April, and 4.0% in May."},{"kind":"tool","tool":"official.lookup","call":"Fetch the ABS May 2026 release's monthly and component movements for the exact original CPI variant.","result":"The original All groups CPI fell 0.7% in May 2026; annual Housing inflation was 6.5%, Food 3.3%, Transport 3.3%, and Alcohol and tobacco 4.7%."},{"kind":"tool","tool":"official.lookup","call":"Check the ABS July 2026 release calendar and May publication's future-release schedule.","result":"The official ABS schedule lists Consumer Price Index, Australia, June 2026 for 29 July 2026 at 11:30am Canberra time; the May release also states next release 29/07/2026."},{"kind":"text","text":"The official 29 July date conflicts with the registered sourceBinding expectedReleaseWindow ending 28 July. I retain the same target but use 29 July 2026 because it is the concrete date verified from the official calendar this run."},{"kind":"text","text":"The reference class/base rate is persistence in the same original annual series. The 14 observations from April 2025 through May 2026 were 2.4%, 2.1%, 1.9%, 3.0%, 3.2%, 3.6%, 3.8%, 3.4%, 3.8%, 3.8%, 3.7%, 4.6%, 4.2%, and 4.0%; their mean successive change was +0.12 percentage point."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms point to a modest rebound: the level remains elevated at 4.0%; recent momentum eased from March's 4.6%; May's original 0.7% monthly fall included sharp Transport and Recreation declines that may partly reverse; Housing at 6.5% and administered or indexed prices keep underlying pressure firm. No mid-2026 CPI weight update is scheduled."},{"kind":"math","text":"Prior/update/interval: persistence prior = May's 4.0%; historical sample = the 14 same-variant annual rates from April 2025 to May 2026. Add +0.12 percentage point from the historical mean successive change, about +0.10 for partial reversal of May's transport/travel weakness and sticky housing, and about -0.02 for recent disinflation, giving 4.20%, rounded to 4.2%. Across the 13 successive annual-rate changes, sigma = 0.476 percentage point. The normal 80% half-width is 1.28*sigma = 1.28*0.476 = 0.610, so 4.2% ± 0.61 rounds to implied bounds of 3.6% and 4.8%."},{"kind":"text","text":"Upside risk comes from a larger fuel, travel, or housing rebound and would land above the interval if annual CPI exceeds 4.8%. Downside risk comes from renewed fuel declines, discounting, or faster goods disinflation and would land below the interval if CPI is under 3.6%. These are the concrete outside-the-interval scenarios."},{"kind":"forecast","point":4.2,"ciLow":3.6,"ciHigh":4.8}]}

# Reviewer critique
{
  "summary": "Draft is publication-ready; it identifies the ABS first-print resolver, states a persistence prior, gives a coherent update and volatility-based 80% interval, and flags the ledger release-window discrepancy explicitly.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider adding the exact ABS release time only if the schema has a place for it; the current resolutionDate and reasoning are sufficient.",
    "If the publisher treats the ledger expectedReleaseWindow as authoritative, separately correct that registration metadata rather than changing this forecast target."
  ]
}

Emit the final JSON object only.
