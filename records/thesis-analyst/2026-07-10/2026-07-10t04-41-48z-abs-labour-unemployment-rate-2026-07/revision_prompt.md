# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: abs.labour.unemployment_rate
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "australia-unemployment-rate-july-2026"
- targetUnit: "percent"
- dataPointId: "abs.labour.unemployment_rate.australia.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-08-27", "start": "2026-08-19"}, "field": "abs.labour.unemployment_rate", "releasePolicy": "first_print", "sourceSeriesId": "abs.labour.unemployment_rate", "sourceUrl": "https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release", "table": "Australian Bureau of Statistics Labour Force, Australia, June 2026", "transform": {"factor": 1.0, "operation": "multiply"}}

# Source hints
- Use ABS release calendar and official monthly CPI indicator pages.
- Australia CPI indicator rates print to one decimal.
- Resolution source should be the ABS release page.

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
{"slug":"australia-unemployment-rate-july-2026","country":"AU","type":"data","title":"Australia unemployment rate, July 2026","question":"What will the Australian Bureau of Statistics seasonally adjusted unemployment rate for Australia be for July 2026 in the first print of Labour Force, Australia?","unit":"percent","pointEstimate":4.5,"ciLow":4.3,"ciHigh":4.7,"confidence":0.8,"resolutionDate":"2026-08-20","resolutionSource":"Australian Bureau of Statistics Labour Force, Australia, July 2026","resolutionSourceUrl":"https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release","resolutionRule":"Resolve to the ABS national seasonally adjusted unemployment rate, in percent, for reference period July 2026 as first published in Labour Force, Australia, July 2026. Use the first public print rounded to one decimal percent and ignore later revisions or corrections.","dataPointId":"abs.labour.unemployment_rate.australia.july_2026.first_print","historicalContext":[{"label":"Feb 2026 seasonally adjusted unemployment rate","value":4.3},{"label":"Mar 2026 seasonally adjusted unemployment rate","value":4.3},{"label":"Apr 2026 seasonally adjusted unemployment rate","value":4.5},{"label":"May 2026 seasonally adjusted unemployment rate","value":4.4},{"label":"May 2026 trend unemployment rate","value":4.4}],"drivers":["Latest ABS first-print unemployment rate was 4.4% in May 2026 after 4.5% in April","Trend unemployment rate had edged up to 4.4% by May 2026","May employment rose 40,300 and unemployed people fell 18,300, limiting near-term upside","July survey reference period runs 28 June to 11 July, so much of the outcome is already fixed by run date","Monthly unemployment prints have recently moved by about 0.13 percentage points per month"],"sourceContext":["https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release","https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia","https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/jul-2025"],"runAt":"2026-07-10T04:42:06Z","reasoning":[{"kind":"heading","text":"Australia July 2026 unemployment first-print forecast"},{"kind":"text","text":"The resolver is the ABS Labour Force, Australia national unemployment rate, seasonally adjusted variant, for July 2026. The relevant ABS graph table is the unemployment-rate table with columns Trend (%) and Seasonally adjusted (%); all anchors below use the seasonally adjusted national rate unless explicitly labelled trend."},{"kind":"tool","tool":"official.lookup","call":"Opened ABS Labour Force, Australia latest release page for reference period, latest print, headline statistics, future release dates, and survey dates.","result":"Fetched latest release reference period May 2026, released 25/06/2026; seasonally adjusted unemployment rate 4.4%, down 0.1 ppts from April 2026 at 4.5%; unemployed people 671,300, down 18,300; employed people 14,738,800, up 40,300."},{"kind":"tool","tool":"official.lookup","call":"Opened ABS Labour Force, Australia all-releases page to verify the official release schedule for the target month.","result":"Fetched future release schedule: Labour Force, Australia, June 2026 release date 23/07/2026 11:30am AEST; July 2026 release date 20/08/2026 11:30am AEST; August 2026 release date 24/09/2026 11:30am AEST."},{"kind":"tool","tool":"official.lookup","call":"Read the ABS unemployment-rate history table on the latest Labour Force release page.","result":"Fetched recent seasonally adjusted unemployment-rate prints: Feb 2026 4.3%, Mar 2026 4.3%, Apr 2026 4.5%, May 2026 4.4%; also Sep 2025 4.5%, Oct 2025 4.3%, Nov 2025 4.3%, Dec 2025 4.1%, Jan 2026 4.1%."},{"kind":"tool","tool":"official.lookup","call":"Read ABS survey timing rows for the July 2026 Labour Force collection.","result":"Fetched July 2026 survey timing: reference week starts 28 June 2026 and ends 11 July 2026; enumeration starts 5 July 2026 and ends 25 July 2026; May 2026 collection ran 3 May to 16 May with enumeration 10 May to 30 May."},{"kind":"text","text":"Reference class/base rate: for a short-horizon national unemployment-rate forecast, the base rate is persistence from the latest official seasonally adjusted ABS print, with recent monthly changes providing the dispersion. The latest level is 4.4%, the trend estimate is also 4.4%, and the recent sequence has more upward than downward drift from late 2025 into May 2026, so I center slightly above May rather than exactly at 4.4%."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest ABS seasonally adjusted unemployment rate of 4.4%; historical sample = rounded monthly ABS seasonally adjusted rates from Jun 2024 through May 2026, using successive changes for the level/rate series; adjustment components = +0.05 ppt level/momentum from trend rising to 4.4 and April-May staying high, +0.03 ppt two-month horizon drift, -0.02 ppt from May employment strength, net +0.06 ppt, giving 4.46 rounded to a 4.5% point. Monthly-change sigma from the 23 successive rounded changes is about 0.13 ppt; two-month horizon sigma = sqrt(2)*0.13 = 0.18, so sigma = 0.18 and 80% half-width = 1.28*0.18 = 0.23 ppt. Applying that to 4.46 gives 4.23 to 4.69, rounded to a one-decimal-compatible 4.3% to 4.7% interval."},{"kind":"text","text":"Counter-considerations: upside risk is a weak June print followed by July job losses or a participation rebound that would lift unemployment to 4.8% or higher and land above the interval. Downside risk is another strong employment month with lower participation that would push the first print to 4.2% or lower and land below the interval. Outside the interval would likely require two same-direction monthly surprises rather than ordinary one-month noise."},{"kind":"forecast","point":4.5,"ciLow":4.3,"ciHigh":4.7}]}

# Reviewer critique
{"summary":"Draft is mostly publication-ready, but it should explicitly flag the ledger/sourceBinding table-month discrepancy before publication.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"Canonical sourceBinding.table says \"Labour Force, Australia, June 2026\" while the target, dataPointId, release schedule, and draft resolver all point to July 2026 first print.","actionRequested":"Add a brief reasoning note that the ledger table label appears to be a month typo and that the forecast remains tied to the July 2026 first-print unemployment-rate target."}],"optionalSuggestions":["Clarify that the July reference week was still in progress at run time on 2026-07-10, so the outcome was only partly fixed rather than fully observed.","If space allows, show or cite the full Jun 2024-May 2026 monthly-change sample behind the 0.13 ppt volatility estimate."]}

Emit the final JSON object only.
