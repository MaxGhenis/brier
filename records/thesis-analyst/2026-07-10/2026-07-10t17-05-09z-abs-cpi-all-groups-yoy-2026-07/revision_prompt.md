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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia July 2026 annual CPI","question":"What will the first ABS print of the national All groups Consumer Price Index annual movement for July 2026, in percent and rounded to one decimal, be?","unit":"percent","pointEstimate":4.0,"ciLow":3.3,"ciHigh":4.8,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Consumer Price Index, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 national All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered sourceBinding points to the June 2026 page and retains the former Monthly CPI Indicator naming, while the ABS calendar identifies the applicable release as Consumer Price Index, Australia, July 2026; the target remains dataPointId abs.cpi.all_groups.yoy.2026-07.first_print.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"December 2025 annual CPI","value":3.8},{"label":"January 2026 annual CPI","value":3.8},{"label":"February 2026 annual CPI","value":3.7},{"label":"March 2026 annual CPI","value":4.6},{"label":"April 2026 annual CPI","value":4.2},{"label":"May 2026 annual CPI","value":4.0}],"drivers":["Recent annual CPI momentum eased from 4.6% in March to 4.0% in May","Housing inflation remained elevated at 6.5% in May","Food and transport each rose 3.3% annually in May","Electricity-rebate unwinding can keep headline inflation volatile","July base effects create two-sided risk"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/may-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/feb-2026","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/jan-2026","https://www.abs.gov.au/media-centre/media-releases/cpi-rose-42-year-april-2026","https://www.abs.gov.au/release-calendar/future-releases/202608"],"runAt":"2026-07-10T17:05:29Z","reasoning":[{"kind":"heading","text":"Australia July 2026 annual CPI forecast"},{"kind":"text","text":"The target is the first national All groups CPI annual movement for July 2026, printed to one decimal. It is the weighted-average-of-eight-capital-cities headline series, not trimmed mean, a seasonally adjusted monthly change, or a later quarterly replacement. The ledger's Monthly CPI Indicator label and June-page sourceBinding are stale after the complete monthly CPI transition, but the target identity is unchanged."},{"kind":"tool","tool":"official.lookup","call":"Fetch the ABS January and February 2026 Consumer Price Index releases for the headline All groups annual series.","result":"ABS reported annual CPI of 3.8% in January 2026 and 3.7% in February 2026; December 2025 was 3.8%."},{"kind":"tool","tool":"official.lookup","call":"Fetch the ABS March, April, and May 2026 headline annual CPI observations.","result":"ABS reported annual CPI of 4.6% in March 2026, 4.2% in April 2026, and 4.0% in May 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetch May 2026 ABS component details for current-release mechanisms.","result":"In May 2026 headline CPI was 4.0%; Housing rose 6.5%, Food and non-alcoholic beverages 3.3%, Transport 3.3%, and trimmed mean CPI 3.6% annually."},{"kind":"tool","tool":"official.lookup","call":"Verify the July 2026 CPI publication date in the ABS future-release calendar.","result":"The ABS calendar schedules Consumer Price Index, Australia, reference period July 2026, for 26 August 2026 at 11:30am AEST."},{"kind":"text","text":"The reference class/base rate is the six first-published annual observations from December 2025 through May 2026: 3.8%, 3.8%, 3.7%, 4.6%, 4.2%, and 4.0%. Persistence around the latest 4.0% is the outside-view anchor; the 4.0% six-observation median reinforces it."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms are separated as follows: the level remains near 4%; momentum eased by 0.6 percentage point from March to May; volatile fuel, travel, and food can move individual months; and electricity-rebate exhaustion keeps Housing inflation elevated. These effects support a central value near 4.0% without extrapolating March's spike."},{"kind":"math","text":"Prior/update/interval: persistence prior = May annual CPI of 4.0%, using the December-May historical sample 3.8, 3.8, 3.7, 4.6, 4.2, 4.0. Successive changes are 0.0, -0.1, +0.9, -0.4, and -0.2 percentage point; their sample sigma = 0.50. The empirical 80% half-width is roughly 1.28*sigma = 1.28*0.50 = 0.64 point. Adjustments are -0.1 for recent easing, +0.1 for persistent Housing/electricity pressure, and 0.0 net for other one-offs, leaving 4.0%. The ladder implies 10th/90th bounds of 3.3% and 4.8%, total width 1.5 points versus the sigma-based total width of about 1.28 points, a modest 1.17x widening for rebate and base-effect volatility."},{"kind":"math","text":"Ladder: P(X <= 3.0) = 0.04; P(X <= 3.2) = 0.08; P(X <= 3.4) = 0.12; P(X <= 3.6) = 0.20; P(X <= 3.8) = 0.30; P(X <= 3.9) = 0.40; P(X <= 4.0) = 0.50; P(X <= 4.2) = 0.62; P(X <= 4.4) = 0.73; P(X <= 4.6) = 0.82; P(X <= 4.8) = 0.90; P(X <= 5.2) = 0.95. Linear interpolation gives the median at 4.0, the 10th percentile at 3.3, and the 90th percentile at 4.8, each rounded to one decimal."},{"kind":"text","text":"Upside risk comes from further electricity-rebate unwinding, fuel disruption, or unusually strong rents and services; a combined shock would land above the interval. Downside risk comes from fuel reversal, discounting, or favorable July base effects; synchronized declines across volatile and core components would land below the interval. Outside the interval therefore requires a broader or larger shock than ordinary month-to-month variation."},{"kind":"forecast","point":4.0,"ciLow":3.3,"ciHigh":4.8}],"thresholdLadder":{"thresholds":[3.0,3.2,3.4,3.6,3.8,3.9,4.0,4.2,4.4,4.6,4.8,5.2],"cumulativeProbabilities":[0.04,0.08,0.12,0.2,0.3,0.4,0.5,0.62,0.73,0.82,0.9,0.95]}}

# Reviewer critique
{"summary":"The forecast is internally coherent, but publication is blocked because its resolver source and URL do not match the canonical ledger contract.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft substitutes “Consumer Price Index, Australia, July 2026” and a different URL for the canonical “Monthly Consumer Price Index Indicator, Australia, July 2026” source and URL.","actionRequested":"Restore the canonical resolutionSource, resolutionSourceUrl, and resolutionRule verbatim; document the sourceBinding discrepancy in reasoning without redefining the resolver."},{"rubricItem":"interval","severity":"warning","summary":"The interval is based on only five successive changes in overlapping annual inflation rates, and “empirical 80% half-width” incorrectly describes a normal-theory 1.28× sample-sigma calculation.","actionRequested":"Call this a normal approximation and justify the short sample, or use a longer first-print history to estimate realized forecast-error or month-to-month volatility and derive the bounds."}],"optionalSuggestions":["Preserve the clear distinction between the canonical target contract and any suspected stale ledger metadata.","State whether the 1.17× volatility widening was judgmental or calibrated from comparable rebate/base-effect episodes."]}

Emit the final JSON object only.
