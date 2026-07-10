# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: eurostat.unemployment_rate
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "euro-area-unemployment-rate-july-2026"
- targetUnit: "percent"
- dataPointId: "eurostat.unemployment_rate.euro_area.july_2026.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["ec.europa.eu"], "expectedReleaseWindow": {"end": "2026-09-03", "start": "2026-08-26"}, "field": "eurostat.unemployment_rate", "releasePolicy": "first_print", "sourceSeriesId": "eurostat.unemployment_rate", "sourceUrl": "https://ec.europa.eu/eurostat/news/euro-indicators", "table": "Eurostat monthly unemployment euro-indicators release / une_rt_m data page", "transform": {"factor": 1.0, "operation": "multiply"}}
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
c514dd3e11932fcbb72091523ce3ffbfe3a446d1112c98e4716e9be1055ea15a

# Draft forecast response
{"slug":"euro-area-unemployment-rate-july-2026","country":"EA","type":"data","title":"Euro Area Unemployment Rate, July 2026","question":"Eurostat une_rt_m euro area seasonally adjusted total unemployment rate, age 15-74, July 2026 first print","unit":"percent","pointEstimate":6.2,"ciLow":6.1,"ciHigh":6.3,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"Eurostat euro-indicators unemployment release and une_rt_m data table","resolutionSourceUrl":"https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","resolutionRule":"Resolve to the first Eurostat-published July 2026 euro area seasonally adjusted unemployment rate in dataset une_rt_m for geo=Euro area, sex=total, age=15-74, unit=percent of labour force. Use the one-decimal first print in the Eurostat euro-indicators unemployment release or data page; ignore later revisions.","dataPointId":"eurostat.unemployment_rate.euro_area.july_2026.first_print","historicalContext":[{"label":"May 2026 latest euro area SA unemployment rate","value":6.2},{"label":"Apr 2026 euro area SA unemployment rate","value":6.2},{"label":"Mar 2026 euro area SA unemployment rate","value":6.3},{"label":"Feb 2026 euro area SA unemployment rate","value":6.4},{"label":"May 2025 euro area SA unemployment rate","value":6.3}],"drivers":["Latest euro area unemployment rate stable at 6.2%","Euro area unemployed count fell by 55 thousand in May","Large members mixed: Germany and Spain stable, Italy and Greece lower, France higher","Retail and services indicators show mild demand support","Labour-cost growth still positive but not an immediate layoff signal"],"sourceContext":["https://ec.europa.eu/eurostat/news/euro-indicators/release-calendar","https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/3-02072026-ap","https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/4-06072026-bp","https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/2-01072026-ap","https://ec.europa.eu/eurostat/en/web/products-euro-indicators/w/3-16062026-bp"],"runAt":"2026-07-10T04:37:24Z","reasoning":[{"kind":"heading","text":"Euro area unemployment rate July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the Eurostat une_rt_m euro area seasonally adjusted total unemployment rate for persons aged 15-74, in percent of the labour force, first print for July 2026. The variant is SA total unemployment, not NSA, youth-only, member-state, or revised-vintage data. Resolution uses the first Eurostat euro-indicators unemployment release/data-table value, rounded to one decimal."},{"kind":"tool","tool":"official.lookup","call":"Checked Eurostat euro-indicators release calendar and latest unemployment release scheduling context.","result":"The Eurostat Euro indicators calendar page lists Unemployment as a scheduled indicator and uses Europe/Luxembourg CET/CEST. The latest unemployment release was published 2 July 2026 for May 2026 and states the next unemployment release is 30 July 2026; applying the official July-target calendar entry within the ledger release window gives the July 2026 first-print resolution date 2026-09-01."},{"kind":"tool","tool":"official.lookup","call":"Fetched latest Eurostat unemployment release for euro area totals.","result":"Eurostat reported May 2026 euro area seasonally adjusted unemployment at 6.2%, stable vs April 2026 at 6.2%, down from May 2025 at 6.3%; February 2026 was 6.4% and March 2026 was 6.3%. Euro area unemployed persons were 10.986 million in May 2026, down 55 thousand from April and down 158 thousand from May 2025."},{"kind":"tool","tool":"official.lookup","call":"Fetched large-member unemployment readings from the same Eurostat release table.","result":"May 2026 rates in the Eurostat table: Germany 3.8%, Spain 10.3%, France 8.2%, Italy 5.0%, Greece 8.1%; April 2026 rates were Germany 3.8%, Spain 10.3%, France 8.2%, Italy 5.1%, Greece 9.1%."},{"kind":"tool","tool":"official.lookup","call":"Fetched current Eurostat macro/labour-market context from official euro-indicators pages.","result":"Eurostat reported May 2026 euro area retail trade volume +0.2% m/m after -0.3% in April, June 2026 flash HICP inflation 2.8% after 3.2% in May, services inflation 3.2% after 3.5%, and Q1 2026 euro area hourly labour costs +3.2% y/y with wages and salaries +3.4%."},{"kind":"text","text":"Reference class and base rate: the immediate reference class is recent monthly first-print euro area SA unemployment rates. The base rate is persistence around the latest 6.2%, because the last three monthly readings moved only from 6.4 to 6.3 to 6.2 to 6.2 and unemployment rates usually change in 0.0-0.1 percentage-point increments month to month."},{"kind":"math","text":"Prior/update/interval: persistence prior = 6.2 from the latest official May print; historical sample = successive monthly changes from Feb-May 2026 values 6.4, 6.3, 6.2, 6.2, giving changes -0.1, -0.1, 0.0 and sigma = 0.06 percentage points per month. Adjustment components: level 0.00, momentum -0.03 from falling unemployed count and Italy/Greece declines, demand +0.01 from retail/services resilience, labour-cost/policy-mechanism +0.02 because wage costs remain positive but not recessionary, net 0.00 after rounding. For the two-month-ahead July first print, half-width = 1.28*sqrt(2)*0.06 = 0.11 percentage points; rounded to the one-decimal release grid gives an 80% interval of 6.1 to 6.3 around a 6.2 point."},{"kind":"text","text":"Counter-considerations: upside risk is a summer weakening in France or Spain, or delayed pass-through from high energy and labour costs, which would land above the interval at 6.4% or higher. Downside risk is continued sharp declines in Italy/Greece plus stable Germany and Spain, which would land below the interval at 6.0% or lower. Outside the interval would require two consecutive monthly moves of roughly the same sign rather than the recent near-flat pattern."},{"kind":"forecast","point":6.2,"ciLow":6.1,"ciHigh":6.3}]}
