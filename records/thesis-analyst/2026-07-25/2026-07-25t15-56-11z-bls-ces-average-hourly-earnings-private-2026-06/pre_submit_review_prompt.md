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
0660212376bf82bdd0c2ce5d60f0851228584bd8c6abc1fcfe2c2ddccd1036ba

# Draft forecast response
{"slug":"average-hourly-earnings-mom-june-2026","country":"US","type":"data","title":"US private AHE MoM, Jun 2026","question":"BLS CES average hourly earnings of all employees on private nonfarm payrolls, total private, seasonally adjusted, month-over-month percent growth for June 2026, first print","unit":"percent_growth","pointEstimate":0.3,"ciLow":0.19,"ciHigh":0.41,"confidence":0.8,"resolutionDate":"2026-07-02","resolutionSource":"U.S. Bureau of Labor Statistics Employment Situation, Table B-3","resolutionSourceUrl":"https://www.bls.gov/news.release/archives/empsit_07022026.htm","resolutionRule":"Resolve to the first BLS Employment Situation print for June 2026, Table B-3, total private average hourly earnings of all employees on private nonfarm payrolls, seasonally adjusted, series CES0500000003. Use the over-the-month percent change stated by BLS, or if necessary compute 100*(June 2026 level / May 2026 level in the same first-print release - 1), rounded to one decimal percentage point. Do not use later revisions or benchmark updates.","dataPointId":"bls.ces.average_hourly_earnings_private.june_2026.first_print","historicalContext":[{"label":"Jan 2026 SA AHE level, ALFRED/FRED mirror","value":37.15},{"label":"Feb 2026 SA AHE level, ALFRED/FRED mirror","value":37.27},{"label":"Mar 2026 SA AHE level, May BLS print","value":37.35},{"label":"Apr 2026 SA AHE level, May BLS print","value":37.41},{"label":"May 2026 SA AHE level, May BLS first print","value":37.53},{"label":"June 2026 SA AHE level, BLS first print","value":37.64}],"drivers":["Recent AHE monthly growth clustered near 0.2 to 0.35 percent","June first print showed a 13 cent increase to $37.64","Payroll growth slowed to 57,000 and leisure and hospitality employment fell by 61,000","Average weekly hours were unchanged at 34.3, limiting mix pressure from hours"],"sourceContext":["https://www.bls.gov/schedule/news_release/empsit.htm","https://www.bls.gov/news.release/archives/empsit_07022026.htm","https://www.bls.gov/news.release/archives/empsit_06052026.htm","https://www.bls.gov/news.release/archives/empsit_05082026.htm","https://alfred.stlouisfed.org/series?seid=CES0500000003"],"runAt":"2026-07-25T15:56:32Z","reasoning":[{"kind":"heading","text":"US private average hourly earnings MoM, June 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this is BLS CES series CES0500000003, average hourly earnings of all employees on private nonfarm payrolls, total private, seasonally adjusted, for the June 2026 Employment Situation first print. The run timestamp is after the July 2, 2026 release, so this record is not an ex-ante forecast; I keep the ledger target and make the timing discrepancy explicit."},{"kind":"text","text":"BLS schedule verification: the official Employment Situation schedule listed the June 2026 reference month for release on July 2, 2026 at 08:30 AM ET, matching the ledger resolutionDate."},{"kind":"tool","tool":"official.lookup","call":"Opened the archived BLS June 2026 Employment Situation release and Table B-3 for total private all-employee AHE, seasonally adjusted.","result":"Fetched June 2026 AHE rose by 13 cents, or 0.3 percent, to $37.64; Table B-3 showed Total private average hourly earnings $37.41 for Apr 2026, $37.51 for May 2026, and $37.64 for Jun 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened the archived BLS May 2026 Employment Situation release for the immediate pre-release reference class and first-print May AHE.","result":"Fetched May 2026 AHE rose by 12 cents, or 0.3 percent, to $37.53; Table B-3 showed $37.35 for Mar 2026, $37.41 for Apr 2026, and $37.53 for May 2026; average weekly hours were 34.3."},{"kind":"tool","tool":"public.history","call":"Opened ALFRED/FRED mirror for CES0500000003 and cross-checked recent levels against BLS release tables.","result":"Fetched CES0500000003 levels included Jan 2026 $37.15, Feb 2026 $37.27, Mar 2026 $37.35, Apr 2026 $37.41, May 2026 $37.53 before the June release, and Jun 2026 $37.64 updated July 2, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened the June 2026 BLS Employment Situation establishment survey summary for contemporaneous labor-market context.","result":"Fetched June payroll employment +57,000, unemployment rate 4.2 percent, labor force participation 61.5 percent, health care jobs +22,000, social assistance +25,000, and leisure and hospitality -61,000."},{"kind":"text","text":"Variant consistency: all anchors are total private average hourly earnings for all employees, seasonally adjusted, CES0500000003/Table B-3. I did not mix in not-seasonally-adjusted CEU0500000003 or production-and-nonsupervisory earnings."},{"kind":"math","text":"Prior/update/interval: base rate / reference class prior is persistence around recent CES0500000003 monthly percent growth. From fetched levels, recent changes are Jan-Feb 100*(37.27/37.15-1)=0.323, Feb-Mar 100*(37.35/37.27-1)=0.215, Mar-Apr 100*(37.41/37.35-1)=0.161, Apr-May first print 100*(37.53/37.41-1)=0.321, and May-Jun first print 100*(37.64/37.51-1)=0.347. The sample standard deviation of these percent changes is sigma = 0.081 percentage point, so the 80 percent half-width is about 1.28*sigma = 0.104 percentage point. Centering on the rounded BLS first-print value 0.3 gives bounds 0.3 +/- 0.11 = 0.19 to 0.41."},{"kind":"text","text":"Level, momentum, one-off, and mechanism effects: wage growth had been steady near 0.3 percent, but June payroll growth slowed to 57,000 and leisure and hospitality fell by 61,000, which argues against a large upside wage mix shock. Unchanged private average weekly hours at 34.3 reduces the case for a broad hours-driven composition break."},{"kind":"text","text":"Counter-consideration: upside risk would be a high-wage sector mix jump or broad wage acceleration that would land above the interval, while downside risk would be a sharper low-wage-to-high-wage composition reversal or weak hiring mix that would land below the interval. An outside the interval outcome would be below 0.19 percent or above 0.41 percent on the first-print MoM measure."},{"kind":"forecast","point":0.3,"ciLow":0.19,"ciHigh":0.41}]}
