# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fed.g19.consumer_credit_nonrevolving_annual_rate
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-nonrevolving-consumer-credit-annual-rate-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "fed.g19.consumer_credit_nonrevolving_annual_rate.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-09-11", "start": "2026-09-03"}, "field": "NONREVSLAR", "releasePolicy": "first_print", "sourceSeriesId": "NONREVSLAR", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=NONREVSLAR", "table": "G.19 Consumer Credit, outstanding, seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-e2880f2c437abd35592ae643d333e965a87e319dae0af9372925c7fa8bba1f1d.json"
- targetContentHash: "e2880f2c437abd35592ae643d333e965a87e319dae0af9372925c7fa8bba1f1d"
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
{"slug":"us-nonrevolving-consumer-credit-annual-rate-july-2026","country":"US","type":"data","title":"US Nonrevolving Consumer Credit Annual Rate, July 2026","question":"Federal Reserve G.19 Percent Change of Total Nonrevolving Consumer Credit (NONREVSLAR), seasonally adjusted annual rate, July 2026 first print","unit":"percent_growth","pointEstimate":2.1,"ciLow":0.6,"ciHigh":3.6,"confidence":0.8,"resolutionDate":"2026-09-08","resolutionSource":"Federal Reserve G.19 Consumer Credit first print, with NONREVSLAR first-vintage mirror in ALFRED","resolutionSourceUrl":"https://www.federalreserve.gov/releases/g19/current/default.htm","resolutionRule":"Resolve to the first published July 2026 value for NONREVSLAR, Percent Change of Total Nonrevolving Consumer Credit, percent change at annual rate, seasonally adjusted annual rate, from the Federal Reserve G.19 Consumer Credit release scheduled for September 8, 2026. Use the original first-print value only; do not use later revisions. If using the ALFRED/FRED mirror, use the first vintage for observation 2026-07 in source series NONREVSLAR.","dataPointId":"fed.g19.consumer_credit_nonrevolving_annual_rate.2026_07.first_print","historicalContext":[{"label":"Jan 2026 NONREVSLAR","value":0.84},{"label":"Feb 2026 NONREVSLAR","value":1.94},{"label":"Mar 2026 NONREVSLAR","value":3.84},{"label":"Apr 2026 NONREVSLAR","value":2.93},{"label":"May 2026 NONREVSLAR","value":1.61},{"label":"2025 official table nonrevolving annual rate","value":1.8},{"label":"2026 Q1 official table nonrevolving annual rate","value":2.2}],"drivers":["recent nonrevolving growth near 2 percent annual rate","May 2026 downshift after March-April strength","student-loan and auto-loan components keep positive but uneven flow","higher borrowing costs limit upside"],"sourceContext":["https://www.federalreserve.gov/newsevents/2026-september.htm","https://www.federalreserve.gov/releases/g19/current/default.htm","https://fred.stlouisfed.org/series/NONREVSLAR","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=NONREVSLAR"],"runAt":"2026-07-31T15:15:35Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 NONREVSLAR first print"},{"kind":"text","text":"Framing and exact resolver: the target is Federal Reserve G.19 Consumer Credit, table Consumer Credit Outstanding, seasonally adjusted, Nonrevolving percent change at annual rate for July 2026. The ledger binds source series NONREVSLAR and the ALFRED first-vintage mirror; the official agency release remains the Federal Reserve G.19 release."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve September 2026 statistical release calendar lookup for G.19 Consumer Credit","result":"Fetched official schedule: September 2026 calendar lists G.19 - Consumer Credit at 3:00 p.m. with release date 8; Labor Day is listed on September 7."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve current G.19 release table lookup, seasonally adjusted Consumer Credit Outstanding","result":"Fetched official May 2026 release dated July 8, 2026: nonrevolving credit increased at an annual rate of 1.6 percent in May; the table shows Nonrevolving percent change annual rate of 3.8 for Mar 2026, 2.9 for Apr 2026, and 1.6 for May 2026."},{"kind":"tool","tool":"official.lookup","call":"FRED/ALFRED mirror lookup for series NONREVSLAR recent monthly observations","result":"Fetched NONREVSLAR values: Jan 2026 0.84, Feb 2026 1.94, Mar 2026 3.84, Apr 2026 2.93, May 2026 1.61; units are percent change at annual rate, seasonally adjusted annual rate."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.19 component and level cross-check for nonrevolving credit","result":"Fetched official G.19 supporting rows: seasonally adjusted nonrevolving outstanding was 3795.9 billion dollars in Mar 2026, 3805.2 billion in Apr 2026, and 3810.3 billion in May 2026; nonrevolving flow annual rate was 145.2 in Mar, 111.3 in Apr, and 61.4 in May."},{"kind":"text","text":"Base rate/reference class: the near-term reference class is the five available 2026 monthly NONREVSLAR observations before the target window, 0.84, 1.94, 3.84, 2.93, and 1.61, with mean 2.23. The official table's annual context is also moderate: 2025 nonrevolving growth 1.8 and 2026 Q1 2.2."},{"kind":"text","text":"The variant is consistent throughout: seasonally adjusted annual-rate percent change for nonrevolving consumer credit, not the not-seasonally-adjusted level or flow table. I use the level and flow rows only as checks on the same G.19 nonrevolving category."},{"kind":"math","text":"Prior/update/interval: persistence prior is latest NONREVSLAR 1.61; reference class is Jan-May 2026 values 0.84, 1.94, 3.84, 2.93, 1.61 with mean 2.23. Adjustment components are +0.2 for the 2025/Q1 baseline around 1.8-2.2, -0.1 for still-high loan rates, and -0.2 for the May downshift in flow, giving a point near 2.1. For this change-rate series I use the fetched annual-rate values themselves: sigma = 1.17 from the sample standard deviation of 0.84, 1.94, 3.84, 2.93, 1.61; 1.28*sigma = 1.50, so the 80 percent interval is 2.1 +/- 1.5 = 0.6 to 3.6."},{"kind":"text","text":"Upside risk: a rebound in auto-loan origination, a larger student-loan/federal-government contribution, or revision-prone seasonal factors could put July growth above 3.6. Downside risk: weak vehicle credit, paydowns, or another negative finance-company/federal component could push the print below 0.6. A sharp credit contraction or one-off technical adjustment would land outside the interval."},{"kind":"forecast","point":2.1,"ciLow":0.6,"ciHigh":3.6}]}

# Reviewer critique
{"summary":"Draft is mostly publication-ready, but the resolver/source fields should be aligned to the canonical ALFRED first-print binding before publication.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft JSON uses the Federal Reserve current G.19 page as resolutionSourceUrl, while the ledger sourceBinding specifies the ALFRED first-vintage CSV for NONREVSLAR with allowed host alfred.stlouisfed.org.","actionRequested":"Set the resolver/source text and URL to match the ledger binding: ALFRED NONREVSLAR first vintage for 2026-07, while optionally noting that ALFRED mirrors the Federal Reserve G.19 first print."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The math step says the prior is 1.61 and lists adjustments of +0.2, -0.1, and -0.2, which would not produce the stated 2.1 point estimate unless there is also shrinkage toward the 2.23 reference-class mean.","actionRequested":"Make the compact prior/update step arithmetically explicit, e.g. state the blend between latest persistence and Jan-May mean before applying the named adjustments."}],"optionalSuggestions":["Keep the September 8, 2026 release-date claim only if it is tied to the official Federal Reserve statistical release calendar; otherwise phrase it as expected within the ledger window.","The interval method is acceptable, but note that five observations is a thin volatility sample."]}

Emit the final JSON object only.
