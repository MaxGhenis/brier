# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fed.g17.industrial_production.total_index_mom
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "fed-g17-industrial-production-total-index-mom-june-2026"
- targetUnit: "percent_growth"

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
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
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
{"slug":"fed-g17-industrial-production-total-index-mom-june-2026","country":"US","type":"data","title":"US industrial production MoM, Jun 2026","question":"Federal Reserve G.17 Industrial Production: Total Index, seasonally adjusted, percent change from May 2026 to June 2026, first print","unit":"percent_growth","pointEstimate":0.2,"ciLow":-0.5,"ciHigh":0.9,"confidence":0.8,"resolutionDate":"2026-07-17","resolutionSource":"Federal Reserve G.17 Industrial Production and Capacity Utilization release","resolutionSourceUrl":"https://www.federalreserve.gov/releases/g17/20260717/","resolutionRule":"Resolve to the preliminary first-print June 2026 value for Total index, seasonally adjusted, Percent change, in the Federal Reserve G.17 Industrial Production and Capacity Utilization: Summary table first issued on July 17, 2026. Use the displayed one-decimal percent value; ignore later revisions and annual benchmark revisions.","dataPointId":"fed.g17.industrial_production.total_index_mom.2026-06.first_print","historicalContext":[{"label":"2026-05 first/current print","value":0.1},{"label":"2026-04 revised/current print","value":0.9},{"label":"2026-03 revised/current print","value":-0.3},{"label":"2026-02 revised/current print","value":0.8},{"label":"2026-01 revised/current print","value":-0.4}],"drivers":["Recent total IP momentum is positive but choppy","Manufacturing was flat in May after April strength","Mining added materially in May and may mean-revert","Utilities are weather-sensitive and widen monthly dispersion","Capacity utilization remains below long-run average"],"sourceContext":["https://www.federalreserve.gov/releases/g17/default.htm","https://www.federalreserve.gov/releases/g17/current/default.htm","https://fred.stlouisfed.org/series/INDPRO"],"runAt":"2026-07-08T16:55:28Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 total industrial production MoM"},{"kind":"text","text":"Framing and exact resolver: this targets the Federal Reserve G.17 Summary table, Total index, seasonally adjusted, Percent change, for June 2026. The resolution variant is the first preliminary monthly print, not later revised values; the expected archive page is the July 17, 2026 G.17 release."},{"kind":"tool","tool":"official.lookup","call":"Checked Federal Reserve G.17 release dates page for the June 2026 reporting month release schedule.","result":"The G.17 monthly releases are issued at 9:15 a.m.; the 2026 schedule lists July 17, 2026 after June 15, 2026, so resolutionDate = 2026-07-17."},{"kind":"tool","tool":"official.lookup","call":"Read the Federal Reserve current G.17 Summary table for Total index, seasonally adjusted, 2017=100 and percent change.","result":"Total index levels and percent changes shown: Dec 2025 level 101.5 and change 0.5; Jan 2026 level 101.1 and change -0.4; Feb 2026 level 101.9 and change 0.8; Mar 2026 level 101.6 and change -0.3; Apr 2026 level 102.5 and change 0.9; May 2026 level 102.6 and change 0.1; May 2025 to May 2026 change 1.7."},{"kind":"tool","tool":"official.lookup","call":"Read the Federal Reserve current G.17 sector detail for the May 2026 release.","result":"May 2026 component percent changes: manufacturing 0.0, mining 1.3, utilities -0.4; capacity utilization total industry 76.2 versus long-run 1972-2025 average 79.4."},{"kind":"tool","tool":"fred.lookup","call":"Used FRED as a public history mirror for exact INDPRO seasonally adjusted levels underlying the latest total-index changes.","result":"INDPRO exact levels: May 2026 102.6475, Apr 2026 102.5090, Mar 2026 101.6273, Feb 2026 101.9493, Jan 2026 101.1235; FRED lists the next release date as Jul 17, 2026."},{"kind":"text","text":"Base rate/reference class: recent G.17 monthly total-index percent changes are centered near modest growth, with the last seven current-print/revised values Dec-May equal to 0.5, -0.4, 0.8, -0.3, 0.9, and 0.1 plus the November value -0.2 from the May release table. That makes a simple recent reference class mean about 0.2 percent, while the latest May reading of 0.1 percent and flat manufacturing argue against extrapolating April's 0.9 percent jump."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class prior uses recent G.17 total-index percent changes Nov 2025-May 2026: -0.2, 0.5, -0.4, 0.8, -0.3, 0.9, 0.1; mean = 0.2 and sigma = 0.54 from the values themselves for this change series. Half-width = roughly 1.28*sigma = 1.28*0.54 = 0.69. I set point = 0.2, using +0.05 from positive April-May level momentum, -0.05 from flat May manufacturing and possible mining mean reversion, and 0.00 from utilities/weather uncertainty. Rounded first-print-style 80% bounds are 0.2 - 0.69 = -0.49 to 0.2 + 0.69 = 0.89, reported as -0.5 to 0.9."},{"kind":"text","text":"Counter-considerations: upside risk is a continued rebound in manufacturing or another mining gain like May's 1.3 percent, which would land above the interval if total IP prints above 0.9 percent. Downside risk is a reversal in mining plus weak durable manufacturing or adverse utilities output; that would land below the interval if total IP prints below -0.5 percent."},{"kind":"forecast","point":0.2,"ciLow":-0.5,"ciHigh":0.9}]}

# Reviewer critique
{"summary":"Draft is publishable with no blocking issues; resolver, date, unit, first-print rule, prior/update/interval arithmetic, tails, and JSON fields are coherent.","requiredFixes":[],"optionalSuggestions":["Clarify whether the seven-month volatility sample uses first-print or latest-revised/current values, since the target resolves to first print.","Consider adding a longer historical volatility check as a sensitivity note, because seven monthly observations is a thin interval basis."]}

Emit the final JSON object only.
