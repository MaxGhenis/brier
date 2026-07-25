# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.housing_starts.saar
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "census-housing-starts-saar-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "census.housing_starts.saar.2026-07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.census.gov"], "expectedReleaseWindow": {"end": "2026-08-21", "start": "2026-08-13"}, "field": "HOUST", "releasePolicy": "first_print", "sourceSeriesId": "HOUST", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=HOUST", "table": "New Residential Construction, seasonally adjusted annual rates", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-25-073e7fcf7886b8c861d413549339410a956f2eb86554266f89fbeea6aa7bc373.json"
- targetContentHash: "073e7fcf7886b8c861d413549339410a956f2eb86554266f89fbeea6aa7bc373"
- registrationCommit: "add78fbd9af9ca9b0c7389a9a44a7ec839f2f4af"
- registeredAtUtc: "2026-07-25T15:18:08Z"

# Source hints
- Use Census income, poverty, SPM, and health-insurance release pages, CPS ASEC historical tables, and the Census release calendar.
- For official-poverty targets, distinguish the official poverty measure from SPM and cite the exact Census table or report.
- For SPM targets, name the population group, calendar year, and whether taxes, credits, transfers, medical expenses, or housing adjustments matter for the forecast.
- For ACS table targets, fetch each history year's values from the keyless JSON endpoint https://data.census.gov/api/access/data/table?id=<PRODUCT><YEAR>.<TABLE>&g=010XX00US (for example ACSDT1Y2024.B28005) and read the cited variable columns from the returned JSON.
- api.census.gov requires an API key (keyless requests redirect to missing_key.html); never rely on it in keyless runs, and never present remembered values as fetched ones.
- ACS vintage discipline: never mix 5-year estimates into a 1-year series — 5-year values lag the 1-year series by roughly two years; the product id in the fetch URL (ACSDT1Y vs ACSDT5Y) is the vintage authority.

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
{"slug":"census-housing-starts-saar-july-2026","country":"US","type":"data","title":"US housing starts SAAR, July 2026","question":"What will the Census/HUD first print of privately owned housing starts, total units, seasonally adjusted annual rate, be for July 2026?","unit":"millions","pointEstimate":1.37,"ciLow":1.09,"ciHigh":1.65,"confidence":0.8,"resolutionDate":"2026-08-18","resolutionSource":"U.S. Census Bureau and HUD New Residential Construction release, Table 3","resolutionSourceUrl":"https://www.census.gov/construction/nrc/current/","resolutionRule":"Resolve to the first officially published Census/HUD New Residential Construction estimate for July 2026 privately owned housing starts, total units, seasonally adjusted annual rate, Table 3. Convert thousands of units to millions by multiplying by 0.001 and round to the nearest 0.001 million. Use the initial August 18, 2026 print only; ignore later revisions and benchmark updates.","dataPointId":"census.housing_starts.saar.2026-07.first_print","historicalContext":[{"label":"June 2026 first print HOUST SAAR","value":1.427},{"label":"May 2026 first print HOUST SAAR","value":1.177},{"label":"April 2026 first print HOUST SAAR","value":1.465},{"label":"March 2026 first print HOUST SAAR","value":1.502},{"label":"January 2026 first print HOUST SAAR","value":1.487}],"drivers":["June starts rebound was concentrated in volatile multifamily starts","June permits at 1.367 million SAAR point to softer near-term starts than June starts","Single-family starts were nearly flat around 0.895 million SAAR","High rates and elevated new-home inventory restrain a sustained upside break","Monthly starts dispersion is large, so the 80% interval remains wide"],"sourceContext":["https://www.census.gov/construction/soc/schedule.html","https://www.census.gov/construction/nrc/current/","https://www.census.gov/construction/nrc/data/series.html","https://alfred.stlouisfed.org/release?rid=27","https://fred.stlouisfed.org/series/HOUST/n"],"runAt":"2026-07-25T16:02:32Z","reasoning":[{"kind":"heading","text":"July 2026 US housing starts SAAR forecast"},{"kind":"text","text":"Framing and exact resolver: the target is Census/HUD New Residential Construction Table 3, privately owned housing starts, total units, seasonally adjusted annual rate, for July 2026, first print. The ledger unit is millions, so HOUST thousands are multiplied by 0.001."},{"kind":"tool","tool":"official.lookup","call":"Checked the Census Survey of Construction release schedule for the July 2026 New Residential Construction release.","result":"The Census schedule lists July 2026 New Residential Construction at 8:30 a.m. on August 18, 2026; it also lists June 2026 on July 17, 2026 and May 2026 on June 16, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the July 17, 2026 Census/HUD New Residential Construction release for June 2026 starts and related components.","result":"June 2026 privately owned housing starts were 1,427,000 SAAR; revised May starts were 1,199,000; June single-family starts were 895,000; June starts in buildings with 5 units or more were 513,000; June permits were 1,367,000."},{"kind":"tool","tool":"official.lookup","call":"Read the June 16, 2026 Census/HUD New Residential Construction release for the May first print and revised April comparison.","result":"May 2026 privately owned housing starts were first printed at 1,177,000 SAAR; revised April starts were 1,392,000; May single-family starts were 882,000; May starts in buildings with 5 units or more were 284,000; May permits were 1,413,000."},{"kind":"tool","tool":"official.lookup","call":"Checked ALFRED/FRED HOUST release/history pages and Census historical series context for recent first-print/reference values.","result":"Recent HOUST first-print/reference values used for dispersion were January 2026 1.487 million, February 2026 1.346 million, March 2026 1.502 million, April 2026 1.465 million, May 2026 1.177 million, and June 2026 1.427 million SAAR."},{"kind":"text","text":"Base rate/reference class: the recent first-print level reference class averages about 1.401 million over January-June 2026, with values oscillating between 1.177 million and 1.502 million. That base rate says a July print near 1.35-1.45 million is more plausible than either a new collapse or a durable break above 1.55 million."},{"kind":"math","text":"Prior/update/interval: persistence prior is the latest official first print, 1.427 million, cross-checked against the six-month first-print mean of 1.401 million. Adjustment components: -0.04 million for likely giveback from June's volatile multifamily jump from 0.284 million in May to 0.513 million in June, -0.02 million because June permits at 1.367 million trail starts, and about +0.00 to +0.01 million because single-family starts were stable near 0.895 million. This gives a point near 1.37 million. Interval method uses successive first-print changes from Jan-Jun: -0.141, +0.156, -0.037, -0.288, +0.250 million; sigma = 0.218 million, so 1.28*sigma = 0.279 million. Rounded 80% bounds are 1.37 - 0.28 = 1.09 and 1.37 + 0.28 = 1.65 million."},{"kind":"text","text":"Counter-considerations: upside risk is another multifamily-heavy month or faster conversion of permits to starts, which would land above the interval if total starts exceed 1.65 million. Downside risk is a reversal of June multifamily starts plus weaker single-family starts under high mortgage rates, which would land below the interval if total starts fall under 1.09 million."},{"kind":"forecast","point":1.37,"ciLow":1.09,"ciHigh":1.65}]}

# Reviewer critique
{
  "summary": "The draft is publication-ready on resolver, prior/update logic, uncertainty, tails, and JSON coherence, with only minor clarity improvements suggested.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Add February 2026 1.346 million to historicalContext because the interval calculation uses Jan-Jun successive first-print changes.",
    "Make the sourceBinding alignment slightly clearer by noting that ALFRED/FRED HOUST is only the first-print retrieval/history adapter while Census/HUD is the official release source."
  ]
}

Emit the final JSON object only.
