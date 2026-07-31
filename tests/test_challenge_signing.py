"""Submitter-side keyless signing for the challenge lane (issue #52).

Layered coverage:

- Everything around the cryptographic boundary is exercised through the
  ``verify_fn`` seam fail-closed — inbox hygiene and name-shape rules,
  schema refusals, bundle metadata extraction, the SET requirement, the
  raw-vs-verified cross-check, chronology conservatism, and the
  provenance-block contract the publish adapter stores.
- The cryptographic boundary itself (``_cryptographic_verify``) is
  exercised for real against sigstore-python's own v4.5.0 staging-signed
  test assets with ``Verifier.staging(offline=True)`` — the same
  offline-verification pattern sigstore's own suite uses — covering the
  good path, wrong artifact bytes, a tampered ``integratedTime``, a
  bundle with no signed time source, and certificate-identity
  enforcement. No network or OIDC flow is required.

Fixtures: ``records-push-cd6fb721.dsse.sigstore.json`` is this
repository's own records-push attestation (real Fulcio certificate, real
tlog entry; UUID cross-checked against the live Rekor API 2026-07-31).
``bundle_v3*`` and their artifacts are vendored unmodified from
sigstore/sigstore-python v4.5.0 ``test/assets`` (Apache-2.0).
"""

from __future__ import annotations

import base64
import hashlib
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

import challenge_signing as cs  # noqa: E402
import sign_challenge_submission as sign_cli  # noqa: E402
import verify_challenge_signatures as verify_cli  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures" / "challenge_signing"
REAL_BUNDLE = FIXTURES / "records-push-cd6fb721.dsse.sigstore.json"
SIGSTORE_ARTIFACT = FIXTURES / "bundle_v3.txt"
SIGSTORE_BUNDLE = FIXTURES / "bundle_v3.txt.sigstore"
SIGSTORE_NO_SIGNED_TIME_ARTIFACT = FIXTURES / "bundle_v3_no_signed_time.txt"
SIGSTORE_NO_SIGNED_TIME_BUNDLE = FIXTURES / "bundle_v3_no_signed_time.txt.sigstore.json"

# Pinned from the live Rekor API (logIndex 2291698296), 2026-07-31.
REAL_BUNDLE_UUID = "55ca7d40971d6b07a0b4be3df530d25134e27c70904610549e80106572ae677f"
REAL_BUNDLE_LOG_INDEX = 2291698296
REAL_BUNDLE_INTEGRATED_TIME = 1785427794

# Observed via Verifier.staging(offline=True) against the vendored asset;
# the staging log's top-level (global) index legitimately differs from the
# shard-local inclusionProof.logIndex (25901137).
SIGSTORE_BUNDLE_INTEGRATED_TIME = 1712085549
SIGSTORE_BUNDLE_LOG_INDEX = 25915956

JOLTS_ID = "bls.jolts.hires_rate.2026_06.first_print"

UTC = timezone.utc


def real_bundle_json() -> dict:
    return json.loads(REAL_BUNDLE.read_text())


def real_certificate_der() -> bytes:
    bundle = real_bundle_json()
    return base64.b64decode(bundle["verificationMaterial"]["certificate"]["rawBytes"])


def write_submission(
    path: pathlib.Path,
    *,
    data_point_id: str = JOLTS_ID,
    challenger: str = "github:tester",
) -> pathlib.Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "schemaVersion": cs.SUBMISSION_SCHEMA,
                "challenger": challenger,
                "systemType": "ai",
                "systemName": "test system",
                "dataPointId": data_point_id,
                "pointEstimate": 3.3,
                "ciLow": 3.1,
                "ciHigh": 3.45,
                "generatedAtUtc": "2026-07-31T14:00:00Z",
            }
        )
    )
    return path


SYNTHETIC_BODY = b'{"synthetic": "tlog body"}'


def synthetic_bundle(
    *,
    digest_hex: str,
    integrated_time: int | str = 1785000000,
    log_index: int | str = 123456,
    kind: str = "hashedrekord",
    body: bytes = SYNTHETIC_BODY,
    include_promise: bool = True,
) -> dict:
    entry = {
        "logIndex": log_index,
        "logId": {"keyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0="},
        "kindVersion": {"kind": kind, "version": "0.0.1"},
        "integratedTime": integrated_time,
        "inclusionProof": {"logIndex": "1", "checkpoint": {"envelope": "x"}},
        "canonicalizedBody": base64.b64encode(body).decode(),
    }
    if include_promise:
        entry["inclusionPromise"] = {"signedEntryTimestamp": "AAAA"}
    return {
        "mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
        "verificationMaterial": {
            "certificate": {"rawBytes": base64.b64encode(b"unused").decode()},
            "tlogEntries": [entry],
        },
        "messageSignature": {
            "messageDigest": {
                "algorithm": "SHA2_256",
                "digest": base64.b64encode(bytes.fromhex(digest_hex)).decode(),
            },
            "signature": base64.b64encode(b"unused").decode(),
        },
    }


def make_signed_inbox(
    tmp_path: pathlib.Path,
    *,
    integrated_time: int | str = 1785000000,
) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    inbox = tmp_path / "challenge" / "inbox"
    submission = write_submission(inbox / "tester" / "cell.json")
    digest = hashlib.sha256(submission.read_bytes()).hexdigest()
    bundle = cs.bundle_path_for(submission)
    bundle.write_text(
        json.dumps(synthetic_bundle(digest_hex=digest, integrated_time=integrated_time))
    )
    return inbox, submission, bundle


def stub_verify(**overrides):
    """An honest stand-in for the crypto seam: it returns exactly what a
    real verifier would read back from the synthetic bundle's entry, so the
    raw-vs-verified cross-check passes unless a test skews it."""

    der = real_certificate_der()

    def _stub(
        submission_bytes,
        bundle_text,
        *,
        staging,
        offline=False,
        expected_identity,
        expected_issuer,
    ):
        entry = json.loads(bundle_text)["verificationMaterial"]["tlogEntries"][0]
        values = dict(
            certificate_der=der,
            integrated_time=int(entry["integratedTime"]),
            log_index=int(entry["logIndex"]),
            log_id_key_id=entry["logId"]["keyId"],
            entry_uuid=cs.rekor_entry_uuid(entry["canonicalizedBody"]),
            environment="staging" if staging else "production",
        )
        values.update(overrides)
        return cs.VerifiedEntry(**values)

    return _stub


# --- Rekor entry UUID derivation -------------------------------------------


def test_rekor_uuid_is_the_rfc6962_leaf_hash_of_the_canonicalized_body() -> None:
    entry = real_bundle_json()["verificationMaterial"]["tlogEntries"][0]
    body = base64.b64decode(entry["canonicalizedBody"])
    assert (
        hashlib.sha256(b"\x00" + body).hexdigest()
        == cs.rekor_entry_uuid(entry["canonicalizedBody"])
        == REAL_BUNDLE_UUID
    )


def test_rekor_uuid_refuses_invalid_base64() -> None:
    with pytest.raises(cs.ChallengeSigningError, match="base64"):
        cs.rekor_entry_uuid("not*base64")


# --- Bundle metadata extraction --------------------------------------------


def test_real_bundle_metadata_extracts_the_transparency_log_entry() -> None:
    metadata = cs.parse_bundle_metadata(real_bundle_json())
    assert metadata.log_index == REAL_BUNDLE_LOG_INDEX
    assert metadata.integrated_time == REAL_BUNDLE_INTEGRATED_TIME
    assert metadata.entry_uuid == REAL_BUNDLE_UUID
    assert metadata.entry_kind == "dsse"
    assert metadata.has_inclusion_promise is True
    assert metadata.message_digest_sha256 is None
    assert metadata.media_type.startswith(cs.BUNDLE_MEDIA_TYPE_PREFIX)


def test_synthetic_bundle_metadata_accepts_string_and_int_integers() -> None:
    digest = "ab" * 32
    for value in (123456, "123456"):
        metadata = cs.parse_bundle_metadata(
            synthetic_bundle(digest_hex=digest, log_index=value)
        )
        assert metadata.log_index == 123456
        assert metadata.message_digest_sha256 == digest
        assert metadata.has_inclusion_promise is True


def test_promise_absence_is_reported_not_hidden() -> None:
    metadata = cs.parse_bundle_metadata(
        synthetic_bundle(digest_hex="ab" * 32, include_promise=False)
    )
    assert metadata.has_inclusion_promise is False


@pytest.mark.parametrize(
    "mutate, message",
    [
        (lambda b: b.update(mediaType="application/json"), "not a Sigstore bundle"),
        (lambda b: b.pop("verificationMaterial"), "verificationMaterial"),
        (
            lambda b: b["verificationMaterial"].update(tlogEntries=[]),
            "no transparency-log entry",
        ),
        (
            lambda b: b["verificationMaterial"].update(
                tlogEntries=b["verificationMaterial"]["tlogEntries"] * 2
            ),
            "exactly one transparency-log entry",
        ),
        (
            lambda b: b["verificationMaterial"]["tlogEntries"][0].pop("logId"),
            "logId.keyId",
        ),
        (
            lambda b: b["verificationMaterial"]["tlogEntries"][0].pop(
                "canonicalizedBody"
            ),
            "canonicalizedBody",
        ),
        (
            lambda b: b["verificationMaterial"]["tlogEntries"][0].update(logIndex=True),
            "must be an integer",
        ),
        (
            lambda b: b["messageSignature"]["messageDigest"].update(
                algorithm="SHA2_512"
            ),
            "SHA2_256",
        ),
    ],
)
def test_bundle_metadata_fails_closed_on_malformed_bundles(mutate, message) -> None:
    bundle = synthetic_bundle(digest_hex="ab" * 32)
    mutate(bundle)
    with pytest.raises(cs.ChallengeSigningError, match=message):
        cs.parse_bundle_metadata(bundle)


# --- Chronology -------------------------------------------------------------


def test_date_only_instants_floor_to_utc_midnight() -> None:
    assert cs.parse_utc_instant("2026-08-04", label="x") == datetime(
        2026, 8, 4, tzinfo=UTC
    )


def test_explicit_instants_normalize_to_utc() -> None:
    assert cs.parse_utc_instant("2026-08-04T10:30:00Z", label="x") == datetime(
        2026, 8, 4, 10, 30, tzinfo=UTC
    )
    assert cs.parse_utc_instant("2026-08-04T10:30:00+02:00", label="x") == datetime(
        2026, 8, 4, 8, 30, tzinfo=UTC
    )


@pytest.mark.parametrize("value", ["2026-08-04T10:30:00", "garbage", "2026-13-01"])
def test_underspecified_instants_are_refused(value: str) -> None:
    with pytest.raises(cs.ChallengeSigningError):
        cs.parse_utc_instant(value, label="x")


def test_release_instant_for_the_live_jolts_registration() -> None:
    release = cs.release_instant_for(JOLTS_ID)
    assert release.instant == datetime(2026, 8, 4, tzinfo=UTC)
    assert release.source == "registry_day_floor"


def test_release_instant_takes_the_earlier_of_window_start_and_resolution(
    tmp_path: pathlib.Path,
) -> None:
    targets = tmp_path / "targets.ts"
    targets.write_text(
        "\n".join(
            [
                "  {",
                '    kind: "target_registered",',
                '    dataPointId: "test.series.2026_06.first_print",',
                '    resolutionDate: "2026-08-04",',
                '    sourceBinding: {"adapter": "x", "expectedReleaseWindow":'
                ' {"end": "2026-08-05", "start": "2026-08-02"}},',
                "  },",
                "  {",
                '    kind: "target_registered",',
                '    dataPointId: "other.series.2026_06.first_print",',
                '    resolutionDate: "2026-01-01",',
                "  },",
            ]
        )
    )
    release = cs.release_instant_for(
        "test.series.2026_06.first_print", targets_path=targets
    )
    assert release.instant == datetime(2026, 8, 2, tzinfo=UTC)


def test_release_instant_refuses_unregistered_targets(tmp_path) -> None:
    targets = tmp_path / "targets.ts"
    targets.write_text('    dataPointId: "some.other.id",\n')
    with pytest.raises(cs.ChallengeSigningError, match="not in the generated"):
        cs.release_instant_for("test.missing.id", targets_path=targets)


# --- Inbox hygiene -----------------------------------------------------------


def test_audit_pairs_submissions_with_their_bundles(tmp_path) -> None:
    inbox, submission, bundle = make_signed_inbox(tmp_path)
    unsigned = write_submission(inbox / "other" / "plain.json")
    audit = cs.audit_inbox(inbox)
    assert audit.submissions == [unsigned, submission]
    assert audit.bundles == {submission: bundle}
    assert audit.orphan_bundles == []
    assert audit.unexpected == []


def test_audit_surfaces_orphan_bundles_and_unexpected_files(tmp_path) -> None:
    inbox = tmp_path / "inbox"
    (inbox / "tester").mkdir(parents=True)
    (inbox / "tester" / "gone.json.sigstore.json").write_text("{}")
    (inbox / "tester" / "notes.txt").write_text("hi")
    (inbox / "README.md").write_text("root readme is fine")
    audit = cs.audit_inbox(inbox)
    assert audit.submissions == []
    assert [str(p) for p in audit.orphan_bundles] == ["tester/gone.json.sigstore.json"]
    assert [str(p) for p in audit.unexpected] == ["tester/notes.txt"]


@pytest.mark.parametrize(
    "relative",
    [
        "toplevel.json",  # missing the <login>/ directory level
        "tester/nested/cell.json",  # too deep
        "bad_login/cell.json",  # underscore not allowed in a GitHub login
        "tester/.hidden.json",  # cell names must start alphanumeric
        "tester/README.md",  # README is root-only
    ],
)
def test_audit_rejects_nonconforming_shapes(tmp_path, relative: str) -> None:
    inbox = tmp_path / "inbox"
    path = inbox / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}")
    audit = cs.audit_inbox(inbox)
    assert audit.submissions == []
    assert [str(p) for p in audit.unexpected] == [relative]


def test_audit_rejects_control_characters_in_names(tmp_path) -> None:
    inbox = tmp_path / "inbox"
    (inbox / "tester").mkdir(parents=True)
    evil = inbox / "tester" / "evil\nsigned line.json"
    evil.write_text("{}")
    audit = cs.audit_inbox(inbox)
    assert audit.submissions == []
    assert len(audit.unexpected) == 1


def test_audit_refuses_symlinked_submissions(tmp_path) -> None:
    inbox = tmp_path / "inbox"
    real = write_submission(inbox / "tester" / "real.json")
    (inbox / "tester" / "link.json").symlink_to(real)
    audit = cs.audit_inbox(inbox)
    assert real in audit.submissions
    assert [str(p) for p in audit.unexpected] == ["tester/link.json"]


def test_audit_refuses_a_symlinked_inbox_root(tmp_path) -> None:
    real = tmp_path / "real-inbox"
    real.mkdir()
    link = tmp_path / "inbox-link"
    link.symlink_to(real, target_is_directory=True)
    with pytest.raises(cs.ChallengeSigningError, match="symlink"):
        cs.audit_inbox(link)


def test_audit_refuses_a_missing_inbox(tmp_path) -> None:
    with pytest.raises(cs.ChallengeSigningError, match="missing"):
        cs.audit_inbox(tmp_path / "nope")


def test_the_live_inbox_is_hygienic_and_every_submission_parses() -> None:
    audit = cs.audit_inbox(cs.inbox_root())
    assert audit.orphan_bundles == []
    assert audit.unexpected == []
    assert audit.submissions, "the grandfathered PR #49 submission should exist"
    for submission in audit.submissions:
        cs.load_submission(submission)


# --- Submission schema -------------------------------------------------------


@pytest.mark.parametrize(
    "mutate, message",
    [
        (lambda s: s.update(schemaVersion="v2"), "unsupported"),
        (lambda s: s.update(challenger="pavel"), "github:<login>"),
        (lambda s: s.pop("dataPointId"), "dataPointId"),
    ],
)
def test_submission_schema_fails_closed(tmp_path, mutate, message) -> None:
    path = write_submission(tmp_path / "cell.json")
    payload = json.loads(path.read_text())
    mutate(payload)
    path.write_text(json.dumps(payload))
    with pytest.raises(cs.ChallengeSigningError, match=message):
        cs.load_submission(path)


# --- Certificate identity ----------------------------------------------------


def test_real_fulcio_certificate_identity_extraction() -> None:
    subjects, issuer = cs.extract_certificate_identity(real_certificate_der())
    assert subjects == [
        "https://github.com/ThesisInstitute/thesis/.github/workflows/"
        "record-forecasts.yml@refs/heads/main"
    ]
    assert issuer == "https://token.actions.githubusercontent.com"


# --- verify_submission (seam-stubbed) ---------------------------------------


def test_verify_submission_happy_path_builds_the_provenance_contract(
    tmp_path,
) -> None:
    inbox, submission, bundle = make_signed_inbox(tmp_path)
    verification = cs.verify_submission(
        submission,
        bundle,
        release_at=datetime(2026, 8, 4, tzinfo=UTC),
        verify_fn=stub_verify(),
    )
    assert verification.precedes_release is True  # 2026-07-25 < 2026-08-04
    assert verification.metadata.entry_kind == "hashedrekord"
    block = cs.signature_provenance_block(verification, repo_root=tmp_path)
    assert block == {
        "schemaVersion": "thesis_challenge_signature_v1",
        "scheme": "sigstore_keyless",
        "artifactPath": "challenge/inbox/tester/cell.json",
        "artifactSha256": hashlib.sha256(submission.read_bytes()).hexdigest(),
        "bundlePath": "challenge/inbox/tester/cell.json.sigstore.json",
        "bundleMediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
        "certificateSubjects": [
            "https://github.com/ThesisInstitute/thesis/.github/workflows/"
            "record-forecasts.yml@refs/heads/main"
        ],
        "certificateOidcIssuer": "https://token.actions.githubusercontent.com",
        "identityPolicy": "recorded_not_enforced",
        "sigstoreEnvironment": "production",
        "rekorLogIndex": 123456,
        "rekorLogIdKeyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0=",
        "rekorEntryUuid": cs.rekor_entry_uuid(
            base64.b64encode(SYNTHETIC_BODY).decode()
        ),
        "rekorIntegratedTimeUtc": "2026-07-25T17:20:00Z",
        "rekorIntegratedTimeSource": "signed_entry_timestamp",
        "precedesRelease": True,
        "releaseInstantUtc": "2026-08-04T00:00:00Z",
        "releaseInstantSource": "explicit",
    }


def test_verify_submission_resolves_the_release_from_the_live_registry(
    tmp_path,
) -> None:
    _, submission, bundle = make_signed_inbox(tmp_path)
    verification = cs.verify_submission(submission, bundle, verify_fn=stub_verify())
    assert verification.release_instant_utc == datetime(2026, 8, 4, tzinfo=UTC)
    assert verification.release_instant_source == "registry_day_floor"
    assert verification.precedes_release is True


@pytest.mark.parametrize(
    "integrated, expected",
    [
        (1785000000, True),  # 2026-07-25T17:20:00Z < floor
        (1785801600, False),  # exactly 2026-08-04T00:00:00Z — not strictly before
        (1785801601, False),
    ],
)
def test_prerelease_requires_strictly_before_the_instant(
    tmp_path, integrated: int, expected: bool
) -> None:
    _, submission, bundle = make_signed_inbox(tmp_path, integrated_time=integrated)
    verification = cs.verify_submission(
        submission,
        bundle,
        release_at=datetime(2026, 8, 4, tzinfo=UTC),
        verify_fn=stub_verify(),
    )
    assert verification.precedes_release is expected


def test_verify_submission_refuses_a_bundle_for_different_bytes(tmp_path) -> None:
    _, submission, bundle = make_signed_inbox(tmp_path)
    submission.write_text(submission.read_text() + "\n")
    with pytest.raises(cs.ChallengeSigningError, match="different artifact"):
        cs.verify_submission(
            submission,
            bundle,
            release_at=datetime(2026, 8, 4, tzinfo=UTC),
            verify_fn=stub_verify(),
        )


def test_verify_submission_refuses_non_blob_signatures(tmp_path) -> None:
    inbox = tmp_path / "inbox"
    submission = write_submission(inbox / "tester" / "cell.json")
    bundle = cs.bundle_path_for(submission)
    bundle.write_text(REAL_BUNDLE.read_text())  # dsse-kind attestation bundle
    with pytest.raises(cs.ChallengeSigningError, match="hashedrekord"):
        cs.verify_submission(
            submission,
            bundle,
            release_at=datetime(2026, 8, 4, tzinfo=UTC),
            verify_fn=stub_verify(),
        )


def test_verify_submission_refuses_a_bundle_without_a_signed_entry_timestamp(
    tmp_path,
) -> None:
    """The B1 regression: an unauthenticated integratedTime must never
    reach the chronology comparison."""

    inbox = tmp_path / "inbox"
    submission = write_submission(inbox / "tester" / "cell.json")
    digest = hashlib.sha256(submission.read_bytes()).hexdigest()
    bundle = cs.bundle_path_for(submission)
    bundle.write_text(
        json.dumps(synthetic_bundle(digest_hex=digest, include_promise=False))
    )

    def must_not_run(*args, **kwargs):
        raise AssertionError("crypto seam must not be reached without a SET")

    with pytest.raises(cs.ChallengeSigningError, match="Signed Entry Timestamp"):
        cs.verify_submission(
            submission,
            bundle,
            release_at=datetime(2026, 8, 4, tzinfo=UTC),
            verify_fn=must_not_run,
        )


def test_verify_submission_refuses_a_zero_integrated_time(tmp_path) -> None:
    """sigstore skips SET verification when integratedTime is zero, so a
    zero must be refused structurally, promise or not."""

    inbox = tmp_path / "inbox"
    submission = write_submission(inbox / "tester" / "cell.json")
    digest = hashlib.sha256(submission.read_bytes()).hexdigest()
    bundle = cs.bundle_path_for(submission)
    bundle.write_text(
        json.dumps(synthetic_bundle(digest_hex=digest, integrated_time=0))
    )
    with pytest.raises(cs.ChallengeSigningError, match="Signed Entry Timestamp"):
        cs.verify_submission(
            submission,
            bundle,
            release_at=datetime(2026, 8, 4, tzinfo=UTC),
            verify_fn=stub_verify(),
        )


@pytest.mark.parametrize(
    "skew",
    [
        {"integrated_time": 1},
        {"log_index": 999999},
        {"log_id_key_id": "AAAA"},
        {"entry_uuid": "ff" * 32},
    ],
)
def test_verify_submission_refuses_raw_metadata_that_skews_from_verified(
    tmp_path, skew: dict
) -> None:
    """The verified entry is authoritative; advertised bundle JSON that
    disagrees with it is refused rather than recorded."""

    _, submission, bundle = make_signed_inbox(tmp_path)
    with pytest.raises(cs.ChallengeSigningError, match="does not match"):
        cs.verify_submission(
            submission,
            bundle,
            release_at=datetime(2026, 8, 4, tzinfo=UTC),
            verify_fn=stub_verify(**skew),
        )


def test_verify_submission_refuses_a_certificate_with_no_subject(tmp_path) -> None:
    cryptography = pytest.importorskip("cryptography")
    from datetime import timedelta

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.serialization import Encoding
    from cryptography.x509.oid import NameOID

    assert cryptography is not None
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "no-san")])
    now = datetime(2026, 1, 1, tzinfo=UTC)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=1))
        .sign(key, hashes.SHA256())
    )
    _, submission, bundle = make_signed_inbox(tmp_path)
    with pytest.raises(cs.ChallengeSigningError, match="names no subject"):
        cs.verify_submission(
            submission,
            bundle,
            release_at=datetime(2026, 8, 4, tzinfo=UTC),
            verify_fn=stub_verify(certificate_der=cert.public_bytes(Encoding.DER)),
        )


def test_verify_submission_propagates_crypto_failures(tmp_path) -> None:
    _, submission, bundle = make_signed_inbox(tmp_path)

    def failing(*args, **kwargs):
        raise cs.ChallengeSigningError("signature verification failed: bad SET")

    with pytest.raises(cs.ChallengeSigningError, match="bad SET"):
        cs.verify_submission(
            submission,
            bundle,
            release_at=datetime(2026, 8, 4, tzinfo=UTC),
            verify_fn=failing,
        )


@pytest.mark.parametrize(
    "identity, issuer",
    [
        ("someone@example.com", None),
        (None, "https://github.com/login/oauth"),
        ("someone@example.com", "   "),
        ("", "https://github.com/login/oauth"),
    ],
)
def test_verify_submission_requires_a_complete_identity_requirement(
    tmp_path, identity, issuer
) -> None:
    _, submission, bundle = make_signed_inbox(tmp_path)
    with pytest.raises(cs.ChallengeSigningError, match="identity|issuer|nonempty"):
        cs.verify_submission(
            submission,
            bundle,
            release_at=datetime(2026, 8, 4, tzinfo=UTC),
            expected_identity=identity,
            expected_issuer=issuer,
            verify_fn=stub_verify(),
        )


def test_verify_submission_refuses_a_naive_release_instant(tmp_path) -> None:
    _, submission, bundle = make_signed_inbox(tmp_path)
    with pytest.raises(cs.ChallengeSigningError, match="timezone-aware"):
        cs.verify_submission(
            submission,
            bundle,
            release_at=datetime(2026, 8, 4),  # noqa: DTZ001 - the refusal under test
            verify_fn=stub_verify(),
        )


# --- The cryptographic boundary, for real (offline staging assets) ----------


def _real_verify(artifact: bytes, bundle_text: str, **kwargs):
    pytest.importorskip("sigstore")
    defaults = dict(
        staging=True,
        offline=True,
        expected_identity=None,
        expected_issuer=None,
    )
    defaults.update(kwargs)
    return cs._cryptographic_verify(artifact, bundle_text, **defaults)


def test_e2e_real_bundle_verifies_and_yields_the_set_bound_entry() -> None:
    verified = _real_verify(SIGSTORE_ARTIFACT.read_bytes(), SIGSTORE_BUNDLE.read_text())
    assert verified.integrated_time == SIGSTORE_BUNDLE_INTEGRATED_TIME
    assert verified.log_index == SIGSTORE_BUNDLE_LOG_INDEX
    assert verified.environment == "staging"
    raw = cs.parse_bundle_metadata(json.loads(SIGSTORE_BUNDLE.read_text()))
    assert verified.integrated_time == raw.integrated_time
    assert verified.log_index == raw.log_index
    assert verified.log_id_key_id == raw.log_id_key_id
    assert verified.entry_uuid == raw.entry_uuid
    subjects, issuer = cs.extract_certificate_identity(verified.certificate_der)
    assert subjects and issuer


def test_e2e_real_bundle_refuses_different_artifact_bytes() -> None:
    with pytest.raises(cs.ChallengeSigningError, match="verification failed"):
        _real_verify(SIGSTORE_ARTIFACT.read_bytes() + b"x", SIGSTORE_BUNDLE.read_text())


@pytest.mark.parametrize(
    "tampered_time",
    [
        # +1s stays inside the certificate's validity window, so the refusal
        # can only come from the SET signature check — the sharp regression.
        str(SIGSTORE_BUNDLE_INTEGRATED_TIME + 1),
        "1",  # far outside the window; certificate-time validation also trips
    ],
)
def test_e2e_real_bundle_refuses_a_tampered_integrated_time(
    tampered_time: str,
) -> None:
    tampered = json.loads(SIGSTORE_BUNDLE.read_text())
    tampered["verificationMaterial"]["tlogEntries"][0]["integratedTime"] = tampered_time
    with pytest.raises(cs.ChallengeSigningError):
        _real_verify(SIGSTORE_ARTIFACT.read_bytes(), json.dumps(tampered))


def test_e2e_a_bundle_with_no_signed_time_source_is_refused() -> None:
    """sigstore's own asset with neither a SET nor an RFC 3161 timestamp:
    it must be refused, never verified with an unauthenticated time."""

    with pytest.raises(cs.ChallengeSigningError):
        _real_verify(
            SIGSTORE_NO_SIGNED_TIME_ARTIFACT.read_bytes(),
            SIGSTORE_NO_SIGNED_TIME_BUNDLE.read_text(),
        )


def test_e2e_identity_policy_enforces_for_real() -> None:
    verified = _real_verify(SIGSTORE_ARTIFACT.read_bytes(), SIGSTORE_BUNDLE.read_text())
    subjects, issuer = cs.extract_certificate_identity(verified.certificate_der)
    # The certificate's own identity passes enforcement...
    _real_verify(
        SIGSTORE_ARTIFACT.read_bytes(),
        SIGSTORE_BUNDLE.read_text(),
        expected_identity=subjects[0],
        expected_issuer=issuer,
    )
    # ...and a different identity is refused by the same policy machinery.
    with pytest.raises(cs.ChallengeSigningError, match="verification failed"):
        _real_verify(
            SIGSTORE_ARTIFACT.read_bytes(),
            SIGSTORE_BUNDLE.read_text(),
            expected_identity="attacker@example.com",
            expected_issuer=issuer,
        )


def test_pinned_sigstore_private_view_still_has_the_fields_we_read() -> None:
    """``_cryptographic_verify`` reads ``bundle.log_entry._inner`` (private
    API, acceptable only under the exact ``sigstore==4.5.0`` pin). This
    canary fails loudly on any pin bump that changes the shape."""

    sigstore = pytest.importorskip("sigstore")
    from sigstore.models import Bundle

    assert sigstore.__version__ == "4.5.0"
    bundle = Bundle.from_json(SIGSTORE_BUNDLE.read_text())
    inner = bundle.log_entry._inner
    assert inner.integrated_time and inner.log_index
    assert inner.log_id.key_id and inner.canonicalized_body
    assert inner.inclusion_promise is not None


# --- Sign helper -------------------------------------------------------------


def test_sign_helper_refuses_paths_outside_the_inbox(tmp_path) -> None:
    outside = write_submission(tmp_path / "cell.json")
    with pytest.raises(cs.ChallengeSigningError, match="refusing to sign"):
        sign_cli.sign(outside, staging=False)


def test_sign_helper_refuses_to_overwrite_an_existing_bundle(
    tmp_path, monkeypatch
) -> None:
    inbox = tmp_path / "challenge" / "inbox"
    submission = write_submission(inbox / "tester" / "cell.json")
    cs.bundle_path_for(submission).write_text("{}")
    monkeypatch.setattr(cs, "REPO_ROOT", tmp_path)

    def must_not_run(*args, **kwargs):  # the refusal must precede any signing
        raise AssertionError("sigstore CLI must not be invoked")

    monkeypatch.setattr(sign_cli.subprocess, "run", must_not_run)
    with pytest.raises(cs.ChallengeSigningError, match="refusing to overwrite"):
        sign_cli.sign(submission, staging=False)


def test_sign_helper_invokes_the_sigstore_cli_and_reports(
    tmp_path, monkeypatch, capsys
) -> None:
    inbox = tmp_path / "challenge" / "inbox"
    submission = write_submission(inbox / "tester" / "cell.json")
    monkeypatch.setattr(cs, "REPO_ROOT", tmp_path)
    digest = hashlib.sha256(submission.read_bytes()).hexdigest()
    recorded: dict = {}

    def fake_run(command, check):
        recorded["command"] = command
        cs.bundle_path_for(submission).write_text(
            json.dumps(synthetic_bundle(digest_hex=digest))
        )
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(sign_cli.subprocess, "run", fake_run)
    assert sign_cli.main([str(submission)]) == 0
    assert recorded["command"] == [
        sys.executable,
        "-m",
        "sigstore",
        "sign",
        "--bundle",
        str(cs.bundle_path_for(submission)),
        str(submission),
    ]
    out = capsys.readouterr().out
    assert "logIndex=123456" in out
    assert "Commit BOTH files" in out


def test_sign_helper_fails_when_the_cli_fails(tmp_path, monkeypatch) -> None:
    inbox = tmp_path / "challenge" / "inbox"
    submission = write_submission(inbox / "tester" / "cell.json")
    monkeypatch.setattr(cs, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        sign_cli.subprocess,
        "run",
        lambda command, check: subprocess.CompletedProcess(command, 1),
    )
    assert sign_cli.main([str(submission)]) == 1


# --- Verifier CLI ------------------------------------------------------------


def test_cli_passes_an_unsigned_inbox_and_flags_require_signature(
    tmp_path, capsys
) -> None:
    inbox = tmp_path / "inbox"
    write_submission(inbox / "tester" / "cell.json")
    assert verify_cli.main(["--inbox", str(inbox)]) == 0
    assert "signature optional" in capsys.readouterr().out
    assert verify_cli.main(["--inbox", str(inbox), "--require-signature"]) == 1


def test_cli_json_mode_emits_exactly_one_json_document_on_stdout(
    tmp_path, monkeypatch, capsys
) -> None:
    inbox, submission, bundle = make_signed_inbox(tmp_path)
    write_submission(inbox / "other" / "plain.json")  # unsigned alongside
    monkeypatch.setattr(cs, "_cryptographic_verify", stub_verify())
    code = verify_cli.main(
        ["--inbox", str(inbox), "--release-at", "2026-08-04", "--json"]
    )
    captured = capsys.readouterr()
    assert code == 0
    blocks = json.loads(captured.out)  # the WHOLE stdout is the document
    assert len(blocks) == 1
    assert blocks[0]["schemaVersion"] == "thesis_challenge_signature_v1"
    assert blocks[0]["precedesRelease"] is True
    assert blocks[0]["sigstoreEnvironment"] == "production"
    assert "signed" in captured.err and "checked" in captured.err


def test_cli_scoped_export_still_verifies_the_whole_inbox(
    tmp_path, monkeypatch, capsys
) -> None:
    inbox, submission, bundle = make_signed_inbox(tmp_path)
    corrupt_owner = write_submission(inbox / "other" / "broken.json")
    cs.bundle_path_for(corrupt_owner).write_text("not json")
    monkeypatch.setattr(cs, "_cryptographic_verify", stub_verify())
    code = verify_cli.main(
        [
            "--inbox",
            str(inbox),
            "--release-at",
            "2026-08-04",
            "--submission",
            str(submission),
        ]
    )
    assert code == 1, "an unselected corrupt sidecar must still fail the sweep"
    assert "not readable JSON" in capsys.readouterr().err


def test_cli_fails_on_orphan_bundles(tmp_path, capsys) -> None:
    inbox = tmp_path / "inbox"
    (inbox / "tester").mkdir(parents=True)
    (inbox / "tester" / "gone.json.sigstore.json").write_text("{}")
    assert verify_cli.main(["--inbox", str(inbox)]) == 1
    assert "orphan bundle" in capsys.readouterr().err


def test_cli_fails_when_a_signed_submission_is_not_prerelease(
    tmp_path, monkeypatch
) -> None:
    inbox, *_ = make_signed_inbox(tmp_path, integrated_time=1785801601)
    monkeypatch.setattr(cs, "_cryptographic_verify", stub_verify())
    assert (
        verify_cli.main(["--inbox", str(inbox), "--release-at", "2026-08-04"]) == 0
    ), "chronology outcome alone is a recorded fact, not a failure"
    assert (
        verify_cli.main(
            [
                "--inbox",
                str(inbox),
                "--release-at",
                "2026-08-04",
                "--require-prerelease",
            ]
        )
        == 1
    )


def test_cli_fails_on_a_corrupt_bundle(tmp_path, capsys) -> None:
    inbox = tmp_path / "inbox"
    submission = write_submission(inbox / "tester" / "cell.json")
    cs.bundle_path_for(submission).write_text("not json")
    assert verify_cli.main(["--inbox", str(inbox)]) == 1
    assert "not readable JSON" in capsys.readouterr().err


def test_cli_refuses_staging_json_export(tmp_path, capsys) -> None:
    inbox = tmp_path / "inbox"
    write_submission(inbox / "tester" / "cell.json")
    assert verify_cli.main(["--inbox", str(inbox), "--staging", "--json"]) == 2
    assert "rehearsal" in capsys.readouterr().err


def test_cli_refuses_an_incomplete_identity_pair_even_on_unsigned_inboxes(
    tmp_path, capsys
) -> None:
    """A misconfigured enforcement flag must fail at startup, not silently
    pass because every discovered submission happened to be unsigned."""

    inbox = tmp_path / "inbox"
    write_submission(inbox / "tester" / "cell.json")
    assert (
        verify_cli.main(
            ["--inbox", str(inbox), "--require-identity", "someone@example.com"]
        )
        == 2
    )
    assert "issuer" in capsys.readouterr().err


def test_cli_rejects_a_malformed_release_at(tmp_path) -> None:
    inbox = tmp_path / "inbox"
    write_submission(inbox / "tester" / "cell.json")
    assert verify_cli.main(["--inbox", str(inbox), "--release-at", "yesterday"]) == 2
