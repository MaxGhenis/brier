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
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"US July 2026 monthly deficit","question":"U.S. Treasury Monthly Treasury Statement Table 1 monthly Deficit/Surplus (-) for July 2026, first print, not seasonally adjusted","unit":"usd_billions","pointEstimate":275,"ciLow":200,"ciHigh":365,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, convert to usd_billions by dividing by 1000, and keep deficits positive and surpluses negative. Do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"July 2021 Table 1 deficit, USD billions","value":302.05},{"label":"July 2023 Table 1 deficit, USD billions","value":220.785},{"label":"July 2024 Table 1 deficit, USD billions","value":243.741},{"label":"July 2025 Table 1 deficit, USD billions","value":291.134},{"label":"May 2026 Treasury MTS deficit, USD billions","value":292.648}],"drivers":["July's recurring high-outlay, lower-receipt seasonal pattern","Higher interest and mandatory-program outlays","Customs-receipt strength partially offsets outlay growth","Timing of benefit and other agency payments"],"sourceContext":["https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202506.pdf","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202407.pdf","https://fiscal.treasury.gov/files/reports-statements/mts/mts0921.pdf","https://alfred.stlouisfed.org/release?rd=2026-06-10&rid=363"],"runAt":"2026-07-10T22:03:06Z","thresholdLadder":{"thresholds":[160,190,210,230,250,265,275,290,310,335,365,400,450],"cumulativeProbabilities":[0.03,0.07,0.13,0.22,0.32,0.42,0.5,0.61,0.72,0.82,0.9,0.95,0.98]},"reasoning":[{"kind":"heading","text":"July 2026 U.S. Monthly Treasury Statement deficit"},{"kind":"text","text":"The resolver is the first official July 2026 MTS Table 1 print: monthly Deficit/Surplus (-), in $ millions divided by 1,000, with a deficit recorded as positive. This is the unadjusted monthly Table 1 variant, not fiscal-year-to-date receipts, outlays, financing, or a revised historical value. Treasury's published release schedule was checked for the August 17, 2026 release date."},{"kind":"tool","tool":"official.lookup","call":"Fetched the Treasury Monthly Treasury Statement Table 1 report for June 2025 and its historical monthly Table 1 rows.","result":"Treasury Table 1 reports July 2024 receipts of $330,377 million, outlays of $574,119 million, and a deficit of $243,741 million; June 2025 was a $27,010 million surplus."},{"kind":"tool","tool":"official.lookup","call":"Fetched Treasury's July 2024 MTS Table 1 report to confirm the same monthly deficit series and units.","result":"The official Table 1 July 2024 row is $330,377 million receipts minus $574,119 million outlays, yielding a $243,741 million deficit; Table 1 is explicitly reported in $ millions."},{"kind":"tool","tool":"official.lookup","call":"Fetched the June 10, 2026 MTS release record, which identifies Treasury as the source and reports the latest released monthly budget balance.","result":"The Treasury-sourced release record reports May 2026 federal surplus-or-deficit of -$292,648.46208374 million, receipts of $335,512.18322742 million, and outlays of $628,160.64531116 million."},{"kind":"text","text":"Reference class/base rate: comparable July Table 1 deficits were $302.050 billion in 2021, $220.785 billion in 2023, $243.741 billion in 2024, and $291.134 billion in 2025. The base rate is therefore a roughly $244 billion July deficit, with a wide seasonal and payment-timing spread."},{"kind":"text","text":"Prior/update/interval: I use an equal-weight July-only persistence prior from the fetched Table 1 reference class ($220.785 billion, $243.741 billion, $291.134 billion, and $302.050 billion), centered near $267 billion. I add modest upward pressure from the latest $292.648 billion May deficit and persistent high outlays, then subtract a partial customs-receipt offset; the resulting median is $275 billion. The interval is read from the elicited ladder, whose span is anchored by the $220.785 billion and $302.050 billion July observations rather than a round default band."},{"kind":"math","text":"Ladder: P(X <= 160) = 0.03; P(X <= 190) = 0.07; P(X <= 210) = 0.13; P(X <= 230) = 0.22; P(X <= 250) = 0.32; P(X <= 265) = 0.42; P(X <= 275) = 0.50; P(X <= 290) = 0.61; P(X <= 310) = 0.72; P(X <= 335) = 0.82; P(X <= 365) = 0.90; P(X <= 400) = 0.95; P(X <= 450) = 0.98. Linear interpolation gives 10th percentile at 200, median at 275, and 90th percentile at 365, all in usd_billions."},{"kind":"text","text":"Upside risk is that unusually large benefit, interest, or agency-payment timing lifts the deficit above $365 billion. Downside risk is stronger customs or income-tax receipts and delayed outlays, reducing it below $200 billion. A major payment-timing shift or an exceptional receipt would land outside the interval."},{"kind":"forecast","point":275,"ciLow":200,"ciHigh":365}]}

# Reviewer critique
{"summary":"The forecast is target-coherent and has a clear July-only persistence prior, but its evidence and interval justification need strengthening before publication.","requiredFixes":[{"rubricItem":"update","severity":"blocking","summary":"The move from the roughly $267B July-only prior to $275B is supported mainly by generic drivers and a non-comparable May 2026 balance; the cited latest-release record is an ALFRED mirror rather than an identified official Treasury release.","actionRequested":"Use an official Treasury source for current receipts/outlays evidence and quantify how each July-relevant update changes the prior, or remove the unsupported update and retain the persistence prior."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is derived from the elicited ladder, but the stated historical anchor range does not itself explain the wider $200B–$365B bounds or their probability mass.","actionRequested":"State an explicit interval method using the July historical sample and identified payment-timing uncertainty, including why the tails extend beyond the observed reference range."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The historical reference class omits July 2022 without explanation, making the claimed equal-weight July-only sample potentially incomplete.","actionRequested":"Include the July 2022 Table 1 observation or explicitly document why it is excluded from the prior."}],"optionalSuggestions":["Replace the ALFRED source-context link with the direct official Treasury June 2026 MTS report or release page.","Add the official release-schedule URL or citation supporting the August 17 first-print date."]}

Emit the final JSON object only.
