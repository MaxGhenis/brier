# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: sba.disaster.loan_program.post_charge_off_recovery
- period: 2026
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "sba-disaster-loan-program-post-charge-off-recovery-fy2026"
- country: "US"
- targetUnit: "usd"
- dataPointId: "sba.disaster.loan_program.post_charge_off_recovery.2026.first_print"
- resolutionDate: "2028-12-31"
- resolutionDateBasis: "resolve-by-bound"
- expectedReleaseWindow: {"end": "2028-12-31", "start": "2026-10-01"}
- sourceBinding: {"adapter": "sba-loan-program-performance-pdf", "allowedHosts": ["legacy.sba.gov", "www.sba.gov"], "expectedReleaseWindow": {"end": "2028-12-31", "start": "2026-10-01"}, "field": "Disaster / Disaster", "releasePolicy": "first_print", "sourceSeriesId": "sba.disaster.loan_program.post_charge_off_recovery", "sourceUrl": "https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance", "table": "Table 7 - Post-Charge Off Recovery Amount by Program", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-08-b45924a96911924b1bba90d314423a18025113699e0ce7bf9ccc4a5f46cbd063.json"
- targetContentHash: "b45924a96911924b1bba90d314423a18025113699e0ce7bf9ccc4a5f46cbd063"
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
{"slug":"sba-disaster-loan-program-post-charge-off-recovery-fy2026","country":"US","type":"data","title":"SBA disaster post-charge-off recoveries FY2026","question":"What will SBA first print as FY2026 post-charge-off recovery amount for the Disaster / Disaster program in Table 7, dollars, under the Small Business Administration Loan Program Performance release?","unit":"usd","pointEstimate":103333333,"ciLow":63333333,"ciHigh":150000000,"confidence":0.8,"resolutionDate":"2028-12-31","resolutionSource":"U.S. Small Business Administration Loan Program Performance, Table 7 - Post-Charge Off Recovery Amount by Program","resolutionSourceUrl":"https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance","resolutionRule":"Resolve to the first official SBA print for fiscal year 2026 in Table 7 - Post-Charge Off Recovery Amount by Program, row Disaster under the Disaster section, column 2026, in dollars. Use the first printed value only; later data updates or revisions do not change resolution. If the first print is formatted with dollar signs and commas, remove formatting and keep whole-dollar precision.","dataPointId":"sba.disaster.loan_program.post_charge_off_recovery.2026.first_print","historicalContext":[{"label":"FY2023 Disaster / Disaster post-charge-off recovery amount","value":96563005},{"label":"FY2024 Disaster / Disaster post-charge-off recovery amount","value":126510000},{"label":"FY2025 Q3 Disaster / Disaster post-charge-off recovery amount as of 2025-06-30","value":85429990},{"label":"FY2025 Q3 Disaster / Disaster charge-off amount as of 2025-06-30","value":107714599},{"label":"FY2025 Q3 Disaster / Disaster UPB as of 2025-06-30","value":11976493088}],"drivers":["FY2025 Q3 recoveries already reached $85.43 million, implying a full-year run rate near $114 million if receipts continue proportionally","FY2023 and FY2024 recoveries of $96.56 million and $126.51 million show the current old-methodology base rate is elevated versus 2016-2022","FY2025 Q3 charge-offs of $107.71 million are lower than FY2023-FY2024 but still support a substantial recovery pipeline","FY2025 Q3 UPB of $11.98 billion leaves a large recoverable disaster-loan stock","No revised-methodology official print was available, so current official series history is the admissible base rate"],"sourceContext":["https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance","https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip","https://catalog.data.gov/dataset/small-business-administration-sba-loan-program-performance"],"runAt":"2026-08-08T10:36:12Z","thresholdLadder":{"thresholds":[50000000,60000000,70000000,80000000,90000000,100000000,105000000,110000000,120000000,130000000,145000000,155000000,175000000],"cumulativeProbabilities":[0.04,0.08,0.14,0.23,0.34,0.46,0.52,0.59,0.7,0.79,0.88,0.92,0.97]},"reasoning":[{"kind":"heading","text":"SBA Disaster / Disaster FY2026 post-charge-off recovery forecast"},{"kind":"text","text":"Framing and exact resolver: this forecast is tied to the registered resolve-by-bound target. ResolutionDate byte-echoes the Thesis bound 2028-12-31, not an inferred SBA release day. ResolutionSourceUrl byte-echoes the official announcement URL. The resolving field is Table 7 - Post-Charge Off Recovery Amount by Program, Disaster section, Disaster row, FY2026 column, first official print, whole dollars."},{"kind":"text","text":"Official announcement fetch: the registered SBA methodology page was fetched with the required thesis_announcement_fetch tool at https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance and returned HTTP 200 with 37099 response bytes. That page authenticates the SBA Loan Program Performance source identity only; it does not establish the lab-committed release window or bound."},{"kind":"tool","tool":"official.lookup","call":"Fetched the SBA Loan Program Performance landing page and the linked FY25Q3 WebsiteReports zip from legacy.sba.gov, then read WDS_PostChargeOffRecovery_Report_20250630.pdf Table 7.","result":"Fetched Table 7 values for Disaster / Disaster post-charge-off recovery amount: FY2021 $24,299,527; FY2022 $62,832,738; FY2023 $96,563,005; FY2024 $126,510,000; FY2025 as of 06/30/2025 $85,429,990."},{"kind":"tool","tool":"official.lookup","call":"Fetched the same SBA FY25Q3 zip and read WDS_ChargeOffAmount_Report_20250630.pdf Table 5 for matching Disaster / Disaster charge-off amounts.","result":"Fetched Disaster / Disaster charge-off amounts: FY2022 $180,342,594; FY2023 $322,632,623; FY2024 $299,971,326; FY2025 as of 06/30/2025 $107,714,599; COVID EIDL FY2025 as of 06/30/2025 was separately $4,381,745,489 and is not the resolving row."},{"kind":"tool","tool":"official.lookup","call":"Fetched the same SBA FY25Q3 zip and read WDS_UPB_Report_20250630.pdf Table 1 for matching Disaster / Disaster unpaid principal balance context.","result":"Fetched Disaster / Disaster UPB: FY2022 $9,155,822,926; FY2023 $9,379,479,606; FY2024 $9,789,692,235; FY2025 as of 06/30/2025 $11,976,493,088; COVID EIDL FY2025 UPB was separately $267,078,761,650."},{"kind":"text","text":"Base rate / reference class: while no official print under a revised methodology exists, the current official SBA series is the admissible base rate. The most relevant current-vintage history is the Disaster / Disaster row, not COVID EIDL: $96.56 million in FY2023, $126.51 million in FY2024, and $85.43 million through FY2025 Q3. The announced transition is a regime consideration, so I widen the interval rather than fabricating a revision adjustment."},{"kind":"text","text":"Variant check: all anchors use the same variant as the resolver: gross dollar post-charge-off recovery amount, not recovery rate, not charge-off amount, not UPB, and the Disaster / Disaster row excluding the separate COVID EIDL row."},{"kind":"math","text":"Prior/update/interval: persistence prior is the current official Disaster / Disaster reference class centered on FY2023-FY2025Q3, with FY2025Q3 annualized only as a noisy momentum guide ($85,429,990 over three quarters implies about $113.9 million if linear). Level component anchors near $100-$120 million; momentum pulls slightly below FY2024's $126.51 million; charge-off flow of $107.71 million through FY2025Q3 and UPB of $11.98 billion support ongoing recoveries; methodology-transition risk widens both tails. The 80% interval is read from the elicited ladder, not chosen as a round band."},{"kind":"math","text":"Ladder: P(X <= 50000000) = 0.04; P(X <= 60000000) = 0.08; P(X <= 70000000) = 0.14; P(X <= 80000000) = 0.23; P(X <= 90000000) = 0.34; P(X <= 100000000) = 0.46; P(X <= 105000000) = 0.52; P(X <= 110000000) = 0.59; P(X <= 120000000) = 0.70; P(X <= 130000000) = 0.79; P(X <= 145000000) = 0.88; P(X <= 155000000) = 0.92; P(X <= 175000000) = 0.97. Linear interpolation gives 10th percentile at 63333333, median at 103333333, and 90th percentile at 150000000."},{"kind":"text","text":"Counter-considerations: upside risk comes from unusually strong Treasury Cross Servicing receipts or catch-up recoveries from older disaster charge-offs and would land above the interval if FY2026 exceeds $150,000,000. Downside risk comes from a rapid decline in collectible charged-off Disaster balances, timing slippage of recoveries after FY2025 Q3, or methodology changes that allocate less to the Disaster row and would land below the interval if FY2026 is under $63,333,333. A COVID EIDL surge is outside the interval only if it is reclassified into the Disaster / Disaster row, which the current table structure does not do."},{"kind":"forecast","point":103333333,"ciLow":63333333,"ciHigh":150000000}]}

# Reviewer critique
{"summary":"Draft is mostly coherent, but publication should confirm the required structured announcement-fetch event and tighten the interval-method language around volatility versus ladder elicitation.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The reasoning says the required thesis_announcement_fetch tool was used, but the draft only shows an official.lookup entry, not a structured thesis_announcement_fetch.fetch_official_announcement event for the exact officialAnnouncementUrl.","actionRequested":"Ensure the trace contains a successful structured call to thesis_announcement_fetch.fetch_official_announcement with https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance exactly; do not rely on prose or the official.lookup citation as a substitute."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is attributed to the elicited ladder, but the interval-size justification does not quantify realized volatility or explicitly state why the ladder alone is the uncertainty method.","actionRequested":"Add one compact sentence naming the historical sample used for uncertainty and either a realized-volatility check or an explicit statement that the ladder-derived 10th/90th percentiles are the interval method with methodology-transition widening."}],"optionalSuggestions":["Mention whether any newer SBA FY2025 annual or FY2026 interim old-methodology print was checked and excluded, since the run date is 2026-08-08.","Clarify that the point estimate is the ladder median, not a mean, if the schema expects pointEstimate to be interpreted that way."]}

Emit the final JSON object only.
