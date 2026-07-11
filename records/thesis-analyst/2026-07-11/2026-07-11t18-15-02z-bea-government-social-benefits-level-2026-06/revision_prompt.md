# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bea.government_social_benefits.level
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bea-government-social-benefits-level-june-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.government_social_benefits.level.june_2026.first_print"
- resolutionSourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=A063RC1&vintage_date=2026-06-25"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "A063RC1", "releasePolicy": "first_print", "sourceSeriesId": "A063RC1", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=A063RC1&vintage_date=2026-06-25", "table": "Personal Income and Outlays, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-11-9ff32676acb57877e9b6c73c923544fceea7817cc4e300041781188cd157cc14.json"
- targetContentHash: "9ff32676acb57877e9b6c73c923544fceea7817cc4e300041781188cd157cc14"
- registrationCommit: "357f4e8477327d91775a345ece531f3eb42fa3b7"
- registeredAtUtc: "2026-07-11T18:10:24Z"

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
{"slug":"bea-government-social-benefits-level-june-2026","country":"US","type":"data","title":"US government social benefits, June 2026","question":"What will BEA first report for June 2026 personal current transfer receipts: government social benefits to persons (A063RC1), monthly, seasonally adjusted at an annual rate, in billions of dollars?","unit":"usd_billions","pointEstimate":5028.3,"ciLow":5005.4,"ciHigh":5051.2,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"U.S. Bureau of Economic Analysis, Personal Income and Outlays, Table 2.6","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=A063RC1&vintage_date=2026-06-25","resolutionRule":"Resolve to the June 2026 value of BEA series A063RC1, Personal current transfer receipts: government social benefits to persons, monthly seasonally adjusted annual rate, in billions of dollars, as first published in the July 30, 2026 Personal Income and Outlays release; use the displayed one-decimal value and ignore later revisions. The registered resolver has a concrete discrepancy: its ALFRED vintage_date=2026-06-25 predates the June release and cannot contain the June first print, while BEA's official calendar places the release on July 30 rather than within the registered July 21–29 window. This forecast remains tied to the registered dataPointId and resolver URL, but resolution machinery must correct that binding to the July 30 first-print vintage.","dataPointId":"bea.government_social_benefits.level.june_2026.first_print","historicalContext":[{"label":"January 2026","value":5002.8},{"label":"February 2026","value":4988.0},{"label":"March 2026","value":4991.0},{"label":"April 2026","value":4995.7},{"label":"May 2026","value":5024.4}],"drivers":["May level provides the persistence anchor","Recent monthly changes show modest underlying growth with occasional benefit-payment jumps","Social Security and Medicaid source-data revisions create first-print uncertainty","No identified June policy change warrants extrapolating May's unusually large increase"],"sourceContext":["https://fred.stlouisfed.org/series/A063RC1/","https://www.bea.gov/sites/default/files/2026-06/pi0526.pdf","https://www.bea.gov/news/schedule/"],"runAt":"2026-07-11T18:15:26Z","reasoning":[{"kind":"heading","text":"June 2026 government social benefits first-print forecast"},{"kind":"text","text":"The target is BEA account A063RC/A063RC1 in NIPA Table 2.6: monthly personal current transfer receipts from government social benefits, billions of dollars at a seasonally adjusted annual rate. It resolves on the first June 2026 print, not a later revised observation."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest published A063RC1 monthly observations and units from the BEA-sourced FRED series page.","result":"Fetched January 2026 5002.8, February 4988.0, March 4991.0, April 4995.7, and May 5024.4 billion dollars, monthly seasonally adjusted annual rate."},{"kind":"tool","tool":"official.lookup","call":"Inspect BEA's May 2026 Personal Income and Outlays release for contemporaneous aggregate-income conditions.","result":"BEA reported May personal income up 181.6 billion, disposable personal income up 164.9 billion, and PCE up 156.1 billion; the release also reported revisions to Social Security and Medicaid benefits."},{"kind":"tool","tool":"official.lookup","call":"Calculate the recent A063RC1 reference-class changes from the fetched monthly observations.","result":"Fetched-level successive changes were -14.8, +3.0, +4.7, and +28.7 billion from January through May 2026; their mean was +5.4 billion and sample standard deviation was 17.9 billion."},{"kind":"text","text":"The reference class and base rate are short-horizon monthly level forecasts for this same SAAR series. Persistence is the primary prior: May's 5024.4 level is more informative than extrapolating its exceptional +28.7 increase, while the four-change mean of +5.4 indicates a gently rising underlying path."},{"kind":"text","text":"BEA's official release calendar, corroborated by the May release itself, schedules Personal Income and Outlays for June 2026 at 8:30 a.m. on July 30, 2026. This conflicts with the registered expected window ending July 29 and with its June 25 ALFRED vintage, which is too early to resolve June."},{"kind":"math","text":"Prior/update/interval: persistence model prior = May 5024.4; historical sample = January–May 2026 levels with changes -14.8, +3.0, +4.7, +28.7. Adjustment components are +3.9 billion for the median recent monthly change, +0.0 for known one-offs, and +0.0 for identified June policy changes, giving 5024.4 + 3.9 = 5028.3. From the four successive changes, sample sigma = 17.9 billion; the normal-reference 80% half-width is 1.28*sigma = 1.28*17.9 = 22.9 billion. Thus the final implied bounds are 5028.3 - 22.9 = 5005.4 and 5028.3 + 22.9 = 5051.2."},{"kind":"text","text":"Upside risk comes from another discrete acceleration in Social Security, Medicare, Medicaid, veterans, or disaster-related benefits and would land above the interval if the June increase exceeds about 26.8 billion. Downside risk comes from payment timing, normalization after May, or adverse first-print source-data revisions and would land below the interval if June falls more than about 19.0 billion."},{"kind":"forecast","point":5028.3,"ciLow":5005.4,"ciHigh":5051.2}]}

# Reviewer critique
{"summary":"Draft is mostly publication-ready, but the resolver binding/date discrepancy must be handled explicitly in the published target metadata rather than left as an internally contradictory forecast record.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The draft correctly identifies that the registered ALFRED vintage_date=2026-06-25 cannot contain the June 2026 first print, but its JSON still carries that URL while the rule says to use the July 30 first print.","actionRequested":"Either correct the target/source binding through the approved target metadata path before publication, or keep the canonical resolver fields unchanged and move the discrepancy to reasoning only; do not publish a forecast whose resolver URL and resolution rule point to different vintages."},{"rubricItem":"coherence","severity":"warning","summary":"The draft uses BEA Table 2.6 in the question/resolutionSource, while the ledger sourceBinding says Personal Income and Outlays, Table 1 for field A063RC1.","actionRequested":"Align the table reference with the canonical ledger resolver text or state the table discrepancy explicitly without changing the target identity."}],"optionalSuggestions":["The prior/update/interval step is strong and names the persistence prior, sample, adjustment, sigma method, and bounds.","Tail scenarios are concrete; consider adding one sentence that the interval is intentionally based on only four recent changes and therefore is fragile."]}

Emit the final JSON object only.
