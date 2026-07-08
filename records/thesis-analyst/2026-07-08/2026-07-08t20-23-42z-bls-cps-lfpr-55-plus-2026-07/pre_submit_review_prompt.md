# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cps.lfpr_55_plus
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-lfpr-55-plus-july-2026"
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
046907e474e3b4efb852e74e6122831b4d00f5b4888193c6233b02721eaceb19

# Draft forecast response
{"slug":"us-lfpr-55-plus-july-2026","country":"US","type":"data","title":"US 55+ LFPR, July 2026","question":"BLS Current Population Survey labor force participation rate for people age 55 years and over, seasonally adjusted, July 2026 first print","unit":"percent","pointEstimate":37.1,"ciLow":37.0,"ciHigh":37.2,"confidence":0.8,"resolutionDate":"2026-08-07","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, CPS series LNS11324230","resolutionSourceUrl":"https://data.bls.gov/timeseries/LNS11324230","resolutionRule":"Resolve to the first BLS-published July 2026 value for CPS series LNS11324230, Labor Force Participation Rate - 55 Yrs. & over, seasonally adjusted, in percent, as released in the Employment Situation at 8:30 a.m. ET on August 7, 2026. Use the initially published value rounded to the BLS displayed 0.1 percentage point; ignore later revisions.","dataPointId":"bls.cps.lfpr_55_plus.2026-07.first_print","historicalContext":[{"label":"2026-06 latest","value":37.1},{"label":"2026-05","value":37.1},{"label":"2026-04","value":37.1},{"label":"2026-03","value":37.2},{"label":"2026-02","value":37.3}],"drivers":["55+ participation has flattened at 37.1 for three months","recent older-worker participation is near a 21-year low","aggregate June LFPR fell to 61.5","monthly rounded changes are usually 0.0 or 0.1 percentage point"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm","https://www.bls.gov/news.release/empsit.nr0.htm","https://fred.stlouisfed.org/series/LNS11324230"],"runAt":"2026-07-08T20:24:14Z","reasoning":[{"kind":"heading","text":"Forecast for BLS CPS 55+ labor force participation, July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is the seasonally adjusted CPS household-survey series LNS11324230, Labor Force Participation Rate - 55 Yrs. & over, in percent. Resolution is the first BLS July 2026 Employment Situation print, not a later revised vintage."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS Schedule of Releases for the Employment Situation.","result":"BLS calendar lists July 2026 reference month release on 2026-08-07 at 08:30 AM; June 2026 was released 2026-07-02 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Opened BLS June 2026 Employment Situation Summary for current labor-market context.","result":"BLS reported June 2026 total nonfarm payroll employment +57,000, unemployment rate 4.2 percent, aggregate labor force participation rate 61.5 percent, and aggregate participation down 0.3 percentage point in June."},{"kind":"tool","tool":"public.history_mirror","call":"Opened FRED mirror page for BLS CPS series LNS11324230 to read recent same-variant values.","result":"FRED/BLS series LNS11324230 shows Jun 2026 37.1, May 2026 37.1, Apr 2026 37.1, Mar 2026 37.2, Feb 2026 37.3, percent, seasonally adjusted; updated 2026-07-02 8:33 AM CDT; next release date 2026-08-07."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS Employment Situation Table A-1 for aggregate household-survey participation context.","result":"BLS Table A-1 shows seasonally adjusted total participation rates of Feb 2026 62.0, Mar 2026 61.9, Apr 2026 61.8, May 2026 61.8, Jun 2026 61.5."},{"kind":"text","text":"Reference class and base rate: for a monthly rounded participation-rate series, the best short-horizon reference class is recent same-series one-month changes in the same seasonally adjusted variant. The fetched 55+ path fell 0.2 percentage point from Feb to Jun but was unchanged at 37.1 in Apr, May, and Jun, so persistence at 37.1 is the base rate anchor."},{"kind":"math","text":"Prior/update/interval: persistence prior using recent BLS/FRED same-series history Feb-Jun 2026 = 37.3, 37.2, 37.1, 37.1, 37.1. Successive changes are -0.1, -0.1, 0.0, 0.0, so sample sigma = 0.058 percentage point. Level component = 37.1; momentum component = -0.05 from the Feb-Jun drift but muted because the last three readings were flat; one-off June aggregate LFPR weakness adds small downside risk of -0.02; policy-mechanism effect = 0.00. Final point rounds to 37.1. 80% half-width is roughly 1.28*sigma = 1.28*0.058 = 0.074, widened to 0.10 after rounding outward to BLS 0.1-point display precision, giving 37.0 to 37.2."},{"kind":"text","text":"Upside risk: a rebound in older workers re-entering after the June labor-force drop, or sampling reversal after three flat 37.1 readings, would land above 37.2. Downside risk: another retirement-heavy labor-force exit like June's aggregate participation decline would land below 37.0; outside the interval would require a rounded monthly move of at least 0.2 percentage point from June."},{"kind":"forecast","point":37.1,"ciLow":37.0,"ciHigh":37.2}]}
