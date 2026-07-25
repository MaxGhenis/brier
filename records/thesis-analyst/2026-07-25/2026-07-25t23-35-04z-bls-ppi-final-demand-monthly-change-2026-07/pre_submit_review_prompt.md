# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: bls.ppi.final_demand_monthly_change
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "bls-ppi-final-demand-monthly-change-july-2026"
- country: "US"
- targetUnit: "percent_growth"
- dataPointId: "bls.wp.WPSFD4.2026-07.first_print"
- sourceBinding: {"adapter": "alfred-fred", "allowedHosts": ["alfred.stlouisfed.org", "www.bls.gov"], "expectedReleaseWindow": {"end": "2026-08-19", "start": "2026-08-11"}, "field": "PPIFIS", "releasePolicy": "first_print", "sourceSeriesId": "PPIFIS", "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=PPIFIS", "table": "Producer Price Index, final demand, seasonally adjusted", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-25-7753f0f1a5d658edcefcd448d480f21171af349f95e6902b968abb25deb8d3b4.json"
- targetContentHash: "7753f0f1a5d658edcefcd448d480f21171af349f95e6902b968abb25deb8d3b4"
- registrationCommit: "6d2b1a2c61155c88851ab8dad6099ae6f9ef5823"
- registeredAtUtc: "2026-07-25T23:27:53Z"
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
178d1466a4fdc80f14d7840ef8dcb0627668db88f2f8c8edf40d8126d5231ceb

# Draft forecast response
{"slug":"bls-ppi-final-demand-monthly-change-july-2026","country":"US","type":"data","title":"US PPI Final Demand MoM, July 2026","question":"What will the U.S. Bureau of Labor Statistics first report for the seasonally adjusted one-month percent change in the Producer Price Index for final demand for July 2026?","unit":"percent_growth","pointEstimate":0.35,"ciLow":-0.16,"ciHigh":0.86,"confidence":0.8,"resolutionDate":"2026-08-13","resolutionSource":"U.S. Bureau of Labor Statistics Producer Price Index news release, Table 1","resolutionSourceUrl":"https://www.bls.gov/news.release/ppi.t01.htm","resolutionRule":"Resolve to the first BLS-published seasonally adjusted 1-month percent change for Final demand, group code FD item code 4, in the Producer Price Index news release for July 2026, scheduled for August 13, 2026 at 8:30 a.m. ET. Use the first print as published, in percent, rounded to the BLS one-decimal release value; do not replace it with later revisions.","dataPointId":"bls.wp.WPSFD4.2026-07.first_print","historicalContext":[{"label":"2026-06 final demand MoM SA first/current release","value":-0.3},{"label":"2026-05 final demand MoM SA","value":0.6},{"label":"2026-04 final demand MoM SA","value":1.1},{"label":"2026-03 final demand MoM SA","value":0.8},{"label":"2026-02 final demand MoM SA","value":0.5},{"label":"2026-01 final demand MoM SA","value":0.6},{"label":"2025-07 final demand MoM SA","value":0.8}],"drivers":["Recent final-demand PPI base rate is positive but volatile","June decline was energy-led and unlikely to repeat at the same size","Services inflation remained positive in June","July gasoline readings were rising by late month but still near or below the June monthly average","High 12-month PPI inflation keeps upside pressure on non-energy components"],"sourceContext":["https://www.bls.gov/schedule/news_release/ppi.htm","https://www.bls.gov/news.release/archives/ppi_07152026.htm","https://www.bls.gov/news.release/ppi.t01.htm","https://www.eia.gov/dnav/pet/pet_pri_gnd_a_epm0_pte_dpgal_w.htm","https://www.eia.gov/dnav/pet/pet_pri_gnd_a_epmr_pte_dpgal_m.htm"],"runAt":"2026-07-25T23:35:19Z","reasoning":[{"kind":"heading","text":"US PPI final demand monthly change for July 2026"},{"kind":"text","text":"Framing and exact resolver: this forecast targets the BLS Producer Price Index for final demand, seasonally adjusted, one-month percent change for July 2026, group code FD item code 4. The variant is the headline final-demand SA monthly percent change in Table 1, first print only, not the unadjusted 12-month change and not later revised data."},{"kind":"tool","tool":"official.lookup","call":"Checked the BLS Producer Price Index release schedule for the July 2026 reference month.","result":"BLS lists Producer Price Index for July 2026 with release date Aug. 13, 2026 and release time 08:30 AM; the full 2026 selected-release calendar also shows Producer Price Index for July 2026 on Thursday, August 13, 2026 at 08:30 AM."},{"kind":"tool","tool":"official.lookup","call":"Fetched the latest BLS PPI news release for June 2026 and Table A recent history for the same SA final-demand monthly-change variant.","result":"BLS reported final demand fell -0.3 percent in June 2026, advanced 0.6 percent in May 2026, and advanced 1.1 percent in April 2026; Table A also shows Jan. 2026 0.6, Feb. 2026 0.5, Mar. 2026 0.8, and July 2025 0.8."},{"kind":"tool","tool":"official.lookup","call":"Fetched BLS Table 1 component details for the latest release to separate energy, goods, and services mechanisms.","result":"For June 2026, Table 1 shows final demand -0.3, final demand goods -1.4, final demand energy -6.4, final demand foods -0.6, goods less foods and energy 0.2, final demand services 0.2, and final demand less foods, energy, and trade services 0.1."},{"kind":"tool","tool":"official.lookup","call":"Checked EIA gasoline data as a public energy-price cross-check for July conditions before the PPI release.","result":"EIA all-grades U.S. gasoline was 4.187 on 06/15/26, 4.048 on 06/22/26, 3.964 on 06/29/26, 3.911 on 07/06/26, 3.987 on 07/13/26, and 4.131 on 07/20/26 dollars per gallon; EIA monthly regular gasoline was 4.050 in Jun-26 after 4.479 in May-26."},{"kind":"text","text":"Reference class/base rate: using the same BLS final-demand SA monthly percent-change series from June 2025 through June 2026 gives values 0.2, 0.8, -0.2, 0.6, 0.1, 0.4, 0.4, 0.6, 0.5, 0.8, 1.1, 0.6, -0.3, a base rate mean of about 0.43 percentage point per month. The recent reference class is hot but very energy-sensitive."},{"kind":"math","text":"Prior/update/interval: persistence/reference-class prior is the Jun. 2025-Jun. 2026 BLS Table A history with mean 0.43. Adjustment components: -0.15 for June's large energy drop not fully reversing because partial July gasoline is below the June monthly average despite a late-month rise, +0.05 for still-positive services and core final-demand pressure, and +0.02 for high 5.5 percent 12-month headline PPI momentum, giving 0.43 - 0.15 + 0.05 + 0.02 = 0.35. For the 80% interval, the sample standard deviation of the 13 monthly changes is sigma = 0.40 percentage point, so half-width is roughly 1.28*sigma = 1.28*0.40 = 0.51; 0.35 +/- 0.51 gives -0.16 to 0.86."},{"kind":"text","text":"Counter-considerations: upside risk is a larger July pass-through from renewed gasoline, diesel, crude, trade-margin, or tariff-related cost pressure, which would land above the interval if headline final-demand energy and services both spike. Downside risk is a second month of falling fuels or a reversal in trade margins, which would land below the interval if final-demand goods repeat a June-like decline. An outside the interval outcome would likely require another energy shock or a broad services-margin reversal rather than ordinary monthly noise."},{"kind":"forecast","point":0.35,"ciLow":-0.16,"ciHigh":0.86}]}
