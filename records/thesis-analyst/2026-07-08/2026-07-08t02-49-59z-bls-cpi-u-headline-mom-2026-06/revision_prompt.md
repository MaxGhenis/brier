# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.cpi.u.headline_mom
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-cpi-u-mom-june-2026"

# Source hints
- Use the official agency release calendar, not inferred cadence.
- FRED may be used as a history mirror, but resolution cites the agency.
- For FOMC targets, resolve to the target range upper bound after the announcement.
- For DOL claims, name the week-ending date and cite the release date.

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
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
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
{"slug":"us-cpi-u-mom-june-2026","country":"US","type":"data","title":"US CPI-U MoM June 2026","question":"BLS Consumer Price Index for All Urban Consumers, U.S. city average, all items, seasonally adjusted month-over-month percent change for June 2026, first print","unit":"percent_growth","pointEstimate":0.2,"ciLow":-0.1,"ciHigh":0.5,"confidence":0.8,"resolutionDate":"2026-07-14","resolutionSource":"U.S. Bureau of Labor Statistics, Consumer Price Index Summary","resolutionSourceUrl":"https://www.bls.gov/news.release/cpi.nr0.htm","resolutionRule":"Resolve to the first-published seasonally adjusted month-over-month percent change in the all-items CPI-U for June 2026 in the BLS Consumer Price Index Summary released on July 14, 2026 at 8:30 a.m. ET. Use the headline Table A value rounded to one decimal percent as first published; ignore later seasonal-adjustment revisions.","dataPointId":"bls.cpi.u.headline_mom.june_2026.first_print","historicalContext":[{"label":"Dec 2025 CPI-U all items SA MoM percent","value":0.3},{"label":"Jan 2026 CPI-U all items SA MoM percent","value":0.2},{"label":"Feb 2026 CPI-U all items SA MoM percent","value":0.3},{"label":"Mar 2026 CPI-U all items SA MoM percent","value":0.9},{"label":"Apr 2026 CPI-U all items SA MoM percent","value":0.6},{"label":"May 2026 CPI-U all items SA MoM percent","value":0.5},{"label":"Jul 6 2026 EIA U.S. regular gasoline dollars per gallon","value":3.777}],"drivers":["Recent headline CPI base rate was high but energy-driven","June weekly gasoline prices fell steadily after the May CPI print","Core CPI was 0.2 percent in May and keeps the non-energy center positive","Food and shelter remained low-positive in May","Energy reversal is the main downshift from earlier June forecasts"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm","https://www.bls.gov/news.release/cpi.nr0.htm","https://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_nus_w.htm"],"runAt":"2026-07-08T02:51:27Z","thresholdLadder":{"thresholds":[-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7],"cumulativeProbabilities":[0.03,0.06,0.1,0.23,0.36,0.5,0.65,0.78,0.9,0.96,0.98]},"reasoning":[{"kind":"heading","text":"Forecast June 2026 headline CPI-U month-over-month"},{"kind":"text","text":"Framing and exact resolver: this is BLS CPI-U all items, U.S. city average, seasonally adjusted month-over-month percent change for June 2026, first print. The series variant is headline CPI-U SA MoM from BLS CPI Summary Table A; anchors below use that same variant, not NSA index levels or core CPI as the target."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS CPI release schedule for the June 2026 reference month.","result":"Fetched official schedule: Consumer Price Index reference month June 2026 has release date Jul. 14, 2026 and release time 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Fetched the current BLS Consumer Price Index Summary Table A for recent headline and component monthly changes.","result":"Fetched BLS Table A values: all items CPI-U 0.3 in Dec 2025, 0.2 in Jan 2026, 0.3 in Feb 2026, 0.9 in Mar 2026, 0.6 in Apr 2026, and 0.5 in May 2026; May core was 0.2, food 0.2, shelter 0.3, energy 3.9, gasoline 7.0 percent."},{"kind":"tool","tool":"official.lookup","call":"Fetched EIA weekly U.S. retail gasoline prices for the June CPI pricing window and latest available week.","result":"Fetched EIA U.S. regular gasoline prices: 06/01/26 4.305, 06/08/26 4.146, 06/15/26 4.052, 06/22/26 3.914, 06/29/26 3.831, 07/06/26 3.777 dollars per gallon; all-grades gasoline was 4.439, 4.281, 4.187, 4.048, 3.964, 3.911 over the same dates."},{"kind":"text","text":"Base rate/reference class: the six same-variant BLS headline SA MoM prints from Dec 2025 through May 2026 average 0.47 percent, with latest persistence at 0.5. That base rate is inflated by the energy shock: BLS reported energy monthly increases of 10.9 in March, 3.8 in April, and 3.9 percent in May."},{"kind":"text","text":"Update from previous run/context: an older catalog forecast was centered higher before the full June gasoline decline was visible; I treat that only as strategy context, not evidence. The public EIA price path since June 1 makes the energy contribution materially lower than in May, while May core 0.2, food 0.2, and shelter 0.3 keep a positive non-energy floor."},{"kind":"math","text":"Ladder: P(X <= -0.3) = 0.03; P(X <= -0.2) = 0.06; P(X <= -0.1) = 0.10; P(X <= 0.0) = 0.23; P(X <= 0.1) = 0.36; P(X <= 0.2) = 0.50; P(X <= 0.3) = 0.65; P(X <= 0.4) = 0.78; P(X <= 0.5) = 0.90; P(X <= 0.6) = 0.96; P(X <= 0.7) = 0.98. Linear interpolation gives p10 = -0.1, p50 = 0.2, and p90 = 0.5, each already at one-decimal print precision."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior is the BLS recent headline SA MoM reference class Dec 2025-May 2026 values [0.3, 0.2, 0.3, 0.9, 0.6, 0.5], mean = 0.467. Adjustment components are about -0.20 for gasoline/energy reversal, -0.05 for core mean reversion from April, and 0.00 to +0.05 for shelter/food persistence, giving center near 0.20. Interval method uses realized dispersion of the fetched change values themselves: sigma = 0.258, so 1.28*sigma = 0.330. The ladder-implied 80% half-width is 0.30 around 0.2, close to the realized-volatility half-width, so no extra widening is applied."},{"kind":"text","text":"Counter-consideration and scenarios: upside risk would land above the interval if June gasoline seasonal adjustment or renewed oil disruption keeps energy CPI positive while shelter/core services reaccelerate, pushing headline above 0.5. Downside risk would land below the interval if gasoline, airfares, and vehicle-related prices fall together enough to offset core services and food, pushing headline below -0.1. An outside the interval miss would most likely come from an energy seasonal-adjustment surprise rather than the stable core categories."},{"kind":"forecast","point":0.2,"ciLow":-0.1,"ciHigh":0.5}]}

# Reviewer critique
{"summary":"The draft is publishable with a clear BLS first-print resolver, coherent point/interval fields, and no evident leakage or unit ambiguity.","requiredFixes":[],"optionalSuggestions":["State explicitly that the persistence/base-rate prior is the chosen simple time-series prior, or add one sentence ruling out a richer model because the release is near-term and dominated by energy component timing.","Consider noting that the volatility estimate uses only six recent monthly prints, so the interval is intentionally tied to recent realized volatility rather than a long-run CPI distribution."]}

Emit the final JSON object only.
