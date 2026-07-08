# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ssa.ssi.recipients_aged_65_plus
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ssi-recipients-aged-65-plus-june-2026"
- targetUnit: "thousands"
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
29dc6c4443d692c9b6a63e44d968b44d71dbd78d6c32e9d070d8f7159ac9060e

# Draft forecast response
{"slug":"ssi-recipients-aged-65-plus-june-2026","country":"US","type":"data","title":"SSI recipients aged 65+ June 2026","question":"Social Security Administration SSI Monthly Statistics Table 1 number of recipients, all federally administered payments, Total row, Age 65 or older column, June 2026, first print","unit":"thousands","pointEstimate":2503.1,"ciLow":2496.2,"ciHigh":2510,"confidence":0.8,"resolutionDate":"2026-07-31","resolutionSource":"Social Security Administration SSI Monthly Statistics","resolutionSourceUrl":"https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-06/table01.html","resolutionRule":"Resolve to the first published June 2026 value in SSA SSI Monthly Statistics Table 1, All Federally Administered Payments, Number of recipients, row Total, column Age 65 or older. SSA publishes whole recipient counts; convert to thousands by dividing by 1,000 and report to the same 0.001-thousand precision implied by whole recipients. Use the first official print only and ignore later revisions or returned-check adjustments after the first June 2026 table is posted. SSA's public schedule provides month-level monthly timing rather than a specific day; 2026-07-31 is the catalog latest expected resolution by-date for the June 2026 monthly publication, not a claimed exact release day.","dataPointId":"ssa.ssi.recipients_aged_65_plus.2026_06.first_print","historicalContext":[{"label":"2026-05 latest first-print proxy","value":2501.549},{"label":"2026-04","value":2500.422},{"label":"2026-03","value":2502.133},{"label":"2026-02","value":2506.79},{"label":"2026-01","value":2509.113},{"label":"2025-06 year-earlier June","value":2484.16}],"drivers":["Aged-65-plus SSI caseload has risen year over year","Early-2026 level drifted down from January to April before a small May rebound","Same-variant May-to-June 2025 change was positive but modest","No new benefit-level policy shock is assumed for June 2026"],"sourceContext":["https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/index.html","https://www.ssa.gov/policy/pub_schedule.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-05/table01.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-04/table01.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-03/table01.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-02/table01.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-01/table01.html","https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2025-06/table01.html"],"runAt":"2026-07-08T20:13:39Z","reasoning":[{"kind":"heading","text":"SSI aged-65-plus recipients, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this targets the NSA administrative count in SSA SSI Monthly Statistics Table 1, All Federally Administered Payments, Number of recipients, row Total, Age 65 or older column. All anchors below use this same Table 1 variant, not Table 2 totals, federal-payment-only recipients, state-only recipients, or OASDI dual-entitlement counts."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics current index and SSA Publishing Schedule for release timing.","result":"Fetched timing evidence: current SSI Monthly Statistics page is May 2026 and states released June 2026; SSA Publishing Schedule lists SSI Monthly Statistics frequency as Monthly; run date is 2026-07-08; the schedule gives month-level timing but no exact June 2026 release day, so 2026-07-31 is used as the catalog latest expected by-date."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics May 2026 Table 1 for latest same-variant value.","result":"Fetched May 2026 Table 1 Total row Age 65 or older = 2,501,549 recipients, equal to 2501.549 thousand; all recipients = 7,322,937; aged eligibility category = 1,184,449."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics January through April 2026 Table 1 pages for recent same-year history.","result":"Fetched same-variant Age 65 or older counts: January 2026 = 2,509,113, February 2026 = 2,506,790, March 2026 = 2,502,133, April 2026 = 2,500,422 recipients, or 2509.113, 2506.790, 2502.133, 2500.422 thousand."},{"kind":"tool","tool":"official.lookup","call":"Opened SSA SSI Monthly Statistics May through December 2025 Table 1 pages for reference-class dispersion and seasonality.","result":"Fetched same-variant Age 65 or older counts: May 2025 = 2,482,524, June 2025 = 2,484,160, July 2025 = 2,487,107, August 2025 = 2,497,163, September 2025 = 2,508,702, October 2025 = 2,504,084, November 2025 = 2,506,451, December 2025 = 2,512,399 recipients."},{"kind":"text","text":"Base rate/reference class: the recent official-source class is monthly Table 1 aged-65-plus recipient levels from May 2025 through May 2026. The latest level, 2501.549 thousand, is 19.025 thousand above May 2025 but 7.564 thousand below January 2026; that argues for persistence with a small positive June seasonal/current adjustment rather than a large trend extrapolation."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2026 latest level 2501.549 thousand; historical sample = same-variant May 2025-May 2026 monthly levels; adjustment components = +1.636 thousand for the May-to-June 2025 seasonal move, +0.0 for policy mechanism because no June 2026 SSI eligibility/payment rule shock is assumed, and about -0.1 rounding/current-drift offset after the early-2026 decline, giving point 2501.549 + 1.636 - 0.085 = 2503.100 thousand. Interval method uses sample standard deviation of successive monthly changes from May 2025 to May 2026: changes were +1.636, +2.947, +10.056, +11.539, -4.618, +2.367, +5.948, -3.286, -2.323, -4.657, -1.711, +1.127 thousand; sigma = 5.392, half-width = 1.28*sigma = 6.902 thousand, so 80% interval = 2503.100 +/- 6.902 = [2496.198, 2510.002], rounded to 2496.2 to 2510.0 thousand."},{"kind":"text","text":"Counter-considerations: upside risk is a continuation of the May rebound plus faster aged inflows, which would land above the interval if June rises by more than about 8.5 thousand recipients from May. Downside risk is renewed terminations or returned-check downward adjustment in the first print, which would land below the interval if June falls by more than about 5.3 thousand from May. A policy or administrative cleanup affecting aged SSI eligibility would be the main outside the interval scenario."},{"kind":"forecast","point":2503.1,"ciLow":2496.2,"ciHigh":2510}]}
