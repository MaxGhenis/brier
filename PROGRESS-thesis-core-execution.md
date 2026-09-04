# Progress: thesis core execution + shared security

Owner: execution lane (`thesis_core/security.py`, `thesis_core/execution.py`,
the narrow security extraction in `scripts/run_thesis_analyst.py`,
`tests/thesis_core/test_execution.py`, `tests/thesis_core/test_security.py`).

This file is deliberately lane-scoped rather than a shared `PROGRESS.md` so the
concurrent contracts/store/adapters/publication owners do not collide on one
file.

## State

Starting. Plan (`docs/thesis-core-plan.md`) and architecture read; the
contracts (`thesis_core/contracts.py`) and store (`thesis_core/store.py`)
modules that `execution.py` depends on do not exist in the worktree yet, so
security lands first and execution is written against the agreed interface and
re-checked against the real files as they appear.

## Done

- Read `AGENTS.md`, `docs/thesis-core-plan.md`,
  `docs/thesis-core-architecture.md`, `docs/thesis-core-plan-review-response.md`.
- Inventoried the credential-hygiene block in `scripts/run_thesis_analyst.py`
  (lines 1325-1457) and its only two consumers: the runner itself and
  `tests/test_thesis_analyst_env_hygiene.py`.

## Next

1. `thesis_core/security.py` (stdlib only) + runner re-export + hygiene tests.
2. `thesis_core/execution.py`: prompt assembly, persistence baseline,
   subprocess transport, lease/heartbeat, sealed run.
3. `tests/thesis_core/test_execution.py` against the real `core_store`
   PostgreSQL fixture.
