# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.dod.prime_award_obligations
- period: FY2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
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
c563dc57e89d66f528402af4e6ce0d1b474708e656e521f9790a5cf923161397

# Draft forecast response
{
  "slug": "us-dod-prime-award-obligations-fy2026",
  "country": "US",
  "type": "data",
  "title": "DoD prime award obligations, FY2026",
  "question": "What will USAspending API v2 report for Department of Defense agency 097 prime award obligations for fiscal year 2026, in billions of dollars, using the registered query snapshot and first available registered snapshot policy?",
  "unit": "usd_billions",
  "pointEstimate": 550,
  "ciLow": 485,
  "ciHigh": 615,
  "confidence": 0.8,
  "resolutionDate": "2026-10-22",
  "resolutionSource": "USAspending API v2, agency 097 award summary",
  "resolutionSourceUrl": "https://api.usaspending.gov/api/v2/agency/097/awards/?fiscal_year={fiscal_year}",
  "resolutionRule": "Resolve from USAspending API v2 endpoint /api/v2/agency/097/awards/?fiscal_year=2026, field obligations, for Department of Defense top-tier agency code 097. Use the registered query snapshot policy, multiply obligations dollars by 1e-9, and round to billions USD. Later API changes after the registered snapshot are irrelevant.",
  "dataPointId": "usaspending.dod.prime_award_obligations.fy2026.registered_query_snapshot",
  "historicalContext": [
    {
      "label": "USAspending-derived mirror snapshot, earlier crawl current total",
      "value": 129.7
    },
    {
      "label": "USAspending-derived mirror snapshot, mid crawl current total",
      "value": 148.6
    },
    {
      "label": "USAspending-derived mirror snapshot, later crawl current total",
      "value": 212.9
    },
    {
      "label": "USAspending-derived mirror snapshot, later crawl current total",
      "value": 217.9
    },
    {
      "label": "USAspending-derived mirror snapshot, late crawl current total",
      "value": 245.1
    },
    {
      "label": "USAspending-derived mirror snapshot, latest inspected current total",
      "value": 246.7
    }
  ],
  "drivers": [
    "FY2026 DoD budget materially above FY2025",
    "large acquisition and O&M funding base",
    "DoD award data lag creates snapshot risk",
    "late fiscal-year procurement surge",
    "current USAspending-derived snapshots still below full-year pace"
  ],
  "sourceContext": [
    "https://api.usaspending.gov/docs/endpoints",
    "https://www.usaspending.gov/agency/department-of-defense",
    "https://app.g2xchange.com/agencies/9748",
    "https://g2xchange.com/app/agencies/97CY",
    "https://www.cbo.gov/publication/62396",
    "https://www.congress.gov/crs-product/R44027",
    "https://app.thesisinstitute.org/specs.json"
  ],
  "runAt": "2026-08-11T15:03:48Z",
  "activityLog": [],
  "reasoning": [
    {
      "kind": "heading",
      "text": "DoD FY2026 Prime Award Obligations Forecast"
    },
    {
      "kind": "text",
      "text": "Framing: the registered target is USAspending agency 097 prime award obligations for FY2026. The target context gives an expectedReleaseWindow ending 2026-10-22; I use that lab-committed bound as resolutionDate and keep the registered URL template unchanged. The ledger targetUnit is billions USD, represented in the contract as usd_billions."
    },
    {
      "kind": "tool",
      "tool": "usaspending.api.docs",
      "call": "Open USAspending API endpoint documentation and the agency awards endpoint description.",
      "result": "Fetched USAspending API docs: endpoints do not require authorization; /api/v2/agency/<TOPTIER_AGENCY_CODE>/awards/ returns agency award summary information including transaction_count and obligations. The browsable example response carried fiscal_year=2026, transaction_count=1611371, obligations=146176922599.78 for agency 012."
    },
    {
      "kind": "tool",
      "tool": "web.search.usaspending_mirror_snapshots",
      "call": "Search public USAspending-derived agency pages for current DoD award totals and subagency breakdowns.",
      "result": "Fetched USAspending-derived public snippets with current totals: 129,709,702,780; 148,551,377,687; 212,895,410,643; 217,858,434,553; 245,069,031,666; and 246,670,846,817 dollars across DoD-associated pages."
    },
    {
      "kind": "tool",
      "tool": "web.search.subagency_breakdown",
      "call": "Inspect latest DoD subagency breakdown in the public USAspending-derived snippets.",
      "result": "Latest inspected current total was 246,670,846,817 dollars; listed components included Department of the Navy 72,149,134,174, Department of the Air Force 57,590,357,180, and Department of the Army 53,792,358,774 dollars."
    },
    {
      "kind": "tool",
      "tool": "cbo.defense_budget",
      "call": "Fetch public FY2026 DoD budget context from CBO and Defense Department summaries.",
      "result": "CBO/DoD budget context fetched: DoD FY2026 request totaled 961.6 billion dollars; CBO reported total FY2026 acquisition funding of 384 billion dollars and operation/support funding of 558 billion dollars; DoD described the FY2026 request as 13.4 percent above FY2025."
    },
    {
      "kind": "tool",
      "tool": "crs.usaspending_timing",
      "call": "Fetch public USAspending timing caveat for DoD award data.",
      "result": "CRS/USAspending timing context fetched: federal award transactions generally report within 30 days, while Department of Defense data may have a longer lag, generally 90 days."
    },
    {
      "kind": "text",
      "text": "Base rate / reference class: the inspected USAspending-derived current snapshots ranged from 129.7 to 246.7 billion dollars, with the latest inspected value at 246.7. That is not a full-year final; it is the pre-resolution running stock. The base-rate prior is therefore current-run persistence adjusted to a fiscal-year snapshot, not the raw 246.7 value."
    },
    {
      "kind": "text",
      "text": "Model candidates under thesis_model_candidate_v1, stated compactly: persistence candidate point 246.7, p10 215, p50 246.7, p90 280, interval_method snapshot empirical, calibration_n 6, train cutoff latest inspected mirror snapshot, rejected because the resolver is the FY2026 registered snapshot after fiscal-year close; budget-scaled candidate point 550, p10 485, p50 550, p90 615, interval_method widened snapshot-change residual, calibration_n 6, train cutoff latest inspected mirror snapshot, selected because FY2026 DoD funding and late fiscal-year award flow imply a much larger post-close snapshot than current YTD mirror persistence."
    },
    {
      "kind": "math",
      "text": "Snapshot changes in billions were 18.8, 64.3, 5.0, 27.2, and 1.6; their sample dispersion is about 25.1. For a post-close registered snapshot with DoD delay and late-year procurement concentration, I widen to sigma = 50.8. Half-width = 1.28*sigma = 65.0. Point = 550 based on budget-scaled snapshot prior; 80% interval = 550 - 65 to 550 + 65 = 485 to 615."
    },
    {
      "kind": "math",
      "text": "Prior/update/interval: prior = budget-scaled current USAspending-derived snapshot, historical sample = six inspected DoD current-total snapshots from 129.7 to 246.7 billion dollars plus FY2026 DoD budget context of 961.6 billion dollars total and 384 billion dollars acquisition funding; adjustment components = upward late-fiscal-year award flow and FY2026 defense funding increase, partially offset by 90-day DoD reporting lag; interval method = widened snapshot-change residual with sigma = 50.8 and half-width roughly 1.28*sigma = 65.0, implying bounds 485 and 615."
    },
    {
      "kind": "text",
      "text": "Counter-consideration: downside risk would land below the interval if the October registered API snapshot still excludes most late-FY DoD contract actions because of the 90-day delay or if award obligations are shifted into account spending not captured by prime awards. Upside risk would land above the interval if reconciliation-funded acquisition and shipbuilding obligations hit USAspending before the snapshot or if a large September obligation wave is visible earlier than usual."
    },
    {
      "kind": "forecast",
      "point": 550,
      "ciLow": 485,
      "ciHigh": 615
    }
  ]
}
