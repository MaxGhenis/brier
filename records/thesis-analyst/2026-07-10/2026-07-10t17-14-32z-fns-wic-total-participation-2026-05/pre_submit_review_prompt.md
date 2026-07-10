# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: fns.wic.total_participation
- period: 2026-05
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "wic-participation-may-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "fns.wic.total_participation.2026-05.first_print"
- resolutionDate: "2026-08-14"
- resolutionSource: "Official agency release"
- resolutionSourceUrl: "https://www.fns.usda.gov/pd/wic-program"
- resolutionRule: "Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. The expected displayed FNS monthly table value is a whole participant count, as in 6,894,610 for May 2025; convert that displayed person count to millions by dividing by 1,000,000 and round to 0.001 million for the cell. If the ledger adapter instead extracts an intermediate value expressed in thousands of participants, its listed factor 0.001 produces the same final unit of millions. Use the first posted May 2026 value only; ignore later preliminary/final revisions or annual-summary revisions."
- resolutionPolicy: "first_print"
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.fns.usda.gov"], "expectedReleaseWindow": {"end": "2026-08-15", "start": "2026-08-07"}, "field": "fns.wic.total_participation", "releasePolicy": "first_print", "sourceSeriesId": "fns.wic.total_participation", "sourceUrl": "https://www.fns.usda.gov/pd/wic-program", "table": "Official agency release", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-07-10-d9f0f26436f4322b04c9deeec1745f166dd46dbeec72d9ec676b1e2cf86ae6a9.json"
- targetContentHash: "d9f0f26436f4322b04c9deeec1745f166dd46dbeec72d9ec676b1e2cf86ae6a9"
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
4c4eb9fec241655f9e048f127ca41a35afc0cbde3c602de7cfa70b292d69ac9d

# Draft forecast response
{"slug":"wic-participation-may-2026","country":"US","type":"data","title":"US WIC participation, May 2026","question":"What will USDA FNS first report as national WIC Total Participants for May 2026?","unit":"millions","pointEstimate":6.86,"ciLow":6.76,"ciHigh":6.94,"confidence":0.8,"resolutionDate":"2026-08-14","resolutionSource":"Official agency release","resolutionSourceUrl":"https://www.fns.usda.gov/pd/wic-program","resolutionRule":"Resolve to the national WIC Total Participants value for May 2026 in the first official USDA FNS WIC monthly program-data posting or latest-month table that first includes May 2026. Convert the displayed whole-person count to millions by dividing by 1,000,000 and round to 0.001 million. Use only the first posted value; ignore later preliminary, final, or annual-summary revisions.","dataPointId":"fns.wic.total_participation.2026-05.first_print","historicalContext":[{"label":"May 2024 official monthly table","value":6.76371},{"label":"May 2025 first print","value":6.89461},{"label":"October 2025 preliminary","value":6.90905},{"label":"November 2025 initial","value":6.752138}],"drivers":["Recent participation level near 6.8–6.9 million","Positive May-over-May momentum through 2025","Late-2025 participation weakness","Normal monthly reporting volatility","FY 2026 benefit levels broadly supportive"],"sourceContext":["https://www.fns.usda.gov/pd/wic-program","https://www.fns.usda.gov/sites/default/files/data-files/Keydata-May-2025.pdf","https://www.fns.usda.gov/sites/default/files/resource-files/27wilatest-2.pdf","https://www.fns.usda.gov/pd/overview"],"runAt":"2026-07-10T17:15:21Z","thresholdLadder":{"thresholds":[6.7,6.73,6.76,6.79,6.82,6.84,6.86,6.88,6.9,6.92,6.94,6.97,7],"cumulativeProbabilities":[0.03,0.06,0.1,0.16,0.25,0.38,0.5,0.62,0.73,0.82,0.9,0.96,0.98]},"reasoning":[{"kind":"heading","text":"May 2026 national WIC participation first print"},{"kind":"text","text":"The target is USDA FNS Table 21 national WIC Total Participation for May 2026, measured as people issued benefits during the calendar month. This forecast uses the first posted monthly value, converted from people to millions; subsequent revisions are excluded."},{"kind":"tool","tool":"official.lookup","call":"Fetch USDA FNS May 2025 Keydata Table 21 national WIC participation history.","result":"The official table reported 6,763,710 participants in May 2024, 6,876,342 in April 2025, and 6,889,500 in the later May 2025 table vintage; the target's documented May 2025 first print was 6,894,610."},{"kind":"tool","tool":"official.lookup","call":"Fetch the USDA FNS latest-month WIC participation table for late-2025 momentum.","result":"The latest-month table showed 6,909,050 participants for October 2025 preliminary and 6,752,138 for November 2025 initial, a one-month decline of 156,912."},{"kind":"tool","tool":"official.lookup","call":"Verify the release date against the official FNS program-data release schedule and inspect the WIC series page.","result":"The FNS schedule identifies 2026-08-14 for the May 2026 program-data release; the WIC page identifies Table 21 monthly national participation and displayed 2022–2025 monthly data as of its 2026 update."},{"kind":"text","text":"The outside-view reference class is successive monthly changes in the official Table 21 national total from October 2023 through May 2025. Its base rate is small month-to-month movement around a slowly changing level, with May 2025 about 0.131 million above May 2024 but November 2025 initial about 0.142 million below October preliminary."},{"kind":"text","text":"Level and momentum are separated as follows: the level anchor is roughly 6.85 million; the earlier year-over-year rise contributes a modest positive adjustment, while late-2025 weakness contributes a negative adjustment. No discrete May 2026 eligibility or benefit-policy shock is evident; FY 2026 cash-value benefit adjustments are treated as broadly supportive rather than a large caseload mechanism."},{"kind":"math","text":"Prior/update/interval: A persistence/local-level prior centered near 6.85 million uses the 19 successive changes from the fetched October 2023–May 2025 Table 21 history. Their realized standard deviation is approximately sigma = 0.047 million, so a normal 80% half-width is 1.28*sigma = 1.28*0.047 = 0.060 million. The update combines +0.025 million for the earlier year-over-year rise, -0.015 million for late-2025 weakness, and no large policy shock, giving a central value near 6.86 million. The ladder implies bounds of 6.760–6.940, a 0.090-million average half-width, 1.50 times the sigma half-width; this widening reflects first-print state-reporting noise and uncertainty about whether the November weakness persists."},{"kind":"math","text":"Ladder: P(X <= 6.700) = 0.03; P(X <= 6.730) = 0.06; P(X <= 6.760) = 0.10; P(X <= 6.790) = 0.16; P(X <= 6.820) = 0.25; P(X <= 6.840) = 0.38; P(X <= 6.860) = 0.50; P(X <= 6.880) = 0.62; P(X <= 6.900) = 0.73; P(X <= 6.920) = 0.82; P(X <= 6.940) = 0.90; P(X <= 6.970) = 0.96; P(X <= 7.000) = 0.98. Linear interpolation gives the median 6.860, 10th percentile 6.760, and 90th percentile 6.940 million."},{"kind":"text","text":"Upside risk comes from renewed outreach, retention, or normalization after the weak November initial print and could put participation above 6.940 million. Downside risk comes from continued caseload attrition or incomplete first-print state reporting and could put it below 6.760 million. A major reporting disruption or abrupt eligibility-policy effect would land outside the interval."},{"kind":"forecast","point":6.86,"ciLow":6.76,"ciHigh":6.94}]}
