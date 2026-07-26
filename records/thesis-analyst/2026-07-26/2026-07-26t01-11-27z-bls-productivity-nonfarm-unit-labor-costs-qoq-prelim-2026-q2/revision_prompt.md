# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.productivity.nonfarm_unit_labor_costs_qoq_prelim
- period: 2026-Q2
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-unit-labor-costs-q2-2026-prelim"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.productivity.nonfarm_unit_labor_costs_qoq_prelim.2026_q2.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-08-06"}, "field": "PRS85006112", "releasePolicy": "first_print", "sourceSeriesId": "PRS85006112", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PRS85006112", "table": "Productivity and Costs, nonfarm business sector", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-a7e6c99f351819961a9cdf9259bebf1c1e21fac9e5f690026b9e4ce20813392c.json"
- targetContentHash: "a7e6c99f351819961a9cdf9259bebf1c1e21fac9e5f690026b9e4ce20813392c"
- registrationCommit: "145f6612f225710a4621f124b13bf5d5ae5d97ac"
- registeredAtUtc: "2026-07-26T00:55:04Z"

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
{"slug":"us-unit-labor-costs-q2-2026-prelim","country":"US","type":"data","title":"US Q2 2026 preliminary unit labor costs","question":"What will BLS first report for nonfarm business sector unit labor costs, seasonally adjusted percent change from previous quarter at an annual rate, in 2026 Q2 preliminary Productivity and Costs?","unit":"percent_growth","pointEstimate":3,"ciLow":-0.8,"ciHigh":6.8,"confidence":0.8,"resolutionDate":"2026-08-06","resolutionSource":"U.S. Bureau of Labor Statistics Productivity and Costs, Table 2","resolutionSourceUrl":"https://www.bls.gov/news.release/prod2.t02.htm","resolutionRule":"Resolve to the first-published BLS Productivity and Costs preliminary second-quarter 2026 value for nonfarm business sector unit labor costs, seasonally adjusted percent change from previous quarter at an annual rate, rounded to one decimal place as published in Table 2 on August 6, 2026; ignore later revised releases and later data-vintage changes.","dataPointId":"bls.productivity.nonfarm_unit_labor_costs_qoq_prelim.2026_q2.first_print","historicalContext":[{"label":"2026 Q1 revised BLS Table 2","value":1.8},{"label":"2026 Q1 preliminary BLS Table A1","value":2.3},{"label":"2025 Q4 preliminary BLS Table A1","value":2.8},{"label":"2025 Q3 preliminary BLS Table A1","value":-1.9},{"label":"2025 Q2 preliminary BLS Table A1","value":1.6}],"drivers":["Q1 unit labor costs were moderate after downward revision","private payroll hours were nearly flat through June","nominal earnings growth remains near 3.5 percent year over year","productivity first prints are volatile because output and compensation source data are incomplete","unit labor costs mechanically rise when hourly compensation outpaces productivity"],"sourceContext":["https://www.bls.gov/schedule/news_release/prod2.htm","https://www.bls.gov/news.release/prod2.t02.htm","https://www.bls.gov/news.release/prod2.htm","https://www.bls.gov/news.release/archives/prod2_05072026.htm","https://www.bls.gov/news.release/archives/prod2_03052026.htm","https://www.bls.gov/news.release/archives/prod2_01082026.htm","https://www.bls.gov/news.release/archives/prod2_08072025.htm","https://www.bls.gov/news.release/archives/empsit_07022026.htm","https://fred.stlouisfed.org/series/PRS85006112"],"runAt":"2026-07-26T01:12:43Z","reasoning":[{"kind":"heading","text":"US nonfarm unit labor costs, Q2 2026 preliminary"},{"kind":"text","text":"Framing and exact resolver: this is BLS nonfarm business sector unit labor costs, seasonally adjusted percent change from previous quarter at an annual rate, first print for 2026 Q2. The ledger sourceBinding points to ALFRED/FRED series PRS85006112 as a first-print mirror, but the official resolution source should be the BLS Productivity and Costs release/table for the first official print."},{"kind":"tool","tool":"official.lookup","call":"BLS Productivity and Costs release schedule lookup","result":"BLS schedule lists Second Quarter 2026 (P) on Aug. 06, 2026 at 08:30 AM and Second Quarter 2026 (R) on Sep. 03, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"BLS current Productivity and Costs Table 2 lookup for the same nonfarm business variant","result":"BLS Table 2 for 2026 Q1 revised shows nonfarm business unit labor costs 1.8, labor productivity 0.3, output 1.0, hours worked 0.7, and hourly compensation 2.1, all seasonally adjusted annualized rates."},{"kind":"tool","tool":"official.lookup","call":"BLS preliminary/recent-release reference class lookup","result":"Recent first prints for the target variant were 2026 Q1 unit labor costs 2.3 with productivity 0.8 and hourly compensation 3.1; 2025 Q4 unit labor costs 2.8 with productivity 2.8 and hourly compensation 5.7; 2025 Q3 unit labor costs -1.9 with productivity 4.9 and hourly compensation 2.9; 2025 Q2 unit labor costs 1.6 with productivity 2.4 and hourly compensation 4.0."},{"kind":"tool","tool":"official.lookup","call":"BLS June 2026 Employment Situation lookup for Q2 labor-cost and hours signals","result":"BLS reported June 2026 total nonfarm payroll employment +57,000, unemployment 4.2, average hourly earnings $37.64, average hourly earnings up 3.5 percent over the year, average weekly hours 34.3, and aggregate weekly hours index 116.8 versus 116.6 in April and 116.7 in May."},{"kind":"tool","tool":"mirror.lookup","call":"FRED/ALFRED PRS85006112 recent history mirror check","result":"FRED/ALFRED PRS85006112 reports Q1 2026 1.8, Q4 2025 2.1, Q3 2025 1.0, Q2 2025 -2.9, and Q1 2025 7.3 for Nonfarm Business Sector: Unit Labor Costs for All Workers, percent change at annual rate, seasonally adjusted."},{"kind":"text","text":"Reference class and base rate: using the same BLS nonfarm business unit-labor-costs variant, recent revised values from 2021 Q3 through 2026 Q1 average about 2.9 percent annualized, while the last four preliminary first prints before this target average about 1.2 percent but with a shutdown/benchmark-distorted negative Q3 2025. I weight the broader base rate more than the short preliminary sequence because this series is mechanically noisy and revised."},{"kind":"text","text":"Variant control: all anchors above are nonfarm business sector, seasonally adjusted, percent change from previous quarter at an annual rate. I do not mix in manufacturing, year-over-year, index-level, or final-vintage-only variants for the point forecast."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior is 2.9 from the 2021 Q3-2026 Q1 BLS revised reference class. Update components: Q1 revised ULC of 1.8 pulls slightly down, June payroll-hours softness (aggregate weekly hours 116.6 in April, 116.7 in May, 116.8 in June) supports positive productivity but not a boom, and 3.5 percent year-over-year hourly earnings plus recent compensation volatility keep compensation growth near 3.5-4.0. Net update leaves point near 3.0. Interval method uses realized dispersion of same-series quarterly annualized values [8.0, 3.5, 7.2, 3.5, 7.0, -1.7, 2.2, 2.4, 1.2, 1.2, 5.5, 1.1, 1.1, 2.9, 7.3, -2.9, 1.0, 2.1, 1.8]; sample sigma = 3.0, so 80 percent half-width is about 1.28*sigma = 1.28*3.0 = 3.8. Point 3.0 minus/plus 3.8 gives -0.8 to 6.8."},{"kind":"text","text":"Counter-considerations: upside risk is a compensation-per-hour jump with only modest output growth, which would land above the interval if preliminary hourly compensation prints near 8 percent and productivity is flat or negative. Downside risk is a strong Q2 output/productivity first print combined with subdued compensation, which would land below the interval if productivity exceeds compensation by more than about 1 percentage point annualized."},{"kind":"forecast","point":3,"ciLow":-0.8,"ciHigh":6.8}]}

# Reviewer critique
{
  "summary": "The draft is broadly publishable but needs resolver alignment with the canonical ALFRED first-print binding and a clearer statement on the time-series/model prior.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The forecast JSON names BLS Table 2 as the resolution source and URL, while the canonical ledger contract binds this target to the ALFRED/FRED adapter, allowed host alfred.stlouisfed.org, field PRS85006112, first_print policy, and sourceUrl https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PRS85006112.",
      "actionRequested": "Keep the same target, slug, dataPointId, and 2026-08-06 date, but make the resolution fields conform to the canonical ledger binding or explicitly state the ledger discrepancy in the reasoning while preserving the ledger-bound resolver fields."
    },
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "The draft uses a persistence/base-rate prior but does not clearly say whether a time-series or model prior was used or intentionally ruled out.",
      "actionRequested": "Add a compact sentence explaining that no separate AR/time-series model was used, or name the model prior and how it affected the point estimate."
    }
  ],
  "optionalSuggestions": [
    "Clarify that the volatility sample used for the interval is revised-vintage history rather than preliminary first-print history, if that is the intended sample.",
    "Make the resolver text distinguish official BLS publication from the ledger's ALFRED first-print mirror without changing the contracted target."
  ]
}

Emit the final JSON object only.
