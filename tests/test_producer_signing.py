from __future__ import annotations

import builtins
import hashlib
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import producer_signing_pins as producer_pins  # noqa: E402
import verify_record_chain as record_chain  # noqa: E402
from receipt.sign import (  # noqa: E402
    generate_signing_keypair,
    sign_payload,
    spki_sha256,
)
from verify_record_chain import ChainError, verify_chain  # noqa: E402


def write_json(path: pathlib.Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def add_witness(snapshot: pathlib.Path) -> None:
    write_json(
        snapshot.with_suffix(".witness.json"),
        {
            "schemaVersion": "thesis_rfc3161_witness_v1",
            "status": "unavailable",
            "digestSha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
            "reason": "synthetic producer-signing fixture",
        },
    )


def logical(records: pathlib.Path, path: pathlib.Path) -> str:
    return f"records/{path.relative_to(records).as_posix()}"


@pytest.fixture
def synthetic_chain(
    tmp_path: pathlib.Path,
) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path]:
    records = tmp_path / "records"
    first = records / "2026-01-01" / "digest-genesis.json"
    write_json(
        first,
        {
            "schemaVersion": "thesis_record_snapshot_v2",
            "snapshotKind": "chain_genesis",
            "runId": "genesis",
            "recordedAt": "2026-01-01T00:00:00Z",
        },
    )
    add_witness(first)

    activation = records / "2026-01-02" / "digest-activation.json"
    write_json(
        activation,
        {
            "schemaVersion": "thesis_record_snapshot_v2",
            "snapshotKind": "recorder_run",
            "runId": "activation",
            "recordedAt": "2026-01-02T00:00:00Z",
            "chain": {
                "prevDigestPath": logical(records, first),
                "prevDigestSha256": hashlib.sha256(first.read_bytes()).hexdigest(),
            },
        },
    )
    add_witness(activation)

    post_activation = records / "2026-01-03" / "digest-post-activation.json"
    write_json(
        post_activation,
        {
            "schemaVersion": "thesis_record_snapshot_v2",
            "snapshotKind": "recorder_run",
            "runId": "post-activation",
            "recordedAt": "2026-01-03T00:00:00Z",
            "chain": {
                "prevDigestPath": logical(records, activation),
                "prevDigestSha256": hashlib.sha256(activation.read_bytes()).hexdigest(),
            },
        },
    )
    add_witness(post_activation)

    write_json(
        records / "CHAIN_GENESIS.json",
        {
            "schemaVersion": "thesis_record_chain_genesis_v1",
            "firstSnapshot": logical(records, first),
            "legacyDigests": [],
        },
    )
    write_json(
        records / "CHAIN_HEAD.json",
        {
            "schemaVersion": "thesis_record_chain_head_v1",
            "snapshotPath": logical(records, post_activation),
            "snapshotSha256": hashlib.sha256(post_activation.read_bytes()).hexdigest(),
        },
    )
    return records, first, activation, post_activation


def activate_signing(
    monkeypatch: pytest.MonkeyPatch,
    records: pathlib.Path,
    activation: pathlib.Path,
    public_key_pem: bytes,
    *,
    pin: str | None = None,
) -> pathlib.Path:
    public_key = record_chain.physical_path(records, producer_pins.PUBLIC_KEY_RELPATH)
    public_key.parent.mkdir(parents=True, exist_ok=True)
    public_key.write_bytes(public_key_pem)
    monkeypatch.setattr(
        producer_pins,
        "PRODUCER_SPKI_SHA256",
        pin or spki_sha256(public_key_pem),
    )
    monkeypatch.setattr(
        producer_pins,
        "ACTIVATION_SNAPSHOT",
        logical(records, activation),
    )
    return public_key


def sign_snapshot(snapshot: pathlib.Path, private_key_pem: bytes) -> pathlib.Path:
    signature = record_chain.producer_signature_path(snapshot)
    signature.write_bytes(
        sign_payload(
            private_key_pem,
            snapshot.read_bytes(),
            domain=producer_pins.SIGNATURE_DOMAIN,
        )
    )
    return signature


def assert_chain_error(
    records: pathlib.Path,
    expected: str,
) -> None:
    with pytest.raises(ChainError) as caught:
        verify_chain(records, allow_pre_enumeration=True)
    assert str(caught.value) == expected


def test_live_records_tree_verifies_while_producer_signing_is_dormant() -> None:
    assert producer_pins.producer_signing_active() is False
    assert verify_chain(ROOT / "records").ordered


def test_dormant_signing_rejects_a_stray_signature_anywhere(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
) -> None:
    records, _first, _activation, _post_activation = synthetic_chain
    stray = records / "unrelated" / "stray.producer.sig"
    stray.parent.mkdir(parents=True)
    stray.write_bytes(b"stray")

    assert_chain_error(
        records,
        "producer signature is present while producer signing is dormant: "
        "records/unrelated/stray.producer.sig",
    )


@pytest.mark.parametrize(
    ("pin", "activation"),
    [
        ("0" * 64, None),
        (None, "records/2026-01-02/digest-activation.json"),
    ],
)
def test_half_armed_signing_pins_refuse(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
    pin: str | None,
    activation: str | None,
) -> None:
    records, _first, _boundary, _post_activation = synthetic_chain
    monkeypatch.setattr(producer_pins, "PRODUCER_SPKI_SHA256", pin)
    monkeypatch.setattr(producer_pins, "ACTIVATION_SNAPSHOT", activation)

    assert_chain_error(records, "producer signing pins are half-armed")


def test_dormant_verification_does_not_import_receipt(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, _first, _activation, _post_activation = synthetic_chain
    real_import = builtins.__import__

    def guarded_import(name: str, *args: object, **kwargs: object) -> object:
        if name == "receipt" or name.startswith("receipt."):
            raise AssertionError("dormant verification imported receipt")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    assert len(verify_chain(records, allow_pre_enumeration=True).ordered) == 3


def test_active_signing_accepts_a_valid_post_boundary_signature(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, _first, activation, post_activation = synthetic_chain
    private_key, public_key = generate_signing_keypair()
    activate_signing(monkeypatch, records, activation, public_key)
    sign_snapshot(post_activation, private_key)

    assert len(verify_chain(records, allow_pre_enumeration=True).ordered) == 3


def test_active_signing_rejects_a_missing_signature(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, _first, activation, post_activation = synthetic_chain
    _private_key, public_key = generate_signing_keypair()
    activate_signing(monkeypatch, records, activation, public_key)

    assert_chain_error(
        records,
        "missing or non-regular producer signature: "
        f"{logical(records, record_chain.producer_signature_path(post_activation))}",
    )


def test_active_signing_rejects_a_non_64_byte_signature(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, _first, activation, post_activation = synthetic_chain
    _private_key, public_key = generate_signing_keypair()
    activate_signing(monkeypatch, records, activation, public_key)
    signature = record_chain.producer_signature_path(post_activation)
    signature.write_bytes(b"short")

    assert_chain_error(
        records,
        f"producer signature for {logical(records, signature)} must be exactly "
        "64 raw bytes; found=5",
    )


def test_active_signing_rejects_a_bit_flipped_signature(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, _first, activation, post_activation = synthetic_chain
    private_key, public_key = generate_signing_keypair()
    activate_signing(monkeypatch, records, activation, public_key)
    signature = sign_snapshot(post_activation, private_key)
    raw = signature.read_bytes()
    signature.write_bytes(bytes([raw[0] ^ 1]) + raw[1:])

    assert_chain_error(
        records,
        "producer Ed25519 signature verification failed for "
        f"{logical(records, signature)}",
    )


def test_active_signing_rejects_a_public_key_outside_the_spki_pin(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, _first, activation, post_activation = synthetic_chain
    _trusted_private, trusted_public = generate_signing_keypair()
    other_private, other_public = generate_signing_keypair()
    activate_signing(
        monkeypatch,
        records,
        activation,
        other_public,
        pin=spki_sha256(trusted_public),
    )
    sign_snapshot(post_activation, other_private)

    assert_chain_error(
        records,
        "producer public-key SPKI is not code-pinned for "
        f"{producer_pins.PUBLIC_KEY_RELPATH}: "
        f"{spki_sha256(other_public)}",
    )


def test_active_signing_validates_a_malformed_key_when_activation_is_head(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, _first, _activation, post_activation = synthetic_chain
    public_key = record_chain.physical_path(records, producer_pins.PUBLIC_KEY_RELPATH)
    public_key.parent.mkdir(parents=True)
    public_key.write_bytes(b"not an Ed25519 public key")
    monkeypatch.setattr(producer_pins, "PRODUCER_SPKI_SHA256", "0" * 64)
    monkeypatch.setattr(
        producer_pins,
        "ACTIVATION_SNAPSHOT",
        logical(records, post_activation),
    )

    assert_chain_error(
        records,
        "producer public key is invalid: "
        f"{producer_pins.PUBLIC_KEY_RELPATH}: cannot decode Ed25519 public key",
    )


def test_active_signing_checks_the_spki_pin_when_activation_is_head(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, _first, _activation, post_activation = synthetic_chain
    _trusted_private, trusted_public = generate_signing_keypair()
    _other_private, other_public = generate_signing_keypair()
    activate_signing(
        monkeypatch,
        records,
        post_activation,
        other_public,
        pin=spki_sha256(trusted_public),
    )

    assert_chain_error(
        records,
        "producer public-key SPKI is not code-pinned for "
        f"{producer_pins.PUBLIC_KEY_RELPATH}: "
        f"{spki_sha256(other_public)}",
    )


def test_active_signing_rejects_a_symlinked_signature(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    records, _first, activation, post_activation = synthetic_chain
    private_key, public_key = generate_signing_keypair()
    activate_signing(monkeypatch, records, activation, public_key)
    target = tmp_path / "detached-signature"
    target.write_bytes(
        sign_payload(
            private_key,
            post_activation.read_bytes(),
            domain=producer_pins.SIGNATURE_DOMAIN,
        )
    )
    signature = record_chain.producer_signature_path(post_activation)
    signature.symlink_to(target)

    assert_chain_error(
        records,
        "missing or non-regular producer signature: " f"{logical(records, signature)}",
    )


@pytest.mark.parametrize("signed_position", ["before", "boundary"])
def test_active_signing_rejects_a_signature_at_or_before_activation(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
    signed_position: str,
) -> None:
    records, first, activation, post_activation = synthetic_chain
    private_key, public_key = generate_signing_keypair()
    activate_signing(monkeypatch, records, activation, public_key)
    forbidden_snapshot = first if signed_position == "before" else activation
    forbidden_signature = sign_snapshot(forbidden_snapshot, private_key)
    sign_snapshot(post_activation, private_key)

    assert_chain_error(
        records,
        "producer signature is forbidden at or before activation: "
        f"{logical(records, forbidden_signature)}",
    )


def test_active_signing_rejects_an_activation_snapshot_absent_from_the_chain(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, _first, _activation, _post_activation = synthetic_chain
    _private_key, public_key = generate_signing_keypair()
    public_key_path = record_chain.physical_path(
        records, producer_pins.PUBLIC_KEY_RELPATH
    )
    public_key_path.parent.mkdir(parents=True)
    public_key_path.write_bytes(public_key)
    monkeypatch.setattr(producer_pins, "PRODUCER_SPKI_SHA256", spki_sha256(public_key))
    absent = "records/2026-01-09/digest-absent.json"
    monkeypatch.setattr(producer_pins, "ACTIVATION_SNAPSHOT", absent)

    assert_chain_error(
        records,
        "producer signing activation snapshot is absent from the reachable "
        f"chain: {absent}",
    )


def test_active_signing_rejects_an_orphan_signature(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, _first, activation, post_activation = synthetic_chain
    private_key, public_key = generate_signing_keypair()
    activate_signing(monkeypatch, records, activation, public_key)
    sign_snapshot(post_activation, private_key)
    orphan = records / "trust" / "orphan.producer.sig"
    orphan.write_bytes(b"orphan")

    assert_chain_error(
        records,
        "orphan producer signature is not a post-activation snapshot sibling: "
        "records/trust/orphan.producer.sig",
    )


def test_active_signing_rejects_a_symlinked_public_key(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
) -> None:
    records, _first, activation, post_activation = synthetic_chain
    private_key, public_key = generate_signing_keypair()
    public_key_path = activate_signing(monkeypatch, records, activation, public_key)
    public_key_path.unlink()
    detached = tmp_path / "producer.pub"
    detached.write_bytes(public_key)
    public_key_path.symlink_to(detached)
    sign_snapshot(post_activation, private_key)

    assert_chain_error(
        records,
        "missing or non-regular producer public key: "
        f"{producer_pins.PUBLIC_KEY_RELPATH}",
    )


def test_active_signing_refuses_when_receipt_is_not_importable(
    synthetic_chain: tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    records, _first, activation, post_activation = synthetic_chain
    private_key, public_key = generate_signing_keypair()
    activate_signing(monkeypatch, records, activation, public_key)
    sign_snapshot(post_activation, private_key)
    real_import = builtins.__import__

    def missing_receipt(name: str, *args: object, **kwargs: object) -> object:
        if name == "receipt" or name.startswith("receipt."):
            raise ImportError("receipt deliberately hidden")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", missing_receipt)
    assert_chain_error(
        records,
        "producer signing is active but the receipt package is not installed",
    )
