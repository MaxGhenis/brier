# Challenge lane v2: API intake design (2026-08-23)

*Written when the v1 lane was withdrawn from main (operator decision,
2026-08-23): v1 shipped ahead of its dependencies — human-discretion PR
merges as intake, optional signing, no scoring ingestion, no headline-tier
path — while the grading loop it showcases still carries resolver debt.
This branch holds the complete v1 implementation plus this target design.
Build it when the lane wins a roadmap slot; the operator's standing
requirement is that signing is mandatory from the first v2 submission.*

## The four proofs a submission needs

An external win is only undisputable if every submission carries:

1. **Who** — an identity bound to the artifact (OIDC via Sigstore keyless;
   GitHub account remains the challenger identity, one account = one
   challenger).
2. **What** — the exact bytes, immutable (the signature covers the
   submission file's digest).
3. **When** — proof the forecast existed before the outcome *without
   trusting Thesis*: the Rekor transparency-log inclusion gives the digest
   an independent public timestamp. This is what lets an external row meet
   the same witnessed-chronology bar as internal runs under the v5 tiers.
4. **How scored** — the identical mechanical pipeline; no
   challenger-specific code paths (v1 already got this right).

## Submission lifecycle

1. Challenger signs the submission JSON with Sigstore keyless
   (`uvx --from sigstore sigstore sign …`) — after the final byte edit.
2. One POST to forecast-api: `{submission, sigstoreBundle}`. **Signing is
   required; unsigned submissions are refused with the exact reason.**
3. The server validates mechanically, with zero human discretion: schema;
   target exists, is open, and is registered; one-shot per identity per
   dataPointId (first accepted content wins); quantile grid coherent;
   signature verifies; Rekor inclusion proof checks; digest matches.
   Immediate response: accepted-with-receipt (record path + commit +
   digest) or a precise refusal.
4. On accept the server writes the canonical record through the same
   attested records path as every internal run (commit → witnessed), under
   `records/challenge/…`. External rows become headline-eligible under the
   v5 tiers with no special cases.
5. `site/src/data/challenge.ts` becomes generated output of
   `records/challenge/` (deleting the v1 hand-maintained registry), and
   scoring ingestion reads only from records.
6. The PR inbox either retires or becomes a thin second client of the same
   validator — one intake brain, two doors.

## Display requirements before any promotion

- Lead time on every external row (submitted → resolved): one-shot blocks
  updates, not late submission, and "beat the agents" claims must show the
  information-horizon difference until horizon-matched comparison exists.
- The trace exemption stays visibly labeled (v1 rule 6).
- Per-challenger history one click from any win, as the honest answer to
  reputation cherry-picking across accounts (sybil note, v1).

## v2+ options, each needing its own pass

- Commit-reveal (accept sealed digests, reveal at resolution).
- Prizes (changes the abuse calculus entirely; revisit sybil posture).
- Horizon-matched multi-update scoring (must never change v1 scores
  retroactively).

## What was grandfathered at withdrawal

Two accepted v1 submissions (PavelMakarchuk / jolts-hires-rate,
khs / u6-underemployment-rate, both 2026-07-31, GitHub-identity-attributed,
claimed-time tier, reward-excluded) remain published on their cells, keep
flowing through the daily recorder, and their witnessed records stand.
Withdrawal closed the door; it did not unpublish anyone.
