# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bea.disposable_personal_income.level
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bea-disposable-personal-income-level-june-2026"
- country: "US"
- targetUnit: "usd_billions"
- dataPointId: "bea.disposable_personal_income.level.june_2026.first_print"
- resolutionDate: "2026-07-30"
- resolutionSource: "ALFRED DSPI CSV source binding for BEA disposable personal income first print"
- resolutionSourceUrl: "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25"
- resolutionRule: "Resolve through the canonical ledger generic-url binding at the supplied ALFRED DSPI CSV URL, field DSPI, with first_print policy, to the BEA disposable personal income series DSPI / account code A067RC for June 2026, in billions of dollars at a seasonally adjusted annual rate, rounded to one decimal. Ignore later revisions. BEA provenance is the Personal Income and Outlays first release; the supplied ALFRED vintage_date appears to correspond to the prior May 2026 print, so this discrepancy is noted but the forecast remains tied to the retained ledger binding."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-07-29", "start": "2026-07-21"}, "field": "DSPI", "releasePolicy": "first_print", "sourceSeriesId": "DSPI", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25", "table": "Personal Income and Outlays, Table 1", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-123ce8782db84a3d7daf502c09b752d32f0756b451f512b2661b632666c8caf3.json"
- targetContentHash: "123ce8782db84a3d7daf502c09b752d32f0756b451f512b2661b632666c8caf3"
- registrationCommit: "0d80683b051be25572f40ea4731fa5062af6d211"
- registeredAtUtc: "2026-07-10T12:36:34Z"
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
2b3abc1222f5bee5a19c95a9a86ef34cdb0d01ab405a864e781fe1c4180b91f9

# Draft forecast response
{"slug":"bea-disposable-personal-income-level-june-2026","country":"US","type":"data","title":"US disposable personal income, June 2026","question":"What will BEA first report for June 2026 current-dollar disposable personal income, seasonally adjusted at an annual rate, in billions of dollars?","unit":"usd_billions","pointEstimate":23725.0,"ciLow":23615.0,"ciHigh":23830.0,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"ALFRED DSPI CSV source binding for BEA disposable personal income first print","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25","resolutionRule":"Resolve through the canonical ledger generic-url binding at the supplied ALFRED DSPI CSV URL, field DSPI, with first_print policy, to the BEA disposable personal income series DSPI / account code A067RC for June 2026, in billions of dollars at a seasonally adjusted annual rate, rounded to one decimal. Ignore later revisions. BEA provenance is the Personal Income and Outlays first release; the supplied ALFRED vintage_date appears to correspond to the prior May 2026 print, so this discrepancy is noted but the forecast remains tied to the retained ledger binding.","dataPointId":"bea.disposable_personal_income.level.june_2026.first_print","historicalContext":[{"label":"January 2026 DSPI","value":23395.9},{"label":"February 2026 DSPI","value":23382.4},{"label":"March 2026 DSPI","value":23510.4},{"label":"April 2026 DSPI","value":23486.9},{"label":"May 2026 DSPI","value":23651.7}],"drivers":["May level of $23,651.7 billion SAAR","Typical recent monthly level increase near $68.9 billion","Continued wage and salary growth","Likely unwind of May farm-support boost","Elevated nominal inflation supports the level"],"sourceContext":["https://www.bea.gov/news/2026/personal-income-and-outlays-may-2026","https://www.bea.gov/news/schedule/","https://fred.stlouisfed.org/data/DSPI","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25"],"runAt":"2026-07-10T17:07:08Z","reasoning":[{"kind":"heading","text":"June 2026 disposable personal income first-print forecast"},{"kind":"text","text":"The target is BEA current-dollar disposable personal income, DSPI / NIPA account code A067RC, in billions of dollars at a seasonally adjusted annual rate. All anchors use that nominal SAAR variant. Resolution is the first June 2026 print rounded to one decimal, with later revisions ignored. The retained ledger URL has vintage_date=2026-06-25, apparently the prior May-release vintage; this is a concrete binding discrepancy, but the forecast remains tied to the registered target."},{"kind":"tool","tool":"official.lookup","call":"Inspect BEA's official Personal Income and Outlays release schedule for the June 2026 report.","result":"BEA schedules Personal Income and Outlays, June 2026 for July 30, 2026 at 8:30 a.m. EDT."},{"kind":"tool","tool":"series.lookup","call":"Fetch the recent monthly DSPI level history from the FRED public mirror of the BEA series.","result":"DSPI was 23395.9 in January 2026, 23382.4 in February, 23510.4 in March, 23486.9 in April, and 23651.7 in May, all billions of dollars SAAR."},{"kind":"tool","tool":"official.lookup","call":"Inspect BEA's May 2026 Personal Income and Outlays first release for current-dollar DPI and related components.","result":"BEA reported May disposable personal income increased $164.9 billion, or 0.7%; personal income increased $181.6 billion, PCE increased $156.1 billion, and the PCE price index rose 0.4% month over month."},{"kind":"text","text":"The outside-view base rate uses the 12 successive DSPI changes from May 2025 through May 2026: 41.5, 139.0, 105.9, 82.6, -28.8, 48.0, 55.1, 230.0, -13.5, 128.0, -23.5, and 164.8 billion. Their median is 68.9 billion, providing a robust persistence prior for the June increase."},{"kind":"text","text":"Level and momentum favor another nominal increase from 23651.7. Wage and salary growth and elevated prices support the trend, while May's farm proprietors' income received a second round of Supplemental Disaster Relief Program payments, creating a one-off likely to fade in June. I therefore place the central increment near 73.3 billion, only modestly above the 68.9 billion reference-class median."},{"kind":"math","text":"Prior/update/interval: The model is a median-change persistence prior using the 12 monthly changes listed above. The sample standard deviation of those changes is sigma = 80.0 billion: sqrt(sum((change - 77.4)^2)/11) = sqrt(70488/11) = 80.0. A normal-reference 80% half-width is roughly 1.28*sigma = 1.28*80.0 = 102.4 billion. Starting from 23651.7, the 68.9 base-rate increment plus about 4.4 billion for continuing nominal wage/price momentum, tempered by expected fading of May farm support, gives 23725.0. The ladder implies bounds 110.0 below and 105.0 above the median, closely matching the 102.4 billion sigma half-width."},{"kind":"math","text":"Ladder: P(X <= 23550) = 0.03; P(X <= 23580) = 0.06; P(X <= 23615) = 0.10; P(X <= 23640) = 0.17; P(X <= 23670) = 0.28; P(X <= 23700) = 0.41; P(X <= 23725) = 0.50; P(X <= 23750) = 0.61; P(X <= 23780) = 0.73; P(X <= 23805) = 0.82; P(X <= 23830) = 0.90; P(X <= 23860) = 0.95; P(X <= 23900) = 0.98. Linear interpolation therefore gives q10=23615.0, q50=23725.0, and q90=23830.0 billion."},{"kind":"text","text":"Upside risk comes from stronger-than-expected payroll compensation, bonuses, transfers, or another farm-support payment and could put the print above 23830.0. Downside risk comes from a sharper unwind of May farm income, weaker wages, or higher personal taxes and could put it below 23615.0. Either outcome would land outside the interval."},{"kind":"forecast","point":23725.0,"ciLow":23615.0,"ciHigh":23830.0}],"thresholdLadder":{"thresholds":[23550,23580,23615,23640,23670,23700,23725,23750,23780,23805,23830,23860,23900],"cumulativeProbabilities":[0.03,0.06,0.1,0.17,0.28,0.41,0.5,0.61,0.73,0.82,0.9,0.95,0.98]}}
