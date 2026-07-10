# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fns.snap.total_persons
- period: 2026-05
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "snap-participation-may-2026"
- targetUnit: "millions"
- dataPointId: "usda.fns.snap.persons.may_2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-10-04", "start": "2026-09-26"}, "field": "Persons", "releasePolicy": "first_print", "sourceSeriesId": "fns.snap.total_persons", "sourceUrl": "https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap", "table": "FNS SNAP data tables, national monthly participation (thousands)", "transform": {"factor": 0.001, "operation": "multiply"}}

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
{"slug":"snap-participation-may-2026","country":"US","type":"data","title":"SNAP Participation, May 2026","question":"What will USDA FNS first report as total SNAP persons participating for May 2026 in the national monthly Persons table, not seasonally adjusted, converted to millions?","unit":"millions","pointEstimate":38.2,"ciLow":37.15,"ciHigh":39.25,"confidence":0.8,"resolutionDate":"2026-10-04","resolutionSource":"USDA Food and Nutrition Service SNAP Data Tables, national monthly Persons, Households, Benefits, and Average Monthly Benefit per Person and Household","resolutionSourceUrl":"https://www.fns.usda.gov/sites/default/files/resource-files/snap-4fymonthly-2.pdf","resolutionRule":"Resolve to the first official USDA FNS print for May 2026 total SNAP Persons in the national monthly participation table, using the not seasonally adjusted national total. Convert official persons to millions by multiplying by 0.000001, or official thousands to millions by multiplying by 0.001 if the released table is in thousands. Use the first print only; ignore later revisions unless the first print is withdrawn before publication as an official release.","dataPointId":"usda.fns.snap.persons.may_2026","historicalContext":[{"label":"Nov 2025 initial","value":40.395735},{"label":"Oct 2025 preliminary","value":41.0918},{"label":"Sep 2025","value":41.63309},{"label":"May 2025","value":42.248301},{"label":"Nov 2024","value":43.018848}],"drivers":["Recent official SNAP participation fell from 43.019 million in November 2024 to 40.396 million in November 2025.","Expanded 2025-2026 eligibility and work-requirement enforcement points to further participation losses by May 2026.","The November 2025 initial print is explicitly preliminary and subject to significant revision, so I avoid extrapolating its exact one-month drop mechanically.","Economic need and food-price pressure limit the downside because eligible households still have strong demand for benefits.","State implementation timing creates wide uncertainty around the May 2026 first print."],"sourceContext":["https://www.fns.usda.gov/pd/supplemental-nutrition-assistance-program-snap","https://www.fns.usda.gov/sites/default/files/resource-files/snap-4fymonthly-2.pdf","https://www.fns.usda.gov/sites/default/files/resource-files/snap-persons-2.pdf","https://www.fns.usda.gov/sites/default/files/resource-files/snap-annualsummary-2.pdf","https://apnews.com/article/4e9016f6919a603cb7d35b9c9fcb9048"],"runAt":"2026-07-10T04:17:17Z","reasoning":[{"kind":"heading","text":"USDA FNS SNAP persons forecast for May 2026"},{"kind":"text","text":"Framing and exact resolver: this is the USDA FNS SNAP national monthly Persons series, not state detail, not annual QC, not benefits paid, and not seasonally adjusted. The target unit is millions and the resolver is first print; the official table currently labels FY 2026 values as preliminary and subject to revision, so this forecast targets the first May 2026 print rather than later revised values."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA FNS SNAP Data Tables page and national monthly SNAP PDF.","result":"Fetched official national monthly values: May 2025 Persons 42,248,301; Sep 2025 Persons 41,633,090; Oct 2025 Persons 41,091,800; Nov 2025 Persons 40,395,735; FY 2026-to-date annual summary 40,743,768 persons as of data dated February 13, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA FNS SNAP Number of Persons Participating state-level PDF for the latest available month.","result":"Fetched official latest state-detail totals: TOTAL November 2024 43,018,848; TOTAL October 2025 41,091,800; TOTAL November 2025 initial 40,395,735; November 2025 vs October 2025 percent change -1.7%; November 2025 vs November 2024 percent change -6.1%."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA FNS SNAP annual participation and cost summary PDF.","result":"Fetched official annual average participation: FY 2023 42,177 thousand; FY 2024 41,452 thousand; FY 2025 42,126 thousand; FY 2025 average benefit per person 187.94 dollars; FY 2025 total benefits 95,007.20 million dollars."},{"kind":"tool","tool":"public.lookup","call":"Checked public reporting on 2026 SNAP policy implementation and participation pressure.","result":"Fetched public policy context with numbers: AP reported nearly 42 million Americans receive SNAP, the expanded work requirements apply to adults aged 55-64 in addition to prior groups, and CBO projected about 2.4 million fewer SNAP participants over the next decade."},{"kind":"text","text":"Release-date note: the canonical ledger target supplies an expected official release window ending 2026-10-04 for the May 2026 first print. I used that target-contract resolutionDate. Discrepancy: in the accessible FNS pages fetched here, I found official table update dates and latest-month metadata, but not a separate public FNS calendar entry naming the May 2026 SNAP release date."},{"kind":"text","text":"Base rate/reference class: for this same official national monthly Persons variant, recent month-to-month changes from Nov 2024 through Nov 2025 averaged about -0.219 million per month, with the last four official changes at -0.204, -0.541, and -0.696 million into the Oct-Nov policy/shutdown period. The base rate is therefore a declining caseload, not a flat persistence series."},{"kind":"math","text":"Prior/update/interval: persistence prior starts from the latest official first-print national value of 40.395735 million in Nov 2025. Historical sample is the same USDA FNS national monthly Persons series from Nov 2024-Nov 2025; successive-change sigma = 0.27 million. A one-month 80% half-width is 1.28*sigma = 0.35 million; scaling six months gives about 0.35*sqrt(6) = 0.86 million. Level/momentum adjustment applies -0.8 million for continuing recent decline, policy-mechanism adjustment applies -1.1 million for expanded work requirements and immigrant eligibility tightening by spring 2026, and one-off/reporting adjustment adds -0.3 million because latest initial prints show disruption but may revise. Point = 40.396 - 0.8 - 1.1 - 0.3 = 38.196 million, rounded to 38.20. I widen the six-month 0.86 million half-width to 1.05 million because policy implementation is staggered by state and first-print reporting is volatile, yielding 37.15 to 39.25 million."},{"kind":"text","text":"Counter-considerations: upside risk would come from November 2025 being materially undercounted or revised upward before the May first print pattern, from court or state administrative delays slowing terminations, or from weaker labor-market conditions raising eligible need; those would land above the interval if participation remains over 39.25 million. Downside risk would come from faster state enforcement, large documentation failures, or additional immigrant/work-rule terminations by May; those would land below the interval if participation falls under 37.15 million. Outside the interval is most plausible if the latest official initial prints are not comparable to normal participation counts."},{"kind":"forecast","point":38.2,"ciLow":37.15,"ciHigh":39.25}]}

# Reviewer critique
{
  "summary": "Publishable after warnings are addressed: the forecast is coherent and well traced, but the resolver URL and size of the policy adjustment need tightening.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "resolutionSourceUrl points to the current PDF rather than the canonical ledger sourceUrl for the SNAP data tables page.",
      "actionRequested": "Use the canonical FNS SNAP data tables page as the resolver URL, and keep the PDF/table name in the resolver text if needed."
    },
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "the -1.1 million policy-mechanism adjustment is material but only loosely tied to cited evidence and implementation timing by May 2026.",
      "actionRequested": "Add one sentence connecting the adjustment to concrete policy effective dates, affected groups, or explain why the CBO decade-scale estimate justifies a spring-2026 movement of this size."
    },
    {
      "rubricItem": "prior_update_interval",
      "severity": "warning",
      "summary": "the compact step has the right ingredients, but the base-rate prior appears after several evidence/tool notes rather than clearly before inside-view updates.",
      "actionRequested": "Reorder or relabel the compact step so the persistence/base-rate prior is stated first, followed by the policy and reporting adjustments."
    }
  ],
  "optionalSuggestions": [
    "State explicitly that the 37.15-39.25 interval is an 80% interval to match confidence.",
    "Clarify whether the target table is expected to print raw persons or thousands, while preserving the existing conversion rule for either case."
  ]
}

Emit the final JSON object only.
