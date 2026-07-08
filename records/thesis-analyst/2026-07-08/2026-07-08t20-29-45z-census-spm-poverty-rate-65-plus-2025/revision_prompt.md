# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.spm.poverty_rate_65_plus
- period: 2025
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "spm-senior-poverty-2025"
- targetUnit: "percent"

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
{"slug":"spm-senior-poverty-2025","country":"US","type":"data","title":"US senior SPM poverty rate, 2025","question":"What will the U.S. Census Bureau first report as the Supplemental Poverty Measure poverty rate for people age 65 years and older for calendar year 2025 in Poverty in the United States: 2025, Table B-2 or successor first-release table?","unit":"percent","pointEstimate":15.3,"ciLow":13.1,"ciHigh":17.5,"confidence":0.8,"resolutionDate":"2026-09-08","resolutionSource":"U.S. Census Bureau Poverty in the United States: 2025 first-release tables","resolutionSourceUrl":"https://www.census.gov/topics/income-poverty/supplemental-poverty-measure/data/tables.html","resolutionRule":"Resolve to the first Census Bureau published calendar-year 2025 Supplemental Poverty Measure poverty rate for people age 65 years and older, reported in percent, normally Table B-2 of Poverty in the United States: 2025. Use the initially released value rounded to one decimal percentage point; ignore later errata, benchmark updates, revised CPS ASEC files, or later table revisions unless Census labels the original first print as withdrawn before public release.","dataPointId":"census.spm.poverty_rate_65_plus.2025.first_print","historicalContext":[{"label":"2024 first print age 65+ SPM poverty rate","value":15.0},{"label":"2023 first print age 65+ SPM poverty rate","value":14.2},{"label":"2022 first print age 65+ SPM poverty rate","value":14.1},{"label":"2021 first print age 65+ SPM poverty rate","value":10.7},{"label":"2024 all-person SPM poverty rate","value":12.9}],"drivers":["Latest same-variant senior SPM rate was 15.0 percent in 2024","Senior SPM includes taxes, credits, transfers, medical out-of-pocket expenses, and housing adjustments, not just pretax cash income","2024 senior SPM rose despite flat all-person SPM, showing age-specific medical and threshold pressure","Social Security COLA supports nominal resources but medical premiums and out-of-pocket costs remain senior-specific downside risk","No 2025 policy shock comparable to pandemic-era temporary transfers is assumed"],"sourceContext":["https://www.census.gov/about/event-calendar.html","https://www.census.gov/library/publications/2025/demo/p60-287.html","https://www.census.gov/data/tables/2025/demo/income-poverty/p60-287.html","https://www2.census.gov/programs-surveys/demo/tables/p60/287/tableB-2.xlsx","https://www.census.gov/content/dam/Census/library/visualizations/2025/demo/p60-287/figure8.pdf","https://www.census.gov/newsroom/blogs/research-matters/2025/09/supplemental-poverty-measure.html"],"runAt":"2026-07-08T20:30:10Z","reasoning":[{"kind":"heading","text":"Forecast for 2025 senior Supplemental Poverty Measure poverty rate"},{"kind":"text","text":"Framing and exact resolver: this targets the Census Bureau first print for calendar-year 2025 people age 65 years and older under the Supplemental Poverty Measure. This is not the official poverty measure: SPM resources include taxes, refundable credits, and noncash transfers, and subtract necessary expenses including medical out-of-pocket and work expenses, with thresholds adjusted for housing tenure and geography."},{"kind":"tool","tool":"official.lookup","call":"Checked the Census Bureau Event Calendar and annual income, poverty, and health-insurance release context for the calendar-year 2025 first print.","result":"Fetched official Census event-calendar surface last revised 2026-01-29 and the annual Income, Poverty, and Health Insurance release timing used for this target: calendar-year 2025 first print scheduled for 2026-09-08."},{"kind":"tool","tool":"official.lookup","call":"Opened the Census Poverty in the United States: 2024 publication page and table listing for the exact SPM table family.","result":"Fetched report number P60-287, publication date 2025-09-09, overall 2024 official poverty rate 10.6 percent, overall 2024 SPM rate 12.9 percent, and Table B-2 title: Number and Percentage of People in Poverty Using the Supplemental Poverty Measure by Age, Race, and Hispanic Origin: 2009 to 2024."},{"kind":"tool","tool":"official.lookup","call":"Opened Census Figure 8 and Table B-2-linked context for the age 65+ SPM history.","result":"Fetched same-variant age 65 years and older SPM rates from Census figure/table context: 2024 = 15.0 percent, 2023 about 14.2 percent, 2022 about 14.1 percent, and 2021 about 10.7 percent; the same figure shows 2024 official-plus age 65+ poverty at 9.9 percent."},{"kind":"tool","tool":"official.lookup","call":"Opened the 2025 Census Research Matters SPM threshold blog for mechanics behind the 2024 first-print level.","result":"Fetched SPM threshold increases from 2023 to 2024: owners with a mortgage 5.8 percent, owners without a mortgage 5.6 percent, renters 5.2 percent, versus official poverty thresholds up 2.9 percent; the blog states 2024 overall SPM was 12.9 percent and anchored 2024 SPM was 12.4 percent."},{"kind":"text","text":"Base rate/reference class: the relevant official-source reference class is recent Table B-2 senior SPM first prints. The post-pandemic-transfer senior series was roughly 14.1 in 2022, 14.2 in 2023, and 15.0 in 2024, so the base rate is near 14.4 to 15.0 rather than the all-person 12.9 percent level."},{"kind":"text","text":"Level, momentum, and policy mechanism: the 2024 jump for seniors looks tied to SPM threshold, housing, and medical-expense mechanics rather than a broad all-person poverty surge. For 2025, Social Security COLA and continued older-adult benefit receipt support resources, but Medicare premiums, medical out-of-pocket costs, and housing-adjusted thresholds keep senior SPM above official-plus poverty and make a full reversal unlikely."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest same-variant senior SPM level 15.0 percent; historical sample = 2021-2024 senior SPM first-print rates 10.7, 14.1, 14.2, 15.0; adjustment components = +0.2 for continued threshold/medical-expense pressure, +0.1 for age-specific 2024 upward momentum, and 0.0 for no assumed new broad anti-poverty transfer shock, giving point 15.0 + 0.2 + 0.1 = 15.3. Interval method uses sample standard deviation of successive changes: 2021-2022 = +3.4, 2022-2023 = +0.1, 2023-2024 = +0.8 percentage points; sigma = 1.74, half-width = 1.28*sigma = 2.23, so 80% interval = 15.3 +/- 2.23 = [13.1, 17.5] after one-decimal rounding."},{"kind":"text","text":"Counter-consideration: downside risk is that the 2024 senior increase was mostly a one-year threshold/expense adjustment and 2025 Social Security and retirement-income gains offset medical costs, which would land near 13.1 or below the interval. Upside risk is another large SPM threshold or medical-expense shock, weaker survey income for older adults, or reduced transfer effectiveness, which would land above the interval near 17.6 or higher. The main outside the interval scenario is a large methodological or threshold shock in Table B-2 rather than ordinary income momentum."},{"kind":"forecast","point":15.3,"ciLow":13.1,"ciHigh":17.5}]}

# Reviewer critique
{"summary":"Draft is publication-ready under the rubric; resolver, prior, update, interval, tails, and JSON fields are coherent with the target contract.","requiredFixes":[],"optionalSuggestions":["Consider noting that the volatility estimate is based on only three annual changes and is therefore a judgmental 80% interval rather than a stable time-series estimate.","If space allows, cite the exact Census event-calendar entry title for the 2026-09-08 release date."]}

Emit the final JSON object only.
