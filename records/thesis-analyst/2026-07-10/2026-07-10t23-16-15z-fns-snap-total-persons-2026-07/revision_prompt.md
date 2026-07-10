# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fns.snap.total_persons
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "snap-participation-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "usda.fns.snap.persons.july_2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-12-07", "start": "2026-11-29"}, "field": "Persons", "releasePolicy": "first_print", "sourceSeriesId": "fns.snap.total_persons", "sourceUrl": "https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap", "table": "FNS SNAP data tables, national monthly participation (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-9a15e6578b701e805a6459126176e230c3d057077fa7f2b829d129dfa24dae30.json"
- targetContentHash: "9a15e6578b701e805a6459126176e230c3d057077fa7f2b829d129dfa24dae30"
- registrationCommit: "a6aa0d72352081ffa58d0615c5daf6c7c553e4ee"
- registeredAtUtc: "2026-07-10T23:13:40Z"

# Source hints
- Use USDA FNS program-data pages, official data tables, and the FNS data release calendar.
- For SNAP, WIC, and QC targets, distinguish annual fiscal-year quality-control releases from monthly participation tables.
- If the catalog unit is millions, convert official person counts to millions in the emitted cell.

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
{"slug":"snap-participation-july-2026","country":"US","type":"data","title":"US SNAP participation, July 2026","question":"What will USDA FNS report as national SNAP participation (Persons) for July 2026 in the first published monthly table, in millions?","unit":"millions","pointEstimate":35.9,"ciLow":34.8,"ciHigh":37.0,"confidence":0.8,"resolutionDate":"2026-12-07","resolutionSource":"USDA Food and Nutrition Service SNAP Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","resolutionRule":"Resolve to the Persons value for July 2026 in the first official FNS SNAP national monthly participation table published for that month. Convert the table value from thousands to millions by multiplying by 0.001 and round to three decimals; ignore all subsequent revisions. No release-day correction or grace exception applies.","dataPointId":"usda.fns.snap.persons.july_2026","historicalContext":[{"label":"January 2026","value":38.456892},{"label":"February 2026","value":37.72941},{"label":"March 2026","value":37.298271},{"label":"July 2025","value":42.01283}],"drivers":["rapid recent participation decline","expanded SNAP eligibility and work-requirement effects","slowing month-to-month decline by March","administrative reporting and preliminary-data volatility"],"sourceContext":["https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","https://www.fns.usda.gov/sites/default/files/resource-files/snap-4fymonthly-6.pdf"],"runAt":"2026-07-10T23:17:11Z","reasoning":[{"kind":"heading","text":"Forecast: July 2026 national SNAP participation"},{"kind":"text","text":"The resolver is the first official national monthly SNAP table's Persons value for July 2026, not a quality-control release, state subtotal, household count, annual average, or later revision. The stable series page is the exact FNS SNAP Data Tables page; the ledger's official-calendar registration fixes publication on 2026-12-07."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest USDA FNS national monthly SNAP participation PDF and read the Persons column for FY 2026.","result":"The June 12, 2026 table reports 38,456,892 persons in January 2026, 37,729,410 in February 2026, and 37,298,271 in March 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetch the same-variant historical Persons observations from the official national monthly table.","result":"The table reports 42,012,830 persons in July 2025, 41,836,900 in August 2025, 41,633,090 in September 2025, and 41,091,800 in October 2025."},{"kind":"tool","tool":"official.lookup","call":"Check the official FNS publication metadata and registered release schedule for the exact monthly table.","result":"The official table is dated June 12, 2026, contains data through March 2026, and the official schedule registers the July 2026 first print for 2026-12-07."},{"kind":"text","text":"The reference class/base rate is the 24 successive monthly changes from March 2024 through March 2026 in the same Persons series. Participation moved from 41.572 million in March 2024 to 37.298 million in March 2026; the mean monthly change was about -0.178 million, while the latest five changes were materially more negative as eligibility and administrative changes took effect."},{"kind":"math","text":"Prior/update/interval: The model is a damped monthly-change persistence prior using the 24-change historical sample. Its level anchor is March 2026 at 37.298 million. The 24 successive changes have sum about -4.273 million and sum of squares about 5.053, so sample sigma = sqrt((5.053 - 24*(-0.178)^2)/23) = 0.432 million. Level and momentum imply four further declines averaging about 0.35 million, giving 37.298 - 4*0.35 = 35.898, rounded to 35.9. The one-month 80% half-width is 1.28*sigma = 1.28*0.432 = 0.553 million; I widen it to about 1.10 million because July is four monthly transitions beyond the March anchor, approximately sqrt(4)*0.553. Final implied bounds are 35.9 - 1.1 = 34.8 and 35.9 + 1.1 = 37.0 million."},{"kind":"text","text":"Upside risk comes from the March deceleration persisting, delayed implementation, or reinstatement of eligible cases; participation above 37.0 million would land outside the interval. Downside risk comes from another wave of eligibility terminations or unusually fast recertification effects; participation below 34.8 million would land outside the interval."},{"kind":"forecast","point":35.9,"ciLow":34.8,"ciHigh":37.0}]}

# Reviewer critique
{
  "summary": "The draft is publishable in structure, but it has a likely blocking evidence/model issue around the claimed 2026 SNAP decline and policy driver, which appears inconsistent with the cited historical values and needs substantiation or revision.",
  "requiredFixes": [
    {
      "rubricItem": "update",
      "severity": "blocking",
      "summary": "The inside-view update relies on 'expanded SNAP eligibility and work-requirement effects' and 'rapid recent participation decline,' but the cited evidence only shows reported series values and does not substantiate the policy mechanism or why the recent decline should average -0.35 million per month through July.",
      "actionRequested": "Either cite concrete official evidence for the eligibility/work-requirement implementation affecting this target period, or remove that driver and restate the update as a purely statistical momentum adjustment with a clear shrinkage rationale."
    },
    {
      "rubricItem": "base_rate",
      "severity": "warning",
      "summary": "The draft states a 24-change March 2024 through March 2026 base-rate sample, but only a few observations are shown in historicalContext and sourceContext.",
      "actionRequested": "Add enough compact detail to make the historical sample auditable, such as the start/end values, mean monthly change, latest five-change mean, and confirmation that all values come from the same first-print FNS Persons series."
    },
    {
      "rubricItem": "model_prior",
      "severity": "warning",
      "summary": "The model prior is named as damped monthly-change persistence, but the damping rule is not explicit; the forecast uses -0.35 million per month without showing how it is derived from the 24-month mean and latest-five momentum.",
      "actionRequested": "State the exact formula or judgmental weighting that maps the historical mean and recent changes to the -0.35 million monthly decline."
    },
    {
      "rubricItem": "interval",
      "severity": "warning",
      "summary": "The interval uses sqrt(4) scaling of one-month volatility, which is reasonable, but it appears to ignore uncertainty in the selected -0.35 million monthly drift and possible first-print reporting noise.",
      "actionRequested": "Briefly state whether the 80% interval is innovation-only or includes drift/model uncertainty; widen or justify unchanged bounds accordingly."
    }
  ],
  "optionalSuggestions": [
    "Keep the resolver wording; it matches the ledger target, unit conversion, first-print rule, and 2026-12-07 resolution date.",
    "Clarify whether 'expanded SNAP eligibility' is intended to mean expanded restrictions or administrative eligibility changes, since the phrase currently reads directionally ambiguous.",
    "Add one sentence that no catalog forecast point or interval was used as an input."
  ]
}

Emit the final JSON object only.
