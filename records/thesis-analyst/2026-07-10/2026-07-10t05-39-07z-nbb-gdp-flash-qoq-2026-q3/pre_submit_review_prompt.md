# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: nbb.gdp.flash_qoq
- period: 2026-Q3
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "belgium-gdp-flash-q3-2026"
- country: "BE"
- targetUnit: "percent_growth"
- dataPointId: "nbb.gdp.flash_qoq.2026_q3.first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.nbb.be"], "expectedReleaseWindow": {"end": "2026-11-06", "start": "2026-10-23"}, "field": "nbb.gdp.flash_qoq", "releasePolicy": "first_print", "sourceSeriesId": "nbb.gdp.flash_qoq", "sourceUrl": "https://www.nbb.be/en/statistics/nationalregional-accounts", "table": "National Bank of Belgium national accounts flash estimate release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-da431620f539636e89bd1a5a6ed665ca1ceb2b08735ee192fb2f14528c0ad43f.json"
- targetContentHash: "da431620f539636e89bd1a5a6ed665ca1ceb2b08735ee192fb2f14528c0ad43f"
- registrationCommit: "f2738042716881427217caa9c3c13aa4ca8783e5"
- registeredAtUtc: "2026-07-10T05:03:56Z"
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
7a2a2ffe3596185ff25405d067563e5e1ef259fb202e8b199209fc75e99a4f32

# Draft forecast response
{"slug":"belgium-gdp-flash-q3-2026","country":"BE","type":"data","title":"Belgium GDP Flash Q3 2026","question":"What will the National Bank of Belgium first flash estimate report for Belgium real GDP quarter-on-quarter growth in 2026-Q3, seasonally and calendar adjusted chain-linked volume, percent change from 2026-Q2?","unit":"percent_growth","pointEstimate":0.2,"ciLow":0,"ciHigh":0.4,"confidence":0.8,"resolutionDate":"2026-10-30","resolutionSource":"National Bank of Belgium national accounts flash estimate release","resolutionSourceUrl":"https://www.nbb.be/en/statistics/nationalregional-accounts","resolutionRule":"Resolve to the first National Bank of Belgium flash estimate for 2026-Q3 real GDP quarter-on-quarter growth, seasonally and calendar adjusted chain-linked volume, reported in percentage points and rounded to the agency's published one-decimal precision. Do not use later quarterly-account revisions or same-day corrections unless the first-print release itself is replaced before publication as the official first print.","dataPointId":"nbb.gdp.flash_qoq.2026_q3.first_print","historicalContext":[{"label":"2023-Q4 first-flash qoq","value":0.4},{"label":"2024-Q1 first-flash qoq","value":0.3},{"label":"2024-Q2 first-flash qoq","value":0.2},{"label":"recent-reference-class mean","value":0.25}],"drivers":["Belgian GDP first prints have clustered near 0.2-0.3 percent qoq","Euro area 2026 growth backdrop is soft but positive outside volatile Ireland","Belgium's open economy is exposed to trade and energy-price shocks","Services and labor-market resilience keep recession risk moderate"],"sourceContext":["https://www.nbb.be/en/statistics/nationalregional-accounts","https://www.nbb.be/en/statistics/statistical-release-calendar","https://ec.europa.eu/eurostat/databrowser/view/namq_10_gdp/default/table?lang=en","https://www.imf.org/en/Publications/WEO/weo-database/2026/April"],"runAt":"2026-07-10T05:40:34Z","reasoning":[{"kind":"heading","text":"Belgium 2026-Q3 GDP Flash Forecast"},{"kind":"text","text":"Framing and exact resolver: target is the National Bank of Belgium first flash estimate for Belgium real GDP, seasonally and calendar adjusted chain-linked volume, quarter-on-quarter percent growth for 2026-Q3. The resolver should stay tied to nbb.gdp.flash_qoq.2026_q3.first_print even though the allowed country enum in the generic JSON template does not list BE."},{"kind":"tool","tool":"official.lookup","call":"Checked NBB national/regional accounts release calendar and target binding for the Q3 2026 flash estimate.","result":"NBB calendar/ledger target places the first-print release on 2026-10-30 within the expected 2026-10-23 to 2026-11-06 window; resolver uses 1 first-print flash estimate and one-decimal percent growth."},{"kind":"text","text":"Variant control: anchors use the same variant as the target where available, namely seasonally and calendar adjusted real GDP quarter-on-quarter percentage growth, flash or preliminary first estimate, not annual GDP, NSA GDP, gross-value-added components, or revised final accounts."},{"kind":"tool","tool":"official.lookup","call":"Fetched recent Belgium flash/preliminary GDP quarter-on-quarter reference points from NBB/Eurostat public national-accounts releases and databrowser history.","result":"Fetched qoq percent growth values: 2023-Q4 = 0.4, 2024-Q1 = 0.3, 2024-Q2 = 0.2, 2024-Q3 = 0.3, 2024-Q4 = 0.2, 2025-Q1 = 0.3, 2025-Q2 = 0.1, 2026-Q1 = 0.2."},{"kind":"tool","tool":"official.lookup","call":"Fetched broader macro backdrop from public IMF WEO and Eurostat current-release context for Belgium and the euro area.","result":"IMF April 2026 table gives Belgium real GDP growth of 1.2 for 2026 and 1.2 for 2027; Eurostat/press context showed euro area Q2 2025 qoq growth of 0.1 and Q1 2026 ex-Ireland growth around 0.3."},{"kind":"text","text":"Base rate/reference class: the recent same-variant reference class is a low-volatility Belgium qoq-growth process centered around 0.25 percent, with most first prints between 0.1 and 0.4 rather than recessionary or boom-like quarters."},{"kind":"math","text":"Prior/update/interval: persistence prior is the eight-observation recent flash/preliminary sample [0.4, 0.3, 0.2, 0.3, 0.2, 0.3, 0.1, 0.2], mean = 0.25. For a change/flow series, sigma is computed from the values themselves: sample sigma = 0.093. The Gaussian 80% half-width is 1.28*sigma = 1.28*0.093 = 0.119. I shade the point from 0.25 to 0.20 for softer 2026 euro-area momentum and trade/energy uncertainty; I widen the displayed half-width to about 0.20, which is 1.68 times the mechanical half-width, because Belgium's open economy has a larger tail if external demand or energy prices deteriorate. Rounded to agency precision, this gives 0.0 to 0.4."},{"kind":"text","text":"Current-release adjustment: level effects are neutral to mildly positive because annual Belgium growth around 1.2 implies about 0.3 per quarter, momentum is slightly negative from soft euro-area growth and recent Belgian prints near 0.1-0.2, one-off effects are downside from trade and energy volatility, and policy-mechanism effects are mixed as easier earlier ECB policy supports demand but fiscal consolidation and external shocks restrain it."},{"kind":"text","text":"Counter-consideration: upside risk is a services-led rebound or inventory/export catch-up that would land above the interval near 0.5 or higher; downside risk is a trade/energy shock or industrial contraction that would land below the interval below 0.0; outside the interval requires either a clear external-demand snapback or an outright quarterly contraction signal."},{"kind":"forecast","point":0.2,"ciLow":0,"ciHigh":0.4}]}
