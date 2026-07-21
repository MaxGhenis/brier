# Producer signing progress

## State

Discovery and impact analysis are in progress. The branch is still in the
dormant, behavior-preserving state; no producer-signing code or records have
been changed yet.

## Done

- Read the repository conventions and the record-chain, witness, recorder,
  custody, provenance-test, and recorder-workflow surfaces in the required
  order.
- Confirmed that recorder custody closes over each snapshot's body directory,
  while snapshot-sibling completeness belongs in the record-chain verifier.
- Confirmed that `receipt` is not currently installed or locked in this
  checkout and that the main dependency list is empty.

## Next

- Finish dependency/CI and `receipt.sign` API inspection.
- Add dormant pins and fail-closed verifier integration with exact-message
  tests.
- Add the idempotent proposer CLI and tests.
- Add the optional dependency lock, workflow step, and ceremony runbook.
- Run Black, Ruff, targeted tests, and the full pytest suite; perform the
  dormant-path and orphan-file self-audit; write the final report.
