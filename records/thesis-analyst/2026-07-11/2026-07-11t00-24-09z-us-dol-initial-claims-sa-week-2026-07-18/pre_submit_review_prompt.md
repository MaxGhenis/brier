# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: us.dol.initial_claims.sa
- period: week_2026-07-18
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-18"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "us.dol.initial_claims.sa.week_2026-07-18"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-07-25", "start": "2026-07-21"}, "field": "ICSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "ICSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA", "table": "ALFRED graph CSV", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-11-744098c1b345176f966ba181700538215eeef034556de85c3664a099ad0ebe9f.json"
- targetContentHash: "744098c1b345176f966ba181700538215eeef034556de85c3664a099ad0ebe9f"
- registrationCommit: "acccfc0a6925ff3385b5c0e29b544fb6310a3f73"
- registeredAtUtc: "2026-07-11T00:23:25Z"
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
8349effe59579877d852c712cc029b97e7a75b8dc7c7ab1fc67026762fadf7b0

# Draft forecast response
{"slug":"initial-claims-week-2026-07-18","country":"US","type":"data","title":"US initial claims, week ending July 18","question":"What will the advance first-print number of US seasonally adjusted initial unemployment insurance claims be for the week ending July 18, 2026?","unit":"thousands","pointEstimate":216,"ciLow":203,"ciHigh":229,"confidence":0.8,"resolutionDate":"2026-07-23","resolutionSource":"U.S. Department of Labor Unemployment Insurance Weekly Claims release","resolutionSourceUrl":"https://www.dol.gov/agencies/eta/ui-claims","resolutionRule":"Resolve to the advance first-print seasonally adjusted US initial claims figure for the week ending July 18, 2026, in the DOL release scheduled for July 23, 2026, expressed in thousands and rounded to the nearest thousand. Ignore all subsequent revisions.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-18","historicalContext":[{"label":"week ending 2026-07-04 advance SA","value":215},{"label":"week ending 2026-06-27 comparison SA","value":217},{"label":"week ending 2026-06-20 comparison SA","value":216},{"label":"week ending 2026-06-13 comparison SA","value":227},{"label":"week ending 2025-07-19 SA reference","value":218}],"drivers":["recent claims level near 215 thousand","four-week average declining to 218.75 thousand","stable low insured-unemployment rate","July seasonal-adjustment volatility"],"sourceContext":["https://www.dol.gov/newsroom/releases/eta/eta20260709","https://www.dol.gov/sites/dolgov/files/OPA/newsreleases/ui-claims/20261132.pdf","https://www.dol.gov/newsroom/releases?agency=39&page=0&state=All&topic=132&year=all","https://www.dol.gov/agencies/eta/ui-claims"],"runAt":"2026-07-11T00:24:33Z","reasoning":[{"kind":"heading","text":"Advance US initial claims for the week ending July 18, 2026"},{"kind":"text","text":"The target is the DOL advance first print for US initial claims, seasonally adjusted, for the week ending July 18, 2026. The DOL schedule verifies release on Thursday, July 23, 2026. Resolution uses the advance SA figure only, not NSA claims, the four-week average, or a revised vintage; the series is ICSA and the release table is UNEMPLOYMENT INSURANCE DATA FOR REGULAR STATE PROGRAMS."},{"kind":"tool","tool":"official.lookup","call":"Read the July 9, 2026 DOL Weekly Claims release and its regular-state-program table.","result":"DOL reported advance SA initial claims of 215 thousand for July 4, 2026; the comparison levels were 217 thousand for June 27 and 216 thousand for June 20, while the four-week average was 218.75 thousand."},{"kind":"tool","tool":"official.lookup","call":"Read recent DOL Weekly Claims releases for the same seasonally adjusted initial-claims variant.","result":"The same-variant sequence for May 30 through July 4 was 225, 230, 227, 216, 217, and 215 thousand; the latest weekly change was -2 thousand."},{"kind":"tool","tool":"official.lookup","call":"Read the historical table embedded in the July 9 DOL release for the comparable July period and recent 2026 changes.","result":"The historical table shows 2025 SA claims of 228 thousand on July 5, 221 thousand on July 12, and 218 thousand on July 19; its 27 weekly changes from January 3 through July 4, 2026 range from -25 to +19 thousand."},{"kind":"text","text":"The reference class and base rate are low-volatility weekly claims observations outside recession: the latest six same-variant readings center near 218 thousand, while the comparable July 2025 sequence declined from 228 to 218 thousand. Persistence therefore anchors the forecast near 215-218 thousand."},{"kind":"text","text":"Level is about 215 thousand and recent momentum is mildly downward; one-off holiday and auto-retooling seasonality can create July noise even after adjustment. No official release evidence indicates a policy mechanism or broad layoffs requiring a large directional shift, so the net update is +1 thousand from the latest advance level."},{"kind":"math","text":"Prior/update/interval: The model is persistence around the latest 215 thousand observation, checked against the six-reading recent historical sample of 225, 230, 227, 216, 217, and 215. Adjustments are +1 thousand for mean reversion, 0 for weak downward momentum, 0 for policy, and 0 net for July one-offs, giving 216. For interval sizing, the 27 successive weekly changes from January 3 through July 4 have sum 12 and sum of squares 2748, so sample sigma = sqrt((2748 - 12^2/27)/(27-1)) = 10.27 thousand. The normal 80% half-width is 1.28*sigma = 13.15 thousand; 216 ± 13.15 rounds to final implied bounds of 203 and 229 thousand."},{"kind":"text","text":"Upside risk comes from concentrated auto-sector or other temporary layoffs and would land above the interval if the first print exceeds 229 thousand. Downside risk comes from unusually favorable seasonal adjustment or fewer filings and would land below the interval if the first print is under 203 thousand. Either outcome would be outside the interval and falsify the assumed calm-regime persistence model."},{"kind":"forecast","point":216,"ciLow":203,"ciHigh":229}]}
