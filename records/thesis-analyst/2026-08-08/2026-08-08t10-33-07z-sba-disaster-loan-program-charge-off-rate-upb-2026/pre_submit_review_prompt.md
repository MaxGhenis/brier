# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: sba.disaster.loan_program.charge_off_rate_upb
- period: 2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "sba-disaster-loan-program-charge-off-rate-upb-fy2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "sba.disaster.loan_program.charge_off_rate_upb.2026.first_print"
- resolutionDate: "2028-12-31"
- resolutionDateBasis: "resolve-by-bound"
- expectedReleaseWindow: {"end": "2028-12-31", "start": "2026-10-01"}
- sourceBinding: {"adapter": "sba-loan-program-performance-pdf", "allowedHosts": ["legacy.sba.gov", "www.sba.gov"], "expectedReleaseWindow": {"end": "2028-12-31", "start": "2026-10-01"}, "field": "Disaster / Disaster", "releasePolicy": "first_print", "sourceSeriesId": "sba.disaster.loan_program.charge_off_rate_upb", "sourceUrl": "https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance", "table": "Table 9 - Charge Off Rates as a Percent of Unpaid Principal Balance (UPB) Amount by Program", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-08-906824b00a5ed65ceace2ba302641e64074ee35726253ca6a0dafb1a5fb77b39.json"
- targetContentHash: "906824b00a5ed65ceace2ba302641e64074ee35726253ca6a0dafb1a5fb77b39"
- registrationCommit: "f71dfe6fa8d7fff8803423814942573b7502ac0b"
- registeredAtUtc: "2026-08-08T10:26:30Z"

# Resolve-by-bound target contract (machine checked)
- registeredResolveByBound: "2028-12-31"
- officialAnnouncementUrl: "https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance"
The bound and expected release window are Thesis lab commitments, not timing claims made by the announcement. The announcement authenticates methodology identity only; it does not establish the bound or expected release window. This is an outer bound, not a scheduled release day. resolutionDate must byte-echo the registered resolve-by bound; never infer a more specific day from cadence.
resolutionSourceUrl must byte-echo officialAnnouncementUrl. Call `thesis_announcement_fetch.fetch_official_announcement` with that exact URL. The publisher authenticates the structured draft/final tool event; a reasoning-token claim, search result, same-host page, or prose citation cannot substitute for it.
Base rate during a methodology transition: while NO official print under the announced revised methodology exists — including revised historical or backcast estimates — the CURRENT official series is the admissible base rate: fetch it from its official source, name its vintage explicitly, and state the announced transition as the regime consideration in the sigma step. Do not refuse for lack of the unpublished revised series, and do not fabricate or pre-apply revision adjustments. The moment any revised-methodology official print exists, revised prints are required and old-methodology history stops being admissible.
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
d8d9cc0a9a32ca3f490a5aaa939a5f00969fce617bad10098b9251409a2b6a42

# Draft forecast response
{"slug":"sba-disaster-loan-program-charge-off-rate-upb-fy2026","country":"US","type":"data","title":"SBA Disaster Charge-Off Rate FY2026","question":"What will the SBA first print for FY2026 Disaster / Disaster charge-off rates as a percent of unpaid principal balance in Table 9 of Small Business Administration Loan Program Performance?","unit":"percent","pointEstimate":1.6,"ciLow":0.72,"ciHigh":3.25,"confidence":0.8,"resolutionDate":"2028-12-31","resolutionSource":"Official SBA Loan Program Performance Table 9","resolutionSourceUrl":"https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance","resolutionRule":"Resolve to the first official SBA Loan Program Performance print for FY2026, Table 9 - Charge Off Rates as a Percent of Unpaid Principal Balance (UPB) Amount by Program, field Disaster / Disaster. Use the percentage as printed by SBA, currently to 0.01 percentage point precision; do not use later revisions or same-day corrections unless they are the first official print itself.","dataPointId":"sba.disaster.loan_program.charge_off_rate_upb.2026.first_print","historicalContext":[{"label":"2025 Q3 current official vintage","value":0.9},{"label":"2024 full-year","value":3.06},{"label":"2023 full-year","value":3.44},{"label":"2022 full-year","value":1.97},{"label":"2016-2024 median","value":1.46}],"drivers":["Current official FY2025 Q3 Disaster / Disaster charge-off rate is only 0.90 percent","Recent full-year charge-off rates were elevated in FY2022-FY2024","Disaster UPB rose to 11.98 billion dollars by June 30 2025, diluting a fixed charge-off dollar flow","COVID EIDL is a separate row and is not included in the resolver field"],"sourceContext":["https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance","https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip","https://www.congress.gov/crs-product/R48558"],"runAt":"2026-08-08T10:33:26Z","thresholdLadder":{"thresholds":[0.4,0.6,0.8,1,1.2,1.4,1.6,1.8,2.1,2.5,3,3.5,4.2],"cumulativeProbabilities":[0.04,0.07,0.12,0.2,0.3,0.4,0.5,0.6,0.7,0.78,0.87,0.93,0.97]},"reasoning":[{"kind":"heading","text":"SBA Disaster / Disaster FY2026 charge-off rate forecast"},{"kind":"text","text":"Framing: the target is the first official FY2026 SBA Loan Program Performance Table 9 print for the Disaster program row labeled Disaster, not the separate COVID EIDL row. The resolution date byte-echoes the Thesis resolve-by-bound of 2028-12-31; this is an outer bound, not an inferred SBA release date. The resolutionSourceUrl byte-echoes the registered methodology-announcement URL, and the required official announcement fetch returned HTTP 200 for 37099 bytes with response SHA-256 5a77a6bb8e74afdefcffd588fb37cab831ca69385b69d6911b900a99efaede64."},{"kind":"tool","tool":"official.lookup","call":"Fetched the SBA Loan Program Performance page and FY25Q3 zip, then extracted Table 9 Charge Off Rates from WDS_ChargeOffRates_Report_20250630.pdf.","result":"For Disaster / Disaster, fetched charge-off rates were 2016 1.46%, 2017 1.39%, 2018 1.09%, 2019 1.98%, 2020 1.42%, 2021 0.20%, 2022 1.97%, 2023 3.44%, 2024 3.06%, and 2025 Q3 0.90%."},{"kind":"tool","tool":"official.lookup","call":"Fetched the SBA FY25Q3 UPB table WDS_UPB_Report_20250630.pdf for the same Disaster / Disaster row.","result":"For Disaster / Disaster, fetched UPB was $9,155,822,926 in 2022, $9,379,479,606 in 2023, $9,789,692,235 in 2024, and $11,976,493,088 as of 2025-06-30."},{"kind":"tool","tool":"official.lookup","call":"Fetched the SBA FY25Q3 Charge Off Amount table WDS_ChargeOffAmount_Report_20250630.pdf for the same Disaster / Disaster row.","result":"For Disaster / Disaster, fetched charge-off amounts were $180,342,594 in 2022, $322,632,623 in 2023, $299,971,326 in 2024, and $107,714,599 as of 2025-06-30."},{"kind":"tool","tool":"public.context","call":"Checked CRS disaster-loan program context for forward-looking credit risk in the disaster account.","result":"CRS table values for FY2025 disaster-loan assumptions included a 3.16% borrower interest rate, 29.39% default rate, and 29.17% post-default recovery rate; FY2024 values were 2.93%, 28.22%, and 27.76% respectively."},{"kind":"text","text":"Reference class and base rate: the current official SBA Table 9 vintage through 2025-06-30 is the admissible base rate because no separate revised/backcast official print was found. The 2016-2024 full-year Disaster / Disaster history has a median of 1.46%, with a recent elevated cluster at 1.97%, 3.44%, and 3.06% in FY2022-FY2024, while the FY2025 partial-year print is much lower at 0.90%."},{"kind":"text","text":"Variant control: all numeric anchors above are the SBA Table 9 charge-off rate as a percent of UPB for Disaster / Disaster. I excluded COVID EIDL values even though they appear under Disaster, because COVID EIDL is a separate row and the target field is Disaster / Disaster."},{"kind":"text","text":"Prior/update/interval: persistence prior is the 2016-2024 full-year reference class centered near the 1.46% median, updated downward from the FY2022-FY2024 high-rate cluster by the FY2025 Q3 0.90% rate and larger 2025 UPB denominator, then nudged upward for lagged disaster-loan credit stress and CRS default-rate assumptions near 28%-29%; interval method is the elicited threshold ladder anchored by the fetched 0.90%, 1.46%, 1.97%, 3.06%, and 3.44% values, with the announced methodology-transition/regime consideration handled by widening the upper tail rather than applying any fabricated revision adjustment."},{"kind":"math","text":"Ladder: P(X <= 0.4) = 0.04; P(X <= 0.6) = 0.07; P(X <= 0.8) = 0.12; P(X <= 1.0) = 0.20; P(X <= 1.2) = 0.30; P(X <= 1.4) = 0.40; P(X <= 1.6) = 0.50; P(X <= 1.8) = 0.60; P(X <= 2.1) = 0.70; P(X <= 2.5) = 0.78; P(X <= 3.0) = 0.87; P(X <= 3.5) = 0.93; P(X <= 4.2) = 0.97. Linear interpolation gives 10th percentile at 0.72, median at 1.60, and 90th percentile at 3.25."},{"kind":"text","text":"Counter-considerations: upside risk for the rate is a delayed wave of default determinations on older disaster loans or a smaller-than-expected FY2026 UPB denominator, which would land above the interval if charge-offs resembled FY2023 while UPB stopped growing. Downside risk is continuation of FY2025's low run rate or unusually high recoverability, which could land below the interval if annual charge-offs stay near the 2025 Q3 pace against a large UPB base."},{"kind":"forecast","point":1.6,"ciLow":0.72,"ciHigh":3.25}]}
