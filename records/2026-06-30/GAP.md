# No snapshot for 2026-06-30

The daily recorder failed this day (run 28454791399, exit 22): the app
deployment of 2026-06-30 ("Build clean target architecture for Thesis",
fb525fc on codex/baseline-discipline-pack) retired `/specs.json` in favor of
`/targets.json`, and the workflow still fetched the old surface. No snapshot
of the published surfaces was captured, so there is no independent
timestamped record of what the site served this day.

Note this was also the resolution date for the FY2025 SNAP payment error
rate cells (USDA FNS QC release). The resolution events themselves appear in
`/log.json` with their own timestamps and are captured in the next
successful snapshot; only this day's external anchor is missing.

Recorded honestly rather than backfilled — a gap in the chain is a gap.
