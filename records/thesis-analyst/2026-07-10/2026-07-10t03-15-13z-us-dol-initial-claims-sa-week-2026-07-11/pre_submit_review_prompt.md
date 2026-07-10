# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: us.dol.initial_claims.sa
- period: week_2026-07-11
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-11"
- targetUnit: "thousands"
- dataPointId: "us.dol.initial_claims.sa.week_2026-07-11"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-18", "start": "2026-07-14"}, "field": "ICSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "ICSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA", "table": "ALFRED graph CSV", "transform": {"factor": 0.001, "operation": "multiply"}}
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
bdbbe3bfe36feba9ab551bb61fa50f21a565a9a138b4a5e9b57bdfc0d89f9f3d

# Draft forecast response
{"slug":"initial-claims-week-2026-07-11","country":"US","type":"data","title":"US initial claims, week ending July 11","question":"What will the U.S. Department of Labor report as the advance seasonally adjusted initial unemployment claims for the week ending July 11, 2026, in the first print?","unit":"thousands","pointEstimate":216,"ciLow":204,"ciHigh":228,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims release","resolutionSourceUrl":"https://www.dol.gov/newsroom/releases/eta/eta20260716","resolutionRule":"Resolve to the advance seasonally adjusted initial claims figure for the week ending July 11, 2026, reported in the first U.S. Department of Labor Unemployment Insurance Weekly Claims release issued for that week, in thousands of claims. Use the first print only; do not incorporate later revisions, corrected later vintages, or FRED/ALFRED revisions. If the exact newsroom URL differs, use the DOL UI Weekly Claims release/archive for the July 16, 2026 release.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-11","historicalContext":[{"label":"2026-07-04 advance SA initial claims","value":215},{"label":"2026-06-27 advance SA initial claims","value":215},{"label":"2026-06-20 advance SA initial claims","value":215},{"label":"2026-06-13 advance SA initial claims","value":226},{"label":"2026-06-06 advance SA initial claims","value":229},{"label":"2026-07-04 SA 4-week average","value":218.75}],"drivers":["latest advance SA print held at 215 thousand","four-week average near 219 thousand","late-June pullback from the early-June 229 thousand local high","holiday and auto-retooling seasonal residual risk around early July","continued claims rate steady at 1.2 percent"],"sourceContext":["https://oui.doleta.gov/unemploy/claims_arch.asp","https://www.dol.gov/newsroom/releases/eta","https://www.dol.gov/newsroom/releases/eta/eta20260709","https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA"],"runAt":"2026-07-10T03:15:36Z","reasoning":[{"kind":"heading","text":"US advance seasonally adjusted initial claims for week ending July 11, 2026"},{"kind":"text","text":"Framing and exact resolver: this is the DOL Employment and Training Administration advance seasonally adjusted initial claims series, ICSA-equivalent, for the week ending July 11, 2026, in thousands, resolved on the first official DOL weekly claims release and not from later revised vintages."},{"kind":"tool","tool":"official.lookup","call":"Checked DOL Office of Unemployment Insurance claims archive publication schedule.","result":"The archive page says the UI Weekly Claims News Release is published each week Thursday morning at 8:30 AM EST, lists Wednesday November 25, 2026 at 8:30 AM EST as the only non-Thursday exception shown, and was updated July 9, 2026; for the week ending Saturday July 11, 2026, the scheduled Thursday release date is July 16, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched the July 9, 2026 DOL UI Weekly Claims release for the latest official print.","result":"For week ending July 4, 2026, advance seasonally adjusted initial claims were 215,000, down 2,000 from the previous week's revised 217,000; the 4-week moving average was 218,750, down 3,750; advance insured unemployment for week ending June 27 was 1,814,000 and the insured unemployment rate was 1.2 percent."},{"kind":"tool","tool":"official.lookup","call":"Read recent DOL ETA weekly claims release snippets on the DOL newsroom releases page for same-variant advance SA initial claims.","result":"Recent advance SA first prints were: July 4 215,000; June 27 215,000; June 20 215,000; June 13 226,000; June 6 229,000; May 30 225,000; May 23 215,000; May 16 209,000; May 9 211,000; May 2 200,000; April 25 189,000."},{"kind":"tool","tool":"official.lookup","call":"Checked the latest DOL PDF table for same-release context and prior-year comparison.","result":"The July 9 release table labeled Seasonally Adjusted Data shows Initial Claims (SA) 215,000 for July 4, 217,000 for June 27, change -2,000, June 20 at 216,000, and prior-year comparable week 228,000; the same table shows Initial Claims (NSA) 224,583 for July 4 and 214,616 for June 27."},{"kind":"text","text":"Base rate/reference class: for the same advance SA variant, the near-term reference class is weekly first prints from late April through early July 2026, which moved from 189 thousand to 229 thousand before flattening at 215 thousand for three straight advance prints."},{"kind":"text","text":"Level and momentum: the latest level is 215 thousand, the latest DOL 4-week average is 218.75 thousand, and the local momentum has cooled from early-June highs of 229 thousand and 226 thousand to the mid-210s. A pure persistence forecast is 215, while a 4-week-average pull is about 219."},{"kind":"text","text":"Mechanism adjustment: early July can be noisy because holiday timing and auto-plant retooling interact with seasonal factors, but the SA series already adjusts for normal July layoffs. I give only a small upward adjustment from persistence because the last three advance readings are flat at 215 thousand and continuing-claims context is not signaling a sharp layoff break."},{"kind":"math","text":"Prior/update/interval: persistence prior = 215 from the latest advance SA first print; historical sample = the last 11 fetched advance SA first prints in thousands, 189, 200, 211, 209, 215, 225, 229, 226, 215, 215, 215; adjustment components = +2 toward the 218.75 four-week average, -1 for the late-June downshift, +0 holiday residual after seasonal adjustment, giving point 216. Weekly changes in the fetched sample are +11, +11, -2, +6, +10, +4, -3, -11, 0, 0, so sigma = 7.2 thousand and 1.28*sigma = 9.2 thousand; I widen to a 12 thousand half-width, within 1.75x, because early-July seasonal residuals can create larger one-week misses, yielding 204 to 228."},{"kind":"text","text":"Counter-consideration: upside risk is a seasonal-adjustment miss or state-level layoff spike that would push the first print above 228 thousand; downside risk is another broad decline in filings after the June pullback that would land below 204 thousand. Outside the interval would require a move larger than the recent ordinary week-to-week dispersion, not just another 215 thousand plateau print."},{"kind":"forecast","point":216,"ciLow":204,"ciHigh":228}]}
