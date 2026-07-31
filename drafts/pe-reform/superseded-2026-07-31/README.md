# SUPERSEDED — do not quote the 4.49M

These two files are the first output of `scripts/pe_reform_cell.py` (PR #65),
kept only so the defect has a record. **The number in them was never computed by
PolicyEngine.** Nothing here may be cited, put on a slide, or fed to a
downstream lane.

## What was wrong

`minwage-15-draft-cell.json` reports **4.49M** (80% CI 3.04–5.94) people "newly
exposed" to the Medicaid work requirement. Three independent defects, any one of
which is disqualifying:

1. **The population count bypassed the engine.** The script opened
   `populace_us_2024.h5` with h5py, read the raw `weight` column, and multiplied
   it by a hand-written approximation of `medicaid_work_requirement_eligible`:
   an earnings band, an hours proxy imputed from `hourly_wage`, and exactly two
   exemptions (`is_disabled`, `is_full_time_college_student`). The real variable
   also exempts pregnancy, caretakers of children ≤13, the medically frail, AIAN
   members, veterans, former foster youth and Medicare enrollees. So the figure
   is a spreadsheet rule applied to PolicyEngine's data, presented as a
   PolicyEngine result. House doctrine: never touch the weights directly, always
   go through the microsimulation.

2. **The model/data pairing was uncertified.** The run used whatever
   `policyengine-us` was installed on the dev box — **1.784.3**. Populace build P
   certifies **1.764.6** (its `release_manifest.json`), and 1.784.3 has no
   certified build at all. Under `POLICYENGINE.md` §0.2 an uncertified pairing is
   inadmissible for a published number. Nothing in the old code path checked.

3. **The dataset was not a pinned build.** It globbed the newest
   `populace_us_*.h5` out of the HuggingFace cache, so the artifact records a
   filename rather than a build tag and the run is not reproducible.

The `sigma_scope = 0.25 × count` term in the interval was an unexplained
assertion standing in for defect (1) — the proxy rule's blind spots. It is not a
measurement of anything.

## What replaced it

`scripts/pe_reform_cell.py` now routes both stages through the audited wrapper
(`scripts/tools/policyengine.py`, `POLICYENGINE.md`):

- the engine computes the variable under both arms on a pinned build, and
  transitions are counted with the weights the engine returns;
- `pe.require_certification` refuses before the microdata is touched, so an
  uncertified pairing produces no number rather than a caveated one;
- output is confined to `drafts/`.

A replacement figure is not in this directory because it does not exist yet: it
needs either the certified stack (`policyengine-us==1.764.6` +
`policyengine-core==3.26.11`) on a big-memory box, or the Modal path
(`modal run scripts/tools/modal_population.py`). Until one of those runs, the
honest state of this cell is "no number", which is what the loop now emits.
