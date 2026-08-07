# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.dod.prime_contract_obligations
- period: FY2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-prime-contract-obligations-fy2026"
- country: "US"
- targetUnit: "billions USD"
- dataPointId: "usaspending.dod.prime_contract_obligations.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "results[category=contracts].aggregated_amount", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.agency.097.obligations_by_award_category.contracts", "sourceUrl": "https://api.usaspending.gov/api/v2/agency/097/obligations_by_award_category/?fiscal_year={fiscal_year}", "table": "USAspending API v2, agency 097 (DoD) obligations by award category, contracts row, fiscal year to date", "transform": {"factor": 1e-09, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-07-8b3a9c297b91e44b81cdda9bca2c64337b021348fba63395c4b5879b6e3e94be.json"
- targetContentHash: "8b3a9c297b91e44b81cdda9bca2c64337b021348fba63395c4b5879b6e3e94be"
- registrationCommit: "a6991688486115b857a52f29c370ed8f884457e3"
- registeredAtUtc: "2026-08-07T17:54:06Z"
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
485867f3ef642bd7fd321da7f63fa3bd5193208ffab44732112b22f4eeda9ee0

# Draft forecast response
{"slug":"us-dod-prime-contract-obligations-fy2026","country":"US","type":"data","title":"DoD prime contract obligations FY2026","question":"What will USAspending.gov first print for Department of Defense agency 097 obligations by award category, contracts row, fiscal year 2026, in billions of current U.S. dollars?","unit":"usd_billions","pointEstimate":485,"ciLow":405,"ciHigh":565,"confidence":0.8,"resolutionDate":"2026-10-22","resolutionSource":"USAspending API v2, agency 097 obligations by award category","resolutionSourceUrl":"https://api.usaspending.gov/api/v2/agency/097/obligations_by_award_category/?fiscal_year=2026","resolutionRule":"Resolve to the first registered-query snapshot on 2026-10-22 from api.usaspending.gov API v2 endpoint /api/v2/agency/097/obligations_by_award_category/?fiscal_year=2026, taking results[category=contracts].aggregated_amount and multiplying by 1e-9. Use the first official print only; do not revise for later API restatements or same-day corrections unless the registered snapshot itself is replaced before capture. Round to the agency-published dollar amount converted to billions USD.","dataPointId":"usaspending.dod.prime_contract_obligations.fy2026.registered_query_snapshot","historicalContext":[{"label":"FY2024 CRS FPDS DoD contract obligations","value":445.23},{"label":"FY2023 CRS FPDS DoD contract obligations","value":456},{"label":"FY2022 CRS FPDS DoD contract obligations","value":414},{"label":"FY2021 CRS FPDS DoD contract obligations","value":389},{"label":"FY2020 CRS FPDS DoD contract obligations","value":423}],"drivers":["FY2026 total DoD budget request near $961.6B including $113.3B reconciliation funding","acquisition-heavy reconciliation funding should lift contractable dollars but may be multi-year","regular FY2026 procurement and O&M authorizations are not materially above FY2025","DoD contract obligations have recently stayed around the mid-$400B range","USAspending DoD contract data publication lag makes this a strict first-snapshot target"],"sourceContext":["https://api.usaspending.gov/api/v2/agency/097/obligations_by_award_category/?fiscal_year=2026","https://api.usaspending.gov/docs/endpoints","https://www.usaspending.gov/agency/department-of-defense","https://www.congress.gov/crs_external_products/R/PDF/R48784/R48784.2.pdf","https://www.cbo.gov/publication/62396","https://www.defense.gov/News/Transcripts/Transcript/Article/4228828/background-briefing-on-fy-2026-defense-budget/","https://www.congress.gov/crs-product/IN12641"],"runAt":"2026-08-07T19:08:54Z","reasoning":[{"kind":"heading","text":"DoD prime contract obligations FY2026 forecast"},{"kind":"text","text":"Framing and exact resolver: the target is the USAspending API v2 agency 097 obligations_by_award_category endpoint, fiscal_year=2026, contracts row only, transformed from dollars to billions USD. I keep the ledger resolver and its 2026-10-22 registered-query snapshot date; the observed value should be the first official API print for that snapshot, not a later revised history."},{"kind":"tool","tool":"official.lookup","call":"USAspending endpoint and publication-variant lookup for agency 097 obligations_by_award_category and DoD award data timing","result":"USAspending documents /api/v2/agency/<TOPTIER_AGENCY_CODE>/obligations_by_award_category/ as the endpoint for a breakdown of obligations by award category within a fiscal year; the target uses agency code 097 and fiscal_year 2026. USAspending pages also state a 90-day delay for displaying Department of Defense contract award data, so the forecast is explicitly for the registered 2026-10-22 API snapshot rather than a later complete-final restatement."},{"kind":"tool","tool":"official.lookup","call":"CRS FPDS history lookup for DOD vs non-DOD contract obligations, FY2015-FY2024","result":"The CRS FPDS figure gives recent DoD contract-obligation history in billions of nominal dollars: FY2020 about 423, FY2021 about 389, FY2022 about 414, FY2023 about 456, and FY2024 about 445.23 from the FY2024 contract-type stack 300.68 fixed-price + 140.46 cost-reimbursement + 4.09 time-and-materials/labor-hours."},{"kind":"tool","tool":"official.lookup","call":"CBO and DoD FY2026 budget request lookup","result":"CBO reports the DoD FY2026 budget request totaled 961 billion dollars including 113 billion dollars from the 2025 reconciliation act; the DoD briefing gives 961.6 billion total for DoD, 848.3 billion discretionary, and 113.3 billion mandatory reconciliation funding."},{"kind":"tool","tool":"official.lookup","call":"CRS FY2026 NDAA funding authorization lookup by appropriation title","result":"CRS reports enacted FY2026 NDAA Division A values of 161.7 billion dollars for Procurement, 145.7 billion for RDT&E, 291.5 billion for O&M, 193.2 billion for MILPERS, and 855.7 billion for total DoD-military subfunction 051; the comparable enacted FY2025 NDAA Procurement and O&M figures were 167.8 billion and 294.5 billion."},{"kind":"text","text":"Base rate/reference class: the best outside-view anchor is recent FPDS/USAspending-style DoD prime contract obligations, not total DoD budget authority. FY2020-FY2024 was roughly 389B to 456B with a recent center near 425B-445B, and FY2024 was 445.23B. That makes a no-shock persistence prior around 450B before considering FY2026 funding changes."},{"kind":"text","text":"Variant consistency: all anchors are for DoD procurement contract obligations or prime contract obligations measured in current-dollar billions, excluding Other Transaction Agreement obligations when the CRS FPDS source says they are excluded. The resolver is narrower in implementation because it reads USAspending's contracts award-category row for agency 097, but it is the closest official public history for the same prime-contract obligation concept."},{"kind":"math","text":"Prior/update/interval: persistence prior model uses FY2023-FY2024 near-last-value history at 450B, with the FY2020-FY2024 reference class 423, 389, 414, 456, 445.23. Adjustment components: +20B for FY2026 acquisition-heavy reconciliation funding that should partly obligate through contracts, +10B for nominal price/wage growth and defense-industrial capacity, +5B for policy emphasis on shipbuilding, munitions, missile defense, and industrial-base buys, offset by -0B to -15B because enacted regular Procurement and O&M are not above FY2025 and some reconciliation budget authority is multi-year. Point = 450 + 35 = 485. Interval method: sample standard deviation of the longer FY2015-FY2024 DoD contract-obligation values, approximately 273, 296, 322, 360, 383, 423, 389, 414, 456, 445, gives sigma = 62.6; 80% half-width = 1.28*sigma = 1.28*62.6 = 80.1, so 485 +/- 80 gives 405 to 565."},{"kind":"text","text":"Upside risk: a fast obligation of the reconciliation-funded acquisition tranche, large munitions and shipbuilding awards, or accelerated year-end contract actions would land above the interval, especially if the USAspending contracts row captures more than 565B by the registered snapshot. Downside risk: continuing resolution effects, slow obligation of multi-year reconciliation funds, award protests, or a stronger DoD publication lag would land below the interval, especially below 405B."},{"kind":"forecast","point":485,"ciLow":405,"ciHigh":565}]}
