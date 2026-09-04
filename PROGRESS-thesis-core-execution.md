# Progress: thesis core execution + shared security

Owner: execution lane — `thesis_core/security.py`, `thesis_core/execution.py`,
the narrow security extraction in `scripts/run_thesis_analyst.py`,
`tests/thesis_core/test_execution.py` and `tests/thesis_core/test_security.py`.

Lane-scoped rather than a shared `PROGRESS.md` so the concurrent
contracts/store/adapters/publication/site owners do not collide on one file.

## State

Both owned modules are implemented, tested and committed. The lane is green
against a real PostgreSQL cluster and the legacy runner suite.

## Done

- `thesis_core/security.py` (stdlib only): the moved allowlisted subprocess
  environment and redaction helpers, plus key-aware redaction, `redact_url`,
  `redact_headers`, `redact_value` and `is_credential_key`.
- `scripts/run_thesis_analyst.py` re-exports every moved name and bootstraps
  the checkout root, so direct absolute-path invocation still works with no
  PYTHONPATH, no editable install and no core extra (verified under system
  Python 3.9 from another working directory).
- `thesis_core/execution.py`: `execute_forecast`, the persistence baseline
  (`persistence_distribution`), the prompt builder (`build_prompt`), the
  operator_subprocess transport, and the cohort-proof dispatch gate.
- `tests/thesis_core/test_security.py` (81 cases) and
  `tests/thesis_core/test_execution.py` (49 cases, real subprocesses + real
  PostgreSQL).

## API published to the other lanes

- Adapters/evidence: `redact_url(url, *, credential_params=())`,
  `redact_headers(headers, *, credential_headers=(), safe_headers=(),
  drop_unlisted=True)`, `redact_value(value, *, credential_keys=())`. Apply
  before canonicalization and hashing; clean input is byte-identical.
  Never route opaque binary evidence (RFC 3161 DER, signatures, archived
  bodies) through them.
- Publication/worker: `verify_cohort_proof(*, experiment_id, cohort_proof_id,
  task_id) -> str` returns the verified token's SHA-256 hex; any exception
  refuses dispatch; a boolean is rejected. Already wired in `worker.py` via
  `publication.verify_cohort_for_dispatch`.
- Root/CLI: a `baseline` forecaster must pin
  `execution.PERSISTENCE_BASELINE_VERSION` in `agent_version` or
  `inference_settings["baseline_version"]`; an `operator_subprocess`
  forecaster must register `inference_settings["argv"]`.

## Next

- Nothing outstanding in this lane. Open to review findings from root's
  independent code review.
