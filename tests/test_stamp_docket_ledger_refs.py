from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from stamp_docket_ledger_refs import StampError, stamp_docket  # noqa: E402


def _catalog() -> dict:
    return {
        "series": [
            {
                "uuid": "direct-uuid",
                "concept": "direct.series",
                "aliases": [],
            },
            {
                "uuid": "legacy-uuid",
                "concept": "legacy.series",
                "aliases": ["direct.series", "alias.series"],
            },
        ]
    }


def test_canonical_concept_precedes_alias_and_alias_match_records_concept() -> None:
    docket = {
        "comment": "fixture",
        "series": [
            {"series": "direct.series", "cadence": "monthly", "slug": "a"},
            {"series": "alias.series", "cadence": "monthly", "slug": "b"},
        ],
    }

    stamped, aliases = stamp_docket(_catalog(), docket)

    assert stamped["series"][0]["ledger"] == {
        "uuid": "direct-uuid",
        "concept": "direct.series",
    }
    assert stamped["series"][1]["ledger"] == {
        "uuid": "legacy-uuid",
        "concept": "legacy.series",
    }
    assert aliases == [("alias.series", "legacy.series")]
    assert list(stamped["series"][0]) == ["series", "cadence", "slug", "ledger"]


def test_missing_docket_series_are_listed_together() -> None:
    docket = {
        "series": [
            {"series": "missing.b", "cadence": "monthly", "slug": "b"},
            {"series": "missing.a", "cadence": "monthly", "slug": "a"},
        ]
    }

    with pytest.raises(StampError) as exc_info:
        stamp_docket(_catalog(), docket)

    assert "missing.a" in str(exc_info.value)
    assert "missing.b" in str(exc_info.value)


def test_cli_is_idempotent_and_writes_indent_two_with_trailing_newline(
    tmp_path: pathlib.Path,
) -> None:
    catalog_path = tmp_path / "catalog.json"
    docket_path = tmp_path / "docket.json"
    catalog_path.write_text(json.dumps(_catalog(), indent=2) + "\n")
    docket_path.write_text(
        json.dumps(
            {
                "series": [
                    {
                        "series": "alias.series",
                        "cadence": "monthly",
                        "slug": "alias",
                    }
                ]
            },
            indent=2,
        )
        + "\n"
    )
    command = [
        sys.executable,
        str(ROOT / "scripts" / "stamp_docket_ledger_refs.py"),
        "--catalog",
        str(catalog_path),
        "--docket",
        str(docket_path),
    ]

    first = subprocess.run(command, check=True, capture_output=True, text=True)
    first_bytes = docket_path.read_bytes()
    second = subprocess.run(command, check=True, capture_output=True, text=True)

    assert "updated" in first.stdout
    assert "alias match: alias.series -> legacy.series" in first.stdout
    assert "unchanged" in second.stdout
    assert docket_path.read_bytes() == first_bytes
    assert first_bytes.endswith(b"\n")
    assert b'  "series": [' in first_bytes
