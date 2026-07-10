# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.productivity.nonfarm_qoq_prelim
- period: 2026-Q3
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-nonfarm-productivity-q3-2026-prelim"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.productivity.nonfarm_qoq_prelim.2026_q3.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-11-13", "start": "2026-10-30"}, "field": "bls.productivity.nonfarm_qoq_prelim", "releasePolicy": "first_print", "sourceSeriesId": "bls.productivity.nonfarm_qoq_prelim", "sourceUrl": "https://www.bls.gov/news.release/prod2.t02.htm", "table": "U.S. Bureau of Labor Statistics Productivity and Costs news release, Table 2", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-305e7cc4fb0cea02fc06d094b277fc0b19edb85507cbcefe73e0b64e7d6e02df.json"
- targetContentHash: "305e7cc4fb0cea02fc06d094b277fc0b19edb85507cbcefe73e0b64e7d6e02df"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"

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
{"slug":"us-nonfarm-productivity-q3-2026-prelim","country":"US","type":"data","title":"US Nonfarm Productivity Q3 2026 Preliminary","question":"What will BLS first report for nonfarm business sector labor productivity, seasonally adjusted percent change from previous quarter at annual rate, in 2026 Q3 preliminary Table 2?","unit":"percent_growth","pointEstimate":1.7,"ciLow":-1.7,"ciHigh":5.1,"confidence":0.8,"resolutionDate":"2026-11-05","resolutionSource":"U.S. Bureau of Labor Statistics Productivity and Costs news release, Table 2","resolutionSourceUrl":"https://www.bls.gov/news.release/prod2.t02.htm","resolutionRule":"Resolve to the first BLS Productivity and Costs preliminary release for Third Quarter 2026, Table 2, Nonfarm business sector, row 2026 III, Labor productivity, seasonally adjusted percent change from previous quarter at annual rate. Use the one-decimal value printed in the first official release on 2026-11-05 and do not apply later revised releases.","dataPointId":"bls.productivity.nonfarm_qoq_prelim.2026_q3.first_print","historicalContext":[{"label":"2026 Q1 revised, BLS/FRED PRS85006092","value":0.3},{"label":"2025 Q4 revised, BLS/FRED PRS85006092","value":1.6},{"label":"2025 Q3 revised, BLS/FRED PRS85006092","value":5.2},{"label":"2025 Q2 revised, BLS/FRED PRS85006092","value":4.2},{"label":"2021Q1-2026Q1 revised-history sigma used for interval","value":2.64}],"drivers":["Recent revised productivity slowed to 0.3 percent in 2026 Q1 after strong 2025 readings","Post-2021 reference class remains volatile but centered near 1.5 percent annualized","Q3 first print will depend on early GDP/output and hours estimates available to BLS in November","AI/capital-deepening narrative supports a modest positive trend but not a large near-term jump"],"sourceContext":["https://www.bls.gov/schedule/news_release/prod2.htm","https://www.bls.gov/news.release/prod2.t02.htm","https://fred.stlouisfed.org/series/PRS85006092","https://fred.stlouisfed.org/data/PRS85006092"],"runAt":"2026-07-10T05:42:00Z","reasoning":[{"kind":"heading","text":"US nonfarm business labor productivity, 2026 Q3 preliminary first print"},{"kind":"text","text":"Framing and exact resolver: target is BLS Productivity and Costs Table 2, nonfarm business sector Labor productivity, seasonally adjusted percent change from previous quarter at an annual rate, for 2026 Q3 preliminary. The FRED/BLS series code used for history is PRS85006092; resolution remains the BLS first-print Table 2, not FRED."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Productivity and Costs release schedule for the Third Quarter 2026 preliminary release.","result":"BLS schedule lists Third Quarter 2026 (P) on Nov. 05, 2026 at 08:30 AM and Third Quarter 2026 (R) on Dec. 08, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Fetched current BLS Productivity and Costs Table 2 for nonfarm business sector labor productivity and components.","result":"BLS Table 2 shows 2026 Q1 labor productivity 0.3, output 1.0, hours worked 0.7; 2025 Q4 labor productivity 1.6, 2025 Q3 5.2, 2025 Q2 4.2, 2025 Q1 -0.9."},{"kind":"tool","tool":"history.lookup","call":"Fetched FRED mirror of BLS PRS85006092, Percent Change at Annual Rate, Seasonally Adjusted, quarterly.","result":"FRED PRS85006092 reports Q1 2026 0.3, Q4 2025 1.6, Q3 2025 5.2, Q2 2025 4.2, Q1 2025 -0.9; the date range is 1947-04-01 to 2026-01-01 and last updated 2026-06-04 7:41 AM CDT."},{"kind":"tool","tool":"history.lookup","call":"Read recent BLS/FRED history for the post-2020 reference class used to size uncertainty.","result":"For 2021Q1-2026Q1 PRS85006092 values are 2.9, 0.8, -2.4, 2.3, -4.9, -2.9, 0.2, 2.3, 0.9, 4.1, 5.1, 3.9, 0.2, 3.7, 3.7, 1.4, -0.9, 4.2, 5.2, 1.6, 0.3."},{"kind":"text","text":"Base rate/reference class: the post-2020 nonfarm business productivity values average about 1.5 percent annualized, while the 2023-2025 subset is stronger at about 2.8 percent. I put more weight on the broader post-2020 base rate because quarterly productivity first prints are noisy and 2025 likely included tariff and inventory timing effects."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class prior is the 2021Q1-2026Q1 PRS85006092 mean, 31.7/21 = 1.51. I add +0.2 for moderate trend productivity and likely normalization after the weak 2026 Q1 print, giving point = 1.7. For this change-rate series I compute sigma from the fetched values themselves: squared deviations from 1.51 sum to about 146.4, variance = 146.4/21 = 6.97, sigma = 2.64. The 80 percent normal half-width is roughly 1.28*sigma = 1.28*2.64 = 3.38, so 1.7 +/- 3.4 gives -1.7 to 5.1 after one-decimal rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a Q3 output rebound with flat or falling hours, which would land above the interval if productivity prints above 5.1. Downside risk is weak real output with continued hours growth, which would land below the interval if productivity prints below -1.7. A large inventory/tariff timing swing or a recession-style hours adjustment is the main outside the interval scenario."},{"kind":"forecast","point":1.7,"ciLow":-1.7,"ciHigh":5.1}]}

# Reviewer critique
{"summary":"Draft is publishable with no blocking issues; resolver, first-print rule, point, interval, and JSON fields are coherent, with only minor clarity improvements recommended.","requiredFixes":[],"optionalSuggestions":["Clarify that the 2021Q1-2026Q1 history uses revised BLS/FRED values as a proxy for first-print volatility, or switch to first-print vintage history if available.","State explicitly that no separate AR or econometric time-series model was used beyond the reference-class/persistence prior.","Tighten the +0.2 adjustment by separating the weak-Q1 mean-reversion component from the AI/capital-deepening trend component."]}

Emit the final JSON object only.
