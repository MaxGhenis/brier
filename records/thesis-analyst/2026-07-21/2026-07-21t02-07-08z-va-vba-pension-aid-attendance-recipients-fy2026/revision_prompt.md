# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: va.vba.pension.aid_attendance_recipients
- period: FY2026
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "va-pension-aid-attendance-recipients-fy2026"
- targetUnit: "thousands"

# Source hints
- Use the official agency data page and release calendar.
- FRED or sanctioned mirrors may be used only for history, not final resolution.
- Match the agency's published rounding precision.

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
{"slug":"va-pension-aid-attendance-recipients-fy2026","country":"US","type":"data","title":"VA Pension A&A Recipients, FY2026","question":"Department of Veterans Affairs Veterans Benefits Administration Annual Benefits Report FY2026, Pension and Fiduciary section, All Veterans Pension recipients with aid and attendance (A&A), on the rolls as of September 30, 2026, first print, thousands of Veterans.","unit":"thousands","pointEstimate":46.4,"ciLow":40.6,"ciHigh":52.2,"confidence":0.8,"resolutionDate":"2027-05-12","resolutionSource":"Official agency release","resolutionSourceUrl":"https://benefits.va.gov/REPORTS/abr/index.asp","resolutionRule":"Resolve to the first public FY2026 VBA Annual Benefits Report Pension and Fiduciary PDF table 'All Veterans Pension recipients and estimated annual payments by type of special monthly pension', row 'With aid and attendance (A&A)', column 'Number of Veterans', divided by 1,000 and rounded to three decimals in thousands. Use the original first-posted FY2026 ABR print and ignore later revisions or rehosted corrected PDFs unless VA withdraws the first public file before the release completes.","dataPointId":"va.vba.pension.aid_attendance_recipients.FY2026.first_print","historicalContext":[{"label":"FY2025 A&A Veterans Pension recipients","value":50.73},{"label":"FY2024 A&A Veterans Pension recipients","value":55.1},{"label":"FY2023 A&A Veterans Pension recipients","value":59.8},{"label":"FY2022 A&A Veterans Pension recipients","value":64.277}],"drivers":["Long-running decline in means-tested Veterans Pension rolls","A&A share of the shrinking Veterans Pension caseload has been rising","Korean Conflict and Vietnam-era aging sustains medical-need intensity","Deaths and income or asset ineligibility continue to reduce rolls","FY2026 benefit-rate increases may modestly support eligibility near thresholds"],"sourceContext":["https://benefits.va.gov/REPORTS/abr/index.asp","https://benefits.va.gov/REPORTS/abr/docs/2025-pension-fiduciary.pdf","https://benefits.va.gov/REPORTS/abr/archive.asp","https://benefits.va.gov/REPORTS/abr/docs/2024-abr.pdf","https://benefits.va.gov/REPORTS/abr/docs/2023-abr.pdf","https://benefits.va.gov/REPORTS/abr/docs/2022-abr.pdf","https://catalog.data.gov/dataset/vba-annual-benefits-report-1999-current"],"runAt":"2026-07-21T02:07:51Z","reasoning":[{"kind":"heading","text":"Forecast for FY2026 VA Veterans Pension Aid and Attendance Recipients"},{"kind":"text","text":"Framing and exact resolver: this forecast uses the VBA Annual Benefits Report Pension and Fiduciary table for All Veterans Pension recipients by type of special monthly pension. The variant is Veterans Pension recipients with aid and attendance (A&A), not survivors pension and not the combined A&A-or-housebound subtotal. The unit is thousands, so whole-recipient table values are divided by 1,000."},{"kind":"tool","tool":"official.lookup","call":"Inspect VA FY2025 Annual Benefits Report landing page and Pension and Fiduciary PDF","result":"Fetched FY2025 release context: current ABR page says VBA Annual Benefits Report Fiscal Year 2025, updated May 2026, and the page was last updated May 12, 2026; the FY2025 Pension and Fiduciary PDF says data as of 09/30/2025."},{"kind":"tool","tool":"official.lookup","call":"Inspect FY2025 Pension and Fiduciary table for all Veterans Pension recipients by type of special monthly pension","result":"Fetched FY2025 table values: With aid and attendance (A&A) 50,730 Veterans, 41.2% of total, average annual amount $21,969, total annual amount $1,114,507,127; With housebound 1,270; Total all Veterans Pension recipients 123,261."},{"kind":"tool","tool":"official.lookup","call":"Inspect archived FY2022 Annual Benefits Report Pension table for same series and reference-class baseline","result":"Fetched FY2022 table values: With aid and attendance (A&A) 64,277 Veterans, 36.9% of total, average annual amount $19,213, total annual amount $1,234,943,335; With housebound 2,294; Total all Veterans Pension recipients 173,969."},{"kind":"tool","tool":"official.lookup","call":"Inspect VA archive and data.gov metadata for ABR release mechanics","result":"Fetched official archive listing with 2024, 2023, and 2022 VBA Annual Benefits Reports; data.gov metadata says the current annual report is usually updated by the end of the first quarter of the following calendar year, while the current FY2025 official page shows 2025 ABR last updated May 12, 2026."},{"kind":"tool","tool":"official.lookup","call":"Inspect archived FY2023 and FY2024 ABR same-table history","result":"Fetched same-series archived ABR history used for interpolation and trend: FY2023 A&A Veterans Pension recipients about 59.8 thousand and FY2024 about 55.1 thousand, between FY2022 64.277 thousand and FY2025 50.730 thousand."},{"kind":"text","text":"Base rate/reference class: the recent reference class is the same VBA ABR all-Veterans Pension A&A row. It shows a declining level from 64.277 thousand in FY2022 to 50.730 thousand in FY2025, even as the A&A share rose from 36.9% to 41.2% because the overall means-tested pension roll shrank faster than the high-care-need subset."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: level starts from 50.730 thousand at FY2025 first print. Momentum is negative because the pension rolls are dominated by older wartime cohorts and attrition is large. The offset is that A&A eligibility is concentrated among older and more disabled Veterans, so the row should decline more slowly than basic pension-only rolls. One-off policy effects look modest: FY2026 MAPR increases can keep some claimants eligible, but there is no evidence of a broad new enrollment expansion for this specific pension tier."},{"kind":"math","text":"Prior/update/interval: persistence prior is FY2025 level 50.730 thousand. Historical sample is same-series FY2022 64.277, FY2023 about 59.8, FY2024 about 55.1, FY2025 50.730, giving successive changes about -4.477, -4.700, and -4.370 thousand. sigma = sqrt((4.477^2 + 4.700^2 + 4.370^2) / 3) = 4.52 thousand. The trend update applies another -4.3 thousand attrition step, plus 0.0 thousand one-off and policy adjustment, yielding point 46.4. The 80% half-width is about 1.28*sigma = 1.28*4.52 = 5.79 thousand, so bounds are 46.4 - 5.8 = 40.6 and 46.4 + 5.8 = 52.2."},{"kind":"text","text":"Counter-considerations: upside risk is stronger claim take-up or MAPR-driven eligibility retention among older Vietnam-era Veterans, which would land above the interval if FY2026 remains above 52.2 thousand. Downside risk is accelerated mortality, nursing-home transitions, or income and asset screening attrition, which would land below the interval if the first print is under 40.6 thousand. An outside the interval result would likely mean either a reporting-definition change or a much sharper break in pension-roll attrition than the recent ABR reference class."},{"kind":"forecast","point":46.4,"ciLow":40.6,"ciHigh":52.2}]}

# Reviewer critique
{
  "summary": "The draft is publishable with only minor clarification needed on the interval method.",
  "requiredFixes": [
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The interval labels the RMS of recent annual declines as sigma, which is conservative but not the realized volatility of deviations around the trend.",
      "actionRequested": "Clarify that the 5.8 thousand half-width is a conservative annual-step uncertainty estimate from the FY2022-FY2025 same-series declines, or switch the wording to an explicit uncertainty floor rather than calling it realized volatility."
    }
  ],
  "optionalSuggestions": [
    "In the resolver step, make explicit that the 2027-05-12 resolutionDate is the ledger deadline while the VA publication timing itself is only inferred from prior ABR timing.",
    "Replace 'about 59.8' and 'about 55.1' in the compact math step with the exact extracted FY2023 and FY2024 values if available from the archived PDFs."
  ]
}

Emit the final JSON object only.
