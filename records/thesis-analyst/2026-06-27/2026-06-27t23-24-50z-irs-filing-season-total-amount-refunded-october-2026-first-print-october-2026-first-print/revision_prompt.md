# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: irs.filing_season.total_amount_refunded.october_2026.first_print
- period: October 2026 first print
- conditional_on: null

# Source hints
- Use IRS filing-season statistics, annual inflation-adjustment revenue procedures, and official IRS release pages.
- For threshold targets, resolve to the first official IRS value for the named tax year and parameter, not an inferred estimate once the official figure is available.
- Match the catalog unit, usually nominal dollars or billions of nominal dollars.

# Default promoted forecasting practices
- Resolve the exact first-print target before inside-view evidence.
- Fetch and state the recent official-source reference class.
- Anchor on the outside-view base rate before current-release adjustments.
- Separate level, momentum, one-off, and policy-mechanism effects before combining them.
- Size the 80% interval from realized first-print dispersion, then widen or skew only for stated reasons.
- Name concrete upside, downside, and outside-the-interval scenarios.

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
- reasoning must contain at least 7 steps, at least 3 tool steps whose result strings include fetched numbers, one explicit base-rate or reference-class step, one math step, one counter-consideration, and a final forecast step whose numbers exactly match the cell.
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead. Numbers may come from official public sources or inspected local run/model artifacts, but the provenance must be clear.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.1.0, prompt 9435029c5fb9, tools e15bf40583f8, promptMode fast)


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
{"slug":"irs-total-refunds-october-2026","country":"US","type":"data","title":"IRS cumulative refunds, October 2026","question":"What total amount refunded will the IRS report in its first October 2026 Filing Season Statistics snapshot for current-year individual income tax returns, first print, nominal USD billions?","unit":"usd_billions","pointEstimate":368,"ciLow":356,"ciHigh":385,"confidence":0.8,"resolutionDate":"2026-10-31","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.irs.gov/newsroom/filing-season-statistics-for-week-ending-oct-17-2025","resolutionRule":"Resolve to the first IRS Filing Season Statistics page published for an October 2026 week ending date after the October 15 extended individual filing deadline. Use the reported current-year individual-return line 'Total amount refunded', in nominal USD billions, rounded to the nearest 1 billion. If multiple October 2026 snapshots are posted, the earliest October 2026 snapshot governs; ignore later revisions or later October snapshots.","dataPointId":"irs.filing_season.total_amount_refunded.october_2026.first_print","historicalContext":[{"label":"2026 May 8 total amount refunded","value":324.757},{"label":"2025 Oct 17 total amount refunded","value":311.651},{"label":"2024 Oct 18 total amount refunded","value":309.929},{"label":"2023 Oct 20 total amount refunded","value":308.986},{"label":"2023-2025 average May-to-first-October addition","value":39.75}],"drivers":["2026 refunds running far above 2025 by early May","post-May extension-season additions usually near 37 to 42 billion","2025 tax-law changes raised refundable and overwithheld amounts","October 15 extension deadline concentrates late returns","IRS staffing and paper-processing frictions widen timing risk"],"sourceContext":["https://www.irs.gov/newsroom/filing-season-statistics-for-week-ending-may-8-2026","https://www.irs.gov/newsroom/filing-season-statistics-for-week-ending-oct-17-2025","https://www.irs.gov/newsroom/filing-season-statistics-for-week-ending-oct-18-2024","https://www.irs.gov/newsroom/filing-season-statistics-for-week-ending-oct-20-2023","https://www.irs.gov/newsroom/filing-season-statistics-for-week-ending-may-9-2025","https://www.irs.gov/newsroom/filing-season-statistics-for-week-ending-may-10-2024","https://www.irs.gov/newsroom/filing-season-statistics-for-week-ending-may-12-2023","https://www.irs.gov/pub/irs-drop/rp-25-32.pdf"],"runAt":"2026-06-27T23:25:31Z","reasoning":[{"kind":"heading","text":"Forecast IRS October 2026 cumulative refunds"},{"kind":"text","text":"Resolver is the IRS Filing Season Statistics current-year individual-return line for total amount refunded in the first October 2026 snapshot. The target is nominal USD billions, not fiscal-year Treasury cash refunds."},{"kind":"tool","tool":"official.lookup","call":"Opened the IRS May 8, 2026 Filing Season Statistics page for the latest in-season level.","result":"Fetched IRS May 8, 2026 table: total returns received 144.992 million, total number of refunds 99.138 million, total amount refunded 324.757 USD billion, average refund 3276 USD, versus 274.979 USD billion on May 9, 2025."},{"kind":"tool","tool":"official.lookup","call":"Opened the IRS Oct. 17, 2025 Filing Season Statistics page for the latest prior-year October analogue.","result":"Fetched IRS Oct. 17, 2025 table: total returns received 163.594 million, total number of refunds 102.122 million, total amount refunded 311.651 USD billion, average refund 3052 USD; the page was last reviewed or updated 2025-10-24."},{"kind":"tool","tool":"official.lookup","call":"Opened the IRS Oct. 18, 2024 Filing Season Statistics page for an additional first-October reference point.","result":"Fetched IRS Oct. 18, 2024 table: total returns received 161.489 million, total number of refunds 103.185 million, total amount refunded 309.929 USD billion, average refund 3004 USD."},{"kind":"tool","tool":"official.lookup","call":"Opened the IRS Oct. 20, 2023 and May 2023 Filing Season Statistics pages to size the May-to-October increment.","result":"Fetched IRS Oct. 20, 2023 total amount refunded 308.986 USD billion and May 12, 2023 total amount refunded 266.849 USD billion, implying a 42.137 USD billion May-to-first-October addition."},{"kind":"tool","tool":"official.lookup","call":"Opened the IRS May 2024 and May 2025 Filing Season Statistics pages to complete the increment reference class.","result":"Fetched IRS May 10, 2024 total amount refunded 269.488 USD billion and May 9, 2025 total amount refunded 274.979 USD billion; paired with first-October values of 309.929 and 311.651, the additions were 40.441 and 36.672 USD billion."},{"kind":"tool","tool":"official.policy.lookup","call":"Opened IRS Rev. Proc. 2025-32 for tax-year 2026 policy parameters affecting refunds.","result":"Fetched Rev. Proc. 2025-32: OBBBA set the 2025 standard deduction at 31500 USD for joint returns and 15750 USD for single filers; for tax year 2026 the standard deduction is 32200 USD joint and 16100 USD single, and the 2026 child tax credit is 2200 USD with 1700 USD refundable."},{"kind":"text","text":"Base-rate/reference-class step: the cleanest outside view is May-to-first-October additions in the three most recent comparable filing-season pages. Those increments were 42.137, 40.441, and 36.672 billion, averaging 39.75 billion, with a narrow historical range but based on only three observations."},{"kind":"text","text":"Prior-run update: the catalog target had a 370 billion point using a 324.757 billion May 2026 anchor and an approximately 41.8 billion historical add-on. Recomputing the first-October reference class gives a slightly lower mechanical add-on of 39.75 billion, but the unusually refund-heavy 2026 filing season argues against cutting the forecast much."},{"kind":"math","text":"Mechanical base = 324.757 + ((308.986 - 266.849) + (309.929 - 269.488) + (311.651 - 274.979)) / 3 = 324.757 + 39.75 = 364.51. I add about 3.5 billion for elevated 2026 refund generosity and possible late-filer refund concentration after tax-law changes, giving 368.0. I set the 80% interval at 356 to 385: wider than the 2023-2025 increment dispersion because 2026 has a policy and processing regime shift."},{"kind":"text","text":"Counter-consideration: if the 18.1 percent May refund-dollar jump mostly reflects front-loaded direct-deposit refunds rather than higher full-season liability refunds, the remaining May-to-October increment could undershoot the recent 36.7 to 42.1 billion band and the outcome could land near 356 billion."},{"kind":"text","text":"Upside scenario: if extension filers claim the new deductions and refundable credits at high rates, and IRS processing catches up despite staffing strain, cumulative refunds could exceed 385 billion by the first October snapshot."},{"kind":"forecast","point":368,"ciLow":356,"ciHigh":385}]}

# Reviewer critique
{
  "summary": "The forecast is broadly coherent, but the resolver metadata needs a firmer official-source and resolution-date treatment before publication.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "resolutionSourceUrl points to the 2025 analogue page, not an official 2026 resolver page, calendar, placeholder, or stable IRS index for the future first print.",
      "actionRequested": "Replace the resolver source with a stable IRS Filing Season Statistics index or official 2026 placeholder/calendar if available, and state that the final observation will be the first qualifying October 2026 IRS page once published."
    },
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "resolutionDate is set to 2026-10-31 without showing official support; this appears inferred from cadence rather than verified.",
      "actionRequested": "Use an officially supported expected publication/resolution date, or encode the resolution date as the specific first qualifying IRS publication date once known rather than defaulting to 2026-10-31."
    },
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "The +3.5 billion inside-view adjustment is directionally explained but not tightly tied to the cited policy evidence or observed 2026 refund composition.",
      "actionRequested": "Add one sentence quantifying why elevated May 2026 refunds and cited tax-year policy changes justify roughly +3.5 billion rather than using the mechanical 364.5 billion prior."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The 80% interval is said to be wider than recent increment dispersion, but the lower and upper bounds imply much larger downside/upside increment deviations than the three-year reference class.",
      "actionRequested": "State the implied May-to-October increment range behind 356 to 385 and explain why those tails are appropriate for an 80% interval under the 2026 regime shift."
    }
  ],
  "optionalSuggestions": [
    "Clarify whether 'first October 2026 snapshot' means the first October week-ending date after October 15, not any earlier October page.",
    "Rename '2025 tax-law changes' more precisely if the cited Rev. Proc. is for tax year 2026 parameters."
  ]
}

Emit the final JSON object only.
