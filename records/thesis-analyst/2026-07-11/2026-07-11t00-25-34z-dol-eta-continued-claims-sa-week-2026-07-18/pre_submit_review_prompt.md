# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: dol.eta.continued_claims.sa
- period: week_2026-07-18
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "continued-claims-week-2026-07-18"
- country: "US"
- targetUnit: "millions"
- dataPointId: "dol.eta.continued_claims.sa.week_2026-07-18.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"], "expectedReleaseWindow": {"end": "2026-08-01", "start": "2026-07-28"}, "field": "CCSA", "releasePolicy": "advance_vintage", "sourceSeriesId": "CCSA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CCSA", "table": "ALFRED graph CSV", "transform": {"factor": 1e-06, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-11-303f08a03edb98ea7f4d37396fa9d9285464d3539e074f49a39462ce133153f7.json"
- targetContentHash: "303f08a03edb98ea7f4d37396fa9d9285464d3539e074f49a39462ce133153f7"
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
664a7fc087cc10d82a4ac9ba5e3d7b89a6e1aab0fd9a9285ec02648c2f98685f

# Draft forecast response
{"slug":"continued-claims-week-2026-07-18","country":"US","type":"data","title":"US Continued Claims, July 18 Week","question":"What will the first-print U.S. seasonally adjusted continued claims level be for the week ending July 18, 2026?","unit":"millions","pointEstimate":1.828,"ciLow":1.806,"ciHigh":1.85,"confidence":0.8,"resolutionDate":"2026-07-30","resolutionSource":"U.S. Department of Labor Unemployment Insurance Weekly Claims release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance first-print seasonally adjusted insured unemployment level for the week ending July 18, 2026, in the U.S. Department of Labor release scheduled for July 30, 2026, converted from persons to millions and rounded to 0.001 million. Ignore all subsequent revisions.","dataPointId":"dol.eta.continued_claims.sa.week_2026-07-18.first_print","historicalContext":[{"label":"week ending 2026-06-27 first print","value":1.814},{"label":"week ending 2026-06-20 first print","value":1.814},{"label":"week ending 2026-06-13 first print","value":1.821},{"label":"week ending 2026-06-06 first print","value":1.81},{"label":"week ending 2026-05-30 first print","value":1.795}],"drivers":["Recent continued-claims level near 1.81 million","Mild positive five-week momentum","Initial claims steady near 215,000","Holiday-period seasonal-adjustment uncertainty"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://www.dol.gov/sites/dolgov/files/OPA/newsreleases/ui-claims/20261132.pdf","https://www.dol.gov/sites/dolgov/files/OPA/newsreleases/ui-claims/20261092.pdf","https://alfred.stlouisfed.org/series?seid=CCSA","https://www.dol.gov/index.php/newsroom/releases/opa/opa20200701"],"runAt":"2026-07-11T00:26:09Z","reasoning":[{"kind":"heading","text":"Continued claims for the week ending July 18, 2026"},{"kind":"text","text":"The target is ETA series CCSA: advance first-print U.S. insured unemployment, seasonally adjusted, for the week ending July 18—not the NSA level, four-week average, or a later revised vintage. Resolution uses the July 30 release and reports millions."},{"kind":"tool","tool":"official.lookup","call":"Checked the Department of Labor's official release-timing announcement and the target's calendar window.","result":"DOL states that Weekly Claims is released each Thursday at 8:30 a.m. ET; Thursday following the established two-week reporting lag for the week ending 2026-07-18 is 2026-07-30, within the registered 2026-07-28 to 2026-08-01 window."},{"kind":"tool","tool":"official.lookup","call":"Read DOL Weekly Claims releases for the recent seasonally adjusted insured-unemployment reference class.","result":"Fetched first-print SA insured unemployment of 1,795,000 for 2026-05-30, 1,810,000 for 2026-06-06, and 1,821,000 for 2026-06-13; DOL also reported the insured unemployment rate at 1.2%."},{"kind":"tool","tool":"official.lookup","call":"Checked the July 2 DOL release and ALFRED CCSA advance-vintage history for the latest weeks.","result":"Fetched first-print SA insured unemployment of 1,814,000 for 2026-06-20 and 1,814,000 for 2026-06-27; recent SA initial claims were 215,000 for both 2026-06-20 and 2026-06-27."},{"kind":"text","text":"Base rate/reference class: persistence dominates this weekly level series. The five first prints from May 30 through June 27 averaged 1.811 million, while their net change was only +0.019 million; steady initial claims near 0.215 million argue against an abrupt break."},{"kind":"math","text":"Prior/update/interval: persistence prior = 1.814 million, using the five first-print observations 1.795, 1.810, 1.821, 1.814, 1.814. Successive changes are +0.015, +0.011, -0.007, and 0.000 million; their mean is +0.00475 and sample sigma = 0.0101 million. Three-week momentum adds 3×0.00475 = 0.01425, giving 1.82825, rounded to 1.828. For a three-step horizon, sigma scales to 0.0101×sqrt(3) = 0.0175; the 80% half-width is roughly 1.28×sigma = 0.0224, yielding final implied bounds 1.806 to 1.850 million."},{"kind":"text","text":"Level and momentum point mildly upward, while stable initial claims provide no strong deterioration signal. Holiday-related seasonal adjustment is the main one-off risk; no discrete policy mechanism warrants an additional shift."},{"kind":"text","text":"Upside risk: a broad rise in benefit duration or delayed hiring could land above 1.850 million. Downside risk: faster claimant exits or unusually favorable seasonal adjustment could land below 1.806 million. Either outcome would be outside the interval."},{"kind":"forecast","point":1.828,"ciLow":1.806,"ciHigh":1.85}]}
