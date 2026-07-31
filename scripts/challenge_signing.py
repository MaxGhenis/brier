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


_LOGIN_DIR_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
_CELL_FILE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\.json$")


def _conforming_relative(relative: pathlib.Path, *, suffix: str) -> bool:
    """Inbox entries are exactly ``<login>/<cell>.json`` (+ bundle suffix).

    The shape rule doubles as output-injection defense: printed paths can
    only contain characters from these anchored patterns, so a Git-valid
    filename embedding a newline or other control bytes lands in
    ``unexpected`` and fails the sweep instead of forging status lines.
    """

    if len(relative.parts) != 2:
        return False
    login, name = relative.parts
    if not _LOGIN_DIR_RE.fullmatch(login):
        return False
    if suffix:
        if not name.endswith(suffix):
            return False
        name = name[: -len(suffix)]  # <cell>.json.sigstore.json -> <cell>.json
    return bool(_CELL_FILE_RE.fullmatch(name)) and not name.endswith(".sigstore.json")


def audit_inbox(root: pathlib.Path) -> InboxAudit:
    """Enumerate the challenge inbox fail-closed.

    Submissions are ``<login>/<cell>.json`` regular files; each may have
    exactly one sidecar bundle named by :func:`bundle_path_for`. Bundles
    without a submission, files at any other depth or name shape, symlinks
    anywhere (including the inbox root itself), and non-root README.md
    files are surfaced for refusal rather than skipped.
    """

    if root.is_symlink():
        raise ChallengeSigningError(f"challenge inbox root is a symlink: {root}")
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
        if relative == pathlib.Path("README.md"):
            continue  # the one root-level doc; nested READMEs are unexpected
        if path.name.endswith(BUNDLE_SUFFIX):
            if _conforming_relative(relative, suffix=BUNDLE_SUFFIX):
                continue  # paired below; orphans detected after the scan
            unexpected.append(relative)
            continue
        if _conforming_relative(relative, suffix=""):
            submissions.append(path)
            continue
        unexpected.append(relative)
    submission_set = set(submissions)
    for path in sorted(root.rglob(f"*{BUNDLE_SUFFIX}")):
        relative = path.relative_to(root)
        if path.is_symlink() or not path.is_file():
            continue  # already listed as unexpected above
        if not _conforming_relative(relative, suffix=BUNDLE_SUFFIX):
            continue  # already listed as unexpected above
        owner = path.with_name(path.name[: -len(BUNDLE_SUFFIX)])
        if owner in submission_set:
            bundles[owner] = path
        else:
            orphans.append(relative)
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
    has_inclusion_promise: bool
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
    if len(entries) != 1:
        # Matches sigstore-python's own bundle rule; with several entries the
        # "which entry timestamps this artifact" question becomes ambiguous.
        raise ChallengeSigningError(
            "bundle must contain exactly one transparency-log entry; got "
            f"{len(entries)}"
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
    promise = entry.get("inclusionPromise")
    has_promise = isinstance(promise, dict) and bool(
        promise.get("signedEntryTimestamp")
    )
    return BundleMetadata(
        media_type=media_type,
        log_index=_int_field(entry.get("logIndex"), label="logIndex"),
        log_id_key_id=key_id,
        integrated_time=_int_field(entry.get("integratedTime"), label="integratedTime"),
        entry_uuid=rekor_entry_uuid(body),
        entry_kind=kind,
        has_inclusion_promise=has_promise,
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


@dataclass(frozen=True)
class VerifiedEntry:
    """Values read back from the cryptographically verified bundle object.

    Only produced after sigstore verification succeeds AND the bundle's
    transparency-log entry carries a verified Signed Entry Timestamp, so
    ``integrated_time``, ``log_index``, ``log_id_key_id``, and the
    canonicalized body behind ``entry_uuid`` are all covered by Rekor's
    signature over the entry's canonical payload — never by unverified
    bundle JSON.
    """

    certificate_der: bytes
    integrated_time: int
    log_index: int
    log_id_key_id: str
    entry_uuid: str
    environment: str


def _cryptographic_verify(
    submission_bytes: bytes,
    bundle_text: str,
    *,
    staging: bool,
    offline: bool = False,
    expected_identity: str | None,
    expected_issuer: str | None,
) -> VerifiedEntry:
    """Verify the bundle with sigstore-python; return authenticated values.

    This is the module's only trust decision and is delegated entirely to
    the sigstore package (Fulcio chain, SCT, Merkle inclusion proof against
    the signed checkpoint, Signed Entry Timestamp, and the signature over
    the artifact bytes). Chronology values are read back from the verified
    bundle object — never trusted from pre-verification JSON — and require
    a verified SET: sigstore 4.5.0 accepts v0.2+ bundles with no inclusion
    promise when an RFC 3161 timestamp is present, and only verifies the
    SET when the promise exists alongside a nonzero ``integratedTime``
    (``sigstore/models.py`` ``TransparencyLogEntry._verify``), so both are
    required here or the bundle is refused for chronology purposes.
    Raises ``ChallengeSigningError`` on any failure.
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
        # docstring); every cryptographic claim stays fully verified.
        verification_policy = policy.UnsafeNoOp()
    verifier = (
        Verifier.staging(offline=offline)
        if staging
        else Verifier.production(offline=offline)
    )
    try:
        verifier.verify_artifact(submission_bytes, bundle, verification_policy)
    except VerificationError as exc:
        raise ChallengeSigningError(f"signature verification failed: {exc}") from exc

    # ``_inner`` is sigstore-python's protobuf view of the entry the
    # verifier just checked. Private API, acceptable only because the
    # dependency is exact-pinned; test_challenge_signing guards the shape.
    inner = bundle.log_entry._inner
    if inner.inclusion_promise is None or not inner.integrated_time:
        raise ChallengeSigningError(
            "bundle carries no Signed Entry Timestamp binding its "
            "integratedTime (v0.2+ bundles may omit the inclusion promise "
            "when an RFC 3161 timestamp is present, and sigstore skips SET "
            "verification for a zero integratedTime); Rekor chronology "
            "cannot be established — re-sign with the sigstore CLI default "
            "flow, which uploads to Rekor and embeds the promise"
        )
    certificate = bundle.signing_certificate
    if certificate is None:
        raise ChallengeSigningError("bundle carries no signing certificate")
    from cryptography.hazmat.primitives.serialization import Encoding

    return VerifiedEntry(
        certificate_der=certificate.public_bytes(Encoding.DER),
        integrated_time=int(inner.integrated_time),
        log_index=int(inner.log_index),
        log_id_key_id=base64.b64encode(inner.log_id.key_id).decode(),
        entry_uuid=hashlib.sha256(b"\x00" + inner.canonicalized_body).hexdigest(),
        environment="staging" if staging else "production",
    )


@dataclass(frozen=True)
class SignatureVerification:
    submission_path: pathlib.Path
    bundle_path: pathlib.Path
    artifact_sha256: str
    metadata: BundleMetadata
    verified: VerifiedEntry
    certificate_subjects: list[str]
    certificate_oidc_issuer: str | None
    identity_enforced: bool
    integrated_time_utc: datetime
    release_instant_utc: datetime | None
    release_instant_source: str | None
    precedes_release: bool | None


def _validated_identity_requirements(
    expected_identity: str | None, expected_issuer: str | None
) -> tuple[str | None, str | None]:
    """Both-or-neither, and never blank: an empty --require-issuer would
    silently disable issuer checking inside sigstore while the output still
    claimed the identity was enforced."""

    if expected_identity is None and expected_issuer is None:
        return None, None
    if expected_identity is None or expected_issuer is None:
        raise ChallengeSigningError(
            "identity enforcement needs BOTH an expected identity and the "
            "OIDC issuer that vouched for it"
        )
    identity = expected_identity.strip()
    issuer = expected_issuer.strip()
    if not identity or not issuer:
        raise ChallengeSigningError("expected identity and issuer must be nonempty")
    return identity, issuer


def verify_submission(
    submission_path: pathlib.Path,
    bundle_path: pathlib.Path | None = None,
    *,
    release_at: datetime | None = None,
    targets_path: pathlib.Path | None = None,
    expected_identity: str | None = None,
    expected_issuer: str | None = None,
    staging: bool = False,
    offline: bool = False,
    verify_fn: Callable[..., VerifiedEntry] | None = None,
) -> SignatureVerification:
    """Fully verify one signed submission (crypto, digest, chronology)."""

    expected_identity, expected_issuer = _validated_identity_requirements(
        expected_identity, expected_issuer
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
    if not metadata.has_inclusion_promise or metadata.integrated_time <= 0:
        # Structural twin of the seam's post-verification SET requirement:
        # without a promise-bound nonzero integratedTime there is no Rekor
        # chronology to verify, so refuse before any network trust decision.
        raise ChallengeSigningError(
            "bundle carries no Signed Entry Timestamp binding its "
            "integratedTime; Rekor chronology cannot be established "
            f"({bundle_path})"
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
    verified = (verify_fn or _cryptographic_verify)(
        submission_bytes,
        bundle_text,
        staging=staging,
        offline=offline,
        expected_identity=expected_identity,
        expected_issuer=expected_issuer,
    )
    # The SET covers the entry's canonical payload (body, integratedTime,
    # logID, logIndex), so the verified object and the raw bundle JSON must
    # agree exactly; any skew means the bundle's advertised metadata is not
    # what Rekor signed.
    if (
        verified.integrated_time != metadata.integrated_time
        or verified.log_index != metadata.log_index
        or verified.log_id_key_id != metadata.log_id_key_id
        or verified.entry_uuid != metadata.entry_uuid
    ):
        raise ChallengeSigningError(
            "bundle metadata does not match its cryptographically verified "
            f"transparency-log entry ({bundle_path})"
        )
    subjects, issuer = extract_certificate_identity(verified.certificate_der)
    if not subjects:
        raise ChallengeSigningError(
            "signing certificate names no subject; a keyless certificate "
            f"must carry a subject alternative name ({bundle_path})"
        )
    integrated = datetime.fromtimestamp(verified.integrated_time, tz=timezone.utc)

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
        verified=verified,
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
        "sigstoreEnvironment": verification.verified.environment,
        "rekorLogIndex": verification.verified.log_index,
        "rekorLogIdKeyId": verification.verified.log_id_key_id,
        "rekorEntryUuid": verification.verified.entry_uuid,
        "rekorIntegratedTimeUtc": _utc_iso(verification.integrated_time_utc),
        "rekorIntegratedTimeSource": "signed_entry_timestamp",
        "precedesRelease": verification.precedes_release,
        "releaseInstantUtc": (
            _utc_iso(verification.release_instant_utc)
            if verification.release_instant_utc
            else None
        ),
        "releaseInstantSource": verification.release_instant_source,
    }
