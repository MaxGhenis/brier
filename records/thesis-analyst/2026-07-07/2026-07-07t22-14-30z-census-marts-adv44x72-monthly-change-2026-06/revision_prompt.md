# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.marts.adv44x72.monthly_change
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "census-marts-adv44x72-monthly-change-june-2026"
- targetUnit: "percent_growth"

# Source hints
- Use Census income, poverty, SPM, and health-insurance release pages, CPS ASEC historical tables, and the Census release calendar.
- For official-poverty targets, distinguish the official poverty measure from SPM and cite the exact Census table or report.
- For SPM targets, name the population group, calendar year, and whether taxes, credits, transfers, medical expenses, or housing adjustments matter for the forecast.

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
{"slug":"census-marts-adv44x72-monthly-change-june-2026","country":"US","type":"data","title":"US advance retail sales monthly change, June 2026","question":"What will the U.S. Census Bureau first print for the seasonally adjusted advance monthly percent change in retail and food services sales, total NAICS 44X72, from May 2026 to June 2026?","unit":"percent_growth","pointEstimate":0.3,"ciLow":-1.0,"ciHigh":1.6,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Census Bureau Advance Monthly Sales for Retail and Food Services release","resolutionSourceUrl":"https://www.census.gov/retail/marts/www/marts_current.pdf","resolutionRule":"Resolve to the first Census Bureau Advance Monthly Sales for Retail and Food Services PDF released for June 2026, Table 2, Retail & food services total, percent change for June 2026 Advance from May 2026, seasonally adjusted and not price-adjusted. Use the printed value rounded to 0.1 percentage point and ignore all later revisions or benchmark updates.","dataPointId":"census.marts.adv44x72.monthly_change.2026-06.first_print","historicalContext":[{"label":"2026-05 advance from 2026-04","value":0.9},{"label":"2026-04 revised from 2026-03","value":0.4},{"label":"2025-05 adjusted from 2025-04, computed from Table 1 levels","value":-1.1}],"drivers":["May advance print was strong at +0.9% after revised April +0.4%","Total retail and food services sales level was $763.7 billion in May 2026","Recent same-series monthly changes show high noise, with a small positive central tendency","Gasoline and motor-vehicle categories boosted May and could fade in June","First-print advance estimate is based on an early subsample and is revision-prone"],"sourceContext":["https://www.census.gov/retail/release_schedule.html","https://www.census.gov/economic-indicators/calendar-listview.html","https://www.census.gov/retail/marts/www/marts_current.pdf","https://www.census.gov/retail/index.html","https://www.census.gov/econ/currentdata/?programCode=MARTS"],"runAt":"2026-07-07T22:14:55Z","reasoning":[{"kind":"heading","text":"June 2026 advance retail sales monthly-change forecast"},{"kind":"text","text":"Framing and exact resolver: this target is Census MARTS/Advance Monthly Sales for Retail and Food Services, total retail and food services NAICS 44X72, seasonally adjusted and not adjusted for price changes. The first-print value is the Table 2 percent change for June 2026 Advance from May 2026, not the later MRTS preliminary revision."},{"kind":"tool","tool":"official.lookup","call":"Checked Census Monthly Retail Trade release schedule and Economic Indicator calendar for June 2026 Advance Monthly Retail Trade Report.","result":"Census lists the Advance Monthly Retail Trade Report data month June 2026 for release on July 16, 2026 at 8:30 am; the calendar separately lists Advance Monthly Sales for Retail and Food Services on July 16, 2026 at 8:30 AM for period June 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the May 2026 Census advance retail sales release PDF text and headline values.","result":"The May 2026 release says adjusted retail and food services sales were $763.7 billion, up 0.9 percent from April 2026 and up 6.9 percent from May 2025; March 2026 to April 2026 was revised from +0.5 percent to +0.4 percent."},{"kind":"tool","tool":"official.lookup","call":"Read Census Table 1 and Table 2 for recent same-series adjusted total retail and food services values.","result":"Table 1 adjusted total retail and food services levels were 763705 million for May 2026, 757036 million for April 2026, 754013 million for March 2026, 714568 million for May 2025, and 722442 million for April 2025; Table 2 prints May 2026 from April 2026 at +0.9 and April 2026 from March 2026 at +0.4."},{"kind":"text","text":"Base rate/reference class: using the same Census advance total retail and food services monthly-change variant, the recent fetched values are +0.9, +0.4, and the Table 1 April-to-May 2025 adjusted-level change of roughly -1.1. That small sample centers near zero but with material month-to-month volatility."},{"kind":"text","text":"Variant consistency: all anchors are Census Advance Monthly Sales for Retail and Food Services total retail and food services, seasonally adjusted, not price-adjusted, and expressed as month-over-month percent changes for the same total 44X72 concept."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior uses recent same-variant monthly changes [0.9, 0.4, -1.1], mean = (0.9 + 0.4 - 1.1)/3 = 0.07. Current-release adjustment adds +0.25 for May momentum and still-solid ex-gas/ex-auto breadth, subtracts -0.05 for possible payback from gasoline/vehicle strength, giving point about 0.27 rounded to 0.3. For the interval, sample sigma = 1.04 from [0.9, 0.4, -1.1]; 1.28*sigma = 1.33, so 0.3 +/- 1.3 gives about -1.0 to 1.6."},{"kind":"text","text":"Upside risk: a stronger June auto rebound, continued nonstore strength, or gasoline-price/category lift would land above the interval. Downside risk: a June reversal in gasoline stations plus weaker vehicle and discretionary categories would land below the interval. A broad nominal-spending shock or seasonal-adjustment surprise is the main outside the interval scenario."},{"kind":"forecast","point":0.3,"ciLow":-1.0,"ciHigh":1.6}]}

# Reviewer critique
{"summary":"Draft is publishable after tightening support for the update and interval, but the resolver/target fields are coherent with the ledger contract.","requiredFixes":[{"rubricItem":"update","severity":"warning","summary":"The +0.25 momentum/breadth adjustment cites ex-gas/ex-auto breadth and gasoline/vehicle category effects, but the cited evidence summarized in the draft only supports total May/April prints and total levels.","actionRequested":"Either add the specific Census table/category evidence supporting ex-gas, ex-auto, gasoline, and motor-vehicle claims, or reduce/rephrase the adjustment as a judgmental persistence/momentum update from the total-series prints only."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is based on realized volatility from only three monthly observations, including one 2025 value computed from current-vintage Table 1 levels, which is a weak volatility estimate for this noisy series.","actionRequested":"Use a longer same-series monthly-change sample where available, or explicitly label the 3-point sigma as a fallback heuristic and explain why the resulting +/-1.3 percentage point band is appropriate."},{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact step is mostly present, but the historical sample is too loosely described as the same advance variant even though the 2025 observation appears computed from Table 1 levels rather than taken as a first-print Table 2 advance value.","actionRequested":"Clarify whether the historical sample uses first-print advance values or current-vintage Census levels, and avoid calling it the same first-print variant unless verified."}],"optionalSuggestions":["Consider naming the release time in the resolver sentence: July 16, 2026 at 8:30 AM ET.","If possible, cite or preserve a stable release artifact instead of relying only on the rolling marts_current.pdf URL.","Tail scenarios are adequate, but could be made slightly more target-specific by quantifying what category moves would push the total below -1.0 or above 1.6."]}

Emit the final JSON object only.
