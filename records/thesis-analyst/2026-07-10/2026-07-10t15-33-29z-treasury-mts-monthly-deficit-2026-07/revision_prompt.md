# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: treasury.mts.monthly_deficit
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-mts-deficit-july-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "treasury.mts.monthly_deficit.july_2026.first_print"
- resolutionDate: "2026-08-17"
- resolutionSource: "U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1"
- resolutionSourceUrl: "https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/"
- resolutionRule: "Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, convert to usd_billions by dividing by 1000, and keep deficits positive and surpluses negative. Do not revise for later MTS revisions or corrected historical tables."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["fiscaldata.treasury.gov"], "expectedReleaseWindow": {"end": "2026-08-17", "start": "2026-08-09"}, "field": "treasury.mts.monthly_deficit", "releasePolicy": "first_print", "sourceSeriesId": "treasury.mts.monthly_deficit", "sourceUrl": "https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/", "table": "U.S. Department of the Treasury, Monthly Treasury Statement (Table 1)", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-ccce2d4ba13735bf7cf54d29cec40a578718bf06407927c523573dd505f8a3f5.json"
- targetContentHash: "ccce2d4ba13735bf7cf54d29cec40a578718bf06407927c523573dd505f8a3f5"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"

# Source hints
- Use U.S. Treasury Monthly Treasury Statement pages, fiscal-year tables, and official release schedules.
- For MTS targets, distinguish monthly amounts, fiscal-year-to-date amounts, receipts, outlays, refunds, and deficit concepts.
- Match the catalog unit, usually billions of nominal dollars.

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
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"US July 2026 monthly budget deficit","question":"U.S. Department of the Treasury Monthly Treasury Statement Table 1, July 2026 monthly Deficit/Surplus (-), first print","unit":"usd_billions","pointEstimate":303,"ciLow":251,"ciHigh":355,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, convert to usd_billions by dividing by 1000, and keep deficits positive and surpluses negative. Do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"July 2025 deficit, USD billions","value":291},{"label":"July 2024 deficit, USD billions","value":243.741},{"label":"July 2023 deficit, USD billions","value":220.782},{"label":"July 2022 deficit, USD billions","value":211.052},{"label":"July 2021 deficit, USD billions","value":302.05}],"drivers":["July’s recurring deficit-month seasonality","Higher baseline outlays, including interest and mandatory programs","Customs-duty receipts partly offsetting higher outlays","Monthly timing and payment-date variation"],"sourceContext":["https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202507.pdf","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202407.pdf","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202306.pdf"],"runAt":"2026-07-10T15:33:49Z","reasoning":[{"kind":"heading","text":"July 2026 Monthly Treasury Statement deficit"},{"kind":"text","text":"The target is the first-print July 2026 monthly flow in Treasury MTS Table 1, “Deficit/Surplus (-),” reported in $ millions and converted to positive USD billions for a deficit. This uses the unsmoothed, non-seasonally-adjusted Table 1 monthly variant; it is not the fiscal-year-to-date balance, receipts, outlays, or a revised vintage."},{"kind":"tool","tool":"official.lookup","call":"Fetched the Treasury MTS Table 1 July 2025 report for the latest same-month official reference observation.","result":"Treasury Table 1 reports July 2025 receipts of $339,293 million, outlays of $630,376 million, and a monthly deficit of $291,083 million (291.083 USD billions)."},{"kind":"tool","tool":"official.lookup","call":"Fetched Treasury MTS Table 1 historical July observations from published statements for the same monthly deficit concept.","result":"Treasury Table 1 reports July deficits of $211,052 million in 2022, $220,782 million in 2023, and $243,741 million in 2024; the July 2021 comparison is $302,050 million."},{"kind":"tool","tool":"official.lookup","call":"Checked the official Treasury MTS release schedule for the registered July 2026 statement date.","result":"The Treasury schedule assigns the July 2026 MTS first print to August 17, 2026; the statement is scheduled for 2:00 p.m., and the target resolves on that initial official print."},{"kind":"text","text":"The reference class is the non-pandemic July Table 1 deficit flow: July has been a deficit month in 68 of 70 fiscal years in Treasury’s historical note. The 2021–25 same-month values provide a more relevant base rate than adjacent months because July cash timing is strongly seasonal."},{"kind":"text","text":"Prior/update/interval: The persistence prior is the 2021–25 July Table 1 sample (302.050, 211.052, 220.782, 243.741, 291.083 USD billions), with mean 253.742; the latest 291.083 level and continuing outlay growth shift that prior upward, while stronger customs receipts partly offset it. For this flow series, sigma = 41.0 USD billions from the values themselves; 1.28*sigma = 52.5 USD billions, so the implied 80% bounds around 303 are 250.5 and 355.5, rounded to 251 and 355."},{"kind":"math","text":"Point forecast = 291.083 latest July level + 20.0 higher baseline outlays − 8.1 additional customs-receipt offset = 302.983, rounded to 303 USD billions. Interval = 303 ± (1.28 × 41.0) = 303 ± 52.5, rounded to [251, 355]."},{"kind":"text","text":"Upside risk: unexpectedly large mandatory-program, interest, or payment-timing outlays would land above the interval. Downside risk: customs receipts or delayed outlays could make the deficit materially smaller; a combination of unusually strong receipts and shifted payments would land below the interval."},{"kind":"forecast","point":303,"ciLow":251,"ciHigh":355}]}

# Reviewer critique
{"summary":"The target contract and forecast fields are coherent, but the material point-estimate update is not supported by cited, quantitative current evidence and the draft does not clearly address a time-series/model prior.","requiredFixes":[{"rubricItem":"model_prior","severity":"warning","summary":"The draft uses a same-month persistence sample but neither applies a time-series model nor explicitly explains why one is unsuitable for this seasonal monthly cash-flow target.","actionRequested":"Add a concise statement ruling out a time-series model (for example, because the five-observation same-month sample is too small and payment timing dominates), or provide a clearly specified model prior and its result."},{"rubricItem":"update","severity":"blocking","summary":"The +20.0 billion outlay adjustment and -8.1 billion customs-receipt offset are asserted without dated, quantitative evidence or a source showing why they apply to July 2026.","actionRequested":"Cite official current evidence for both adjustment components, state the relevant amounts/changes and translation to the July monthly balance, or remove/scale back unsupported adjustments and revise the point estimate accordingly."}],"optionalSuggestions":["State whether the reported 41.0 billion sigma is the sample standard deviation to make the interval method fully reproducible.","Cite the Treasury historical-note source for the 68-of-70 July-deficit claim, or omit that statistic."]}

Emit the final JSON object only.
