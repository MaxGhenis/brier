# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: usda.fns.snap.maximum_allotment.household_size_4.48dc.fy2027
- period: FY2027
- conditional: null

# Rubric
Check these items and name concrete fixes when needed:
1. Exact resolver, source, first-print rule, and resolution date.
2. Base-rate or persistence prior stated before inside-view updates.
3. Time-series/model prior used or explicitly ruled out.
4. Current evidence justifies material movement from the prior.
5. Interval size comes from realized volatility or explicit uncertainty.
6. Tail scenarios are concrete and tied to the target.
7. Point, interval, final forecast step, and JSON fields are coherent.
8. No leakage, subjective resolver, or unit ambiguity.

# Required response
Return JSON only, with this shape:
{
  "summary": "one sentence",
  "requiredFixes": [
    {
      "rubricItem": "resolver|base_rate|model_prior|update|interval|tails|coherence|leakage",
      "severity": "warning|blocking",
      "summary": "specific issue",
      "actionRequested": "specific change requested"
    }
  ],
  "optionalSuggestions": ["short suggestions"]
}

# Original forecaster prompt hash material
364489524df2e85ea759881e81d308ed576f8ba95f9ef16bb6067bc23c6ba02a

# Draft forecast response
{"slug":"snap-max-allotment-family-4-fy2027","country":"US","type":"data","title":"SNAP family-4 max allotment FY2027","question":"What will the first USDA FNS FY2027 maximum monthly SNAP allotment for a household of 4 in the 48 contiguous states and DC be, in dollars per month?","unit":"usd","pointEstimate":1021,"ciLow":1000,"ciHigh":1055,"confidence":0.8,"resolutionDate":"2026-09-30","resolutionSource":"USDA Food and Nutrition Service SNAP FY2027 Cost-of-Living Adjustments","resolutionSourceUrl":"https://www.fns.usda.gov/snap/fy-2027-cola","resolutionRule":"Resolve to the first USDA FNS FY2027 SNAP COLA table or memorandum value for maximum monthly allotments, household size 4, 48 contiguous states and DC. Use the first posted FY2027 table even if later revised; record the dollar amount as published, with no conversion beyond treating it as dollars per month. If the table is posted before 2026-09-30, that first post still governs.","dataPointId":"usda.fns.snap.maximum_allotment.household_size_4.48dc.fy2027.first_print","historicalContext":[{"label":"FY2023 official first print","value":939},{"label":"FY2024 official/catalog reference","value":973},{"label":"FY2025 official/catalog reference","value":975},{"label":"FY2026 catalog anchor","value":994}],"drivers":["June 2026 Thrifty Food Plan cost","Food-at-home CPI running 2.7 percent year over year in May 2026","ERS 2026 food-at-home forecast midpoint 2.8 percent","Annual FNS COLA table effective October 1","Low but nonzero policy-change risk around TFP rules"],"sourceContext":["https://www.fns.usda.gov/snap/fy-2023-cola","https://www.usda.gov/guidance-documents/snap/fns/snap-fy-2024-cost-living-adjustments-0","https://www.usda.gov/guidance-documents/snap/fns/snap-fy-2025-cost-living-adjustments","https://www.bls.gov/news.release/cpi.nr0.htm","https://www.ers.usda.gov/data-products/food-price-outlook/summary-findings","https://www.ecfr.gov/current/title-7/subtitle-B/chapter-II/subchapter-C/part-273/subpart-D/section-273.10"],"runAt":"2026-06-27T23:13:24Z","reasoning":[{"kind":"heading","text":"SNAP FY2027 maximum allotment, household of 4"},{"kind":"text","text":"Resolver is the first USDA FNS FY2027 SNAP COLA table for the household-size-4 maximum monthly allotment in the 48 contiguous states and DC. The repo already registers the canonical slug snap-max-allotment-family-4-fy2027 and target date 2026-09-30, so I reuse that rather than creating a near-duplicate."},{"kind":"tool","tool":"local.repo","call":"rg and sed over forecast-cells.ts and ledger-targets.generated.ts for the target registration","result":"Fetched canonical slug snap-max-allotment-family-4-fy2027; catalog values include FY2024 973, FY2025 975, FY2026e 994, prior point 1010, prior CI 975 to 1045, and ledger resolutionDate 2026-09-30."},{"kind":"tool","tool":"official.fns.lookup","call":"Open USDA FNS SNAP FY2023 COLA page for an official inline reference point and effective-date mechanics","result":"Fetched FY2023 memorandum date August 9, 2022, effective Oct. 1, 2022, and household-of-4 48 states/DC maximum allotment 939 dollars."},{"kind":"tool","tool":"official.usda.guidance.lookup","call":"Open USDA Guidance Portal entries for FY2024 and FY2025 SNAP COLA issue dates","result":"Fetched FY2024 issued date August 3, 2023 and FY2025 issued date August 2, 2024; FNS pages show FY2024 page updated March 16, 2026 and FY2025 page updated March 6, 2026."},{"kind":"tool","tool":"official.ecfr.lookup","call":"Open 7 CFR 273.10 maximum SNAP allotment rule","result":"Fetched 7 CFR 273.10 current as of 6/24/2026; maximum allotments are adjusted annually, posted in an FNS web table, effective October 1, and based on 100% of the preceding June TFP rounded down to the nearest lower dollar."},{"kind":"tool","tool":"official.bls.lookup","call":"Open BLS May 2026 CPI release for current food-at-home momentum","result":"Fetched BLS May 2026 CPI: all items +0.5 percent monthly and +4.2 percent year over year; food at home +0.1 percent monthly and +2.7 percent year over year; June 2026 CPI scheduled for July 14, 2026."},{"kind":"tool","tool":"official.ers.lookup","call":"Open USDA ERS June 2026 Food Price Outlook summary","result":"Fetched ERS June 2026 forecast: food-at-home prices predicted +2.8 percent in 2026 with 95 percent prediction interval 1.4 to 4.4 percent; all food +3.2 percent with interval 2.2 to 4.2 percent."},{"kind":"text","text":"Base-rate/reference class: recent first-print household-of-4 values moved 939 to 973 to 975, and the local FY2026 anchor is 994. The year-to-year changes are about +3.6 percent, +0.2 percent, and +1.9 percent, with the current inflation evidence closer to the upper part of that recent range than to the FY2025 near-flat COLA."},{"kind":"text","text":"Level, momentum, and mechanism: the best level anchor is the FY2026 catalog anchor of 994 dollars. Current grocery inflation has not collapsed; BLS shows 2.7 percent year-over-year food-at-home inflation in May 2026 and ERS puts 2026 food-at-home inflation at 2.8 percent. The eCFR rule makes this a mechanical TFP/June-cost update unless Congress or USDA changes the TFP basis before the FY2027 table."},{"kind":"math","text":"Point: 994 dollars FY2026 anchor x 1.027 May food-at-home momentum = 1020.8, rounded to about 1021 dollars as an expected first-print value. Interval: apply ERS-like food-at-home uncertainty and policy/mechanical rounding around the FY2026 anchor: low roughly 994 x 1.006 = 1000, high roughly 994 x 1.061 = 1055, allowing extra upside for June food/TFP category strength and modest downside for a cooler June or lower TFP basket movement."},{"kind":"text","text":"Counter-consideration: outside the lower bound if June 2026 TFP costs soften sharply or legislation freezes/rebases SNAP maximum allotments before the FY2027 table; outside the upper bound if a fresh TFP reevaluation, commodity shock, or food-at-home spike pushes the June TFP several points above current CPI signals."},{"kind":"forecast","point":1021,"ciLow":1000,"ciHigh":1055}]}
