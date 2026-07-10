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
- Size the 80% interval by reading it off your elicited threshold ladder, and SHOW the derivation in the 'Ladder:' math step: state the interpolated values literally as '10th percentile at X', 'median at Y', and '90th percentile at Z'. Ground the rung placement in the fetched reference-class history (state which fetched values anchored the rung span in the Prior/update/interval step). Never default to a round hedged band.
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

Emit the final JSON object only. (agent thesis.analyst v2.2.0, prompt 7ef119647b35, tools e15bf40583f8, promptMode ladder_v2)

# Threshold-ladder elicitation (promptMode ladder_v2)
This run elicits the distribution as binary exceedance questions BEFORE stating any point estimate, then derives the published numbers from the ladder.
- After research, choose 11-15 strictly increasing thresholds t in the target's print units spanning your genuine uncertainty: the first rung's cumulative probability must be <= 0.10 and the last >= 0.90.
- For each rung independently answer the binary question 'What is the probability the first print is <= t?', as if pricing a binary market. Probabilities must be non-decreasing across rungs and within [0.01, 0.99].
- Add one math reasoning step that begins 'Ladder:' and lists every rung literally as 'P(X <= t) = p' pairs, then states the interpolated '10th percentile at X', 'median at Y', and '90th percentile at Z' in the same step.
- Derive the published numbers FROM the ladder by linear interpolation between rungs: pointEstimate at cumulative 0.50, ciLow at 0.10, ciHigh at 0.90, each rounded to the print precision. The cell fields and the final forecast step must equal these derived values exactly.
- Keep every other requirement above (base rate, upside/downside/outside-the-interval risks, Prior/update/interval step).
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
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC total participants, May 2026","question":"USDA FNS national WIC Total Participants for May 2026, calendar-month reporting, first official print","unit":"millions","pointEstimate":6.84,"ciLow":6.75,"ciHigh":6.95,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Convert the displayed whole-person count to millions by dividing by 1,000,000 and round to 0.001 million. Use the first posted value only; ignore later preliminary, final, and annual-summary revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"November 2024 total participants","value":6.829},{"label":"October 2025 preliminary total participants","value":6.909},{"label":"November 2025 initial total participants","value":6.752}],"drivers":["recent national participation level","month-to-month administrative reporting volatility","WIC eligibility and enrollment conditions","first-print reporting noise"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://www.fns.usda.gov/sites/default/files/resource-files/27wilatest-2.pdf"],"runAt":"2026-07-10T22:05:33Z","thresholdLadder":{"thresholds":[6.7,6.72,6.75,6.78,6.8,6.82,6.84,6.86,6.89,6.92,6.95,6.98,7.02],"cumulativeProbabilities":[0.02,0.04,0.1,0.18,0.28,0.39,0.5,0.61,0.72,0.82,0.9,0.95,0.98]},"reasoning":[{"kind":"heading","text":"USDA FNS WIC total participation: May 2026 first print"},{"kind":"text","text":"The resolver is the national WIC Total Participants series, calendar-month May 2026, using the first official print only. The FNS WIC Data Tables page is the series table page; the published count is converted from persons to millions."},{"kind":"tool","tool":"official.release_calendar","call":"Checked the official FNS release-calendar entry for the May 2026 WIC monthly-program-data posting.","result":"The official schedule lists the May 2026 WIC posting for 2026-08-14, within the stated 2026-08-07 to 2026-08-15 release window."},{"kind":"tool","tool":"official.lookup","call":"Fetched the FNS WIC Latest Month Participation table and read the national TOTAL row.","result":"The FNS table reports TOTAL participation of 6,829,321 in November 2024, 6,909,050 for October 2025 preliminary, and 6,752,138 for November 2025 initial."},{"kind":"tool","tool":"official.compare","call":"Fetched the national-row comparison columns in the FNS WIC Latest Month Participation table.","result":"The table reports November 2025 initial participation of 6,752,138, a -2.3% change from October 2025's 6,909,050 and a -1.1% change from November 2024's 6,829,321."},{"kind":"tool","tool":"official.table_metadata","call":"Fetched the FNS WIC Data Tables page to identify the published monthly national and latest-month table classes.","result":"FNS lists Monthly Data - National Level for FY 2022 through November 2025 and identifies the latest state-level month as November 2025; the associated latest-month total is 6,752,138 participants."},{"kind":"text","text":"Base rate/reference class: recent official national totals span 6.752 to 6.909 million, with the 6.829 million November 2024 reading providing a level anchor. These are the same total-participants variant as the resolver, not annual WIC quality-control data or a smoothed series."},{"kind":"text","text":"Prior/update/interval: I use a persistence prior centered near the recent 6.83 million reference-class level, anchored by fetched November 2024 6.829, October 2025 6.909, and November 2025 initial 6.752 million. I adjust modestly upward from the depressed initial November print for ordinary seasonal/enrollment recovery, retain reporting-volatility uncertainty, and use the elicited threshold ladder rather than a parametric interval; its rung span is anchored in those fetched values."},{"kind":"math","text":"Ladder: P(X <= 6.70) = 0.02; P(X <= 6.72) = 0.04; P(X <= 6.75) = 0.10; P(X <= 6.78) = 0.18; P(X <= 6.80) = 0.28; P(X <= 6.82) = 0.39; P(X <= 6.84) = 0.50; P(X <= 6.86) = 0.61; P(X <= 6.89) = 0.72; P(X <= 6.92) = 0.82; P(X <= 6.95) = 0.90; P(X <= 6.98) = 0.95; P(X <= 7.02) = 0.98. Linear interpolation gives 10th percentile at 6.75, median at 6.84, and 90th percentile at 6.95 million."},{"kind":"text","text":"Upside risk: stronger enrollment or a rebound after the low November initial print could lift May above 6.95 million. Downside risk: continued enrollment attrition or unusually low state reporting could push it below 6.75 million. A broad administrative disruption or an unusually large reporting discontinuity would land outside the interval."},{"kind":"forecast","point":6.84,"ciLow":6.75,"ciHigh":6.95}]}

# Reviewer critique
{"summary":"The forecast is structurally coherent and uses the correct target, but its May-specific upward adjustment and interval justification need stronger, explicitly evidenced support.","requiredFixes":[{"rubricItem":"update","severity":"warning","summary":"The move from the 6.752 million November 2025 initial print to a 6.840 million May 2026 forecast is attributed to “ordinary seasonal/enrollment recovery” without any cited May-seasonality history or current enrollment evidence.","actionRequested":"Either add official same-month or month-to-month historical evidence supporting the recovery adjustment, or describe the estimate as a persistence-based judgment and reduce/remove the unsupported seasonal component."},{"rubricItem":"interval","severity":"warning","summary":"The 80% interval is obtained from the elicited ladder, but the rationale only says its span is “anchored” in three observations and does not quantify realized first-print or month-to-month variation.","actionRequested":"State a concrete uncertainty basis for the ladder width, such as a defined historical sample and observed dispersion/range, or explicitly explain how administrative first-print uncertainty determined the 6.75–6.95 bounds."},{"rubricItem":"resolver","severity":"warning","summary":"The resolution rule is nearly aligned but omits the canonical fallback to the latest-month table that first includes May 2026 and the explicit 0.001-million rounding instruction.","actionRequested":"Use the ledger resolver text verbatim or add the latest-month-table fallback and round-to-0.001-million requirement."}],"optionalSuggestions":["Explicitly label the persistence prior as the time-series model choice, rather than leaving that inference implicit.","Add a direct official URL or document identifier for the release-calendar evidence."]}

Emit the final JSON object only.
