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
d3d4ec4a65cc5782452c9c4feb8508923e6eb10947f1e98aa480c9b5e0fa0781

# Draft forecast response
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"US MTS July 2026 Deficit","question":"U.S. Department of the Treasury Monthly Treasury Statement Table 1 monthly deficit/surplus for July 2026, first official print, nominal dollars, deficits positive and surpluses negative.","unit":"usd_billions","pointEstimate":308.1,"ciLow":262.4,"ciHigh":353.8,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, convert to usd_billions by dividing by 1000, and keep deficits positive and surpluses negative. Do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"July 2022 first-print deficit","value":211.052},{"label":"July 2023 first-print deficit","value":220.782},{"label":"July 2024 first-print deficit","value":243.741},{"label":"July 2025 first-print deficit","value":291.143}],"drivers":["July has recently been a large deficit month","2025 customs-duty receipts lifted revenue but outlays still jumped","health, Social Security, defense, and net interest outlays remain high","FY2026 budget-estimate deficit is near FY2025 run-rate, limiting trend extrapolation"],"sourceContext":["https://fiscal.treasury.gov/accounting/monthly-treasury-statement","https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","https://fiscal.treasury.gov/system/files/files/reports-statements/mts/mts0725.pdf","https://fiscal.treasury.gov/system/files/files/reports-statements/mts/mts0724.pdf","https://fiscal.treasury.gov/system/files/files/reports-statements/mts/mts0723.pdf"],"runAt":"2026-07-10T05:27:41Z","reasoning":[{"kind":"heading","text":"US MTS July 2026 Monthly Deficit Forecast"},{"kind":"text","text":"Framing and exact resolver: this is the first-print U.S. Treasury Monthly Treasury Statement Table 1 monthly deficit/surplus for July 2026, not fiscal-year-to-date deficit, receipts, outlays, refunds, or a revised vintage. The table is in $ millions; the forecast is in usd_billions with deficits positive."},{"kind":"tool","tool":"official.lookup","call":"Opened the Bureau of the Fiscal Service Monthly Treasury Statement page and prior-issue archive.","result":"The official MTS page says the MTS is normally released on the 8th workday of the month following the reporting month; the page was last updated January 15, 2026, and Fiscal Service says the data moved to FiscalData on November 25, 2025."},{"kind":"text","text":"Resolution-date note: applying the official 8th-workday policy to July 2026 points to August 12, 2026, while the registered ledger window runs through 2026-08-17. I keep the target tied to the ledger resolution date of 2026-08-17 and would still resolve on the first official July 2026 print if it appears earlier."},{"kind":"tool","tool":"official.lookup","call":"Read MTS July 2025 PDF, Table 1 and Table 3.","result":"For July 2025, Table 1 reported receipts of 338,492 million, outlays of 629,635 million, and a monthly deficit of 291,143 million; Table 3 reported customs duties of 27,670 million and total receipts of 338,492 million."},{"kind":"tool","tool":"official.lookup","call":"Read MTS July 2024 and July 2023 PDFs, Table 1.","result":"For July 2024, Table 1 reported receipts of 330,377 million, outlays of 574,119 million, and a deficit of 243,741 million; for July 2023, receipts were 276,161 million, outlays were 496,943 million, and the deficit was 220,782 million."},{"kind":"tool","tool":"official.lookup","call":"Read MTS July 2023 PDF comparable FY2022 row and MTS July 2025 budget-estimate columns.","result":"For July 2022, Table 1 reported receipts of 269,331 million, outlays of 480,383 million, and a deficit of 211,052 million; July 2025 Table 2 showed next-fiscal-year 2026 budget estimates of receipts 6,011,381 million, outlays 7,612,734 million, and deficit 1,601,353 million."},{"kind":"text","text":"Reference class/base rate: the same-variant July first-print monthly deficits for 2022-2025 were 211.052, 220.782, 243.741, and 291.143 usd_billions. The four-year mean is 241.6795, but the last two observations and higher nominal outlay level argue for anchoring closer to 2025 than to the full mean."},{"kind":"math","text":"Prior/update/interval: persistence prior = July 2025 first-print deficit of 291.143; historical sample = July 2022-2025 first-print Table 1 monthly deficits of 211.052, 220.782, 243.741, 291.143; adjustment components = +18.961 from 40% of the 2024-to-2025 increase, -10.000 for continuing high customs/tariff receipts, +8.000 for higher benefit, health, defense, and interest outlays; point = 291.143 + 18.961 - 10.000 + 8.000 = 308.104. Interval method = sample standard deviation of the July deficit values themselves because this is a monthly flow; sigma = 35.710, half-width = 1.28*sigma = 45.709, so 80% interval = 308.104 +/- 45.709 = 262.395 to 353.813."},{"kind":"text","text":"Upside risk: the deficit would land above the interval if July outlays repeat another unusually large health, education, or interest timing surge while tariff receipts fade. Downside risk: it would land below the interval if customs receipts remain near or above the July 2025 surge and benefit or agency payments shift out of July. Outside the interval on either side would most likely come from payment-calendar timing rather than a smooth macro trend."},{"kind":"forecast","point":308.1,"ciLow":262.4,"ciHigh":353.8}]}
