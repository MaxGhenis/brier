# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bea.ita.personal_transfer_payments
- period: 2026-Q2
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-personal-transfer-payments-q2-2026"
- country: "US"
- targetUnit: "usd_millions"
- dataPointId: "bea.ita.personal_transfer_payments.2026_q2.first_print"
- expectedReleaseWindow: {"end": "2026-09-24", "start": "2026-09-24"}
- sourceBinding: {"adapter": "bea-ita-itable", "allowedHosts": ["apps.bea.gov", "www.bea.gov"], "expectedReleaseWindow": {"end": "2026-09-24", "start": "2026-09-24"}, "field": "Line 18: Personal transfers (QSA)", "releasePolicy": "first_print", "sourceSeriesId": "ITA:T5.1:L18:QSA", "sourceUrl": "https://apps.bea.gov/iTable/?ReqID=62&step=6&isuri=1&tablelist=62&product=1", "table": "U.S. International Transactions, Table 5.1, line 18 (Personal transfers), quarterly seasonally adjusted", "transform": {"applicationId": 62, "basis": "QSA", "cadence": "quarterly", "factor": 1, "lineNumber": "18", "operation": "identity", "productId": "1", "rowLabel": "Personal transfers", "tableList": "62", "unit": "usd_millions"}}
- targetRegistrationPath: "records/targets/2026-08-12-7226e22181e3efd6ac0e1740ffc7d079b1a45949f34982c6290fd74391665925.json"
- targetContentHash: "7226e22181e3efd6ac0e1740ffc7d079b1a45949f34982c6290fd74391665925"
- registrationCommit: "d50ffb7c957ea27fad25c6e0c6fee0aa2471bc84"
- registeredAtUtc: "2026-08-12T21:16:44Z"
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
8e4d2b859d3afecb66e53783dda0cf63daa23998e98173f43cddf548260841c7

# Draft forecast response
{"slug":"us-personal-transfer-payments-q2-2026","country":"US","type":"data","title":"US personal transfers Q2 2026","question":"What will BEA report as the first-print value for U.S. International Transactions Table 5.1, line 18, Personal transfers, quarterly seasonally adjusted, for 2026 Q2, in millions of dollars?","unit":"usd_millions","pointEstimate":18467,"ciLow":18081,"ciHigh":18852,"confidence":0.8,"resolutionDate":"2026-09-24","resolutionSource":"BEA, U.S. International Transactions and Investment Position","resolutionSourceUrl":"https://apps.bea.gov/iTable/?ReqID=62&step=6&isuri=1&tablelist=62&product=1","resolutionRule":"Resolve from BEA U.S. International Transactions, Table 5.1, line 18 (Personal transfers), quarterly seasonally adjusted, for 2026 Q2, first print only, as a whole-number millions-of-dollars value in the official iTable release; later revisions do not change resolution.","dataPointId":"bea.ita.personal_transfer_payments.2026_q2.first_print","historicalContext":[{"label":"BEA ITA Table 5.1 line 18, 2025 Q1 current June 24 2026 vintage","value":18688},{"label":"BEA ITA Table 5.1 line 18, 2025 Q2 current June 24 2026 vintage","value":18641},{"label":"BEA ITA Table 5.1 line 18, 2025 Q3 current June 24 2026 vintage","value":18596},{"label":"BEA ITA Table 5.1 line 18, 2025 Q4 current June 24 2026 vintage","value":18552},{"label":"BEA ITA Table 5.1 line 18, 2026 Q1 current June 24 2026 vintage","value":18511}],"drivers":["Latest BEA line-18 print is 18,511","Recent quarterly changes are small negatives","Trailing-four-change candidate beats persistence","No direct current signal for a large break"],"sourceContext":["https://www.bea.gov/news/schedule","https://apps.bea.gov/iTablecore/data/app/GetStep","https://apps.bea.gov/iTable/?ReqID=62&step=6&isuri=1&tablelist=62&product=1","https://app.thesisinstitute.org/specs.json"],"runAt":"2026-08-12T21:18:54Z","reasoning":[{"kind":"heading","text":"Resolve BEA ITA personal transfers"},{"kind":"text","text":"The registered target fixes slug us-personal-transfer-payments-q2-2026, unit usd_millions, dataPointId bea.ita.personal_transfer_payments.2026_q2.first_print, and BEA ITA Table 5.1 line 18 Personal transfers (QSA) as the resolving series. I attempted the required specs.json slug check; the fetched page returned HTTP 404 content, so I found no contrary public specs entry and kept the registered slug."},{"kind":"tool","tool":"curl","call":"curl -L -sS https://www.bea.gov/news/schedule | rg -n -C 2 'International Transactions and Investment Position|September 24|2nd Quarter 2026'","result":"BEA schedule excerpt showed September 24 at 8:30 AM for 'U.S. International Transactions and Investment Position, 2nd Quarter 2026'."},{"kind":"tool","tool":"bea.itable","call":"POST https://apps.bea.gov/iTablecore/data/app/GetStep with appid 62, Product 1, TableList 62","result":"Fetched BEA Table 5.1 response identity Id 6206, AppId 62, Number 6; table description 'Release Date: June 24, 2026 - Next Release Date: September 24, 2026'; line 18 Personal transfers values included 2025 Q1 18,688, 2025 Q2 18,641, 2025 Q3 18,596, 2025 Q4 18,552, 2026 Q1 18,511."},{"kind":"tool","tool":"bea.itable.history","call":"POST selected-year BEA iTable requests for 2020-2026, Filter_#2=1, Filter_#3=18","result":"Fetched line 18 Personal transfers QSA values in usd_millions: 2020 Q1 12,777; 2020 Q2 12,793; 2020 Q3 12,931; 2020 Q4 13,193; 2021 Q1 13,336; 2021 Q2 13,586; 2021 Q3 13,944; 2021 Q4 14,410; 2022 Q1 14,618; 2022 Q2 15,315; 2022 Q3 15,909; 2022 Q4 16,400; 2023 Q1 16,525; 2023 Q2 16,749; 2023 Q3 17,074; 2023 Q4 17,499; 2024 Q1 18,023; 2024 Q2 18,405; 2024 Q3 18,642; 2024 Q4 18,737; 2025 Q1 18,688; 2025 Q2 18,641; 2025 Q3 18,596; 2025 Q4 18,552; 2026 Q1 18,511."},{"kind":"text","text":"Base rate/reference class: the last 24 fetched quarter-to-quarter changes in BEA Table 5.1 line 18 have mean +238.9, sigma 220.4, range -49 to +697. The recent plateau is clear: the last five changes are -49, -47, -45, -44, and -41, so a pure last-print persistence prior is 18,511 and a trailing-four-change prior is 18,467."},{"kind":"tool","tool":"model_candidates","call":"Compute thesis_model_candidate_v1 persistence and trailing-four-change candidates from fetched BEA values","result":"Candidate persistence: point 18,511, p10 18,125, p50 18,511, p90 18,897, 80% interval [18,125,18,897], calibration_n 24, walk-forward MAE from 2022 Q1 197.2. Candidate trailing4_change: point 18,467, p10 18,081, p50 18,467, p90 18,852, 80% interval [18,081,18,852], calibration_n 24, walk-forward MAE from 2022 Q1 172.1."},{"kind":"math","text":"Prior/update/interval: prior is the trailing-four-change model because its walk-forward MAE 172.1 beats persistence MAE 197.2 on the fetched 2022 Q1-2026 Q1 history. Historical sample is 2020 Q1-2026 Q1 BEA line 18 current official values, with latest value 18,511 and last four changes -47, -45, -44, -41, so point = 18,511 + mean(-47,-45,-44,-41) = 18,466.75, rounded to 18,467. Adjustment components: no extra current-evidence adjustment beyond recent line-18 momentum. Interval method: last-24 change dispersion sigma = 220.4; 1.28*sigma = 282.1, widened to 1.75*sigma = 385.7 because the reference class includes a transition from fast growth to a flat/down plateau and Q2 first print may reveal whether that plateau persists. Bounds = 18,466.75 +/- 385.7 = [18,081.0, 18,852.5], rounded to [18,081, 18,852]."},{"kind":"text","text":"Sanity check: using a 386-million half-width around a one-quarter-ahead prior would have covered 8 of the last 10 fetched quarter-to-quarter changes; the two misses were the larger pre-plateau 2023 Q4 and 2024 Q1 increases."},{"kind":"text","text":"Upside risk outside the interval if personal transfer payments reaccelerate toward the 2023-2024 growth regime or if BEA's Q2 first print incorporates a level reset above recent current-vintage values. Downside risk would land below the interval if the 2025-2026 decline steepens materially rather than continuing near -40 to -50 million per quarter."},{"kind":"forecast","point":18467,"ciLow":18081,"ciHigh":18852}]}
