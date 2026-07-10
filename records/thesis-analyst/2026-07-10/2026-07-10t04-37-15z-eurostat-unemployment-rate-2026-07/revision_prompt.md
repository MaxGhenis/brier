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
- targetUnit: "percent"
- dataPointId: "eurostat.unemployment_rate.euro_area.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["ec.europa.eu"], "expectedReleaseWindow": {"end": "2026-09-03", "start": "2026-08-26"}, "field": "eurostat.unemployment_rate", "releasePolicy": "first_print", "sourceSeriesId": "eurostat.unemployment_rate", "sourceUrl": "https://ec.europa.eu/eurostat/news/euro-indicators", "table": "Eurostat monthly unemployment euro-indicators release / une_rt_m data page", "transform": {"factor": 1.0, "operation": "multiply"}}

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
{"slug":"euro-area-unemployment-rate-july-2026","country":"EA","type":"data","title":"Euro Area Unemployment Rate, July 2026","question":"Eurostat une_rt_m euro area seasonally adjusted total unemployment rate, age 15-74, July 2026 first print","unit":"percent","pointEstimate":6.2,"ciLow":6.1,"ciHigh":6.3,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"Eurostat euro-indicators unemployment release and une_rt_m data table","resolutionSourceUrl":"https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","resolutionRule":"Resolve to the first Eurostat-published July 2026 euro area seasonally adjusted unemployment rate in dataset une_rt_m for geo=Euro area, sex=total, age=15-74, unit=percent of labour force. Use the one-decimal first print in the Eurostat euro-indicators unemployment release or data page; ignore later revisions.","dataPointId":"eurostat.unemployment_rate.euro_area.july_2026.first_print","historicalContext":[{"label":"May 2026 latest euro area SA unemployment rate","value":6.2},{"label":"Apr 2026 euro area SA unemployment rate","value":6.2},{"label":"Mar 2026 euro area SA unemployment rate","value":6.3},{"label":"Feb 2026 euro area SA unemployment rate","value":6.4},{"label":"May 2025 euro area SA unemployment rate","value":6.3}],"drivers":["Latest euro area unemployment rate stable at 6.2%","Euro area unemployed count fell by 55 thousand in May","Large members mixed: Germany and Spain stable, Italy and Greece lower, France higher","Retail and services indicators show mild demand support","Labour-cost growth still positive but not an immediate layoff signal"],"sourceContext":["https://ec.europa.eu/eurostat/news/euro-indicators/release-calendar","https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/3-02072026-ap","https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/4-06072026-bp","https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/2-01072026-ap","https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/3-16062026-bp"],"runAt":"2026-07-10T04:37:24Z","reasoning":[{"kind":"heading","text":"Euro area unemployment rate July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the Eurostat une_rt_m euro area seasonally adjusted total unemployment rate for persons aged 15-74, in percent of the labour force, first print for July 2026. The variant is SA total unemployment, not NSA, youth-only, member-state, or revised-vintage data. Resolution uses the first Eurostat euro-indicators unemployment release/data-table value, rounded to one decimal."},{"kind":"tool","tool":"official.lookup","call":"Checked Eurostat euro-indicators release calendar and latest unemployment release scheduling context.","result":"The Eurostat Euro indicators calendar page lists Unemployment as a scheduled indicator and uses Europe/Luxembourg CET/CEST. The latest unemployment release was published 2 July 2026 for May 2026 and states the next unemployment release is 30 July 2026; applying the official July-target calendar entry within the ledger release window gives the July 2026 first-print resolution date 2026-09-01."},{"kind":"tool","tool":"official.lookup","call":"Fetched latest Eurostat unemployment release for euro area totals.","result":"Eurostat reported May 2026 euro area seasonally adjusted unemployment at 6.2%, stable vs April 2026 at 6.2%, down from May 2025 at 6.3%; February 2026 was 6.4% and March 2026 was 6.3%. Euro area unemployed persons were 10.986 million in May 2026, down 55 thousand from April and down 158 thousand from May 2025."},{"kind":"tool","tool":"official.lookup","call":"Fetched large-member unemployment readings from the same Eurostat release table.","result":"May 2026 rates in the Eurostat table: Germany 3.8%, Spain 10.3%, France 8.2%, Italy 5.0%, Greece 8.1%; April 2026 rates were Germany 3.8%, Spain 10.3%, France 8.2%, Italy 5.1%, Greece 9.1%."},{"kind":"tool","tool":"official.lookup","call":"Fetched current Eurostat macro/labour-market context from official euro-indicators pages.","result":"Eurostat reported May 2026 euro area retail trade volume +0.2% m/m after -0.3% in April, June 2026 flash HICP inflation 2.8% after 3.2% in May, services inflation 3.2% after 3.5%, and Q1 2026 euro area hourly labour costs +3.2% y/y with wages and salaries +3.4%."},{"kind":"text","text":"Reference class and base rate: the immediate reference class is recent monthly first-print euro area SA unemployment rates. The base rate is persistence around the latest 6.2%, because the last three monthly readings moved only from 6.4 to 6.3 to 6.2 to 6.2 and unemployment rates usually change in 0.0-0.1 percentage-point increments month to month."},{"kind":"math","text":"Prior/update/interval: persistence prior = 6.2 from the latest official May print; historical sample = successive monthly changes from Feb-May 2026 values 6.4, 6.3, 6.2, 6.2, giving changes -0.1, -0.1, 0.0 and sigma = 0.06 percentage points per month. Adjustment components: level 0.00, momentum -0.03 from falling unemployed count and Italy/Greece declines, demand +0.01 from retail/services resilience, labour-cost/policy-mechanism +0.02 because wage costs remain positive but not recessionary, net 0.00 after rounding. For the two-month-ahead July first print, half-width = 1.28*sqrt(2)*0.06 = 0.11 percentage points; rounded to the one-decimal release grid gives an 80% interval of 6.1 to 6.3 around a 6.2 point."},{"kind":"text","text":"Counter-considerations: upside risk is a summer weakening in France or Spain, or delayed pass-through from high energy and labour costs, which would land above the interval at 6.4% or higher. Downside risk is continued sharp declines in Italy/Greece plus stable Germany and Spain, which would land below the interval at 6.0% or lower. Outside the interval would require two consecutive monthly moves of roughly the same sign rather than the recent near-flat pattern."},{"kind":"forecast","point":6.2,"ciLow":6.1,"ciHigh":6.3}]}

# Reviewer critique
{"summary":"Draft is publishable after tightening the prior/model and interval support; no blocking leakage, unit, resolver, or coherence issue found.","requiredFixes":[{"rubricItem":"base_rate","severity":"warning","summary":"The persistence/base-rate prior is stated after several evidence and macro update paragraphs, so the reasoning does not cleanly put the prior before inside-view updates.","actionRequested":"Move or restate the base-rate prior near the start, before current drivers, with May 2026 6.2% as the explicit anchor."},{"rubricItem":"model_prior","severity":"warning","summary":"The draft uses a persistence/random-walk logic but does not explicitly label it as the time-series/model prior or state why a richer model is not used.","actionRequested":"Add one sentence naming the model prior, e.g. one-decimal random-walk persistence with no drift, and note that richer modeling is ruled out because only short-horizon official monthly prints are being forecast."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is based on only three monthly changes from Feb-May 2026, which is a thin realized-volatility sample for interval calibration.","actionRequested":"Either use a longer recent monthly sample from une_rt_m, or explicitly state that the short sample is a near-term calibration and add judgmental uncertainty to cover sampling error."}],"optionalSuggestions":["Keep the exact 2026-09-01 resolution date tied to the Eurostat calendar entry if available in the saved trace.","Consider making resolutionSourceUrl the euro-indicators release/calendar page while keeping the data browser as supporting source context.","The upside and downside tails are concrete and do not need major revision."]}

Emit the final JSON object only.
