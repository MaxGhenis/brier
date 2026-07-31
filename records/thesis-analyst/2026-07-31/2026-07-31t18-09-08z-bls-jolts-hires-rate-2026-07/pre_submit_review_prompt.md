# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.jolts.hires_rate
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "jolts-hires-rate-july-2026"
- country: "US"
- targetUnit: "percent"
- dataPointId: "bls.jolts.hires_rate.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-09-08", "start": "2026-08-31"}, "field": "JTSHIR", "releasePolicy": "first_print", "sourceSeriesId": "JTSHIR", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=JTSHIR", "table": "JOLTS news release, Table 1", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-31-e671b0edb90aafc5fc73877f6a8d96e8c7fcb0a1580cbaa97f206d4e787cc5d8.json"
- targetContentHash: "e671b0edb90aafc5fc73877f6a8d96e8c7fcb0a1580cbaa97f206d4e787cc5d8"
- registrationCommit: "7ecbc85cc4110060218f856d50321ab93db3af3b"
- registeredAtUtc: "2026-07-31T18:02:17Z"
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
e0841093f1e320496e55204d40250d2ca1898b368f6beeac2fc1663cc2b58065

# Draft forecast response
{"slug":"jolts-hires-rate-july-2026","country":"US","type":"data","title":"US JOLTS hires rate, July 2026","question":"What will the BLS first-print seasonally adjusted total nonfarm hires rate be for July 2026 in the Job Openings and Labor Turnover Survey?","unit":"percent","pointEstimate":3.3,"ciLow":3.1,"ciHigh":3.5,"confidence":0.8,"resolutionDate":"2026-09-01","resolutionSource":"U.S. Bureau of Labor Statistics Job Openings and Labor Turnover Survey","resolutionSourceUrl":"https://data.bls.gov/timeseries/JTS000000000000000HIR","resolutionRule":"Resolve to the first value published by BLS for the seasonally adjusted total nonfarm hires rate, series JTS000000000000000HIR / FRED mirror JTSHIR, for July 2026 in the JOLTS release. The unit is percent, rounded to one decimal. Use the first official print only; ignore later monthly revisions, annual benchmark revisions, and later vintage changes except as archival evidence of the first print.","dataPointId":"bls.jolts.hires_rate.2026_07.first_print","historicalContext":[{"label":"May 2026 latest SA total nonfarm hires rate","value":3.3},{"label":"April 2026 SA total nonfarm hires rate","value":3.3},{"label":"March 2026 SA total nonfarm hires rate","value":3.5},{"label":"February 2026 SA total nonfarm hires rate","value":3.1},{"label":"January 2026 SA total nonfarm hires rate","value":3.4},{"label":"July 2025 SA total nonfarm hires rate","value":3.3}],"drivers":["Recent hires rate has been pinned near 3.3 percent","May 2026 BLS release described hires as unchanged at 5.2 million and 3.3 percent","Low labor-market churn keeps the persistence prior strong","Two-month forecast horizon allows June and July volatility but not a regime-break assumption","First-print rounded-to-one-decimal target makes 3.3 the modal bin"],"sourceContext":["https://www.bls.gov/schedule/news_release/jolts.htm?stream=business","https://www.bls.gov/schedule/2026/","https://www.bls.gov/news.release/archives/jolts_06302026.htm","https://fred.stlouisfed.org/data/JTSHIR","https://data.bls.gov/timeseries/JTS000000000000000HIR"],"runAt":"2026-07-31T18:09:36Z","reasoning":[{"kind":"heading","text":"US JOLTS total nonfarm hires rate, July 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this forecast is for the BLS JOLTS seasonally adjusted total nonfarm hires rate, series JTS000000000000000HIR, mirrored as JTSHIR, for reference month July 2026. The release variant is seasonally adjusted, total nonfarm, rate, first print, in percent rounded to one decimal."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS JOLTS release schedule page for the reference-month release date.","result":"The BLS schedule lists July 2026 JOLTS for Sep. 01, 2026 at 10:00 AM, June 2026 JOLTS for Aug. 04, 2026 at 10:00 AM, and August 2026 JOLTS for Sep. 29, 2026 at 10:00 AM."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS 2026 selected-release calendar as an official date cross-check.","result":"The September 2026 calendar lists Tuesday, September 1, 2026 at 10:00 AM for Job Openings and Labor Turnover Survey for July 2026; the August 2026 calendar lists Tuesday, August 04, 2026 at 10:00 AM for June 2026."},{"kind":"tool","tool":"official.lookup","call":"Read the BLS May 2026 JOLTS release archive and Table A / Table 1 text for the latest official print available before this run.","result":"For May 2026, BLS reported hires unchanged at 5.2 million and the hires rate unchanged at 3.3 percent; Table A showed total hires of 5,170 thousand in May 2026, 5,215 thousand in April 2026, and 5,328 thousand in May 2025, with rates of 3.3, 3.3, and 3.4 percent respectively."},{"kind":"tool","tool":"history.lookup","call":"Read FRED/ALFRED public JTSHIR history as a mirror of BLS series JTS000000000000000HIR.","result":"Recent JTSHIR values were May 2026 3.3, Apr 2026 3.3, Mar 2026 3.5, Feb 2026 3.1, Jan 2026 3.4, Dec 2025 3.3, Nov 2025 3.2, Oct 2025 3.3, Sep 2025 3.3, and Aug 2025 3.2 percent."},{"kind":"tool","tool":"history.lookup","call":"Pulled a recent reference-class window from the FRED JTSHIR table for realized dispersion and persistence checks.","result":"The 2024-01 through 2026-05 rate path included 2024-01 3.6, 2024-06 3.3, 2024-12 3.3, 2025-06 3.4, 2025-07 3.3, 2025-12 3.3, 2026-01 3.4, 2026-02 3.1, 2026-03 3.5, 2026-04 3.3, and 2026-05 3.3 percent."},{"kind":"text","text":"Reference class and base rate: since early 2024 the total nonfarm seasonally adjusted hires rate has mostly sat in a narrow 3.2 to 3.6 percent band, with July 2025 at 3.3 percent and the latest May 2026 print also 3.3 percent. That makes a persistence base rate around 3.3 percent the right starting point."},{"kind":"math","text":"Prior/update/interval: persistence prior = latest May 2026 value of 3.3 percent, with a small level adjustment of 0.0 because BLS described hires as unchanged and recent churn indicators were stable; momentum adjustment = 0.0 because Apr-to-May was 0.0 and the recent 3-month average is about (3.5+3.3+3.3)/3 = 3.37, which rounds near 3.3; one-off/policy adjustment = 0.0 because there is no official-source evidence of a July hiring regime break. For the 2024-01 to 2026-05 fetched window, successive monthly changes have sample sigma = 0.13 percentage point; 80 percent half-width = 1.28*sigma = 1.28*0.13 = 0.166 percentage point, rounded to the one-decimal target as about 0.2. Final implied bounds: 3.3 - 0.2 = 3.1 and 3.3 + 0.2 = 3.5."},{"kind":"text","text":"Counter-considerations: upside risk would come from summer leisure, retail, or government hiring rebounding enough to push the rounded first print to 3.6 or higher, which would land above the interval. Downside risk would come from a broad hiring freeze or sharp payroll slowdown pushing the first print to 3.0 or lower, which would land outside the interval below. The middle case is that low churn persists and July rounds to 3.3."},{"kind":"forecast","point":3.3,"ciLow":3.1,"ciHigh":3.5}]}
