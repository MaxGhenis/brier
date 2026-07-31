# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.productivity.nonfarm_unit_labor_costs_qoq_prelim
- period: 2026-Q3
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-unit-labor-costs-q3-2026-prelim"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.productivity.nonfarm_unit_labor_costs_qoq_prelim.2026_q3.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-11-13", "start": "2026-10-30"}, "field": "PRS85006112", "releasePolicy": "first_print", "sourceSeriesId": "PRS85006112", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PRS85006112", "table": "Productivity and Costs, nonfarm business sector", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-5acb920aa1125b4d971bd7b22bdf4bd31f9a5ede261d0e7074400403a66e4391.json"
- targetContentHash: "5acb920aa1125b4d971bd7b22bdf4bd31f9a5ede261d0e7074400403a66e4391"
- registrationCommit: "7ecbc85cc4110060218f856d50321ab93db3af3b"
- registeredAtUtc: "2026-07-31T18:02:17Z"

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
{"slug":"us-unit-labor-costs-q3-2026-prelim","country":"US","type":"data","title":"US nonfarm unit labor costs Q3 2026 prelim","question":"What will BLS report as the first-print seasonally adjusted annualized quarter-over-quarter percent change in nonfarm business sector unit labor costs for 2026 Q3?","unit":"percent_growth","pointEstimate":2.4,"ciLow":-0.3,"ciHigh":5.1,"confidence":0.8,"resolutionDate":"2026-11-05","resolutionSource":"U.S. Bureau of Labor Statistics Productivity and Costs preliminary news release","resolutionSourceUrl":"https://www.bls.gov/news.release/prod2.nr0.htm","resolutionRule":"Resolve to the first-print Table A1 value for nonfarm business sector unit labor costs, percent change from previous quarter at a seasonally adjusted annualized rate, in the BLS Productivity and Costs: Third Quarter 2026, Preliminary release scheduled for November 5, 2026. Use the value rounded to one decimal place as published in that first release; ignore later revised releases and database revisions.","dataPointId":"bls.productivity.nonfarm_unit_labor_costs_qoq_prelim.2026_q3.first_print","historicalContext":[{"label":"2026-Q1 preliminary","value":2.3},{"label":"2025-Q4 preliminary","value":2.8},{"label":"2025-Q3 preliminary","value":-1.9},{"label":"2025-Q2 preliminary","value":1.6},{"label":"2025-Q1 preliminary","value":5.7},{"label":"2024-Q4 preliminary","value":3.0},{"label":"2024-Q3 preliminary","value":1.9},{"label":"2024-Q2 preliminary","value":0.9}],"drivers":["Recent first-print nonfarm ULC values average about 2.0 percent SAAR","Compensation growth remains the positive level anchor for ULC","Productivity gains can quickly push ULC below trend","First-print Q3 uses the preliminary BLS Productivity and Costs variant, not later revisions"],"sourceContext":["https://www.bls.gov/productivity/schedule-releases.htm","https://www.bls.gov/news.release/archives/prod2_05072026.htm","https://www.bls.gov/news.release/archives/prod2_03052026.htm","https://www.bls.gov/news.release/archives/prod2_01082026.htm","https://www.bls.gov/news.release/archives/prod2_08072025.htm","https://www.bls.gov/news.release/archives/prod2_05082025.htm","https://www.bls.gov/news.release/archives/prod2_02062025.htm","https://www.bls.gov/news.release/archives/prod2_11072024.htm","https://www.bls.gov/news.release/archives/prod2_08012024.htm"],"runAt":"2026-07-31T18:16:39Z","reasoning":[{"kind":"heading","text":"US nonfarm business unit labor costs, 2026 Q3 preliminary"},{"kind":"text","text":"Framing and exact resolver: this is the BLS Productivity and Costs nonfarm business sector unit labor costs series, quarterly percent change from the previous quarter at a seasonally adjusted annualized rate, first print for 2026 Q3. The release and all historical anchors below use the same preliminary-release variant rather than revised database values."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Productivity Program schedule of releases and revisions for Productivity and Costs.","result":"BLS lists initial release of Second Quarter 2026 data on August 6, 2026, revision of Second Quarter 2026 data on September 3, 2026, initial release of Third Quarter 2026 data on November 5, 2026, and revision of Third Quarter 2026 data on December 8, 2026."},{"kind":"tool","tool":"official.lookup","call":"Read BLS archived preliminary Productivity and Costs releases for recent nonfarm business unit labor cost first prints.","result":"Fetched first-print nonfarm business unit labor costs: 2026-Q1 was 2.3 percent, 2025-Q4 was 2.8 percent, and 2025-Q3 was -1.9 percent, all SAAR percent changes from previous quarter."},{"kind":"tool","tool":"official.lookup","call":"Read additional BLS archived preliminary Productivity and Costs releases to build the reference class.","result":"Fetched first-print nonfarm business unit labor costs: 2025-Q2 was 1.6 percent, 2025-Q1 was 5.7 percent, 2024-Q4 was 3.0 percent, 2024-Q3 was 1.9 percent, and 2024-Q2 was 0.9 percent, all SAAR percent changes from previous quarter."},{"kind":"text","text":"The base rate/reference class is the eight most recent available same-variant preliminary nonfarm business ULC prints: 0.9, 1.9, 3.0, 5.7, 1.6, -1.9, 2.8, and 2.3 percent. Their mean is 2.04 percent; persistence from 2026-Q1 is 2.3 percent, so both point to a low-to-mid 2 percent forecast before current-quarter specifics."},{"kind":"math","text":"Prior/update/interval: persistence prior = 2.3 from the latest same-variant 2026-Q1 preliminary print; historical sample = the eight preliminary prints from 2024-Q2 through 2026-Q1 with mean 2.04. Adjustment components: +0.2 for compensation growth staying positive, +0.1 for uncertainty before the not-yet-released Q2 productivity print, and -0.2 for the tendency of stronger productivity to offset hourly compensation in this series, giving point = 2.4. For a change/flow series, sigma is computed from the values themselves: sample standard deviation of [0.9, 1.9, 3.0, 5.7, 1.6, -1.9, 2.8, 2.3] gives sigma = 2.14. The 80 percent normal half-width is 1.28*sigma = 1.28*2.14 = 2.74, rounded to 2.7, so bounds are 2.4 - 2.7 = -0.3 and 2.4 + 2.7 = 5.1."},{"kind":"text","text":"Upside risk is a quarter with compensation growth near recent highs and weak productivity, which would land above the interval if ULC exceeds 5.1 percent. Downside risk is another productivity surge like 2025-Q3, which would push ULC below zero; a very large productivity surprise with subdued compensation would land below the interval."},{"kind":"forecast","point":2.4,"ciLow":-0.3,"ciHigh":5.1}]}

# Reviewer critique
{"summary":"Draft is mostly coherent, but it should reconcile the published resolver fields with the canonical ledger source binding before publication.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft resolver names the BLS news release URL, while the canonical ledger sourceBinding specifies the ALFRED/FRED PRS85006112 first-print source URL and allowed host.","actionRequested":"Align the forecast's resolver/source fields with the canonical ledger contract, or explicitly state the ledger discrepancy in reasoning while keeping the target tied to the same slug and dataPointId."}],"optionalSuggestions":["Clarify why the eight-print sample is sufficient for volatility rather than using a longer same-variant preliminary history.","The interval math is acceptable, but note that ULC is often revision-prone and first-print noise may widen tails."]}

Emit the final JSON object only.
