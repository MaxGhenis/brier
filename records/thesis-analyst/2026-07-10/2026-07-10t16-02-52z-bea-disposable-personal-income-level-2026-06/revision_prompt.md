# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.disposable_personal_income.level
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bea-disposable-personal-income-level-june-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.disposable_personal_income.level.june_2026.first_print"
- resolutionDate: "2026-07-30"
- resolutionSource: "ALFRED DSPI CSV source binding for BEA disposable personal income first print"
- resolutionSourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25"
- resolutionRule: "Resolve through the canonical ledger generic-url binding at the supplied ALFRED DSPI CSV URL, field DSPI, with first_print policy, to the BEA disposable personal income series DSPI / account code A067RC for June 2026, in billions of dollars at a seasonally adjusted annual rate, rounded to one decimal. Ignore later revisions. BEA provenance is the Personal Income and Outlays first release; the supplied ALFRED vintage_date appears to correspond to the prior May 2026 print, so this discrepancy is noted but the forecast remains tied to the retained ledger binding."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "DSPI", "releasePolicy": "first_print", "sourceSeriesId": "DSPI", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25", "table": "Personal Income and Outlays, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-123ce8782db84a3d7daf502c09b752d32f0756b451f512b2661b632666c8caf3.json"
- targetContentHash: "123ce8782db84a3d7daf502c09b752d32f0756b451f512b2661b632666c8caf3"
- registrationCommit: "0d80683b051be25572f40ea4731fa5062af6d211"
- registeredAtUtc: "2026-07-10T12:36:34Z"

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
{"slug":"bea-disposable-personal-income-level-june-2026","country":"US","type":"data","title":"US disposable personal income, June 2026","question":"What will BEA first report for disposable personal income (DSPI / NIPA account A067RC), June 2026, billions of dollars at a seasonally adjusted annual rate?","unit":"usd_billions","pointEstimate":23710.0,"ciLow":23620.0,"ciHigh":23840.0,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"ALFRED DSPI CSV source binding for BEA disposable personal income first print","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25","resolutionRule":"Resolve through the canonical ledger generic-url binding at the supplied ALFRED DSPI CSV URL, field DSPI, with first_print policy, to the BEA disposable personal income series DSPI / account code A067RC for June 2026, in billions of dollars at a seasonally adjusted annual rate, rounded to one decimal. Ignore later revisions. BEA provenance is the Personal Income and Outlays first release; the supplied ALFRED vintage_date appears to correspond to the prior May 2026 print, so this discrepancy is noted but the forecast remains tied to the retained ledger binding.","dataPointId":"bea.disposable_personal_income.level.june_2026.first_print","historicalContext":[{"label":"May 2026 DSPI","value":23651.7},{"label":"Apr 2026 DSPI","value":23486.9},{"label":"Mar 2026 DSPI","value":23510.4},{"label":"May 2025 DSPI","value":22722.6}],"drivers":["May 2026 DSPI was 23651.7 billion, up 164.8 billion from April","May farm proprietors' income jump likely partly reverses or fades in June","Compensation and transfer receipts still provide positive underlying momentum","Personal current taxes rose 16.8 billion in May and may absorb part of June personal income growth","Resolution is the first print only; later BEA revisions are ignored"],"sourceContext":["https://www.bea.gov/news/schedule","https://www.bea.gov/news/2026/personal-income-and-outlays-may-2026","https://fred.stlouisfed.org/series/DSPI","https://fred.stlouisfed.org/data/DSPI","https://fred.stlouisfed.org/release/tables?eid=155443&rid=54","https://alfred.stlouisfed.org/series?seid=DSPI","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25"],"runAt":"2026-07-10T16:03:14Z","thresholdLadder":{"thresholds":[23500.0,23550.0,23600.0,23620.0,23650.0,23680.0,23700.0,23710.0,23730.0,23760.0,23800.0,23840.0,23880.0,23940.0],"cumulativeProbabilities":[0.03,0.06,0.09,0.10,0.18,0.32,0.46,0.50,0.62,0.75,0.86,0.90,0.95,0.98]},"reasoning":[{"kind":"heading","text":"BEA disposable personal income, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: target is BEA disposable personal income, DSPI / NIPA account A067RC, current dollars in billions at a seasonally adjusted annual rate for June 2026. I keep the ledger binding to ALFRED DSPI field DSPI and first_print policy even though the supplied vintage_date=2026-06-25 appears to be the May 2026 release vintage rather than the forthcoming June first print."},{"kind":"tool","tool":"official.lookup","call":"BEA release schedule lookup for Personal Income and Outlays, June 2026","result":"BEA schedule lists Personal Income and Outlays, June 2026 on July 30, 2026 at 8:30 AM; the page also lists GDP (Advance Estimate), 2nd Quarter 2026 on July 30, 2026 at 8:30 AM."},{"kind":"tool","tool":"official.lookup","call":"BEA May 2026 Personal Income and Outlays release lookup","result":"BEA reported May 2026 personal income +181.6 billion, disposable personal income +164.9 billion or +0.7 percent, PCE +156.1 billion or +0.7 percent, personal saving 704.2 billion, and saving rate 3.0 percent."},{"kind":"tool","tool":"fred.lookup","call":"FRED DSPI latest observations and metadata lookup","result":"FRED DSPI shows May 2026 23651.7, Apr 2026 23486.9, Mar 2026 23510.4, Feb 2026 23382.4, Jan 2026 23395.9; units are billions of dollars at a seasonally adjusted annual rate and BEA account code A067RC."},{"kind":"tool","tool":"fred.release_table","call":"FRED release table 2.6 Personal Income and Its Disposition, Monthly for May 2026","result":"Line 27 disposable personal income was 23651.7 in May 2026, 23486.9 in Apr 2026, and 22722.6 in May 2025; line 26 personal current taxes were 3264.7 in May 2026 and 3247.9 in Apr 2026; line 10 farm proprietors' income was 106.9 in May 2026 and 47.3 in Apr 2026."},{"kind":"text","text":"Variant control: all anchors are current-dollar disposable personal income, not real DPI, in billions of dollars at a seasonally adjusted annual rate. The relevant BEA table is Personal Income and Outlays Table 2.6, line 27, and the FRED/ALFRED mirror series is DSPI."},{"kind":"text","text":"The reference class and base rate are monthly DSPI level changes after the recent BEA revisions, using Feb 2024 through May 2026 successive changes. The average change over that window is +77.5 billion, while the latest five observations show one-off volatility: Jan 2026 23395.9, Feb 23382.4, Mar 23510.4, Apr 23486.9, and May 23651.7."},{"kind":"math","text":"Prior/update/interval: persistence prior starts from May DSPI 23651.7 plus the Feb 2024-May 2026 base-rate mean monthly change of +77.5. I adjust down by about 19.2 billion for likely fading of May's farm-proprietor boost and tax drag, giving a point change of +58.3 and point level 23651.7 + 58.3 = 23710.0. For realized dispersion, successive changes from Feb 2024-May 2026 sum to 2170.8 over 28 changes, mean = 77.5, sum of squared deviations = 145189.3 over 27 df, so sigma = sqrt(145189.3/27) = 73.3; the normal 80 percent half-width is about 1.28*sigma = 93.8. The ladder-implied half-width is (23840.0 - 23620.0)/2 = 110.0, or 1.17x the sigma half-width, widened modestly because farm-payment and tax timing can dominate one month of DPI."},{"kind":"math","text":"Ladder: P(X <= 23500.0) = 0.03; P(X <= 23550.0) = 0.06; P(X <= 23600.0) = 0.09; P(X <= 23620.0) = 0.10; P(X <= 23650.0) = 0.18; P(X <= 23680.0) = 0.32; P(X <= 23700.0) = 0.46; P(X <= 23710.0) = 0.50; P(X <= 23730.0) = 0.62; P(X <= 23760.0) = 0.75; P(X <= 23800.0) = 0.86; P(X <= 23840.0) = 0.90; P(X <= 23880.0) = 0.95; P(X <= 23940.0) = 0.98. Linear interpolation gives the 10th percentile 23620.0, median 23710.0, and 90th percentile 23840.0."},{"kind":"text","text":"Counter-considerations: upside risk is another large farm or transfer-payment impulse plus steady wages, which would land above the interval if June DSPI exceeds 23840.0. Downside risk is a reversal of the May farm boost combined with stronger personal tax payments, which would land below the interval if June DSPI is under 23620.0. A broader labor-income shock or special benefit/tax timing issue is the main outside the interval scenario."},{"kind":"forecast","point":23710.0,"ciLow":23620.0,"ciHigh":23840.0}]}

# Reviewer critique
{"summary":"The draft is publication-ready: it matches the ledger target, states a persistence/base-rate prior, gives explicit update components, derives the interval from realized monthly volatility, and keeps the ALFRED first-print binding despite the noted vintage-date discrepancy.","requiredFixes":[],"optionalSuggestions":["Consider changing the driver text from '+164.8 billion' to '+164.9 billion' if matching the BEA release wording is preferred; the underlying level arithmetic is coherent either way.","If space allows, name the Feb 2024-May 2026 sample as 28 monthly changes in the compact prior/update/interval step to make the sample definition even more explicit."]}

Emit the final JSON object only.
