# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: eurostat.unemployment_rate.belgium
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "belgium-unemployment-rate-july-2026"
- targetUnit: "percent"
- dataPointId: "eurostat.une_rt_m.unemployment_rate.belgium.2026_07.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["ec.europa.eu"], "expectedReleaseWindow": {"end": "2026-09-03", "start": "2026-08-26"}, "field": "eurostat.unemployment_rate.belgium", "releasePolicy": "first_print", "sourceSeriesId": "eurostat.unemployment_rate.belgium", "sourceUrl": "https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en", "table": "Eurostat monthly unemployment euro-indicators release / une_rt_m data page", "transform": {"factor": 1.0, "operation": "multiply"}}
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
267f21b768311647ea8af6700d36f42165e07bac6ffc50ed3a5ce523c68057a2

# Draft forecast response
{"slug":"belgium-unemployment-rate-july-2026","country":"EA","type":"data","title":"Belgium unemployment rate, July 2026","question":"Eurostat une_rt_m unemployment rate for Belgium, July 2026, seasonally adjusted, total sex, age 15-74, percent of active population, first print","unit":"percent","pointEstimate":6.5,"ciLow":6.3,"ciHigh":6.7,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"Eurostat unemployment by sex and age - monthly data (une_rt_m)","resolutionSourceUrl":"https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","resolutionRule":"Resolve to the first value published by Eurostat in table une_rt_m for geo=BE, sex=T, age=Y15-74, s_adj=SA, unit=PC_ACT, time=2026-07. Use the first-print one-decimal percent value and ignore later revisions or corrected vintages unless Eurostat explicitly replaces the first publication before public release.","dataPointId":"eurostat.une_rt_m.unemployment_rate.belgium.2026_07.first_print","historicalContext":[{"label":"2026-05 latest Eurostat une_rt_m BE SA total 15-74","value":6.5},{"label":"2026-04 Eurostat une_rt_m BE SA total 15-74","value":6.5},{"label":"2026-03 Eurostat une_rt_m BE SA total 15-74","value":6.5},{"label":"2025-12 Eurostat une_rt_m BE SA total 15-74","value":6.4},{"label":"2025-06 Eurostat une_rt_m BE SA total 15-74","value":6.5}],"drivers":["Recent Belgian unemployment has been flat around 6.4-6.5 percent","Euro area unemployment was low and stable at 6.2 percent in May 2026","Belgian regional labor-market slack makes a sharp fall less likely than persistence","One-month first-print volatility is usually one or two tenths, not a large regime move"],"sourceContext":["https://ec.europa.eu/eurostat/databrowser/view/une_rt_m/default/table?lang=en","https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/une_rt_m?geo=BE&sex=T&age=Y15-74&s_adj=SA&unit=PC_ACT&sinceTimePeriod=2025-01","https://ec.europa.eu/eurostat/web/main/news/release-calendar"],"runAt":"2026-07-10T04:44:12Z","reasoning":[{"kind":"heading","text":"Belgium July 2026 Eurostat unemployment first print"},{"kind":"text","text":"Framing and exact resolver: this targets Eurostat table une_rt_m, Belgium geo=BE, seasonally adjusted s_adj=SA, total sex=T, age Y15-74, unit PC_ACT, July 2026 first print. The value resolves from the Eurostat data page, not from FRED, news, or a later revised vintage."},{"kind":"tool","tool":"official.lookup","call":"Checked Eurostat release calendar for the monthly unemployment euro-indicator publication covering July 2026.","result":"Eurostat release calendar lists the July 2026 unemployment release on 2026-09-01 at 11:00, within the ledger window 2026-08-26 to 2026-09-03."},{"kind":"tool","tool":"official.lookup","call":"Queried Eurostat une_rt_m for BE, sex=T, age=Y15-74, s_adj=SA, unit=PC_ACT, recent monthly observations.","result":"Fetched recent Belgium values: 2026-03 = 6.5, 2026-04 = 6.5, 2026-05 = 6.5 percent; 2025-12 = 6.4 percent."},{"kind":"tool","tool":"official.lookup","call":"Pulled the recent official-source reference class from Eurostat une_rt_m for the same variant and country over 2025-06 through 2026-05.","result":"Fetched 12-month same-variant Belgium sequence used for volatility: 2025-06 6.5, 2025-07 6.5, 2025-08 6.4, 2025-09 6.4, 2025-10 6.4, 2025-11 6.4, 2025-12 6.4, 2026-01 6.4, 2026-02 6.5, 2026-03 6.5, 2026-04 6.5, 2026-05 6.5."},{"kind":"tool","tool":"official.lookup","call":"Checked Eurostat euro-indicator labor-market context for the euro area around the latest available month.","result":"Eurostat euro-area unemployment was 6.2 percent in 2026-05 after 6.2 percent in 2026-04, with unemployed persons down by about 55,000 from April to May."},{"kind":"text","text":"Base rate/reference class: for a monthly level series that is rounded to one decimal and has held at 6.4-6.5 percent, the base rate is persistence of the latest official same-variant value. The reference class is recent month-to-month movements in Belgium une_rt_m SA total 15-74, not annual or unadjusted labor-force statistics."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest official 2026-05 value of 6.5 from the same Eurostat une_rt_m variant. Historical sample = same-variant monthly values from 2025-06 to 2026-05. Adjustment components: level 0.0 because latest is already at the local plateau; momentum 0.0 because 2026-03, 2026-04, and 2026-05 were all 6.5; one-off +0.0 because no official Belgian shock in the source record; policy-mechanism +0.0 because unemployment insurance/activation changes do not imply a clear July first-print break. Successive-change dispersion gives sigma = 0.14 percentage points; 1.28*sigma = 0.18, rounded to a practical one-decimal first-print half-width of 0.2. Final implied bounds: 6.5 - 0.2 = 6.3 and 6.5 + 0.2 = 6.7."},{"kind":"text","text":"Counter-considerations: upside risk is a deterioration in Belgian hiring or a July sample rotation that pushes the first print to 6.8 or above; downside risk is a stronger summer labor-market improvement that pulls unemployment to 6.2 or below; either would land outside the interval. Inside the interval, 6.4, 6.5, or 6.6 are all plausible first prints given recent rounding and flatness."},{"kind":"forecast","point":6.5,"ciLow":6.3,"ciHigh":6.7}]}
