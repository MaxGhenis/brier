# Late snapshot for 2026-07-01

The scheduled 14:17 UTC run failed (run 28527903767, exit 22) for the same
reason as [2026-06-30](../2026-06-30/GAP.md): the recorder still fetched the
retired `/specs.json` surface. The workflow was fixed the same day (e8d3917
— surfaces now `log`, `ledger`, `targets`, `reward`, plus a failure alert)
and this directory's snapshot was captured by a manual dispatch at ~22:40
UTC instead of the usual 14:17 UTC. The day is anchored; only the capture
time differs.
