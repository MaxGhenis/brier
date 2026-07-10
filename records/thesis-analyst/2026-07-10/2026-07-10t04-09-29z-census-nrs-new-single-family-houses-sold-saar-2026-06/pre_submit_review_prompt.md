# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: census.nrs.new_single_family_houses_sold_saar
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-new-home-sales-saar-june-2026"
- targetUnit: "thousands"
- dataPointId: "census.nrs.new_single_family_houses_sold_saar.2026_06.first_print"
- resolutionSourceUrl: "https://www.census.gov/construction/nrs/current/index.html"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.census.gov"], "expectedReleaseWindow": {"end": "2026-07-24", "start": "2026-07-24"}, "field": "Sales of new single-family houses; United States; seasonally adjusted annual rate", "releasePolicy": "first_print", "sourceSeriesId": "NRS new single-family houses sold United States seasonally adjusted annual rate", "sourceUrl": "https://www.census.gov/construction/nrs/current/index.html", "table": "Monthly New Residential Sales, Table 1. New Houses Sold and For Sale", "transform": {"factor": 1, "operation": "identity"}}
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
9875b56d31cb7b5318c5ec8f05b73a1ddede285804a5a782c48a50945405c9ff

# Draft forecast response
{"slug":"us-new-home-sales-saar-june-2026","country":"US","type":"data","title":"US New Home Sales SAAR, June 2026","question":"What will the U.S. Census Bureau/HUD first-print estimate be for sales of new single-family houses in the United States in June 2026, seasonally adjusted annual rate, in thousands?","unit":"thousands","pointEstimate":603,"ciLow":517,"ciHigh":689,"confidence":0.8,"resolutionDate":"2026-07-24","resolutionSource":"U.S. Census Bureau and HUD Monthly New Residential Sales release, Table 1a","resolutionSourceUrl":"https://www.census.gov/construction/nrs/current/index.html","resolutionRule":"Resolve to the first-print United States value for Sales of new single-family houses, seasonally adjusted annual rate, in Monthly New Residential Sales Table 1a for June 2026, rounded as Census reports it in thousands of units. Use the July 24, 2026 first release only; ignore later revisions or historical-table updates.","dataPointId":"census.nrs.new_single_family_houses_sold_saar.2026_06.first_print","historicalContext":[{"label":"2026-05 latest first print SAAR","value":580},{"label":"2026-04 revised SAAR in May release","value":626},{"label":"2026-03 revised SAAR in May release","value":664},{"label":"2025-06 revised SAAR in May release","value":665},{"label":"2026 year-to-date NSA sales through May","value":275}],"drivers":["May 2026 new-home sales fell to 580 thousand SAAR from 626 thousand in April","High 10.3 months' supply points to weak builder absorption","2026 year-to-date not seasonally adjusted sales were 275 thousand, 7.0 percent below 2025","Single-family starts and permits were roughly stable in May, limiting downside from construction flow","Large monthly sampling and revision noise supports a wide interval"],"sourceContext":["https://www.census.gov/construction/nrs/current/index.html","https://www.census.gov/construction/nrs/pdf/newressales.pdf","https://www.census.gov/construction/soc/schedule.html","https://www.census.gov/construction/nrc/current/index.html"],"runAt":"2026-07-10T04:09:45Z","reasoning":[{"kind":"heading","text":"June 2026 US New Home Sales SAAR Forecast"},{"kind":"text","text":"Framing and exact resolver: this forecasts the Census/HUD Monthly New Residential Sales first print for June 2026, Table 1a seasonally adjusted annual rate, United States sales of new single-family houses, in thousands. This uses the same SAAR variant for every anchor and historical value."},{"kind":"tool","tool":"official.lookup","call":"Opened Census New Residential Sales current release page for May 2026.","result":"Fetched May 2026 new single-family houses sold at 580,000 SAAR, April 2026 at 626,000 SAAR, May 2025 at 622,000 SAAR, inventory at 496,000, and months' supply at 10.3."},{"kind":"tool","tool":"official.lookup","call":"Opened Census/HUD May 2026 New Residential Sales PDF, Table 1a.","result":"Fetched Table 1a SAAR United States sales history: 2025 May 622, June 665, July 648, August 698, September 714, October 652, November 757, December 723; 2026 January 576, February 630, March 664, April 626, May 580, all in thousands."},{"kind":"tool","tool":"official.lookup","call":"Opened Census Survey of Construction release schedule.","result":"Fetched official schedule showing June 2026 survey month: New Residential Construction release July 17, 2026 and New Residential Sales release July 24, 2026 at 10:00 a.m."},{"kind":"tool","tool":"official.lookup","call":"Opened Census New Residential Construction May 2026 release for related builder-flow indicators.","result":"Fetched May 2026 building permits at 1,413,000 SAAR, total housing starts at 1,177,000 SAAR, single-family starts at 882,000 SAAR, and single-family permits at 886,000 SAAR."},{"kind":"text","text":"Base rate/reference class: recent same-series SAAR levels from May 2025 through May 2026 averaged about 659 thousand before the latest drop, while the first five months of 2026 averaged 615 thousand. The latest 580 thousand print is below both, so persistence alone looks too low but the elevated 10.3 months' supply argues against full reversion toward the 2025 average."},{"kind":"math","text":"Prior/update/interval: persistence prior is latest same-variant SAAR of 580. Historical sample is the 13 fetched monthly Table 1a SAAR values from 2025-05 through 2026-05. Adjustment components: +25 for partial rebound after a 46 thousand May decline and mean reversion toward the 2026 year-to-date SAAR average near 615, +8 for June 2025 being 43 above May 2025 in the same series, -10 for high 10.3 months' supply and weak year-to-date NSA sales, giving 580 + 25 + 8 - 10 = 603. Successive changes are +43, -17, +50, +16, -62, +105, -34, -147, +54, +34, -38, -46; sample sigma = 67.4 thousand, so 80% half-width is roughly 1.28*sigma = 86.3 thousand. Rounded interval: 603 - 86 = 517 and 603 + 86 = 689."},{"kind":"text","text":"Counter-consideration: upside risk is a builder-incentive rebound like February-March 2026 or November 2025, which would land above the interval if June prints above 689 thousand. Downside risk is another demand shock from mortgage-rate pressure or cancellations, which would land below the interval if sales fall below 517 thousand."},{"kind":"forecast","point":603,"ciLow":517,"ciHigh":689}]}
