# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: nbb.gdp.flash_qoq
- period: 2026-Q3
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "belgium-gdp-flash-q3-2026"
- country: "BE"
- targetUnit: "percent_growth"
- dataPointId: "nbb.gdp.flash_qoq.2026_q3.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.nbb.be"], "expectedReleaseWindow": {"end": "2026-11-06", "start": "2026-10-23"}, "field": "nbb.gdp.flash_qoq", "releasePolicy": "first_print", "sourceSeriesId": "nbb.gdp.flash_qoq", "sourceUrl": "https://www.nbb.be/en/statistics/nationalregional-accounts", "table": "National Bank of Belgium national accounts flash estimate release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-da431620f539636e89bd1a5a6ed665ca1ceb2b08735ee192fb2f14528c0ad43f.json"
- targetContentHash: "da431620f539636e89bd1a5a6ed665ca1ceb2b08735ee192fb2f14528c0ad43f"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"

# Source hints
- Use the official agency data page and release calendar.
- FRED or sanctioned mirrors may be used only for history, not final resolution.
- Match the agency's published rounding precision.

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
{"slug":"belgium-gdp-flash-q3-2026","country":"BE","type":"data","title":"Belgium GDP Flash Q3 2026","question":"What will the National Bank of Belgium first flash estimate report for Belgium real GDP quarter-on-quarter growth in 2026-Q3, seasonally and calendar adjusted chain-linked volume, percent change from 2026-Q2?","unit":"percent_growth","pointEstimate":0.2,"ciLow":0,"ciHigh":0.4,"confidence":0.8,"resolutionDate":"2026-10-30","resolutionSource":"National Bank of Belgium national accounts flash estimate release","resolutionSourceUrl":"https://www.nbb.be/en/statistics/nationalregional-accounts","resolutionRule":"Resolve to the first National Bank of Belgium flash estimate for 2026-Q3 real GDP quarter-on-quarter growth, seasonally and calendar adjusted chain-linked volume, reported in percentage points and rounded to the agency's published one-decimal precision. Do not use later quarterly-account revisions or same-day corrections unless the first-print release itself is replaced before publication as the official first print.","dataPointId":"nbb.gdp.flash_qoq.2026_q3.first_print","historicalContext":[{"label":"2023-Q4 first-flash qoq","value":0.4},{"label":"2024-Q1 first-flash qoq","value":0.3},{"label":"2024-Q2 first-flash qoq","value":0.2},{"label":"recent-reference-class mean","value":0.25}],"drivers":["Belgian GDP first prints have clustered near 0.2-0.3 percent qoq","Euro area 2026 growth backdrop is soft but positive outside volatile Ireland","Belgium's open economy is exposed to trade and energy-price shocks","Services and labor-market resilience keep recession risk moderate"],"sourceContext":["https://www.nbb.be/en/statistics/nationalregional-accounts","https://www.nbb.be/en/statistics/statistical-release-calendar","https://ec.europa.eu/eurostat/databrowser/view/namq_10_gdp/default/table?lang=en","https://www.imf.org/en/Publications/WEO/weo-database/2026/April"],"runAt":"2026-07-10T05:40:34Z","reasoning":[{"kind":"heading","text":"Belgium 2026-Q3 GDP Flash Forecast"},{"kind":"text","text":"Framing and exact resolver: target is the National Bank of Belgium first flash estimate for Belgium real GDP, seasonally and calendar adjusted chain-linked volume, quarter-on-quarter percent growth for 2026-Q3. The resolver should stay tied to nbb.gdp.flash_qoq.2026_q3.first_print even though the allowed country enum in the generic JSON template does not list BE."},{"kind":"tool","tool":"official.lookup","call":"Checked NBB national/regional accounts release calendar and target binding for the Q3 2026 flash estimate.","result":"NBB calendar/ledger target places the first-print release on 2026-10-30 within the expected 2026-10-23 to 2026-11-06 window; resolver uses 1 first-print flash estimate and one-decimal percent growth."},{"kind":"text","text":"Variant control: anchors use the same variant as the target where available, namely seasonally and calendar adjusted real GDP quarter-on-quarter percentage growth, flash or preliminary first estimate, not annual GDP, NSA GDP, gross-value-added components, or revised final accounts."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent Belgium flash/preliminary GDP quarter-on-quarter reference points from NBB/Eurostat public national-accounts releases and databrowser history.","result":"Fetched qoq percent growth values: 2023-Q4 = 0.4, 2024-Q1 = 0.3, 2024-Q2 = 0.2, 2024-Q3 = 0.3, 2024-Q4 = 0.2, 2025-Q1 = 0.3, 2025-Q2 = 0.1, 2026-Q1 = 0.2."},{"kind":"tool","tool":"official.lookup","call":"Fetched broader macro backdrop from public IMF WEO and Eurostat current-release context for Belgium and the euro area.","result":"IMF April 2026 table gives Belgium real GDP growth of 1.2 for 2026 and 1.2 for 2027; Eurostat/press context showed euro area Q2 2025 qoq growth of 0.1 and Q1 2026 ex-Ireland growth around 0.3."},{"kind":"text","text":"Base rate/reference class: the recent same-variant reference class is a low-volatility Belgium qoq-growth process centered around 0.25 percent, with most first prints between 0.1 and 0.4 rather than recessionary or boom-like quarters."},{"kind":"math","text":"Prior/update/interval: persistence prior is the eight-observation recent flash/preliminary sample [0.4, 0.3, 0.2, 0.3, 0.2, 0.3, 0.1, 0.2], mean = 0.25. For a change/flow series, sigma is computed from the values themselves: sample sigma = 0.093. The Gaussian 80% half-width is 1.28*sigma = 1.28*0.093 = 0.119. I shade the point from 0.25 to 0.20 for softer 2026 euro-area momentum and trade/energy uncertainty; I widen the displayed half-width to about 0.20, which is 1.68 times the mechanical half-width, because Belgium's open economy has a larger tail if external demand or energy prices deteriorate. Rounded to agency precision, this gives 0.0 to 0.4."},{"kind":"text","text":"Current-release adjustment: level effects are neutral to mildly positive because annual Belgium growth around 1.2 implies about 0.3 per quarter, momentum is slightly negative from soft euro-area growth and recent Belgian prints near 0.1-0.2, one-off effects are downside from trade and energy volatility, and policy-mechanism effects are mixed as easier earlier ECB policy supports demand but fiscal consolidation and external shocks restrain it."},{"kind":"text","text":"Counter-consideration: upside risk is a services-led rebound or inventory/export catch-up that would land above the interval near 0.5 or higher; downside risk is a trade/energy shock or industrial contraction that would land below the interval below 0.0; outside the interval requires either a clear external-demand snapback or an outright quarterly contraction signal."},{"kind":"forecast","point":0.2,"ciLow":0,"ciHigh":0.4}]}

# Reviewer critique
{"summary":"Publishable after a small clarification to make the historical prior sample auditable and internally consistent.","requiredFixes":[{"rubricItem":"prior_update_interval","severity":"warning","summary":"The compact prior/update/interval step uses an eight-observation sample, but the top-level historicalContext only lists three dated observations plus a mean, and the sample appears non-contiguous without explanation.","actionRequested":"List the full dated reference-class observations used for the 0.25 prior, or state why omitted quarters were unavailable/excluded, so the mean and volatility calculation are reproducible."}],"optionalSuggestions":["State whether the interval is based on first-print value volatility rather than forecast-error volatility, since the sample is small.","Keep the resolver tied to the ledger date/source as written; it is coherent with the target contract."]}

Emit the final JSON object only.
