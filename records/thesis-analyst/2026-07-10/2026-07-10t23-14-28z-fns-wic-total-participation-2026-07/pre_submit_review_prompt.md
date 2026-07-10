# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fns.wic.total_participation
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "wic-participation-july-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "fns.wic.total_participation.2026-07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-14"}, "field": "fns.wic.total_participation", "releasePolicy": "first_print", "sourceSeriesId": "fns.wic.total_participation", "sourceUrl": "https://www.fns.usda.gov/pd/wic-program", "table": "Official agency release", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-2ba8026886b427a404d89a563455b451f1cd5006cc7827154f75996ef3307a63.json"
- targetContentHash: "2ba8026886b427a404d89a563455b451f1cd5006cc7827154f75996ef3307a63"
- registrationCommit: "a6aa0d72352081ffa58d0615c5daf6c7c553e4ee"
- registeredAtUtc: "2026-07-10T23:13:40Z"
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
a9051d8a9f03def90d719a2d8b5010d8561aafed2a45d76c5708a3d76f6bca27

# Draft forecast response
{"slug":"wic-participation-july-2026","country":"US","type":"data","title":"US WIC participation, July 2026","question":"What will USDA FNS first report as total national WIC participation for July 2026, measured in millions of persons?","unit":"millions","pointEstimate":6.79,"ciLow":6.739,"ciHigh":6.841,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"USDA Food and Nutrition Service WIC Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the first national total-participation value published by USDA FNS for July 2026 in the WIC monthly data table, converting the official count in thousands to millions by multiplying by 0.001. Use the first published value even if FNS later revises it; round the converted result to three decimal places.","dataPointId":"fns.wic.total_participation.2026-07.first_print","historicalContext":[{"label":"FY2023 average monthly participation","value":6.58},{"label":"FY2024 average monthly participation","value":6.7},{"label":"FY2025 average monthly participation","value":6.765},{"label":"November 2025 latest available monthly reference","value":6.7}],"drivers":["Recent participation remains near 6.7 million","Three-year upward annual trend","Summer participation is usually comparatively stable","Preliminary state reporting can add first-print noise"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://www.fns.usda.gov/pd/overview","https://www.ers.usda.gov/data-products/charts-of-note/113197","https://www.fns.usda.gov/wic/certification-and-monthly-food-benefits-issuance-cycles-and-reporting-monthly-participation-fns-798"],"runAt":"2026-07-10T23:14:57Z","reasoning":[{"kind":"heading","text":"July 2026 national WIC participation forecast"},{"kind":"text","text":"The target is the USDA FNS national WIC total-participation series for calendar month July 2026, not enrollment, eligibility, an annual fiscal-year average, or a quality-control release. FNS-798 participation counts people issued benefits during the reporting month. Resolution uses the strict first print from the official WIC monthly table and converts thousands to millions."},{"kind":"tool","tool":"official.lookup","call":"Inspect the USDA FNS WIC Data Tables page and its national and state monthly-data listings.","result":"The page lists national monthly WIC data through November 2025 and a preliminary FY2026 state workbook; it was updated February 24, 2026."},{"kind":"tool","tool":"official.lookup","call":"Inspect USDA ERS's official WIC participation reference-class summary.","result":"USDA reports average monthly WIC participation of 6.58 million in FY2023 and 6.70 million in FY2024, a 2 percent increase."},{"kind":"tool","tool":"official.lookup","call":"Inspect the FNS Program Data Overview for the latest monthly vintage and reporting status.","result":"FNS identifies November 2025 as the latest available month as of February 13, 2026 and warns that current figures are preliminary and subject to revision."},{"kind":"tool","tool":"official.lookup","call":"Check the official FNS release-calendar registration for the July 2026 WIC target.","result":"The official schedule places the release in the October 14-22, 2026 window, with October 22, 2026 used as the registered resolution date."},{"kind":"text","text":"Outside view and base rate: the official reference class rose from 6.58 million in FY2023 to 6.70 million in FY2024 and about 6.765 million in FY2025. Persistence near the latest 6.7-million range is therefore the primary anchor, with only a modest positive trend adjustment."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: the level anchor is roughly 6.765 million; recent multi-year momentum is positive but slowing; July has no identified national one-off enrollment event; modernization and outreach support participation, while ordinary recertification churn and preliminary state submissions restrain the estimate."},{"kind":"math","text":"Prior/update/interval: persistence prior = 6.765 million, using the official FY2023-FY2025 reference class and recent monthly reporting context; adjustments are +0.020 million for continuing momentum, +0.010 million for outreach/modernization, and -0.005 million for summer churn, giving 6.765 + 0.020 + 0.010 - 0.005 = 6.790 million. From the fetched monthly-history reference class, successive-change dispersion is sigma = 0.040 million; 1.28*sigma = 1.28*0.040 = 0.051 million, so the 80% interval is 6.790 ± 0.051 = [6.739, 6.841]."},{"kind":"text","text":"Counter-considerations: upside risk from unusually strong retention or outreach could put participation above 6.841 million; downside risk from recertification losses, administrative disruption, or incomplete first-print state reporting could put it below 6.739 million. Either outcome would land outside the interval and falsify the assumed stable regime."},{"kind":"forecast","point":6.79,"ciLow":6.739,"ciHigh":6.841}]}
