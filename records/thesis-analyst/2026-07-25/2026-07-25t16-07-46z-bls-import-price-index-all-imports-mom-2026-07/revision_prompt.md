# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.import_price_index.all_imports_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bls-import-price-index-all-imports-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.import_price_index.all_imports_mom.2026-07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-21", "start": "2026-08-13"}, "field": "IR", "releasePolicy": "first_print", "sourceSeriesId": "IR", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=IR", "table": "U.S. Import Price Indexes, Table 1", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-25-8983b218a33d3fd3bc5b3336383aeb665cc0dcb05f4ca3ec4c6bb3791c189c4e.json"
- targetContentHash: "8983b218a33d3fd3bc5b3336383aeb665cc0dcb05f4ca3ec4c6bb3791c189c4e"
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
{"slug":"bls-import-price-index-all-imports-mom-july-2026","country":"US","type":"data","title":"US Import Prices MoM, July 2026","question":"What will the BLS first print for the U.S. Import Price Index (End Use): All Commodities (IR), not seasonally adjusted, monthly percent change for July 2026?","unit":"percent_growth","pointEstimate":1.0,"ciLow":0.1,"ciHigh":1.9,"confidence":0.8,"resolutionDate":"2026-08-18","resolutionSource":"BLS U.S. Import and Export Price Indexes, Table 1","resolutionSourceUrl":"https://www.bls.gov/news.release/ximpim.t01.htm","resolutionRule":"Resolve to the first BLS U.S. Import and Export Price Indexes news release for July 2026, Table 1, row 'All commodities', monthly percent change for June 2026 to July 2026, reported in percent to one decimal. Use the first official print only and ignore later revisions.","dataPointId":"bls.import_price_index.all_imports_mom.2026-07.first_print","historicalContext":[{"label":"2026-06 first/latest BLS all imports MoM","value":0.3},{"label":"2026-05 BLS all imports MoM","value":1.7},{"label":"2026-04 BLS all imports MoM","value":2.1},{"label":"2026-03 BLS all imports MoM","value":0.9},{"label":"2026-02 BLS all imports MoM","value":1.0},{"label":"2026-01 BLS all imports MoM","value":0.5}],"drivers":["June import-price momentum cooled to +0.3 after very strong April-May prints","Nonfuel imports were still rising at +0.4 in June and carry about 90% weight","Late-July crude-oil spike raises fuel-import upside risk","Broad dollar firmness modestly offsets imported-goods price pressure","First-print target is the NSA BLS Table 1 all-commodities monthly percent change"],"sourceContext":["https://www.bls.gov/schedule/news_release/ximpim.htm","https://www.bls.gov/news.release/ximpim.t01.htm","https://www.bls.gov/news.release/ximpim.nr0.htm","https://fred.stlouisfed.org/series/IR","https://fred.stlouisfed.org/series/DCOILBRENTEU","https://www.wsj.com/finance/commodities-futures/oil-futures-edge-lower-on-likely-technical-correction-2971174b"],"runAt":"2026-07-25T16:07:57Z","reasoning":[{"kind":"heading","text":"BLS July 2026 All-Imports Monthly Price Forecast"},{"kind":"text","text":"Resolver framing: this targets BLS Import Price Index (End Use): All Commodities, series IR, not seasonally adjusted, Table 1 monthly percent change for July 2026, first print only. FRED/ALFRED can mirror history, but final resolution should cite the BLS release table."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS schedule for U.S. Import and Export Price Indexes release dates.","result":"BLS schedule lists June 2026 released on July 17, 2026 at 08:30 AM and July 2026 scheduled for August 18, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Read BLS Table 1 for the latest all-commodities import price index and recent monthly changes.","result":"BLS Table 1 shows All commodities relative importance 100.000, May 2026 index 150.3, June 2026 index 150.8, annual change 7.1, and monthly changes 0.9 for Feb-to-Mar, 2.1 for Mar-to-Apr, 1.7 for Apr-to-May, and 0.3 for May-to-Jun."},{"kind":"tool","tool":"official.lookup","call":"Read BLS June 2026 release summary for component momentum.","result":"The BLS summary says all imports rose 0.3 in June after 1.7 in May and 2.1 in April; fuel imports fell 0.4 in June after rising 12.6 in May; petroleum fell 0.7, natural gas rose 9.2, and nonfuel imports rose 0.4 in June after 0.7 in May."},{"kind":"tool","tool":"history.lookup","call":"Checked FRED/BLS mirror for series IR index levels around the latest release.","result":"FRED reports IR at 150.8 in June 2026, 150.3 in May 2026, 147.8 in April 2026, 144.8 in March 2026, and 143.5 in February 2026, updated July 17, 2026."},{"kind":"tool","tool":"market.lookup","call":"Checked public oil-price context because fuel imports are the volatile July mechanism.","result":"FRED/EIA Brent spot was 70.46 on June 30 and 69.56 on July 6, while late-July market reporting showed Brent at 96.78 and WTI at 89.31, implying a sharp upside move after the early-July official spot observations."},{"kind":"text","text":"Reference class/base rate: the immediate six-month all-imports MoM reference class is 0.5, 1.0, 0.9, 2.1, 1.7, and 0.3, with a mean near 1.08. The June print cooled sharply, but the regime is still above the pre-2026 flat readings because fuel and nonfuel import prices have both been contributing at times."},{"kind":"math","text":"Prior/update/interval: Use a recent-realized-value persistence prior on Jan-Jun 2026 BLS all-imports monthly changes [0.5, 1.0, 0.9, 2.1, 1.7, 0.3], whose sample mean is 1.08 and sample sigma = 0.69 percentage points; 1.28*sigma = 0.88 percentage points. Update the point from the 1.08 base rate to 1.0: -0.2 for June cooling and a firmer dollar/nonfuel moderation, +0.1 to +0.2 for late-July oil/fuel upside with about 10% fuel weight and still-positive nonfuel goods. Rounded 80% bounds are 1.0 +/- 0.9, or 0.1 to 1.9."},{"kind":"text","text":"Counter-considerations: upside risk is a sustained late-July fuel-import jump if Brent near the high-$90s feeds directly into the BLS pricing month, which would land above the interval. Downside risk is a rapid oil reversal plus weaker nonfuel industrial supplies or automotive import prices, which would land below the interval."},{"kind":"forecast","point":1.0,"ciLow":0.1,"ciHigh":1.9}]}

# Reviewer critique
{"summary":"The draft is publishable: it matches the BLS first-print target, states a recent persistence prior, gives an explicit volatility-based interval, and keeps the forecast coherent with the JSON fields.","requiredFixes":[],"optionalSuggestions":["Consider noting that the interval is based on only six recent monthly observations; a broader historical realized-volatility check would make the uncertainty claim more robust.","The oil-price update would be stronger if the cited late-July quote source were summarized with date/time and whether it reflects spot or futures pricing."]}

Emit the final JSON object only.
