# Thesis pre-submit forecast review

You are a reviewer for a forecast before publication. Review the draft forecast, the target spec, cited public evidence, and any relevant local repo context or prior traces if useful. This extra context is optional; do not require it when the draft is already clear. Do not use future outcomes, private knowledge, or hidden chain-of-thought. Do not produce a replacement forecast.

# Target
- series: ssa.ssi.total_recipients
- period: 2026-08
- conditional: null


# Canonical ledger target context
Use these ledger fields as the target contract for slug, unit, dataPointId, resolutionDate, and resolver text. The cell's unit must equal targetUnit below byte-for-byte, even when it is not a member of the contract's exploratory unit menu. If you find a concrete ledger error, keep the forecast tied to the same target and state the discrepancy in reasoning rather than silently changing the target.
- catalogSlug: "ssi-recipients-august-2026"
- country: "US"
- targetUnit: "millions"
- dataPointId: "ssa.ssi.total_recipients.2026-08.first_print"
- expectedReleaseWindow: {"end": "2026-10-04", "start": "2026-09-26"}
- sourceBinding: {"adapter": "generic-url", "allowedHosts": ["www.ssa.gov"], "expectedReleaseWindow": {"end": "2026-10-04", "start": "2026-09-26"}, "field": "ssa.ssi.total_recipients", "releasePolicy": "first_print", "sourceSeriesId": "ssa.ssi.total_recipients", "sourceUrl": "https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-07/table02.html", "table": "Social Security Administration SSI Monthly Statistics", "transform": {"factor": 0.001, "operation": "multiply"}}
- targetRegistrationPath: "records/targets/2026-08-12-9e48da0da68cd2dfb368416d94e9714b1c294f8fcbee6ed27a1720e493ef0300.json"
- targetContentHash: "9e48da0da68cd2dfb368416d94e9714b1c294f8fcbee6ed27a1720e493ef0300"
- registrationCommit: "d50ffb7c957ea27fad25c6e0c6fee0aa2471bc84"
- registeredAtUtc: "2026-08-12T21:16:44Z"
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
bca8dd494c0788dee5cd54a293fc20d609151a732560f61052b927da921f51bf

# Draft forecast response
{
  "slug": "ssi-recipients-august-2026",
  "country": "US",
  "type": "data",
  "title": "SSI total recipients, Aug. 2026",
  "question": "Social Security Administration SSI Monthly Statistics Table 2 total number of recipients for August 2026, all federally administered payments, end-of-month not seasonally adjusted administrative count, first print.",
  "unit": "millions",
  "pointEstimate": 7.3,
  "ciLow": 7.276,
  "ciHigh": 7.324,
  "confidence": 0.8,
  "resolutionDate": "2026-10-04",
  "resolutionSource": "Social Security Administration SSI Monthly Statistics",
  "resolutionSourceUrl": "https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-07/table02.html",
  "resolutionRule": "Resolve to the first published August 2026 value in SSA SSI Monthly Statistics Table 2, row August 2026, column Total number of recipients for all federally administered payments. The resolving observation is the first August 2026 Table 2 print whenever SSA posts it; 2026-10-04 is the registered latest expected by-date from the Thesis target expectedReleaseWindow, not a claimed exact release day. The registered bound source URL is the July 2026 Table 2 page that authenticates the table structure; use the analogous first-posted August 2026 Table 2 row when SSA publishes it. SSA publishes counts as whole recipients; convert to millions by dividing by 1,000,000 and round forecast display values to three decimals. Use the first official print only and ignore later revisions or adjusted checks after the first August 2026 table is posted.",
  "dataPointId": "ssa.ssi.total_recipients.2026-08.first_print",
  "historicalContext": [
    {"label": "2026-07 total SSI recipients, millions", "value": 7.300297},
    {"label": "2026-06 total SSI recipients, millions", "value": 7.323731},
    {"label": "2026-05 total SSI recipients, millions", "value": 7.322937},
    {"label": "2026-04 total SSI recipients, millions", "value": 7.338132},
    {"label": "2026-03 total SSI recipients, millions", "value": 7.351825},
    {"label": "2026-02 total SSI recipients, millions", "value": 7.358913},
    {"label": "2026-01 total SSI recipients, millions", "value": 7.36951},
    {"label": "2025-12 total SSI recipients, millions", "value": 7.392201},
    {"label": "2025-11 total SSI recipients, millions", "value": 7.391176},
    {"label": "2025-10 total SSI recipients, millions", "value": 7.393406},
    {"label": "2025-09 total SSI recipients, millions", "value": 7.436689},
    {"label": "2025-08 total SSI recipients, millions", "value": 7.405735},
    {"label": "2025-07 total SSI recipients, millions", "value": 7.394877}
  ],
  "drivers": [
    "latest official July 2026 total is 7.300 million recipients",
    "January-July 2026 sequence declined by about 0.069 million recipients",
    "one-step walk-forward error is marginally lower for persistence than expanding drift",
    "July-August 2025 seasonal move was positive, partly offsetting recent downward momentum",
    "monthly administrative churn dominates short-horizon uncertainty"
  ],
  "sourceContext": [
    "https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-07/table02.html",
    "https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/index.html",
    "https://www.ssa.gov/policy/pub_schedule.html"
  ],
  "runAt": "2026-08-12T21:28:32Z",
  "reasoning": [
    {"kind": "heading", "text": "Forecast for SSA SSI total recipients, August 2026"},
    {"kind": "text", "text": "Framing and exact resolver: this targets SSA SSI Monthly Statistics Table 2, All Federally Administered Payments, the August 2026 row and Total number of recipients column, reported as an end-of-month administrative count and resolved on the first print. The target registry binds resolutionDate 2026-10-04 and resolutionSourceUrl to the July 2026 Table 2 URL; I preserve that bound URL while forecasting the registered August 2026 dataPointId."},
    {"kind": "tool", "tool": "local.registry", "call": "Inspected records/targets/2026-08-12-9e48da0da68cd2dfb368416d94e9714b1c294f8fcbee6ed27a1720e493ef0300.json and site/src/data/ledger-targets.generated.ts; attempted https://app.thesisinstitute.org/specs.json.", "result": "Fetched local public target fields: slug ssi-recipients-august-2026, unit millions, dataPointId ssa.ssi.total_recipients.2026-08.first_print, registered resolutionDate 2026-10-04, expectedReleaseWindow 2026-09-26 to 2026-10-04, and sourceBinding URL https://www.ssa.gov/policy/docs/statcomps/ssi_monthly/2026-07/table02.html; app specs fetch returned HTTP 404 during this run."},
    {"kind": "tool", "tool": "ssa.page", "call": "Opened SSA SSI Monthly Statistics index and publishing schedule pages.", "result": "Fetched official timing evidence: the current SSA SSI Monthly Statistics index is July 2026 and says released August 2026; it lists Table 2 as Number of recipients by type of payment, total payments, and average monthly payment; SSA Publishing Schedule lists SSI Monthly Statistics with frequency Monthly; the target bound remains 2026-10-04 because the registry provides a latest expected by-date rather than an exact official day."},
    {"kind": "tool", "tool": "ssa.table02", "call": "Opened SSA SSI Monthly Statistics July 2026 Table 2 and read the Total number of recipients values.", "result": "Fetched Table 2 total recipients: 2025-07 7,394,877; 2025-08 7,405,735; 2025-09 7,436,689; 2025-10 7,393,406; 2025-11 7,391,176; 2025-12 7,392,201; 2026-01 7,369,510; 2026-02 7,358,913; 2026-03 7,351,825; 2026-04 7,338,132; 2026-05 7,322,937; 2026-06 7,323,731; 2026-07 7,300,297."},
    {"kind": "tool", "tool": "model.candidates", "call": "Computed thesis_model_candidate_v1 candidates from the fetched July 2025-July 2026 SSA Table 2 levels in millions.", "result": "thesis_model_candidate_v1 persistence: point 7.300297, p10 7.276333, p50 7.300297, p90 7.324261, 80% interval 7.276333-7.324261, 90% interval 7.269505-7.331089, interval_method residual_changes_sigma, calibration_n 12, train_cutoff 2026-07, walk_forward_mae 0.014003, walk_forward_rmse 0.018775. Expanding-drift candidate: point 7.292415, p10 7.268451, p50 7.292415, p90 7.316379, 80% interval 7.268451-7.316379, 90% interval 7.261622-7.323208, interval_method residual_changes_sigma, calibration_n 12, train_cutoff 2026-07, walk_forward_mae 0.014051, walk_forward_rmse 0.022720."},
    {"kind": "text", "text": "Base rate/reference class: the trailing 13 same-table first-print levels from July 2025 through July 2026 range from 7.300297 million to 7.436689 million, with mean level 7.367648 million. The latest-value persistence prior is 7.300297 million; recent successive changes have mean -0.007882 million, median -0.008843 million, and the 2026 sequence has fallen from 7.369510 million in January to 7.300297 million in July."},
    {"kind": "text", "text": "Benchmark and update: persistence slightly beats the expanding-drift rule in this short walk-forward window, so it is the selected candidate. Current evidence pulls mildly downward because the January-July 2026 same-source decline is 0.069213 million, while the only directly fetched July-to-August seasonal comparison, 2025-07 to 2025-08, was +0.010858 million; those offset enough that the rounded August forecast stays at 7.300 million."},
    {"kind": "math", "text": "Prior/update/interval: prior is selected latest-value persistence at 7.300297 million using the fetched July 2025-July 2026 Table 2 sample. Adjustment components are -0.007882 million from the trailing mean monthly change, plus +0.010858 million from the fetched 2025 July-to-August same-month seasonal move, damped 25% because persistence won walk-forward MAE, giving an unrounded point close to 7.300 million after display rounding. Interval method is residual_changes_sigma on the 12 fetched successive monthly changes: sigma = 0.018722 million, so 80% half-width is 1.28*sigma = 1.28*0.018722 = 0.023964 million; 7.300297 - 0.023964 = 7.276333 and 7.300297 + 0.023964 = 7.324261, rounded to 7.276 to 7.324."},
    {"kind": "text", "text": "Counter-consideration: upside risk outside the interval would require a rebound above 7.324 million, such as a July drop that fully reverses plus another positive August seasonal intake month like 2025. Downside risk outside the interval would require August to continue the January-July downtrend at more than about two recent-sigma monthly moves, landing below 7.276 million."},
    {"kind": "forecast", "point": 7.3, "ciLow": 7.276, "ciHigh": 7.324}
  ]
}
