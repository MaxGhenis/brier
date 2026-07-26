# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.m3.durable_goods_new_orders_mom
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-durable-goods-orders-mom-june-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "census.m3.durable_goods_new_orders_mom.2026_06.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-27", "start": "2026-07-27"}, "field": "DGORDER", "releasePolicy": "first_print", "sourceSeriesId": "DGORDER", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGORDER", "table": "Advance Report on Durable Goods Manufacturers' Shipments, Inventories, and Orders", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-270b7d2d593a239ac3373efdb5ec9fa3809df3e9eb60f5b3e1bc8120e239921b.json"
- targetContentHash: "270b7d2d593a239ac3373efdb5ec9fa3809df3e9eb60f5b3e1bc8120e239921b"
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
{"slug":"us-durable-goods-orders-mom-june-2026","country":"US","type":"data","title":"US durable goods orders MoM, June 2026","question":"What will the U.S. Census Bureau first report for seasonally adjusted manufacturers' new orders for durable goods (DGORDER), month-over-month percent growth, for June 2026?","unit":"percent_growth","pointEstimate":1.8,"ciLow":-4.8,"ciHigh":8.4,"confidence":0.8,"resolutionDate":"2026-07-27","resolutionSource":"ALFRED/FRED vintage mirror of the U.S. Census Bureau M3 Advance Report on Durable Goods Manufacturers' Shipments, Inventories, and Orders","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGORDER","resolutionRule":"Use the first-print June 2026 seasonally adjusted DGORDER observation released with the Census M3 Advance Report on July 27, 2026. Convert the first-print level to month-over-month percent growth versus the May 2026 first-print DGORDER level as 100*(June/May - 1), reported in percentage points. Later M3 full-report values, benchmark revisions, and subsequent ALFRED vintages do not replace the first print.","dataPointId":"census.m3.durable_goods_new_orders_mom.2026_06.first_print","historicalContext":[{"label":"May 2026 first advance MoM","value":-4.5},{"label":"April 2026 MoM","value":8.5},{"label":"March 2026 MoM from DGORDER levels","value":1.3},{"label":"February 2026 MoM from DGORDER levels","value":-1.2},{"label":"January 2026 MoM from DGORDER levels","value":-0.4}],"drivers":["May transport drop leaves rebound risk","June ISM new orders still expanding","Manufacturing output flat in June","Aircraft orders make headline series volatile","Exports and prices temper the upside"],"sourceContext":["https://www.census.gov/manufacturing/m3/release_schedule.html","https://www.census.gov/economic-indicators/calendar-listview.html?sec_ak_reference=18.52333b8.1542589455.5b7ef1e9","https://www.census.gov/manufacturing/m3/adv/current/index.html","https://fred.stlouisfed.org/series/DGORDER","https://www.ismworld.org/supply-management-news-and-reports/reports/ism-pmi-reports/pmi/june/","https://www.federalreserve.gov/Releases/g17/current/default.htm?mod=article_inline","https://boeing.mediaroom.com/2026-07-14-Boeing-Announces-Second-Quarter-Deliveries","https://flightplan.forecastinternational.com/2026/07/14/airbus-and-boeing-report-june-2026-commercial-aircraft-orders-and-deliveries/"],"runAt":"2026-07-26T00:57:04Z","reasoning":[{"kind":"heading","text":"US durable goods orders MoM, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this targets the Census M3 Advance Report headline series for manufacturers' new orders for durable goods, seasonally adjusted, FRED/ALFRED series code DGORDER. The ledger source binding points to ALFRED DGORDER; I am forecasting the first-print month-over-month percent growth for June 2026, not the later full M3 revision."},{"kind":"tool","tool":"official.lookup","call":"Checked Census M3 release schedule and Census economic indicators calendar for the June 2026 advance durable goods release date.","result":"Census lists Survey Month June 2026 with Advance Report on Durable Goods and Advance Total Manufacturing on 7/27/2026 at 8:30 a.m.; the full report is listed for 8/4/2026. The calendar-list view also lists Advance Report on Durable Goods--Manufacturers' Shipments, Inventories, and Orders on July 27, 2026 at 8:30 AM for period June 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the current Census M3 advance durable goods release for the latest first-print reference point.","result":"The June 25, 2026 Census advance report said May 2026 new orders for manufactured durable goods decreased $15.6 billion, or 4.5 percent, to $332.1 billion; April increased 8.5 percent; excluding transportation, new orders increased 1.3 percent; transportation equipment decreased $18.5 billion, or 14.0 percent, to $113.5 billion."},{"kind":"tool","tool":"fred.lookup","call":"Checked DGORDER recent levels from the public FRED/ALFRED mirror of Census M3.","result":"FRED DGORDER showed May 2026 = 332,050 million dollars, April 2026 = 347,618, March 2026 = 320,485, February 2026 = 316,233, and January 2026 = 319,975; these imply approximate MoM changes of May -4.5 percent, April +8.5 percent, March +1.3 percent, February -1.2 percent, and January -0.4 percent."},{"kind":"tool","tool":"survey.lookup","call":"Checked June manufacturing demand indicators before the durable goods release.","result":"ISM's June 2026 Manufacturing PMI was 53.3 percent, down 0.7 point from May 54.0; the New Orders Index was 56.0, down 0.8 point from May 56.8; Production was 52.2, down 2.1 points from May 54.3; Backlog of Orders was 50.5, down 1.7 points from May 52.2."},{"kind":"tool","tool":"official.lookup","call":"Checked June industrial production and aircraft-related public data for transport and production context.","result":"The Federal Reserve G.17 release reported June 2026 industrial production +0.1 percent and manufacturing output unchanged at 0.0 percent. Boeing reported 171 commercial airplane deliveries in Q2 2026 and 314 year-to-date; public June aircraft order coverage reported Boeing booked 121 gross commercial aircraft orders and delivered 64 jets in June."},{"kind":"text","text":"Base rate / reference class: using the recent DGORDER monthly percent changes from January 2024 through May 2026 gives a volatile 29-observation reference class with mean about +0.47 percentage point and sigma about 5.15 percentage points. The series is dominated by aircraft and other transportation swings, so the May transportation drop and June aircraft order rebound matter more than a smooth manufacturing trend."},{"kind":"math","text":"Prior/update/interval: persistence prior is the 2024-01 to 2026-05 DGORDER MoM base rate mean of +0.47 pp. I add +1.3 pp for transport/aircraft rebound after May's -14.0 percent transportation drop and June Boeing order strength, +0.4 pp for ISM new orders at 56.0, subtract 0.2 pp for flat Fed manufacturing output, and subtract 0.2 pp for softer exports/prices drag, giving +1.8 percent. Interval method uses realized dispersion of DGORDER MoM values themselves: sigma = 5.15, so 80 percent half-width is roughly 1.28*sigma = 1.28*5.15 = 6.59 pp; +1.8 +/- 6.6 gives [-4.8, 8.4] after rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a much larger-than-assumed aircraft booking print or defense capital-goods jump, which would land above the interval if total orders rise more than about 8.4 percent. Downside risk is that June aircraft orders do not translate into Census M3 timing, or nontransport durable categories reverse despite ISM breadth, which would land below the interval if total orders fall more than about 4.8 percent."},{"kind":"forecast","point":1.8,"ciLow":-4.8,"ciHigh":8.4}]}

# Reviewer critique
{
  "summary": "The draft satisfies the publication rubric with a clear first-print resolver, stated base-rate prior, explicit update math, volatility-based interval, and coherent JSON fields.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider naming the exact ALFRED vintage date expected for the July 27, 2026 first print if the pipeline depends on vintage selection.",
    "Consider clarifying that FRED/ALFRED is only the ledger mirror and that the underlying statistical release is the Census M3 Advance Report."
  ]
}

Emit the final JSON object only.
