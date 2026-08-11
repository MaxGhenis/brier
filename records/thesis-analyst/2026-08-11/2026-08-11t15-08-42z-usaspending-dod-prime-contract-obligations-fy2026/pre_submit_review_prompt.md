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
2ac732fda50583662c37241e51e9458dd65cd2c650ba36e9c5e9650be5274a1d

# Draft forecast response
No compliant cell emitted.

I could not satisfy the analyst contract in this environment because:

- Local command execution fails before running (`bwrap: loopback: Failed RTM_NEWADDR`), so I cannot produce the required `runAt` from `date -u +%Y-%m-%dT%H:%M:%SZ`.
- I could fetch the registered USAspending endpoint’s current FY value: contracts `aggregated_amount = 238,617,208,309.69`, and the API docs confirm this endpoint returns obligations by award category for a requested or current fiscal year. ([api.usaspending.gov](https://api.usaspending.gov/api/v2/agency/097/obligations_by_award_category/))
- I could not vary `fiscal_year` through the available browser tool to fetch the required recent historical reference class from the same resolver.

Under the honesty rules, that is not enough to ground a forecast cell, so I’m dropping the cell rather than inventing history, model candidates, or `runAt`.
