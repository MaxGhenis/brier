# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: eurostat.unemployment_rate
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "euro-area-unemployment-rate-july-2026"
- country: "EA"
- targetUnit: "percent"
- dataPointId: "eurostat.unemployment_rate.euro_area.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["ec.europa.eu"], "expectedReleaseWindow": {"end": "2026-09-03", "start": "2026-08-26"}, "field": "eurostat.unemployment_rate", "releasePolicy": "first_print", "sourceSeriesId": "eurostat.unemployment_rate", "sourceUrl": "https://ec.europa.eu/eurostat/news/euro-indicators", "table": "Eurostat monthly unemployment euro-indicators release / une_rt_m data page", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-0fbb8f5d88f4627312ef5d9d5e31cffc94afec5f3b75f5c117adba8543bb2d08.json"
- targetContentHash: "0fbb8f5d88f4627312ef5d9d5e31cffc94afec5f3b75f5c117adba8543bb2d08"
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
6b7fe849d45f759ebbf3f327fccb33419909da246dc9528d429e8f21a98b97d6

# Draft forecast response
{"slug":"euro-area-unemployment-rate-july-2026","country":"EA","type":"data","title":"Euro area unemployment rate, July 2026","question":"Eurostat une_rt_m euro area unemployment rate, July 2026, seasonally adjusted total age 15-74, first print","unit":"percent","pointEstimate":6.2,"ciLow":6,"ciHigh":6.4,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"Eurostat monthly unemployment euro-indicators release / une_rt_m data page","resolutionSourceUrl":"https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","resolutionRule":"Resolve to Eurostat's first published July 2026 euro area seasonally adjusted unemployment rate in table une_rt_m / the monthly unemployment euro-indicators release, for total sex and age 15-74, reported in percent to one decimal. Use the first print only and ignore later revisions.","dataPointId":"eurostat.unemployment_rate.euro_area.july_2026.first_print","historicalContext":[{"label":"May 2026 latest","value":6.2},{"label":"Apr 2026","value":6.2},{"label":"Mar 2026","value":6.3},{"label":"Feb 2026","value":6.4},{"label":"May 2025","value":6.3}],"drivers":["latest first-print anchor at 6.2 percent","Feb-May 2026 drift down from 6.4 to 6.2","May unemployment count fell by 55 thousand in the euro area","same variant throughout: euro area seasonally adjusted total age 15-74 rate","two unpublished monthly steps remain before the July target"],"sourceContext":["https://ec.europa.eu/eurostat/news/euro-indicators/release-calendar","https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/3-02072026-ap","https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en"],"runAt":"2026-07-10T05:29:16Z","reasoning":[{"kind":"heading","text":"Euro area unemployment rate, July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this forecast targets Eurostat table une_rt_m, euro area unemployment rate, seasonally adjusted, total sex, age 15-74, percent, for July 2026. The resolution is the first official print, not a revised vintage."},{"kind":"tool","tool":"official.lookup","call":"Eurostat euro-indicators release calendar and latest unemployment release schedule lookup","result":"Eurostat's release calendar page lists Unemployment and uses Europe/Luxembourg time; the May 2026 unemployment release is dated 2 July 2026, gives a latest euro area rate of 6.2%, and states the next unemployment release is 30 July 2026. The registered July 2026 target resolves on the subsequent unemployment calendar slot, 2026-09-01."},{"kind":"tool","tool":"official.lookup","call":"Eurostat May 2026 euro area unemployment release overview","result":"Fetched latest same-series official values: May 2026 euro area seasonally adjusted unemployment rate 6.2%, April 2026 6.2%, May 2025 6.3%, EU May 2026 5.9%, and euro area unemployed persons 10.986 million."},{"kind":"tool","tool":"official.lookup","call":"Eurostat May 2026 release table for seasonally adjusted unemployment totals","result":"Fetched table history for the euro area rate: May 2025 6.3%, February 2026 6.4%, March 2026 6.3%, April 2026 6.2%, May 2026 6.2%; euro area unemployment counts were 11.144 million, 11.223 million, 11.136 million, 11.041 million, and 10.986 million for those same columns."},{"kind":"text","text":"Base rate / reference class: for this low-volatility monthly rate series, the outside-view prior is persistence at the latest official one-decimal print. The recent reference class is the same Eurostat euro area SA total age 15-74 rate, where the last five displayed values were tightly clustered between 6.2 and 6.4 percent."},{"kind":"text","text":"Level, momentum, and mechanism: the level is historically low at 6.2%; momentum from February to May is mildly downward, but the last month is flat at 6.2. The May count decline of 55 thousand supports no near-term jump, while two months of macro noise before the July reference month argues against narrowing the interval too much."},{"kind":"math","text":"Prior/update/interval: persistence prior 6.2 from May 2026; historical sample May 2025, Feb-May 2026 values 6.3, 6.4, 6.3, 6.2, 6.2; adjustment components are 0.0 for latest flat momentum, -0.05 for Feb-May downtrend, and +0.05 for two-step mean reversion/rounding risk, leaving point 6.2. Successive changes are +0.1, -0.1, -0.1, 0.0; one-month sample sigma is about 0.10. Because July is two unreleased monthly steps after May, forecast sigma = 0.10*sqrt(2) = 0.14, so the 80% half-width is roughly 1.28*sigma = 1.28*0.14 = 0.18, rounded to a one-decimal compatible 0.2; final implied bounds are 6.0 to 6.4."},{"kind":"text","text":"Counter-considerations: upside risk is a sharper employment deterioration in June-July that would lift the rounded first print to 6.5 or above, outside the interval. Downside risk is continued labor-market tightening and falling unemployment counts that would land below the interval at 5.9 or less."},{"kind":"forecast","point":6.2,"ciLow":6,"ciHigh":6.4}]}
