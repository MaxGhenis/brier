# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: census.construction_spending.total_mom
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-construction-spending-mom-june-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "census.construction_spending.total_mom.2026_06.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-03", "start": "2026-08-03"}, "field": "TTLCONS", "releasePolicy": "first_print", "sourceSeriesId": "TTLCONS", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=TTLCONS", "table": "Value of Construction Put in Place Survey", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-9556fc5386456478cfc719b06a95f8b8a7e3afbff792293f2bb96d8d77565a3e.json"
- targetContentHash: "9556fc5386456478cfc719b06a95f8b8a7e3afbff792293f2bb96d8d77565a3e"
- registrationCommit: "145f6612f225710a4621f124b13bf5d5ae5d97ac"
- registeredAtUtc: "2026-07-26T00:55:04Z"

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
{"slug":"us-construction-spending-mom-june-2026","country":"US","type":"data","title":"US construction spending MoM, June 2026","question":"What will the U.S. Census Bureau first report as the month-over-month percent change in total construction spending, seasonally adjusted annual rate, for June 2026?","unit":"percent_growth","pointEstimate":0.05,"ciLow":-0.36,"ciHigh":0.46,"confidence":0.8,"resolutionDate":"2026-08-03","resolutionSource":"U.S. Census Bureau Monthly Construction Spending release","resolutionSourceUrl":"https://www.census.gov/construction/c30/current/index.html","resolutionRule":"Resolve to the first Census Monthly Construction Spending print for June 2026 total construction spending, seasonally adjusted annual rate. Use the headline month-over-month percent change versus the revised May 2026 estimate in that first release; if resolving from TTLCONS levels, compute 100*(June 2026 first-print SAAR / revised May 2026 SAAR in the same first-print release - 1), round to one decimal percentage point, and ignore later revisions.","dataPointId":"census.construction_spending.total_mom.2026_06.first_print","historicalContext":[{"label":"Feb 2026 revised MoM from TTLCONS levels","value":-0.271},{"label":"Mar 2026 revised MoM from TTLCONS levels","value":0.444},{"label":"Apr 2026 revised MoM from TTLCONS levels","value":0.348},{"label":"May 2026 revised MoM from TTLCONS levels","value":0.143}],"drivers":["Recent TTLCONS momentum is mildly positive but slowing","June housing starts rebounded while permits fell","Private residential spending remains rate-sensitive","Public construction is still a positive offset","May first print showed total spending only 0.1 percent higher"],"sourceContext":["https://www.census.gov/construction/c30/release.html","https://www.census.gov/construction/c30/current/index.html","https://fred.stlouisfed.org/series/TTLCONS","https://www.census.gov/construction/nrc/current/index.html"],"runAt":"2026-07-26T01:07:50Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 total construction spending MoM"},{"kind":"text","text":"Framing and exact resolver: this is the Census Value of Construction Put in Place total construction series, seasonally adjusted annual rate, first print for June 2026. The ledger binds dataPointId census.construction_spending.total_mom.2026_06.first_print and TTLCONS; the economic target is the headline percent change from revised May to June in the first Census release."},{"kind":"tool","tool":"official.lookup","call":"Checked Census Construction Spending release schedule for the June 2026 reporting period.","result":"Census schedule lists the June reporting period release date as August 3, 2026 at 10:00 a.m.; nearby rows show May on July 1, 2026 and July on September 1, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked the latest Census Monthly Construction Spending release for current total, private, residential, nonresidential, and public construction levels.","result":"May 2026 total construction spending was $2,210.2 billion SAAR, 0.1 percent above revised April at $2,207.1 billion; May 2025 was $2,244.4 billion; private was $1,669.0 billion, residential $930.2 billion, nonresidential $738.7 billion, and public $541.2 billion."},{"kind":"tool","tool":"fred.lookup","call":"Checked public FRED/TTLCONS mirror of Census total construction spending levels for recent reference-class calculations.","result":"TTLCONS levels fetched from the public series page were May 2026 2,210,214 million, Apr 2026 2,207,051 million, Mar 2026 2,199,399 million, Feb 2026 2,189,683 million, and Jan 2026 2,195,636 million."},{"kind":"tool","tool":"official.lookup","call":"Checked Census/HUD New Residential Construction June 2026 release for current residential construction signal.","result":"June 2026 permits were 1,367,000 SAAR, 3.0 percent below revised May 1,410,000; housing starts were 1,427,000 SAAR, 19.0 percent above revised May 1,199,000; completions were 1,392,000 SAAR, 3.3 percent above revised May 1,347,000."},{"kind":"text","text":"Reference class/base rate: using recent TTLCONS level-implied total construction spending MoM changes, Feb through May 2026 were -0.271, +0.444, +0.348, and +0.143 percent, averaging about +0.166 percent. The base rate is therefore mildly positive, but May's first-print headline was only +0.1 percent and year-to-date spending was reported 2.7 percent below the same 2025 period."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent Census/TTLCONS revised MoM history for Feb-May 2026, values -0.271, 0.444, 0.348, 0.143 percent. Adjustment components: -0.08 pp for falling June permits and still-soft private/residential conditions, +0.04 pp for the June starts/completions rebound, and -0.08 pp for slowing May total momentum versus the +0.166 base rate, giving a point near +0.05 percent. Interval method: sample dispersion of those four MoM values gives sigma = 0.317 percentage points; 1.28*sigma = 0.406 pp, so an 80 percent interval around 0.05 is about -0.36 to +0.46 percent after rounding."},{"kind":"text","text":"The variant is total construction spending, seasonally adjusted annual rate, not unadjusted monthly dollars and not a private-only, residential-only, or FRED-transformed growth variant. Public construction is a meaningful upside risk because May public spending was +0.5 percent MoM, while downside risk comes from private nonresidential weakness and permits down 3.0 percent in June. A broad public-construction surge with resilient private work would land above the interval; a sharp giveback in private residential or nonresidential work would land below the interval, outside the interval."},{"kind":"forecast","point":0.05,"ciLow":-0.36,"ciHigh":0.46}]}

# Reviewer critique
{
  "summary": "The draft is mostly coherent, but it does not explicitly reconcile its Census resolver fields with the ledger's ALFRED/FRED sourceBinding.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The JSON uses Census as resolutionSourceUrl while the canonical ledger sourceBinding specifies the ALFRED TTLCONS CSV URL and allowed host.",
      "actionRequested": "Either align the resolver/source fields to the ledger sourceBinding or explicitly state in reasoning that the ledger uses ALFRED/TTLCONS as the mechanical binding while the underlying official first print is Census, without changing the target."
    }
  ],
  "optionalSuggestions": [
    "The interval is defensible but based on only four recent monthly observations; mention that the small sample makes the 80% band approximate.",
    "Tail scenarios would be stronger with rough magnitudes, for example what size public surge or private pullback would push the result outside the interval."
  ]
}

Emit the final JSON object only.
