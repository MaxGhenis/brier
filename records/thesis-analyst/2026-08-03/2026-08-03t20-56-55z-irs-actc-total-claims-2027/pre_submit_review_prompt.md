# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: irs.actc.total_claims
- period: 2027
- conditional: Legislation enacted by 2027-12-31 makes the IRC §24(d)(1)(B)(i) earned-income threshold no more than $1 for tax year 2027.


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "additional-child-tax-credit-total-claims-ty2027-threshold-one-dollar"
- country: "US"
- targetUnit: "millions"
- dataPointId: "irs.actc.total_claims.2027.first_print.threshold_one_dollar"
- resolutionDate: "2029-12-31"
- sourceBinding: {"adapter": "irs-soi-pub1304", "allowedHosts": ["www.irs.gov"], "expectedReleaseWindow": {"end": "2029-12-31", "start": "2029-01-01"}, "field": "refundable_child_tax_credit_returns", "releasePolicy": "first_print", "sourceSeriesId": "irs.actc.total_claims", "sourceUrl": "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304", "table": "IRS SOI Individual Income Tax Returns Complete Report (Publication 1304), Table 3.3, all returns total row, refundable child tax credit or additional child tax credit, number of returns", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-03-6978365a2924b850a9516b49451ed3e07b2bb14321ea908344ce17744296f5e6.json"
- targetContentHash: "6978365a2924b850a9516b49451ed3e07b2bb14321ea908344ce17744296f5e6"
- registrationCommit: "a4f59c018641c8d772975263735424cb5d46bb25"
- registeredAtUtc: "2026-08-03T20:13:09Z"
- conditional: "Legislation enacted by 2027-12-31 makes the IRC \u00a724(d)(1)(B)(i) earned-income threshold no more than $1 for tax year 2027."
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
457650e42ee8cdb944e48364dafd23585c4e828ce7fe49d1691908aa51b9b3c1

# Draft forecast response
{
  "error": "forecast_not_produced",
  "reason": "I could not honestly ground the base-rate history required for this cell. The local command runner failed before execution with `bwrap: setting up uid map: Permission denied`, so I could not run `date -u`, inspect the local resolver, download/parse the IRS XLS files, or echo raw `curl` responses as required. The web fetch tool reached the IRS Publication 1304 Table 3.3 index and current-law pages, but it cannot decode the official IRS Excel files that contain the target historical values. Under the supplied honesty rules, I must not substitute remembered or inferred Table 3.3 values.",
  "target": {
    "slug": "additional-child-tax-credit-total-claims-ty2027-threshold-one-dollar",
    "dataPointId": "irs.actc.total_claims.2027.first_print.threshold_one_dollar",
    "unit": "millions",
    "conditionalOn": "Legislation enacted by 2027-12-31 makes the IRC §24(d)(1)(B)(i) earned-income threshold no more than $1 for tax year 2027."
  },
  "sources_reached": [
    "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304",
    "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304-basic-tables-part-3",
    "https://www.irs.gov/credits-deductions/individuals/child-tax-credit"
  ]
}
