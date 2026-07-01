# No snapshot for 2026-07-01

Same cause as [2026-06-30](../2026-06-30/GAP.md): the recorder still fetched
the retired `/specs.json` surface (run 28527903767, exit 22). Fixed
2026-07-02 UTC by pointing the workflow at the surfaces the app actually
serves (`log`, `ledger`, `targets`, `reward`) and adding a failure alert so
a broken run files an issue the same day.
