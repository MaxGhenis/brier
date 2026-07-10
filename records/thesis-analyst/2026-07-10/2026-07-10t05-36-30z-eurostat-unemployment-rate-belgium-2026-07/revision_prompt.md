# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: eurostat.unemployment_rate.belgium
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "belgium-unemployment-rate-july-2026"
- country: "BE"
- targetUnit: "percent"
- dataPointId: "eurostat.une_rt_m.unemployment_rate.belgium.2026_07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["ec.europa.eu"], "expectedReleaseWindow": {"end": "2026-09-03", "start": "2026-08-26"}, "field": "eurostat.unemployment_rate.belgium", "releasePolicy": "first_print", "sourceSeriesId": "eurostat.unemployment_rate.belgium", "sourceUrl": "https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en", "table": "Eurostat monthly unemployment euro-indicators release / une_rt_m data page", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-f2450430ddeb46be2e3d63b9b8e4a4e1b976b106bf685c4aecdd49b40f482653.json"
- targetContentHash: "f2450430ddeb46be2e3d63b9b8e4a4e1b976b106bf685c4aecdd49b40f482653"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"

# Source hints
- Use Eurostat euro-indicators release calendar and official HICP/IP pages.
- Euro-area HICP rates print to one decimal.
- Resolution source should be the Eurostat release/data page.

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
{"slug":"belgium-unemployment-rate-july-2026","country":"BE","type":"data","title":"Belgium unemployment rate, July 2026","question":"What will Eurostat first print for Belgium's seasonally adjusted total unemployment rate, age 15-74, in July 2026 in une_rt_m?","unit":"percent","pointEstimate":6.1,"ciLow":5.9,"ciHigh":6.3,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"Eurostat monthly unemployment euro-indicators release / une_rt_m data page","resolutionSourceUrl":"https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","resolutionRule":"Resolve to the first Eurostat print in table une_rt_m for geo=BE, s_adj=SA, sex=T, age=Y15-74, unit=PC_ACT, time=2026-07, reported in percent to one decimal. Use the first official value published for that monthly observation; do not substitute later revisions.","dataPointId":"eurostat.une_rt_m.unemployment_rate.belgium.2026_07.first_print","historicalContext":[{"label":"2026-03 Eurostat une_rt_m BE SA total age 15-74","value":6.1},{"label":"2026-04 Eurostat une_rt_m BE SA total age 15-74","value":6.1},{"label":"2026-05 Eurostat une_rt_m BE SA total age 15-74","value":6.0},{"label":"2025-06 Eurostat une_rt_m BE SA total age 15-74","value":6.5}],"drivers":["Latest available Belgium monthly unemployment rate was near 6.0 percent rather than materially rising.","Monthly one-decimal unemployment rates are highly persistent; recent changes are mostly 0.0 or 0.1 percentage point.","Small upside pressure from a softer Belgian labour market is offset by stable euro-area unemployment conditions.","First-print target is the Eurostat seasonally adjusted total age 15-74 PC_ACT variant, not a national unadjusted or revised series."],"sourceContext":["https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","https://ec.europa.eu/eurostat/web/main/news/euro-indicators/release-calendar","https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/une_rt_m?geo=BE&sex=T&age=Y15-74&s_adj=SA&unit=PC_ACT&lastTimePeriod=12&lang=en"],"runAt":"2026-07-10T05:37:39Z","reasoning":[{"kind":"heading","text":"Belgium July 2026 unemployment first print"},{"kind":"text","text":"Framing and exact resolver: this forecast targets Eurostat table une_rt_m, Belgium geo=BE, seasonally adjusted s_adj=SA, total sex=T, age Y15-74, unit PC_ACT, for 2026-07. I use the same variant for anchors and history and resolve on the first official Eurostat print, rounded to one decimal percent."},{"kind":"tool","tool":"official.lookup","call":"Checked Eurostat Euro-indicators release calendar for the Unemployment indicator and the July 2026 monthly release timing.","result":"Official calendar context used for this run: the unemployment release is scheduled for 2026-09-01 in Europe/Luxembourg time, inside the registered 2026-08-26 to 2026-09-03 window; this fixes resolutionDate=2026-09-01."},{"kind":"tool","tool":"official.lookup","call":"Queried Eurostat une_rt_m for the latest Belgium SA total age 15-74 unemployment rates in percent of active population.","result":"Fetched latest same-variant values: 2026-03=6.1, 2026-04=6.1, 2026-05=6.0 percent for BE, s_adj=SA, sex=T, age=Y15-74, unit=PC_ACT."},{"kind":"tool","tool":"official.lookup","call":"Queried Eurostat une_rt_m for a recent reference class of Belgium monthly observations in the same variant.","result":"Fetched recent history: 2025-06=6.5, 2025-07=6.4, 2025-08=6.3, 2025-09=6.2, 2025-10=6.2, 2025-11=6.1, 2025-12=6.1, 2026-01=6.1, 2026-02=6.0, 2026-03=6.1, 2026-04=6.1, 2026-05=6.0 percent."},{"kind":"text","text":"Base rate / reference class: the same-series outside view is strong persistence around 6.0 to 6.2 percent after a drift down from 6.5 percent in mid-2025. With only June and July still to print before the target, the base rate says July should usually remain within a few tenths of the latest 6.0 percent."},{"kind":"math","text":"Prior/update/interval: persistence prior from the 12-month Eurostat same-variant sample is latest value 6.0. Successive monthly changes are -0.1,-0.1,-0.1,0.0,-0.1,0.0,0.0,-0.1,+0.1,0.0,-0.1, so sigma = 0.07 percentage point. For a two-month-ahead July value, 1.28*sigma*sqrt(2)=1.28*0.07*1.41=0.13. I widen to 0.20, about 1.54x the mechanical two-step half-width, because first-print monthly labour-force estimates are rounded to one decimal and can absorb small survey noise. Level 6.0 plus a +0.05 soft-labour-market adjustment rounds the point to 6.1; 6.1 +/- 0.2 gives 5.9 to 6.3."},{"kind":"text","text":"Level, momentum, one-off, and policy effects: level is near 6.0; momentum is mildly downward over the prior year but flat in spring 2026; I see no one-off July mechanism large enough to move the rate by more than a few tenths; policy effects are slow-moving and do not justify departing from the persistence prior."},{"kind":"text","text":"Counter-considerations: upside risk is a sharp deterioration in hiring or labour-force re-entry that would push the first print to 6.4 or above, outside the interval. Downside risk is a stronger summer employment gain or favourable survey rotation that would land below the interval at 5.8 or less."},{"kind":"forecast","point":6.1,"ciLow":5.9,"ciHigh":6.3}]}

# Reviewer critique
{"summary":"Draft is publishable after tightening the evidence for the small upward adjustment from the persistence prior.","requiredFixes":[{"rubricItem":"update","severity":"warning","summary":"The +0.05 soft-labour-market adjustment moves the rounded point from a 6.0 latest-value persistence prior to 6.1, but the draft does not cite concrete current evidence for Belgian labour-market softness beyond same-series persistence and mild downward/flat momentum.","actionRequested":"Either add specific cited evidence supporting the upside adjustment, or remove/neutralize the adjustment and make the final point follow the stated persistence prior."}],"optionalSuggestions":["State explicitly that the 5.9-6.3 interval is centered on the rounded 6.1 point and is an 80% interval after widening for first-print and rounding uncertainty.","Keep the Eurostat release-calendar check in the final trace because it supports the 2026-09-01 resolutionDate within the registered release window."]}

Emit the final JSON object only.
