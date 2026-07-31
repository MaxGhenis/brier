# Challenge-lane submitter signing (Sigstore keyless)

*Shipped 2026-07-31 per
[#52](https://github.com/ThesisInstitute/thesis/issues/52). Optional for
every submission; the first submission
([#49](https://github.com/ThesisInstitute/thesis/pull/49)) predates this
and is grandfathered as GitHub-identity-attributed.*

A challenge submission's two key claims — *this exact artifact* and
*before the release* — otherwise rest on this repository's history and
custody chain. Keyless signing makes both claims verifiable without
trusting Thesis at all: the signature binds the submission file's exact
bytes, and the Rekor transparency log gives that digest an independent
public timestamp.

This distributes **proof, not signing authority**. Publish-side signing is
unchanged and stays CI-only: producer signatures over record snapshots
(`docs/producer-signing-ceremony.md`), workflow attestations on every
records push, and RFC 3161 witnesses. Nothing in the submitter-signing
path reads or writes `records/**`; challenger PRs still touch only
`challenge/inbox/`.

## Signing (challenger side, one command)

Sign the submission file you are about to PR — after your final edit, since
any byte change invalidates the signature:

```bash
uvx --from sigstore sigstore sign challenge/inbox/<you>/<cell>.json
```

A browser window opens for OIDC login (choose GitHub); the bundle lands
beside your submission as `<cell>.json.sigstore.json` — the verifier's
expected name — and the signature is uploaded to the public Rekor log.
Commit **both files** in your PR. Equivalent with cosign (the flag matters:
only the new bundle format is accepted):

```bash
cosign sign-blob --new-bundle-format \
    --bundle challenge/inbox/<you>/<cell>.json.sigstore.json \
    challenge/inbox/<you>/<cell>.json
```

Working inside a clone of this repo, the guard-railed wrapper does the
same with schema and path checks plus a receipt printout:

```bash
uv run --extra challenge python scripts/sign_challenge_submission.py \
    challenge/inbox/<you>/<cell>.json
```

To rehearse without touching the production log, add `--staging` (staging
bundles do not verify against production trust roots — never PR one).

## What verification establishes

```bash
uv run --extra challenge python scripts/verify_challenge_signatures.py
```

sweeps the inbox fail-closed. For each signed submission it checks:

1. **Cryptographic validity** — delegated entirely to
   [sigstore-python](https://github.com/sigstore/sigstore-python) (pinned
   `sigstore==4.5.0` in the `challenge` extra): certificate chains to
   Fulcio, certificate transparency SCT, Rekor inclusion, Rekor's signed
   entry timestamp, and the signature over the submission's exact bytes.
2. **Digest match** — the bundle's `messageDigest` equals the file's
   sha256, reported as `artifactSha256`. A bundle made for different bytes
   is refused outright.
3. **Chronology** — the Rekor `integratedTime` must *strictly precede* the
   target's release instant. By default that instant is derived
   conservatively from the registered target: the earlier of
   `resolutionDate` and `sourceBinding.expectedReleaseWindow.start`,
   floored to 00:00:00 UTC of that day (day-granularity fields prove
   nothing about intraday order, so the signature must beat the day's
   first instant). At scoring time, pass the actual first-print instant
   with `--release-at` for the exact comparison.

Unsigned submissions are listed and remain valid. A present-but-invalid
bundle always fails the sweep: a broken proof is tampering evidence, not a
missing option. Orphan bundles (no matching submission) and unexpected
inbox files fail it too.

### Identity is recorded, not enforced (by default)

A keyless certificate from the interactive flow names the GitHub-verified
**email** the challenger logged in with; there is no mechanical mapping
from that email to the `challenger: github:<login>` field, so account
attribution stays where it always was — the GitHub identity that opened
the inbox PR. The verifier records the certificate's subjects and OIDC
issuer verbatim (`identityPolicy: recorded_not_enforced`).

Challengers who want account-bound certificates can sign from a GitHub
Actions workflow in their own fork (ambient OIDC): the certificate subject
becomes their `https://github.com/<owner>/<repo>/...` workflow identity,
checkable with:

```bash
uv run --extra challenge python scripts/verify_challenge_signatures.py \
    --require-identity 'https://github.com/<owner>/<repo>/.github/workflows/sign.yml@refs/heads/main' \
    --require-issuer https://token.actions.githubusercontent.com
```

## What the published record stores

The publish adapter (in progress; see #43/#49) copies each accepted
submission into `records/` through the attested workflow path and already
records the **merge SHA**. For signed submissions it additionally stores
the verifier's `thesis_challenge_signature_v1` block verbatim
(`verify_challenge_signatures.py --json`, or
`challenge_signing.signature_provenance_block()` from Python):

| Field | Meaning |
|---|---|
| `artifactPath`, `artifactSha256` | repo-relative submission path and its digest |
| `bundlePath`, `bundleMediaType` | the sidecar bundle the proof lives in |
| `rekorLogIndex`, `rekorLogIdKeyId` | transparency-log coordinates |
| `rekorEntryUuid` | RFC 6962 leaf hash of the entry's canonicalized body |
| `rekorIntegratedTimeUtc` | the independent public timestamp |
| `certificateSubjects`, `certificateOidcIssuer` | recorded signer identity |
| `identityPolicy` | `recorded_not_enforced` or `enforced` |
| `precedesRelease`, `releaseInstantUtc`, `releaseInstantSource` | the chronology verdict and what it was measured against |

Anyone can then re-verify independently: fetch the submission and bundle at
the merge SHA, `sigstore verify` the pair, and look the entry up at
`https://search.sigstore.dev/?logIndex=<rekorLogIndex>` (the entry UUID
equals `sha256(0x00 || canonicalizedBody)`; derivation cross-checked
against the live log 2026-07-31).

## How this composes with existing custody

Three independent proof legs, none sharing a trust root:

| Leg | Proves | Trust root |
|---|---|---|
| Git provenance (PR, merge SHA) | who submitted, what entered the repo | GitHub |
| Records chain (producer signature, workflow attestations, dual-TSA witnesses) | what Thesis published and when | code-pinned Ed25519 SPKI + RFC 3161 TSAs |
| Submitter signature (this doc) | the artifact existed, digest-exact, before the release — regardless of Thesis | Sigstore (Fulcio/Rekor) |

The v5 chronology tiers are unchanged: headline eligibility still comes
from the witnessed records chain. The Rekor timestamp is an additional,
platform-independent proof recorded on the challenge record; wiring it
into tier computation (e.g. as an alternative witness source for external
submissions) is future work and must be its own reviewed change.

## Rollout

- **Now**: optional. Unsigned submissions stay valid and attributed via
  the PR. PR #49 grandfathered.
- **Later** (any prize or ranked tier): required —
  `--require-signature` and `--require-prerelease` are the enforcement
  switches, to be wired into the intake gate when that tier exists.

First live-fire checklist (first signed submission): challenger signs with
the one-liner, PRs both files, maintainer runs the sweep before merge,
adapter embeds the provenance block, and the record's `rekorLogIndex` is
spot-checked on search.sigstore.dev.
