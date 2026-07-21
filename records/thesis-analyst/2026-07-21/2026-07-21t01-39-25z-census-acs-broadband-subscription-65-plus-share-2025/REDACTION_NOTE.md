# Redaction note — 2026-07-21

During this run's draft phase, the agent executed `env | rg -i 'CENSUS|API|KEY'`
while scouting for a Census API key. The command output — 18 credential
environment variables from the launching shell — was captured verbatim into
`draft_codex_events.jsonl` / `draft_codex_stdout.jsonl`, and the final-phase
agent's `sed` read of the draft trace propagated it into
`codex_events.jsonl` / `codex_stdout.jsonl`. GitHub push protection blocked the
first push of these records; no secret reached the public repository.

The four trace files were redacted in place (76 replacements, `[REDACTED]`
markers) before any successful push. Because redaction changes artifact
hashes, this run's `custody_root.json` no longer matched and was removed:
**this run is deliberately unattested** and is excluded from recorder
artifact commitments. The published catalog cell for
`broadband-subscription-65-plus-2025` was regenerated from a clean
replacement run executed under a sanitized environment with the identical
resolution contract (same dataPointId, resolution date, source, and rule);
see `records/thesis-analyst/batches/2026-07-21-broadband-rerun-*.json`.

Pipeline hardening (environment allowlist for agent subprocesses and
credential redaction before records are written) is tracked separately.
