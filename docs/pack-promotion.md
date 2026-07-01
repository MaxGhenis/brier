# Pack Promotion

Packs start as experimental forecasting interventions. A pack should stay
optional while Thesis is still measuring whether it helps. Once the evidence is
strong enough, the useful part of the pack should move into the default Brier
or thesis.analyst prompt, skill, or tool policy.

Promotion is for general forecasting practices, not domain-specific facts. A
practice like "state the base rate before the inside view" can become default.
A source such as "use the BLS 2024-2034 employment projection for occupation
targets" should remain a pack or source-specific skill because it applies only
to some targets.

## Promotion Gate

A pack insight can be promoted when all of these are true:

1. It improves held-out forecast accuracy across enough resolved Thesis runs,
   measured primarily by normalized CRPS and secondarily by interval coverage.
2. The gain is robust across more than one target family, horizon, model, or
   prompt mode, unless the promoted rule is deliberately domain-scoped.
3. It does not use future information, private labels, hidden human edits, or
   outcome leakage.
4. It can be stated as a compact default rule that agents can follow without
   making traces less auditable.
5. It has a failure mode. The promotion note should say when the rule should
   not apply or when it should be weakened.

## Workflow

1. Run the pack as an ablation: same target family, same resolver, comparable
   model/prompt settings, with and without the pack.
2. Score resolved runs through the Brier reward export.
3. Record the evidence: affected pack, run set, score delta, interval coverage,
   domains tested, and known limitations.
4. If promoted, move the general rule into `agents/thesis-analyst/system.md`,
   a universal skill such as `skills/calibration.md`, or the Brier training
   policy.
5. Bump the agent version and rely on `promptHash`/`toolPolicyHash` to separate
   old runs from new default behavior.
6. Keep the original pack as a historical ablation label or mark it as
   superseded by the default agent version. Do not delete old run records.

## Current Promoted Practices

The following practices are already treated as default thesis.analyst behavior:

- resolve the exact first-print target before forecasting;
- fetch recent official-source history in the run;
- treat the outside-view base rate as the prior forecast before inside-view
  adjustments;
- weight the base-rate prior heavily by default, with explicit weights when
  blending persistence, recent momentum, and current evidence;
- publish simple benchmark baselines, including last-print persistence and
  panel shrinkage when applicable, before scoring the agent's own update;
- require named, direct current evidence before moving materially away from
  the strongest benchmark baseline, and shrink back when evidence is weak or
  already reflected in the official history;
- size 80% intervals from realized first-print dispersion;
- name concrete scenarios that would land outside each tail;
- update a forecast when new relevant official information arrives, while
  preserving earlier runs as separate scored records.

These defaults can still be challenged. If future scored runs show that a
default rule hurts accuracy, it should be demoted back into an experimental
pack or narrowed to the domains where it helps.
