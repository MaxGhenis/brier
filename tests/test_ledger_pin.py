from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pin_ledger  # noqa: E402
import register_targets  # noqa: E402
from register_targets import (  # noqa: E402
    RegistrationError,
    registration_content_hash,
    validate_ledger_pin_binding,
)


def _pin_binding() -> dict:
    return {
        "repo": "PolicyEngine/ledger",
        "branch": "codex/thesis-ledger-facts",
        "sha": "a" * 40,
        "jsonlSha256": "b" * 64,
        "lineCount": 107,
    }


def test_refresh_refuses_a_rewritten_ledger_line() -> None:
    previous = ['{"source_record_id":"a"}', '{"source_record_id":"b"}']
    rewritten = ['{"source_record_id":"a","value":9}', '{"source_record_id":"b"}']

    with pytest.raises(pin_ledger.PinError, match="rewrites ledger line 1"):
        pin_ledger._require_extension(previous, rewritten, label="commit test")


def test_refresh_refuses_a_truncated_ledger() -> None:
    previous = ['{"source_record_id":"a"}', '{"source_record_id":"b"}']

    with pytest.raises(pin_ledger.PinError, match="truncates the ledger"):
        pin_ledger._require_extension(previous, previous[:1], label="commit test")


def test_refresh_accepts_a_pure_append() -> None:
    previous = ['{"source_record_id":"a"}']
    appended = ['{"source_record_id":"a"}', '{"source_record_id":"b"}']

    pin_ledger._require_extension(previous, appended, label="commit test")


def test_v3_registration_hash_commits_to_the_ledger_pin() -> None:
    snapshot = {
        "schemaVersion": "thesis_target_registration_v3",
        "registeredAtUtc": "2030-01-01T00:00:00Z",
        "targets": [{"dataPointId": "test.series.2030"}],
        "ledgerPin": _pin_binding(),
    }

    baseline = registration_content_hash(snapshot)
    moved_pin = {
        **snapshot,
        "ledgerPin": {**_pin_binding(), "lineCount": 108},
    }

    assert registration_content_hash(moved_pin) != baseline


def test_v3_registration_requires_the_ledger_pin() -> None:
    snapshot = {
        "schemaVersion": "thesis_target_registration_v3",
        "registeredAtUtc": "2030-01-01T00:00:00Z",
        "targets": [{"dataPointId": "test.series.2030"}],
    }

    with pytest.raises(RegistrationError, match="missing=\\['ledgerPin'\\]"):
        registration_content_hash(snapshot)


def test_v2_registration_hashes_remain_stable() -> None:
    snapshot = {
        "schemaVersion": "thesis_target_registration_v2",
        "registeredAtUtc": "2030-01-01T00:00:00Z",
        "targets": [{"dataPointId": "test.series.2030"}],
    }

    # v2 predates the pin; its payload must not gain one retroactively.
    assert registration_content_hash(snapshot) == registration_content_hash(
        dict(snapshot)
    )
    with pytest.raises(RegistrationError):
        registration_content_hash({**snapshot, "ledgerPin": _pin_binding()})


def test_pin_binding_validation_fails_closed() -> None:
    with pytest.raises(RegistrationError, match="bind exactly"):
        validate_ledger_pin_binding({**_pin_binding(), "extra": 1})
    with pytest.raises(RegistrationError, match="commit SHA"):
        validate_ledger_pin_binding({**_pin_binding(), "sha": "main"})
    with pytest.raises(RegistrationError, match="lineCount"):
        validate_ledger_pin_binding({**_pin_binding(), "lineCount": -1})


def test_registration_reads_the_committed_pin(monkeypatch, tmp_path) -> None:
    pin_path = tmp_path / "ledger-pin.json"
    pin_path.write_text(
        json.dumps(
            {
                "schemaVersion": "thesis_ledger_pin_v1",
                **_pin_binding(),
                "jsonlBytes": 12345,
                "pinnedAtUtc": "2030-01-01T00:00:00Z",
            }
        )
    )
    monkeypatch.setattr(register_targets, "LEDGER_PIN_PATH", pin_path)

    binding = register_targets.load_ledger_pin_binding()

    assert binding == _pin_binding()


def test_registration_without_a_pin_file_fails_closed(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setattr(
        register_targets, "LEDGER_PIN_PATH", tmp_path / "missing.json"
    )

    with pytest.raises(RegistrationError, match="committed ledger pin"):
        register_targets.load_ledger_pin_binding()
