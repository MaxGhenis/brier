# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.real_earnings.avg_hourly_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-real-avg-hourly-earnings-mom-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.real_earnings.avg_hourly_mom.2026-07.first_print"
- resolutionDate: "2026-08-12"
- resolutionSource: "U.S. Bureau of Labor Statistics Real Earnings Table A-1"
- resolutionSourceUrl: "https://www.bls.gov/news.release/realer.t01.htm"
- resolutionRule: "Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-18", "start": "2026-08-10"}, "field": "bls.real_earnings.avg_hourly_mom", "releasePolicy": "first_print", "sourceSeriesId": "bls.real_earnings.avg_hourly_mom", "sourceUrl": "https://www.bls.gov/news.release/realer.t01.htm", "table": "U.S. Bureau of Labor Statistics Real Earnings Table A-1", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-8662209989befa5925d38419a847521e7a1076b91048aef177ca79c7544f4334.json"
- targetContentHash: "8662209989befa5925d38419a847521e7a1076b91048aef177ca79c7544f4334"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"

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
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US real average hourly earnings, July 2026","question":"U.S. BLS Table A-1 seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, July 2026 first print","unit":"percent","pointEstimate":-0.1,"ciLow":-0.5,"ciHigh":0.3,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"2025-12 first print","value":-0.3},{"label":"2026-01 first print","value":0.3},{"label":"2026-02 first print","value":0.2},{"label":"2026-03 first print","value":-0.6},{"label":"2026-04 first print","value":-0.5},{"label":"2026-05 first print","value":-0.1}],"drivers":["Recent real-hourly-earnings prints have been mostly negative after inflation deflation","June nominal private average hourly earnings rose 0.3 percent","July CPI inflation relative to nominal earnings is the dominant unresolved offset"],"sourceContext":["https://www.bls.gov/schedule/2026/08_sched.htm","https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/news.release/archives/realer_02132026.htm","https://www.bls.gov/news.release/archives/realer_03112026.htm","https://www.bls.gov/news.release/archives/realer_04102026.htm","https://www.bls.gov/news.release/archives/empsit_07022026.htm"],"runAt":"2026-07-10T15:35:05Z","reasoning":[{"kind":"heading","text":"July 2026 real average hourly earnings first-print forecast"},{"kind":"text","text":"The resolver is BLS Real Earnings Table A-1: the seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls. Table A-1 uses CPI-U to deflate this all-employees series; all anchors below use that same SA Table A-1 variant. The official BLS August 2026 calendar schedules Real Earnings for July 2026 on August 12 at 08:30 Eastern, verifying the 2026-08-12 resolution date."},{"kind":"tool","tool":"official.lookup","call":"Fetch BLS Real Earnings Table A-1 for the latest available official release.","result":"BLS Table A-1 fetched real average hourly earnings over-the-month changes of 0.4 percent in May 2025, -0.6 percent in March 2026, -0.5 percent in April 2026, and -0.1 percent in May 2026; the associated May 2026 CPI-U change was 0.5 percent and nominal average-hourly-earnings change was 0.3 percent."},{"kind":"tool","tool":"official.lookup","call":"Fetch the BLS archived January 2026 Real Earnings release, Table A-1.","result":"The BLS January 2026 Table A-1 release fetched a -0.3 percent December 2025 real average hourly earnings change and a 0.3 percent January 2026 change; January real average hourly earnings were $11.38."},{"kind":"tool","tool":"official.lookup","call":"Fetch the BLS archived February and March 2026 Real Earnings releases, Table A-1.","result":"The BLS February release fetched a 0.2 percent February 2026 real average hourly earnings change and $11.40 level; the March release fetched a -0.6 percent March 2026 change and $11.32 level."},{"kind":"tool","tool":"official.lookup","call":"Fetch the BLS June 2026 Employment Situation release for the latest nominal earnings signal.","result":"The BLS June Employment Situation fetched total-private average hourly earnings of $37.51 in May and $37.64 in June, a $0.13 or 0.3 percent increase; total-private average weekly hours were 34.3 in both months."},{"kind":"text","text":"Reference class/base rate: the six December-to-May first-print Table A-1 changes (-0.3, 0.3, 0.2, -0.6, -0.5, -0.1 percent) average -0.17 percent. The latest -0.1 percent is less negative than March and April but does not establish a sustained positive-real-pay regime."},{"kind":"text","text":"The June nominal 0.3 percent hourly-earnings increase is a modest positive adjustment versus the negative recent real-pay base rate. It is not enough to project a positive July real print without knowing July CPI-U, so the combined point remains -0.1 percent."},{"kind":"math","text":"Prior/update/interval: persistence/mean-reversion prior is the six first-print SA Table A-1 values from December-May, with mean -0.17 percent; adjustments are +0.1 percentage point for June's 0.3 percent nominal wage momentum, offset by unresolved July CPI-U deflation risk. For this change series, using the values themselves gives sample sigma = 0.37 percentage point; 1.28*sigma = 0.47 percentage point. A one-decimal 80% interval centered near the adjusted -0.1 point is -0.5 to 0.3 percent, half-width 0.40 percentage point, or 0.86 times the dispersion-based width."},{"kind":"text","text":"upside risk: a soft July CPI-U print combined with another roughly 0.3 percent nominal wage gain would land above the interval. downside risk: CPI-U acceleration with flat nominal hourly earnings would land below the interval; a large energy or goods-price move is the principal outside the interval scenario."},{"kind":"forecast","point":-0.1,"ciLow":-0.5,"ciHigh":0.3}]}

# Reviewer critique
{"summary":"The forecast is resolver-correct and internally coherent overall, but its stated 80% interval is narrower than its own volatility calculation without a sufficient justification.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The stated 80% dispersion-based width is ±0.47 percentage point, while the submitted interval uses ±0.40 percentage point (and is asymmetric after rounding); the unexplained 0.86 multiplier weakens the interval method.","actionRequested":"Either use bounds consistent with the stated 1.28×sample-sigma method, or explicitly justify the narrowing with a concrete uncertainty adjustment and recalculate the claimed coverage/confidence accordingly."},{"rubricItem":"tails","severity":"warning","summary":"The upside and downside scenarios identify relevant drivers but do not quantify the wage/CPI combinations or resulting target values.","actionRequested":"State concrete tail conditions and approximate Table A-1 outcomes, such as a nominal-wage change and CPI-U change that would imply a value above 0.3% or below -0.5%."}],"optionalSuggestions":["Consider noting that the six-observation December–May reference class is a short sample and briefly explain why it is adequate for a July forecast or supplement it with a longer first-print history."]}

Emit the final JSON object only.
