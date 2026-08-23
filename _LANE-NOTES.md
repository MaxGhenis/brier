# GDM lane registration notes

Status: branch work only. This file is the required first deliverable and will
be expanded with the implemented series, verification, and post-merge operator
commands before the branch is complete.

## Production registration path

The committed docket is the reviewed source of target templates. The roller
loads `scripts/docket_series.json` (`scripts/roll_docket.py:46-49` and
`scripts/roll_docket.py:1072-1095`), derives eligible target specs, and preserves
a conditional unit atomically under the roll cap (`scripts/roll_docket.py:960-983`).
Therefore a feature branch may legitimately edit:

- `scripts/docket_series.json`: series identity, cadence/explicit periods,
  source binding, release policy/window, and conditional declarations that the
  production roller is meant to consume.
- `scripts/roll_docket.py` and `scripts/register_targets.py`: reviewed target
  selection and contract validation. Registration fixes the adapter, official
  source, field/table, transform, release policy, and release window
  (`docs/thesis-analyst-runner.md:12-18`); its supported adapter allowlist lives
  at `scripts/register_targets.py:54-71`.
- `scripts/resolve_pending.py`, parser modules, non-record fixtures, and tests:
  resolver code turns an official first print into a Ledger fact
  (`scripts/resolve_pending.py:1-8`). A new source family must be implemented and
  fixture-tested here before docket admission, rather than left for the roll to
  interpret.
- `site/src/data/ledger-targets.ts`: the TypeScript adapter union deliberately
  mirrors the Python allowlist (`site/src/data/ledger-targets.ts:6-27`).
- `site/src/data/conditions.ts` and its tests: reviewed condition identities,
  exact forecast-text aliases, complements, deadlines, and evidence evaluation
  are ordinary source inputs (`site/src/data/conditions.ts:13-49` and
  `site/src/data/conditions.ts:62-129`).
- `site/src/data/conditional-groups.ts` only after its referenced forecast cells
  have been published. The registry supports `unconditionalSlug`
  (`site/src/data/conditional-groups.ts:3-20`), but the catalog test requires
  every live group and named baseline to resolve (`site/src/__tests__/forecast-catalog.test.ts:2473-2485`).
  Pre-roll group metadata must therefore remain an explicitly non-live draft or
  be added in a post-publication source commit.
- `drafts/ledger-ingestion/` when a proposed metric still lacks a passable
  resolver. Such a request is visible work, not docket admission
  (`AGENTS.md:292-312`).

The allowlisted roll workflow, not this feature branch, owns the stateful
registration and publication outputs:

1. It runs the trusted selector over the committed docket
   (`.github/workflows/roll-docket.yml:101-147`).
2. `scripts/register_targets.py` writes immutable canonical snapshots under
   `records/targets/` before forecasting; its contract explicitly assigns the
   commit/push to the privileged workflow (`scripts/register_targets.py:1-13`).
   The workflow creates and commits those registrations
   (`.github/workflows/roll-docket.yml:149-180`).
3. The unprivileged analyst produces a data bundle. The publisher validates and
   applies that bundle (`.github/workflows/roll-docket.yml:483-505`); no cell from
   the exploratory GDM runs is copied into site source.
4. Trusted `scripts/register_wave.py` rematerializes registrations, generates
   the auto forecast module, finalizes `ledger-targets.generated.ts`, and wires
   the module into `forecast-cells.ts` (`scripts/register_wave.py:128-181` and
   `scripts/register_wave.py:184-203`). The workflow invokes it and runs the site
   suite (`.github/workflows/roll-docket.yml:516-545`).
5. Only the workflow commits `records/thesis-analyst/**` and generated site data,
   pushes, and attests the result (`.github/workflows/roll-docket.yml:547-562`
   and `.github/workflows/roll-docket.yml:655-659`). The repository rule is
   categorical: `records/**` belongs to allowlisted workflows and records
   content never lands through PRs (`AGENTS.md:357-370` and
   `AGENTS.md:386-402`).

Consequently this branch will not edit `records/**`,
`site/src/data/ledger-targets.generated.ts`, any generated
`site/src/data/forecast-examples/auto-*.ts` module, or generated forecast-cell
wiring. It will provide reviewed registrations/resolvers/conditions and tests;
the workflow will mint preregistration snapshots and publish newly generated
cells after merge.

## Conditional baseline constraint found during path audit

The requested reader-facing pattern needs three forecasts as one information
set: an unconditional baseline plus two independently generated conditional
arms. The current roller understands exactly two arms
(`scripts/roll_docket.py:589-607` and `scripts/roll_docket.py:664-666`), while
registration rejects an unconditional target when the same docket template has
a matching conditional pair (`scripts/register_targets.py:1376-1413`). A
separate baseline entry with the same series and period is not a safe escape,
because matching is by committed series/period template
(`scripts/register_targets.py:1110-1135`).

The production-safe change is therefore a minimal three-member conditional
unit: one explicitly declared unconditional member and two arms, all selected
atomically. That keeps the baseline from being generated in a different wave
with a different information set. The implementation and ticket-selection
implications will be recorded here after tests establish the final contract.

## Implementation ledger

To be completed as coherent commits land.

## Post-merge operator sequence

To be completed only after the admitted/draft boundary and exact series names
are final. No command in this section will be run from this branch.
