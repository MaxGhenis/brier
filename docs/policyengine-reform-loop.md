# The PolicyEngine reform loop

The smallest end-to-end path through the lab for a *policy* target rather than
an official data series:

```
one-parameter reform -> PolicyEngine computes -> outcome metric -> draft cell
```

`scripts/pe_reform_cell.py` is the whole loop. It changes exactly one
PolicyEngine-US parameter, has the **engine** recompute a population outcome
under baseline and reform, sizes an 80% interval from the run itself, and emits
a draft cell that satisfies [`docs/cell-contract.md`](cell-contract.md).

Both legs go through the audited wrapper (`scripts/tools/policyengine.py`,
[`POLICYENGINE.md`](../POLICYENGINE.md)). Output is confined to `drafts/`.

> **Superseded number.** The first revision of this loop reported **4.49M** by
> opening the Populace HDF5 with h5py, reading its `weight` column and
> multiplying by a hand-written approximation of the variable, on a model
> version the data build does not certify. That figure is not a PolicyEngine
> result and must not be cited; see
> [`drafts/pe-reform/superseded-2026-07-31/README.md`](../drafts/pe-reform/superseded-2026-07-31/README.md).

## Environment

PolicyEngine-US is not part of the repo's own dependency set; it is a heavy
install (~80 packages, plus a ~330 MB microdata download) and it pins older
numpy/pandas ranges than this repo runs. Install it into its own venv:

```bash
python -m venv C:/pe/v
C:/pe/v/Scripts/python -m pip install policyengine-us
```

**Use a short path on Windows.** PolicyEngine's parameter and variable trees
exceed the 260-character `MAX_PATH` limit under a normal project-nested venv.
A too-deep install fails *silently in a way that looks like success*: pip
reports an `OSError`, but the package directory is left behind without a
`dist-info` and without `variables/`, so `import policyengine_us` gets far
enough to raise a confusing `ModuleNotFoundError: policyengine_us.variables`.
Verify an install with:

```bash
C:/pe/v/Scripts/python -m pip list | grep policyengine-us
```

If `policyengine-us` is absent from `pip list` but the directory exists, that
is the long-path failure. Enabling `LongPathsEnabled` machine-wide also fixes
it, but the short path needs no privileges and no undocumented machine state.

The microdata (`policyengine/populace-us`, `populace_us_2024.h5`) downloads on
first `Microsimulation()` and is cached under `~/.cache/huggingface`.

## Certification — why most boxes cannot produce this number

A Populace build is certified for exactly one `policyengine-us` version, named
in the build's own `release_manifest.json`. Build P certifies **1.764.6**; the
newest wheel (1.784.3) has no certified build at all. Running any other pairing
is inadmissible ([`POLICYENGINE.md`](../POLICYENGINE.md) §0.2).

`pe.require_certification` raises **before the microdata is touched**, so an
uncertified pairing yields no number rather than a number carrying a warning,
and `pe_reform_cell.py` refuses to emit a cell on top of it. On a box with the
default `pip install policyengine-us` this is what you will see, and it is
correct:

```
UNCERTIFIED PAIRING: build certifies policyengine-us==1.764.6, running 1.784.3.
```

To get past it, either install the certified stack
(`scripts/tools/requirements-tax.txt`) on a big-memory box, or use Modal, which
is the only path that satisfies both constraints at once — a national microsim
OOMs a 16 GB laptop, and the certified stack is not what a dev box has
installed.

## Usage

```bash
# certified national run on Modal (32 GB, pins 1.764.6 + core 3.26.11)
modal run scripts/tools/modal_population.py
python3 scripts/pe_reform_cell.py \
    --from-run drafts/pe-reform/buildP-population-medicaid_work_requirement_eligible-2027.json

# or locally, if this box has the certified stack AND the memory
C:/pe/v/Scripts/python scripts/pe_reform_cell.py
```

It writes the draft cell array plus a sibling `.run.json` recording the reform,
the certified pairing, the dataset build, and every derived quantity that
appears in the trace — all under `drafts/`. `--out` outside `drafts/` is
refused: a draft that can land in `examples/` is a draft that gets cited as one.

Publication is **not** part of this loop. `spawned_cells_to_ts.py` requires a
custody envelope that only a recorded `run_thesis_analyst.py` agent run
legitimately produces, so the loop stops at a validated draft.

## The minimum wage caveat — read this before citing a number

PolicyEngine-US is a **static** tax-benefit model. Raising the minimum wage
does not raise anybody's earnings in it. Across the entire US model the
parameter `gov.dol.minimum_wage` is read by exactly four variables, and in
every one it is a **threshold**, never a wage floor:

| Variable | Scope |
| --- | --- |
| `medicaid_work_requirement_eligible` | national |
| `nm_cdcc_eligible` | New Mexico |
| `ok_ccs_activity_eligible` | Oklahoma |
| `sd_cca_parent_in_eligible_activity` | South Dakota |

In the Medicaid variable it sets
`monthly_income_threshold = minimum_wage * monthly_hours_threshold` (80
hours). The income route to satisfying the OBBBA community-engagement
requirement is `medicaid_household_income >= threshold * 12`.

So inside the model the causal direction is the opposite of the intuitive
read: **minimum wage up -> income bar up -> fewer people clear the income
route -> modelled eligibility down**, because earnings are held fixed. That is
the *threshold-indexation* channel. It is **not** an estimate of the
labour-market effect of a wage floor, and any cell produced here says so in
its question, its `conditionalOn`, its drivers, and its trace.

A single-household check of the mechanism (no microdata required):

| | minimum wage | annual income bar | $10k earner eligible? |
| --- | --- | --- | --- |
| baseline | $7.25 | $6,960 | yes |
| reform | $15.00 | $14,400 | no |

Two timing constraints follow from the OBBBA parameters: the work requirement
only applies from `2027-01-01` (`work_requirements/applies.yaml`) and the
80-hour threshold is likewise 2027+. The simulation period must be 2027.

## How the interval is derived

A microsimulation returns a deterministic point, not a distribution, so the
interval has to be constructed rather than read off. Two independent
components, combined in quadrature at ±1.28σ for 80%:

- **Sampling sigma** — a bootstrap of the weighted transition count, resampling
  *households*, because persons inside one share a survey weight and are not
  independent draws. Cluster ids come from the engine
  (`household_id` mapped to the metric's entity), not from the dataset.
- **Drift sigma** — a fraction of the point (`--drift-sigma-frac`, default 25%)
  covering model and dataset movement between authoring and resolution, since
  the cell resolves against the then-current certified pairing rather than a
  pinned one.

**The drift term is the weakest input in the cell and the trace says so.** The
only in-repo measurement of build-to-build drift is the build O → build P
refresh recorded in #64, which moved a comparable static-microsim budget line by
+14% while roughly tripling its child-poverty line. One figure covering a
two-order spread is a judgement, so it is chosen wide and labelled, not dressed
up as a measurement.

> An earlier version of this document claimed the drift term was "half the
> weighted population sitting within ±2% of the new income bar … measured from
> the microdata rather than asserted as a percentage". That was never
> implemented — the code asserted a flat 25% of the count under the name
> `sigma_scope`, standing in for the proxy rule's blind spots. The term is
> smaller now in what it has to cover (the engine applies the real exemptions),
> and it is described honestly.

## Why it resolves against the *then-current* release

The obvious resolution rule — recompute with a pinned version and dataset — is
wrong. It would make the answer deterministic and fully known at authoring
time: a computation, not a forecast, with a genuinely zero interval.

The cell instead resolves against the latest `policyengine-us` release
available on the resolution date, using that release's default microdata.
Model churn and data revision become the thing being forecast, which is real,
sizeable, and exactly what the drift term above quantifies. PolicyEngine ships
many releases (the baseline here was `1.784.3`), and a threshold-crossing
statistic is unusually exposed to that churn.

## Limitations

- Static model: no labour supply, no employment response, no wage pass-through.
- The interval covers survey sampling and model drift. It does not cover the
  possibility that PolicyEngine changes what the parameter *means* — e.g. a
  future release letting the wage floor feed earnings would invalidate the
  target rather than move it.
- A policy counterfactual has no official first print. It resolves by
  reproducible recomputation, which is automatic and auditable, but it is a
  different resolution class from the data cells in the main catalog.
