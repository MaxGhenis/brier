# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fed.g19.consumer_credit_revolving_annual_rate
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-revolving-consumer-credit-annual-rate-june-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "fed.g19.consumer_credit_revolving_annual_rate.2026_06.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-07", "start": "2026-08-07"}, "field": "REVOLSLAR", "releasePolicy": "first_print", "sourceSeriesId": "REVOLSLAR", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=REVOLSLAR", "table": "G.19 Consumer Credit, outstanding, seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-cec067d33e053f0a17dfd4f1ee060bd6b882769ef9a08ee35f3d7cb0a5dbd4e8.json"
- targetContentHash: "cec067d33e053f0a17dfd4f1ee060bd6b882769ef9a08ee35f3d7cb0a5dbd4e8"
- registrationCommit: "145f6612f225710a4621f124b13bf5d5ae5d97ac"
- registeredAtUtc: "2026-07-26T00:55:04Z"

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

Emit the final JSON object only. (agent thesis.analyst v2.4.0, prompt 7ef119647b35, tools 50a06b62f9be, promptMode fast)


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
{"slug":"us-revolving-consumer-credit-annual-rate-june-2026","country":"US","type":"data","title":"US revolving credit growth, Jun 2026","question":"Federal Reserve G.19 percent change of total revolving consumer credit (REVOLSLAR), June 2026, seasonally adjusted annual rate, first print.","unit":"percent_growth","pointEstimate":3.8,"ciLow":-2.6,"ciHigh":10.2,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"Federal Reserve Board G.19 Consumer Credit statistical release","resolutionSourceUrl":"https://www.federalreserve.gov/releases/g19/20260807/","resolutionRule":"Resolve to the first official Federal Reserve G.19 Consumer Credit print for June 2026 in the Consumer Credit Outstanding table, seasonally adjusted, row Revolving under Total percent change (annual rate), series REVOLSLAR. Use the value as first posted on the August 7, 2026 release; ignore later revisions. Record in percent growth at annual rate, using the official displayed precision or the unrounded first-vintage REVOLSLAR value if the release data file exposes more precision.","dataPointId":"fed.g19.consumer_credit_revolving_annual_rate.2026_06.first_print","historicalContext":[{"label":"May 2026 REVOLSLAR latest","value":-4.71},{"label":"April 2026 REVOLSLAR","value":10.36},{"label":"March 2026 REVOLSLAR","value":9.66},{"label":"February 2026 REVOLSLAR","value":1.03},{"label":"January 2026 REVOLSLAR","value":1.64}],"drivers":["revolving credit annualized monthly growth is volatile","March and April strength partly reversed in May","credit-card borrowing remains constrained by elevated rates","June forecast uses current-regime dispersion rather than cadence inference"],"sourceContext":["https://www.federalreserve.gov/newsevents/2026-august.htm","https://www.federalreserve.gov/releases/g19/current/default.htm","https://fred.stlouisfed.org/data/REVOLSLAR","https://www.federalreserve.gov/releases/g19/about.htm"],"runAt":"2026-07-26T01:16:27Z","reasoning":[{"kind":"heading","text":"US revolving consumer credit annual-rate forecast for June 2026"},{"kind":"text","text":"Framing and exact resolver: the target is Federal Reserve G.19 Consumer Credit, series REVOLSLAR, the seasonally adjusted annual-rate percent change of total revolving consumer credit for June 2026, first print. All anchors use the same seasonally adjusted annual-rate percent-change variant; the Board G.19 page is the agency resolver and FRED/ALFRED is only a history mirror for REVOLSLAR."},{"kind":"tool","tool":"official.lookup","call":"Checked the Federal Reserve August 2026 statistical release calendar for G.19 Consumer Credit.","result":"The Federal Reserve August 2026 calendar lists Statistical Releases with G.19 - Consumer Credit at 3:00 p.m. on release date 7, verifying the 2026-08-07 resolution date."},{"kind":"tool","tool":"official.lookup","call":"Read the Federal Reserve current G.19 release table for the latest same-variant observations.","result":"The July 8, 2026 G.19 release covers May 2026; the seasonally adjusted annual-rate Revolving row shows May -4.7, Apr 10.4, Mar 9.7, Q1 2026 4.1, and 2025 3.1 percent."},{"kind":"tool","tool":"history.lookup","call":"Read FRED table data for REVOLSLAR as a public mirror of Board G.19 history.","result":"REVOLSLAR recent observations are May 2026 -4.71, Apr 2026 10.36, Mar 2026 9.66, Feb 2026 1.03, Jan 2026 1.64; 2025 monthly values include Dec 7.04 and Nov -0.70."},{"kind":"tool","tool":"methodology.lookup","call":"Checked the Federal Reserve G.19 about page for how annual growth rates are calculated.","result":"The G.19 methodology says percent changes and levels are calculated from unrounded data; revolving credit is a major type of credit, and the table reports annual growth rates, levels, and flows of outstanding credit."},{"kind":"text","text":"Base rate / reference class: in the current post-2023 regime, monthly REVOLSLAR values are centered around low single-digit growth but have sharp monthly reversals. The 2024-Jan through 2026-May sample has mean about 3.96, while the latest five months average 3.60, so a point forecast near 3.8 keeps the base rate while not chasing May's -4.71 print."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior is the 2024-Jan through 2026-May REVOLSLAR sample, n = 29, mean = 3.96; current-release adjustment is -0.2 for May weakness after Mar 9.66 and Apr 10.36 strength, plus about 0.0 for policy/rate mechanism because credit-card rates remain high but stable. For this change-rate series I size uncertainty from the values themselves: sigma = 4.96, so the 80% half-width is 1.28*sigma = 1.28*4.96 = 6.35. Point = 3.8; interval = 3.8 +/- 6.35 = [-2.55, 10.15], rounded to [-2.6, 10.2]."},{"kind":"text","text":"Counter-considerations: upside risk is another rebound like March-April if card balances recover after May's paydown, which would land above the interval if annualized revolving growth exceeds 10.2. Downside risk is a second consecutive contraction from deleveraging or tighter card credit, which would land below the interval if growth is below -2.6. Outside the interval would require a monthly swing larger than typical current-regime dispersion, not just normal noise."},{"kind":"forecast","point":3.8,"ciLow":-2.6,"ciHigh":10.2}]}

# Reviewer critique
{
  "summary": "Draft is methodologically coherent, but its resolver/source fields conflict with the canonical ledger sourceBinding.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft resolves to the Federal Reserve release URL and says ALFRED/FRED is only a history mirror, while the canonical ledger contract binds this target to the alfred-fred adapter, allowed host alfred.stlouisfed.org, sourceSeriesId REVOLSLAR, and sourceUrl https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=REVOLSLAR.",
      "actionRequested": "Align resolutionSource, resolutionSourceUrl, resolutionRule, and sourceContext with the ledger sourceBinding, or explicitly state in reasoning that the ledger resolver binding appears inconsistent with the official-agency preference while keeping the published fields tied to the canonical target."
    }
  ],
  "optionalSuggestions": [
    "Add one sentence saying the 2024-Jan through 2026-May sample was chosen as the current-rate-regime reference class rather than a longer pre-2024 sample.",
    "State whether the interval sigma is the sample standard deviation of monthly annual-rate values, not forecast-error volatility, to remove any ambiguity."
  ]
}

Emit the final JSON object only.
