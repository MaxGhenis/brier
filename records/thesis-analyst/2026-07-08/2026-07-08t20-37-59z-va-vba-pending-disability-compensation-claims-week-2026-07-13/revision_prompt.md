# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: va.vba.pending_disability_compensation_claims
- period: week_2026-07-13
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "va-pending-disability-claims-2026-07-13"
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
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
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
{"slug":"va-pending-disability-claims-2026-07-13","country":"US","type":"data","title":"VA pending disability claims, July 13 2026","question":"VA Veterans Benefits Administration Monday Morning Workload Report claims inventory, pending rating bundle disability compensation and pension claims, week of 2026-07-13, first print, not seasonally adjusted","unit":"thousands","pointEstimate":603.7,"ciLow":597.8,"ciHigh":609.6,"confidence":0.8,"resolutionDate":"2026-07-13","resolutionSource":"Official VA Veterans Benefits Administration Detailed Claims Data / Monday Morning Workload Report","resolutionSourceUrl":"https://www.benefits.va.gov/REPORTS/detailed_claims_data.asp","resolutionRule":"Resolve to the first official VA VBA Monday Morning Workload Report claims inventory value for the 07/13/2026 report date, using the agency's published whole-claim first print converted to thousands and rounded to three decimals; ignore later revisions or display refreshes after the first posted report.","dataPointId":"va.vba.mmwr.claims_inventory.week_2026-07-13.first_print","historicalContext":[{"label":"2026-06-15 report claims inventory","value":594.08},{"label":"2026-06-22 report claims inventory","value":596.291},{"label":"2026-06-29 report claims inventory","value":599.02},{"label":"2026-07-06 report claims inventory","value":601.63}],"drivers":["latest official level was 601.630 thousand pending claims","recent weekly momentum was upward by roughly 2.5 thousand claims","normal-week processing after the Independence Day week should limit further accumulation","holiday timing and intake volatility widen the one-week interval"],"sourceContext":["https://www.benefits.va.gov/REPORTS/detailed_claims_data.asp","https://www.benefits.va.gov/reports/mmwr_va_claims_online.asp"],"runAt":"2026-07-08T20:38:05Z","reasoning":[{"kind":"heading","text":"VA VBA pending disability compensation claims forecast"},{"kind":"text","text":"Framing and exact resolver: this is the VA VBA Monday Morning Workload Report claims inventory series, the rating-bundle disability compensation and pension claims that normally require development and a VBA claims processor decision; I use the not seasonally adjusted first print in whole claims and convert to thousands."},{"kind":"tool","tool":"official.lookup","call":"Opened VA Detailed Claims Data page for the current status cards and series definition.","result":"Fetched current status card values: 601,630 Pending Claims, 69,193 Rating-Related Backlog Claims, 94.26% 3-Month Issue-Level Accuracy, 94.07% 12-Month Issue-Level Accuracy."},{"kind":"tool","tool":"official.lookup","call":"Checked the 2026 Monday Morning Workload Reports table on the VA Detailed Claims Data page for the release schedule.","result":"Fetched report schedule entries including 07/06/2026 linked as the latest posted report, 07/13/2026 listed as the next target report date, 07/20/2026, and 07/27/2026; this verifies resolutionDate 2026-07-13 from the official VA page rather than inferring from cadence."},{"kind":"tool","tool":"official.lookup","call":"Used the official VA weekly report series as the recent reference class for the same claims inventory variant.","result":"Fetched recent claims inventory values in thousands for the same VA MMWR claims inventory variant: 594.080 on 2026-06-15, 596.291 on 2026-06-22, 599.020 on 2026-06-29, and 601.630 on 2026-07-06."},{"kind":"text","text":"Reference class and base rate: for a one-week-ahead level forecast, persistence plus the recent same-series weekly change is the base rate. The latest level is 601.630 thousand and the last three week-to-week changes were +2.211, +2.729, and +2.610 thousand, so the outside-view central tendency is a continued modest increase rather than a flat print."},{"kind":"math","text":"Prior/update/interval: persistence prior = 601.630 thousand from the 2026-07-06 first print; historical sample = recent VA MMWR claims inventory weekly changes from 2026-06-15 through 2026-07-06 plus a broader recent-release volatility allowance; adjustment components = +2.1 thousand level/momentum, +0.0 thousand policy mechanism because no new adjudication rule was identified, and -0.0 thousand one-off holiday rebound offset because the target week is mostly normal operations; interval method = one-week successive-change dispersion with sigma = 4.6 thousand, so 80% half-width = 1.28*4.6 = 5.9 thousand; final implied bounds are 603.7 - 5.9 = 597.8 and 603.7 + 5.9 = 609.6 thousand."},{"kind":"text","text":"Level, momentum, one-off, and mechanism effects: the level anchor is 601.630 thousand; momentum adds about 2 thousand because the latest official sequence is rising; the July 4 timing could have lifted the latest inventory but does not by itself imply a large reversal; absent a new VA processing surge or intake shock, weekly movement should stay in a single-digit-thousand range."},{"kind":"text","text":"Counter-considerations: upside risk is a claims-intake burst or slower completions that would land above the interval, especially if pending claims exceed 609.6 thousand; downside risk is a catch-up completion week or unusually low intake that would land below the interval, especially below 597.8 thousand; outside the interval would require a weekly change of roughly less than -3.8 thousand or greater than +8.0 thousand from the 601.630 thousand latest level."},{"kind":"forecast","point":603.7,"ciLow":597.8,"ciHigh":609.6}]}

# Reviewer critique
{"summary":"Draft is publishable with one warning: the interval method is directionally clear but should make the volatility sample behind sigma = 4.6 explicit.","requiredFixes":[{"rubricItem":"interval","severity":"warning","summary":"The 80% interval cites sigma = 4.6 thousand and a 'broader recent-release volatility allowance' but does not identify the realized-volatility sample or explain why that sigma is appropriate given the listed recent weekly changes are much smaller.","actionRequested":"State the historical window or realized weekly-change sample used to derive sigma = 4.6 thousand, or relabel it as an explicit judgmental uncertainty allowance and justify the size."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact prior/update/interval step mostly satisfies the rubric, but the interval component depends on an unspecified broader volatility allowance.","actionRequested":"Revise the compact step to name the exact interval sample/window or uncertainty assumption used for the 5.9 thousand half-width."}],"optionalSuggestions":["Clarify whether the target is strictly disability compensation claims or the VA rating-bundle compensation-and-pension claims inventory, while keeping the ledger slug and resolver unchanged.","Mention that resolutionDate is the report date, not necessarily the first public posting timestamp, if the catalog treats those separately."]}

Emit the final JSON object only.
