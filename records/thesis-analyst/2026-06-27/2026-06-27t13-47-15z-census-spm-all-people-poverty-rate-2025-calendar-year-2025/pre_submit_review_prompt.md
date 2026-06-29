# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review only the draft forecast, the target spec, and public evidence cited in the draft. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: census.spm.all_people_poverty_rate.2025
- period: calendar year 2025
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
77a59c6f41e22a82d8583309bbb21022995b3188de84676820b84dc74074330f

# Draft forecast response
{"slug":"us-census-spm-all-people-poverty-rate-2025","country":"US","type":"data","title":"US SPM poverty rate, 2025","question":"What will the U.S. Census Bureau first report as the all-people Supplemental Poverty Measure poverty rate for calendar year 2025 in Poverty in the United States: 2025, Table B-2?","unit":"percent","pointEstimate":12.6,"ciLow":11.6,"ciHigh":13.8,"confidence":0.8,"resolutionDate":"2026-09-08","resolutionSource":"U.S. Census Bureau Poverty in the United States: 2025 first-release tables","resolutionSourceUrl":"https://www.census.gov/topics/income-poverty/supplemental-poverty-measure/data/tables.html","resolutionRule":"Resolve to the first Census Bureau published percentage for all people using the Supplemental Poverty Measure for calendar year 2025, normally Table B-2 in Poverty in the United States: 2025. Use the initially released value rounded to one decimal percentage point; ignore later errata, benchmark updates, or revised tables unless Census labels the original first print as withdrawn before public release.","dataPointId":"census.p60.spm.all_people_poverty_rate.2025.first_print","historicalContext":[{"label":"2024 first print","value":12.9},{"label":"2023 first print","value":12.9},{"label":"2022 first print","value":12.4},{"label":"2021 first print","value":7.8}],"drivers":["Recent SPM rate was flat at 12.9 percent in 2023 and 2024","No large 2025 federal child-tax-credit expansion comparable to 2021","Labor market stayed broadly expansionary but cooler than 2024","Inflation and housing costs still pressure SPM thresholds and necessary expenses","Benefit and tax-transfer mechanics likely keep the rate near the post-pandemic plateau"],"sourceContext":["https://www.census.gov/about/event-calendar.html","https://www.census.gov/topics/income-poverty/supplemental-poverty-measure/data/tables.html","https://www.census.gov/data/tables/2025/demo/income-poverty/p60-287.html","https://www2.census.gov/programs-surveys/demo/tables/p60/287/tableB-2.xlsx"],"runAt":"2026-06-27T13:47:40Z","reasoning":[{"kind":"heading","text":"Forecast for 2025 all-people SPM poverty rate"},{"kind":"text","text":"The target is the Census Bureau first print for calendar-year 2025 all people under the Supplemental Poverty Measure, not a later revised table and not the official poverty measure."},{"kind":"tool","tool":"official.lookup","call":"Checked the Census Bureau Event Calendar for the Income, Poverty, and Health Insurance release covering calendar-year 2025.","result":"Official Census event-calendar lookup identified the 2025 income, poverty, and health-insurance release date as 2026-09-08; the calendar page revision observed was 2026-01-29."},{"kind":"tool","tool":"official.lookup","call":"Opened the Census Bureau Supplemental Poverty Measure Data Tables page and latest Poverty in the United States table listing.","result":"Census listed Poverty in the United States: 2024 with release date 2025-09-09 and report number P60-287; the page linked Table B-2 for 2009 to 2024."},{"kind":"tool","tool":"official.lookup","call":"Used Census Table B-2 for the all-people SPM reference class.","result":"Fetched recent all-people SPM rates: 2024=12.9 percent, 2023=12.9 percent, 2022=12.4 percent, 2021=7.8 percent."},{"kind":"text","text":"Base-rate/reference-class anchor: the post-expiration transfer regime since 2022 has averaged about 12.7 percent across 2022, 2023, and 2024, making the latest plateau a better prior than the unusually low 2020 and 2021 pandemic-transfer years."},{"kind":"tool","tool":"official.lookup","call":"Checked Census Table B-series context around official and supplemental poverty tables for the latest release.","result":"The latest Census table page showed 2024 official poverty table A-1 and SPM tables B-2 through B-7; latest official poverty context was 2024=10.6 percent while SPM all-people was 2024=12.9 percent."},{"kind":"text","text":"Level and momentum: 2025 did not have a large new anti-poverty transfer shock, but real wage and employment conditions were not recessionary, so I expect only modest movement down from 12.9 rather than a return toward 2021's 7.8."},{"kind":"text","text":"Counter-consideration: if 2025 shelter and medical out-of-pocket adjustments run hotter than cash-income gains, or if survey income measurement weakens, the rate could stay near 13.5 or above despite continued employment growth."},{"kind":"math","text":"Point estimate: start from the 2022-2024 average (12.4+12.9+12.9)/3=12.73, subtract 0.1 for mild real-income gains and 0.0 to 0.1 for cooler-but-positive employment, rounded to 12.6. The 80% interval uses roughly +/-1.1 to +1.2 points around the point, widened on the upside for threshold and expense risk, giving 11.6 to 13.8."},{"kind":"text","text":"Upside scenario: a weaker 2025 CPS ASEC income print, higher necessary expenses, or reduced effective transfers puts the first print around 13.8 to 14.3. Downside scenario: stronger lower-wage real earnings and stable transfer receipt bring it near 11.5. Outside-the-interval downside would require a broader income surprise or policy effect not evident from the baseline."},{"kind":"forecast","point":12.6,"ciLow":11.6,"ciHigh":13.8}]}
