# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: eurostat.unemployment_rate
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "euro-area-unemployment-rate-july-2026"
- country: "EA"
- targetUnit: "percent"
- dataPointId: "eurostat.unemployment_rate.euro_area.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["ec.europa.eu"], "expectedReleaseWindow": {"end": "2026-09-03", "start": "2026-08-26"}, "field": "eurostat.unemployment_rate", "releasePolicy": "first_print", "sourceSeriesId": "eurostat.unemployment_rate", "sourceUrl": "https://ec.europa.eu/eurostat/news/euro-indicators", "table": "Eurostat monthly unemployment euro-indicators release / une_rt_m data page", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-0fbb8f5d88f4627312ef5d9d5e31cffc94afec5f3b75f5c117adba8543bb2d08.json"
- targetContentHash: "0fbb8f5d88f4627312ef5d9d5e31cffc94afec5f3b75f5c117adba8543bb2d08"
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
{"slug":"euro-area-unemployment-rate-july-2026","country":"EA","type":"data","title":"Euro area unemployment rate, July 2026","question":"Eurostat une_rt_m euro area unemployment rate, July 2026, seasonally adjusted total age 15-74, first print","unit":"percent","pointEstimate":6.2,"ciLow":6,"ciHigh":6.4,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"Eurostat monthly unemployment euro-indicators release / une_rt_m data page","resolutionSourceUrl":"https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","resolutionRule":"Resolve to Eurostat's first published July 2026 euro area seasonally adjusted unemployment rate in table une_rt_m / the monthly unemployment euro-indicators release, for total sex and age 15-74, reported in percent to one decimal. Use the first print only and ignore later revisions.","dataPointId":"eurostat.unemployment_rate.euro_area.july_2026.first_print","historicalContext":[{"label":"May 2026 latest","value":6.2},{"label":"Apr 2026","value":6.2},{"label":"Mar 2026","value":6.3},{"label":"Feb 2026","value":6.4},{"label":"May 2025","value":6.3}],"drivers":["latest first-print anchor at 6.2 percent","Feb-May 2026 drift down from 6.4 to 6.2","May unemployment count fell by 55 thousand in the euro area","same variant throughout: euro area seasonally adjusted total age 15-74 rate","two unpublished monthly steps remain before the July target"],"sourceContext":["https://ec.europa.eu/eurostat/news/euro-indicators/release-calendar","https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/3-02072026-ap","https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en"],"runAt":"2026-07-10T05:29:16Z","reasoning":[{"kind":"heading","text":"Euro area unemployment rate, July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this forecast targets Eurostat table une_rt_m, euro area unemployment rate, seasonally adjusted, total sex, age 15-74, percent, for July 2026. The resolution is the first official print, not a revised vintage."},{"kind":"tool","tool":"official.lookup","call":"Eurostat euro-indicators release calendar and latest unemployment release schedule lookup","result":"Eurostat's release calendar page lists Unemployment and uses Europe/Luxembourg time; the May 2026 unemployment release is dated 2 July 2026, gives a latest euro area rate of 6.2%, and states the next unemployment release is 30 July 2026. The registered July 2026 target resolves on the subsequent unemployment calendar slot, 2026-09-01."},{"kind":"tool","tool":"official.lookup","call":"Eurostat May 2026 euro area unemployment release overview","result":"Fetched latest same-series official values: May 2026 euro area seasonally adjusted unemployment rate 6.2%, April 2026 6.2%, May 2025 6.3%, EU May 2026 5.9%, and euro area unemployed persons 10.986 million."},{"kind":"tool","tool":"official.lookup","call":"Eurostat May 2026 release table for seasonally adjusted unemployment totals","result":"Fetched table history for the euro area rate: May 2025 6.3%, February 2026 6.4%, March 2026 6.3%, April 2026 6.2%, May 2026 6.2%; euro area unemployment counts were 11.144 million, 11.223 million, 11.136 million, 11.041 million, and 10.986 million for those same columns."},{"kind":"text","text":"Base rate / reference class: for this low-volatility monthly rate series, the outside-view prior is persistence at the latest official one-decimal print. The recent reference class is the same Eurostat euro area SA total age 15-74 rate, where the last five displayed values were tightly clustered between 6.2 and 6.4 percent."},{"kind":"text","text":"Level, momentum, and mechanism: the level is historically low at 6.2%; momentum from February to May is mildly downward, but the last month is flat at 6.2. The May count decline of 55 thousand supports no near-term jump, while two months of macro noise before the July reference month argues against narrowing the interval too much."},{"kind":"math","text":"Prior/update/interval: persistence prior 6.2 from May 2026; historical sample May 2025, Feb-May 2026 values 6.3, 6.4, 6.3, 6.2, 6.2; adjustment components are 0.0 for latest flat momentum, -0.05 for Feb-May downtrend, and +0.05 for two-step mean reversion/rounding risk, leaving point 6.2. Successive changes are +0.1, -0.1, -0.1, 0.0; one-month sample sigma is about 0.10. Because July is two unreleased monthly steps after May, forecast sigma = 0.10*sqrt(2) = 0.14, so the 80% half-width is roughly 1.28*sigma = 1.28*0.14 = 0.18, rounded to a one-decimal compatible 0.2; final implied bounds are 6.0 to 6.4."},{"kind":"text","text":"Counter-considerations: upside risk is a sharper employment deterioration in June-July that would lift the rounded first print to 6.5 or above, outside the interval. Downside risk is continued labor-market tightening and falling unemployment counts that would land below the interval at 5.9 or less."},{"kind":"forecast","point":6.2,"ciLow":6,"ciHigh":6.4}]}

# Reviewer critique
{"summary":"Draft is publishable after tightening the interval support: resolver, first-print rule, unit, point, and JSON fields are coherent, but the volatility calculation overstates the historical grounding because it uses a sparse non-contiguous sample as one-month changes.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The interval is presented as realized-volatility based, but the sample mixes May 2025 with Feb-May 2026 and calls the resulting differences one-month changes.","actionRequested":"Either recompute the interval from a contiguous monthly history for the same Eurostat series or reframe the 0.2 half-width as an explicit judgmental uncertainty allowance, naming the limited sample caveat."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact prior/update/interval step names the components, but the historical sample and interval method are internally imprecise because the first difference is not a one-month change.","actionRequested":"Revise that sentence so the historical sample, monthly-change calculation, sigma estimate, and implied 6.0-6.4 bounds are consistent."}],"optionalSuggestions":["Consider making the resolver URL match the ledger source emphasis by mentioning both the Eurostat euro-indicators release and une_rt_m data page.","Tail scenarios are adequate, but could be stronger if they name the required rounded first-print outcomes: 6.5+ upside and 5.9 or lower downside."]}

Emit the final JSON object only.
