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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI annual rate, July 2026","question":"What will the Australian Bureau of Statistics first print for the July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, not seasonally adjusted, in percent rounded to one decimal?","unit":"percent","pointEstimate":4.3,"ciLow":3.5,"ciHigh":5.2,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger sourceBinding URL appears to point to the ABS Consumer Price Index, Australia, June 2026 page rather than the July 2026 Monthly CPI Indicator page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and documents that discrepancy rather than changing the target identity.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"2026-05 All groups CPI annual movement","value":4.0},{"label":"2026-04 All groups CPI annual movement","value":4.2},{"label":"2026-03 All groups CPI annual movement","value":4.6},{"label":"2026-02 All groups CPI annual movement","value":3.7}],"drivers":["Recent all-groups annual CPI is near 4 percent after a March fuel shock","July fuel-excise and oil-price pass-through can lift the annual rate again","Housing and rents remain sticky upside contributors","Monthly CPI indicator is partial-sample and prints to one decimal","First-print target ignores later corrections or quarterly-CPI replacement values"],"sourceContext":["https://www.abs.gov.au/release-calendar","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/april-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/march-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026"],"runAt":"2026-07-10T21:14:13Z","thresholdLadder":{"thresholds":[3.0,3.3,3.6,3.8,4.0,4.2,4.4,4.6,4.8,5.0,5.2,5.5,5.8],"cumulativeProbabilities":[0.03,0.07,0.12,0.20,0.31,0.43,0.54,0.65,0.75,0.83,0.90,0.96,0.98]},"reasoning":[{"kind":"heading","text":"Australia July 2026 monthly CPI indicator forecast"},{"kind":"text","text":"Framing: the resolver is the ABS Monthly Consumer Price Index Indicator, Australia, July 2026 release, All groups CPI annual movement, first print, in percent rounded to one decimal. I use the same monthly-indicator all-groups annual variant for anchors; I do not mix in quarterly CPI, seasonally adjusted variants, trimmed mean, or later revisions."},{"kind":"tool","tool":"official.lookup","call":"Check ABS release calendar and target page contract for the July 2026 Monthly Consumer Price Index Indicator release.","result":"ABS release calendar target is 26 August 2026 for the July 2026 Monthly CPI Indicator; the registered target window is 2026-08-25 to 2026-09-02 and the first-print value will be one decimal percent."},{"kind":"tool","tool":"official.lookup","call":"Read ABS Monthly Consumer Price Index Indicator, Australia, May 2026 release for the same All groups CPI annual movement variant and component context.","result":"Fetched May 2026 All groups CPI annual movement 4.0%; housing annual movement 5.2%; rents annual movement 7.4%; automotive fuel annual movement -5.1%."},{"kind":"tool","tool":"official.lookup","call":"Read ABS Monthly Consumer Price Index Indicator, Australia, April 2026 release for the same All groups CPI annual movement variant.","result":"Fetched April 2026 All groups CPI annual movement 4.2%; March 2026 comparison 4.6%; trimmed mean inflation 3.4%."},{"kind":"tool","tool":"official.lookup","call":"Read ABS Monthly Consumer Price Index Indicator, Australia, March 2026 release for the same All groups CPI annual movement variant and shock context.","result":"Fetched March 2026 All groups CPI annual movement 4.6%; February 2026 comparison 3.7%; automotive fuel annual movement 32.8%."},{"kind":"text","text":"Reference class and base rate: for near-term Australian monthly CPI indicator all-groups annual forecasts, the strongest public reference class is recent same-series persistence plus one- to three-month shock reversal. The fetched same-variant sequence 3.7%, 4.6%, 4.2%, 4.0% anchors the ladder span: most mass stays in the high-3s to high-4s, with a meaningful right tail if fuel or housing re-accelerates."},{"kind":"text","text":"Prior/update/interval: persistence prior is the recent same-series All groups CPI annual movement centered around the May 2026 4.0% print, using the February-May 2026 sample of 3.7%, 4.6%, 4.2%, and 4.0%; I update upward for the July fuel-excise/oil pass-through risk and sticky housing/rent pressure, partly offset by likely normalization from the March fuel spike and monthly-indicator sampling noise. The interval method is a threshold ladder grounded on the fetched 3.7%-4.6% recent range, widened for two unknown monthly prints before July and one-off fuel-policy effects; final implied bounds are 10th percentile 3.5, median 4.3, and 90th percentile 5.2."},{"kind":"math","text":"Ladder: P(X <= 3.0) = 0.03; P(X <= 3.3) = 0.07; P(X <= 3.6) = 0.12; P(X <= 3.8) = 0.20; P(X <= 4.0) = 0.31; P(X <= 4.2) = 0.43; P(X <= 4.4) = 0.54; P(X <= 4.6) = 0.65; P(X <= 4.8) = 0.75; P(X <= 5.0) = 0.83; P(X <= 5.2) = 0.90; P(X <= 5.5) = 0.96; P(X <= 5.8) = 0.98. Linear interpolation gives 10th percentile at 3.48, median at 4.33, and 90th percentile at 5.20; rounded to the ABS print precision this is 10th percentile at 3.5, median at 4.3, and 90th percentile at 5.2."},{"kind":"text","text":"Counter-considerations: upside risk is a larger July fuel rebound, rent acceleration, or supply shock that would land above the interval near 5.3% or higher. Downside risk is a sharper fuel reversal, energy subsidy effect, or broad goods disinflation that would land outside the interval below 3.5%. The central case keeps annual inflation above target but below the March shock peak."},{"kind":"forecast","point":4.3,"ciLow":3.5,"ciHigh":5.2}]}

# Reviewer critique
{
  "summary": "The draft is publishable with one warning: its upward update is directionally explained but should quantify or cite the July fuel/oil-policy adjustment more concretely.",
  "requiredFixes": [
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "The point estimate moves from a 4.0% May persistence anchor to 4.3%, but the July fuel-excise/oil pass-through adjustment is asserted without a concrete magnitude or cited current evidence.",
      "actionRequested": "Add a short quantified update bridge, e.g. how much of the +0.3pp central shift comes from fuel/oil, housing/rents, and sampling/noise, or explicitly state the adjustment is judgmental and why it is limited."
    }
  ],
  "optionalSuggestions": [
    "State that the threshold ladder represents the 10th-90th percentile 80% interval to make confidence semantics explicit.",
    "If available in the trace, include one current public oil/fuel or policy datapoint supporting the upside fuel-risk driver."
  ]
}

Emit the final JSON object only.
