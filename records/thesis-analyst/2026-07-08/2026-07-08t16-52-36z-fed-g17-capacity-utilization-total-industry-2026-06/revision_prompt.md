# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fed.g17.capacity_utilization.total_industry
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "fed-g17-capacity-utilization-total-industry-june-2026"
- targetUnit: "percent"

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
{"slug":"fed-g17-capacity-utilization-total-industry-june-2026","country":"US","type":"data","title":"US total industry capacity utilization, June 2026","question":"Federal Reserve G.17 Capacity Utilization: Total Industry, June 2026, seasonally adjusted percent of capacity, first print","unit":"percent","pointEstimate":76.2,"ciLow":75.6,"ciHigh":76.8,"confidence":0.8,"resolutionDate":"2026-07-17","resolutionSource":"Federal Reserve G.17 Industrial Production and Capacity Utilization release","resolutionSourceUrl":"https://www.federalreserve.gov/releases/g17/20260717/default.htm","resolutionRule":"Resolve to the first-print June 2026 value, in percent of capacity and seasonally adjusted, for the G.17 Capacity utilization table row 'Total industry' as first published in the Federal Reserve's July 17, 2026 monthly G.17 release. Use the displayed one-decimal percent value; ignore later revisions, annual benchmark revisions, and later FRED updates.","dataPointId":"fed.g17.capacity_utilization.total_industry.2026-06.first_print","historicalContext":[{"label":"May 2026 TCU latest mirror","value":76.1663},{"label":"Apr 2026 TCU","value":76.1289},{"label":"Mar 2026 TCU","value":75.5388},{"label":"Feb 2026 TCU","value":75.847},{"label":"Jan 2026 TCU","value":75.305}],"drivers":["May utilization already rebounded to 76.2 percent","Recent total IP growth was positive but manufacturing was flat in May","Mining utilization strength offsets weak utilities utilization","Capacity growth keeps utilization below its 1972-2025 average"],"sourceContext":["https://www.federalreserve.gov/releases/g17/default.htm","https://www.federalreserve.gov/releases/g17/20260615/default.htm","https://fred.stlouisfed.org/series/TCU"],"runAt":"2026-07-08T16:53:10Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 total industry capacity utilization"},{"kind":"text","text":"Framing and exact resolver: this is the Federal Reserve G.17 Capacity Utilization: Total Industry series, seasonally adjusted percent of capacity. The target is the first published June 2026 value in the July 17, 2026 G.17 release; the series code mirror is FRED TCU, but resolution is to the Federal Reserve release table."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 release calendar lookup for 2026 monthly releases","result":"The G.17 release calendar says monthly releases are issued at 9:15 a.m.; 2026 dates include June 15 and July 17, so the June 2026 observation is scheduled for first release on 2026-07-17."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve June 15, 2026 G.17 current release summary and capacity utilization table","result":"The May 2026 release says total IP rose 0.1 percent in May after 0.9 percent in April, manufacturing output was 0.0 percent in May, mining rose 1.3 percent, utilities fell 0.4 percent, and total industry capacity utilization edged up to 76.2 percent."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 capacity utilization table for recent total industry values","result":"The total industry capacity utilization row shows May 2025 75.9, Dec 2025 75.6, Jan 2026 75.3, Feb 2026 75.8, Mar 2026 75.5, Apr 2026 76.1, and May 2026 76.2 percent."},{"kind":"tool","tool":"fred.history_mirror","call":"FRED TCU mirror for precise recent observations sourced to the Federal Reserve Board","result":"FRED TCU lists May 2026 76.1663, Apr 2026 76.1289, Mar 2026 75.5388, Feb 2026 75.8470, and Jan 2026 75.3050 percent; it also shows next release date Jul 17, 2026."},{"kind":"math","text":"Prior/update/interval: base rate prior is a near-persistence model for total industry utilization using the recent Federal Reserve/FRED reference class of monthly level changes from Dec 2025 through May 2026: -0.30, +0.54, -0.31, +0.59, +0.04 percentage point, giving sigma = 0.44. Level prior starts at May 2026 TCU 76.1663; momentum adjustment is +0.03 from the positive April-May IP/utilization trend, one-off adjustment is 0.00 because utilities weakness and mining strength offset, and policy-mechanism adjustment is 0.00. Point = 76.1663 + 0.03 = 76.20. 80% half-width is roughly 1.28*sigma = 1.28*0.44 = 0.56, rounded to a one-decimal first-print interval of 75.6 to 76.8."},{"kind":"text","text":"Counter-considerations: upside risk would come from another mining jump plus warmer-weather utility output and a rebound in manufacturing, which would land above the interval if utilization prints above 76.8. Downside risk is a June industrial production pullback or capacity benchmark-related weakness across manufacturing; a broad drop larger than about 0.6 point would land below the interval. Outside the interval would require a shock comparable to the largest recent month-to-month moves, not just normal rounding noise."},{"kind":"forecast","point":76.2,"ciLow":75.6,"ciHigh":76.8}]}

# Reviewer critique
{"summary":"Draft is publication-ready: resolver, prior/update/interval logic, tail scenarios, and JSON fields are coherent with the target contract.","requiredFixes":[],"optionalSuggestions":["Consider noting that the five-month volatility sample is intentionally short and recent; a longer monthly-change sample would make the interval basis stronger."]}

Emit the final JSON object only.
