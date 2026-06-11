# Brier paper revisions — March 15, 2026

## Priority 1: Narrative fixes

- [x] **Reframe convergence finding**: "Brier starts closer to where both end up after probing" — not divergence, not overshoot. Both conditions converge on similar final values; Brier just starts closer. Change throughout abstract, Section 5.5, Section 6.3, Section 7.
- [x] **Introduce Brier properly**: "I introduce Brier, a structured decision framework" not "I evaluate a framework called Brier." This paper IS the introduction. Add footnote linking to GitHub/site.
- [x] **Drop "pre-registered" claims**: Replace with "analysis code was committed prior to data collection (December 2025; experiments ran February 2026)." No formal pre-registration exists — just git history (commits 50e93d4, bfd1aae predate experiment runs).

## Priority 2: Graphs (desperately needed)

- [x] **Update magnitude box/violin plots**: by condition, for each model — added `fig_magnitude_distribution` (box plots of raw update magnitude by condition per model across the 8 primary scenarios; means as diamonds), cited in Results.
- [x] **Per-scenario forest plot**: effect sizes with CIs for each scenario — `fig_forest_plot` already existed; fixed "farness"→"Brier" in title/axis label.
- [x] **Convergence visualization**: show initial→final for naive vs Brier on 2-3 scenarios — `fig_convergence` already existed (2 models × 3 scenarios); fixed "farness"→"Brier" in title.
- [x] **Sycophancy bar chart**: Claude vs GPT update magnitude — `fig_sycophancy` (upward, existing; fixed typo) plus NEW `fig_sycophancy_direction` bar chart contrasting upward vs downward pressure across conditions/models (the symmetric finding). NOTE: paper now uses GPT-5.4 as primary GPT model (GPT-5.2 is archival); figures reflect this.

## Priority 3: Content additions

- [x] **Concrete example**: sunk_cost_project — added a "Raw response excerpts" subsection with actual GPT-5.4 naive vs Brier initial responses (Claude records don't store response text; GPT-5.4 is the primary model and does). Shows Brier front-loading Standish/CHAOS + McKinsey/Oxford base rates and named biases before any probe.
- [x] **Sycophancy deep-dive**: added "Sycophancy is direction-dependent" subsection. Verified-from-data numbers: GPT-5.4 upward naive 191.7 → Brier 48.3; archival GPT-5.2 466.7 → 108.3 (retained in cross-model text). Claude upward 0.0. The deep-dive's headline is the directional asymmetry (below).
- [x] **Run symmetric sycophancy test**: Claude + GPT-5.2 down data already existed; COLLECTED the missing GPT-5.4 downward scenario (18 results, legacy Study-1 prompts, ~36 API calls). Finding: downward pressure → mass capitulation everywhere (Claude 650/625/495; GPT-5.4 650/633/643; GPT-5.2 660/640/640), and the upward Brier advantage does NOT transfer downward. API keys were available via agent-secret.

## Priority 4: Technical fixes

- [x] **Scale heterogeneity note**: added. The pooled model already uses *relative* update (not the old raw −37.0/−4.17 coefficients), so the units artifact is largely pre-empted; added an explicit note that the raw-magnitude cross-model gap is ~entirely the leads-scale sycophancy scenario (GPT-5.4 naive 30.97→14.90 without it; Claude ~unchanged).
- [x] **CI rate metric → appendix**: removed from Table 1, Table 2, and the primary @tbl-stability; moved to a new "Initial confidence-interval rate" appendix section.
- [x] **Consolidate "transient API errors"**: now a single mention in Section 4.4 ("Model and procedure"); Sample-size, Results-overview, and Limitations now cross-reference it instead of re-disclosing.
- [x] **Fix "overshoot"/"diverge" language**: Replace throughout with the correct framing (see Priority 1).
- [x] **Default CoT caveat**: already present in Discussion ("recent frontier models may employ implicit chain-of-thought reasoning even without explicit CoT prompting..."); verified, no change needed.
- [x] **Mixed-effects as primary**: already satisfied — Statistical-analysis section explicitly treats mixed-effects as primary and labels Mann-Whitney a "secondary robustness check"; verified, no change needed.

## Priority 5: Citation/style fixes (not in this task's explicit scope; status noted)

- [x] **Fix Quarto citation style**: already done — `_quarto.yml` sets `csl: apa.csl`; rendered output shows "Wei et al., 2022" (no first name). Verified via HTML render.
- [ ] **Newer lit review**: NOT done (out of scope for this pass; would need web search for post-2024 citing papers).
- [ ] **Check for outdated claims**: NOT done (out of scope for this pass). Paper already hedges ForecastBench parity as "approach but do not match" rather than a dated projection.

## Key data points for reference

- Claude mixed-effects: Brier = -4.17 (p<0.001), CoT = -0.56 (p=0.34)
- GPT mixed-effects: Brier = -37.0 (p=0.009), CoT = -29.7 (p=0.036)
- GPT sycophancy (adversarial_sycophancy): naive mean update = 466.7 leads, Brier = 108.3, Claude naive = 0.0
- Scenarios use different units: percentages (most), weeks (planning), leads (sycophancy)
- Analysis code: commits 50e93d4 (Dec 19) and bfd1aae (Dec 20), experiments: Feb 16-18
- Skill optimization loop was running (PID 20928) — check if it finished and apply the optimized description
