# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

Hard scope: Do not inspect the local repository or workspace. Do not run ls, cat, sed, rg, find, git, or open local files. The schema is fully specified below. You may use web search, official public URLs, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands only.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.spm.child_poverty_rate.2025
- period: calendar year 2025
- conditional_on: null

# Source hints
- Use the official agency release calendar, not inferred cadence.
- FRED may be used as a history mirror, but resolution cites the agency.
- For FOMC targets, resolve to the target range upper bound after the announcement.
- For DOL claims, name the week-ending date and cite the release date.

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
- Every tool step result must include at least one fetched numeric value. Put qualitative source notes in text steps instead.
- resolutionDate must be verified from an official release calendar or announcement schedule this run. Do not infer it from cadence.
- runAt must be the actual UTC date command output from this run.
- Slug should be stable and descriptive; if the same target already exists, reuse the obvious canonical slug rather than inventing a near-duplicate.

Emit the final JSON object only. (agent thesis.analyst v2.1.0, prompt 3a08d7c397df, tools e15bf40583f8, promptMode fast)


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
{"slug":"us-census-spm-child-poverty-rate-2025","country":"US","type":"data","title":"US child SPM poverty rate, 2025","question":"U.S. Census Bureau Supplemental Poverty Measure poverty rate for people under age 18 in calendar year 2025, percent, first print in the 2025 Income, Poverty and Health Insurance Coverage annual release, not revised values","unit":"percent","pointEstimate":13.4,"ciLow":11.7,"ciHigh":15.4,"confidence":0.8,"resolutionDate":"2026-09-08","resolutionSource":"U.S. Census Bureau annual Income, Poverty and Health Insurance Coverage release","resolutionSourceUrl":"https://www.census.gov/newsroom/releases/calendar.html","resolutionRule":"Resolve to the first U.S. Census Bureau published Supplemental Poverty Measure rate for people under age 18 for calendar year 2025, in percent, rounded to one decimal place as first printed in the annual Income, Poverty and Health Insurance Coverage release or its SPM table package. Ignore later revisions, reissues, or replicated calculations unless the first print is formally corrected by Census on the release day.","dataPointId":"census.spm.child_poverty_rate.2025.first_print","historicalContext":[{"label":"2021 child SPM poverty rate","value":5.2},{"label":"2022 child SPM poverty rate","value":12.4},{"label":"2023 child SPM poverty rate","value":13.7},{"label":"2024 child SPM poverty rate","value":13.8}],"drivers":["Post-2021 child tax credit expiration keeps the level far above the pandemic low","2025 labor market remained broadly supportive but softer than 2023-2024","Lower inflation reduces threshold/resource mismatch versus 2022 shock","No large new federal child cash transfer was in force for calendar 2025","Sampling and SPM expense adjustments create about 1 to 2 percentage points of first-print uncertainty"],"sourceContext":["https://www.census.gov/newsroom/releases/calendar.html","https://www.census.gov/library/publications/2025/demo/p60-286.html","https://www.census.gov/data/tables/time-series/demo/income-poverty/supplemental-poverty-measure.html","https://www.census.gov/library/stories/2025/09/poverty-measure-includes-noncash-government-assistance.html"],"runAt":"2026-06-27T13:51:22Z","reasoning":[{"kind":"heading","text":"Forecast of the 2025 Census child Supplemental Poverty Measure rate"},{"kind":"text","text":"The resolver is the Census Bureau's first printed Supplemental Poverty Measure poverty rate for people under age 18 for calendar year 2025, reported in the annual Income, Poverty and Health Insurance Coverage release package. Later revised tables are out of scope."},{"kind":"tool","tool":"official.lookup","call":"Checked the Census Bureau release calendar for the annual Income, Poverty and Health Insurance Coverage release covering calendar year 2025.","result":"The official calendar entry gives release date 2026-09-08 and release time 10:00 a.m. for the 2025 Income, Poverty and Health Insurance Coverage annual statistics."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent Census SPM child poverty reference points from the official SPM publication/table series.","result":"Official child SPM poverty rates were 5.2 percent in 2021, 12.4 percent in 2022, 13.7 percent in 2023, and 13.8 percent in 2024."},{"kind":"tool","tool":"official.lookup","call":"Fetched latest broad poverty context from the Census 2024 income and poverty release materials.","result":"The 2024 official poverty rate was 10.6 percent, down 0.4 percentage point from 11.0 percent in 2023, while the overall SPM rate was 12.9 percent in 2024 and 12.9 percent in 2023."},{"kind":"tool","tool":"official.lookup","call":"Fetched policy-mechanism context from the Census SPM materials on transfers and expenses.","result":"Census reported Social Security moved 28.7 million people out of SPM poverty in 2024 and medical expenses moved more than 7.0 million people into SPM poverty in 2024; these figures matter less directly for children than refundable credits, SNAP, housing, child care, and payroll-tax effects."},{"kind":"text","text":"Base-rate/reference-class anchor: after the temporary 2021 child tax credit expansion ended, the child SPM rate returned to a high-12 to high-13 percent range. The three post-expansion observations, 2022 through 2024, average 13.3 percent, while the latest two average 13.75 percent."},{"kind":"text","text":"Level effect: the 2024 first print is the best starting point because the policy regime for child cash benefits in calendar 2025 was much closer to 2024 than to 2021. This argues for an anchor near 13.8 percent rather than the 2021 low."},{"kind":"text","text":"Momentum and macro adjustment: 2025 had lower inflation pressure than the 2022 shock and no large recession, which should modestly reduce SPM poverty through real resources and threshold dynamics. Softer labor conditions and elevated housing and child care costs keep the improvement limited."},{"kind":"text","text":"One-off and policy-mechanism adjustment: no new 2025 federal child allowance comparable to the expanded 2021 CTC was in place, so downside improvement is bounded. SNAP, housing assistance, tax credits, work expenses, and child care expenses can still move the SPM child rate noticeably in the first print."},{"kind":"text","text":"Counter-consideration: upside risk is meaningful if CPS ASEC measured earnings for low-income families disappoint, housing and child care expenses push more families below SPM thresholds, or benefit participation/resource measurement weakens. Downside risk comes from stronger low-wage earnings, lower inflation thresholds, and larger refundable-credit effects than expected."},{"kind":"math","text":"Post-expansion mean = (12.4 + 13.7 + 13.8) / 3 = 13.3. Latest-year anchor = 13.8. Apply -0.4 percentage point for lower inflation and still-positive real income support, then add 0.0 for no major child-transfer expansion: point = 13.4. For the 80% interval, use about +/-1.8 percentage points around the point from recent first-print dispersion and skew slightly upward for expense and sampling risk: 11.7 to 15.4."},{"kind":"forecast","point":13.4,"ciLow":11.7,"ciHigh":15.4}]}

# Reviewer critique
{"summary":"Draft is mostly coherent on target definition and prior, but it needs stronger cited support for the 2025 inside-view adjustment and a clearer model/interval rationale before publication.","requiredFixes":[{"rubricItem":"update","severity":"blocking","summary":"The -0.4 pp movement from the 2024 anchor rests on claims about 2025 labor market, inflation, real income support, housing, and child care costs, but the cited evidence shown is mainly Census 2024/SPM context and does not substantiate those 2025 conditions.","actionRequested":"Either cite public 2025 evidence for the macro and cost claims used in the adjustment, or reduce/reframe the adjustment as judgmental with a smaller or explicitly uncertain update from the persistence prior."},{"rubricItem":"model_prior","severity":"warning","summary":"The draft uses a post-expansion mean and latest-year anchor, but does not explicitly identify this as the time-series/model prior or explain why a richer model is ruled out.","actionRequested":"Add a sentence naming the prior as a persistence/post-2021 mean blend and explicitly state that a formal time-series model is not used because the relevant post-policy regime has only three observations."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is described as about +/-1.8 pp from recent dispersion and skew, but the calculation is not shown and the cited recent post-expansion observations alone do not obviously imply that width.","actionRequested":"Tie the interval to a stated empirical volatility or explicit uncertainty components, such as recent year-to-year changes, sampling/error risk, and SPM expense-policy uncertainty, with enough arithmetic to justify 11.7 to 15.4."},{"rubricItem":"resolver","severity":"warning","summary":"The resolver is specific, but the resolution source URL is a generic release calendar page that may change and the exact first-print table location is not pinned.","actionRequested":"Add the expected Census SPM table package or annual poverty/SPM release page as the resolution source when available, while keeping the release calendar as date support."}],"optionalSuggestions":["Clarify whether confidence means an 80% central interval so it matches ciLow and ciHigh.","State that the unit is percentage points/percent rounded to one decimal in both the question and resolution rule.","Add one concrete upside and downside numeric tail example tied to plausible child SPM mechanisms."]}

Emit the final JSON object only.
