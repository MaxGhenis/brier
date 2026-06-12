# Skill: calibration — deriving the point and the 80% interval

The number is the output of a stated computation, never a vibe.

## Point estimate
- Default: blend persistence (last print), momentum (trend of last 3-6
  prints), and the base rate (mean/median of the recent distribution).
  State the weights in the math step.
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

## Base rate step (mandatory)
One trace step must quantify the reference class explicitly, e.g.:
"Last 24 MoM core CPI prints: mean +0.26%, std 0.08, range 0.1-0.45;
16 of 24 within ±0.1 of trailing 3-month mean."

## Round numbers
Match the precision of the published series (CPI MoM to 0.1, claims to the
nearest 1k, rates to 0.1pp). The forecast step and cell fields must agree
exactly.
