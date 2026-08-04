#!/usr/bin/env python3
"""Publish a batch's winning cells as a wave module in one step.

Wraps the by-hand publish flow: pick the latest passing run per slug from
batch manifests, convert them with spawned_cells_to_ts.py, register their
ledger targets, and wire the module into forecast-cells.ts (idempotent —
existing import lines are left alone).

Usage:
    python3 scripts/register_wave.py --name auto-2026-07-10 \
        --batch records/thesis-analyst/batches/2026-07-10/roll.json
        [--allow-missing]

The module lands at site/src/data/forecast-examples/{name}.ts exporting
{NAME}_WAVE. Exits 2 when the batch produced no publishable cells (callers
treat that as "nothing to do"), 1 on missing slugs without --allow-missing.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile

from register_targets import materialize_registration_snapshots

ROOT = pathlib.Path(__file__).resolve().parents[1]
CELLS_TS = ROOT / "site" / "src" / "data" / "forecast-cells.ts"
EXAMPLES = ROOT / "site" / "src" / "data" / "forecast-examples"


def derive_batch_provenance(batches: list[dict]) -> str:
    """Return the explicit converter provenance shared by validated batches."""

    provenances = {
        (
            "local_operator_attested"
            if batch.get("generationTicket") is not None
            else "ci"
        )
        for batch in batches
    }
    if len(provenances) != 1:
        raise ValueError(
            "batch manifests mix ticketed and ordinary publication provenance"
        )
    return provenances.pop()


def converter_command(
    candidate: pathlib.Path,
    const: str,
    run_files: list[str],
    batch_paths: list[str],
    module: pathlib.Path,
    provenance: str | None,
) -> list[str]:
    """Build the trusted converter invocation with preserved provenance."""

    command = [
        sys.executable,
        str(ROOT / "scripts" / "spawned_cells_to_ts.py"),
        str(candidate),
        const,
        *run_files,
        *sum((["--batch-manifest", path] for path in batch_paths), start=[]),
        "--replace-module",
        str(module),
    ]
    if provenance is not None:
        command.extend(["--provenance", provenance])
    return command


def replay_provenance_for_module(
    module: pathlib.Path, derived_provenance: str
) -> str | None:
    """Preserve an existing module's explicit or legacy-unlabeled state."""

    if module.is_symlink():
        raise ValueError(f"wave destination is not a regular file: {module}")
    if not module.exists():
        return derived_provenance
    if not module.is_file():
        raise ValueError(f"wave destination is not a regular file: {module}")

    from verify_wave_reproducibility import committed_run_provenance

    committed_provenance = committed_run_provenance(module.read_text())
    if committed_provenance is None:
        return None
    if committed_provenance != derived_provenance:
        raise ValueError(
            "existing wave predictionRun provenance differs from derived batch "
            f"provenance: {committed_provenance} != {derived_provenance}"
        )
    return committed_provenance


def install_wave_candidate(candidate: pathlib.Path, module: pathlib.Path) -> None:
    """Install a generated wave without ever rewriting a prior module."""

    candidate_bytes = candidate.read_bytes()
    if module.exists():
        if module.is_symlink() or not module.is_file():
            raise ValueError(f"wave destination is not a regular file: {module}")
        if module.read_bytes() != candidate_bytes:
            raise ValueError(
                "refusing to overwrite non-identical generated wave: "
                f"{module.relative_to(ROOT)}"
            )
        return
    module.parent.mkdir(parents=True, exist_ok=True)
    module.write_bytes(candidate_bytes)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--batch", action="append", required=True)
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()

    batch_payloads = [json.loads(pathlib.Path(path).read_text()) for path in args.batch]
    derived_provenance = derive_batch_provenance(batch_payloads)
    winners: dict[str, str] = {}
    wanted: set[str] = set()
    registration_paths: set[pathlib.Path] = set()
    for batch in batch_payloads:
        for result in batch["results"]:
            slug = result["target"]["catalogSlug"]
            wanted.add(slug)
            registration_path = result["target"].get("targetRegistrationPath")
            if registration_path:
                registration_paths.add(ROOT / registration_path)
            if result["ok"] and result.get("cellsPath"):
                winners[slug] = result["cellsPath"]

    missing = sorted(wanted - set(winners))
    # The untrusted artifact contains data only. Recreate/verify the
    # preregistration blocks from canonical snapshots before finalizing them
    # from validated cell JSON below. This also preserves failed-run retries.
    materialize_registration_snapshots(sorted(registration_paths))
    if missing:
        print(f"no passing run for: {', '.join(missing)}", file=sys.stderr)
        if not args.allow_missing:
            return 1
    if not winners:
        print("no publishable cells", file=sys.stderr)
        return 2

    const = re.sub(r"[^A-Z0-9]+", "_", args.name.upper()).strip("_") + "_WAVE"
    module = EXAMPLES / f"{args.name}.ts"
    run_files = sorted(set(winners.values()))
    provenance = replay_provenance_for_module(module, derived_provenance)

    with tempfile.TemporaryDirectory(prefix="thesis-wave-") as temp_dir:
        candidate = pathlib.Path(temp_dir) / module.name
        subprocess.run(
            converter_command(
                candidate,
                const,
                run_files,
                args.batch,
                module,
                provenance,
            ),
            check=True,
        )
        install_wave_candidate(candidate, module)
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_ledger_targets.py"),
            *run_files,
        ],
        check=True,
    )

    source = CELLS_TS.read_text()
    import_line = f'import {{ {const} }} from "./forecast-examples/{args.name}";'
    if import_line not in source:
        anchor = re.search(
            r'^import \{ [A-Z0-9_]+ \} from "\./forecast-examples/[^"]+";$',
            source,
            re.MULTILINE,
        )
        assert anchor, "no forecast-examples import anchor found"
        source = source.replace(
            anchor.group(0), anchor.group(0) + "\n" + import_line, 1
        )
        spread = re.search(r"^  \.\.\.[A-Z0-9_]+,$", source, re.MULTILINE)
        assert spread, "no wave spread anchor found"
        source = source.replace(
            spread.group(0), spread.group(0) + f"\n  ...{const},", 1
        )
        CELLS_TS.write_text(source)
        print(f"registered {const} in forecast-cells.ts")
    print(f"published {len(winners)} cells -> {module.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
