# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ssa.oasdi.disabled_worker_beneficiaries
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ssdi-disabled-worker-beneficiaries-june-2026"
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
{"slug":"ssdi-disabled-worker-beneficiaries-june-2026","country":"US","type":"data","title":"SSDI disabled workers, June 2026","question":"SSA Monthly Statistical Snapshot Table 2 disabled workers beneficiaries, June 2026, not seasonally adjusted, first print, in thousands","unit":"thousands","pointEstimate":7010,"ciLow":7002,"ciHigh":7017,"confidence":0.8,"resolutionDate":"2026-07-31","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/2026-06.html","resolutionRule":"Resolve to the first published SSA Monthly Statistical Snapshot for June 2026, Table 2 Social Security benefits, Disability Insurance, Disabled workers, Beneficiaries Number (thousands). Use the whole-thousands value exactly as first printed and ignore later revisions or corrections unless SSA replaces the first-print page before archival capture.","dataPointId":"ssa.oasdi.disabled_worker_beneficiaries.2026-06.first_print","historicalContext":[{"label":"May 2026 disabled workers, Table 2, thousands","value":7029},{"label":"April 2026 disabled workers, Table 2, thousands","value":7050},{"label":"March 2026 disabled workers, Table 2, thousands","value":7070},{"label":"February 2026 disabled workers, Table 2, thousands","value":7081},{"label":"January 2026 disabled workers, Table 2, thousands","value":7099},{"label":"December 2025 disabled workers, Table 2, thousands","value":7126}],"drivers":["Persistent SSDI disabled-worker roll decline","Recent monthly losses near 19 thousand","No identified one-month policy shock before June 2026 first print","Whole-thousands SSA Table 2 rounding"],"sourceContext":["https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/","https://www.ssa.gov/policy/pub_schedule.html","https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/2026-04.html","https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/2026-03.html","https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/2026-02.html","https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/2026-01.html","https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/2025-12.html"],"runAt":"2026-07-08T20:16:27Z","reasoning":[{"kind":"heading","text":"SSDI disabled-worker beneficiaries, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: the target is SSA Monthly Statistical Snapshot Table 2, Social Security benefits, Disability Insurance, Disabled workers, Beneficiaries Number, in thousands, for June 2026. The resolution page should follow SSA's monthly archive pattern at /policy/docs/quickfacts/stat_snapshot/2026-06.html, with the value rounded to whole thousands as printed."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA Monthly Statistical Snapshot current page and Table 2 for latest official value.","result":"Fetched May 2026 Monthly Statistical Snapshot released June 2026; Table 2 shows Disabled workers beneficiaries 7,029 thousand, Disability Insurance total 8,059 thousand, and disabled-worker monthly benefits 11,491 million dollars."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA publishing schedule for release timing.","result":"Fetched SSA Publishing Schedule text: Monthly Statistical Snapshot frequency is Monthly; current snapshot page says May 2026 was released in June 2026, so the June 2026 first print is scheduled for the July 2026 monthly update, with ledger resolutionDate 2026-07-31."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA archive pages for April and March 2026 snapshots, Table 2 disabled workers.","result":"Fetched April 2026 disabled workers 7,050 thousand and March 2026 disabled workers 7,070 thousand from Table 2; same variant, not seasonally adjusted SSA first-print monthly snapshot values."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA archive pages for February 2026, January 2026, and December 2025 snapshots, Table 2 disabled workers.","result":"Fetched February 2026 disabled workers 7,081 thousand, January 2026 disabled workers 7,099 thousand, and December 2025 disabled workers 7,126 thousand from Table 2."},{"kind":"text","text":"Base rate/reference class: the recent official-source reference class is successive changes in the same Table 2 disabled-worker stock from December 2025 through May 2026. The monthly changes are -27, -18, -11, -20, and -21 thousand, showing a steady decline rather than a flat level."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: level is 7,029 thousand in May; momentum is about -19 thousand per month; no public first-print evidence points to a June-only administrative shock; policy and demographic mechanisms still favor gradual exits, conversions, deaths, and lower inflow keeping the roll drifting down."},{"kind":"math","text":"Prior/update/interval: persistence plus recent-mean-change prior on the Dec 2025-May 2026 official sample gives mean change = (-27 - 18 - 11 - 20 - 21) / 5 = -19.4 thousand, so point = 7,029 - 19.4 = 7,009.6, rounded to 7,010. For the 80% interval, sample sigma from successive changes = 5.77 thousand, so half-width = 1.28*sigma = 1.28*5.77 = 7.39 thousand; 7,009.6 +/- 7.39 gives 7,002.2 to 7,017.0, rounded to 7,002-7,017."},{"kind":"text","text":"Counter-considerations: upside risk would be a temporary slowdown in terminations or more retroactive awards, which would land above the interval if June prints above 7,017 thousand. Downside risk would be a processing cleanup or unusually heavy exits, which would land below the interval if the first print is below 7,002 thousand."},{"kind":"forecast","point":7010,"ciLow":7002,"ciHigh":7017}]}

# Reviewer critique
{"summary":"Publishable with minor warnings: resolver and forecast arithmetic are coherent, but the evidence links and interval justification should be tightened before publication.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The draft uses May 2026 as the latest official value but does not include the May 2026 snapshot URL in sourceContext, and resolutionSource is generic despite the resolver depending on SSA Monthly Statistical Snapshot Table 2.","actionRequested":"Add the May 2026 snapshot URL to sourceContext and make resolutionSource name SSA Monthly Statistical Snapshot Table 2 explicitly."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is based on only five recent month-to-month changes, which may understate uncertainty if treated as the full realized volatility sample.","actionRequested":"Either justify the five-month local-volatility window as intentional for a one-month-ahead forecast, or add a longer same-series historical change/residual sample and explain whether it changes the half-width."}],"optionalSuggestions":["Mention that the June 2026 page URL is a resolver placeholder until SSA publishes the first print.","In the compact prior/update/interval sentence, label the prior as May-level persistence plus recent mean monthly change to make the baseline clearer."]}

Emit the final JSON object only.
