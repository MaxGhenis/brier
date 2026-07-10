# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.cpi.annual_rate
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ons-cpi-annual-rate-june-2026"
- targetUnit: "percent"
- dataPointId: "ons.cpi.annual_rate.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/may2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-21", "start": "2026-07-13"}, "field": "official_release:ons:cpi:2026-05:cpi_annual_rate", "releasePolicy": "first_print", "sourceSeriesId": "ons.cpi.annual_rate", "sourceUrl": "https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/may2026", "table": "Consumer price inflation, UK: May 2026", "transform": {"factor": 1, "operation": "identity"}}

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
{"slug":"ons-cpi-annual-rate-june-2026","country":"UK","type":"data","title":"UK CPI Annual Rate, June 2026","question":"Office for National Statistics CPI annual rate 00: all items 2015=100, UK, June 2026, first print, not seasonally adjusted, rounded to one decimal percent.","unit":"percent","pointEstimate":2.8,"ciLow":2.4,"ciHigh":3.1,"confidence":0.8,"resolutionDate":"2026-07-22","resolutionSource":"Office for National Statistics Consumer price inflation, UK: June 2026 / CPI annual rate 00: all items 2015=100 time series D7G7","resolutionSourceUrl":"https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7g7/mm23","resolutionRule":"Resolve to the first ONS-published value for CPI ANNUAL RATE 00: ALL ITEMS 2015=100, series D7G7, for 2026 JUN, in percent and rounded to one decimal place. Use the first official print in the June 2026 consumer price inflation release or the same-day D7G7 time-series update; ignore later revisions or corrections unless ONS replaces the first print before the release is made public.","dataPointId":"ons.cpi.annual_rate.june_2026.first_print","historicalContext":[{"label":"2026 MAY CPI annual rate D7G7","value":2.8},{"label":"2026 APR CPI annual rate D7G7","value":2.8},{"label":"2026 MAR CPI annual rate D7G7","value":3.3},{"label":"2025 JUN CPI annual rate D7G7","value":3.6},{"label":"2026 MAY CPI index D7BT","value":142.4},{"label":"2025 JUN CPI index D7BT","value":138.9}],"drivers":["May 2026 CPI annual rate was 2.8 percent, unchanged from April","June 2025 base month had a 0.3 percent monthly CPI increase","Recent core CPI was 2.6 percent while services CPI rose to 3.7 percent in May","Food inflation slowed and goods inflation eased in May","Transport and motor fuels were the main upward pressure in May"],"sourceContext":["https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7g7/mm23","https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/may2026","https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7oe/mm23","https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23"],"runAt":"2026-07-10T03:54:19Z","reasoning":[{"kind":"heading","text":"Forecast UK CPI Annual Rate For June 2026"},{"kind":"text","text":"Exact resolver: ONS CPI annual rate 00: all items 2015=100, series D7G7, UK, 2026 JUN, first print, percent, one decimal. The ledger hint points to the May 2026 bulletin and field 2026-05, which is a discrepancy for a June 2026 target; I keep the same slug and dataPointId but use the D7G7 series page as the stable exact-series resolver and the June 2026 first print when released."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS D7G7 CPI annual rate time-series page and latest release metadata.","result":"Fetched D7G7 values: 2026 MAY 2.8, 2026 APR 2.8, 2026 MAR 3.3, 2026 FEB 3.0, 2026 JAN 3.0, 2025 JUN 3.6; release date 17 June 2026 and next release 22 July 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Consumer price inflation, UK: May 2026 bulletin for first-print context, component drivers, and next-release announcement.","result":"Fetched May bulletin figures: CPI 12-month rate 2.8% in May 2026, unchanged from April; CPI monthly rate 0.2% in May 2026, same as May 2025; core CPI 2.6%, CPI goods 2.0%, CPI services 3.7%; next release 22 July 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS D7OE CPI monthly-rate time series for month-on-month base-rate evidence.","result":"Fetched D7OE monthly rates: 2025 JUN 0.3, 2025 JUL 0.1, 2025 AUG 0.3, 2025 SEP 0.0, 2025 OCT 0.4, 2025 NOV -0.2, 2025 DEC 0.4, 2026 JAN -0.5, 2026 FEB 0.4, 2026 MAR 0.7, 2026 APR 0.7, 2026 MAY 0.2."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS D7BT CPI all-items index page to translate a plausible June monthly change into the annual-rate target.","result":"Fetched D7BT index levels: 2025 JUN 138.9, 2026 MAY 142.4, 2026 APR 142.1, 2026 MAR 141.0, 2025 MAY 138.4."},{"kind":"text","text":"Base rate / reference class: for this one-month-ahead annual-rate forecast, the outside-view prior is near persistence in D7G7 because recent annual rates were 3.0, 3.0, 3.3, 2.8, 2.8 from January through May 2026 and the annual rate only changes when the new monthly CPI move differs from the same month a year earlier. The June 2025 base monthly rate was 0.3%, so a June 2026 monthly move around 0.2% to 0.3% implies an annual rate around 2.7% to 2.8% before rounding."},{"kind":"math","text":"Prior/update/interval: persistence prior from the D7G7 recent-history/reference-class sample starts at May 2026 = 2.8. Index arithmetic with D7BT gives 142.4*(1+0.002)=142.6848, and (142.6848/138.9 - 1)*100 = 2.7248, which rounds to 2.7; using a 0.3% monthly move gives about 2.8. Adjustment components: +0.05 pp from transport/fuel pressure and services stickiness, -0.05 pp from food/goods easing, net near 2.75 and first-print rounded point 2.8. For interval sizing, use successive D7G7 monthly changes from 2025 JUN to 2026 MAY: +0.2, 0.0, 0.0, -0.2, -0.4, +0.2, -0.4, 0.0, +0.3, -0.5, 0.0; sigma = 0.27 percentage points, so 1.28*sigma = 0.35 pp. Around a 2.75 center this gives about 2.40 to 3.10, reported as 2.4 to 3.1."},{"kind":"text","text":"Counter-considerations: upside risk is a larger June fuel, airfare, or services move after May transport inflation of 6.8% and services CPI of 3.7%, which would land above the interval if the monthly all-items increase materially exceeded about 0.6%. Downside risk is renewed goods and food disinflation plus lower fuel prices, which would land below the interval if June all-items CPI was flat or negative while the 2025 base month was +0.3%."},{"kind":"forecast","point":2.8,"ciLow":2.4,"ciHigh":3.1}]}

# Reviewer critique
{
  "summary": "Draft is mostly publishable, but its resolver metadata conflicts with the canonical ledger contract and needs explicit alignment or documented exception handling.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "Draft changes the canonical resolutionSourceUrl from the ledger May 2026 bulletin URL to the D7G7 time-series URL and resolves via the June 2026 release, while the ledger binding still names May 2026 and field 2026-05.",
      "actionRequested": "Keep the JSON target fields tied to the ledger contract, or explicitly flag this as a concrete ledger error in the reasoning while preserving the target slug/dataPointId and making the intended June 2026 first-print resolver unambiguous."
    }
  ],
  "optionalSuggestions": [
    "Add one sentence saying the resolutionDate of 2026-07-22 comes from the ONS next-release notice, since the ledger expectedReleaseWindow appears inconsistent.",
    "The prior/update/interval step is strong; consider naming the volatility sample as monthly D7G7 annual-rate changes through May 2026 to make the interval provenance easier to audit.",
    "Tail scenarios are concrete and target-specific; no change needed there."
  ]
}

Emit the final JSON object only.
