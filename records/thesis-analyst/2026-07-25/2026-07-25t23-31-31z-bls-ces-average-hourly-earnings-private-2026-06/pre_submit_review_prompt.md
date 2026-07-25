# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.ces.average_hourly_earnings_private
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "average-hourly-earnings-mom-june-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.ces.average_hourly_earnings_private.june_2026.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-09", "start": "2026-07-01"}, "field": "CES0500000003", "releasePolicy": "first_print", "sourceSeriesId": "CES0500000003", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CES0500000003", "table": "Employment Situation, Table B-3", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-25-4e95b3f8be235216f79894e8fefeb3decf704b26f7a9ccfda13a0626158771f2.json"
- targetContentHash: "4e95b3f8be235216f79894e8fefeb3decf704b26f7a9ccfda13a0626158771f2"
- registrationCommit: "add78fbd9af9ca9b0c7389a9a44a7ec839f2f4af"
- registeredAtUtc: "2026-07-25T15:18:08Z"
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
8736f7190f8901adf5f8285f11780933f06fcc1085542a859f08939ab3ec373f

# Draft forecast response
{"slug":"average-hourly-earnings-mom-june-2026","country":"US","type":"data","title":"US private AHE MoM, June 2026","question":"What was the first-print month-over-month percent change in BLS CES0500000003, Average Hourly Earnings of All Employees, Total Private, seasonally adjusted, for June 2026?","unit":"percent_growth","pointEstimate":0.3,"ciLow":0.2,"ciHigh":0.4,"confidence":0.8,"resolutionDate":"2026-07-02","resolutionSource":"BLS Employment Situation, Table B-3","resolutionSourceUrl":"https://www.bls.gov/news.release/archives/empsit_07022026.htm","resolutionRule":"Resolve to the first BLS Employment Situation print for June 2026, Table B-3, Average hourly earnings of all employees on private nonfarm payrolls, Total private, seasonally adjusted, series CES0500000003, expressed as the over-the-month percent change rounded to one decimal percentage point. Do not use later revisions or FRED/ALFRED revised vintages as the final source.","dataPointId":"bls.ces.average_hourly_earnings_private.june_2026.first_print","historicalContext":[{"label":"Feb 2026 MoM from FRED levels","value":0.323},{"label":"Mar 2026 MoM from FRED levels","value":0.215},{"label":"Apr 2026 MoM from FRED levels","value":0.161},{"label":"May 2026 MoM from FRED levels","value":0.321},{"label":"June 2026 first print","value":0.3}],"drivers":["Recent private AHE gains clustered near 0.2-0.3 percent","May first print was a firm 0.3 percent gain","Payroll mix effects can move average hourly earnings independent of wage rates","Resolution is the seasonally adjusted total private all-employees series, not production workers or NSA earnings"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm","https://fred.stlouisfed.org/series/CES0500000003","https://www.bls.gov/news.release/archives/empsit_06052026.htm","https://www.bls.gov/news.release/archives/empsit_07022026.htm"],"runAt":"2026-07-25T23:32:15Z","reasoning":[{"kind":"heading","text":"US private average hourly earnings MoM, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: the target is BLS CES0500000003, Average Hourly Earnings of All Employees, Total Private, seasonally adjusted, in Employment Situation Table B-3. The requested unit is month-over-month percent growth, resolved on the first official June 2026 print and not on later revisions."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Employment Situation release schedule for the June 2026 reference month.","result":"BLS listed Employment Situation for June 2026 at 08:30 on Jul. 02, 2026; adjacent schedule entries included May 2026 on Jun. 05, 2026 and July 2026 on Aug. 07, 2026."},{"kind":"tool","tool":"fred.lookup","call":"Fetched the same seasonally adjusted total private AHE series CES0500000003 as a public history mirror before computing recent MoM rates.","result":"FRED showed CES0500000003 levels before the June print context: Jan 2026 37.15, Feb 2026 37.27, Mar 2026 37.35, Apr 2026 37.41, May 2026 37.53 dollars per hour."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS May 2026 Employment Situation archive, Table B-3, to confirm the variant and recent official values.","result":"BLS Table B-3 for May 2026 showed Total private average hourly earnings of $37.35 in Mar. 2026, $37.41 in Apr. 2026, and $37.53 in May 2026 for all employees, seasonally adjusted."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS June 2026 Employment Situation archive for the first-print resolution page and series value.","result":"BLS reported that in June average hourly earnings for all employees on private nonfarm payrolls rose by 13 cents, or 0.3 percent, to $37.64; Summary table B also showed Total private average hourly earnings of $37.64 in June 2026."},{"kind":"text","text":"Base rate/reference class: recent monthly changes from the same CES0500000003 seasonally adjusted level were Feb 0.323 percent, Mar 0.215 percent, Apr 0.161 percent, and May 0.321 percent, giving a short-run reference-class mean near 0.255 percent before any June-specific adjustment."},{"kind":"math","text":"Prior/update/interval: persistence prior is the Jan-May 2026 CES0500000003 short-run reference class from FRED/BLS levels; historical sample values are 0.323, 0.215, 0.161, and 0.321 percent MoM. Adjustment components: +0.02 pp for the firm May wage print and still-positive 3.5 percent year-over-year earnings trend, +0.02 pp for composition risk in a soft payroll month, leaving a rounded point near 0.30 percent. Interval method uses the sample dispersion of recent MoM values: sigma = 0.081 percentage points, so 1.28*sigma = 0.104 percentage points; rounded 80 percent bounds are 0.20 to 0.40 percent."},{"kind":"text","text":"Counter-considerations: upside risk would come from a high-wage industry mix or stronger hourly pay settlements and would land above the interval if the first print rounded to 0.5 percent or higher; downside risk would come from lower-wage hiring mix or payback after May and would land below the interval if the print rounded to 0.1 percent or lower."},{"kind":"forecast","point":0.3,"ciLow":0.2,"ciHigh":0.4}]}
