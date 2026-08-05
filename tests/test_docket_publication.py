from __future__ import annotations

import argparse
import json
import os
import pathlib
import stat
import subprocess
import sys
from collections.abc import Mapping

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import docket_publication  # noqa: E402
from canonical_json import canonical_bytes, canonical_sha256  # noqa: E402
from docket_publication import PublicationError  # noqa: E402
from register_targets import (  # noqa: E402
    REGISTRATION_SCHEMA,
    registration_content_hash,
)

BATCH = pathlib.PurePosixPath("records/thesis-analyst/batches/2030-01-10/run.json")
RUN_PREFIX = pathlib.PurePosixPath(
    "records/thesis-analyst/2030-01-10/2030-01-10t12-00-00z-agency-test-rate"
)
REGISTRATION = pathlib.PurePosixPath(f"records/targets/2030-01-10-{'a' * 64}.json")

TEST_LEDGER_PIN = {
    "repo": "PolicyEngine/ledger",
    "branch": "codex/thesis-ledger-facts",
    "sha": "f" * 40,
    "jsonlSha256": "0" * 64,
    "lineCount": 128,
}



def git(repo: pathlib.Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def initialize_checkout(
    path: pathlib.Path,
    tracked: Mapping[pathlib.PurePosixPath, bytes] | None = None,
) -> pathlib.Path:
    path.mkdir()
    git(path, "init")
    files = tracked or {pathlib.PurePosixPath("records/base.json"): b"{}\n"}
    for relative, payload in files.items():
        destination = path.joinpath(*relative.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
    git(path, "add", ".")
    git(
        path,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-m",
        "base",
    )
    return path


def batch_payload(
    run_prefix: pathlib.PurePosixPath | None = None,
) -> dict[str, object]:
    results: list[dict[str, object]] = []
    if run_prefix is not None:
        results.append(
            {
                "target": {"targetRegistrationPath": REGISTRATION.as_posix()},
                "manifestPath": (run_prefix / "manifest.json").as_posix(),
            }
        )
    return {
        "schemaVersion": "thesis_batch_manifest_v1",
        "targets": len(results),
        "results": results,
    }


def write_bundle(
    root: pathlib.Path,
    files: Mapping[pathlib.PurePosixPath, bytes] | None = None,
    *,
    batch: dict[str, object] | None = None,
    modes: Mapping[pathlib.PurePosixPath, int] | None = None,
) -> pathlib.Path:
    bundle = root / "bundle"
    repo = bundle / "repo"
    payloads = {
        BATCH: (json.dumps(batch or batch_payload()) + "\n").encode(),
        **(files or {}),
    }
    entries = []
    for relative, payload in payloads.items():
        path = repo.joinpath(*relative.parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        path.chmod((modes or {}).get(relative, 0o644))
        entries.append(
            {
                "path": relative.as_posix(),
                "bytes": path.stat().st_size,
                "sha256": docket_publication.sha256(path),
                "mode": stat.S_IMODE(path.stat().st_mode),
            }
        )
    (bundle / "bundle_manifest.json").write_text(
        json.dumps(
            {
                "schemaVersion": docket_publication.BUNDLE_SCHEMA,
                "batchManifest": BATCH.as_posix(),
                "files": entries,
            }
        )
        + "\n"
    )
    return bundle


def test_stage_copies_only_invocation_scoped_delta(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = initialize_checkout(tmp_path / "repo")
    batch_path = repo.joinpath(*BATCH.parts)
    batch_path.parent.mkdir(parents=True)
    batch_path.write_text(json.dumps(batch_payload()) + "\n")
    (repo / "not-allowed.txt").write_text("do not publish\n")
    monkeypatch.setattr(docket_publication, "ROOT", repo)

    bundle = tmp_path / "staged-bundle"
    docket_publication.stage(
        argparse.Namespace(
            bundle_dir=str(bundle),
            batch=BATCH.as_posix(),
            trusted_targets=None,
        )
    )

    manifest = json.loads((bundle / "bundle_manifest.json").read_text())
    assert manifest["schemaVersion"] == docket_publication.BUNDLE_SCHEMA
    assert manifest["batchManifest"] == BATCH.as_posix()
    assert [entry["path"] for entry in manifest["files"]] == [BATCH.as_posix()]
    assert manifest["files"][0]["mode"] == stat.S_IMODE(batch_path.stat().st_mode)
    assert not (bundle / "repo" / "not-allowed.txt").exists()


def test_trusted_target_comparison_rejects_bool_for_number(
    tmp_path: pathlib.Path,
) -> None:
    trusted_target = {
        "catalogSlug": "agency-test-rate-january-2030",
        "valueScale": 1.0,
        "sourceBinding": {"transform": {"operation": "multiply", "factor": 1.0}},
    }
    untrusted_target = json.loads(json.dumps(trusted_target))
    untrusted_target["sourceBinding"]["transform"]["factor"] = True
    trusted_path = tmp_path / "trusted.json"
    trusted_path.write_text(json.dumps({"targets": [trusted_target]}))

    with pytest.raises(PublicationError, match="privileged registration"):
        docket_publication.compare_trusted_targets(
            {"results": [{"target": untrusted_target}]},
            str(trusted_path),
        )


def test_batch_count_rejects_boolean_number_confusion() -> None:
    batch = batch_payload(RUN_PREFIX)
    batch["targets"] = True

    with pytest.raises(PublicationError, match="target count"):
        docket_publication.batch_scope(BATCH, batch)


def test_load_bundle_rejects_uninventoried_file(tmp_path: pathlib.Path) -> None:
    bundle = write_bundle(tmp_path)
    extra = bundle / "repo" / "records" / "extra.json"
    extra.parent.mkdir(parents=True, exist_ok=True)
    extra.write_text("{}\n")

    with pytest.raises(PublicationError, match="inventory mismatch"):
        docket_publication.load_bundle(bundle, BATCH.as_posix())


def test_repository_paths_reject_traversal_and_nested_symlinks(
    tmp_path: pathlib.Path,
) -> None:
    with pytest.raises(PublicationError, match="unsafe repository path"):
        docket_publication.relative_repo_path("records/../CHAIN_GENESIS.json")

    root = tmp_path / "root"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (root / "records").symlink_to(outside, target_is_directory=True)
    with pytest.raises(PublicationError, match="symlink|escapes"):
        docket_publication.safe_join(
            root, pathlib.PurePosixPath("records/thesis-analyst/run.json")
        )


def test_load_bundle_blocks_different_byte_overwrite(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    existing = RUN_PREFIX / "activity.log"
    checkout = initialize_checkout(
        tmp_path / "checkout", {existing: b"trusted history\n"}
    )
    monkeypatch.setattr(docket_publication, "ROOT", checkout)
    bundle = write_bundle(
        tmp_path,
        {existing: b"rewritten history\n"},
        batch=batch_payload(RUN_PREFIX),
    )

    with pytest.raises(PublicationError, match="may not overwrite HEAD path"):
        docket_publication.load_bundle(bundle, BATCH.as_posix())


def test_load_bundle_repo_root_override_controls_append_only_checkout(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checkout_a = initialize_checkout(
        tmp_path / "checkout-a", {BATCH: b'{"different": true}\n'}
    )
    checkout_b = initialize_checkout(tmp_path / "checkout-b")
    monkeypatch.setattr(docket_publication, "ROOT", checkout_a)
    bundle = write_bundle(tmp_path, batch=batch_payload())

    with pytest.raises(PublicationError, match="may not overwrite HEAD path"):
        docket_publication.load_bundle(bundle, BATCH.as_posix())

    docket_publication.load_bundle(
        bundle,
        BATCH.as_posix(),
        repo_root=checkout_b,
    )


def test_load_bundle_blocks_chain_genesis(tmp_path: pathlib.Path) -> None:
    forbidden = pathlib.PurePosixPath("CHAIN_GENESIS.json")
    bundle = write_bundle(tmp_path, {forbidden: b"{}\n"})

    with pytest.raises(PublicationError, match="record-chain control files"):
        docket_publication.load_bundle(bundle, BATCH.as_posix())


def test_load_bundle_blocks_typescript(tmp_path: pathlib.Path) -> None:
    forbidden = RUN_PREFIX / "ledger-targets.generated.ts"
    bundle = write_bundle(
        tmp_path,
        {forbidden: b"export const injected = true;\n"},
        batch=batch_payload(RUN_PREFIX),
    )

    with pytest.raises(PublicationError, match="executable source code"):
        docket_publication.load_bundle(bundle, BATCH.as_posix())


def test_load_bundle_blocks_path_outside_exact_invocation_scope(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checkout = initialize_checkout(tmp_path / "checkout")
    monkeypatch.setattr(docket_publication, "ROOT", checkout)
    other_run = pathlib.PurePosixPath(
        "records/thesis-analyst/2030-01-10/2030-01-10t12-00-00z-other-run/activity.log"
    )
    bundle = write_bundle(
        tmp_path,
        {other_run: b"out of scope\n"},
        batch=batch_payload(RUN_PREFIX),
    )

    with pytest.raises(PublicationError, match="outside this invocation"):
        docket_publication.load_bundle(bundle, BATCH.as_posix())


def test_load_bundle_allows_identical_restatement(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    existing = RUN_PREFIX / "activity.log"
    payload = b"byte-identical history\n"
    checkout = initialize_checkout(tmp_path / "checkout", {existing: payload})
    monkeypatch.setattr(docket_publication, "ROOT", checkout)
    bundle = write_bundle(
        tmp_path,
        {existing: payload},
        batch=batch_payload(RUN_PREFIX),
    )

    repo, manifest = docket_publication.load_bundle(bundle, BATCH.as_posix())
    docket_publication.apply_bundle(repo, manifest)

    assert checkout.joinpath(*existing.parts).read_bytes() == payload


def test_committed_batch_selects_only_its_deterministic_wave(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    payload = (json.dumps(batch_payload()) + "\n").encode()
    checkout = initialize_checkout(tmp_path / "checkout", {BATCH: payload})
    monkeypatch.setattr(docket_publication, "ROOT", checkout)
    bundle_repo = tmp_path / "bundle-repo"
    batch_path = bundle_repo.joinpath(*BATCH.parts)
    batch_path.parent.mkdir(parents=True)
    batch_path.write_bytes(payload)

    expected_hash = docket_publication.hashlib.sha256(payload).hexdigest()
    assert docket_publication.published_wave_collision_exclusion(
        bundle_repo, BATCH
    ) == (
        checkout
        / "site/src/data/forecast-examples"
        / f"auto-2030-01-10-{expected_hash}.ts"
    )

    batch_path.write_text(json.dumps(batch_payload()))
    assert (
        docket_publication.published_wave_collision_exclusion(bundle_repo, BATCH)
        is None
    )


def test_load_bundle_blocks_executable_mode(tmp_path: pathlib.Path) -> None:
    executable = RUN_PREFIX / "activity.log"
    bundle = write_bundle(
        tmp_path,
        {executable: b"data only\n"},
        batch=batch_payload(RUN_PREFIX),
        modes={executable: 0o755},
    )

    with pytest.raises(PublicationError, match="executable bundle file"):
        docket_publication.load_bundle(bundle, BATCH.as_posix())


def test_run_inventory_rejects_unreferenced_extra_file(tmp_path: pathlib.Path) -> None:
    repo = tmp_path / "repo"
    run_dir = repo.joinpath(*RUN_PREFIX.parts)
    run_dir.mkdir(parents=True)
    manifest_relative = RUN_PREFIX / "manifest.json"
    artifact_relative = RUN_PREFIX / "activity.log"
    custody_relative = RUN_PREFIX / "custody_root.json"
    manifest = {
        "artifacts": [
            {"path": manifest_relative.as_posix()},
            {"path": artifact_relative.as_posix()},
        ]
    }
    repo.joinpath(*manifest_relative.parts).write_text(json.dumps(manifest))
    repo.joinpath(*artifact_relative.parts).write_text("declared\n")
    repo.joinpath(*custody_relative.parts).write_text("{}\n")
    (run_dir / "surprise.txt").write_text("not in custody graph\n")

    with pytest.raises(PublicationError, match="run file inventory mismatch"):
        docket_publication.validate_run_file_inventory(
            repo, manifest_relative, manifest
        )


@pytest.mark.parametrize(
    "sample, expected",
    [
        (b"ghp_" + b"a" * 36, "GitHub token"),
        (b"sk-proj-" + b"a" * 24, "OpenAI API key"),
        (b"AKIA" + b"A" * 16, "AWS access key"),
        (b"xoxb-" + b"a" * 24, "Slack token"),
        (b"-----BEGIN PRIVATE KEY-----", "private key"),
    ],
)
def test_secret_scanner_detects_common_token_shapes(
    sample: bytes, expected: str
) -> None:
    assert expected in docket_publication.scan_bytes(sample)


def test_scan_staged_rejects_secret(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    (repo / "records").mkdir()
    (repo / "records" / "leak.txt").write_bytes(b"ghp_" + b"a" * 36)
    git(repo, "add", "records/leak.txt")
    monkeypatch.setattr(docket_publication, "ROOT", repo)

    with pytest.raises(PublicationError, match="possible GitHub token"):
        docket_publication.scan_staged(argparse.Namespace())


def test_validate_target_registration_rejects_snapshot_tampering(
    tmp_path: pathlib.Path,
) -> None:
    contract = {
        "series": "agency.test.rate",
        "period": "2030-01",
        "catalogSlug": "agency-test-rate-january-2030",
        "dataPointId": "agency.test.rate.2030_01.first_print",
        "unit": "percent",
        "valueScale": 1.0,
        "resolutionDateBasis": "resolve-by-bound",
        "resolutionDate": "2030-03-31",
        "sourceBinding": {
            "adapter": "generic-url",
            "expectedReleaseWindow": {
                "start": "2030-02-01",
                "end": "2030-03-31",
            },
        },
    }
    snapshot = {
        "schemaVersion": REGISTRATION_SCHEMA,
        "registeredAtUtc": "2030-01-10T11:59:00Z",
        "targets": [contract],
        "ledgerPin": TEST_LEDGER_PIN,
    }
    content_hash = registration_content_hash(snapshot)
    relative = pathlib.Path("records/targets") / f"2030-01-10-{content_hash}.json"
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    path.write_bytes(canonical_bytes(snapshot) + b"\n")
    target = {
        "series": contract["series"],
        "period": contract["period"],
        "catalogSlug": contract["catalogSlug"],
        "dataPointId": contract["dataPointId"],
        "targetUnit": contract["unit"],
        "valueScale": contract["valueScale"],
        "resolutionDateBasis": contract["resolutionDateBasis"],
        "resolutionDate": contract["resolutionDate"],
        "expectedReleaseWindow": contract["sourceBinding"][
            "expectedReleaseWindow"
        ],
        "sourceBinding": contract["sourceBinding"],
        "targetRegistrationPath": relative.as_posix(),
        "targetContentHash": content_hash,
    }

    docket_publication.validate_target_registration(tmp_path, target)
    with pytest.raises(PublicationError) as error:
        docket_publication.validate_target_registration(
            tmp_path, {**target, "resolutionDateBasis": "release-calendar"}
        )
    assert str(error.value) == (
        "target registration contract mismatch for resolutionDateBasis: "
        f"{relative.as_posix()}"
    )
    snapshot["targets"][0]["unit"] = "ratio"
    path.write_text(json.dumps(snapshot))
    with pytest.raises(PublicationError, match="hash mismatch"):
        docket_publication.validate_target_registration(tmp_path, target)


def test_validate_target_registration_rejects_malformed_bounded_snapshot(
    tmp_path: pathlib.Path,
) -> None:
    contract = {
        "series": "agency.test.rate",
        "period": "2030-01",
        "catalogSlug": "agency-test-rate-january-2030",
        "dataPointId": "agency.test.rate.2030_01.first_print",
        "unit": "percent",
        "valueScale": 1.0,
        "resolutionDateBasis": "resolve-by-bound",
        "resolutionDate": "2030-03-31",
        "sourceBinding": {"adapter": "generic-url"},
    }
    snapshot = {
        "schemaVersion": REGISTRATION_SCHEMA,
        "registeredAtUtc": "2030-01-10T11:59:00Z",
        "targets": [contract],
        "ledgerPin": TEST_LEDGER_PIN,
    }
    hash_payload = {
        "schemaVersion": REGISTRATION_SCHEMA,
        "targets": [contract],
        "ledgerPin": TEST_LEDGER_PIN,
    }
    content_hash = canonical_sha256(hash_payload)
    relative = pathlib.Path("records/targets") / f"2030-01-10-{content_hash}.json"
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    path.write_bytes(canonical_bytes(snapshot) + b"\n")
    target = {
        "series": contract["series"],
        "period": contract["period"],
        "catalogSlug": contract["catalogSlug"],
        "dataPointId": contract["dataPointId"],
        "targetUnit": contract["unit"],
        "valueScale": contract["valueScale"],
        "resolutionDateBasis": contract["resolutionDateBasis"],
        "resolutionDate": contract["resolutionDate"],
        "sourceBinding": contract["sourceBinding"],
        "targetRegistrationPath": relative.as_posix(),
        "targetContentHash": content_hash,
    }

    with pytest.raises(PublicationError) as error:
        docket_publication.validate_target_registration(tmp_path, target)
    assert str(error.value) == (
        "resolve-by-bound target requires an exact expectedReleaseWindow"
    )


def committed_registration(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    registered_at: str = "2030-01-10T11:59:00Z",
    author_at: str = "2030-01-10T12:00:00Z",
    committer_at: str | None = None,
) -> tuple[pathlib.Path, dict[str, object]]:
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    git(checkout, "init")
    (checkout / "README.md").write_text("base\n")
    git(checkout, "add", "README.md")
    git(
        checkout,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-m",
        "base",
    )
    contract = {
        "series": "agency.test.rate",
        "period": "2030-01",
        "catalogSlug": "agency-test-rate-january-2030",
        "dataPointId": "agency.test.rate.2030_01.first_print",
        "unit": "percent",
        "valueScale": 1.0,
        "sourceBinding": {"adapter": "generic-url"},
    }
    snapshot = {
        "schemaVersion": REGISTRATION_SCHEMA,
        "registeredAtUtc": registered_at,
        "targets": [contract],
        "ledgerPin": TEST_LEDGER_PIN,
    }
    content_hash = registration_content_hash(snapshot)
    relative = pathlib.PurePosixPath(f"records/targets/2030-01-10-{content_hash}.json")
    path = checkout.joinpath(*relative.parts)
    path.parent.mkdir(parents=True)
    path.write_bytes(canonical_bytes(snapshot) + b"\n")
    git(checkout, "add", relative.as_posix())
    env = {
        **dict(os.environ),
        "GIT_AUTHOR_DATE": author_at,
        "GIT_COMMITTER_DATE": committer_at or author_at,
    }
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=test",
            "-c",
            "user.email=test@example.com",
            "commit",
            "-m",
            "register",
        ],
        cwd=checkout,
        env=env,
        check=True,
        capture_output=True,
    )
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=checkout, text=True
    ).strip()
    monkeypatch.setattr(docket_publication, "ROOT", checkout)
    target: dict[str, object] = {
        "series": contract["series"],
        "period": contract["period"],
        "catalogSlug": contract["catalogSlug"],
        "dataPointId": contract["dataPointId"],
        "targetUnit": contract["unit"],
        "valueScale": contract["valueScale"],
        "sourceBinding": contract["sourceBinding"],
        "registeredAtUtc": registered_at,
        "targetRegistrationPath": relative.as_posix(),
        "targetContentHash": content_hash,
        "registrationCommit": commit,
    }
    return checkout, target


def test_registration_commit_must_be_ancestor_and_predate_run(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checkout, target = committed_registration(tmp_path, monkeypatch)

    docket_publication.validate_target_registration(
        checkout,
        target,
        run_started_at="2030-01-10T12:01:00Z",
        require_git_binding=True,
    )

    with pytest.raises(PublicationError, match="does not predate run start"):
        docket_publication.validate_target_registration(
            checkout,
            target,
            run_started_at="2030-01-10T11:59:30Z",
            require_git_binding=True,
        )

    with pytest.raises(PublicationError, match="does not predate run start"):
        docket_publication.validate_target_registration(
            checkout,
            target,
            run_started_at="2030-01-10T12:00:00Z",
            require_git_binding=True,
        )

    with pytest.raises(PublicationError, match="not an ancestor"):
        docket_publication.validate_target_registration(
            checkout,
            {**target, "registrationCommit": "f" * 40},
            run_started_at="2030-01-10T12:01:00Z",
            require_git_binding=True,
        )


def test_registration_timestamp_cannot_be_backdated_far_before_commit(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checkout, target = committed_registration(
        tmp_path,
        monkeypatch,
        registered_at="2030-01-10T10:00:00Z",
    )

    with pytest.raises(PublicationError, match="not contemporaneous"):
        docket_publication.validate_target_registration(
            checkout,
            target,
            run_started_at="2030-01-10T12:01:00Z",
            require_git_binding=True,
        )


def test_registration_timestamp_must_match_committer_time_after_rebase(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checkout, target = committed_registration(
        tmp_path,
        monkeypatch,
        registered_at="2030-01-10T10:00:00Z",
        author_at="2030-01-10T10:01:00Z",
        committer_at="2030-01-10T12:00:00Z",
    )

    with pytest.raises(PublicationError, match="committer time"):
        docket_publication.validate_target_registration(
            checkout,
            target,
            run_started_at="2030-01-10T12:01:00Z",
            require_git_binding=True,
        )


def test_cell_seal_must_not_postdate_batch_result_finish(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = {
        "series": "agency.test.rate",
        "period": "2030-01",
        "conditional": None,
        "registrationCommit": "a" * 40,
        "targetContentHash": "b" * 64,
        "targetRegistrationPath": f"records/targets/2030-01-01-{'b' * 64}.json",
        "registeredAtUtc": "2030-01-01T00:00:00Z",
    }
    manifest = {
        "schemaVersion": "thesis_analyst_run_manifest_v1",
        "createdAt": "2030-01-10T12:00:00Z",
        "runStartedAt": "2030-01-10T12:00:00Z",
        "series": target["series"],
        "period": target["period"],
        "conditional": None,
        "targetContext": target,
        **{
            field: target[field]
            for field in docket_publication.REGISTRATION_BINDING_FIELDS
        },
    }
    result = {
        "target": target,
        "manifestPath": (RUN_PREFIX / "manifest.json").as_posix(),
        "startedAt": "2030-01-10T11:59:59Z",
        "finishedAt": "2030-01-10T12:00:10Z",
    }
    cell = {
        "runStartedAt": "2030-01-10T12:00:00Z",
        "runAt": "2030-01-10T12:00:11Z",
        **{
            field: target[field]
            for field in docket_publication.REGISTRATION_BINDING_FIELDS
        },
    }
    monkeypatch.setattr(
        docket_publication,
        "validate_target_registration",
        lambda *_args, **_kwargs: {},
    )

    with pytest.raises(PublicationError, match="postdates batch result finish"):
        docket_publication.validate_run_binding(
            pathlib.Path("."),
            result,
            manifest,
            [cell],
            require_git_binding=True,
        )


@pytest.mark.parametrize(
    ("publish_upper", "message"),
    [
        (None, "requires publishValidatedAtUtc"),
        ("2030-01-10T12:01:59Z", "after privileged publication"),
    ],
)
def test_privileged_publication_requires_and_enforces_upper_bound(
    tmp_path: pathlib.Path,
    publish_upper: str | None,
    message: str,
) -> None:
    batch = tmp_path.joinpath(*BATCH.parts)
    batch.parent.mkdir(parents=True)
    batch.write_text(
        json.dumps(
            {
                "schemaVersion": "thesis_batch_manifest_v1",
                "promptMode": "fast",
                "startedAt": "2030-01-10T12:00:00Z",
                "finishedAt": "2030-01-10T12:02:00Z",
                "targets": 0,
                "results": [],
            }
        )
        + "\n"
    )

    with pytest.raises(PublicationError, match=message):
        docket_publication.validate_cells(
            tmp_path,
            BATCH.as_posix(),
            require_git_binding=True,
            publish_validated_at_utc=publish_upper,
        )


def _real_pre_cutover_v2_target() -> dict:
    """Project a real committed pre-cutover v2 snapshot into a batch target."""

    for path in sorted((ROOT / "records" / "targets").glob("*.json")):
        snapshot = json.loads(path.read_text())
        if snapshot.get("schemaVersion") != "thesis_target_registration_v2":
            continue
        rows = snapshot.get("targets") or []
        if len(rows) != 1:
            continue
        contract = rows[0]
        relative = path.relative_to(ROOT).as_posix()
        commits = subprocess.check_output(
            ["git", "log", "--diff-filter=A", "--format=%H", "--", relative],
            cwd=ROOT,
            text=True,
        ).split()
        if len(commits) != 1:
            continue
        return {
            "series": contract["series"],
            "period": contract["period"],
            "catalogSlug": contract["catalogSlug"],
            "dataPointId": contract["dataPointId"],
            "country": contract["country"],
            "targetUnit": contract["unit"],
            "valueScale": contract["valueScale"],
            "expectedReleaseWindow": contract["sourceBinding"][
                "expectedReleaseWindow"
            ],
            "sourceBinding": contract["sourceBinding"],
            "registeredAtUtc": snapshot["registeredAtUtc"],
            "targetContentHash": registration_content_hash(snapshot),
            "targetRegistrationPath": relative,
            "registrationCommit": commits[0],
        }
    pytest.skip("repository has no single-target pre-cutover v2 registration")


def test_pre_cutover_v2_registration_requires_explicit_grandfather() -> None:
    target = _real_pre_cutover_v2_target()
    run_started_at = "2026-07-10T23:59:59Z"

    with pytest.raises(PublicationError, match="privileged publication requires"):
        docket_publication.validate_target_registration(
            ROOT,
            target,
            run_started_at=run_started_at,
            require_git_binding=True,
        )

    snapshot = docket_publication.validate_target_registration(
        ROOT,
        target,
        run_started_at=run_started_at,
        require_git_binding=True,
        allow_pre_cutover_v2=True,
    )
    assert snapshot["schemaVersion"] == "thesis_target_registration_v2"


def test_grandfathered_v2_must_strictly_predate_the_cutover(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = _real_pre_cutover_v2_target()
    monkeypatch.setattr(
        docket_publication,
        "V3_REGISTRATION_CUTOVER_COMMIT",
        target["registrationCommit"],
    )

    with pytest.raises(PublicationError, match="strictly predate the v3 cutover"):
        docket_publication.validate_target_registration(
            ROOT,
            target,
            run_started_at="2026-07-10T23:59:59Z",
            require_git_binding=True,
            allow_pre_cutover_v2=True,
        )


def test_tampered_pre_cutover_v2_content_hash_is_rejected() -> None:
    target = dict(_real_pre_cutover_v2_target())
    original = target["targetContentHash"]
    target["targetContentHash"] = ("0" if original[0] != "0" else "1") + original[1:]

    with pytest.raises(PublicationError, match="hash mismatch"):
        docket_publication.validate_target_registration(
            ROOT,
            target,
            run_started_at="2026-07-10T23:59:59Z",
            require_git_binding=True,
            allow_pre_cutover_v2=True,
        )
