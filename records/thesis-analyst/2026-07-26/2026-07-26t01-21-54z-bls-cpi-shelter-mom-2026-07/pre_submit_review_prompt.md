# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cpi.shelter_mom
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-cpi-shelter-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.cpi.shelter_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-12", "start": "2026-08-12"}, "field": "CUSR0000SAH1", "releasePolicy": "first_print", "sourceSeriesId": "CUSR0000SAH1", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CUSR0000SAH1", "table": "Consumer Price Index, U.S. city average, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-26-5c82767a6ab5fb1c8b9100ba47b05d629ddfb3651373d64f7772cdbd833e5ad9.json"
- targetContentHash: "5c82767a6ab5fb1c8b9100ba47b05d629ddfb3651373d64f7772cdbd833e5ad9"
- registrationCommit: "145f6612f225710a4621f124b13bf5d5ae5d97ac"
- registeredAtUtc: "2026-07-26T00:55:04Z"
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
39429e0ac45c022fbea33f443df7a94614064216046220c9c0ee6d2603e0912e

# Draft forecast response
{"slug":"us-cpi-shelter-mom-july-2026","country":"US","type":"data","title":"US CPI Shelter MoM, July 2026","question":"What will the first-print seasonally adjusted month-over-month percent change be for BLS CPI-U shelter in U.S. city average, series CUSR0000SAH1, for July 2026?","unit":"percent_growth","pointEstimate":0.24,"ciLow":0.03,"ciHigh":0.45,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Consumer Price Index release","resolutionSourceUrl":"https://www.bls.gov/news.release/cpi.t01.htm","resolutionRule":"Resolve to the first BLS CPI release for July 2026, published August 12, 2026, using the seasonally adjusted CPI-U shelter series for U.S. city average, CUSR0000SAH1. Compute month-over-month percent growth from the first-print July 2026 and June 2026 seasonally adjusted index levels as 100*(July/June - 1), or use the BLS first-print seasonally adjusted percent-change table if exact index levels are not exposed at resolution time. Do not revise for later seasonal-adjustment revisions or subsequent corrections unless the first-print file itself is replaced before ordinary publication.","dataPointId":"bls.cpi.shelter_mom.2026_07.first_print","historicalContext":[{"label":"2026-06 shelter SA MoM","value":0.1},{"label":"2026-05 shelter SA MoM","value":0.3},{"label":"2026-04 shelter SA MoM","value":0.6},{"label":"2026-03 shelter SA MoM","value":0.3},{"label":"2026-02 shelter SA MoM","value":0.2},{"label":"2026-01 shelter SA MoM","value":0.2},{"label":"2025-12 shelter SA MoM","value":0.4}],"drivers":["Shelter inflation slowed sharply in June but rent and OER remained positive","Lodging away from home was a one-month drag that may partly unwind","Recent seven-month shelter reference class centers near 0.30 percent","July first print resolves from the same seasonally adjusted CPI-U shelter variant"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm","https://www.bls.gov/news.release/cpi.nr0.htm","https://www.bls.gov/news.release/cpi.t01.htm","https://fred.stlouisfed.org/series/CUSR0000SAH1","https://alfred.stlouisfed.org/series?seid=CUSR0000SAH1"],"runAt":"2026-07-26T01:22:14Z","reasoning":[{"kind":"heading","text":"US CPI-U shelter month-over-month forecast for July 2026"},{"kind":"text","text":"Framing and exact resolver: this targets the first-print July 2026 seasonally adjusted CPI-U shelter index for U.S. city average, series CUSR0000SAH1. The ledger uses ALFRED/FRED as the first-print binding, but the economic source is BLS; FRED/ALFRED is only a history mirror."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS CPI release schedule for the July 2026 CPI reference month.","result":"BLS lists Consumer Price Index for July 2026 on August 12, 2026 at 08:30 AM, and the June CPI release also states the July 2026 CPI is scheduled for Wednesday, August 12, 2026 at 8:30 a.m. ET."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS current CPI release Table A for the same CPI-U shelter seasonally adjusted percent-change variant.","result":"Shelter seasonally adjusted MoM percent changes were Dec 2025 0.4, Jan 2026 0.2, Feb 2026 0.2, Mar 2026 0.3, Apr 2026 0.6, May 2026 0.3, Jun 2026 0.1; the 12-month shelter change in June 2026 was 3.3."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS CPI Table 1 component details for shelter, rent, and owners' equivalent rent.","result":"In June 2026 Table 1, shelter relative importance was 35.149, shelter SA MoM was 0.1, rent of primary residence SA MoM was 0.1, and owners' equivalent rent SA MoM was 0.2."},{"kind":"tool","tool":"history.lookup","call":"Checked FRED/ALFRED mirror for CUSR0000SAH1 index levels and latest update timing.","result":"CUSR0000SAH1 was Jun 2026 428.501, May 2026 427.998, Apr 2026 426.642, Mar 2026 424.069, Feb 2026 422.942; FRED showed updated Jul 14, 2026 8:10 AM CDT and next release date Aug 12, 2026."},{"kind":"text","text":"Reference class/base rate: the recent same-variant BLS shelter MoM reference class is the seven printed monthly changes from Dec 2025 through Jun 2026. Its mean is 0.30 percent, but the last print was 0.1 and the exact CUSR0000SAH1 index calculation gives Jun about 0.118 and May about 0.318, so the short-term trend is below the mean."},{"kind":"text","text":"Level, momentum, one-off, and mechanism effects: shelter still has positive rent and OER mechanics, with June rent at 0.1 and OER at 0.2, but the aggregate was pulled down by lodging away from home falling 2.3 percent in June. I treat that lodging move as a partial one-off drag, while keeping some disinflationary momentum from the softer rent/OER prints."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class prior is the Dec 2025-Jun 2026 BLS shelter MoM mean of 0.30 percent. Updates are -0.08 for June's soft exact 0.118 reading and lower rent/OER momentum, +0.03 for partial lodging-drag reversal, and -0.01 for core services softness, giving 0.30 - 0.08 + 0.03 - 0.01 = 0.24. Interval method uses realized dispersion of the seven BLS printed shelter MoM values themselves: sigma = 0.163; 1.28*sigma = 0.209, so the 80 percent interval is 0.24 +/- 0.21 = [0.03, 0.45] after rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a rebound in lodging away from home plus firmer OER that would land above the interval, especially if July shelter returns near April's 0.6. Downside risk is another weak lodging month or sharper rent slowdown that would land outside the interval below 0.03."},{"kind":"forecast","point":0.24,"ciLow":0.03,"ciHigh":0.45}]}
