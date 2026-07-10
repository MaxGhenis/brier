# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: fns.wic.total_participation
- period: 2026-05
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "wic-participation-may-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "fns.wic.total_participation.2026-05.first_print"
- resolutionDate: "2026-08-14"
- resolutionSource: "Official agency release"
- resolutionSourceUrl: "https://www.fns.usda.gov/pd/wic-program"
- resolutionRule: "Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. The expected displayed FNS monthly table value is a whole participant count, as in 6,894,610 for May 2025; convert that displayed person count to millions by dividing by 1,000,000 and round to 0.001 million for the cell. If the ledger adapter instead extracts an intermediate value expressed in thousands of participants, its listed factor 0.001 produces the same final unit of millions. Use the first posted May 2026 value only; ignore later preliminary/final revisions or annual-summary revisions."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-08-15", "start": "2026-08-07"}, "field": "fns.wic.total_participation", "releasePolicy": "first_print", "sourceSeriesId": "fns.wic.total_participation", "sourceUrl": "https://www.fns.usda.gov/pd/wic-program", "table": "Official agency release", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-d9f0f26436f4322b04c9deeec1745f166dd46dbeec72d9ec676b1e2cf86ae6a9.json"
- targetContentHash: "d9f0f26436f4322b04c9deeec1745f166dd46dbeec72d9ec676b1e2cf86ae6a9"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"

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

# Threshold-ladder elicitation (promptMode ladder)
This run elicits the distribution as binary exceedance questions BEFORE stating any point estimate, then derives the published numbers from the ladder.
- After research, choose 11-15 strictly increasing thresholds t in the target's print units spanning your genuine uncertainty: the first rung's cumulative probability must be <= 0.10 and the last >= 0.90.
- For each rung independently answer the binary question 'What is the probability the first print is <= t?', as if pricing a binary market. Probabilities must be non-decreasing across rungs and within [0.01, 0.99].
- Add one math reasoning step that begins 'Ladder:' and lists every rung literally as 'P(X <= t) = p' pairs.
- Derive the published numbers FROM the ladder by linear interpolation between rungs: pointEstimate at cumulative 0.50, ciLow at 0.10, ciHigh at 0.90, each rounded to the print precision. The cell fields and the final forecast step must equal these derived values exactly.
- Keep every fast-mode requirement above (sigma arithmetic, base rate, upside/downside/outside-the-interval risks). In the Prior/update/interval step, also state how the ladder-implied 80% width compares to the 1.28*sigma width.
- Add this top-level field to the cell JSON, with your actual rungs as two equal-length numeric arrays:
{
  "thresholdLadder": {
    "thresholds": [
      "strictly increasing numeric rungs"
    ],
    "cumulativeProbabilities": [
      "non-decreasing, within [0.01, 0.99]"
    ]
  }
}


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
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC participation, May 2026","question":"What will USDA FNS first report as national WIC Total Participants for May 2026?","unit":"millions","pointEstimate":6.86,"ciLow":6.76,"ciHigh":6.94,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Convert the displayed whole-person count to millions by dividing by 1,000,000 and round to 0.001 million. Use only the first posted value; ignore later preliminary, final, or annual-summary revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"May 2024 official monthly table","value":6.76371},{"label":"May 2025 first print","value":6.89461},{"label":"October 2025 preliminary","value":6.90905},{"label":"November 2025 initial","value":6.752138}],"drivers":["Recent participation level near 6.8–6.9 million","Positive May-over-May momentum through 2025","Late-2025 participation weakness","Normal monthly reporting volatility","FY 2026 benefit levels broadly supportive"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://www.fns.usda.gov/sites/default/files/data-files/Keydata-May-2025.pdf","https://www.fns.usda.gov/sites/default/files/resource-files/27wilatest-2.pdf","https://www.fns.usda.gov/pd/overview"],"runAt":"2026-07-10T17:15:21Z","thresholdLadder":{"thresholds":[6.7,6.73,6.76,6.79,6.82,6.84,6.86,6.88,6.9,6.92,6.94,6.97,7],"cumulativeProbabilities":[0.03,0.06,0.1,0.16,0.25,0.38,0.5,0.62,0.73,0.82,0.9,0.96,0.98]},"reasoning":[{"kind":"heading","text":"May 2026 national WIC participation first print"},{"kind":"text","text":"The target is USDA FNS Table 21 national WIC Total Participation for May 2026, measured as people issued benefits during the calendar month. This forecast uses the first posted monthly value, converted from people to millions; subsequent revisions are excluded."},{"kind":"tool","tool":"official.lookup","call":"Fetch USDA FNS May 2025 Keydata Table 21 national WIC participation history.","result":"The official table reported 6,763,710 participants in May 2024, 6,876,342 in April 2025, and 6,889,500 in the later May 2025 table vintage; the target's documented May 2025 first print was 6,894,610."},{"kind":"tool","tool":"official.lookup","call":"Fetch the USDA FNS latest-month WIC participation table for late-2025 momentum.","result":"The latest-month table showed 6,909,050 participants for October 2025 preliminary and 6,752,138 for November 2025 initial, a one-month decline of 156,912."},{"kind":"tool","tool":"official.lookup","call":"Verify the release date against the official FNS program-data release schedule and inspect the WIC series page.","result":"The FNS schedule identifies 2026-08-14 for the May 2026 program-data release; the WIC page identifies Table 21 monthly national participation and displayed 2022–2025 monthly data as of its 2026 update."},{"kind":"text","text":"The outside-view reference class is successive monthly changes in the official Table 21 national total from October 2023 through May 2025. Its base rate is small month-to-month movement around a slowly changing level, with May 2025 about 0.131 million above May 2024 but November 2025 initial about 0.142 million below October preliminary."},{"kind":"text","text":"Level and momentum are separated as follows: the level anchor is roughly 6.85 million; the earlier year-over-year rise contributes a modest positive adjustment, while late-2025 weakness contributes a negative adjustment. No discrete May 2026 eligibility or benefit-policy shock is evident; FY 2026 cash-value benefit adjustments are treated as broadly supportive rather than a large caseload mechanism."},{"kind":"math","text":"Prior/update/interval: A persistence/local-level prior centered near 6.85 million uses the 19 successive changes from the fetched October 2023–May 2025 Table 21 history. Their realized standard deviation is approximately sigma = 0.047 million, so a normal 80% half-width is 1.28*sigma = 1.28*0.047 = 0.060 million. The update combines +0.025 million for the earlier year-over-year rise, -0.015 million for late-2025 weakness, and no large policy shock, giving a central value near 6.86 million. The ladder implies bounds of 6.760–6.940, a 0.090-million average half-width, 1.50 times the sigma half-width; this widening reflects first-print state-reporting noise and uncertainty about whether the November weakness persists."},{"kind":"math","text":"Ladder: P(X <= 6.700) = 0.03; P(X <= 6.730) = 0.06; P(X <= 6.760) = 0.10; P(X <= 6.790) = 0.16; P(X <= 6.820) = 0.25; P(X <= 6.840) = 0.38; P(X <= 6.860) = 0.50; P(X <= 6.880) = 0.62; P(X <= 6.900) = 0.73; P(X <= 6.920) = 0.82; P(X <= 6.940) = 0.90; P(X <= 6.970) = 0.96; P(X <= 7.000) = 0.98. Linear interpolation gives the median 6.860, 10th percentile 6.760, and 90th percentile 6.940 million."},{"kind":"text","text":"Upside risk comes from renewed outreach, retention, or normalization after the weak November initial print and could put participation above 6.940 million. Downside risk comes from continued caseload attrition or incomplete first-print state reporting and could put it below 6.760 million. A major reporting disruption or abrupt eligibility-policy effect would land outside the interval."},{"kind":"forecast","point":6.86,"ciLow":6.76,"ciHigh":6.94}]}

# Reviewer critique
{"summary":"The draft is publication-ready: it matches the target contract and provides a coherent persistence prior, evidence-weighted update, volatility-based 80% interval, and concrete tails.","requiredFixes":[],"optionalSuggestions":["Note the ledger adapter’s 0.001 factor applies only if extraction is in thousands; the draft’s whole-person division by 1,000,000 is correct.","Consider citing the exact historical observations used to calculate the stated 19-change standard deviation for reproducibility."]}

Emit the final JSON object only.
