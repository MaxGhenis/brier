# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: bls.ces.home_health_care_services.employment
- period: 2026-07
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "home-health-services-employment-july-2026"
- targetUnit: "thousands"

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
{"slug":"home-health-services-employment-july-2026","country":"US","type":"data","title":"US home health employment, July 2026","question":"What will BLS first report for seasonally adjusted all employees in home health care services, CES6562160001, for July 2026?","unit":"thousands","pointEstimate":1888.8,"ciLow":1881.5,"ciHigh":1896.1,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"Official agency release","resolutionSourceUrl":"https://data.bls.gov/timeseries/CES6562160001","resolutionRule":"Resolve to the first-print BLS Current Employment Statistics value for CES6562160001, All employees, home health care services, seasonally adjusted, July 2026, as published with the Employment Situation release on 2026-08-07 at 08:30 ET, in thousands of persons and rounded to one decimal. Ignore later revisions, benchmark revisions, and subsequent data-file updates.","dataPointId":"bls.ces.home_health_care_services.employment.2026-07.first_print","historicalContext":[{"label":"2026-06 latest SA employment","value":1880.8},{"label":"2026-05 SA employment","value":1877.5},{"label":"2026-04 SA employment","value":1868.0},{"label":"2026-03 SA employment","value":1858.5},{"label":"2025-07 SA employment","value":1799.2}],"drivers":["Demographic demand keeps home-health payrolls on an upward trend","Recent three-month gains were strong before a softer June print","July seasonal-adjusted first print has often shown positive growth in this industry","Policy and reimbursement uncertainty could slow hiring but no clear July break is visible in the public series"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm","https://data.bls.gov/timeseries/CES6562160001","https://fred.stlouisfed.org/series/CES6562160001","https://www.bls.gov/web/empsit/cesseriespub.htm"],"runAt":"2026-07-21T01:37:35Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 BLS home health care services employment"},{"kind":"text","text":"Framing and exact resolver: this forecast targets BLS Current Employment Statistics series CES6562160001, all employees in home health care services, seasonally adjusted, measured in thousands of persons. The target is the July 2026 first print, not a later revised CES vintage."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Employment Situation release schedule for the July 2026 reference month.","result":"BLS lists July 2026 Employment Situation for release on Aug. 07, 2026 at 08:30 AM; the same schedule shows June 2026 released Jul. 02, 2026 and August 2026 scheduled Sep. 04, 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS CES published-series listing for the target industry identity.","result":"The CES published-series table lists home health care services as industry 65-621600, NAICS 6216, private, with a published start year of 1985."},{"kind":"tool","tool":"history.lookup","call":"Fetched recent observations for CES6562160001 from the public BLS-sourced FRED mirror to read the latest available CES history before the July release.","result":"CES6562160001 is seasonally adjusted, monthly, thousands of persons; recent values are 2026-06 = 1880.8, 2026-05 = 1877.5, 2026-04 = 1868.0, 2026-03 = 1858.5, 2026-02 = 1848.7."},{"kind":"tool","tool":"history.lookup","call":"Pulled the 2025-07 through 2026-06 reference-class run of monthly levels for current momentum and dispersion.","result":"The last 12 monthly changes ending 2026-06 were +20.4, +7.1, +7.2, +10.0, +5.6, +1.2, +16.7, +1.7, +9.8, +9.5, +9.5, and +3.3 thousand; their mean is 8.5 thousand."},{"kind":"text","text":"Base rate / reference class: home health care services employment has had persistent positive drift in the recent public CES history. The most relevant base rate is the latest 12 observed month-to-month changes in this same seasonally adjusted series, because the target is a one-month-ahead level forecast and the series has a strong trend."},{"kind":"math","text":"Prior/update/interval: persistence prior is latest level 1880.8 plus the recent 12-month average change of 8.5; historical sample is Jul 2025-Jun 2026 monthly changes in CES6562160001; adjustment components are -0.5 thousand for June's softer +3.3 reading versus prior +9.5 gains and +0.0 for no identified one-off July policy shock, giving 1880.8 + 8.0 = 1888.8. Interval method uses realized dispersion of those same successive changes: sigma = 5.67, so 1.28*sigma = 7.26; rounded 80% bounds are 1888.8 - 7.3 = 1881.5 and 1888.8 + 7.3 = 1896.1."},{"kind":"text","text":"Counter-considerations: upside risk is another double-digit July gain like 2025-07's +20.4, which would land above the interval. Downside risk is a hiring pause or reimbursement-driven slowdown near zero change, which would land below the interval. A renewed classification or benchmark-like break outside the interval is possible but not my central case for a first print."},{"kind":"forecast","point":1888.8,"ciLow":1881.5,"ciHigh":1896.1}]}

# Reviewer critique
{"summary":"The draft is publishable: resolver, prior, update, interval math, tails, and JSON fields are coherent with the target contract.","requiredFixes":[],"optionalSuggestions":["Consider naming the BLS CES time-series page as the resolution source rather than the generic phrase \"Official agency release\" if the publication pipeline displays that field directly.","If space allows, add one sentence explaining why the latest 12 monthly changes are preferred over a longer historical sample."]}

Emit the final JSON object only.
