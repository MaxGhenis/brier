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
{"slug":"us-mts-deficit-july-2026","country":"US","type":"data","title":"U.S. Monthly Treasury Deficit — July 2026","question":"What will the U.S. Treasury Monthly Treasury Statement Table 1 report as the not-seasonally-adjusted monthly deficit for July 2026 on its first official print?","unit":"usd_billions","pointEstimate":287.5,"ciLow":37.5,"ciHigh":500,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, convert to usd_billions by dividing by 1000, and keep deficits positive and surpluses negative. Do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"January 2026","value":94.615},{"label":"February 2026","value":307.501},{"label":"March 2026","value":164.1},{"label":"April 2026","value":-215.024},{"label":"May 2026","value":292.648}],"drivers":["July is typically a large-deficit month outside the April tax-receipt peak","Persistent interest and entitlement outlays","Monthly cash-flow and payment-calendar volatility","Customs and other receipts provide partial offset"],"sourceContext":["https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government","https://fred.stlouisfed.org/series/MTSDS133FMS","https://fiscal.treasury.gov/accounting/monthly-treasury-statement"],"runAt":"2026-07-10T00:00:00Z","thresholdLadder":{"thresholds":[0,50,100,150,200,250,275,300,325,350,400,450,500,550],"cumulativeProbabilities":[0.07,0.11,0.16,0.22,0.3,0.38,0.44,0.56,0.65,0.72,0.8,0.86,0.9,0.94]},"reasoning":[{"kind":"heading","text":"July 2026 Monthly Treasury Statement deficit forecast"},{"kind":"text","text":"The target is the first-print, not-seasonally-adjusted July 2026 monthly Deficit/Surplus (-) in Table 1, expressed as a positive deficit in usd_billions. The supplied ledger contract fixes resolution on 2026-08-17 and excludes later revisions."},{"kind":"tool","tool":"official.lookup","call":"Look up the prior-year July MTS Table 1 observation","result":"The July 2025 first-print observation was a $291.142660 billion deficit, with receipts of $338.491848 billion and outlays of $629.634509 billion."},{"kind":"tool","tool":"official.lookup","call":"Fetch the recent official-source reference class through the Treasury Fiscal Service series mirror","result":"The MTS series reported January 2026 at a $94.615162 billion deficit, February at $307.501433 billion, March at $164.100339 billion, April at a $215.024140 billion surplus, and May at a $292.648462 billion deficit."},{"kind":"tool","tool":"official.lookup","call":"Verify MTS release convention and source definition","result":"The Fiscal Service describes MTS as covering receipts, outlays, and surplus or deficit; its release convention is the 8th workday at 2:00 p.m., and the current dataset is available in machine-readable formats."},{"kind":"text","text":"The base rate/reference class is the recent five-month flow distribution plus the July seasonal anchor near $291.143 billion. July should remain a substantial deficit because it follows the June quarter-end tax-receipt timing and precedes September year-end, while higher interest and entitlement outlays support a persistent deficit floor."},{"kind":"text","text","text":"Level and momentum favor a result near the recent non-tax-month observations; the April surplus is treated as a tax-calendar outlier rather than a new regime. The July 2025 anchor and continuing spending pressure pull the center toward roughly $288 billion."},{"kind":"text","text":"Prior/update/interval: The persistence-and-seasonality prior is the five fetched January-May 2026 flow values, updated toward the July 2025 first print of 291.143 by recurring payment timing and higher interest costs. Using the values themselves, sigma = 211.8 usd_billions; 1.28*sigma implies a roughly 271.1 usd_billions half-width. The ladder-implied 80% interval is 37.5 to 500.0, a 231.25 usd_billions half-width, narrower than the dispersion-based half-width because the ladder assigns limited probability to negative deficits and extreme cash-flow outcomes."},{"kind":"math","text":"Ladder: P(X <= 0) = 0.07; P(X <= 50) = 0.11; P(X <= 100) = 0.16; P(X <= 150) = 0.22; P(X <= 200) = 0.30; P(X <= 250) = 0.38; P(X <= 275) = 0.44; P(X <= 300) = 0.56; P(X <= 325) = 0.65; P(X <= 350) = 0.72; P(X <= 400) = 0.80; P(X <= 450) = 0.86; P(X <= 500) = 0.90; P(X <= 550) = 0.94. Linear interpolation gives ciLow = 37.500 at 0.10, pointEstimate = 287.500 at 0.50, and ciHigh = 500.000 at 0.90."},{"kind":"text","text":"Upside risk is a deficit above $500 billion from an unusual acceleration in outlays or delayed receipts. Downside risk is a deficit below $37.5 billion if receipts are unusually strong or payments shift across the month. A result outside the interval would most likely reflect a major payment-calendar, policy, or reporting-timing shock."},{"kind":"forecast","point":287.5,"ciLow":37.5,"ciHigh":500}]}
