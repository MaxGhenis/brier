# The open challenge: external forecasters on the registered docket

*Design, 2026-07-19. Status: schema + intake validator implemented; intake
workflow and site surfaces staged behind cross-model review (the intake
path is a trust surface).*

## Why

Accuracy is commodifying — every lab now ships a forecaster, and their
performance claims reduce to "trust the founder." The durable layer is
canonicity: the place where competing systems' claims become comparable
and checkable. Thesis's registered docket, mechanical resolution, and
witnessed chronology are exactly that machinery, so instead of entering
news-question tournaments off-design, we host: any external system may
forecast any open registered target, and its claims inherit the same
custody, the same scoring, and the same chronology tiers as our own
agents. A challenger who shows up validates the venue; a challenger who
wins earns a claim nobody can dispute — including us.

## Rules (v1)

1. **Question set.** The open registered docket, nothing else. Every
   target auto-resolves from a registered official source; no question is
   ever resolved by human judgment.
2. **Who may enter.** Any system. Participants self-declare
   `systemType` (`ai` | `human` | `hybrid`); the headline challenge is
   AI-vs-AI and leaderboards segment by declaration. Identity = the
   GitHub account that submits; one account is one challenger.
3. **One shot per target.** A challenger's first valid submission for a
   dataPointId is final; later submissions for the same pair are
   rejected. This matches our own agents' one-registered-run-per-lane
   discipline and blocks last-minute-information advantage. (Horizon-
   matched multi-update scoring is a possible v2; it must never change
   v1 scores retroactively.)
4. **Chronology is inherited, not negotiated.** A submission enters the
   records chain through the attested intake path and is externally
   witnessed like any records commit. The v5 tiers then apply verbatim:
   witnessed before the observation → headline-eligible;
   claimed-time-only → published below the fold; on or after the
   observation → violated. No special cases.
5. **Distributions, not vibes.** Minimum: point estimate + 80% central
   interval (scored via the same interval-seeded CDF our fallback uses).
   Encouraged: a quantile grid (`quantiles`: 0.05–0.95), scored as a
   piecewise-linear CDF exactly like agent-native distributions.
   `distributionProvenance: external_submission` labels every score.
6. **No trace requirement — visibly.** Our agents publish full reasoning
   traces; challengers may not want to. External cells are exempt from
   the trace-depth rubric and the site renders "reasoning: not published"
   on them. The transparency gap stays legible instead of being papered
   over.
7. **Scoring.** Identical to agents: exact CRPS on the materialized CDF,
   normalization only by pre-registered ledger dispersion, paired
   persistence comparison where a baseline exists. No challenger-specific
   scoring code paths.
8. **No prizes (v1).** Recognition is the leaderboard and the custody of
   the claim. Money changes the abuse calculus; it can come later with
   its own design pass.

## Mechanism

Challengers never touch trust surfaces:

- A challenger opens a PR adding one JSON file under
  `challenge-inbox/` (schema below; template in that directory). The
  inbox is data-only staging — nothing reads it at build or score time.
- The **intake workflow** (privileged, to be reviewed before landing)
  validates the file with `scripts/validate_challenge_submission.py`
  against trusted-HEAD code: schema, target exists and is an open
  registered target, no prior submission for the (challenger, target)
  pair, finite numbers, coherent interval/quantiles.
- On pass, the workflow writes the canonical submission record under
  `records/challenge/YYYY-MM-DD/…` via the same commit → attested push →
  recorder-witness path every records writer uses, and closes the PR
  with a receipt (record path + commit). On fail, it comments the
  precise refusal and closes. Challenger PRs are never merged; the
  privileged copy is the record.
- The site build reads `records/challenge/` only: external cells join
  scoring with `agent: <challengerId>` and `participation: external`.

Sybil note: many-accounts entry is visible by construction (every
submission names its account) and buys nothing under one-shot-per-target
plus no prizes; revisit with any prize design.

## Submission schema (`thesis_challenge_submission_v1`)

```json
{
  "schemaVersion": "thesis_challenge_submission_v1",
  "challenger": "github:preseen-team",
  "systemType": "ai",
  "systemName": "Preseen Chestnut",
  "dataPointId": "us.dol.initial_claims.sa.week_2026-07-25",
  "pointEstimate": 214.0,
  "ciLow": 200.0,
  "ciHigh": 229.0,
  "quantiles": [
    {"p": 0.05, "value": 196.0},
    {"p": 0.25, "value": 207.0},
    {"p": 0.5, "value": 214.0},
    {"p": 0.75, "value": 221.0},
    {"p": 0.95, "value": 233.0}
  ],
  "generatedAtUtc": "2026-07-20T14:00:00Z",
  "notes": "optional, ≤500 chars, rendered verbatim with the cell"
}
```

`quantiles` optional; when present it must be strictly increasing in
both `p` and `value`, include 0.1/0.5/0.9 or bracket them, and agree
with `ciLow`/`ciHigh` at 0.1/0.9 within interpolation tolerance.
`generatedAtUtc` is the challenger's claim; chronology never trusts it —
the witnessed intake commit is the clock.

## Build plan

| Piece | Status |
|---|---|
| Design (this doc) | done |
| `scripts/validate_challenge_submission.py` + tests | done |
| Intake workflow (`challenge-intake.yml`) | staged — cross-model review first (privileged writer + PR-triggered = the risky pair) |
| Attestation allowlist entry for the intake workflow | with the workflow |
| Site: scoring ingestion of `records/challenge/`, external flag on leaderboards | next |
| `/challenge` page: rules, how to enter, live external scores | next |
| Outreach (Preseen, Mantic, FutureSearch, Metaculus bot authors) | after the lane is live-fired end to end |
