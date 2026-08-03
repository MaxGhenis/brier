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
- targetRegistrationPath: "records/targets/2026-08-03-b92e9752beaf38a9e2e735c5066e7c741e29436546e7fab2c8d0568f05355909.json"
- targetContentHash: "b92e9752beaf38a9e2e735c5066e7c741e29436546e7fab2c8d0568f05355909"
- registrationCommit: "a4f59c018641c8d772975263735424cb5d46bb25"
- registeredAtUtc: "2026-08-03T20:13:09Z"
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
ac0a4ac28aa24f57de9d5ca8e231680b9520e01f44b886847c925b63dbd2ad31

# Draft forecast response
{
  "slug": "additional-child-tax-credit-total-claims-ty2027-current-law",
  "country": "US",
  "type": "conditional",
  "title": "ACTC total claims, TY2027 current law",
  "question": "What will IRS SOI Publication 1304, Table 3.3, all returns total row, report as the number of returns claiming the refundable child tax credit or additional child tax credit for tax year 2027, first print, under the stated current-law condition?",
  "unit": "millions",
  "pointEstimate": 19.4,
  "ciLow": 17.6,
  "ciHigh": 21.3,
  "confidence": 0.8,
  "resolutionDate": "2029-12-31",
  "resolutionSource": "Internal Revenue Service, SOI Individual Income Tax Returns Complete Report Publication 1304",
  "resolutionSourceUrl": "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304",
  "resolutionRule": "Resolve from the first print of IRS SOI Individual Income Tax Returns Complete Report Publication 1304 for tax year 2027, Table 3.3, All Returns: Tax Liability, Tax Credits, and Tax Payments, all returns total row, refundable child tax credit or additional child tax credit, number of returns. Divide the raw number of returns by 1,000,000 and report in millions. Later revisions are ignored. The registered ledger sourceBinding uses adapter irs-soi-pub1304, sourceSeriesId irs.actc.total_claims, field refundable_child_tax_credit_returns, releasePolicy first_print, and transform multiply by 1e-06. If the conditional event fails, leave unresolved.",
  "dataPointId": "irs.actc.total_claims.2027.first_print.current_law",
  "conditionalOn": "No legislation enacted by 2027-12-31 changes the IRC §24(d)(1)(B)(i) earned-income threshold of $2,500 for tax year 2027; current law holds. The $2,500 operative amount is applied by IRC §24(h)(6), while §24(d)(1)(B)(i) contains the underlying $3,000 amount.",
  "historicalContext": [
    {
      "label": "TY2016 ACTC claims, IRS Table 3.3 extract",
      "value": 18.9
    },
    {
      "label": "TY2017 ACTC claims, IRS Table 3.3 extract",
      "value": 17.522
    },
    {
      "label": "TY2020 ACTC claims, IRS Table A extract",
      "value": 19.1
    }
  ],
  "drivers": [
    "last comparable ACTC claims near 19 million",
    "2027 current law keeps $2,500 earned-income threshold",
    "ACTC refundable cap is $1,700 under post-2025 law",
    "Puerto Rico ACTC filing rules broaden post-2021",
    "child population and filing compliance drift modestly"
  ],
  "sourceContext": [
    "https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304",
    "https://www.irs.gov/downloads/irs-soi?page=7",
    "https://www.irs.gov/irm/part3/irm_03-038-147r",
    "https://www.irs.gov/credits-deductions/individuals/child-tax-credit",
    "https://taxfoundation.org/data/all/federal/irs-form-1040-income-tax-credits/",
    "https://taxfoundation.org/research/all/federal/family-provisions-in-the-new-tax-code/",
    "https://www.congress.gov/crs-product/R41873"
  ],
  "runAt": "2026-08-03T20:21:19Z",
  "reasoning": [
    {
      "kind": "heading",
      "text": "ACTC total claims, tax year 2027"
    },
    {
      "kind": "text",
      "text": "The ledger target fixes the slug, unit, dataPointId, first-print resolver, and resolutionDate. I found a discrepancy in live release-date verification: IRS pages currently expose TY2023 Publication 1304 tables and the SOI directory, but not a tax-year 2027 Publication 1304 calendar date. I therefore keep the registered 2029-12-31 resolutionDate and treat it as the ledger's expected-window endpoint."
    },
    {
      "kind": "tool",
      "tool": "irs.pub1304.index",
      "call": "Opened IRS Publication 1304 page and Table 3.3 listing.",
      "result": "IRS Publication 1304 page says Table A covers tax years 1990-2023 XLS; Table 3.3 is 'All Returns: Tax Liability, Tax Credits, and Tax Payments' by size of AGI; the Table 3.3 row lists 2023 XLS, 2022 XLS, 2021 XLS, 2020 XLS, 2019 XLS, 2018 XLS, 2017 XLS, 2016 XLS, and earlier years. Page last reviewed/updated 2026-03-27 on the table index and 2026-07-22 on the main Publication 1304 page."
    },
    {
      "kind": "tool",
      "tool": "irs.soi_directory",
      "call": "Opened IRS /downloads/irs-soi directory excerpt for current table files.",
      "result": "IRS directory showed 23in33ar.xls dated 2026-03-26 07:11:00 with size 103 KB for TY2023 Table 3.3 all returns; 23intaba.xls dated 2026-03-26 07:11:08 with size 437 KB for TY2023 Table A; adjacent Table 3.3 component files included 23in33ci.xls 252.5 KB and 23in33cv.xls 111.5 KB."
    },
    {
      "kind": "tool",
      "tool": "irs.irm_law_context",
      "call": "Fetched IRS IRM child-credit processing excerpts and IRS child tax credit page.",
      "result": "IRS IRM 3.38.147 reports maximum refundable ACTC per qualifying child: 2022 = $1,500, 2023 = $1,600, 2024 and later = $1,700. IRS child tax credit page reviewed 2026-06-28 states the Child Tax Credit is up to $2,200 per qualifying child, ACTC up to $1,700 per qualifying child, and earned income must be at least $2,500 to be eligible for ACTC."
    },
    {
      "kind": "tool",
      "tool": "public_extracts.of_irs_tables",
      "call": "Inspected public extracts that cite IRS SOI Table 3.3 and Table A where the browser could not parse XLS binaries.",
      "result": "Tax Foundation extract citing IRS Table 3.3 reports TY2016 ACTC claims of more than 18.9 million and TY2017 total ACTC claims of 17,522,252. Tax Foundation extract citing IRS SOI Table A reports TY2020 Additional Child Tax Credit claims of 19.1 million and amount $33.70 billion. A public extract of IRS Complete Report 2022 reports refundable child tax credit or additional child tax credit amount of $34,843 million for TY2022, but it did not expose the claims count."
    },
    {
      "kind": "text",
      "text": "Base-rate/reference class: I used comparable non-ARPA ACTC claim-count points where the number of returns was exposed: TY2016 18.9 million, TY2017 17.522 million, and TY2020 19.1 million. Mean = 18.507 million, median = 18.9 million, range = 17.522-19.1 million. The 2021 fully refundable/advance CTC year is structurally non-comparable, and the available TY2022 excerpt exposed amount ($34.843 billion) but not the count."
    },
    {
      "kind": "tool",
      "tool": "model_candidates.local",
      "call": "Constructed thesis_model_candidate_v1-style candidates from fetched comparable count history.",
      "result": "persistence candidate: point 19.1, p10 17.8, p50 19.1, p90 20.4, 80% interval 17.8-20.4, 90% interval 17.5-20.9, interval_method='empirical comparable-history widened', calibration_n=3, train_cutoff='TY2020', walk_forward_score='not enough comparable post-TCJA non-ARPA count points'. drift/current-law candidate: point 19.4, p10 17.6, p50 19.4, p90 21.3, 80% interval 17.6-21.3, 90% interval 17.2-21.8, interval_method='persistence plus law/demographic widening', calibration_n=3, train_cutoff='TY2020 plus 2026 current-law parameters'."
    },
    {
      "kind": "math",
      "text": "Prior = last comparable ACTC claims, TY2020 = 19.1 million. Current-law update: +0.2 million for higher post-2025 CTC/ACTC parameters ($2,200 CTC and $1,700 ACTC versus $2,000/$1,400 in TY2020) because more low-tax-liability filers can have a refundable portion; +0.1 million for Puerto Rico and filing-rule inclusion changes after 2021; 0.0 million for the $2,500 threshold because the conditional explicitly keeps it unchanged. Point = 19.1 + 0.2 + 0.1 = 19.4 million. Interval: comparable-history range 17.522-19.1 is too narrow for a 2027 policy-parameter forecast; widen lower side by 0.1 million and upper side by 2.2 million for law take-up, Puerto Rico take-up, child-population, filing compliance, and late-processing uncertainty, giving 17.6-21.3 million. Rounded to 0.1 million."
    },
    {
      "kind": "text",
      "text": "Prior/update/interval: prior is last-print persistence from TY2020 ACTC claims of 19.1 million, checked against a three-point comparable sample of TY2016 18.9, TY2017 17.522, and TY2020 19.1 million. Adjustments are +0.2 for the permanently larger $2,200/$1,700 CTC/ACTC parameters and +0.1 for Puerto Rico/filing-rule inclusion, with no threshold adjustment because the conditional keeps $2,500. Interval method is empirical comparable-history range widened for 2027 law and filing uncertainty, implying bounds 17.6-21.3 million."
    },
    {
      "kind": "text",
      "text": "Counter-consideration: outcome would fall below 17.6 million if child-eligible filing falls materially, SSN/taxpayer-ID enforcement removes more claims than recent history suggests, or high employment/tax liability shifts families from ACTC to nonrefundable CTC. It would exceed 21.3 million if IRS outreach and Puerto Rico filing uptake expand substantially, if low-income families file at much higher rates, or if the enlarged credit causes many more returns to have unused CTC converted into ACTC."
    },
    {
      "kind": "forecast",
      "point": 19.4,
      "ciLow": 17.6,
      "ciHigh": 21.3
    }
  ]
}
