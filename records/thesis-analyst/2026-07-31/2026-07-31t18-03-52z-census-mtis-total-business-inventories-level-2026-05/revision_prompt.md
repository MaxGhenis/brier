# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.mtis.total_business_inventories_level
- period: 2026-05
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-total-business-inventories-may-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "census.mtis.total_business_inventories_level.may_2026.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-21", "start": "2026-07-13"}, "field": "BUSINV", "releasePolicy": "first_print", "sourceSeriesId": "BUSINV", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BUSINV", "table": "Manufacturing and Trade Inventories and Sales", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-1ca2bf7bff1465285894c8aded9c645ff264ba74716a17112923e0cba4beba9f.json"
- targetContentHash: "1ca2bf7bff1465285894c8aded9c645ff264ba74716a17112923e0cba4beba9f"
- registrationCommit: "7ecbc85cc4110060218f856d50321ab93db3af3b"
- registeredAtUtc: "2026-07-31T18:02:17Z"

# Source hints
- Use Census income, poverty, SPM, and health-insurance release pages, CPS ASEC historical tables, and the Census release calendar.
- For official-poverty targets, distinguish the official poverty measure from SPM and cite the exact Census table or report.
- For SPM targets, name the population group, calendar year, and whether taxes, credits, transfers, medical expenses, or housing adjustments matter for the forecast.
- For ACS table targets, fetch each history year's values from the keyless JSON endpoint https://data.census.gov/api/access/data/table?id=<PRODUCT><YEAR>.<TABLE>&g=010XX00US (for example ACSDT1Y2024.B28005) and read the cited variable columns from the returned JSON.
- api.census.gov requires an API key (keyless requests redirect to missing_key.html); never rely on it in keyless runs, and never present remembered values as fetched ones.
- ACS vintage discipline: never mix 5-year estimates into a 1-year series — the 5-year file is a five-year average, so its level trails the 1-year series; the product id in the fetch URL (ACSDT1Y vs ACSDT5Y) is the vintage authority.

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
{"slug":"us-total-business-inventories-may-2026","country":"US","type":"data","title":"US Total Business Inventories, May 2026","question":"U.S. Census Bureau Manufacturing and Trade Inventories and Sales total business inventories, May 2026, seasonally adjusted end-of-month level, first print","unit":"usd_billions","pointEstimate":2736.2,"ciLow":2725.3,"ciHigh":2747.1,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Census Bureau Manufacturing and Trade Inventories and Sales release","resolutionSourceUrl":"https://www.census.gov/mtis/current/index.html","resolutionRule":"Resolve to the first U.S. Census Bureau Manufacturing and Trade Inventories and Sales release for May 2026, using the seasonally adjusted manufacturers' and trade inventories end-of-month level for total business inventories, reported in billions of dollars. Use the first print released on July 16, 2026 at 10:00 a.m.; do not use later revisions or benchmark revisions.","dataPointId":"census.mtis.total_business_inventories_level.may_2026.first_print","historicalContext":[{"label":"May 2026 first print, SA total business inventories","value":2736.158},{"label":"April 2026, SA total business inventories","value":2728.142},{"label":"March 2026, SA total business inventories","value":2712.902},{"label":"February 2026, SA total business inventories","value":2686.289},{"label":"January 2026, SA total business inventories","value":2676.882}],"drivers":["Census first print for May 2026 was already published on July 16, 2026","May inventories increased modestly from April","Recent monthly level changes in early 2026 were positive but uneven","Sales rose faster than inventories, lowering the inventory-sales ratio"],"sourceContext":["https://www.census.gov/mtis/current/index.html","https://www.census.gov/mtis/release_schedule.html","https://fred.stlouisfed.org/series/BUSINV","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=BUSINV"],"runAt":"2026-07-31T18:04:14Z","reasoning":[{"kind":"heading","text":"US Total Business Inventories May 2026 First Print"},{"kind":"text","text":"Framing and exact resolver: target is Census MTIS total business inventories, BUSINV-equivalent seasonally adjusted end-of-month level, May 2026, first print, in USD billions. The ledger expects an ALFRED-FRED first-print mirror, but the official agency release is Census MTIS; I keep the target unchanged and resolve to the Census first print."},{"kind":"tool","tool":"official.lookup","call":"Checked the Census MTIS release schedule for the May 2026 data month.","result":"The Census MTIS schedule lists May 2026 for release on July 16, 2026 at 10:00 a.m.; nearby releases include April 2026 on June 17, 2026 and June 2026 on August 14, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked the Census MTIS current May 2026 release page.","result":"Census reported May 2026 manufacturers' and trade inventories at $2,736.2 billion, up 0.3 percent from April 2026 and up 3.1 percent from May 2025; May sales were $2,135.0 billion and the inventory-sales ratio was 1.28."},{"kind":"tool","tool":"official.lookup","call":"Checked the public FRED/Census BUSINV time-series mirror for recent seasonally adjusted total business inventories levels.","result":"BUSINV observations were May 2026 2,736.158, April 2026 2,728.142, March 2026 2,712.902, February 2026 2,686.289, and January 2026 2,676.882 billion dollars."},{"kind":"tool","tool":"official.lookup","call":"Checked the ALFRED release-vintage context for the same Census MTIS BUSINV series.","result":"The ALFRED May 14, 2026 MTIS release page showed BUSINV as total business inventories, seasonally adjusted, millions of dollars, with last observation March 2026 at 2,709,734.0 million dollars before later revisions."},{"kind":"text","text":"Reference class and base rate: for a level series released monthly, the most relevant reference class is recent first-print or near-current monthly BUSINV changes. Early-2026 changes from the public time-series mirror were positive each month, so persistence plus recent momentum points to another modest increase rather than a flat or declining May level."},{"kind":"math","text":"Prior/update/interval: persistence prior starts from April 2026 BUSINV 2728.142. Recent change sample uses Jan-Apr-to-May adjacent changes in billions: Feb-Jan = 9.407, Mar-Feb = 26.613, Apr-Mar = 15.240, May-Apr = 8.016. The mean change is 14.819 and sigma = 8.5 using the sample standard deviation of those changes. A roughly 80% normal half-width is 1.28*sigma = 10.9. With the already-published Census first print at 2736.158, the rounded point is 2736.2 and the implied 80% interval is 2736.2 +/- 10.9 = [2725.3, 2747.1]."},{"kind":"text","text":"Level, momentum, and one-off effects: the level anchor is the published May first print of 2736.158 billion. Momentum was still positive but slower than March and April, consistent with the Census-reported 0.3 percent monthly gain. No policy mechanism changes the definition; the release is seasonally adjusted and not price-adjusted."},{"kind":"text","text":"Counter-consideration: upside risk would be a stronger accumulation cycle or revisions-sensitive component mix that would land above the interval; downside risk would be a broad liquidation after April or weaker retail/wholesale stocks that would land below the interval. Because this target is first print and the release has already occurred, those risks describe pre-release uncertainty rather than revision policy."},{"kind":"forecast","point":2736.2,"ciLow":2725.3,"ciHigh":2747.1}]}

# Reviewer critique
{
  "summary": "The draft is not publishable as a forecast because it uses the already-released May 2026 value as the point estimate and interval anchor.",
  "requiredFixes": [
    {
      "rubricItem": "leakage",
      "severity": "blocking",
      "summary": "The reasoning states that the Census first print was already published on July 16, 2026 and uses the observed May 2026 value of 2736.158 to set the point estimate.",
      "actionRequested": "Remove all post-resolution outcome evidence and rebuild the forecast only from information available before the July 16, 2026 release; do not use the realized May 2026 value in the point, interval, drivers, or historicalContext."
    },
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The draft resolver fields use Census current pages, while the canonical ledger sourceBinding specifies the ALFRED-FRED BUSINV first-print mirror with transform factor 0.001.",
      "actionRequested": "Align the machine-readable resolver/source fields with the ledger contract, or explicitly preserve the ledger target while noting any claimed Census-vs-ALFRED discrepancy only in reasoning."
    },
    {
      "rubricItem": "base_rate",
      "severity": "blocking",
      "summary": "The stated base-rate sample includes the May-April change, which is the target outcome itself.",
      "actionRequested": "State a prior before inside-view updates using only pre-May-2026 observations, such as recent monthly changes ending with April 2026 or a longer historical same-series sample."
    },
    {
      "rubricItem": "interval",
      "severity": "blocking",
      "summary": "The interval is centered on the realized May first print and its volatility sample includes the target-period change.",
      "actionRequested": "Compute uncertainty from pre-release realized volatility or an explicit ex ante uncertainty model, and center it on the ex ante forecast rather than the observed outcome."
    },
    {
      "rubricItem": "coherence",
      "severity": "blocking",
      "summary": "The historicalContext, drivers, reasoning, point estimate, and final forecast are coherent with the realized value rather than with a genuine pre-release forecast.",
      "actionRequested": "Revise all fields so they describe a forecast made before resolution, with no realized May 2026 first-print value or post-release Census facts."
    }
  ],
  "optionalSuggestions": [
    "Use April 2026 as the latest permissible level anchor if forecasting before the May release.",
    "Make the Prior/update/interval step compactly list the pre-release sample window, adjustment components, interval method, and implied bounds."
  ]
}

Emit the final JSON object only.
