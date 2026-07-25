# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fed.g17.industrial_production.total_index_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "fed-g17-industrial-production-total-index-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "fed.g17.industrial_production.total_index_mom.2026-07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.federalreserve.gov"], "expectedReleaseWindow": {"end": "2026-08-21", "start": "2026-08-13"}, "field": "INDPRO", "releasePolicy": "first_print", "sourceSeriesId": "INDPRO", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=INDPRO", "table": "G.17 Industrial Production and Capacity Utilization, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-25-1c094ee348b852723e3688fabd1382fc7f4f49e12b96cd97b987441d17a4ba27.json"
- targetContentHash: "1c094ee348b852723e3688fabd1382fc7f4f49e12b96cd97b987441d17a4ba27"
- registrationCommit: "add78fbd9af9ca9b0c7389a9a44a7ec839f2f4af"
- registeredAtUtc: "2026-07-25T15:18:08Z"

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
{"slug":"fed-g17-industrial-production-total-index-mom-july-2026","country":"US","type":"data","title":"US Total Industrial Production MoM, Jul 2026","question":"Federal Reserve G.17 total industrial production index, seasonally adjusted monthly percent change for July 2026, first print.","unit":"percent_growth","pointEstimate":0.1,"ciLow":-0.6,"ciHigh":0.8,"confidence":0.8,"resolutionDate":"2026-08-18","resolutionSource":"Federal Reserve G.17 Industrial Production and Capacity Utilization","resolutionSourceUrl":"https://www.federalreserve.gov/releases/g17/current/table11.htm","resolutionRule":"Resolve to the first Federal Reserve G.17 monthly release for July 2026, Table 11 IP percent change / Total IP monthly rate, seasonally adjusted, preliminary first print. Use the one-decimal percent change printed by the agency on the initial August 18, 2026 release; ignore later revisions, same-day corrections not included in the first posted release, and the planned autumn 2026 annual revision.","dataPointId":"fed.g17.industrial_production.total_index_mom.2026-07.first_print","historicalContext":[{"label":"June 2026 preliminary monthly percent change","value":0.1},{"label":"May 2026 revised monthly percent change","value":0.1},{"label":"April 2026 revised monthly percent change","value":0.8},{"label":"March 2026 revised monthly percent change","value":-0.3},{"label":"February 2026 revised monthly percent change","value":0.9},{"label":"January 2026 revised monthly percent change","value":-0.4}],"drivers":["Recent total IP momentum is mildly positive after Q2 growth but June slowed to 0.1 percent.","Manufacturing was flat in June while mining and utilities each added 0.4 percent, leaving the July balance sensitive to energy and weather components.","The 2023-2026 reference class has frequent monthly reversals around a near-flat base rate, so a small positive point with a wide 80 percent interval is appropriate.","Capacity utilization at 76.1 percent remains below its long-run average, limiting evidence for a strong sustained production acceleration."],"sourceContext":["https://www.federalreserve.gov/releases/g17/","https://www.federalreserve.gov/releases/g17/current/default.htm","https://www.federalreserve.gov/releases/g17/current/table1.htm","https://www.federalreserve.gov/releases/g17/current/table11.htm","https://fred.stlouisfed.org/series/INDPRO"],"runAt":"2026-07-25T15:58:18Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 Total Industrial Production MoM"},{"kind":"text","text":"The target is the Federal Reserve G.17 Total IP monthly percent change, seasonally adjusted, for July 2026 on the first official print. The same seasonally adjusted Total IP variant is used for the anchors and interval; the ledger sourceBinding names INDPRO, while the forecasted value is the G.17 monthly percent-change print derived from that total index target."},{"kind":"tool","tool":"official.lookup","call":"Checked the Federal Reserve G.17 release dates page for the official August 2026 calendar date.","result":"The Federal Reserve G.17 calendar lists 2026 releases including July 17 as the most recent monthly release and August 18, 2026 as the next monthly release; monthly releases are issued at 9:15 a.m."},{"kind":"tool","tool":"official.lookup","call":"Read the Federal Reserve current G.17 release summary dated July 17, 2026.","result":"The current release says total industrial production ticked up 0.1 percent in June 2026, grew at a 4.0 percent annual rate in Q2, stood at 102.6 percent of its 2017 average, was 1.1 percent above June 2025, and capacity utilization was 76.1 percent."},{"kind":"tool","tool":"official.lookup","call":"Read Federal Reserve G.17 Table 1 for the recent monthly Total IP and major industry group changes.","result":"Table 1 reports Total IP monthly changes for Jan-Jun 2026 of -0.4, 0.9, -0.3, 0.8, 0.1, and 0.1 percent; June 2026 manufacturing was 0.0 percent, mining was 0.4 percent, and utilities was 0.4 percent."},{"kind":"tool","tool":"official.lookup","call":"Read Federal Reserve G.17 Table 11 for the historical reference class and index levels.","result":"Table 11 reports Total IP monthly percent changes of -0.3, 1.0, -0.1, 0.1, -0.2, 0.5, 0.4, -0.3, 0.0, -0.4, -0.2, 0.5 for 2025 and -0.4, 0.9, -0.3, 0.8, 0.1, 0.1 for Jan-Jun 2026; it also lists IP index levels of 101.0, 101.9, 101.6, 102.4, 102.6, and 102.6 for Jan-Jun 2026."},{"kind":"tool","tool":"history.lookup","call":"Checked FRED INDPRO as a public mirror for recent total index levels and the next release marker, while keeping the Federal Reserve as resolver.","result":"FRED INDPRO shows Jun 2026 at 102.6395, May 2026 at 102.5606, Apr 2026 at 102.4196, Mar 2026 at 101.6172, and Feb 2026 at 101.9263; it lists the next release date as Aug 18, 2026."},{"kind":"text","text":"The base rate / reference class is official G.17 monthly Total IP percent changes from 2023 through June 2026. Across those 42 fetched monthly prints the mean is about 0.07 percent, while the latest six months average 0.20 percent and the latest two months are both 0.1 percent. I anchor near persistence at 0.1 percent rather than extrapolating the strong April-February rebound."},{"kind":"math","text":"Prior/update/interval: persistence prior is 0.1 percent from the latest June and May prints, with a 2023-Jun 2026 official Table 11 reference-class base rate near 0.07 percent; adjustment components are +0.05 for Q2 annualized strength, -0.05 for flat June manufacturing and below-average utilization, and 0.00 for unknown July weather/energy noise, leaving a 0.10 point. For the interval, use the 42 monthly change values from 2023-Jun 2026; sigma = 0.55 percentage point from those fetched values, so 1.28*sigma = 0.70 percentage point. Point 0.10 minus/plus 0.70 gives -0.60 to 0.80."},{"kind":"text","text":"Upside risk is a hot-weather utilities jump plus another mining gain or auto rebound, which would land above the interval if July Total IP prints above 0.8 percent. Downside risk is a reversal in durable manufacturing or utilities after June strength, which would land below the interval if the first print is below -0.6 percent; outside the interval would require a broad sector move rather than ordinary month-to-month noise."},{"kind":"forecast","point":0.1,"ciLow":-0.6,"ciHigh":0.8}]}

# Reviewer critique
{"summary":"Publishable with only minor clarity tightening: resolver, unit, first-print rule, prior/update math, interval, tails, and JSON fields are broadly coherent.","requiredFixes":[{"rubricItem":"base_rate","severity":"warning","summary":"The prior is present, but it appears after current-evidence tool notes and driver language, so the draft does not cleanly state the base-rate/persistence anchor before inside-view updates.","actionRequested":"Move or duplicate the base-rate sentence near the start of reasoning before current June/Q2 manufacturing/utilization discussion, naming the 2023-Jun 2026 sample and the 0.1 percent persistence anchor."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The interval method cites 42 monthly values from 2023-Jun 2026, but the visible evidence only enumerates 2025 and Jan-Jun 2026 values, so the historical sample behind sigma is not fully auditable from the draft text.","actionRequested":"Add a compact note that the 2023-2024 Table 11 monthly changes were included in the 42-month sigma calculation, or state where those fetched values are recorded."}],"optionalSuggestions":["Use the Federal Reserve release dates page or eventual archived August 18 release page as the resolver URL if the catalog supports a stable first-print archive link.","Keep FRED/ALFRED described only as a mirror or index-level history aid, with Federal Reserve G.17 Table 11 as the resolving authority."]}

Emit the final JSON object only.
