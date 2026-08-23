# GDM lane registration notes

Status: branch work complete; no roll, ticket, publication, push, PR, or
records/** write was performed.

## Outcome

None of the four proposed identities exists in the Chronicle series catalog
pinned by Thesis at cf0b3a7f0d9fda3c21939dac26d9104ca913896f. The frozen
catalog contains zero concept-or-alias matches for:

- nces.naep.g8_math_average_scale_score
- ncses.sei.publications_output.us_se_articles
- bls.oews.elementary_school_teachers_mean_annual_wage
- congress.appropriations.nsf_fy2027_enacted_full_year

That is a mechanical admission blocker, not a naming inconvenience. Every
docket row must carry a nonempty Chronicle UUID and concept and match a catalog
row by UUID (tests/test_docket_ledger_containment.py:224-260). Both the pinned
catalog and the current authoritative Chronicle catalog are CI gates
(tests/test_docket_ledger_containment.py:785-830). The stamper refuses a series
with no catalog row and copies, rather than invents, the catalog UUID
(scripts/stamp_docket_ledger_refs.py:310-355). Thesis resolution proposals are
also forbidden from minting or superseding Chronicle identities
(scripts/resolve_pending.py:10582-10592).

Therefore this branch does not edit scripts/docket_series.json. Doing so with a
fabricated UUID, or weakening the containment gate, would enroll an identity
that Chronicle has never admitted. Instead it lands four explicit ingestion
work items and the conditional-pair draft. This follows the repository rule
that ingestion requires history, witnessed first prints, a passable resolver,
verified anchors, and docket admission; unresolved requests stay visible
(AGENTS.md:292-312).

The requested adapters were not partially installed. Each new adapter requires
tests against saved real official response bytes, but curl could not resolve
the NCES, NCSES, BLS, or Congress hosts in this sandbox. The exploratory
directories contain target specifications and forecast results, not official
response custody fixtures. Their dataPointIds, metric definitions, and source
leads informed the drafts; none of their cells was copied.

## Production registration path

### Files a normal feature branch may edit

1. Chronicle must first admit a series in its own reviewed repository: seed
   history, immutable UUID-registry row, regenerated series_catalog.json, real
   official first-print custody, and anchors. Thesis deliberately cannot do
   this in resolve_pending.py (scripts/resolve_pending.py:10582-10592).

2. A later Thesis source branch may add the admitted identity to
   scripts/docket_series.json with its canonical ledger UUID/concept, explicit
   period or safe cadence, sourceBinding, release policy, value scale, unit,
   and release-calendar date or reviewed bound. The selector reads exactly
   that registry (scripts/roll_docket.py:46-49 and
   scripts/roll_docket.py:1118-1139).

3. Adapter/resolver code, non-record real-response fixtures, anchor
   verification, and tests also belong in the source branch. The registration
   contract fixes data-point identity, unit, scale, adapter, field/table,
   transform, release policy, and release window
   (docs/thesis-analyst-runner.md:12-18). The Python adapter allowlist is
   scripts/register_targets.py:54-71; the TypeScript mirror is
   site/src/data/ledger-targets.ts:6-27. Source bindings are derived and
   allowlisted at scripts/register_targets.py:646-750 and signed into the
   contract at scripts/register_targets.py:753-799.

4. Reviewed condition identities and exact matchStrings belong in
   site/src/data/conditions.ts (site/src/data/conditions.ts:13-49 and
   site/src/data/conditions.ts:62-129). Live reader-facing comparison entries
   belong in site/src/data/conditional-groups.ts only after every referenced
   cell exists. That registry already supports unconditionalSlug, gapNote, and
   nonExhaustivePair (site/src/data/conditional-groups.ts:3-20), while the
   catalog test requires every arm and baseline to resolve
   (site/src/__tests__/forecast-catalog.test.ts:2473-2485).

5. drafts/ledger-ingestion and other explicit draft files are the legitimate
   branch location for blocked proposals. They are not production registration
   and do not make a target eligible to roll (AGENTS.md:303-312).

### Files only allowlisted workflows write

1. The ordinary roll workflow selects targets using trusted repository code
   (.github/workflows/roll-docket.yml:101-147), invokes
   scripts/register_targets.py, and writes immutable registrations before any
   forecast runs (.github/workflows/roll-docket.yml:149-180).

2. scripts/register_targets.py writes canonical records/targets snapshots; its
   own contract says the privileged workflow commits and pushes those exact
   bytes before forecasting (scripts/register_targets.py:1-13).

3. The unprivileged analyst returns a data bundle. The publisher applies and
   validates it, then trusted scripts/register_wave.py rematerializes target
   registrations, converts validated cells, regenerates ledger targets, and
   wires forecast-cells.ts (scripts/register_wave.py:128-203;
   .github/workflows/roll-docket.yml:483-562).

4. The workflow alone commits records/thesis-analyst/** and generated site
   artifacts and attests the pushed commit
   (.github/workflows/roll-docket.yml:547-562 and
   .github/workflows/roll-docket.yml:655-659). The repository rule is
   categorical: records/** belongs to allowlisted workflows and records content
   does not land through PRs (AGENTS.md:357-402).

5. Updating the Chronicle pin is also stateful workflow work. pin_ledger.py
   writes records/ledger/availability.json, generated availability data, and
   ledger-pin.json together (scripts/pin_ledger.py:64-72 and
   scripts/pin_ledger.py:1393-1399); resolve-and-rebuild.yml performs that pin,
   custody verification, commit, push, and attestation
   (.github/workflows/resolve-and-rebuild.yml:96-165).

Consequently this branch does not edit records/**,
site/src/data/ledger-targets.generated.ts, generated auto forecast modules, or
forecast-cells.ts. The requested historical example
site/src/data/forecast-examples/s3596-conditionals-2026-07-31.ts is absent from
origin/main; it was inspected at historical commit be5b8944 instead.

## Series decisions

### NAEP grade-8 mathematics, 2026 and 2030

Draft: drafts/ledger-ingestion/nces-naep-g8-math-average-scale-score.json:1-81.

- Identity is the national NT, grade-8 mathematics MRPCM composite, TOTAL,
  MN:MN mean—not the NP public-school jurisdiction used in some exploratory
  material. The exact API query template is recorded at lines 9-12 and the
  binding dimensions at lines 22-38.
- Resolution retains the API decimal as evidence but scores the NCES published
  whole-number print using decimal round-half-up. Thus 273.83 resolves to 274;
  the rule and anchor are at lines 39-40 and 71-73.
- The official calendar gives seasons, not days: Winter 2026 assessment /
  estimated Winter 2027 release; 2028 / estimated Fall 2028; 2030 / estimated
  Fall 2030 (lines 41-45). The draft therefore uses reviewed
  resolve-by-bound windows, never invented release days (lines 47-69).
- The future docket must contain exactly the reviewed 2026 and 2030 one-shots
  (and the three-member 2030 comparison), not an annual cadence. It must not
  accidentally preregister 2027, 2029, or other non-assessment years
  (lines 74-79).

Official discovery/API references:

- https://www.nationsreportcard.gov/api_documentation.aspx
- https://nces.ed.gov/nationsreportcard/about/calendar.aspx
- https://www.nationsreportcard.gov/reports/mathematics/2024/g4_8/supporting-files/summary-of-results.pdf

### NCSES U.S. S&E articles, 2029

Draft: drafts/ledger-ingestion/ncses-sei-us-se-articles.json:1-69.

- Metric is U.S. articles in all S&E fields, fractionally counted by
  institutional address, in thousands. Figure 29 reports the 2024 raw count
  439,892, which resolves as 439.892; no integer-thousand rounding
  (lines 7-38 and 57-60).
- Resolution uses the first NCSES Indicators edition that actually reports
  publication year 2029, preserves its first print, and refuses a guessed
  future product slug or later revision (lines 8, 12, and 38).
- NCSES currently lists the next release as TBD. The 2031-cycle inference is
  plausible but is not an official release date. The draft records a broad
  2030-01-01 through 2032-12-31 lab bound and labels it as such
  (lines 39-54).

Official references:

- https://www.ncses.nsf.gov/pubs/nsbsep20261/figure/29
- https://ncses.nsf.gov/schedule-of-release-dates
- https://ncses.nsf.gov/indicators/reports

### BLS OEWS elementary-school-teacher mean annual wage, May 2027

Draft:
drafts/ledger-ingestion/bls-oews-elementary-school-teachers-mean-annual-wage.json:1-68.

- The requested current occupation page now redirects to the tables landing
  page. The clean source is the official May national bulk ZIP discovered from
  https://www.bls.gov/oes/tables.htm; require the national cross-industry row
  OCC_CODE 25-2021 and A_MEAN (lines 7-37).
- The sourceBinding remains generic-url, matching existing generic official URL
  registrations, while resolve_pending receives a dedicated OEWS parsing route
  that authenticates archive year, workbook member, scope, occupation, and
  field (lines 22-37 and 61-66).
- BLS has not posted a May 2027 release day. The January-June 2028 interval is
  an explicit conservative Thesis bound, not a cadence-derived agency promise
  (lines 38-53). Anchor candidates are at lines 56-59.

Official references:

- https://www.bls.gov/oes/tables.htm
- https://www.bls.gov/news.release/ocwage.htm
- https://www.bls.gov/schedule/news_release/ocwage.htm

### NSF FY2027 full-year enacted appropriation

Draft:
drafts/ledger-ingestion/congress-nsf-fy2027-enacted-full-year-appropriation.json:1-59.

CRS R48929 is the cleanest proposed machine-resolvable source: freeze the first
revision whose CJS table labels an aggregate National Science Foundation
FY2027 amount Enacted. Temporary CRs do not resolve it; once law supplies
authority through 2027-09-30, a full-year CR counts at the CRS annualized
aggregate (the specified comparator uses $8,750M). CRS scope governs
rescissions, transfers, balances, and scorekeeping, avoiding judgmental
recomputation from bill prose (lines 22-37).

It remains a policy-state draft. There is no real CRS revision fixture, only
one anchor candidate, no admitted Chronicle identity, and no safe future
expectedReleaseWindow start: full-year authority can become knowable at any
time. A null window cannot mint an attested ticket, and inventing one would
violate chronology (lines 38-57). Do not register the FY2027 target if the
answer becomes knowable before admission and preregistration; admit the
recurring identity for a later fiscal year instead.

Official references:

- https://www.congress.gov/crs-product/R48929
- https://nsf-gov-resources.nsf.gov/files/Budget%20Update.pdf

## Conditional pairs

The production-ready condition identities are in
site/src/data/conditions.ts:415-493:

- The teacher-pay conditions bind the exact H.R. 2021 and S. 2481 wording via
  matchStrings. The enacted arm uses the existing provision_enacted mechanism;
  the neither-enacted arm is its literal recorded-status complement over the
  same deadline (lines 415-457).
- The NSF thresholds use the existing recorded_status kind, so no new condition
  kind was needed. They are deliberately not complements: an enacted level
  strictly between $5,000M and $7,000M satisfies neither arm
  (lines 458-493).

The exact future baseline/arm slugs, dataPointIds, conditionIds, deadlines, and
gap notes are staged at drafts/gdm-lane-conditional-pairs.json:1-70. Both
comparisons explicitly name unconditionalSlug and explain that all three
forecasts are independently generated in one preregistration wave; the
differences are elicitation contrasts, not causal estimates. The S&E note also
marks the threshold pair non-exhaustive (lines 38-67).

The roller/registrar previously supported only two conditional arms. This
branch adds an optional exact unconditional object and treats baseline plus
arms as one comparison unit:

- emission, identity validation, and baseline-first ordering:
  scripts/roll_docket.py:589-788;
- atomic roll-cap and exclusion handling:
  scripts/roll_docket.py:1005-1088;
- ordinary-roll exclusion and bounded-ticket routing:
  scripts/roll_docket.py:1109-1171;
- byte-for-byte docket reauthentication:
  scripts/register_targets.py:1370-1617;
- all-member pruning if one target is unbindable:
  scripts/register_targets.py:2060-2136;
- exact-slug ticket selection cannot split a baseline from its arms:
  scripts/generation_tickets.py:985-1032;
- failed-run retry cannot split the comparison:
  scripts/retry_batch_targets.py:505-557.

Tests cover emission/malformed declarations
(tests/test_roll_docket.py:1317-1380), exact registration
(tests/test_register_targets.py:3753-3810), unbindable-member pruning
(tests/test_register_targets.py:4062-4101), ticket selection
(tests/test_generation_tickets.py:1171-1205), retry atomicity
(tests/test_retry_batch_targets.py:562-591), exact matchStrings and
non-complement thresholds (site/src/__tests__/conditions.test.ts:110-180).

No live entries were added to site/src/data/conditional-groups.ts because its
catalog gate requires cells that do not yet exist. Add those entries only
after publication, using unconditionalSlug for both groups, the staged gapNote,
and nonExhaustivePair: true only for the S&E funding thresholds.

## Implementation ledger

Commits, in order:

1. 4562a62a Document GDM registration trust boundary
2. 446505e2 Support unconditional conditional-comparison baselines
3. fbc8c564 Stage GDM series admissions and conditions

Files added:

- _LANE-NOTES.md — trust-boundary map, decisions, verification, and this
  operator runbook.
- drafts/ledger-ingestion/nces-naep-g8-math-average-scale-score.json:1-81
- drafts/ledger-ingestion/ncses-sei-us-se-articles.json:1-69
- drafts/ledger-ingestion/bls-oews-elementary-school-teachers-mean-annual-wage.json:1-68
- drafts/ledger-ingestion/congress-nsf-fy2027-enacted-full-year-appropriation.json:1-59
- drafts/gdm-lane-conditional-pairs.json:1-70

Files changed:

- scripts/roll_docket.py:589-788 and 1005-1171
- scripts/register_targets.py:1370-1617 and 2060-2136
- scripts/generation_tickets.py:985-1032
- scripts/retry_batch_targets.py:505-557
- site/src/data/conditions.ts:415-493
- tests/test_roll_docket.py:1266-1380
- tests/test_register_targets.py:3746-3810 and 4062-4101
- tests/test_generation_tickets.py:1171-1205
- tests/test_retry_batch_targets.py:434-591
- site/src/__tests__/conditions.test.ts:110-180

Intentionally untouched:

- scripts/docket_series.json
- scripts/resolve_pending.py and adapter fixtures
- site/src/data/conditional-groups.ts
- site/src/data/ledger-targets.generated.ts
- site/src/data/forecast-cells.ts and generated forecast modules
- records/**

## Verification

- Python ruff: clean for the four changed scripts and their four test modules.
- Focused Python suite: 364 passed in 117.69s.
- Focused site conditions suite: 26 passed in 26.78s.
- Prettier check: clean for the changed TypeScript files.
- Full site suite: 877 passed and 1 failed with the exact committed
  pinned-ledger bytes supplied locally because sandbox DNS cannot reach
  raw.githubusercontent.com. The one failure is pre-existing on origin/main:
  us-employment-cost-index-total-compensation-q3-2026 is a registered target
  with no forecast cell. origin/main contains the slug only in
  ledger-targets.generated.ts, and this branch does not change that file or the
  forecast catalog.
- Production build: Next 16 Turbopack could not bind an internal sandbox port
  (Operation not permitted). The webpack backend, using the same committed
  pinned-ledger bytes locally, compiled TypeScript, prerendered all 1,719 static
  pages, and completed successfully.
- All five draft JSON files pass jq parsing.
- git diff --check: passed after this final note update.

The first uv invocation could not use its default cache and a redirected cache
then attempted a dependency download that sandbox DNS blocked. The already
installed ruff, pytest, and Bun toolchain supplied the reported checks; no
dependency or lockfile was changed.

## Exact post-merge operator sequence

Nothing below was run on this branch.

### 1. Admit the identities in Chronicle

In the Chronicle repository, translate each draft's chronicleSeed into reviewed
series seed/history changes, mint the canonical immutable UUIDs, add real
official first-print custody, regenerate series_catalog.json, and merge only
after its tests pass. This is required for NAEP, NCSES, OEWS, and the recurring
NSF identity. FY2027 NSF target registration remains prohibited unless a safe
pre-answer window still exists.

### 2. Let the allowlisted Thesis workflow witness the new Chronicle catalog

After Chronicle admission is on the configured Chronicle branch:

    gh workflow run resolve-and-rebuild.yml --ref main

Wait for that workflow's pin/custody commit and records attestation to land on
Thesis main. Do not copy or locally commit its records output.

### 3. Land a follow-up Thesis admission branch

From the freshly pinned Thesis main, fetch the exact pinned catalog:

    set -euo pipefail
    PIN_SHA=$(jq -r .sha site/src/data/ledger-pin.json)
    curl -fL --retry 3 -A 'thesis-catalog-freeze/1.0' \
      "https://raw.githubusercontent.com/PolicyEngine/chronicle/$PIN_SHA/ledger/series_catalog.json" \
      -o tests/fixtures/ledger_series_catalog.json

Then, in coherent reviewed commits:

1. Fetch the real official response fixtures named in each draft; implement the
   NAEP, NCSES, OEWS, and—if still viable—CRS resolvers and parser tests.
2. Verify at least three historical first-print anchors per admitted identity
   and update docs/anchor-verifications.md.
3. Translate only now-passable drafts into scripts/docket_series.json. Use
   explicit one-shot periods/bounds: NAEP 2026 and 2030 only; NCSES 2029 only;
   OEWS May 2027 only. Include the staged unconditional-plus-two-arm declarations
   for NAEP 2030 and NCSES 2029.
4. Stamp canonical Chronicle identities, never hand-type UUIDs:

       python3 scripts/stamp_docket_ledger_refs.py \
         --catalog tests/fixtures/ledger_series_catalog.json \
         --docket scripts/docket_series.json

5. Run containment, resolver, roll, registration, ticket, site, and build tests;
   merge the source branch without any records/** files.

### 4. Register and mint the bounded targets

There is no ordinary roll-docket dispatch for the current drafts.
resolve-by-bound rows are explicitly skipped by ordinary roll
(scripts/roll_docket.py:1109-1114 and 1142-1151). The ticket workflow is the
registration lane: it calls roll_docket.py --include-bounded, selects an exact
series, creates missing immutable registrations, pushes and attests them, then
mints the ticket (.github/workflows/mint-generation-ticket.yml:1-5 and
.github/workflows/mint-generation-ticket.yml:75-170).

After the follow-up docket branch is merged, dispatch:

    gh workflow run mint-generation-ticket.yml --ref main \
      -f series=nces.naep.g8_math_average_scale_score \
      -f prompt_mode=fast \
      -f codex_model=gpt-5.5 \
      -f codex_reasoning_effort=high \
      -f codex_network=true \
      -f attempt=1

    gh workflow run mint-generation-ticket.yml --ref main \
      -f series=ncses.sei.publications_output.us_se_articles \
      -f prompt_mode=fast \
      -f codex_model=gpt-5.5 \
      -f codex_reasoning_effort=high \
      -f codex_network=true \
      -f attempt=1

    gh workflow run mint-generation-ticket.yml --ref main \
      -f series=bls.oews.elementary_school_teachers_mean_annual_wage \
      -f prompt_mode=fast \
      -f codex_model=gpt-5.5 \
      -f codex_reasoning_effort=high \
      -f codex_network=true \
      -f attempt=1

Selecting the NAEP series includes its due 2026 target and the atomic 2030
baseline/arms; selecting NCSES includes its 2029 baseline/arms. Exact-slug
selection is also safe, but all three comparison slugs must be supplied
together. Do not dispatch NSF FY2027 unless the final admitted row has a
non-null authenticated future window and the policy answer is still unknown.

If an agency publishes a specific official release day before registration,
replace that target's draft bound with release-calendar review metadata and
use the ordinary workflow instead:

    gh workflow run roll-docket.yml --ref main \
      -f series=EXACT_DOCKET_SERIES \
      -f max_targets=3

Never dispatch both lanes for the same target.

### 5. Generate and publish each minted ticket

After each mint workflow commits its ticket, use the exact ticket path printed
by the workflow:

    set -euo pipefail
    git fetch origin main
    TICKET_PATH='records/tickets/YYYY-MM-DD/YYYY-MM-DD-LOWERCASE_HEX.json'
    TICKET_COMMIT=$(git log --full-history --diff-filter=A --format=%H \
      origin/main -- "$TICKET_PATH")
    RUN_ROOT=$(mktemp -d)
    git worktree add --detach "$RUN_ROOT/checkout" "$TICKET_COMMIT"
    cd "$RUN_ROOT/checkout"

    WORK_DIR=$(mktemp -d)
    uv run python scripts/run_thesis_batch.py --ticket "$TICKET_PATH" \
      | tee "$WORK_DIR/run.log"
    BATCH_ABS=$(sed -n 's/^batch manifest: //p' "$WORK_DIR/run.log")
    test -n "$BATCH_ABS" && test -f "$BATCH_ABS"
    BATCH_PATH=$(BATCH_ABS="$BATCH_ABS" uv run python - <<'PY'
    import os
    import pathlib

    root = pathlib.Path.cwd().resolve()
    batch = pathlib.Path(os.environ["BATCH_ABS"]).resolve()
    try:
        print(batch.relative_to(root).as_posix())
    except ValueError as exc:
        raise SystemExit(f"batch manifest is outside checkout: {batch}") from exc
    PY
    )
    jq '{targets: .targets}' "$TICKET_PATH" > "$WORK_DIR/trusted-targets.json"
    uv run python scripts/docket_publication.py stage \
      --bundle-dir "$WORK_DIR/bundle" \
      --batch "$BATCH_PATH" \
      --trusted-targets "$WORK_DIR/trusted-targets.json"

Package only the staged bundle into an orphan transport commit:

    set -euo pipefail
    TICKET_ID=$(jq -r .ticketId "$TICKET_PATH")
    tar -C "$WORK_DIR/bundle" -cf "$WORK_DIR/bundle.tar" \
      bundle_manifest.json repo
    zstd -q -f "$WORK_DIR/bundle.tar" -o "$WORK_DIR/bundle.tar.zst"
    shasum -a 256 "$WORK_DIR/bundle.tar.zst" \
      | awk '{print $1 "  bundle.tar.zst"}' > "$WORK_DIR/bundle.sha256"
    HASH_BLOB=$(git hash-object -w "$WORK_DIR/bundle.sha256")
    TAR_BLOB=$(git hash-object -w "$WORK_DIR/bundle.tar.zst")
    TREE_SHA=$(printf '100644 blob %s\tbundle.sha256\n100644 blob %s\tbundle.tar.zst\n' \
      "$HASH_BLOB" "$TAR_BLOB" | git mktree)
    BUNDLE_SHA=$(printf 'Attested generation bundle %s\n' "$TICKET_ID" \
      | git commit-tree "$TREE_SHA")
    git push origin "$BUNDLE_SHA:refs/heads/attested/$TICKET_ID"

    gh workflow run publish-attested.yml --ref main \
      -f ticket_path="$TICKET_PATH" \
      -f bundle_sha="$BUNDLE_SHA"

This transport push contains only bundle.tar.zst and bundle.sha256; the
allowlisted publisher reconstructs, validates, commits, and attests records and
generated site data. The authoritative procedure is AGENTS.md:116-193.

### 6. Add reader-facing groups after cells publish

Once all referenced baseline and arm cells are live, add the two
CONDITIONAL_GROUPS entries in a normal source branch. Copy the exact staged
slugs and gap notes, set unconditionalSlug on both, and set
nonExhaustivePair: true only on the S&E group. Then run the full site test and
build. This last source commit exposes the baseline-versus-arm gaps without
rewriting generated cells.
