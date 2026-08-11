# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.dod.prime_award_obligations
- period: FY2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-prime-award-obligations-fy2026"
- country: "US"
- targetUnit: "billions USD"
- dataPointId: "usaspending.dod.prime_award_obligations.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "obligations", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.agency.097.awards.obligations", "sourceUrl": "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year={fiscal_year}", "table": "USAspending API v2, agency 097 (DoD) award summary, prime award obligations, fiscal year to date", "transform": {"factor": 1e-09, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-07-59b334c6612eaf1c20be70ad587590901539f4fc2a11749e9f6a8f1ef2927907.json"
- targetContentHash: "59b334c6612eaf1c20be70ad587590901539f4fc2a11749e9f6a8f1ef2927907"
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
e365d15819f8330c85d08bab715d8f2fee986bfbd1a2121f28df3cc653a733ff

# Draft forecast response
{
  "slug": "us-dod-prime-award-obligations-fy2026",
  "country": "US",
  "type": "data",
  "title": "US DoD prime award obligations FY2026",
  "question": "What will USAspending API v2 report for Department of Defense agency 097 prime award obligations for FY2026, in billions USD, on the registered query snapshot, using the obligations field from /api/v2/agency/097/awards/?fiscal_year=2026?",
  "unit": "billions USD",
  "pointEstimate": 455,
  "ciLow": 380,
  "ciHigh": 530,
  "confidence": 0.8,
  "resolutionDate": "2026-10-22",
  "resolutionSource": "USAspending API v2, agency 097 awards",
  "resolutionSourceUrl": "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year={fiscal_year}",
  "resolutionRule": "Resolve from USAspending API v2 agency 097 awards endpoint for fiscal_year=2026, field obligations, transformed by multiplying by 1e-9 to billions USD. Use the registered query snapshot policy for the first resolving snapshot in the Thesis expectedReleaseWindow 2026-10-15 through 2026-10-22; the lab-committed outer bound is 2026-10-22. Round to the nearest 0.1 billion USD. Later API changes after the registered snapshot are irrelevant.",
  "dataPointId": "usaspending.dod.prime_award_obligations.fy2026.registered_query_snapshot",
  "historicalContext": [
    {
      "label": "FY2026 current USAspending agency 097 awards obligations fetched this run",
      "value": 245.1
    },
    {
      "label": "FY2024 DoD top-six subagency obligations shown in fetched USAspending API tutorial, summed",
      "value": 427.5
    },
    {
      "label": "FY2026 current USAspending agency 097 awards transaction count, millions",
      "value": 2.2
    }
  ],
  "drivers": [
    "Current FY2026 DoD award obligations already 245.1B",
    "DoD contract and IDV publication lag affects snapshot completeness",
    "FY2024 top-six DoD subagency obligations imply a high annual floor",
    "Registered snapshot occurs after FY2026 close",
    "Weak complete-history access keeps interval wide"
  ],
  "sourceContext": [
    "https://api.usaspending.gov/api/v2/agency/097/awards/",
    "https://api.usaspending.gov/api/v2/agency/097/",
    "https://api.usaspending.gov/docs/endpoints",
    "https://ua-libraries-research-data-services.github.io/UALIB_ScholarlyAPI_Cookbook/r/usa-spending.html"
  ],
  "runAt": "2026-08-11T18:15:10Z",
  "activityLog": [],
  "reasoning": [
    {
      "kind": "heading",
      "text": "USAspending DoD FY2026 Prime Award Obligations"
    },
    {
      "kind": "text",
      "text": "Resolution target is the registered USAspending API v2 agency 097 awards endpoint, fiscal_year=2026, obligations field, converted to billions USD. This is a registered query snapshot target with expectedReleaseWindow 2026-10-15 to 2026-10-22, so I use the ledger outer deadline 2026-10-22 rather than inferring a release-calendar day."
    },
    {
      "kind": "tool",
      "tool": "usaspending.awards",
      "call": "GET https://api.usaspending.gov/api/v2/agency/097/awards/",
      "result": "Fetched agency 097 awards endpoint: fiscal_year 2026, latest_action_date 2026-07-10T00:00:00, transaction_count 2205913, obligations 245063144206.58 USD = 245.063 billion USD."
    },
    {
      "kind": "tool",
      "tool": "usaspending.agency_overview",
      "call": "GET https://api.usaspending.gov/api/v2/agency/097/",
      "result": "Fetched agency overview: fiscal_year 2026, toptier_code 097, name Department of Defense, agency_id 1173, subtier_agency_count 36; overview text states DoD contract and IDV data are subject to a 90-day publication delay, while other DoD data are not."
    },
    {
      "kind": "tool",
      "tool": "usaspending.docs",
      "call": "Open USAspending endpoint contract for /api/v2/agency/{toptier_code}/awards/{?fiscal_year,agency_type,award_type_codes}",
      "result": "Fetched endpoint contract: fiscal_year is an optional number parameter; response attributes include toptier_code, fiscal_year, latest_action_date, transaction_count, obligations, and messages; sample response shows fiscal_year 2021, transaction_count 2, obligations 90000.0."
    },
    {
      "kind": "tool",
      "tool": "usaspending.cookbook_subagency_fy2024",
      "call": "Inspect public USAspending API tutorial section retrieving DoD FY2024 subagency data",
      "result": "Fetched public API example for Department of Defense FY2024 sub_agency: Navy obligations 135984528084, Army 108188048621, Air Force 101536586326, Defense Logistics Agency 53148863110, Defense Health Agency 20196091028, Missile Defense Agency 8463883396; top-six sum = 427.518 billion USD."
    },
    {
      "kind": "text",
      "text": "Base rate / reference class: the directly fetched target endpoint gives 245.1B through latest_action_date 2026-07-10, while the fetched FY2024 DoD top-six subagency obligations alone sum to 427.5B. I could not fetch complete fiscal-year history because the local shell failed before running curl/date, and browser safe-open rules blocked fiscal_year query variants. I therefore use a conservative benchmark prior around the FY2024 top-six floor plus smaller-subagency residual, rather than treating the incomplete FY2026 YTD run rate as the annual level."
    },
    {
      "kind": "math",
      "text": "Model candidates: incomplete-YTD run-rate = 245.063 * 365 / 283 = 316.1B, but this underweights late reporting and DoD publication lag; FY2024 top-six floor = 427.5B before smaller subagencies. Selected benchmark prior = 455.0B, reflecting the FY2024 top-six floor plus a modest residual for the other 30 DoD subagencies visible in the agency overview. No current fetched signal justifies a large move above the recent DoD scale, so no positive inside-view adjustment is added."
    },
    {
      "kind": "math",
      "text": "Prior/update/interval: prior = 455.0B from FY2024 top-six official API example plus smaller-subagency residual; historical sample is the fetched FY2026 YTD target endpoint and fetched FY2024 DoD subagency breakdown; adjustment components = 0.0B net because FY2026 YTD is incomplete and lagged. Interval method is fallback-prior dispersion from the wide gap between incomplete YTD run-rate and annualized DoD scale: sigma = 58.6B, half-width = 1.28*sigma = 75.0B, so 80% interval = 455.0 +/- 75.0 = [380.0, 530.0]B."
    },
    {
      "kind": "text",
      "text": "Downside risk outside the interval: if the registered October snapshot still misses a large share of late-FY DoD contract or IDV awards because of publication delay, the API obligations field could land below 380B. Upside risk outside the interval: if late-FY contract awards and IDVs post faster than the current latest_action_date pattern, or FY2026 procurement obligations materially exceed the FY2024 scale, the snapshot could land above 530B."
    },
    {
      "kind": "forecast",
      "point": 455,
      "ciLow": 380,
      "ciHigh": 530
    }
  ]
}
