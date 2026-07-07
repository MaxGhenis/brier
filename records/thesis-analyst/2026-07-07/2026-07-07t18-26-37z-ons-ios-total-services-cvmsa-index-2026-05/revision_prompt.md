# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.ios.total_services_cvmsa_index
- period: 2026-05
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "uk-index-of-services-may-2026"
- targetUnit: "index_points"

# Source hints
- Use ONS time-series pages, ONS API, and ONS release calendar.
- UK CPI/CPIH prints to one decimal; labour-market rates print to one decimal.
- Resolution source should be the relevant ONS release or time-series page.

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
{"slug":"uk-index-of-services-may-2026","country":"UK","type":"data","title":"UK Index of Services May 2026","question":"What will the Office for National Statistics report as the first-print Total Services chained-volume seasonally adjusted Index of Services index for May 2026, 2022=100, index points?","unit":"index_points","pointEstimate":104.7,"ciLow":104.1,"ciHigh":105.3,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"Office for National Statistics Index of Services, UK: May 2026","resolutionSourceUrl":"https://www.ons.gov.uk/economy/economicoutputandproductivity/output/bulletins/indexofservices/may2026","resolutionRule":"Resolve to the first ONS print for May 2026 in the Index of Services time series IOS1 or the ONS Index of Services main components and sectors table, using the Total Services chained-volume seasonally adjusted index, 2022=100, in index points. Use the first value published in the 16 July 2026 Index of Services, UK: May 2026 release and ignore later revisions.","dataPointId":"ons.ios.total_services_cvmsa_index.2026-05.first_print","historicalContext":[{"label":"Apr 2026 official monthly growth, percent","value":-0.2},{"label":"Mar 2026 official monthly growth, percent","value":0.3},{"label":"Feb 2026 official monthly growth, percent","value":0.5},{"label":"Jan 2026 official monthly growth, percent","value":0},{"label":"Dec 2025 official monthly growth, percent","value":0.3},{"label":"Nov 2025 official monthly growth, percent","value":0.3}],"drivers":["April services fallback creates modest rebound base","Q1 2026 services momentum was positive","May first print will incorporate wider national-accounts revisions back to January 2024","Middle East conflict note in April release adds downside uncertainty","Service-sector source mix is broad, with MBS at 34.9 percent of GVA weight"],"sourceContext":["https://www.ons.gov.uk/economy/economicoutputandproductivity/output/bulletins/indexofservices/latest","https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/indexofservices","https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/indexofservicesandmaincomponentsto4dp","https://www.ons.gov.uk/economy/economicoutputandproductivity/output/bulletins/indexofservices/march2026","https://www.ons.gov.uk/economy/economicoutputandproductivity/output/bulletins/indexofservices/february2026","https://www.ons.gov.uk/economy/economicoutputandproductivity/output/bulletins/indexofservices/december2025"],"runAt":"2026-07-07T18:28:05Z","reasoning":[{"kind":"heading","text":"UK total services CVMSA index, May 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this forecast targets the ONS Total Services chained-volume seasonally adjusted Index of Services index, 2022=100, for May 2026, not a gross, non-seasonally adjusted, quarterly, or revised-vintage variant. The ONS dataset identifier used for the time-series page is IOS1; the related detailed table is the Index of Services main components and sectors to four decimal places."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Index of Services, UK: April 2026 latest bulletin for release timing and current first-print context.","result":"Fetched release date 12 June 2026, next release 16 July 2026, April 2026 monthly services output -0.2%, three months to April 2026 +0.8%, and previous three months to March 2026 +0.8%."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS IOS1 dataset page and four-decimal main-components dataset page for dataset identity and next-release metadata.","result":"Fetched IOS1 dataset released 12 June 2026, next release 16 July 2026; four-decimal components dataset released 12 June 2026, next release 16 July 2026, with April 2026, March 2026, and February 2026 editions listed."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS March 2026, February 2026, January 2026, and December 2025 Index of Services bulletins for recent official-source reference class.","result":"Fetched monthly services output changes: March 2026 +0.3%, February 2026 +0.5%, January 2026 0.0%, December 2025 +0.3%, November 2025 +0.1% in the December bulletin vintage, and Q1 2026 +0.8% versus Q4 2025."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS November 2025 and October 2025 Index of Services bulletins for additional recent official monthly movement history.","result":"Fetched November 2025 monthly services output +0.3%, October 2025 monthly services output -0.3%, September 2025 monthly services output +0.2%, and three months to November 2025 +0.2%."},{"kind":"tool","tool":"official.lookup","call":"Checked ONS April 2026 bulletin data-source and quality lines for mechanism and uncertainty context.","result":"Fetched April 2026 response rates 70.2% by forms returned and 84.3% by turnover coverage; ONS listed MBS 34.9%, Retail Sales Inquiry 4.8%, government expenditure 15.3%, households expenditure 11.2%, finance expenditure 8.0%, NPISH 1.9%, and other 3.6% as IoS data-source weights."},{"kind":"text","text":"Base rate/reference class: for this level series I anchor the one-month-ahead change on recent ONS monthly IoS movements, where the latest eight readings are small but not noise-free: +0.2, -0.3, +0.3, +0.3, 0.0, +0.5, +0.3, and -0.2 percent from September 2025 through April 2026. That supports a mild positive mean, but April's fall and the announced national-accounts revision window argue against extrapolating the strong Q1 run fully."},{"kind":"math","text":"Prior/update/interval: persistence prior is April 2026 total-services index level carried forward, with an approximate current level anchor of 104.6 index points inferred for the 2022=100 total-services index scale; historical sample is the official recent monthly movements +0.2, -0.3, +0.3, +0.3, 0.0, +0.5, +0.3, -0.2 converted near a 104 index level to index-point changes of +0.21, -0.31, +0.31, +0.31, +0.00, +0.52, +0.31, -0.21. The sample standard deviation of those successive changes gives sigma = 0.29 index points, so a mechanical 80% half-width is about 1.28*sigma = 0.37. I widen to 0.60 because the May first print will arrive with revisions open back to January 2024 and because April had a stated disruption-related fall. Point update is +0.1 index point from April persistence, so 104.6 + 0.1 = 104.7, with 80% interval 104.1 to 105.3."},{"kind":"text","text":"Level, momentum, one-off, and policy-mechanism effects: the level prior is a total-services index a little above 104 on a 2022=100 basis; momentum from Q1 and the three months to April is positive; the April monthly fall is treated as partly one-off; policy effects are indirect and small over a one-month horizon, mainly through public-service volumes and household-facing services rather than an explicit policy-rate rule."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in administrative support, wholesale and retail, or information and communication after April's drop, which would land above the interval if May prints around +0.7% or more on the month. Downside risk is a broader conflict- or demand-related services pullback, especially in consumer-facing and business services, which would land below the interval if May falls around -0.6% or more. A large benchmark or seasonal-adjustment interaction in the July release could also put the first-print level outside the interval even with ordinary May activity."},{"kind":"forecast","point":104.7,"ciLow":104.1,"ciHigh":105.3}]}

# Reviewer critique
{"summary":"Draft is publishable with only minor tightening: resolver/date/source and forecast JSON are coherent, but the level anchor and interval widening need clearer provenance.","requiredFixes":[{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact step uses an 'approximate current level anchor of 104.6' without naming the exact observed April 2026 index value or the source/table field used to obtain it.","actionRequested":"State the April 2026 first-print Total Services CVMSA index level, or explicitly say it is reconstructed from recent growth rates and identify the starting value/source used for that reconstruction."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval starts from realized recent monthly volatility, but the widening from 0.37 to 0.60 index points is qualitative and mixes ordinary May uncertainty with July benchmark/revision risk.","actionRequested":"Add one sentence quantifying or bounding the extra revision/benchmark allowance, or label it as a judgmental add-on beyond the recent-growth volatility estimate."}],"optionalSuggestions":["Replace vague driver wording like 'April services fallback' with 'April services fall' or 'April pullback'.","If available, name the exact IOS1 time-series/table row used for Total Services CVMSA to reduce resolver ambiguity."]}

Emit the final JSON object only.
