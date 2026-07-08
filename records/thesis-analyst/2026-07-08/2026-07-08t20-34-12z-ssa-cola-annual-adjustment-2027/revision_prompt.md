# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ssa.cola.annual_adjustment
- period: 2027
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "social-security-cola-2027"
- targetUnit: "percent"

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
{"slug":"social-security-cola-2027","country":"US","type":"data","title":"Social Security COLA 2027","question":"Social Security Administration annual cost-of-living adjustment for Social Security benefits payable in 2027, first official print, percent rounded to the nearest tenth.","unit":"percent","pointEstimate":3.8,"ciLow":0.7,"ciHigh":6.9,"confidence":0.8,"resolutionDate":"2026-10-14","resolutionSource":"Social Security Administration latest Cost-of-Living Adjustment page","resolutionSourceUrl":"https://www.ssa.gov/oact/cola/latestCOLA.html","resolutionRule":"Resolve to the first official SSA published COLA for Social Security benefits beginning with December 2026 benefits payable in January 2027. Use the percent adjustment rounded to the nearest tenth of one percent under the SSA CPI-W formula comparing the average CPI-W for July, August, and September 2026 with the average CPI-W for July, August, and September 2025. Ignore later revisions or corrections unless SSA formally identifies the first print as corrected.","dataPointId":"ssa.cola.annual_adjustment.2027.first_print","historicalContext":[{"label":"latest official COLA, benefits payable 2026","value":2.8},{"label":"official COLA, benefits payable 2025","value":2.5},{"label":"official COLA, benefits payable 2024","value":3.2},{"label":"official COLA, benefits payable 2023","value":8.7},{"label":"official COLA, benefits payable 2022","value":5.9}],"drivers":["May 2026 CPI-W already 3.645 percent above the 2025 Q3 CPI-W base average","Energy inflation lifted near-term CPI but may partly reverse before Q3","Core CPI is lower than headline, limiting persistence","SSA formula rounds the Q3 CPI-W increase to the nearest tenth","September 2026 CPI release fixes the last resolving input on October 14, 2026"],"sourceContext":["https://www.ssa.gov/oact/cola/latestCOLA.html","https://www.ssa.gov/oact/cola/colaseries.html","https://www.bls.gov/schedule/2026/10_sched.htm","https://www.bls.gov/news.release/cpi.nr0.htm"],"runAt":"2026-07-08T20:34:22Z","reasoning":[{"kind":"heading","text":"Forecast for 2027 Social Security COLA"},{"kind":"text","text":"Framing and exact resolver: this forecasts SSA's first official annual COLA for Social Security benefits payable in January 2027, not CPI-U, CPI-E, SSI dollars, taxable maximum, or average benefit dollars. The resolving CPI variant is CPI-W, U.S. city average, all items, series code CWUR0000SA0."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA latest Cost-of-Living Adjustment page to verify formula, latest print, rounding precision, and the 2025 Q3 CPI-W base for the next COLA calculation.","result":"Fetched latest COLA = 2.8 percent; SSA states the Q3 2025 CPI-W average = 317.265, Q3 2024 base average = 308.729, July 2025 CPI-W = 316.349, August 2025 = 317.306, September 2025 = 318.139, and the published calculation was (317.265 - 308.729) / 308.729 x 100 = 2.8 percent."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA COLA history page for the recent official reference class of annual COLA outcomes.","result":"Fetched recent official COLAs: 2016 = 0.3, 2017 = 2.0, 2018 = 2.8, 2019 = 1.6, 2020 = 1.3, 2021 = 5.9, 2022 = 8.7, 2023 = 3.2, 2024 = 2.5, 2025 = 2.8 percent."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS October 2026 release calendar to verify the release date for the September 2026 CPI input that completes Q3 2026 CPI-W.","result":"Fetched official schedule: Consumer Price Index for September 2026 is scheduled on October 14, 2026 at 08:30 AM Eastern; this is the first scheduled release containing the September 2026 CPI-W needed for SSA's 2027 COLA calculation."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS May 2026 CPI Summary for latest CPI-W and inflation momentum before the Q3 measurement window.","result":"Fetched May 2026 CPI-W = 328.829, CPI-W 12-month change = 4.4 percent, CPI-W not-seasonally-adjusted monthly change = 0.7 percent, CPI-U 12-month change = 4.2 percent, core CPI-U 12-month change = 2.9 percent, and energy 12-month change = 23.5 percent."},{"kind":"text","text":"Base rate/reference class: the recent SSA COLA sample averages 3.11 percent over 2016-2025, but it is fat-tailed because pandemic and energy shocks produced 5.9 and 8.7 percent outcomes. A plain outside-view prior is around 3.1 percent, with a wide realized-dispersion interval."},{"kind":"math","text":"Current-input math: using SSA's Q3 2025 CPI-W base average 317.265 and BLS May 2026 CPI-W 328.829 gives (328.829 - 317.265) / 317.265 x 100 = 3.645 percent. I round the point above that to 3.8 percent because Q3 still includes July-September, core inflation is positive, and energy strength may not fully persist."},{"kind":"math","text":"Prior/update/interval: model is a 2016-2025 SSA COLA reference-class prior with a May-2026 CPI-W nowcast update; historical sample = [0.3, 2.0, 2.8, 1.6, 1.3, 5.9, 8.7, 3.2, 2.5, 2.8], mean = 3.11, sigma = 2.46 from the values themselves, half-width = 1.28*sigma = 3.14. Adjustment components are level +0.54 from the May CPI-W implied 3.645 percent versus the 3.11 base rate, momentum +0.25 for positive core inflation, one-off energy -0.10 for reversal risk, and policy-mechanism 0.00 because the SSA formula is automatic, giving a 3.8 point. Interval arithmetic: 3.8 - 3.14 = 0.66 and 3.8 + 3.14 = 6.94, rounded to 0.7 to 6.9 percent."},{"kind":"text","text":"Counter-consideration: upside risk is another gasoline or tariff-driven Q3 price jump that would land above the interval near or above 7.0 percent. Downside risk is a sharp energy reversal plus soft core readings in July-September that would land below the interval near zero. Outside the interval would also occur if a government shutdown or formal correction changes the first SSA publication timing or label, but the value should still be mechanically determined from CPI-W."},{"kind":"forecast","point":3.8,"ciLow":0.7,"ciHigh":6.9}]}

# Reviewer critique
{
  "summary": "The draft is publishable with only minor clarity improvements; resolver, evidence, prior/update math, interval, and JSON fields are broadly coherent.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Clarify that the 80% interval is an approximate normal-reference interval from the 2016-2025 realized COLA standard deviation, not a calibrated backtest.",
    "Tighten the correction rule to preserve first-print wording: resolve to SSA's first official COLA print, ignoring later corrections unless the resolver policy explicitly treats the first print as invalid.",
    "Consider stating that the lower tail is mechanically floored at 0.0% if the rounded CPI-W increase is zero or negative."
  ]
}

Emit the final JSON object only.
