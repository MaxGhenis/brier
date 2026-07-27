# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fed.g17.manufacturing_production_mom
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-manufacturing-production-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "fed.g17.manufacturing_production_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-18", "start": "2026-08-18"}, "field": "IPMAN", "releasePolicy": "first_print", "sourceSeriesId": "IPMAN", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=IPMAN", "table": "G.17 Industrial Production and Capacity Utilization, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-27-0d63736cc967eb9230750b56083858fb59e269bc2b8d629918cec1b630bfbc54.json"
- targetContentHash: "0d63736cc967eb9230750b56083858fb59e269bc2b8d629918cec1b630bfbc54"
- registrationCommit: "e494ebc7a9b410a6fcffab9e5439408ff3d09413"
- registeredAtUtc: "2026-07-27T18:01:44Z"

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
{"slug":"us-manufacturing-production-mom-july-2026","country":"US","type":"data","title":"US manufacturing production m/m, July 2026","question":"Federal Reserve G.17 Manufacturing (NAICS) industrial production, seasonally adjusted monthly percent change for July 2026, first print","unit":"percent_growth","pointEstimate":0.1,"ciLow":-0.32,"ciHigh":0.52,"confidence":0.8,"resolutionDate":"2026-08-18","resolutionSource":"Federal Reserve G.17 Industrial Production and Capacity Utilization, Table 1","resolutionSourceUrl":"https://www.federalreserve.gov/releases/g17/current/table1.htm","resolutionRule":"Resolve to the first-print preliminary July 2026 monthly percent change for the G.17 Table 1 Manufacturing (NAICS) row, seasonally adjusted, as issued on August 18, 2026 at 9:15 a.m.; use the published one-decimal percent change and ignore later revisions or annual-revision updates. The ledger sourceBinding names IPMAN, an index series, while the target unit is percent_growth; this forecast is tied to the same target and interprets it as the official Table 1 monthly percent change implied by the IPMAN manufacturing NAICS index.","dataPointId":"fed.g17.manufacturing_production_mom.2026_07.first_print","historicalContext":[{"label":"June 2026 first/current G.17 Manufacturing (NAICS) m/m","value":0},{"label":"May 2026 G.17 Manufacturing (NAICS) m/m","value":0.1},{"label":"April 2026 G.17 Manufacturing (NAICS) m/m","value":0.7},{"label":"March 2026 G.17 Manufacturing (NAICS) m/m","value":0.1}],"drivers":["Recent manufacturing NAICS momentum slowed to 0.0 percent in June after 0.1 percent in May and 0.7 percent in April.","Second-quarter manufacturing NAICS growth was positive but front-loaded, with no clear June carry-through.","Durable manufacturing slipped in June while nondurable manufacturing rose, suggesting offsetting components rather than a broad surge.","Manufacturing capacity utilization remained below its long-run average, limiting inflationary production pressure but leaving room for modest output gains."],"sourceContext":["https://www.federalreserve.gov/releases/g17/","https://www.federalreserve.gov/releases/g17/current/table1.htm","https://www.federalreserve.gov/releases/g17/current/table4.htm","https://fred.stlouisfed.org/series/IPMAN"],"runAt":"2026-07-27T18:19:18Z","reasoning":[{"kind":"heading","text":"US Manufacturing Production July 2026 First Print"},{"kind":"text","text":"Framing and exact resolver: the target is the Federal Reserve G.17 Manufacturing (NAICS) industrial production monthly percent change, seasonally adjusted, for July 2026. I resolve on the first official print in Table 1; FRED/ALFRED IPMAN is used only as the public index mirror for the same Manufacturing (NAICS) series."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 release calendar lookup","result":"Fetched Fed calendar shows 2026 G.17 monthly release dates include July 17 as the most recent monthly release and August 18 as the next release; monthly releases are issued at 9:15 a.m.; listed 2026 dates include Jan 16, Feb 18, Mar 16, Apr 16, May 15, Jun 15, Jul 17, Aug 18, Sep 18, Oct 16, Nov 17, and Dec 16."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 current Table 1 percent-change lookup","result":"Fetched Table 1 Manufacturing (NAICS), seasonally adjusted monthly rates: Jan 2026 0.1, Feb 2026 0.7, Mar 2026 0.1, Apr 2026 0.7, May 2026 0.1, Jun 2026 0.0; Q2 2026 annual rate 4.6 and June 2025 to June 2026 change 1.1."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 current release industry-detail lookup","result":"Fetched current-release narrative: manufacturing output was unchanged in June at 0.0, durable manufacturing decreased 0.1, nondurable manufacturing increased 0.2, petroleum and coal products increased 2.1, and manufacturing output rose at a 4.7 annual rate in Q2."},{"kind":"tool","tool":"history.lookup","call":"FRED IPMAN exact index mirror lookup","result":"Fetched IPMAN index levels from FRED mirror: Jun 2026 98.6995, May 2026 98.6976, Apr 2026 98.5997, Mar 2026 97.8760, Feb 2026 97.7645; next release date shown as Aug 18, 2026."},{"kind":"text","text":"Reference class/base rate: using the same seasonally adjusted Manufacturing (NAICS) monthly-rate variant, the last six official monthly prints average 0.283 percent. I discount that upward mean because the latest month was flat, durable manufacturing was negative, and the Q2 strength appears front-loaded rather than accelerating into June."},{"kind":"math","text":"Prior/update/interval: persistence prior is recent Fed G.17 Manufacturing (NAICS) m/m prints from Jan-Jun 2026 [0.1, 0.7, 0.1, 0.7, 0.1, 0.0], with base rate mean 0.283; updates are -0.10 for June flatness, -0.05 for durable weakness, and -0.03 for front-loaded Q2, giving about 0.10 after rounding. For the 80% interval, sample dispersion of those monthly percent changes is sigma = 0.33, so half-width = 1.28*sigma = 1.28*0.33 = 0.42; point 0.10 minus/plus 0.42 gives [-0.32, 0.52]."},{"kind":"text","text":"Counter-considerations: upside risk is a July rebound in autos or high-tech manufacturing that would land above the interval; downside risk is a broad durable-goods pullback or plant shutdown effects that would land below the interval; outside the interval would require a monthly move larger than roughly 0.5 percent or below roughly -0.3 percent on the first print."},{"kind":"forecast","point":0.1,"ciLow":-0.32,"ciHigh":0.52}]}

# Reviewer critique
{
  "summary": "Draft is mostly coherent, but the resolver/source fields do not exactly follow the canonical ledger contract and the interval relies on a very short six-month sample.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft's resolutionSource and resolutionSourceUrl point to Federal Reserve Table 1, while the canonical ledger sourceBinding specifies the ALFRED/FRED IPMAN CSV, allowed host alfred.stlouisfed.org, and first_print policy.",
      "actionRequested": "Align the resolver fields with the ledger sourceBinding, or explicitly state the ledger discrepancy while keeping the target tied to the ledger dataPointId and sourceBinding rather than silently substituting a different resolver URL."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The 80% interval uses sigma from only Jan-Jun 2026, which is a very small and unusually recent sample for realized volatility.",
      "actionRequested": "Either use a longer realized-volatility sample for Manufacturing m/m changes or justify why the six-month sample is the intended uncertainty basis."
    }
  ],
  "optionalSuggestions": [
    "Clarify whether the ALFRED IPMAN index first print will be converted to a monthly percent change or whether the published one-decimal Table 1 percent change is authoritative.",
    "The tail scenarios are concrete, but they could name which July subcomponents would plausibly move the aggregate outside the stated bounds."
  ]
}

Emit the final JSON object only.
