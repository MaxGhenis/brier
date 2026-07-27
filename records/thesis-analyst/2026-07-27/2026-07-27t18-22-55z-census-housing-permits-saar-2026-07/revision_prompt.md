# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.housing.permits_saar
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-building-permits-july-2026"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "census.housing.permits_saar.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-18", "start": "2026-08-18"}, "field": "PERMIT", "releasePolicy": "first_print", "sourceSeriesId": "PERMIT", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PERMIT", "table": "New Residential Construction, seasonally adjusted annual rates", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-27-c7a4e40bb0cd9b0e5c28fbfbb3441e05bf8245b1c02cc5b13590b8e7d0f72cd2.json"
- targetContentHash: "c7a4e40bb0cd9b0e5c28fbfbb3441e05bf8245b1c02cc5b13590b8e7d0f72cd2"
- registrationCommit: "e494ebc7a9b410a6fcffab9e5439408ff3d09413"
- registeredAtUtc: "2026-07-27T18:01:44Z"

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
{"slug":"us-building-permits-july-2026","country":"US","type":"data","title":"US Building Permits, July 2026","question":"What will the U.S. Census Bureau first report for privately owned housing units authorized by building permits in July 2026, seasonally adjusted annual rate, in thousands?","unit":"thousands","pointEstimate":1375,"ciLow":1295,"ciHigh":1455,"confidence":0.8,"resolutionDate":"2026-08-18","resolutionSource":"ALFRED/FRED PERMIT first vintage, mirroring the Census New Residential Construction first print","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PERMIT","resolutionRule":"Resolve to the first ALFRED vintage for FRED series PERMIT for observation month 2026-07, in thousands of privately owned housing units authorized by building permits at a seasonally adjusted annual rate. Use the first print released with the Census New Residential Construction report on 2026-08-18; ignore later revisions, benchmarks, and revised-building-permits releases.","dataPointId":"census.housing.permits_saar.2026_07.first_print","historicalContext":[{"label":"2026-06 first print","value":1367},{"label":"2026-05 first print","value":1413},{"label":"2026-04 first print","value":1442},{"label":"2026-03 first print","value":1372}],"drivers":["June total permits fell to 1367 thousand SAAR","Recent first-print permits remain near the 1370-1440 thousand range","Mortgage rates and Treasury yields were elevated in late July","June starts rebounded, limiting downside from the latest permit drop","Multifamily permits are volatile and dominate month-to-month interval width"],"sourceContext":["https://www.census.gov/construction/bps/schedule.html","https://www.census.gov/economic-indicators/calendar-listview.html","https://www.census.gov/construction/nrc/current/index.html","https://www.census.gov/construction/nrc/current/","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PERMIT","https://myhome.freddiemac.com/buying/mortgage-rates","https://www.federalreserve.gov/releases/h15/default.htm"],"runAt":"2026-07-27T18:23:27Z","reasoning":[{"kind":"heading","text":"US July 2026 Building Permits First Print"},{"kind":"text","text":"Framing and exact resolver: the target is total privately owned housing units authorized by building permits, seasonally adjusted annual rate, measured in thousands, for July 2026. The ledger binds resolution to PERMIT first print via ALFRED; the agency source behind the print is Census/HUD New Residential Construction, and I am using the total SAAR variant throughout rather than single-family, multifamily-only, revised permits, or not-seasonally-adjusted permits."},{"kind":"tool","tool":"official.lookup","call":"Checked Census Building Permits Survey and Economic Indicators release calendars for New Residential Construction July 2026.","result":"Fetched release schedule: July 2026 New Residential Construction is scheduled for August 18, 2026 at 8:30 AM, with revised building permits scheduled for August 25, 2026; the Economic Indicators list view also shows New Residential Construction on August 18, 2026 at 8:30 AM for July 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked Census New Residential Construction current June 2026 release for latest total permits and related components.","result":"Fetched June 2026 first-print permits of 1,367,000 SAAR, 3.0 percent below revised May 2026 at 1,410,000 and 2.3 percent below June 2025 at 1,399,000; single-family authorizations were 871,000 and buildings with 5 units or more were 445,000; June starts were 1,427,000, up 19.0 percent from revised May."},{"kind":"tool","tool":"official.lookup","call":"Checked prior Census New Residential Construction releases and archived/search-indexed release text for the recent first-print reference class.","result":"Fetched May 2026 first-print permits of 1,413,000 SAAR, April 2026 first-print permits of 1,442,000 SAAR, and March 2026 first-print permits of 1,372,000 SAAR; April's release also cited March revised at 1,363,000, while the first-print March value used here is 1,372,000."},{"kind":"tool","tool":"market.lookup","call":"Checked public rate context from Freddie Mac PMMS and Federal Reserve H.15 because permits are interest-rate sensitive.","result":"Fetched Freddie Mac average 30-year fixed mortgage rate of 6.58 percent as of July 23, 2026 and 15-year fixed rate of 5.96 percent; fetched Federal Reserve H.15 10-year Treasury constant maturity values of 4.55 on July 17, 4.60 on July 20, and 4.63 on July 21, 2026."},{"kind":"text","text":"Base rate/reference class: for this monthly level series, the starting base rate is persistence from the latest same-variant first print, 1367 thousand, cross-checked against the recent four-month first-print average of (1372 + 1442 + 1413 + 1367) / 4 = 1398.5 thousand. The recent range is narrow by housing-cycle standards but month-to-month multifamily swings make the next print noisy."},{"kind":"math","text":"Prior/update/interval: persistence prior = 1367 from June 2026 first print; historical sample = first-print total SAAR permits for March-June 2026 of 1372, 1442, 1413, 1367; adjustment components = +8 thousand partial mean reversion toward the 1398.5 four-month average, -5 thousand for elevated mortgage/Treasury rates, +5 thousand because June starts strength and multifamily volatility argue against extrapolating the full June drop; final point = 1367 + 8 = 1375. Successive changes are +70, -29, -46; sample standard deviation of these changes gives sigma = 62.6 thousand, and 1.28*sigma = 80.2 thousand, so the rounded 80 percent interval is 1375 +/- 80 = [1295, 1455]."},{"kind":"text","text":"Upside risk: a rebound in multifamily applications similar to April's jump, easing local bottlenecks, or builders pulling permits before financing costs rise further would land above the interval. Downside risk: another leg up in mortgage rates, weak single-family demand, or a large reversal in five-plus-unit permits would land below the interval. Outside the interval would require roughly an 80 thousand move from the 1375 center, which is larger than two of the last three monthly changes but still plausible in this series."},{"kind":"forecast","point":1375,"ciLow":1295,"ciHigh":1455}]}

# Reviewer critique
{"summary":"Draft is publication-ready with the ledger target, first-print resolver, prior/update/interval logic, tails, and JSON fields aligned.","requiredFixes":[],"optionalSuggestions":["Name the time-series prior explicitly as a random-walk/persistence model to make rubric item 3 easier to audit.","If space allows, state that Census links are evidence sources while ALFRED PERMIT first vintage remains the binding resolver."]}

Emit the final JSON object only.
