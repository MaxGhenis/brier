# Skill: calibration — deriving the point and the 80% interval

The number is the output of a stated computation, never a vibe.

## Point estimate

- Default: start with the strongest base-rate prior, not an inside-view blend.
  For repeated official series this is usually last-print persistence; for
  panel targets it is persistence plus cross-sectional shrinkage; for level
  targets without a recent print it is the mean/median of the reference class.
  This prior is the forecast unless current evidence clears the update test.
- Before applying inside-view adjustments, write down benchmark forecasts the
  run must beat: last-print persistence for repeated series, and
  persistence plus cross-sectional shrinkage for panel targets.
- For repeated numeric series with enough history, write down model candidates
  under the `thesis_model_candidate_v1` schema before choosing the agent
  forecast. At minimum include persistence; when available and appropriate,
  include an open-source time-series adapter such as statsmodels local-level,
  StatsForecast AutoETS/AutoARIMA/Theta, or a hierarchical reconciler. The
  candidate is only admissible if it reports point, p10/p50/p90, 80% and 90%
  intervals, train cutoff, interval method, calibration_n, and any
  walk-forward score.
- If the proposed point moves materially away from the strongest benchmark,
  the trace must name the current evidence that justifies the move. Without
  that evidence, shrink the point back toward the benchmark.
- When combining prior, momentum, and current evidence, state the weights in
  the math step. The prior should normally carry 70-90% of the weight for
  short-horizon official series unless the current signal is direct,
  release-specific, and historically predictive.
- Do not count generic narratives twice. If a mechanism is already reflected
  in the recent official history, it should not move the point away from the
  prior without new evidence.
- For policy-conditional cells: point = unconditional model + the decomposed
  policy effect (see the policy skills). The conditional-minus-unconditional
  gap must fall out of the model, not be asserted.

## 80% interval

- Compute the realized dispersion of recent FIRST prints: std or the
  10th-90th percentile band of the last 24 comparable prints (or all
  available if fewer). First prints, not revised values — we resolve on
  first print, so revision noise is part of the distribution.
- Width = that band, widened (state the factor) for: conditioning
  uncertainty, structural breaks in the series, releases with known extra
  variance (e.g. annual revisions landing in the target print).
- Asymmetry is allowed and often right (rates bounded below, error rates
  skewed); justify it from the historical distribution, not taste.
- Sanity check: would roughly 8 of the last 10 prints have landed inside an
  interval built this way? Say so in the trace.
- Panel targets need an additional sanity check: would the interval have
  covered the entity's last one or two first-print moves, and does the
  cross-sectional distribution show fatter tails than the single-series
  history?
- If the selected model candidate lacks native intervals, wrap it rather than
  dropping uncertainty: use conformal intervals if there is enough calibration
  history, residual/bootstrap intervals if fitted residuals exist, panel
  empirical intervals for related government series, or an explicit
  fallback-prior interval for sparse histories. Label the interval method in
  the trace.

## Base rate step (mandatory)

One trace step must quantify the reference class explicitly, e.g.:
"Last 24 MoM core CPI prints: mean +0.26%, std 0.08, range 0.1-0.45;
16 of 24 within ±0.1 of trailing 3-month mean."

## Round numbers

Match the precision of the published series (CPI MoM to 0.1, claims to the
nearest 1k, rates to 0.1pp). The forecast step and cell fields must agree
exactly.
