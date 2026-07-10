# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: us.dol.initial_claims.sa
- period: week_2026-07-11
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-11"
- targetUnit: "thousands"
- dataPointId: "us.dol.initial_claims.sa.week_2026-07-11"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-18", "start": "2026-07-14"}, "field": "ICSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "ICSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA", "table": "ALFRED graph CSV", "transform": {"factor": 0.001, "operation": "multiply"}}

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
{"slug":"initial-claims-week-2026-07-11","country":"US","type":"data","title":"US Initial Claims, Week Ending Jul 11","question":"What will the U.S. Department of Labor Employment and Training Administration report as the advance seasonally adjusted initial claims for unemployment insurance for the week ending July 11, 2026, in the first print?","unit":"thousands","pointEstimate":218,"ciLow":204,"ciHigh":232,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260716","resolutionRule":"Resolve to the first published advance seasonally adjusted initial claims figure for the week ending July 11, 2026 in the U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims Report released on July 16, 2026. Convert persons to thousands by dividing by 1,000. Use the first print only; ignore later revisions, benchmark updates, and ALFRED/FRED vintage changes after the release.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-11","historicalContext":[{"label":"week ending 2026-07-04 advance initial claims SA","value":215},{"label":"week ending 2026-06-27 revised initial claims SA","value":217},{"label":"week ending 2026-07-04 four-week moving average SA","value":218.75},{"label":"week ending 2026-07-04 initial claims NSA","value":224.583},{"label":"comparable week 2025 initial claims NSA","value":241.361}],"drivers":["Recent SA level has held near 215 thousand for three reported weeks","Four-week SA average is 218.75 thousand and falling","Unadjusted claims rose less than seasonal factors expected in the latest release","Holiday-week seasonal adjustment around early July can add first-print noise","Continuing claims remain elevated but not sharply accelerating"],"sourceContext":["https://www.dol.gov/newsroom/releases/eta/eta20260709","https://www.dol.gov/newsroom/releases/eta","https://oui.doleta.gov/unemploy/claims.asp","https://www.dol.gov/newsroom/economicdata"],"runAt":"2026-07-10T03:25:11Z","reasoning":[{"kind":"heading","text":"US initial claims SA forecast for week ending July 11, 2026"},{"kind":"text","text":"Framing and exact resolver: the target is DOL ETA Unemployment Insurance Weekly Claims, series ICSA / advance seasonally adjusted initial claims, for the week ending July 11, 2026. The ledger unit is thousands and the first-print resolver is the July 16, 2026 DOL release; FRED/ALFRED may mirror history but the official DOL release is the resolution source."},{"kind":"tool","tool":"official.lookup","call":"Opened DOL ETA release archive for recent Unemployment Insurance Weekly Claims Reports and release timing.","result":"Fetched official archive entries: July 9, 2026 release for week ending July 4 had initial claims SA 215,000; July 2, 2026 release for week ending June 27 had initial claims SA 215,000 before revision; June 25, 2026 release for week ending June 20 had initial claims SA 215,000."},{"kind":"tool","tool":"official.lookup","call":"Opened the July 9, 2026 DOL Unemployment Insurance Weekly Claims Report PDF.","result":"Fetched latest official first-print/revised values: week ending July 4 advance initial claims SA 215,000; previous week revised level 217,000; 4-week moving average 218,750; prior-year comparable initial claims SA 228,000."},{"kind":"tool","tool":"official.lookup","call":"Read DOL July 9 release table for unadjusted and continuing-claims context.","result":"Fetched latest NSA and continuing context: initial claims NSA 224,583 for week ending July 4 versus 214,616 prior week and 241,361 one year earlier; insured unemployment SA 1,814,000 for week ending June 27."},{"kind":"tool","tool":"official.lookup","call":"Checked DOL economic data and OUI pages for publication channel and data currency.","result":"Fetched DOL publication context: the OUI weekly claims data page was updated July 9, 2026; DOL economic data page identifies ETA as publisher of the Unemployment Insurance Weekly Claims Report; the latest release was embargoed until 8:30 a.m. Eastern on Thursday, July 9, 2026."},{"kind":"text","text":"Variant discipline: every anchor above is for regular state-program initial claims, seasonally adjusted where the target says SA. NSA figures are used only as a holiday/seasonal-adjustment diagnostic, not as the target level."},{"kind":"text","text":"Reference class and base rate: the recent official-source reference class is weekly first-print/revised SA initial claims around the current level. The latest reported sequence is roughly 189, 200, 211, 209, 215, 225, 229, 226, 215, 217, and 215 thousand across late April through July 4, with the last three target-consistent readings clustered at 215-217 thousand and a 218.75 thousand four-week average."},{"kind":"math","text":"Prior/update/interval: persistence prior uses the latest official SA level of 215 thousand and the 4-week average of 218.75 thousand; historical sample is the latest official weekly SA sequence from late April through July 4. Adjustment components are +2 thousand toward the 4-week average, +1 thousand for mild mean reversion after several sub-220 readings, and 0 thousand for no clear layoff shock. Point = 215 + 2 + 1 = 218 thousand. For interval width, compute successive weekly changes on the fetched SA history; including the April 25 holiday drop gives sigma = 11.0 thousand, so 1.28*sigma = 14.1 thousand. Rounding to whole thousands gives an 80% interval of 218 +/- 14 = 204 to 232 thousand."},{"kind":"text","text":"Counter-considerations: upside risk is a sharper post-holiday or auto-related claims rise that would land above the interval, especially if large states reverse the latest NSA shortfall. Downside risk is another benign seasonal adjustment print near 200 thousand. A genuine outside the interval downside would require the SA first print to fall below 204 thousand, which would be a larger move than the recent non-holiday changes."},{"kind":"forecast","point":218,"ciLow":204,"ciHigh":232}]}

# Reviewer critique
{"summary":"The draft is publication-ready with only minor clarity improvements; resolver, units, prior/update math, interval, and JSON fields are coherent.","requiredFixes":[],"optionalSuggestions":["Clarify that the 80% interval uses recent weekly SA changes from the cited late-April-to-July-4 sequence, since the exact calculation is only summarized.","If the catalog resolver ultimately uses ALFRED advance vintage as the mechanical adapter, mention that DOL is the official first-print source and ALFRED is only the mirrored retrieval mechanism."]}

Emit the final JSON object only.
