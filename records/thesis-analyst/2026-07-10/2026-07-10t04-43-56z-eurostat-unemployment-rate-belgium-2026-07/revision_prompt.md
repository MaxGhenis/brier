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
- targetUnit: "percent"
- dataPointId: "eurostat.une_rt_m.unemployment_rate.belgium.2026_07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["ec.europa.eu"], "expectedReleaseWindow": {"end": "2026-09-03", "start": "2026-08-26"}, "field": "eurostat.unemployment_rate.belgium", "releasePolicy": "first_print", "sourceSeriesId": "eurostat.unemployment_rate.belgium", "sourceUrl": "https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en", "table": "Eurostat monthly unemployment euro-indicators release / une_rt_m data page", "transform": {"factor": 1.0, "operation": "multiply"}}

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
{"slug":"belgium-unemployment-rate-july-2026","country":"EA","type":"data","title":"Belgium unemployment rate, July 2026","question":"Eurostat une_rt_m unemployment rate for Belgium, July 2026, seasonally adjusted, total sex, age 15-74, percent of active population, first print","unit":"percent","pointEstimate":6.5,"ciLow":6.3,"ciHigh":6.7,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"Eurostat unemployment by sex and age - monthly data (une_rt_m)","resolutionSourceUrl":"https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","resolutionRule":"Resolve to the first value published by Eurostat in table une_rt_m for geo=BE, sex=T, age=Y15-74, s_adj=SA, unit=PC_ACT, time=2026-07. Use the first-print one-decimal percent value and ignore later revisions or corrected vintages unless Eurostat explicitly replaces the first publication before public release.","dataPointId":"eurostat.une_rt_m.unemployment_rate.belgium.2026_07.first_print","historicalContext":[{"label":"2026-05 latest Eurostat une_rt_m BE SA total 15-74","value":6.5},{"label":"2026-04 Eurostat une_rt_m BE SA total 15-74","value":6.5},{"label":"2026-03 Eurostat une_rt_m BE SA total 15-74","value":6.5},{"label":"2025-12 Eurostat une_rt_m BE SA total 15-74","value":6.4},{"label":"2025-06 Eurostat une_rt_m BE SA total 15-74","value":6.5}],"drivers":["Recent Belgian unemployment has been flat around 6.4-6.5 percent","Euro area unemployment was low and stable at 6.2 percent in May 2026","Belgian regional labor-market slack makes a sharp fall less likely than persistence","One-month first-print volatility is usually one or two tenths, not a large regime move"],"sourceContext":["https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/une_rt_m?geo=BE&sex=T&age=Y15-74&s_adj=SA&unit=PC_ACT&sinceTimePeriod=2025-01","https://ec.europa.eu/eurostat/web/main/news/release-calendar"],"runAt":"2026-07-10T04:44:12Z","reasoning":[{"kind":"heading","text":"Belgium July 2026 Eurostat unemployment first print"},{"kind":"text","text":"Framing and exact resolver: this targets Eurostat table une_rt_m, Belgium geo=BE, seasonally adjusted s_adj=SA, total sex=T, age Y15-74, unit PC_ACT, July 2026 first print. The value resolves from the Eurostat data page, not from FRED, news, or a later revised vintage."},{"kind":"tool","tool":"official.lookup","call":"Checked Eurostat release calendar for the monthly unemployment euro-indicator publication covering July 2026.","result":"Eurostat release calendar lists the July 2026 unemployment release on 2026-09-01 at 11:00, within the ledger window 2026-08-26 to 2026-09-03."},{"kind":"tool","tool":"official.lookup","call":"Queried Eurostat une_rt_m for BE, sex=T, age=Y15-74, s_adj=SA, unit=PC_ACT, recent monthly observations.","result":"Fetched recent Belgium values: 2026-03 = 6.5, 2026-04 = 6.5, 2026-05 = 6.5 percent; 2025-12 = 6.4 percent."},{"kind":"tool","tool":"official.lookup","call":"Pulled the recent official-source reference class from Eurostat une_rt_m for the same variant and country over 2025-06 through 2026-05.","result":"Fetched 12-month same-variant Belgium sequence used for volatility: 2025-06 6.5, 2025-07 6.5, 2025-08 6.4, 2025-09 6.4, 2025-10 6.4, 2025-11 6.4, 2025-12 6.4, 2026-01 6.4, 2026-02 6.5, 2026-03 6.5, 2026-04 6.5, 2026-05 6.5."},{"kind":"tool","tool":"official.lookup","call":"Checked Eurostat euro-indicator labor-market context for the euro area around the latest available month.","result":"Eurostat euro-area unemployment was 6.2 percent in 2026-05 after 6.2 percent in 2026-04, with unemployed persons down by about 55,000 from April to May."},{"kind":"text","text":"Base rate/reference class: for a monthly level series that is rounded to one decimal and has held at 6.4-6.5 percent, the base rate is persistence of the latest official same-variant value. The reference class is recent month-to-month movements in Belgium une_rt_m SA total 15-74, not annual or unadjusted labor-force statistics."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest official 2026-05 value of 6.5 from the same Eurostat une_rt_m variant. Historical sample = same-variant monthly values from 2025-06 to 2026-05. Adjustment components: level 0.0 because latest is already at the local plateau; momentum 0.0 because 2026-03, 2026-04, and 2026-05 were all 6.5; one-off +0.0 because no official Belgian shock in the source record; policy-mechanism +0.0 because unemployment insurance/activation changes do not imply a clear July first-print break. Successive-change dispersion gives sigma = 0.14 percentage points; 1.28*sigma = 0.18, rounded to a practical one-decimal first-print half-width of 0.2. Final implied bounds: 6.5 - 0.2 = 6.3 and 6.5 + 0.2 = 6.7."},{"kind":"text","text":"Counter-considerations: upside risk is a deterioration in Belgian hiring or a July sample rotation that pushes the first print to 6.8 or above; downside risk is a stronger summer labor-market improvement that pulls unemployment to 6.2 or below; either would land outside the interval. Inside the interval, 6.4, 6.5, or 6.6 are all plausible first prints given recent rounding and flatness."},{"kind":"forecast","point":6.5,"ciLow":6.3,"ciHigh":6.7}]}

# Reviewer critique
{"summary":"Draft is broadly publishable on resolver, prior, and target logic, but it needs fixes for a likely country-field mismatch and an unsupported interval-volatility calculation.","requiredFixes":[{"rubricItem":"coherence","severity":"blocking","summary":"The JSON field \"country\":\"EA\" conflicts with the Belgium target and title/question.","actionRequested":"Change the country/geography field to the repository's Belgium value, likely \"BE\" or \"Belgium\", while keeping the same catalog slug and target."},{"rubricItem":"interval","severity":"warning","summary":"The stated sigma = 0.14 is not clearly supported by the listed 2025-06 to 2026-05 monthly sequence, whose rounded month-to-month changes appear much smaller.","actionRequested":"Recompute the interval dispersion from the stated historical sample or explicitly label the 0.2 half-width as a judgmental/rounding first-print uncertainty allowance rather than a direct realized-volatility result."}],"optionalSuggestions":["State explicitly that the forecast is two months ahead from the latest May 2026 observation to July 2026, since June is not yet used.","If the schema expects ISO-like country codes, prefer a canonical country value and avoid euro-area shorthand in Belgium-specific records."]}

Emit the final JSON object only.
