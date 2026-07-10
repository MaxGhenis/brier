#!/usr/bin/env python3
"""Fail-closed verification for the forecast record chain and RFC 3161 proofs."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from canonical_json import canonical_bytes, canonical_sha256

SNAPSHOT_RE = re.compile(r"digest-[A-Za-z0-9][A-Za-z0-9._-]*\.json$")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
TRUST_BUNDLE_RE = re.compile(r"records/trust/tsa-anchors-v[1-9][0-9]*\.json")
UTC = timezone.utc
SHA256_OID = "2.16.840.1.101.3.4.2.1"
CODE_PINNED_TRUST_BUNDLES: dict[str, dict[str, Any]] = {
    "records/trust/tsa-anchors-v1.json": {
        "bundleId": "tsa-anchors-v1",
        "path": "records/trust/tsa-anchors-v1.json",
        "sha256": "737bc9a149726f375edaebcd39b34116d90a5d29e9a043bcb0437998928e5791",
        "size": 1049,
        "canonicalJsonSha256": (
            "9930588eb27ba631446416cf0d2bdac80785e73cf1d32e1d2ed70b0bb49f3d39"
        ),
    }
}
CODE_PINNED_TSA_IDENTITIES = {
    "tsa-anchors-v1": {
        "freetsa-root-2016": {
            "rootSpkiSha256": (
                "52c54ba340885605314daa1857c8763b94087d05c636092938d4e2d1818e99b5"
            ),
            "signerSpkiSha256": {
                "fa02bd555e3e483d62b4e70be6218692068d2b0b0a7525db58dcbf2901cdb072"
            },
        }
    }
}
CODE_PINNED_GENESIS_ENUMERATIONS: dict[str, dict[str, Any]] = {
    "records/GENESIS_RECORDS.json": {
        "path": "records/GENESIS_RECORDS.json",
        "sha256": "b4d3d7033e3c5f81cbaf31c76ae1b029746f53803edbae228935899826a59f5d",
        "canonicalJsonSha256": (
            "b4d3d7033e3c5f81cbaf31c76ae1b029746f53803edbae228935899826a59f5d"
        ),
        "size": 1057414,
        "entryCount": 4754,
        "totalSize": 635115664,
        "sourceCommit": "0a57bfc58ea3578cf3c43b3edd2d414813566ce8",
    }
}


class ChainError(ValueError):
    pass


@dataclass(frozen=True)
class WitnessEvidence:
    status: str
    digest_sha256: str
    anchor_id: str | None = None
    trust_bundle_id: str | None = None
    trust_bundle_path: str | None = None
    policy_oid: str | None = None
    imprint_algorithm_oid: str | None = None
    gen_time: str | None = None
    tsa_subject: str | None = None
    tsa_certificate_sha256: str | None = None
    tsa_spki_sha256: str | None = None


@dataclass(frozen=True)
class ChainVerification:
    ordered: tuple[Path, ...]
    witnesses: dict[Path, WitnessEvidence]
    enumeration_cutover: Path | None


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def logical_path(records: Path, path: Path) -> str:
    return str(Path("records") / path.relative_to(records))


def physical_path(records: Path, value: str) -> Path:
    logical = Path(value)
    if (
        logical.is_absolute()
        or ".." in logical.parts
        or "\\" in value
        or not logical.parts
    ):
        raise ChainError(f"unsafe record path in genesis/chain: {value!r}")
    if logical.parts[0] == "records":
        logical = Path(*logical.parts[1:])
    path = records / logical
    try:
        path.resolve().relative_to(records.resolve())
    except ValueError as exc:
        raise ChainError(f"record path escapes records root: {value!r}") from exc
    return path


def snapshot_paths(records: Path) -> list[Path]:
    return sorted(
        path
        for path in records.glob("????-??-??/digest-*.json")
        if SNAPSHOT_RE.fullmatch(path.name) and not path.name.endswith(".witness.json")
    )


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ChainError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ChainError(f"record must be a JSON object: {path}")
    return value


def _run_openssl(
    arguments: list[str],
    *,
    input_bytes: bytes | None = None,
    binary: bool = False,
    env: dict[str, str] | None = None,
) -> bytes | str:
    command = ["openssl", *arguments]
    process_env = os.environ.copy()
    process_env.update({"OPENSSL_CONF": "/dev/null", "LC_ALL": "C"})
    if env:
        process_env.update(env)
    try:
        completed = subprocess.run(
            command,
            input=input_bytes,
            capture_output=True,
            check=False,
            env=process_env,
        )
    except FileNotFoundError as exc:
        raise ChainError("openssl is required to verify RFC 3161 tokens") from exc
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).decode(errors="replace").strip()
        raise ChainError(f"OpenSSL command failed ({' '.join(command)}): {detail}")
    if binary:
        return completed.stdout
    return completed.stdout.decode(errors="strict")


def _certificate_identity(path: Path) -> dict[str, str]:
    certificate_der = _run_openssl(
        ["x509", "-in", str(path), "-outform", "DER"], binary=True
    )
    assert isinstance(certificate_der, bytes)
    public_key_pem = _run_openssl(
        ["x509", "-in", str(path), "-pubkey", "-noout"], binary=True
    )
    assert isinstance(public_key_pem, bytes)
    public_key_der = _run_openssl(
        ["pkey", "-pubin", "-outform", "DER"],
        input_bytes=public_key_pem,
        binary=True,
    )
    assert isinstance(public_key_der, bytes)
    description = _run_openssl(
        [
            "x509",
            "-in",
            str(path),
            "-noout",
            "-serial",
            "-subject",
            "-nameopt",
            "RFC2253",
        ]
    )
    assert isinstance(description, str)
    fields: dict[str, str] = {}
    for line in description.splitlines():
        key, separator, value = line.partition("=")
        if separator:
            fields[key] = value
    return {
        "certificateSha256": hashlib.sha256(certificate_der).hexdigest(),
        "spkiSha256": hashlib.sha256(public_key_der).hexdigest(),
        "serial": fields.get("serial", "").upper(),
        "subject": fields.get("subject", ""),
    }


def _read_der_tlv(data: bytes, offset: int) -> tuple[int, bytes, int]:
    if offset >= len(data):
        raise ChainError("truncated DER value in RFC 3161 TSTInfo")
    tag = data[offset]
    offset += 1
    if offset >= len(data):
        raise ChainError("truncated DER length in RFC 3161 TSTInfo")
    first = data[offset]
    offset += 1
    if first & 0x80:
        count = first & 0x7F
        if count == 0 or count > 4 or offset + count > len(data):
            raise ChainError("invalid DER length in RFC 3161 TSTInfo")
        length = int.from_bytes(data[offset : offset + count], "big")
        offset += count
    else:
        length = first
    end = offset + length
    if end > len(data):
        raise ChainError("truncated DER content in RFC 3161 TSTInfo")
    return tag, data[offset:end], end


def _decode_oid(data: bytes) -> str:
    if not data:
        raise ChainError("empty policy OID in RFC 3161 token")
    first = data[0]
    values = [min(first // 40, 2), first - min(first // 40, 2) * 40]
    current = 0
    continuation = False
    for byte in data[1:]:
        current = (current << 7) | (byte & 0x7F)
        continuation = bool(byte & 0x80)
        if not continuation:
            values.append(current)
            current = 0
    if continuation:
        raise ChainError("truncated policy OID in RFC 3161 token")
    return ".".join(str(value) for value in values)


def _parse_generalized_time(value: str) -> datetime:
    match = re.fullmatch(r"(\d{14})(?:\.(\d+))?Z", value)
    if not match:
        raise ChainError(f"unsupported RFC 3161 genTime: {value!r}")
    parsed = datetime.strptime(match.group(1), "%Y%m%d%H%M%S").replace(tzinfo=UTC)
    fraction = match.group(2)
    if fraction:
        parsed = parsed.replace(microsecond=int((fraction + "000000")[:6]))
    return parsed


def _format_utc(value: datetime) -> str:
    value = value.astimezone(UTC)
    if value.microsecond:
        return (
            value.isoformat(timespec="microseconds")
            .rstrip("0")
            .rstrip(".")
            .replace("+00:00", "Z")
        )
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_tst_info(data: bytes) -> tuple[str, str, bytes, datetime]:
    tag, sequence, end = _read_der_tlv(data, 0)
    if tag != 0x30 or end != len(data):
        raise ChainError("RFC 3161 TSTInfo is not one complete DER sequence")
    offset = 0
    tag, _version, offset = _read_der_tlv(sequence, offset)
    if tag != 0x02:
        raise ChainError("RFC 3161 TSTInfo lacks a version")
    tag, policy, offset = _read_der_tlv(sequence, offset)
    if tag != 0x06:
        raise ChainError("RFC 3161 TSTInfo lacks a policy OID")
    tag, message_imprint, offset = _read_der_tlv(sequence, offset)
    if tag != 0x30:
        raise ChainError("RFC 3161 TSTInfo lacks a message imprint")
    imprint_offset = 0
    tag, algorithm_identifier, imprint_offset = _read_der_tlv(
        message_imprint, imprint_offset
    )
    if tag != 0x30:
        raise ChainError("RFC 3161 message imprint lacks AlgorithmIdentifier")
    algorithm_offset = 0
    tag, algorithm_oid, algorithm_offset = _read_der_tlv(
        algorithm_identifier, algorithm_offset
    )
    if tag != 0x06:
        raise ChainError("RFC 3161 message imprint lacks an algorithm OID")
    if algorithm_offset < len(algorithm_identifier):
        tag, parameters, algorithm_offset = _read_der_tlv(
            algorithm_identifier, algorithm_offset
        )
        if tag != 0x05 or parameters:
            raise ChainError("unsupported RFC 3161 imprint algorithm parameters")
    if algorithm_offset != len(algorithm_identifier):
        raise ChainError("trailing RFC 3161 imprint AlgorithmIdentifier data")
    tag, hashed_message, imprint_offset = _read_der_tlv(message_imprint, imprint_offset)
    if tag != 0x04 or imprint_offset != len(message_imprint):
        raise ChainError("invalid RFC 3161 hashed message")
    tag, _serial, offset = _read_der_tlv(sequence, offset)
    if tag != 0x02:
        raise ChainError("RFC 3161 TSTInfo lacks a serial number")
    tag, gen_time, _offset = _read_der_tlv(sequence, offset)
    if tag != 0x18:
        raise ChainError("RFC 3161 TSTInfo lacks a genTime")
    try:
        gen_time_text = gen_time.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ChainError("RFC 3161 genTime is not ASCII") from exc
    return (
        _decode_oid(policy),
        _decode_oid(algorithm_oid),
        hashed_message,
        _parse_generalized_time(gen_time_text),
    )


def _parse_rfc3339(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ChainError(f"missing or invalid timestamp claim {label}")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ChainError(f"invalid timestamp claim {label}: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ChainError(f"timestamp claim lacks a timezone {label}: {value!r}")
    return parsed.astimezone(UTC)


def _creation_claims(payload: dict[str, Any]) -> list[tuple[str, datetime]]:
    claims: list[tuple[str, datetime]] = []
    for key in ("recordedAt", "createdAt"):
        if key in payload:
            claims.append((key, _parse_rfc3339(payload[key], key)))
    dependencies = payload.get("dependencies")
    if isinstance(dependencies, dict):
        stack: list[tuple[str, dict[str, Any]]] = [("dependencies", dependencies)]
        while stack:
            prefix, current = stack.pop()
            for key, value in current.items():
                label = f"{prefix}.{key}"
                if isinstance(value, dict):
                    stack.append((label, value))
                elif key in {"builtAt", "createdAt", "recordedAt", "fetchedAt"}:
                    claims.append((label, _parse_rfc3339(value, label)))
    if not any(label == "recordedAt" for label, _ in claims):
        raise ChainError("snapshot lacks top-level recordedAt creation claim")
    return claims


def validate_token_time(
    payload: dict[str, Any],
    gen_time: datetime,
    *,
    now: datetime,
    max_future_seconds: int,
    max_token_lead_seconds: int,
) -> None:
    """Validate signed time against wall time and internal creation claims."""

    current = now.astimezone(UTC)
    if gen_time > current + timedelta(seconds=max_future_seconds):
        raise ChainError(
            f"RFC 3161 genTime {_format_utc(gen_time)} postdates verification "
            f"time {_format_utc(current)}"
        )
    for label, claim in _creation_claims(payload):
        if gen_time < claim - timedelta(seconds=max_token_lead_seconds):
            raise ChainError(
                f"RFC 3161 genTime {_format_utc(gen_time)} impossibly precedes "
                f"{label}={_format_utc(claim)}"
            )


def _trust_bundle_reference(
    records: Path, path: Path, payload: dict[str, Any]
) -> dict[str, Any]:
    return {
        "bundleId": payload.get("bundleId"),
        "path": logical_path(records, path),
        "sha256": sha256_file(path),
        "size": path.stat().st_size,
        "canonicalJsonSha256": canonical_sha256(payload),
    }


def _load_trust_bundle(
    records: Path, reference: dict[str, Any]
) -> tuple[Path, dict[str, Any]]:
    logical = reference.get("path")
    if not isinstance(logical, str) or not TRUST_BUNDLE_RE.fullmatch(logical):
        raise ChainError(
            f"TSA trust bundle path is not immutable/versioned: {logical!r}"
        )
    if CODE_PINNED_TRUST_BUNDLES.get(logical) != reference:
        raise ChainError(
            f"TSA trust bundle is not independently pinned by verifier code: {logical}"
        )
    path = physical_path(records, logical)
    if not path.is_file() or path.is_symlink():
        raise ChainError(f"TSA trust bundle is missing or not regular: {path}")
    payload = load_json(path)
    if payload.get("schemaVersion") != "thesis_tsa_trust_bundle_v1":
        raise ChainError(
            f"unsupported TSA trust schema: {payload.get('schemaVersion')!r}"
        )
    if not isinstance(payload.get("bundleId"), str) or not payload["bundleId"]:
        raise ChainError(f"TSA trust bundle lacks bundleId: {path}")
    if path.read_bytes() not in {
        canonical_bytes(payload),
        canonical_bytes(payload) + b"\n",
    }:
        raise ChainError(f"TSA trust configuration is not canonical JSON: {path}")
    anchors = payload.get("anchors")
    if not isinstance(anchors, list) or not anchors:
        raise ChainError("TSA trust bundle must contain at least one anchor")
    actual_reference = _trust_bundle_reference(records, path, payload)
    if reference != actual_reference:
        raise ChainError(
            f"TSA trust bundle commitment mismatch for {logical}: "
            f"expected {reference}, got {actual_reference}"
        )
    return path, payload


def _bootstrap_trust_bundles(
    records: Path, genesis: dict[str, Any], *, required: bool
) -> dict[str, dict[str, Any]]:
    reference = genesis.get("tsaTrustBundle")
    if reference is None and not required:
        return {}
    if not isinstance(reference, dict):
        raise ChainError("chain genesis lacks the pinned TSA trust bundle")
    path, _payload = _load_trust_bundle(records, reference)
    return {logical_path(records, path): reference}


def _trust_bundle_updates(
    records: Path, payload: dict[str, Any]
) -> list[dict[str, Any]]:
    updates = payload.get("trustBundleUpdates") or []
    if not isinstance(updates, list):
        raise ChainError("snapshot trustBundleUpdates must be a list")
    validated: list[dict[str, Any]] = []
    for reference in updates:
        if not isinstance(reference, dict):
            raise ChainError("snapshot trust bundle update is not an object")
        _load_trust_bundle(records, reference)
        validated.append(reference)
    return validated


def _activate_trust_bundles(
    active: dict[str, dict[str, Any]], updates: list[dict[str, Any]]
) -> None:
    ids = {str(reference.get("bundleId")): path for path, reference in active.items()}
    for reference in updates:
        path = str(reference["path"])
        bundle_id = str(reference["bundleId"])
        if path in active and active[path] != reference:
            raise ChainError(f"TSA trust bundle path was reused with new bytes: {path}")
        if bundle_id in ids and ids[bundle_id] != path:
            raise ChainError(
                f"TSA trust bundle ID was reused at a new path: {bundle_id}"
            )
        active[path] = reference
        ids[bundle_id] = path


def _select_anchor(
    records: Path, witness: dict[str, Any], trust: dict[str, Any]
) -> dict[str, Any]:
    anchor_id = witness.get("tsaAnchorId")
    endpoint = witness.get("tsa")
    candidates = [
        anchor
        for anchor in trust["anchors"]
        if isinstance(anchor, dict)
        and (
            (anchor_id and anchor.get("id") == anchor_id)
            or (not anchor_id and endpoint and anchor.get("endpoint") == endpoint)
        )
    ]
    if len(candidates) != 1:
        raise ChainError(
            "witness does not select exactly one pinned TSA anchor: "
            f"id={anchor_id!r}, endpoint={endpoint!r}"
        )
    anchor = candidates[0]
    if anchor_id and endpoint != anchor.get("endpoint"):
        raise ChainError("witness TSA endpoint does not match its pinned anchor")
    root = anchor.get("rootCertificate")
    if not isinstance(root, dict):
        raise ChainError(f"TSA anchor {anchor.get('id')!r} lacks rootCertificate")
    root_path = physical_path(records, str(root.get("path", "")))
    if not root_path.is_file() or root_path.is_symlink():
        raise ChainError(
            f"pinned TSA root is missing or not a regular file: {root_path}"
        )
    if sha256_file(root_path) != root.get("pemSha256"):
        raise ChainError(f"pinned TSA root PEM hash mismatch: {root_path}")
    identity = _certificate_identity(root_path)
    if identity["certificateSha256"] != root.get("certificateSha256"):
        raise ChainError(f"pinned TSA root certificate hash mismatch: {root_path}")
    if identity["spkiSha256"] != root.get("spkiSha256"):
        raise ChainError(f"pinned TSA root SPKI hash mismatch: {root_path}")
    bundle_id = str(trust.get("bundleId"))
    code_identity = CODE_PINNED_TSA_IDENTITIES.get(bundle_id, {}).get(
        str(anchor.get("id"))
    )
    if not isinstance(code_identity, dict):
        raise ChainError(
            f"TSA identity is not independently pinned in verifier code: "
            f"{bundle_id}/{anchor.get('id')}"
        )
    if identity["spkiSha256"] != code_identity.get("rootSpkiSha256"):
        raise ChainError("TSA root SPKI differs from the verifier code pin")
    configured_signers = anchor.get("allowedSigners")
    configured_spkis = (
        {
            signer.get("spkiSha256")
            for signer in configured_signers
            if isinstance(signer, dict)
        }
        if isinstance(configured_signers, list)
        else set()
    )
    if configured_spkis != code_identity.get("signerSpkiSha256"):
        raise ChainError("TSA signer SPKIs differ from the verifier code pins")
    return anchor


def verify_witness(
    path: Path,
    *,
    records: Path | None = None,
    now: datetime | None = None,
    trusted_bundles: dict[str, dict[str, Any]] | None = None,
) -> WitnessEvidence:
    records = (records or path.parents[1]).resolve()
    digest_sha = sha256_file(path)
    witness_path = path.with_suffix(".witness.json")
    if not witness_path.is_file():
        raise ChainError(f"missing explicit witness marker for {path}")
    witness = load_json(witness_path)
    if witness.get("schemaVersion") != "thesis_rfc3161_witness_v1":
        raise ChainError(f"unsupported witness schema for {path}")
    if witness.get("digestSha256") != digest_sha:
        raise ChainError(
            f"witness digest mismatch for {path}: expected {digest_sha}, "
            f"got {witness.get('digestSha256')}"
        )
    status = witness.get("status")
    if status not in {"available", "unavailable"}:
        raise ChainError(f"invalid witness status for {path}: {status!r}")
    if status == "unavailable":
        if not witness.get("reason"):
            raise ChainError(f"unavailable witness lacks a reason for {path}")
        return WitnessEvidence(status=status, digest_sha256=digest_sha)

    token_path = physical_path(records, str(witness.get("tokenPath", "")))
    if not token_path.is_file() or token_path.is_symlink():
        raise ChainError(f"witness token is missing for {path}: {token_path}")
    if sha256_file(token_path) != witness.get("tokenSha256"):
        raise ChainError(f"witness token hash mismatch for {path}")

    if trusted_bundles is None:
        genesis = load_json(records / "CHAIN_GENESIS.json")
        trusted_bundles = _bootstrap_trust_bundles(records, genesis, required=True)
    bundle_path = witness.get("trustBundlePath")
    bundle_sha = witness.get("trustBundleSha256")
    if not isinstance(bundle_path, str) or bundle_path not in trusted_bundles:
        raise ChainError(
            f"witness selects an untrusted TSA bundle for {path}: {bundle_path!r}"
        )
    bundle_reference = trusted_bundles[bundle_path]
    if bundle_sha != bundle_reference.get("sha256"):
        raise ChainError(f"witness TSA trust-bundle hash mismatch for {path}")
    _trust_path, trust = _load_trust_bundle(records, bundle_reference)
    if witness.get("trustBundleId") != trust.get("bundleId"):
        raise ChainError(f"witness TSA trust-bundle ID mismatch for {path}")
    anchor = _select_anchor(records, witness, trust)
    root_path = physical_path(records, str(anchor["rootCertificate"]["path"]))

    with tempfile.TemporaryDirectory(prefix="thesis-tsa-") as temporary:
        temp = Path(temporary)
        token_der = temp / "token.der"
        tst_info = temp / "tst-info.der"
        signer = temp / "signer.pem"
        empty_ca_dir = temp / "empty-ca"
        empty_ca_dir.mkdir()
        _run_openssl(
            [
                "ts",
                "-reply",
                "-config",
                "/dev/null",
                "-in",
                str(token_path),
                "-token_out",
                "-out",
                str(token_der),
            ]
        )
        _run_openssl(
            [
                "cms",
                "-verify",
                "-inform",
                "DER",
                "-in",
                str(token_der),
                "-noverify",
                "-nosigs",
                "-out",
                str(tst_info),
            ]
        )
        policy_oid, imprint_algorithm_oid, hashed_message, gen_time = _parse_tst_info(
            tst_info.read_bytes()
        )

        allowed_policies = anchor.get("allowedPolicyOids")
        if not isinstance(allowed_policies, list) or policy_oid not in allowed_policies:
            raise ChainError(
                f"RFC 3161 policy {policy_oid!r} is not allowed for TSA anchor "
                f"{anchor.get('id')!r}"
            )
        allowed_imprints = anchor.get("allowedImprintAlgorithmOids")
        if (
            not isinstance(allowed_imprints, list)
            or imprint_algorithm_oid not in allowed_imprints
        ):
            raise ChainError(
                f"RFC 3161 imprint algorithm {imprint_algorithm_oid!r} is not "
                f"allowed for TSA anchor {anchor.get('id')!r}"
            )
        if imprint_algorithm_oid != SHA256_OID or len(hashed_message) != 32:
            raise ChainError(
                "RFC 3161 witness must use a 32-byte SHA-256 message imprint"
            )
        payload = load_json(path)
        validate_token_time(
            payload,
            gen_time,
            now=now or datetime.now(UTC),
            max_future_seconds=int(anchor.get("maxFutureSeconds", 300)),
            max_token_lead_seconds=int(anchor.get("maxTokenLeadSeconds", 300)),
        )

        verification_env = {
            "SSL_CERT_DIR": str(empty_ca_dir),
            "SSL_CERT_FILE": "/dev/null",
        }
        verification_time = str(int(gen_time.timestamp()))
        # No -CAstore here: OpenSSL loads default trust locations only when
        # NO CA option is given, so the pinned -CAfile plus an empty -CApath
        # already excludes them — and ubuntu's OpenSSL 3.0 rejects the
        # "file:/dev/null" store URI outright (live-caught 2026-07-10 in the
        # register job; macOS OpenSSL accepted it).
        _run_openssl(
            [
                "ts",
                "-verify",
                "-config",
                "/dev/null",
                "-data",
                str(path),
                "-in",
                str(token_path),
                "-CAfile",
                str(root_path),
                "-CApath",
                str(empty_ca_dir),
                "-attime",
                verification_time,
            ],
            env=verification_env,
        )
        _run_openssl(
            [
                "cms",
                "-verify",
                "-inform",
                "DER",
                "-in",
                str(token_der),
                "-CAfile",
                str(root_path),
                "-no-CApath",
                "-no-CAstore",
                "-purpose",
                "timestampsign",
                "-attime",
                verification_time,
                "-signer",
                str(signer),
                "-out",
                str(tst_info),
            ],
            env=verification_env,
        )
        signer_identity = _certificate_identity(signer)

    allowed_signers = anchor.get("allowedSigners")
    if not isinstance(allowed_signers, list) or signer_identity not in allowed_signers:
        raise ChainError(
            "RFC 3161 token signer is not pinned for TSA anchor "
            f"{anchor.get('id')!r}: {signer_identity}"
        )
    declared = {
        "tsaPolicyOid": policy_oid,
        "tsaImprintAlgorithmOid": imprint_algorithm_oid,
        "tsaGenTime": _format_utc(gen_time),
        "tsaSignerCertificateSha256": signer_identity["certificateSha256"],
        "tsaSignerSpkiSha256": signer_identity["spkiSha256"],
    }
    for key, actual in declared.items():
        if key in witness and witness[key] != actual:
            raise ChainError(
                f"witness {key} mismatch for {path}: expected {actual}, "
                f"got {witness[key]}"
            )
    return WitnessEvidence(
        status=status,
        digest_sha256=digest_sha,
        anchor_id=str(anchor["id"]),
        trust_bundle_id=str(trust["bundleId"]),
        trust_bundle_path=bundle_path,
        policy_oid=policy_oid,
        imprint_algorithm_oid=imprint_algorithm_oid,
        gen_time=_format_utc(gen_time),
        tsa_subject=signer_identity["subject"],
        tsa_certificate_sha256=signer_identity["certificateSha256"],
        tsa_spki_sha256=signer_identity["spkiSha256"],
    )


def _verify_enumeration_against_git(
    records: Path, source_commit: str, entries: list[dict[str, Any]]
) -> None:
    """Bind the enumeration to the named Git tree when repository data exists."""

    repository = records.parent
    if not (repository / ".git").exists():
        return
    completed = subprocess.run(
        [
            "git",
            "ls-tree",
            "-r",
            "-z",
            "--long",
            source_commit,
            "--",
            "records",
        ],
        cwd=repository,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise ChainError(
            "cannot inspect genesis enumeration source Git tree: "
            + completed.stderr.decode(errors="replace").strip()
        )
    tree: list[tuple[str, str, int]] = []
    for item in completed.stdout.split(b"\0"):
        if not item:
            continue
        metadata, separator, path_bytes = item.partition(b"\t")
        if not separator:
            raise ChainError("unexpected git ls-tree output for genesis enumeration")
        fields = metadata.decode().split()
        if len(fields) != 4:
            raise ChainError("unexpected git ls-tree metadata for genesis enumeration")
        mode, object_type, object_id, size_text = fields
        try:
            logical = path_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ChainError("genesis Git tree contains a non-UTF-8 path") from exc
        if mode != "100644" or object_type != "blob":
            raise ChainError(f"genesis Git tree contains non-regular record: {logical}")
        tree.append((logical, object_id, int(size_text)))
    enumerated_paths = [str(entry["path"]) for entry in entries]
    tree_paths = [logical for logical, _object_id, _size in tree]
    if enumerated_paths != tree_paths:
        raise ChainError(
            "genesis enumeration membership differs from its source Git tree: "
            f"unlisted={sorted(set(tree_paths) - set(enumerated_paths))}, "
            f"extra={sorted(set(enumerated_paths) - set(tree_paths))}"
        )
    for entry, (_logical, _object_id, tree_size) in zip(entries, tree):
        if entry["size"] != tree_size:
            raise ChainError(
                f"genesis enumeration size differs from Git tree: {entry['path']}"
            )
        if "\n" in entry["path"] or "\r" in entry["path"]:
            raise ChainError("genesis enumeration path contains a line break")
    hash_process = subprocess.run(
        ["git", "hash-object", "--stdin-paths"],
        cwd=repository,
        input=("\n".join(enumerated_paths) + "\n").encode(),
        capture_output=True,
        check=False,
    )
    if hash_process.returncode != 0:
        raise ChainError(
            "cannot hash genesis enumeration worktree files: "
            + hash_process.stderr.decode(errors="replace").strip()
        )
    worktree_ids = hash_process.stdout.decode().splitlines()
    tree_ids = [object_id for _logical, object_id, _size in tree]
    if worktree_ids != tree_ids:
        mismatch = next(
            (
                logical
                for logical, expected, actual in zip(tree_paths, tree_ids, worktree_ids)
                if expected != actual
            ),
            "<unknown>",
        )
        raise ChainError(
            f"enumerated worktree record differs from source Git tree: {mismatch}"
        )


def _verify_enumeration(
    records: Path, genesis: dict[str, Any], cutover: dict[str, Any]
) -> None:
    reference = genesis.get("legacyEnumeration")
    commitments = cutover.get("genesisCommitments")
    if not isinstance(reference, dict) or not isinstance(commitments, dict):
        raise ChainError("enumeration cutover lacks genesis commitments")
    reference_path = reference.get("path")
    if CODE_PINNED_GENESIS_ENUMERATIONS.get(str(reference_path)) != reference:
        raise ChainError(
            "genesis enumeration is not independently pinned by verifier code"
        )
    committed = commitments.get("legacyEnumeration")
    if committed != reference:
        raise ChainError("cutover legacy enumeration commitment differs from genesis")
    enumeration_path = physical_path(records, str(reference.get("path", "")))
    if not enumeration_path.is_file() or enumeration_path.is_symlink():
        raise ChainError(f"committed genesis enumeration is absent: {enumeration_path}")
    raw = enumeration_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != reference.get("sha256"):
        raise ChainError("genesis enumeration raw SHA-256 mismatch")
    if len(raw) != reference.get("size"):
        raise ChainError("genesis enumeration size mismatch")
    enumeration = load_json(enumeration_path)
    if enumeration_path.read_bytes() != canonical_bytes(enumeration):
        raise ChainError("genesis enumeration is not canonical JSON")
    if canonical_sha256(enumeration) != reference.get("canonicalJsonSha256"):
        raise ChainError("genesis enumeration canonical SHA-256 mismatch")
    if enumeration.get("schemaVersion") != "thesis_legacy_record_enumeration_v1":
        raise ChainError("unsupported genesis enumeration schema")
    if enumeration.get("sourceCommit") != reference.get("sourceCommit"):
        raise ChainError("genesis enumeration source commit mismatch")
    entries = enumeration.get("entries")
    if not isinstance(entries, list) or len(entries) != reference.get("entryCount"):
        raise ChainError("genesis enumeration entry count mismatch")
    if enumeration.get("entryCount") != len(entries):
        raise ChainError("genesis enumeration self-declared entry count mismatch")
    previous_path = ""
    listed: set[str] = set()
    total_size = 0
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "size"}:
            raise ChainError("invalid genesis enumeration entry")
        logical = entry.get("path")
        digest = entry.get("sha256")
        size = entry.get("size")
        if not isinstance(logical, str) or not logical.startswith("records/"):
            raise ChainError(f"invalid genesis enumeration path: {logical!r}")
        if logical <= previous_path or logical in listed:
            raise ChainError(
                "genesis enumeration paths are not strictly sorted and unique"
            )
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise ChainError(f"invalid genesis enumeration hash for {logical}")
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise ChainError(f"invalid genesis enumeration size for {logical}")
        path = physical_path(records, logical)
        if not path.is_file() or path.is_symlink():
            raise ChainError(f"enumerated legacy record is missing: {logical}")
        raw_file = path.read_bytes()
        if len(raw_file) != size:
            raise ChainError(
                f"enumerated legacy record size mismatch for {logical}: "
                f"expected {size}, got {len(raw_file)}"
            )
        actual = hashlib.sha256(raw_file).hexdigest()
        if actual != digest:
            raise ChainError(
                f"enumerated legacy record hash mismatch for {logical}: "
                f"expected {digest}, got {actual}"
            )
        listed.add(logical)
        previous_path = logical
        total_size += size
    if total_size != enumeration.get("totalSize") or total_size != reference.get(
        "totalSize"
    ):
        raise ChainError("genesis enumeration total size mismatch")
    _verify_enumeration_against_git(
        records, str(enumeration.get("sourceCommit", "")), entries
    )

    genesis_commitment = commitments.get("chainGenesis")
    if not isinstance(genesis_commitment, dict):
        raise ChainError("cutover lacks CHAIN_GENESIS commitment")
    genesis_path = records / "CHAIN_GENESIS.json"
    if genesis_commitment != {
        "path": "records/CHAIN_GENESIS.json",
        "sha256": sha256_file(genesis_path),
        "size": genesis_path.stat().st_size,
        "canonicalJsonSha256": canonical_sha256(genesis),
    }:
        raise ChainError("cutover CHAIN_GENESIS commitment mismatch")

    trust_reference = genesis.get("tsaTrustBundle")
    trust_commitment = commitments.get("tsaTrustBundle")
    if not isinstance(trust_reference, dict) or trust_commitment != trust_reference:
        raise ChainError("cutover TSA trust-bundle commitment mismatch")
    _load_trust_bundle(records, trust_reference)

    legacy_entries = genesis.get("legacyDigests")
    if not isinstance(legacy_entries, list):
        raise ChainError("genesis legacyDigests must be a list")
    enumeration_by_path = {entry["path"]: entry for entry in entries}
    for entry in legacy_entries:
        if not isinstance(entry, dict):
            raise ChainError("legacy digest entry must be an object")
        enumerated = enumeration_by_path.get(entry.get("path"))
        if not enumerated or enumerated["sha256"] != entry.get("sha256"):
            raise ChainError(
                "legacy digest is not identically committed by the full "
                f"enumeration: {entry.get('path')}"
            )


def verify_chain(
    records: Path,
    *,
    now: datetime | None = None,
    allow_pre_enumeration: bool = False,
    bootstrap_trust_bundle: dict[str, Any] | None = None,
) -> ChainVerification:
    records = records.resolve()
    genesis_path = records / "CHAIN_GENESIS.json"
    if not genesis_path.is_file():
        raise ChainError(f"missing chain genesis: {genesis_path}")
    genesis = load_json(genesis_path)
    if genesis.get("schemaVersion") != "thesis_record_chain_genesis_v1":
        raise ChainError(
            f"unsupported genesis schema: {genesis.get('schemaVersion')!r}"
        )
    if not allow_pre_enumeration and (
        "legacyEnumeration" not in genesis
        or "enumerationCutoverSnapshot" not in genesis
    ):
        raise ChainError(
            "chain lacks the mandatory complete genesis enumeration cutover"
        )

    legacy_entries = genesis.get("legacyDigests")
    if not isinstance(legacy_entries, list):
        raise ChainError("genesis legacyDigests must be a list")
    listed_legacy: set[str] = set()
    for entry in legacy_entries:
        if not isinstance(entry, dict):
            raise ChainError("legacy digest entry must be an object")
        logical = str(entry.get("path"))
        if logical in listed_legacy:
            raise ChainError(f"duplicate legacy digest in genesis: {logical}")
        listed_legacy.add(logical)
        path = physical_path(records, logical)
        if not path.is_file():
            raise ChainError(f"genesis-listed legacy digest is missing: {logical}")
        actual = sha256_file(path)
        if actual != entry.get("sha256"):
            raise ChainError(
                f"legacy digest hash mismatch for {logical}: "
                f"expected {entry.get('sha256')}, got {actual}"
            )
    discovered_legacy = {
        logical_path(records, path) for path in records.glob("????-??-??/digest.json")
    }
    if discovered_legacy != listed_legacy:
        raise ChainError(
            "legacy digest enumeration mismatch: "
            f"unlisted={sorted(discovered_legacy - listed_legacy)}, "
            f"missing={sorted(listed_legacy - discovered_legacy)}"
        )

    snapshots = snapshot_paths(records)
    first_logical = genesis.get("firstSnapshot")
    if not isinstance(first_logical, str) or not first_logical:
        raise ChainError("genesis firstSnapshot must name one snapshot")
    first = physical_path(records, first_logical)
    if first not in snapshots:
        raise ChainError(f"genesis snapshot is missing or malformed: {first_logical}")

    snapshot_set = set(snapshots)
    successors: dict[Path, list[Path]] = {path: [] for path in snapshots}
    payloads: dict[Path, dict[str, Any]] = {}
    for path in snapshots:
        payload = load_json(path)
        payloads[path] = payload
        if payload.get("schemaVersion") != "thesis_record_snapshot_v2":
            raise ChainError(f"unsupported snapshot schema in {path}")
        _creation_claims(payload)
        chain = payload.get("chain")
        if path == first:
            if chain is not None:
                raise ChainError(
                    f"genesis snapshot must not have a chain block: {path}"
                )
        else:
            if not isinstance(chain, dict):
                raise ChainError(f"missing chain block after genesis: {path}")
            previous_logical = chain.get("prevDigestPath")
            if not isinstance(previous_logical, str):
                raise ChainError(f"missing chain.prevDigestPath in {path}")
            previous = physical_path(records, previous_logical)
            if previous not in snapshot_set:
                raise ChainError(f"missing predecessor for {path}: {previous_logical}")
            expected_sha = sha256_file(previous)
            if chain.get("prevDigestSha256") != expected_sha:
                raise ChainError(
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
            raise ChainError(
                f"fork after {logical_path(records, cursor)}: "
                + ", ".join(logical_path(records, child) for child in children)
            )
        cursor = children[0]
        if cursor in visited:
            raise ChainError(f"cycle at {logical_path(records, cursor)}")
        visited.add(cursor)
        ordered.append(cursor)
    if visited != snapshot_set:
        raise ChainError(
            "orphaned snapshot(s) not reachable from genesis: "
            + ", ".join(
                logical_path(records, path) for path in sorted(snapshot_set - visited)
            )
        )

    commitment_snapshots = [
        path for path in ordered if "genesisCommitments" in payloads[path]
    ]
    cutover_kind_snapshots = [
        path
        for path in ordered
        if payloads[path].get("snapshotKind") == "genesis_enumeration_cutover"
    ]
    if len(commitment_snapshots) > 1 or len(cutover_kind_snapshots) > 1:
        raise ChainError("record chain contains more than one genesis cutover")
    if commitment_snapshots != cutover_kind_snapshots:
        raise ChainError(
            "genesisCommitments may appear only on the unique enumeration cutover"
        )

    if bootstrap_trust_bundle is not None:
        if not allow_pre_enumeration or "tsaTrustBundle" in genesis:
            raise ChainError(
                "explicit trust bootstrap is only allowed for a pre-enumeration chain"
            )
        bundle_path, _bundle = _load_trust_bundle(records, bootstrap_trust_bundle)
        active_bundles = {logical_path(records, bundle_path): bootstrap_trust_bundle}
    else:
        active_bundles = _bootstrap_trust_bundles(
            records,
            genesis,
            required=not allow_pre_enumeration or "tsaTrustBundle" in genesis,
        )
    pending_updates: list[dict[str, Any]] = []
    witnesses: dict[Path, WitnessEvidence] = {}
    for path in ordered:
        evidence = verify_witness(
            path,
            records=records,
            now=now,
            trusted_bundles=active_bundles,
        )
        witnesses[path] = evidence
        pending_updates.extend(_trust_bundle_updates(records, payloads[path]))
        # A trust-set transition becomes authoritative only after an external
        # witness made with an already-active bundle covers the transition.
        # Therefore a snapshot can never bootstrap the bundle used by its own
        # token; unavailable markers leave updates pending for a later old-key
        # witness.
        if evidence.status == "available":
            _activate_trust_bundles(active_bundles, pending_updates)
            pending_updates.clear()

    cutover_logical = genesis.get("enumerationCutoverSnapshot")
    cutover_path: Path | None = None
    if "legacyEnumeration" in genesis or cutover_logical is not None:
        if not isinstance(cutover_logical, str):
            raise ChainError("genesis enumeration cutover path is missing")
        cutover_path = physical_path(records, cutover_logical)
        if cutover_path not in visited:
            raise ChainError(
                "genesis enumeration cutover is absent from the reachable chain"
            )
        if payloads[cutover_path].get("snapshotKind") != "genesis_enumeration_cutover":
            raise ChainError(
                "named genesis enumeration cutover has the wrong snapshot kind"
            )
        if commitment_snapshots != [cutover_path]:
            raise ChainError(
                "named genesis enumeration cutover is not the unique committed cutover"
            )
        _verify_enumeration(records, genesis, payloads[cutover_path])
        legacy_tip = payloads[first].get("legacyTip")
        if not isinstance(legacy_tip, dict) or legacy_tip != legacy_entries[-1]:
            raise ChainError(
                "first chained snapshot legacyTip differs from CHAIN_GENESIS"
            )
        first_dependencies = payloads[first].get("dependencies")
        recorder_commit = (
            first_dependencies.get("recorderRepositoryCommit")
            if isinstance(first_dependencies, dict)
            else None
        )
        source_commit = genesis["legacyEnumeration"].get("sourceCommit")
        if source_commit != recorder_commit:
            raise ChainError(
                "genesis enumeration source commit differs from the first "
                "snapshot recorderRepositoryCommit"
            )
    elif not allow_pre_enumeration:
        raise ChainError(
            "chain lacks the mandatory complete genesis enumeration cutover"
        )

    head_path = records / "CHAIN_HEAD.json"
    if not head_path.is_file():
        raise ChainError(f"missing chain head commitment: {head_path}")
    head = load_json(head_path)
    if head.get("schemaVersion") != "thesis_record_chain_head_v1":
        raise ChainError(
            f"unsupported chain head schema: {head.get('schemaVersion')!r}"
        )
    expected_head_path = logical_path(records, ordered[-1])
    expected_head_sha = sha256_file(ordered[-1])
    if head.get("snapshotPath") != expected_head_path:
        raise ChainError(
            f"chain head path mismatch: expected {expected_head_path}, "
            f"got {head.get('snapshotPath')}"
        )
    if head.get("snapshotSha256") != expected_head_sha:
        raise ChainError(
            f"chain head hash mismatch: expected {expected_head_sha}, "
            f"got {head.get('snapshotSha256')}"
        )
    return ChainVerification(
        ordered=tuple(ordered),
        witnesses=witnesses,
        enumeration_cutover=cutover_path,
    )


def verify_records(
    records: Path,
    *,
    now: datetime | None = None,
    allow_pre_enumeration: bool = False,
) -> list[Path]:
    """Compatibility wrapper returning the ordered snapshot paths."""

    return list(
        verify_chain(
            records,
            now=now,
            allow_pre_enumeration=allow_pre_enumeration,
        ).ordered
    )


def main() -> int:
    records = Path(sys.argv[1] if len(sys.argv) > 1 else "records")
    try:
        verification = verify_chain(records)
    except ChainError as exc:
        print(f"CHAIN BROKEN: {exc}", file=sys.stderr)
        return 1
    available = [
        (path, evidence)
        for path, evidence in verification.witnesses.items()
        if evidence.status == "available"
    ]
    for path, evidence in available:
        print(
            "witness OK: "
            f"{logical_path(records.resolve(), path)} genTime={evidence.gen_time} "
            f"policy={evidence.policy_oid} anchor={evidence.anchor_id}"
        )
    print(
        f"chain OK: {len(verification.ordered)} snapshot(s), "
        f"availableWitnesses={len(available)}, head={verification.ordered[-1]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
