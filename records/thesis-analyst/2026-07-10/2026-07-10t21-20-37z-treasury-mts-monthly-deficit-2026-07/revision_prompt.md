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
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"U.S. MTS July 2026 Deficit","question":"What will the U.S. Department of the Treasury first report as the Monthly Treasury Statement Table 1 monthly Deficit/Surplus (-) for July 2026, converted to billions of dollars with deficits positive?","unit":"usd_billions","pointEstimate":270.0,"ciLow":201.1,"ciHigh":358.0,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, convert to usd_billions by dividing by 1000, round the forecast cell to one decimal billion dollars, and keep deficits positive and surpluses negative. Do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"july_2025_deficit","value":291.0},{"label":"july_2024_deficit","value":244.0},{"label":"july_2023_deficit","value":220.8},{"label":"july_2022_deficit","value":211.1},{"label":"fy2025_deficit","value":1775.0}],"drivers":["July is usually a deficit month after June tax-payment strength fades","recent July deficits clustered around roughly $210 billion to $291 billion","higher customs duties raise receipts relative to pre-2025 history","interest, Social Security, Medicare, defense, and enacted tax-policy costs keep outlays high","first-print monthly cash timing can move the print by tens of billions"],"sourceContext":["https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","https://www.fiscal.treasury.gov/reports-statements/mts/","https://apnews.com/article/992949ccc115fddbf3838a6213cf2c94","https://www.cbo.gov/"],"runAt":"2026-07-10T21:21:54Z","thresholdLadder":{"thresholds":[170,190,210,230,250,270,290,310,330,350,370,400],"cumulativeProbabilities":[0.04,0.075,0.12,0.20,0.34,0.50,0.64,0.74,0.82,0.88,0.93,0.97]},"reasoning":[{"kind":"heading","text":"U.S. Monthly Treasury Statement July 2026 Deficit Forecast"},{"kind":"text","text":"Framing: the resolver is the first-print U.S. Treasury Monthly Treasury Statement Table 1 monthly Deficit/Surplus (-) for July 2026, in the same monthly, not fiscal-year-to-date, nominal cash-budget variant. The official release calendar identifies the July 2026 MTS release date as 2026-08-17, and the target uses the first print with no later revisions."},{"kind":"tool","tool":"official.lookup","call":"Treasury Monthly Treasury Statement Table 1 history for July monthly Deficit/Surplus (-), converted from $ millions to usd_billions and sign-flipped so deficits are positive","result":"Fetched July deficits: 2025 = 291.0, 2024 = 244.0, 2023 = 220.8, 2022 = 211.1, 2021 = 302.1 usd_billions."},{"kind":"tool","tool":"official.lookup","call":"Treasury/AP public report cross-check for July 2025 MTS monthly receipts, outlays, and deficit","result":"Fetched July 2025 monthly deficit = 291.0 usd_billions, receipts about 338.0 usd_billions, outlays about 629.0 usd_billions, and reported year-over-year deficit increase about 20%."},{"kind":"tool","tool":"official.lookup","call":"Treasury final Monthly Treasury Statement fiscal-year totals used only as fiscal backdrop, not as the monthly target","result":"Fetched FY2025 final totals: receipts = 5235.0 usd_billions, outlays = 7010.0 usd_billions, deficit = 1775.0 usd_billions; FY2024 deficit reference = 1833.0 usd_billions."},{"kind":"text","text":"Reference class/base rate: recent official July MTS prints put the normal range near the low-$200 billions through low-$300 billions, with 2025 at 291.0 and 2021 at 302.1 showing that a July deficit around or above $300 billion is plausible without a crisis, while 2022-2024 anchor the lower-to-middle band."},{"kind":"text","text":"Prior/update/interval: I start from a persistence prior centered between the recent July sample median and the latest July print, using the fetched July 2022-2025 values of 211.1, 220.8, 244.0, and 291.0 plus the 2021 high of 302.1 to anchor the rung span. I adjust downward from 2025 for stronger tariff/customs receipts, then upward for higher interest and mandatory outlays and tax-policy deficit pressure. The interval method is the threshold ladder below, yielding final implied 80% bounds of 201.1 to 358.0."},{"kind":"text","text":"Upside risk for the deficit is a July outlay bulge from interest, defense, Medicare, or benefit timing that pushes the print toward the 330-370 range. Downside risk is customs receipts and delayed outlays holding the deficit near 200-230. A major calendar shift or unusually large one-off payment would land outside the interval, above 358.0 if outlays bunch heavily or below 201.1 if receipts are unusually strong and payments slip."},{"kind":"math","text":"Ladder: P(X <= 170) = 0.04; P(X <= 190) = 0.075; P(X <= 210) = 0.12; P(X <= 230) = 0.20; P(X <= 250) = 0.34; P(X <= 270) = 0.50; P(X <= 290) = 0.64; P(X <= 310) = 0.74; P(X <= 330) = 0.82; P(X <= 350) = 0.88; P(X <= 370) = 0.93; P(X <= 400) = 0.97. Linear interpolation gives 10th percentile at 201.1, median at 270.0, and 90th percentile at 358.0."},{"kind":"math","text":"Published values are derived from the ladder only: pointEstimate = median = 270.0 usd_billions; ciLow = 10th percentile = 201.1 usd_billions; ciHigh = 90th percentile = 358.0 usd_billions."},{"kind":"forecast","point":270.0,"ciLow":201.1,"ciHigh":358.0}]}

# Reviewer critique
{
  "summary": "Draft is mostly publication-ready, but it should align the resolver text exactly with the ledger and make the interval/update support more explicit.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The draft resolutionRule adds 'round the forecast cell to one decimal billion dollars,' which is not part of the canonical resolver and could confuse the observation rule.",
      "actionRequested": "Replace the draft resolutionRule with the ledger resolver text exactly, keeping forecast rounding separate from resolution."
    },
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "The move from the latest July print of 291.0 to a 270.0 median is directionally explained, but the tariff/customs, interest, mandatory outlay, and tax-policy adjustments are not quantified or tied to specific evidence.",
      "actionRequested": "Add a compact sentence giving approximate adjustment sizes or explaining why the net update is about -21 billion from July 2025."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The interval is derived from the ladder, but the draft does not explicitly connect the 80% width to realized July volatility or a named uncertainty judgment.",
      "actionRequested": "State either the realized dispersion of recent July prints or an explicit uncertainty rationale for why an 80% interval of 201.1 to 358.0 is appropriate."
    }
  ],
  "optionalSuggestions": [
    "Add the 2021 July value to historicalContext since it is used in reasoning.",
    "Make sourceContext more specific by naming the CBO item or report used for tax-policy/outlay pressure."
  ]
}

Emit the final JSON object only.
