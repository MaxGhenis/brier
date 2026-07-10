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
{"slug":"us-real-avg-hourly-earnings-mom-july-2026","country":"US","type":"data","title":"US real hourly earnings, July 2026","question":"What will the first BLS print show for the July 2026 seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls?","unit":"percent","pointEstimate":0.1,"ciLow":-0.4,"ciHigh":0.6,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Real Earnings Table A-1","resolutionSourceUrl":"https://www.bls.gov/news.release/realer.t01.htm","resolutionRule":"Resolve to the first BLS Real Earnings Table A-1 value for July 2026, seasonally adjusted over-the-month percent change in real average hourly earnings for all employees on private nonfarm payrolls, as first printed on the official release page; use the one-decimal percent value shown by BLS and do not revise for later updates.","dataPointId":"bls.real_earnings.avg_hourly_mom.2026-07.first_print","historicalContext":[{"label":"January 2026 first print","value":0.3},{"label":"February 2026 first print","value":0.2},{"label":"March 2026 first print","value":-0.6},{"label":"April 2026 first print","value":-0.5},{"label":"May 2026 first print","value":-0.1}],"drivers":["Nominal hourly-pay growth near 0.3 percent","Monthly CPI-U inflation determines the real-wage subtraction","Recent first prints have unusually wide dispersion","One-decimal BLS publication rounding"],"sourceContext":["https://www.bls.gov/schedule/2026/08_sched.htm","https://www.bls.gov/news.release/archives/realer_02132026.htm","https://www.bls.gov/news.release/archives/realer_03112026.htm","https://www.bls.gov/news.release/archives/realer_04102026.htm","https://www.bls.gov/news.release/archives/realer_05122026.htm","https://www.bls.gov/news.release/archives/realer_06102026.htm","https://www.bls.gov/news.release/archives/empsit_07022026.htm"],"runAt":"2026-07-10T17:13:17Z","reasoning":[{"kind":"heading","text":"July 2026 real average hourly earnings forecast"},{"kind":"text","text":"The target is the first-print, one-decimal value in BLS Real Earnings Table A-1 for all employees on private nonfarm payrolls: seasonally adjusted real average hourly earnings over the month. Table A-1 uses CPI-U to deflate nominal earnings; no later revision replaces the first print."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS August 2026 release calendar.","result":"The official calendar schedules July 2026 Real Earnings for August 12, 2026 at 8:30 a.m. ET, alongside July CPI."},{"kind":"tool","tool":"official.lookup","call":"Read archived BLS Real Earnings Table A-1 releases for January through March 2026.","result":"First-printed monthly real average hourly earnings changes were January 0.3%, February 0.2%, and March -0.6%; the corresponding first-print CPI-U changes were 0.2%, 0.3%, and 0.9%."},{"kind":"tool","tool":"official.lookup","call":"Read archived BLS Real Earnings Table A-1 releases for April and May 2026.","result":"First-printed real hourly earnings changes were April -0.5% and May -0.1%; nominal hourly earnings changed 0.2% and 0.3%, while CPI-U changed 0.6% and 0.5%."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS June 2026 Employment Situation earnings data.","result":"June average hourly earnings for all private employees rose 0.3% to $37.64, following a May level of $37.51; the 12-month increase was 3.5%."},{"kind":"text","text":"The outside-view base rate/reference class is the six available first-print monthly observations from December 2025 through May 2026: 0.0%, 0.3%, 0.2%, -0.6%, -0.5%, and -0.1%. Their mean is -0.12% and median is -0.05%. Recent negative prints largely reflect temporarily elevated CPI-U rather than collapsing nominal wages."},{"kind":"text","text":"Mechanisms: the level of nominal hourly earnings remains high and its momentum is about 0.3% monthly; CPI-U is the principal subtraction and recent 0.5%-0.9% readings created the negative one-offs. A normalization of monthly inflation toward roughly 0.2%-0.3%, combined with wage growth around 0.3%, shifts the July real change toward zero or slightly positive."},{"kind":"math","text":"Prior/update/interval: Start from a persistence/reference-class prior near the six-print median of -0.05%. Using the change-series values themselves [0.0, 0.3, 0.2, -0.6, -0.5, -0.1], the sample standard deviation is sigma = 0.37 percentage point, so 1.28*sigma = 0.47 point. Update by about +0.15 point for persistent 0.3% nominal wage growth and anticipated CPI normalization, yielding a 0.1% center. The ladder implies an 80% interval of -0.4% to 0.6%, a 0.50-point half-width, close to the 0.47-point empirical width."},{"kind":"math","text":"Ladder: P(X <= -0.5) = 0.06; P(X <= -0.4) = 0.10; P(X <= -0.3) = 0.18; P(X <= -0.2) = 0.27; P(X <= -0.1) = 0.38; P(X <= 0.0) = 0.46; P(X <= 0.1) = 0.50; P(X <= 0.2) = 0.61; P(X <= 0.3) = 0.71; P(X <= 0.4) = 0.79; P(X <= 0.5) = 0.85; P(X <= 0.6) = 0.90; P(X <= 0.7) = 0.95. Linear interpolation places the 10th, 50th, and 90th percentiles exactly at -0.4%, 0.1%, and 0.6%, respectively."},{"kind":"text","text":"Upside risk comes from July CPI-U near zero while nominal hourly pay rises at least 0.4%; that could land above the interval. Downside risk comes from another energy- or tariff-related CPI jump near 0.8% with weak wage growth; that would land below the interval. Composition-driven hourly-pay volatility is an additional outside-the-interval mechanism."},{"kind":"forecast","point":0.1,"ciLow":-0.4,"ciHigh":0.6}],"thresholdLadder":{"thresholds":[-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7],"cumulativeProbabilities":[0.06,0.1,0.18,0.27,0.38,0.46,0.5,0.61,0.71,0.79,0.85,0.9,0.95]}}

# Reviewer critique
{"summary":"The target contract and forecast fields are coherent, but the prior sample, model treatment, and +0.15-point update need clearer support.","requiredFixes":[{"rubricItem":"base_rate","severity":"warning","summary":"The six-observation prior includes December 2025 at 0.0%, but that observation is absent from historicalContext and lacks a cited archived release.","actionRequested":"Cite and list the December first print, or recompute the prior and volatility from the five documented observations."},{"rubricItem":"model_prior","severity":"warning","summary":"No distinct time-series/model prior is used or explicitly ruled out; the reference-class median is only labeled a persistence prior.","actionRequested":"State why a more formal time-series model is unsuitable for this short, noisy sample, or provide its estimate separately."},{"rubricItem":"update","severity":"warning","summary":"The +0.15-point adjustment relies mainly on anticipated CPI normalization and nominal wage persistence, while the real-earnings base rate already embeds typical wage growth and no current July CPI evidence is available.","actionRequested":"Decompose the adjustment without double-counting embedded nominal-wage behavior and justify its magnitude using cited pre-forecast evidence; otherwise shrink it toward the prior."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact calculation depends on the undocumented December observation and combines two update mechanisms into one judgmental increment.","actionRequested":"Use a fully cited historical sample and itemize the numerical contribution of each adjustment component."}],"optionalSuggestions":["Clarify that nominal wage growth minus CPI-U inflation is an approximation to the BLS index calculation.","Add the December archived BLS URL if retaining the six-print sample."]}

Emit the final JSON object only.
