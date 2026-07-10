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
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US real average hourly earnings, July 2026","question":"What will the U.S. Bureau of Labor Statistics first print in Real Earnings Table A-1 for the July 2026 seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls?","unit":"percent","pointEstimate":0.0,"ciLow":-0.7,"ciHigh":0.7,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"May 2026","value":-0.1},{"label":"April 2026","value":-0.5},{"label":"March 2026","value":-0.6}],"drivers":["nominal average-hourly-earnings growth relative to CPI-U","volatile month-to-month CPI-U inflation","seasonally adjusted private-nonfarm all-employee composition"],"sourceContext":["https://www.bls.gov/news.release/realer.t01.htm","https://www.bls.gov/schedule/2026/home.htm"],"runAt":"2026-07-10T22:04:40Z","thresholdLadder":{"thresholds":[-1.0,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4],"cumulativeProbabilities":[0.03,0.06,0.13,0.23,0.37,0.53,0.68,0.79,0.87,0.93,0.96,0.98,0.99]},"reasoning":[{"kind":"heading","text":"July 2026 real average hourly earnings, first print"},{"kind":"text","text":"The resolver is the BLS Real Earnings Table A-1, seasonally adjusted all employees on private nonfarm payrolls: the real average hourly earnings over-the-month percent-change row. This is the same variant for every historical anchor; Table A-1 deflates earnings using CPI-U."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS Real Earnings Table A-1 for the latest available official release and read the seasonally adjusted real average hourly earnings over-the-month row.","result":"The May 2026 first-print table reports -0.1 percent for real average hourly earnings; April 2026 is -0.5 percent and March 2026 is -0.6 percent. The same table reports May CPI-U at +0.5 percent and nominal average hourly earnings at +0.3 percent."},{"kind":"tool","tool":"official.lookup","call":"Fetched the BLS 2026 release calendar to verify the scheduled release for the target month.","result":"The official calendar lists Real Earnings for July 2026 on Wednesday, August 12, 2026 at 08:30 AM Eastern; it also lists Real Earnings for June 2026 on July 14, 2026 at 08:30 AM Eastern."},{"kind":"tool","tool":"official.lookup","call":"Fetched the current Table A-1 levels and related monthly changes as a consistency check on the real-wage arithmetic.","result":"For May 2026, Table A-1 reports real average hourly earnings of $11.24, CPI-U of 333.979, nominal average hourly earnings of $37.53, and a -0.1 percent monthly real hourly-earnings change."},{"kind":"text","text":"The reference class/base rate is monthly seasonally adjusted Table A-1 real hourly-earnings growth. The three latest fetched prints are all negative (-0.6, -0.5, and -0.1), but the May shortfall narrowed because nominal hourly earnings rose 0.3 percent while CPI-U rose 0.5 percent; mean reversion toward zero is therefore more likely than a fourth similarly large decline."},{"kind":"math","text":"Prior/update/interval: I use a persistence-with-mean-reversion prior centered near 0.0 percent, anchored by the fetched March -0.6, April -0.5, and May -0.1 Table A-1 values. The adjustment components are nominal wage growth minus CPI-U inflation, with composition and seasonal noise retained as residual uncertainty. I elicited the interval from the threshold ladder rather than a parametric sigma: its span is anchored on those fetched negative prints and allows symmetric positive inflation/wage surprises. Ladder: P(X <= -1.0) = 0.03; P(X <= -0.8) = 0.06; P(X <= -0.6) = 0.13; P(X <= -0.4) = 0.23; P(X <= -0.2) = 0.37; P(X <= 0.0) = 0.53; P(X <= 0.2) = 0.68; P(X <= 0.4) = 0.79; P(X <= 0.6) = 0.87; P(X <= 0.8) = 0.93; P(X <= 1.0) = 0.96; P(X <= 1.2) = 0.98; P(X <= 1.4) = 0.99. Linear interpolation gives 10th percentile at -0.7, median at 0.0, and 90th percentile at 0.7; rounded to BLS's one-decimal print precision, the point is 0.0 percent and the 80% interval is -0.7 to 0.7 percent."},{"kind":"text","text":"upside risk: a soft or negative July CPI-U print combined with firm nominal earnings could lift real hourly earnings above 0.7 percent. downside risk: a renewed CPI-U jump while nominal earnings growth slows could push the print below -0.7 percent. A larger energy-price or composition shock would land outside the interval."},{"kind":"forecast","point":0.0,"ciLow":-0.7,"ciHigh":0.7}]}

# Reviewer critique
{"summary":"The resolver and forecast fields are coherent, but the prior and interval justification need stronger, correctly ordered support.","requiredFixes":[{"rubricItem":"base_rate","severity":"blocking","summary":"The base-rate prior appears after the latest-release evidence, so the update sequence is reversed.","actionRequested":"State the reference class and pre-evidence prior before presenting the March–May observations or other current evidence."},{"rubricItem":"model_prior","severity":"warning","summary":"“Persistence-with-mean-reversion” is named but not estimated or supported beyond three recent prints.","actionRequested":"Use a longer historical Table A-1 sample to summarize a time-series prior (for example mean, dispersion, and persistence), or explicitly rule out a fitted model and justify the alternative prior."},{"rubricItem":"interval","severity":"blocking","summary":"The 80% interval is elicited from the ladder but its width is only said to be “anchored” on three negative observations; it lacks a quantified realized-volatility or uncertainty basis.","actionRequested":"Tie the ladder width to a stated historical dispersion/sample or quantify the wage-growth, CPI-U, composition, and seasonal uncertainty components that support the -0.7 to 0.7 bounds."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact step names the components and bounds, but does not distinguish the historical prior sample from the current-evidence update in a reproducible way.","actionRequested":"State the historical sample window and prior statistic, then specify how the March–May pattern and current wage/CPI evidence move that prior to 0.0."}],"optionalSuggestions":["Name the exact Table A-1 historical sample window used for the prior and volatility check.","Clarify whether the stated May CPI-U and nominal earnings changes are seasonally adjusted in the same form used for the target."]}

Emit the final JSON object only.
