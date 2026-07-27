# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cpi.rent_primary_residence_mom
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-cpi-primary-rent-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.cpi.rent_primary_residence_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-12", "start": "2026-08-12"}, "field": "CUSR0000SEHA", "releasePolicy": "first_print", "sourceSeriesId": "CUSR0000SEHA", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CUSR0000SEHA", "table": "Consumer Price Index, U.S. city average, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-27-68ada9204070c13b03e259eb171ac8fc62e5b065f182f8ae9d1f736b2483025b.json"
- targetContentHash: "68ada9204070c13b03e259eb171ac8fc62e5b065f182f8ae9d1f736b2483025b"
- registrationCommit: "e494ebc7a9b410a6fcffab9e5439408ff3d09413"
- registeredAtUtc: "2026-07-27T18:01:44Z"
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
c525a94c3cfc46a21a0ed3ce0f8b7c3c3c3e9512dbac14f44ce2b7403f43f7e1

# Draft forecast response
{"slug":"us-cpi-primary-rent-mom-july-2026","country":"US","type":"data","title":"US CPI Primary Rent MoM, July 2026","question":"BLS CPI-U Rent of Primary Residence in U.S. city average (CUSR0000SEHA), July 2026, seasonally adjusted month-over-month percent growth, first official print","unit":"percent_growth","pointEstimate":0.22,"ciLow":0.09,"ciHigh":0.35,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Consumer Price Index release","resolutionSourceUrl":"https://data.bls.gov/timeseries/CUSR0000SEHA","resolutionRule":"Resolve to the first official BLS print for July 2026 CPI-U rent of primary residence, U.S. city average, seasonally adjusted series CUSR0000SEHA. Compute percent growth as 100*(July 2026 first-vintage index / June 2026 first-vintage index - 1), in percentage points, with no later revisions or same-day correction grace unless BLS replaces the first print before publication.","dataPointId":"bls.cpi.rent_primary_residence_mom.2026_07.first_print","historicalContext":[{"label":"2026-06 exact derived MoM from FRED level","value":0.1495},{"label":"2026-05 exact derived MoM from FRED level","value":0.3619},{"label":"2026-04 exact derived MoM from FRED level","value":0.5451},{"label":"2026-03 exact derived MoM from FRED level","value":0.1901},{"label":"BLS rounded 2026-06 SA MoM table value","value":0.1}],"drivers":["Latest rounded BLS table shows primary rent slowing to 0.1 percent SA MoM in June after 0.4 in May and 0.5 in April","Exact index-derived June growth was 0.1495 percent, below the recent valid-change mean of 0.2674 percent","Rent inflation is sticky and lagged, so one low month should pull the forecast down but not to zero","Recent dispersion from valid one-month changes supports an 80 percent band of about plus or minus 0.13 percentage point"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm","https://www.bls.gov/news.release/cpi.t02.htm","https://fred.stlouisfed.org/data/CUSR0000SEHA","https://alfred.stlouisfed.org/series?seid=CUSR0000SEHA"],"runAt":"2026-07-27T18:09:42Z","reasoning":[{"kind":"heading","text":"US CPI primary rent MoM forecast for July 2026"},{"kind":"text","text":"Framing and exact resolver: this targets the seasonally adjusted CPI-U rent of primary residence index for the U.S. city average, series CUSR0000SEHA, converted to month-over-month percent growth for July 2026 on the first official BLS print. The variant is seasonally adjusted, U.S. city average, not regional, not unadjusted, and not owners' equivalent rent."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS CPI release schedule for the July 2026 reference month.","result":"BLS lists Consumer Price Index for July 2026 with release date Aug. 12, 2026 and release time 08:30 AM; the adjacent June 2026 CPI release is listed for Jul. 14, 2026 at 08:30 AM."},{"kind":"tool","tool":"fred.lookup","call":"Fetched the latest CUSR0000SEHA seasonally adjusted index levels from the public FRED table, a BLS-sourced history mirror.","result":"CUSR0000SEHA levels: Feb 2026 441.865, Mar 2026 442.705, Apr 2026 445.118, May 2026 446.729, Jun 2026 447.397; source labels the series as Index 1982-1984=100, Seasonally Adjusted, Monthly, last updated 2026-07-14 8:10 AM CDT."},{"kind":"tool","tool":"official.lookup","call":"Checked BLS CPI Table 2 for the latest same-variant rounded percent-change row.","result":"BLS Table 2 for June 2026 shows Rent of primary residence relative importance 7.680, Jun 2025-Jun 2026 unadjusted percent change 2.8, May 2026-Jun 2026 unadjusted percent change 0.1, and seasonally adjusted percent changes Mar-Apr 0.5, Apr-May 0.4, May-Jun 0.1."},{"kind":"tool","tool":"fred.history","call":"Computed recent exact one-month percent changes from fetched CUSR0000SEHA levels, excluding the missing Oct 2025 FRED observation for the change calculation.","result":"Exact derived MoM values used for the reference class include Feb 2025 0.2869, Mar 2025 0.3084, Apr 2025 0.3239, May 2025 0.2298, Jun 2025 0.2292, Jul 2025 0.2338, Aug 2025 0.2853, Sep 2025 0.2156, Dec 2025 0.2704, Jan 2026 0.2490, Feb 2026 0.1314, Mar 2026 0.1901, Apr 2026 0.5451, May 2026 0.3619, Jun 2026 0.1495 percent."},{"kind":"text","text":"Base rate/reference class: the 15 valid recent exact index-derived monthly changes average 0.2674 percent. The latest rounded BLS table and exact June calculation point lower than that base rate, while the April and May prints argue against assuming the series has fully reset to a very low monthly pace."},{"kind":"math","text":"Prior/update/interval: persistence prior is the recent valid-change mean from CUSR0000SEHA, 0.2674 percent. Adjustment components: -0.06 pp for June's low exact 0.1495 percent and rounded BLS 0.1 percent signal, +0.01 pp for sticky rent renewal inertia, and +0.00 pp for no identified July-specific policy break, giving 0.2674 - 0.06 + 0.01 = 0.2174, rounded to 0.22. Interval method uses the sample standard deviation of the 15 valid recent exact MoM values: sigma = 0.099 percentage point. The 80 percent normal half-width is roughly 1.28*sigma = 1.28*0.099 = 0.127 percentage point, so 0.22 +/- 0.13 gives 0.09 to 0.35 after rounding."},{"kind":"text","text":"Counter-considerations: upside risk is a repeat of the April-May rebound in sampled rents or seasonal adjustment that would land above the interval, above 0.35 percent. Downside risk is another very soft rent sample or a correction in lagged market rents that would land below the interval, below 0.09 percent. Outside the interval would most likely reflect a data-processing or sampling surprise rather than a visible release-calendar issue."},{"kind":"forecast","point":0.22,"ciLow":0.09,"ciHigh":0.35}]}
