from __future__ import annotations

import datetime as dt
import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_ledger_targets  # noqa: E402
import register_targets  # noqa: E402
import register_wave  # noqa: E402
from canonical_json import canonical_bytes, canonical_sha256  # noqa: E402


def sample_target() -> dict:
    return {
        "series": "agency.test.rate",
        "period": "2030-01",
        "catalogSlug": "agency-test-rate-january-2030",
        "targetUnit": "percent",
        "valueScale": 1,
        "previousTarget": {
            "period": "2029-12",
            "dataPointId": "agency.test.rate.2029_12.first_print",
            "country": "US",
            "unit": "percent",
            "resolutionDate": "2030-01-15",
            "resolutionSource": "Agency table A",
            "resolutionSourceUrl": "https://data.example.gov/table-a",
        },
    }


def configure_registration_root(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> pathlib.Path:
    generated = tmp_path / "ledger-targets.generated.ts"
    generated.write_text(
        'import type { TargetRegisteredLedgerEntry } from "./ledger-targets";\n'
        "export const GENERATED_FORECAST_TARGETS = [\n"
        "] satisfies TargetRegisteredLedgerEntry[];\n"
    )
    monkeypatch.setattr(register_targets, "ROOT", tmp_path)
    monkeypatch.setattr(register_targets, "GENERATED_TARGETS", generated)
    return generated


def configure_generator_root(
    tmp_path: pathlib.Path,
    generated: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    hand_authored = tmp_path / "ledger-targets.ts"
    hand_authored.write_text("export const TARGETS = [];\n")
    monkeypatch.setattr(generate_ledger_targets, "ROOT", tmp_path)
    monkeypatch.setattr(generate_ledger_targets, "GENERATED", generated)
    monkeypatch.setattr(generate_ledger_targets, "HAND_AUTHORED", hand_authored)


def test_registration_snapshot_round_trip_and_hash_stability(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    generated = configure_registration_root(tmp_path, monkeypatch)

    registration_date = dt.date(2030, 1, 10)
    registered_at_utc = "2030-01-10T14:32:05Z"
    target = sample_target()
    reordered = dict(reversed(list(target.items())))
    snapshot = register_targets.build_snapshot(
        [target], registration_date, registered_at_utc
    )
    reordered_snapshot = register_targets.build_snapshot(
        [reordered], registration_date, registered_at_utc
    )
    later_snapshot = register_targets.build_snapshot(
        [target], registration_date, "2030-01-10T23:59:59Z"
    )
    content_hash = register_targets.registration_content_hash(snapshot)
    assert content_hash == register_targets.registration_content_hash(
        reordered_snapshot
    )
    assert content_hash == register_targets.registration_content_hash(later_snapshot)
    assert canonical_sha256(snapshot) != canonical_sha256(later_snapshot)
    with pytest.raises(
        register_targets.RegistrationError, match="top-level fields do not match"
    ):
        register_targets.registration_content_hash({**snapshot, "backdatedBy": "agent"})

    targets_path = tmp_path / "targets.json"
    targets_path.write_text(json.dumps({"targets": [target]}))
    registrations = register_targets.register(
        targets_path, registration_date, registered_at_utc
    )
    assert len(registrations) == 1
    registration = registrations[0]
    snapshot_path = registration["path"]
    snapshot = registration["snapshot"]

    assert registration["existing"] is False
    assert registration["registeredAtUtc"] == registered_at_utc
    assert registration["targetContentHash"] == content_hash
    assert snapshot_path.name == f"2030-01-10-{content_hash}.json"
    assert snapshot_path.read_bytes() == canonical_bytes(snapshot) + b"\n"
    assert snapshot["registeredAtUtc"] == registered_at_utc
    assert (
        register_targets.registration_content_hash(
            json.loads(snapshot_path.read_text())
        )
        == content_hash
    )
    round_trip = json.loads(targets_path.read_text())["targets"][0]
    contract = snapshot["targets"][0]
    assert contract["dataPointId"] == "agency.test.rate.2030_01.first_print"
    assert round_trip["dataPointId"] == contract["dataPointId"]
    assert round_trip["sourceBinding"] == contract["sourceBinding"]
    assert round_trip["registeredAt"] == registered_at_utc
    assert round_trip["registeredAtUtc"] == registered_at_utc
    assert round_trip["targetContentHash"] == content_hash
    assert round_trip["targetRegistrationPath"].startswith("records/targets/")
    generated_text = generated.read_text()
    assert 'registrationState: "preregistered"' in generated_text
    assert f'registeredAt: "{registered_at_utc}"' in generated_text
    assert f'targetContentHash: "{content_hash}"' in generated_text
    preregistration = generate_ledger_targets.preregistration_for(
        generated_text, contract["dataPointId"]
    )
    assert preregistration is not None
    _, registration = preregistration
    cell = {
        "dataPointId": contract["dataPointId"],
        "unit": "percent",
        "resolutionSourceUrl": "https://data.example.gov/releases/january",
        "country": "US",
        "resolutionDate": "2030-02-15",
        "resolutionSource": "Agency table A",
        "resolutionRule": "First published January 2030 value.",
        "title": "Agency test rate",
    }
    generate_ledger_targets.validate_preregistered_contract(cell, registration)
    assert (
        generate_ledger_targets.entry_for(cell, registration)["registrationState"]
        == "published"
    )


def test_registration_retry_reuses_immutable_snapshot_and_generated_target(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    generated = configure_registration_root(tmp_path, monkeypatch)
    targets_path = tmp_path / "targets.json"
    targets_path.write_text(json.dumps({"targets": [sample_target()]}))

    [original] = register_targets.register(
        targets_path,
        dt.date(2030, 1, 10),
        "2030-01-10T14:32:05Z",
    )
    original_path = original["path"]
    original_snapshot_bytes = original_path.read_bytes()
    original_generated_bytes = generated.read_bytes()

    # A later workflow retry receives the unregistered docket target again.
    targets_path.write_text(json.dumps({"targets": [sample_target()]}))
    [retry] = register_targets.register(
        targets_path,
        dt.date(2030, 1, 11),
        "2030-01-11T09:08:07Z",
    )

    assert retry["existing"] is True
    assert retry["path"] == original_path
    assert retry["registeredAtUtc"] == "2030-01-10T14:32:05Z"
    assert retry["targetContentHash"] == original["targetContentHash"]
    assert original_path.read_bytes() == original_snapshot_bytes
    assert generated.read_bytes() == original_generated_bytes
    round_trip = json.loads(targets_path.read_text())["targets"][0]
    assert round_trip["registeredAt"] == "2030-01-10T14:32:05Z"
    assert round_trip["registeredAtUtc"] == "2030-01-10T14:32:05Z"
    assert round_trip["targetRegistrationPath"] == original_path.relative_to(
        tmp_path
    ).as_posix()


def test_registration_retry_fails_closed_on_generated_target_mismatch(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    generated = configure_registration_root(tmp_path, monkeypatch)
    targets_path = tmp_path / "targets.json"
    raw_targets = json.dumps({"targets": [sample_target()]})
    targets_path.write_text(raw_targets)
    [original] = register_targets.register(
        targets_path,
        dt.date(2030, 1, 10),
        "2030-01-10T14:32:05Z",
    )
    snapshot_bytes = original["path"].read_bytes()

    generated.write_text(
        generated.read_text().replace(
            'registeredAt: "2030-01-10T14:32:05Z"',
            'registeredAt: "1999-12-31T23:59:59Z"',
            1,
        )
    )
    mismatched_generated_bytes = generated.read_bytes()
    targets_path.write_text(raw_targets)

    with pytest.raises(
        register_targets.RegistrationError,
        match="not the exact immutable preregistration",
    ):
        register_targets.register(
            targets_path,
            dt.date(2030, 1, 11),
            "2030-01-11T09:08:07Z",
        )

    assert original["path"].read_bytes() == snapshot_bytes
    assert generated.read_bytes() == mismatched_generated_bytes
    assert targets_path.read_text() == raw_targets


def test_empty_registration_is_a_byte_identical_no_op(
    tmp_path: pathlib.Path, monkeypatch
) -> None:
    generated = configure_registration_root(tmp_path, monkeypatch)
    generated_bytes = generated.read_bytes()
    targets_path = tmp_path / "targets.json"
    targets_path.write_text('{"targets": []}\n')
    targets_bytes = targets_path.read_bytes()

    assert (
        register_targets.register(
            targets_path,
            dt.date(2030, 1, 10),
            "2030-01-10T14:32:05Z",
        )
        == []
    )

    assert targets_path.read_bytes() == targets_bytes
    assert generated.read_bytes() == generated_bytes
    assert not (tmp_path / "records" / "targets").exists()


def test_bind_registration_commits_uses_snapshot_introducing_commit(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generated = configure_registration_root(tmp_path, monkeypatch)
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "add", generated.name], cwd=tmp_path, check=True, capture_output=True
    )
    commit_args = [
        "git",
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
    ]
    subprocess.run(
        [*commit_args, "-m", "base"], cwd=tmp_path, check=True, capture_output=True
    )
    targets_path = tmp_path / "targets.json"
    targets_path.write_text(json.dumps({"targets": [sample_target()]}))
    register_targets.register(
        targets_path,
        dt.date(2030, 1, 10),
        "2030-01-10T14:32:05Z",
    )
    subprocess.run(
        ["git", "add", "records/targets", generated.name],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [*commit_args, "-m", "register"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True
    ).strip()

    metadata = register_targets.bind_registration_commits(targets_path, head)

    target = json.loads(targets_path.read_text())["targets"][0]
    assert target["registrationCommit"] == head
    assert metadata["sourceCommit"] == head
    assert metadata["registrationCommits"] == [head]


def test_publisher_regenerates_typescript_from_canonical_snapshot(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generated = configure_registration_root(tmp_path, monkeypatch)
    empty_module = generated.read_bytes()
    targets_path = tmp_path / "targets.json"
    targets_path.write_text(json.dumps({"targets": [sample_target()]}))
    [registration] = register_targets.register(
        targets_path,
        dt.date(2030, 1, 10),
        "2030-01-10T14:32:05Z",
    )
    expected = generated.read_bytes()

    generated.write_bytes(empty_module)
    register_targets.materialize_registration_snapshots([registration["path"]])

    assert generated.read_bytes() == expected


def test_wave_install_is_append_only(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(register_wave, "ROOT", tmp_path)
    module = tmp_path / "site/src/data/forecast-examples/auto-full-hash.ts"
    candidate = tmp_path / "candidate.ts"
    candidate.write_text("trusted candidate\n")

    register_wave.install_wave_candidate(candidate, module)
    register_wave.install_wave_candidate(candidate, module)
    assert module.read_bytes() == candidate.read_bytes()

    candidate.write_text("different candidate\n")
    with pytest.raises(ValueError, match="refusing to overwrite"):
        register_wave.install_wave_candidate(candidate, module)
    assert module.read_text() == "trusted candidate\n"


def test_published_target_is_exactly_regenerated_and_retry_safe(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generated = configure_registration_root(tmp_path, monkeypatch)
    configure_generator_root(tmp_path, generated, monkeypatch)
    raw_target_payload = json.dumps({"targets": [sample_target()]})
    targets_path = tmp_path / "targets.json"
    targets_path.write_text(raw_target_payload)
    [registration] = register_targets.register(
        targets_path,
        dt.date(2030, 1, 10),
        "2030-01-10T14:32:05Z",
    )
    target = json.loads(targets_path.read_text())["targets"][0]
    cell = {
        "slug": target["catalogSlug"],
        "dataPointId": target["dataPointId"],
        "unit": target["targetUnit"],
        "country": target["country"],
        "resolutionDate": "2030-02-15",
        "resolutionSource": "Agency table A",
        "resolutionSourceUrl": "https://data.example.gov/releases/january",
        "resolutionRule": "First published January 2030 value.",
        "title": "Agency test rate",
        "targetRegistrationPath": target["targetRegistrationPath"],
        "targetContentHash": target["targetContentHash"],
        "registeredAtUtc": target["registeredAtUtc"],
    }
    cells_path = tmp_path / "cells.json"
    cells_path.write_text(json.dumps([cell]))
    monkeypatch.setattr(sys, "argv", ["generate_ledger_targets.py", str(cells_path)])

    assert generate_ledger_targets.main() == 0
    published = generated.read_bytes()
    assert 'registrationState: "published"' in published.decode()

    # Post-commit regeneration and a later registration retry are byte-exact.
    assert generate_ledger_targets.main() == 0
    register_targets.materialize_registration_snapshots([registration["path"]])
    assert generated.read_bytes() == published
    targets_path.write_text(raw_target_payload)
    [retry] = register_targets.register(
        targets_path,
        dt.date(2030, 1, 11),
        "2030-01-11T09:08:07Z",
    )
    assert retry["existing"] is True
    assert generated.read_bytes() == published

    generated.write_text(
        generated.read_text().replace(
            'resolutionSource: "Agency table A"',
            'resolutionSource: "Tampered table"',
            1,
        )
    )
    with pytest.raises(ValueError, match="differs from canonical"):
        generate_ledger_targets.main()


def test_claims_binding_is_data_driven_and_advance_vintage() -> None:
    contract = register_targets.build_contract(
        {
            "series": "us.dol.initial_claims.sa",
            "period": "week_2030-01-05",
            "catalogSlug": "initial-claims-week-2030-01-05",
            "targetUnit": "thousands",
            "valueScale": 0.001,
        },
        dt.date(2030, 1, 6),
    )

    assert contract["dataPointId"] == "us.dol.initial_claims.sa.week_2030-01-05"
    assert contract["sourceBinding"] == {
        "adapter": "alfred-fred",
        "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA",
        "sourceSeriesId": "ICSA",
        "field": "ICSA",
        "table": "ALFRED graph CSV",
        "transform": {"operation": "multiply", "factor": 0.001},
        "releasePolicy": "advance_vintage",
        "allowedHosts": ["alfred.stlouisfed.org"],
        "expectedReleaseWindow": {"start": "2030-01-08", "end": "2030-01-12"},
    }


def test_publisher_contract_enforces_allowed_hosts_membership() -> None:
    registration = {
        "unit": "thousands",
        "sourceBinding": {
            "sourceUrl": "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=ICSA",
            "allowedHosts": ["alfred.stlouisfed.org", "www.dol.gov"],
        },
    }
    cell = {
        "dataPointId": "us.dol.initial_claims.sa.week_2030-01-05",
        "unit": "thousands",
        "resolutionSourceUrl": "https://www.dol.gov/ui/data.pdf",
    }
    generate_ledger_targets.validate_preregistered_contract(cell, registration)

    with pytest.raises(ValueError, match="not among the preregistered"):
        generate_ledger_targets.validate_preregistered_contract(
            dict(cell, resolutionSourceUrl="https://evil.example/data"),
            registration,
        )

    legacy = {
        "unit": "thousands",
        "sourceBinding": {"sourceUrl": "https://alfred.stlouisfed.org/g.csv"},
    }
    generate_ledger_targets.validate_preregistered_contract(
        dict(cell, resolutionSourceUrl="https://alfred.stlouisfed.org/g.csv"),
        legacy,
    )
    with pytest.raises(ValueError, match="not among the preregistered"):
        generate_ledger_targets.validate_preregistered_contract(cell, legacy)

    with pytest.raises(ValueError, match="not among the preregistered"):
        generate_ledger_targets.validate_preregistered_contract(
            cell, {"unit": "thousands", "sourceBinding": {}}
        )
