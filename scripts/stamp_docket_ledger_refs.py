#!/usr/bin/env python3
"""Stamp docket series with canonical PolicyEngine Ledger catalog references.

Canonical concept matches take precedence over aliases. This matters because a
legacy catalog row may retain another row's canonical concept as an alias. An
alias-only docket match must be unique; missing and ambiguous matches are
reported together before the docket file is changed.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_DOCKET = ROOT / "scripts" / "docket_series.json"


class StampError(ValueError):
    """The docket cannot be mapped uniquely into the ledger catalog."""


def _object(path: pathlib.Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StampError(f"cannot read {label} {path}: {exc}") from exc
    if type(value) is not dict:
        raise StampError(f"{label} must be a JSON object: {path}")
    return value


def stamp_docket(
    catalog: dict[str, Any], docket: dict[str, Any]
) -> tuple[dict[str, Any], list[tuple[str, str]]]:
    """Return a stamped docket and the alias-to-concept matches used."""

    catalog_rows = catalog.get("series")
    docket_rows = docket.get("series")
    if type(catalog_rows) is not list:
        raise StampError("catalog.series must be a list")
    if type(docket_rows) is not list:
        raise StampError("docket.series must be a list")

    concepts: dict[str, dict[str, Any]] = {}
    aliases: dict[str, list[dict[str, Any]]] = {}
    catalog_errors: list[str] = []
    for index, row in enumerate(catalog_rows):
        if type(row) is not dict:
            catalog_errors.append(f"catalog series[{index}] is not an object")
            continue
        concept = row.get("concept")
        uuid = row.get("uuid")
        row_aliases = row.get("aliases")
        if type(concept) is not str or not concept:
            catalog_errors.append(f"catalog series[{index}] has no concept")
            continue
        if type(uuid) is not str or not uuid:
            catalog_errors.append(f"catalog concept {concept!r} has no uuid")
            continue
        if concept in concepts:
            catalog_errors.append(f"duplicate catalog concept {concept!r}")
            continue
        if type(row_aliases) is not list or any(
            type(alias) is not str for alias in row_aliases
        ):
            catalog_errors.append(
                f"catalog concept {concept!r} aliases must be a string list"
            )
            continue
        concepts[concept] = row
        for alias in row_aliases:
            aliases.setdefault(alias, []).append(row)
    if catalog_errors:
        raise StampError("invalid catalog:\n- " + "\n- ".join(catalog_errors))

    missing: list[str] = []
    ambiguous: list[str] = []
    matches: list[tuple[dict[str, Any], dict[str, Any], str]] = []
    for index, entry in enumerate(docket_rows):
        if type(entry) is not dict or type(entry.get("series")) is not str:
            missing.append(f"series[{index}] has no string series identifier")
            continue
        name = entry["series"]
        row = concepts.get(name)
        match_kind = "concept"
        if row is None:
            candidates = aliases.get(name, [])
            if not candidates:
                missing.append(name)
                continue
            if len(candidates) != 1:
                candidate_names = sorted(str(item["concept"]) for item in candidates)
                ambiguous.append(f"{name}: {', '.join(candidate_names)}")
                continue
            row = candidates[0]
            match_kind = "alias"
        matches.append((entry, row, match_kind))

    problems: list[str] = []
    if missing:
        problems.append("no catalog row:\n- " + "\n- ".join(sorted(missing)))
    if ambiguous:
        problems.append("ambiguous catalog alias:\n- " + "\n- ".join(sorted(ambiguous)))
    if problems:
        raise StampError("cannot stamp docket:\n" + "\n".join(problems))

    alias_matches: list[tuple[str, str]] = []
    for entry, row, match_kind in matches:
        entry["ledger"] = {"uuid": row["uuid"], "concept": row["concept"]}
        if match_kind == "alias":
            alias_matches.append((entry["series"], row["concept"]))
    return docket, alias_matches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True, type=pathlib.Path)
    parser.add_argument("--docket", type=pathlib.Path, default=DEFAULT_DOCKET)
    args = parser.parse_args()

    try:
        catalog = _object(args.catalog, "catalog")
        docket = _object(args.docket, "docket")
        stamped, alias_matches = stamp_docket(catalog, docket)
        output = json.dumps(stamped, indent=2) + "\n"
        previous = args.docket.read_text()
        if output != previous:
            args.docket.write_text(output)
            disposition = "updated"
        else:
            disposition = "unchanged"
    except StampError as exc:
        print(f"docket ledger stamping failed: {exc}", file=sys.stderr)
        return 1

    print(f"{disposition} {args.docket}: {len(stamped['series'])} ledger references")
    for source, concept in alias_matches:
        print(f"alias match: {source} -> {concept}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
