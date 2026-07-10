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

# Threshold-ladder elicitation (promptMode ladder)
This run elicits the distribution as binary exceedance questions BEFORE stating any point estimate, then derives the published numbers from the ladder.
- After research, choose 11-15 strictly increasing thresholds t in the target's print units spanning your genuine uncertainty: the first rung's cumulative probability must be <= 0.10 and the last >= 0.90.
- For each rung independently answer the binary question 'What is the probability the first print is <= t?', as if pricing a binary market. Probabilities must be non-decreasing across rungs and within [0.01, 0.99].
- Add one math reasoning step that begins 'Ladder:' and lists every rung literally as 'P(X <= t) = p' pairs.
- Derive the published numbers FROM the ladder by linear interpolation between rungs: pointEstimate at cumulative 0.50, ciLow at 0.10, ciHigh at 0.90, each rounded to the print precision. The cell fields and the final forecast step must equal these derived values exactly.
- Keep every fast-mode requirement above (sigma arithmetic, base rate, upside/downside/outside-the-interval risks). In the Prior/update/interval step, also state how the ladder-implied 80% width compares to the 1.28*sigma width.
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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia July 2026 CPI Annual Rate","question":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, All groups CPI annual movement, July 2026, first print, not seasonally adjusted headline indicator","unit":"percent","pointEstimate":4.2,"ciLow":3.2,"ciHigh":5.1,"confidence":0.8,"thresholdLadder":{"thresholds":[2.8,3,3.2,3.4,3.6,3.8,4,4.2,4.4,4.6,4.8,5,5.1,5.3],"cumulativeProbabilities":[0.03,0.06,0.1,0.16,0.24,0.33,0.42,0.5,0.59,0.68,0.77,0.86,0.9,0.95]},"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger sourceBinding URL appears to point to the ABS Consumer Price Index, Australia, June 2026 page rather than the July 2026 Monthly CPI Indicator page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print and documents that discrepancy rather than changing the target identity.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"2026-05 All groups CPI annual movement","value":4},{"label":"2026-04 All groups CPI annual movement","value":4.2},{"label":"2026-03 All groups CPI annual movement","value":4.6},{"label":"2026-02 All groups CPI annual movement","value":3.7}],"drivers":["Recent headline CPI elevated around 4.0 percent in May","March fuel shock lifted the annual rate to 4.6 percent before partial retracement","Underlying inflation around 3.6 percent keeps persistence risk above target","July print will include fuel, rent, housing, food and policy-rebate timing effects","First-print ABS monthly indicator rounds the annual movement to one decimal"],"sourceContext":["https://www.abs.gov.au/release-calendar","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/may-2026","https://www.theguardian.com/australia-news/2026/jun/24/interest-rate-hikes-remain-on-cards-as-underlying-inflation-climbs-economists-warn","https://www.news.com.au/finance/economy/australian-economy/australias-inflation-battle-continues-as-rba-warns-of-more-tough-decisions/news-story/ffcedc46df18140671179984d1b2c634","https://www.couriermail.com.au/business/economy/australian-economy/fresh-interest-rate-hikes-loom-as-australias-inflation-surges/news-story/fe39837033488648baed79c4771dbf20"],"runAt":"2026-07-10T13:48:12Z","reasoning":[{"kind":"heading","text":"Australia July 2026 Monthly CPI Indicator Forecast"},{"kind":"text","text":"Framing and exact resolver: forecast the ABS Monthly Consumer Price Index Indicator, Australia, July 2026, All groups CPI annual movement, first print, not seasonally adjusted headline indicator, in percent rounded to one decimal. This is the monthly CPI indicator variant; every anchor and historical value used here is the same All groups CPI annual movement variant, not quarterly CPI, trimmed mean, seasonally adjusted CPI, or a later revision."},{"kind":"tool","tool":"official.lookup","call":"Check ABS release calendar and ledger target fields for the July 2026 Monthly CPI Indicator release date and resolver identity.","result":"ABS calendar/target context gives release date 2026-08-26, expected release window 2026-08-25 to 2026-09-02, target unit percent with one-decimal printed annual movement, and dataPointId abs.cpi.all_groups.yoy.2026-07.first_print."},{"kind":"tool","tool":"official.lookup","call":"Look up recent ABS Monthly CPI Indicator All groups CPI annual movement reference points reported from the public release coverage.","result":"Fetched recent All groups CPI annual movement values: May 2026 = 4.0 percent, April 2026 = 4.2 percent, March 2026 = 4.6 percent, February 2026 = 3.7 percent."},{"kind":"tool","tool":"official.lookup","call":"Look up component and macro context around the recent monthly CPI prints while keeping the target series as headline All groups CPI annual movement.","result":"Fetched context numbers: March 2026 headline = 4.6 percent with automotive fuel up 32.8 percent year over year; May 2026 headline = 4.0 percent with trimmed mean = 3.6 percent and home building reported up 5.6 percent annually."},{"kind":"text","text":"Base rate/reference class: for monthly All groups CPI annual-rate targets two months ahead, a persistence prior using the latest official-source headline rate and recent successive changes is a strong base rate because the target is a year-over-year rate with overlapping 11 of 12 months already mostly determined by recent prices. The reference class here is the latest contiguous observed annual movements from February through May 2026: 3.7, 4.6, 4.2, 4.0."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: level starts from May at 4.0 percent; momentum from March to May is downward after the fuel-shock peak, with changes of +0.9, -0.4, and -0.2 percentage points; one-off fuel volatility can pull July either way; policy-rebate and fuel-excise timing can distort monthly headline CPI; persistent rents, housing, food, and services keep the center above the RBA target band."},{"kind":"math","text":"Prior/update/interval: persistence prior = 4.0 from May 2026 All groups CPI annual movement; historical sample = February-May 2026 annual rates 3.7, 4.6, 4.2, 4.0; adjustment components = +0.2 for sticky underlying/rent/food/service inflation, +0.1 for possible rebound after temporary fuel relief, -0.1 for slowing economy and partial fuel reversal, giving a 4.2 center before ladder rounding. Successive changes are +0.9, -0.4, -0.2, so sample sigma = 0.70 percentage points and the normal 80 percent half-width is roughly 1.28*sigma = 0.90. The ladder-implied 80 percent interval is 3.2 to 5.1, half-width about 0.95 around the 4.2 median, very close to the 1.28*sigma width."},{"kind":"math","text":"Ladder: P(X <= 2.8) = 0.03; P(X <= 3.0) = 0.06; P(X <= 3.2) = 0.10; P(X <= 3.4) = 0.16; P(X <= 3.6) = 0.24; P(X <= 3.8) = 0.33; P(X <= 4.0) = 0.42; P(X <= 4.2) = 0.50; P(X <= 4.4) = 0.59; P(X <= 4.6) = 0.68; P(X <= 4.8) = 0.77; P(X <= 5.0) = 0.86; P(X <= 5.1) = 0.90; P(X <= 5.3) = 0.95. Linear interpolation gives p10 = 3.2, p50 = 4.2, and p90 = 5.1, each already at one-decimal print precision."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed fuel or import-cost spike, stronger rent and dwelling-price pass-through, or rebate expiry that would land above the interval at more than 5.1 percent. Downside risk is a sharper fuel reversal, broader household-demand weakening, or new price subsidies that would land below the interval at less than 3.2 percent. Outside the interval would require a materially larger one-month shock or policy-price adjustment than seen in the February-May reference window."},{"kind":"text","text":"Resolver discrepancy note: the registered ledger sourceBinding URL points to the ABS Consumer Price Index, Australia, June 2026 page, but the operative target is the Monthly Consumer Price Index Indicator, Australia, July 2026 All groups CPI annual movement first print at dataPointId abs.cpi.all_groups.yoy.2026-07.first_print; I keep the forecast tied to the canonical slug and document the mismatch rather than changing identity."},{"kind":"forecast","point":4.2,"ciLow":3.2,"ciHigh":5.1}]}

# Reviewer critique
{"summary":"Draft is broadly publishable against the target contract, but the interval support should be strengthened because it rests on only three recent monthly changes.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is justified from a sample sigma computed on only three February-May 2026 month-to-month changes, including a fuel-shock reversal period, which is a thin basis for realized volatility.","actionRequested":"Either broaden the historical volatility sample for Monthly CPI Indicator annual-rate changes or explicitly state why the three-change shock-window sample is sufficient for the July 2026 first print."},{"rubricItem":"update","severity":"warning","summary":"The +0.2 net movement above the 4.0 persistence prior is plausible but only loosely tied to cited evidence; the component adjustments are mostly qualitative.","actionRequested":"Tie each material adjustment to a cited official or clearly identified public datum, or reduce the claimed precision of the adjustment components."}],"optionalSuggestions":["Keep the ledger discrepancy note; it correctly preserves the target identity while flagging the sourceBinding mismatch.","Consider replacing tabloid/news citations with official ABS/RBA sources where available, since the resolver and evidence base are official-series focused.","State explicitly that June 2026 is not used because it was not yet available at run time, if that is true."]}

Emit the final JSON object only.
