# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fed.g19.consumer_credit_revolving_annual_rate
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-revolving-consumer-credit-annual-rate-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "fed.g19.consumer_credit_revolving_annual_rate.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-09-11", "start": "2026-09-03"}, "field": "REVOLSLAR", "releasePolicy": "first_print", "sourceSeriesId": "REVOLSLAR", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=REVOLSLAR", "table": "G.19 Consumer Credit, outstanding, seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-e8c422ab399745706c6839ee625f75f62f0b4457d9c926a0c692f68969714c3e.json"
- targetContentHash: "e8c422ab399745706c6839ee625f75f62f0b4457d9c926a0c692f68969714c3e"
- registrationCommit: "0249a6f266d1d202c43782056e77403612358765"
- registeredAtUtc: "2026-07-31T14:48:09Z"

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
{"slug":"us-revolving-consumer-credit-annual-rate-july-2026","country":"US","type":"data","title":"US revolving consumer credit annual rate, July 2026","question":"Federal Reserve G.19 Percent Change of Total Revolving Consumer Credit (REVOLSLAR), seasonally adjusted annual rate, July 2026 first print","unit":"percent_growth","pointEstimate":3.5,"ciLow":-3.5,"ciHigh":10.5,"confidence":0.8,"resolutionDate":"2026-09-08","resolutionSource":"Federal Reserve G.19 Consumer Credit","resolutionSourceUrl":"https://www.federalreserve.gov/releases/g19/20260908/","resolutionRule":"Resolve to the first-published July 2026 value for Percent Change of Total Revolving Consumer Credit, REVOLSLAR, in the Federal Reserve G.19 Consumer Credit table 'Consumer Credit Outstanding, seasonally adjusted, percent change annual rate.' Use the first print released on September 8, 2026, with no later revisions; if the Board table shows one decimal but ALFRED/FRED first vintage exposes hundredths for REVOLSLAR, use that first-vintage value.","dataPointId":"fed.g19.consumer_credit_revolving_annual_rate.2026_07.first_print","historicalContext":[{"label":"May 2026 REVOLSLAR latest official/FRED mirror","value":-4.71},{"label":"Apr 2026 REVOLSLAR","value":10.36},{"label":"Mar 2026 REVOLSLAR","value":9.66},{"label":"2025 average in Fed G.19 table","value":3.1},{"label":"2026 Q1 in Fed G.19 table","value":4.1}],"drivers":["recent monthly volatility after strong March-April and weak May","2025-2026 revolving growth running slower than 2022-2023 rebound","high credit card APRs restrain revolving balance growth","July first print is two monthly observations beyond the latest official May value"],"sourceContext":["https://www.federalreserve.gov/newsevents/2026-september.htm","https://www.federalreserve.gov/releases/g19/current/","https://fred.stlouisfed.org/data/REVOLSLAR","https://fred.stlouisfed.org/series/REVOLSLAR"],"runAt":"2026-07-31T15:12:05Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 REVOLSLAR first print"},{"kind":"text","text":"Framing: the target is the Federal Reserve G.19 seasonally adjusted annual-rate percent change for total revolving consumer credit, series REVOLSLAR, for July 2026. I use the same variant throughout: revolving credit, seasonally adjusted, percent change at annual rate, first print."},{"kind":"tool","tool":"official.lookup","call":"Checked Federal Reserve September 2026 calendar for G.19 release timing.","result":"The Federal Reserve September 2026 calendar lists G.19 Consumer Credit at 3:00 p.m. on release date 8 in September 2026, so the verified resolution date is 2026-09-08."},{"kind":"tool","tool":"official.lookup","call":"Checked current Federal Reserve G.19 release for latest official values and variant.","result":"The July 8, 2026 G.19 release covers May 2026; revolving credit decreased at an annual rate of -4.7 percent in May, after 10.4 percent in April and 9.7 percent in March in the one-decimal Board table; the same table shows 2025 revolving growth of 3.1 percent and 2026 Q1 of 4.1 percent."},{"kind":"tool","tool":"fred.lookup","call":"Checked FRED REVOLSLAR mirror for exact recent observations and metadata.","result":"FRED series REVOLSLAR is monthly, seasonally adjusted annual rate, percent change at annual rate; latest observations shown were May 2026 -4.71, Apr 2026 10.36, Mar 2026 9.66, Feb 2026 1.03, and Jan 2026 1.64, last updated 2026-07-08 2:01 PM CDT."},{"kind":"tool","tool":"fred.history","call":"Read REVOLSLAR history from 2023-01 through 2026-05 for a recent reference class.","result":"Recent reference class values included 2023 monthly REVOLSLAR from 7.25 to -2.51, 2024 from 8.76 to 8.68 with a -9.18 November print, 2025 from 4.64 to 7.04, and 2026 through May values 1.64, 1.03, 9.66, 10.36, -4.71."},{"kind":"text","text":"Base rate: the recent non-pandemic reference class, 2023-01 through 2026-05, has a mean near 5.02 percent, while the more current 2025 through May 2026 average is closer to 3.22 percent; I anchor between these, leaning toward the lower recent regime because 2025-2026 revolving growth has slowed from the 2022-2023 rebound."},{"kind":"math","text":"Prior/update/interval: persistence/base prior is the 2023-01 to 2026-05 REVOLSLAR sample mean 5.02; current-regime pull from 2025-May 2026 average 3.22 and the latest -4.71 May print lowers the point by about 1.5 percentage points, while March 9.66 and April 10.36 keep it above zero, giving 3.5. For the 80% interval, using the 41 fetched REVOLSLAR values themselves as a change-rate series gives sigma = 5.47; 1.28*sigma = 1.28*5.47 = 7.00, so 3.5 +/- 7.0 gives [-3.5, 10.5]."},{"kind":"text","text":"Mechanisms: level growth in revolving balances remains positive on average, but momentum is mixed after the sharp May contraction; high credit card APRs are a drag, and no official June or July G.19 print is available yet to confirm whether May was one-off paydown or a turn lower."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed summer borrowing surge like March-April 2026, which would land above the interval if July prints above 10.5 percent; downside risk is another broad paydown or credit-card charge-off tightening episode, which would land below the interval if July prints below -3.5 percent."},{"kind":"forecast","point":3.5,"ciLow":-3.5,"ciHigh":10.5}]}

# Reviewer critique
{"summary":"Draft is largely coherent, but the resolver/source fields do not match the canonical ledger sourceBinding for first-print resolution.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft sets resolutionSourceUrl to a Federal Reserve release page, while the ledger target contract binds resolution to the alfred-fred adapter, allowed host alfred.stlouisfed.org, sourceSeriesId REVOLSLAR, and sourceUrl https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=REVOLSLAR.","actionRequested":"Change the resolver/source fields to match the ledger binding exactly, or explicitly state a concrete ledger discrepancy while keeping the same target; keep the first-print/no-revisions rule for REVOLSLAR."}],"optionalSuggestions":["Clarify that 2026-09-08 is the expected Federal Reserve release date being used inside the ledger's 2026-09-03 to 2026-09-11 expected release window.","In the interval sentence, say whether sigma is the sample standard deviation of monthly annualized rates rather than month-to-month changes, to avoid ambiguity."]}

Emit the final JSON object only.
