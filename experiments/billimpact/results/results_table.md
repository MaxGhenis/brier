# Results table — one row per configuration cell

Generated 2026-07-31T10:29:55-04:00 from `experiments/billimpact/runs_api.reparsed.jsonl`.

**N = 2520 runs read, 2516 scored, 42 configuration cells, 12 units.** Sweep completion: 2520/2520 cells (100.0%).

Every row states its own N. Reps per (cell, unit) = 5 by pre-registration; a partial sweep will show fewer.

**Column definitions.**

- `n_runs` — runs in this configuration cell, pooled over units and repeats. `n_units` — distinct units contributing. `n_scored` — runs with a parsed forecast.
- `median_persons` — median across units of the per-unit median forecast, in persons. Units differ in scale by ~4x (CA ~4.4M vs OH ~1.4M), so this column is **not** comparable across units; it is here for face-validity only. Use `median_norm`.
- `median_norm` — median of (forecast / that unit's unconditioned median), where the unconditioned median is the unit's median forecast at `policy_context=none` with the other four dimensions at reference (elicitation=point_ci_json, pipeline=single_pass, model=claude-sonnet-5, magnitude=actual). 1.000 means identical to the unconditioned forecast.
- `sd_reps_%` — mean across units of (SD of the forecast across repeats within this cell / mean forecast) x 100. This is the per-config variance that the pre-registration forbids omitting. `sd_reps_persons` is the same in persons.
- `mean_crps` / `sd_crps` — CRPS against the first print, persons, across all runs in the cell. `crps_norm` — CRPS divided by the SD of that unit's own supplied 60-month history (frozen in ground_truth.json at pre-registration). **Never normalised by the model's own interval width.**
- `cov80` — fraction of runs whose 80% interval contains the first print (nominal 0.80). `mean_pit` — mean probability integral transform (calibrated = 0.50, uniform). `width` — mean 80% interval width, persons; `width_norm` — the same divided by the unit's history SD.
- `n_implaus` — runs flagged `implausible_extraction`. A parsed forecast is flagged `implausible_extraction` when its point OR either interval endpoint falls outside [0.1x, 10x] the unit's last observed history value. This band is deliberately loose (a state SNAP caseload cannot move 10-fold in 30 months). It exists to separate an extraction artefact from a forecast, not to filter forecasts by quality. **Flagged runs are retained in every number in this table**; the sensitivity analysis that excludes them is reported separately in `dispersion.md` and `primary_analyses.md`.

| policy_context | elicitation | pipeline | model | magnitude | n_runs | n_units | n_scored | n_parse_fail | n_api_err | n_implaus | median_persons | median_norm | sd_reps_% | sd_reps_persons | mean_crps | sd_crps | mean_crps_norm | cov80 | mean_pit | width | width_norm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| none | cot_then_json | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,900,000 | 1.007 | 1.97 | 66017 | 100,750 | 100,675 | 0.654 | 0.700 | 0.500 | 364,333 | 2.570 |
| none | forced_choice_bins | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,950,000 | 1.017 | 3.42 | 129,335 | 173,472 | 250,288 | 0.994 | 0.500 | 0.424 | 250,383 | 1.722 |
| none | free_text | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,865,000 | 0.988 | 4.45 | 146,068 | 142,398 | 151,439 | 0.971 | 0.550 | 0.583 | 382,833 | 2.491 |
| none | point_ci_json | debate | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,900,000 | 1.011 | 1.79 | 58705 | 109,440 | 97846 | 0.711 | 0.850 | 0.493 | 503,833 | 3.693 |
| none | point_ci_json | single_pass | claude-fable-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,955,000 | 1.021 | 0.70 | 26360 | 99020 | 75689 | 0.618 | 0.867 | 0.423 | 543,000 | 3.565 |
| none | point_ci_json | single_pass | claude-haiku-4-5-20251001 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 3,048,500 | 0.964 | 1.01 | 26492 | 307,269 | 371,916 | 2.168 | 0.167 | 0.486 | 159,050 | 1.006 |
| none | point_ci_json | single_pass | claude-opus-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,900,000 | 1.007 | 0.99 | 32872 | 88788 | 56368 | 0.584 | 0.983 | 0.479 | 599,083 | 3.977 |
| none | point_ci_json | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,875,000 | 1.000 | 1.91 | 54524 | 131,963 | 119,532 | 0.873 | 0.500 | 0.545 | 309,000 | 2.202 |
| operative_only | cot_then_json | single_pass | claude-sonnet-5 | actual | 60 | 12 | 59 | 1 | 0 | 0 | 2,900,000 | 1.000 | 3.20 | 103,541 | 129,607 | 139,689 | 0.929 | 0.576 | 0.529 | 321,695 | 2.346 |
| operative_only | forced_choice_bins | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 3,040,000 | 0.990 | 1.47 | 48973 | 298,206 | 330,998 | 2.134 | 0.183 | 0.450 | 177,167 | 1.204 |
| operative_only | free_text | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,840,000 | 0.990 | 3.07 | 93783 | 183,510 | 253,286 | 1.201 | 0.300 | 0.617 | 283,447 | 1.926 |
| operative_only | point_ci_json | debate | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,900,000 | 1.010 | 2.15 | 72129 | 130,620 | 147,132 | 0.732 | 0.683 | 0.521 | 376,000 | 2.692 |
| operative_only | point_ci_json | single_pass | claude-fable-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,950,000 | 1.017 | 0.98 | 34881 | 89209 | 73773 | 0.549 | 0.833 | 0.411 | 462,167 | 3.061 |
| operative_only | point_ci_json | single_pass | claude-haiku-4-5-20251001 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 3,115,000 | 0.951 | 1.22 | 28910 | 311,665 | 368,152 | 2.208 | 0.017 | 0.468 | 141,267 | 0.879 |
| operative_only | point_ci_json | single_pass | claude-opus-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,922,500 | 1.010 | 1.01 | 31440 | 85999 | 58474 | 0.555 | 1.000 | 0.472 | 556,333 | 3.776 |
| operative_only | point_ci_json | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,850,000 | 0.993 | 0.69 | 19234 | 141,059 | 110,957 | 1.094 | 0.317 | 0.613 | 233,833 | 1.549 |
| operative_only | point_ci_json | single_pass | claude-sonnet-5 | inert | 60 | 12 | 60 | 0 | 0 | 0 | 2,835,000 | 0.981 | 1.57 | 49192 | 169,748 | 187,724 | 1.238 | 0.250 | 0.649 | 242,333 | 1.617 |
| operative_only | point_ci_json | single_pass | claude-sonnet-5 | severe | 60 | 12 | 60 | 0 | 0 | 0 | 2,840,000 | 1.000 | 0.47 | 10908 | 127,762 | 95106 | 1.034 | 0.233 | 0.627 | 248,167 | 1.645 |
| operative_plus_purpose | cot_then_json | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,900,000 | 1.000 | 3.37 | 118,690 | 122,916 | 175,807 | 0.784 | 0.650 | 0.541 | 342,375 | 2.415 |
| operative_plus_purpose | forced_choice_bins | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,900,000 | 0.993 | 1.63 | 54139 | 320,459 | 374,346 | 2.197 | 0.167 | 0.508 | 176,500 | 1.140 |
| operative_plus_purpose | free_text | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,865,000 | 0.981 | 4.70 | 149,441 | 192,713 | 260,712 | 1.374 | 0.367 | 0.606 | 291,753 | 1.944 |
| operative_plus_purpose | point_ci_json | debate | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,900,000 | 1.000 | 1.74 | 59092 | 111,641 | 99421 | 0.759 | 0.667 | 0.537 | 376,667 | 2.629 |
| operative_plus_purpose | point_ci_json | single_pass | claude-fable-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,955,000 | 1.019 | 0.91 | 39372 | 93002 | 80782 | 0.573 | 0.817 | 0.417 | 469,500 | 3.077 |
| operative_plus_purpose | point_ci_json | single_pass | claude-haiku-4-5-20251001 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,967,500 | 0.951 | 1.11 | 29796 | 303,530 | 380,359 | 2.092 | 0.117 | 0.515 | 150,233 | 0.944 |
| operative_plus_purpose | point_ci_json | single_pass | claude-opus-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,905,000 | 1.008 | 0.76 | 27021 | 84731 | 55570 | 0.551 | 1.000 | 0.475 | 556,250 | 3.764 |
| operative_plus_purpose | point_ci_json | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,790,000 | 0.976 | 0.71 | 18705 | 196,583 | 279,278 | 1.336 | 0.283 | 0.636 | 242,833 | 1.632 |
| purpose_only | cot_then_json | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,825,000 | 0.988 | 2.88 | 92723 | 117,833 | 108,545 | 0.835 | 0.600 | 0.585 | 341,500 | 2.448 |
| purpose_only | forced_choice_bins | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,875,000 | 1.000 | 3.07 | 108,553 | 165,482 | 153,878 | 1.567 | 0.367 | 0.539 | 234,083 | 1.463 |
| purpose_only | free_text | single_pass | claude-sonnet-5 | actual | 60 | 12 | 59 | 1 | 0 | 0 | 2,840,000 | 0.993 | 2.80 | 80583 | 132,957 | 114,051 | 0.907 | 0.458 | 0.631 | 298,475 | 2.015 |
| purpose_only | point_ci_json | debate | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,885,000 | 1.007 | 2.32 | 82246 | 125,463 | 131,836 | 0.784 | 0.800 | 0.534 | 474,667 | 3.317 |
| purpose_only | point_ci_json | single_pass | claude-fable-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,955,000 | 1.021 | 0.62 | 20965 | 91034 | 73558 | 0.577 | 0.833 | 0.426 | 471,000 | 3.202 |
| purpose_only | point_ci_json | single_pass | claude-haiku-4-5-20251001 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,965,000 | 0.947 | 0.85 | 20218 | 311,812 | 367,349 | 2.245 | 0.083 | 0.534 | 172,400 | 1.134 |
| purpose_only | point_ci_json | single_pass | claude-opus-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,930,000 | 1.014 | 0.96 | 31615 | 90566 | 61017 | 0.582 | 1.000 | 0.470 | 577,333 | 3.862 |
| purpose_only | point_ci_json | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,750,000 | 0.973 | 0.79 | 24326 | 148,304 | 121,836 | 1.072 | 0.283 | 0.676 | 289,500 | 2.082 |
| summary | cot_then_json | single_pass | claude-sonnet-5 | actual | 60 | 12 | 58 | 2 | 0 | 0 | 2,872,500 | 1.000 | 2.79 | 92512 | 125,909 | 153,394 | 0.876 | 0.638 | 0.549 | 335,690 | 2.428 |
| summary | forced_choice_bins | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,850,000 | 1.021 | 2.73 | 89845 | 250,164 | 279,056 | 1.642 | 0.317 | 0.544 | 201,583 | 1.406 |
| summary | free_text | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,855,000 | 0.990 | 3.24 | 101,887 | 185,947 | 255,713 | 1.113 | 0.450 | 0.606 | 298,541 | 2.139 |
| summary | point_ci_json | debate | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,900,000 | 1.013 | 2.26 | 82109 | 116,610 | 137,492 | 0.717 | 0.783 | 0.497 | 442,500 | 3.120 |
| summary | point_ci_json | single_pass | claude-fable-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,950,000 | 1.020 | 0.51 | 18069 | 96164 | 73084 | 0.600 | 0.867 | 0.417 | 521,333 | 3.425 |
| summary | point_ci_json | single_pass | claude-haiku-4-5-20251001 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,915,000 | 0.952 | 0.97 | 22199 | 291,324 | 377,340 | 2.077 | 0.200 | 0.573 | 167,617 | 1.061 |
| summary | point_ci_json | single_pass | claude-opus-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,915,000 | 1.010 | 1.14 | 37385 | 93599 | 68153 | 0.600 | 0.967 | 0.468 | 574,417 | 3.795 |
| summary | point_ci_json | single_pass | claude-sonnet-5 | actual | 60 | 12 | 60 | 0 | 0 | 0 | 2,860,000 | 0.997 | 1.13 | 41169 | 155,182 | 179,353 | 1.180 | 0.417 | 0.595 | 267,000 | 1.875 |

## Data quality

- Lines in file: **2520** (blank 0, malformed JSON 0, missing required field 0).
- Records read (one per `cell_key`): **2520**; duplicate `cell_key` seen: **0**, of which 0 were resolved in favour of a later record that parsed (the rest kept the first occurrence); unknown unit_id: **0**.
- **Records removed from the runs file by another process** (found in sibling quarantine files beside it — reported, not analysed, because a dropped-run count computed only from `--runs` would silently understate):
    - `runs_api.quarantined.jsonl`: 9 record(s); 9 of those cells were subsequently re-run and ARE present in the runs file, 0 are not; reasons {'max_tokens truncation; re-run with raised cap': 9}
- API errors: **0**.
- Parse failures: **4** (0.16% of records read)
    - `single_value_no_interval (output truncated at max_tokens=3000)`: 2
    - `no_scale_candidates (output truncated at max_tokens=3000)`: 1
    - `single_value_no_interval (output truncated at max_tokens=2000)`: 1
- Parse failures attributable to output truncation at the harness `max_tokens` cap: **4** of 4.
- Parse modes: {'json_v2': 2212, 'prose_bracketed_v2': 275, 'prose_ordered_v2': 27, 'failed_v2': 4, 'prose_spread_v2': 1, 'prose_pair_v2': 1}. `json` is the intended path; `prose_triple` / `prose_ordered` are the free-text regex fallbacks in `harness.parse_forecast` and carry more extraction risk.
- Runs scored: **2516**; scoring exceptions: 0.
- Forecasts flagged `implausible_extraction` (retained, **not dropped**): **0** — see the section above.
- `truth` disagreements between run records and ground_truth.json: **0**.
- Pre-registered grid: **2520** (unit, config, rep) cells; observed **2520**; **missing 0** (2520/2520 cells (100.0%)). Observed cells not in the planned grid: 0.
