# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ons.ppi.output_manufactured_products_index
- period: 2026-07
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "uk-ppi-output-manufactured-products-index-july-2026"
- country: "UK"
- targetUnit: "index_points"
- dataPointId: "ons.ppi.output_manufactured_products_index.2026_07.first_print"
- expectedReleaseWindow: {"end": "2026-08-19", "start": "2026-08-19"}
- resolutionSourceUrl: "https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/gd6y/ppi"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ons.gov.uk"], "expectedReleaseWindow": {"end": "2026-08-19", "start": "2026-08-19"}, "field": "Value for 2026 JUL", "releasePolicy": "first_print", "sourceSeriesId": "GD6Y", "sourceUrl": "https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/gd6y/ppi", "table": "Producer price inflation time series (PPI), PPI INDEX OUTPUT TOTAL - C Manufactured products, excluding Duty 2015=100", "transform": {"factor": 1, "operation": "identity"}}
- targetRegistrationPath: "records/targets/2026-08-12-59fe84d9767a7e8726e3fd651f20fb8df77596f93a26306d99f1bb5327e40946.json"
- targetContentHash: "59fe84d9767a7e8726e3fd651f20fb8df77596f93a26306d99f1bb5327e40946"
- registrationCommit: "1063640b5acfa3c9e2e601737b5395a1431ec540"
- registeredAtUtc: "2026-08-12T16:02:57Z"
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
61a9c7ee8028104b7127163c3d95281fec3d85d4c7809fe63cb3d691ea7e8530

# Draft forecast response
{"slug":"uk-ppi-output-manufactured-products-index-july-2026","country":"UK","type":"data","title":"UK PPI Output Manufactured Products Index, July 2026","question":"What will the ONS first-print value be for GD6Y, PPI INDEX OUTPUT TOTAL - C Manufactured products, excluding Duty 2015=100, for 2026 JUL?","unit":"index_points","pointEstimate":154.0,"ciLow":152.9,"ciHigh":155.1,"confidence":0.8,"resolutionDate":"2026-08-19","resolutionSource":"Office for National Statistics Producer price inflation time series, series GD6Y","resolutionSourceUrl":"https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/gd6y/ppi","resolutionRule":"Resolve to the first ONS-published value for 2026 JUL in time series GD6Y, PPI INDEX OUTPUT TOTAL - C Manufactured products, excluding Duty 2015=100, on the 19 August 2026 Producer price inflation UK July 2026 time series release. Use the one-decimal index value exactly as first printed by ONS; ignore later revisions, superseded files, and corrections unless ONS replaces the first print before the first public release is complete on that release day.","dataPointId":"ons.ppi.output_manufactured_products_index.2026_07.first_print","historicalContext":[{"label":"2026 JUN","value":153.4},{"label":"2026 MAY","value":152.6},{"label":"2026 APR","value":152.2},{"label":"2026 MAR","value":149.5},{"label":"2025 JUL","value":144.3}],"drivers":["Recent GD6Y level momentum remained positive through June 2026","June bulletin said headline output PPI annual inflation eased to 3.5% and monthly output prices were flat","Refined petroleum output prices fell in June, limiting near-term upside from the spring spike","July seasonal changes in GD6Y since 2016 average about +0.65 index points"],"sourceContext":["https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/gd6y/ppi","https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/producerpriceindexstatisticalbulletindataset/current","https://www.ons.gov.uk/releasecalendar?highlight=true&keywords=inflation&limit=10&page=1&release-type=type-upcoming&sort=date-newest","https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/producerpriceinflation/june2026includingservicesapriltojune2026"],"runAt":"2026-08-12T16:05:27Z","reasoning":[{"kind":"heading","text":"UK GD6Y July 2026 first-print forecast"},{"kind":"text","text":"Framing and exact resolver: this forecast targets ONS series GD6Y, PPI INDEX OUTPUT TOTAL - C Manufactured products, excluding Duty 2015=100, for 2026 JUL, in index_points. The resolving variant is the ONS first-print monthly time-series value from the Producer price inflation UK July 2026 time series release; all anchors below use the same GD6Y manufactured-products excluding-duty index variant."},{"kind":"tool","tool":"official.lookup","call":"Checked the ONS release calendar for Producer price inflation, UK: July 2026 and its connected time-series release.","result":"The ONS release calendar lists Producer price inflation, UK: July 2026 time series for 19 August 2026 at 7:00am, confirmed; the same calendar page also lists Producer price inflation, UK: July 2026 for 19 August 2026 at 7:00am."},{"kind":"tool","tool":"official.lookup","call":"Fetched ONS GD6Y monthly values from the official time-series page.","result":"GD6Y values fetched from ONS: 2026 MAR 149.5, 2026 APR 152.2, 2026 MAY 152.6, 2026 JUN 153.4; 2026 Q2 is 152.7 and 2025 JUL is 144.3."},{"kind":"tool","tool":"official.lookup","call":"Fetched ONS PPI dataset page metadata for the current published vintage.","result":"The ONS Producer price inflation time series dataset current page has Release date 22 July 2026 and Next release 19 August 2026; the latest dataset file is the July 2026 vintage, and the previous version was superseded 22 July 2026 07:00."},{"kind":"tool","tool":"official.lookup","call":"Fetched the June 2026 ONS Producer price inflation bulletin for current-release context.","result":"ONS reported producer output factory gate prices rose 3.5% in the year to June 2026, down from 3.7% in May, and monthly output prices were flat in June; input prices rose 7.3% annually and fell 2.0% monthly; coke and refined petroleum output prices rose 43.0% annually but fell 5.9% monthly in June."},{"kind":"text","text":"Reference class/base rate: for this level index, I used recent month-to-month GD6Y changes as the base rate, with the last 29 monthly changes from 2024 JAN to 2026 JUN averaging +0.414 index points and a sample standard deviation of 0.823. July-only changes from 2016 through 2025 averaged about +0.650, with a sample standard deviation about 0.868."},{"kind":"math","text":"Prior/update/interval: persistence prior is June GD6Y 153.4 plus the historical July seasonal mean change of +0.65, tempered slightly because the June bulletin showed output PPI annual inflation easing and petroleum output prices falling; level component 153.4, momentum/seasonal component +0.6, one-off petroleum drag about -0.1 relative to spring momentum, policy-mechanism effect 0.0, giving point 154.0. For the interval, using recent level-series successive changes, sigma = 0.823 index points, so 1.28*sigma = 1.054; rounding to a one-decimal first print gives an 80% interval of 154.0 +/- 1.1 = [152.9, 155.1]."},{"kind":"text","text":"Counter-consideration: upside risk is a renewed July jump in refined petroleum, metals, or other manufactured-output prices after the Middle East-linked volatility noted by ONS, which would land above the interval if GD6Y rises more than 1.7 points from June. Downside risk is a sharper reversal in petroleum and imported input costs feeding into factory-gate prices, which would land outside the interval below 152.9 if GD6Y falls by more than 0.5 points from June."},{"kind":"forecast","point":154.0,"ciLow":152.9,"ciHigh":155.1}]}
