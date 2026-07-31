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
- targetRegistrationPath: "records/targets/2026-07-31-e645bf2872cf26dcc4a3bfa091261d81b90d71cd3980d36dc32aef7c1b1cbb3b.json"
- targetContentHash: "e645bf2872cf26dcc4a3bfa091261d81b90d71cd3980d36dc32aef7c1b1cbb3b"
- registrationCommit: "0249a6f266d1d202c43782056e77403612358765"
- registeredAtUtc: "2026-07-31T14:48:09Z"
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
7fd3f4526b1e55be383278fe0eec08186b8bd86e9f207cca9c11b776cb516206

# Draft forecast response
{"slug":"average-hourly-earnings-mom-june-2026","country":"US","type":"data","title":"US private AHE MoM, Jun 2026","question":"What was the first-print month-over-month percent growth in BLS CES average hourly earnings of all employees, total private, seasonally adjusted, series CES0500000003, for June 2026?","unit":"percent_growth","pointEstimate":0.347,"ciLow":0.251,"ciHigh":0.442,"confidence":0.8,"resolutionDate":"2026-07-02","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table B-3","resolutionSourceUrl":"https://www.bls.gov/news.release/archives/empsit_07022026.htm","resolutionRule":"Resolve to the first BLS Employment Situation print for June 2026, Table B-3, total private average hourly earnings of all employees, seasonally adjusted, series CES0500000003. Compute percent growth as 100*(June 2026 first-print dollars per hour / May 2026 value printed in the same first-release table - 1). Use the archived July 2, 2026 release as the first-print record and do not revise after later CES revisions.","dataPointId":"bls.ces.average_hourly_earnings_private.june_2026.first_print","historicalContext":[{"label":"2026-06 BLS first-print level, dollars/hour","value":37.64},{"label":"2026-05 level printed in June release, dollars/hour","value":37.51},{"label":"2026-04 level printed in June release, dollars/hour","value":37.41},{"label":"2026-03 FRED/BLS mirror level, dollars/hour","value":37.35},{"label":"2026-02 FRED/BLS mirror level, dollars/hour","value":37.27}],"drivers":["Target is already released as of run date; forecast records the public first print with a timing-discrepancy note","BLS Table B-3 total private AHE rose 13 cents to $37.64 in June","Recent monthly wage-growth reference class centered near 0.26 percent","Payroll growth slowed and unemployment was 4.2 percent, reducing pressure for an upside wage surprise"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm?source=post_page---------------------------","https://www.bls.gov/news.release/archives/empsit_07022026.htm","https://fred.stlouisfed.org/series/CES0500000003","https://www.bls.gov/news.release/archives/empsit_06052026.htm"],"runAt":"2026-07-31T14:57:24Z","reasoning":[{"kind":"heading","text":"US private average hourly earnings MoM, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: the ledger target is average-hourly-earnings-mom-june-2026, dataPointId bls.ces.average_hourly_earnings_private.june_2026.first_print, and the relevant BLS variant is CES average hourly earnings of all employees on private nonfarm payrolls, total private, seasonally adjusted, Table B-3, series CES0500000003. I found a ledger discrepancy: the sourceBinding points to a level series with a multiply transform, while the slug and targetUnit percent_growth require a month-over-month percent-growth transform; I keep the same target and resolve growth from the first-print level values."},{"kind":"tool","tool":"official.lookup","call":"BLS Employment Situation release schedule lookup for reference month June 2026","result":"Fetched official schedule numbers: June 2026 Employment Situation release date Jul. 02, 2026 at 08:30 AM; May 2026 release date Jun. 05, 2026 at 08:30 AM; July 2026 release date Aug. 07, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"BLS archived Employment Situation release for June 2026, Table B-3 and release text","result":"Fetched first-print numbers from the July 2, 2026 BLS archive: average hourly earnings rose 13 cents, or 0.3 percent, to $37.64; Table B-3 total private values were June 2025 $36.36, April 2026 $37.41, May 2026 $37.51, June 2026 $37.64; total nonfarm payroll employment was +57,000 and unemployment was 4.2 percent."},{"kind":"tool","tool":"history.lookup","call":"FRED/BLS mirror for CES0500000003 recent observations and metadata","result":"Fetched recent series numbers for CES0500000003: Jun 2026 37.64, May 2026 37.51, Apr 2026 37.41, Mar 2026 37.35, Feb 2026 37.27; source is U.S. Bureau of Labor Statistics, release Employment Situation, dollars per hour, seasonally adjusted, monthly."},{"kind":"tool","tool":"official.lookup","call":"BLS May 2026 Employment Situation archive for pre-release wage context","result":"Fetched prior-release numbers: May 2026 release printed total private average hourly earnings at $37.53, up 12 cents or 0.3 percent; it printed March 2026 $37.35 and April 2026 $37.41; total nonfarm payrolls increased 172,000 and unemployment was 4.3 percent."},{"kind":"text","text":"Base rate/reference class: recent same-series monthly growth was the anchor, using the fetched total private SA level sequence Jan 2026 37.15, Feb 2026 37.27, Mar 2026 37.35, Apr 2026 37.41, May 2026 37.51, Jun 2026 37.64. The corresponding monthly growth observations are 0.323, 0.215, 0.161, 0.267, and 0.347 percent, giving a recent base rate near 0.262 percent before the already-public June print is applied."},{"kind":"math","text":"Prior/update/interval: persistence prior = recent CES0500000003 monthly percent-growth reference class from Jan-Jun 2026 fetched levels; historical sample growths = 0.323, 0.215, 0.161, 0.267, 0.347 percent; adjustment components = +0.084 percentage point because the June first-print BLS release is already public and Table B-3 gives $37.64 versus $37.51, small downside from slower payroll growth (+57,000) already embodied in the print, no further revision adjustment because first-print rule; interval method = sample dispersion of the five fetched monthly growth values, sigma = 0.07469 percentage points, 80% half-width = 1.28*sigma = 0.09560 percentage points; final implied bounds = 0.34657 - 0.09560 = 0.25097 and 0.34657 + 0.09560 = 0.44218 percent."},{"kind":"math","text":"Point calculation: 100 * (37.64 / 37.51 - 1) = 0.346574 percent, rounded to 0.347 percent. This differs from the BLS release-text rounded 0.3 percent because the target is stored as percent_growth and the rule uses unrounded Table B-3 dollar levels."},{"kind":"text","text":"Counter-consideration: upside risk would have been a broader wage acceleration from tighter labor supply or compositional shifts that pushed the June level above about $37.68, landing above the interval; downside risk would have been weak service-sector pay or composition that held the level below about $37.60, landing below the interval; the observed first print is inside the interval."},{"kind":"forecast","point":0.347,"ciLow":0.251,"ciHigh":0.442}]}
