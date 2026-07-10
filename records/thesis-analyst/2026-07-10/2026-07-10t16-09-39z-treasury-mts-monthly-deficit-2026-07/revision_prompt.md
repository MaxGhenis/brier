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
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"US MTS July 2026 Deficit","question":"What will the U.S. Department of the Treasury first-print Monthly Treasury Statement Table 1 monthly Deficit/Surplus (-) be for July 2026, converted from $ millions to usd_billions with deficits positive?","unit":"usd_billions","pointEstimate":319.1,"ciLow":240,"ciHigh":430,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, convert to usd_billions by dividing by 1000, and keep deficits positive and surpluses negative. Do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"July 2023 MTS monthly deficit","value":221},{"label":"July 2024 MTS monthly deficit","value":244},{"label":"July 2025 MTS monthly deficit implied from 20% y/y","value":292.8}],"drivers":["July deficit seasonality with large monthly outlays","higher net interest and Social Security cost-of-living spending","tariff receipts offset part but not most of deficit pressure","2025 tax law and debt-service uncertainty widen the interval"],"sourceContext":["https://fiscal.treasury.gov/accounting/monthly-treasury-statement","https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","https://www.marketwatch.com/story/budget-deficit-climbs-10-in-july-government-spends-more-on-interest-than-medicare-military-b5a35b48","https://apnews.com/article/us-budget-deficit-trump-tariffs-treasury-992949ccc115fddbf3838a6213cf2c94"],"runAt":"2026-07-10T16:10:47Z","thresholdLadder":{"thresholds":[200,230,250,270,290,310,330,350,370,400,430,470,520],"cumulativeProbabilities":[0.04,0.08,0.12,0.2,0.32,0.45,0.56,0.66,0.74,0.83,0.9,0.96,0.99]},"reasoning":[{"kind":"heading","text":"Forecast for July 2026 Monthly Treasury Statement deficit"},{"kind":"text","text":"Framing and exact resolver: this is the U.S. Treasury Monthly Treasury Statement Table 1 monthly Deficit/Surplus (-), not fiscal-year-to-date deficit, receipts, outlays, refunds, or a revised historical table. The target is first print for July 2026, in $ millions divided by 1000 into usd_billions, with deficits reported positive."},{"kind":"tool","tool":"official.lookup","call":"Checked Bureau of the Fiscal Service Monthly Treasury Statement page and FiscalData MTS dataset landing path for the official resolver and table family.","result":"Fetched official MTS context: the Fiscal Service page says MTS covers 3 concepts, receipts, outlays, and surplus or deficit; it says data moved to FiscalData on 2025-11-25; page last updated 2026-01-15."},{"kind":"tool","tool":"official.lookup","call":"Checked official release-calendar target date for the July 2026 MTS first print.","result":"Fetched release-date contract for the July 2026 MTS: official release date 2026-08-17, expected release window 2026-08-09 to 2026-08-17, first-print policy 1 print only."},{"kind":"tool","tool":"news.lookup","call":"Fetched recent July monthly deficit reference-class numbers reported from Treasury data.","result":"Fetched July 2024 deficit 244 usd_billions and July 2023 deficit 221 usd_billions; July 2024 was up 10% year over year."},{"kind":"tool","tool":"news.lookup","call":"Fetched July 2025 Treasury-data coverage for tariff and deficit update.","result":"Fetched July 2025 deficit was up 20% year over year versus July 2024, implying 244*1.20 = 292.8 usd_billions; customs revenue was up 273%, or 21 usd_billions, and gross national debt was near 37 trillion dollars."},{"kind":"text","text":"Reference class and base rate: the same-month July deficits immediately before this target were about 221, 244, and 292.8 usd_billions. The base rate is a large July deficit near the high-200s, with a positive trend from debt service and entitlement COLA outlays partly offset by customs receipts."},{"kind":"math","text":"Prior/update/interval: persistence prior is July 2025 implied 292.8 from the same MTS monthly-deficit reference class. Historical sample is July deficits 221, 244, and 292.8, so sigma = 36.7 from the values themselves for this flow series; 1.28*sigma = 47.0. Adjustment components: +15 for underlying outlay and interest growth, +10 for tax-law/revenue softness, +0 to -10 for tariff/customs offset, and +0 to +10 for first-print timing noise, centering near 319. The ladder-implied 80% interval is 240 to 430, average half-width about 95, roughly 2.0 times 1.28*sigma; I widened beyond the raw three-July dispersion because the 2026 policy, tariff, debt-service, and appropriations regime is not well represented by only three same-month observations."},{"kind":"math","text":"Ladder: P(X <= 200) = 0.04; P(X <= 230) = 0.08; P(X <= 250) = 0.12; P(X <= 270) = 0.20; P(X <= 290) = 0.32; P(X <= 310) = 0.45; P(X <= 330) = 0.56; P(X <= 350) = 0.66; P(X <= 370) = 0.74; P(X <= 400) = 0.83; P(X <= 430) = 0.90; P(X <= 470) = 0.96; P(X <= 520) = 0.99. Linear interpolation gives p10 = 240.0, p50 = 319.1, and p90 = 430.0 usd_billions."},{"kind":"text","text":"Counter-considerations: upside risk for a larger deficit would be a weak July receipts print, faster net-interest accrual, or front-loaded benefit and defense outlays; a deficit above 430 would land above the interval. Downside risk would be another customs-revenue surge, delayed outlays, or unexpectedly strong nonwithheld tax receipts; a deficit below 240 would land outside the interval on the low side."},{"kind":"forecast","point":319.1,"ciLow":240,"ciHigh":430}]}

# Reviewer critique
{
  "summary": "The draft is publishable after a small resolver URL cleanup; the prior, update, interval, tails, and JSON forecast fields are mostly coherent.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The draft uses a more specific FiscalData table URL, while the canonical ledger target specifies the dataset landing URL.",
      "actionRequested": "Set resolutionSourceUrl to the canonical ledger URL https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/ or explicitly note that the table-specific URL is only supporting context, not a target change."
    }
  ],
  "optionalSuggestions": [
    "State explicitly that the persistence/ladder approach is the time-series model prior, and that no separate fitted model was used because only same-month July observations were used.",
    "Tighten the prior/update sentence by naming the net adjustment from 292.8 to 319.1 as about +26.3 usd_billions."
  ]
}

Emit the final JSON object only.
