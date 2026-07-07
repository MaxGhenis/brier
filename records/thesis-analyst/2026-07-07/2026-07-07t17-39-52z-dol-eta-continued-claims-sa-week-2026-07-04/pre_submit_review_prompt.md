# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: dol.eta.continued_claims.sa
- period: week_2026-07-04
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-07-04"
- targetUnit: "millions"
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
a7935098bdeedb4ae00e5366aeb2a4230d6632bda8dd2672cdd9f90927a74d3e

# Draft forecast response
{"slug":"continued-claims-week-2026-07-04","country":"US","type":"data","title":"US continued claims, Jul 4 2026","question":"What will the U.S. Department of Labor Employment and Training Administration first print show for seasonally adjusted insured unemployment, also called continued claims, for the week ending July 4, 2026?","unit":"millions","pointEstimate":1.82,"ciLow":1.783,"ciHigh":1.858,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor, Employment and Training Administration, Unemployment Insurance Weekly Claims news release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance first-print seasonally adjusted insured unemployment number for the week ending July 4, 2026 in the DOL ETA Unemployment Insurance Weekly Claims release scheduled for July 16, 2026. Use the regular state programs Seasonally Adjusted Insured Unemployment / Continued Claims variant, convert persons to millions, and ignore later revisions or historical restatements.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-04.first_print","historicalContext":[{"label":"latest SA insured unemployment, week ending 2026-06-20","value":1.814},{"label":"previous SA insured unemployment, week ending 2026-06-13","value":1.812},{"label":"SA insured unemployment, week ending 2026-06-06","value":1.8},{"label":"latest 4-week average SA insured unemployment, week ending 2026-06-20","value":1.803},{"label":"prior-year comparable SA insured unemployment","value":1.954}],"drivers":["Latest official SA continued claims were 1.814 million, up 0.002 million on the week","Recent four-week average rose to 1.803 million, showing mild upward momentum","Initial claims eased to 215,000 and the initial-claims four-week average fell to 222,000, limiting expected further increases","First-print target is the DOL ETA SA insured-unemployment variant, not NSA all-program continued weeks claimed"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims_arch.asp","https://fred.stlouisfed.org/series/CCSA"],"runAt":"2026-07-07T17:40:20Z","reasoning":[{"kind":"heading","text":"Forecast for DOL ETA SA continued claims, week ending July 4, 2026"},{"kind":"text","text":"Framing and exact resolver: this forecasts the DOL ETA first-print regular-state-program seasonally adjusted insured unemployment series, also called continued claims, for the week ending July 4, 2026. The target is in millions; the agency release table reports the same SA variant in thousands/persons, so all anchors here use that same variant."},{"kind":"tool","tool":"official.lookup","call":"Opened DOL UI Weekly Claims latest news release at https://www.dol.gov/ui/data.pdf and read the release header and seasonally adjusted data text.","result":"The July 2, 2026 DOL release reported advance seasonally adjusted insured unemployment of 1,814,000 for week ending June 20, 2026, up 2,000 from the revised 1,812,000 for week ending June 13, 2026; the latest 4-week average was 1,803,000."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL regular state programs table in the July 2, 2026 UI Weekly Claims release.","result":"The table showed Insured Unemployment (SA) of 1,814,000 for June 20, 1,812,000 for June 13, 1,800,000 for June 6, and prior-year comparable 1,954,000; Insured Unemployment Rate (SA) was 1.2 percent."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL publication schedule on the official claims archive page https://oui.doleta.gov/unemploy/claims_arch.asp.","result":"The official schedule says the UI Weekly Claims News Release is published each Thursday at 8:30 AM EST, with the listed 2026 exception Wednesday November 25, 2026; July 16, 2026 is the Thursday first release that contains week ending July 4 continued claims."},{"kind":"tool","tool":"history.lookup","call":"Checked FRED CCSA public mirror for recent values and source metadata.","result":"FRED series CCSA listed 2026-06-20 at 1,814,000, 2026-06-13 at 1,812,000, 2026-06-06 at 1,800,000, 2026-05-30 at 1,786,000, and next release date July 9, 2026; FRED identifies the source as U.S. Employment and Training Administration and the unit as Number, Seasonally Adjusted."},{"kind":"text","text":"Base rate / reference class: over recent official weekly SA continued-claims changes, a persistence or local-random-walk prior is usually hard to beat for two weeks ahead. The recent level is near 1.81 million, below the comparable 2025 level of 1.954 million but rising modestly through June 2026."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest 1.814 million for week ending June 20. Historical sample = last 13 one-week SA insured-unemployment changes from DOL release table: -45, +22, -1, -32, -18, +18, -5, +14, -14, +15, +14, +12, +2 thousand, with mean about -1.4 thousand and sigma = 20.7 thousand per week. Adjustment components: level +0.000 million, recent momentum +0.012 million over two weeks, easing initial-claims inflow -0.006 million, no special policy effect +0.000 million, giving 1.814 + 0.006 = 1.820 million. For a two-week-ahead level forecast, sigma = sqrt(2) * 0.0207 = 0.0293 million, and 1.28*sigma = 0.0375 million, so the 80% interval is about 1.820 +/- 0.038 = [1.783, 1.858] million."},{"kind":"text","text":"Counter-considerations: upside risk is that continued claims keep drifting higher from benefit-duration persistence or state-level school-year layoffs, which would land above the interval if July 4 SA insured unemployment is above 1.858 million. Downside risk is that recent lower initial claims feed through faster than usual or June increases are revised away, which would land below the interval if the first print is under 1.783 million. Outside the interval would most likely require either a two-week jump above about 44,000 from the June 20 level or a drop of more than about 31,000."},{"kind":"forecast","point":1.82,"ciLow":1.783,"ciHigh":1.858}]}
