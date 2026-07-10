# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: treasury.mts.monthly_deficit
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-mts-deficit-july-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "treasury.mts.monthly_deficit.july_2026.first_print"
- resolutionDate: "2026-08-17"
- resolutionSource: "U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1"
- resolutionSourceUrl: "https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/"
- resolutionRule: "Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, convert to usd_billions by dividing by 1000, and keep deficits positive and surpluses negative. Do not revise for later MTS revisions or corrected historical tables."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["fiscaldata.treasury.gov"], "expectedReleaseWindow": {"end": "2026-08-17", "start": "2026-08-09"}, "field": "treasury.mts.monthly_deficit", "releasePolicy": "first_print", "sourceSeriesId": "treasury.mts.monthly_deficit", "sourceUrl": "https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/", "table": "U.S. Department of the Treasury, Monthly Treasury Statement (Table 1)", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-ccce2d4ba13735bf7cf54d29cec40a578718bf06407927c523573dd505f8a3f5.json"
- targetContentHash: "ccce2d4ba13735bf7cf54d29cec40a578718bf06407927c523573dd505f8a3f5"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"
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
897b48ec36dc71f6796d3e4e3953a33e1a64a737e074117e0454667e6d3970ef

# Draft forecast response
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"US July 2026 monthly budget deficit","question":"U.S. Department of the Treasury Monthly Treasury Statement Table 1, July 2026 monthly Deficit/Surplus (-), first print","unit":"usd_billions","pointEstimate":303,"ciLow":251,"ciHigh":355,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, convert to usd_billions by dividing by 1000, and keep deficits positive and surpluses negative. Do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"July 2025 deficit, USD billions","value":291},{"label":"July 2024 deficit, USD billions","value":243.741},{"label":"July 2023 deficit, USD billions","value":220.782},{"label":"July 2022 deficit, USD billions","value":211.052},{"label":"July 2021 deficit, USD billions","value":302.05}],"drivers":["July’s recurring deficit-month seasonality","Higher baseline outlays, including interest and mandatory programs","Customs-duty receipts partly offsetting higher outlays","Monthly timing and payment-date variation"],"sourceContext":["https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202507.pdf","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202407.pdf","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202306.pdf"],"runAt":"2026-07-10T15:33:49Z","reasoning":[{"kind":"heading","text":"July 2026 Monthly Treasury Statement deficit"},{"kind":"text","text":"The target is the first-print July 2026 monthly flow in Treasury MTS Table 1, “Deficit/Surplus (-),” reported in $ millions and converted to positive USD billions for a deficit. This uses the unsmoothed, non-seasonally-adjusted Table 1 monthly variant; it is not the fiscal-year-to-date balance, receipts, outlays, or a revised vintage."},{"kind":"tool","tool":"official.lookup","call":"Fetched the Treasury MTS Table 1 July 2025 report for the latest same-month official reference observation.","result":"Treasury Table 1 reports July 2025 receipts of $339,293 million, outlays of $630,376 million, and a monthly deficit of $291,083 million (291.083 USD billions)."},{"kind":"tool","tool":"official.lookup","call":"Fetched Treasury MTS Table 1 historical July observations from published statements for the same monthly deficit concept.","result":"Treasury Table 1 reports July deficits of $211,052 million in 2022, $220,782 million in 2023, and $243,741 million in 2024; the July 2021 comparison is $302,050 million."},{"kind":"tool","tool":"official.lookup","call":"Checked the official Treasury MTS release schedule for the registered July 2026 statement date.","result":"The Treasury schedule assigns the July 2026 MTS first print to August 17, 2026; the statement is scheduled for 2:00 p.m., and the target resolves on that initial official print."},{"kind":"text","text":"The reference class is the non-pandemic July Table 1 deficit flow: July has been a deficit month in 68 of 70 fiscal years in Treasury’s historical note. The 2021–25 same-month values provide a more relevant base rate than adjacent months because July cash timing is strongly seasonal."},{"kind":"text","text":"Prior/update/interval: The persistence prior is the 2021–25 July Table 1 sample (302.050, 211.052, 220.782, 243.741, 291.083 USD billions), with mean 253.742; the latest 291.083 level and continuing outlay growth shift that prior upward, while stronger customs receipts partly offset it. For this flow series, sigma = 41.0 USD billions from the values themselves; 1.28*sigma = 52.5 USD billions, so the implied 80% bounds around 303 are 250.5 and 355.5, rounded to 251 and 355."},{"kind":"math","text":"Point forecast = 291.083 latest July level + 20.0 higher baseline outlays − 8.1 additional customs-receipt offset = 302.983, rounded to 303 USD billions. Interval = 303 ± (1.28 × 41.0) = 303 ± 52.5, rounded to [251, 355]."},{"kind":"text","text":"Upside risk: unexpectedly large mandatory-program, interest, or payment-timing outlays would land above the interval. Downside risk: customs receipts or delayed outlays could make the deficit materially smaller; a combination of unusually strong receipts and shifted payments would land below the interval."},{"kind":"forecast","point":303,"ciLow":251,"ciHigh":355}]}
