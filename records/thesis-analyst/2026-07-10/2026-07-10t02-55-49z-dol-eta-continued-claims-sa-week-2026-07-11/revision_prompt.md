# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: dol.eta.continued_claims.sa
- period: week_2026-07-11
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-07-11"
- targetUnit: "millions"
- dataPointId: "dol.eta.continued_claims.sa.week_2026-07-11.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-25", "start": "2026-07-21"}, "field": "CCSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "CCSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA", "table": "ALFRED graph CSV", "transform": {"factor": 1e-06, "operation": "multiply"}}

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
{"slug":"continued-claims-week-2026-07-11","country":"US","type":"data","title":"US Continued Claims, Jul 11 2026","question":"What will the U.S. Department of Labor Employment and Training Administration first report for seasonally adjusted continued claims (insured unemployment), CCSA, for the week ending July 11, 2026?","unit":"millions","pointEstimate":1.817,"ciLow":1.776,"ciHigh":1.858,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor Employment and Training Administration, Unemployment Insurance Weekly Claims News Release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the first DOL ETA Unemployment Insurance Weekly Claims News Release published on July 23, 2026 at 8:30 a.m. ET. Use the Seasonally Adjusted Data / Unemployment Insurance Data for Regular State Programs line for Insured Unemployment (SA) for the week ending July 11, 2026, convert persons to millions by multiplying by 0.000001, and round to three decimals. Ignore later revisions and use ALFRED/FRED only as first-vintage retrieval aids if needed.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-11.first_print","historicalContext":[{"label":"2026-06-27 CCSA latest","value":1.814},{"label":"2026-06-20 CCSA","value":1.806},{"label":"2026-06-13 CCSA","value":1.812},{"label":"2026-06-06 CCSA","value":1.8},{"label":"2026-05-30 CCSA","value":1.786}],"drivers":["latest seasonally adjusted insured unemployment was 1.814 million","four-week average was 1.808 million","initial claims for week ending July 4 were 215,000","recent continued-claims momentum is mildly upward but choppy","target is the SA CCSA variant, not NSA or all-program continued weeks claimed"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims_arch.asp","https://fred.stlouisfed.org/series/CCSA","https://alfred.stlouisfed.org/series?seid=CCSA"],"runAt":"2026-07-10T02:56:40Z","reasoning":[{"kind":"heading","text":"Forecast for DOL ETA CCSA, Week Ending July 11 2026"},{"kind":"text","text":"Framing and exact resolver: this target is DOL ETA seasonally adjusted insured unemployment, series CCSA, for the week ending July 11, 2026, first print only. All anchors below use the same seasonally adjusted continued-claims variant, not unadjusted state claims and not total continued weeks claimed across all programs."},{"kind":"tool","tool":"official.lookup","call":"Opened the DOL Office of Unemployment Insurance archive and publication schedule page for the UI Weekly Claims News Release.","result":"Fetched schedule says the UI Weekly Claims News Release is published each Thursday at 8:30 AM EST, with 1 listed 2026 exception, Wednesday November 25, 2026; page updated July 9, 2026. Therefore the first DOL release carrying insured unemployment for week ending July 11, 2026 is Thursday July 23, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened the latest DOL UI Weekly Claims News Release PDF published July 9, 2026.","result":"Fetched latest official SA data: initial claims for week ending July 4, 2026 were 215,000; insured unemployment for week ending June 27, 2026 was 1,814,000; previous week revised level was 1,806,000; 4-week moving average was 1,808,000."},{"kind":"tool","tool":"mirror.lookup","call":"Opened FRED series CCSA as a public history mirror for the DOL ETA series identity and latest observations.","result":"Fetched CCSA observations: 2026-06-27 = 1,814,000; 2026-06-20 = 1,806,000; 2026-06-13 = 1,812,000; 2026-06-06 = 1,800,000; 2026-05-30 = 1,786,000. Units are Number, Seasonally Adjusted, Weekly ending Saturday."},{"kind":"tool","tool":"mirror.lookup","call":"Opened ALFRED vintage series page for CCSA to confirm the vintage-capable series binding.","result":"Fetched ALFRED CCSA page showing 2026-06-27 = 1,814,000, source U.S. Employment and Training Administration, release Unemployment Insurance Weekly Claims Report, seasonal adjustment Seasonally Adjusted, and release-date coverage through 2026-07-09."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL PDF historical SA weekly claims table for recent CCSA dispersion.","result":"Fetched recent insured unemployment SA history in thousands: Jan 3 2026 = 1,875; Jan 10 = 1,865; Jan 17 = 1,823; Jan 24 = 1,842; Jan 31 = 1,859; Feb 7 = 1,865; Feb 14 = 1,827; Feb 21 = 1,871; Feb 28 = 1,847; Mar 7 = 1,851; Mar 14 = 1,816; Mar 21 = 1,832; Mar 28 = 1,787; Apr 4 = 1,809; Apr 11 = 1,808; Apr 18 = 1,776; Apr 25 = 1,758; May 2 = 1,776; May 9 = 1,771; May 16 = 1,785; May 23 = 1,771; May 30 = 1,786; Jun 6 = 1,800; Jun 13 = 1,812; Jun 20 = 1,806; Jun 27 = 1,814."},{"kind":"text","text":"The reference class and base rate are short-horizon weekly changes in the same SA insured-unemployment level. Recent history is centered near 1.81 million: the latest print is 1.814 million, the latest 4-week average is 1.808 million, and the latest five observations average 1.804 million."},{"kind":"math","text":"Prior/update/interval: persistence prior is 1.814 million from the latest CCSA first-print/mirror observation; historical sample is the 26 recent weekly SA changes from Jan 3 through Jun 27, 2026: -25, -10, -42, 19, 17, 6, -38, 44, -24, 4, -35, 16, -45, 22, -1, -32, -18, 18, -5, 14, -14, 15, 14, 12, -6, 8 thousand. The sample standard deviation is sigma = 0.023 million; 1.28*sigma = 0.029 million. For a two-week-ahead first print I scale by sqrt(2), giving about 0.041 million half-width. Level adjustment is +0.003 million because June-to-late-June momentum is mildly positive while latest initial claims at 215,000 are stable. Final bounds are 1.817 - 0.041 = 1.776 and 1.817 + 0.041 = 1.858."},{"kind":"text","text":"Upside risk: if continuing-benefit duration lengthens or July school/auto seasonal adjustment noise pushes repeat claims higher, the value would land above the interval. Downside risk: if the 215,000 initial-claims week maps into fewer continuing claims or the June rise revises away in the first July prints, it would land below the interval. A shock large enough to move weekly SA continued claims by more than about 40,000 over the next two target weeks is outside the interval scenario."},{"kind":"forecast","point":1.817,"ciLow":1.776,"ciHigh":1.858}]}

# Reviewer critique
{"summary":"Publishable with minor tightening: the resolver, unit, first-print rule, prior, update, interval, and JSON fields are broadly coherent, but the interval sample description has a counting inconsistency and the update could be quantified more clearly.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The volatility sample says it uses 26 recent weekly changes from Jan 3 through Jun 27, 2026, but the displayed Jan 3 through Jun 27 levels imply 25 within-sample changes; the listed first change appears to require a prior Dec 2025 observation not shown.","actionRequested":"Clarify the volatility sample by either adding the missing pre-Jan-3 observation or changing the description/count to match the displayed observations."},{"rubricItem":"update","severity":"warning","summary":"The +0.003 million adjustment is directionally plausible but only loosely tied to quantified evidence beyond 'mildly positive' momentum and stable initial claims.","actionRequested":"State the adjustment arithmetic explicitly, for example how much comes from recent CCSA momentum versus initial-claims stability, or say it is a judgmental small upward adjustment."}],"optionalSuggestions":["Mention that ALFRED/FRED are retrieval mirrors only and DOL ETA remains the resolving source, matching the ledger source-binding constraint.","For tail scenarios, name approximate numeric thresholds, such as below 1.776 million or above 1.858 million, to make the interval interpretation sharper."]}

Emit the final JSON object only.
