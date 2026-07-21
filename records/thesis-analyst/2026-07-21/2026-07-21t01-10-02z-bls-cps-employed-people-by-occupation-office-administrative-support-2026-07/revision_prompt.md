# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cps.employed_people_by_occupation.office_administrative_support
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "cps-office-admin-employment-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "bls.cps.employed_people_by_occupation.office_administrative_support.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-07-29"}, "field": "Office and administrative support occupations", "releasePolicy": "first_print", "sourceSeriesId": "bls.cps.employed_people_by_occupation.office_administrative_support", "sourceUrl": "https://www.bls.gov/web/empsit/cpseea19.htm", "table": "CPS Employment Situation Table A-19, employed persons by occupation, not seasonally adjusted (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-21-148ed0329886292f905056a164baddd005c4f488016df31b37fd3083d7030d8e.json"
- targetContentHash: "148ed0329886292f905056a164baddd005c4f488016df31b37fd3083d7030d8e"
- registrationCommit: "36b3b6b19986083e354c0bd56b0090751cfaeba7"
- registeredAtUtc: "2026-07-21T01:00:49Z"

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
{"slug":"cps-office-admin-employment-july-2026","country":"US","type":"data","title":"US office and administrative support employment, July 2026","question":"What will BLS first report for employed people in office and administrative support occupations in July 2026, not seasonally adjusted, in millions?","unit":"millions","pointEstimate":16.34,"ciLow":16.16,"ciHigh":16.52,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table A-19","resolutionSourceUrl":"https://www.bls.gov/web/empsit/cpseea19.htm","resolutionRule":"Resolve to the July 2026 total employed value for “Office and administrative support occupations” in CPS Employment Situation Table A-19, not seasonally adjusted, as first published by BLS on August 7, 2026. Convert the reported thousands to millions by multiplying by 0.001 and retain three decimal places. Ignore subsequent revisions.","dataPointId":"bls.cps.employed_people_by_occupation.office_administrative_support.july_2026.first_print","historicalContext":[{"label":"January 2026 first print, NSA millions","value":16.355},{"label":"February 2026 first print, NSA millions","value":16.38},{"label":"March 2026 first print, NSA millions","value":16.563},{"label":"April 2026 first print, NSA millions","value":16.471},{"label":"May 2026 first print, NSA millions","value":16.335},{"label":"June 2026 first print, NSA millions","value":16.184},{"label":"July 2025 first print, NSA millions","value":16.565}],"drivers":["usual June-to-July seasonal increase in the unadjusted series","recent three-month decline in office-support employment","CPS sampling volatility","weak aggregate household employment momentum"],"sourceContext":["https://www.bls.gov/web/empsit/cpseea19.htm","https://www.bls.gov/schedule/news_release/empsit.htm","https://www.bls.gov/news.release/archives/empsit_07022026.pdf","https://www.bls.gov/news.release/archives/empsit_06052026.pdf","https://www.bls.gov/news.release/archives/empsit_05082026.pdf","https://www.bls.gov/news.release/archives/empsit_04032026.pdf","https://www.bls.gov/news.release/archives/empsit_03062026.pdf","https://www.bls.gov/news.release/archives/empsit_02112026.pdf","https://www.bls.gov/news.release/archives/empsit_08012025.pdf","https://www.bls.gov/news.release/archives/empsit_08022024.pdf","https://www.bls.gov/news.release/archives/empsit_07052024.pdf"],"runAt":"2026-07-21T01:10:37Z","reasoning":[{"kind":"heading","text":"July 2026 office and administrative support employment forecast"},{"kind":"text","text":"The target is the total employed count for Office and administrative support occupations in CPS Table A-19, not seasonally adjusted and reported in thousands, converted to millions. Resolution uses the first July 2026 print only. The official BLS calendar schedules it for August 7, 2026; this conflicts with the ledger sourceBinding window ending August 6, so the verified official date is used without changing the target."},{"kind":"tool","tool":"official.lookup","call":"Fetch the BLS Employment Situation release schedule for the July 2026 reference month.","result":"The official schedule lists July 2026 for release on 2026-08-07 at 8:30 AM ET."},{"kind":"tool","tool":"official.lookup","call":"Fetch first-published 2026 Table A-13/A-19 office and administrative support employment totals from BLS Employment Situation releases.","result":"Not-seasonally-adjusted employment was 16,355 thousand in January, 16,380 thousand in February, 16,563 thousand in March, 16,471 thousand in April, 16,335 thousand in May, and 16,184 thousand in June 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetch recent June and July reference-class values from archived BLS occupational employment tables.","result":"July employment was 15,814 thousand in 2024 and 16,565 thousand in 2025; June was 15,568 thousand in 2024 and 16,469 thousand in 2025, giving June-to-July changes of +246 thousand and +96 thousand."},{"kind":"text","text":"The outside-view base rate is the recent June-to-July reference class: the two observed increases average (+0.246 + 0.096)/2 = +0.171 million. Applied mechanically to June 2026's 16.184 million, that gives 16.355 million."},{"kind":"text","text":"Level is 16.184 million in June. Momentum is negative: the March-to-June path fell 0.379 million. The one-off seasonal mechanism points upward in July, while policy and aggregate labor-market effects are modestly negative because June household employment weakened. I therefore trim the seasonal prior by 0.015 million to 16.340 million."},{"kind":"math","text":"Prior/update/interval: persistence-plus-July-seasonality prior, using January-June 2026 first-print NSA levels and the 2024-2025 June-to-July reference class; adjustments are +0.171 million seasonal, -0.015 million for recent negative momentum, and 0.000 million for other mechanisms, yielding 16.184 + 0.171 - 0.015 = 16.340 million. Successive 2026 changes are +0.025, +0.183, -0.092, -0.136, and -0.151 million; their sample standard deviation is sigma = 0.140 million. The normal 80% half-width is 1.28*sigma = 1.28*0.140 = 0.179 million, implying 16.161 to 16.519 million, rounded outward to final bounds of 16.16 to 16.52 million."},{"kind":"text","text":"Upside risk comes from a July seasonal increase nearer 2024's +0.246 million, which could push the print toward the upper bound. Downside risk comes from continuation of the March-June contraction. An unusually large CPS sampling move or a decline exceeding about 0.024 million from June would land outside the interval below 16.16; a gain above about 0.336 million would land outside the interval above 16.52."},{"kind":"forecast","point":16.34,"ciLow":16.16,"ciHigh":16.52}]}

# Reviewer critique
{
  "summary": "The draft is publishable with no blocking issues; it clearly identifies the BLS first-print Table A-19 resolver, states a persistence-plus-seasonality prior, explains the small downward update, and keeps the point and interval coherent.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider noting in the final JSON or validation notes that the ledger release window appears stale because BLS schedules the July 2026 Employment Situation release for 2026-08-07.",
    "The interval would be stronger if it referenced a longer realized-volatility sample or target-specific June-to-July residuals, rather than only five 2026 month-to-month changes."
  ]
}

Emit the final JSON object only.
