# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.pce_price_index.monthly_change
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bea-pce-price-index-monthly-change-june-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bea.pce_price_index.monthly_change.june_2026.first_print"
- resolutionSourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PCEPI&vintage_date=2026-06-25"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "PCEPI", "releasePolicy": "first_print", "sourceSeriesId": "PCEPI", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PCEPI&vintage_date=2026-06-25", "table": "Personal Income and Outlays", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-15-3f121ef8159dd9e82324d35927f3da89eb6731dce7171364f190afb81d01f7ce.json"
- targetContentHash: "3f121ef8159dd9e82324d35927f3da89eb6731dce7171364f190afb81d01f7ce"
- registrationCommit: "6dcfcbe86a61d979569d385cd1372ae83573a1f9"
- registeredAtUtc: "2026-07-15T19:13:18Z"

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
{"slug":"bea-pce-price-index-monthly-change-june-2026","country":"US","type":"data","title":"US PCE Prices, June 2026","question":"What will BEA report as the seasonally adjusted June 2026 percent change from May in the PCE price index, first print?","unit":"percent_growth","pointEstimate":-0.1,"ciLow":-0.29,"ciHigh":0.09,"confidence":0.8,"resolutionDate":"2026-07-29","resolutionSource":"U.S. Bureau of Economic Analysis Personal Income and Outlays release","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PCEPI&vintage_date=2026-06-25","resolutionRule":"Resolve to the seasonally adjusted percent change from May to June 2026 in the headline PCE price index (PCEPI), as first published by BEA in Personal Income and Outlays, June 2026, rounded to BEA's published one-decimal precision; ignore subsequent revisions.","dataPointId":"bea.pce_price_index.monthly_change.june_2026.first_print","historicalContext":[{"label":"January 2026 first-print monthly PCE inflation","value":0.3},{"label":"February 2026 first-print monthly PCE inflation","value":0.4},{"label":"March 2026 first-print monthly PCE inflation","value":0.7},{"label":"April 2026 first-print monthly PCE inflation","value":0.4},{"label":"May 2026 first-print monthly PCE inflation","value":0.4},{"label":"June 2026 CPI-U monthly change","value":-0.4},{"label":"June 2026 core CPI monthly change","value":0.0}],"drivers":["June CPI energy reversal","Flat June core CPI","PCE's lower energy weight","Recent elevated PCE momentum"],"sourceContext":["https://www.bea.gov/news/2026/personal-income-and-outlays-january-2026","https://www.bea.gov/index.php/news/2026/personal-income-and-outlays-february-2026","https://www.bea.gov/news/2026/personal-income-and-outlays-march-2026","https://www.bea.gov/news/2026/personal-income-and-outlays-april-2026","https://www.bea.gov/index.php/news/2026/personal-income-and-outlays-may-2026","https://www.bls.gov/news.release/archives/cpi_07142026.htm","https://www.bea.gov/news/schedule/"],"runAt":"2026-07-15T19:13:18Z","reasoning":[{"kind":"heading","text":"June 2026 headline PCE price forecast"},{"kind":"text","text":"The target is the first-published, seasonally adjusted one-month change in BEA's headline PCE price index, series PCEPI, from NIPA table 2.8.7—not core PCE or a year-over-year rate. The ledger has concrete resolver defects: BEA's official calendar schedules this release for July 30, 2026, not the registered July 29 resolutionDate, while the mandated ALFRED vintage URL is dated June 25 and therefore cannot contain June's first print; this forecast remains tied to the registered target fields as instructed."},{"kind":"tool","tool":"official.lookup","call":"Fetched BEA January and February 2026 Personal Income and Outlays releases.","result":"BEA reported headline PCE price-index changes of 0.3% in January 2026 and 0.4% in February 2026; February core PCE was 0.4%."},{"kind":"tool","tool":"official.lookup","call":"Fetched BEA March and April 2026 Personal Income and Outlays releases.","result":"BEA reported headline PCE price-index changes of 0.7% in March 2026 and 0.4% in April 2026; the corresponding core readings were 0.3% and 0.2%."},{"kind":"tool","tool":"official.lookup","call":"Fetched BEA May 2026 Personal Income and Outlays release.","result":"BEA reported May 2026 headline PCE inflation of 0.4%, core PCE inflation of 0.3%, and real PCE growth of 0.3%."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS June 2026 CPI release as contemporaneous public-price evidence.","result":"BLS reported June 2026 CPI-U fell 0.4% seasonally adjusted, core CPI was 0.0%, energy fell 5.7%, and food rose 0.2%."},{"kind":"text","text":"The reference class/base rate is the five first-print monthly headline PCE observations for January-May 2026: 0.3%, 0.4%, 0.7%, 0.4%, and 0.4%, averaging 0.44%. This establishes an elevated persistence prior before June-specific information."},{"kind":"text","text":"Inside-view update: the level remains high year over year, but June momentum changed sharply. The one-off 5.7% energy decline pulls headline inflation down; flat core CPI indicates broad monthly disinflation; PCE's different weights, especially its lower gasoline weight, should make headline PCE less negative than CPI. No policy mechanism implies mechanically copying the -0.4% CPI print."},{"kind":"math","text":"Prior/update/interval: persistence model prior = 0.44%, using the January-May first-print historical sample [0.3, 0.4, 0.7, 0.4, 0.4]. Adjustment components are approximately -0.40 percentage point for the June energy reversal and -0.14 point for flat core momentum/PCE-weight translation, giving 0.44 - 0.40 - 0.14 = -0.10%. For this change series, dispersion is computed from the values themselves: sample sigma = sqrt(((0.3-0.44)^2+(0.4-0.44)^2+(0.7-0.44)^2+(0.4-0.44)^2+(0.4-0.44)^2)/4) = 0.152, rounded sigma = 0.15. The 80% half-width is 1.28*sigma = 1.28*0.15 = 0.192, so -0.10 ± 0.192 gives final implied bounds of -0.292% and 0.092%, rounded to [-0.29%, 0.09%]."},{"kind":"text","text":"Upside risk: stronger PCE-specific services or portfolio-management prices could keep the print positive. Downside risk: a larger pass-through from gasoline and other energy declines could push it below -0.29%. Outside the interval on the upside would require a positive print of roughly 0.1% or more; a print below -0.3% would also be outside the interval."},{"kind":"forecast","point":-0.1,"ciLow":-0.29,"ciHigh":0.09}]}

# Reviewer critique
{
  "summary": "Draft is mostly forecast-method complete, but publication should block on the resolver/sourceBinding discrepancy and tighten the uncertainty basis.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft identifies concrete ledger defects: BEA schedules Personal Income and Outlays, June 2026 for 2026-07-30, while the registered resolutionDate is 2026-07-29, and the ALFRED vintage URL dated 2026-06-25 cannot contain the June 2026 first print.",
      "actionRequested": "Before publication, correct or formally waive the target registration/sourceBinding so the resolver uses a post-release first-print source for PCEPI and the official 2026-07-30 release date; keep any forecast record tied to the existing target hash until that target-level decision is made."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The 80% interval is based on only five Jan-May 2026 monthly PCE observations, which understates translation and nowcast uncertainty from CPI to PCE and from volatile energy components.",
      "actionRequested": "Either justify why a five-observation sigma is sufficient for this target or widen/derive the interval from a longer realized monthly PCE sample, historical CPI-to-PCE nowcast errors, or an explicit added uncertainty component."
    }
  ],
  "optionalSuggestions": [
    "State whether the forecast rounds to BEA one-decimal precision only for resolution or whether point/interval JSON intentionally remain at two decimals.",
    "Make the -0.40 energy and -0.14 core/PCE-weight adjustments less opaque by briefly tying them to PCE weights or historical CPI-PCE pass-through."
  ]
}

Emit the final JSON object only.
