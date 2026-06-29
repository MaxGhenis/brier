# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review only the draft forecast, the target spec, and public evidence cited in the draft. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: statjp.lfs.unemployment_rate
- period: 2026-05
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
755b58f09e0d21fccd6ed9ea764aa82342a0c908b3b6cd8bdc22a1ba04d91e6d

# Draft forecast response
{"slug":"jp-lfs-unemployment-rate-2026-05","country":"JP","type":"data","title":"Japan May 2026 unemployment rate","question":"Japan Statistics Bureau Labour Force Survey Basic Tabulation, May 2026 seasonally adjusted unemployment rate, first print","unit":"percent","pointEstimate":2.5,"ciLow":2.3,"ciHigh":2.8,"confidence":0.8,"resolutionDate":"2026-06-30","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.stat.go.jp/data/roudou/sokuhou/tsuki/index.html","resolutionRule":"Resolve to the first-print seasonally adjusted complete unemployment rate for May 2026 in the Statistics Bureau of Japan Labour Force Survey Basic Tabulation, published at the agency's stated precision of one decimal percentage point. Use the initial June 30, 2026 print and ignore later revisions or seasonal-adjustment updates.","dataPointId":"statjp.lfs.unemployment_rate.2026-05.first_print","historicalContext":[{"label":"2026-04 seasonally adjusted unemployment rate","value":2.5},{"label":"2026-03 seasonally adjusted unemployment rate","value":2.7},{"label":"2026-02 seasonally adjusted unemployment rate","value":2.6},{"label":"2026-01 seasonally adjusted unemployment rate","value":2.7},{"label":"2025 annual unemployment rate","value":2.5},{"label":"2024 annual unemployment rate","value":2.5},{"label":"2023 annual unemployment rate","value":2.6}],"drivers":["latest unemployment rate fell to 2.5 percent","recent 2026 monthly range is narrow at 2.5 to 2.7 percent","employment up year over year but unemployed persons also up year over year","Japan labor market level remains near the 2024-2025 average","one-month rounded moves are usually small but 0.2 point reversals are possible"],"sourceContext":["https://www.stat.go.jp/data/roudou/sokuhou/tsuki/index.html","https://www.stat.go.jp/data/roudou/pdf/kohyo26.pdf","https://www.stat.go.jp/data/roudou/sokuhou/tsuki/pdf/gaiyou.pdf","https://www.e-stat.go.jp/stat-search/files?cycle=0&tclass=000001226526"],"runAt":"2026-06-27T12:57:12Z","reasoning":[{"kind":"heading","text":"Forecast Japan May 2026 first-print unemployment rate"},{"kind":"text","text":"The resolver is the Statistics Bureau of Japan Labour Force Survey Basic Tabulation complete unemployment rate, seasonally adjusted, for May 2026, taken from the first official monthly release and rounded as the agency publishes it to one decimal percentage point."},{"kind":"tool","tool":"official.lookup","call":"Opened the Statistics Bureau monthly Labour Force Survey results page for the latest official release.","result":"Latest official page is the 2026 April release, published 2026-05-29, with seasonally adjusted complete unemployment rate 2.5%, down 0.2 percentage point from the prior month."},{"kind":"tool","tool":"official.lookup","call":"Opened the official 2026 Labour Force Survey release schedule PDF.","result":"The schedule lists the 2026年5月分 Basic Tabulation release date as 2026-06-30 and notes Basic Tabulation releases at 8:30."},{"kind":"tool","tool":"official.lookup","call":"Read the latest official monthly summary table for recent values and annual context.","result":"The page reports 2023 annual 2.6%, 2024 annual 2.5%, 2025 annual 2.5%, and 2026 monthly values of Jan 2.7%, Feb 2.6%, Mar 2.7%, Apr 2.5%."},{"kind":"tool","tool":"official.lookup","call":"Read the latest official PDF summary for labor-market level and momentum details.","result":"The April 2026 PDF reports employed persons 68.60 million, up 0.64 million year over year; unemployed persons 1.93 million, up 0.05 million year over year; labor force 70.53 million, up 0.69 million year over year; seasonally adjusted unemployment rate 2.5%."},{"kind":"text","text":"Base-rate/reference-class anchor: the recent official-source reference class is a low-volatility range around 2.5 to 2.7 percent. The 2024 and 2025 annual rates were both 2.5 percent, so the outside-view anchor is 2.5 percent rather than a trend extrapolation away from the recent mean."},{"kind":"text","text":"Level, momentum, and one-off effects: the latest 2.5 percent level is already at the two-year annual average. The month-to-month momentum is downward from March to April, but the year-over-year unemployed count is still positive, which argues against a confident break below 2.5 percent. No policy-mechanism or calendar event points to a large May discontinuity."},{"kind":"text","text":"Counter-consideration: April's 0.2 point drop could partially reverse if labor-force participation rose or if the unemployed count continued its year-over-year increase; an upside print of 2.7 to 2.8 percent is plausible. The downside scenario is continued strong employment absorption pushing the rounded rate to 2.3 or 2.4 percent. Outside the interval would likely require an unusually sharp one-month labor-force or employment shock."},{"kind":"math","text":"Point calculation: start from the official April level 2.5, blend with the 2026 Jan-Apr average (2.7+2.6+2.7+2.5)/4 = 2.625 and the 2024-2025 annual anchor 2.5, then give most weight to the latest level because the target is one month ahead and rounded to 0.1; resulting latent forecast is about 2.55, rounded forecast 2.5. The 80% interval uses recent rounded monthly dispersion of about 0.1-0.2 point, widened for release noise to 2.3-2.8."},{"kind":"forecast","point":2.5,"ciLow":2.3,"ciHigh":2.8}]}
