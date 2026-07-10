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
{"slug":"continued-claims-week-2026-07-11","country":"US","type":"data","title":"US Continued Claims, Jul 11 2026","question":"What will the U.S. Department of Labor first report for seasonally adjusted continued claims, week ending 2026-07-11, in the Unemployment Insurance Weekly Claims release?","unit":"millions","pointEstimate":1.815,"ciLow":1.775,"ciHigh":1.855,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims release","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260723","resolutionRule":"Resolve to the first published seasonally adjusted continued claims, also labeled insured unemployment, for the week ending July 11, 2026, in the Department of Labor ETA Unemployment Insurance Weekly Claims release scheduled for July 23, 2026. Convert the reported count to millions by multiplying by 1e-6. Use the first official print only; later revisions or ALFRED/FRED vintage updates after the first release do not change resolution.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-11.first_print","historicalContext":[{"label":"2026-06-27 continued claims SA latest","value":1.81},{"label":"2026-06-20 continued claims SA prior revised","value":1.802},{"label":"2026-06-13 continued claims SA prior rounded","value":1.81},{"label":"2026-06-06 continued claims SA prior rounded","value":1.81},{"label":"2026-05-30 continued claims SA prior rounded","value":1.8},{"label":"2026-05-23 continued claims SA prior revised","value":1.77}],"drivers":["SA continued claims have been clustered near 1.80 to 1.82 million","latest initial claims for week ending 2026-07-04 were 215000, not signaling a layoff break","June payroll growth slowed to 57000, supporting mild persistence in benefit duration","recent weekly continued-claims changes imply about 0.03 million two-week uncertainty"],"sourceContext":["https://www.dol.gov/newsroom/releases/eta/eta20260723","https://www.dol.gov/ui/data.pdf","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA","https://apnews.com/article/8d1f553fde8124606b2e3350fe789776","https://www.wsj.com/economy/jobs/u-s-jobless-claims-edged-lower-last-week-f35e8718","https://www.wsj.com/economy/jobs/u-s-jobless-claims-fell-last-week-a62436da","https://www.wsj.com/economy/jobs/u-s-jobless-claims-fell-last-week-ceec6b9f","https://www.wsj.com/economy/jobs/u-s-jobless-claims-rose-last-week-70b53ca9"],"runAt":"2026-07-10T03:42:04Z","reasoning":[{"kind":"heading","text":"Forecast for DOL CCSA week ending 2026-07-11"},{"kind":"text","text":"Framing and exact resolver: this is the DOL ETA seasonally adjusted continued claims series, FRED/ALFRED code CCSA, for the week ending 2026-07-11. The target is the first print in millions, not a later revised vintage; all anchors below refer to the same seasonally adjusted continued-claims variant."},{"kind":"tool","tool":"official.lookup","call":"Checked DOL ETA release timing for Unemployment Insurance Weekly Claims and the target lag structure.","result":"The official release slot for the weekly claims report covering continued claims for week ending 2026-07-11 is 2026-07-23 at 8:30 ET; the continued-claims reference week lags the initial-claims week by 1 week."},{"kind":"tool","tool":"official.lookup","call":"Checked the most recent DOL-reported weekly claims release and public mirrors of the same DOL figures.","result":"For the release on 2026-07-09, initial claims for week ending 2026-07-04 were 215000, down 2000 from 217000, and continued claims for week ending 2026-06-27 were about 1810000, up 8000 from a revised prior level near 1802000."},{"kind":"tool","tool":"official.lookup","call":"Pulled recent CCSA history from ALFRED/FRED mirror and contemporaneous DOL-release reporting for the SA continued-claims variant.","result":"Recent SA continued-claims levels in millions: 2026-05-23 1.770, 2026-05-30 1.800, 2026-06-06 1.810, 2026-06-13 1.810 to 1.820 depending on first/revised rounding, 2026-06-20 about 1.802 to 1.810, 2026-06-27 1.810."},{"kind":"tool","tool":"official.lookup","call":"Checked broader labor-market current-release context from public DOL/BLS reporting.","result":"The June 2026 employment report showed 57000 nonfarm payroll jobs added and an unemployment rate of 4.2 percent; weekly initial claims were 215000 for 2026-07-04 after 215000 for 2026-06-27 and roughly 226000 to 229000 in mid-June."},{"kind":"text","text":"Reference class and base rate: for a stable level series like SA continued claims, the best short-horizon base rate is persistence plus recent weekly drift. The last six rounded weekly observations sit in a tight 1.77 to 1.82 million range, with no latest initial-claims breakout suggesting a sharp move by the 2026-07-11 continued-claims week."},{"kind":"math","text":"Prior/update/interval: persistence prior uses the latest first/revised level around 1.810 million for 2026-06-27; historical sample uses recent weekly CCSA levels 1.770, 1.800, 1.810, 1.815 midpoint for 2026-06-13 rounding, 1.802, 1.810. Adjustment components are +0.003 million for slower June payrolls and longer duration, +0.002 million for the latest +8000 weekly move, and 0.000 million for stable initial claims, giving point 1.810 + 0.005 = 1.815. Weekly-change sigma from the fetched recent history is about 0.022 million; for a two-week-ahead level, sigma = 0.031 million after sqrt(2) scaling, and 1.28*sigma = 0.040 million, so the 80% interval is 1.815 +/- 0.040 = [1.775, 1.855]."},{"kind":"text","text":"Upside risk is a sudden rise in benefit duration or a jump in July layoffs that would push continued claims above 1.855 million. Downside risk is faster exits from UI or seasonal-adjustment noise that would pull the first print below 1.775 million. A recessionary layoff spike or a large seasonal-factor miss would land outside the interval."},{"kind":"forecast","point":1.815,"ciLow":1.775,"ciHigh":1.855}]}
