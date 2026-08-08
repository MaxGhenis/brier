# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: sba.disaster.loan_program.charge_off_amount
- period: 2026
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "sba-disaster-loan-program-charge-off-amount-fy2026"
- country: "US"
- targetUnit: "usd"
- dataPointId: "sba.disaster.loan_program.charge_off_amount.2026.first_print"
- resolutionDate: "2028-12-31"
- resolutionDateBasis: "resolve-by-bound"
- expectedReleaseWindow: {"end": "2028-12-31", "start": "2026-10-01"}
- sourceBinding: {"adapter": "sba-loan-program-performance-pdf", "allowedHosts": ["legacy.sba.gov", "www.sba.gov"], "expectedReleaseWindow": {"end": "2028-12-31", "start": "2026-10-01"}, "field": "Disaster / Disaster", "releasePolicy": "first_print", "sourceSeriesId": "sba.disaster.loan_program.charge_off_amount", "sourceUrl": "https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance", "table": "Table 5 - Charge Off Amount by Program", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-08-3712ecd491933ff0b63b1afda38ca028e9101ec5afca669293cb07ee3ce9984a.json"
- targetContentHash: "3712ecd491933ff0b63b1afda38ca028e9101ec5afca669293cb07ee3ce9984a"
- registrationCommit: "f71dfe6fa8d7fff8803423814942573b7502ac0b"
- registeredAtUtc: "2026-08-08T10:26:30Z"

# Resolve-by-bound target contract (machine checked)
- registeredResolveByBound: "2028-12-31"
- officialAnnouncementUrl: "https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance"
The bound and expected release window are Thesis lab commitments, not timing claims made by the announcement. The announcement authenticates methodology identity only; it does not establish the bound or expected release window. This is an outer bound, not a scheduled release day. resolutionDate must byte-echo the registered resolve-by bound; never infer a more specific day from cadence.
resolutionSourceUrl must byte-echo officialAnnouncementUrl. Call `thesis_announcement_fetch.fetch_official_announcement` with that exact URL. The publisher authenticates the structured draft/final tool event; a reasoning-token claim, search result, same-host page, or prose citation cannot substitute for it.
Base rate during a methodology transition: while NO official print under the announced revised methodology exists — including revised historical or backcast estimates — the CURRENT official series is the admissible base rate: fetch it from its official source, name its vintage explicitly, and state the announced transition as the regime consideration in the sigma step. Do not refuse for lack of the unpublished revised series, and do not fabricate or pre-apply revision adjustments. The moment any revised-methodology official print exists, revised prints are required and old-methodology history stops being admissible.

# Generation ticket
ticket: 2026-08-08-0f89261369bdb0dd9889f661e4ba4c238ad2a3a35fdd90e3a0a8d060c7c5cb3a
nonce: 0f89261369bdb0dd9889f661e4ba4c238ad2a3a35fdd90e3a0a8d060c7c5cb3a

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
- Size the 80% interval by reading it off your elicited threshold ladder, and SHOW the derivation in the 'Ladder:' math step: state the interpolated values literally as '10th percentile at X', 'median at Y', and '90th percentile at Z'. Ground the rung placement in the fetched reference-class history (state which fetched values anchored the rung span in the Prior/update/interval step). Never default to a round hedged band.
- When a release has variants (gross vs smoothed/synthetic, SA vs NSA, flash vs final), the resolution rule must name the variant and every anchor and historical value must come from that same variant; say so once in a text step.
- resolutionSourceUrl must byte-echo the registered official methodology-announcement URL shown in the bounded target context. Use the `thesis_announcement_fetch.fetch_official_announcement` tool on that exact URL; put any separately fetched resolving table or data-artifact URL in sourceContext.
- Name concrete upside, downside, and outside-the-interval scenarios, using the literal phrases "upside risk", "downside risk", and "outside the interval" (or "would land above/below the interval") so the falsification step is machine-checkable.

# Required JSON shape
{
  "slug": "kebab-case-unique-vs-catalog",
  "country": "US|UK|CA|AU|EA|JP",
  "type": "data",
  "title": "Short display title",
  "question": "Exact agency series, period, adjustment, first print",
  "unit": "percent|count|thousands|millions|usd|usd_millions|usd_billions|gbp_billions|ratio|percent_growth",
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
- resolutionDate must byte-echo the registered Thesis lab-committed resolve-by bound shown in the target context. It is an outer bound, not a scheduled release day; the official announcement does not establish it, and you must not infer a more specific date from cadence.
- Do not use existing local catalog point estimates or intervals as forecast evidence. If inspected, treat them only as non-authoritative prior strategy context and keep them out of tool-result evidence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.5.7, prompt a954cfd8c691, tools 024388e49298, promptMode ladder_v2)

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
{"slug":"sba-disaster-loan-program-charge-off-amount-fy2026","country":"US","type":"data","title":"SBA Disaster loan charge-offs FY2026","question":"What will the SBA first print for Table 5, Charge Off Amount by Program, Disaster / Disaster, fiscal year 2026, be in dollars?","unit":"usd","pointEstimate":258333333,"ciLow":85714286,"ciHigh":575000000,"confidence":0.8,"resolutionDate":"2028-12-31","resolutionSource":"Official SBA Loan Program Performance report","resolutionSourceUrl":"https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance","resolutionRule":"Resolve to the first official SBA Loan Program Performance Table 5 - Charge Off Amount by Program print for fiscal year 2026, field Disaster / Disaster, in dollars as printed. Use the first print only; do not replace it with later data-update revisions. The 2028-12-31 resolutionDate is the registered Thesis resolve-by bound, not a scheduled SBA release date.","dataPointId":"sba.disaster.loan_program.charge_off_amount.2026.first_print","historicalContext":[{"label":"FY2022 official current-vintage Disaster charge-off amount","value":180342594},{"label":"FY2023 official current-vintage Disaster charge-off amount","value":322632623},{"label":"FY2024 official current-vintage Disaster charge-off amount","value":299971326},{"label":"FY2025 Q3 partial Disaster charge-off amount","value":107714599}],"drivers":["Recent completed Disaster charge-offs are elevated versus 2016-2021 but below the COVID EIDL distortion in the Disaster subtotal.","FY2025 partial Disaster charge-offs of 107714599 through 2025-06-30 imply full-year risk near but below FY2023-FY2024 if seasonality is ordinary.","Disaster UPB rose to 11976493088 by FY2025 Q3, supporting a higher dollar base than pre-2022 years.","FY2025 Q3 gross approvals of 5266748331 add future exposure, but charge-offs usually lag approvals."],"sourceContext":["https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance","https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip","https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip#WebsiteReports_FY25Q3/WDS_ChargeOffAmount_Report_20250630.pdf","https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip#WebsiteReports_FY25Q3/WDS_ChargeOffRates_Report_20250630.pdf","https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip#WebsiteReports_FY25Q3/WDS_UPB_Report_20250630.pdf"],"runAt":"2026-08-08T10:30:19Z","thresholdLadder":{"thresholds":[50000000,100000000,150000000,200000000,250000000,275000000,300000000,350000000,400000000,500000000,650000000,900000000],"cumulativeProbabilities":[0.05,0.12,0.25,0.38,0.48,0.54,0.6,0.7,0.78,0.87,0.93,0.97]},"reasoning":[{"kind":"heading","text":"SBA Disaster loan charge-off amount FY2026 first print"},{"kind":"text","text":"Framing and exact resolver: the target is SBA Loan Program Performance Table 5 - Charge Off Amount by Program, row Disaster under the Disaster section, fiscal year 2026 first print, unit dollars. I keep resolutionSourceUrl byte-equal to the registered methodology announcement URL and use 2028-12-31 as the Thesis lab resolve-by bound, not as an inferred SBA release date."},{"kind":"tool","tool":"thesis_announcement_fetch.fetch_official_announcement","call":"fetch_official_announcement exact registered URL https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance","result":"Fetched official announcement/landing page with HTTP 200, 37099 response bytes, and response SHA-256 5a77a6bb8e74afdefcffd588fb37cab831ca69385b69d6911b900a99efaede64; the page advertises tables with data through June 30, 2025 and links the FY25Q3 package."},{"kind":"tool","tool":"official.lookup","call":"Downloaded SBA FY25Q3 Loan Program Performance ZIP and extracted WDS_ChargeOffAmount_Report_20250630.pdf Table 5.","result":"Fetched current official vintage as of 2025-06-30: Disaster / Disaster charge-off amounts were 180342594 in FY2022, 322632623 in FY2023, 299971326 in FY2024, and 107714599 for partial FY2025 through 2025-06-30."},{"kind":"tool","tool":"official.lookup","call":"Extracted SBA WDS_ChargeOffRates_Report_20250630.pdf Table 9 for the same Disaster / Disaster variant.","result":"Fetched same-variant charge-off rates: Disaster / Disaster was 1.97% in FY2022, 3.44% in FY2023, 3.06% in FY2024, and 0.90% for partial FY2025 through 2025-06-30."},{"kind":"tool","tool":"official.lookup","call":"Extracted SBA WDS_UPB_Report_20250630.pdf Table 1 and WDS_GrossApproval_Report_20250630.pdf Table 2 for Disaster / Disaster exposure context.","result":"Fetched same-program exposure context: Disaster / Disaster UPB was 9155822926 in FY2022, 9379479606 in FY2023, 9789692235 in FY2024, and 11976493088 for partial FY2025; gross approvals were 2336141093 in FY2022, 3272486099 in FY2023, 1832895854 in FY2024, and 5266748331 for partial FY2025."},{"kind":"text","text":"Reference class/base rate: I use the current official SBA vintage, not FRED or a catalog forecast, because no later revised-methodology print for this registered target exists. The completed FY2016-FY2024 Disaster / Disaster charge-off amounts span 18405594 to 322632623, with the most relevant recent completed values 180342594, 322632623, and 299971326; FY2025 is only a partial value at 107714599 through June 30, 2025."},{"kind":"text","text":"Variant discipline: every historical anchor is the Disaster / Disaster row, excluding COVID EIDL and excluding the Disaster subtotal, because the resolver field is Disaster / Disaster rather than aggregate Disaster programs."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent completed official reference class centered near the FY2022-FY2024 values 180342594, 322632623, and 299971326. Level effect is positive from UPB rising to 11976493088 in partial FY2025; momentum effect is mixed because FY2025 charge-offs are only 107714599 through three quarters while FY2024 was 299971326; one-off/policy effect allows large disaster-cohort charge-offs but excludes COVID EIDL; interval method is threshold-ladder interpolation anchored by the FY2016-FY2024 completed range and the FY2025 partial print. I put the median below FY2023-FY2024 but above FY2022, with 80% bounds covering a low normalization year and a high stress year."},{"kind":"math","text":"Ladder: P(X <= 50000000) = 0.05; P(X <= 100000000) = 0.12; P(X <= 150000000) = 0.25; P(X <= 200000000) = 0.38; P(X <= 250000000) = 0.48; P(X <= 275000000) = 0.54; P(X <= 300000000) = 0.60; P(X <= 350000000) = 0.70; P(X <= 400000000) = 0.78; P(X <= 500000000) = 0.87; P(X <= 650000000) = 0.93; P(X <= 900000000) = 0.97. Linear interpolation gives 10th percentile at 85714286, median at 258333333, and 90th percentile at 575000000."},{"kind":"text","text":"Counter-considerations: upside risk is a delayed charge-off wave from the larger FY2025 Disaster approval and UPB base, which would land above the interval if FY2026 charge-off rates resemble or exceed FY2023-FY2024 while balances keep expanding. Downside risk is continued low observed FY2025 runoff and recoverability improvements, which would land below the interval if FY2026 resembles FY2021 or the early FY2025 pace. An outside the interval outcome is most plausible from a major disaster-loan cohort accounting change or unexpectedly severe liquidation cycle."},{"kind":"forecast","point":258333333,"ciLow":85714286,"ciHigh":575000000}]}

# Reviewer critique
{"summary":"The draft is broadly publishable, with resolver, first-print rule, unit, bound date, prior/update structure, interval, tails, and JSON fields mostly coherent.","requiredFixes":[{"rubricItem":"update","severity":"warning","summary":"The draft relies on the FY2025 Q3 package as the current official vintage for a forecast run dated 2026-08-08, but it does not state whether later SBA Loan Program Performance vintages were checked and unavailable.","actionRequested":"Add one sentence confirming that the registered SBA landing page was checked at run time and that no later admissible official Disaster / Disaster charge-off vintage was available, or update the evidence to the latest official vintage available before the run."},{"rubricItem":"model_prior","severity":"warning","summary":"The persistence prior is clear, but the draft does not explicitly say whether a formal time-series model was considered and ruled out.","actionRequested":"Add a compact note that a formal time-series model was ruled out or downweighted because the completed same-row sample is short, structurally affected by disaster cohorts, and partially observed FY2025 is not a completed annual observation."}],"optionalSuggestions":["In the prior/update/interval step, name the FY2016-FY2024 completed sample size explicitly.","Clarify that the 10th and 90th percentile bounds are 85714286 and 575000000, matching the JSON ciLow and ciHigh."]}

Emit the final JSON object only.
