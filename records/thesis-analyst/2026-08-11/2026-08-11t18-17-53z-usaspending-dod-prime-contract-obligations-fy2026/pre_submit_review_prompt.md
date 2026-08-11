# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.dod.prime_contract_obligations
- period: FY2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
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
0458d0eaf11e40c604848e617b2b51020c8d39aae65e1d65f17f0a112ef17c2b

# Draft forecast response
{
  "slug": "us-dod-prime-contract-obligations-fy2026",
  "country": "US",
  "type": "data",
  "title": "FY2026 DoD prime contract obligations",
  "question": "What will USAspending API v2 report for Department of Defense agency 097 obligations by award category, contracts row, fiscal year 2026, as a registered query snapshot resolving on the first available post-FY2026 closeout snapshot?",
  "unit": "billions USD",
  "pointEstimate": 505.0,
  "ciLow": 464.6,
  "ciHigh": 545.4,
  "confidence": 0.8,
  "resolutionDate": "2026-10-22",
  "resolutionSource": "USAspending API v2, agency 097 obligations by award category",
  "resolutionSourceUrl": "https://api.usaspending.gov/api/v2/agency/097/obligations_by_award_category/?fiscal_year=2026",
  "resolutionRule": "Resolve from USAspending API v2 endpoint /api/v2/agency/097/obligations_by_award_category/?fiscal_year=2026, using the results row where category=contracts and field aggregated_amount, multiplied by 1e-09 to convert dollars to billions USD. This is a registered_query_snapshot target for FY2026; later revisions after the registered snapshot are not part of the first-print resolution. Round to one decimal billion USD. The Thesis ledger commits the expected release window 2026-10-15 through 2026-10-22 and the resolutionDate is the outer bound 2026-10-22.",
  "dataPointId": "usaspending.dod.prime_contract_obligations.fy2026.registered_query_snapshot",
  "historicalContext": [
    {
      "label": "FY2022 GAO FPDS defense agencies services plus products, constant FY2022 dollars proxy",
      "value": 415.0
    },
    {
      "label": "FY2023 GAO FPDS defense agencies services plus products, constant FY2023 dollars proxy",
      "value": 456.0
    },
    {
      "label": "FY2024 GAO FPDS defense agencies services plus products, constant FY2024 dollars proxy",
      "value": 445.0
    },
    {
      "label": "FY2025 GAO FPDS defense agencies services plus products, constant FY2025 dollars proxy",
      "value": 491.0
    }
  ],
  "drivers": [
    "FY2025 defense contract level persistence",
    "FY2026 acquisition funding support",
    "mandatory reconciliation funding available through 2029",
    "closeout reporting lag and deobligation risk"
  ],
  "sourceContext": [
    "https://api.usaspending.gov/docs/endpoints",
    "https://api.usaspending.gov/api/v2/agency/097/obligations_by_award_category/?fiscal_year=2026",
    "https://files.gao.gov/multimedia/Federal_Government_Contracting-FY2022/index.html",
    "https://files.gao.gov/multimedia/Federal_Government_Contracting/index.html",
    "https://files.gao.gov/multimedia/Federal_Government_Contracting-FY2024/index.html",
    "https://files.gao.gov/multimedia/Federal_Government_Contracting-FY2025/index.html",
    "https://www.cbo.gov/publication/62396",
    "https://www.congress.gov/crs-product/IN12641",
    "https://app.thesisinstitute.org/specs.json"
  ],
  "runAt": "2026-08-11T18:18:52Z",
  "reasoning": [
    {
      "kind": "heading",
      "text": "FY2026 DoD prime contract obligations"
    },
    {
      "kind": "text",
      "text": "The registered target is the USAspending API v2 agency 097 obligations_by_award_category contracts row for fiscal_year=2026. The unit, slug, dataPointId, and 2026-10-22 outer-bound resolution date are taken from the canonical ledger target. I attempted the required specs.json check; the hosted fetch returned no visible body, so I kept the ledger-provided slug rather than inventing a replacement."
    },
    {
      "kind": "tool",
      "tool": "usaspending.docs",
      "call": "Fetched USAspending API endpoint index for /api/v2/agency/<TOPTIER_AGENCY_CODE>/obligations_by_award_category/ and target code 097 with fiscal_year=2026.",
      "result": "USAspending API docs list GET /api/v2/agency/<TOPTIER_AGENCY_CODE>/obligations_by_award_category/ as returning obligations by award category within a single fiscal year; target uses TOPTIER_AGENCY_CODE=097 and fiscal_year=2026."
    },
    {
      "kind": "tool",
      "tool": "gao.fpds.dashboard",
      "call": "Fetched GAO Governmentwide Contracting FY2022 dashboard.",
      "result": "GAO FPDS FY2022 defense agencies: services $205B, products $210B, total proxy $415B; source states data are GAO analysis of Federal Procurement Data System data as of May 2023."
    },
    {
      "kind": "tool",
      "tool": "gao.fpds.dashboard",
      "call": "Fetched GAO Governmentwide Contracting FY2023 and FY2024 dashboards.",
      "result": "GAO FPDS FY2023 defense agencies: services $230B, products $226B, total proxy $456B. GAO FPDS FY2024 defense agencies: services $240B, products $205B, total proxy $445B."
    },
    {
      "kind": "tool",
      "tool": "gao.fpds.dashboard",
      "call": "Fetched GAO Governmentwide Contracting FY2025 dashboard.",
      "result": "GAO FPDS FY2025 defense agencies: services $238B, products $253B, total proxy $491B; GAO also states governmentwide contract obligations were $793B and other transaction agreements were $18.2B, not included in contract obligations."
    },
    {
      "kind": "tool",
      "tool": "budget.current_signal",
      "call": "Fetched CBO FY2026 defense budget analysis and CRS FY2026 NDAA funding summary.",
      "result": "CBO reports DoD FY2026 acquisition funding in the budget request was $384B, 18% more than appropriated for 2025; CRS reports enacted FY2026 NDAA DOD-Military authorization total $855.7B versus enacted FY2025 $849.9B, with procurement $161.7B and RDT&E $145.7B."
    },
    {
      "kind": "text",
      "text": "Base rate / reference class: the recent FPDS defense-contract proxy totals are FY2022 415, FY2023 456, FY2024 445, FY2025 491 billions. Last-print persistence is 491.0. The simple one-year-change history is +41, -11, +46, so recent realized changes have mean +25.3 and a wide range from -11 to +46."
    },
    {
      "kind": "math",
      "text": "Model candidates under thesis_model_candidate_v1, computed from fetched history: persistence candidate point=491.0, p10=450.6, p50=491.0, p90=531.4, 80% interval 450.6-531.4, 90% interval 439.0-543.0, interval_method=successive-change residual normal, calibration_n=3, train_cutoff=FY2025; mean-change candidate point=516.3, p10=475.9, p50=516.3, p90=556.7, 80% interval 475.9-556.7, calibration_n=3. I select persistence-plus-current-budget-update because the sample is short and FY2026 budget evidence supports only a modest upward move, not the full mean-change rule."
    },
    {
      "kind": "math",
      "text": "Prior/update/interval: prior=last-print persistence 491.0 from FY2025 GAO FPDS defense services+products proxy; historical sample=FY2022-FY2025 values 415,456,445,491; adjustment components=+14.0 for FY2026 acquisition funding support and mandatory reconciliation availability, shrunk because enacted base procurement/RDT&E is not uniformly above FY2025 and funds are available through 2029; point=491.0+14.0=505.0. For uncertainty, successive changes are +41,-11,+46, mean change 25.3, sigma = 31.6; 80% half-width roughly 1.28*sigma = 40.4, so interval is 505.0-40.4=464.6 to 505.0+40.4=545.4."
    },
    {
      "kind": "text",
      "text": "Sanity check: an 80% band with half-width about $40B would have covered FY2023, FY2024, and FY2025 moves around a persistence prior except for years with unusually large positive swings near the upper edge. That is acceptable here because FY2026 has supportive budget authority but also reporting lag, continuing-resolution timing, and deobligation risks."
    },
    {
      "kind": "text",
      "text": "Upside risk: the result would land above the interval if DoD obligates a large share of reconciliation-funded shipbuilding, missiles, and RDT&E-related contract actions before the registered snapshot or if late September closeout awards are reported unusually quickly. Downside risk: the result would land below the interval if FY2026 contract reporting lags past the October snapshot, if procurement execution is delayed, or if large prior-year deobligations hit the contracts row."
    },
    {
      "kind": "forecast",
      "point": 505.0,
      "ciLow": 464.6,
      "ciHigh": 545.4
    }
  ]
}
