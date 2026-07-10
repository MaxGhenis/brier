# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.disposable_personal_income.level
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bea-disposable-personal-income-level-june-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.disposable_personal_income.level.june_2026.first_print"
- resolutionSourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "DSPI", "releasePolicy": "first_print", "sourceSeriesId": "DSPI", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25", "table": "Personal Income and Outlays, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-123ce8782db84a3d7daf502c09b752d32f0756b451f512b2661b632666c8caf3.json"
- targetContentHash: "123ce8782db84a3d7daf502c09b752d32f0756b451f512b2661b632666c8caf3"
- registrationCommit: "0d80683b051be25572f40ea4731fa5062af6d211"
- registeredAtUtc: "2026-07-10T12:36:34Z"

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
{"slug":"bea-disposable-personal-income-level-june-2026","country":"US","type":"data","title":"US disposable personal income, June 2026","question":"What will BEA report as the first-print June 2026 disposable personal income level, seasonally adjusted annual rate, in Table 2.6 / DSPI?","unit":"usd_billions","pointEstimate":23741.4,"ciLow":23634.4,"ciHigh":23848.3,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"U.S. Bureau of Economic Analysis, Personal Income and Outlays, Table 2.6 / DSPI first print","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25","resolutionRule":"Resolve to the first official BEA-published value for June 2026 disposable personal income, BEA account code A067RC / FRED-ALFRED series DSPI, in billions of dollars at a seasonally adjusted annual rate, rounded to one decimal. Use the initial June 2026 Personal Income and Outlays release print and ignore later revisions; the ledger ALFRED URL is retained as the target binding even though its stated vintage date appears to correspond to the May 2026 release rather than the July 30, 2026 June first print.","dataPointId":"bea.disposable_personal_income.level.june_2026.first_print","historicalContext":[{"label":"2026-05 latest DSPI","value":23651.7},{"label":"2026-04 DSPI","value":23486.9},{"label":"2026-03 DSPI","value":23510.4},{"label":"2026-02 DSPI","value":23382.4},{"label":"2026-01 DSPI","value":23395.9}],"drivers":["May 2026 DSPI rose 164.8 billion from April","Recent 2023-2026 monthly DSPI gains average about 89.7 billion","May personal income rose 181.6 billion and DPI rose 164.9 billion","June payroll and transfer-income persistence should keep the level near trend","One-month volatility supports a roughly 107.0 billion 80 percent half-width"],"sourceContext":["https://www.bea.gov/news/schedule","https://www.bea.gov/data/income-saving/personal-income","https://fred.stlouisfed.org/series/DSPI","https://fred.stlouisfed.org/data/DSPI","https://fred.stlouisfed.org/release/tables?eid=155443&rid=54"],"runAt":"2026-07-10T12:37:34Z","reasoning":[{"kind":"heading","text":"BEA DSPI June 2026 Forecast"},{"kind":"text","text":"Framing and exact resolver: the target is BEA disposable personal income, DSPI / account code A067RC, monthly, seasonally adjusted annual rate, billions of dollars, first print for June 2026. The official BEA schedule puts Personal Income and Outlays, June 2026 on July 30, 2026 at 8:30 AM; this conflicts with the ledger expected window ending 2026-07-29 and with the ledger ALFRED vintage_date=2026-06-25, which appears to point to the May 2026 release. I keep the forecast tied to the supplied slug and dataPointId and use the official calendar date for resolution."},{"kind":"tool","tool":"official.lookup","call":"Opened BEA release schedule for 2026 Personal Income and Outlays","result":"Fetched release-calendar numbers: Personal Income and Outlays, June 2026 is listed for July 30, 2026 at 8:30 AM; Personal Income and Outlays, July 2026 is listed for August 26, 2026 at 8:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Opened BEA Personal Income page/current release summary","result":"Fetched official release numbers: for May 2026, personal income increased 181.6 billion, DPI increased 164.9 billion or 0.7 percent, PCE increased 156.1 billion or 0.7 percent, and personal saving was 704.2 billion with a 3.0 percent saving rate."},{"kind":"tool","tool":"public.history","call":"Opened FRED DSPI page and table data, sourced to BEA","result":"Fetched DSPI levels in billions of dollars SAAR: May 2026 23651.7, Apr 2026 23486.9, Mar 2026 23510.4, Feb 2026 23382.4, Jan 2026 23395.9; FRED last updated the series on Jun 25, 2026 7:43 AM CDT and lists next release date Jul 30, 2026."},{"kind":"tool","tool":"public.history","call":"Opened FRED release Table 2.6 for Personal Income and Its Disposition, Monthly","result":"Fetched component levels: May 2026 personal income 26916.4, compensation of employees 16250.2, wages and salaries 13388.8, personal current taxes 3264.7, and disposable personal income 23651.7 billion; Apr 2026 disposable personal income was 23486.9 billion."},{"kind":"text","text":"Base rate / reference class: using successive monthly DSPI level changes from Feb 2023 through May 2026 gives a 40-observation recent-cycle reference class. The mean change is 89.7 billion, while the last 12 changes average 77.4 billion; I weight the broader 2023-2026 base rate more because May had a rebound after April weakness but no obvious June-specific fiscal cliff is visible in the public release summary."},{"kind":"text","text":"Current-release adjustment: May 2026 was strong because DPI rose 164.9 billion and DSPI rose 164.8 billion, with wages and salaries at 13388.8 billion and proprietors' income at 2193.6 billion. I do not extrapolate the full May jump, but the level and labor-income trend make a positive June change more likely than a flat or negative one."},{"kind":"math","text":"Prior/update/interval: persistence-plus-mean-change model using May 2026 DSPI 23651.7 plus the 2023-2026 average monthly change of 89.7 gives 23741.4. Historical sample is the 40 successive monthly changes from Feb 2023-May 2026; sigma = 83.6 from those successive changes, so the 80 percent normal half-width is roughly 1.28*sigma = 107.0. No widening beyond that is applied because this is a level series with recent volatility already including negative and large positive monthly moves; implied 80 percent bounds are 23741.4 - 107.0 = 23634.4 and 23741.4 + 107.0 = 23848.3."},{"kind":"text","text":"Counter-considerations: upside risk is a June continuation of May's proprietors' income and transfer-receipt strength, which would land above the interval if DSPI rises more than about 196.6 billion from May. Downside risk is a reversal in farm/proprietors' income, asset income, or tax withholding that would land below the interval if DSPI falls more than about 17.3 billion from May; outside the interval would most likely reflect a discrete tax, transfer, or annual-update effect not visible in the May release."},{"kind":"forecast","point":23741.4,"ciLow":23634.4,"ciHigh":23848.3}]}

# Reviewer critique
{"summary":"Mostly publishable methodologically, but resolver metadata is not fully coherent with the canonical ledger binding.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft names BEA Table 2.6/Table 1 inconsistently and uses a BEA prose resolver while the canonical target binding is ALFRED generic-url DSPI with first-print policy.","actionRequested":"Make the resolver/source wording explicitly match the ledger binding: ALFRED DSPI at the supplied URL as the retained source binding, with BEA DSPI/A067RC first-print provenance noted in reasoning rather than replacing the resolver."},{"rubricItem":"coherence","severity":"warning","summary":"The question says Table 2.6 / DSPI, while the canonical sourceBinding says Personal Income and Outlays, Table 1; the draft repeats Table 2.6 without flagging this table-label mismatch.","actionRequested":"Add a short note that the target is DSPI/A067RC regardless of the table-label discrepancy, and do not let the table label redefine the datapoint."}],"optionalSuggestions":["Keep the July 30, 2026 official BEA release-date discrepancy note, but make clear whether the JSON resolutionDate is intentionally using the official calendar instead of the ledger metadata.","The prior/update/interval and tails are compact and internally coherent; no replacement forecast is needed."]}

Emit the final JSON object only.
