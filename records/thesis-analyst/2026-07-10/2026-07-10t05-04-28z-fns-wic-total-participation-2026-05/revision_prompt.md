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
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC participation, May 2026","question":"USDA FNS WIC Program total participants for May 2026, national total, not seasonally adjusted, first official print","unit":"millions","pointEstimate":6.96,"ciLow":6.806,"ciHigh":7.114,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Convert the official person count to millions by dividing by 1,000,000 and round to 0.001 million for the cell. Use the first posted value only; ignore later preliminary/final revisions or annual-summary revisions. The ledger binding says transform factor 0.001, but the fetched FNS monthly PDF displays total participants as person counts such as 6,894,610 for May 2025, so the emitted forecast uses the catalog unit millions from person counts.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"latest Nov 2025 initial","value":6.752138},{"label":"Oct 2025 preliminary","value":6.90905},{"label":"May 2025","value":6.89461},{"label":"May 2024","value":6.76371},{"label":"May 2023","value":6.696739}],"drivers":["Recent FNS first-available total fell sharply in November 2025 versus October 2025","May participation has been above the preceding November in the last three fetched fiscal-year histories","FY2025 annual average participation was higher than FY2024 and FY2023","No core FY2026 WIC eligibility or benefit mechanism points to a May 2026 collapse before the FY2027 budget year"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-2.pdf","https://www.fns.usda.gov/sites/default/files/resource-files/27wilatest-2.pdf","https://www.fns.usda.gov/data-research/data-visualization/program-data-release-dates"],"runAt":"2026-07-10T05:04:47Z","reasoning":[{"kind":"heading","text":"USDA FNS WIC total participation, May 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the USDA FNS WIC national Total Participants series for May 2026, not seasonally adjusted, resolved on the first official print from the WIC monthly program-data tables. The FNS WIC page is the exact series page; the target is a first-print value, so later revisions are excluded."},{"kind":"tool","tool":"official.lookup","call":"Opened USDA FNS WIC Data Tables page and identified the monthly national and latest-month WIC data resources.","result":"The FNS WIC page lists Monthly Data - National Level as FY 2022 through November 2025, links FY 2026 preliminary state-level participation, and shows page updated February 24, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched the FNS WIC monthly national PDF for annual and monthly totals through FY2026-to-date.","result":"The monthly national PDF reports FY2025 annual Total Participants 6,866,095, FY2024 6,704,329, FY2023 6,575,977, May 2023 6,696,739, May 2024 6,763,710, May 2025 6,894,610, Oct 2025 6,909,050, and Nov 2025 6,752,138."},{"kind":"tool","tool":"official.lookup","call":"Fetched the FNS latest-month participation PDF to check the first-available/recent-release format.","result":"The latest-month PDF is dated data as of February 13, 2025 and reports TOTAL participation of 6,829,321 for November 2024, 6,909,050 for October 2025 preliminary, and 6,752,138 for November 2025 initial, a -2.3% monthly change and -1.1% year-over-year change."},{"kind":"tool","tool":"official.lookup","call":"Checked the official FNS program-data release calendar for the May 2026 WIC monthly release date.","result":"The FNS program-data release calendar gives the May 2026 WIC monthly program-data release date as 2026-08-14, within the registered expected release window 2026-08-07 to 2026-08-15."},{"kind":"text","text":"Base rate/reference class: for the same WIC total-participation variant, the three fetched May observations were 6.696739 million in 2023, 6.763710 million in 2024, and 6.894610 million in 2025. The three historical November-to-May moves were +0.300006 million from Nov 2022 to May 2023, +0.139673 million from Nov 2023 to May 2024, and +0.065289 million from Nov 2024 to May 2025."},{"kind":"text","text":"Level and momentum: the clean May-to-May trend points upward, with May 2025 above May 2024 by 0.130900 million and May 2024 above May 2023 by 0.066971 million. The latest initial November 2025 level is unusually low relative to October 2025, so I discount a pure Nov 2025 persistence forecast and treat part of the drop as reporting/timing or temporary churn risk rather than a permanent level shift."},{"kind":"text","text":"Policy and mechanism: WIC participation is driven by categorical eligibility, income eligibility, state administration, births/young-child caseload, and take-up. I do not see a May 2026 core-program policy change in the fetched official tables; proposed FY2027 benefit changes would begin after this May target, so they are not a direct level cut for this observation."},{"kind":"math","text":"Prior/update/interval: persistence prior uses the historical Nov-to-May reference class from fetched FNS monthly totals: changes were 0.300006, 0.139673, and 0.065289 million, average = 0.168323, so Nov 2025 initial 6.752138 + 0.168323 = 6.920461 million. May-trend prior uses May 2025 plus average of the two May-to-May gains: 6.894610 + ((0.066971 + 0.130900)/2) = 6.993546 million. I weight these to 6.960 million after a small caution for the weak Nov 2025 first print. Horizon-matched dispersion from those Nov-to-May changes gives sigma = 0.119953 million; 1.28*sigma = 0.1535 million, rounded to 0.154, so the 80% interval is 6.960 - 0.154 = 6.806 and 6.960 + 0.154 = 7.114 million."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound from the depressed November 2025 initial count plus stronger child caseload growth, which would land above the interval if May first print exceeds 7.114 million. Downside risk is a persistent administrative or funding disruption carrying through spring 2026, or a genuine caseload drop rather than a temporary November print, which would land below the interval if May first print is under 6.806 million. Outside the interval would therefore require either a larger-than-historical spring rebound or a continuation of the November 2025 shock."},{"kind":"forecast","point":6.96,"ciLow":6.806,"ciHigh":7.114}]}

# Reviewer critique
{
  "summary": "Draft is publishable after small clarity fixes on unit conversion and one inconsistent source-date statement; the quantitative prior/update/interval structure is otherwise coherent.",
  "requiredFixes": [
    {
      "rubricItem": "resolver",
      "severity": "warning",
      "summary": "The resolver text says divide person counts by 1,000,000 while also noting the ledger transform factor is 0.001, creating apparent ambiguity about whether the official table value is persons or thousands of persons.",
      "actionRequested": "Clarify that the final resolved unit is millions and specify exactly which displayed FNS table value format is expected for May 2026; keep the ledger discrepancy note but make the operational conversion unambiguous."
    },
    {
      "rubricItem": "update",
      "severity": "warning",
      "summary": "The evidence note says the latest-month PDF is dated February 13, 2025 while reporting October/November 2025 values, which is internally inconsistent.",
      "actionRequested": "Correct or remove the inconsistent date in the cited evidence summary so the public evidence record is credible."
    }
  ],
  "optionalSuggestions": [
    "State explicitly that the three-observation volatility sample is thin and the 80% interval is approximate.",
    "Name the final weighting between the Nov-to-May persistence prior and May-trend prior rather than saying only that they were weighted to 6.960."
  ]
}

Emit the final JSON object only.
