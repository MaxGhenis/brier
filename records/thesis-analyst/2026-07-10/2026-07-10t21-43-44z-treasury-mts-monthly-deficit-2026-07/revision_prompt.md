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
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"U.S. July 2026 monthly deficit","question":"What will the U.S. Treasury Monthly Treasury Statement Table 1 report as the July 2026 monthly deficit, in nominal USD billions, on its first print?","unit":"usd_billions","pointEstimate":305.455,"ciLow":210,"ciHigh":400,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, divide by 1000 to obtain usd_billions, and report deficits as positive and surpluses as negative. Do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"July 2023 deficit","value":220.782},{"label":"July 2024 deficit","value":243.741},{"label":"July 2025 deficit","value":291.143},{"label":"May 2026 deficit","value":292.648}],"drivers":["July deficits rose from $220.782B in 2023 to $291.143B in 2025","FY2026 spending and interest remain elevated","July tax receipts are seasonally weaker than April receipts","Payment timing can shift tens of billions between adjacent months"],"sourceContext":["https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202501.pdf","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202505.pdf","https://fiscaldata.treasury.gov/release-calendar/"],"runAt":"2026-07-10T21:44:12Z","thresholdLadder":{"thresholds":[170,200,220,240,260,280,300,320,340,360,380,400,430],"cumulativeProbabilities":[0.05,0.08,0.12,0.18,0.26,0.36,0.47,0.58,0.68,0.77,0.84,0.9,0.95]},"reasoning":[{"kind":"heading","text":"July 2026 Monthly Treasury Statement deficit forecast"},{"kind":"text","text":"The target is the first-print July 2026 monthly Deficit/Surplus (-) in MTS Table 1, not the fiscal-year-to-date balance. Table 1 is denominated in $ millions; I divide by 1000 and reverse the table's sign convention so deficits are positive. Later revisions are excluded."},{"kind":"tool","tool":"official.lookup","call":"Read Treasury MTS Table 1 for the July reference class.","result":"Official Table 1 values were July 2023 receipts $276.161B, outlays $496.943B, deficit $220.782B; July 2024 receipts $330.377B, outlays $574.119B, deficit $243.741B; and July 2025 receipts $338.492B, outlays $629.635B, deficit $291.143B."},{"kind":"tool","tool":"official.lookup","call":"Read the May 2026 MTS Table 1 for current-fiscal-year momentum.","result":"FY2026 Table 1 showed May receipts $335.512B, outlays $628.161B, and a $292.648B monthly deficit; FY2026 year-to-date through May was receipts $3,655.648B and outlays $4,901.851B."},{"kind":"tool","tool":"official.calendar","call":"Check the Treasury Fiscal Data release calendar for the July 2026 MTS.","result":"The official release calendar listed the July 2026 Monthly Treasury Statement for 2026-08-17; the dataset notes that MTS publication is normally on the 8th workday after the reporting month."},{"kind":"text","text":"The reference class base rate is the three most recent same-month first prints: $220.782B, $243.741B, and $291.143B. Their upward progression and the $292.648B May 2026 deficit place the central July 2026 mass near $300B rather than near the broader all-month average."},{"kind":"text","text":"Prior/update/interval: I use a recency-weighted same-month persistence prior over the fetched July 2023-2025 sample, anchored by $220.782B and $291.143B. I update upward for higher FY2026 nominal outlays and debt-service pressure, temper that adjustment because receipts have also risen, and allow wide payment-calendar and policy uncertainty. The interval is read from the elicited empirical threshold ladder, yielding final implied 80% bounds of $210.000B to $400.000B."},{"kind":"math","text":"Ladder: P(X <= 170) = 0.05; P(X <= 200) = 0.08; P(X <= 220) = 0.12; P(X <= 240) = 0.18; P(X <= 260) = 0.26; P(X <= 280) = 0.36; P(X <= 300) = 0.47; P(X <= 320) = 0.58; P(X <= 340) = 0.68; P(X <= 360) = 0.77; P(X <= 380) = 0.84; P(X <= 400) = 0.90; P(X <= 430) = 0.95. Linear interpolation gives the 10th percentile at 210.000, median at 305.455, and 90th percentile at 400.000 usd_billions."},{"kind":"text","text":"Upside risk to the deficit comes from accelerated benefit or defense payments, weaker individual-income-tax receipts, larger refunds, or unusually high interest outlays; a combination could land above the interval. Downside risk comes from strong withheld taxes, customs receipts, delayed payments, or unusually large offsetting receipts; a major timing shift could land below the interval."},{"kind":"forecast","point":305.455,"ciLow":210,"ciHigh":400}]}

# Reviewer critique
{"summary":"The forecast is resolver-safe and internally coherent, but its prior and inside-view updates are not quantified and no time-series/model prior is used or explicitly ruled out.","requiredFixes":[{"rubricItem":"model_prior","severity":"blocking","summary":"No time-series or model-based prior is presented, and the draft does not explain why one was ruled out.","actionRequested":"Add a simple documented model prior using the July history, such as persistence, trend, or recency weighting, or explicitly state why the limited sample makes such a model unsuitable."},{"rubricItem":"prior_update_interval","severity":"blocking","summary":"The compact step does not give a numeric prior, recency weights, or quantified adjustment components, so the derivation of the 305.455 point estimate cannot be audited.","actionRequested":"State the numeric pre-update prior, the July 2023–2025 sample and weighting formula, each upward or downward adjustment in USD billions, and how these produce the final central estimate; retain the ladder-derived 10th and 90th percentiles."},{"rubricItem":"update","severity":"warning","summary":"Elevated May 2026 outlays and debt-service pressure are asserted to move the forecast upward, but their incremental relevance to July and the size of the movement are not demonstrated.","actionRequested":"Quantify the movement from the same-month prior and tie each adjustment to cited current evidence; otherwise leave the central estimate at the prior."},{"rubricItem":"interval","severity":"warning","summary":"The interval is mechanically derived from the ladder, but the ladder probabilities are not grounded in observed July forecast errors or an explicit uncertainty calculation and are incorrectly called empirical.","actionRequested":"Describe the ladder as elicited and justify its width using observed same-month variability, timing-shift magnitudes, or another explicit uncertainty estimate."}],"optionalSuggestions":["Cite the exact official MTS reports or rows supporting each historical July value.","Give approximate numeric thresholds for the above-$400B and below-$210B tail scenarios."]}

Emit the final JSON object only.
