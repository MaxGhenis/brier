# Thesis analyst fast public-release run

Return exactly one JSON object and no Markdown. Do not wrap it in a code fence.

# Context access
You may inspect the local repository/workspace when useful. This is optional, not required. Useful read-only context can include docs/cell-contract.md, site/src/data/forecast-cells.ts, site/src/data/ledger-targets.ts, prediction packs, generated comparison data, records/thesis-analyst run manifests, full activity artifacts, prior reasoning traces, and model-candidate files. You may run read-only commands such as rg, sed, cat, find, git log/status/show, `date -u +%Y-%m-%dT%H:%M:%SZ`, and short inline arithmetic commands. Local context is admissible only when it is a public repository artifact, a published Thesis record, or a generated file derived from public official sources. Do not use private meeting notes, call transcripts, email/chat content, pasted attachments, personal notes, or other non-public local files as forecast evidence, source context, or tool-call provenance. If such material is present on disk, ignore it; if a prior run cites it, treat that run as tainted for evidence purposes. Do not modify files. Treat prior forecasts as historical forecasts or strategy context, not as ground-truth outcomes. If prior runs affect your forecast, briefly state the update from the previous run; if they do not matter, ignore them. Existing catalog pointEstimate, ciLow, and ciHigh values are not official evidence for a new forecast; use local catalog context to verify target identity/resolver fields only unless explicitly auditing an existing forecast.

Goal: produce one auditable forecast for an automatically resolvable government/public statistical release. Resolve on the first official print unless the series itself is a policy decision level after an announcement.

# Question spec
- series: ons.trade.total_goods_services_balance
- period: 2026-06
- conditionalOn: null

# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "uk-total-trade-balance-june-2026"
- country: "UK"
- targetUnit: "gbp_billions"
- dataPointId: "ons.trade.total_goods_services_balance.2026_06.first_print"
- expectedReleaseWindow: {"end": "2026-08-13", "start": "2026-08-13"}
- resolutionSourceUrl: "https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbj/mret"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-08-13", "start": "2026-08-13"}, "field": "Value for 2026 JUN", "releasePolicy": "first_print", "sourceSeriesId": "IKBJ", "sourceUrl": "https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbj/mret", "table": "UK trade time series (MRET), Total Trade (TT): WW: Balance: BOP: CP: SA", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-12-7a0ae17b689ac183bc50f5ad2c6a2a2ea46ab25d580b163d84bd14f6a87b3b41.json"
- targetContentHash: "7a0ae17b689ac183bc50f5ad2c6a2a2ea46ab25d580b163d84bd14f6a87b3b41"
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
{"slug":"uk-total-trade-balance-june-2026","country":"UK","type":"data","title":"UK Total Trade Balance, June 2026","question":"ONS Total Trade (TT): WW: Balance: BOP: CP: SA, June 2026, first print","unit":"gbp_billions","pointEstimate":-3.1,"ciLow":-6.8,"ciHigh":0.6,"confidence":0.8,"resolutionDate":"2026-08-13","resolutionSource":"Office for National Statistics UK trade time series (MRET), series IKBJ","resolutionSourceUrl":"https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbj/mret","resolutionRule":"Resolve to the first official ONS value for 2026 JUN in MRET series IKBJ, Total Trade (TT): WW: Balance: BOP: CP: SA, in £m, multiplied by 0.001 to express gbp_billions. Use the first print published for the June 2026 UK trade time series; do not substitute later revisions or same-day corrections unless the first print is withdrawn before publication as an official value.","dataPointId":"ons.trade.total_goods_services_balance.2026_06.first_print","historicalContext":[{"label":"2026 MAY","value":-1.044},{"label":"2026 APR","value":-7.053},{"label":"2026 MAR","value":-10.467},{"label":"2026 FEB","value":-5.757},{"label":"2026 JAN","value":1.498},{"label":"2025 JUN","value":-4.109}],"drivers":["May 2026 balance improved sharply from April but the 2026 year-to-date run rate remains deficit-heavy","Recent IKBJ monthly balances are volatile, especially around March and April 2026","Goods exports rose in May while goods imports also rose, leaving uncertainty about whether the May improvement persists","Services estimates are partly forecast-based before quarterly benchmark data, adding revision and nowcast risk","Exact resolver is ONS MRET series IKBJ in current-price seasonally adjusted total trade balance"],"sourceContext":["https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbj/mret","https://www.gov.uk/government/statistics/announcements/uk-trade-june-2026-time-series","https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/bulletins/uktrade/latest"],"runAt":"2026-08-12T16:07:02Z","reasoning":[{"kind":"heading","text":"UK June 2026 Total Trade Balance Forecast"},{"kind":"text","text":"Framing and exact resolver: this forecast targets ONS MRET series IKBJ, Total Trade (TT): WW: Balance: BOP: CP: SA, for 2026 JUN, first print. The source page reports units of £m, so the ledger transform is multiply by 0.001 into gbp_billions. Historical anchors below use the same IKBJ current-price seasonally adjusted total trade balance variant."},{"kind":"tool","tool":"official.lookup","call":"Checked the official GOV.UK announcement for UK trade: June 2026 time series release timing.","result":"Release date fetched as 13 August 2026 7:00am confirmed; previous listed time was 13 August 2026 9:30am."},{"kind":"tool","tool":"official.lookup","call":"Fetched exact ONS MRET IKBJ recent monthly observations from the ONS time-series page.","result":"Fetched IKBJ values: 2026 MAY = -1044 £m, 2026 APR = -7053 £m, 2026 MAR = -10467 £m, 2026 FEB = -5757 £m, 2026 JAN = 1498 £m."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent same-month and prior-year IKBJ observations for reference-class context.","result":"Fetched IKBJ values: 2025 JUN = -4109 £m, 2025 MAY = -3280 £m, 2025 APR = -3895 £m, 2024 JUN = -3274 £m, 2024 MAY = -2888 £m."},{"kind":"tool","tool":"official.lookup","call":"Checked the latest ONS UK trade bulletin for current-release movement notes, treating bulletin aggregates as qualitative context where they exclude precious metals while the resolver remains IKBJ.","result":"ONS reported May 2026 goods exports at £35.0bn, goods imports at £54.5bn, goods balance at -£19.5bn, goods exports up £1.5bn, goods imports up £0.5bn, and the three-month total trade deficit excluding precious metals at -£9.1bn."},{"kind":"text","text":"Base rate / reference class: the recent IKBJ monthly balance reference class from June 2024 through May 2026 has mean -2.94 gbp_billions; the latest five 2026 observations average -4.56 gbp_billions, while May alone was much less negative at -1.044 gbp_billions. I give most weight to regression from May toward the recent deficit base rate, with some weight on weak early-2026 momentum."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class model uses 24 monthly IKBJ values from 2024 JUN to 2026 MAY; base mean = -2.94 gbp_billions, latest May = -1.044, 2026 Jan-May mean = -4.56. Point update = 0.45*(-2.94) + 0.30*(-1.044) + 0.25*(-4.56) = -2.78, then rounded a little more negative to -3.1 because March-April 2026 showed unusually large deficits and May's improvement may partly reverse. For this flow series I size dispersion from the values themselves: sigma = 2.89 gbp_billions over the 24-month sample, so 80% half-width is about 1.28*sigma = 1.28*2.89 = 3.70; final bounds are -3.1 +/- 3.7 = [-6.8, 0.6]."},{"kind":"text","text":"Counter-consideration: upside risk is another unusually strong services surplus or precious-metals-related swing that would land above the interval with a surplus greater than 0.6 gbp_billions. Downside risk is a repeat of March-April weakness in total trade or a goods-import jump not matched by exports, which would land outside the interval below -6.8 gbp_billions."},{"kind":"forecast","point":-3.1,"ciLow":-6.8,"ciHigh":0.6}]}

# Reviewer critique
{"summary":"The draft is publication-ready against the rubric, with exact target binding, an explicit prior/update/interval calculation, coherent fields, and no apparent leakage or unit ambiguity.","requiredFixes":[],"optionalSuggestions":["Consider noting that the interval uses level dispersion rather than one-step forecast-error volatility, but the current uncertainty method is explicit enough for publication."]}

Emit the final JSON object only.
