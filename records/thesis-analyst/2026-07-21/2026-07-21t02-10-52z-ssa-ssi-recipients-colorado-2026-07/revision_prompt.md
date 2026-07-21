# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ssa.ssi.recipients.colorado
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ssi-recipients-colorado-july-2026"
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
{"slug":"ssi-recipients-colorado-july-2026","country":"US","type":"data","title":"Colorado SSI recipients, July 2026","question":"Social Security Administration SSI Monthly Statistics Table 4 number of recipients, all federally administered payments, Colorado, July 2026, non-seasonally adjusted, first print","unit":"thousands","pointEstimate":66.367,"ciLow":66.167,"ciHigh":66.567,"confidence":0.8,"resolutionDate":"2026-08-31","resolutionSource":"Social Security Administration SSI Monthly Statistics","resolutionSourceUrl":"https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-07/table04.html","resolutionRule":"Resolve to the first published July 2026 value in SSA SSI Monthly Statistics Table 4, row Colorado, column Total number of recipients for all federally administered payments. SSA publishes whole recipient counts; convert to thousands by dividing by 1,000 and report to the same 0.001-thousand precision implied by whole recipients. Use the first official print only and ignore later revisions after the first July 2026 table is posted. SSA's public schedule and archive give month-level monthly timing rather than a specific day; 2026-08-31 is the latest expected by-date for the July 2026 monthly publication.","dataPointId":"ssa.ssi.recipients.colorado.2026-07.first_print","historicalContext":[{"label":"2026-06 Colorado federal-payment SSI recipients, thousands","value":66.417},{"label":"2026-05 Colorado total SSI recipients, thousands","value":66.403},{"label":"2026-04 Colorado total SSI recipients, thousands","value":66.539},{"label":"2026-02 Colorado total SSI recipients, thousands","value":66.914},{"label":"2026-01 Colorado total SSI recipients, thousands","value":67.018},{"label":"2025-12 Colorado total SSI recipients, thousands","value":67.134}],"drivers":["June 2026 Colorado count was 66.417 thousand before the target month","Recent Colorado SSI recipient counts drifted lower from January to June","May-to-June momentum was nearly flat after earlier declines","National all-recipient SSI counts were nearly flat from May to June","Whole-recipient SSA counts are converted to thousands"],"sourceContext":["https://www.ssa.gov/policy/pub_schedule.html","https://www.ssa.gov/policy/statistics.html?keyword=ssi","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-06/table10.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-05/table04.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-04/table04.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-02/table04.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-01/table04.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2025-12/table04.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-06/table15.html"],"runAt":"2026-07-21T02:11:04Z","reasoning":[{"kind":"heading","text":"Forecast for Colorado SSI recipients in July 2026"},{"kind":"text","text":"Framing and exact resolver: this is SSA SSI Monthly Statistics Table 4, All Federally Administered Payments, row Colorado, Total column, for July 2026, non-seasonally adjusted and first print. The resolution page should be the stable July 2026 Table 4 URL; Table 4 is the exact variant for the target."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA Publishing Schedule and the SSA statistics archive for SSI Monthly Statistics timing.","result":"Fetched timing evidence: SSA Publishing Schedule lists SSI Monthly Statistics frequency as Monthly; SSA statistics archive lists SSI Monthly Statistics last released June 2026 and next expected July 2026, so the July 2026 data table is expected on month-level timing with by-date 2026-08-31."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics June 2026 Table 10 and June 2026 Table 15 for Colorado and supplementation cross-check.","result":"Fetched June 2026 Colorado federal-payment recipients of 66,417; June 2026 Table 15 federally administered state supplementation lists All areas 1,304,252 and does not list Colorado, supporting that Colorado's federal-payment count is the all federally administered total."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics May and April 2026 Table 4 pages for recent same-variant Colorado history.","result":"Fetched Colorado all federally administered totals: May 2026 66,403 recipients and April 2026 66,539 recipients; May components were aged 12,120 and blind/disabled 54,283."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics February and January 2026 Table 4 pages for earlier 2026 same-variant history.","result":"Fetched Colorado all federally administered totals: February 2026 66,914 recipients and January 2026 67,018 recipients; February components were aged 12,188 and blind/disabled 54,726."},{"kind":"tool","tool":"official.lookup","call":"Used the official December 2025 Table 4 page as the year-turn anchor for Colorado.","result":"Fetched Colorado December 2025 total of 67,134 recipients, with aged 12,264 and blind/disabled 54,870."},{"kind":"text","text":"Base rate/reference class: the reference class is recent first-print SSA SSI Monthly Statistics Colorado total-recipient levels in the same all-federally-administered, non-seasonally-adjusted Table 4 variant. The base rate is a stable mid-66-thousand to high-67-thousand Colorado caseload, with the latest available count 66.417 thousand in June."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanism: the level anchor is June 2026 at 66.417 thousand. Momentum is slightly negative over the first half of 2026, but May-to-June was nearly flat, so I apply only a small additional decline for July. I do not add a one-off shock; eligibility, terminations, aging, deaths, and administrative processing should move the count gradually at monthly frequency."},{"kind":"math","text":"Prior/update/interval: persistence prior is June 2026 at 66.417 thousand; historical sample for dispersion uses fetched same-variant adjacent changes Dec->Jan, Jan->Feb, Apr->May, and May->Jun: -0.116, -0.104, -0.136, and +0.014 thousand. Adjustment components are -0.050 thousand for residual first-half downward momentum, +0.000 for one-off shocks, and +0.000 for identifiable policy mechanism shifts, giving point 66.417 - 0.050 = 66.367 thousand. sigma = sqrt((0.116^2 + 0.104^2 + 0.136^2 + 0.014^2) / 4) = 0.104 thousand. The raw 80% half-width is roughly 1.28*sigma = 1.28*0.104 = 0.133 thousand; I widen to 0.200 thousand, 1.50x the raw half-width, because the fast-run sample is short and skips March. Final implied bounds are 66.367 - 0.200 = 66.167 and 66.367 + 0.200 = 66.567."},{"kind":"text","text":"Counter-considerations: upside risk would be a July administrative rebound or delayed entries in aged recipients, which would land above the interval if Colorado exceeded 66.567 thousand. Downside risk would be unusually heavy terminations, disability-recipient attrition, or returned-check/eligibility cleanup effects reflected before first publication, which would land below the interval if Colorado came in under 66.167 thousand. An outside the interval result would imply a larger processing swing than the recent adjacent-month reference class."},{"kind":"forecast","point":66.367,"ciLow":66.167,"ciHigh":66.567}]}

# Reviewer critique
{"summary":"The draft is close, but publication should fix a provenance inconsistency around the latest June anchor and tighten the model-prior/update explanation.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The resolver correctly targets July 2026 SSA SSI Monthly Statistics Table 4, but the latest June evidence/sourceContext cites Table 10/Table 15 even though the same-variant June Table 4 page exists and contains Colorado total recipients of 66,417.","actionRequested":"Replace the June history/tool/sourceContext references with the June 2026 Table 4 URL and describe the June anchor as Table 4 row Colorado, Total column; drop the Table 10/Table 15 supplementation cross-check unless it is clearly labeled as non-resolving context."},{"rubricItem":"model_prior","severity":"warning","summary":"The trace uses last-print persistence as the prior, but does not clearly state whether any formal time-series/model candidate was run or ruled out for this repeated monthly series.","actionRequested":"Add one sentence in the prior/update step stating that persistence is the selected time-series prior, or explicitly rule out a separate model candidate because the fetched sample is short/irregular."},{"rubricItem":"update","severity":"warning","summary":"The -0.050 thousand downward adjustment is plausible but only loosely tied to current evidence, since May-to-June was nearly flat and the rationale is residual first-half momentum.","actionRequested":"Either shrink the movement closer to June persistence or state more concretely why the January-to-June decline should still dominate the nearly flat May-to-June print."}],"optionalSuggestions":["If available, include March 2026 Table 4 or explain its absence so the volatility sample does not appear selectively gapped.","Rename the June historicalContext label from federal-payment to same-variant Table 4 total recipients for consistency with the resolver."]}

Emit the final JSON object only.
