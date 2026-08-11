# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fns.wic.total_participation
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "wic-participation-august-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "fns.wic.total_participation.2026-08.first_print"
- expectedReleaseWindow: {"end": "2026-11-26", "start": "2026-11-18"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-11-26", "start": "2026-11-18"}, "field": "fns.wic.total_participation", "releasePolicy": "first_print", "sourceSeriesId": "fns.wic.total_participation", "sourceUrl": "https://www.fns.usda.gov/pd/wic-program", "table": "USDA Food and Nutrition Service WIC Data Tables", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-11-feba7a565069c13feaf303a049c80f5809cbf7568d04215f7350943843d58995.json"
- targetContentHash: "feba7a565069c13feaf303a049c80f5809cbf7568d04215f7350943843d58995"
- registrationCommit: "e8c13ea71f583ab7105a64de5fe4c8594cfcb6d0"
- registeredAtUtc: "2026-08-11T12:50:27Z"
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
78ab36dbe75d3814b51c6596062766d1a9558013908e0944a66ad01ebe7f12f3

# Draft forecast response
{"slug":"wic-participation-august-2026","country":"US","type":"data","title":"US WIC participation, August 2026","question":"What will USDA FNS first report as total WIC participation for August 2026, not seasonally adjusted, converted from the official participant count to millions?","unit":"millions","pointEstimate":6.96,"ciLow":6.83,"ciHigh":7.09,"confidence":0.8,"resolutionDate":"2026-11-26","resolutionSource":"USDA Food and Nutrition Service WIC Data Tables","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve using the first official USDA FNS WIC Data Tables print for August 2026 total participation, specifically the national total in the WIC PROGRAM: TOTAL PARTICIPATION or successor WIC monthly participation table. Convert the official participant count to millions and do not use later revisions or corrections unless the first posted file is unavailable and FNS replaces it before a value can be recorded.","dataPointId":"fns.wic.total_participation.2026-08.first_print","historicalContext":[{"label":"Apr 2025 initial total participation","value":6.856889},{"label":"Mar 2025 preliminary total participation","value":6.848436},{"label":"Aug 2024 total participation","value":6.830287},{"label":"FY 2024 annual average participation","value":6.704329}],"drivers":["WIC participation was still running above year-earlier levels in early 2025","Spring-to-late-summer seasonality has recently added about 0.1 million participants","FY 2025 average participation around 6.9 million supports a high-6.9 million level prior","Birth demographics and caseload normalization limit further upside","Federal funding continuity through FY 2026 reduces disruption risk before August 2026"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://fns-prod.azureedge.us/sites/default/files/resource-files/37wic-monthly-7.pdf","https://fns-prod.azureedge.us/sites/default/files/resource-files/27wilatest-7.pdf","https://ers.usda.gov/topics/food-nutrition-assistance/wic-program","https://www.fns.usda.gov/data-research/data-release-calendar"],"runAt":"2026-08-11T13:19:05Z","reasoning":[{"kind":"heading","text":"Forecast for August 2026 WIC total participation"},{"kind":"text","text":"Framing and exact resolver: this is the USDA FNS WIC total participation series for August 2026, first print only, not seasonally adjusted. I use the WIC Data Tables national/state participation totals and express the final answer in millions of participants."},{"kind":"tool","tool":"official.lookup","call":"Opened the USDA FNS WIC Data Tables page and followed the national monthly WIC table link.","result":"The WIC page listed monthly data and the national monthly PDF reported FY 2024 annual average total participants of 6,704,329, FY 2023 total participants of 6,575,977, and FY 2022 total participants of 6,260,190."},{"kind":"tool","tool":"official.lookup","call":"Fetched the USDA FNS national monthly WIC Participation and Costs PDF for recent monthly totals.","result":"Recent national total participants were Aug 2024 6,830,287; Sep 2024 6,838,250; Oct 2024 6,907,665; Nov 2024 6,829,237; Dec 2024 6,784,625; Jan 2025 6,821,051; Feb 2025 6,800,868; Mar 2025 6,848,436; Apr 2025 6,856,889."},{"kind":"tool","tool":"official.lookup","call":"Fetched the USDA FNS latest-month WIC PROGRAM: TOTAL PARTICIPATION PDF to check the same initial-print national total.","result":"The latest-month table showed TOTAL Apr 2024 6,722,042, Mar 2025 6,848,436, and Apr 2025 initial 6,856,889, with Apr 2025 up 0.1% from Mar 2025 and up 2.0% from Apr 2024."},{"kind":"tool","tool":"official.lookup","call":"Checked the FNS release-calendar target window and stable WIC source page for the registered first-print date basis.","result":"The registered official FNS WIC release window for the August 2026 target is 2026-11-18 to 2026-11-26, so the bound resolution date is 2026-11-26; the same source family currently reports Apr 2025 initial participation of 6,856,889."},{"kind":"text","text":"Reference class and base rate: for a monthly level series like WIC total participation, the best base rate is persistence plus recent month-to-month dispersion in the same USDA FNS table. The visible FNS sequence is stable around 6.8 to 6.9 million, while the Apr 2025 year-over-year gain of 2.0% and FY 2025 average participation around 6.9 million argue against reverting to the lower FY 2024 average."},{"kind":"math","text":"Prior/update/interval: persistence prior starts from Apr 2025 initial 6.856889 million; seasonal update uses Apr-to-Aug 2024 gain of 6.830287 - 6.722042 = 0.108245 million, implying about 6.965 million for a comparable August level; policy/funding continuity adds 0.00 million, while slowing births/caseload normalization subtracts about 0.005 million, giving point 6.96 million. For the interval, successive monthly changes from Aug 2024 through Apr 2025 are +0.007963, +0.069415, -0.078428, -0.044612, +0.036426, -0.020183, +0.047568, +0.008453 million; sigma = 0.049 million. A one-month 80% half-width is 1.28*sigma = 0.063 million; I widen to about 0.13 million for release-lag, seasonality, and August 2026 policy/demographic uncertainty, about 2.1x the one-month half-width, yielding 6.83 to 7.09 million."},{"kind":"text","text":"Counter-consideration: upside risk would come from stronger outreach, higher eligibility take-up, or state reporting that keeps the summer caseload above the recent seasonal path and would land above the interval. Downside risk would come from funding disruption, administrative churn, or a sharper child/birth-cohort decline, which could push the first print below the interval. Outside the interval would require roughly a 0.13 million miss from the persistence-plus-seasonality path."},{"kind":"forecast","point":6.96,"ciLow":6.83,"ciHigh":7.09}]}
