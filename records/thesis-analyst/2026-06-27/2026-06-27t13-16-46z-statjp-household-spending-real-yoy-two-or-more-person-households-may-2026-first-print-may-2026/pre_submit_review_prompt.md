# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review only the draft forecast, the target spec, and public evidence cited in the draft. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: statjp.household_spending.real_yoy.two_or_more_person_households.may_2026.first_print
- period: May 2026
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
9549d9ab0fe379298db1d73058821f012a6d13ef1735f31bffe192ae8ad97996

# Draft forecast response
{"slug":"statjp-household-spending-real-yoy-two-or-more-person-households-may-2026-first-print","country":"JP","type":"data","title":"Japan household spending real YoY, May 2026","question":"Statistics Bureau of Japan Family Income and Expenditure Survey, consumption expenditures for two-or-more-person households, real year-over-year percent change, May 2026, first preliminary print","unit":"percent_growth","pointEstimate":-1.1,"ciLow":-4,"ciHigh":2.2,"confidence":0.8,"resolutionDate":"2026-07-07","resolutionSource":"Statistics Bureau of Japan Family Income and Expenditure Survey monthly preliminary report","resolutionSourceUrl":"https://www.stat.go.jp/data/kakei/sokuhou/tsuki/pdf/fies_mr.pdf","resolutionRule":"Resolve to the first preliminary Statistics Bureau of Japan Family Income and Expenditure Survey monthly report value for real consumption expenditures, two-or-more-person households, May 2026, year-over-year percent change. Use the agency-published one-decimal-percent figure from the first print released on 2026-07-07; ignore later revisions or annual recalculations.","dataPointId":"statjp.fies.consumption_expenditures.real_yoy.two_or_more_person_households.2026-05.first_print","historicalContext":[{"label":"2026-Apr first print","value":-0.5},{"label":"2026-Mar first print","value":-2.9},{"label":"2026-Feb first print","value":-1.8},{"label":"2026-Jan first print","value":-1},{"label":"2025-May first print","value":4.7}],"drivers":["Recent official real spending prints were negative through April 2026","May 2025 comparison base was high at plus 4.7 percent","April 2026 showed less weakness than March but not a clear positive run rate","Real purchasing-power pressure still limits volume growth","One-off calendar and bonus-timing effects can move the monthly household survey materially"],"sourceContext":["https://www.stat.go.jp/data/kakei/sokuhou/tsuki/pdf/fies_mr.pdf","https://www.stat.go.jp/data/kakei/index.html","https://www.stat.go.jp/data/kouhyou/index.html"],"runAt":"2026-06-27T13:17:51Z","reasoning":[{"kind":"heading","text":"Forecast for Japan May 2026 real household spending YoY first print"},{"kind":"text","text":"The resolver is the Statistics Bureau of Japan first preliminary monthly Family Income and Expenditure Survey print for consumption expenditures of two-or-more-person households, real year-over-year change, May 2026. The agency reports this series to one decimal percent, so the forecast is also stated to one decimal percent."},{"kind":"tool","tool":"official.lookup","call":"Checked the Statistics Bureau of Japan household spending data page and current monthly preliminary report for the target series and recent official prints.","result":"The April 2026 preliminary report shows real consumption expenditures for two-or-more-person households at -0.5 percent year over year in 2026-Apr, after -2.9 percent in 2026-Mar, -1.8 percent in 2026-Feb, and -1.0 percent in 2026-Jan."},{"kind":"tool","tool":"official.lookup","call":"Read the same official monthly report table for the recent reference class of first-print real year-over-year values.","result":"The 12-month sequence from 2025-May through 2026-Apr is 4.7, 1.3, 1.4, 2.3, 1.8, -3.0, -2.3, -2.7, -1.0, -1.8, -2.9, -0.5 percent."},{"kind":"tool","tool":"official.lookup","call":"Checked the official Statistics Bureau publication schedule page for the May 2026 household spending release date.","result":"The official schedule places the May 2026 household spending first-print release on 2026-07-07; the current report page identifies the monthly preliminary report as the release vehicle and reports April 2026 at -0.5 percent."},{"kind":"text","text":"Base-rate/reference-class anchor: the latest 12 official monthly first prints average about -0.2 percent, while the latest four average about -1.6 percent. I put more weight on the recent negative run because inflation-adjusted household spending has remained weak into 2026, but I do not extrapolate the March trough mechanically because April rebounded to -0.5 percent."},{"kind":"text","text":"Level and momentum effects point slightly negative: the January-April 2026 run is below zero, and May must compare against May 2025's high 4.7 percent print. That high base makes a positive May 2026 year-over-year result harder even if the month-to-month level is stable."},{"kind":"text","text":"Policy and one-off mechanisms are mixed. Wage gains and fiscal support can lift nominal outlays, but the target is real spending, so price levels subtract from the volume measure. Calendar, weather, and sample-composition noise can still produce a large positive or negative one-month print."},{"kind":"text","text":"Counter-consideration: April's improvement from -2.9 percent to -0.5 percent could mark a real turning point if wage settlements or durable-goods purchases pulled May up. Conversely, if the high May 2025 base and food-price pressure dominate, the print could fall below -4.0 percent."},{"kind":"math","text":"I anchor at the 12-month mean near -0.2 percent, blend toward the latest-four-month mean near -1.6 percent, then subtract a small high-base adjustment from May 2025's +4.7 percent comparison, yielding about -1.1 percent. The realized monthly dispersion in the 12 official prints supports an 80 percent interval roughly 3 percentage points wide on each side; I use -4.0 to 2.2 percent, slightly skewed downside because the base effect is adverse."},{"kind":"text","text":"Upside outside-the-interval scenario: real wage gains and delayed services or durable-goods spending lift the first print above 2.2 percent. Downside outside-the-interval scenario: food and utility inflation plus the high May 2025 base push real spending below -4.0 percent. Central scenario: still-negative but less severe real spending, close to April's weakness."},{"kind":"forecast","point":-1.1,"ciLow":-4,"ciHigh":2.2}]}
