# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usaspending.cdfi.assistance_transaction_obligations
- period: FY2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-cdfi-assistance-transaction-obligations-fy2026"
- country: "US"
- targetUnit: "usd_millions"
- dataPointId: "usaspending.cdfi.assistance_transaction_obligations.fy2026.registered_query_snapshot"
- expectedReleaseWindow: {"end": "2026-10-22", "start": "2026-10-15"}
- sourceBinding: {"adapter": "usaspending-api", "allowedHosts": ["api.usaspending.gov"], "expectedReleaseWindow": {"end": "2026-10-22", "start": "2026-10-15"}, "field": "results[time_period.fiscal_year={fiscal_year}].aggregated_amount", "releasePolicy": "registered_query_snapshot", "sourceSeriesId": "usaspending.search.spending_over_time.cdfi.program_obligations", "sourceUrl": "https://api.usaspending.gov/api/v2/search/spending_over_time/", "table": "USAspending API v2 advanced search, CDFI Fund awarding-subagency financial-assistance award transactions, obligations by fiscal year", "transform": {"agency": {"name": "Community Development Financial Institutions Fund", "tier": "subtier", "type": "awarding"}, "awardTypeCodes": ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11"], "factor": 1e-06, "fiscalYear": "{fiscal_year}", "group": "fiscal_year", "operation": "multiply", "requestMethod": "POST", "spendingLevel": "transactions"}}
- targetRegistrationPath: "records/targets/2026-08-11-6e45cb2f4898f951845f89900e3c0befff43d9dc3bc3a0f7749231020fb88f32.json"
- targetContentHash: "6e45cb2f4898f951845f89900e3c0befff43d9dc3bc3a0f7749231020fb88f32"
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
bd771e5186623caac19e152e6cb6c2a442be589c26fed30770ca2817a6db4369

# Draft forecast response
I’m dropping this cell rather than publishing an ungrounded forecast.

I could not execute the required registered USAspending `POST /api/v2/search/spending_over_time/` query in this environment: local shell commands fail before start with `bwrap: setting up uid map: Permission denied`, and the browser fetch path can only open the endpoint as GET, which returns `405 Method Not Allowed`. USAspending’s docs confirm this endpoint is POST-only and does not require authorization. ([api.usaspending.gov](https://api.usaspending.gov/docs/endpoints)) ([]())

Because the machine-checked target requires historicalContext from the exact registered query, substituting agency-profile totals or remembered values would violate the contract. No JSON cell emitted.
