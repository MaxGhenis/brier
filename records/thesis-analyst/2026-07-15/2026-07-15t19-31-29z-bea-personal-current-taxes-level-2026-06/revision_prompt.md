# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.personal_current_taxes.level
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bea-personal-current-taxes-level-june-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.personal_current_taxes.level.june_2026.first_print"
- resolutionSourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=W055RC1&vintage_date=2026-06-25"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "W055RC1", "releasePolicy": "first_print", "sourceSeriesId": "W055RC1", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=W055RC1&vintage_date=2026-06-25", "table": "Personal Income and Outlays, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-15-d1c11d1dca6d4747e72624aa27b4adfe284e7962b4f1245f57fee44b2530ec36.json"
- targetContentHash: "d1c11d1dca6d4747e72624aa27b4adfe284e7962b4f1245f57fee44b2530ec36"
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
{"slug":"bea-personal-current-taxes-level-june-2026","country":"US","type":"data","title":"US personal current taxes, June 2026","question":"What will BEA report as June 2026 personal current taxes, monthly seasonally adjusted annual rate, in the first print?","unit":"usd_billions","pointEstimate":3277.2,"ciLow":3266.8,"ciHigh":3287.6,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"U.S. Bureau of Economic Analysis Personal Income and Outlays, Table 2.6","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=W055RC1&vintage_date=2026-06-25","resolutionRule":"Resolve to the June 2026 first-published value for BEA personal current taxes, account W055RC/W055RC1, in Table 2.6, monthly seasonally adjusted annual rate, billions of dollars, rounded to one decimal. Ignore all subsequent revisions. The registered ALFRED URL and expected window are discrepant: its 2026-06-25 vintage predates the June observation, while BEA's official calendar schedules the first print for 2026-07-30; resolution remains tied to the registered target but requires the BEA first print.","dataPointId":"bea.personal_current_taxes.level.june_2026.first_print","historicalContext":[{"label":"January 2026","value":3214.7},{"label":"February 2026","value":3215.3},{"label":"March 2026","value":3229.5},{"label":"April 2026","value":3247.9},{"label":"May 2026","value":3264.7}],"drivers":["recent monthly tax-receipt momentum","continued nominal income and wage growth","withholding and estimated-payment noise","first-print measurement uncertainty"],"sourceContext":["https://www.bea.gov/news/schedule/","https://www.bea.gov/sites/default/files/2026-06/pi0526.pdf","https://fred.stlouisfed.org/series/W055RC1","https://fred.stlouisfed.org/release/tables?eid=155443&rid=54"],"runAt":"2026-07-15T19:32:02Z","reasoning":[{"kind":"heading","text":"June 2026 personal current taxes forecast"},{"kind":"text","text":"The target is BEA account W055RC/W055RC1 in Personal Income and Outlays Table 2.6: monthly personal current taxes, seasonally adjusted at an annual rate, billions of dollars, first print for June 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked the BEA 2026 release schedule and the May Personal Income and Outlays release for the announced June 2026 publication date.","result":"BEA schedules Personal Income and Outlays, June 2026 for July 30, 2026 at 8:30 a.m. EDT; the May release independently states the next release is July 30, 2026 at 8:30 a.m. EDT."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest W055RC1 monthly reference-class observations from the BEA-sourced series and Table 2.6 mirror.","result":"January-May 2026 values were 3214.7, 3215.3, 3229.5, 3247.9, and 3264.7 billion dollars SAAR; May 2025 was 3203.2."},{"kind":"tool","tool":"official.lookup","call":"Checked the latest BEA Personal Income and Outlays release for contemporaneous income conditions.","result":"May 2026 personal income increased 181.6 billion dollars, disposable personal income increased 164.9 billion dollars, and personal current taxes rose from 3247.9 to 3264.7 billion dollars SAAR."},{"kind":"text","text":"The reference class and base rate are the four successive changes from January through May 2026: 0.6, 14.2, 18.4, and 16.8 billion dollars. Their mean is 12.5, indicating positive recent momentum after the nearly flat January-February move."},{"kind":"math","text":"Prior/update/interval: The model is a one-month persistence-plus-mean-change prior using the January-May 2026 historical sample. Starting from 3264.7, the base-rate increment is (0.6 + 14.2 + 18.4 + 16.8)/4 = 12.5. Level effect: 3264.7. Momentum effect: +12.5. One-off adjustment: 0.0 because no June-specific tax-policy discontinuity was identified. Policy-mechanism adjustment: 0.0. Point = 3264.7 + 12.5 = 3277.2. The sample standard deviation of those successive changes is sigma = sqrt(197.8/3) = 8.12. The normal 80% half-width is 1.28*sigma = 1.28*8.12 = 10.39, giving 3277.2 ± 10.39, or 3266.8 to 3287.6 after rounding."},{"kind":"text","text":"Upside risk comes from unusually strong wage withholding, capital-gains-related estimated payments, or stronger taxable income and would land above the interval. Downside risk comes from refund timing, weaker withholding, or an adverse first-print seasonal adjustment and would land below the interval. A tax-policy or payment-timing discontinuity could place the result outside the interval."},{"kind":"text","text":"Resolver discrepancy: the registered expected window ends July 29 and its fixed ALFRED vintage is June 25, but BEA's official schedule and release notice both give July 30. I therefore use the verified July 30 release date while preserving the registered slug, dataPointId, and resolver URL."},{"kind":"forecast","point":3277.2,"ciLow":3266.8,"ciHigh":3287.6}]}

# Reviewer critique
{
  "summary": "Draft has a solid prior/update/interval structure, but it is not publishable until the resolver metadata is aligned with the canonical ledger target or the ledger error is corrected through the proper target process.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "Top-level resolutionDate is 2026-07-30, but the canonical ledger target contract requires 2026-07-29; resolutionSource also names BEA Table 2.6 while the ledger binding names the registered ALFRED W055RC1 URL and Personal Income and Outlays Table 1.",
      "actionRequested": "Keep the forecast tied to the registered slug/dataPointId/source URL and either set the JSON resolver fields to the canonical ledger values while preserving the discrepancy note in reasoning, or route a corrected target registration before publication."
    },
    {
      "rubricItem": "resolver",
      "severity": "blocking",
      "summary": "The draft identifies a likely concrete ledger error: the registered ALFRED vintage_date=2026-06-25 predates the June 2026 observation and cannot contain the June first print.",
      "actionRequested": "Do not rely on the impossible ALFRED vintage as if it resolves June 2026; explicitly flag this as a target-contract discrepancy for review while keeping the forecast on the same target."
    },
    {
      "rubricItem": "coherence",
      "severity": "warning",
      "summary": "The question/title refer to Table 2.6, while the canonical sourceBinding says Personal Income and Outlays, Table 1.",
      "actionRequested": "Harmonize the table reference with the ledger contract or state that W055RC1 appears in the cited mirror/table but the registered binding names Table 1."
    }
  ],
  "optionalSuggestions": [
    "The four-change January-May sample is very short; mention that the 80% interval is narrow because it uses only recent realized monthly changes.",
    "Tail scenarios are directionally useful, but could be more concrete by naming approximate June change sizes needed to miss the interval."
  ]
}

Emit the final JSON object only.
