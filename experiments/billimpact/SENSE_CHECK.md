# SENSE CHECK — pre-demo audit against the room (2026-07-31, ~12:45 EDT)

Reviewer stance: knowledgeable, skeptical-but-fair audience member — Max Ghenis,
David Trimmer, policy researchers, AI-tool builders. People who know CRPS, know
model tiers cold, know these benefit programs, and recompute sign tests in
their heads. Surfaces reviewed: `RESULTS.md`, `TWO_LEGS_S3596.md`,
`forward/FORWARD-S3596.md`, `results/demo_page.html` (present, reviewed in
full, including the embedded JS data), both demo figures (read as images), the
PR #61 body, plus the substrate they cite (`results/*.md`, `CHECK2.md`,
`final_multimetric.json`, `runs_envelope.jsonl`, `s3596_conditional_runs.jsonl`,
`envelope_sweep.py`, the ground-truth files, and PR #64). Every inherited
number was checked against primary sources on the web; the verification
appendix at the bottom records exactly what was and was not confirmed.

Ranked. Each item: where, why it is a red flag *to this audience*, exact
replacement wording.

---

## RED FLAGS

### 1. TWO_LEGS_S3596.md misreads PR #64's "−1.2%" as "−1.2pp" — the "10x delta gap" is a units artifact, and the file says it isn't

**Where:** `TWO_LEGS_S3596.md` lines 7 ("**child poverty −1.2pp** (17.02% →
16.82% …)"), 8–9 ("stale published numbers (−$1.6B / **−0.4pp**)"), and the
entire "The gap is the finding" paragraph (lines 18–27), including the
sentence "a 10x delta gap is not a units artifact."

**Why it's fatal here:** PR #64 (Trimmer's own PR) reports "child poverty
**−1.2%** (17.02%→16.82%)". 17.02 − 16.82 = **0.20 percentage points**; −1.2%
is the *relative* change (0.20/17.02), which is PolicyEngine's house
convention — their published research page for this same bill says "Reduces
child poverty by 0.4%" alongside "Gini … by 0.024%", both relative (verified
today; see appendix). TWO_LEGS quotes the very levels that refute its own
label. The downstream synthesis — "the forecast leg concedes roughly a tenth
of the mechanical effect" — compares PE's *relative* −1.2% against the
forecast leg's *absolute* −0.10/−0.15pp. Compared consistently (pp vs pp:
−0.20 vs −0.10/−0.15; or relative vs relative: −1.2% vs ≈−0.7/−1.1%), the
forecast leg concedes **one-half to three-quarters** of the mechanical effect,
not a tenth. The sentence "a 10x delta gap is not a units artifact" asserts
the exact opposite of what is true. Trimmer wrote the source PR; Max builds
microsims; either will spot 17.02−16.82≠1.2 in seconds, and the error sits in
the one file that is *about their work*.

**Replacement:** rewrite the two numbers and the synthesis. Suggested:

> **Mechanical leg** (PR #64, D. Trimmer): … budgetary impact −$1.83B; child
> poverty **−0.20pp** (17.02% → 16.82%; −1.2% relative, PE poverty measure,
> 2026) … stale published numbers (−$1.6B / −0.4% relative) superseded by the
> refresh — the poverty effect tripled, which is the PR's own argument for
> admissibility gates.

> **The comparison holds up — and the harness result is where the gap lives.**
> The forecast leg's conditional delta (−0.10 to −0.15pp) is roughly half to
> three-quarters of the mechanical −0.20pp, on measures that are not
> commensurable (PE poverty measure on build P, 2026 static, vs Census SPM
> child rate, 2027 realized), so the levels should not be over-read in either
> direction. The 10x effect in this study is elsewhere: hold the models fixed
> and vary only *what they are shown* — full bill text yields Δ −0.1 to
> −0.2pp, the bill's *name alone* yields −1.5pp (fable-5, paired elicitation,
> `runs_envelope.jsonl`). The delta a bill-conditioned forecaster reports can
> swing an order of magnitude on context alone, which is the study's actual
> thesis — and why the mechanical delta must be injected from the mechanical
> leg, not re-derived inside the forecast.

Note: the commit message for `8f4f9894` ("mechanical (-1.2pp, PR64)") carries
the same error and is immutable — one more reason the doc itself must be
corrected before anyone reads the log.

### 2. Demo page §07 claims the witness tier for records that are claimed-time at best

**Where:** `results/demo_page.html`, section 07 lede: "runs committed with
timestamps and **sealed by the recorder workflow (RFC-3161 witness)**"; and
the chip "**per-config lanes registered**" with "(4 lanes × 3 reps running)".

**Why:** the chronology tiers are the hosts' own credibility machinery
(`site/src/data/thesis-log.ts`). The recorder has not run — the PR is open,
and `FORWARD-S3596.md`'s own §"To register" lists merge + `gh workflow run
record-forecasts.yml` as *future* steps. Until then everything is
claimed-time-from-git-history, which FORWARD states correctly. Claiming
"sealed … RFC-3161 witness" on the demo surface is precisely the vocabulary
misuse this room owns, aimed at the people who built the tiers. Same problem
with "registered" for the lanes: 16 targets were *selected*; runs exist for
T01–T04 only (the lane session was cancelled mid-run, per FORWARD); nothing is
merged or sealed.

**Replacement (lede):** "…runs committed with timestamps — claimed-time
chronology from git history, upgraded to the witness-verified tier when the
recorder workflow runs on merge (RFC-3161 seal; one command, listed in
`forward/FORWARD-S3596.md`)."
**Replacement (chip):** title "And the harness becomes a live experiment" →
value "**per-config lanes prepared**" → body: "16 near-resolving
program-level targets selected for per-configuration forecast lanes; 4 lanes ×
3 reps complete on the first four targets, the rest queued. Registration =
merge + recorder seal, pending. Finding 1 then re-measures itself — out of
training distribution, scored mechanically as targets resolve (first
resolutions from August 2026; the S.3596 targets in 2028)."

### 3. The §06 lever quotes a superseded n=7 read (0.178), and CHECK2 already says so

**Where:** `results/demo_page.html` §06: "reasoning effort → max: nCRPS 0.267
→ 0.178 (partial n · final n pending)". Also anywhere the §5 refresh inherits
these numbers when it lands in `RESULTS.md`.

**Why:** `CHECK2.md` Item 3 verdict is **SUPERSEDED** — the 0.178 was an n=7
read; at S2 (n=117, 25/28 units) the cell is **0.2143 with cov80 0.829**, and
still filling. The "0.267" base matches no current row either (B1 opus
operative_only is 0.268; `final_multimetric.json` has opus bill 0.261 →
effort=max 0.247, opus no-bill 0.253 → max[plain] 0.198). Anyone who opens
`final_multimetric.json` (committed in the same PR) cannot reproduce either
number — a stale-derived-state failure on the page's single most quotable
product claim. The badge "partial n" does not save it: the *direction*
survives, the *magnitude* roughly halved.

**Replacement:** re-derive from the pinned batch at page-freeze and quote that
batch state, e.g.: "reasoning effort → max: nCRPS 0.253 → 0.198 (opus-5,
no-bill, n=24 of 28 units — final n pending)" — or, if the batch is still
moving at freeze, drop the numbers: "reasoning effort → max was the largest
single accuracy lever measured (final magnitude landing; direction stable
across every batch cut)." Keep the existing Finding-3 caveat sentence — it is
the best line in the section. Also add the coverage: the effort-max cells run
cov80 0.83–0.94 against nominal 0.80 (see item 4).
Corollary: the Leg-2 numbers (0.243 / 0.326 / 19-28 wins / CI excludes zero)
**are** verified — but on batch B1 specifically (`CHECK2.md` Items 1–2, which
also note the full file has drifted: 18/28 at S2). Add "(batch-pinned
analysis; `CHECK2.md`)" somewhere on the page footer and quote one batch state
everywhere, which is CHECK2's own instruction.

### 4. Over-coverage arms are about to land in §5 — do not let cov80 > 0.90 read as a win

**Where (prospective, RESULTS.md §5 refresh + any spoken claim):**
instruction-style arms run cov80 **0.88–0.96** (CHECK2 Item 8), MAS arms
**0.90–1.00** (Item 9: variance_auditor literally 1.00), effort-max cells
0.83–0.94, `final_multimetric.json` rows up to 0.922. And in corpus A
(`results/results_table.md`), opus-5's cells sit at cov80 **0.97–1.00**.

**Why:** the room is full of forecasters; for a nominal-80% interval, 0.95
coverage is *miscalibration in the wide direction*, not caution. The trap is
presenting "premortem style: nCRPS 0.183!" with its 0.95 coverage either
unmentioned or mentioned approvingly. Similarly, if anyone asks "which model
was calibrated?", the honest corpus-A answer is *none*: sonnet/haiku
under-cover (0.50 → 0.02–0.32), opus over-covers (0.97–1.00, widths 3.8–4.0
history-SDs), fable is nearest nominal (0.82–0.87).

**Prescription:** every nCRPS comparison in the §5 refresh ships its cov80 and
width beside it; label anything ≥0.90 "over-wide (nominal 0.80)"; never
present coverage above nominal as favorable. Have the corpus-A calibration
answer ready as one sentence: "nobody was calibrated — the small models were
overconfident, opus bought its CRPS with intervals twice as wide as nominal,
and bill text made the miscalibration worse in every case."

### 5. The "best arm ignores the bill" pull-quote is one screenshot away — and the fable CTC row doesn't reconcile

**Where:** demo page §06 Leg 2 ("Outcome forecast: frontier tier, **no bill
text in the prompt**" / "Best measured arm — opus-5, no bill text");
`forward/FORWARD-S3596.md` table (fable row: 48.5 → 48.9 labeled **+0.3**);
demo page §07 CTC card ("fable-5 **agrees, at** +0.3M").

**Why (a):** Leg 2's summary line, screenshotted alone, is the devastating
quote: "their bill-impact tool works best when you don't show it the bill."
The composition framing lives in Leg 3 and the footer — not inside Leg 2,
where the quote will be cropped from.
**Fix (a):** add as Leg 2's first bullet: "**Bill-blind by design** — the
statute's effect enters through Leg 1's computed delta at composition (Leg 3),
not by pasting the bill into the forecast prompt, where Findings 2–3 show it
buys recall and overconfidence, not information."

**Why (b):** in FORWARD's table, 48.9 − 48.5 = **+0.4**, but the Δ column says
+0.3 (it is the median of within-run deltas: 0.4/0.3/0.2 — a legitimate
statistic, but the table's own columns don't reproduce it, and this room
reproduces derived numbers from the payload). The demo page hides fable's
levels behind "agrees, at +0.3M" — which both dodges the arithmetic and uses
corroboration language for two arms of the same experiment (two LLMs agreeing
is shared prior, not evidence).
**Fix (b):** FORWARD table footnote: "Δ = median of within-run deltas; for
fable-CTC this differs from the difference of scenario medians (48.5 → 48.9;
per-rep Δ 0.4/0.3/0.2, median +0.3)." Demo card: replace "agrees, at +0.3M"
with fable's actual levels "48.5M → 48.9M · within-run Δ +0.3M" and drop the
word "agrees".

### 6. Envelope results: never let fable's name-only −1.5pp sit near the mechanical number

**Where (prospective):** the S.3596-envelope arm is landing in `RESULTS.md`
this afternoon (banner). Its strongest cell: fable-5, `named_only`, paired →
SPM delta median **−1.5pp** (reps −1.5/−1.9/−1.1; `runs_envelope.jsonl`).
Trimmer's mechanical number is "−1.2" (relative %; item 1). Two files apart
today; one table apart if drafted carelessly.

**Why:** "−1.5 ≈ −1.2" invites the exact accidental-corroboration reading the
study exists to kill — different quantities (pp vs relative %), different
measures (Census SPM 2027 vs PE measure 2026), and above all different
*mechanisms*: the name-only arm is the **recall** arm. If its output lands
near the mechanical estimate, that is a coincidence of scale that would
*indict* the arm, not validate it.

**Prescription:** in the envelope write-up, (i) never tabulate any mechanical
number in or beside the envelope table; (ii) frame the envelope result as
context-sensitivity of the delta itself: "full bill −0.1/−0.2pp → name alone
−1.5pp: a 10x swing from context alone, in the direction Finding 3 predicts —
the name invites the model to price in what it remembers the bill's coverage
saying, not what the text computes to"; (iii) state per-cell n — one cell
(CTC · summary · fable · paired) has **n=2**, so say "medians of 3 (one cell
n=2)" rather than a blanket "3 reps".

### 7. "10/12 units, p=0.002" reads as a wrong sign test — state the denominator

**Where:** `RESULTS.md` §2 ("forecasts fell in 10/12 units, median −2.65%
(p=0.002)") and the §2 table row; demo page §04 fine print ("down in 10/12
units, p=0.002"); `PREREG-AMENDMENT-2.md` line 11.

**Why:** a sign test on 10/12 is p=0.039 two-sided, and this crowd computes
binomial tails in their head. The actual construction is correct — zero-shift
units are dropped, so it is 10/10 nonzero → p=0.00195
(`analyze.py:1347`, `binom_two_sided_p(purpose_neg, n_purpose_nonzero)`) — but
none of the three surfaces says so, so the reported p looks wrong by 20x.

**Replacement (all three places):** "fell in 10 of 12 units (two unmoved; sign
test on the 10 nonzero units, p=0.002)". The neighboring claims are already
denominator-clean ("12/12, p=0.0005" ✓; "8/9 *moving* units, p=0.039" ✓ —
that wording is the model to copy).

### 8. Inherited history tables: SPM row fully verified; the CTC row is not — fix labels before anyone projects it

**Where:** `envelope_sweep.py` TARGETS (in-prompt "HISTORY (as published)");
`site/src/data/forecast-cells.ts` (SPM: lines 642–647, 1104–1110; CTC: lines
2937–2942 and the `irs.lookup` reasoning step at 2965–2967). Not displayed on
the demo page — exposure is via projected prompts, the site cell pages, or a
direct question.

**Verified (keep as-is):** SPM child poverty **2021 5.2 / 2022 12.4 / 2023
13.7 / 2024 13.4** — all four confirmed against Census-derived primary
reporting (appendix). The "(expanded monthly CTC in effect)" annotation on
2021 is good; keep it.

**Not verified (fix):** CTC qualifying children **TY2019 48 / TY2021 61 /
TY2022 49**, implicitly sourced to IRS SOI:
- **61 (TY2021)** — real and children-denominated, but it is the
  Treasury/IRS *advance-payment* coverage figure ("more than 61 million
  children", December 2021 disbursement), not an SOI tabulation of qualifying
  children claimed on returns. Right number, wrong implied source.
- **48 (TY2019)** — could not be verified as *children*. The best-sourced
  match is ~48 million **filers/returns** claiming the CTC (Tax Foundation
  primer; consistent with the SOI CTC+ODC returns line). If the true TY2019
  qualifying-children count differs, every surface repeating 48 "children" is
  wrong; if it coincidentally matches, the label is still an unsourced
  coincidence.
- **49 (TY2022)** — found **no** source. IRS SOI TY2022 shows ACTC on 17.8M
  returns and $110.4B total CTC; no qualifying-children count surfaced in the
  SOI TY2022 CTC research paper's extractable text or anywhere else I
  searched.

**Prescription:** before 17:00, relabel the history block per-row, e.g.
"TY2019 ~48 (returns claiming CTC — children count not published) · TY2021
61 (children covered by advance payments, Treasury) · TY2022 —", or drop
TY2019/TY2022 and keep only the Treasury-sourced 61 with its label. The
registered target's own resolution rule already hedges ("…or the closest
directly comparable official count") — align the history label with that
hedge. Do not re-run the forecasts over this; disclose that the prompt's
history block carried these labels if asked. Also pre-brief the presenter:
fable's raw `mechanism` text says "$3,000 to $1" (the statutory layer — §2(a)
literally strikes "$3,000" from IRC §24(d)(1)(B)(i), and §2(b) strikes
§24(h)(6), the $2,500 override), while every page surface says "$2,500 → $1"
(the correct *operational* delta under current law). Both are right at their
own layer; FORWARD links the raw JSONL, so someone may open it and ask.

### 9. The FPUC surfaces never say the units — and this is a BEA-literate room

**Where:** `results/demo_recall_anchoring.png` y-axis "median forecast, UI
outlays (**units as published**)"; demo page §04 chip "(first print 570.6)"
and stepper line "≈ the remembered 570"; §04 derivation panel "(UI outlays,
annualized $B)" with "baseline 36 + 31 = 67".

**Why:** 570.6 is `W825RC1` — Personal current transfer receipts: government
social benefits to persons: **unemployment insurance**, monthly, **billions of
dollars at a seasonally adjusted annual rate**. Verified: BEA "Personal Income
and Outlays, January 2021" (released 2021-02-26), Table 3 line 26 reads
"…281.1  307.8  **570.6**" — Nov, Dec 2020, Jan 2021 at SAAR; the Dec→Jan jump
*is* the $300 FPUC restart the corpus targets. "Units as published" is a
dodge; a BEA-literate reader either does the SAAR conversion silently and
wonders why the page didn't, or — worse — a non-BEA reader takes 570.6 as a
monthly or quarterly flow. "Annualized $B" in the derivation panel is close
but nonstandard.

**Replacement:** figure y-axis: "UI benefits, $B (seasonally adjusted annual
rate — BEA W825RC1)". Figcaption add: "Values are SAAR: Jan-2021's first print
of 570.6 corresponds to ~$47B of benefits paid in the month." §04 chip: "first
print 570.6 ($B, SAAR)". Derivation panel title: "(UI outlays, $B SAAR)" — the
arithmetic (300 × 2.0M × 52 ≈ 31; 36 + 31 = 67) is already exactly right *as*
SAAR, which is worth saying out loud: the model annualized correctly.

### 10. Smaller, still worth 10 minutes

- **Uncommitted design vs the "100%" stat.** `quantile_sweep.py` +
  `runs_quantile.jsonl` are untracked (git status) while the page stat-strip
  claims "100% of designs committed to git before their first run." If any
  quantile-CDF number reaches a surface, that claim is falsified by the repo's
  own status output. Commit the runner before citing the arm, or scope the
  stat ("every pre-registered arm's design committed before its first run;
  one exploratory probe (quantile-CDF) labeled as such").
- **Run-count sync.** Hero says "roughly 6,000 scored runs"; `RESULTS.md`
  says "~5,600 … at time of writing." Pick the freeze-time number and make
  hero, statstrip, and RESULTS totals agree.
- **RESULTS §4 editing scar:** "fable ran only the full-bill conditions and is
  marked — elsewhere." reads as a broken sentence. Suggest: "fable-5 ran only
  the full-bill conditions; its other cells are marked '—' in the table."
- **Dispersion figure verdict boxes** show the naive ratios ("EXCEEDS 1.81×
  noise") that §1 itself calls the wrong construction. Verdicts match the
  pre-registered bootstrap test, so it is defensible — add one figcaption
  clause: "verdict boxes show the pre-registered ratio test; the red-team
  permutation restatement (RESULTS §1) strengthens every EXCEEDS verdict."
- **Hero tone (optional):** "Teams everywhere are building bill→forecast
  tools. Nobody measures the plumbing." — in front of the team whose lab
  measures forecasts for a living, consider self-implication: "Nobody —
  including us, until this morning — measures the plumbing." Cheap insurance;
  the current line is defensible since the harness (not accuracy) is the
  unmeasured thing.
- **Spoken-register guard:** nothing in any file calls sonnet "mid-tier"
  (checked) — keep it that way live; say "the smaller/faster tier" or name
  models plainly. Same guard for haiku: the only correct frame for the §05
  table is the one already used — the tool saturates every tier; the 4%
  no-tool row is the model's own capability.

---

## CLEARED (checked, fine as they stand)

- **Haiku/tools framing** (`RESULTS.md` §4; page §05): "the tool converts
  every model to 100% — haiku 4→100" is the correct frame everywhere it
  appears; the no-tools view is the page default, so capability shows first.
  No "mid-tier" phrasing anywhere in the reviewed surfaces.
- **"Ground truth" doctrine:** applied to first prints (data) only.
  PolicyEngine is "reference implementation … a model input, never ground
  truth for behavior" in both `RESULTS.md` §4 and the page footer (#7).
  `FORWARD-S3596.md` is careful ("claimed-time chronology from git history"
  until the recorder runs) — the §07 page lede (item 2) is the only witness
  overclaim found.
- **S.3596 mechanics:** "$2,500 → $1" is the correct operational description —
  verified against the bill text itself (§2(a) strikes "$3,000" from IRC
  §24(d)(1)(B)(i); §2(b) strikes §24(h)(6), the $2,500 override; effective
  TY2026+) and corroborated by TPC and the sponsors' releases. It **is**
  S.3596, 119th Congress (2025–2026), Hassan/Young — the reintroduced bill
  really does carry the same number as the 118th-Congress version, so
  "currently pending" and "(119th Congress)" in `envelope_sweep.py` are right.
- **S.3596 conditional medians:** every number in FORWARD's table and the page
  §07 cards reproduces from `s3596_conditional_runs.jsonl` (independently
  recomputed here; also CHECK2 Item 10) — sole caveat is the fable-CTC Δ
  convention (item 5b).
- **Behavioral-uptake framing (seeded item 9):** present at every appearance
  of +0.2–0.3M — FORWARD's "NOT mechanical … behavioral uptake claim," and the
  page card's *visible* details-summary "Behavioral-uptake claim — the
  mechanical Δ is zero," plus "If uptake is a fiction, this row gets scored
  for it," which is the right sentence for this room.
- **Demo page §02 widget vs substrate:** all FL·2023-12 medians, spreads, and
  noise floors match `dispersion.md` exactly (models 1.054/1.007/1.137/1.054;
  contexts 1.000/1.018/1.007/0.982/0.982; elicitation 1.007/1.018/1.036/1.125;
  spreads 13.0/11.8/3.6; noise 2.0/2.9/4.3); the unconditioned median 2.80M
  reproduces from `runs_api.jsonl` (2.65–2.85M reps); truth 3,004,132 as
  frozen. "One dial at a time … this page does not invent them" is exactly the
  right guard against off-axis interpolation.
- **§03 calibration numbers:** widths/coverages match `results_table.md`
  (none: 309k/0.50; operative: 234k/0.32; pooled shown-context coverage
  0.325→"0.33"). Under-coverage presented as the failure it is; `skill.md`
  says "badly over-confident," correct polarity, and the coverage-drop table
  uses bucketed p-values, labeled as such.
- **The N=8 bake-off (`RESULTS.md` §5 current text):** "directional, not
  significant at N=8" with the contamination-direction caveat is exactly
  right; the sonnet-loses-to-persistence sentence is plain naming, not tier
  disparagement.
- **Statistical hygiene generally:** "12/12 (p=0.0005)" ✓ exact; "8/9 moving
  units (p=0.039)" ✓ exact with the right denominator wording; N-statements
  footer (#1–#8) is strong, and #8 ("Where a 'best measured arm' is named, it
  is a comparison inside this study, not a product endorsement") defuses the
  0-configs-recommended vs best-arm tension explicitly. Bootstrap/paired
  constructions are producible on request (`CHECK2.md` documents them,
  including seeds and batch definitions).
- **PR #61 body:** framing matches the repo (dispersion-is-the-deliverable, no
  praise of weak models, "$374.85, PolicyEngine-verified" household delta);
  the closing forecast-api CDF-drift flag is a constructive bug report, cited
  to `PR_STATUS.md`, and the right kind of thing to hand the hosts.
- **TWO_LEGS certification note** (household checks on 1.784.3 vs certified
  1.764.6-on-build-P): correctly scoped — certification governs
  model↔data-build pairing for population runs; household arithmetic uses no
  population build; stating the version anyway is the right call. (Keep this;
  fix only the units, item 1.)
- **Recall figure honesty details:** future arm "never scored; the measurand
  is dose-response" appears on both the page and the figure caption; fable's
  $900-extreme exception is disclosed in the caption rather than hidden.

---

## Verification appendix (what was checked against what, today)

| Claim | Verdict | Source |
|---|---|---|
| SPM child poverty 2021 = 5.2% (record low, expanded-CTC year) | **Verified** | Census SEHSD wp2022-24 + census.gov "Record Drop in Child Poverty" (2022-09) |
| SPM child poverty 2022 = 12.4% (more than doubled) | **Verified** | Census-derived reporting (Columbia CPSP; census.gov SPM pages) |
| SPM child poverty 2023 = 13.7% | **Verified** | Census 2024-09 release, echoed in CRS R48854 and First Focus |
| SPM child poverty 2024 = 13.4% (no stat. change vs 13.7) | **Verified** | Census 2025-09 release ("Poverty in the United States: 2024"); CRS R48854; AAP/First Focus coverage |
| CTC qualifying children TY2021 = 61M | **Number real, source mislabeled** — Treasury/IRS advance-payment coverage ("more than 61 million children," Dec-2021 disbursement), not an SOI return tabulation | Treasury press releases + JEC |
| CTC qualifying children TY2019 = 48M | **NOT verified as children** — best match is ~48M *filers/returns* claiming CTC (Tax Foundation primer). Possible returns-vs-children conflation | Tax Foundation "The Child Tax Credit: A Primer" |
| CTC qualifying children TY2022 = 49M | **NOT verified** — no source found; SOI TY2022 shows ACTC on 17.8M returns, $110.4B total CTC, no child count in extractable text of the SOI TY2022 CTC paper (24rpctcunderclaims.pdf, read in full) | irs.gov SOI |
| W825RC1 units = $B, seasonally adjusted annual rate, monthly, BEA | **Verified** | FRED series metadata (title/mirror), BEA release table headers |
| W825RC1 Jan-2021 first print = 570.6 | **Verified** | BEA "Personal Income and Outlays, January 2021" (2021-02-26), pi0121.pdf Table 3 line 26: …307.8 (Dec) → 570.6 (Jan) |
| PR #64 "child poverty −1.2%" is relative, = −0.20pp | **Verified** | PR #64 body (17.02→16.82); PolicyEngine research page publishes "Reduces child poverty by 0.4%" alongside "Gini … 0.024%" — relative convention |
| S.3596 = 119th Congress, Hassan/Young, strikes "$3,000"→"$1" in §24(d)(1)(B)(i) + strikes §24(h)(6), TY2026+ | **Verified** | Bill text PDF (scratchpad copy = repo copy, diff-identical §2); congress.gov 119th listing; TPC/R Street/sponsor releases for the $2,500 operational framing |
| FL·2023-12 demo-widget numbers, S.3596 conditional medians, B1 bake-off numbers, A3/A4 monotonicity claims | **Reproduced** from repo substrate (this review + `CHECK2.md`) | local recomputation |

Nothing in this file modifies any other file; every fix above is wording, a
label, a footnote, or a re-derivation at freeze — no re-runs required, except
that item 3's lever number must be re-read from the pinned batch before it is
spoken aloud.
