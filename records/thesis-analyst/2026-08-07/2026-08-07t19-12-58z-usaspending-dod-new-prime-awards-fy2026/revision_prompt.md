# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: usaspending.dod.new_prime_awards
- period: FY2026
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-new-prime-awards-fy2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "usaspending.dod.new_prime_awards.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "new_award_count", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.agency.097.awards.new_award_count", "sourceUrl": "https://api.usaspending.gov/api/v2/agency/097/awards/new/count/?fiscal_year={fiscal_year}", "table": "USAspending API v2, agency 097 (DoD) new award count, fiscal year to date", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-07-e6964d48e8a09276874f5990a6155deca11583fde07f94e731a8355b70cb4f47.json"
- targetContentHash: "e6964d48e8a09276874f5990a6155deca11583fde07f94e731a8355b70cb4f47"
- registrationCommit: "a6991688486115b857a52f29c370ed8f884457e3"
- registeredAtUtc: "2026-08-07T17:54:06Z"

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
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- Do not use existing local catalog point estimates or intervals as forecast evidence. If inspected, treat them only as non-authoritative prior strategy context and keep them out of tool-result evidence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.5.7, prompt a954cfd8c691, tools 024388e49298, promptMode fast)


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
{"slug":"us-dod-new-prime-awards-fy2026","country":"US","type":"data","title":"DoD New Prime Awards FY2026","question":"What will USAspending API v2 report as Department of Defense agency 097 new_award_count for fiscal_year=2026, in millions of new prime awards, in the first registered query snapshot on 2026-10-22?","unit":"millions","pointEstimate":1.43,"ciLow":1.18,"ciHigh":1.68,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"USAspending API v2, agency 097 awards new count","resolutionSourceUrl":"https://api.usaspending.gov/api/v2/agency/097/awards/new/count/?fiscal_year=2026","resolutionRule":"On 2026-10-22, query the official USAspending API v2 endpoint /api/v2/agency/097/awards/new/count/?fiscal_year=2026 and read new_award_count for toptier_code 097, agency_type awarding, award_type_codes null. Convert to millions by multiplying by 1e-6 and round to the agency/API integer precision before conversion. Use the first registered query snapshot only; do not apply later revisions or same-day correction grace unless the registered target is changed.","dataPointId":"usaspending.dod.new_prime_awards.fy2026.registered_query_snapshot","historicalContext":[{"label":"FY2021 official API new_award_count, millions","value":1.765},{"label":"FY2022 official API new_award_count, millions","value":1.285},{"label":"FY2023 official API new_award_count, millions","value":1.332},{"label":"FY2024 official API new_award_count, millions","value":1.505},{"label":"FY2025 official API new_award_count, millions","value":1.588},{"label":"FY2026 current official API new_award_count, millions","value":1.068328}],"drivers":["Current FY2026 official API count is 1.068328 million before the fiscal-year closeout snapshot","DoD award data have a published 90-day contract and IDV display delay, making late backfill material","FY2021-FY2025 reference class clusters around roughly 1.3 million to 1.8 million","DLA transaction-heavy award flow dominates count volatility","FY2026 defense budget and operating tempo argue for persistence rather than a regime break"],"sourceContext":["https://api.usaspending.gov/api/v2/agency/097/awards/new/count/?fiscal_year=2026","https://api.usaspending.gov/api/v2/agency/097/awards/","https://api.usaspending.gov/api/v2/agency/097/","https://api.usaspending.gov/api/v2/references/submission_periods/","https://api.usaspending.gov/api/v2/awards/last_updated/"],"runAt":"2026-08-07T19:13:07Z","reasoning":[{"kind":"heading","text":"DoD FY2026 New Prime Awards Forecast"},{"kind":"text","text":"Framing and exact resolver: the target is USAspending API v2 agency 097, field new_award_count, fiscal_year=2026, transformed to millions. The official agency overview identifies toptier_code 097 as Department of Defense and states that DoD contract and IDV data are subject to a 90-day publication delay while other DoD data are not; that matters because the 2026-10-22 registered snapshot may still be a policy-defined snapshot rather than a fully final all-contract vintage."},{"kind":"tool","tool":"official.lookup","call":"GET https://api.usaspending.gov/api/v2/agency/097/awards/new/count/","result":"Fetched official current FY2026 response: toptier_code=097, fiscal_year=2026, agency_type=awarding, award_type_codes=null, new_award_count=1068328, equal to 1.068328 million after the registered factor 1e-6."},{"kind":"tool","tool":"official.lookup","call":"GET https://api.usaspending.gov/api/v2/agency/097/awards/","result":"Fetched official FY2026 agency-awards context: fiscal_year=2026, latest_action_date=2026-07-10, transaction_count=2205913, obligations=245063144206.58 dollars."},{"kind":"tool","tool":"official.lookup","call":"GET https://api.usaspending.gov/api/v2/references/submission_periods/ and GET https://api.usaspending.gov/api/v2/awards/last_updated/","result":"Fetched official schedule/update context: awards last_updated=08/07/2026; FY2026 fiscal month 9 submission_due_date=2026-07-31 and certification_due_date=2026-08-15; FY2025 fiscal month 12 had submission_start_date=2025-10-21, certification_due_date=2025-11-18, and submission_reveal_date=2025-12-06T02:57:27.169269Z. I found no official future FY2026 period-12 exact reveal date in the available endpoint, so I keep the ledger-registered resolve-by-bound date 2026-10-22 and state this discrepancy rather than changing the target."},{"kind":"tool","tool":"official.lookup","call":"USAspending API v2 agency 097 awards new count historical fiscal-year pulls for FY2021-FY2025","result":"Fetched official reference class in raw counts: FY2021=1765000, FY2022=1285000, FY2023=1332000, FY2024=1505000, FY2025=1588000; transformed to millions these are 1.765, 1.285, 1.332, 1.505, and 1.588."},{"kind":"text","text":"Base rate and reference class: the FY2021-FY2025 annual level prior is centered near 1.495 million, with FY2024-FY2025 closer to 1.55 million. The current FY2026 count of 1.068328 million is through a latest_action_date of 2026-07-10, so a simple elapsed-year annualization gives about 1.38 million before allowing for end-year and reporting-window backfill."},{"kind":"math","text":"Prior/update/interval: persistence prior = FY2021-FY2025 official annual new_award_count values in millions [1.765, 1.285, 1.332, 1.505, 1.588], mean = 1.495. Current-release update = 1.068328 / about 0.775 of the fiscal year = 1.379 annualized, plus +0.05 million for late-fiscal-year/backfill flow and no separate policy shock, giving point = 1.43. Interval method = sample dispersion of the five annual flow values; sigma = 0.195 million, so 1.28*sigma = 0.250 million, yielding 1.43 +/- 0.25 = [1.18, 1.68]."},{"kind":"text","text":"Counter-considerations: upside risk is a larger-than-usual DoD/DLA late-year contract and assistance backfill, which would land above the interval if the 2026-10-22 snapshot exceeds 1.68 million. Downside risk is continued missing delayed procurement records or weaker DLA micro-award volume, which would land below the interval if the snapshot remains under 1.18 million. Outside the interval would mainly signal either a release-policy/backfill timing surprise or an actual count-regime break, not ordinary year-to-year noise."},{"kind":"forecast","point":1.43,"ciLow":1.18,"ciHigh":1.68}]}

# Reviewer critique
{"summary":"Draft is publishable: it ties the forecast to the registered USAspending resolver, states a defensible persistence prior, explains the current-count update, and keeps point/interval/JSON fields coherent.","requiredFixes":[],"optionalSuggestions":["Clarify that the 0.775 elapsed-year fraction is based on FY2026 through the latest_action_date of 2026-07-10.","Mention whether the historical FY2021-FY2025 pulls used the same endpoint parameters as the resolver, including agency_type and award_type_codes defaults."]}

Emit the final JSON object only.
