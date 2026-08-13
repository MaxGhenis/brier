# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: nbb.consumer_confidence.indicator
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "belgium-consumer-confidence-august-2026"
- country: "BE"
- targetUnit: "index_points"
- dataPointId: "nbb.consumer_confidence.indicator.2026-08.first_print"
- expectedReleaseWindow: {"end": "2026-08-24", "start": "2026-08-16"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.nbb.be"], "expectedReleaseWindow": {"end": "2026-08-24", "start": "2026-08-16"}, "field": "nbb.consumer_confidence.indicator", "releasePolicy": "first_print", "sourceSeriesId": "nbb.consumer_confidence.indicator", "sourceUrl": "https://www.nbb.be/en/statistics/business-surveys/consumer-survey", "table": "National Bank of Belgium consumer survey release", "transform": {"factor": 1, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-13-85f1c5d5aba56fd5c8b4cc2845d2513bbcb103b6accdac664944e1d803362c46.json"
- targetContentHash: "85f1c5d5aba56fd5c8b4cc2845d2513bbcb103b6accdac664944e1d803362c46"
- registrationCommit: "448b17e91d8ee0fa53f512a75460719c172b1358"
- registeredAtUtc: "2026-08-13T06:52:40Z"
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
63e6741fc4c2a445211a420e1398c03a4ba049137398c2100ca75d4ca6606167

# Draft forecast response
{
  "slug": "belgium-consumer-confidence-august-2026",
  "country": "BE",
  "type": "data",
  "title": "Belgium consumer confidence, August 2026",
  "question": "National Bank of Belgium consumer confidence indicator for August 2026, seasonally adjusted, first official print",
  "unit": "index_points",
  "pointEstimate": -5.0,
  "ciLow": -11.0,
  "ciHigh": 1.0,
  "confidence": 0.8,
  "resolutionDate": "2026-08-21",
  "resolutionSource": "National Bank of Belgium consumer survey release",
  "resolutionSourceUrl": "https://www.nbb.be/en/statistics/business-surveys/consumer-survey",
  "resolutionRule": "Resolve to the first National Bank of Belgium published consumer confidence indicator for 2026-08, seasonally adjusted, reported in signed index points and rounded to the agency's published precision. Use the first official NBB print only; ignore later NBB.Stat revisions, corrections after the first release, FRED, and third-party mirrors. The registered source URL is https://www.nbb.be/en/statistics/business-surveys/consumer-survey; during this run that URL returned an NBB 404 shell, while current official NBB latest-figures pages provided the calendar and history, so keep the forecast tied to the same registered target and source binding.",
  "dataPointId": "nbb.consumer_confidence.indicator.2026-08.first_print",
  "historicalContext": [
    {"label": "2026-07 consumer confidence indicator", "value": -5.0},
    {"label": "2026-06 consumer confidence indicator", "value": -7.0},
    {"label": "2026-05 consumer confidence indicator", "value": -10.0},
    {"label": "2026-04 consumer confidence indicator", "value": -9.0},
    {"label": "2026-03 consumer confidence indicator", "value": -6.0},
    {"label": "2026-02 consumer confidence indicator", "value": 1.0}
  ],
  "drivers": [
    "July first print improved to -5 but remained negative",
    "persistence is the strongest simple benchmark",
    "July savings and economic-expectation balances improved",
    "July unemployment expectations worsened slightly",
    "recent monthly change sigma is 3.37 index points"
  ],
  "sourceContext": [
    "https://www.nbb.be/en/statistics/latest-figures/consumer-confidence-indicator-2026m7",
    "https://www.nbb.be/en/statistics/latest-figures?search=consumer%20confidence&scope=2",
    "https://www.nbb.be/en/statistics/methodology/topics/firms-and-short-term-business-statistics/consumer-confidence",
    "https://www.nbb.be/en/statistics/business-surveys/consumer-survey",
    "https://app.thesisinstitute.org/specs.json"
  ],
  "runAt": "2026-08-13T17:38:43Z",
  "reasoning": [
    {"kind": "heading", "text": "Belgium August 2026 NBB Consumer Confidence Forecast"},
    {"kind": "text", "text": "Framing and exact resolver: the target is the National Bank of Belgium's first published August 2026 consumer confidence indicator, seasonally adjusted, in signed index points. The canonical ledger target uses country BE, unit index_points, dataPointId nbb.consumer_confidence.indicator.2026-08.first_print, and an expected release window from 2026-08-16 through 2026-08-24."},
    {"kind": "tool", "tool": "official.lookup", "call": "Fetched the NBB upcoming latest-figures view for consumer confidence releases.", "result": "Fetched official schedule numbers: Firms and short-term business statistics, period 2026M8, Consumer confidence indicator, Publication, release date 21 Aug 2026; the same page's August calendar grid shows 2 results for 2026-08-21."},
    {"kind": "tool", "tool": "official.lookup", "call": "Fetched the official NBB July 2026 consumer confidence indicator release page and extracted the headline table.", "result": "Fetched NBB release numbers: release date 22 Jul 2026 11:00, period 2026M7; consumer confidence indicator values were 2025 Jul -4, Aug -2, Sep -1, Oct 0, Nov 2, Dec -1, 2026 Jan 4, Feb 1, Mar -6, Apr -9, May -10, Jun -7, Jul -5."},
    {"kind": "tool", "tool": "official.lookup", "call": "Fetched the NBB consumer-confidence methodology page for target identity and construction.", "result": "Fetched methodology numbers: the survey covers approximately 1850 households, interviews run between the 1st and 15th days of each month, the indicator is the arithmetic mean of 4 seasonally adjusted key question balances, and balances are bounded from -100 to +100."},
    {"kind": "tool", "tool": "local.model", "call": "Computed thesis_model_candidate_v1-style one-step benchmarks from the fetched NBB history.", "result": "Model candidate numbers from fetched history: persistence point -5.0, p10 -9.3, p50 -5.0, p90 -0.7, 80% interval [-9.3, -0.7], 90% interval [-10.5, 0.5], train cutoff 2026-07, calibration_n 12, walk-forward MAE 2.75; recent monthly changes were 2, 1, 1, 2, -3, 5, -3, -7, -3, -1, 3, 2."},
    {"kind": "tool", "tool": "network.check", "call": "Checked the requested public specs slug endpoint before finalizing.", "result": "Fetched https://app.thesisinstitute.org/specs.json and received HTTP 404 with an HTML body of 11289 bytes rather than a specs JSON document; the registered slug belgium-consumer-confidence-august-2026 was kept."},
    {"kind": "text", "text": "Base rate/reference class: using the 13 official NBB monthly first prints from 2025-07 through 2026-07, the latest print is -5.0, the 13-print mean is -2.9, the last-six mean is -6.0, the last-three mean is -7.3, and the range is -10.0 to 4.0. Persistence is the base rate because it has the lowest walk-forward MAE among the simple candidates."},
    {"kind": "text", "text": "Level, momentum, one-off, and policy mechanisms: the level remains negative but has improved from May -10 and June -7 to July -5; momentum is upward, but the July table also shows unemployment expectations at 14, worse than June 13, while savings improved from 19 to 23. I have no direct public August survey signal before the first print, so I do not move materially away from the persistence benchmark."},
    {"kind": "math", "text": "Prior/update/interval: persistence prior = -5.0 from the July 2026 first print; historical sample = NBB 2025-07 through 2026-07 first-print table; adjustment components = +0.0 for August because July's improvement and unemployment deterioration are already in the latest print and no direct August signal is fetched. For this level survey-balance series, use successive monthly changes: sigma = 3.37 from changes [2, 1, 1, 2, -3, 5, -3, -7, -3, -1, 3, 2]. The raw 80% half-width is 1.28*sigma = 4.31; widen by about 1.39x to 6.0 for survey volatility and source-binding/calendar uncertainty, giving -5.0 - 6.0 = -11.0 and -5.0 + 6.0 = 1.0."},
    {"kind": "text", "text": "Counter-consideration and falsification: upside risk is a stronger August improvement in household saving and macro expectations, which would land above the interval if the first print is 1.1 or higher. Downside risk is a renewed deterioration in unemployment or financial-situation expectations, which would land below the interval if the first print is -11.1 or lower. Outside the interval would require a larger one-month move than most recent NBB changes."},
    {"kind": "forecast", "point": -5.0, "ciLow": -11.0, "ciHigh": 1.0}
  ]
}
