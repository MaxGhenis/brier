# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.productivity.nonfarm_unit_labor_costs_qoq_prelim
- period: 2026-Q2
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-unit-labor-costs-q2-2026-prelim"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.productivity.nonfarm_unit_labor_costs_qoq_prelim.2026_q2.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-06", "start": "2026-08-06"}, "field": "PRS85006112", "releasePolicy": "first_print", "sourceSeriesId": "PRS85006112", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PRS85006112", "table": "Productivity and Costs, nonfarm business sector", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-a7e6c99f351819961a9cdf9259bebf1c1e21fac9e5f690026b9e4ce20813392c.json"
- targetContentHash: "a7e6c99f351819961a9cdf9259bebf1c1e21fac9e5f690026b9e4ce20813392c"
- registrationCommit: "145f6612f225710a4621f124b13bf5d5ae5d97ac"
- registeredAtUtc: "2026-07-26T00:55:04Z"
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
85eaabd9c8e588c9122fcda3bba41305dbaec2c67f03afed92383833a82a2e3c

# Draft forecast response
{"slug":"us-unit-labor-costs-q2-2026-prelim","country":"US","type":"data","title":"US Q2 2026 preliminary unit labor costs","question":"What will BLS first report for nonfarm business sector unit labor costs, seasonally adjusted percent change from previous quarter at an annual rate, in 2026 Q2 preliminary Productivity and Costs?","unit":"percent_growth","pointEstimate":3,"ciLow":-0.8,"ciHigh":6.8,"confidence":0.8,"resolutionDate":"2026-08-06","resolutionSource":"U.S. Bureau of Labor Statistics Productivity and Costs, Table 2","resolutionSourceUrl":"https://www.bls.gov/news.release/prod2.t02.htm","resolutionRule":"Resolve to the first-published BLS Productivity and Costs preliminary second-quarter 2026 value for nonfarm business sector unit labor costs, seasonally adjusted percent change from previous quarter at an annual rate, rounded to one decimal place as published in Table 2 on August 6, 2026; ignore later revised releases and later data-vintage changes.","dataPointId":"bls.productivity.nonfarm_unit_labor_costs_qoq_prelim.2026_q2.first_print","historicalContext":[{"label":"2026 Q1 revised BLS Table 2","value":1.8},{"label":"2026 Q1 preliminary BLS Table A1","value":2.3},{"label":"2025 Q4 preliminary BLS Table A1","value":2.8},{"label":"2025 Q3 preliminary BLS Table A1","value":-1.9},{"label":"2025 Q2 preliminary BLS Table A1","value":1.6}],"drivers":["Q1 unit labor costs were moderate after downward revision","private payroll hours were nearly flat through June","nominal earnings growth remains near 3.5 percent year over year","productivity first prints are volatile because output and compensation source data are incomplete","unit labor costs mechanically rise when hourly compensation outpaces productivity"],"sourceContext":["https://www.bls.gov/schedule/news_release/prod2.htm","https://www.bls.gov/news.release/prod2.t02.htm","https://www.bls.gov/news.release/prod2.htm","https://www.bls.gov/news.release/archives/prod2_05072026.htm","https://www.bls.gov/news.release/archives/prod2_03052026.htm","https://www.bls.gov/news.release/archives/prod2_01082026.htm","https://www.bls.gov/news.release/archives/prod2_08072025.htm","https://www.bls.gov/news.release/archives/empsit_07022026.htm","https://fred.stlouisfed.org/series/PRS85006112"],"runAt":"2026-07-26T01:12:43Z","reasoning":[{"kind":"heading","text":"US nonfarm unit labor costs, Q2 2026 preliminary"},{"kind":"text","text":"Framing and exact resolver: this is BLS nonfarm business sector unit labor costs, seasonally adjusted percent change from previous quarter at an annual rate, first print for 2026 Q2. The ledger sourceBinding points to ALFRED/FRED series PRS85006112 as a first-print mirror, but the official resolution source should be the BLS Productivity and Costs release/table for the first official print."},{"kind":"tool","tool":"official.lookup","call":"BLS Productivity and Costs release schedule lookup","result":"BLS schedule lists Second Quarter 2026 (P) on Aug. 06, 2026 at 08:30 AM and Second Quarter 2026 (R) on Sep. 03, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"BLS current Productivity and Costs Table 2 lookup for the same nonfarm business variant","result":"BLS Table 2 for 2026 Q1 revised shows nonfarm business unit labor costs 1.8, labor productivity 0.3, output 1.0, hours worked 0.7, and hourly compensation 2.1, all seasonally adjusted annualized rates."},{"kind":"tool","tool":"official.lookup","call":"BLS preliminary/recent-release reference class lookup","result":"Recent first prints for the target variant were 2026 Q1 unit labor costs 2.3 with productivity 0.8 and hourly compensation 3.1; 2025 Q4 unit labor costs 2.8 with productivity 2.8 and hourly compensation 5.7; 2025 Q3 unit labor costs -1.9 with productivity 4.9 and hourly compensation 2.9; 2025 Q2 unit labor costs 1.6 with productivity 2.4 and hourly compensation 4.0."},{"kind":"tool","tool":"official.lookup","call":"BLS June 2026 Employment Situation lookup for Q2 labor-cost and hours signals","result":"BLS reported June 2026 total nonfarm payroll employment +57,000, unemployment 4.2, average hourly earnings $37.64, average hourly earnings up 3.5 percent over the year, average weekly hours 34.3, and aggregate weekly hours index 116.8 versus 116.6 in April and 116.7 in May."},{"kind":"tool","tool":"mirror.lookup","call":"FRED/ALFRED PRS85006112 recent history mirror check","result":"FRED/ALFRED PRS85006112 reports Q1 2026 1.8, Q4 2025 2.1, Q3 2025 1.0, Q2 2025 -2.9, and Q1 2025 7.3 for Nonfarm Business Sector: Unit Labor Costs for All Workers, percent change at annual rate, seasonally adjusted."},{"kind":"text","text":"Reference class and base rate: using the same BLS nonfarm business unit-labor-costs variant, recent revised values from 2021 Q3 through 2026 Q1 average about 2.9 percent annualized, while the last four preliminary first prints before this target average about 1.2 percent but with a shutdown/benchmark-distorted negative Q3 2025. I weight the broader base rate more than the short preliminary sequence because this series is mechanically noisy and revised."},{"kind":"text","text":"Variant control: all anchors above are nonfarm business sector, seasonally adjusted, percent change from previous quarter at an annual rate. I do not mix in manufacturing, year-over-year, index-level, or final-vintage-only variants for the point forecast."},{"kind":"math","text":"Prior/update/interval: persistence/base-rate prior is 2.9 from the 2021 Q3-2026 Q1 BLS revised reference class. Update components: Q1 revised ULC of 1.8 pulls slightly down, June payroll-hours softness (aggregate weekly hours 116.6 in April, 116.7 in May, 116.8 in June) supports positive productivity but not a boom, and 3.5 percent year-over-year hourly earnings plus recent compensation volatility keep compensation growth near 3.5-4.0. Net update leaves point near 3.0. Interval method uses realized dispersion of same-series quarterly annualized values [8.0, 3.5, 7.2, 3.5, 7.0, -1.7, 2.2, 2.4, 1.2, 1.2, 5.5, 1.1, 1.1, 2.9, 7.3, -2.9, 1.0, 2.1, 1.8]; sample sigma = 3.0, so 80 percent half-width is about 1.28*sigma = 1.28*3.0 = 3.8. Point 3.0 minus/plus 3.8 gives -0.8 to 6.8."},{"kind":"text","text":"Counter-considerations: upside risk is a compensation-per-hour jump with only modest output growth, which would land above the interval if preliminary hourly compensation prints near 8 percent and productivity is flat or negative. Downside risk is a strong Q2 output/productivity first print combined with subdued compensation, which would land below the interval if productivity exceeds compensation by more than about 1 percentage point annualized."},{"kind":"forecast","point":3,"ciLow":-0.8,"ciHigh":6.8}]}
