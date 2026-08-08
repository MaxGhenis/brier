# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: sba.disaster.loan_program.charge_off_amount
- period: 2026
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "sba-disaster-loan-program-charge-off-amount-fy2026"
- country: "US"
- targetUnit: "usd"
- dataPointId: "sba.disaster.loan_program.charge_off_amount.2026.first_print"
- resolutionDate: "2028-12-31"
- resolutionDateBasis: "resolve-by-bound"
- expectedReleaseWindow: {"end": "2028-12-31", "start": "2026-10-01"}
- sourceBinding: {"adapter": "sba-loan-program-performance-pdf", "allowedHosts": ["legacy.sba.gov", "www.sba.gov"], "expectedReleaseWindow": {"end": "2028-12-31", "start": "2026-10-01"}, "field": "Disaster / Disaster", "releasePolicy": "first_print", "sourceSeriesId": "sba.disaster.loan_program.charge_off_amount", "sourceUrl": "https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance", "table": "Table 5 - Charge Off Amount by Program", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-08-3712ecd491933ff0b63b1afda38ca028e9101ec5afca669293cb07ee3ce9984a.json"
- targetContentHash: "3712ecd491933ff0b63b1afda38ca028e9101ec5afca669293cb07ee3ce9984a"
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
daaf6f9c13154bd26a5e66a7bc89d5903f82ee81bc82a16f5f4eff6235005441

# Draft forecast response
{"slug":"sba-disaster-loan-program-charge-off-amount-fy2026","country":"US","type":"data","title":"SBA Disaster loan charge-offs FY2026","question":"What will the SBA first print for Table 5, Charge Off Amount by Program, Disaster / Disaster, fiscal year 2026, be in dollars?","unit":"usd","pointEstimate":258333333,"ciLow":85714286,"ciHigh":575000000,"confidence":0.8,"resolutionDate":"2028-12-31","resolutionSource":"Official SBA Loan Program Performance report","resolutionSourceUrl":"https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance","resolutionRule":"Resolve to the first official SBA Loan Program Performance Table 5 - Charge Off Amount by Program print for fiscal year 2026, field Disaster / Disaster, in dollars as printed. Use the first print only; do not replace it with later data-update revisions. The 2028-12-31 resolutionDate is the registered Thesis resolve-by bound, not a scheduled SBA release date.","dataPointId":"sba.disaster.loan_program.charge_off_amount.2026.first_print","historicalContext":[{"label":"FY2022 official current-vintage Disaster charge-off amount","value":180342594},{"label":"FY2023 official current-vintage Disaster charge-off amount","value":322632623},{"label":"FY2024 official current-vintage Disaster charge-off amount","value":299971326},{"label":"FY2025 Q3 partial Disaster charge-off amount","value":107714599}],"drivers":["Recent completed Disaster charge-offs are elevated versus 2016-2021 but below the COVID EIDL distortion in the Disaster subtotal.","FY2025 partial Disaster charge-offs of 107714599 through 2025-06-30 imply full-year risk near but below FY2023-FY2024 if seasonality is ordinary.","Disaster UPB rose to 11976493088 by FY2025 Q3, supporting a higher dollar base than pre-2022 years.","FY2025 Q3 gross approvals of 5266748331 add future exposure, but charge-offs usually lag approvals."],"sourceContext":["https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance","https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip","https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip#WebsiteReports_FY25Q3/WDS_ChargeOffAmount_Report_20250630.pdf","https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip#WebsiteReports_FY25Q3/WDS_ChargeOffRates_Report_20250630.pdf","https://legacy.sba.gov/sites/default/files/2025-09/WebsiteReports_FY25Q3.zip#WebsiteReports_FY25Q3/WDS_UPB_Report_20250630.pdf"],"runAt":"2026-08-08T10:30:19Z","thresholdLadder":{"thresholds":[50000000,100000000,150000000,200000000,250000000,275000000,300000000,350000000,400000000,500000000,650000000,900000000],"cumulativeProbabilities":[0.05,0.12,0.25,0.38,0.48,0.54,0.6,0.7,0.78,0.87,0.93,0.97]},"reasoning":[{"kind":"heading","text":"SBA Disaster loan charge-off amount FY2026 first print"},{"kind":"text","text":"Framing and exact resolver: the target is SBA Loan Program Performance Table 5 - Charge Off Amount by Program, row Disaster under the Disaster section, fiscal year 2026 first print, unit dollars. I keep resolutionSourceUrl byte-equal to the registered methodology announcement URL and use 2028-12-31 as the Thesis lab resolve-by bound, not as an inferred SBA release date."},{"kind":"tool","tool":"thesis_announcement_fetch.fetch_official_announcement","call":"fetch_official_announcement exact registered URL https://legacy.sba.gov/document/report-small-business-administration-loan-program-performance","result":"Fetched official announcement/landing page with HTTP 200, 37099 response bytes, and response SHA-256 5a77a6bb8e74afdefcffd588fb37cab831ca69385b69d6911b900a99efaede64; the page advertises tables with data through June 30, 2025 and links the FY25Q3 package."},{"kind":"tool","tool":"official.lookup","call":"Downloaded SBA FY25Q3 Loan Program Performance ZIP and extracted WDS_ChargeOffAmount_Report_20250630.pdf Table 5.","result":"Fetched current official vintage as of 2025-06-30: Disaster / Disaster charge-off amounts were 180342594 in FY2022, 322632623 in FY2023, 299971326 in FY2024, and 107714599 for partial FY2025 through 2025-06-30."},{"kind":"tool","tool":"official.lookup","call":"Extracted SBA WDS_ChargeOffRates_Report_20250630.pdf Table 9 for the same Disaster / Disaster variant.","result":"Fetched same-variant charge-off rates: Disaster / Disaster was 1.97% in FY2022, 3.44% in FY2023, 3.06% in FY2024, and 0.90% for partial FY2025 through 2025-06-30."},{"kind":"tool","tool":"official.lookup","call":"Extracted SBA WDS_UPB_Report_20250630.pdf Table 1 and WDS_GrossApproval_Report_20250630.pdf Table 2 for Disaster / Disaster exposure context.","result":"Fetched same-program exposure context: Disaster / Disaster UPB was 9155822926 in FY2022, 9379479606 in FY2023, 9789692235 in FY2024, and 11976493088 for partial FY2025; gross approvals were 2336141093 in FY2022, 3272486099 in FY2023, 1832895854 in FY2024, and 5266748331 for partial FY2025."},{"kind":"text","text":"Reference class/base rate: I use the current official SBA vintage, not FRED or a catalog forecast, because no later revised-methodology print for this registered target exists. The completed FY2016-FY2024 Disaster / Disaster charge-off amounts span 18405594 to 322632623, with the most relevant recent completed values 180342594, 322632623, and 299971326; FY2025 is only a partial value at 107714599 through June 30, 2025."},{"kind":"text","text":"Variant discipline: every historical anchor is the Disaster / Disaster row, excluding COVID EIDL and excluding the Disaster subtotal, because the resolver field is Disaster / Disaster rather than aggregate Disaster programs."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent completed official reference class centered near the FY2022-FY2024 values 180342594, 322632623, and 299971326. Level effect is positive from UPB rising to 11976493088 in partial FY2025; momentum effect is mixed because FY2025 charge-offs are only 107714599 through three quarters while FY2024 was 299971326; one-off/policy effect allows large disaster-cohort charge-offs but excludes COVID EIDL; interval method is threshold-ladder interpolation anchored by the FY2016-FY2024 completed range and the FY2025 partial print. I put the median below FY2023-FY2024 but above FY2022, with 80% bounds covering a low normalization year and a high stress year."},{"kind":"math","text":"Ladder: P(X <= 50000000) = 0.05; P(X <= 100000000) = 0.12; P(X <= 150000000) = 0.25; P(X <= 200000000) = 0.38; P(X <= 250000000) = 0.48; P(X <= 275000000) = 0.54; P(X <= 300000000) = 0.60; P(X <= 350000000) = 0.70; P(X <= 400000000) = 0.78; P(X <= 500000000) = 0.87; P(X <= 650000000) = 0.93; P(X <= 900000000) = 0.97. Linear interpolation gives 10th percentile at 85714286, median at 258333333, and 90th percentile at 575000000."},{"kind":"text","text":"Counter-considerations: upside risk is a delayed charge-off wave from the larger FY2025 Disaster approval and UPB base, which would land above the interval if FY2026 charge-off rates resemble or exceed FY2023-FY2024 while balances keep expanding. Downside risk is continued low observed FY2025 runoff and recoverability improvements, which would land below the interval if FY2026 resembles FY2021 or the early FY2025 pace. An outside the interval outcome is most plausible from a major disaster-loan cohort accounting change or unexpectedly severe liquidation cycle."},{"kind":"forecast","point":258333333,"ciLow":85714286,"ciHigh":575000000}]}
