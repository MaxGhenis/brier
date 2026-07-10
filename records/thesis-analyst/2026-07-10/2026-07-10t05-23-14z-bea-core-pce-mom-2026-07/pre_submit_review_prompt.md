# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bea.core_pce.mom
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-core-pce-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "us.bea.core_pce.mom_sa.2026-07"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.bea.gov"], "expectedReleaseWindow": {"end": "2026-09-03", "start": "2026-08-26"}, "field": "bea.core_pce.mom", "releasePolicy": "first_print", "sourceSeriesId": "bea.core_pce.mom", "sourceUrl": "https://www.bea.gov/data/personal-consumption-expenditures-price-index-excluding-food-and-energy", "table": "U.S. Bureau of Economic Analysis, Personal Income and Outlays", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-32674225cad71e81ea6b8ff485cc40f0187cf9a4186ed313499c427655355a93.json"
- targetContentHash: "32674225cad71e81ea6b8ff485cc40f0187cf9a4186ed313499c427655355a93"
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
64a70e0b352461531c14453cffe8ec910a1a95fde4c46c6b5a84f64aa444ac8c

# Draft forecast response
{"slug":"us-core-pce-mom-july-2026","country":"US","type":"data","title":"US Core PCE MoM, July 2026","question":"U.S. Bureau of Economic Analysis core personal consumption expenditures price index excluding food and energy, seasonally adjusted percent change from the preceding month, July 2026 first print.","unit":"percent_growth","pointEstimate":0.28,"ciLow":0.2,"ciHigh":0.36,"confidence":0.8,"resolutionDate":"2026-08-26","resolutionSource":"U.S. Bureau of Economic Analysis, Personal Income and Outlays","resolutionSourceUrl":"https://www.bea.gov/data/personal-consumption-expenditures-price-index-excluding-food-and-energy","resolutionRule":"Resolve to the first BEA publication of the seasonally adjusted monthly percent change from the preceding month for the PCE price index excluding food and energy for July 2026, as published in Personal Income and Outlays / NIPA Table 2.8.7 or its linked official BEA release table. Use the first print only; do not revise for later annual, benchmark, or routine revisions. Record in percent growth, matching BEA rounding where the first print is displayed.","dataPointId":"us.bea.core_pce.mom_sa.2026-07","historicalContext":[{"label":"2026-05 implied MoM from PCEPILFE index","value":0.3200505911295837},{"label":"2026-04 implied MoM from PCEPILFE index","value":0.25049674122294974},{"label":"2026-03 implied MoM from PCEPILFE index","value":0.29621358395170994},{"label":"2026-02 implied MoM from PCEPILFE index","value":0.3939122649955218}],"drivers":["Recent core PCE monthly index changes imply a roughly 0.32 percent four-month base rate but with May elevated versus April.","The BEA exact series page shows year-over-year core PCE inflation at 3.4 percent in May 2026, up from 3.3 percent in April and March.","Core CPI-type signals and oil-driven headline pressure argue against using headline energy strength directly because this target excludes food and energy.","Two-month-ahead uncertainty remains dominated by service-price and financial-services components rather than the release calendar."],"sourceContext":["https://www.bea.gov/news/schedule","https://www.bea.gov/data/personal-consumption-expenditures-price-index-excluding-food-and-energy","https://fred.stlouisfed.org/series/PCEPILFE"],"runAt":"2026-07-10T05:23:39Z","reasoning":[{"kind":"heading","text":"US core PCE month-over-month forecast for July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this targets the BEA seasonally adjusted PCE price index excluding food and energy, July 2026, monthly percent change from the preceding month, first print. The relevant BEA account code visible through the FRED mirror is DPCCRG, and the BEA linked monthly table is Table 2.8.7, Percent Change From Preceding Period in Prices for Personal Consumption Expenditures by Major Type of Product."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA release schedule for the July 2026 Personal Income and Outlays release date.","result":"BEA schedule lists Personal Income and Outlays, July 2026 on August 26, 2026 at 8:30 AM; the same schedule page was last modified on 7/10/26."},{"kind":"tool","tool":"official.lookup","call":"Checked BEA core PCE exact series page for recent published year-over-year values and release metadata.","result":"BEA exact series page reports core PCE price index excluding food and energy year-over-year values: May 2026 +3.4%, April 2026 +3.3%, March 2026 +3.3%, February 2026 +3.0%; current release June 25, 2026 and next release July 30, 2026."},{"kind":"tool","tool":"fred.lookup","call":"Checked FRED PCEPILFE, a public mirror whose source is the U.S. Bureau of Economic Analysis, for recent seasonally adjusted index values used to calculate same-variant monthly changes.","result":"PCEPILFE index values, seasonally adjusted, 2017=100: May 2026 130.082, Apr 2026 129.667, Mar 2026 129.343, Feb 2026 128.961, Jan 2026 128.455; updated Jun 25, 2026 7:43 AM CDT."},{"kind":"tool","tool":"calculator","call":"Converted recent BEA/FRED core PCE index values into monthly percent changes.","result":"Computed monthly percent changes: Feb 2026 0.3939122649955218, Mar 2026 0.29621358395170994, Apr 2026 0.25049674122294974, May 2026 0.3200505911295837; four-month mean 0.3151682953249413."},{"kind":"text","text":"Reference class/base rate: because this is a change-rate target, I use recent same-variant seasonally adjusted core PCE monthly percent changes as the base rate rather than year-over-year values or headline PCE. The four observed monthly changes average about 0.315 percent, while the latest BEA page shows the year-over-year rate rising to 3.4 percent, so the outside view is elevated but not accelerating every month."},{"kind":"math","text":"Prior/update/interval: persistence prior from recent same-variant BEA/FRED PCEPILFE monthly changes is 0.315 percent using Feb-May 2026. Adjustment components: -0.04 for mean reversion from May's elevated 0.320 percent and April's softer 0.250 percent, +0.01 for still-high 3.4 percent year-over-year core PCE and service-price stickiness, -0.005 for excluding direct food and energy pass-through, giving a rounded point of 0.28. Interval method uses the values themselves for this change-rate series: sigma = 0.060 from the four computed monthly changes; 1.28*sigma = 0.077, so 0.28 +/- 0.077 implies about [0.20, 0.36] after practical BEA-display rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a July rebound in core services, portfolio-management fees, medical services, or tariff-sensitive goods that would land above the interval near 0.37 percent or higher. Downside risk is a broad goods deflation month plus cooler rent and medical-service readings that would land below the interval near 0.19 percent or lower. A large one-month methodology or seasonal-factor surprise would be outside the interval, but I do not treat that as the central case."},{"kind":"forecast","point":0.28,"ciLow":0.2,"ciHigh":0.36}]}
