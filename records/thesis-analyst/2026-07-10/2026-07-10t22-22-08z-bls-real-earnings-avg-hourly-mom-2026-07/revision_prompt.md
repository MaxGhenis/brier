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
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US Real Average Hourly Earnings MoM — July 2026","question":"What will the first-print July 2026 seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls be in BLS Real Earnings Table A-1?","unit":"percent","pointEstimate":-0.1,"ciLow":-0.7,"ciHigh":0.5,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"2026-01","value":0.3},{"label":"2026-02","value":0.1},{"label":"2026-03","value":-0.6},{"label":"2026-04","value":-0.5},{"label":"2026-05","value":-0.1}],"drivers":["moderating nominal wage growth","CPI-U deflator volatility","recent negative real-earnings momentum","seasonal-adjustment noise"],"sourceContext":["https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/news.release/archives/realer_04102026.htm","https://www.bls.gov/schedule/2026/08_sched_list.htm","https://www.bls.gov/schedule/2026/07_sched_list.htm"],"runAt":"2026-07-10T22:22:19Z","thresholdLadder":{"thresholds":[-1,-0.7,-0.5,-0.3,-0.1,0,0.1,0.3,0.5,0.7,1],"cumulativeProbabilities":[0.05,0.1,0.2,0.32,0.46,0.56,0.68,0.8,0.89,0.95,0.98]},"reasoning":[{"kind":"heading","text":"US real average hourly earnings, July 2026 first print"},{"kind":"text","text":"The target is the BLS CES series bls.real_earnings.avg_hourly_mom, specifically Table A-1 for all employees on private nonfarm payrolls, seasonally adjusted, and resolved at the first official July 2026 print without later revisions."},{"kind":"tool","tool":"official.lookup","call":"BLS official release calendar lookup for the target release date","result":"The BLS August 2026 release schedule lists Real Earnings for July 2026 at 08:30 a.m. ET on August 12, 2026, verifying the resolution date rather than inferring it from cadence."},{"kind":"tool","tool":"official.lookup","call":"BLS Real Earnings Table A-1 recent-series lookup","result":"The official Table A-1 page reports the recent seasonally adjusted over-the-month real average hourly earnings changes as March 2026 -0.6 percent, April 2026 -0.5 percent, and May 2026 -0.1 percent."},{"kind":"tool","tool":"official.lookup","call":"BLS archived Real Earnings history lookup","result":"The official March 2026 archive reports January 2026 at 0.3 percent and February 2026 at 0.1 percent for the same Table A-1 seasonally adjusted series."},{"kind":"text","text":"The base rate/reference class is the five fetched 2026 observations: 0.3, 0.1, -0.6, -0.5, and -0.1 percent. Their median is -0.1 percent, with four of five values between -0.6 and 0.3."},{"kind":"text","text":"The exact variant is the gross all-employee, private nonfarm payrolls, seasonally adjusted real average hourly earnings series in BLS Table A-1, deflated with CPI-U; no production-and-nonsupervisory, NSA, weekly-earnings, or revised-vintage values are mixed in."},{"kind":"text","text":"Prior/update/interval: A persistence prior centered near the five-observation median of -0.1 percent is adjusted modestly for recent negative momentum, while CPI-U and nominal hourly-pay surprises create two-sided monthly noise; the fetched reference class anchors the rung span from -0.6 to 0.3 percent, producing an elicited 80% interval from -0.7 to 0.5 percent."},{"kind":"math","text":"Ladder: P(X <= -1) = 0.05; P(X <= -0.7) = 0.1; P(X <= -0.5) = 0.2; P(X <= -0.3) = 0.32; P(X <= -0.1) = 0.46; P(X <= 0) = 0.56; P(X <= 0.1) = 0.68; P(X <= 0.3) = 0.8; P(X <= 0.5) = 0.89; P(X <= 0.7) = 0.95; P(X <= 1) = 0.98. Linear interpolation gives 10th percentile at -0.7, median at -0.06, and 90th percentile at 0.53; rounding to BLS one-decimal print precision gives 10th percentile at -0.7, median at -0.1, and 90th percentile at 0.5."},{"kind":"text","text":"Downside risk is a renewed CPI acceleration with nominal pay below trend, which would land below the interval; upside risk is softer CPI alongside firm nominal wage growth, which would land above the interval. An unusually large seasonal-adjustment change or release-month data shock would be outside the interval."},{"kind":"forecast","point":-0.1,"ciLow":-0.7,"ciHigh":0.5}]}

# Reviewer critique
{"summary":"The forecast is publication-ready in resolver, target coherence, traceability, and ladder structure, with minor gaps in explicit model-prior framing and evidence for the stated update.","requiredFixes":[{"rubricItem":"model_prior","severity":"warning","summary":"The persistence prior is stated, but no explicit time-series/model prior or ruled-out alternative is identified.","actionRequested":"Name the persistence or other time-series prior explicitly as the model prior and briefly state why no richer model is used."},{"rubricItem":"update","severity":"warning","summary":"The draft mentions moderating nominal wages and CPI-U volatility without citing current observations, while the point remains at the prior median.","actionRequested":"Either state explicitly that current evidence does not warrant movement from the prior, or cite dated nominal-wage/CPI evidence and quantify its adjustment."}],"optionalSuggestions":["Clarify that the -0.7 to 0.5 bounds are the interpolated 10th and 90th percentiles from the threshold ladder, rather than implying they are directly realized-volatility bounds."]}

Emit the final JSON object only.
