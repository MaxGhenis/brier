# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bea.government_social_benefits.medicaid
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bea-government-social-benefits-medicaid-june-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.government_social_benefits.medicaid.june_2026.first_print"
- resolutionSourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=W729RC1&vintage_date=2026-06-25"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "W729RC1", "releasePolicy": "first_print", "sourceSeriesId": "W729RC1", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=W729RC1&vintage_date=2026-06-25", "table": "Personal Income and Outlays, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-15-62975454c04b5d6bf9b9c76239d4d6289d2ff47c42e835a321a73bc441c57acb.json"
- targetContentHash: "62975454c04b5d6bf9b9c76239d4d6289d2ff47c42e835a321a73bc441c57acb"
- registrationCommit: "0b8a29cc7d9bec54ef1d71247d06c1bf17d64355"
- registeredAtUtc: "2026-07-15T16:29:07Z"
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
3520c95295c76b45b26799c6e1ff51f3bcf0dd42e2ce9eecc0f1ca5bba98d692

# Draft forecast response
{"slug":"bea-government-social-benefits-medicaid-june-2026","country":"US","type":"data","title":"BEA Medicaid Benefits, June 2026","question":"What will BEA first report for Personal current transfer receipts: Government social benefits to persons: Medicaid, June 2026, seasonally adjusted annual rate?","unit":"usd_billions","pointEstimate":1054.5,"ciLow":1043.8,"ciHigh":1065.2,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"U.S. Bureau of Economic Analysis, Personal Income and Outlays, Table 2.6","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=W729RC1&vintage_date=2026-06-25","resolutionRule":"Resolve to the first-print June 2026 value for BEA series W729RC1, Personal current transfer receipts: Government social benefits to persons: Medicaid, in billions of dollars at a seasonally adjusted annual rate, as published in Personal Income and Outlays Table 2.6. Use the originally released value, not later revisions; record to one decimal billion dollars. The ledger URL points to an ALFRED/FRED mirror and its vintage_date=2026-06-25 appears inconsistent with a June 2026 first print, but this forecast remains tied to the registered target and uses the BEA July 30, 2026 release date.","dataPointId":"bea.government_social_benefits.medicaid.june_2026.first_print","historicalContext":[{"label":"May 2026 W729RC1","value":1052.2},{"label":"Apr 2026 W729RC1","value":1055.7},{"label":"Mar 2026 W729RC1","value":1061.1},{"label":"Jun 2025 W729RC1","value":1004.3},{"label":"Jun 2024 W729RC1","value":939.6}],"drivers":["May 2026 level was 1052.2 billion SAAR after four months of softening from February 2026","Recent May-to-June reference class usually rises, with June changes of 4.5 in 2024 and 11.5 in 2025 but -9.8 in 2023","Medicaid level remains elevated after the 2025 rise, so persistence dominates with only a small June seasonal/update lift","BEA calendar verifies Personal Income and Outlays, June 2026 for July 30, 2026 at 8:30 AM"],"sourceContext":["https://www.bea.gov/news/schedule","https://fred.stlouisfed.org/series/W729RC1","https://fred.stlouisfed.org/data/W729RC1","https://fred.stlouisfed.org/release/tables?eid=155443&rid=54"],"runAt":"2026-07-15T16:30:34Z","reasoning":[{"kind":"heading","text":"BEA Medicaid Benefits June 2026 First Print"},{"kind":"text","text":"Framing and exact resolver: the target is BEA NIPA monthly series W729RC1, Medicaid under government social benefits to persons, in billions of dollars at a seasonally adjusted annual rate. The BEA release schedule lists Personal Income and Outlays, June 2026 for July 30, 2026 at 8:30 AM; the registered ledger mirror URL uses ALFRED vintage_date=2026-06-25, which is earlier than the scheduled June 2026 release and appears to be a ledger-source discrepancy rather than evidence about the June value."},{"kind":"tool","tool":"official.lookup","call":"BEA release schedule lookup for Personal Income and Outlays, June 2026","result":"Fetched BEA schedule: Personal Income and Outlays, June 2026 is scheduled for July 30, 2026 at 8:30 AM; the same schedule page shows Personal Income and Outlays, July 2026 on August 26, 2026."},{"kind":"tool","tool":"official.lookup","call":"FRED/BEA series page for W729RC1 latest monthly values","result":"Fetched W729RC1 values: May 2026 = 1052.2, Apr 2026 = 1055.7, Mar 2026 = 1061.1, Feb 2026 = 1062.0, Jan 2026 = 1057.4, units billions of dollars SAAR, monthly."},{"kind":"tool","tool":"official.lookup","call":"FRED release table 2.6, Personal Income and Its Disposition, Monthly","result":"Fetched table 2.6 Medicaid row: May 2026 = 1052.2, Apr 2026 = 1055.7, May 2025 = 992.8; government social benefits to persons were May 2026 = 5024.4 and Apr 2026 = 4995.7."},{"kind":"tool","tool":"official.lookup","call":"FRED table-data history for W729RC1 reference class and recent June comparisons","result":"Fetched W729RC1 history: Jun 2025 = 1004.3 after May 2025 = 992.8, Jun 2024 = 939.6 after May 2024 = 935.1, Jun 2023 = 905.5 after May 2023 = 915.3, Jun 2022 = 821.9 after May 2022 = 821.0, Jun 2021 = 753.3 after May 2021 = 747.3."},{"kind":"math","text":"Prior/update/interval: base rate/reference class is a persistence-plus-June-change model using the same W729RC1 SAAR variant; recent May-to-June changes were +11.5 in 2025, +4.5 in 2024, -9.8 in 2023, +0.9 in 2022, and +6.0 in 2021, so I use a roughly +4.2 billion June base lift from May. Current-release adjustment subtracts 2.0 for 2026 downward momentum from Feb 1062.0 to May 1052.2 and adds 0.1 for the still-high level/policy baseline, giving 1052.2 + 4.2 - 2.0 + 0.1 = 1054.5. For the 80% interval, the 2024-01 through 2026-05 successive monthly changes have sigma = 8.35 billion; 1.28*sigma = 10.69, so 1054.5 +/- 10.7 gives 1043.8 to 1065.2."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed catch-up or accounting jump like mid-2025 that would land above the interval if June prints above 1065.2. Downside risk is a continuation of the spring 2026 slide or a redetermination-related drop like June 2023 that would land below the interval if June prints below 1043.8. Values outside the interval would most likely reflect an administrative timing change, not ordinary month-to-month drift."},{"kind":"forecast","point":1054.5,"ciLow":1043.8,"ciHigh":1065.2}]}
