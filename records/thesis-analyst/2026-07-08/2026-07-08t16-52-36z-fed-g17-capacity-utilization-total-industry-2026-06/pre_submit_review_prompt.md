# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fed.g17.capacity_utilization.total_industry
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "fed-g17-capacity-utilization-total-industry-june-2026"
- targetUnit: "percent"
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
5b9021c6f711e626dcdf7c2aaf3369f7daf4bbc16cf9cece9a14b752d926c5f3

# Draft forecast response
{"slug":"fed-g17-capacity-utilization-total-industry-june-2026","country":"US","type":"data","title":"US total industry capacity utilization, June 2026","question":"Federal Reserve G.17 Capacity Utilization: Total Industry, June 2026, seasonally adjusted percent of capacity, first print","unit":"percent","pointEstimate":76.2,"ciLow":75.6,"ciHigh":76.8,"confidence":0.8,"resolutionDate":"2026-07-17","resolutionSource":"Federal Reserve G.17 Industrial Production and Capacity Utilization release","resolutionSourceUrl":"https://www.federalreserve.gov/releases/g17/20260717/default.htm","resolutionRule":"Resolve to the first-print June 2026 value, in percent of capacity and seasonally adjusted, for the G.17 Capacity utilization table row 'Total industry' as first published in the Federal Reserve's July 17, 2026 monthly G.17 release. Use the displayed one-decimal percent value; ignore later revisions, annual benchmark revisions, and later FRED updates.","dataPointId":"fed.g17.capacity_utilization.total_industry.2026-06.first_print","historicalContext":[{"label":"May 2026 TCU latest mirror","value":76.1663},{"label":"Apr 2026 TCU","value":76.1289},{"label":"Mar 2026 TCU","value":75.5388},{"label":"Feb 2026 TCU","value":75.847},{"label":"Jan 2026 TCU","value":75.305}],"drivers":["May utilization already rebounded to 76.2 percent","Recent total IP growth was positive but manufacturing was flat in May","Mining utilization strength offsets weak utilities utilization","Capacity growth keeps utilization below its 1972-2025 average"],"sourceContext":["https://www.federalreserve.gov/releases/g17/default.htm","https://www.federalreserve.gov/releases/g17/20260615/default.htm","https://fred.stlouisfed.org/series/TCU"],"runAt":"2026-07-08T16:53:10Z","reasoning":[{"kind":"heading","text":"Forecast for June 2026 total industry capacity utilization"},{"kind":"text","text":"Framing and exact resolver: this is the Federal Reserve G.17 Capacity Utilization: Total Industry series, seasonally adjusted percent of capacity. The target is the first published June 2026 value in the July 17, 2026 G.17 release; the series code mirror is FRED TCU, but resolution is to the Federal Reserve release table."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 release calendar lookup for 2026 monthly releases","result":"The G.17 release calendar says monthly releases are issued at 9:15 a.m.; 2026 dates include June 15 and July 17, so the June 2026 observation is scheduled for first release on 2026-07-17."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve June 15, 2026 G.17 current release summary and capacity utilization table","result":"The May 2026 release says total IP rose 0.1 percent in May after 0.9 percent in April, manufacturing output was 0.0 percent in May, mining rose 1.3 percent, utilities fell 0.4 percent, and total industry capacity utilization edged up to 76.2 percent."},{"kind":"tool","tool":"official.lookup","call":"Federal Reserve G.17 capacity utilization table for recent total industry values","result":"The total industry capacity utilization row shows May 2025 75.9, Dec 2025 75.6, Jan 2026 75.3, Feb 2026 75.8, Mar 2026 75.5, Apr 2026 76.1, and May 2026 76.2 percent."},{"kind":"tool","tool":"fred.history_mirror","call":"FRED TCU mirror for precise recent observations sourced to the Federal Reserve Board","result":"FRED TCU lists May 2026 76.1663, Apr 2026 76.1289, Mar 2026 75.5388, Feb 2026 75.8470, and Jan 2026 75.3050 percent; it also shows next release date Jul 17, 2026."},{"kind":"math","text":"Prior/update/interval: base rate prior is a near-persistence model for total industry utilization using the recent Federal Reserve/FRED reference class of monthly level changes from Dec 2025 through May 2026: -0.30, +0.54, -0.31, +0.59, +0.04 percentage point, giving sigma = 0.44. Level prior starts at May 2026 TCU 76.1663; momentum adjustment is +0.03 from the positive April-May IP/utilization trend, one-off adjustment is 0.00 because utilities weakness and mining strength offset, and policy-mechanism adjustment is 0.00. Point = 76.1663 + 0.03 = 76.20. 80% half-width is roughly 1.28*sigma = 1.28*0.44 = 0.56, rounded to a one-decimal first-print interval of 75.6 to 76.8."},{"kind":"text","text":"Counter-considerations: upside risk would come from another mining jump plus warmer-weather utility output and a rebound in manufacturing, which would land above the interval if utilization prints above 76.8. Downside risk is a June industrial production pullback or capacity benchmark-related weakness across manufacturing; a broad drop larger than about 0.6 point would land below the interval. Outside the interval would require a shock comparable to the largest recent month-to-month moves, not just normal rounding noise."},{"kind":"forecast","point":76.2,"ciLow":75.6,"ciHigh":76.8}]}
