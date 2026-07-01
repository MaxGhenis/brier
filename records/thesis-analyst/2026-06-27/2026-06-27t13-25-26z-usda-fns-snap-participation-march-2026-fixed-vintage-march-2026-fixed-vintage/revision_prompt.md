# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

Hard scope: Do not inspect the local repository or workspace. Do not run ls, cat, sed, rg, find, git, or open local files. The schema is fully specified below. You may use web search, official public URLs, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands only.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: usda.fns.snap.participation.march_2026.fixed_vintage
- period: March 2026 fixed vintage
- conditional_on: null

# Source hints
- Use the official agency data page and release calendar.
- FRED or sanctioned mirrors may be used only for history, not final resolution.
- Match the agency's published rounding precision.

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
{"slug":"usda-fns-snap-participation-march-2026-fixed-vintage","country":"US","type":"data","title":"US SNAP Participation, Mar 2026","question":"USDA Food and Nutrition Service SNAP national Average Participation for March 2026, not seasonally adjusted, first-print fixed vintage","unit":"millions","pointEstimate":41.92,"ciLow":40.95,"ciHigh":42.85,"confidence":0.8,"resolutionDate":"2026-07-10","resolutionSource":"USDA Food and Nutrition Service SNAP Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","resolutionRule":"Resolve to the first USDA FNS SNAP monthly national Average Participation value published for March 2026 in the FY2026 national monthly SNAP data table. Convert persons to millions and round to three decimals. Use the first official print only; ignore later revisions or refreshed vintages.","dataPointId":"usda.fns.snap.average_participation.2026-03.first_print","historicalContext":[{"label":"FY2025 Mar","value":41.759},{"label":"FY2025 Jun","value":41.812},{"label":"FY2025 Sep","value":41.734},{"label":"FY2025 Nov latest available","value":41.687}],"drivers":["SNAP caseloads have been nearly flat around 41.7 million in recent official monthly prints","Labor-market drift and food-price pressure support a small upward tilt into early 2026","Expanded work-requirement and recertification enforcement risks pull participation lower","March has limited seasonal signal relative to administrative and policy effects","First-print uncertainty is dominated by state reporting lags and later revisions"],"sourceContext":["https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","https://www.fns.usda.gov/data-research/data-release-calendar","https://www.fns.usda.gov/snap/supplemental-nutrition-assistance-program"],"runAt":"2026-06-27T13:26:10Z","reasoning":[{"kind":"heading","text":"Forecast for USDA FNS SNAP March 2026 First-Print Participation"},{"kind":"text","text":"The resolver is the first USDA Food and Nutrition Service publication of national SNAP Average Participation for March 2026. The target is an administrative count, not seasonally adjusted, resolved from the official FNS SNAP data table rather than FRED or news mirrors."},{"kind":"tool","tool":"official.lookup","call":"Checked the USDA FNS SNAP data table page for the national monthly SNAP participation series and latest visible reference class.","result":"Fetched official monthly national Average Participation reference points: FY2025 Mar 41.759 million, FY2025 Jun 41.812 million, FY2025 Sep 41.734 million, and FY2025 Nov 41.687 million."},{"kind":"tool","tool":"official.lookup","call":"Checked the official FNS data release calendar / posting schedule for the March 2026 fixed-vintage availability date.","result":"Fetched the SNAP Program Data posting date for the March 2026 first-print fixed vintage as 2026-07-10, with the schedule entry tied to the monthly SNAP data table refresh."},{"kind":"tool","tool":"official.lookup","call":"Checked USDA FNS SNAP program context for scale and administrative mechanism.","result":"Fetched program context showing SNAP serves about 42 million people nationally and is administered through 50 states plus the District of Columbia, which explains state-reporting lag risk."},{"kind":"text","text":"Base-rate/reference-class anchor: recent official monthly first-print participation is tightly clustered around 41.7 million. A neutral outside-view forecast would therefore start near 41.75 million before adding early-2026 macro and policy adjustments."},{"kind":"text","text":"Level and momentum: the latest official points show little trend, so I keep the level close to the recent 41.7 million baseline and do not extrapolate a large increase."},{"kind":"text","text":"Current-release adjustments: mild labor-market and household-budget pressure add about 0.20 million to the baseline, while work-requirement enforcement, churn, and recertification frictions subtract about 0.05 million, yielding a small net upward adjustment."},{"kind":"math","text":"Point calculation: 41.75 million recent baseline + 0.20 million macro/need pressure - 0.03 million policy/churn adjustment = 41.92 million. Interval: recent first-print monthly dispersion is modest, but March 2026 has policy and state-reporting uncertainty, so I use an 80% range of roughly -0.97 to +0.93 million around the point, giving 40.95 to 42.85 million."},{"kind":"text","text":"Counter-consideration: a downside outside-the-interval case would be rapid enforcement of eligibility/work-rule changes or unusually high procedural churn pushing participation below 40.95 million; an upside outside-the-interval case would be a sharper labor-market deterioration or delayed disenrollment pushing participation above 42.85 million."},{"kind":"forecast","point":41.92,"ciLow":40.95,"ciHigh":42.85}]}

# Reviewer critique
{"summary":"The draft is mostly publishable, but it needs tighter support for the release-date rule and interval derivation before publication.","requiredFixes":[{"rubricItem":"resolver","severity":"warning","summary":"The resolver and first-print rule are clear, but the draft asserts the 2026-07-10 posting date without quoting or identifying the exact calendar entry name/date from the cited release calendar.","actionRequested":"Add the exact USDA FNS release-calendar entry used to verify that the March 2026 SNAP data first print is scheduled for 2026-07-10."},{"rubricItem":"model_prior","severity":"warning","summary":"The draft states a persistence/base-rate prior but does not clearly say whether a time-series model was used or ruled out.","actionRequested":"Add one sentence explicitly ruling out a formal time-series model, or state the simple persistence/trend model used and why it is adequate."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is plausible but not tied to a measured realized volatility, revision error, or explicit uncertainty calculation.","actionRequested":"Explain the interval width using recent month-to-month variation, historical first-print misses/revisions, or a named judgmental uncertainty assumption."},{"rubricItem":"update","severity":"warning","summary":"The +0.20 million macro/need adjustment and -0.03 to -0.05 million policy adjustment are directionally explained but weakly evidenced from the cited public sources.","actionRequested":"Either cite concrete public evidence for these adjustment sizes from the cited materials or label them explicitly as judgmental adjustments."},{"rubricItem":"coherence","severity":"warning","summary":"The drivers mention a -0.05 million policy drag, while the math uses -0.03 million.","actionRequested":"Make the policy/churn adjustment numerically consistent across the reasoning and point calculation."}],"optionalSuggestions":["Clarify whether historicalContext values are first-print values or latest visible official values.","State that the unit conversion is from persons to millions for all displayed historical points as well as the final resolved value."]}

Emit the final JSON object only.
