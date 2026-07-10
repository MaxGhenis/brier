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
{"slug":"australia-cpi-annual-rate-july-2026","country":"AU","type":"data","title":"Australia CPI Annual Rate, July 2026","question":"What will the Australian Bureau of Statistics first print for All groups CPI, Australia, original annual change for July 2026?","unit":"percent","pointEstimate":3.8,"ciLow":3.0,"ciHigh":4.6,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"Australian Bureau of Statistics Monthly Consumer Price Index Indicator, Australia, July 2026 release","resolutionSourceUrl":"https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/jul-2026","resolutionRule":"Resolve to the first ABS-published July 2026 Consumer Price Index, Australia All groups CPI original annual movement, in percent, rounded to one decimal as printed by ABS. Use the original first print only; ignore later revisions, corrections, or quarterly-CPI replacement values. The registered ledger resolver names the ceased Monthly CPI Indicator and its sourceBinding points to a June 2026 CPI page; this forecast remains tied to dataPointId abs.cpi.all_groups.yoy.2026-07.first_print while documenting that the official scheduled July 2026 ABS publication is Consumer Price Index, Australia.","dataPointId":"abs.cpi.all_groups.yoy.2026-07.first_print","historicalContext":[{"label":"May 2026 annual CPI","value":4.0},{"label":"April 2026 annual CPI","value":4.2},{"label":"March 2026 annual CPI","value":4.6},{"label":"February 2026 annual CPI","value":3.7},{"label":"July 2025 annual CPI","value":3.0},{"label":"July 2025 monthly CPI","value":1.3}],"drivers":["May 2026 headline CPI was 4.0%, below April's 4.2% but still elevated","Trimmed mean inflation rose to 3.6% in May 2026","July 2025 base month had a high 1.3% monthly rise","Housing remained a large contributor at 6.5% annual inflation in May","Transport inflation cooled from March spike but remained volatile"],"sourceContext":["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia","https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/monthly-consumer-price-index-indicator/sep-2025","https://www.abs.gov.au/about/key-priorities/big-data-timely-insights-phase-2/complete-monthly-measure-cpi","https://www.abs.gov.au/media-centre/media-statements/abs-announces-monthly-cpi-start-november-2025"],"runAt":"2026-07-10T16:00:29Z","thresholdLadder":{"thresholds":[2.6,2.9,3.1,3.3,3.5,3.7,3.8,3.9,4.1,4.3,4.5,4.6,4.9],"cumulativeProbabilities":[0.04,0.08,0.13,0.20,0.30,0.43,0.50,0.58,0.70,0.80,0.88,0.92,0.97]},"reasoning":[{"kind":"heading","text":"Australia July 2026 All Groups CPI Annual Inflation"},{"kind":"text","text":"Framing and exact resolver: the target is the ABS first print for All groups CPI, Australia, original annual change for July 2026, rounded to one decimal. The ledger calls this the Monthly CPI Indicator, but ABS official pages say the Monthly CPI Indicator ceased after September 2025 and the complete Monthly CPI is now published under Consumer Price Index, Australia; I keep the ledger dataPointId and document the discrepancy."},{"kind":"tool","tool":"official.lookup","call":"ABS Consumer Price Index, Australia latest release page and future-release schedule lookup","result":"Fetched May 2026 CPI release: annual CPI 4.0%, April 2026 annual CPI 4.2%, May original monthly CPI -0.7%, May seasonally adjusted monthly CPI -0.1%, trimmed mean annual inflation 3.6%, and official future release date for Consumer Price Index, Australia, July 2026 of 26/08/2026 11:30am AEST."},{"kind":"tool","tool":"official.lookup","call":"ABS All groups CPI monthly and annual movement table","result":"Fetched annual All groups CPI history: Apr-25 2.4%, May-25 2.1%, Jun-25 1.9%, Jul-25 3.0%, Aug-25 3.2%, Sep-25 3.6%, Oct-25 3.8%, Nov-25 3.4%, Dec-25 3.8%, Jan-26 3.8%, Feb-26 3.7%, Mar-26 4.6%, Apr-26 4.2%, May-26 4.0%; monthly changes included Jun-25 0.1%, Jul-25 1.3%, Mar-26 1.1%, Apr-26 0.4%, May-26 -0.7%."},{"kind":"tool","tool":"official.lookup","call":"ABS CPI groups and contributions tables for current-release drivers","result":"Fetched May 2026 group annual rates: Housing 6.5%, Food and non-alcoholic beverages 3.3%, Transport 3.3%, Clothing and footwear 5.0%, Education 4.8%; contribution table showed May 2026 Housing contribution 1.4071 percentage points and Transport contribution 0.3722 percentage points."},{"kind":"tool","tool":"official.lookup","call":"ABS transition and final Monthly CPI Indicator pages","result":"Fetched ABS transition evidence: September 2025 was the final Monthly CPI Indicator release with annual indicator 3.5%, July 2025 indicator 2.8%, August 2025 indicator 3.0%, and the first complete Monthly CPI publication began with October 2025 on 26/11/2025."},{"kind":"text","text":"Variant consistency: all anchors and calculations use the ABS complete Monthly CPI, All groups CPI, Australia, original annual movement from the page table 'All groups CPI, Australia, monthly and annual movement (%)'; I do not mix in seasonally adjusted, trimmed mean, or the old Monthly CPI Indicator as the target series."},{"kind":"math","text":"Prior/update/interval: base rate/reference class prior is persistence in the complete Monthly CPI annual rate from Apr-25 to May-26. The latest annual rate is 4.0%; the high Jul-25 base month (+1.3% m/m after Jun-25 +0.1%) mechanically pulls July 2026 annual inflation down unless Jun-Jul 2026 monthly gains repeat the rebate/fuel spike, while sticky trimmed mean at 3.6%, housing at 6.5%, and broad services pressure offset some downside. Successive annual-rate changes from Apr-25..May-26 were -0.3, -0.2, +1.1, +0.2, +0.4, +0.2, -0.4, +0.4, 0.0, -0.1, +0.9, -0.4, -0.2 percentage points; sample sigma = 0.48, so 1.28*sigma = 0.62 percentage points. I widen to a ladder-implied 80% half-width of 0.8 points, about 1.29x the sigma half-width, because June and July are both still unknown and July base/rebate effects are unusually lumpy."},{"kind":"math","text":"Ladder: P(X <= 2.6) = 0.04; P(X <= 2.9) = 0.08; P(X <= 3.1) = 0.13; P(X <= 3.3) = 0.20; P(X <= 3.5) = 0.30; P(X <= 3.7) = 0.43; P(X <= 3.8) = 0.50; P(X <= 3.9) = 0.58; P(X <= 4.1) = 0.70; P(X <= 4.3) = 0.80; P(X <= 4.5) = 0.88; P(X <= 4.6) = 0.92; P(X <= 4.9) = 0.97. Linear interpolation gives p10 between 2.9 and 3.1 at 2.98, rounded to 3.0; p50 at 3.8; p90 between 4.5 and 4.6 at 4.55, rounded to 4.6."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed fuel or electricity/rebate shock plus sticky housing that would land above the interval. Downside risk is further fuel reversal and weak discretionary prices pushing the July print toward the low 3s. Outside the interval below 3.0 would likely require very soft June-July monthly CPI despite the known sticky components; outside the interval above 4.6 would likely require another March-like energy or administered-price jump."},{"kind":"forecast","point":3.8,"ciLow":3.0,"ciHigh":4.6}]}

# Reviewer critique
{
  "summary": "Draft is mostly methodologically sound, but it should not publish while resolver fields diverge from the canonical ledger target contract.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft changes the canonical resolutionSourceUrl and resolver wording from the ledger Monthly CPI Indicator July 2026 target to a Consumer Price Index, Australia URL and rule.",
      "actionRequested": "Set resolutionSource, resolutionSourceUrl, and resolutionRule to the canonical ledger fields exactly; keep the ABS publication-discrepancy explanation only in reasoning, not by changing target fields."
    },
    {
      "rubricItem": "coherence",
      "severity": "warning",
      "summary": "The question/title/resolver wording alternates between Monthly CPI Indicator and Consumer Price Index, Australia, which could make the published target identity look ambiguous.",
      "actionRequested": "Keep the JSON target identity aligned with catalogSlug, dataPointId, unit, and canonical resolver text; explain any ABS naming transition as context without redefining the target."
    }
  ],
  "optionalSuggestions": [
    "The prior/update/interval step is strong; consider making the final implied 80% bounds explicit in the same sentence as the point estimate.",
    "Tail scenarios are concrete, but the upside tail could name the specific July-relevant administered-price or energy channels if known from ABS history."
  ]
}

Emit the final JSON object only.
