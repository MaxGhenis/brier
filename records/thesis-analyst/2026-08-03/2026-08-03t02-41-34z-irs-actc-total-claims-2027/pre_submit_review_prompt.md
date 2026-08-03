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
- targetRegistrationPath: "records/targets/2026-08-03-e1e24629b485515d803523111d9d5866c88fcbee6e13d0b33a3599e9c15011df.json"
- targetContentHash: "e1e24629b485515d803523111d9d5866c88fcbee6e13d0b33a3599e9c15011df"
- registrationCommit: "966f199f95948a7544dae5ba2f4b7101643a311f"
- registeredAtUtc: "2026-08-03T02:32:28Z"
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
6f55fec6869afe934a5aebced76bad799bba230fd59d3f3b420ae01c416ec49c

# Draft forecast response
I can’t produce a valid Thesis forecast cell for this run.

The official IRS Publication 1304 page and Table 3.3 XLS links are available, and IRS says the TY2023 Pub 1304 tables were released in March 2026, but the available browsing layer would not parse the XLS/CSV files containing the ACTC count values. ([irs.gov](https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304-basic-tables-part-3)) The local shell also failed before running even `date -u`, so I could not satisfy the required `runAt` rule or echo raw fetched table excerpts.

Per the harness honesty rule, I’m stopping rather than substituting remembered or inferred ACTC history. No forecast cell emitted.
