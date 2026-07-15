# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: census.m3.defense_capital_goods.inventories
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-defense-capital-goods-inventories-june-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "census.m3.defense_capital_goods.inventories.2026_06.first_print"
- resolutionSourceUrl: "https://www.census.gov/manufacturing/m3/adv/current/index.html"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.census.gov"], "expectedReleaseWindow": {"end": "2026-07-27", "start": "2026-07-27"}, "field": "Defense capital goods; Inventories; seasonally adjusted; preliminary June 2026 value", "releasePolicy": "first_print", "sourceSeriesId": "M3_ADV_TABLE2_DEFENSE_CAPITAL_GOODS_INVENTORY_SA", "sourceUrl": "https://www.census.gov/manufacturing/m3/adv/current/index.html", "table": "Monthly Advance Report on Durable Goods Manufacturers' Shipments, Inventories and Orders, Table 2 - Unfilled Orders and Inventory", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-15-8dd3078fe13d3af0a3b419b722d536b8642ab37d614e8373b70faea0c7284901.json"
- targetContentHash: "8dd3078fe13d3af0a3b419b722d536b8642ab37d614e8373b70faea0c7284901"
- registrationCommit: "05b56ed86beda8ccde0b2891912278d9ab065f09"
- registeredAtUtc: "2026-07-15T19:28:27Z"
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
a48fd8d0491afcc089094163d9312c097f2ded89549c3cfa4ff913c2a3f96977

# Draft forecast response
{"slug":"us-defense-capital-goods-inventories-june-2026","country":"US","type":"data","title":"US defense capital-goods inventories, June 2026","question":"What will the U.S. Census Bureau first report for seasonally adjusted defense capital goods total inventories in June 2026?","unit":"usd_billions","pointEstimate":28.35,"ciLow":28.22,"ciHigh":28.48,"confidence":0.8,"resolutionDate":"2026-07-27","resolutionSource":"U.S. Census Bureau Monthly Advance Report on Durable Goods Manufacturers' Shipments, Inventories and Orders","resolutionSourceUrl":"https://www.census.gov/manufacturing/m3/adv/current/index.html","resolutionRule":"Resolve to the preliminary June 2026 value for Defense capital goods; Total Inventories in Table 2 of the first U.S. Census Bureau June 2026 Advance Report, using the seasonally adjusted estimate in millions of dollars multiplied by 0.001 and rounded to three decimal places in USD billions. Ignore all later revisions and corrections not contained in that first print.","dataPointId":"census.m3.defense_capital_goods.inventories.2026_06.first_print","historicalContext":[{"label":"2026-01 first print, SA","value":27.82},{"label":"2026-02 first print, SA","value":27.877},{"label":"2026-03 first print, SA","value":28.088},{"label":"2026-04 first print, SA","value":28.121},{"label":"2026-05 first print, SA","value":28.257}],"drivers":["persistent nominal inventory accumulation","recent positive monthly momentum","defense aircraft and other long-cycle production inventories","survey and concurrent-seasonal-adjustment noise"],"sourceContext":["https://www.census.gov/manufacturing/m3/adv/current/index.html","https://www.census.gov/manufacturing/m3/adv/pdf/table2a.pdf","https://www.census.gov/manufacturing/m3/historical_data/pressreleases/adv/2026/jan26adv.pdf","https://www.census.gov/manufacturing/m3/historical_data/pressreleases/adv/2026/feb26adv.pdf","https://www.census.gov/manufacturing/m3/historical_data/pressreleases/adv/2026/mar26adv.pdf","https://www.census.gov/manufacturing/m3/historical_data/pressreleases/adv/2026/apr26adv.pdf","https://www.census.gov/economic-indicators/calendar-listview.html"],"runAt":"2026-07-15T19:34:10Z","reasoning":[{"kind":"heading","text":"June 2026 defense capital-goods inventories forecast"},{"kind":"text","text":"The resolver is Census M3 Advance Table 2 series M3_ADV_TABLE2_DEFENSE_CAPITAL_GOODS_INVENTORY_SA: preliminary June 2026 defense capital goods total inventories, seasonally adjusted, reported in millions and converted to USD billions. The first official print alone controls; later revisions do not."},{"kind":"text","text":"The Census economic-indicator calendar explicitly schedules the June 2026 Advance Report on Durable Goods for July 27, 2026 at 8:30 a.m. EDT, verifying the ledger resolution date rather than inferring it from monthly cadence."},{"kind":"tool","tool":"official.lookup","call":"Fetch the latest Census M3 May 2026 Advance Table 2 defense capital-goods inventory row.","result":"The official seasonally adjusted preliminary values were May 2026 28,257 million, revised April 2026 28,161 million, and March 2026 28,022 million; May rose 0.3%."},{"kind":"tool","tool":"official.lookup","call":"Fetch the Census January 2026 Advance Table 2 defense capital-goods inventory history.","result":"The official seasonally adjusted values shown were January 2026 27,820 million, December 2025 27,668 million, and November 2025 27,738 million."},{"kind":"tool","tool":"official.lookup","call":"Fetch first-print defense capital-goods inventories from the February, March, and April 2026 Census advance releases.","result":"The preliminary seasonally adjusted prints were February 2026 27,877 million, March 2026 28,088 million, and April 2026 28,121 million."},{"kind":"text","text":"Outside view/base rate: the seven-month first-print reference class from November 2025 through May 2026 is 27.738, 27.668, 27.820, 27.877, 28.088, 28.121, and 28.257 billion. Six monthly changes average +0.0865 billion and are positive in five of six months, favoring another moderate increase over pure level persistence."},{"kind":"text","text":"Level is anchored at May's 28.257 billion. Momentum contributes about +0.087 billion from the mean monthly change. No identified one-off warrants a large adjustment; the policy/production mechanism is gradual accumulation in long-cycle defense manufacturing, so the combined estimate is rounded to 28.350 billion."},{"kind":"math","text":"Prior/update/interval: persistence-plus-drift prior using the seven first-print observations from November 2025-May 2026; successive changes are -0.070, +0.152, +0.057, +0.211, +0.033, and +0.136 billion. Their mean is +0.0865 and sample sigma = 0.101 billion. Point = 28.257 + 0.0865 = 28.3435, rounded to 28.35. The normal 80% half-width is 1.28*sigma = 1.28*0.101 = 0.129 billion, giving 28.35 ± 0.13 = [28.22, 28.48]."},{"kind":"text","text":"Upside risk comes from unusually rapid accumulation tied to aircraft, missile, ship, or communications production and would land above the interval if June adds more than about 0.22 billion. Downside risk is a drawdown, delivery-driven liquidation, or noisy seasonal adjustment; a fall of more than about 0.04 billion from May would land below the interval. Either would be outside the interval and falsify the smooth-accumulation reference class."},{"kind":"forecast","point":28.35,"ciLow":28.22,"ciHigh":28.48}]}
