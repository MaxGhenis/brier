# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.pce.core_mom
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bea-pce-core-mom-june-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bea.pce.core_mom.june_2026.first_print"
- resolutionSourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PCEPILFE&vintage_date=2026-06-25"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "PCEPILFE", "releasePolicy": "first_print", "sourceSeriesId": "PCEPILFE", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PCEPILFE&vintage_date=2026-06-25", "table": "Personal Income and Outlays", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-15-5839898680c429f390013595cf61531a7d62b72b9316886807d2aa9c05680b79.json"
- targetContentHash: "5839898680c429f390013595cf61531a7d62b72b9316886807d2aa9c05680b79"
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
{"slug":"bea-pce-core-mom-june-2026","country":"US","type":"data","title":"US Core PCE MoM, June 2026","question":"What will the BEA first-print seasonally adjusted month-over-month percent change be for the Personal Consumption Expenditures price index excluding food and energy, June 2026?","unit":"percent_growth","pointEstimate":0.19,"ciLow":0.08,"ciHigh":0.3,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"BEA Personal Income and Outlays / ALFRED PCEPILFE first vintage","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PCEPILFE&vintage_date=2026-06-25","resolutionRule":"Resolve to the first-print June 2026 seasonally adjusted month-over-month percent change in BEA's PCE price index excluding food and energy, series PCEPILFE / BEA account DPCCRG, from the Personal Income and Outlays release. Use the first official print only; do not use later revisions. If using PCEPILFE index levels, compute 100*(June 2026 index / May 2026 index - 1) and round consistently with BEA's published one-decimal percent-change presentation.","dataPointId":"bea.pce.core_mom.june_2026.first_print","historicalContext":[{"label":"May 2026 PCEPILFE MoM derived from 130.082/129.667","value":0.32},{"label":"April 2026 PCEPILFE MoM derived from 129.667/129.343","value":0.251},{"label":"March 2026 PCEPILFE MoM derived from 129.343/128.961","value":0.296},{"label":"February 2026 PCEPILFE MoM derived from 128.961/128.455","value":0.394}],"drivers":["June core CPI was flat, lowering the near-term PCE read-through","June PPI core services and core final-demand measures were positive but milder than May","May core PCE was still firm at 0.3 percent","Shelter and medical-care CPI components cooled in June","PPI trade and financial-service components keep some upside pressure"],"sourceContext":["https://www.bea.gov/news/schedule","https://www.bea.gov/news/2026/personal-income-and-outlays-may-2026","https://fred.stlouisfed.org/series/PCEPILFE","https://fred.stlouisfed.org/release/tables?eid=3208&rid=54","https://www.bls.gov/news.release/cpi.nr0.htm","https://www.bls.gov/news.release/ppi.nr0.htm"],"runAt":"2026-07-15T16:39:05Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 Core PCE MoM"},{"kind":"text","text":"Framing and exact resolver: the target is the BEA first-print seasonally adjusted PCE price index excluding food and energy for June 2026, not headline PCE, not market-based core PCE, and not a revised vintage. I kept the catalog slug and dataPointId. I found a ledger discrepancy: the provided ALFRED resolution URL uses vintage_date=2026-06-25, while BEA's official calendar and May release both show the June 2026 Personal Income and Outlays release on July 30, 2026; the forecast remains tied to this target and states the discrepancy rather than changing the catalog identity."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA release schedule and the May 2026 Personal Income and Outlays next-release notice for the June 2026 PCE release date.","result":"BEA schedule lists Personal Income and Outlays, June 2026 on July 30, 2026 at 8:30 AM; the May release also says Next release: July 30, 2026 at 8:30 a.m. EDT for Personal Income and Outlays, June 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched BEA/FRED PCEPILFE recent same-variant history for the seasonally adjusted core PCE chain-type price index.","result":"PCEPILFE index values: Jan 2026 128.455, Feb 2026 128.961, Mar 2026 129.343, Apr 2026 129.667, May 2026 130.082. BEA May release reports PCE price index excluding food and energy +0.3 percent in April and +0.3 percent in May, with 3.4 percent year-over-year in May."},{"kind":"tool","tool":"official.lookup","call":"Fetched June 2026 BLS CPI details used as the main consumer-price input into the PCE nowcast.","result":"June 2026 CPI-U fell 0.4 percent month over month and rose 3.5 percent year over year; all items less food and energy was unchanged at 0.0 percent month over month and rose 2.6 percent year over year; energy fell 5.7 percent; shelter rose 0.1 percent; medical care services fell 0.1 percent."},{"kind":"tool","tool":"official.lookup","call":"Fetched June 2026 BLS PPI details for PCE-relevant services and goods pipeline inputs.","result":"June 2026 PPI final demand fell 0.3 percent; final demand less foods, energy, and trade services rose 0.1 percent; final demand goods fell 1.4 percent; final demand services rose 0.2 percent; gasoline fell 12.0 percent; margins for fuels and lubricants retailing rose 13.0 percent."},{"kind":"text","text":"Reference class / base rate: the same-variant PCEPILFE recent monthly growth rates from the fetched index levels are about 0.394 percent in February, 0.296 percent in March, 0.251 percent in April, and 0.320 percent in May, for a short-run base rate near 0.315 percent. That is the persistence prior before mapping June CPI and PPI inputs into core PCE."},{"kind":"math","text":"Prior/update/interval: persistence prior = mean(Feb-May derived PCEPILFE MoM) = (0.394 + 0.296 + 0.251 + 0.320)/4 = 0.315 percent. Adjustments: June core CPI flat rather than May's 0.2 percent subtracts 0.09 pp; June PPI final demand less foods, energy, and trade services at 0.1 percent and services at 0.2 percent subtracts 0.03 pp versus May's firmer inputs; residual PCE-specific services, portfolio/financial fees, and healthcare add back 0.00 to 0.02 pp. Final point = 0.315 - 0.09 - 0.03 - 0.005 = 0.19 percent. For the interval, using the four fetched recent PCEPILFE monthly changes, sigma = 0.060 percentage points; 1.28*sigma = 0.077 pp. I widen to about 0.11 pp, or 1.45x the reference half-width, because CPI/PPI-to-PCE mapping and financial-services components are not fully pinned down before BEA. This gives 0.19 +/- 0.11 = [0.08, 0.30]."},{"kind":"text","text":"Counter-considerations: upside risk would come from PCE-weighted financial services, insurance, or healthcare prices staying closer to May's firm pulse despite flat core CPI, which would land above the interval if core PCE prints above 0.30 percent. Downside risk would come from the June flat core CPI pass-through dominating PCE services and goods, plus weaker portfolio-management fees, which would land below the interval if the first print is below 0.08 percent. An outside the interval outcome is most plausible if BEA-specific source-data adjustments or a large services component diverges sharply from CPI/PPI."},{"kind":"forecast","point":0.19,"ciLow":0.08,"ciHigh":0.3}]}

# Reviewer critique
{"summary":"The draft is publishable with one resolver metadata caveat: it clearly states the ledger/source-date discrepancy and otherwise satisfies the prior, update, interval, tails, and coherence requirements.","requiredFixes":[],"optionalSuggestions":["Consider making the ALFRED vintage-date discrepancy even more explicit in the final resolver paragraph: the ledger URL has vintage_date=2026-06-25 even though the June 2026 first print is expected with the July 30, 2026 BEA release.","If the publication pipeline allows reviewer notes, flag the expectedReleaseWindow ending 2026-07-29 versus the stated BEA July 30, 2026 release date for catalog follow-up."]}

Emit the final JSON object only.
