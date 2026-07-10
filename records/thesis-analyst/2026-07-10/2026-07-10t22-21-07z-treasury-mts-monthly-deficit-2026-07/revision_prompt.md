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
{"slug":"us-mts-deficit-july-2026-fast","country":"US","type":"data","title":"U.S. July 2026 Monthly Treasury Deficit","question":"What will the U.S. Treasury Monthly Treasury Statement Table 1 report for the July 2026 monthly deficit, in nominal dollars, on the first print?","unit":"usd_billions","pointEstimate":296,"ciLow":213,"ciHigh":380,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, divide by 1000, keep deficits positive and surpluses negative, and do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"May 2026","value":292.648},{"label":"April 2026","value":-215.024},{"label":"March 2026","value":164.1},{"label":"February 2026","value":307.501},{"label":"January 2026","value":94.615},{"label":"July 2025","value":291},{"label":"July 2024","value":243.741},{"label":"July 2023","value":220.782}],"drivers":["seasonally high July outlays","rising interest and entitlement spending","tariff and other receipt growth","monthly cash-flow timing"],"sourceContext":["https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202506.pdf","https://fred.stlouisfed.org/series/MTSDS133FMS","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202501.pdf"],"runAt":"2026-07-10T00:00:00Z","thresholdLadder":{"thresholds":[200,220,240,260,280,300,320,340,360,380,400],"cumulativeProbabilities":[0.06,0.12,0.22,0.32,0.42,0.52,0.62,0.72,0.82,0.9,0.95]},"reasoning":[{"kind":"heading","text":"U.S. July 2026 Monthly Treasury Deficit"},{"kind":"text","text":"The target is the first official July 2026 Monthly Treasury Statement print, Table 1, monthly Deficit/Surplus (-), expressed in usd_billions with deficits positive. The canonical ledger contract gives resolutionDate 2026-08-17; Treasury describes MTS as a summary of receipts, outlays, and surplus or deficit, and the release schedule places the first-print window in August."},{"kind":"tool","tool":"official.lookup","call":"Fetched official Treasury MTS Table 1 reference-class observations from published reports.","result":"The official Treasury January 2025 MTS fetched July 2024 at $243,741 million, June 2024 at $70,965 million, May 2024 at $347,131 million, and July 2023 at $220,782 million; under the target convention these are deficits of 243.741, 70.965, 347.131, and 220.782 usd_billions."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest official-source-linked MTS series observations through the June 10, 2026 release.","result":"The fetched MTS series reported January 2026 surplus/deficit of -$94,615.162 million, February of -$307,501.433 million, March of -$164,100.339 million, April of $215,024.140 million, and May of -$292,648.462 million; converting to positive-deficit convention gives 94.615, 307.501, 164.100, -215.024, and 292.648 usd_billions."},{"kind":"tool","tool":"official.lookup","call":"Fetched the prior July first-print reference from the Treasury MTS release coverage.","result":"July 2025 was fetched at approximately $291 billion deficit, while July 2024 was fetched at $243.741 billion and July 2023 at $220.782 billion; July deficits therefore cluster near $220-$300 billion but can move with cash-flow timing."},{"kind":"text","text":"The series is not seasonally adjusted and is the gross monthly deficit, not fiscal-year-to-date deficit, receipts, outlays, or a revised historical value. July is typically a deficit month because outlays remain large while receipts are less concentrated than in April and June; interest, Social Security, Medicare, and calendar timing create substantial month-to-month variation."},{"kind":"text","text":"The base rate is the fetched July reference class of 220.782, 243.741, and approximately 291 usd_billions, supplemented by the latest five-month path of 94.615, 307.501, 164.100, -215.024, and 292.648. The central estimate is near the upper part of the July reference class because recent deficits remain large and interest and entitlement outlays are persistent."},{"kind":"text","text":"Prior/update/interval: A persistence prior from the July 2023-2025 reference class centers near 252 usd_billions; the update components are elevated interest and entitlement outlays, continued receipt growth, and one-off calendar timing. I use a threshold-ladder interval rather than a parametric distribution; fetched July values 220.782, 243.741, and approximately 291 anchor the rung span from 200 to 400."},{"kind":"math","text":"Ladder: P(X <= 200) = 0.06; P(X <= 220) = 0.12; P(X <= 240) = 0.22; P(X <= 260) = 0.32; P(X <= 280) = 0.42; P(X <= 300) = 0.52; P(X <= 320) = 0.62; P(X <= 340) = 0.72; P(X <= 360) = 0.82; P(X <= 380) = 0.90; P(X <= 400) = 0.95. Linear interpolation gives 10th percentile at 213.3, rounded to 213; median at 296; 90th percentile at 380."},{"kind":"text","text":"Downside risk is a receipt-heavy month or delayed outlays producing a deficit below 213 billion. Upside risk is faster outlay growth, especially interest or benefit payments, producing a deficit above 380 billion; an unusual timing shift or major fiscal transaction would land outside the interval."},{"kind":"forecast","point":296,"ciLow":213,"ciHigh":380}]}

# Reviewer critique
{"summary":"The draft is largely coherent and tied to the canonical target, but it needs stronger justification and calibration for the update and interval.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 213–380 interval is presented as a threshold-ladder result, but the ladder probabilities and width are not tied to realized July volatility or an explicit uncertainty calibration.","actionRequested":"Explain how the ladder probabilities and bounds were calibrated from the July reference class, broader monthly volatility, or another explicit uncertainty method."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The prior/update step names the July 2023–2025 sample and qualitative drivers, but does not quantify how those drivers move the 252 billion prior to 296 billion.","actionRequested":"State the numerical adjustment, or clearly explain why the evidence supports the approximately 44 billion upward movement."},{"rubricItem":"tails","severity":"warning","summary":"Tail scenarios are directionally relevant but generic and do not identify concrete July 2026 cash-flow mechanisms or their expected effect on the target.","actionRequested":"Tie each tail to a specific target-relevant mechanism, such as receipt timing, benefit-payment timing, or interest outlays, and indicate whether it pushes the deficit above or below the interval."}],"optionalSuggestions":["Clarify the exact official provenance of the approximately 291 billion July 2025 observation.","Keep the FRED citation explicitly labeled as a history mirror rather than a resolution source."]}

Emit the final JSON object only.
