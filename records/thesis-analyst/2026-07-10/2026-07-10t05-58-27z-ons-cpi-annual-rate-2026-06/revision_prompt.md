# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.cpi.annual_rate
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ons-cpi-annual-rate-june-2026"
- country: "UK"
- targetUnit: "percent"
- dataPointId: "ons.cpi.annual_rate.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/may2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-21", "start": "2026-07-13"}, "field": "official_release:ons:cpi:2026-05:cpi_annual_rate", "releasePolicy": "first_print", "sourceSeriesId": "ons.cpi.annual_rate", "sourceUrl": "https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/may2026", "table": "Consumer price inflation, UK: May 2026", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-4b43796ec16bef4a5646e73b93a73d7b4eadfde3cbf2968f078cfb42a59154f0.json"
- targetContentHash: "4b43796ec16bef4a5646e73b93a73d7b4eadfde3cbf2968f078cfb42a59154f0"
- registeredAtUtc: "2026-07-10T05:58:27Z"

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
{"slug":"ons-cpi-annual-rate-june-2026","country":"UK","type":"data","title":"UK CPI Annual Rate, June 2026","question":"What will the ONS Consumer Prices Index (CPI) all-items 12-month annual rate for the UK be for June 2026, not seasonally adjusted, in the first print?","unit":"percent","pointEstimate":2.9,"ciLow":2.5,"ciHigh":3.3,"confidence":0.8,"resolutionDate":"2026-07-22","resolutionSource":"Office for National Statistics, Consumer price inflation, UK: June 2026","resolutionSourceUrl":"https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/june2026","resolutionRule":"Resolve to the first ONS-published CPI all-items 12-month rate for June 2026 in Table 1 of Consumer price inflation, UK: June 2026, in percent rounded to one decimal place. Use the first print only; ignore later revisions, corrections, or time-series updates unless ONS replaces the first bulletin before the normal publication time. The ledger supplied a May 2026 bulletin URL and a 2026-05 field, which appears inconsistent with the June 2026 dataPointId; this forecast keeps the same target identity but uses the June 2026 first-print bulletin as the substantive resolver.","dataPointId":"ons.cpi.annual_rate.june_2026.first_print","historicalContext":[{"label":"2026 May CPI annual rate","value":2.8},{"label":"2026 April CPI annual rate","value":2.8},{"label":"2026 March CPI annual rate","value":3.3},{"label":"2026 February CPI annual rate","value":3.0},{"label":"2025 June CPI annual rate","value":3.6}],"drivers":["May CPI annual rate held at 2.8% after April's fall","June 2025 base month had CPI index 138.9 and 0.3% monthly inflation","May 2026 CPI index was 142.4, so a normal June monthly rise implies about 2.8% to 3.0% annual inflation","services inflation rose to 3.7% and transport inflation to 6.8%, adding upside pressure","food, household services, and goods inflation were easing, limiting the upside"],"sourceContext":["https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/may2026","https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/april2026","https://www.ons.gov.uk/releasecalendar"],"runAt":"2026-07-10T05:59:22Z","reasoning":[{"kind":"heading","text":"UK CPI June 2026 First-Print Forecast"},{"kind":"text","text":"Framing and exact resolver: target is the ONS Consumer Prices Index all-items 12-month annual rate for June 2026, the non-seasonally-adjusted CPI headline rate shown in Table 1 of the first Consumer price inflation, UK: June 2026 bulletin. The ONS May 2026 bulletin says the next release is 22 July 2026, so I use 2026-07-22 as the verified resolution date. The supplied ledger URL points to May 2026 and the sourceBinding field says 2026-05; that is a concrete ledger inconsistency for a June 2026 target, so I keep slug/dataPointId target identity and note the discrepancy rather than changing the target concept."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Consumer price inflation, UK: May 2026 and read release metadata plus Table 1.","result":"Fetched ONS numbers: release date 17 June 2026; next release 22 July 2026; May 2026 CPI index 142.4; May 2026 CPI 12-month rate 2.8%; May 2026 CPI 1-month rate 0.2%; April 2026 CPI 12-month rate 2.8%."},{"kind":"tool","tool":"official.lookup","call":"Read ONS May 2026 Table 1 recent CPI annual-rate history for the same CPI variant.","result":"Fetched same-variant CPI annual rates: May 2025 3.4%, Jun 2025 3.6%, Jul 2025 3.8%, Aug 2025 3.8%, Sep 2025 3.8%, Oct 2025 3.6%, Nov 2025 3.2%, Dec 2025 3.4%, Jan 2026 3.0%, Feb 2026 3.0%, Mar 2026 3.3%, Apr 2026 2.8%, May 2026 2.8%."},{"kind":"tool","tool":"official.lookup","call":"Read ONS May 2026 CPI component table and commentary for current-release pressure points.","result":"Fetched ONS component numbers: May 2026 CPI services annual rate 3.7%, CPI goods annual rate 2.0%, core CPI 2.6%, transport 6.8%, food and non-alcoholic beverages 2.2%, motor fuels 24.6%, petrol 157.4 pence per litre."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Consumer price inflation, UK: April 2026 to cross-check prior month dynamics and base effects.","result":"Fetched ONS April numbers: April 2026 CPI annual rate 2.8%, March 2026 CPI annual rate 3.3%, April 2026 CPI monthly rate 0.7%, April 2025 CPI monthly rate 1.2%, April 2026 CPI index 142.1, June 2025 CPI index 138.9."},{"kind":"text","text":"Base rate/reference class: for one-month-ahead forecasts of this exact ONS CPI annual-rate series, the strongest base rate is persistence plus recent monthly changes. The latest three headline CPI annual rates were 3.3%, 2.8%, and 2.8%, averaging 2.97% if using March-May but 2.87% if downweighting March's pre-April energy-price-cap step. Since the June 2025 base month already had a 0.3% monthly CPI rise, June 2026 needs a monthly rise materially above 0.3% to push the annual rate above 2.9%."},{"kind":"math","text":"Prior/update/interval: persistence prior is 2.8% from the latest ONS first-print headline, with a reference class of 12 successive monthly changes in the same CPI annual-rate series from May 2025 to May 2026: +0.2, +0.2, 0.0, 0.0, -0.2, -0.4, +0.2, -0.4, 0.0, +0.3, -0.5, 0.0 percentage points. The sample standard deviation of those changes is sigma = 0.27, so an 80% normal half-width is roughly 1.28*sigma = 0.35 percentage points. Level/index arithmetic: May 2026 CPI index 142.4 divided by June 2025 CPI index 138.9 gives 2.52% before June's monthly change; adding a plausible +0.3% to +0.4% June monthly move implies about 2.8% to 2.9%. I add +0.1 point for services/transport pressure and Middle East fuel pass-through, giving a 2.9% point estimate; I round the interval outward to 2.5% to 3.3% for one-decimal first-print risk."},{"kind":"text","text":"Current-release adjustment: the level effect from April's energy-price-cap fall has already entered the annual rate, while May's headline was unchanged at 2.8%. Transport and services are the main upside mechanism, but goods, food, and household-services easing keep the central forecast below 3.0% unless June air fares, fuel, or package holidays are unusually strong."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed fuel and air-fare jump after the Middle East shock, which would land above the interval if June monthly CPI exceeded about 0.75%. Downside risk is another broad goods and food disinflation month plus falling domestic energy/fuel prices, which would land below the interval if the June monthly CPI index fell or rose by less than about -0.05% after rounding. Outside the interval would most likely require a large transport-energy surprise or an unusually broad retail discounting month."},{"kind":"forecast","point":2.9,"ciLow":2.5,"ciHigh":3.3}]}

# Reviewer critique
{"summary":"Draft is mostly publication-ready methodologically, but its resolver fields intentionally diverge from the supplied ledger contract and should be reconciled before publication.","requiredFixes":[{"rubricItem":"resolver","severity":"blocking","summary":"The JSON fields use June 2026 bulletin URL/text and 2026-07-22 resolutionDate, while the canonical ledger contract supplied May 2026 URL/sourceBinding and an expected window ending 2026-07-21.","actionRequested":"Either update the canonical ledger target before publication or keep the JSON resolver fields exactly tied to the ledger contract and state the May/June discrepancy only in reasoning; do not publish with unresolved contract-field divergence."},{"rubricItem":"coherence","severity":"warning","summary":"The downside tail says below-interval risk occurs if June monthly CPI 'fell or rose by less than about -0.05%', which is internally awkward because a rise cannot be less than a negative threshold.","actionRequested":"Rephrase the downside trigger to a monthly CPI change below about -0.05%, or a fall/near-flat print below that threshold."}],"optionalSuggestions":["In the compact Prior/update/interval step, separate the +0.1pp services/transport adjustment from the Middle East fuel-pass-through assumption so readers can see whether it is one combined adjustment or two effects.","Consider naming whether the 80% interval is intended to be symmetric before rounding or deliberately widened for one-decimal first-print risk."]}

Emit the final JSON object only.
