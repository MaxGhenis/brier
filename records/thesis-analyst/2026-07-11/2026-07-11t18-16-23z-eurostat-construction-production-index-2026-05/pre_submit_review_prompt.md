# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: eurostat.construction.production_index
- period: 2026-05
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "euro-area-construction-production-index-may-2026"
- country: "EA"
- targetUnit: "index_points"
- dataPointId: "eurostat.construction.production_index.2026_05.first_print"
- resolutionSourceUrl: "https://ec.europa.eu/eurostat/databrowser/view/sts_copr_m/default/table?lang=en"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["ec.europa.eu"], "expectedReleaseWindow": {"end": "2026-07-20", "start": "2026-07-20"}, "field": "freq=M, unit=I21, s_adj=SCA, indic_bt=PRD, nace_r2=F, geo=EA20", "releasePolicy": "first_print", "sourceSeriesId": "sts_copr_m.M.I21.SCA.PRD.F.EA20", "sourceUrl": "https://ec.europa.eu/eurostat/databrowser/view/sts_copr_m/default/table?lang=en", "table": "sts_copr_m: Production in construction - monthly data", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-11-88e510f907520fe3734008853e5f0f83c6b6296c6f9c0dd7d76a6a9c8f0bee49.json"
- targetContentHash: "88e510f907520fe3734008853e5f0f83c6b6296c6f9c0dd7d76a6a9c8f0bee49"
- registrationCommit: "357f4e8477327d91775a345ece531f3eb42fa3b7"
- registeredAtUtc: "2026-07-11T18:10:24Z"
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
5975c9f1db1035f0b547fc885e48d40a37d9f14d692954c9b43698e3e6bad865

# Draft forecast response
{"slug":"euro-area-construction-production-index-may-2026","country":"EA","type":"data","title":"Euro-area construction production, May 2026","question":"What will Eurostat first report for the May 2026 euro-area production-in-construction index, calendar and seasonally adjusted, 2021=100, series sts_copr_m.M.I21.SCA.PRD.F.EA20?","unit":"index_points","pointEstimate":105.7,"ciLow":104.4,"ciHigh":107.1,"confidence":0.8,"resolutionDate":"2026-07-20","resolutionSource":"Eurostat Production in construction release and sts_copr_m data table","resolutionSourceUrl":"https://ec.europa.eu/eurostat/databrowser/view/sts_copr_m/default/table?lang=en","resolutionRule":"Resolve to the first value Eurostat publishes on 20 July 2026 for May 2026 in sts_copr_m, series freq=M, unit=I21, s_adj=SCA, indic_bt=PRD, nace_r2=F, geo=EA20. Use the calendar-and-seasonally-adjusted production-in-construction index, 2021=100, as printed to one decimal. Do not substitute monthly growth, calendar-adjusted data, EU data, or a later revision. The ledger unit is index_points, although that value is absent from the prompt's enumerated unit examples.","dataPointId":"eurostat.construction.production_index.2026_05.first_print","historicalContext":[{"label":"November 2025","value":104.3},{"label":"December 2025","value":104.6},{"label":"January 2026","value":103.6},{"label":"February 2026","value":103.1},{"label":"March 2026","value":104.9},{"label":"April 2026","value":105.5}],"drivers":["April level of 105.5 index points","six-month mean monthly change of 0.24 points","March-April rebound after January-February weakness","weak buildings but stronger civil engineering and specialised construction"],"sourceContext":["https://ec.europa.eu/eurostat/web/products-euro-indicators/w/4-18062026-ap","https://ec.europa.eu/eurostat/web/main/news/euro-indicators/release-calendar","https://ec.europa.eu/eurostat/databrowser/view/sts_copr_m/default/table?lang=en"],"runAt":"2026-07-11T18:16:38Z","reasoning":[{"kind":"heading","text":"Euro-area construction production index for May 2026"},{"kind":"text","text":"The target is Eurostat table sts_copr_m, exact series sts_copr_m.M.I21.SCA.PRD.F.EA20: total construction for EA20, calendar and seasonally adjusted, 2021=100. The resolver is the May 2026 first print, not a growth rate or later revision."},{"kind":"tool","tool":"official.lookup","call":"Read the monthly index table in Eurostat's 18 June 2026 Production in construction release.","result":"Euro-area SCA index values were 104.3 in November 2025, 104.6 in December, 103.6 in January 2026, 103.1 in February, 104.9 in March, and 105.5 in April."},{"kind":"tool","tool":"official.lookup","call":"Read Eurostat's month-on-month total-construction reference class from the same official release.","result":"Euro-area monthly changes from November 2025 through April 2026 were -0.9%, +0.3%, -1.0%, -0.5%, +1.7%, and +0.6%, respectively."},{"kind":"tool","tool":"official.lookup","call":"Read Eurostat's April annual and sector detail to assess the composition of momentum.","result":"April 2026 total construction was 0.9% above April 2025; buildings fell 5.2% year over year, while civil engineering rose 4.4% and specialised construction rose 1.7%."},{"kind":"text","text":"The outside-view base rate is short-run level persistence: the six official index levels fluctuate around 104-105, while the five successive level changes average +0.24 points. Level is therefore anchored at April's 105.5, with only a small positive continuation."},{"kind":"text","text":"Current-release adjustments are approximately net zero beyond the persistence prior: recent momentum is positive, the March-April rebound may partly reverse as a one-off, weak building activity offsets stronger civil engineering and specialised work, and no specific policy mechanism warrants a further adjustment."},{"kind":"text","text":"Eurostat's official release states that the next Production in construction release is 20 July 2026, matching the official Euro-indicators calendar and verifying the ledger resolution date rather than inferring it from monthly cadence."},{"kind":"math","text":"Prior/update/interval: The model is a persistence-plus-mean-change prior using the six November-April official index observations. Successive changes are +0.3, -1.0, -0.5, +1.8, and +0.6 points; their mean is +0.24 and sample sigma = 1.08 points. Starting from 105.5 gives 105.5 + 0.24 = 105.74, rounded to 105.7. The empirical 80% half-width is 1.28*sigma = 1.28*1.08 = 1.38 points, implying 105.74 ± 1.38 = 104.36 to 107.12, rounded to 104.4-107.1."},{"kind":"text","text":"Upside risk comes from another broad rebound like March, which would land above the interval. Downside risk comes from renewed building-sector weakness or reversal of the March-April surge; a monthly fall exceeding roughly 1.1 points would land below the interval. Either outcome would be outside the interval and falsify the central persistence view."},{"kind":"forecast","point":105.7,"ciLow":104.4,"ciHigh":107.1}]}
