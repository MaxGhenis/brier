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
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"US MTS July 2026 Deficit","question":"U.S. Department of the Treasury Monthly Treasury Statement Table 1 monthly deficit/surplus for July 2026, first official print, nominal dollars, deficits positive and surpluses negative.","unit":"usd_billions","pointEstimate":308.1,"ciLow":262.4,"ciHigh":353.8,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, convert to usd_billions by dividing by 1000, and keep deficits positive and surpluses negative. Do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"July 2022 first-print deficit","value":211.052},{"label":"July 2023 first-print deficit","value":220.782},{"label":"July 2024 first-print deficit","value":243.741},{"label":"July 2025 first-print deficit","value":291.143}],"drivers":["July has recently been a large deficit month","2025 customs-duty receipts lifted revenue but outlays still jumped","health, Social Security, defense, and net interest outlays remain high","FY2026 budget-estimate deficit is near FY2025 run-rate, limiting trend extrapolation"],"sourceContext":["https://fiscal.treasury.gov/accounting/monthly-treasury-statement","https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","https://fiscal.treasury.gov/system/files/files/reports-statements/mts/mts0725.pdf","https://fiscal.treasury.gov/system/files/files/reports-statements/mts/mts0724.pdf","https://fiscal.treasury.gov/system/files/files/reports-statements/mts/mts0723.pdf"],"runAt":"2026-07-10T05:27:41Z","reasoning":[{"kind":"heading","text":"US MTS July 2026 Monthly Deficit Forecast"},{"kind":"text","text":"Framing and exact resolver: this is the first-print U.S. Treasury Monthly Treasury Statement Table 1 monthly deficit/surplus for July 2026, not fiscal-year-to-date deficit, receipts, outlays, refunds, or a revised vintage. The table is in $ millions; the forecast is in usd_billions with deficits positive."},{"kind":"tool","tool":"official.lookup","call":"Opened the Bureau of the Fiscal Service Monthly Treasury Statement page and prior-issue archive.","result":"The official MTS page says the MTS is normally released on the 8th workday of the month following the reporting month; the page was last updated January 15, 2026, and Fiscal Service says the data moved to FiscalData on November 25, 2025."},{"kind":"text","text":"Resolution-date note: applying the official 8th-workday policy to July 2026 points to August 12, 2026, while the registered ledger window runs through 2026-08-17. I keep the target tied to the ledger resolution date of 2026-08-17 and would still resolve on the first official July 2026 print if it appears earlier."},{"kind":"tool","tool":"official.lookup","call":"Read MTS July 2025 PDF, Table 1 and Table 3.","result":"For July 2025, Table 1 reported receipts of 338,492 million, outlays of 629,635 million, and a monthly deficit of 291,143 million; Table 3 reported customs duties of 27,670 million and total receipts of 338,492 million."},{"kind":"tool","tool":"official.lookup","call":"Read MTS July 2024 and July 2023 PDFs, Table 1.","result":"For July 2024, Table 1 reported receipts of 330,377 million, outlays of 574,119 million, and a deficit of 243,741 million; for July 2023, receipts were 276,161 million, outlays were 496,943 million, and the deficit was 220,782 million."},{"kind":"tool","tool":"official.lookup","call":"Read MTS July 2023 PDF comparable FY2022 row and MTS July 2025 budget-estimate columns.","result":"For July 2022, Table 1 reported receipts of 269,331 million, outlays of 480,383 million, and a deficit of 211,052 million; July 2025 Table 2 showed next-fiscal-year 2026 budget estimates of receipts 6,011,381 million, outlays 7,612,734 million, and deficit 1,601,353 million."},{"kind":"text","text":"Reference class/base rate: the same-variant July first-print monthly deficits for 2022-2025 were 211.052, 220.782, 243.741, and 291.143 usd_billions. The four-year mean is 241.6795, but the last two observations and higher nominal outlay level argue for anchoring closer to 2025 than to the full mean."},{"kind":"math","text":"Prior/update/interval: persistence prior = July 2025 first-print deficit of 291.143; historical sample = July 2022-2025 first-print Table 1 monthly deficits of 211.052, 220.782, 243.741, 291.143; adjustment components = +18.961 from 40% of the 2024-to-2025 increase, -10.000 for continuing high customs/tariff receipts, +8.000 for higher benefit, health, defense, and interest outlays; point = 291.143 + 18.961 - 10.000 + 8.000 = 308.104. Interval method = sample standard deviation of the July deficit values themselves because this is a monthly flow; sigma = 35.710, half-width = 1.28*sigma = 45.709, so 80% interval = 308.104 +/- 45.709 = 262.395 to 353.813."},{"kind":"text","text":"Upside risk: the deficit would land above the interval if July outlays repeat another unusually large health, education, or interest timing surge while tariff receipts fade. Downside risk: it would land below the interval if customs receipts remain near or above the July 2025 surge and benefit or agency payments shift out of July. Outside the interval on either side would most likely come from payment-calendar timing rather than a smooth macro trend."},{"kind":"forecast","point":308.1,"ciLow":262.4,"ciHigh":353.8}]}

# Reviewer critique
{
  "summary": "The draft is publishable with no blocking issues; it clearly preserves the registered target while noting the release-date discrepancy.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Add the July 2022 source URL or note that the 2022 value came from the comparable prior-year row in the July 2023 MTS.",
    "Briefly justify why the interval uses cross-sectional July levels rather than recent July year-over-year changes or forecast-error volatility."
  ]
}

Emit the final JSON object only.
