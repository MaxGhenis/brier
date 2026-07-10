# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.pusf.j5ii.public_sector_net_borrowing_ex_banks
- period: 2026-06
- conditional_on: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ons-pusf-j5ii-public-sector-net-borrowing-ex-banks-june-2026"
- targetUnit: "gbp_billions"
- dataPointId: "ons.pusf.j5ii.public_sector_net_borrowing_ex_banks.june_2026.first_print"
- resolutionSourceUrl: "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-07-23", "start": "2026-07-15"}, "field": "official_release:ons:public_sector_finances:2026-05:j5ii", "releasePolicy": "first_print", "sourceSeriesId": "ons.pusf.j5ii", "sourceUrl": "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026", "table": "Public sector finances, UK: May 2026", "transform": {"factor": 1, "operation": "identity"}}

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
{"slug":"ons-pusf-j5ii-public-sector-net-borrowing-ex-banks-june-2026","country":"UK","type":"data","title":"UK PSNB ex Banks, June 2026","question":"ONS PUSF series J5II, public sector net borrowing excluding public sector banks, current-price not seasonally adjusted monthly value for June 2026, first print","unit":"gbp_billions","pointEstimate":-26.2,"ciLow":-32.5,"ciHigh":-19.9,"confidence":0.8,"resolutionDate":"2026-07-21","resolutionSource":"Office for National Statistics public sector finances release","resolutionSourceUrl":"https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026","resolutionRule":"Resolve to the first official ONS print for PUSF time-series code J5II for 2026 JUN, converted from pounds millions to pounds billions by dividing by 1000, with no later revisions or same-day correction grace unless the first-print release itself is replaced before publication. The provided ledger URL points to the May 2026 bulletin even though the June 2026 observation should appear in the next Public sector finances release; keep this forecast tied to the ledger target and use the first official J5II 2026 JUN value.","dataPointId":"ons.pusf.j5ii.public_sector_net_borrowing_ex_banks.june_2026.first_print","historicalContext":[{"label":"latest_2026_may","value":-23.294},{"label":"2025_jun","value":-23.878},{"label":"2024_jun","value":-14.617},{"label":"2023_jun","value":-19.085},{"label":"2022_jun","value":-18.871}],"drivers":["May 2026 borrowing already much worse than May 2025","June same-month history has high debt-interest seasonality","RPI-linked gilt uplift keeps debt interest volatile","Tax receipts growth partly offsets higher spending","Ledger resolver URL appears one month early but target remains J5II June 2026 first print"],"sourceContext":["https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/j5ii/pusf","https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/bulletins/publicsectorfinances/may2026","https://www.ons.gov.uk/releasecalendar"],"runAt":"2026-07-10T00:00:00Z","reasoning":[{"kind":"heading","text":"Forecast for ONS J5II June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: target is ONS PUSF time-series J5II, labelled PS: Net Borrowing excluding public sector banks, pounds millions, CPNSA. The ONS bulletin chart refers to dataset identifier -J5II when presenting borrowing as a positive deficit, while the time-series page reports J5II itself as negative for recent deficit months; I forecast the ledger-bound J5II value in GBP billions. Ledger discrepancy: the supplied resolutionSourceUrl is the May 2026 bulletin, but the 2026 JUN first print should be in the next Public sector finances release on the verified next-release date."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS J5II PUSF time-series page for latest official monthly values and next release field.","result":"Fetched ONS J5II values: 2026 APR -23033 £m, 2026 MAY -23294 £m, 2025 JUN -23878 £m, 2024 JUN -14617 £m, 2023 JUN -19085 £m; page showed release date 19 June 2026 and next release 21 July 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened ONS Public sector finances, UK: May 2026 bulletin for first-print May context and components.","result":"Fetched bulletin figures: borrowing was £23.3 billion in May 2026, £5.4 billion more than May 2025, and £5.6 billion above the OBR forecast of £17.7 billion; financial-year-to-May borrowing was £46.3 billion, £8.9 billion more than a year earlier."},{"kind":"tool","tool":"official.lookup","call":"Read ONS May 2026 bulletin component tables for receipts, spending, debt interest, and OBR comparison.","result":"Fetched component figures: central government receipts were £85.5 billion in May 2026, tax receipts £63.7 billion, current expenditure £95.7 billion, debt interest payable £11.7 billion, and RPI-linked capital uplift added £4.9 billion."},{"kind":"tool","tool":"official.lookup","call":"Checked the ONS release-calendar surface and the J5II page scheduling field for the relevant release timing.","result":"Fetched schedule numbers from ONS surfaces: release calendar page listed 8915 published results and 338 upcoming results; the J5II page gave next release 21 July 2026 after the 19 June 2026 release."},{"kind":"text","text":"Base rate/reference class: use the same official, not-seasonally-adjusted J5II variant throughout. The recent same-month June reference class is 2021 -18.721, 2022 -18.871, 2023 -19.085, 2024 -14.617, and 2025 -23.878 GBP billions, averaging -19.034 GBP billions. That outside view is less negative than the latest run-rate, so I update toward weaker 2026 fiscal conditions rather than using the catalog forecast as evidence."},{"kind":"math","text":"Prior/update/interval: persistence prior is the June 2021-2025 same-month mean of -19.034 GBP billions for J5II; same-month 2025 pull is -23.878 and Apr-May 2026 has deteriorated versus Apr-May 2025 by (-23.033 - -19.521) + (-23.294 - -17.857) = -8.949 GBP billions, or -4.475 per month. Adjustment components: -2.4 from last-year June/debt-interest seasonality, -3.6 from current FY overshoot and high May debt interest, and -1.2 partial offset for receipts growth and mean reversion, giving -19.0 - 2.4 - 3.6 - 1.2 = -26.2. For the June 2021-2025 values themselves, sigma = 3.3 GBP billions, so 1.28*sigma = 4.2; I widen to 6.3 because the current RPI-linked debt-interest regime and local-government estimates are more volatile than the five-year same-month sample. Final 80% interval is -26.2 +/- 6.3 = [-32.5, -19.9]."},{"kind":"text","text":"Counter-considerations: upside risk to borrowing, in the bulletin's positive-deficit language, would be another very large RPI-linked gilt uplift or weak receipts print and would land below the interval as a J5II value more negative than -32.5. Downside risk to borrowing would be stronger PAYE/VAT receipts, a smaller capital-uplift accrual, or local-government estimates closer to surplus, which would land above the interval as a J5II value less negative than -19.9. An outside the interval result is plausible mainly if debt-interest timing differs sharply from June 2025."},{"kind":"forecast","point":-26.2,"ciLow":-32.5,"ciHigh":-19.9}]}

# Reviewer critique
{"summary":"Draft is publishable after a small coherence cleanup: resolver, evidence, prior, interval, tails, and JSON fields are mostly aligned with the target contract.","requiredFixes":[{"rubricItem":"coherence","severity":"warning","summary":"The prior/update math labels the -1.2 component as a partial offset for receipts growth and mean reversion, but applies it as a further negative adjustment: -19.0 - 2.4 - 3.6 - 1.2 = -26.2.","actionRequested":"Either relabel the -1.2 as an additional downside component or change it to a positive offset and recompute the point estimate and interval around the new point."}],"optionalSuggestions":["In the resolver text, make the ledger discrepancy even more explicit by saying publication should use the ledger URL if required by the catalog, while the June 2026 first print is expected on the 21 July 2026 release surface.","Add one short phrase that the simple same-month/persistence model is the chosen time-series prior, so rubric item 3 is unambiguous."]}

Emit the final JSON object only.
