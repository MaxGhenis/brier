# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fns.snap.total_persons
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "snap-participation-june-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "usda.fns.snap.persons.june_2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-11-03", "start": "2026-10-26"}, "field": "Persons", "releasePolicy": "first_print", "sourceSeriesId": "fns.snap.total_persons", "sourceUrl": "https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap", "table": "FNS SNAP data tables, national monthly participation (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-fa0d017e2d4445b343793d95ea532622f4da9946c9dc0ce333ef7298be904a6d.json"
- targetContentHash: "fa0d017e2d4445b343793d95ea532622f4da9946c9dc0ce333ef7298be904a6d"
- registrationCommit: "79e7796ea8cde8d3c263a226250346d3aa2c88d9"
- registeredAtUtc: "2026-07-10T17:47:41Z"

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
{"slug":"snap-participation-june-2026","country":"US","type":"data","title":"US SNAP Participation, June 2026","question":"What will USDA FNA first report for total persons participating in SNAP nationally in June 2026, unadjusted, in millions?","unit":"millions","pointEstimate":35.55,"ciLow":34.71,"ciHigh":36.39,"confidence":0.8,"resolutionDate":"2026-11-03","resolutionSource":"USDA Food and Nutrition Administration SNAP Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","resolutionRule":"Resolve to the first value published for Persons for June 2026 in the USDA FNA SNAP national monthly participation table, reported in thousands and multiplied by 0.001 to millions. Use the first print available on the specified SNAP Data Tables page; disregard later revisions. Round the resolved value to three decimal places in millions.","dataPointId":"usda.fns.snap.persons.june_2026","historicalContext":[{"label":"January 2026 first available official table value","value":38.456892},{"label":"February 2026 first available official table value","value":37.72941},{"label":"March 2026 latest official table value","value":37.298271},{"label":"June 2025 official table value","value":42.08488}],"drivers":["Strong FY2026 participation downtrend","Recent monthly decline beginning to moderate","Tighter eligibility and work-requirement environment","Administrative reporting volatility"],"sourceContext":["https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","https://fns-prod.azureedge.us/sites/default/files/resource-files/snap-4fymonthly-6.pdf","https://fns-prod.azureedge.us/pd/overview","https://www.fns.usda.gov/snap/recipient/eligibility"],"runAt":"2026-07-10T17:51:47Z","reasoning":[{"kind":"heading","text":"June 2026 national SNAP participation forecast"},{"kind":"text","text":"The resolver is the unadjusted national Persons field for June 2026 in the FNS/FNA SNAP monthly participation table, not an annual quality-control measure. The official table reports persons in thousands; the cell converts that figure to millions. The first print is binding, with no correction-day grace period."},{"kind":"tool","tool":"official.lookup","call":"Fetch the USDA FNA SNAP national monthly participation table and read the latest FY2026 Persons observations.","result":"The table dated June 12, 2026 reports 38,456,892 persons in January 2026, 37,729,410 in February 2026, and 37,298,271 in March 2026, equivalent to 38.456892, 37.729410, and 37.298271 million."},{"kind":"tool","tool":"official.lookup","call":"Fetch the same official SNAP table's recent reference-class history.","result":"Official Persons values were 42,180,523 in February 2025, 42,193,855 in March, 42,353,149 in April, 42,248,301 in May, 42,084,880 in June, 42,012,830 in July, 41,836,900 in August, and 41,633,090 in September."},{"kind":"tool","tool":"official.lookup","call":"Check the official SNAP table's FY2026 transition and annual summaries.","result":"Persons fell from 41,091,800 in October 2025 to 39,997,940 in November and 39,205,146 in December; USDA reports FY2025 average participation of 42,383,194 and the preliminary FY2026-to-date average of 38,963,243."},{"kind":"tool","tool":"official.lookup","call":"Verify the release timing against the official FNA program-data schedule and target release window.","result":"The official schedule places the June 2026 SNAP monthly-table release on 2026-11-03; the latest table available during this run covered March 2026 and was dated 2026-06-12."},{"kind":"text","text":"The outside-view base rate is persistence with drift for a slowly moving administrative caseload. The 13 monthly changes from February 2025 through March 2026 average -0.376 million, but the FY2026 decline is much steeper: October-to-March participation fell 3.794 million. Level is therefore anchored at March's 37.298 million; momentum remains negative, while the shrinking March decline supplies a moderating adjustment."},{"kind":"text","text":"Mechanisms are separated as follows: level 37.298 million; momentum approximately -0.58 million per month over April-June; moderation adds about 0.10 million per month relative to the latest FY2026 trend; tighter eligibility and work rules retain a negative policy adjustment. These components imply about 35.55 million rather than simple flat persistence."},{"kind":"math","text":"Prior/update/interval: persistence-with-drift prior; historical sample is the 13 successive monthly changes from February 2025 through March 2026. Their sample standard deviation is sigma = 0.376 million, so the one-step 80% half-width is 1.28*sigma = 1.28*0.376 = 0.482 million. For a three-month horizon, scale by sqrt(3): 0.482*1.732 = 0.835, rounded to 0.84 million. Point = 37.298 - 1.748 = 35.550; bounds = 35.550 +/- 0.840 = [34.710, 36.390]."},{"kind":"text","text":"Upside risk: faster stabilization in enrollment or delayed implementation of tighter eligibility rules would land above 36.39 million. Downside risk: continued declines near the November-January pace, broad recertification losses, or unusually aggressive enforcement would land below 34.71 million, outside the interval."},{"kind":"forecast","point":35.55,"ciLow":34.71,"ciHigh":36.39}]}

# Reviewer critique
{
  "summary": "The draft is mostly publishable, but it should correct the agency/source naming and tighten the compact prior/update step so the numerical adjustment is fully auditable.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The draft repeatedly says USDA FNA/Food and Nutrition Administration, but the target resolver is USDA FNS/Food and Nutrition Service SNAP data tables.",
      "actionRequested": "Change the title/reasoning/resolutionSource text to USDA Food and Nutrition Service or USDA FNS while keeping the same resolver URL, first-print rule, dataPointId, unit conversion, and 2026-11-03 resolutionDate."
    },
    {
      "rubricItem": "prior_update_interval",
      "severity": "warning",
      "summary": "The compact Prior/update/interval step gives the final -1.748 million adjustment but does not break out the stated momentum, moderation, and policy components in the same auditable step.",
      "actionRequested": "Revise the compact step to explicitly show the March 2026 anchor, the three-month drift or momentum calculation, any moderation and policy adjustments, the resulting point, the volatility sample, the sqrt(3) interval scaling, and the final implied bounds."
    }
  ],
  "optionalSuggestions": [
    "Clarify whether the 13-change volatility sample is based on first-print values only, if that is knowable from the cited table.",
    "Make the downside tail slightly more concrete by naming what monthly decline path would put June 2026 below 34.71 million."
  ]
}

Emit the final JSON object only.
