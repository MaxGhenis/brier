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
5463c0552b4405d16fbdeeaea6a88683ad1e16a0bd1fdadb97feeb9e701cc92f

# Draft forecast response
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"U.S. July 2026 monthly deficit","question":"What will the U.S. Treasury Monthly Treasury Statement Table 1 report as the July 2026 monthly deficit, in nominal USD billions, on its first print?","unit":"usd_billions","pointEstimate":305.455,"ciLow":210,"ciHigh":400,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, divide by 1000 to obtain usd_billions, and report deficits as positive and surpluses as negative. Do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"July 2023 deficit","value":220.782},{"label":"July 2024 deficit","value":243.741},{"label":"July 2025 deficit","value":291.143},{"label":"May 2026 deficit","value":292.648}],"drivers":["July deficits rose from $220.782B in 2023 to $291.143B in 2025","FY2026 spending and interest remain elevated","July tax receipts are seasonally weaker than April receipts","Payment timing can shift tens of billions between adjacent months"],"sourceContext":["https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202501.pdf","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202505.pdf","https://fiscaldata.treasury.gov/release-calendar/"],"runAt":"2026-07-10T21:44:12Z","thresholdLadder":{"thresholds":[170,200,220,240,260,280,300,320,340,360,380,400,430],"cumulativeProbabilities":[0.05,0.08,0.12,0.18,0.26,0.36,0.47,0.58,0.68,0.77,0.84,0.9,0.95]},"reasoning":[{"kind":"heading","text":"July 2026 Monthly Treasury Statement deficit forecast"},{"kind":"text","text":"The target is the first-print July 2026 monthly Deficit/Surplus (-) in MTS Table 1, not the fiscal-year-to-date balance. Table 1 is denominated in $ millions; I divide by 1000 and reverse the table's sign convention so deficits are positive. Later revisions are excluded."},{"kind":"tool","tool":"official.lookup","call":"Read Treasury MTS Table 1 for the July reference class.","result":"Official Table 1 values were July 2023 receipts $276.161B, outlays $496.943B, deficit $220.782B; July 2024 receipts $330.377B, outlays $574.119B, deficit $243.741B; and July 2025 receipts $338.492B, outlays $629.635B, deficit $291.143B."},{"kind":"tool","tool":"official.lookup","call":"Read the May 2026 MTS Table 1 for current-fiscal-year momentum.","result":"FY2026 Table 1 showed May receipts $335.512B, outlays $628.161B, and a $292.648B monthly deficit; FY2026 year-to-date through May was receipts $3,655.648B and outlays $4,901.851B."},{"kind":"tool","tool":"official.calendar","call":"Check the Treasury Fiscal Data release calendar for the July 2026 MTS.","result":"The official release calendar listed the July 2026 Monthly Treasury Statement for 2026-08-17; the dataset notes that MTS publication is normally on the 8th workday after the reporting month."},{"kind":"text","text":"The reference class base rate is the three most recent same-month first prints: $220.782B, $243.741B, and $291.143B. Their upward progression and the $292.648B May 2026 deficit place the central July 2026 mass near $300B rather than near the broader all-month average."},{"kind":"text","text":"Prior/update/interval: I use a recency-weighted same-month persistence prior over the fetched July 2023-2025 sample, anchored by $220.782B and $291.143B. I update upward for higher FY2026 nominal outlays and debt-service pressure, temper that adjustment because receipts have also risen, and allow wide payment-calendar and policy uncertainty. The interval is read from the elicited empirical threshold ladder, yielding final implied 80% bounds of $210.000B to $400.000B."},{"kind":"math","text":"Ladder: P(X <= 170) = 0.05; P(X <= 200) = 0.08; P(X <= 220) = 0.12; P(X <= 240) = 0.18; P(X <= 260) = 0.26; P(X <= 280) = 0.36; P(X <= 300) = 0.47; P(X <= 320) = 0.58; P(X <= 340) = 0.68; P(X <= 360) = 0.77; P(X <= 380) = 0.84; P(X <= 400) = 0.90; P(X <= 430) = 0.95. Linear interpolation gives the 10th percentile at 210.000, median at 305.455, and 90th percentile at 400.000 usd_billions."},{"kind":"text","text":"Upside risk to the deficit comes from accelerated benefit or defense payments, weaker individual-income-tax receipts, larger refunds, or unusually high interest outlays; a combination could land above the interval. Downside risk comes from strong withheld taxes, customs receipts, delayed payments, or unusually large offsetting receipts; a major timing shift could land below the interval."},{"kind":"forecast","point":305.455,"ciLow":210,"ciHigh":400}]}
