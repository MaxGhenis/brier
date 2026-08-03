# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: irs.actc.total_claims
- period: 2027
- conditional: No legislation enacted by 2027-12-31 changes the IRC §24(d)(1)(B)(i) earned-income threshold of $2,500 for tax year 2027; current law holds. The $2,500 operative amount is applied by IRC §24(h)(6), while §24(d)(1)(B)(i) contains the underlying $3,000 amount.


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "additional-child-tax-credit-total-claims-ty2027-current-law"
- country: "US"
- targetUnit: "millions"
- dataPointId: "irs.actc.total_claims.2027.first_print.current_law"
- resolutionDate: "2029-12-31"
- sourceBinding: {"adapter": "irs-soi-pub1304", "allowedHosts": ["www.irs.gov"], "expectedReleaseWindow": {"end": "2029-12-31", "start": "2029-01-01"}, "field": "refundable_child_tax_credit_returns", "releasePolicy": "first_print", "sourceSeriesId": "irs.actc.total_claims", "sourceUrl": "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304", "table": "IRS SOI Individual Income Tax Returns Complete Report (Publication 1304), Table 3.3, all returns total row, refundable child tax credit or additional child tax credit, number of returns", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-03-750dfdf6ca78138736340c8c49dc41d3810bd19e710ea3bd16f3a316b62a0bc2.json"
- targetContentHash: "750dfdf6ca78138736340c8c49dc41d3810bd19e710ea3bd16f3a316b62a0bc2"
- registrationCommit: "966f199f95948a7544dae5ba2f4b7101643a311f"
- registeredAtUtc: "2026-08-03T02:32:28Z"
- conditional: "No legislation enacted by 2027-12-31 changes the IRC \u00a724(d)(1)(B)(i) earned-income threshold of $2,500 for tax year 2027; current law holds. The $2,500 operative amount is applied by IRC \u00a724(h)(6), while \u00a724(d)(1)(B)(i) contains the underlying $3,000 amount."
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
210778c13b27840cb3d620174cc196481c47fa37c0f8184d886c5d060362dd24

# Draft forecast response
{
  "status": "dropped",
  "dataPointId": "irs.actc.total_claims.2027.first_print.current_law",
  "catalogSlug": "additional-child-tax-credit-total-claims-ty2027-current-law",
  "reason": "I could not honestly produce a forecast cell because the required official base-rate history could not be fetched and echoed this run. Local shell commands failed before execution with `bwrap: setting up uid map: Permission denied`, so I could not `curl` and parse the IRS XLS files. The web tool could inspect the IRS index/PDF pages, but the IRS Table 3.3 XLS files needed for 6-24 comparable first-print ACTC claim counts were unsupported as Excel content. I did fetch one official 2022 line-item excerpt showing Schedule 8812 ACTC line 27 count 17,219,508 and amount 32,036,369 thousand dollars, but that is not enough to size the required base-rate interval.",
  "partialSourcesFetched": [
    {
      "name": "IRS SOI Publication 1304 Basic Tables Part 3 index",
      "url": "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304-basic-tables-part-3",
      "usedFor": "Confirmed Table 3.3 XLS links exist for 2023 back through earlier tax years."
    },
    {
      "name": "IRS Publication 4801 Rev. 12-2024, 2022 Individual Income Tax Returns Line Item Estimates",
      "url": "https://www.irs.gov/pub/irs-prior/p4801--122024.pdf",
      "usedFor": "Fetched official 2022 Schedule 8812 ACTC line 27 count and amount excerpt."
    },
    {
      "name": "26 USC 24 preliminary/current-law text",
      "url": "https://uscode.house.gov/view.xhtml?edition=prelim&req=granuleid%3AUSC-prelim-title26-section24",
      "usedFor": "Confirmed IRC section 24(h)(6) substitutes $2,500 for $3,000."
    }
  ],
  "runAt": "2026-08-03T00:00:00Z",
  "agent": "thesis.analyst",
  "agentVersion": "v2.4.0",
  "promptHash": "7ef119647b35",
  "toolsHash": "50a06b62f9be"
}
