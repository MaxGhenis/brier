# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.retail_sales.volume_mom
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ons-retail-sales-volume-mom-june-2026"
- targetUnit: "percent_growth"
- dataPointId: "ons.retail_sales.volume_mom.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-23", "start": "2026-07-15"}, "field": "official_release:ons:retail_sales:2026-05:volume_mom", "releasePolicy": "first_print", "sourceSeriesId": "ons.retail_sales.volume_mom", "sourceUrl": "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026", "table": "Retail sales, Great Britain: May 2026", "transform": {"factor": 1, "operation": "identity"}}

# Source hints
- Use ONS time-series pages, ONS API, and ONS release calendar.
- UK CPI/CPIH prints to one decimal; labour-market rates print to one decimal.
- Resolution source should be the relevant ONS release or time-series page.

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
{"slug":"ons-retail-sales-volume-mom-june-2026","country":"UK","type":"data","title":"UK Retail Sales Volume MoM, Jun 2026","question":"What will the Office for National Statistics report as the first-print month-on-month percentage change in seasonally adjusted retail sales volumes, Great Britain, for June 2026?","unit":"percent_growth","pointEstimate":0.1,"ciLow":-1.4,"ciHigh":1.6,"confidence":0.8,"resolutionDate":"2026-07-24","resolutionSource":"Office for National Statistics Retail sales, Great Britain statistical bulletin","resolutionSourceUrl":"https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026","resolutionRule":"Resolve to the first ONS print of the seasonally adjusted all-retailing retail sales volume month-on-month percentage change for June 2026, in percentage points, as published in the Retail sales, Great Britain bulletin or Retail Sales Index dataset on 2026-07-24. Use the initial published value only; ignore later revisions. The ledger URL currently points to the May 2026 bulletin even though the period is June 2026; keep the target tied to dataPointId ons.retail_sales.volume_mom.june_2026.first_print and resolve against the June first-print value when released.","dataPointId":"ons.retail_sales.volume_mom.june_2026.first_print","historicalContext":[{"label":"2026-05 first-estimate/revised current bulletin","value":1.2},{"label":"2026-04 revised in May bulletin","value":-1.0},{"label":"2026-03 revised in May bulletin","value":0.7}],"drivers":["May weather-and-promotion boost creates payback risk","June heat can support seasonal goods and non-store demand","Recent monthly retail-volume growth is volatile around a modest positive base rate","Use seasonally adjusted all-retailing volume variant only"],"sourceContext":["https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/may2026","https://www.ons.gov.uk/businessindustryandtrade/retailindustry/datasets/retailsalesindexreferencetables","https://www.ons.gov.uk/releasecalendar"],"runAt":"2026-07-10T04:01:56Z","reasoning":[{"kind":"heading","text":"ONS retail sales volume MoM, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the ONS Retail Sales Index all-retailing quantity bought, seasonally adjusted, month-on-month volume percentage change for Great Britain. The canonical ledger target is June 2026 first print, but the supplied resolutionSourceUrl and sourceBinding field point to the May 2026 bulletin and 2026-05; that appears to be a ledger discrepancy, so I keep the same slug, dataPointId, and resolver substance while noting that the June first-print value is the target."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Retail sales, Great Britain: May 2026 bulletin for latest same-variant monthly volume movements and next-release notice.","result":"Fetched numbers: release date 19 June 2026; next release 24 July 2026; May 2026 retail sales volumes +1.2% month on month; April 2026 -1.0% month on month; March 2026 +0.7% month on month; three months to May 2026 +0.4%; year to May 2026 +3.2%."},{"kind":"tool","tool":"official.lookup","call":"Checked the ONS Retail Sales Index dataset page linked from the bulletin for dataset identity and release timing.","result":"Fetched numbers: dataset release date 19 June 2026; next release 24 July 2026; dataset covers retail sales in value and volume terms, seasonally and non-seasonally adjusted."},{"kind":"tool","tool":"official.lookup","call":"Checked ONS release-calendar surface and bulletin announcement schedule for the resolution date rather than inferring from cadence.","result":"Fetched numbers: ONS release-calendar page showed 338 upcoming releases and recent entries at 9:30am; the ONS retail-sales bulletin specifically states next release 24 July 2026, which I use as the verified resolutionDate."},{"kind":"tool","tool":"official.lookup","call":"Read ONS same-release quality and component notes for May 2026 to condition the June forecast.","result":"Fetched numbers: May 2026 Retail Sales Index survey response rate was 57.0%; returned-form response was 3.9 percentage points below the past-12-month average; turnover coverage was 85.0%; non-store retailers rose 6.1% month on month; online spending values rose 3.3% month on month; online share rose from 28.1% in April to 28.8% in May."},{"kind":"text","text":"Base rate/reference class: for this change/flow series, the latest same-variant ONS monthly values are +0.7, -1.0, and +1.2, averaging +0.3%. That outside-view base rate is mildly positive but dominated by noise and one-off weather/promotional effects."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior is the recent ONS same-variant monthly sample for all-retailing seasonally adjusted volume growth, values [0.7, -1.0, 1.2], mean = 0.3. Adjustment components: -0.3 percentage point payback after May's hot-weather and promotion-led +1.2; +0.1 percentage point from continued summer/heat-sensitive demand and event-related discretionary spending; 0.0 percentage point from quality/timing because the first print should still capture the standard monthly survey. Final point = 0.3 - 0.3 + 0.1 = 0.1. Interval method: because this is a change series, compute dispersion from the fetched values themselves; sample sigma = 1.15, so 80% half-width is roughly 1.28*sigma = 1.47, rounded to 1.5. Interval = 0.1 +/- 1.5 = [-1.4, 1.6]."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: the recent level is not recessionary, with May up 3.2% on a year earlier, but month-to-month momentum alternates sharply. The key one-off is possible reversal of May's promotion and hot-weather boost, partly offset by June heat and summer goods. I do not see a direct policy mechanism large enough to move June retail volumes by more than normal monthly volatility."},{"kind":"text","text":"Counter-considerations: upside risk is another heat-driven or event-driven surge in non-store, department, clothing, outdoor, and electronics spending, which would land above the interval if broad store categories repeat May-scale gains. Downside risk is payback from May pull-forward, household caution, or disrupted shopping patterns, which would land below the interval if food and non-food both fall sharply. Outside the interval would require a monthly move below -1.4% or above +1.6%, larger than the fitted recent 80% band."},{"kind":"forecast","point":0.1,"ciLow":-1.4,"ciHigh":1.6}]}

# Reviewer critique
{"summary":"Draft is mostly publishable, but the prior and interval rely on an unusually thin three-month sample that should be strengthened or explicitly justified.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is based on sample volatility from only three monthly observations, which is too thin to establish realized volatility for a noisy MoM retail series.","actionRequested":"Use a longer same-variant historical sample for realized MoM volatility, or explicitly state that the three-point sigma is a fallback and justify why a wider/narrower interval remains appropriate."},{"rubricItem":"base_rate","severity":"warning","summary":"The base-rate prior is stated, but it is effectively a three-month recent average rather than a broader reference-class base rate.","actionRequested":"Add a compact longer-history or multi-year same-series base rate, or explicitly explain why the recent three-month persistence prior is preferred over a longer base-rate prior."}],"optionalSuggestions":["In the resolver language, keep the ledger May-2026 URL discrepancy note but make the first-print June 2026 target sentence the dominant resolver statement.","Clarify that the -0.3pp payback adjustment is judgmental rather than estimated from historical post-surge reversals."]}

Emit the final JSON object only.
