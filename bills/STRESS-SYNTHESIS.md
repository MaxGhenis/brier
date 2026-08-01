# Overnight stress test — synthesis (2026-08-01, cycles 1-9)

Max's directive: "keep going through the night - apply it to more bills of random types to stress test it."

**Method.** Random sampling of 119th-Congress bills via direct govinfo XML probing (types hr/s/hjres/sjres, versions ih/is/eh/etc.; 3 constitutional amendments also landed in the net), one deliberate mega-bill (H.R.1 engrossed), extraction by offline gpt-5.6-sol lanes in detached worktrees against the frozen contract (exemplar: farm-bill-2-0.json), integrator validation of every artifact (JSON parses, stance indexes in range, series_hints verified against scripts/docket_series.json). Artifacts accumulate on `hack/stress-bills` (NEVER merged); full per-bill notes in FINDINGS.md.

**Honesty ground rules held all night:** zero invented series_hints (the only 3 hints emitted — SNAP + two USAspending DoD series on H.R.1 — are all registered); zero stance-index errors; refusals and coverage limits recorded verbatim.

## Coverage

| bill | chars | provisions | metrics | hints | name |
|---|---:|---:|---:|---:|---|
| 119hr1eh | 999,294 | 13 | 36 | 3 | One Big Beautiful Bill Act (H.R. 1, House-engrossed text) |
| 119hr608ih | 15,470 | 3 | 9 | 0 | Cover Outstanding Vulnerable Expansion-eligible Residents No |
| 119hr5595ih | 8,155 | 1 | 3 | 0 | Requiring Excise for Migrant Income Transfers Act (REMIT Act |
| 119s1082is | 7,304 | 3 | 8 | 0 | Safeguarding Medicaid Act (S. 1082) |
| 119hr1811ih | 6,804 | 2 | 0 | 0 | Judicial Ethics Enforcement Act of 2025 (H.R. 1811) |
| 119s2718is | 5,909 | 1 | 3 | 0 | S. 2718 — To amend the Community Development Banking and Fin |
| 119hr978ih | 4,354 | 3 | 7 | 0 | Superior National Forest Restoration Act of 2025 (H.R. 978) |
| 119s767is | 4,225 | 3 | 7 | 0 | HIDTA Enhancement Act (S. 767) |
| 119hr2449ih | 4,203 | 1 | 2 | 0 | Future Uses of Technology Upholding Reliable and Enhanced Ne |
| 119s2075is | 3,304 | 1 | 3 | 0 | Future Long Range Assault Aircraft Medical Evacuation and Sp |
| 119hr8058ih | 3,145 | 1 | 0 | 0 | United States Secret Service Reserve Fund Act of 2026 (H.R.  |
| 119hr1021ih | 2,995 | 3 | 8 | 0 | Small Business Disaster Damage Fairness Act of 2025 (H.R. 10 |
| 119sjres56is | 2,921 | 1 | 0 | 0 | Life Month Resolution (S.J. Res. 56) |
| 119hjres122ih | 2,865 | 1 | 0 | 0 | Proposing an amendment to the Constitution of the United Sta |
| 119s1188is | 2,781 | 1 | 2 | 0 | Facilitating Lower Atmospheric Released Emissions Act (FLARE |
| 119hr80ih | 2,662 | 1 | 0 | 0 | Drain the Intelligence Community Swamp Act of 2025 (H.R. 80) |
| 119sjres48is | 1,824 | 1 | 0 | 0 | A joint resolution proposing an amendment to the Constitutio |
| 119hjres78ih | 1,524 | 1 | 0 | 0 | A joint resolution providing for congressional disapproval u |
| 119hjres42ih | 1,463 | 1 | 0 | 0 | A joint resolution providing for congressional disapproval u |
| 119hjres29ih | 1,452 | 1 | 0 | 0 | Proposing an amendment to the Constitution of the United Sta |
| 119sjres74is | 1,344 | 1 | 0 | 0 | A joint resolution providing for congressional disapproval u |
| 119hjres79ih | 1,324 | 1 | 0 | 0 | Providing for congressional disapproval under chapter 8 of t |
| 119sjres73is | 1,233 | 1 | 0 | 0 | A joint resolution providing for congressional disapproval u |
| 119hr2781ih | 1,195 | 1 | 0 | 0 | Engaging Next-generation Leaders in Information about Servic |
| 119hjres39ih | 1,168 | 1 | 0 | 0 | A joint resolution providing for congressional disapproval u |
| 119hjres109ih | 1,086 | 1 | 0 | 0 | Disapproving the action of the District of Columbia Council  |
| 119s3022is | 1,048 | 1 | 0 | 0 | Save Our Seas 2.0 Marine Debris Infrastructure Programs Reau |
| 119hr1847ih | 978 | 1 | 0 | 0 | H.R. 1847 — To codify Executive Order 14158 relating to esta |

Final: **28 artifacts** — 11 substantive (metrics > 0), 17 honest zeros (60%).

**The docket's honest shape:** 60% of randomly sampled bills (17 of 28) are symbolic, naming, single-command, constitutional-amendment, or disapproval measures that yield zero forecastable metrics. The contract correctly refuses to inflate these — every zero-metric artifact says why in its honesty note. Scaling to millions of forecasts means a cheap fast-path for this majority and deep extraction for the substantive minority, not uniform effort.

## What the contract handled well
- Substantive program bills (S. 1082 Medicaid, S. 767 HIDTA, H.R. 978, H.R. 1021 SBA, H.R. 608): goals/effects/barriers/metrics/stances all populated naturally; 3 provisions and 7-9 metrics per bill was the comfortable working shape.
- Honest zeros: `sourceLimits`-style prose notes let tiny/symbolic bills pass through without fabrication.
- The mega-bill (995k chars, 1,018 pages, 334 sections): 13 title-level provisions with an explicit coverage map ("five high-impact blocks read closely; small titles read in full; remaining coverage selective") — the coarse-then-enrich shape fits the schema.
- One-sided conditionals: free-text conditionals can express "observation exists only under enactment; the non-enactment value is missing, not zero" (S. 1082).

## Where the contract strained (recurring, cross-bill)
1. **Incorporated law is not first-class** — the single most repeated finding (all 7 disapproval resolutions (6 CRA + 1 DC Council), S. 1082, S. 1188, H.R. 2449, H.R. 1847). No typed field for the incorporated/amended instrument, its version, provenance, or the baseline law; a CRA resolution's entire substance lives in a rule the artifact cannot cite structurally.
2. **No provision-dependency or sequencing edges** — H.R. 1021's GAO report evaluates §2 but is its own obligation; S. 1082's verification→resource-test one-year gap is a cross-provision state transition; H.R. 2449's nested clocks (120 days post-enactment, then reports from establishment date) are date arithmetic the schema can only narrate.
3. **Three-valued stances can't express direction/lag/ceiling/sufficiency** — "serves" conflates measures-the-goal with higher-is-better; at title scale (H.R.1) matrices are dominated by `orthogonal`; ceilings (CRP's 27M acres) vs targets aren't distinguishable.
4. **No typed honesty/sourceLimits field** — every lane independently invented the same workaround (disclosure prose in `context`). The convention is now de facto; make it schema.
5. **Mega-scale structure** — no `title > subtitle > part > section` path, section-range, or source-span fields; no way to share one metric across two titles without drift (H.R.1 Titles VI/VII border ops, IV/XI health financing); "unobligated balance" rescissions need a baseline-date field to avoid fabricating fixed dollar amounts.
6. **Zero-metric bills have no machine-readable marker** — H.R. 80's goals are real legal commands with no public evidence channel; the artifact can only leave metrics empty, indistinguishable from "not yet extracted."
7. **Named cohorts** (H.R. 80's 51-person list), **overtaken-by-later-law** (S. 1188 references §168(k) paragraphs struck by P.L. 119-21), and **State-variant thresholds** (S. 1082 "or such amount as the State shall establish") each lack any typed home.

## Harness lessons
- **Write-early wins on mega-bills.** Attempt 1 on H.R.1 died AFTER structural mapping, BEFORE writing JSON — total loss. Attempt 2's brief (coarse valid artifact first, enrich incrementally, valid JSON after every title) succeeded. Default for anything >100k chars.
- **Silent lane deaths happen** — one lane died at startup leaving only the brief echo in its log. Plain rerun succeeded. Liveness = artifact-exists + process-gone, never log-looks-fine.
- **Sandbox honesty held**: offline lanes reported "vitest unavailable / DNS blocked" rather than claiming test results; lanes cannot commit (worktree git metadata sits outside the writable sandbox) so the integrator commits — which is also the right trust boundary.
- **The sampler is a reliable ingestion path**: direct govinfo XML file URLs hit on 25/25 sampled probes tonight (listings are JS app-shell; files are not). Every artifact records its govinfo URL — the exact backfill hook #111 needs for Axiom-first ingestion.

## Recommended follow-ups (issue-worthy, morning triage)
1. **Contract v2 schema gaps** — one issue collecting: incorporatedInstruments[], typed sourceLimits, provisionDependencies[], structuralPath/sourceSpan, cohort/target-set, baselineLaw/overtaken-by markers, evidence-channel marker for honest zeros. (Findings 1-7 above.)
2. **Disapproval-resolution fast path** — 7 of 28 random bills were disapproval resolutions (6 CRA chapter-8, 1 DC Council) with identical shape (single provision, incorporated rule, zero metrics). Auto-template them; reserve sol lanes for substantive bills.
3. **Mega-bill pipeline** — write-early brief as standard, per-title source spans, shared-metric dedup. Feeds the millions-of-forecasts URL/scale design (#88 thread).
4. **Stance matrix v2 or documented semantics** — at minimum document that `serves` ≠ directionality; consider direction/timing enrichment.
5. **#111 tie-in** — artifacts' recorded govinfo URLs are the Axiom backfill worklist.
