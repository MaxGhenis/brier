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
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"U.S. MTS July 2026 Deficit","question":"What will the U.S. Department of the Treasury first report as the Monthly Treasury Statement Table 1 monthly Deficit/Surplus (-) for July 2026, converted to billions of dollars with deficits positive?","unit":"usd_billions","pointEstimate":270.0,"ciLow":201.1,"ciHigh":358.0,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, convert to usd_billions by dividing by 1000, round the forecast cell to one decimal billion dollars, and keep deficits positive and surpluses negative. Do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"july_2025_deficit","value":291.0},{"label":"july_2024_deficit","value":244.0},{"label":"july_2023_deficit","value":220.8},{"label":"july_2022_deficit","value":211.1},{"label":"fy2025_deficit","value":1775.0}],"drivers":["July is usually a deficit month after June tax-payment strength fades","recent July deficits clustered around roughly $210 billion to $291 billion","higher customs duties raise receipts relative to pre-2025 history","interest, Social Security, Medicare, defense, and enacted tax-policy costs keep outlays high","first-print monthly cash timing can move the print by tens of billions"],"sourceContext":["https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","https://www.fiscal.treasury.gov/reports-statements/mts/","https://apnews.com/article/992949ccc115fddbf3838a6213cf2c94","https://www.cbo.gov/"],"runAt":"2026-07-10T21:21:54Z","thresholdLadder":{"thresholds":[170,190,210,230,250,270,290,310,330,350,370,400],"cumulativeProbabilities":[0.04,0.075,0.12,0.20,0.34,0.50,0.64,0.74,0.82,0.88,0.93,0.97]},"reasoning":[{"kind":"heading","text":"U.S. Monthly Treasury Statement July 2026 Deficit Forecast"},{"kind":"text","text":"Framing: the resolver is the first-print U.S. Treasury Monthly Treasury Statement Table 1 monthly Deficit/Surplus (-) for July 2026, in the same monthly, not fiscal-year-to-date, nominal cash-budget variant. The official release calendar identifies the July 2026 MTS release date as 2026-08-17, and the target uses the first print with no later revisions."},{"kind":"tool","tool":"official.lookup","call":"Treasury Monthly Treasury Statement Table 1 history for July monthly Deficit/Surplus (-), converted from $ millions to usd_billions and sign-flipped so deficits are positive","result":"Fetched July deficits: 2025 = 291.0, 2024 = 244.0, 2023 = 220.8, 2022 = 211.1, 2021 = 302.1 usd_billions."},{"kind":"tool","tool":"official.lookup","call":"Treasury/AP public report cross-check for July 2025 MTS monthly receipts, outlays, and deficit","result":"Fetched July 2025 monthly deficit = 291.0 usd_billions, receipts about 338.0 usd_billions, outlays about 629.0 usd_billions, and reported year-over-year deficit increase about 20%."},{"kind":"tool","tool":"official.lookup","call":"Treasury final Monthly Treasury Statement fiscal-year totals used only as fiscal backdrop, not as the monthly target","result":"Fetched FY2025 final totals: receipts = 5235.0 usd_billions, outlays = 7010.0 usd_billions, deficit = 1775.0 usd_billions; FY2024 deficit reference = 1833.0 usd_billions."},{"kind":"text","text":"Reference class/base rate: recent official July MTS prints put the normal range near the low-$200 billions through low-$300 billions, with 2025 at 291.0 and 2021 at 302.1 showing that a July deficit around or above $300 billion is plausible without a crisis, while 2022-2024 anchor the lower-to-middle band."},{"kind":"text","text":"Prior/update/interval: I start from a persistence prior centered between the recent July sample median and the latest July print, using the fetched July 2022-2025 values of 211.1, 220.8, 244.0, and 291.0 plus the 2021 high of 302.1 to anchor the rung span. I adjust downward from 2025 for stronger tariff/customs receipts, then upward for higher interest and mandatory outlays and tax-policy deficit pressure. The interval method is the threshold ladder below, yielding final implied 80% bounds of 201.1 to 358.0."},{"kind":"text","text":"Upside risk for the deficit is a July outlay bulge from interest, defense, Medicare, or benefit timing that pushes the print toward the 330-370 range. Downside risk is customs receipts and delayed outlays holding the deficit near 200-230. A major calendar shift or unusually large one-off payment would land outside the interval, above 358.0 if outlays bunch heavily or below 201.1 if receipts are unusually strong and payments slip."},{"kind":"math","text":"Ladder: P(X <= 170) = 0.04; P(X <= 190) = 0.075; P(X <= 210) = 0.12; P(X <= 230) = 0.20; P(X <= 250) = 0.34; P(X <= 270) = 0.50; P(X <= 290) = 0.64; P(X <= 310) = 0.74; P(X <= 330) = 0.82; P(X <= 350) = 0.88; P(X <= 370) = 0.93; P(X <= 400) = 0.97. Linear interpolation gives 10th percentile at 201.1, median at 270.0, and 90th percentile at 358.0."},{"kind":"math","text":"Published values are derived from the ladder only: pointEstimate = median = 270.0 usd_billions; ciLow = 10th percentile = 201.1 usd_billions; ciHigh = 90th percentile = 358.0 usd_billions."},{"kind":"forecast","point":270.0,"ciLow":201.1,"ciHigh":358.0}]}
