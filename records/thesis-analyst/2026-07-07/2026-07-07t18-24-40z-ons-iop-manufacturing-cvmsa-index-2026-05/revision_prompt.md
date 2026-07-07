# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.iop.manufacturing_cvmsa_index
- period: 2026-05
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "uk-manufacturing-output-index-may-2026"
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
{"slug":"uk-manufacturing-output-index-may-2026","country":"UK","type":"data","title":"UK manufacturing output index, May 2026","question":"ONS Index of Production series K22A, C: manufacturing chained volume measure seasonally adjusted index, May 2026, first print","unit":"index_points","pointEstimate":101.6,"ciLow":100.3,"ciHigh":102.9,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"Office for National Statistics Index of Production, UK: May 2026 and DIOP time series K22A","resolutionSourceUrl":"https://www.ons.gov.uk/economy/economicoutputandproductivity/output/timeseries/k22a/diop","resolutionRule":"Resolve to the first ONS-published value for 2026 MAY in time series K22A, IOP: C:MANUFACTURING: CVMSA, index base year 2023=100, rounded to one decimal as published in the first Index of Production, UK: May 2026 release. Ignore later revisions or corrections unless the first release itself is withdrawn before publication.","dataPointId":"ons.iop.manufacturing_cvmsa_index.2026-05.first_print","historicalContext":[{"label":"2026 APR latest K22A","value":101.5},{"label":"2026 MAR K22A","value":101.1},{"label":"2026 FEB K22A","value":99.9},{"label":"2026 JAN K22A","value":100.1},{"label":"2025 DEC K22A","value":100.0}],"drivers":["April 2026 level already above recent average","recent manufacturing three-month growth positive","monthly K22A changes remain noisy around a flat base rate","May first print may be affected by wider revisions opened back to January 2024"],"sourceContext":["https://www.ons.gov.uk/economy/economicoutputandproductivity/output/timeseries/k22a/diop","https://www.ons.gov.uk/releases/indexofproductionukmay2026","https://www.ons.gov.uk/economy/economicoutputandproductivity/output/bulletins/indexofproduction/april2026"],"runAt":"2026-07-07T18:25:05Z","reasoning":[{"kind":"heading","text":"UK manufacturing output index, May 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this forecast targets ONS DIOP time series K22A, labelled IOP: C:MANUFACTURING: CVMSA. All anchors use the same chained volume measure, seasonally adjusted manufacturing index variant, base year 2023=100, not gross, non-seasonally adjusted, smoothed, or synthetic variants."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS K22A time-series page for DIOP manufacturing CVMSA index.","result":"The ONS page identified Series ID K22A, units index base year = 100, release date 12 June 2026, next release 16 July 2026, and recent monthly values 2026 JAN 100.1, 2026 FEB 99.9, 2026 MAR 101.1, 2026 APR 101.5."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS release page for Index of Production, UK: May 2026.","result":"The ONS release page gives the release date as 16 July 2026 at 7:00am and states the May 2026 release is not yet published as of this run."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS Index of Production, UK: April 2026 bulletin for latest official context.","result":"ONS reported April 2026 manufacturing up 0.4% on the month, production output 0.0% on the month, manufacturing up 0.6% in the three months to April 2026, and 8 of 13 manufacturing subsectors increased in April."},{"kind":"tool","tool":"official.lookup","call":"Read the official K22A monthly history from January 2022 through April 2026 on the ONS time-series page.","result":"Reference class values include 2022 JAN 99.3, 2023 JAN 99.1, 2024 JAN 100.6, 2025 JAN 99.0, 2026 JAN 100.1, and latest 2026 APR 101.5; the 51 monthly successive changes from 2022 FEB to 2026 APR sum to +2.2 index points."},{"kind":"text","text":"Base rate / reference class: the outside-view prior is persistence plus the 2022 JAN to 2026 APR K22A monthly-change distribution. That sample is centered close to flat, with mean monthly change about +0.04 index points, so the base rate alone would put May near 101.5 to 101.6."},{"kind":"text","text":"Level and momentum update: the latest level, 101.5 in April 2026, is above the 2025 annual value of 99.6 and the 2023 base of 100.0, while recent official momentum is positive: 99.9 in February, 101.1 in March, and 101.5 in April. I apply only a small positive current-release adjustment because the series is noisy and April already followed a large March rise."},{"kind":"math","text":"Prior/update/interval: persistence prior on K22A April 2026 = 101.5; historical sample = monthly K22A successive changes from 2022 FEB through 2026 APR, n = 51, mean change = +0.04, sum of changes = +2.2, sum of squared changes = 51.02; adjustment components = +0.04 base-rate drift, +0.10 recent manufacturing momentum, -0.04 mean reversion from the elevated April level, giving point 101.5 + 0.10 = 101.6. Interval method uses realized dispersion of successive level changes: sigma = 1.01, so 80% half-width is roughly 1.28*sigma = 1.29, rounded to 1.3 index points; 101.6 - 1.3 = 100.3 and 101.6 + 1.3 = 102.9."},{"kind":"text","text":"Counter-considerations: upside risk is a broad May gain across pharmaceuticals, electronics, and metals after April's 8 of 13 subsectors rising, which would land above the interval if K22A prints above 102.9. Downside risk is reversal in those volatile subsectors or a weak transport/electrical-equipment drag, which would land below the interval if K22A prints below 100.3. Outside the interval would most likely require a move larger than the recent monthly-change reference class expects or a revision-linked first-print discontinuity."},{"kind":"forecast","point":101.6,"ciLow":100.3,"ciHigh":102.9}]}

# Reviewer critique
{"summary":"Draft is publication-ready with no blocking fixes identified.","requiredFixes":[],"optionalSuggestions":["In the compact prior/update step, explicitly say the interval is for the May first-print level, not a revised later vintage.","If space allows, name whether the 2022-2026 volatility calculation uses population or sample standard deviation, though the current bounds are coherent."]}

Emit the final JSON object only.
