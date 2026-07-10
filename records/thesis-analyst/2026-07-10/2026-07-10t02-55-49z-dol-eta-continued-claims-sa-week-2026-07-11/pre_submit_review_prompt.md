# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: dol.eta.continued_claims.sa
- period: week_2026-07-11
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-07-11"
- targetUnit: "millions"
- dataPointId: "dol.eta.continued_claims.sa.week_2026-07-11.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-25", "start": "2026-07-21"}, "field": "CCSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "CCSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA", "table": "ALFRED graph CSV", "transform": {"factor": 1e-06, "operation": "multiply"}}
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
e03db443333969cbe00e2a4495bc25869a7413e91ba4811f3e9e6795c19d871b

# Draft forecast response
{"slug":"continued-claims-week-2026-07-11","country":"US","type":"data","title":"US Continued Claims, Jul 11 2026","question":"What will the U.S. Department of Labor Employment and Training Administration first report for seasonally adjusted continued claims (insured unemployment), CCSA, for the week ending July 11, 2026?","unit":"millions","pointEstimate":1.817,"ciLow":1.776,"ciHigh":1.858,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor Employment and Training Administration, Unemployment Insurance Weekly Claims News Release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the first DOL ETA Unemployment Insurance Weekly Claims News Release published on July 23, 2026 at 8:30 a.m. ET. Use the Seasonally Adjusted Data / Unemployment Insurance Data for Regular State Programs line for Insured Unemployment (SA) for the week ending July 11, 2026, convert persons to millions by multiplying by 0.000001, and round to three decimals. Ignore later revisions and use ALFRED/FRED only as first-vintage retrieval aids if needed.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-11.first_print","historicalContext":[{"label":"2026-06-27 CCSA latest","value":1.814},{"label":"2026-06-20 CCSA","value":1.806},{"label":"2026-06-13 CCSA","value":1.812},{"label":"2026-06-06 CCSA","value":1.8},{"label":"2026-05-30 CCSA","value":1.786}],"drivers":["latest seasonally adjusted insured unemployment was 1.814 million","four-week average was 1.808 million","initial claims for week ending July 4 were 215,000","recent continued-claims momentum is mildly upward but choppy","target is the SA CCSA variant, not NSA or all-program continued weeks claimed"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims_arch.asp","https://fred.stlouisfed.org/series/CCSA","https://alfred.stlouisfed.org/series?seid=CCSA"],"runAt":"2026-07-10T02:56:40Z","reasoning":[{"kind":"heading","text":"Forecast for DOL ETA CCSA, Week Ending July 11 2026"},{"kind":"text","text":"Framing and exact resolver: this target is DOL ETA seasonally adjusted insured unemployment, series CCSA, for the week ending July 11, 2026, first print only. All anchors below use the same seasonally adjusted continued-claims variant, not unadjusted state claims and not total continued weeks claimed across all programs."},{"kind":"tool","tool":"official.lookup","call":"Opened the DOL Office of Unemployment Insurance archive and publication schedule page for the UI Weekly Claims News Release.","result":"Fetched schedule says the UI Weekly Claims News Release is published each Thursday at 8:30 AM EST, with 1 listed 2026 exception, Wednesday November 25, 2026; page updated July 9, 2026. Therefore the first DOL release carrying insured unemployment for week ending July 11, 2026 is Thursday July 23, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened the latest DOL UI Weekly Claims News Release PDF published July 9, 2026.","result":"Fetched latest official SA data: initial claims for week ending July 4, 2026 were 215,000; insured unemployment for week ending June 27, 2026 was 1,814,000; previous week revised level was 1,806,000; 4-week moving average was 1,808,000."},{"kind":"tool","tool":"mirror.lookup","call":"Opened FRED series CCSA as a public history mirror for the DOL ETA series identity and latest observations.","result":"Fetched CCSA observations: 2026-06-27 = 1,814,000; 2026-06-20 = 1,806,000; 2026-06-13 = 1,812,000; 2026-06-06 = 1,800,000; 2026-05-30 = 1,786,000. Units are Number, Seasonally Adjusted, Weekly ending Saturday."},{"kind":"tool","tool":"mirror.lookup","call":"Opened ALFRED vintage series page for CCSA to confirm the vintage-capable series binding.","result":"Fetched ALFRED CCSA page showing 2026-06-27 = 1,814,000, source U.S. Employment and Training Administration, release Unemployment Insurance Weekly Claims Report, seasonal adjustment Seasonally Adjusted, and release-date coverage through 2026-07-09."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL PDF historical SA weekly claims table for recent CCSA dispersion.","result":"Fetched recent insured unemployment SA history in thousands: Jan 3 2026 = 1,875; Jan 10 = 1,865; Jan 17 = 1,823; Jan 24 = 1,842; Jan 31 = 1,859; Feb 7 = 1,865; Feb 14 = 1,827; Feb 21 = 1,871; Feb 28 = 1,847; Mar 7 = 1,851; Mar 14 = 1,816; Mar 21 = 1,832; Mar 28 = 1,787; Apr 4 = 1,809; Apr 11 = 1,808; Apr 18 = 1,776; Apr 25 = 1,758; May 2 = 1,776; May 9 = 1,771; May 16 = 1,785; May 23 = 1,771; May 30 = 1,786; Jun 6 = 1,800; Jun 13 = 1,812; Jun 20 = 1,806; Jun 27 = 1,814."},{"kind":"text","text":"The reference class and base rate are short-horizon weekly changes in the same SA insured-unemployment level. Recent history is centered near 1.81 million: the latest print is 1.814 million, the latest 4-week average is 1.808 million, and the latest five observations average 1.804 million."},{"kind":"math","text":"Prior/update/interval: persistence prior is 1.814 million from the latest CCSA first-print/mirror observation; historical sample is the 26 recent weekly SA changes from Jan 3 through Jun 27, 2026: -25, -10, -42, 19, 17, 6, -38, 44, -24, 4, -35, 16, -45, 22, -1, -32, -18, 18, -5, 14, -14, 15, 14, 12, -6, 8 thousand. The sample standard deviation is sigma = 0.023 million; 1.28*sigma = 0.029 million. For a two-week-ahead first print I scale by sqrt(2), giving about 0.041 million half-width. Level adjustment is +0.003 million because June-to-late-June momentum is mildly positive while latest initial claims at 215,000 are stable. Final bounds are 1.817 - 0.041 = 1.776 and 1.817 + 0.041 = 1.858."},{"kind":"text","text":"Upside risk: if continuing-benefit duration lengthens or July school/auto seasonal adjustment noise pushes repeat claims higher, the value would land above the interval. Downside risk: if the 215,000 initial-claims week maps into fewer continuing claims or the June rise revises away in the first July prints, it would land below the interval. A shock large enough to move weekly SA continued claims by more than about 40,000 over the next two target weeks is outside the interval scenario."},{"kind":"forecast","point":1.817,"ciLow":1.776,"ciHigh":1.858}]}
