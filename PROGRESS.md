# Producer signing progress

## State

The verifier and proposer are implemented and covered by targeted tests.
Producer signing remains dormant: both activation constants are `None`, the
live records tree is unchanged, and neither dormant command path imports
`receipt`.

## Done

- Read the repository conventions and the record-chain, witness, recorder,
  custody, provenance-test, and recorder-workflow surfaces in the required
  order.
- Confirmed that recorder custody closes over each snapshot's body directory,
  while snapshot-sibling completeness belongs in the record-chain verifier.
- Confirmed that `receipt` is not currently installed or locked in this
  checkout and that the main dependency list is empty.
- Audited the chain-verifier call graph and custody scopes. Snapshot signature
  siblings are owned by the record-chain verifier, not run-body custody.
- Added the frozen producer-signing policy constants and half-armed refusal.
- Added chain-order-aware verification for the activation boundary, public-key
  SPKI pin, exact snapshot bytes, 64-byte raw signatures, symlink checks, and
  global orphan/stray signature detection.
- Added exact-message verifier tests for dormant, half-armed, active-valid,
  missing, malformed, wrong-key, bit-flipped, symlinked, boundary, orphan, and
  missing-package states.
- Added the proposer CLI with private-key/SPKI self-check, domain-separated
  signing, optional target selection, exclusive writes, invalid-signature
  refusal, idempotence, and environment cleanup.
- Closed a discovered symlinked-date-directory escape in both verifier and
  proposer; neither now accepts a snapshot nor writes a signature through a
  symlinked path component.
- Ran the 30 producer-signing tests against the cached byte-identical
  `receipt==0.2.0` package: 30 passed.

## Next

- Add the optional dependency lock, workflow step, and ceremony runbook.
- Run Black, Ruff, targeted tests, and the full pytest suite; perform the
  dormant-path and orphan-file self-audit; write the final report.
