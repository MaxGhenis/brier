# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: abs.labour.employment_change.australia
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "abs-labour-employment-change-australia-june-2026"
- country: "AU"
- targetUnit: "thousands"
- dataPointId: "abs.labour.employment_change.australia.june_2026.first_print"
- resolutionSourceUrl: "https://data.api.abs.gov.au/rest/data/LF/M3.3.1599.20.AUS.M?lastNObservations=30&format=jsondata"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["data.api.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "LF/M3.3.1599.20.AUS.M", "releasePolicy": "first_print", "sourceSeriesId": "LF/M3.3.1599.20.AUS.M", "sourceUrl": "https://data.api.abs.gov.au/rest/data/LF/M3.3.1599.20.AUS.M?lastNObservations=30&format=jsondata", "table": "Labour Force, Australia (dataflow LF: employed persons, seasonally adjusted, Australia; month-over-month change)", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-11-9a4cf7b9cebbebe4e882759f230d2b8ffe00c7c7a45533ba7e10642ad8e46eb5.json"
- targetContentHash: "9a4cf7b9cebbebe4e882759f230d2b8ffe00c7c7a45533ba7e10642ad8e46eb5"
- registrationCommit: "357f4e8477327d91775a345ece531f3eb42fa3b7"
- registeredAtUtc: "2026-07-11T18:10:24Z"

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
{"slug":"abs-labour-employment-change-australia-june-2026","country":"AU","type":"data","title":"Australia employment change, June 2026","question":"What will the ABS first report for the June 2026 month-over-month change in employed people, seasonally adjusted, Australia?","unit":"thousands","pointEstimate":18.0,"ciLow":-22.3,"ciHigh":58.3,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"Australian Bureau of Statistics Labour Force, Australia release","resolutionSourceUrl":"https://data.api.abs.gov.au/rest/data/LF/M3.3.1599.20.AUS.M?lastNObservations=30&format=jsondata","resolutionRule":"Resolve to the first value published by the Australian Bureau of Statistics for June 2026 in series LF/M3.3.1599.20.AUS.M: employed persons, seasonally adjusted, Australia, month-over-month change, in thousands. Use the first-print value as published, including its published precision; ignore all later revisions or corrections.","dataPointId":"abs.labour.employment_change.australia.june_2026.first_print","historicalContext":[{"label":"2026-05 employment change, SA, thousands","value":40.3},{"label":"2026-04 employment change, SA, thousands","value":-40.7},{"label":"2026-03 employment change, SA, thousands","value":19.4},{"label":"2026-02 employment change, SA, thousands","value":22.9},{"label":"2026-01 employment change, SA, thousands","value":34.7},{"label":"2025-12 employment change, SA, thousands","value":57.2}],"drivers":["Recent employment momentum remains positive","Vacancies declined 2.1% over three months","Survey modernisation raises sampling uncertainty","Underlying trend employment growth is near 20 thousand"],"sourceContext":["https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release","https://www.abs.gov.au/release-calendar/future-releases/202607/rcc_labour","https://www.abs.gov.au/statistics/labour/jobs/job-vacancies-australia/latest-release","https://data.api.abs.gov.au/rest/data/LF/M3.3.1599.20.AUS.M?lastNObservations=30&format=jsondata"],"runAt":"2026-07-11T18:14:15Z","reasoning":[{"kind":"heading","text":"Australia June 2026 seasonally adjusted employment change"},{"kind":"text","text":"The target is the first June 2026 print for ABS series LF/M3.3.1599.20.AUS.M, employed persons in Australia, seasonally adjusted, month-over-month change in thousands. It is not trend or original employment, and later revisions do not replace the first print."},{"kind":"tool","tool":"official.lookup","call":"Inspect the ABS Labour Force, Australia May 2026 release and its seasonally adjusted employment table.","result":"ABS reported May 2026 employed people at 14,738.8 thousand, up 40.3 thousand from April; the corresponding trend level was 14,753.7 thousand, up 20.2 thousand."},{"kind":"tool","tool":"official.lookup","call":"Fetch recent seasonally adjusted employed-person levels from the ABS Labour Force release table and calculate monthly changes.","result":"The latest 12 monthly changes from June 2025 through May 2026 were -10.5, 32.3, -13.2, 9.8, 33.8, -38.7, 57.2, 34.7, 22.9, 19.4, -40.7, and 40.3 thousand; their mean was 12.3 thousand."},{"kind":"tool","tool":"official.lookup","call":"Verify the June 2026 Labour Force publication date on the official ABS future-release calendar.","result":"The ABS calendar schedules Labour Force, Australia for Thursday 23 July 2026 at 11:30am AEST, with reference period June 2026."},{"kind":"tool","tool":"official.lookup","call":"Inspect the latest official ABS Job Vacancies release for labour-demand context.","result":"Seasonally adjusted job vacancies were 329.5 thousand in May 2026, down 2.1% or 7.1 thousand from February and 30.3% below the May 2022 peak."},{"kind":"text","text":"The outside-view base rate is the 12-month mean employment change of 12.3 thousand. Momentum is mildly stronger: the latest trend increase was 20.2 thousand and four of the latest five seasonally adjusted changes were positive. Against that, falling vacancies argue against extrapolating May's 40.3 thousand gain."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms point in different directions: the employment level remains high; recent momentum is positive; monthly Labour Force sampling and the survey-system transition can create one-off volatility; and softer labour demand should restrain underlying hiring. I therefore adjust the 12.3-thousand prior upward by 8 thousand for trend and momentum, then downward by about 2 thousand for weaker vacancies, yielding 18 thousand."},{"kind":"math","text":"Prior/update/interval: the persistence model uses the mean of the 12 fetched June 2025-May 2026 seasonally adjusted employment changes as the prior (12.3 thousand), with +8 thousand for recent positive momentum and the 20.2-thousand trend gain, and -2.3 thousand for weaker vacancies, giving 18.0 thousand. For this change/flow series, the interval method uses the values themselves: sample sigma = 31.5 thousand. The normal 80% half-width is 1.28*sigma = 1.28*31.5 = 40.3 thousand, so the final implied bounds are 18.0-40.3 = -22.3 and 18.0+40.3 = 58.3 thousand."},{"kind":"text","text":"Upside risk comes from another strong participation-supported hiring month or a favourable rotation-group draw and would land above the interval if employment rises by more than 58.3 thousand. Downside risk comes from sharper labour-demand weakening or adverse survey volatility and would land below the interval if employment falls by more than 22.3 thousand."},{"kind":"forecast","point":18.0,"ciLow":-22.3,"ciHigh":58.3}]}

# Reviewer critique
{"summary":"The draft is publication-ready against the rubric, with resolver, prior, update, interval, tails, and JSON fields coherent for the registered target.","requiredFixes":[],"optionalSuggestions":["Consider stating explicitly that the 31.5 thousand sigma is computed from the same 12 monthly changes listed in the prior sample.","The vacancy adjustment would be slightly clearer if tied to a rough historical elasticity or described as judgmental."]}

Emit the final JSON object only.
