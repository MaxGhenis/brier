# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: us.dol.initial_claims.sa
- period: week_2026-07-25
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-25"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "us.dol.initial_claims.sa.week_2026-07-25"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-08-01", "start": "2026-07-28"}, "field": "ICSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "ICSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA", "table": "ALFRED graph CSV", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-20-14230433262478cb1134d42fc94b9c1eab391028cc750beb6151ad05ce20889a.json"
- targetContentHash: "14230433262478cb1134d42fc94b9c1eab391028cc750beb6151ad05ce20889a"
- registrationCommit: "134572ec0e53debeec96716bf346510a889628ee"
- registeredAtUtc: "2026-07-20T18:27:38Z"
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
f9c731ee340318a2c849ab111eca07b3ee31a4e55639d41b3930cec6316de421

# Draft forecast response
{"slug":"initial-claims-week-2026-07-25","country":"US","type":"data","title":"US initial claims, week ending July 25","question":"What will the advance first print of US seasonally adjusted initial unemployment insurance claims be for the week ending July 25, 2026?","unit":"thousands","pointEstimate":212,"ciLow":202,"ciHigh":222,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"U.S. Department of Labor Unemployment Insurance Weekly Claims Report","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance figure for seasonally adjusted initial claims for the week ending July 25, 2026, published by the U.S. Department of Labor on July 30, 2026, expressed in thousands and rounded to the nearest thousand. Use that first official print only; ignore subsequent revisions.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-25","historicalContext":[{"label":"week ending 2026-07-11","value":208},{"label":"week ending 2026-07-04","value":216},{"label":"week ending 2026-06-27","value":217},{"label":"week ending 2026-06-20","value":216},{"label":"week ending 2026-06-13","value":227}],"drivers":["Recent claims level near 208 thousand","Partial mean reversion toward the five-week average","Low recent week-to-week dispersion","Holiday-related seasonal-adjustment uncertainty"],"sourceContext":["https://alfred.stlouisfed.org/series?seid=ICSA","https://oui.doleta.gov/unemploy/archive.asp","https://fred.stlouisfed.org/releases/calendar?m=&ob=n&od=asc&rid=180&ve=2026-12-31&vs=2026-01-01&y="],"runAt":"2026-07-21T01:02:00Z","reasoning":[{"kind":"heading","text":"Advance initial claims forecast for the week ending July 25, 2026"},{"kind":"text","text":"The target is the advance first print of national seasonally adjusted initial claims, series ICSA, for the week ending Saturday, July 25, 2026. The DOL publication schedule says the report is issued Thursday at 8:30 a.m. Eastern and lists only November 25 as a 2026 exception; the release calendar confirms July 30. Resolution therefore uses the July 30 DOL report without later revisions."},{"kind":"tool","tool":"official.lookup","call":"Inspect the DOL Employment and Training Administration UI claims archive and publication schedule.","result":"The schedule states weekly publication on Thursday at 8:30 a.m. Eastern and identifies 1 exceptional 2026 release date, November 25; therefore the July 25 reference week is scheduled for July 30, 2026."},{"kind":"tool","tool":"alfred.lookup","call":"Fetch recent ICSA observations from the public ALFRED history mirror.","result":"Seasonally adjusted ICSA values, in thousands, were 227 on 2026-06-13, 216 on 2026-06-20, 217 on 2026-06-27, 216 on 2026-07-04, and 208 on 2026-07-11."},{"kind":"tool","tool":"calendar.lookup","call":"Check the published Unemployment Insurance Weekly Claims Report release calendar.","result":"The calendar lists releases on July 23 and July 30, 2026, both at 7:30 a.m. Central, equivalent to 8:30 a.m. Eastern."},{"kind":"text","text":"The five-week reference class has a 216.8-thousand mean and a 208-thousand latest observation. The base rate is short-horizon persistence with modest mean reversion: the level is low relative to that recent mean, while the sequence 227, 216, 217, 216, 208 does not show an accelerating rise."},{"kind":"text","text":"Level contributes a 208-thousand anchor; momentum is mildly negative; mean reversion contributes about +4 thousand; no verified policy mechanism warrants a large displacement. Holiday-related seasonal adjustment around early July is the main one-off uncertainty. All anchors refer to the same seasonally adjusted advance ICSA variant."},{"kind":"math","text":"Prior/update/interval: The model is persistence plus partial mean reversion, using the five fetched observations 227, 216, 217, 216, and 208. Successive changes are -11, +1, -1, and -8 thousand; their sample standard deviation is sigma = sqrt(96.75/3) = 5.7 thousand per week. The unseen July 18 release makes this effectively a two-step forecast, so the horizon-adjusted sigma is 5.7*sqrt(2) = 8.1 and the 80% half-width is roughly 1.28*sigma = 10.4 thousand. The 208 persistence prior plus a +4-thousand mean-reversion adjustment and approximately zero net momentum, one-off, and policy adjustments gives 212; rounding 212 ± 10.4 to whole thousands implies bounds of 202 and 222."},{"kind":"text","text":"Upside risk comes from a renewed burst of layoffs or unusually adverse seasonal adjustment and would land above the interval if the first print exceeds 222 thousand. Downside risk comes from continued unusually low filings or favorable seasonal adjustment and would land below the interval if the first print is under 202 thousand."},{"kind":"forecast","point":212,"ciLow":202,"ciHigh":222}]}
