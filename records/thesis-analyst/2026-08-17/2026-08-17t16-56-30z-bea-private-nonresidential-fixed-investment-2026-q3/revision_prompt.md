# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.private_nonresidential_fixed_investment
- period: 2026-Q3
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-private-nonresidential-fixed-investment-q3-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.private_nonresidential_fixed_investment.2026_q3.first_print"
- expectedReleaseWindow: {"end": "2026-10-29", "start": "2026-10-29"}
- sourceBinding: {"adapter": "bea-release", "allowedHosts": ["apps.bea.gov", "www.bea.gov"], "expectedReleaseWindow": {"end": "2026-10-29", "start": "2026-10-29"}, "field": "Line 2: Nonresidential", "releasePolicy": "first_print", "sourceSeriesId": "T50305:L2", "sourceUrl": "https://apps.bea.gov/iTable/?ReqID=19&step=3&isuri=1&nipa_table_list=145&categories=survey", "table": "Gross Domestic Product advance release, NIPA Table 5.3.5, line 2 (Nonresidential)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-17-78ab7e77198fa656ee058e98fa6d3e8743b3f9f24714b851883bee7fff4d2114.json"
- targetContentHash: "78ab7e77198fa656ee058e98fa6d3e8743b3f9f24714b851883bee7fff4d2114"
- registrationCommit: "f3a73cbcc701b9315d3ec1d35ea05889b2c07f95"
- registeredAtUtc: "2026-08-17T16:54:17Z"

# Source hints
- Use the official agency release calendar, not inferred cadence.
- FRED may be used as a history mirror, but resolution cites the agency.
- For FOMC targets, resolve to the target range upper bound after the announcement.
- For DOL claims, name the week-ending date and cite the release date.

# Default promoted forecasting practices
- Resolve the exact first-print target before inside-view evidence.
- Fetch and state the recent official-source reference class: at least 6 distinct prints are MANDATORY whenever the official source exposes them.
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
  "unit": "the registered targetUnit, byte-for-byte",
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
      "period": {
        "type": "month",
        "value": "2026-04"
      },
      "label": "Human-readable period label",
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
- historicalContext must contain at least 6 distinct numeric fetched prints. Every entry needs a canonical period object: type month with YYYY-MM, quarter with YYYY-Q1..Q4, year/fiscal_year with YYYY, or week_ending with YYYY-MM-DD. Its label must unambiguously name that same period. The whole trimmed label must be one closed printable-ASCII form: YYYY-MM, Month YYYY, YYYY Month, YYYY-QN, YYYY QN, QN YYYY, YYYY, calendar year YYYY, FY2026, fiscal year YYYY, YYYY-MM-DD, or week ending YYYY-MM-DD. Never add source names, first-print or revision prose, ranges, or a second period cue to the label. Relative, contradictory, non-ASCII, and multi-period labels refuse. Alternate labels do not make duplicate canonical periods distinct. Validation refuses fewer unless the sealed checkout carries the reviewed authorization below.
- Only when the official source exposes fewer than 6 prints, fetch all available prints and add this top-level audit commentary (replace 5 with the actual count and give a nonempty detail): {"historyAvailability": {"status": "official_source_exposes_fewer_than_six_prints", "availablePrintCount": 5, "detail": "Series began recently; the official source exposes only these five prints."}}
  This model-authored commentary never authorizes an exception: a reviewed docket entry in the sealed checkout must independently list the exact target period, available count, and canonical periods.
- sourceContext must contain at least 2 source URLs actually used.
- sourceContext, reasoning, drivers, and tool calls must not cite or use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or non-public local files.
- reasoning must contain at least 7 steps, at least 3 tool steps whose result strings include fetched numbers, one explicit base-rate or reference-class step (literally say "base rate" or "reference class"), one math step, one counter-consideration that states what would land outside the 80% interval (literally use "upside risk", "downside risk", or "outside the interval"), one step beginning Prior/update/interval:, and a final forecast step whose numbers exactly match the cell.
- Every tool step result must include at least one fetched numeric value — an actual statistic from the source, not just field names or identifiers. Definitional lookups (data dictionaries, field definitions, methodology pages) belong in text steps, as do other qualitative source notes. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- Do not use existing local catalog point estimates or intervals as forecast evidence. If inspected, treat them only as non-authoritative prior strategy context and keep them out of tool-result evidence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.5.11, prompt 87db344b803f, tools 024388e49298, promptMode fast)


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
{"slug":"us-private-nonresidential-fixed-investment-q3-2026","country":"US","type":"data","title":"US private nonresidential fixed investment, Q3 2026","question":"What will BEA report as the first-print nominal seasonally adjusted annual-rate value for private nonresidential fixed investment, NIPA Table 5.3.5 line 2, in 2026-Q3?","unit":"usd_billions","pointEstimate":4710,"ciLow":4630,"ciHigh":4790,"confidence":0.8,"resolutionDate":"2026-10-29","resolutionSource":"U.S. Bureau of Economic Analysis GDP advance release, NIPA Table 5.3.5 line 2","resolutionSourceUrl":"https://apps.bea.gov/iTable/?ReqID=19&step=3&isuri=1&nipa_table_list=145&categories=survey","resolutionRule":"Resolve to the first official BEA GDP advance-release print for 2026-Q3, NIPA Table 5.3.5, line 2 Nonresidential, nominal seasonally adjusted annual rate. Use the published table value transformed by multiplying the table's millions-of-dollars value by 0.001 to usd_billions. Do not use later second, third, annual-update, or comprehensive-revision values except insofar as BEA has already incorporated them into the first Q3 advance-release table on 2026-10-29.","dataPointId":"bea.private_nonresidential_fixed_investment.2026_q3.first_print","historicalContext":[{"period":{"type":"quarter","value":"2023-Q1"},"label":"2023-Q1","value":3756.575},{"period":{"type":"quarter","value":"2023-Q2"},"label":"2023-Q2","value":3854.267},{"period":{"type":"quarter","value":"2023-Q3"},"label":"2023-Q3","value":3871.644},{"period":{"type":"quarter","value":"2023-Q4"},"label":"2023-Q4","value":3941.343},{"period":{"type":"quarter","value":"2024-Q1"},"label":"2024-Q1","value":3963.752},{"period":{"type":"quarter","value":"2024-Q2"},"label":"2024-Q2","value":4012.411},{"period":{"type":"quarter","value":"2024-Q3"},"label":"2024-Q3","value":4069.186},{"period":{"type":"quarter","value":"2024-Q4"},"label":"2024-Q4","value":4046.39},{"period":{"type":"quarter","value":"2025-Q1"},"label":"2025-Q1","value":4137.819},{"period":{"type":"quarter","value":"2025-Q2"},"label":"2025-Q2","value":4207.512},{"period":{"type":"quarter","value":"2025-Q3"},"label":"2025-Q3","value":4293.474},{"period":{"type":"quarter","value":"2025-Q4"},"label":"2025-Q4","value":4364.412},{"period":{"type":"quarter","value":"2026-Q1"},"label":"2026-Q1","value":4490.516},{"period":{"type":"quarter","value":"2026-Q2"},"label":"2026-Q2","value":4623.657}],"drivers":["recent nominal PNFI level has risen for five straight quarters","Q2 advance release showed current-dollar GDP up 7.9 percent SAAR","BEA said Q2 investment growth reflected equipment and intellectual property gains partly offset by structures","September 2026 annual update can shift the level before the Q3 advance print","Q3 first print will include partial source data and BEA projections"],"sourceContext":["https://www.bea.gov/news/schedule/full","https://www.bea.gov/news/2026/gdp-advance-estimate-2nd-quarter-2026","https://fred.stlouisfed.org/series/PNFI","https://db.nomics.world/BEA/NIPA-T50305/A008RC-Q","https://apps.bea.gov/iTable/?ReqID=19&step=3&isuri=1&nipa_table_list=145&categories=survey"],"runAt":"2026-08-17T16:56:49Z","reasoning":[{"kind":"heading","text":"US private nonresidential fixed investment, 2026-Q3 first print"},{"kind":"text","text":"Resolver framing: this is BEA NIPA Table 5.3.5 line 2, Nonresidential, nominal seasonally adjusted annual rate. The ledger table value is in millions and the target unit is usd_billions, so resolution multiplies the official table value by 0.001."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA's 2026 release schedule for the GDP advance estimate covering 2026-Q3.","result":"BEA lists GDP (Advance Estimate), 3rd Quarter 2026 on October 29, 2026 at 8:30 AM; the same schedule page lists GDP (Advance Estimate), 2nd Quarter 2026 on July 30, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched current public BEA/FRED mirror history for PNFI, BEA account A008RC, quarterly SAAR billions of dollars.","result":"Recent fetched values were 2025-Q1 4137.819, 2025-Q2 4207.512, 2025-Q3 4293.474, 2025-Q4 4364.412, 2026-Q1 4490.516, and 2026-Q2 4623.657 usd_billions."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA's Q2 2026 advance GDP release for current-quarter macro context and source assumptions.","result":"The Q2 2026 advance release reported real GDP +1.5 percent SAAR, current-dollar GDP +7.9 percent SAAR, real final sales to private domestic purchasers +3.9 percent, and PCE price index +5.1 percent."},{"kind":"tool","tool":"official.lookup","call":"Checked the BEA-derived DBnomics NIPA-T50305 A008RC-Q page for table identity and latest line value scale.","result":"DBnomics identifies BEA NIPA Table 5.3.5 line 2 A008RC-Q as Nonresidential quarterly and shows 2026-Q2=4,623,657 in the BEA table's millions scale, equivalent to 4623.657 usd_billions after the registered 0.001 transform."},{"kind":"text","text":"Base rate/reference class: using the 2023-Q1 through 2026-Q2 quarterly level history, the outside-view one-quarter change averaged about 66.7 usd_billions. The recent five changes were stronger, about +69.7, +86.0, +70.9, +126.1, and +133.1, so pure persistence from 2026-Q2 would point somewhat above the long recent mean."},{"kind":"math","text":"Prior/update/interval: persistence prior is last observed PNFI level 4623.657 plus the 2023-Q1 to 2026-Q2 mean quarterly change of 66.7, giving 4690.4. I add about 20 for continued Q2 nominal momentum and equipment/IPP strength, while subtracting no explicit policy drag because financing-cost restraint is already visible in the recent level series, giving a point near 4710. For interval sizing, successive changes in the 2023-Q1 to 2026-Q2 fetched history have sigma = 43.5 usd_billions, so 1.28*sigma = 55.7. I widen to an 80 usd_billions half-width because the September 2026 annual update can shift the level before the Q3 first print and the advance estimate still uses partial source data plus projections; final 80 percent bounds are 4710-80=4630 and 4710+80=4790."},{"kind":"text","text":"Upside risk: a continuing AI/data-center equipment and software investment surge, stronger Q3 nominal GDP, or upward annual-update level revision would land above the interval. Downside risk: a pullback in nonresidential structures, weaker capital-goods imports/shipments, or a downward annual-update rebasing would land below the interval. An outside the interval outcome would most likely require both a large annual-update level shift and an unusually large Q3 source-data surprise."},{"kind":"forecast","point":4710,"ciLow":4630,"ciHigh":4790}]}

# Reviewer critique
{
  "summary": "The draft is publishable: resolver fields match the ledger target, the prior/update/interval logic is compact and coherent, and no blocking leakage or unit issue is apparent.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Tighten the driver wording to specify the five straight increases run from 2025-Q1 through 2026-Q2.",
    "In the interval step, briefly state whether sigma is computed on level changes using 2023-Q1 to 2026-Q2 consecutive quarters."
  ]
}

Emit the final JSON object only.
