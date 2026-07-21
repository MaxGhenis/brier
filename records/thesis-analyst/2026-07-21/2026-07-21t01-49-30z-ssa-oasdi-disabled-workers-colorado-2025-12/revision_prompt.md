# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ssa.oasdi.disabled_workers.colorado
- period: 2025-12
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ssdi-disabled-workers-colorado-december-2025"
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
{"slug":"ssdi-disabled-workers-colorado-december-2025","country":"US","type":"data","title":"Colorado SSDI Disabled Workers, December 2025","question":"Social Security Administration Annual Statistical Supplement Table 5.J2 number of OASDI disabled workers in current-payment status, Colorado, December 2025, non-seasonally adjusted, first print","unit":"thousands","pointEstimate":75.8,"ciLow":71.0,"ciHigh":80.6,"confidence":0.8,"resolutionDate":"2027-02-28","resolutionSource":"Social Security Administration Annual Statistical Supplement","resolutionSourceUrl":"https://www.ssa.gov/policy/docs/statcomps/supplement/2026/5j.html","resolutionRule":"Resolve to the first published December 2025 value in SSA Annual Statistical Supplement, 2026, Table 5.J2, row Colorado, column Disability: Disabled workers. SSA publishes whole beneficiary counts; convert to thousands by dividing by 1,000 and report to 0.001-thousand precision. Use the first official print only and ignore later revisions. SSA's public schedule gives a 2026-edition release window rather than an exact section day; 2027-02-28 is the latest official completion by-date for the 2026 Annual Statistical Supplement.","dataPointId":"ssa.oasdi.disabled_workers.colorado.2025-12.first_print","historicalContext":[{"label":"2024-12 Colorado disabled workers, thousands","value":77.912},{"label":"2023-12 Colorado disabled workers, thousands","value":79.912},{"label":"2022-12 Colorado disabled workers, thousands","value":83.08},{"label":"2021-12 Colorado disabled workers, thousands","value":87.507},{"label":"2020-12 Colorado disabled workers, thousands","value":92.314}],"drivers":["Colorado disabled-worker beneficiary count has declined each year from 92.314 thousand in 2020 to 77.912 thousand in 2024","The annual decline decelerated from -4.807 thousand in 2021 to -2.000 thousand in 2024","National disabled-worker counts also remain on a gradual downward path, anchoring against a rebound","Current-payment-status administrative counts are whole beneficiaries converted to thousands","No discrete 2025 policy change suggests a sudden Colorado level break"],"sourceContext":["https://www.ssa.gov/policy/pub_schedule.html","https://www.ssa.gov/policy/docs/statcomps/supplement/2025/5j.html","https://www.ssa.gov/policy/docs/statcomps/supplement/2024/5j.html","https://www.ssa.gov/policy/docs/statcomps/supplement/2023/5j.html","https://www.ssa.gov/policy/docs/statcomps/supplement/2022/5j.html","https://www.ssa.gov/policy/docs/statcomps/supplement/2021/5j.html"],"runAt":"2026-07-21T01:49:36Z","reasoning":[{"kind":"heading","text":"Forecast for Colorado SSDI Disabled Workers in December 2025"},{"kind":"text","text":"Framing and exact resolver: this target is the non-seasonally adjusted SSA administrative count of OASDI disabled workers in current-payment status, Colorado, December 2025, from Annual Statistical Supplement Table 5.J2. The variant is disabled workers only, not disabled-worker spouses or children, and all anchors below use that same Table 5.J2 current-payment-status variant."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA Publishing Schedule for Annual Statistical Supplement timing.","result":"Fetched timing evidence: Annual Statistical Supplement frequency is Annual; the 2026 edition release window is June 2026-February 2027 and expected completion is February 28, 2027."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA Annual Statistical Supplement 2025 Table 5.J2 for December 2024 Colorado history.","result":"Fetched Table 5.J2 same-variant values: Colorado total OASDI beneficiaries 987,075; Colorado disabled workers 77,912; all-areas disabled workers 7,231,147 for December 2024."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA Annual Statistical Supplement 2024 and 2023 Table 5.J2 pages for December 2023 and December 2022 history.","result":"Fetched Table 5.J2 same-variant values: Colorado disabled workers 79,912 in December 2023 and 83,080 in December 2022; Colorado total OASDI beneficiaries were 959,232 in 2023 and 939,291 in 2022."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA Annual Statistical Supplement 2022 and 2021 Table 5.J2 pages for December 2021 and December 2020 history.","result":"Fetched Table 5.J2 same-variant values: Colorado disabled workers 87,507 in December 2021 and 92,314 in December 2020; all-areas disabled workers were 7,877,129 in 2021 and 8,151,016 in 2020."},{"kind":"text","text":"Base rate/reference class: the reference class is recent annual first-print SSA Table 5.J2 Colorado disabled-worker levels. The base rate is a steadily declining but decelerating series: 92.314 thousand in 2020, 87.507 in 2021, 83.080 in 2022, 79.912 in 2023, and 77.912 in 2024."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanism: level starts at 77.912 thousand in December 2024. Momentum remains negative, but the annual drop slowed from -4.807 to -4.427 to -3.168 to -2.000 thousand. One-off effects look limited because this is an administrative stock count. Policy mechanics point to continued attrition from terminations, mortality, conversions to retirement age, and awards, with no obvious 2025 break large enough to reverse the trend."},{"kind":"math","text":"Prior/update/interval: persistence prior is December 2024 at 77.912 thousand; historical sample for dispersion uses same-variant successive Colorado changes 2020->2021, 2021->2022, 2022->2023, and 2023->2024: -4.807, -4.427, -3.168, and -2.000 thousand. Adjustment components are -2.000 thousand for last-year momentum and -0.112 thousand for continued national DI attrition, giving point 77.912 - 2.112 = 75.800 thousand. sigma = sqrt((4.807^2 + 4.427^2 + 3.168^2 + 2.000^2) / 4) = 3.766 thousand. The 80% half-width is roughly 1.28*sigma = 1.28*3.766 = 4.820 thousand, so bounds are 75.800 - 4.820 = 70.980 and 75.800 + 4.820 = 80.620, rounded to 71.0 and 80.6."},{"kind":"text","text":"Counter-considerations: upside risk is that 2025 awards or administrative reinstatements run stronger than the recent decelerating decline, which would land above the interval if Colorado exceeds 80.6 thousand. Downside risk is a renewed acceleration in conversions, deaths, terminations, or fewer disability awards, which would land below the interval if the first print is under 71.0 thousand. An outside the interval result would most likely reflect an administrative processing shift, a definitional/table change, or a much larger policy/eligibility shock than recent annual dispersion."},{"kind":"forecast","point":75.8,"ciLow":71.0,"ciHigh":80.6}]}

# Reviewer critique
{"summary":"Draft is publishable: resolver, prior, update, interval derivation, tails, and JSON fields are coherent with the ledger target.","requiredFixes":[],"optionalSuggestions":["Consider saying explicitly that no separate fitted time-series model was used beyond persistence plus recent annual-change momentum.","Interval is conservative because sigma is RMS annual change rather than residual volatility; acceptable, but note this if the format allows."]}

Emit the final JSON object only.
