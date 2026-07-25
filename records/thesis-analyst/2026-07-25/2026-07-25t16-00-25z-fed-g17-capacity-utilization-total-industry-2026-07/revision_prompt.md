# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fed.g17.capacity_utilization.total_industry
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "fed-g17-capacity-utilization-total-industry-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "fed.g17.capacity_utilization.total_industry.2026-07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.federalreserve.gov"], "expectedReleaseWindow": {"end": "2026-08-21", "start": "2026-08-13"}, "field": "TCU", "releasePolicy": "first_print", "sourceSeriesId": "TCU", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TCU", "table": "G.17 Industrial Production and Capacity Utilization, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-25-a51d56b832ff97c356a370807bab06ccf4e39b9e37608915beb9eff4dac89265.json"
- targetContentHash: "a51d56b832ff97c356a370807bab06ccf4e39b9e37608915beb9eff4dac89265"
- registrationCommit: "add78fbd9af9ca9b0c7389a9a44a7ec839f2f4af"
- registeredAtUtc: "2026-07-25T15:18:08Z"

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

Emit the final JSON object only. (agent thesis.analyst v2.3.0, prompt 7ef119647b35, tools 5d0da8127872, promptMode fast)


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
{"slug":"fed-g17-capacity-utilization-total-industry-july-2026","country":"US","type":"data","title":"US Total Industry Capacity Utilization, July 2026","question":"Federal Reserve G.17 Capacity Utilization: Total industry, July 2026, seasonally adjusted percent of capacity, first print","unit":"percent","pointEstimate":76.14,"ciLow":75.62,"ciHigh":76.66,"confidence":0.8,"resolutionDate":"2026-08-18","resolutionSource":"Federal Reserve G.17 Industrial Production and Capacity Utilization, Table 7","resolutionSourceUrl":"https://www.federalreserve.gov/releases/g17/20260818/table7.htm","resolutionRule":"Resolve to the first official Federal Reserve G.17 July 2026 value for Table 7 Capacity Utilization, Total industry, seasonally adjusted percent of capacity, as first published on the August 18, 2026 release. Use the first-print value in percent, without later revisions; if only the one-decimal table value is available, use that official rounded value, otherwise use the corresponding first-print TCU value from the official/FRED-ALFRED release binding.","dataPointId":"fed.g17.capacity_utilization.total_industry.2026-07.first_print","historicalContext":[{"label":"2026-06 latest TCU","value":76.0937},{"label":"2026-05 TCU","value":76.1019},{"label":"2026-04 TCU","value":76.0625},{"label":"2026-03 TCU","value":75.5313},{"label":"2026-02 TCU","value":75.8299},{"label":"2026-01 TCU","value":75.242}],"drivers":["June total industry utilization was flat at 76.1 percent and 3.3 percentage points below its 1972-2025 average","manufacturing utilization edged down while mining and utilities rose in June","recent monthly TCU changes imply about 0.41 percentage point one-month dispersion","capacity growth and modest IP momentum point to little net July movement","upside risk from stronger utilities demand or another mining gain","downside risk from softer manufacturing output or reversal in mining/utilities"],"sourceContext":["https://www.federalreserve.gov/releases/g17/","https://www.federalreserve.gov/releases/g17/20260717/default.htm","https://www.federalreserve.gov/releases/g17/20260717/table7.htm","https://fred.stlouisfed.org/series/TCU","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TCU"],"runAt":"2026-07-25T16:00:46Z","reasoning":[{"kind":"heading","text":"US Total Industry Capacity Utilization, July 2026 First Print"},{"kind":"text","text":"Framing and exact resolver: this forecast is for Federal Reserve G.17 Table 7, Capacity Utilization, Total industry, seasonally adjusted percent of capacity, July 2026 first print. The ledger target uses series code TCU and first_print policy; FRED/ALFRED can mirror the history, but resolution should cite the Federal Reserve G.17 release."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 release calendar for 2026 monthly release dates","result":"The Federal Reserve G.17 page lists 2026 monthly releases including July 17 as the most recent monthly release and August 18, 2026 as the next monthly release at 9:15 a.m.; this verifies resolutionDate 2026-08-18 for July 2026 data."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 July 17, 2026 current release summary and Table 7","result":"The July 17, 2026 G.17 release says total capacity utilization was unchanged at 76.1 percent in June, 3.3 percentage points below its 1972-2025 average of 79.4; Table 7 shows total industry 2026 Jan 75.2, Feb 75.8, Mar 75.5, Apr 76.1, May 76.1, June 76.1."},{"kind":"tool","tool":"fred.lookup","call":"FRED/ALFRED TCU recent observations used as detailed public history mirror for the official G.17 series","result":"FRED TCU shows Jun 2026 76.0937, May 2026 76.1019, Apr 2026 76.0625, Mar 2026 75.5313, and Feb 2026 75.8299; updated July 17, 2026, with next release date August 18, 2026."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 July 2026 sector detail for current-release adjustment","result":"The June 2026 release reports total IP up 0.1 percent, manufacturing output unchanged, mining output up 0.4 percent, utilities output up 0.4 percent, manufacturing utilization 75.7, mining utilization 87.4, and utilities utilization 69.5."},{"kind":"text","text":"Reference class/base rate: for a one-month-ahead level forecast of a rate series, I anchor on persistence of the latest official/FRED TCU level and the recent same-series monthly changes, not on the long-run 79.4 average, because capacity utilization gaps tend to close slowly absent a large output shock."},{"kind":"text","text":"Level, momentum, and mechanism: the level anchor is June TCU 76.0937. Momentum is mildly positive because April-June stayed near 76.1 after a March dip, total IP still rose 0.1 percent in June, and mining/utilities rose 0.4 percent each; the offset is flat manufacturing output and manufacturing utilization easing to 75.7. I add only +0.05 percentage point for July because the target is a monthly rate and capacity growth mechanically dampens a small output increase."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest TCU 76.0937 from the official/FRED history; historical sample = detailed monthly TCU Dec 2025-Jun 2026 values 75.6422, 75.2420, 75.8299, 75.5313, 76.0625, 76.1019, 76.0937; adjustment components = +0.03 for recent IP/utilization momentum, +0.02 for mining/utilities strength, -0.00 for flat manufacturing net, so point = 76.0937 + 0.05 = 76.1437, rounded to 76.14. Interval method = sample standard deviation of successive monthly changes -0.4002, +0.5879, -0.2986, +0.5312, +0.0394, -0.0082; sigma = 0.411 percentage point, 80 percent half-width = 1.28*sigma = 0.526, so interval = 76.1437 +/- 0.526 = 75.62 to 76.66 after rounding."},{"kind":"text","text":"Counter-consideration: upside risk would come from a hot July utilities month plus another mining gain, which could push utilization above 76.66; downside risk would be a broad manufacturing pullback or a reversal in mining/utilities that would land below the interval. Outside the interval requires about a 0.57 percentage point rise or a 0.47 percentage point drop from the June detailed level, larger than most recent non-shock monthly moves."},{"kind":"forecast","point":76.14,"ciLow":75.62,"ciHigh":76.66}]}

# Reviewer critique
{
  "summary": "Draft is publishable with only a minor ordering/clarity fix around the stated prior.",
  "requiredFixes": [
    {
      "rubricItem": "base_rate",
      "severity": "warning",
      "summary": "The persistence/base-rate prior is present, but it appears after several current-evidence tool results and driver statements, so the reasoning order does not cleanly state the prior before inside-view updates.",
      "actionRequested": "Move or restate the persistence prior near the start of the reasoning before sector, IP, mining, utilities, or manufacturing update evidence is applied."
    }
  ],
  "optionalSuggestions": [
    "Mention that the official rounded Table 7 value may be one decimal while the ALFRED TCU binding preserves more decimals, and that the target remains percent either way.",
    "Keep the compact prior/update/interval paragraph; it satisfies the trace-depth requirements well."
  ]
}

Emit the final JSON object only.
