# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.government_social_benefits.medicare
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bea-government-social-benefits-medicare-june-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.government_social_benefits.medicare.june_2026.first_print"
- resolutionSourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=W824RC1&vintage_date=2026-06-25"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "W824RC1", "releasePolicy": "first_print", "sourceSeriesId": "W824RC1", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=W824RC1&vintage_date=2026-06-25", "table": "Personal Income and Outlays, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-15-d9074bfce2314259e94b6212a4c40f3b45ecba5251b62858fc2cd2c4610df70e.json"
- targetContentHash: "d9074bfce2314259e94b6212a4c40f3b45ecba5251b62858fc2cd2c4610df70e"
- registrationCommit: "0b8a29cc7d9bec54ef1d71247d06c1bf17d64355"
- registeredAtUtc: "2026-07-15T16:29:07Z"

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
{"slug":"bea-government-social-benefits-medicare-june-2026","country":"US","type":"data","title":"US Medicare Benefits, June 2026","question":"What will BEA first print for personal current transfer receipts: government social benefits to persons: Medicare, monthly seasonally adjusted annual rate, June 2026?","unit":"usd_billions","pointEstimate":1342.3,"ciLow":1338.3,"ciHigh":1346.3,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"U.S. Bureau of Economic Analysis, Personal Income and Outlays, Table 1, with W824RC1 original-vintage mirror","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=W824RC1&vintage_date=2026-06-25","resolutionRule":"Resolve to the first published value for W824RC1, personal current transfer receipts: government social benefits to persons: Medicare, for 2026-06, in billions of dollars at a seasonally adjusted annual rate, rounded to one decimal. Use the first print from the BEA Personal Income and Outlays June 2026 release and ignore later revisions. The registered ALFRED URL is retained as target contract, but its vintage_date=2026-06-25 is before the verified July 30, 2026 BEA release date and therefore is not itself a valid June first-print outcome vintage.","dataPointId":"bea.government_social_benefits.medicare.june_2026.first_print","historicalContext":[{"label":"2026-05 latest","value":1332.0},{"label":"2026-04","value":1321.7},{"label":"2026-03","value":1311.4},{"label":"2026-02","value":1301.0},{"label":"2026-01","value":1290.6},{"label":"2025-12 vintage context","value":1280.1}],"drivers":["recent W824RC1 level trend is very smooth near +10.3 billion per month","Medicare benefit accruals are policy-driven and trend-like at monthly frequency","first-print/original-vintage risk and BEA release mechanics warrant wider uncertainty than the visible recent run-rate","same variant throughout: monthly seasonally adjusted annual rate, billions of dollars"],"sourceContext":["https://www.bea.gov/news/schedule","https://fred.stlouisfed.org/series/W824RC1","https://alfred.stlouisfed.org/series?seid=W824RC1","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=W824RC1&vintage_date=2026-06-25"],"runAt":"2026-07-15T16:33:57Z","reasoning":[{"kind":"heading","text":"Forecast for BEA Medicare government social benefits, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: the target is BEA/FRED series W824RC1, personal current transfer receipts: government social benefits to persons: Medicare, monthly, billions of dollars, seasonally adjusted annual rate. I use the same SAAR billions variant for every historical anchor and forecast value."},{"kind":"tool","tool":"official.lookup","call":"Checked the BEA release schedule for Personal Income and Outlays, June 2026.","result":"BEA schedule lists Personal Income and Outlays, June 2026 on July 30, 2026 at 8:30 AM; the BEA schedule page was last modified 7/15/26."},{"kind":"tool","tool":"official.lookup","call":"Checked current public W824RC1 series display for latest observations and release metadata.","result":"FRED display for W824RC1 shows May 2026 = 1332.0, Apr 2026 = 1321.7, Mar 2026 = 1311.4, Feb 2026 = 1301.0, Jan 2026 = 1290.6, units billions of dollars SAAR, monthly, updated Jun 25, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked ALFRED W824RC1 vintage/context page for older visible observations and definition.","result":"ALFRED W824RC1 page shows Dec 2025 = 1280.1, Nov 2025 = 1269.5, Oct 2025 = 1258.9, Sep 2025 = 1248.3, Aug 2025 = 1237.6; notes identify BEA Account Code W824RC and Medicare benefits."},{"kind":"text","text":"Reference class/base rate: for this smooth level series, the useful base rate is the recent successive monthly change in the same W824RC1 SAAR billions series. The visible Aug 2025-May 2026 run is almost linear, with changes of about +10.3 to +10.7 billion per month."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest May 2026 level plus recent mean monthly change; historical sample = fetched Aug 2025-May 2026 visible W824RC1 values; adjustment components = level 1332.0, momentum +10.38, one-off/policy-mechanism 0.0 because no fetched evidence of a June discontinuity; point = 1332.0 + 10.38 = 1342.38, rounded to 1342.3. For fetched successive changes 10.7, 10.6, 10.6, 10.6, 10.5, 10.4, 10.4, 10.3, 10.3, sigma = 0.13, so 1.28*sigma = 0.17. I widen the 80% half-width to 4.0 because the displayed recent run-rate is policy-smoothed and materially understates first-print/original-vintage and release-mechanics risk for a benefits accrual series; final implied bounds are 1342.3 - 4.0 = 1338.3 and 1342.3 + 4.0 = 1346.3."},{"kind":"text","text":"Upside risk: a stronger Medicare accrual month, updated seasonal factors, or a June-specific trust-fund/payment adjustment would land above the interval if the first print exceeds 1346.3. Downside risk: a monthly accrual pause, offsetting seasonal revision, or weaker-than-trend benefits booking would land below the interval if the first print is under 1338.3."},{"kind":"text","text":"Target-contract discrepancy noted: the ledger sourceBinding expected release window ends 2026-07-29 and the registered ALFRED vintage URL uses vintage_date=2026-06-25, but the official BEA schedule verified this run gives July 30, 2026 for Personal Income and Outlays, June 2026. I keep the canonical slug, unit, dataPointId, and registered mirror URL rather than silently changing the target."},{"kind":"forecast","point":1342.3,"ciLow":1338.3,"ciHigh":1346.3}]}

# Reviewer critique
{
  "summary": "Draft is publishable on forecasting method and coherence, with one catalog-contract discrepancy already surfaced: the registered ALFRED vintage/window appears inconsistent with the BEA/FRED July 30, 2026 first-print release.",
  "requiredFixes": [],
  "optionalSuggestions": [
    "Add the FRED next-release metadata to the resolver evidence, since it independently supports July 30, 2026 for the next W824RC1 update.",
    "If the publisher requires strict ledger-field equality, resolve the catalog registration issue rather than changing only the forecast text."
  ]
}

Emit the final JSON object only.
