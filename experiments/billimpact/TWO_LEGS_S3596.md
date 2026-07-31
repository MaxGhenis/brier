# S.3596, both legs measured — the synthesis

Two independent measurements of the same bill landed today:

**Mechanical leg** (PR #64, D. Trimmer): S.3596 priced on certified Populace
build P via the validated PolicyEngine call path — budgetary impact −$1.83B;
**child poverty −1.2pp** (17.02% → 16.82%, PE poverty measure, 2026); gains
bottom-concentrated (D1 +$31.90/yr vs D10 +$0.30/yr). Certified stack
policyengine-us==1.764.6 on build P; stale published numbers (−$1.6B / −0.4pp)
superseded by the refresh — the poverty effect tripled, which is the PR's own
argument for admissibility gates.

**Forecast leg** (this study): opus-5 and fable-5, conditioned on enactment,
forecasting the Census-published SPM child poverty rate for CY2027 against the
registered target `census.spm.child_poverty_rate.2027`: **−0.10 to −0.15pp**
(medians of 3 reps; mechanical grounding table in-prompt).

**The gap is the finding.** The forecast leg concedes roughly a tenth of the
mechanical effect. Measure universes differ (PE's poverty measure on build P
vs Census SPM child rate; 2026 static vs 2027 realized), so levels are not
commensurable — but a 10x delta gap is not a units artifact. It is the same
behavior this study demonstrated causally elsewhere: forecasters anchor on the
published series trajectory and shade it, rather than propagating the
mechanical effect of the statute in front of them (recall-anchoring; see
RESULTS.md §3a). The product implication is the composition architecture: the
mechanical delta must be injected from the mechanical leg, not re-derived
inside the forecast.

Certification note: this study's household point-checks ran policyengine-us
1.784.3. Under the #64 contract that pairing question does not arise —
certification governs model↔data-build pairing for population runs, and
household arithmetic uses no population build — but the version is stated
here so the distinction is explicit.
