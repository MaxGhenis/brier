"""Submitter-side keyless signing for the challenge lane (issue #52).

Cryptographic verification is delegated to sigstore-python and exercised
through a seam (``verify_fn`` / ``_cryptographic_verify``): these tests
stub the crypto boundary and cover everything around it fail-closed —
inbox hygiene, schema refusals, bundle metadata extraction, the Rekor
entry-UUID derivation, chronology conservatism, and the provenance block
contract the publish adapter stores. The fixture bundle is real: this
repository's own records-push attestation for commit cd6fb721 (fetched
from the GitHub attestation store 2026-07-31), whose entry UUID was
cross-checked against the live Rekor API the same day.
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

# Pinned from the live Rekor API (logIndex 2291698296), 2026-07-31.
REAL_BUNDLE_UUID = "55ca7d40971d6b07a0b4be3df530d25134e27c70904610549e80106572ae677f"
REAL_BUNDLE_LOG_INDEX = 2291698296
REAL_BUNDLE_INTEGRATED_TIME = 1785427794

JOLTS_ID = "bls.jolts.hires_rate.2026_06.first_print"


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


def synthetic_bundle(
    *,
    digest_hex: str,
    integrated_time: int | str = 1785000000,
    log_index: int | str = 123456,
    kind: str = "hashedrekord",
    body: bytes = b'{"synthetic": "tlog body"}',
) -> dict:
    return {
        "mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
        "verificationMaterial": {
            "certificate": {"rawBytes": base64.b64encode(b"unused").decode()},
            "tlogEntries": [
                {
                    "logIndex": log_index,
                    "logId": {"keyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0="},
                    "kindVersion": {"kind": kind, "version": "0.0.1"},
                    "integratedTime": integrated_time,
                    "inclusionPromise": {"signedEntryTimestamp": "AAAA"},
                    "canonicalizedBody": base64.b64encode(body).decode(),
                }
            ],
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


def stub_verify(**_overrides):
    der = real_certificate_der()

    def _stub(
        submission_bytes, bundle_text, *, staging, expected_identity, expected_issuer
    ):
        return der

    return _stub


UTC = timezone.utc


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
    assert metadata.tlog_entry_count == 1
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
    (inbox / "README.md").write_text("readme is fine")
    audit = cs.audit_inbox(inbox)
    assert audit.submissions == []
    assert [str(p) for p in audit.orphan_bundles] == ["tester/gone.json.sigstore.json"]
    assert [str(p) for p in audit.unexpected] == ["tester/notes.txt"]


def test_audit_refuses_symlinked_submissions(tmp_path) -> None:
    inbox = tmp_path / "inbox"
    real = write_submission(inbox / "tester" / "real.json")
    (inbox / "tester" / "link.json").symlink_to(real)
    audit = cs.audit_inbox(inbox)
    assert real in audit.submissions
    assert [str(p) for p in audit.unexpected] == ["tester/link.json"]


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


# --- verify_submission -------------------------------------------------------


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
        "rekorLogIndex": 123456,
        "rekorLogIdKeyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0=",
        "rekorEntryUuid": cs.rekor_entry_uuid(
            base64.b64encode(b'{"synthetic": "tlog body"}').decode()
        ),
        "rekorIntegratedTimeUtc": "2026-07-25T17:20:00Z",
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


def test_verify_submission_requires_an_issuer_with_an_identity(tmp_path) -> None:
    _, submission, bundle = make_signed_inbox(tmp_path)
    with pytest.raises(cs.ChallengeSigningError, match="issuer"):
        cs.verify_submission(
            submission,
            bundle,
            release_at=datetime(2026, 8, 4, tzinfo=UTC),
            expected_identity="someone@example.com",
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
    assert "signing is optional" in capsys.readouterr().out
    assert verify_cli.main(["--inbox", str(inbox), "--require-signature"]) == 1


def test_cli_verifies_a_signed_inbox_and_emits_provenance_json(
    tmp_path, monkeypatch, capsys
) -> None:
    inbox, submission, bundle = make_signed_inbox(tmp_path)
    monkeypatch.setattr(cs, "_cryptographic_verify", stub_verify())
    code = verify_cli.main(
        [
            "--inbox",
            str(inbox),
            "--release-at",
            "2026-08-04",
            "--json",
        ]
    )
    out = capsys.readouterr().out
    assert code == 0
    assert "precedes release" in out
    blocks = json.loads(out[out.index("[") : out.rindex("]") + 1])
    assert len(blocks) == 1
    assert blocks[0]["schemaVersion"] == "thesis_challenge_signature_v1"
    assert blocks[0]["precedesRelease"] is True


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


def test_cli_rejects_a_malformed_release_at(tmp_path) -> None:
    inbox = tmp_path / "inbox"
    write_submission(inbox / "tester" / "cell.json")
    assert verify_cli.main(["--inbox", str(inbox), "--release-at", "yesterday"]) == 2
