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
   Fulcio, certificate transparency SCT, the Merkle inclusion proof
   against the log's signed checkpoint, the Signed Entry Timestamp, and
   the signature over the submission's exact bytes.
2. **Digest match** — the bundle's `messageDigest` equals the file's
   sha256, reported as `artifactSha256`. A bundle made for different bytes
   is refused outright.
3. **An authenticated time source is REQUIRED.** Chronology values are
   read back from the *cryptographically verified* transparency-log
   entry, never from the bundle's advertised JSON, and the entry must
   carry a Signed Entry Timestamp binding a nonzero `integratedTime` —
   sigstore accepts v0.2+ bundles with no inclusion promise when an
   RFC 3161 timestamp is present, and skips SET verification for a zero
   `integratedTime`, so both cases are refused here (a bundle whose
   `integratedTime` is not SET-bound has no authenticated Rekor
   chronology; TSA-time support would be a separate, explicitly labeled
   extension). The advertised bundle metadata must equal the verified
   entry exactly or the bundle is refused.
4. **Chronology** — the SET-bound `integratedTime` must *strictly
   precede* the target's release instant. By default that instant is
   derived conservatively from the registered target: the earlier of
   `resolutionDate` and `sourceBinding.expectedReleaseWindow.start`,
   floored to 00:00:00 UTC of that day (day-granularity fields prove
   nothing about intraday order, so the signature must beat the day's
   first instant). At scoring time, pass the actual first-print instant
   with `--release-at` for the exact comparison.

Unsigned submissions are listed and remain schema-checked-valid (full
intake validation happens at publication). A present-but-invalid bundle
always fails the sweep — the sweep always covers the whole inbox, even
when `--submission` narrows the export — a broken proof is tampering
evidence, not a missing option. Orphan bundles (no matching submission),
symlinks, and any file not shaped `<login>/<cell>.json` fail it too. In
`--json` mode stdout carries exactly one JSON document (diagnostics on
stderr), and `--staging` (rehearsals) refuses `--json` so staging proof
can never feed the adapter. A successful default exit does **not** mean
every signature precedes its release — publishers read `precedesRelease`
per block, or gate with `--require-prerelease`.

### Identity is recorded, not enforced (by default)

A keyless certificate from the interactive flow names the GitHub-verified
**email** the challenger logged in with; there is no mechanical mapping
from that email to the `challenger: github:<login>` field. **The
signature therefore never authenticates the `challenger` account** — it
proves that the recorded certificate principal signed these exact bytes,
nothing more. Account attribution is a separate leg that the publish
adapter MUST enforce mechanically (tracked in #71 as a follow-up to the
#69 adapter): `challenger` must equal `github:<PR opener>`, the inbox
path's `<login>/` directory must match, and the published record must
persist the PR number, opener, and merge SHA. Until #71 lands, that
binding is covered by the human review every inbox PR gets before merge.
The verifier records the certificate's subjects and OIDC issuer verbatim
(`identityPolicy: recorded_not_enforced`) and refuses a certificate with
no subject at all.

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

The publish adapter (`scripts/ingest_challenge_submissions.py`, landed in
#69; it already skips `*.sigstore.json` sidecars during discovery) copies
each accepted submission into `records/` through the attested workflow
path and records the **merge commit**. Wiring it to store the verifier's
`thesis_challenge_signature_v1` block verbatim for signed submissions
(`verify_challenge_signatures.py --json`, or
`challenge_signing.signature_provenance_block()` from Python) is the
integration step that follows this PR, alongside the opener-identity
enforcement tracked in #71:

| Field | Meaning |
|---|---|
| `artifactPath`, `artifactSha256` | repo-relative submission path and its digest |
| `bundlePath`, `bundleMediaType` | the sidecar bundle the proof lives in |
| `rekorLogIndex`, `rekorLogIdKeyId` | transparency-log coordinates, read from the verified entry |
| `rekorEntryUuid` | RFC 6962 leaf hash of the verified entry's canonicalized body |
| `rekorIntegratedTimeUtc`, `rekorIntegratedTimeSource` | the independent public timestamp and its authentication (`signed_entry_timestamp`) |
| `sigstoreEnvironment` | `production` (staging bundles are never exported) |
| `certificateSubjects`, `certificateOidcIssuer` | recorded signer identity — NOT the challenger account (see above) |
| `identityPolicy` | `recorded_not_enforced` or `enforced` |
| `precedesRelease`, `releaseInstantUtc`, `releaseInstantSource` | the chronology verdict and what it was measured against |

Anyone can then re-verify independently: fetch the submission and bundle at
the merge SHA, `sigstore verify` the pair, and look the entry up at
`https://search.sigstore.dev/?logIndex=<rekorLogIndex>` (the entry UUID
equals `sha256(0x00 || canonicalizedBody)`; derivation cross-checked
against the live log 2026-07-31).

## How this composes with existing custody

Three proof legs with partially overlapping trust domains — overlaps
stated plainly rather than claimed away:

| Leg | Proves | Trust domain |
|---|---|---|
| Git provenance (PR, merge SHA) | who submitted, what entered the repo | GitHub |
| Records chain (producer signature, workflow attestations, dual-TSA witnesses) | what Thesis published and when | code-pinned Ed25519 SPKI + RFC 3161 TSAs; the workflow-attestation half also rests on GitHub (Actions identity) and Sigstore (Fulcio) infrastructure |
| Submitter signature (this doc) | the artifact existed, digest-exact, before the release — regardless of Thesis | Sigstore (Fulcio/Rekor) |

The producer Ed25519 key and the RFC 3161 witnesses are the separately
rooted parts; submitter signatures and records-push attestations both
lean on Sigstore infrastructure, and Git provenance shares GitHub with
the Actions identities. A Sigstore compromise would therefore degrade
two legs at once — the producer signature and TSA witnesses are the
custody that survives it.

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
