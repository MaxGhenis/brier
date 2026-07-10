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
{"slug":"bea-disposable-personal-income-level-june-2026","country":"US","type":"data","title":"US disposable personal income, June 2026","question":"BEA disposable personal income (DSPI / account code A067RC), June 2026, billions of dollars at a seasonally adjusted annual rate, first print.","unit":"usd_billions","pointEstimate":23730.0,"ciLow":23606.5,"ciHigh":23853.5,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"BEA Personal Income and Outlays, Table 2.6 (DSPI / account code A067RC), first release","resolutionSourceUrl":"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DSPI&vintage_date=2026-06-25","resolutionRule":"Resolve through the canonical ledger generic-url binding at the supplied ALFRED DSPI CSV URL, field DSPI, with first_print policy, to the BEA disposable personal income series DSPI / account code A067RC for June 2026, in billions of dollars at a seasonally adjusted annual rate, rounded to one decimal. Ignore later revisions. BEA provenance is the Personal Income and Outlays first release; the supplied ALFRED vintage_date appears to correspond to the prior May 2026 print, so this discrepancy is noted but the forecast remains tied to the retained ledger binding.","dataPointId":"bea.disposable_personal_income.level.june_2026.first_print","historicalContext":[{"label":"January 2026 DSPI","value":23395.9},{"label":"February 2026 DSPI","value":23382.4},{"label":"March 2026 DSPI","value":23510.4},{"label":"April 2026 DSPI","value":23486.9},{"label":"May 2026 DSPI","value":23651.7}],"drivers":["May's unusually large farm-payment contribution should fade","June payroll and wage growth support a continued nominal-income gain","Personal-current-tax and transfer-receipt movements remain the main residual uncertainty"],"sourceContext":["https://www.bea.gov/news/2026/personal-income-and-outlays-may-2026","https://www.bea.gov/news/schedule/full","https://fred.stlouisfed.org/series/DSPI","https://www.bls.gov/news.release/archives/empsit_07022026.htm"],"runAt":"2026-07-10T15:31:54Z","reasoning":[{"kind":"heading","text":"June 2026 BEA disposable personal income first-print forecast"},{"kind":"text","text":"The target is current-dollar disposable personal income, BEA Table 2.6 line 27 / account code A067RC, in billions of dollars at a seasonally adjusted annual rate. The official BEA schedule verifies that Personal Income and Outlays for June 2026 is scheduled for July 30, 2026 at 8:30 a.m. EDT. The retained ledger resolver uses an ALFRED DSPI URL whose 2026-06-25 vintage is the prior May print; I retain that binding and its strict first_print, no-later-revisions rule."},{"kind":"tool","tool":"history.lookup","call":"Fetched the DSPI history mirror for the BEA series, using the same monthly SAAR current-dollar variant as the target.","result":"FRED, sourced to BEA and identifying account code A067RC, reports DSPI of 23,395.9 in Jan 2026, 23,382.4 in Feb, 23,510.4 in Mar, 23,486.9 in Apr, and 23,651.7 billion dollars SAAR in May."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest official BEA Personal Income and Outlays release and its Table 2.6-linked figures.","result":"BEA's May release reports DPI increased $164.9 billion (0.7 percent) in May; its release table reports May DSPI 23,651.7, April 23,486.9, May personal income 26,916.4, and May personal saving 704.2 billion dollars SAAR."},{"kind":"tool","tool":"official.lookup","call":"Fetched the official BLS June Employment Situation as a contemporaneous input to June wage income.","result":"BLS reports June nonfarm payroll employment rose 57,000, private average hourly earnings rose $0.13 (0.3 percent) to $37.64, aggregate weekly payrolls rose 0.4 percent, and the unemployment rate was 4.2 percent."},{"kind":"text","text":"The reference class/base rate is the latest four successive monthly DSPI changes: -13.5, +128.0, -23.5, and +164.8 billion dollars SAAR. May's large gain reflected farm proprietors' income and a second round of USDA Supplemental Disaster Relief Program payments, an explicitly identified one-off component rather than a stable monthly trend."},{"kind":"math","text":"Prior/update/interval: I use a persistence-plus-mean-change prior from the Jan-May 2026 same-variant DSPI history. The four successive changes have mean +63.95 and sample sigma = 96.5 billion; 1.28*sigma = 123.5 billion. Starting at May's 23,651.7, the prior implies 23,715.7. I add about 14.3 for June's positive wage/payroll signal, but do not carry forward May's farm-payment surge, giving 23,730.0. The 80% interval is 23,730.0 +/- 123.5 = [23,606.5, 23,853.5], exactly the historical-dispersion width."},{"kind":"text","text":"Counter-consideration: upside risk is a further large farm-payment or transfer-receipt increase, or unexpectedly low personal current taxes, which could put June DSPI above 23,853.5. Downside risk is a sharper reversal of farm proprietors' income, weaker compensation, or higher taxes; a combined reversal would land below 23,606.5 and outside the interval."},{"kind":"forecast","point":23730.0,"ciLow":23606.5,"ciHigh":23853.5}]}
