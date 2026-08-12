# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ons.trade.total_goods_services_balance
- period: 2026-06
- conditional: null


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
# Rubric
Check these items and name concrete fixes when needed:
1. Exact resolver, source, first-print rule, and resolution date.
2. Base-rate or persistence prior stated before inside-view updates.
3. Time-series/model prior used or explicitly ruled out.
4. Current evidence justifies material movement from the prior.
5. Interval size comes from realized volatility or explicit uncertainty.
6. A compact Prior/update/interval step names the prior, historical sample, adjustment components, interval method, and implied bounds.
7. Tail scenarios are concrete and tied to the target.
8. Point, interval, final forecast step, and JSON fields are coherent.
9. No leakage, catalog point/interval circularity, subjective resolver, or unit ambiguity.

# Required response
Return JSON only, with this shape:
{
  "summary": "one sentence",
  "requiredFixes": [
    {
      "rubricItem": "resolver|base_rate|model_prior|update|interval|prior_update_interval|tails|coherence|leakage",
      "severity": "warning|blocking",
      "summary": "specific issue",
      "actionRequested": "specific change requested"
    }
  ],
  "optionalSuggestions": ["short suggestions"]
}

# Original forecaster prompt hash material
366e582b73046846f2e4ac92f430422239c70996afd58cd8219b53a591958e3f

# Draft forecast response
{"slug":"uk-total-trade-balance-june-2026","country":"UK","type":"data","title":"UK Total Trade Balance, June 2026","question":"ONS Total Trade (TT): WW: Balance: BOP: CP: SA, June 2026, first print","unit":"gbp_billions","pointEstimate":-3.1,"ciLow":-6.8,"ciHigh":0.6,"confidence":0.8,"resolutionDate":"2026-08-13","resolutionSource":"Office for National Statistics UK trade time series (MRET), series IKBJ","resolutionSourceUrl":"https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbj/mret","resolutionRule":"Resolve to the first official ONS value for 2026 JUN in MRET series IKBJ, Total Trade (TT): WW: Balance: BOP: CP: SA, in £m, multiplied by 0.001 to express gbp_billions. Use the first print published for the June 2026 UK trade time series; do not substitute later revisions or same-day corrections unless the first print is withdrawn before publication as an official value.","dataPointId":"ons.trade.total_goods_services_balance.2026_06.first_print","historicalContext":[{"label":"2026 MAY","value":-1.044},{"label":"2026 APR","value":-7.053},{"label":"2026 MAR","value":-10.467},{"label":"2026 FEB","value":-5.757},{"label":"2026 JAN","value":1.498},{"label":"2025 JUN","value":-4.109}],"drivers":["May 2026 balance improved sharply from April but the 2026 year-to-date run rate remains deficit-heavy","Recent IKBJ monthly balances are volatile, especially around March and April 2026","Goods exports rose in May while goods imports also rose, leaving uncertainty about whether the May improvement persists","Services estimates are partly forecast-based before quarterly benchmark data, adding revision and nowcast risk","Exact resolver is ONS MRET series IKBJ in current-price seasonally adjusted total trade balance"],"sourceContext":["https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbj/mret","https://www.gov.uk/government/statistics/announcements/uk-trade-june-2026-time-series","https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/bulletins/uktrade/latest"],"runAt":"2026-08-12T16:07:02Z","reasoning":[{"kind":"heading","text":"UK June 2026 Total Trade Balance Forecast"},{"kind":"text","text":"Framing and exact resolver: this forecast targets ONS MRET series IKBJ, Total Trade (TT): WW: Balance: BOP: CP: SA, for 2026 JUN, first print. The source page reports units of £m, so the ledger transform is multiply by 0.001 into gbp_billions. Historical anchors below use the same IKBJ current-price seasonally adjusted total trade balance variant."},{"kind":"tool","tool":"official.lookup","call":"Checked the official GOV.UK announcement for UK trade: June 2026 time series release timing.","result":"Release date fetched as 13 August 2026 7:00am confirmed; previous listed time was 13 August 2026 9:30am."},{"kind":"tool","tool":"official.lookup","call":"Fetched exact ONS MRET IKBJ recent monthly observations from the ONS time-series page.","result":"Fetched IKBJ values: 2026 MAY = -1044 £m, 2026 APR = -7053 £m, 2026 MAR = -10467 £m, 2026 FEB = -5757 £m, 2026 JAN = 1498 £m."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent same-month and prior-year IKBJ observations for reference-class context.","result":"Fetched IKBJ values: 2025 JUN = -4109 £m, 2025 MAY = -3280 £m, 2025 APR = -3895 £m, 2024 JUN = -3274 £m, 2024 MAY = -2888 £m."},{"kind":"tool","tool":"official.lookup","call":"Checked the latest ONS UK trade bulletin for current-release movement notes, treating bulletin aggregates as qualitative context where they exclude precious metals while the resolver remains IKBJ.","result":"ONS reported May 2026 goods exports at £35.0bn, goods imports at £54.5bn, goods balance at -£19.5bn, goods exports up £1.5bn, goods imports up £0.5bn, and the three-month total trade deficit excluding precious metals at -£9.1bn."},{"kind":"text","text":"Base rate / reference class: the recent IKBJ monthly balance reference class from June 2024 through May 2026 has mean -2.94 gbp_billions; the latest five 2026 observations average -4.56 gbp_billions, while May alone was much less negative at -1.044 gbp_billions. I give most weight to regression from May toward the recent deficit base rate, with some weight on weak early-2026 momentum."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class model uses 24 monthly IKBJ values from 2024 JUN to 2026 MAY; base mean = -2.94 gbp_billions, latest May = -1.044, 2026 Jan-May mean = -4.56. Point update = 0.45*(-2.94) + 0.30*(-1.044) + 0.25*(-4.56) = -2.78, then rounded a little more negative to -3.1 because March-April 2026 showed unusually large deficits and May's improvement may partly reverse. For this flow series I size dispersion from the values themselves: sigma = 2.89 gbp_billions over the 24-month sample, so 80% half-width is about 1.28*sigma = 1.28*2.89 = 3.70; final bounds are -3.1 +/- 3.7 = [-6.8, 0.6]."},{"kind":"text","text":"Counter-consideration: upside risk is another unusually strong services surplus or precious-metals-related swing that would land above the interval with a surplus greater than 0.6 gbp_billions. Downside risk is a repeat of March-April weakness in total trade or a goods-import jump not matched by exports, which would land outside the interval below -6.8 gbp_billions."},{"kind":"forecast","point":-3.1,"ciLow":-6.8,"ciHigh":0.6}]}
