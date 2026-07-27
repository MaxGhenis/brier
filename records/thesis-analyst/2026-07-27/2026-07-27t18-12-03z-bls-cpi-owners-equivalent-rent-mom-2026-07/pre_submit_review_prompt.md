# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.cpi.owners_equivalent_rent_mom
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-cpi-owners-equivalent-rent-mom-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.cpi.owners_equivalent_rent_mom.2026_07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org"], "expectedReleaseWindow": {"end": "2026-08-12", "start": "2026-08-12"}, "field": "CUSR0000SEHC", "releasePolicy": "first_print", "sourceSeriesId": "CUSR0000SEHC", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=CUSR0000SEHC", "table": "Consumer Price Index, U.S. city average, monthly seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-27-f4b72ba7dad3ac2c455b575ad60048778d8042f7b8fd1be3f386dbf34b25af80.json"
- targetContentHash: "f4b72ba7dad3ac2c455b575ad60048778d8042f7b8fd1be3f386dbf34b25af80"
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
4edf1902ea706038be50fa6ff1fe894631d96f7eb64e2c1e9b31ca0d96bedabb

# Draft forecast response
{"slug":"us-cpi-owners-equivalent-rent-mom-july-2026","country":"US","type":"data","title":"US CPI OER MoM, July 2026","question":"What will the first-print month-over-month percent change be for BLS CPI-U Owners' equivalent rent of residences in U.S. city average, seasonally adjusted, series CUSR0000SEHC, for July 2026?","unit":"percent_growth","pointEstimate":0.25,"ciLow":0.1,"ciHigh":0.4,"confidence":0.8,"resolutionDate":"2026-08-12","resolutionSource":"U.S. Bureau of Labor Statistics Consumer Price Index release, CPI-U series CUSR0000SEHC","resolutionSourceUrl":"https://data.bls.gov/timeseries/CUSR0000SEHC","resolutionRule":"Resolve to the first-print July 2026 seasonally adjusted CPI-U Owners' equivalent rent of residences index for U.S. city average, series CUSR0000SEHC, released by BLS on August 12, 2026. Compute percent_growth as (July 2026 index / June 2026 index - 1) * 100 using the first published index values, rounded to two decimals for this forecast cell; ignore later revisions, annual seasonal-adjustment revisions, and ALFRED/FRED backfilled vintages.","dataPointId":"bls.cpi.owners_equivalent_rent_mom.2026_07.first_print","historicalContext":[{"label":"Jun 2026 MoM from BLS index 441.741 vs 440.683","value":0.24},{"label":"May 2026 MoM from BLS index 440.683 vs 439.379","value":0.297},{"label":"Apr 2026 MoM from BLS index 439.379 vs 437.051","value":0.533},{"label":"Mar 2026 MoM from BLS index 437.051 vs 435.813","value":0.284}],"drivers":["Recent OER monthly growth slowed to 0.24% in June after a 0.53% April spike and 0.30% May reading","June CPI release said shelter rose only 0.1% while OER rose 0.2%, favoring a below-early-2026 pace","OER is a large and lagged shelter component, so month-to-month volatility is usually limited versus energy or goods","First-print target is seasonally adjusted CPI-U series CUSR0000SEHC, not NSA shelter or rent of primary residence"],"sourceContext":["https://www.bls.gov/schedule/news_release/cpi.htm","https://data.bls.gov/timeseries/CUSR0000SEHC","https://www.bls.gov/news.release/cpi.nr0.htm?form=MG0AV3","https://www.bls.gov/cpi/factsheets/owners-equivalent-rent-and-rent.htm"],"runAt":"2026-07-27T18:12:12Z","reasoning":[{"kind":"heading","text":"Forecast for July 2026 CPI-U owners' equivalent rent MoM"},{"kind":"text","text":"Framing and exact resolver: the target is BLS CPI-U Owners' equivalent rent of residences in U.S. city average, seasonally adjusted, series CUSR0000SEHC. The forecast is the July 2026 first-print month-over-month percent change, computed from the first published July and June index levels; this uses the same seasonally adjusted variant for all anchors."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Consumer Price Index release calendar for the July 2026 reference month.","result":"BLS lists Consumer Price Index for July 2026 with release date Aug. 12, 2026 and release time 08:30 AM; adjacent CPI release rows include June 2026 on Jul. 14, 2026 and August 2026 on Sep. 11, 2026."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS public time-series table for CUSR0000SEHC, seasonally adjusted CPI-U owners' equivalent rent of residences.","result":"BLS table shows CUSR0000SEHC values: Dec 2025 433.884, Jan 2026 434.837, Feb 2026 435.813, Mar 2026 437.051, Apr 2026 439.379, May 2026 440.683, Jun 2026 441.741."},{"kind":"tool","tool":"official.lookup","call":"Checked the June 2026 BLS CPI news release for contemporaneous shelter and OER context.","result":"BLS reported all-items CPI -0.4% SA in June 2026, all items less food and energy 0.0%, shelter +0.1%, and owners' equivalent rent +0.2% in June 2026."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS rent and owners' equivalent rent factsheet for component importance and definition context.","result":"BLS relative-importance table for December 2025 lists shelter at 35.625, owners' equivalent rent of residences at 26.204, rent of primary residence at 7.840, and lodging away from home at 1.289 percent of the CPI market basket."},{"kind":"text","text":"Base rate/reference class: using the latest continuous official CUSR0000SEHC first-print style history from Dec 2025 through Jun 2026, the six observed 2026 monthly changes are 0.220%, 0.224%, 0.284%, 0.533%, 0.297%, and 0.240%, with a mean near 0.300%. The June rounded OER print of 0.2% and the softer shelter aggregate argue for a July point below that six-month mean but not a break from the positive OER trend."},{"kind":"math","text":"Prior/update/interval: persistence prior is recent official CUSR0000SEHC MoM history, with the Jan-Jun 2026 reference class above. Adjustment components: start from the six-month mean 0.300%, subtract 0.04 pp for the latest June 0.240% value being below the mean, subtract 0.01 pp because June shelter was only 0.1%, and keep 0.00 pp for one-off energy/goods effects because they do not directly drive OER. Point = 0.300 - 0.040 - 0.010 = 0.250%. Interval method: realized sample dispersion of the six monthly OER values gives sigma = 0.118 percentage points; 1.28*sigma = 0.151 pp, so the 80% interval is about 0.250 +/- 0.151 = 0.099 to 0.401, rounded to 0.10 to 0.40."},{"kind":"text","text":"Counter-considerations: upside risk is a renewed catch-up in sampled rents after April's 0.533% jump, which would land above the interval if July OER prints above 0.40%. Downside risk is a broad shelter deceleration following June's 0.1% shelter increase, which would land below the interval if July OER is under 0.10%. Outside the interval would likely require either another April-like rotation shock or an abrupt near-zero rent-equivalence print."},{"kind":"forecast","point":0.25,"ciLow":0.1,"ciHigh":0.4}]}
