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
{"slug":"initial-claims-week-2026-07-11","country":"US","type":"data","title":"US Initial Claims, Week Ending Jul 11","question":"What will the U.S. Department of Labor report as the advance seasonally adjusted initial claims for unemployment insurance for the week ending July 11, 2026, first print?","unit":"thousands","pointEstimate":216,"ciLow":202,"ciHigh":230,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"U.S. Department of Labor Employment and Training Administration Unemployment Insurance Weekly Claims release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance first-print U.S. total seasonally adjusted initial claims figure, in thousands, for the week ending July 11, 2026, as published by the U.S. Department of Labor Employment and Training Administration in the Unemployment Insurance Weekly Claims release dated July 16, 2026. Use the release's rounded thousand value; ignore later revisions and ALFRED/FRED vintage updates except as mirrors of the first official print.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-11","historicalContext":[{"label":"latest_week_2026-07-04_sa_initial_claims","value":215},{"label":"prior_week_2026-06-27_sa_initial_claims_revised","value":217},{"label":"week_2026-06-20_sa_initial_claims","value":216},{"label":"latest_4wk_average_2026-07-04","value":218.75},{"label":"prior_year_comparable_week_sa_initial_claims","value":228}],"drivers":["Latest SA initial claims were 215 thousand, down 2 thousand from the revised prior week.","The 4-week average fell to 218.75 thousand, keeping the near-term level around the high 210s.","Seasonally adjusted continuing claims were stable at 1814 thousand for the lagged week, not signaling a fresh layoff break.","July holiday-week adjustment can create noise, but the target is the SA advance print from the same DOL variant."],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims.asp"],"runAt":"2026-07-10T03:05:28Z","reasoning":[{"kind":"heading","text":"Forecast for DOL SA Initial Claims, Week Ending July 11, 2026"},{"kind":"text","text":"Framing and exact resolver: the target is the U.S. Department of Labor Employment and Training Administration advance seasonally adjusted U.S. initial claims value, series code ICSA in the ledger, for week ending July 11, 2026, first print only. The DOL release dated July 16, 2026 is the resolver; FRED/ALFRED can mirror the vintage but is not the final authority."},{"kind":"tool","tool":"official.lookup","call":"Opened the current DOL UI Weekly Claims PDF release at https://www.dol.gov/ui/data.pdf.","result":"The DOL release was embargoed until 8:30 A.M. Eastern on Thursday, July 9, 2026; for week ending July 4, 2026, advance SA initial claims were 215,000, down 2,000 from the prior week's revised 217,000."},{"kind":"tool","tool":"official.lookup","call":"Read the national summary table in the same DOL release.","result":"The table reports Initial Claims (SA) of 215,000 for July 4, 217,000 for June 27, 216,000 for June 20, and 228,000 for the comparable prior-year week; the 4-week moving average was 218,750."},{"kind":"tool","tool":"official.lookup","call":"Read the DOL continuing-claims and OUI data-page context.","result":"The DOL release reports seasonally adjusted insured unemployment of 1,814,000 for week ending June 27, up 8,000 from 1,806,000; the OUI weekly claims data page was updated July 9, 2026."},{"kind":"text","text":"Variant check: every numeric anchor used here is the DOL seasonally adjusted U.S. initial claims variant from the weekly release, in thousands, matching the target unit and the ICSA-style target. NSA state totals such as 224,583 for July 4 are used only as qualitative context, not as target-history inputs."},{"kind":"text","text":"Reference class and base rate: for the 2026 year-to-date SA initial-claims sequence through July 4, the level mostly sat in the 201-230 thousand range, with a recent 4-week average of 218.75 thousand. A persistence base rate around the latest 215 thousand is stronger than a trend-extrapolated jump because the latest four weekly changes were +5, -3, +1, and -2 thousand."},{"kind":"math","text":"Prior/update/interval: persistence prior model on the DOL SA initial-claims level uses the January 3-July 4, 2026 historical sample of weekly changes: -6, +9, +1, +19, 0, -22, +3, +3, -1, -8, +6, -8, +15, -10, +7, -25, +9, +13, -2, +2, +13, +5, -3, -11, +1, -2 thousand. The average change is +0.3, so latest 215 + 0.3 gives 215.3; level/momentum adjustment is +0.5 for the still-low but slightly below-average latest print, one-off July-holiday noise adjustment is 0 after seasonal adjustment, and policy-mechanism adjustment is 0. Rounded point = 216. For interval sizing, sigma = 10.4 from those successive changes; 1.28*sigma = 13.3, rounded to a 14 thousand half-width, giving final implied bounds 216 - 14 = 202 and 216 + 14 = 230."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed education, transportation, or manufacturing layoff pulse like the prior large state moves, which would land above the interval if SA claims print above 230 thousand. Downside risk is another broad low-layoff week with holiday-seasonal factors absorbing NSA filings, which would land below the interval if the first print is under 202 thousand. Outside the interval would therefore require a weekly move larger than roughly the recent 80% one-week change range."},{"kind":"forecast","point":216,"ciLow":202,"ciHigh":230}]}
