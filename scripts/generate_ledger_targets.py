#!/usr/bin/env python3
"""Append target registrations for spawned cells to ledger-targets.generated.ts.

Every published forecast must have a Thesis target ledger entry for its
dataPointId (requireLedgerTarget throws at build time otherwise). Hand-authored
entries live in ledger-targets.ts; everything spawned by the thesis.analyst
pipeline registers here.  Docket targets are preregistered by
``register_targets.py``; publication verifies and finalizes that entry rather
than allowing the forecast to create its own grading contract.

Usage:
  python3 scripts/generate_ledger_targets.py CELLS1.json [CELLS2.json ...]

Idempotent: dataPointIds already registered in either ledger file are skipped.
"""

import json
import pathlib
import re
import sys
from urllib.parse import urlparse

from register_targets import registration_for_cell

ROOT = pathlib.Path(__file__).resolve().parents[1]
GENERATED = ROOT / "site" / "src" / "data" / "ledger-targets.generated.ts"
HAND_AUTHORED = ROOT / "site" / "src" / "data" / "ledger-targets.ts"


def registered_data_point_ids() -> set[str]:
    ids = set()
    for path in (GENERATED, HAND_AUTHORED):
        ids.update(re.findall(r'dataPointId:\s*\n?\s*"([^"]+)"', path.read_text()))
    return ids


def entry_for(cell: dict, registration: dict | None = None) -> dict:
    entry = {
        "kind": "target_registered",
        "dataPointId": cell["dataPointId"],
        "observationId": f"obs.{cell['dataPointId']}",
        "country": cell["country"],
        "periodLabel": cell["resolutionDate"],
        "unit": cell["unit"],
        "resolutionDate": cell["resolutionDate"],
        "resolutionSource": cell["resolutionSource"],
        "resolutionSourceUrl": cell.get("resolutionSourceUrl"),
        "resolutionRule": cell["resolutionRule"],
        "resolutionPolicy": "first_print",
        "sourceKind": "official_release",
        "source": cell["resolutionSource"],
        "sourceUrl": cell.get("resolutionSourceUrl"),
        "note": (
            "Target registration generated from the recorded thesis.analyst "
            f"run for {cell['title']}."
        ),
    }
    if registration:
        entry.update(
            {
                key: registration[key]
                for key in (
                    "registeredAt",
                    "targetContentHash",
                    "series",
                    "period",
                    "catalogSlug",
                    "valueScale",
                    "sourceBinding",
                    "resolutionDateBasis",
                    # The pinned ledger state must survive publication, or the
                    # site's N5 backfill gate (which fires only when
                    # ledgerPinLineCount is a number) silently skips the
                    # published target and a backfilled print could grade it.
                    "ledgerPinSha",
                    "ledgerPinLineCount",
                )
                if key in registration
            }
        )
        entry["registrationState"] = "published"
    return {k: v for k, v in entry.items() if v is not None}


def ts_literal(entry: dict) -> str:
    lines = ["  {"]
    for key, value in entry.items():
        lines.append(f"    {key}: {json.dumps(value, ensure_ascii=False)},")
    lines.append("  },")
    return "\n".join(lines)


def generated_entry_blocks(source: str) -> list[re.Match[str]]:
    return list(re.finditer(r"^  \{\n(?:    .*\n)*?  \},$", source, re.MULTILINE))


def block_value(block: str, key: str):
    match = re.search(rf"^    {re.escape(key)}: (.*),$", block, re.MULTILINE)
    return json.loads(match.group(1)) if match else None


def generated_entry_for(
    source: str, data_point_id: str
) -> re.Match[str] | None:
    return next(
        (
            match
            for match in generated_entry_blocks(source)
            if block_value(match.group(0), "dataPointId") == data_point_id
        ),
        None,
    )


def preregistration_for(
    source: str, data_point_id: str
) -> tuple[re.Match[str], dict] | None:
    for match in generated_entry_blocks(source):
        block = match.group(0)
        if block_value(block, "dataPointId") != data_point_id:
            continue
        if block_value(block, "registrationState") != "preregistered":
            return None
        keys = (
            "unit",
            "registeredAt",
            "targetContentHash",
            "series",
            "period",
            "catalogSlug",
            "valueScale",
            "sourceBinding",
            "resolutionDateBasis",
        )
        return match, {key: block_value(block, key) for key in keys}
    return None


def validate_preregistered_contract(cell: dict, registration: dict) -> None:
    if cell.get("unit") != registration.get("unit"):
        raise ValueError(
            f"unit {cell.get('unit')!r} does not match preregistration "
            f"{registration.get('unit')!r} for {cell.get('dataPointId')}"
        )
    binding = registration.get("sourceBinding") or {}
    allowed_hosts = {
        str(host).strip().lower()
        for host in (binding.get("allowedHosts") or [])
        if str(host).strip()
    }
    source_host = (
        urlparse(str(binding.get("sourceUrl") or "")).hostname or ""
    ).lower()
    if source_host:
        allowed_hosts.add(source_host)
    actual_host = (
        urlparse(str(cell.get("resolutionSourceUrl") or "")).hostname or ""
    ).lower()
    if not allowed_hosts or actual_host not in allowed_hosts:
        raise ValueError(
            f"resolution source host {actual_host!r} is not among the "
            f"preregistered source binding hosts {sorted(allowed_hosts)!r} "
            f"for {cell.get('dataPointId')}"
        )


def main() -> int:
    cells = []
    for path in sys.argv[1:]:
        cells.extend(json.load(open(path)))
    existing = registered_data_point_ids()
    source = GENERATED.read_text()
    new_entries = []
    replacements: list[tuple[int, int, str]] = []
    finalized_ids: set[str] = set()
    for cell in cells:
        if cell.get("targetRegistrationPath"):
            if cell["dataPointId"] in finalized_ids:
                continue
            registration = registration_for_cell(cell)
            validate_preregistered_contract(cell, registration)
            match = generated_entry_for(source, cell["dataPointId"])
            if match is None:
                raise ValueError(
                    "registered cell has no generated preregistration for "
                    f"{cell['dataPointId']}"
                )
            expected = ts_literal(entry_for(cell, registration))
            state = block_value(match.group(0), "registrationState")
            if state == "preregistered":
                replacements.append((match.start(), match.end(), expected))
            elif state != "published" or match.group(0) != expected:
                raise ValueError(
                    "published generated target differs from canonical "
                    f"registration and cell for {cell['dataPointId']}"
                )
            finalized_ids.add(cell["dataPointId"])
            continue
        if cell["dataPointId"] in existing:
            if cell["dataPointId"] in finalized_ids:
                continue
            preregistration = preregistration_for(source, cell["dataPointId"])
            if preregistration:
                match, registration = preregistration
                validate_preregistered_contract(cell, registration)
                replacements.append(
                    (
                        match.start(),
                        match.end(),
                        ts_literal(entry_for(cell, registration)),
                    )
                )
                finalized_ids.add(cell["dataPointId"])
            continue
        existing.add(cell["dataPointId"])
        new_entries.append(entry_for(cell))
    if not new_entries and not replacements:
        print("nothing to register")
        return 0
    for start, end, replacement in sorted(replacements, reverse=True):
        source = source[:start] + replacement + source[end:]
    closer = "] satisfies" if "] satisfies" in source else "];"
    idx = source.rindex(closer)
    block = ""
    if new_entries:
        block = "\n".join(ts_literal(entry) for entry in new_entries) + "\n"
    GENERATED.write_text(source[:idx] + block + source[idx:])
    print(
        f"registered {len(new_entries)} and finalized {len(replacements)} "
        f"targets -> {GENERATED}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
