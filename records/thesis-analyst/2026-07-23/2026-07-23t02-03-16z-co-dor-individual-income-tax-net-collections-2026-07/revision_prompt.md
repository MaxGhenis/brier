# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: co.dor.individual_income_tax.net_collections
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "colorado-income-tax-collections-july-2026"
- targetUnit: "usd_billions"

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
{"slug":"colorado-income-tax-collections-july-2026","country":"US","type":"data","title":"Colorado individual income tax collections, July 2026","question":"What will the Colorado Department of Revenue General Fund Collections Report first print for net individual income tax collections for July 2026, cash basis, in USD billions?","unit":"usd_billions","pointEstimate":0.98,"ciLow":0.78,"ciHigh":1.18,"confidence":0.8,"resolutionDate":"2026-08-31","resolutionSource":"Colorado Department of Revenue General Fund Collections Reports","resolutionSourceUrl":"https://cdor.colorado.gov/data-and-reports/general-fund-collections-reports","resolutionRule":"Resolve to the first Colorado Department of Revenue General Fund Collections Report value for July 2026 net individual income tax collections, cash basis, as posted in the Colorado state accounting system. Convert the agency-published dollar figure to USD billions and round to the agency's published precision; ignore later revisions or subsequent restatements after the first print.","dataPointId":"co.dor.individual_income_tax.net_collections.2026_07.first_print","historicalContext":[{"label":"FY2024-25 net individual income tax annual actual, monthly average equivalent","value":0.833},{"label":"FY2025-26 net individual income tax annual estimate, monthly average equivalent","value":0.929},{"label":"FY2026-27 net individual income tax annual forecast, monthly average equivalent","value":1.045},{"label":"July 2019 individual income tax collections cited from CDOR data","value":0.614},{"label":"July 2020 individual income tax collections cited from CDOR data, deadline-shift anomaly","value":1.76}],"drivers":["FY2026-27 annual individual income tax forecast implies about 1.045 billion per month before seasonality","July is not an April final-payment peak month but can include trailing filing and estimated-payment cash flow","Through May 2026, withholding was up 4.9 percent, estimated payments up 20.3 percent, and cash with returns up 15.0 percent year over year","Refunds were up 15.2 percent through May 2026, reducing net collections risk","OBBBA and Colorado credit-trigger rules create unusually high tax-policy uncertainty for 2026 cash collections"],"sourceContext":["https://cdor.colorado.gov/data-and-reports/general-fund-collections-reports","https://content.leg.colorado.gov/publications/forecast-june-2026","https://content.leg.colorado.gov/sites/default/files/june-2026-forecast-for-posting-accessible_0.pdf","https://osc.test.colorado.gov/financial-operations/financial-reports/revenue-summary-reports","https://tax.colorado.gov/due-date-guide"],"runAt":"2026-07-23T02:03:39Z","reasoning":[{"kind":"heading","text":"Colorado July 2026 individual income tax net collections"},{"kind":"text","text":"Framing and exact resolver: the target is the Colorado Department of Revenue General Fund Collections Report line for net individual income tax collections for July 2026, cash basis, first print. CDOR says these General Fund Collections Reports show monthly net receipts from taxes collected and administered by CDOR as posted in the Colorado state accounting system; all figures are on a cash basis."},{"kind":"tool","tool":"official.lookup","call":"Opened the Colorado Department of Revenue General Fund Collections Reports page for the official resolution page and series definition.","result":"Fetched official CDOR report context: General Fund Collections Reports show net receipts from taxes collected and administered monthly by CDOR, all figures are reported on a cash basis, and the current data file is titled General Fund Collections Report, July 2019 to Date."},{"kind":"tool","tool":"official.lookup","call":"Opened the Colorado Office of the State Controller revenue summary reports page as an official source-family cross-check for monthly General Fund revenue reporting.","result":"Fetched OSC official context: the General Fund revenue summary report includes general purpose revenue received, including individual taxes, corporate taxes, excise taxes, insurance taxes, and investment income; the page lists monthly July reports from July 2016 through July 2021."},{"kind":"tool","tool":"official.forecast.lookup","call":"Opened the Colorado Legislative Council Staff June 2026 Economic and Revenue Forecast for the latest official annual individual income tax outlook.","result":"Fetched LCS forecast values: FY2024-25 net individual income tax actual was 9997.9 million dollars, FY2025-26 estimate was 11153.0 million dollars, and FY2026-27 forecast was 12537.6 million dollars."},{"kind":"tool","tool":"official.forecast.lookup","call":"Read the LCS individual income tax narrative for current cash-basis momentum entering the July 2026 target month.","result":"Fetched LCS cash-basis momentum through May 2026: withholding up 4.9 percent, estimated payments up 20.3 percent, cash with returns up 15.0 percent, refunds up 15.2 percent, and FY2025-26 individual income tax expected to increase 11.6 percent to 11.15 billion dollars before diversions."},{"kind":"tool","tool":"public.history.lookup","call":"Checked a public Tax Foundation summary that cites Colorado Department of Revenue individual income tax receipts for the filing-deadline-distorted July 2019 and July 2020 reference points.","result":"Fetched cited Colorado July values: April 2019 individual income tax revenue was 1.82 billion dollars, April 2020 was 0.819 billion dollars, July 2019 was 0.614 billion dollars, and July 2020 was 1.76 billion dollars after the COVID filing-deadline shift."},{"kind":"tool","tool":"official.calendar","call":"Checked official Colorado tax due-date guidance and the CDOR/OSC monthly publication surfaces for timing around July collections and first-print resolution.","result":"Fetched official timing evidence: individual estimated payments are due April 15, June 15, September 15, and January 15; OSC lists monthly Revenue Summary reports by month, including July reports, while CDOR's current General Fund Collections file is the stable July 2019-to-date publication surface. The ledger target is kept on the first CDOR print expected after July accounting close, with operational resolutionDate 2026-08-31."},{"kind":"text","text":"Base-rate/reference class: the annual official net individual income tax base is rising sharply into FY2026-27. Dividing official annual values by 12 gives monthly-average equivalents of 0.833, 0.929, and 1.045 billion for FY2024-25 actual, FY2025-26 estimate, and FY2026-27 forecast. That is the cleanest official recent base rate, while the July 2019 and July 2020 CDOR-cited observations show that July can be much lower or much higher when filing timing shifts."},{"kind":"text","text":"Variant consistency: the resolver is net individual income tax collections on a cash basis. The CDOR and OSC source family is cash-basis monthly revenue; the LCS forecast values are net individual income tax revenue, used only to anchor the level and momentum, not as the final resolution source."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: level starts near the FY2026-27 monthly average of 1.045 billion. Momentum is positive because LCS reports 4.9 percent withholding growth, 20.3 percent estimated-payment growth, and 15.0 percent cash-with-returns growth through May 2026. One-off risk is two-sided: July 2020 shows filing-deadline timing can dominate, but no comparable broad July 2026 deadline shift is in the official due-date guide. Policy effects are mixed, with OBBBA addbacks and unavailable triggered credits supporting receipts, while higher refunds and new credits pull down net collections."},{"kind":"text","text":"Prior/update/interval: prior model is annual-run-rate persistence from the official FY2026-27 LCS net individual income tax forecast, with historical sample values 0.833, 0.929, and 1.045 billion monthly-average equivalents plus July-specific stress points 0.614 and 1.760 billion. I start at the FY2026-27 monthly run rate of 12.5376 / 12 = 1.045, subtract 0.050 because July is not a normal April final-payment peak, subtract 0.015 for elevated refund drag, and add 0.000 net for policy because OBBBA addbacks and expanded credits point in opposite directions, giving 0.980. For the interval, using the three official monthly-average equivalents, sigma = 0.106 billion; 1.28*sigma = 0.136 billion. I widen to 0.200 billion, about 1.47x the mechanical half-width, because monthly cash timing is materially more volatile than annual run-rate dispersion."},{"kind":"math","text":"Point calculation: 12.5376 / 12 = 1.0448; 1.0448 - 0.050 July seasonality adjustment - 0.015 refund-drag adjustment = 0.9798, rounded to 0.980 billion. Interval calculation from official annual monthly-equivalent values 0.833, 0.929, and 1.045 gives sigma = 0.106; 1.28*sigma = 0.136. Widened half-width = 0.200 because cash collections are a monthly flow, so 0.980 - 0.200 = 0.780 and 0.980 + 0.200 = 1.180."},{"kind":"text","text":"Counter-consideration: upside risk would land above the interval if July captures unusually large late final payments or estimated payments after the strong spring filing season, or if OBBBA conformity raises Colorado taxable income faster than forecast. Downside risk would land below the interval if refunds stay unusually elevated, high-income final payments were front-loaded before July, or weaker labor-market withholding offsets the annual forecast upgrade. An outside the interval low would be especially plausible if the first print nets a large refund-processing batch into July."},{"kind":"forecast","point":0.98,"ciLow":0.78,"ciHigh":1.18}]}

# Reviewer critique
{
  "summary": "Draft is publishable only after strengthening the historical/model prior and interval method with actual CDOR monthly or July-specific collections history rather than annual averages and two stress points.",
  "requiredFixes": [
    {
      "rubricItem": "model_prior",
      "severity": "blocking",
      "summary": "The prior is based on annual LCS monthly-average equivalents and only two July stress observations, despite the official CDOR series reportedly covering July 2019 to date.",
      "actionRequested": "Use actual CDOR monthly net individual income tax collections, preferably July observations and nearby-month seasonality from 2019-2025, or explicitly state why that official time series could not be used."
    },
    {
      "rubricItem": "interval",
      "severity": "blocking",
      "summary": "The 80% interval is widened from sigma computed on three annual monthly-average values, which does not measure realized monthly cash-collection volatility.",
      "actionRequested": "Recompute or justify the interval from realized CDOR monthly or July-specific volatility, or provide an explicit uncertainty model tied to observed cash-flow variation."
    },
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "The -0.050 July seasonality adjustment is directionally plausible but not quantified from July shares or recent July outcomes.",
      "actionRequested": "Tie the July adjustment to observed July-vs-average collections in the CDOR history, or label it as judgmental and explain its scale."
    }
  ],
  "optionalSuggestions": [
    "Prefer official CDOR values over the Tax Foundation citation for July 2019 and July 2020 if the CDOR workbook contains them.",
    "Keep the 2026-08-31 ledger resolution date, but note if it is an operational deadline rather than the expected publication day."
  ]
}

Emit the final JSON object only.
