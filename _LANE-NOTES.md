# Conditional policy-chain lane notes

## Scope and baseline

- Branch: `feat/conditional-policy-chain-rubric` at the requested base
  `0878919f` (clean at start; `origin/main` had advanced by three unrelated
  records/witness commits, so this lane was not rebased).
- Protected records, docket, generated site data, ledger-entry drafts, and
  workflows remain out of scope. No push or PR action is authorized.

## Decisions

- Apply the fail-closed policy-chain validator to ordinary `fast` and `full`
  runs only. Full prompts already embed `docs/cell-contract.md` verbatim, so
  documenting the rule there gives full mode the exact syntax without changing
  the versioned analyst system prompt.
- Keep `ladder` and `ladder_v2` byte-stable. Both reuse `build_fast_prompt`, so
  their builders explicitly opt out of the new conditional-only block; their
  validator remains untouched.
- Treat `Policy chain:` as a case-sensitive, position-zero prefix. A cited
  precedent path requires every HTTP(S) URL in that step to appear exactly in
  `sourceContext`.
- Give the exact phrase `no fetched precedent` precedence over URLs in the
  same step, because a population-count or resolver URL is not evidence of a
  precedent. That fallback requires bound wording followed by a numeric value
  and the literal low-confidence label; URLs are removed before bound parsing
  so digits inside a URL cannot satisfy the numeric gate.
- Require the pre-submit reviewer to return `REQUEST_CHANGES` plus a blocking
  `policy_chain` finding for a noncompliant conditional draft, and to compare
  the stated policy effect's direction and size with its cited precedent.
- Gate that reviewer addition on both a present conditional and prompt mode
  `fast`/`full`. This preserves the old reviewer bytes for unconditional runs
  and for the sealed ladder lanes.
- Accept common explicit effect-bound forms (labeled ranges, `between`, `±`,
  and two-sided inequalities), but reject confidence levels, population
  counts, and resolution years as substitute bounds. Require the
  low-confidence label to attach syntactically to the policy term/effect.
- Parse cited HTTP(S) URLs through `urlparse` and require a hostname; strip
  ordinary surrounding/Markdown punctuation before exact `sourceContext`
  comparison.

## Verification

- `UV_PROJECT_ENVIRONMENT=/opt/homebrew UV_CACHE_DIR=/private/tmp/thesis-policy-uv-cache uv run --no-sync pytest tests/test_thesis_analyst_runner.py tests/test_thesis_analyst_env_hygiene.py tests/test_verify_attested_bundle.py`
  — 308 passed in 73.18s. `--no-sync` used the installed development
  environment because the sandbox cannot write the default uv cache or reach
  PyPI.
- `UV_PROJECT_ENVIRONMENT=/opt/homebrew UV_CACHE_DIR=/private/tmp/thesis-policy-uv-cache uv run --no-sync ruff check scripts/run_thesis_analyst.py scripts/thesis_records_to_comparisons.py tests/test_thesis_analyst_runner.py tests/test_thesis_analyst_env_hygiene.py`
  — passed.
- `uv run --no-sync ruff format --check` for the two touched Python files —
  passed; `git diff --check` passed.
- Direct comparison with `HEAD` confirmed byte-identical conditional ladder
  forecast/reviewer prompts. Forecast SHA-256 values remain
  `e47e6781dbc1aa6ee9744745de440bf84cbb6a2ac09d1ba0db7ba194e600d980`
  (`ladder`) and
  `3c507e8d51b5264f6297c27c7444e9154ae309accc62fd027e3fffd5a93489a9`
  (`ladder_v2`). Reviewer SHA-256 values remain
  `c1650d4d8cfc90bd3504a0a1ae812bec3049118739f37e6a124758782cba3606`
  and `9d705983b0e3a9ffd61d1ca886b250b9b318c193a60486c613916a1406129d6f`,
  respectively.

## Final report

### Error strings added

- `conditional policy chain: missing reasoning step beginning exactly 'Policy chain:'`
- `conditional policy chain: Policy chain step must cite a precedent URL also listed exactly in sourceContext or contain exact phrase 'no fetched precedent'`
- `conditional policy chain: precedent URL in Policy chain step is not listed exactly in sourceContext: {url!r}`
- `conditional policy chain: 'no fetched precedent' path must state a numeric policy-term bound`
- `conditional policy chain: 'no fetched precedent' path must label the policy term low-confidence`

### Files touched

- `scripts/run_thesis_analyst.py`: fast conditional prompt block and ladder
  opt-outs at lines 726-835 and 1033-1110; mode-gated reviewer rubric at lines
  2262-2341; URL/bound/low-confidence parsing and conditional validator at
  lines 2744-2882; fast/full-only validation hook at line 2940; live reviewer
  mode binding at line 3906.
- `docs/cell-contract.md`: conditional decomposition/reviewer contract at line
  151 and literal fast/full validation rule at line 167.
- `tests/test_thesis_analyst_runner.py`: shared fake-Codex helpers at lines
  2365-2399; end-to-end and adversarial validator tests at lines 2403-2670;
  fast prompt, reviewer, sealed-ladder, and mode-boundary tests at lines
  4526-4637. Existing verbatim conditional-binding coverage remains at lines
  4233 and 4497.
- `_LANE-NOTES.md`: decision journal, verification record, and this final
  report.

### Tests added

- `test_fast_conditional_policy_chain_with_cited_precedent_passes`
- `test_fast_conditional_policy_chain_missing_step_fails_closed`
- `test_fast_conditional_policy_chain_url_must_be_in_source_context`
- `test_conditional_policy_chain_rejects_url_without_hostname`
- `test_fast_conditional_policy_chain_requires_precedent_or_explicit_fallback`
- `test_fast_conditional_policy_chain_no_precedent_with_bound_passes`
- `test_conditional_policy_chain_accepts_clear_numeric_bound_forms`
- `test_conditional_policy_chain_does_not_treat_confidence_as_effect_bound`
- `test_conditional_policy_chain_requires_low_confidence_term_label`
- `test_conditional_policy_chain_does_not_ignore_a_conflicting_second_step`
- `test_fast_conditional_policy_chain_no_precedent_requires_bound_and_confidence`
- `test_fast_nonconditional_cell_is_unaffected_by_policy_chain_gate`
- `test_pre_submit_review_requires_conditional_policy_chain_changes`
- `test_conditional_policy_chain_prompt_does_not_modify_ladder_contracts`
- `test_conditional_policy_chain_validation_respects_prompt_mode_boundary`

No protected path was changed. No PR was opened and nothing was pushed.

STOP
