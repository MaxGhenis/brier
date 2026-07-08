# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.construction.output_mom_sa
- period: 2026-05
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "uk-construction-output-growth-may-2026"
- targetUnit: "percent_growth"

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
{"slug":"uk-construction-output-growth-may-2026","country":"UK","type":"data","title":"UK Construction Output Growth, May 2026","question":"What will the first ONS estimate of total construction output in Great Britain, seasonally adjusted chained volume measure, month-on-month percentage growth be for May 2026?","unit":"percent_growth","pointEstimate":0.1,"ciLow":-0.9,"ciHigh":1.1,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"Office for National Statistics Construction output in Great Britain: May 2026 and Output in the construction industry: all-work summary","resolutionSourceUrl":"https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/bulletins/constructionoutputingreatbritain/may2026","resolutionRule":"Resolve to the first ONS-published estimate for May 2026 monthly total construction output in Great Britain, seasonally adjusted chained volume measure, all work, month-on-month percentage growth, rounded to one decimal place. Use the value in the first Construction output in Great Britain: May 2026 release or its associated Output in the construction industry all-work summary dataset on 16 July 2026; ignore later revisions.","dataPointId":"ons.outputintheconstructionindustryallworksummary.total_construction_output_mom_sa.2026-05.first_print","historicalContext":[{"label":"2026-04 latest monthly growth","value":0.1},{"label":"2026-03 monthly growth","value":1.5},{"label":"2026-02 monthly growth","value":0.5},{"label":"2026-01 first monthly growth","value":0.2},{"label":"2025-12 monthly growth","value":-0.5},{"label":"2025-11 first monthly growth","value":-1.3},{"label":"2025-10 first monthly growth","value":-0.6},{"label":"2025-09 monthly growth","value":0.2},{"label":"2025-08 first monthly growth","value":-0.3},{"label":"2025-07 monthly growth","value":0.2}],"drivers":["April growth slowed to 0.1% after March's 1.5% financial-year push","three-month total output momentum was positive at 1.6% to April 2026","repair and maintenance was stronger than new work in April","Q1 2026 new orders fell 10.5%, limiting upside for new work","recent monthly volatility implies about 0.8 percentage-point sigma"],"sourceContext":["https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/bulletins/constructionoutputingreatbritain/latest","https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/datasets/outputintheconstructionindustryallworksummary","https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/bulletins/constructionoutputingreatbritain/previousreleases","https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/bulletins/constructionoutputingreatbritain/march2026newordersandconstructionoutputpriceindicesjanuarytomarch2026","https://www.ons.gov.uk/businessindustryandtrade/constructionindustry/bulletins/constructionoutputingreatbritain/september2025newordersandconstructionoutputpriceindicesjulytoseptember2025"],"runAt":"2026-07-08T16:57:27Z","reasoning":[{"kind":"heading","text":"UK construction output growth, May 2026 first print"},{"kind":"text","text":"Framing and exact resolver: target is ONS total construction output in Great Britain, all work, chained volume measure, seasonally adjusted, month-on-month percent growth for May 2026. I use the same SA all-work monthly growth variant for all anchors; the all-work summary dataset page is the table source, while the May 2026 bulletin is the first-print resolution page."},{"kind":"tool","tool":"official.lookup","call":"ONS latest construction output bulletin and all-work summary dataset schedule lookup","result":"The latest ONS construction output bulletin was for April 2026, released 12 June 2026, and both the bulletin and all-work summary dataset state the next release is 16 July 2026."},{"kind":"tool","tool":"official.lookup","call":"ONS April 2026 construction output bulletin main-points lookup","result":"Fetched latest same-variant values: monthly total construction output grew 0.1% in April 2026, after 1.5% in March 2026 and 0.5% in February 2026; three-month total output grew 1.6% to April 2026."},{"kind":"tool","tool":"official.lookup","call":"ONS March 2026 construction output bulletin lookup for components and orders","result":"Fetched March 2026 details: monthly total output grew 1.5%, new work grew 2.0%, repair and maintenance grew 0.8%, and Q1 2026 new orders fell 10.5% versus Q4 2025."},{"kind":"tool","tool":"official.lookup","call":"ONS previous releases lookup for recent monthly reference class","result":"Fetched same-variant recent monthly growth prints: July 2025 0.2%, August 2025 -0.3%, September 2025 0.2%, October 2025 -0.6%, November 2025 -1.3%, December 2025 -0.5%, January 2026 0.2%, February 2026 1.0%, March 2026 1.5%, April 2026 0.1%."},{"kind":"text","text":"Base rate/reference class: the recent official-source monthly all-work SA growth reference class is centered near flat, with mean 0.05% over the ten fetched monthly observations. I anchor near that base rate rather than extrapolating March's 1.5% because ONS described March as helped by financial year-end pushes and April already slowed to 0.1%."},{"kind":"text","text":"Current-release update: level and momentum are mildly positive because the three-month measure rose 1.6% and April did not reverse March's jump. One-off effect is negative because the March financial-year push should not repeat in May. Policy/mechanism pressure is slightly negative from Q1 new orders down 10.5%, but construction output can lag orders, so I do not make a large near-term cut."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior uses the ten ONS same-variant monthly growth values from July 2025 through April 2026: 0.2, -0.3, 0.2, -0.6, -1.3, -0.5, 0.2, 1.0, 1.5, 0.1. Mean = 0.05. sigma = 0.80 using sample standard deviation of those values themselves because this is already a change/flow series. 80% half-width = 1.28*sigma = 1.02. Point update: 0.05 base rate + 0.10 positive three-month momentum - 0.05 March one-off/new-orders drag = 0.10. Rounded 80% interval: 0.10 +/- 1.02 gives about -0.9 to 1.1."},{"kind":"text","text":"Counter-consideration: upside risk is a continued repair-and-maintenance surge plus resilient site activity, which would land above the interval if May prints above 1.1%. Downside risk is delayed work, weak private new housing, or order-book pass-through, which would land outside the interval below -0.9%."},{"kind":"forecast","point":0.1,"ciLow":-0.9,"ciHigh":1.1}]}

# Reviewer critique
{
  "summary": "The draft is publishable in structure but needs the February 2026 prior-sample inconsistency fixed before publication.",
  "requiredFixes": [
    {
      "rubricItem": "coherence",
      "severity": "blocking",
      "summary": "February 2026 is listed as 0.5% in historicalContext and in the April ONS main-points lookup, but the prior sample and math use 1.0%, changing the stated mean, sigma, and interval basis.",
      "actionRequested": "Use one clearly named vintage for the historical sample, correct the February value or label it as first-print if that is intentional, then recompute the mean, sigma, point-update arithmetic, and implied interval bounds."
    }
  ],
  "optionalSuggestions": [
    "State explicitly whether the prior sample uses latest revised prints available on 2026-07-08 or first-print values for each month.",
    "Tighten the tail scenarios by naming example components such as new work versus repair and maintenance for both upside and downside cases."
  ]
}

Emit the final JSON object only.
