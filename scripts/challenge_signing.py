"""Submitter-side keyless signing for challenge-lane submissions.

Design: https://github.com/ThesisInstitute/thesis/issues/52

Challengers may sign the exact submission file they PR into
``challenge/inbox/<name>/<cell>.json`` with Sigstore keyless signing
(cosign or sigstore-python; GitHub OIDC identity). The signature bundle
lands beside the submission as ``<cell>.json.sigstore.json`` — the
sigstore CLI's default output name — and the Rekor transparency log gives
the artifact digest an independent public timestamp. Verification then
establishes two claims without trusting this repository:

- **this exact artifact**: the bundle's signature covers the submission
  file's bytes (sha256 digest match); and
- **before the release**: the Rekor entry's ``integratedTime`` (covered by
  Rekor's signed entry timestamp, which bundle verification checks)
  strictly precedes the target's release instant.

Signing is optional: unsigned submissions remain valid and attributed via
the GitHub identity that opened the PR (the first submission, PR #49,
predates this and is grandfathered). The certificate identity is recorded,
not enforced, by default — a keyless certificate obtained through the
Sigstore OAuth flow names a GitHub-verified email, which has no mechanical
mapping to the ``challenger`` account field; account attribution stays
with the PR. ``--require-identity`` exists for flows (e.g. signing from a
GitHub Actions run in the challenger's fork) where the certificate does
name a checkable identity.

This module distributes *proof*, never signing authority: publish-side
signing (producer signatures, workflow attestations, RFC 3161 witnesses)
stays CI-only and is untouched. Nothing here reads or writes records/**.

Mechanism notes (verified against the live log, 2026-07-31): a Rekor entry
UUID is the RFC 6962 leaf hash ``sha256(0x00 || canonicalizedBody)`` of the
entry's canonicalized body; the 80-character form returned by the Rekor API
prefixes the 16-hex-character tree ID. ``integratedTime`` is a Unix
timestamp in seconds.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
import pathlib
import re
import stat
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
INBOX_RELPATH = pathlib.Path("challenge") / "inbox"
BUNDLE_SUFFIX = ".sigstore.json"
SUBMISSION_SCHEMA = "thesis_challenge_submission_v1"
SIGNATURE_PROVENANCE_SCHEMA = "thesis_challenge_signature_v1"
GENERATED_TARGETS_RELPATH = (
    pathlib.Path("site") / "src" / "data" / "ledger-targets.generated.ts"
)
BUNDLE_MEDIA_TYPE_PREFIX = "application/vnd.dev.sigstore.bundle"
CHALLENGER_RE = re.compile(r"^github:[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Fulcio certificate extension carrying the OIDC issuer. The V2 OID wraps a
# DER UTF8String; the deprecated V1 OID carries the raw value.
_FULCIO_ISSUER_V2_OID = "1.3.6.1.4.1.57264.1.8"
_FULCIO_ISSUER_V1_OID = "1.3.6.1.4.1.57264.1.1"


class ChallengeSigningError(RuntimeError):
    """A refusal to sign, parse, or verify a challenge submission."""


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ensure_regular_file(path: pathlib.Path, *, label: str) -> None:
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise ChallengeSigningError(f"missing {label}: {path}") from exc
    except OSError as exc:
        raise ChallengeSigningError(f"cannot inspect {label} {path}: {exc}") from exc
    if not stat.S_ISREG(metadata.st_mode):
        raise ChallengeSigningError(f"{label} is not a regular file: {path}")


def inbox_root(repo_root: pathlib.Path | None = None) -> pathlib.Path:
    return (repo_root or REPO_ROOT) / INBOX_RELPATH


def bundle_path_for(submission: pathlib.Path) -> pathlib.Path:
    """The sidecar bundle path: ``<cell>.json`` -> ``<cell>.json.sigstore.json``.

    This is the sigstore CLI's default output name, so
    ``uvx sigstore sign <submission>`` lands the bundle where the verifier
    looks with no extra flags.
    """

    return submission.with_name(submission.name + BUNDLE_SUFFIX)


@dataclass(frozen=True)
class InboxAudit:
    submissions: list[pathlib.Path]
    bundles: dict[pathlib.Path, pathlib.Path]
    orphan_bundles: list[pathlib.Path]
    unexpected: list[pathlib.Path]


def audit_inbox(root: pathlib.Path) -> InboxAudit:
    """Enumerate the challenge inbox fail-closed.

    Submissions are ``*.json`` regular files; each may have exactly one
    sidecar bundle named by :func:`bundle_path_for`. Bundles without a
    submission and files of any other kind are surfaced for refusal rather
    than skipped.
    """

    if not root.is_dir():
        raise ChallengeSigningError(f"challenge inbox is missing: {root}")
    submissions: list[pathlib.Path] = []
    bundles: dict[pathlib.Path, pathlib.Path] = {}
    orphans: list[pathlib.Path] = []
    unexpected: list[pathlib.Path] = []
    for path in sorted(root.rglob("*")):
        if path.is_dir() and not path.is_symlink():
            continue
        relative = path.relative_to(root)
        if path.is_symlink() or not path.is_file():
            unexpected.append(relative)
            continue
        if path.name == "README.md":
            continue
        if path.name.endswith(BUNDLE_SUFFIX):
            continue  # paired below, orphans detected after the scan
        if path.suffix == ".json":
            submissions.append(path)
            continue
        unexpected.append(relative)
    submission_set = set(submissions)
    for path in sorted(root.rglob(f"*{BUNDLE_SUFFIX}")):
        if path.is_symlink() or not path.is_file():
            unexpected.append(path.relative_to(root))
            continue
        owner = path.with_name(path.name[: -len(BUNDLE_SUFFIX)])
        if owner in submission_set:
            bundles[owner] = path
        else:
            orphans.append(path.relative_to(root))
    return InboxAudit(
        submissions=submissions,
        bundles=bundles,
        orphan_bundles=orphans,
        unexpected=unexpected,
    )


def load_submission(path: pathlib.Path) -> dict[str, Any]:
    _ensure_regular_file(path, label="challenge submission")
    try:
        payload = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        raise ChallengeSigningError(
            f"challenge submission is not readable JSON: {path}: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise ChallengeSigningError(
            f"challenge submission must be a JSON object: {path}"
        )
    if payload.get("schemaVersion") != SUBMISSION_SCHEMA:
        raise ChallengeSigningError(
            "unsupported challenge submission schema in "
            f"{path}: {payload.get('schemaVersion')!r}"
        )
    challenger = payload.get("challenger")
    if not isinstance(challenger, str) or not CHALLENGER_RE.fullmatch(challenger):
        raise ChallengeSigningError(
            f"challenge submission must name a github:<login> challenger: {path}"
        )
    data_point_id = payload.get("dataPointId")
    if not isinstance(data_point_id, str) or not data_point_id:
        raise ChallengeSigningError(
            f"challenge submission must name a dataPointId: {path}"
        )
    return payload


def rekor_entry_uuid(canonicalized_body_b64: str) -> str:
    """RFC 6962 leaf hash of the canonicalized body = the Rekor entry UUID.

    Verified against the public log 2026-07-31 (entries 150000000 and
    512345678): ``sha256(0x00 || body)`` equals the 64-hex UUID; the API's
    80-character entry ID prefixes the tree ID.
    """

    try:
        body = base64.b64decode(canonicalized_body_b64, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ChallengeSigningError(
            f"bundle canonicalizedBody is not valid base64: {exc}"
        ) from exc
    return hashlib.sha256(b"\x00" + body).hexdigest()


def _int_field(value: Any, *, label: str) -> int:
    """Protobuf JSON renders int64 as strings; accept both, fail closed."""

    if isinstance(value, bool):
        raise ChallengeSigningError(f"bundle {label} must be an integer")
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    raise ChallengeSigningError(f"bundle {label} must be an integer: {value!r}")


@dataclass(frozen=True)
class BundleMetadata:
    media_type: str
    log_index: int
    log_id_key_id: str
    integrated_time: int
    entry_uuid: str
    entry_kind: str
    tlog_entry_count: int
    message_digest_sha256: str | None


def parse_bundle_metadata(bundle: dict[str, Any]) -> BundleMetadata:
    """Extract transparency-log metadata from a Sigstore bundle's JSON.

    Metadata comes straight from the serialized bundle so it can be read
    without the sigstore package; nothing here is trusted until
    :func:`verify_submission` cryptographically verifies the same bundle.
    """

    media_type = bundle.get("mediaType")
    if not isinstance(media_type, str) or not media_type.startswith(
        BUNDLE_MEDIA_TYPE_PREFIX
    ):
        raise ChallengeSigningError(f"not a Sigstore bundle (mediaType {media_type!r})")
    material = bundle.get("verificationMaterial")
    if not isinstance(material, dict):
        raise ChallengeSigningError("bundle is missing verificationMaterial")
    entries = material.get("tlogEntries")
    if not isinstance(entries, list) or not entries:
        raise ChallengeSigningError(
            "bundle carries no transparency-log entry; sign with Rekor "
            "upload enabled (the sigstore CLI default)"
        )
    entry = entries[0]
    if not isinstance(entry, dict):
        raise ChallengeSigningError("bundle tlogEntries[0] is malformed")
    log_id = entry.get("logId")
    key_id = log_id.get("keyId") if isinstance(log_id, dict) else None
    if not isinstance(key_id, str) or not key_id:
        raise ChallengeSigningError("bundle tlog entry is missing logId.keyId")
    body = entry.get("canonicalizedBody")
    if not isinstance(body, str) or not body:
        raise ChallengeSigningError("bundle tlog entry is missing canonicalizedBody")
    kind_version = entry.get("kindVersion")
    kind = kind_version.get("kind") if isinstance(kind_version, dict) else None
    if not isinstance(kind, str) or not kind:
        raise ChallengeSigningError("bundle tlog entry is missing kindVersion.kind")
    digest: str | None = None
    message_signature = bundle.get("messageSignature")
    if isinstance(message_signature, dict):
        message_digest = message_signature.get("messageDigest")
        if isinstance(message_digest, dict):
            algorithm = message_digest.get("algorithm")
            encoded = message_digest.get("digest")
            if algorithm != "SHA2_256" or not isinstance(encoded, str):
                raise ChallengeSigningError("bundle messageDigest must be SHA2_256")
            try:
                digest = base64.b64decode(encoded, validate=True).hex()
            except (binascii.Error, ValueError) as exc:
                raise ChallengeSigningError(
                    f"bundle messageDigest is not valid base64: {exc}"
                ) from exc
    return BundleMetadata(
        media_type=media_type,
        log_index=_int_field(entry.get("logIndex"), label="logIndex"),
        log_id_key_id=key_id,
        integrated_time=_int_field(entry.get("integratedTime"), label="integratedTime"),
        entry_uuid=rekor_entry_uuid(body),
        entry_kind=kind,
        tlog_entry_count=len(entries),
        message_digest_sha256=digest,
    )


def parse_utc_instant(value: str, *, label: str) -> datetime:
    """Parse an ISO-8601 instant; date-only values floor to 00:00:00Z.

    The day floor is deliberate chronology conservatism: a date-granularity
    release field proves nothing about intraday order, so the signature must
    precede the earliest instant of the release day.
    """

    if _DATE_RE.fullmatch(value):
        value = f"{value}T00:00:00+00:00"
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ChallengeSigningError(f"{label} is not ISO-8601: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ChallengeSigningError(f"{label} must carry an explicit offset: {value!r}")
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class ReleaseInstant:
    instant: datetime
    source: str


def release_instant_for(
    data_point_id: str,
    targets_path: pathlib.Path | None = None,
) -> ReleaseInstant:
    """Conservative release instant for a registered target.

    Line-scans the generated targets module (the same authority
    ``resolve_pending.py`` reads) for the target's ``resolutionDate`` and
    ``sourceBinding.expectedReleaseWindow.start``, and returns the earlier
    day floor. Fails closed when the target is absent or carries neither
    field.
    """

    path = targets_path or (REPO_ROOT / GENERATED_TARGETS_RELPATH)
    _ensure_regular_file(path, label="generated targets module")
    current: str | None = None
    resolution_date: str | None = None
    window_start: str | None = None
    found = False
    for line in path.read_text().splitlines():
        dpid = re.search(r'dataPointId:\s*"([^"]+)"', line)
        if dpid:
            if found:
                break  # end of the matched target's block
            current = dpid.group(1)
            if current == data_point_id:
                found = True
            continue
        if not found:
            continue
        rdate = re.search(r'resolutionDate:\s*"([^"]+)"', line)
        if rdate:
            resolution_date = rdate.group(1)
            continue
        binding = re.search(r"sourceBinding:\s*(\{.*\}),?\s*$", line)
        if binding:
            try:
                parsed = json.loads(binding.group(1))
            except ValueError as exc:
                raise ChallengeSigningError(
                    f"sourceBinding for {data_point_id} is not valid JSON: {exc}"
                ) from exc
            window = parsed.get("expectedReleaseWindow")
            if isinstance(window, dict) and isinstance(window.get("start"), str):
                window_start = window["start"]
    if not found:
        raise ChallengeSigningError(
            f"target is not in the generated registry: {data_point_id}"
        )
    candidates: list[datetime] = []
    if resolution_date:
        candidates.append(parse_utc_instant(resolution_date, label="resolutionDate"))
    if window_start:
        candidates.append(
            parse_utc_instant(window_start, label="expectedReleaseWindow.start")
        )
    if not candidates:
        raise ChallengeSigningError(
            f"registered target carries no release date: {data_point_id}"
        )
    return ReleaseInstant(instant=min(candidates), source="registry_day_floor")


def extract_certificate_identity(
    certificate_der: bytes,
) -> tuple[list[str], str | None]:
    """Subject Alternative Names and the Fulcio OIDC issuer from a leaf cert."""

    try:
        from cryptography import x509
        from cryptography.x509.oid import ExtensionOID, ObjectIdentifier
    except ImportError as exc:  # pragma: no cover - ships with the extra
        raise ChallengeSigningError(
            "certificate parsing requires the cryptography package "
            "(install the 'challenge' extra)"
        ) from exc

    cert = x509.load_der_x509_certificate(certificate_der)
    subjects: list[str] = []
    try:
        san = cert.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        )
    except x509.ExtensionNotFound:
        pass
    else:
        for name in san.value:
            value = getattr(name, "value", None)
            if isinstance(value, str):
                subjects.append(value)
    issuer: str | None = None
    for oid, wrapped in (
        (_FULCIO_ISSUER_V2_OID, True),
        (_FULCIO_ISSUER_V1_OID, False),
    ):
        try:
            extension = cert.extensions.get_extension_for_oid(ObjectIdentifier(oid))
        except x509.ExtensionNotFound:
            continue
        raw = extension.value.value  # UnrecognizedExtension payload bytes
        if wrapped:
            # DER UTF8String: tag 0x0c, short-form length, then the value.
            if len(raw) >= 2 and raw[0] == 0x0C and raw[1] == len(raw) - 2:
                issuer = raw[2:].decode("utf-8", errors="strict")
        else:
            issuer = raw.decode("utf-8", errors="replace")
        if issuer:
            break
    return subjects, issuer


def _cryptographic_verify(
    submission_bytes: bytes,
    bundle_text: str,
    *,
    staging: bool,
    expected_identity: str | None,
    expected_issuer: str | None,
) -> bytes:
    """Verify the bundle with sigstore-python; return the leaf cert DER.

    This is the module's only trust decision and is delegated entirely to
    the sigstore package (Fulcio chain, SCT, Rekor inclusion, signed entry
    timestamp, and the signature over the artifact bytes). Raises
    ``ChallengeSigningError`` on any failure.
    """

    try:
        from sigstore.errors import VerificationError
        from sigstore.models import Bundle, InvalidBundle
        from sigstore.verify import Verifier, policy
    except ImportError as exc:
        raise ChallengeSigningError(
            "submitter signature verification requires the sigstore package "
            "(install the 'challenge' extra: uv sync --extra challenge)"
        ) from exc

    try:
        bundle = Bundle.from_json(bundle_text)
    except InvalidBundle as exc:
        raise ChallengeSigningError(f"invalid Sigstore bundle: {exc}") from exc
    if expected_identity is not None:
        verification_policy: Any = policy.Identity(
            identity=expected_identity, issuer=expected_issuer
        )
    else:
        # Certificate identity is recorded, not enforced (see module
        # docstring); the cryptographic claims stay fully verified.
        verification_policy = policy.UnsafeNoOp()
    verifier = Verifier.staging() if staging else Verifier.production()
    try:
        verifier.verify_artifact(submission_bytes, bundle, verification_policy)
    except VerificationError as exc:
        raise ChallengeSigningError(f"signature verification failed: {exc}") from exc
    certificate = bundle.signing_certificate
    if certificate is None:
        raise ChallengeSigningError("bundle carries no signing certificate")
    from cryptography.hazmat.primitives.serialization import Encoding

    return certificate.public_bytes(Encoding.DER)


@dataclass(frozen=True)
class SignatureVerification:
    submission_path: pathlib.Path
    bundle_path: pathlib.Path
    artifact_sha256: str
    metadata: BundleMetadata
    certificate_subjects: list[str]
    certificate_oidc_issuer: str | None
    identity_enforced: bool
    integrated_time_utc: datetime
    release_instant_utc: datetime | None
    release_instant_source: str | None
    precedes_release: bool | None


def verify_submission(
    submission_path: pathlib.Path,
    bundle_path: pathlib.Path | None = None,
    *,
    release_at: datetime | None = None,
    targets_path: pathlib.Path | None = None,
    expected_identity: str | None = None,
    expected_issuer: str | None = None,
    staging: bool = False,
    verify_fn: Callable[..., bytes] | None = None,
) -> SignatureVerification:
    """Fully verify one signed submission (crypto, digest, chronology)."""

    if expected_identity is not None and expected_issuer is None:
        raise ChallengeSigningError(
            "an expected identity needs an expected OIDC issuer (a bare "
            "identity is meaningless without the issuer that vouched for it)"
        )
    submission = load_submission(submission_path)
    bundle_path = bundle_path or bundle_path_for(submission_path)
    _ensure_regular_file(bundle_path, label="signature bundle")
    try:
        bundle_text = bundle_path.read_text()
        bundle_json = json.loads(bundle_text)
    except (OSError, ValueError) as exc:
        raise ChallengeSigningError(
            f"signature bundle is not readable JSON: {bundle_path}: {exc}"
        ) from exc
    if not isinstance(bundle_json, dict):
        raise ChallengeSigningError(
            f"signature bundle must be a JSON object: {bundle_path}"
        )
    metadata = parse_bundle_metadata(bundle_json)
    if metadata.entry_kind != "hashedrekord":
        raise ChallengeSigningError(
            "challenge submissions must be signed as blobs (hashedrekord); "
            f"got tlog entry kind {metadata.entry_kind!r}"
        )
    submission_bytes = submission_path.read_bytes()
    artifact_sha256 = hashlib.sha256(submission_bytes).hexdigest()
    if (
        metadata.message_digest_sha256 is not None
        and metadata.message_digest_sha256 != artifact_sha256
    ):
        raise ChallengeSigningError(
            "bundle was made for a different artifact: digest "
            f"{metadata.message_digest_sha256} != file {artifact_sha256} "
            f"({submission_path})"
        )
    certificate_der = (verify_fn or _cryptographic_verify)(
        submission_bytes,
        bundle_text,
        staging=staging,
        expected_identity=expected_identity,
        expected_issuer=expected_issuer,
    )
    subjects, issuer = extract_certificate_identity(certificate_der)
    integrated = datetime.fromtimestamp(metadata.integrated_time, tz=timezone.utc)

    release: ReleaseInstant | None = None
    if release_at is not None:
        if release_at.tzinfo is None:
            raise ChallengeSigningError("release_at must be timezone-aware")
        release = ReleaseInstant(
            instant=release_at.astimezone(timezone.utc), source="explicit"
        )
    else:
        release = release_instant_for(
            str(submission["dataPointId"]), targets_path=targets_path
        )
    precedes = integrated < release.instant
    return SignatureVerification(
        submission_path=submission_path,
        bundle_path=bundle_path,
        artifact_sha256=artifact_sha256,
        metadata=metadata,
        certificate_subjects=subjects,
        certificate_oidc_issuer=issuer,
        identity_enforced=expected_identity is not None,
        integrated_time_utc=integrated,
        release_instant_utc=release.instant,
        release_instant_source=release.source,
        precedes_release=precedes,
    )


def _utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def signature_provenance_block(
    verification: SignatureVerification,
    *,
    repo_root: pathlib.Path | None = None,
) -> dict[str, Any]:
    """The block the publish adapter stores on the published challenge record.

    The adapter records this verbatim alongside the merge SHA it already
    stores, giving every published challenge record both custody legs: the
    repository's (merge SHA -> witnessed records chain) and the
    platform-independent one (artifact digest -> Rekor entry).
    """

    root = (repo_root or REPO_ROOT).resolve()

    def _relative(path: pathlib.Path) -> str:
        return path.resolve().relative_to(root).as_posix()

    return {
        "schemaVersion": SIGNATURE_PROVENANCE_SCHEMA,
        "scheme": "sigstore_keyless",
        "artifactPath": _relative(verification.submission_path),
        "artifactSha256": verification.artifact_sha256,
        "bundlePath": _relative(verification.bundle_path),
        "bundleMediaType": verification.metadata.media_type,
        "certificateSubjects": list(verification.certificate_subjects),
        "certificateOidcIssuer": verification.certificate_oidc_issuer,
        "identityPolicy": (
            "enforced" if verification.identity_enforced else "recorded_not_enforced"
        ),
        "rekorLogIndex": verification.metadata.log_index,
        "rekorLogIdKeyId": verification.metadata.log_id_key_id,
        "rekorEntryUuid": verification.metadata.entry_uuid,
        "rekorIntegratedTimeUtc": _utc_iso(verification.integrated_time_utc),
        "precedesRelease": verification.precedes_release,
        "releaseInstantUtc": (
            _utc_iso(verification.release_instant_utc)
            if verification.release_instant_utc
            else None
        ),
        "releaseInstantSource": verification.release_instant_source,
    }
