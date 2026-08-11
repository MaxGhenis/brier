# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.ntia.broadband_al11038_obligations
- period: FY2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-ntia-broadband-al11038-obligations-fy2026"
- country: "US"
- targetUnit: "usd_millions"
- dataPointId: "usaspending.ntia.broadband_al11038_obligations.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "results[time_period.fiscal_year={fiscal_year}].aggregated_amount", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.search.spending_over_time.ntia.broadband_program_obligations", "sourceUrl": "https://api.usaspending.gov/api/v2/search/spending_over_time/", "table": "USAspending API v2 advanced search, financial-assistance award transactions filtered to Assistance Listing 11.038, obligations by fiscal year", "transform": {"awardTypeCodes": ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11"], "factor": 1e-06, "fiscalYear": "{fiscal_year}", "group": "fiscal_year", "operation": "multiply", "programNumbers": ["11.038"], "requestMethod": "POST", "spendingLevel": "transactions"}}
- targetRegistrationPath: "records/targets/2026-08-11-e04d264d1888de22891b4b0a6aa7e0f8f3ae8b937613de7e3ee9242f726e37e9.json"
- targetContentHash: "e04d264d1888de22891b4b0a6aa7e0f8f3ae8b937613de7e3ee9242f726e37e9"
- registrationCommit: "49bf9b5726d9faf93b6c96c9d73d4a52dc74c030"
- registeredAtUtc: "2026-08-11T20:38:09Z"
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
5249639e0331c07c79625661a18bac9521bf3d54279a82a3b00061657ee01772

# Draft forecast response
{
  "slug": "us-ntia-broadband-al11038-obligations-fy2026",
  "country": "US",
  "type": "data",
  "title": "NTIA 11.038 FY2026 obligations",
  "question": "What will USAspending API v2 advanced search spending_over_time report as FY2026 aggregated financial-assistance transaction obligations, in usd_millions, for Assistance Listing 11.038 Public Wireless Supply Chain Innovation Fund Grant Program, grouped by fiscal_year, under the registered query snapshot and first registered snapshot policy?",
  "unit": "usd_millions",
  "pointEstimate": 45,
  "ciLow": 5,
  "ciHigh": 290,
  "confidence": 0.8,
  "resolutionDate": "2026-10-22",
  "resolutionSource": "USAspending API v2 advanced search, spending_over_time",
  "resolutionSourceUrl": "https://api.usaspending.gov/api/v2/search/spending_over_time/",
  "resolutionRule": "Resolve from USAspending API v2 advanced search, financial-assistance award transactions filtered to Assistance Listing 11.038, award_type_codes 02-11, spending_level transactions, grouped by fiscal_year; use results[time_period.fiscal_year=2026].aggregated_amount multiplied by 1e-06 and rounded to usd_millions. The registered query snapshot policy resolves on the Thesis lab-committed outer bound 2026-10-22, with expectedReleaseWindow 2026-10-15 through 2026-10-22; later USAspending changes are irrelevant.",
  "dataPointId": "usaspending.ntia.broadband_al11038_obligations.fy2026.registered_query_snapshot",
  "historicalContext": [
    {
      "label": "FY2024 official NTIA first-NOFO award total proxy",
      "value": 140
    },
    {
      "label": "FY2025 official NTIA second-NOFO awarded total proxy",
      "value": 409.852
    },
    {
      "label": "FY2026 fourth-NOFO announced funding ceiling proxy",
      "value": 53
    }
  ],
  "drivers": [
    "NOFO4 closes late in FY2026",
    "Only three expected NOFO4 awards",
    "Prior award cycles were lumpy",
    "FY2026 awards may slip into FY2027",
    "Unexpected late obligations remain possible"
  ],
  "sourceContext": [
    "https://api.usaspending.gov/api/v2/search/spending_over_time/",
    "https://api.usaspending.gov/docs/endpoints",
    "https://www.ntia.gov/press-release/2024/biden-harris-administration-awards-42m-wireless-innovation",
    "https://www.ntia.gov/funding-programs/public-wireless-supply-chain-innovation-fund/innovation-fund-round-2-2024-open-ru",
    "https://www.ntia.gov/funding-programs/public-wireless-supply-chain-innovation-fund",
    "https://www.grants.gov/search-results-detail/363179"
  ],
  "runAt": "2026-08-11T20:50:53Z",
  "activityLog": [],
  "reasoning": [
    {
      "kind": "heading",
      "text": "NTIA Assistance Listing 11.038 FY2026 obligations"
    },
    {
      "kind": "text",
      "text": "The registered target is the USAspending spending_over_time query for financial-assistance award transactions under Assistance Listing 11.038, transformed to usd_millions. The target is a registered query snapshot, so I use the lab-committed 2026-10-22 outer bound rather than inferring a release day."
    },
    {
      "kind": "tool",
      "tool": "web.open",
      "call": "Open USAspending API endpoint documentation and endpoint index for /api/v2/search/spending_over_time/.",
      "result": "Fetched USAspending API docs: endpoints do not require authorization; status codes listed include 200, 400, and 500; /api/v2/search/spending_over_time/ is a POST endpoint returning transaction aggregated amounts."
    },
    {
      "kind": "tool",
      "tool": "web.search",
      "call": "Search official NTIA first-NOFO award page for Wireless Innovation Fund award totals.",
      "result": "Fetched NTIA 2024-02-12 release: final first-NOFO award was $42,299,693.72; NTIA stated this brought first-NOFO Wireless Innovation Fund awards to $140 million across 17 grantees."
    },
    {
      "kind": "tool",
      "tool": "web.search",
      "call": "Search official NTIA Round 2 program page for awarded amount and award ranges.",
      "result": "Fetched NTIA Round 2 page: NTIA awarded $409,852,406.47 under NOFO 2; SRFA 1 award size range was $25,000,000-$45,000,000 per project and SRFA 2 was $5,000,000-$10,000,000 per project."
    },
    {
      "kind": "tool",
      "tool": "web.search",
      "call": "Search current official Grants.gov opportunity NTIA-PWSCIF-26-01 for FY2026 forward-looking obligation evidence.",
      "result": "Fetched Grants.gov opportunity NTIA-PWSCIF-26-01: posted 2026-07-14, closes 2026-09-09, Assistance Listing 11.038, expected number of awards 3."
    },
    {
      "kind": "tool",
      "tool": "web.search",
      "call": "Search NTIA program page for current 2026 program direction.",
      "result": "Fetched NTIA program page: Innovation Fund is a $1.5 billion investment over the next decade; NTIA listed a 2026-03-23 AI RAN listening session and a 2026-03-10 new-direction notice for AI RAN."
    },
    {
      "kind": "text",
      "text": "Base rate/reference class: recent official NTIA award-cycle flow proxies are FY2024 about 140.0 and FY2025 409.852 usd_millions, mean 274.9, range 140.0-409.9. Last-print persistence benchmark is 409.9, but the FY2026 current signal is a much smaller and late-year NOFO4 process: 3 expected awards, applications closing 2026-09-09, with awards expected only after review."
    },
    {
      "kind": "math",
      "text": "Model candidates under thesis_model_candidate_v1, sparse-flow version: persistence candidate point=409.9, p10=165.7, p50=409.9, p90=654.1, 80% interval 165.7-654.1, 90% interval 91.1-728.7, interval_method=sparse annual flow sigma, calibration_n=2, train_cutoff=FY2025, walk_forward_score unavailable because only two comparable award cycles. Current-NOFO candidate point=45.0, p10=5.0, p50=45.0, p90=90.0, 80% interval 5.0-90.0, 90% interval 0.0-120.0, interval_method=NOFO4 timing and award-count cap, calibration_n=3 public program facts, train_cutoff=2026-08-11. I select the current-NOFO candidate but retain the persistence sigma for tail width because obligations are lumpy."
    },
    {
      "kind": "math",
      "text": "Prior/update/interval: prior = last awarded-cycle persistence 409.9 from FY2025 NOFO2; historical sample = FY2024 140.0 and FY2025 409.852 usd_millions; adjustment components = -310 for the late FY2026 NOFO4 close and no fetched official FY2026 award announcement, -55 for only 3 expected NOFO4 awards and likely FY2027 slippage, yielding about 45.0. For the flow values, sample sigma = 190.8; 1.28*sigma = 244.2, so an unbounded 80% band around 45 is about -199 to 289. I bound obligations near zero and round to 5-290 usd_millions."
    },
    {
      "kind": "text",
      "text": "Upside risk outside the interval: NTIA could obligate a delayed Round 3 package or several NOFO4 awards before 2026-09-30, pushing FY2026 transaction obligations above 290. Downside risk outside the interval: all NOFO4 awards could slip into FY2027 and no amendments could post in FY2026, landing below 5."
    },
    {
      "kind": "forecast",
      "point": 45,
      "ciLow": 5,
      "ciHigh": 290
    }
  ]
}
