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
{"slug":"us-mts-deficit-july-2026-fast","country":"US","type":"data","title":"U.S. July 2026 Monthly Treasury Deficit","question":"What will the U.S. Treasury Monthly Treasury Statement Table 1 report for the July 2026 monthly deficit, in nominal dollars, on the first print?","unit":"usd_billions","pointEstimate":296,"ciLow":213,"ciHigh":380,"confidence":0.8,"resolutionDate":"2026-08-17","resolutionSource":"U.S. Department of the Treasury, Bureau of the Fiscal Service, Monthly Treasury Statement Table 1","resolutionSourceUrl":"https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","resolutionRule":"Resolve from the first official Monthly Treasury Statement print for July 2026, Table 1, monthly Deficit/Surplus (-) for July 2026. Use the Table 1 value in $ millions, divide by 1000, keep deficits positive and surpluses negative, and do not revise for later MTS revisions or corrected historical tables.","dataPointId":"treasury.mts.monthly_deficit.july_2026.first_print","historicalContext":[{"label":"May 2026","value":292.648},{"label":"April 2026","value":-215.024},{"label":"March 2026","value":164.1},{"label":"February 2026","value":307.501},{"label":"January 2026","value":94.615},{"label":"July 2025","value":291},{"label":"July 2024","value":243.741},{"label":"July 2023","value":220.782}],"drivers":["seasonally high July outlays","rising interest and entitlement spending","tariff and other receipt growth","monthly cash-flow timing"],"sourceContext":["https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202506.pdf","https://fred.stlouisfed.org/series/MTSDS133FMS","https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202501.pdf"],"runAt":"2026-07-10T00:00:00Z","thresholdLadder":{"thresholds":[200,220,240,260,280,300,320,340,360,380,400],"cumulativeProbabilities":[0.06,0.12,0.22,0.32,0.42,0.52,0.62,0.72,0.82,0.9,0.95]},"reasoning":[{"kind":"heading","text":"U.S. July 2026 Monthly Treasury Deficit"},{"kind":"text","text":"The target is the first official July 2026 Monthly Treasury Statement print, Table 1, monthly Deficit/Surplus (-), expressed in usd_billions with deficits positive. The canonical ledger contract gives resolutionDate 2026-08-17; Treasury describes MTS as a summary of receipts, outlays, and surplus or deficit, and the release schedule places the first-print window in August."},{"kind":"tool","tool":"official.lookup","call":"Fetched official Treasury MTS Table 1 reference-class observations from published reports.","result":"The official Treasury January 2025 MTS fetched July 2024 at $243,741 million, June 2024 at $70,965 million, May 2024 at $347,131 million, and July 2023 at $220,782 million; under the target convention these are deficits of 243.741, 70.965, 347.131, and 220.782 usd_billions."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest official-source-linked MTS series observations through the June 10, 2026 release.","result":"The fetched MTS series reported January 2026 surplus/deficit of -$94,615.162 million, February of -$307,501.433 million, March of -$164,100.339 million, April of $215,024.140 million, and May of -$292,648.462 million; converting to positive-deficit convention gives 94.615, 307.501, 164.100, -215.024, and 292.648 usd_billions."},{"kind":"tool","tool":"official.lookup","call":"Fetched the prior July first-print reference from the Treasury MTS release coverage.","result":"July 2025 was fetched at approximately $291 billion deficit, while July 2024 was fetched at $243.741 billion and July 2023 at $220.782 billion; July deficits therefore cluster near $220-$300 billion but can move with cash-flow timing."},{"kind":"text","text":"The series is not seasonally adjusted and is the gross monthly deficit, not fiscal-year-to-date deficit, receipts, outlays, or a revised historical value. July is typically a deficit month because outlays remain large while receipts are less concentrated than in April and June; interest, Social Security, Medicare, and calendar timing create substantial month-to-month variation."},{"kind":"text","text":"The base rate is the fetched July reference class of 220.782, 243.741, and approximately 291 usd_billions, supplemented by the latest five-month path of 94.615, 307.501, 164.100, -215.024, and 292.648. The central estimate is near the upper part of the July reference class because recent deficits remain large and interest and entitlement outlays are persistent."},{"kind":"text","text":"Prior/update/interval: A persistence prior from the July 2023-2025 reference class centers near 252 usd_billions; the update components are elevated interest and entitlement outlays, continued receipt growth, and one-off calendar timing. I use a threshold-ladder interval rather than a parametric distribution; fetched July values 220.782, 243.741, and approximately 291 anchor the rung span from 200 to 400."},{"kind":"math","text":"Ladder: P(X <= 200) = 0.06; P(X <= 220) = 0.12; P(X <= 240) = 0.22; P(X <= 260) = 0.32; P(X <= 280) = 0.42; P(X <= 300) = 0.52; P(X <= 320) = 0.62; P(X <= 340) = 0.72; P(X <= 360) = 0.82; P(X <= 380) = 0.90; P(X <= 400) = 0.95. Linear interpolation gives 10th percentile at 213.3, rounded to 213; median at 296; 90th percentile at 380."},{"kind":"text","text":"Downside risk is a receipt-heavy month or delayed outlays producing a deficit below 213 billion. Upside risk is faster outlay growth, especially interest or benefit payments, producing a deficit above 380 billion; an unusual timing shift or major fiscal transaction would land outside the interval."},{"kind":"forecast","point":296,"ciLow":213,"ciHigh":380}]}
