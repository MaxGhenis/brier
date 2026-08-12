# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.ppi.output_manufactured_products_index
- period: 2026-07
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "uk-ppi-output-manufactured-products-index-july-2026"
- country: "UK"
- targetUnit: "index_points"
- dataPointId: "ons.ppi.output_manufactured_products_index.2026_07.first_print"
- expectedReleaseWindow: {"end": "2026-08-19", "start": "2026-08-19"}
- resolutionSourceUrl: "https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/gd6y/ppi"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-08-19", "start": "2026-08-19"}, "field": "Value for 2026 JUL", "releasePolicy": "first_print", "sourceSeriesId": "GD6Y", "sourceUrl": "https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/gd6y/ppi", "table": "Producer price inflation time series (PPI), PPI INDEX OUTPUT TOTAL - C Manufactured products, excluding Duty 2015=100", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-12-59fe84d9767a7e8726e3fd651f20fb8df77596f93a26306d99f1bb5327e40946.json"
- targetContentHash: "59fe84d9767a7e8726e3fd651f20fb8df77596f93a26306d99f1bb5327e40946"
- registrationCommit: "1063640b5acfa3c9e2e601737b5395a1431ec540"
- registeredAtUtc: "2026-08-12T16:02:57Z"

# Source hints
- Use ONS time-series pages, ONS API, and ONS release calendar.
- UK CPI/CPIH prints to one decimal; labour-market rates print to one decimal.
- Resolution source should be the relevant ONS release or time-series page.

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
  "unit": "the registered targetUnit, byte-for-byte",
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

Emit the final JSON object only. (agent thesis.analyst v2.5.9, prompt a954cfd8c691, tools 024388e49298, promptMode fast)


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
{"slug":"uk-ppi-output-manufactured-products-index-july-2026","country":"UK","type":"data","title":"UK PPI Output Manufactured Products Index, July 2026","question":"What will the ONS first-print value be for GD6Y, PPI INDEX OUTPUT TOTAL - C Manufactured products, excluding Duty 2015=100, for 2026 JUL?","unit":"index_points","pointEstimate":154.0,"ciLow":152.9,"ciHigh":155.1,"confidence":0.8,"resolutionDate":"2026-08-19","resolutionSource":"Office for National Statistics Producer price inflation time series, series GD6Y","resolutionSourceUrl":"https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/gd6y/ppi","resolutionRule":"Resolve to the first ONS-published value for 2026 JUL in time series GD6Y, PPI INDEX OUTPUT TOTAL - C Manufactured products, excluding Duty 2015=100, on the 19 August 2026 Producer price inflation UK July 2026 time series release. Use the one-decimal index value exactly as first printed by ONS; ignore later revisions, superseded files, and corrections unless ONS replaces the first print before the first public release is complete on that release day.","dataPointId":"ons.ppi.output_manufactured_products_index.2026_07.first_print","historicalContext":[{"label":"2026 JUN","value":153.4},{"label":"2026 MAY","value":152.6},{"label":"2026 APR","value":152.2},{"label":"2026 MAR","value":149.5},{"label":"2025 JUL","value":144.3}],"drivers":["Recent GD6Y level momentum remained positive through June 2026","June bulletin said headline output PPI annual inflation eased to 3.5% and monthly output prices were flat","Refined petroleum output prices fell in June, limiting near-term upside from the spring spike","July seasonal changes in GD6Y since 2016 average about +0.65 index points"],"sourceContext":["https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/gd6y/ppi","https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/producerpriceindexstatisticalbulletindataset/current","https://www.ons.gov.uk/releasecalendar?highlight=true&keywords=inflation&limit=10&page=1&release-type=type-upcoming&sort=date-newest","https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/producerpriceinflation/june2026includingservicesapriltojune2026"],"runAt":"2026-08-12T16:05:27Z","reasoning":[{"kind":"heading","text":"UK GD6Y July 2026 first-print forecast"},{"kind":"text","text":"Framing and exact resolver: this forecast targets ONS series GD6Y, PPI INDEX OUTPUT TOTAL - C Manufactured products, excluding Duty 2015=100, for 2026 JUL, in index_points. The resolving variant is the ONS first-print monthly time-series value from the Producer price inflation UK July 2026 time series release; all anchors below use the same GD6Y manufactured-products excluding-duty index variant."},{"kind":"tool","tool":"official.lookup","call":"Checked the ONS release calendar for Producer price inflation, UK: July 2026 and its connected time-series release.","result":"The ONS release calendar lists Producer price inflation, UK: July 2026 time series for 19 August 2026 at 7:00am, confirmed; the same calendar page also lists Producer price inflation, UK: July 2026 for 19 August 2026 at 7:00am."},{"kind":"tool","tool":"official.lookup","call":"Fetched ONS GD6Y monthly values from the official time-series page.","result":"GD6Y values fetched from ONS: 2026 MAR 149.5, 2026 APR 152.2, 2026 MAY 152.6, 2026 JUN 153.4; 2026 Q2 is 152.7 and 2025 JUL is 144.3."},{"kind":"tool","tool":"official.lookup","call":"Fetched ONS PPI dataset page metadata for the current published vintage.","result":"The ONS Producer price inflation time series dataset current page has Release date 22 July 2026 and Next release 19 August 2026; the latest dataset file is the July 2026 vintage, and the previous version was superseded 22 July 2026 07:00."},{"kind":"tool","tool":"official.lookup","call":"Fetched the June 2026 ONS Producer price inflation bulletin for current-release context.","result":"ONS reported producer output factory gate prices rose 3.5% in the year to June 2026, down from 3.7% in May, and monthly output prices were flat in June; input prices rose 7.3% annually and fell 2.0% monthly; coke and refined petroleum output prices rose 43.0% annually but fell 5.9% monthly in June."},{"kind":"text","text":"Reference class/base rate: for this level index, I used recent month-to-month GD6Y changes as the base rate, with the last 29 monthly changes from 2024 JAN to 2026 JUN averaging +0.414 index points and a sample standard deviation of 0.823. July-only changes from 2016 through 2025 averaged about +0.650, with a sample standard deviation about 0.868."},{"kind":"math","text":"Prior/update/interval: persistence prior is June GD6Y 153.4 plus the historical July seasonal mean change of +0.65, tempered slightly because the June bulletin showed output PPI annual inflation easing and petroleum output prices falling; level component 153.4, momentum/seasonal component +0.6, one-off petroleum drag about -0.1 relative to spring momentum, policy-mechanism effect 0.0, giving point 154.0. For the interval, using recent level-series successive changes, sigma = 0.823 index points, so 1.28*sigma = 1.054; rounding to a one-decimal first print gives an 80% interval of 154.0 +/- 1.1 = [152.9, 155.1]."},{"kind":"text","text":"Counter-consideration: upside risk is a renewed July jump in refined petroleum, metals, or other manufactured-output prices after the Middle East-linked volatility noted by ONS, which would land above the interval if GD6Y rises more than 1.7 points from June. Downside risk is a sharper reversal in petroleum and imported input costs feeding into factory-gate prices, which would land outside the interval below 152.9 if GD6Y falls by more than 0.5 points from June."},{"kind":"forecast","point":154.0,"ciLow":152.9,"ciHigh":155.1}]}

# Reviewer critique
{"summary":"The draft is publication-ready; resolver, prior/update logic, interval construction, tails, and JSON fields are coherent with the ledger target.","requiredFixes":[],"optionalSuggestions":["Clarify the metadata phrase “latest dataset file is the July 2026 vintage” to “22 July 2026 vintage containing June 2026 data” to avoid any appearance of target-month leakage.","If space permits, state whether the 2024 JAN to 2026 JUN volatility sample excludes the target month by construction."]}

Emit the final JSON object only.
