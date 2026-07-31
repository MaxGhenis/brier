# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.construction_spending.total_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-construction-spending-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "census.construction_spending.total_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-09-07", "start": "2026-08-30"}, "field": "TTLCONS", "releasePolicy": "first_print", "sourceSeriesId": "TTLCONS", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TTLCONS", "table": "Value of Construction Put in Place Survey", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-ad912c7b624a6bf7eceafefd874d2906976c63698e7d5ad68b9741aa2a778d7e.json"
- targetContentHash: "ad912c7b624a6bf7eceafefd874d2906976c63698e7d5ad68b9741aa2a778d7e"
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
{"slug":"us-construction-spending-mom-july-2026","country":"US","type":"data","title":"US construction spending MoM, July 2026","question":"What will the U.S. Census Bureau first print show for July 2026 total construction spending, month-over-month percent change, seasonally adjusted annual rate, for total construction?","unit":"percent_growth","pointEstimate":0.1,"ciLow":-0.8,"ciHigh":1.0,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Census Bureau Construction Spending release, mirrored through the registered ALFRED TTLCONS first-vintage binding","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TTLCONS","resolutionRule":"Resolve to the first official print for July 2026 total construction spending, seasonally adjusted annual rate, as the percent change from June 2026 to July 2026 implied by TTLCONS in the registered ALFRED first-vintage source. Use the first posted vintage only; do not incorporate later Census/FRED/ALFRED revisions or same-day corrections unless they are part of the initially posted release vintage. Round to one decimal percentage point, matching the Census/FRED percent-change display convention.","dataPointId":"census.construction_spending.total_mom.2026_07.first_print","historicalContext":[{"label":"May 2026 first/current print percent change","value":0.1},{"label":"Apr 2026 current percent change","value":0.3},{"label":"Mar 2026 current percent change","value":0.4},{"label":"Feb 2026 current percent change","value":-0.3},{"label":"Jan 2026 current percent change","value":-0.9}],"drivers":["recent total construction spending is near flat","private residential was positive in May","private nonresidential and manufacturing remain drags","public construction was positive in May","monthly construction spending changes have wide revision-prone dispersion"],"sourceContext":["https://www.census.gov/construction/c30/release.html","https://www.census.gov/construction/c30/current/index.html","https://fred.stlouisfed.org/series/MPCTXXXXS","https://fred.stlouisfed.org/data/MPCTXXXXS","https://fred.stlouisfed.org/release/tables?eid=22348&rid=229","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TTLCONS"],"runAt":"2026-07-31T15:07:10Z","reasoning":[{"kind":"heading","text":"July 2026 U.S. construction spending MoM first print"},{"kind":"text","text":"Framing and exact resolver: the target is the U.S. Census Bureau Value of Construction Put in Place Survey total construction series, seasonally adjusted annual rate, for July 2026. The canonical ledger binds resolution to ALFRED TTLCONS first_print even though Census is the official agency source; I use Census pages for schedule and release context, and keep the resolver tied to the registered ALFRED TTLCONS first-vintage rule."},{"kind":"tool","tool":"official.lookup","call":"Census Construction Spending release schedule lookup for the July 2026 reporting period","result":"Fetched schedule says Monthly Value of Construction Put in Place July releases on September 1, 2026 at 10:00 a.m.; June releases on August 3, 2026 and August releases on October 1, 2026."},{"kind":"tool","tool":"official.lookup","call":"Census current Construction Spending release lookup for the latest official context","result":"Fetched May 2026 release: total construction spending was $2,210.2 billion SAAR, 0.1 percent above revised April $2,207.1 billion, and 1.5 percent below May 2025 $2,244.4 billion."},{"kind":"tool","tool":"official.lookup","call":"FRED/Census MPCTXXXXS percent-change series lookup for recent monthly values","result":"Fetched MPCTXXXXS values: May 2026 0.1, Apr 2026 0.3, Mar 2026 0.4, Feb 2026 -0.3, Jan 2026 -0.9 percent change from preceding period, seasonally adjusted."},{"kind":"tool","tool":"official.lookup","call":"FRED release table lookup for total construction levels behind the percent-change target","result":"Fetched release table levels: total construction May 2026 2,210,214 million dollars, Apr 2026 2,207,051 million dollars, May 2025 2,244,426 million dollars."},{"kind":"text","text":"The release variant is total construction, seasonally adjusted annual rate, converted to month-over-month percent growth. The target is first print for July 2026, so later revisions to June or July should not be used when resolving."},{"kind":"text","text":"Reference class and base rate: recent monthly percent changes in total construction spending are centered close to zero. The 2024-08 through 2026-05 fetched/cached MPCTXXXXS sequence used for dispersion was 0.2, -0.3, 0.0, -0.2, -0.7, -0.3, -0.2, -0.7, 0.1, -0.2, 0.5, 0.4, 0.4, -0.4, -0.1, 0.6, 1.8, -1.9, -0.8, 0.2, 0.4, 0.1, giving a near-zero mean around -0.05 percentage point."},{"kind":"text","text":"Level, momentum, one-off, and policy-mechanism effects: the latest Census release shows nominal total spending barely positive, public construction positive, private residential positive, and private nonresidential soft. I do not see a clear one-off mechanism that should dominate the base rate by July; July is therefore anchored near flat rather than extrapolating the revised January drop or the December spike."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior is near 0.0 from the recent MPCTXXXXS reference class, with a small positive update from May total spending at +0.1 percent, private residential +0.3 percent, and public construction +0.5 percent, offset by private nonresidential -0.3 percent. I set point = 0.1. For the 22 recent percent-change observations listed above, mean is about -0.05 and sample sigma = 0.69 percentage point; 1.28*sigma = 0.88 percentage point, so an 80% interval around 0.1 is roughly -0.8 to 1.0 after rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in manufacturing, data centers, public infrastructure, or residential improvements that would land above the interval if July prints above 1.0 percent. Downside risk is a renewed private nonresidential/manufacturing pullback or sharper residential decline that would land below the interval if July prints below -0.8 percent."},{"kind":"forecast","point":0.1,"ciLow":-0.8,"ciHigh":1.0}]}

# Reviewer critique
{"summary":"Draft is publishable under the stated contract; resolver, prior/update logic, interval math, tails, and JSON fields are coherent with no blocking issues found.","requiredFixes":[],"optionalSuggestions":["Clarify whether the 22-observation volatility sample uses current revised MPCT values or first-vintage values, since the target resolves first print.","Add one explicit sentence that the time-series prior is a rolling recent-history/persistence prior and no separate AR or structural model is being used."]}

Emit the final JSON object only.
