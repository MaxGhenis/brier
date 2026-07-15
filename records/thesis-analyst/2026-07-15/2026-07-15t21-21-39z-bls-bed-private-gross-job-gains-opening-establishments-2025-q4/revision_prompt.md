# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.bed.private_gross_job_gains.opening_establishments
- period: 2025-Q4
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bls-bed-opening-establishment-gross-job-gains-q4-2025"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "bls.bed.private_gross_job_gains.opening_establishments.2025_q4.first_print"
- resolutionSourceUrl: "https://www.bls.gov/news.release/cewbd.toc.htm"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bls.gov"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-29"}, "field": "Gross job gains at opening establishments; private sector; seasonally adjusted", "releasePolicy": "first_print", "sourceSeriesId": "BLS BED Table 1", "sourceUrl": "https://www.bls.gov/news.release/cewbd.toc.htm", "table": "Business Employment Dynamics, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-15-0da8b2bfeb748c0bd47c8b30aed2a4ac58581d3c578ffd0c870928a8c55d9740.json"
- targetContentHash: "0da8b2bfeb748c0bd47c8b30aed2a4ac58581d3c578ffd0c870928a8c55d9740"
- registrationCommit: "4ca8bf2478e8cea37b8112b8821dc9865efdce9c"
- registeredAtUtc: "2026-07-15T21:20:34Z"

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
{"slug":"bls-bed-opening-establishment-gross-job-gains-q4-2025","country":"US","type":"data","title":"US opening-establishment job gains, Q4 2025","question":"What will BLS first report for private-sector gross job gains at opening establishments in 2025 Q4, seasonally adjusted, in thousands?","unit":"thousands","pointEstimate":1635,"ciLow":1583,"ciHigh":1687,"confidence":0.8,"resolutionDate":"2026-07-29","resolutionSource":"U.S. Bureau of Labor Statistics Business Employment Dynamics release","resolutionSourceUrl":"https://www.bls.gov/news.release/cewbd.toc.htm","resolutionRule":"Resolve to the first value published for 2025 Q4 in BLS Business Employment Dynamics Table 1, Gross job gains—Opening establishments—Total private, seasonally adjusted, in thousands. Use the displayed integer value, equivalent to rounding to the nearest thousand jobs, and ignore all subsequent revisions.","dataPointId":"bls.bed.private_gross_job_gains.opening_establishments.2025_q4.first_print","historicalContext":[{"label":"2023-Q1","value":1570},{"label":"2023-Q2","value":1608},{"label":"2023-Q3","value":1586},{"label":"2023-Q4","value":1637},{"label":"2024-Q1","value":1531},{"label":"2024-Q2","value":1561},{"label":"2024-Q3","value":1564},{"label":"2024-Q4","value":1660},{"label":"2025-Q1","value":1589},{"label":"2025-Q2","value":1527},{"label":"2025-Q3","value":1597}],"drivers":["Recent rebound from 1,527 thousand to 1,597 thousand","Recent Q4 prints of 1,637 thousand and 1,660 thousand","Soft 2025 gross-job-gain environment","Opening-establishment volatility around a stable 1.6 million level"],"sourceContext":["https://www.bls.gov/news.release/cewbd.t01.htm","https://www.bls.gov/schedule/news_release/cewbd.htm","https://www.bls.gov/news.release/archives/cewbd_02262026.pdf"],"runAt":"2026-07-15T21:22:05Z","reasoning":[{"kind":"heading","text":"BLS opening-establishment gross job gains, 2025 Q4"},{"kind":"text","text":"The target is BLS BED Table 1, total-private gross job gains at opening establishments, seasonally adjusted and measured in thousands—not the opening-firm series or an unadjusted variant. Resolution uses the strict first 2025-Q4 print without correction-day or revision exceptions."},{"kind":"tool","tool":"official.lookup","call":"Fetch recent observations from BLS BED Table 1.","result":"BLS reports opening-establishment gross job gains of 1,589 thousand in 2025 Q1, 1,527 thousand in Q2, and 1,597 thousand in Q3, seasonally adjusted."},{"kind":"tool","tool":"official.lookup","call":"Fetch the pre-2025 reference class from BLS BED Table 1.","result":"The 2024 quarterly values were 1,531, 1,561, 1,564, and 1,660 thousand; the 2023 values were 1,570, 1,608, 1,586, and 1,637 thousand."},{"kind":"tool","tool":"official.lookup","call":"Check related total gross job gains and the official release schedule.","result":"Total private gross job gains were 7,448 thousand in 2025 Q1, 7,585 thousand in Q2, and 7,475 thousand in Q3; the BLS calendar schedules the 2025 Q4 BED release for July 29, 2026 at 10:00 AM."},{"kind":"text","text":"The outside-view base rate is the recent 2023-Q1 through 2025-Q3 reference class: opening-establishment gains have centered near 1.585 million, while the two latest Q4 observations were higher at 1.637 million and 1.660 million."},{"kind":"text","text":"Level and momentum point in different directions: the series remains near 1.6 million and rebounded 70 thousand in Q3, but total gross gains eased from 7.585 million to 7.475 million. Recent Q4 strength supports an elevated anchor, while the softer 2025 labor-flow backdrop warrants a modest downward adjustment. No discrete policy or identifiable one-off mechanism justifies a larger shift."},{"kind":"math","text":"Prior/update/interval: A recent-Q4 persistence model uses the 2023-Q4 and 2024-Q4 average, (1,637 + 1,660) / 2 = 1,648.5 thousand, based on the 11-quarter 2023-Q1–2025-Q3 historical sample. Apply a -13.5 thousand adjustment for softer 2025 total gross gains, giving 1,635.0. Because this is a flow series, dispersion is computed from the values themselves: sample sigma = 40.7 thousand. The normal 80% half-width is 1.28*sigma = 1.28*40.7 = 52.1 thousand, implying 1,635 ± 52, or final bounds of 1,583 to 1,687 thousand."},{"kind":"text","text":"Upside risk comes from another Q4 opening surge comparable to or stronger than 2024 and would land above the interval if the first print exceeds 1,687 thousand. Downside risk comes from broad-based establishment-formation weakness or reversal of the Q3 rebound and would land below the interval if the print is under 1,583 thousand."},{"kind":"forecast","point":1635,"ciLow":1583,"ciHigh":1687}]}

# Reviewer critique
{
  "summary": "The draft is publishable: resolver, first-print rule, priors, interval math, tails, and JSON fields are coherent with the ledger target.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Consider stating explicitly whether the 40.7 thousand sigma is computed from all 11 listed observations to remove any ambiguity.",
    "The -13.5 thousand downward adjustment is acceptable, but could be made slightly more auditable by naming it as the sole adjustment component."
  ]
}

Emit the final JSON object only.
