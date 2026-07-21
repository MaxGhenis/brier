# Naming ontology (decided 2026-07-21)

Adopted from a blind design review (functionality-only elicitation, no
legacy names shown), confirmed against an independent in-house analysis,
and approved by Max. Display language changes now; recorded identifiers
migrate in one deliberate pass after the September paper.

## The three concepts

- **Forecaster** — the competing unit and the leaderboard row: a frozen,
  fully specified configuration of model + elicitation protocol +
  briefing. Changing any component creates a new forecaster. "Model"
  refers strictly to the underlying LLM; "agent" refers to the runtime
  actor inside a run (a forecaster may pool several agent runs).
- **Elicitation protocol** (short: protocol) — the declared-in-advance
  procedure that turns research into a submitted probability
  distribution, INCLUDING any independent repeats and the pooling rule
  (median-of-three is a protocol, not a separate knob). Lineage:
  structured expert judgment / probability encoding (Spetzler &
  Staël von Holstein 1975).
- **Briefing** — a versioned, reusable bundle of curated reference
  material handed to the forecaster at the start of a run in the spirit
  of "consider using this." Research is never restricted by a briefing;
  control runs are unassisted, not deprived. The collection is the
  briefing library. Recorded identifiers remain `packId@version` /
  `packSet` until the post-paper migration.

## The access-regime axis (separate from briefings)

**Open-book / closed-book** is a run-level property, not a property of
the briefing artifact. Everything today is open-book: briefed-vs-
unbriefed contrasts measure the marginal value of curated provision
(curation, salience, saved effort) — a null means "the agent finds this
on its own," never "the information is worthless." A future closed-book
mode (agent limited to the briefing, enforced and audited via the
archived activity records) would measure information value proper and
must never share the briefing's bare name.

## Experiment-design requirements that fall out

1. **Usage observability on both arms**: report whether the briefing was
   drawn on and how much of the control's fetched sourcing overlaps the
   briefing's contents (computable from archived run activity —
   `scripts/briefing_usage_report.py`). Without this, null results are
   uninterpretable.
2. **Placebo-shaped controls**: identical scaffold minus the briefing
   content, so the contrast is the material.
3. **Identity completeness**: briefing version and harness version are
   part of forecaster identity; "briefing: none" is an ordinary slot
   value, so control rows are ordinary forecasters.

## Rejected names (with the reasons, so they stay rejected)

"Strategy" anywhere — quant-native and wrong for a scored-not-traded
institution (strategies take positions); also collides with the internal
strategy-docket, which itself renames to protocol in the migration.
"Model" for the row — misattributes protocol/briefing effects to the
LLM. "Bot"/"agent" for the row — actor/configuration confusion.
"Corpus"/"training material" — reads as fine-tuning. "Knowledge base" —
implies retrieval infrastructure. "Toolkit" — collides with callable
tools. "Cheat sheet" — implies illegitimate advantage.

## Post-paper migration list (one deliberate pass, not before)

- `packSet`/`packMode`/`packId` identifiers → briefing terms in
  log.json/reward.json (versioned schema bump, consumers notified).
- `/packs` route → `/briefings` with a permanent redirect.
- strategy-docket / strategy-suite / strategy-lab internals → protocol
  naming.
- Leaderboard export field `agent` → `forecaster` (same pass).
