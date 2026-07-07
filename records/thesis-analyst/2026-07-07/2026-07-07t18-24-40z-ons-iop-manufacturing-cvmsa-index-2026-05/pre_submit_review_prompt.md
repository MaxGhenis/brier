# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ons.iop.manufacturing_cvmsa_index
- period: 2026-05
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "uk-manufacturing-output-index-may-2026"
- targetUnit: "index_points"
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
fb0cd1baad7a6f7052c0a81c99f471477c48b087c3c0564c3515a9f8fdccf023

# Draft forecast response
{"slug":"uk-manufacturing-output-index-may-2026","country":"UK","type":"data","title":"UK manufacturing output index, May 2026","question":"ONS Index of Production series K22A, C: manufacturing chained volume measure seasonally adjusted index, May 2026, first print","unit":"index_points","pointEstimate":101.6,"ciLow":100.3,"ciHigh":102.9,"confidence":0.8,"resolutionDate":"2026-07-16","resolutionSource":"Office for National Statistics Index of Production, UK: May 2026 and DIOP time series K22A","resolutionSourceUrl":"https://www.ons.gov.uk/economy/economicoutputandproductivity/output/timeseries/k22a/diop","resolutionRule":"Resolve to the first ONS-published value for 2026 MAY in time series K22A, IOP: C:MANUFACTURING: CVMSA, index base year 2023=100, rounded to one decimal as published in the first Index of Production, UK: May 2026 release. Ignore later revisions or corrections unless the first release itself is withdrawn before publication.","dataPointId":"ons.iop.manufacturing_cvmsa_index.2026-05.first_print","historicalContext":[{"label":"2026 APR latest K22A","value":101.5},{"label":"2026 MAR K22A","value":101.1},{"label":"2026 FEB K22A","value":99.9},{"label":"2026 JAN K22A","value":100.1},{"label":"2025 DEC K22A","value":100.0}],"drivers":["April 2026 level already above recent average","recent manufacturing three-month growth positive","monthly K22A changes remain noisy around a flat base rate","May first print may be affected by wider revisions opened back to January 2024"],"sourceContext":["https://www.ons.gov.uk/economy/economicoutputandproductivity/output/timeseries/k22a/diop","https://www.ons.gov.uk/releases/indexofproductionukmay2026","https://www.ons.gov.uk/economy/economicoutputandproductivity/output/bulletins/indexofproduction/april2026"],"runAt":"2026-07-07T18:25:05Z","reasoning":[{"kind":"heading","text":"UK manufacturing output index, May 2026 first print"},{"kind":"text","text":"Framing and exact resolver: this forecast targets ONS DIOP time series K22A, labelled IOP: C:MANUFACTURING: CVMSA. All anchors use the same chained volume measure, seasonally adjusted manufacturing index variant, base year 2023=100, not gross, non-seasonally adjusted, smoothed, or synthetic variants."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS K22A time-series page for DIOP manufacturing CVMSA index.","result":"The ONS page identified Series ID K22A, units index base year = 100, release date 12 June 2026, next release 16 July 2026, and recent monthly values 2026 JAN 100.1, 2026 FEB 99.9, 2026 MAR 101.1, 2026 APR 101.5."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS release page for Index of Production, UK: May 2026.","result":"The ONS release page gives the release date as 16 July 2026 at 7:00am and states the May 2026 release is not yet published as of this run."},{"kind":"tool","tool":"official.lookup","call":"Opened the ONS Index of Production, UK: April 2026 bulletin for latest official context.","result":"ONS reported April 2026 manufacturing up 0.4% on the month, production output 0.0% on the month, manufacturing up 0.6% in the three months to April 2026, and 8 of 13 manufacturing subsectors increased in April."},{"kind":"tool","tool":"official.lookup","call":"Read the official K22A monthly history from January 2022 through April 2026 on the ONS time-series page.","result":"Reference class values include 2022 JAN 99.3, 2023 JAN 99.1, 2024 JAN 100.6, 2025 JAN 99.0, 2026 JAN 100.1, and latest 2026 APR 101.5; the 51 monthly successive changes from 2022 FEB to 2026 APR sum to +2.2 index points."},{"kind":"text","text":"Base rate / reference class: the outside-view prior is persistence plus the 2022 JAN to 2026 APR K22A monthly-change distribution. That sample is centered close to flat, with mean monthly change about +0.04 index points, so the base rate alone would put May near 101.5 to 101.6."},{"kind":"text","text":"Level and momentum update: the latest level, 101.5 in April 2026, is above the 2025 annual value of 99.6 and the 2023 base of 100.0, while recent official momentum is positive: 99.9 in February, 101.1 in March, and 101.5 in April. I apply only a small positive current-release adjustment because the series is noisy and April already followed a large March rise."},{"kind":"math","text":"Prior/update/interval: persistence prior on K22A April 2026 = 101.5; historical sample = monthly K22A successive changes from 2022 FEB through 2026 APR, n = 51, mean change = +0.04, sum of changes = +2.2, sum of squared changes = 51.02; adjustment components = +0.04 base-rate drift, +0.10 recent manufacturing momentum, -0.04 mean reversion from the elevated April level, giving point 101.5 + 0.10 = 101.6. Interval method uses realized dispersion of successive level changes: sigma = 1.01, so 80% half-width is roughly 1.28*sigma = 1.29, rounded to 1.3 index points; 101.6 - 1.3 = 100.3 and 101.6 + 1.3 = 102.9."},{"kind":"text","text":"Counter-considerations: upside risk is a broad May gain across pharmaceuticals, electronics, and metals after April's 8 of 13 subsectors rising, which would land above the interval if K22A prints above 102.9. Downside risk is reversal in those volatile subsectors or a weak transport/electrical-equipment drag, which would land below the interval if K22A prints below 100.3. Outside the interval would most likely require a move larger than the recent monthly-change reference class expects or a revision-linked first-print discontinuity."},{"kind":"forecast","point":101.6,"ciLow":100.3,"ciHigh":102.9}]}
