# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: abs.cpi.all_groups.yoy
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "australia-cpi-annual-rate-july-2026"
- targetUnit: "percent"
- dataPointId: "abs.cpi.all_groups.yoy.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-09-02", "start": "2026-08-25"}, "field": "abs.cpi.all_groups.yoy", "releasePolicy": "first_print", "sourceSeriesId": "abs.cpi.all_groups.yoy", "sourceUrl": "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/june-2026", "table": "Australian Bureau of Statistics Consumer Price Index, Australia, June 2026 release", "transform": {"factor": 1.0, "operation": "multiply"}}

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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI Annual Rate, July 2026","question":"Australian Bureau of Statistics Consumer Price Index, Australia: All groups CPI, weighted average of eight capital cities, original annual change for July 2026, first print","unit":"percent","pointEstimate":3.8,"ciLow":3.1,"ciHigh":4.5,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Consumer Price Index, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/july-2026","resolutionRule":"Resolve to the first ABS-published All groups CPI, weighted average of eight capital cities, original annual change for July 2026, printed to one decimal in Consumer Price Index, Australia. Use the first print only and do not revise for later ABS updates. The ledger sourceUrl names the June 2026 release, but the official ABS future-release list identifies the July 2026 CPI release on 26/08/2026, so this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"May 2026 All groups CPI annual change","value":4.0},{"label":"April 2026 All groups CPI annual change","value":4.2},{"label":"March 2026 All groups CPI annual change","value":4.6},{"label":"February 2026 All groups CPI annual change","value":3.7},{"label":"July 2025 All groups CPI annual change","value":3.0}],"drivers":["May 2026 headline CPI annual rate was 4.0 percent","Trimmed mean rose to 3.6 percent in May 2026","Housing annual inflation was 6.5 percent in May 2026","July 2025 monthly base was high at 1.3 percent","May 2026 monthly CPI fell 0.7 percent in original terms"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release","https://www.abs.gov.au/about/key-priorities/big-data-timely-insights-phase-2/complete-monthly-measure-cpi/release-schedule","https://www.abs.gov.au/about/key-priorities/big-data-timely-insights-phase-2/complete-monthly-measure-cpi"],"runAt":"2026-07-10T04:40:23Z","reasoning":[{"kind":"heading","text":"Australia July 2026 CPI annual inflation forecast"},{"kind":"text","text":"Framing and exact resolver: target is the ABS Consumer Price Index, Australia complete monthly CPI, All groups CPI, weighted average of eight capital cities, original annual change for July 2026, first print to one decimal. This is the complete Monthly CPI series that replaced the old Monthly CPI Indicator; anchors below use that same complete CPI variant."},{"kind":"tool","tool":"official.lookup","call":"Opened ABS Consumer Price Index, Australia latest release for May 2026.","result":"Fetched May 2026 release date 24/06/2026; All groups CPI annual change was 4.0 percent in May 2026, down from 4.2 percent in April 2026; monthly original CPI fell 0.7 percent in May and seasonally adjusted fell 0.1 percent."},{"kind":"tool","tool":"official.lookup","call":"Read ABS future-release list on the Consumer Price Index, Australia May 2026 page.","result":"Fetched future releases: June 2026 CPI release 29/07/2026, July 2026 CPI release 26/08/2026, and August 2026 CPI release 30/09/2026."},{"kind":"tool","tool":"official.lookup","call":"Read ABS All groups CPI monthly and annual movement table in the May 2026 release.","result":"Fetched complete CPI annual changes: Apr-25 2.4, May-25 2.1, Jun-25 1.9, Jul-25 3.0, Aug-25 3.2, Sep-25 3.6, Oct-25 3.8, Nov-25 3.4, Dec-25 3.8, Jan-26 3.8, Feb-26 3.7, Mar-26 4.6, Apr-26 4.2, May-26 4.0; fetched monthly original changes include Jun-25 0.1, Jul-25 1.3, Mar-26 1.1, Apr-26 0.4, May-26 -0.7."},{"kind":"tool","tool":"official.lookup","call":"Read ABS group and analytical-series table in the May 2026 CPI release.","result":"Fetched May 2026 annual components: Housing 6.5 percent, Food and non-alcoholic beverages 3.3 percent, Transport 3.3 percent, Trimmed mean 3.6 percent, Weighted median 3.6 percent, Electricity 21.1 percent, Automotive fuel 7.7 percent."},{"kind":"text","text":"Base rate/reference class: the reference class is post-transition complete monthly CPI annual prints from April 2025 through May 2026. The recent base rate is around 3.8 to 4.0 percent, with the last six annual prints at 3.8, 3.7, 4.6, 4.2, and 4.0 after December 2025 at 3.8."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: headline level is still near 4 percent; trimmed mean at 3.6 percent argues underlying inflation is sticky; May's -0.7 percent original monthly fall was a downside one-off mostly through volatile categories; July faces administered price and electricity-review seasonality, but July 2025 already had a large 1.3 percent monthly base that should restrain the year-over-year rate."},{"kind":"math","text":"Prior/update/interval: persistence prior is May 2026 All groups CPI annual inflation at 4.0 percent, using the Apr-25 to May-26 official complete monthly CPI annual-rate sample. Successive annual-rate changes are -0.3, -0.2, 1.1, 0.2, 0.4, 0.2, -0.4, 0.4, 0.0, -0.1, 0.9, -0.4, -0.2, so sigma = 0.48 percentage points. The unadjusted 80 percent half-width is about 1.28*sigma = 0.61 percentage points; I use a 0.7 point half-width because the target is two prints ahead and July energy-policy/base effects are unusually important. Point update is 4.0 minus 0.2 for the high Jul-25 base partly offset by sticky trimmed mean and housing pressure, giving 3.8 with 80 percent interval 3.1 to 4.5."},{"kind":"text","text":"Counter-considerations: upside risk is a large July electricity-price reset or fuel rebound that keeps the annual rate above 4.5 percent; downside risk is a soft June CPI plus another fuel or recreation decline that would land below the interval; outside the interval would likely require either a new administered-price shock above the interval or broad monthly deflation below the interval."},{"kind":"forecast","point":3.8,"ciLow":3.1,"ciHigh":4.5}]}

# Reviewer critique
{"summary":"Draft is publishable with minor review warnings; it ties the forecast to the correct dataPointId and first-print target while explicitly flagging the ledger/source-url discrepancy.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The JSON uses the July 2026 ABS release URL/source while the canonical ledger binding currently names the June 2026 release URL/table.","actionRequested":"Keep the forecast tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print, but make the ledger discrepancy explicit in a top-level source note or reasoning sentence so downstream review sees why the draft resolver differs from sourceBinding.sourceUrl."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is based on a short post-transition one-step annual-rate-change sample and only modestly widened for a two-release-ahead target.","actionRequested":"Add one sentence clarifying why 0.7 percentage points is sufficient for July 2026 despite the two-print horizon, or widen the interval if using two-step realized volatility."}],"optionalSuggestions":["State that the forecast does not use catalog point or interval as an input.","Make the tail scenarios numeric, e.g. specify monthly June/July paths that would push the annual rate below 3.1 or above 4.5."]}

Emit the final JSON object only.
