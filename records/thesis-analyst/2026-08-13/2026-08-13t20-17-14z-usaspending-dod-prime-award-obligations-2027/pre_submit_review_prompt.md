# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.dod.prime_award_obligations
- period: 2027
- conditional: An Act authorizing appropriations for military activities of the Department of Defense for fiscal year 2027 (the FY2027 NDAA; the House-reported bill is H.R. 8800, 119th Congress, House Report 119-698) is enacted into law on or before 2026-12-31.


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-dod-prime-award-obligations-fy2027-fy27-ndaa-enacted"
- country: "US"
- targetUnit: "billions USD"
- dataPointId: "usaspending.dod.prime_award_obligations.2027.registered_query_snapshot.fy27_ndaa_enacted"
- expectedReleaseWindow: {"end": "2027-10-22", "start": "2027-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2027-10-22", "start": "2027-10-15"}, "field": "obligations", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.agency.097.awards.obligations", "sourceUrl": "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year={fiscal_year}", "table": "USAspending API v2, agency 097 (DoD) award summary, prime award obligations, fiscal year to date", "transform": {"factor": 1e-09, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-13-d3e164666cfec76acc158c22d6e10fdb9af935f4eac09a0486ea434862212132.json"
- targetContentHash: "d3e164666cfec76acc158c22d6e10fdb9af935f4eac09a0486ea434862212132"
- registrationCommit: "27d485d528684bbe8281fa349cfbb9587169dd5b"
- registeredAtUtc: "2026-08-13T16:32:19Z"
- conditional: "An Act authorizing appropriations for military activities of the Department of Defense for fiscal year 2027 (the FY2027 NDAA; the House-reported bill is H.R. 8800, 119th Congress, House Report 119-698) is enacted into law on or before 2026-12-31."

# Registered-query series (machine checked)
This series is DEFINED by the registered query in sourceBinding — no published table or headline page exists for it, so agency profile totals and search-result summaries are the WRONG series. Fetch historicalContext by executing the exact registered query for each prior period: substitute each prior period into sourceBinding.sourceUrl ("https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year={fiscal_year}") and GET it, then read the value at sourceBinding.field and apply sourceBinding.transform's operation and factor. History values obtained any other way will fail anchor validation, and a cell without historicalContext fails normalization — if the query cannot be executed, refuse with the fetch evidence rather than omitting history or substituting a broader aggregate.
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
cc8b3673012ffe4bdd6a80be5b55f4ccf224202b1c43aa50eda9707b8f7be942

# Draft forecast response
{
  "slug": "us-dod-prime-award-obligations-fy2027-fy27-ndaa-enacted",
  "country": "US",
  "type": "conditional",
  "title": "DoD FY2027 prime award obligations if FY2027 NDAA enacted",
  "question": "What will USAspending API v2 report for Department of Defense agency 097 prime award obligations for fiscal year 2027, in billions USD, using the registered query snapshot field obligations from the first available FY2027 resolving snapshot?",
  "unit": "billions USD",
  "pointEstimate": 545.3,
  "ciLow": 495.4,
  "ciHigh": 595.2,
  "confidence": 0.8,
  "resolutionDate": "2027-10-22",
  "resolutionSource": "USAspending API v2, agency 097 awards",
  "resolutionSourceUrl": "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2027",
  "resolutionRule": "If the condition is satisfied, on 2027-10-22 fetch USAspending API v2 agency 097 awards with fiscal_year=2027 at https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2027, read JSON field obligations, multiply by 1e-9, and resolve as Department of Defense prime award obligations for fiscal year 2027 in billions USD under registered_query_snapshot releasePolicy. Use the first registered query snapshot; later corrections or changes are irrelevant. Round to the nearest 0.1 billion USD. If the condition is not satisfied, mark the cell unresolved.",
  "dataPointId": "usaspending.dod.prime_award_obligations.2027.registered_query_snapshot.fy27_ndaa_enacted",
  "conditionalOn": "An Act authorizing appropriations for military activities of the Department of Defense for fiscal year 2027 (the FY2027 NDAA; the House-reported bill is H.R. 8800, 119th Congress, House Report 119-698) is enacted into law on or before 2026-12-31.",
  "historicalContext": [
    {
      "label": "USAspending agency 097 obligations FY2023, billions USD",
      "value": 467.3
    },
    {
      "label": "USAspending agency 097 obligations FY2024, billions USD",
      "value": 456.9
    },
    {
      "label": "USAspending agency 097 obligations FY2025, billions USD",
      "value": 501.5
    }
  ],
  "drivers": [
    "completed FY2016-FY2025 upward trend",
    "FY2025 registered-query high print",
    "timely NDAA condition supports normal award cycle",
    "FY2026 still incomplete at run date",
    "large annual obligation volatility"
  ],
  "sourceContext": [
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2016",
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2017",
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2018",
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2019",
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2020",
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2021",
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2022",
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2023",
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2024",
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2025",
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2026",
    "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year=2027"
  ],
  "runAt": "2026-08-13T20:17:30Z",
  "activityLog": [],
  "reasoning": [
    {
      "kind": "heading",
      "text": "Registered USAspending FY2027 DoD Prime Award Obligations"
    },
    {
      "kind": "text",
      "text": "The target is the registered USAspending API v2 query for agency 097, field obligations, transformed by 1e-9 into billions USD. The ledger commits resolutionDate 2027-10-22, matching the end of the expected release window 2027-10-15 to 2027-10-22. The slug was checked against app.thesisinstitute.org/specs.json in this run and no duplicate published slug was returned by the local match command."
    },
    {
      "kind": "tool",
      "tool": "shell.curl",
      "call": "GET registered sourceBinding URL for FY2016-FY2020",
      "result": "USAspending agency 097 awards obligations fetched this run: FY2016 obligations=304733246938.93, FY2017 obligations=327990949917.96, FY2018 obligations=365937501255.11, FY2019 obligations=391333992872.89, FY2020 obligations=431883672152.30; transformed by 1e-9 gives 304.733, 327.991, 365.938, 391.334, 431.884 billions USD."
    },
    {
      "kind": "tool",
      "tool": "shell.curl",
      "call": "GET registered sourceBinding URL for FY2021-FY2025",
      "result": "USAspending agency 097 awards obligations fetched this run: FY2021 obligations=395332709399.53, FY2022 obligations=424512414112.80, FY2023 obligations=467273435599.16, FY2024 obligations=456945504400.91, FY2025 obligations=501543513238.03; transformed by 1e-9 gives 395.333, 424.512, 467.273, 456.946, 501.544 billions USD."
    },
    {
      "kind": "tool",
      "tool": "shell.curl",
      "call": "GET registered sourceBinding URL for FY2026 and FY2027 resolver-state check",
      "result": "USAspending agency 097 awards query fetched this run returned FY2026 obligations=298980123138.95, transformed to 298.980 billions USD, but FY2026 is incomplete on 2026-08-13. FY2027 query returned error detail: Field fiscal_year value 2027 is above max 2026."
    },
    {
      "kind": "text",
      "text": "Base rate / reference class: completed FY2016-FY2025 registered-query obligations have mean 406.7B, range 304.7B to 501.5B, and last completed print 501.5B. Successive completed annual changes are +23.3B, +37.9B, +25.4B, +40.5B, -36.6B, +29.2B, +42.8B, -10.3B, and +44.6B, with mean +21.9B, sigma 27.6B, and range -36.6B to +44.6B. Last-print persistence benchmark for FY2027 is 501.5B; the mean-change trend benchmark is 501.5 + 2*21.9 = 545.3B because FY2026 is not yet a completed print."
    },
    {
      "kind": "text",
      "text": "Model candidates under thesis_model_candidate_v1, train cutoff FY2025 completed registered query: persistence candidate point=501.5B, p10=451.6B, p50=501.5B, p90=551.4B, 80% interval 451.6B-551.4B, 90% interval 431.0B-572.0B, interval_method=annual-change residual sigma over FY2016-FY2025, calibration_n=9, one-step walk-forward MAE=33.4B. Mean-change trend candidate point=545.3B, p10=495.4B, p50=545.3B, p90=595.2B, 80% interval 495.4B-595.2B, 90% interval 463.1B-627.5B, interval_method=two-year annual-change residual sigma sqrt-horizon, calibration_n=9, one-step walk-forward MAE=24.1B. The trend candidate beats persistence in backtest and is selected."
    },
    {
      "kind": "math",
      "text": "Prior/update/interval: prior = mean-change trend candidate from completed FY2016-FY2025 registered-query history; historical sample = 10 completed values and 9 annual changes. Adjustment components: +0.0B for current FY2026 partial print because it is not a comparable completed fiscal-year snapshot; +0.0B for the NDAA mechanism because the forecast is conditional on enactment by 2026-12-31 and no separate numeric appropriation-to-prime-award conversion fetched this run clears the update test. Point = FY2025 501.5B + 2*(mean annual change 21.9B) = 545.3B. Interval method = annual-change residual, two-year horizon. sigma = 27.6B from successive completed annual changes; basic half-width = 1.28*sigma = 35.3B; widen by sqrt(2)=1.41 for two fiscal years beyond the last completed print, half-width = 1.28*27.6*1.41 = 49.9B. Implied 80% bounds = 545.3 - 49.9 = 495.4B and 545.3 + 49.9 = 595.2B."
    },
    {
      "kind": "text",
      "text": "Counter-consideration: downside risk outside the interval would come from a prolonged FY2027 continuing resolution, procurement execution delay, or cancellation-driven award slowdown despite the NDAA condition, which would land below 495.4B. Upside risk outside the interval would come from unusually large shipbuilding, aircraft, munitions, or Ukraine/Indo-Pacific supplemental obligations posting into prime awards before the snapshot, which would land above 595.2B."
    },
    {
      "kind": "forecast",
      "point": 545.3,
      "ciLow": 495.4,
      "ciHigh": 595.2
    }
  ]
}
