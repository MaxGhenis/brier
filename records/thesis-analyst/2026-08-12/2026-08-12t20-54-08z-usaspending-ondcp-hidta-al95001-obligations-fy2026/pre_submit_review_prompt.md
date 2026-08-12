# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.ondcp.hidta_al95001_obligations
- period: FY2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-ondcp-hidta-al95001-obligations-fy2026"
- country: "US"
- targetUnit: "usd_millions"
- dataPointId: "usaspending.ondcp.hidta_al95001_obligations.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "results[time_period.fiscal_year={fiscal_year}].aggregated_amount", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.search.spending_over_time.ondcp.hidta_program_obligations", "sourceUrl": "https://api.usaspending.gov/api/v2/search/spending_over_time/", "table": "USAspending API v2 advanced search, financial-assistance award transactions filtered to Assistance Listing 95.001, obligations by fiscal year", "transform": {"awardTypeCodes": ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11"], "factor": 1e-06, "fiscalYear": "{fiscal_year}", "group": "fiscal_year", "operation": "multiply", "programNumbers": ["95.001"], "requestMethod": "POST", "spendingLevel": "transactions"}}
- targetRegistrationPath: "records/targets/2026-08-11-eb895fc1e680eab66d27b1046b6df148fa4c00829fc42935f4c36fb1c8a4a42a.json"
- targetContentHash: "eb895fc1e680eab66d27b1046b6df148fa4c00829fc42935f4c36fb1c8a4a42a"
- registrationCommit: "49bf9b5726d9faf93b6c96c9d73d4a52dc74c030"
- registeredAtUtc: "2026-08-11T20:38:09Z"

# Registered-query series (machine checked)
This series is DEFINED by the registered query in sourceBinding — no published table or headline page exists for it, so agency profile totals and search-result summaries are the WRONG series. Fetch historicalContext by executing the exact registered query for each prior period: substitute each prior period into sourceBinding.transform's request template and POST it to "https://api.usaspending.gov/api/v2/search/spending_over_time/", then read the value at sourceBinding.field and apply sourceBinding.transform's operation and factor. History values obtained any other way will fail anchor validation, and a cell without historicalContext fails normalization — if the query cannot be executed, refuse with the fetch evidence rather than omitting history or substituting a broader aggregate.
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
a9b68d84af19e5c4c036db479ca0c4b8059b1c52c604bb9edea3e380e465ed78

# Draft forecast response
{
  "slug": "us-ondcp-hidta-al95001-obligations-fy2026",
  "country": "US",
  "type": "data",
  "title": "FY2026 HIDTA AL 95.001 obligations",
  "question": "For FY2026, what will the USAspending API v2 advanced search spending_over_time endpoint return on the first registered-query snapshot for results[time_period.fiscal_year=2026].aggregated_amount, scaled to usd_millions, for prime financial-assistance award transactions filtered to Assistance Listing 95.001, grouped by action-date federal fiscal year, not seasonally adjusted?",
  "unit": "usd_millions",
  "pointEstimate": 271.657676,
  "ciLow": 257.222807,
  "ciHigh": 286.092545,
  "confidence": 0.8,
  "resolutionDate": "2026-10-22",
  "resolutionSource": "USAspending API v2 advanced search registered-query snapshot",
  "resolutionSourceUrl": "https://api.usaspending.gov/api/v2/search/spending_over_time/",
  "resolutionRule": "Resolve from the first archived registered-query snapshot captured in the Thesis expected release window 2026-10-15 through 2026-10-22, with resolutionDate equal to the lab-committed outer bound 2026-10-22. POST to the USAspending API v2 /api/v2/search/spending_over_time/ endpoint with group=fiscal_year, spending_level=transactions, filters.time_period=[{start_date: 2025-10-01, end_date: 2026-09-30}], filters.program_numbers=[95.001], and filters.award_type_codes=[02,03,04,05,06,07,08,09,10,11]. Read the unique result where time_period.fiscal_year is 2026, take aggregated_amount in dollars, multiply by 0.000001, and report in usd_millions. This is a registered_query_snapshot / first snapshot rule; later USAspending revisions are irrelevant.",
  "dataPointId": "usaspending.ondcp.hidta_al95001_obligations.fy2026.registered_query_snapshot",
  "historicalContext": [
    { "label": "FY2019 registered query value, usd_millions", "value": 284.14514631 },
    { "label": "FY2020 registered query value, usd_millions", "value": 270.27144368 },
    { "label": "FY2021 registered query value, usd_millions", "value": 268.60530517 },
    { "label": "FY2022 registered query value, usd_millions", "value": 252.76050027 },
    { "label": "FY2023 registered query value, usd_millions", "value": 266.41544691 },
    { "label": "FY2024 registered query value, usd_millions", "value": 273.95994611 },
    { "label": "FY2025 registered query value, usd_millions", "value": 271.6576756 }
  ],
  "drivers": [
    "last completed fiscal-year persistence",
    "stable FY2019-FY2025 AL 95.001 range",
    "continuous USAspending revision/snapshot risk",
    "FY2026 live query not yet comparable to final snapshot"
  ],
  "sourceContext": [
    "https://api.usaspending.gov/api/v2/search/spending_over_time/",
    "https://raw.githubusercontent.com/fedspendingtransparency/usaspending-api/master/usaspending_api/api_contracts/contracts/v2/search/spending_over_time.md",
    "https://app.thesisinstitute.org/specs.json"
  ],
  "runAt": "2026-08-12T20:55:37Z",
  "reasoning": [
    { "kind": "heading", "text": "FY2026 HIDTA AL 95.001 registered-query forecast" },
    { "kind": "text", "text": "Resolution framing: the target is the USAspending API v2 spending_over_time registered query for Assistance Listing 95.001 prime financial-assistance award transactions, fiscal-year grouped, first archived registered-query snapshot for FY2026. The target registration supplies expectedReleaseWindow 2026-10-15 to 2026-10-22, so I use the lab-committed outer bound 2026-10-22 rather than inferring a release day from cadence." },
    { "kind": "tool", "tool": "repo_and_specs.check", "call": "Parsed records/targets/2026-08-11-eb895fc1e680eab66d27b1046b6df148fa4c00829fc42935f4c36fb1c8a4a42a.json and fetched https://app.thesisinstitute.org/specs.json", "result": "Target registration parsed with catalogSlug us-ondcp-hidta-al95001-obligations-fy2026, targetContentHash eb895fc1e680eab66d27b1046b6df148fa4c00829fc42935f4c36fb1c8a4a42a, expectedReleaseWindow.end 2026-10-22, sourceUrl https://api.usaspending.gov/api/v2/search/spending_over_time/. Fetched specs.json size was 11289 bytes; rg found 0 occurrences of us-ondcp-hidta-al95001-obligations-fy2026." },
    { "kind": "tool", "tool": "usaspending.spending_over_time", "call": "POST group=fiscal_year, spending_level=transactions, program_numbers=[95.001], award_type_codes=[02..11], FY2019-FY2021 time_periods", "result": "USAspending echoed FY2019 aggregated_amount 284145146.31 dollars = 284.14514631 usd_millions; FY2020 aggregated_amount 270271443.68 dollars = 270.27144368 usd_millions; FY2021 aggregated_amount 268605305.17 dollars = 268.60530517 usd_millions." },
    { "kind": "tool", "tool": "usaspending.spending_over_time", "call": "POST same registered query for FY2022-FY2024 time_periods", "result": "USAspending echoed FY2022 aggregated_amount 252760500.27 dollars = 252.76050027 usd_millions; FY2023 aggregated_amount 266415446.91 dollars = 266.41544691 usd_millions; FY2024 aggregated_amount 273959946.11 dollars = 273.95994611 usd_millions." },
    { "kind": "tool", "tool": "usaspending.spending_over_time", "call": "POST same registered query for FY2025 completed period and FY2026 target period as currently visible", "result": "USAspending echoed FY2025 aggregated_amount 271657675.6 dollars = 271.6576756 usd_millions. The same FY2026 target-period query, fetched during this run before the registered snapshot window, echoed aggregated_amount 262984.51 dollars = 0.26298451 usd_millions, which is not comparable to completed fiscal-year snapshots." },
    { "kind": "tool", "tool": "brier.timeseries", "call": "PYTHONPATH=. python3 scripts/run_time_series_models.py --target-id usaspending.ondcp.hidta_al95001_obligations.fy2026.registered_query_snapshot --target-period FY2026 --models persistence --round-increment 0.000001 with FY2019-FY2025 fetched history", "result": "thesis_model_candidate_v1 persistence.last_print generatedAt 2026-08-12T20:55:30Z: pointEstimate 271.657676, p10 256.798422, p50 271.657676, p90 282.257399, interval80 lower 256.798422 upper 282.257399, interval90 lower 256.305646 upper 283.78501, intervalMethod residual_quantile, calibrationN 6, walk_forward_1_step meanAbsoluteError 9.147727064999989." },
    { "kind": "text", "text": "Base rate / reference class: the last 7 completed fiscal-year registered-query values were 284.14514631, 270.27144368, 268.60530517, 252.76050027, 266.41544691, 273.95994611, and 271.6576756 usd_millions. Their mean was 269.687923, median 270.271444, range 252.760500-284.145146, and the strongest simple benchmark is last-print persistence at FY2025 = 271.6576756 usd_millions." },
    { "kind": "math", "text": "Prior/update/interval: prior = persistence.last_print candidate from FY2019-FY2025 completed registered-query history, point 271.657676. Adjustment components: 0.000000 for current FY2026 live-query value because 0.26298451 usd_millions is an in-year continuous USAspending value before the registered snapshot window and not a comparable final fiscal-year snapshot; no other direct current signal was fetched. For interval sizing on this annual flow series, sample sigma = 9.397701 from the 7 completed fetched values; 1.28*sigma = 12.029057. I widen the half-width by 1.20x to 14.434868 because USAspending registered_query_snapshot outcomes can move with late-posted/revised transactions between the live query and the October capture window. Final 80% interval = 271.657676 +/- 14.434868 = [257.222807, 286.092545]. This interval would contain 6 of the 7 completed FY2019-FY2025 registered-query values." },
    { "kind": "text", "text": "Counter-consideration: upside risk outside the interval would be a late FY2026 bulk HIDTA grant obligation or cleanup transaction that pushes the AL 95.001 fiscal-year aggregate above about 286.1 usd_millions. Downside risk outside the interval would land below the interval if FY2026 awards remain unusually delayed, reclassified, or deobligated so that the October registered snapshot stays below about 257.2 usd_millions." },
    { "kind": "forecast", "point": 271.657676, "ciLow": 257.222807, "ciHigh": 286.092545 }
  ]
}
