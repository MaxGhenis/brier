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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia July CPI annual rate","question":"Australian Bureau of Statistics All groups CPI annual movement, Australia, July 2026, original (not seasonally adjusted), first print","unit":"percent","pointEstimate":3.2,"ciLow":2.6,"ciHigh":3.8,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/july-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Monthly Consumer Price Index Indicator All groups CPI annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"May 2026 annual CPI","value":4},{"label":"April 2026 annual CPI","value":4.2},{"label":"March 2026 annual CPI","value":4.6},{"label":"February 2026 annual CPI","value":3.7},{"label":"January 2026 annual CPI","value":3.8},{"label":"July 2025 annual CPI","value":3}],"drivers":["July 2025's 1.3% monthly rise creates a favourable annual base effect","The expiry of electricity-rebate effects should reduce the annual rate as comparisons roll forward","Housing, food, and services inflation remain persistent offsets"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia","https://www.abs.gov.au/release-calendar/future-releases-calendar/202608"],"runAt":"2026-07-10T15:30:28Z","reasoning":[{"kind":"heading","text":"Australia July 2026 all-groups CPI annual movement"},{"kind":"text","text":"The resolver is the original ABS first print of All groups CPI annual movement in percent, original rather than seasonally adjusted, rounded to one decimal. ABS now labels the release Consumer Price Index, Australia; the registered sourceBinding points to the June 2026 Consumer Price Index page rather than the specified July Monthly CPI Indicator page, so I retain the ledger dataPointId and rule rather than changing target identity."},{"kind":"tool","tool":"official.lookup","call":"ABS future-release listing and August 2026 official release calendar lookup for the July 2026 CPI publication date.","result":"ABS lists Consumer Price Index, Australia, July 2026 for 26/08/2026 at 11:30am AEST; its latest May release reports all-groups annual CPI at 4.0%."},{"kind":"tool","tool":"official.lookup","call":"ABS May 2026 Consumer Price Index, Australia release, table 'All groups CPI, Australia, monthly and annual movement (%)'.","result":"Fetched matched-variant annual all-groups CPI rates: Apr-25 2.4%, May-25 2.1%, Jun-25 1.9%, Jul-25 3.0%, Aug-25 3.2%, Sep-25 3.6%, Oct-25 3.8%, Nov-25 3.4%, Dec-25 3.8%, Jan-26 3.8%, Feb-26 3.7%, Mar-26 4.6%, Apr-26 4.2%, May-26 4.0%."},{"kind":"tool","tool":"official.lookup","call":"ABS May 2026 release component and analytical-series lookup.","result":"Fetched May component evidence: electricity annual inflation was 21.1%, housing 6.5%, food and non-alcoholic beverages 3.3%, transport 3.3%, services 3.7%, and trimmed mean 3.6%; May all-groups CPI fell 0.7% in original monthly terms."},{"kind":"text","text":"The reference class/base rate is the 14 monthly all-groups annual prints from Apr-2025 to May-2026, centred near the recent 4.0% level. The same original all-groups annual-movement variant is used for every anchor and historical value; no seasonally adjusted or quarterly value is mixed in."},{"kind":"math","text":"Prior/update/interval: A persistence prior starts from May's 4.0%; the Apr-2025--May-2026 historical sample has successive annual-rate changes with sample standard deviation sigma = 0.48 percentage points. July 2025's 1.3% monthly increase and the roll-forward of electricity-rebate comparisons imply a -0.6 point base-effect adjustment, while persistent housing, food, and services leave a further -0.2 point net adjustment, giving 4.0 - 0.6 - 0.2 = 3.2%. The realized-dispersion interval method gives 1.28*sigma = 0.61 points, rounded to an implied 80% range of 2.6% to 3.8%."},{"kind":"text","text":"Upside risk is a larger July annual electricity-price reset or renewed food and fuel pressure, which would land above the interval if it pushed the annual rate above 3.8%. Downside risk is a sharper reversal of the earlier rebate-related price level plus broad discretionary-price falls; a sufficiently large fall would land below the interval at under 2.6%."},{"kind":"forecast","point":3.2,"ciLow":2.6,"ciHigh":3.8}]}

# Reviewer critique
{"summary":"The draft is coherent and traceable, but its large downward update needs a more explicit evidentiary basis and the ledger source-binding discrepancy should be retained in the resolver text.","requiredFixes":[{"rubricItem":"update","severity":"warning","summary":"The -0.8 percentage-point update is decomposed arithmetically, but the -0.6 base-effect and -0.2 persistence adjustments are asserted without showing the July-specific price-level comparison or evidence supporting their magnitudes.","actionRequested":"Add compact official evidence or a transparent calculation linking the July 2025 1.3% monthly increase and electricity-rebate comparison to the stated -0.6 adjustment, and explain the basis for the additional -0.2 adjustment."},{"rubricItem":"resolver","severity":"warning","summary":"The reasoning documents the registered sourceBinding URL discrepancy, but the forecast's resolutionRule omits the canonical ledger language that records it.","actionRequested":"Include the ledger discrepancy sentence in the resolutionRule, while keeping the same dataPointId, July 2026 first-print source, and 2026-08-26 resolution date."}],"optionalSuggestions":["State explicitly that persistence is the selected time-series prior and that no separate fitted trend/AR model was used.","Name the 13 successive changes underlying the 0.48-point sample standard deviation for easier auditability."]}

Emit the final JSON object only.
