# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ssa.hearings.average_processing_time_days
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ssa-hearings-average-processing-time-june-2026"
- targetUnit: "count"
- resolutionSource: "SSA Office of Hearings Operations, Hearing Office Workload Data, FY2026"
- resolutionSourceUrl: "https://www.ssa.gov/appeals/DataSets/02_HO_Workload_Data.html"
- resolutionRule: "Resolves to the national fiscal-year-to-date Average Processing Time in calendar days (the DSPN_AVGPT concept: average days from hearing request date to disposition date) as first published in SSA's Hearing Office Workload Data for the FY2026 reporting period ending in late June 2026; later revisions do not count."

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
{"slug":"ssa-hearings-average-processing-time-june-2026","country":"US","type":"data","title":"SSA hearings average processing time, Jun 2026","question":"Social Security Administration Office of Hearings Operations Hearing Office Workload Data, FY 2026 cumulative through the June 2026 reporting period, national Average Processing Time in calendar days, first print","unit":"count","pointEstimate":326,"ciLow":322,"ciHigh":330,"confidence":0.8,"resolutionDate":"2026-07-31","resolutionSource":"SSA Office of Hearings Operations, Hearing Office Workload Data, FY2026","resolutionSourceUrl":"https://www.ssa.gov/appeals/DataSets/02_HO_Workload_Data.html","resolutionRule":"Resolves to the national fiscal-year-to-date Average Processing Time in calendar days (the DSPN_AVGPT concept: average days from hearing request date to disposition date) as first published in SSA's Hearing Office Workload Data for the FY2026 reporting period ending in late June 2026; later revisions do not count. Match SSA's integer-day published rounding precision.","dataPointId":"ssa.hearings.average_processing_time_days.2026-06.first_print","historicalContext":[{"label":"October 2025 FY2026 cumulative average processing time, days","value":279},{"label":"November 2025 FY2026 cumulative average processing time, days","value":288},{"label":"December 2025 FY2026 cumulative average processing time, days","value":296},{"label":"January 2026 FY2026 cumulative average processing time, days","value":302},{"label":"February 2026 FY2026 cumulative average processing time, days","value":309},{"label":"March 2026 FY2026 cumulative average processing time, days","value":314},{"label":"April 2026 FY2026 cumulative average processing time, days","value":318},{"label":"May 2026 FY2026 cumulative average processing time, days","value":322}],"drivers":["FY2026 cumulative average processing time has risen every fetched month","Latest same-variant official point is May 2026 at 322 days","Recent increments slowed to +4 days in April and +4 days in May","Fiscal-year-to-date averaging mutes one-month case-mix shocks","Integer-day SSA reporting precision; catalog unit count represents calendar days"],"sourceContext":["https://www.ssa.gov/appeals/DataSets/02_HO_Workload_Data.html","https://www.ssa.gov/appeals/DataSets/05_Average_Processing_Time_Report.html","https://www.ssa.gov/appeals/DataSets/archive/archive_data_reports.html","https://www.ssa.gov/appeals/DataSets/data_dictionary.html","https://www.ssa.gov/policy/pub_schedule.html"],"runAt":"2026-07-08T20:58:40Z","reasoning":[{"kind":"heading","text":"SSA OHO hearings average processing time, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this targets SSA Office of Hearings Operations Hearing Office Workload Data for FY2026 cumulative through June 2026, specifically DSPN_AVGPT average processing time in calendar days from hearing request date to disposition date. The variant is unadjusted administrative hearing-office workload data, not average wait time until hearing held and not a later archive revision."},{"kind":"tool","tool":"official.lookup","call":"Opened the SSA OHO Hearing Office Workload Data current page to verify source family, period, and table variant.","result":"Fetched Hearing Office Workload Data FY 2026 for reporting purposes 09/27/2025 through 05/29/2026; the page states 4 key workload indicators and includes Average Processing Time, with current report period ending 05/29/2026."},{"kind":"tool","tool":"official.lookup","call":"Opened the SSA Hearing Office Average Processing Time Ranking Report current page for same-concept cross-check.","result":"Fetched FY 2026 reporting purposes 09/27/2025 through 05/29/2026, Fiscal YTD Ending 05/29/2026, Workdays 165; the page says the ranking is by average number of days until final disposition of the hearing request."},{"kind":"tool","tool":"official.lookup","call":"Opened the SSA Hearings and Appeals Public Data Files data dictionary for the exact field definition.","result":"Fetched DSPN_AVGPT as SMALLINT, Disposition Average Processing Time, average number of calendar days from Hearing Request Date to Disposition Date; also fetched RPTG_PRD_ENDT as Reporting Period End Date and WRKDAYS as work days."},{"kind":"tool","tool":"official.lookup","call":"Opened the SSA FY2026 archive index and current public pages to assemble the same-variant official reference class.","result":"Fetched same-variant FY2026 cumulative average processing time points: Oct 2025 279 days, Nov 2025 288, Dec 2025 296, Jan 2026 302, Feb 2026 309, Mar 2026 314, Apr 2026 318, May 2026 322."},{"kind":"tool","tool":"official.lookup","call":"Opened the SSA Publishing Schedule and Hearings and Appeals archive index to verify release timing treatment for the ledger resolution date.","result":"Fetched SSA Publishing Schedule text saying anticipated release dates are based on current production plans and may be updated for production or data issues; fetched archive index showing FY2026 Hearing Office Workload Data archived through April 2026 while current pages show May 2026 through 05/29/2026. No exact OHO June placeholder was listed, so I keep the canonical ledger resolutionDate 2026-07-31 as the target by-date."},{"kind":"text","text":"Base rate/reference class: the reference class is the same SSA OHO FY2026 fiscal-year-to-date average-processing-time series. The level rose from 279 days in October 2025 to 322 days in May 2026, a 43-day increase over 7 monthly updates, while the latest two increments were both +4 days."},{"kind":"text","text":"Prior run note: an earlier public Thesis record for this same target used a 326-day point and 322-330 interval; I treat that as strategy context only and keep the forecast because the independently rechecked official history and dispersion support the same numbers."},{"kind":"text","text":"Level, momentum, one-off, and policy split: the level anchor is May's 322 days; momentum remains upward because cumulative FY-to-date dispositions are still clearing older requests; one-off risk is mainly hearing-office mix and transferred workloads; I found no official public source in this run indicating a June-only policy change that would mechanically break trend."},{"kind":"math","text":"Prior/update/interval: persistence-plus-damped-trend prior uses May 2026 at 322 days and the recent official sample of successive changes +9, +8, +6, +7, +5, +4, +4 days. The mean change is 6.14 days, but the latest 2 changes average 4.0 days, so I update May by +4 days for a 326-day point. Interval method uses realized dispersion of successive changes; sigma = 1.95 days, so 1.28*sigma = 2.50 days. I widen to a 4-day half-width because a national disposition-weighted aggregate can move if June completions disproportionately clear older or newer cases, giving final implied bounds of 322 to 330 days after integer-day rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a June cleanup of older pending hearings or heavier disposition weight in slower offices, which would land above the interval if the first print is over 330 days. Downside risk is faster closure of newer cases or a mix shift toward quicker offices, which would land below the interval if the first print is under 322 days. Outside the interval would likely require an unusual case-mix shock rather than ordinary continuation of the May trend."},{"kind":"forecast","point":326,"ciLow":322,"ciHigh":330}]}

# Reviewer critique
{
  "summary": "The forecast is mostly publication-ready, but it should remove the same-target prior Thesis record reference because it creates catalog-circularity risk.",
  "requiredFixes": [
    {
      "rubricItem": "leakage",
      "severity": "blocking",
      "summary": "Reasoning cites an earlier public Thesis record for the same target with the same 326 point and 322-330 interval.",
      "actionRequested": "Remove the prior-run note and any same-target catalog/Thesis forecast reference; make clear the point and interval come only from official SSA history and the stated persistence-plus-damped-trend method."
    }
  ],
  "optionalSuggestions": [
    "In the compact Prior/update/interval step, explicitly label the +4 adjustment as the damped-trend component to make the update decomposition easier to audit.",
    "If available before publication, add the exact SSA release-calendar placeholder for the June FY2026 first print; otherwise keeping the canonical 2026-07-31 by-date is acceptable."
  ]
}

Emit the final JSON object only.
