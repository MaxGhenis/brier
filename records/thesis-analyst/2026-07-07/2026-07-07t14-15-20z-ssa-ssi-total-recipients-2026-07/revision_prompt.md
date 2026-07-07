# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ssa.ssi.total_recipients
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ssi-recipients-july-2026"
- targetUnit: "millions"

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
{"slug":"ssi-recipients-july-2026","country":"US","type":"data","title":"SSI recipients, July 2026","question":"Social Security Administration SSI Monthly Statistics Table 2 total number of recipients for July 2026, all federally administered payments, end of month, first print","unit":"millions","pointEstimate":7.309,"ciLow":7.28,"ciHigh":7.338,"confidence":0.8,"resolutionDate":"2026-08-31","resolutionSource":"Social Security Administration SSI Monthly Statistics","resolutionSourceUrl":"https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-07/table02.html","resolutionRule":"Resolve to the first published July 2026 value in SSA SSI Monthly Statistics Table 2, row July 2026, column Total number of recipients for all federally administered payments. The SSA table publishes counts as whole recipients; convert to millions by dividing by 1,000,000 and round forecast display values to three decimals. Use the first official print only and ignore later revisions or adjusted checks after the first July 2026 table is posted.","dataPointId":"ssa.ssi.total_recipients.2026-07.first_print","historicalContext":[{"label":"2026-05 total SSI recipients, millions","value":7.322937},{"label":"2026-04 total SSI recipients, millions","value":7.338132},{"label":"2026-03 total SSI recipients, millions","value":7.351825},{"label":"2026-02 total SSI recipients, millions","value":7.358913},{"label":"2026-01 total SSI recipients, millions","value":7.36951},{"label":"2025-12 total SSI recipients, millions","value":7.392201}],"drivers":["recent total SSI caseload has declined from 7.392 million in December 2025 to 7.323 million in May 2026","latest two-month average decline is about 0.0146 million recipients","state-supplementation-only recipients continue to edge down","no identified July 2026 policy mechanism creates a discrete caseload break","short-horizon uncertainty is dominated by monthly administrative churn and returned-check adjustment risk"],"sourceContext":["https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-05/table02.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-05/table01.html","https://www.ssa.gov/policy/pub_schedule.html","https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/"],"runAt":"2026-07-07T14:15:30Z","reasoning":[{"kind":"heading","text":"July 2026 SSI total recipients"},{"kind":"text","text":"The exact resolver is SSA SSI Monthly Statistics Table 2, all federally administered payments, total number of recipients for July 2026 at end of month. This is the total SSI recipient count, not federal-payment-only recipients, not state recipients by geography, and not OASDI beneficiaries who also receive SSI."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA publishing schedule and current SSI publications to verify release timing and target source family.","result":"Fetched official timing evidence on July 7, 2026: SSA Publishing Schedule lists SSI Monthly Statistics with frequency Monthly; current SSI Monthly Statistics page is May 2026 and says released June 2026; current Monthly Statistical Snapshot is May 2026 and says released June 2026. The July 2026 SSI monthly first print is therefore tied to the SSA monthly publication expected by August 2026; I use 2026-08-31 as the official by-date because the public schedule provides month-level, not day-level, timing."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics May 2026 Table 2 for the latest total-recipient history.","result":"Fetched Table 2 total SSI recipients: May 2025 = 7,409,168; June 2025 = 7,412,558; July 2025 = 7,394,877; August 2025 = 7,405,735; September 2025 = 7,436,689; October 2025 = 7,393,406; November 2025 = 7,391,176; December 2025 = 7,392,201; January 2026 = 7,369,510; February 2026 = 7,358,913; March 2026 = 7,351,825; April 2026 = 7,338,132; May 2026 = 7,322,937."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics May 2026 Table 1 for recipient composition and same-variant confirmation.","result":"Fetched same-publication Table 1 values for May 2026: total recipients = 7,322,937; federal payment only = 6,018,514; federal payment and state supplementation = 1,181,054; state supplementation only = 123,369; also receiving OASDI benefits = 2,528,904."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA Monthly Statistical Snapshot May 2026 Table 3 as a cross-check against the SSI monthly table.","result":"Fetched snapshot cross-check: May 2026 all SSI recipients = 7,323 thousand; under 18 = 1,016 thousand; ages 18-64 = 3,805 thousand; 65 or older = 2,502 thousand; total payments = 5,736 million dollars; average monthly payment = 738.13 dollars."},{"kind":"text","text":"Base rate/reference class: the reference class is recent first-print SSA SSI Monthly Statistics total-recipient levels from May 2025 through May 2026. The last print is 7.322937 million, while the 2026 sequence has declined every month from 7.369510 million in January to 7.322937 million in May, so a pure persistence prior is too high unless current evidence points to a rebound."},{"kind":"text","text":"Level, momentum, one-off, and policy split: the level is a mature administrative caseload near 7.3 million, not a fast cyclical series. Momentum is downward: January-May 2026 fell by 0.046573 million, and March-May fell by 0.028888 million. I found no official public evidence in the checked SSA release context of a July 2026 policy mechanism that would abruptly expand or contract SSI eligibility; the main one-off risk is administrative timing and returned-check adjustment in the first two months after release."},{"kind":"text","text":"Prior/update/interval: persistence prior is last-print persistence at 7.322937 million, but the reference class of fetched SSA total-recipient values supports a two-month trend update because the July target is two months after the May latest print. The two-month changes in the fetched sample are -0.014291, -0.006823, +0.041812, -0.012329, -0.045513, -0.001205, -0.021666, -0.033288, -0.017685, -0.020781, and -0.028888 million; their mean is -0.014605 million, so the point is 7.322937 - 0.014605 = 7.308332 million, rounded to 7.309. Interval method uses realized dispersion of those two-month changes; sigma = 0.022437 million, so 1.28*sigma = 0.028719 million, giving implied bounds 7.279613 to 7.337051, rounded to 7.280 and 7.338."},{"kind":"math","text":"Point calculation: 7.322937 latest May 2026 total recipients + (-0.014605 two-month mean change) = 7.308332 million, rounded to 7.309 million. Interval calculation: sigma = 0.022437 million from fetched two-month changes; 1.28*sigma = 0.028719 million; 7.308332 - 0.028719 = 7.279613 and 7.308332 + 0.028719 = 7.337051, rounded to 7.280 and 7.338 million."},{"kind":"text","text":"Counter-consideration: upside risk is a rebound like September 2025, when the two-month change reached +0.041812 million, which would land above the interval if July prints above 7.338 million. Downside risk is continued attrition or returned-check adjustment like the October-November 2025 two-month declines, which would land below the interval if July prints below 7.280 million. An outside the interval result would most likely come from administrative cleanup, unusually large awards, or a state-supplementation processing shift visible in the first July table."},{"kind":"forecast","point":7.309,"ciLow":7.28,"ciHigh":7.338}]}

# Reviewer critique
{
  "summary": "The draft is largely publication-ready, with only minor resolver-date wording needing tightening.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The resolution date is justified as a month-end by-date from SSA's month-level publishing schedule, not as a verified exact release date.",
      "actionRequested": "Clarify that 2026-08-31 is the catalog resolution by-date/latest expected resolution date based on SSA's monthly schedule, and that the actual resolving observation is the first July 2026 Table 2 print whenever posted."
    }
  ],
  "optionalSuggestions": [
    "State explicitly that the 80% interval corresponds to approximately +/-1.28 standard deviations from the historical two-month-change sample.",
    "In the tail paragraph, name approximate numeric tail thresholds after unit conversion, e.g. above 7.338 million or below 7.280 million."
  ]
}

Emit the final JSON object only.
