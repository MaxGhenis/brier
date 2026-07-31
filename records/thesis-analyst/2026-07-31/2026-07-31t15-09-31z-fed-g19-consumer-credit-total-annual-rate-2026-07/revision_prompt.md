# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fed.g19.consumer_credit_total_annual_rate
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-consumer-credit-annual-rate-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "fed.g19.consumer_credit_total_annual_rate.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-09-11", "start": "2026-09-03"}, "field": "TOTALSLAR", "releasePolicy": "first_print", "sourceSeriesId": "TOTALSLAR", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TOTALSLAR", "table": "G.19 Consumer Credit, outstanding, seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-e9da62e6d1dd2f607aa873c6707f868a06e2aec454f41f214170fcead022a76d.json"
- targetContentHash: "e9da62e6d1dd2f607aa873c6707f868a06e2aec454f41f214170fcead022a76d"
- registrationCommit: "0249a6f266d1d202c43782056e77403612358765"
- registeredAtUtc: "2026-07-31T14:48:09Z"

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
{"slug":"us-consumer-credit-annual-rate-july-2026","country":"US","type":"data","title":"US consumer credit annual rate, July 2026","question":"What will the Federal Reserve G.19 first-print total consumer credit percent change at an annual rate, seasonally adjusted, be for July 2026?","unit":"percent_growth","pointEstimate":2.4,"ciLow":-0.2,"ciHigh":5.0,"confidence":0.8,"resolutionDate":"2026-09-08","resolutionSource":"Federal Reserve Board G.19 Consumer Credit statistical release","resolutionSourceUrl":"https://www.federalreserve.gov/releases/g19/20260908/","resolutionRule":"Resolve to the first-print Federal Reserve G.19 Consumer Credit value for TOTALSLAR, Total percent change at an annual rate, seasonally adjusted, for observation month July 2026. Use the first official September 8, 2026 print only, with the machine-readable ALFRED/FRED TOTALSLAR first vintage as the public copy of the Fed series; do not use later revisions or same-day correction exceptions unless the Fed replaces the first print before ordinary release posting.","dataPointId":"fed.g19.consumer_credit_total_annual_rate.2026_07.first_print","historicalContext":[{"label":"May 2026 latest TOTALSLAR","value":-0.04},{"label":"Apr 2026 TOTALSLAR","value":4.87},{"label":"Mar 2026 TOTALSLAR","value":5.35},{"label":"2023-01 to 2026-05 reference-class mean","value":2.29}],"drivers":["Recent total consumer credit growth has averaged a little above 2 percent annualized","May 2026 was flat because revolving credit contracted sharply","July same-month observations in 2023-2025 were positive but not boom-like","Higher borrowing costs and credit-card normalization limit upside"],"sourceContext":["https://www.federalreserve.gov/newsevents/2026-september.htm","https://www.federalreserve.gov/releases/g19/current/default.htm","https://www.federalreserve.gov/releases/g19/about.htm","https://fred.stlouisfed.org/series/TOTALSLAR","https://alfred.stlouisfed.org/series?seid=TOTALSLAR"],"runAt":"2026-07-31T15:10:09Z","reasoning":[{"kind":"heading","text":"US G.19 total consumer credit annual-rate forecast"},{"kind":"text","text":"The target is the Federal Reserve G.19 Consumer Credit table, seasonally adjusted Total percent change at annual rate, series code TOTALSLAR, for July 2026 first print. The official Fed September 2026 calendar lists G.19 Consumer Credit on September 8 at 3:00 p.m., so resolutionDate is 2026-09-08."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve current G.19 release and table check for latest same-variant data","result":"Fed G.19 current release dated July 8, 2026 reports May 2026 total consumer credit was unchanged; the table shows Total percent change annual rate -0.04, Revolving -4.71, Nonrevolving 1.61, and Total outstanding 5154.5 billion dollars."},{"kind":"tool","tool":"fred.series","call":"FRED/ALFRED TOTALSLAR recent observations used as public history mirror of Fed G.19","result":"TOTALSLAR recent values: May 2026 -0.04, Apr 2026 4.87, Mar 2026 5.35, Feb 2026 1.70, Jan 2026 1.05 percent change at annual rate, seasonally adjusted."},{"kind":"tool","tool":"history.lookup","call":"Same-month and recent reference-class TOTALSLAR values from public series table","result":"Same-month July values were 2023 July 2.62, 2024 July 4.73, and 2025 July 2.97; recent annual values include 2025 Dec 3.58, 2024 Dec 4.94, and 2023 Dec -1.20."},{"kind":"text","text":"The base rate/reference class is the 2023-01 through 2026-05 monthly TOTALSLAR sample, which avoids the 2022 reopening-credit surge but keeps the current high-rate regime. Its mean is 2.29, close to the trailing 12-month mean of 2.36, so the outside-view anchor is near 2.3 percent."},{"kind":"math","text":"Prior/update/interval: Persistence/reference class prior is 2023-01 through 2026-05 TOTALSLAR values: mean 2.29 and sigma = 2.03 from the values themselves; half-width = 1.28*sigma = 1.28*2.03 = 2.60. Update components: latest May value -0.04 pulls down, March-April strength and July same-month mean 3.44 pull up, and tight-credit conditions keep the point near the recent mean. Point = 2.40; 80% interval = 2.40 +/- 2.60 = [-0.20, 5.00]."},{"kind":"text","text":"Upside risk is a rebound in revolving balances after the May -4.71 revolving print plus resilient auto or student nonrevolving flows, which would land above the interval if total credit growth exceeds 5.0. Downside risk is another revolving contraction or weaker auto-credit origination, which would land outside the interval below -0.2."},{"kind":"forecast","point":2.4,"ciLow":-0.2,"ciHigh":5.0}]}

# Reviewer critique
{
  "summary": "Draft is mostly publishable, but the resolver/source fields should be aligned with the canonical ALFRED first-print binding rather than a Fed release-page URL.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The draft cites the Fed G.19 page as resolutionSourceUrl, while the ledger contract binds resolution to ALFRED/FRED TOTALSLAR via alfred.stlouisfed.org with first_print policy.",
      "actionRequested": "Set or restate the resolver/source fields to the canonical ALFRED TOTALSLAR first-vintage source binding, while still noting the Fed G.19 release as the originating official release if desired."
    }
  ],
  "optionalSuggestions": [
    "In the final reasoning, explicitly say the Fed calendar supports the 2026-09-08 release date but the resolved value is read from the ALFRED first vintage.",
    "The prior/update/interval step is compact and coherent; no replacement forecast is needed."
  ]
}

Emit the final JSON object only.
