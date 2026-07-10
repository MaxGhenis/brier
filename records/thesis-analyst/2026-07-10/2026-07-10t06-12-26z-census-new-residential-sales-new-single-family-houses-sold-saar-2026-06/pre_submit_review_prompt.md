# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: census.new_residential_sales.new_single_family_houses_sold_saar
- period: 2026-06
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "us-new-home-sales-saar-june-2026"
- country: "US"
- targetUnit: "thousands"
- dataPointId: "census.new_residential_sales.new_single_family_houses_sold_saar.2026_06.first_print"
- resolutionSourceUrl: "https://www.census.gov/construction/nrs/current/index.html"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.census.gov"], "expectedReleaseWindow": {"end": "2026-07-24", "start": "2026-07-24"}, "field": "Sales of new single-family houses, United States, seasonally-adjusted annual rate", "releasePolicy": "first_print", "sourceSeriesId": "RESSALES.SOLD.TOTAL.US.SAAR", "sourceUrl": "https://www.census.gov/construction/nrs/current/index.html", "table": "Monthly New Residential Sales, Table 1: New Houses Sold and For Sale", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-07-10-ac8614c86d2fa983f323f64f18c92df648f3ed58f35faa09e85b571954df9ae8.json"
- targetContentHash: "ac8614c86d2fa983f323f64f18c92df648f3ed58f35faa09e85b571954df9ae8"
- registeredAtUtc: "2026-07-10T05:58:27Z"
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
0612b7cb0b6849c1ae4020b025024f22de441e456b2d129141f501bf763f381a

# Draft forecast response
{"slug":"us-new-home-sales-saar-june-2026","country":"US","type":"data","title":"US New Home Sales SAAR, June 2026","question":"What will the U.S. Census Bureau and HUD first report for sales of new single-family houses in the United States in June 2026, seasonally adjusted annual rate, in thousands?","unit":"thousands","pointEstimate":590,"ciLow":525,"ciHigh":655,"confidence":0.8,"resolutionDate":"2026-07-24","resolutionSource":"U.S. Census Bureau and U.S. Department of Housing and Urban Development Monthly New Residential Sales release","resolutionSourceUrl":"https://www.census.gov/construction/nrs/current/index.html","resolutionRule":"Resolve to the first-print value in Monthly New Residential Sales, Table 1, New Houses Sold and For Sale, for Sold during period, United States, seasonally adjusted annual rate, June 2026. Record the published value in thousands of houses at an annual rate; do not apply later revisions or same-day corrections unless the Census first-print release itself republishes the table before the initial public value is captured.","dataPointId":"census.new_residential_sales.new_single_family_houses_sold_saar.2026_06.first_print","historicalContext":[{"label":"May 2026 HSN1F SAAR","value":580},{"label":"Apr 2026 HSN1F SAAR","value":626},{"label":"Mar 2026 HSN1F SAAR","value":664},{"label":"Feb 2026 HSN1F SAAR","value":630},{"label":"Jan 2026 HSN1F SAAR","value":576}],"drivers":["May first-print sales fell to 580 thousand SAAR from revised April 626 thousand","Recent Jan-May values show large month-to-month noise around a roughly 600 thousand level","May new-home inventory was high at 496 thousand and 10.3 months of supply","Single-family starts and permits were soft but not collapsing","Mortgage rates around late June and early July remained near 6.5 percent"],"sourceContext":["https://www.census.gov/construction/nrs/current/index.html","https://www.census.gov/construction/soc/schedule.html","https://fred.stlouisfed.org/series/HSN1F","https://www.census.gov/construction/nrc/current/index.html","https://fred.stlouisfed.org/series/MORTGAGE30US"],"runAt":"2026-07-10T06:12:44Z","reasoning":[{"kind":"heading","text":"US June 2026 new single-family houses sold SAAR first print"},{"kind":"text","text":"Framing and exact resolver: this forecast targets Census/HUD Monthly New Residential Sales, Table 1, Sold during period, United States, seasonally adjusted annual rate, source series HSN1F / RESSALES.SOLD.TOTAL.US.SAAR, for June 2026. The variant is SAAR, not NSA, and the resolution rule is strict first print."},{"kind":"tool","tool":"official.lookup","call":"Opened Census Survey of Construction release schedule for the New Residential Sales release date.","result":"The official schedule lists the June 2026 survey month New Residential Sales release on July 24, 2026 at 10:00 a.m.; it also lists May 2026 New Residential Sales on June 24, 2026."},{"kind":"tool","tool":"official.lookup","call":"Opened Census current Monthly New Residential Sales press release for the latest official first-print facts.","result":"The May 2026 release reported sales of new single-family houses at 580,000 SAAR, 7.3 percent below the April 2026 rate of 626,000 and 6.8 percent below the May 2025 rate of 622,000; for-sale inventory was 496,000 and months' supply was 10.3."},{"kind":"tool","tool":"public.history_mirror","call":"Opened FRED HSN1F, which cites Census/HUD as source, to read recent monthly history for the same SAAR United States series.","result":"Recent HSN1F observations were May 2026 580, Apr 2026 626, Mar 2026 664, Feb 2026 630, and Jan 2026 576, all in thousands at a seasonally adjusted annual rate."},{"kind":"tool","tool":"official.lookup","call":"Opened Census New Residential Construction May 2026 release for supply-side housing indicators.","result":"May 2026 privately owned housing starts were 1,177,000 SAAR, down 15.4 percent from April; single-family starts were 882,000, down 1.9 percent from April; single-family authorizations were 886,000, up 0.6 percent from April."},{"kind":"tool","tool":"public.lookup","call":"Opened FRED MORTGAGE30US, sourced to Freddie Mac PMMS, for current mortgage-rate context.","result":"The 30-year fixed mortgage rate was 6.49 percent on 2026-07-09, 6.43 percent on 2026-07-02, 6.49 percent on 2026-06-25, 6.47 percent on 2026-06-18, and 6.52 percent on 2026-06-11."},{"kind":"text","text":"Base rate / reference class: for a one-month-ahead forecast of a volatile level series, persistence from the latest same-variant official print is the base rate. The latest observed level is 580 thousand, while the Jan-May 2026 run is 576, 630, 664, 626, 580, so a central June value near the high-500s to low-600s is the outside-view anchor."},{"kind":"text","text":"Adjustment components: level starts from May's 580; momentum gets a small positive offset because a 46 thousand May drop followed a 38 thousand April drop and some mean reversion is common; high inventory of 496 thousand and 10.3 months' supply offsets that rebound; mortgage rates near 6.5 percent and soft single-family starts argue against a sharp upside breakout."},{"kind":"math","text":"Prior/update/interval: persistence prior = May 2026 HSN1F 580. Historical sample = fetched Jan-May 2026 HSN1F values 576, 630, 664, 626, 580. Successive changes are +54, +34, -38, -46; their sample mean is +1 and sigma = 50.4 thousand. Adjustment components are +15 thousand mean reversion after the May drop, -5 thousand for high months' supply and affordability, and 0 thousand for starts/rate context, giving point = 580 + 10 = 590. The 80% half-width is roughly 1.28*sigma = 1.28*50.4 = 64.5, rounded to 65, so bounds are 590 - 65 = 525 and 590 + 65 = 655."},{"kind":"text","text":"Counter-considerations: upside risk is a builder-incentive or rate-relief rebound that would land above the interval if June first-print sales exceed about 655 thousand; downside risk is another demand freeze or regional pullback that would land below the interval if the first print is under about 525 thousand. A value outside the interval would most likely reflect a large regional swing, especially in the South or West, rather than normal national noise."},{"kind":"forecast","point":590,"ciLow":525,"ciHigh":655}]}
