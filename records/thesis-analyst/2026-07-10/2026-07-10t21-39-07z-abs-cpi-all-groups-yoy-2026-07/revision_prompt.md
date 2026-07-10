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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI annual rate, July 2026","question":"What will the first ABS-published All groups CPI, Australia annual movement for July 2026 be, in original terms and rounded to one decimal?","unit":"percent","pointEstimate":4.0,"ciLow":3.2,"ciHigh":4.8,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger sourceBinding URL appears to point to the ABS Consumer Price Index, Australia, June 2026 page rather than the July 2026 Monthly CPI Indicator page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and documents that discrepancy rather than changing the target identity.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"March 2026 annual CPI","value":4.6},{"label":"April 2026 annual CPI","value":4.2},{"label":"May 2026 annual CPI","value":4.0},{"label":"July 2025 annual CPI","value":3.0}],"drivers":["May annual CPI momentum eased to 4.0%","services and non-tradables inflation remained firm","electricity-rebate effects elevated housing inflation","July 2025 electricity and headline CPI base effects roll out","higher fuel prices create near-term upside risk"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/april-2026","https://www.abs.gov.au/release-calendar/future-releases-calendar/202608","https://www.rba.gov.au/publications/smp/2026/may/overview.html"],"runAt":"2026-07-10T21:39:23Z","thresholdLadder":{"thresholds":[2.8,3.0,3.2,3.4,3.6,3.8,4.0,4.2,4.4,4.6,4.8,5.0,5.2],"cumulativeProbabilities":[0.04,0.07,0.11,0.18,0.28,0.4,0.52,0.64,0.75,0.84,0.91,0.95,0.97]},"reasoning":[{"kind":"heading","text":"Australia All groups CPI annual movement, July 2026 first print"},{"kind":"text","text":"The target is the original, not seasonally adjusted, All groups CPI annual movement for July 2026, printed to one decimal by ABS. It resolves only to the first print. The ledger calls the release the Monthly CPI Indicator and supplies a sourceBinding for the June CPI page, while the current ABS calendar labels the July publication Consumer Price Index, Australia; I preserve the registered dataPointId and resolver and document this discrepancy rather than changing target identity."},{"kind":"tool","tool":"official.lookup","call":"Fetch the ABS May 2026 Consumer Price Index release and its All groups CPI history.","result":"ABS reported annual All groups CPI of 4.6% in March 2026, 4.2% in April, and 4.0% in May; monthly original CPI was 1.1%, 0.4%, and -0.7%, respectively. July 2025 annual CPI was 3.0% and its monthly movement was 1.3%."},{"kind":"tool","tool":"official.lookup","call":"Fetch ABS May 2026 component and analytical-series movements.","result":"In May 2026, Housing inflation was 6.5%, Transport 3.3%, Food 3.3%, trimmed mean 3.6%, non-tradables 4.7%, and tradables 2.5%. Electricity rose 21.1% annually but only 3.9% excluding government-rebate effects."},{"kind":"tool","tool":"official.lookup","call":"Fetch the RBA May 2026 Statement on Monetary Policy inflation projections.","result":"The RBA projected year-ended CPI inflation of 4.8% for June 2026 and 4.0% for December 2026, with trimmed mean inflation of 3.8% and 3.5%, respectively."},{"kind":"tool","tool":"official.lookup","call":"Verify the July 2026 CPI release date in the ABS August 2026 future-release calendar.","result":"The official ABS calendar places Consumer Price Index, Australia July 2026 on 26 August 2026 at 11:30am, verifying resolutionDate 2026-08-26 rather than inferring it from monthly cadence."},{"kind":"text","text":"Reference class/base rate: the fetched annual sequence from July 2025 through May 2026 was 3.0%, 3.2%, 3.6%, 3.8%, 3.4%, 3.8%, 3.8%, 3.7%, 4.6%, 4.2%, and 4.0%. Persistence near the latest 4.0% is the outside-view anchor, while the observed range of 3.0% to 4.6% anchors the central ladder span."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms point in different directions. The 4.0% May level and 3.6% trimmed mean show persistent underlying pressure; headline momentum eased from March. Expiring electricity rebates raised measured housing inflation, while the unusually large 13.5% July 2025 electricity increase and 1.3% headline monthly increase become adverse base effects when they roll out. Higher fuel costs can offset part of that decline."},{"kind":"math","text":"Ladder: P(X <= 2.8) = 0.04; P(X <= 3.0) = 0.07; P(X <= 3.2) = 0.11; P(X <= 3.4) = 0.18; P(X <= 3.6) = 0.28; P(X <= 3.8) = 0.40; P(X <= 4.0) = 0.52; P(X <= 4.2) = 0.64; P(X <= 4.4) = 0.75; P(X <= 4.6) = 0.84; P(X <= 4.8) = 0.91; P(X <= 5.0) = 0.95; P(X <= 5.2) = 0.97. Linear interpolation gives the 10th percentile at 3.15, median at 3.97, and 90th percentile at 4.77; rounded to the ABS print precision these are 3.2, 4.0, and 4.8."},{"kind":"text","text":"Prior/update/interval: A latest-value persistence model uses the July 2025-May 2026 reference-class sample (3.0%-4.6%) and starts from May's 4.0%. Updates comprise sticky services/non-tradables and fuel pressure upward, offset by recent headline slowing and the July 2025 electricity/headline base effects. The interval method is direct threshold-ladder quantile inversion, yielding final implied 80% bounds of 3.2% to 4.8% and a 4.0% median."},{"kind":"text","text":"Upside risk: a larger fuel shock, renewed electricity-price increases, or broader pass-through into goods and services would land above the interval. Downside risk: a sharp fuel reversal plus a stronger-than-expected electricity base-effect unwind would land below the interval. An outcome outside the interval would therefore require a materially larger one-off price move than embedded in the recent ABS reference class."},{"kind":"forecast","point":4.0,"ciLow":3.2,"ciHigh":4.8}]}

# Reviewer critique
{"summary":"Publication-ready apart from a weakly calibrated interval and one overstated tail claim.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The ladder probabilities are not calibrated to realized month-to-month changes, forecast errors, or another explicit uncertainty calculation; the historical level range alone does not justify the 3.2%–4.8% interval.","actionRequested":"Briefly quantify historical annual-rate change volatility or explain how specific uncertainty components support the ladder's 10th and 90th percentiles."},{"rubricItem":"tails","severity":"warning","summary":"The claim that any result outside the interval requires a move larger than the recent reference class is inconsistent with the cited sample, which already includes 3.0%, below the 3.2% lower bound.","actionRequested":"Remove that claim or distinguish historical levels from prospective one-month shocks, while retaining the concrete upside and downside scenarios."}],"optionalSuggestions":[]}

Emit the final JSON object only.
