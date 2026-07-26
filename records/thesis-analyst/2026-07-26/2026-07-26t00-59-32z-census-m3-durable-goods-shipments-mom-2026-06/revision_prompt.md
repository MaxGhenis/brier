# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.m3.durable_goods_shipments_mom
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-durable-goods-shipments-mom-june-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "census.m3.durable_goods_shipments_mom.2026_06.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-27", "start": "2026-07-27"}, "field": "AMDMVS", "releasePolicy": "first_print", "sourceSeriesId": "AMDMVS", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=AMDMVS", "table": "Advance Report on Durable Goods Manufacturers' Shipments, Inventories, and Orders", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-a6868d95ca561112a7f2dfdd67d57d7a814c370e0af78dca4c81aa75a5272e3f.json"
- targetContentHash: "a6868d95ca561112a7f2dfdd67d57d7a814c370e0af78dca4c81aa75a5272e3f"
- registrationCommit: "145f6612f225710a4621f124b13bf5d5ae5d97ac"
- registeredAtUtc: "2026-07-26T00:55:04Z"

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
{"slug":"us-durable-goods-shipments-mom-june-2026","country":"US","type":"data","title":"US Durable Goods Shipments MoM, Jun 2026","question":"First-print month-over-month percent growth in U.S. Census Bureau M3 Manufacturers' Value of Shipments: Durable Goods (AMDMVS), seasonally adjusted, for June 2026.","unit":"percent_growth","pointEstimate":0.6,"ciLow":-0.22,"ciHigh":1.42,"confidence":0.8,"resolutionDate":"2026-07-27","resolutionSource":"U.S. Census Bureau M3 Advance Report, mirrored in ALFRED/FRED series AMDMVS","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=AMDMVS","resolutionRule":"Use the first official June 2026 print released with the Census M3 Advance Report on Durable Goods at 8:30 a.m. on 2026-07-27. Resolve as 100*(June 2026 seasonally adjusted AMDMVS level minus May 2026 seasonally adjusted AMDMVS level)/(May 2026 seasonally adjusted AMDMVS level), in percent, using the first-print vintage; later revisions do not change resolution. The ledger sourceBinding points to AMDMVS with a multiply transform even though the target unit is percent_growth, so the forecast is tied to the same target and interprets the target as the month-over-month percent growth implied by AMDMVS levels.","dataPointId":"census.m3.durable_goods_shipments_mom.2026_06.first_print","historicalContext":[{"label":"2026-05 m/m from AMDMVS levels","value":1.0044093014090059},{"label":"2026-04 m/m from AMDMVS levels","value":0.6838995293927989},{"label":"2026-03 m/m from AMDMVS levels","value":0.7933804757783034},{"label":"2026-02 m/m from AMDMVS levels","value":1.5626834740827487},{"label":"2026-05 AMDMVS level, millions USD SA","value":328030}],"drivers":["Recent AMDMVS shipments momentum was positive through May 2026","Durable-goods shipments are volatile but less aircraft-order-driven than new orders","Mean reversion from unusually firm early-2026 monthly gains","First-print target uses seasonally adjusted AMDMVS levels and excludes later revisions"],"sourceContext":["https://www.census.gov/manufacturing/m3/release_schedule.html","https://fred.stlouisfed.org/data/AMDMVS","https://fred.stlouisfed.org/series/AMDMVS","https://alfred.stlouisfed.org/series?seid=AMDMVS"],"runAt":"2026-07-26T00:59:51Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 Durable Goods Shipments MoM"},{"kind":"text","text":"Framing and exact resolver: the target is Census M3 durable-goods shipments, seasonally adjusted AMDMVS, June 2026 first print. The Census release schedule verifies the June 2026 Advance Report date as 2026-07-27, with the Full Report on 2026-08-04; I use the advance first print only."},{"kind":"tool","tool":"official.lookup","call":"Opened Census M3 release schedule for June 2026 advance and full report dates.","result":"Fetched schedule row: June 2026 Advance Report on Durable Goods and Advance Total Manufacturing = 7/27/2026 at 8:30 a.m.; Full Report = 8/4/2026 at 10:00 a.m."},{"kind":"tool","tool":"official.lookup","call":"Opened FRED/ALFRED AMDMVS series page to verify series identity, source, units, latest observation, and next release.","result":"Fetched AMDMVS identity: Manufacturers' Value of Shipments: Durable Goods; source U.S. Census Bureau; units Millions of Dollars, Seasonally Adjusted; latest May 2026 = 328,030; next release date = Jul 27, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened FRED table data for AMDMVS and read recent levels used to compute same-variant month-over-month growth.","result":"Fetched AMDMVS levels, millions of dollars SA: Dec 2025 = 312,260; Jan 2026 = 315,099; Feb 2026 = 320,023; Mar 2026 = 322,562; Apr 2026 = 324,768; May 2026 = 328,030."},{"kind":"tool","tool":"calculator","call":"Computed recent month-over-month percent changes from fetched AMDMVS levels.","result":"Fetched-level calculations: Feb 2026 m/m = 100*(320,023-315,099)/315,099 = 1.5627; Mar 2026 = 0.7934; Apr 2026 = 0.6839; May 2026 = 1.0044 percent."},{"kind":"text","text":"Variant discipline: every anchor is AMDMVS, Manufacturers' Value of Shipments: Durable Goods, seasonally adjusted, monthly. I did not mix not-seasonally-adjusted shipments, new orders, excluding-transportation series, or full-report revisions into the first-print target."},{"kind":"text","text":"Base rate/reference class: the 2024-02 through 2026-05 AMDMVS month-over-month changes have a mean of 0.455 percentage points, while the latest four reported changes were all positive at 1.563, 0.793, 0.684, and 1.004 percent, so the base rate is modest positive growth with unusually firm recent momentum."},{"kind":"math","text":"Prior/update/interval: persistence prior is the 2024-02 to 2026-05 AMDMVS m/m reference class. Historical sample = 28 monthly percent changes computed from fetched AMDMVS levels; mean = 0.455. Adjustment components: +0.20 for broad early-2026 positive momentum, -0.05 for mean reversion after four consecutive gains, giving point = 0.60. Interval method uses realized dispersion of the m/m percent changes: sum of squares = 16.9229, sigma = sqrt((16.9229 - 28*0.4550^2)/27) = 0.642 percentage points, so 1.28*sigma = 0.822; point 0.60 +/- 0.82 gives [-0.22, 1.42]."},{"kind":"text","text":"Counter-consideration: upside risk is a stronger transportation-equipment or machinery shipment month that would land above the interval, especially if June catches delayed May shipments. Downside risk is a pullback after the strong January-May level rise or a volatile transportation drop; a broad reversal below about -0.22 percent would land outside the interval on the low side."},{"kind":"forecast","point":0.6,"ciLow":-0.22,"ciHigh":1.42}]}

# Reviewer critique
{
  "summary": "The draft is publication-ready with no blocking issues; it correctly ties the forecast to the ledger target while noting the AMDMVS level-versus-percent-growth binding discrepancy.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider making the time-series prior label more explicit, e.g. simple mean-plus-momentum model rather than persistence prior, since the point is not a pure last-value persistence forecast.",
    "Clarify that the May denominator should be the May value in the same first-print June 2026 vintage if that is the resolver convention."
  ]
}

Emit the final JSON object only.
