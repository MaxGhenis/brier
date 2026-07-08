# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ssa.ssi.recipients_aged_65_plus
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ssi-recipients-aged-65-plus-june-2026"
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
{"slug":"ssi-recipients-aged-65-plus-june-2026","country":"US","type":"data","title":"SSI recipients aged 65+ June 2026","question":"Social Security Administration SSI Monthly Statistics Table 1 number of recipients, all federally administered payments, Total row, Age 65 or older column, June 2026, first print","unit":"thousands","pointEstimate":2503.1,"ciLow":2496.2,"ciHigh":2510,"confidence":0.8,"resolutionDate":"2026-07-31","resolutionSource":"Social Security Administration SSI Monthly Statistics","resolutionSourceUrl":"https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-06/table01.html","resolutionRule":"Resolve to the first published June 2026 value in SSA SSI Monthly Statistics Table 1, All Federally Administered Payments, Number of recipients, row Total, column Age 65 or older. SSA publishes whole recipient counts; convert to thousands by dividing by 1,000 and report to the same 0.001-thousand precision implied by whole recipients. Use the first official print only and ignore later revisions or returned-check adjustments after the first June 2026 table is posted. SSA's public schedule provides month-level monthly timing rather than a specific day; 2026-07-31 is the catalog latest expected resolution by-date for the June 2026 monthly publication, not a claimed exact release day.","dataPointId":"ssa.ssi.recipients_aged_65_plus.2026_06.first_print","historicalContext":[{"label":"2026-05 latest first-print proxy","value":2501.549},{"label":"2026-04","value":2500.422},{"label":"2026-03","value":2502.133},{"label":"2026-02","value":2506.79},{"label":"2026-01","value":2509.113},{"label":"2025-06 year-earlier June","value":2484.16}],"drivers":["Aged-65-plus SSI caseload has risen year over year","Early-2026 level drifted down from January to April before a small May rebound","Same-variant May-to-June 2025 change was positive but modest","No new benefit-level policy shock is assumed for June 2026"],"sourceContext":["https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/index.html","https://www.ssa.gov/policy/pub_schedule.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-05/table01.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-04/table01.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-03/table01.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-02/table01.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-01/table01.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2025-06/table01.html"],"runAt":"2026-07-08T20:13:39Z","reasoning":[{"kind":"heading","text":"SSI aged-65-plus recipients, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this targets the NSA administrative count in SSA SSI Monthly Statistics Table 1, All Federally Administered Payments, Number of recipients, row Total, Age 65 or older column. All anchors below use this same Table 1 variant, not Table 2 totals, federal-payment-only recipients, state-only recipients, or OASDI dual-entitlement counts."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics current index and SSA Publishing Schedule for release timing.","result":"Fetched timing evidence: current SSI Monthly Statistics page is May 2026 and states released June 2026; SSA Publishing Schedule lists SSI Monthly Statistics frequency as Monthly; run date is 2026-07-08; the schedule gives month-level timing but no exact June 2026 release day, so 2026-07-31 is used as the catalog latest expected by-date."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics May 2026 Table 1 for latest same-variant value.","result":"Fetched May 2026 Table 1 Total row Age 65 or older = 2,501,549 recipients, equal to 2501.549 thousand; all recipients = 7,322,937; aged eligibility category = 1,184,449."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics January through April 2026 Table 1 pages for recent same-year history.","result":"Fetched same-variant Age 65 or older counts: January 2026 = 2,509,113, February 2026 = 2,506,790, March 2026 = 2,502,133, April 2026 = 2,500,422 recipients, or 2509.113, 2506.790, 2502.133, 2500.422 thousand."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics May through December 2025 Table 1 pages for reference-class dispersion and seasonality.","result":"Fetched same-variant Age 65 or older counts: May 2025 = 2,482,524, June 2025 = 2,484,160, July 2025 = 2,487,107, August 2025 = 2,497,163, September 2025 = 2,508,702, October 2025 = 2,504,084, November 2025 = 2,506,451, December 2025 = 2,512,399 recipients."},{"kind":"text","text":"Base rate/reference class: the recent official-source class is monthly Table 1 aged-65-plus recipient levels from May 2025 through May 2026. The latest level, 2501.549 thousand, is 19.025 thousand above May 2025 but 7.564 thousand below January 2026; that argues for persistence with a small positive June seasonal/current adjustment rather than a large trend extrapolation."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2026 latest level 2501.549 thousand; historical sample = same-variant May 2025-May 2026 monthly levels; adjustment components = +1.636 thousand for the May-to-June 2025 seasonal move, +0.0 for policy mechanism because no June 2026 SSI eligibility/payment rule shock is assumed, and about -0.1 rounding/current-drift offset after the early-2026 decline, giving point 2501.549 + 1.636 - 0.085 = 2503.100 thousand. Interval method uses sample standard deviation of successive monthly changes from May 2025 to May 2026: changes were +1.636, +2.947, +10.056, +11.539, -4.618, +2.367, +5.948, -3.286, -2.323, -4.657, -1.711, +1.127 thousand; sigma = 5.392, half-width = 1.28*sigma = 6.902 thousand, so 80% interval = 2503.100 +/- 6.902 = [2496.198, 2510.002], rounded to 2496.2 to 2510.0 thousand."},{"kind":"text","text":"Counter-considerations: upside risk is a continuation of the May rebound plus faster aged inflows, which would land above the interval if June rises by more than about 8.5 thousand recipients from May. Downside risk is renewed terminations or returned-check downward adjustment in the first print, which would land below the interval if June falls by more than about 5.3 thousand from May. A policy or administrative cleanup affecting aged SSI eligibility would be the main outside the interval scenario."},{"kind":"forecast","point":2503.1,"ciLow":2496.2,"ciHigh":2510}]}

# Reviewer critique
{
  "summary": "The draft is publishable: it specifies the SSA Table 1 first-print resolver, uses a clear persistence prior with recent same-series evidence, derives the interval from realized monthly volatility, and keeps units coherent.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider making the 2026-07-31 date label explicit in the final JSON-facing text as a by-date rather than an exact scheduled release day.",
    "The tail scenario mentioning returned-check adjustments could clarify that only adjustments present in the first published June 2026 table count."
  ]
}

Emit the final JSON object only.
