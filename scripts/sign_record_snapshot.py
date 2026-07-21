#!/usr/bin/env python3
"""Sign post-activation Thesis record snapshots with the producer key."""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path
from typing import Any, Callable, Sequence

import producer_signing_pins as producer_pins
from verify_record_chain import (
    ChainError,
    ensure_regular_records_file,
    load_json,
    logical_path,
    physical_path,
    producer_signature_path,
    sha256_file,
    snapshot_paths,
)

SIGNING_KEY_ENV = "BRIER_PRODUCER_SIGNING_KEY"


class ProducerSigningError(RuntimeError):
    """A refusal to create or accept a producer signature."""


def _ordered_snapshots(records: Path) -> list[Path]:
    """Validate and return chain order without requiring signatures or witnesses."""

    genesis_path = records / "CHAIN_GENESIS.json"
    if genesis_path.is_symlink() or not genesis_path.is_file():
        raise ProducerSigningError(
            f"missing or non-regular chain genesis: {genesis_path}"
        )
    try:
        genesis = load_json(genesis_path)
    except ChainError as exc:
        raise ProducerSigningError(str(exc)) from exc
    if genesis.get("schemaVersion") != "thesis_record_chain_genesis_v1":
        raise ProducerSigningError(
            f"unsupported genesis schema: {genesis.get('schemaVersion')!r}"
        )

    snapshots = snapshot_paths(records)
    for snapshot in snapshots:
        try:
            ensure_regular_records_file(
                records,
                snapshot,
                message=(
                    "missing or non-regular record snapshot: "
                    f"{logical_path(records, snapshot)}"
                ),
            )
        except ChainError as exc:
            raise ProducerSigningError(str(exc)) from exc

    first_logical = genesis.get("firstSnapshot")
    if not isinstance(first_logical, str) or not first_logical:
        raise ProducerSigningError("genesis firstSnapshot must name one snapshot")
    try:
        first = physical_path(records, first_logical)
    except ChainError as exc:
        raise ProducerSigningError(str(exc)) from exc
    if first not in snapshots:
        raise ProducerSigningError(
            f"genesis snapshot is missing or malformed: {first_logical}"
        )

    snapshot_set = set(snapshots)
    successors: dict[Path, list[Path]] = {path: [] for path in snapshots}
    for path in snapshots:
        try:
            payload = load_json(path)
        except ChainError as exc:
            raise ProducerSigningError(str(exc)) from exc
        if payload.get("schemaVersion") != "thesis_record_snapshot_v2":
            raise ProducerSigningError(f"unsupported snapshot schema in {path}")
        chain = payload.get("chain")
        if path == first:
            if chain is not None:
                raise ProducerSigningError(
                    f"genesis snapshot must not have a chain block: {path}"
                )
            continue
        if not isinstance(chain, dict):
            raise ProducerSigningError(f"missing chain block after genesis: {path}")
        previous_logical = chain.get("prevDigestPath")
        if not isinstance(previous_logical, str):
            raise ProducerSigningError(f"missing chain.prevDigestPath in {path}")
        try:
            previous = physical_path(records, previous_logical)
        except ChainError as exc:
            raise ProducerSigningError(str(exc)) from exc
        if previous not in snapshot_set:
            raise ProducerSigningError(
                f"missing predecessor for {path}: {previous_logical}"
            )
        expected_sha = sha256_file(previous)
        if chain.get("prevDigestSha256") != expected_sha:
            raise ProducerSigningError(
                f"predecessor hash mismatch in {path}: expected {expected_sha}, "
                f"got {chain.get('prevDigestSha256')}"
            )
        successors[previous].append(path)

    ordered = [first]
    visited = {first}
    cursor = first
    while successors[cursor]:
        children = successors[cursor]
        if len(children) != 1:
            raise ProducerSigningError(
                f"fork after {logical_path(records, cursor)}: "
                + ", ".join(logical_path(records, child) for child in sorted(children))
            )
        cursor = children[0]
        if cursor in visited:
            raise ProducerSigningError(f"cycle at {logical_path(records, cursor)}")
        visited.add(cursor)
        ordered.append(cursor)
    if visited != snapshot_set:
        raise ProducerSigningError(
            "orphaned snapshot(s) not reachable from genesis: "
            + ", ".join(
                logical_path(records, path) for path in sorted(snapshot_set - visited)
            )
        )
    return ordered


def _activation_index(records: Path, ordered: list[Path]) -> int:
    activation_logical = producer_pins.ACTIVATION_SNAPSHOT
    if not isinstance(activation_logical, str) or not activation_logical:
        # producer_signing_active() should have rejected this configuration.
        raise ProducerSigningError("producer signing pins are half-armed")
    try:
        activation = physical_path(records, activation_logical)
    except ChainError as exc:
        raise ProducerSigningError(str(exc)) from exc
    if activation not in ordered:
        raise ProducerSigningError(
            "producer signing activation snapshot is absent from the reachable "
            f"chain: {activation_logical}"
        )
    return ordered.index(activation)


def _requested_snapshot(
    records: Path, path: Path, ordered: set[Path], eligible: set[Path]
) -> Path:
    if path.is_absolute():
        candidate = path.resolve()
    else:
        from_working_directory = path.resolve()
        try:
            from_working_directory.relative_to(records)
        except ValueError:
            candidate = (records / path).resolve()
        else:
            candidate = from_working_directory
    try:
        logical = logical_path(records, candidate)
    except ValueError as exc:
        raise ProducerSigningError(
            f"requested snapshot is outside the records root: {path}"
        ) from exc
    if candidate not in ordered:
        raise ProducerSigningError(
            f"requested snapshot is not in the reachable chain: {logical}"
        )
    if candidate not in eligible:
        raise ProducerSigningError(
            "requested snapshot is not strictly after producer signing activation: "
            f"{logical}"
        )
    return candidate


def _select_targets(
    records: Path,
    ordered: list[Path],
    activation_index: int,
    requested: Sequence[Path] | None,
) -> list[Path]:
    eligible = ordered[activation_index + 1 :]
    if not requested:
        return eligible
    ordered_set = set(ordered)
    eligible_set = set(eligible)
    requested_set = {
        _requested_snapshot(records, path, ordered_set, eligible_set)
        for path in requested
    }
    return [path for path in eligible if path in requested_set]


def _regular_file_bytes(path: Path, *, missing_message: str) -> bytes:
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise ProducerSigningError(missing_message) from exc
    except OSError as exc:
        raise ProducerSigningError(f"cannot inspect {path}: {exc}") from exc
    if not stat.S_ISREG(metadata.st_mode):
        raise ProducerSigningError(missing_message)
    try:
        return path.read_bytes()
    except OSError as exc:
        raise ProducerSigningError(f"cannot read {path}: {exc}") from exc


def _existing_signature_bytes(records: Path, signature: Path) -> bytes | None:
    try:
        metadata = signature.lstat()
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise ProducerSigningError(f"cannot inspect {signature}: {exc}") from exc
    logical = logical_path(records, signature)
    if not stat.S_ISREG(metadata.st_mode):
        raise ProducerSigningError(
            f"existing producer signature is not a regular file: {logical}"
        )
    try:
        signature_bytes = signature.read_bytes()
    except OSError as exc:
        raise ProducerSigningError(
            f"cannot read existing producer signature {logical}: {exc}"
        ) from exc
    if len(signature_bytes) != 64:
        raise ProducerSigningError(
            f"existing producer signature must contain exactly 64 raw bytes: {logical}"
        )
    return signature_bytes


def _exclusive_write(path: Path, payload: bytes) -> None:
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except OSError as exc:
        raise ProducerSigningError(
            f"refusing to overwrite producer signature: {path}"
        ) from exc
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def _load_receipt_signing() -> tuple[
    type[Exception],
    Callable[..., bytes],
    Callable[[bytes], str],
    Callable[..., Any],
]:
    try:
        from receipt.sign import (
            SignError,
            sign_payload,
            spki_sha256,
            verify_signature_bytes,
        )
    except ImportError as exc:
        raise ProducerSigningError(
            "producer signing is active but the receipt package is not installed"
        ) from exc
    return SignError, sign_payload, spki_sha256, verify_signature_bytes


def sign_record_snapshots(
    records: Path,
    snapshots: Sequence[Path] | None = None,
) -> list[Path]:
    """Sign selected post-activation snapshots and return newly written siblings."""

    try:
        active = producer_pins.producer_signing_active()
    except ValueError as exc:
        raise ProducerSigningError(str(exc)) from exc
    if not active:
        return []

    sign_error, sign_payload, spki_sha256, verify_signature_bytes = (
        _load_receipt_signing()
    )
    records = records.resolve()
    ordered = _ordered_snapshots(records)
    activation_index = _activation_index(records, ordered)
    eligible = ordered[activation_index + 1 :]
    targets = _select_targets(records, ordered, activation_index, snapshots)

    discovered = sorted(records.rglob(f"*{producer_pins.SIGNATURE_SUFFIX}"))
    discovered_set = set(discovered)
    for snapshot in ordered[: activation_index + 1]:
        signature = producer_signature_path(snapshot)
        if signature in discovered_set:
            raise ProducerSigningError(
                "producer signature is forbidden at or before activation: "
                f"{logical_path(records, signature)}"
            )
    expected_signatures = {producer_signature_path(path) for path in eligible}
    orphaned = sorted(discovered_set - expected_signatures)
    if orphaned:
        raise ProducerSigningError(
            "orphan producer signature is not a post-activation snapshot sibling: "
            f"{logical_path(records, orphaned[0])}"
        )

    public_key_message = (
        "missing or non-regular producer public key: "
        f"{producer_pins.PUBLIC_KEY_RELPATH}"
    )
    public_key_logical = Path(producer_pins.PUBLIC_KEY_RELPATH)
    if public_key_logical.parts[:1] == ("records",):
        public_key_logical = Path(*public_key_logical.parts[1:])
    public_key_candidate = records / public_key_logical
    try:
        ensure_regular_records_file(
            records,
            public_key_candidate,
            message=public_key_message,
        )
        public_key_path = physical_path(records, producer_pins.PUBLIC_KEY_RELPATH)
    except ChainError as exc:
        raise ProducerSigningError(str(exc)) from exc
    public_key_pem = _regular_file_bytes(
        public_key_path,
        missing_message=public_key_message,
    )
    spki_pin = producer_pins.PRODUCER_SPKI_SHA256
    if not isinstance(spki_pin, str) or not spki_pin:
        raise ProducerSigningError("producer signing pins are half-armed")
    try:
        computed_spki = spki_sha256(public_key_pem)
    except sign_error as exc:
        raise ProducerSigningError(
            f"producer public key is invalid: {producer_pins.PUBLIC_KEY_RELPATH}: "
            f"{exc}"
        ) from exc
    if computed_spki != spki_pin:
        raise ProducerSigningError(
            "producer public-key SPKI is not code-pinned for "
            f"{producer_pins.PUBLIC_KEY_RELPATH}: {computed_spki}"
        )

    secret = os.environ.pop(SIGNING_KEY_ENV, None)
    if not secret:
        raise ProducerSigningError(
            f"{SIGNING_KEY_ENV} is required while producer signing is active"
        )
    try:
        private_key_pem = bytearray(secret.encode())
    except UnicodeEncodeError as exc:
        raise ProducerSigningError(
            f"{SIGNING_KEY_ENV} is not a valid Ed25519 private key"
        ) from exc
    finally:
        # os.environ.pop() already removed the process-level copy. Drop the
        # immutable Python string as soon as its erasable working copy exists.
        secret = None

    try:
        try:
            probe = sign_payload(
                bytes(private_key_pem), b"", domain=producer_pins.SIGNATURE_DOMAIN
            )
        except sign_error as exc:
            raise ProducerSigningError(
                f"{SIGNING_KEY_ENV} is not a valid Ed25519 private key"
            ) from exc
        try:
            verify_signature_bytes(
                producer_pins.SIGNATURE_DOMAIN,
                probe,
                public_key_pem,
                public_key_filename=producer_pins.PUBLIC_KEY_RELPATH,
                spki_sha256=spki_pin,
                label="producer signing key self-check",
            )
        except sign_error as exc:
            raise ProducerSigningError(
                f"{SIGNING_KEY_ENV} does not match the code-pinned producer public key"
            ) from exc

        existing: dict[Path, bytes] = {}
        for snapshot in eligible:
            signature = producer_signature_path(snapshot)
            signature_bytes = _existing_signature_bytes(records, signature)
            if signature_bytes is None:
                continue
            existing[snapshot] = signature_bytes
            try:
                verify_signature_bytes(
                    producer_pins.SIGNATURE_DOMAIN + snapshot.read_bytes(),
                    signature_bytes,
                    public_key_pem,
                    public_key_filename=producer_pins.PUBLIC_KEY_RELPATH,
                    spki_sha256=spki_pin,
                    label=logical_path(records, signature),
                )
            except sign_error as exc:
                raise ProducerSigningError(
                    "existing producer signature is invalid: "
                    f"{logical_path(records, signature)}"
                ) from exc

        pending: list[tuple[Path, bytes]] = []
        for snapshot in targets:
            if snapshot in existing:
                continue
            signature = producer_signature_path(snapshot)
            try:
                signature_bytes = sign_payload(
                    bytes(private_key_pem),
                    snapshot.read_bytes(),
                    domain=producer_pins.SIGNATURE_DOMAIN,
                )
            except (OSError, sign_error) as exc:
                raise ProducerSigningError(
                    f"producer signing failed for {logical_path(records, snapshot)}"
                ) from exc
            if len(signature_bytes) != 64:
                raise ProducerSigningError(
                    "producer signer did not return a 64-byte raw signature for "
                    f"{logical_path(records, snapshot)}"
                )
            pending.append((signature, signature_bytes))

        written: list[Path] = []
        for signature, signature_bytes in pending:
            _exclusive_write(signature, signature_bytes)
            written.append(signature)
        return written
    finally:
        private_key_pem[:] = b"\0" * len(private_key_pem)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=Path("records"))
    parser.add_argument("snapshots", nargs="*", type=Path)
    args = parser.parse_args(argv)
    try:
        written = sign_record_snapshots(args.records, args.snapshots)
    except (ChainError, OSError, ProducerSigningError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
