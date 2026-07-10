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
- country: "AU"
- targetUnit: "percent"
- dataPointId: "abs.cpi.all_groups.yoy.2026-07.first_print"
- resolutionDate: "2026-08-26"
- resolutionSource: "Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release"
- resolutionSourceUrl: "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026"
- resolutionRule: "Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger sourceBinding URL appears to point to the ABS Consumer Price Index, Australia, June 2026 page rather than the July 2026 Monthly CPI Indicator page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and documents that discrepancy rather than changing the target identity."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.abs.gov.au"], "expectedReleaseWindow": {"end": "2026-09-02", "start": "2026-08-25"}, "field": "abs.cpi.all_groups.yoy", "releasePolicy": "first_print", "sourceSeriesId": "abs.cpi.all_groups.yoy", "sourceUrl": "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/june-2026", "table": "Australian Bureau of Statistics Consumer Price Index, Australia, June 2026 release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-fc08c8b584fa0779c2421f4944d8c026e568b8990f2942968fad89cfb39c5530.json"
- targetContentHash: "fc08c8b584fa0779c2421f4944d8c026e568b8990f2942968fad89cfb39c5530"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"

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
- Size the 80% interval by reading it off your elicited threshold ladder, and SHOW the derivation in the 'Ladder:' math step: state the interpolated values literally as '10th percentile at X', 'median at Y', and '90th percentile at Z'. Ground the rung placement in the fetched reference-class history (state which fetched values anchored the rung span in the Prior/update/interval step). Never default to a round hedged band.
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

Emit the final JSON object only. (agent thesis.analyst v2.2.0, prompt 7ef119647b35, tools e15bf40583f8, promptMode ladder_v2)

# Threshold-ladder elicitation (promptMode ladder_v2)
This run elicits the distribution as binary exceedance questions BEFORE stating any point estimate, then derives the published numbers from the ladder.
- After research, choose 11-15 strictly increasing thresholds t in the target's print units spanning your genuine uncertainty: the first rung's cumulative probability must be <= 0.10 and the last >= 0.90.
- For each rung independently answer the binary question 'What is the probability the first print is <= t?', as if pricing a binary market. Probabilities must be non-decreasing across rungs and within [0.01, 0.99].
- Add one math reasoning step that begins 'Ladder:' and lists every rung literally as 'P(X <= t) = p' pairs, then states the interpolated '10th percentile at X', 'median at Y', and '90th percentile at Z' in the same step.
- Derive the published numbers FROM the ladder by linear interpolation between rungs: pointEstimate at cumulative 0.50, ciLow at 0.10, ciHigh at 0.90, each rounded to the print precision. The cell fields and the final forecast step must equal these derived values exactly.
- Keep every other requirement above (base rate, upside/downside/outside-the-interval risks, Prior/update/interval step).
- Add this top-level field to the cell JSON, with your actual rungs as two equal-length numeric arrays:
{
  "thresholdLadder": {
    "thresholds": [
      "strictly increasing numeric rungs"
    ],
    "cumulativeProbabilities": [
      "non-decreasing, within [0.01, 0.99]"
    ]
  }
}


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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia July 2026 all-groups CPI annual inflation","question":"Australian Bureau of Statistics complete monthly Consumer Price Index, Australia: All groups CPI annual movement for July 2026, original first print, percent.","unit":"percent","pointEstimate":3.8,"ciLow":3.5,"ciHigh":4.3,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"December 2025 All groups CPI annual movement","value":3.8},{"label":"January 2026 All groups CPI annual movement","value":3.8},{"label":"February 2026 All groups CPI annual movement","value":3.7},{"label":"March 2026 All groups CPI annual movement","value":4.6},{"label":"April 2026 All groups CPI annual movement","value":4.2},{"label":"May 2026 All groups CPI annual movement","value":4.0}],"drivers":["May headline disinflation from 4.2% to 4.0%","Housing annual inflation remained elevated at 6.5% in May","Volatile transport and clothing monthly movements can move the annual print","Underlying trimmed-mean inflation was 3.6% in May"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia","https://www.abs.gov.au/release-calendar/future-releases/202607/rcc_economy"],"runAt":"2026-07-10T00:00:00Z","thresholdLadder":{"thresholds":[3.2,3.3,3.4,3.6,3.7,3.8,3.9,4.0,4.1,4.2,4.3,4.4,4.6],"cumulativeProbabilities":[0.01,0.03,0.08,0.16,0.29,0.46,0.59,0.7,0.79,0.86,0.93,0.97,0.99]},"reasoning":[{"kind":"heading","text":"Australia July 2026 all-groups CPI annual inflation"},{"kind":"text","text":"Target framing: forecast the ABS All groups CPI annual movement for July 2026 in original terms, rounded to one decimal and resolved on the first print. The registered resolver names the ceased Monthly Consumer Price Index Indicator and its sourceBinding points to the June 2026 CPI page; the active ABS production is Consumer Price Index, Australia. I retain the supplied dataPointId, date, and first-print policy rather than changing target identity."},{"kind":"tool","tool":"official.lookup","call":"Fetched the ABS Consumer Price Index, Australia May 2026 release table for the same All groups CPI annual-movement variant.","result":"ABS reported All groups CPI annual movement of 3.8% in Dec-25, 3.8% in Jan-26, 3.7% in Feb-26, 4.6% in Mar-26, 4.2% in Apr-26, and 4.0% in May-26."},{"kind":"tool","tool":"official.lookup","call":"Fetched the May 2026 ABS CPI release overview and analytical-series table.","result":"ABS reported May All groups CPI annual movement at 4.0%, down from 4.2% in April; May trimmed mean was 3.6% after 3.4% in April, while Housing annual movement was 6.5%."},{"kind":"tool","tool":"official.lookup","call":"Fetched the ABS CPI publication future-release schedule to verify the target release date.","result":"ABS lists Consumer Price Index, Australia, July 2026 for 26/08/2026 at 11:30am AEST; adjacent listed dates are 29/07/2026 for June and 30/09/2026 for August."},{"kind":"text","text":"Reference class/base rate: the six fetched monthly annual prints span 3.7% to 4.6%, with a 4.0% latest print and a 3.9% simple average. All anchors are the same national All groups CPI annual-movement variant, not quarterly CPI or a smoothed series."},{"kind":"text","text":"Level and momentum point mildly lower after the 4.6% March spike eased to 4.2% and then 4.0%; persistent housing inflation and a 3.6% trimmed mean limit the expected decline. I therefore center July somewhat below May rather than extrapolating the March shock."},{"kind":"math","text":"Ladder: P(X <= 3.2) = 0.01; P(X <= 3.3) = 0.03; P(X <= 3.4) = 0.08; P(X <= 3.6) = 0.16; P(X <= 3.7) = 0.29; P(X <= 3.8) = 0.46; P(X <= 3.9) = 0.59; P(X <= 4.0) = 0.70; P(X <= 4.1) = 0.79; P(X <= 4.2) = 0.86; P(X <= 4.3) = 0.93; P(X <= 4.4) = 0.97; P(X <= 4.6) = 0.99. Linear interpolation gives 10th percentile at 3.45, median at 3.83, and 90th percentile at 4.26; rounded to the ABS one-decimal print precision these are 3.5%, 3.8%, and 4.3%."},{"kind":"text","text":"Prior/update/interval: persistence/reference-class prior is the fetched Dec-May All groups sequence (3.8, 3.8, 3.7, 4.6, 4.2, 4.0), centered near its 3.9% mean; adjustments are easing headline momentum, persistent 6.5% housing inflation, and uncertainty from volatile monthly components. The interval is read directly from the elicited threshold ladder, whose rung span is anchored by the fetched 3.7% trough and 4.6% March high, yielding 3.5% to 4.3% after one-decimal rounding."},{"kind":"text","text":"Counter-consideration: upside risk is a renewed housing, fuel, or food acceleration that would land above the interval; downside risk is a broad decline in goods and services prices that would land below the interval. A July print above 4.3% or below 3.5% is outside the interval."},{"kind":"forecast","point":3.8,"ciLow":3.5,"ciHigh":4.3}]}

# Reviewer critique
{"summary":"The forecast is internally coherent and preserves the supplied target identity, but it needs an explicit statement about the absence or use of a time-series/model prior.","requiredFixes":[{"rubricItem":"model_prior","severity":"warning","summary":"The reasoning uses a six-observation persistence/reference-class prior but does not explicitly state whether a time-series model was evaluated and ruled out, or identify one that was used.","actionRequested":"Add a concise sentence stating that no separate time-series model was used because the six-month sample is too short/volatile for a reliable fitted model, or document the specific model, sample, and resulting prior if one was used."}],"optionalSuggestions":["Clarify that the 80% interval is the ladder-derived 10th–90th interval; the current wording also invokes historical extrema, which should be described as calibration context rather than the interval derivation.","Name the July-specific observation window or release-status limitation so readers can distinguish currently observed May data from as-yet-unobserved June/July movements."]}

Emit the final JSON object only.
