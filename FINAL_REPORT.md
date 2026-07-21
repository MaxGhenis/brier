# Producer signing final report

## Result

Producer-signature support is complete and dormant on branch
`producer-signing`. No key, public-key file, activation boundary, record, or
signature was added. The branch was not pushed.

The implementation uses `receipt==0.2.0` for Ed25519 signatures over the exact
snapshot bytes with Brier's `thesis-record-snapshot/v1\0` domain prefix. It
fails closed on half-armed pins, stray/orphan signatures, boundary violations,
missing or non-regular files, invalid signatures, a wrong SPKI pin, and a
missing active dependency.

## Delivered

- Frozen dormant policy constants in `scripts/producer_signing_pins.py`.
- Chain-order-aware verification in `scripts/verify_record_chain.py`, including
  global signature-sibling completeness and symlink-component containment.
- An idempotent proposer in `scripts/sign_record_snapshot.py` with private-key
  self-check, environment removal, invalid-signature refusal, and exclusive
  writes.
- A `custody` optional dependency; main `dependencies = []` remains unchanged.
  The generated lock contains the exact supplied wheel and sdist hashes.
- One recorder-workflow signing step between snapshot creation and RFC 3161
  witnessing, with the private key exposed only to that step.
- A ceremony runbook and 32 focused producer-signing tests.

## Verification

The final code passed:

```text
black --check: 4 files unchanged
ruff check: all checks passed
uv lock --offline --check: resolved 82 packages
git diff --check: clean
receipt package under test: 0.2.0
```

Full-suite tail:

```text
......................................................                   [100%]
702 passed in 451.58s (0:07:31)
```

Pytest emitted unrelated temporary-directory cleanup warnings after the green
summary; there were no test failures.

## Commits

```text
df53f5b6 Track producer signing implementation progress
7c131d52 Verify producer-signed record snapshots
4332f03b Add fail-closed record snapshot signer
c38467df Pin receipt for custody signing
1acd3317 Wire dormant snapshot signing into recorder
d5533d89 Document producer signing ceremony
1aef13c5 Harden signing secret handling
```

## Self-audit

- Dormant behavior remains receipt-free and the live records tree verifies.
  Intentional differences from `origin/main` are a global refusal of any
  `.producer.sig`, a loud half-armed-pin refusal, and rejection of snapshots
  reached through symlinked path components.
- Snapshot signature siblings are owned globally by the record-chain verifier:
  dormant signatures refuse, active pre-boundary and orphan signatures refuse,
  and every post-boundary snapshot requires exactly one valid sibling. Run/body
  custody inventories do not treat these day-directory siblings as orphans.
- `records/**`, `CHAIN_GENESIS.json`, docket/publication/resolution code, and
  every workflow except the requested recorder signing step are unchanged.
- Deliberately excluded: key generation, the public key, real pins, and
  signatures belong to the later human ceremony. Activation also requires the
  documented Python 3.11+/custody setup for every raw verifier workflow and an
  allowlisted attested path for the public-key records commit. Those changes
  were outside this branch's workflow constraint.
- V1 has a single key epoch, so rotation cannot overwrite the pin without
  invalidating history. The runbook requires an epoch-preserving verifier
  migration before a new reviewed rotation ceremony.
