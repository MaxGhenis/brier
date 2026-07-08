# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: us.dol.initial_claims.sa
- period: week_2026-07-04
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "initial-claims-week-2026-07-04"
- targetUnit: "thousands"
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
72f24d310cf044065f88b6654ae74f2cb4ee0ce1d2d26f0a4c902e038e215aa6

# Draft forecast response
{"slug":"initial-claims-week-2026-07-04","country":"US","type":"data","title":"US initial claims, week ending Jul 4 2026","question":"What will the U.S. Department of Labor report as the advance seasonally adjusted initial unemployment insurance claims for the week ending July 4, 2026, in the first print?","unit":"thousands","pointEstimate":217,"ciLow":204,"ciHigh":231,"confidence":0.8,"resolutionDate":"2026-07-09","resolutionSource":"U.S. Department of Labor Unemployment Insurance Weekly Claims news release","resolutionSourceUrl":"https://www.dol.gov/ui/data.pdf","resolutionRule":"Resolve to the advance first-print seasonally adjusted Initial Claims figure for regular state programs, reported in thousands, for the week ending July 4, 2026 in the U.S. Department of Labor Unemployment Insurance Weekly Claims release published July 9, 2026. Use the first published print only; do not revise for later revisions or same-day corrections unless DOL republishes the first release before the public 8:30 a.m. ET embargo lift.","dataPointId":"us.dol.initial_claims.sa.week_2026-07-04.first_print","historicalContext":[{"label":"2026-06-27 initial claims SA","value":215},{"label":"2026-06-20 initial claims SA","value":216},{"label":"2026-06-13 initial claims SA","value":227},{"label":"2026-06-06 initial claims SA","value":230},{"label":"2025-07-05 initial claims SA","value":228}],"drivers":["Latest first-print level was low at 215k after a revised 216k prior week","Four-week average of 222k points modestly above the latest weekly print","Recent 2026 changes are volatile but centered near flat","Early-July seasonal adjustment risk is material around holiday weeks","No release-calendar exception applies before July 9, 2026"],"sourceContext":["https://www.dol.gov/ui/data.pdf","https://oui.doleta.gov/unemploy/claims_arch.asp","https://oui.doleta.gov/unemploy/claims.asp"],"runAt":"2026-07-08T02:44:47Z","thresholdLadder":{"thresholds":[198,203,208,212,215,218,221,224,228,232,236,242],"cumulativeProbabilities":[0.04,0.09,0.18,0.3,0.42,0.53,0.64,0.74,0.84,0.91,0.96,0.98]},"reasoning":[{"kind":"heading","text":"Forecast for DOL seasonally adjusted initial claims, week ending July 4, 2026"},{"kind":"text","text":"Framing and exact resolver: the target is the DOL Unemployment Insurance Weekly Claims advance seasonally adjusted Initial Claims figure for regular state programs, in thousands, for the week ending July 4, 2026, first print only. The variant is seasonally adjusted, not NSA, and all anchors below use the same SA initial-claims variant unless explicitly described as release-schedule context."},{"kind":"tool","tool":"official.lookup","call":"Opened current DOL UI Weekly Claims news release PDF at https://www.dol.gov/ui/data.pdf","result":"Fetched latest SA initial claims: week ending June 27, 2026 = 215 thousand; previous revised week ending June 20, 2026 = 216 thousand; change = -1 thousand; 4-week moving average = 222 thousand."},{"kind":"tool","tool":"official.lookup","call":"Read DOL historical SA claims table in the same weekly claims PDF","result":"Fetched recent SA initial claims history: June 6, 2026 = 230 thousand; June 13, 2026 = 227 thousand; June 20, 2026 = 216 thousand; June 27, 2026 = 215 thousand; comparable July 5, 2025 = 228 thousand."},{"kind":"tool","tool":"official.lookup","call":"Checked DOL Office of Unemployment Insurance weekly claims archive publication schedule at https://oui.doleta.gov/unemploy/claims_arch.asp","result":"Fetched publication schedule: weekly UI Claims News Release is published each Thursday at 8:30 AM EST, with listed 2026 exception Wednesday November 25, 2026 at 8:30 AM EST; therefore Thursday July 9, 2026 is the verified release date for the July 4, 2026 week."},{"kind":"tool","tool":"official.lookup","call":"Opened DOL UI Weekly Claims Data page at https://oui.doleta.gov/unemploy/claims.asp to confirm the current official data surface","result":"Fetched page metadata: Unemployment Insurance Weekly Claims Data page updated July 7, 2026; page describes initial claims as measuring emerging unemployment and continued weeks claimed as the number of persons claiming unemployment benefits."},{"kind":"text","text":"Reference class and base rate: for a one-week-ahead SA initial-claims print, the most relevant reference class is the DOL weekly SA history in the current release table. Over the fetched 54 weekly values from June 21, 2025 through June 27, 2026, levels mostly sit around 200k-236k, with the latest four weeks 230k, 227k, 216k, and 215k and the latest 4-week average at 222k. The base rate is therefore a near-flat next print around the latest level to recent average, before holiday-week and noise adjustments."},{"kind":"text","text":"Level, momentum, one-off, and policy mechanisms: level anchors at 215k latest and 222k four-week average; momentum is slightly down over the last two weeks, from 227k to 216k to 215k; one-off risk is elevated because the target week includes the July 4 holiday and seasonal factors can be imperfect; policy mechanisms do not point to an abrupt claims regime change by this release."},{"kind":"math","text":"Prior/update/interval: persistence prior model starts from latest SA initial claims of 215k with the 4-week-average anchor at 222k and comparable 2025 early-July value of 228k; historical sample is the fetched DOL SA weekly table from June 21, 2025 through June 27, 2026. Adjustment components: +2k toward the recent average, -1k for short-term downward momentum, +1k for early-July seasonal-noise skew, giving a center near 217k. From successive weekly changes in the fetched table, sample sigma = 10.4 thousand, so 1.28*sigma = 13.3 thousand. A symmetric 80% interval around 217k would be about 204k to 230k; the ladder-implied 80% bounds are 204k to 231k, essentially the same width and not widened beyond the realized-dispersion reference."},{"kind":"math","text":"Ladder: P(X <= 198) = 0.04; P(X <= 203) = 0.09; P(X <= 208) = 0.18; P(X <= 212) = 0.30; P(X <= 215) = 0.42; P(X <= 218) = 0.53; P(X <= 221) = 0.64; P(X <= 224) = 0.74; P(X <= 228) = 0.84; P(X <= 232) = 0.91; P(X <= 236) = 0.96; P(X <= 242) = 0.98. Linear interpolation gives the 10th percentile between 203 and 208 at 203.6, rounded to 204; the median between 215 and 218 at 217.2, rounded to 217; and the 90th percentile between 228 and 232 at 231.4, rounded to 231."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in filings after holiday timing or state processing backlogs, especially if the latest 215k print understated the run rate; that would land above the interval if the print exceeds 231k. Downside risk is another unusually clean SA print with broad state declines, which would land below the interval if the print is under 204k. Outside the interval is most likely from seasonal-adjustment error around the July 4 week rather than from a true labor-market break."},{"kind":"forecast","point":217,"ciLow":204,"ciHigh":231}]}
