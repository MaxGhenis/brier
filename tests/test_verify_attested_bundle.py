from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import pathlib
import stat
import subprocess
import sys
from dataclasses import dataclass
from typing import Any

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import docket_publication  # noqa: E402
import generation_tickets  # noqa: E402
import run_thesis_analyst as analyst  # noqa: E402
import verify_attested_bundle as verifier  # noqa: E402
from canonical_json import canonical_sha256  # noqa: E402

NONCE = "a" * 64
TICKET_ID = "2030-01-10-deadbeef"
TICKET_RELATIVE = pathlib.PurePosixPath(
    f"records/tickets/2030-01-10/{TICKET_ID}.json"
)
RUN_RELATIVE = pathlib.PurePosixPath(
    "records/thesis-analyst/2030-01-10/"
    "2030-01-10t12-00-00z-agency-test-rate"
)
RUN_STARTED_AT = "2030-01-10T12:00:00Z"
SEALED_AT = "2030-01-10T12:01:00Z"
NOW_UTC = dt.datetime(2030, 1, 10, 13, tzinfo=dt.timezone.utc)


@dataclass
class AttestedFixture:
    repo: pathlib.Path
    bundle: pathlib.Path
    ticket_path: pathlib.Path
    ticket: dict[str, Any]
    ticket_sha: str
    batch_relative: pathlib.PurePosixPath
    run_relative: pathlib.PurePosixPath


def git(repo: pathlib.Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def commit_all(repo: pathlib.Path, message: str) -> str:
    git(repo, "add", "-A")
    git(
        repo,
        "-c",
        "user.name=attested-fixture",
        "-c",
        "user.email=attested@example.com",
        "commit",
        "-m",
        message,
    )
    return git(repo, "rev-parse", "HEAD")


def write_payload(path: pathlib.Path, payload: Any) -> bytes:
    data = (json.dumps(payload, indent=2) + "\n").encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return data


def refresh_bundle_manifest(fixture: AttestedFixture) -> None:
    bundle_repo = fixture.bundle / "repo"
    entries = []
    for path in sorted(
        candidate for candidate in bundle_repo.rglob("*") if candidate.is_file()
    ):
        relative = pathlib.PurePosixPath(path.relative_to(bundle_repo).as_posix())
        raw = path.read_bytes()
        entries.append(
            {
                "path": relative.as_posix(),
                "bytes": len(raw),
                "sha256": sha256_bytes(raw),
                "mode": stat.S_IMODE(path.stat().st_mode),
            }
        )
    write_payload(
        fixture.bundle / "bundle_manifest.json",
        {
            "schemaVersion": docket_publication.BUNDLE_SCHEMA,
            "batchManifest": fixture.batch_relative.as_posix(),
            "files": entries,
        },
    )


def run_path(fixture: AttestedFixture, filename: str) -> pathlib.Path:
    return fixture.bundle.joinpath("repo", *fixture.run_relative.parts, filename)


def run_manifest_path(fixture: AttestedFixture) -> pathlib.Path:
    return run_path(fixture, "manifest.json")


def rewrite_run_manifest(
    fixture: AttestedFixture, mutate: Any
) -> dict[str, Any]:
    path = run_manifest_path(fixture)
    manifest = json.loads(path.read_text())
    mutate(manifest)
    write_payload(path, manifest)
    refresh_bundle_manifest(fixture)
    return manifest


def rewrite_batch(fixture: AttestedFixture, mutate: Any) -> dict[str, Any]:
    path = fixture.bundle.joinpath("repo", *fixture.batch_relative.parts)
    batch = json.loads(path.read_text())
    mutate(batch)
    write_payload(path, batch)
    refresh_bundle_manifest(fixture)
    return batch


def rewrite_run_artifact(
    fixture: AttestedFixture,
    filename: str,
    payload: bytes,
) -> None:
    path = run_path(fixture, filename)
    path.write_bytes(payload)

    def update_ref(manifest: dict[str, Any]) -> None:
        expected = (fixture.run_relative / filename).as_posix()
        matches = [
            artifact
            for artifact in manifest["artifacts"]
            if artifact.get("path") == expected
        ]
        assert len(matches) == 1
        matches[0]["bytes"] = len(payload)
        matches[0]["sha256"] = sha256_bytes(payload)

    rewrite_run_manifest(fixture, update_ref)


def rewrite_final_response(
    fixture: AttestedFixture,
    tmp_path: pathlib.Path,
    cells: list[dict[str, Any]],
) -> None:
    response = json.dumps(cells, indent=2)
    raw_jsonl = codex_jsonl(response)
    parsed_stream = analyst.parse_codex_jsonl(raw_jsonl, "")
    parsed = analyst.extract_json_payload(response)
    parsed_path = tmp_path / "tampered-parsed.json"
    normalized_path = tmp_path / "tampered-normalized.json"
    write_payload(parsed_path, parsed)
    analyst.normalize_cells(parsed_path, normalized_path)
    normalized = json.loads(normalized_path.read_text())

    replacements = {
        "codex_stdout.jsonl": raw_jsonl.encode(),
        "codex_events.jsonl": parsed_stream["eventsJsonl"].encode(),
        "codex_last_message.txt": response.encode(),
        "stdout.txt": response.encode(),
        "raw_response.txt": response.encode(),
        "parsed_cells.json": json.dumps(parsed, indent=2).encode(),
        "normalized_cells.json": (
            json.dumps(normalized, indent=2) + "\n"
        ).encode(),
    }
    for filename, payload in replacements.items():
        rewrite_run_artifact(fixture, filename, payload)


def command_argv(
    fixture: AttestedFixture,
    *,
    prefix: str,
    model: str,
    search: bool,
) -> list[str]:
    argv = ["/opt/thesis/bin/codex"]
    if search:
        argv.append("--search")
    argv.extend(
        [
            "exec",
            "--json",
            "--skip-git-repo-check",
            "--ignore-user-config",
            "-o",
            str(
                fixture.repo.joinpath(
                    *fixture.run_relative.parts,
                    f"{prefix}codex_last_message.txt",
                )
            ),
            "-m",
            model,
            "-c",
            'reasoning_effort="high"',
            "-C",
            str(fixture.repo),
            "-s",
            "read-only",
            "<prompt>",
        ]
    )
    return argv


def codex_jsonl(response: str) -> str:
    return (
        json.dumps(
            {
                "type": "item.completed",
                "item": {"type": "agent_message", "text": response},
            }
        )
        + "\n"
        + json.dumps({"type": "turn.completed", "usage": {}})
        + "\n"
    )


@pytest.fixture
def attested_bundle(tmp_path: pathlib.Path) -> AttestedFixture:
    repo = tmp_path / "checkout"
    repo.mkdir()
    git(repo, "init")

    registration_payload = b'{"schemaVersion":"fixture_registration_v1"}\n'
    registration_hash = sha256_bytes(registration_payload)
    registration_relative = pathlib.PurePosixPath(
        f"records/targets/2030-01-10-{registration_hash}.json"
    )
    registration_path = repo.joinpath(*registration_relative.parts)
    registration_path.parent.mkdir(parents=True)
    registration_path.write_bytes(registration_payload)
    registration_commit = commit_all(repo, "Register synthetic target")

    target = {
        "registrationCommit": registration_commit,
        "targetContentHash": registration_hash,
        "targetRegistrationPath": registration_relative.as_posix(),
        "registeredAtUtc": "2030-01-10T10:00:00Z",
        "catalogSlug": "agency-test-rate-january-2030",
        "series": "agency.test.rate",
        "period": "2030-01",
        "conditional": None,
        "country": "US",
        "targetUnit": "percent",
        "dataPointId": "agency.test.rate.2030_01.first_print",
        "resolutionDate": "2030-02-01",
        "resolutionSource": "Synthetic agency",
        "resolutionSourceUrl": "https://example.gov/series",
        "resolutionRule": "Resolve to the synthetic first print.",
        "sourceBinding": {"adapter": "generic-url"},
    }
    policy = {
        "promptMode": "fast",
        "codexModel": "gpt-ticket-main",
        "codexReasoningEffort": "high",
        "codexSandbox": "read-only",
        "codexNetwork": False,
        "reviewCodexModel": "gpt-ticket-review",
        "reviewCodexSearch": True,
        "timeoutSeconds": 1,
    }
    ticket = generation_tickets.validate_ticket(
        {
            "schemaVersion": generation_tickets.TICKET_SCHEMA,
            "ticketId": TICKET_ID,
            "nonce": NONCE,
            "mintedAtUtc": "2030-01-10T11:00:00Z",
            "expiresAtUtc": "2030-01-11T11:00:00Z",
            "attempt": 1,
            "supersedesTicketId": None,
            "supersededOutcome": None,
            "targets": [target],
            "registrationSetHash": canonical_sha256({"targets": [target]}),
            "policy": policy,
        }
    )
    ticket_path = repo.joinpath(*TICKET_RELATIVE.parts)
    write_payload(ticket_path, ticket)
    ticket_sha = commit_all(repo, "Mint synthetic generation ticket")

    bundle = tmp_path / "bundle"
    batch_relative = pathlib.PurePosixPath(
        "records/thesis-analyst/batches/2030-01-10/"
        f"attested-{TICKET_ID}.json"
    )
    fixture = AttestedFixture(
        repo,
        bundle,
        ticket_path,
        ticket,
        ticket_sha,
        batch_relative,
        RUN_RELATIVE,
    )
    bundle_repo = bundle / "repo"
    bundled_registration = bundle_repo.joinpath(*registration_relative.parts)
    bundled_registration.parent.mkdir(parents=True)
    bundled_registration.write_bytes(registration_payload)

    prompt_context = {
        "ticketId": TICKET_ID,
        "ticketPath": TICKET_RELATIVE.as_posix(),
        "nonce": NONCE,
    }
    prompt, prompt_meta = analyst.build_run_prompt(
        target["series"],
        target["period"],
        target["conditional"],
        policy["promptMode"],
        target,
        ticket=prompt_context,
        network_tools=policy["codexNetwork"],
    )
    raw_cells = [
        {
            "slug": target["catalogSlug"],
            "country": "US",
            "type": "data",
            "title": "Synthetic agency test rate",
            "question": "What will the synthetic rate be?",
            "unit": "percent",
            "pointEstimate": 1.0,
            "ciLow": 0.5,
            "ciHigh": 1.5,
            "confidence": 0.8,
            "resolutionDate": target["resolutionDate"],
            "resolutionSource": target["resolutionSource"],
            "resolutionSourceUrl": target["resolutionSourceUrl"],
            "resolutionRule": target["resolutionRule"],
            "dataPointId": target["dataPointId"],
            "historicalContext": [
                {"label": "2029-11", "value": 0.8},
                {"label": "2029-12", "value": 0.9},
            ],
            "drivers": ["Synthetic momentum"],
            "sourceContext": [target["resolutionSourceUrl"]],
            "runAt": "2030-01-10T12:00:30Z",
            "reasoning": [
                {"kind": "math", "text": "sigma = 0.39; 1.28*sigma = 0.50."},
                {"kind": "forecast", "point": 1.0, "ciLow": 0.5, "ciHigh": 1.5},
            ],
        }
    ]
    last_message = json.dumps(raw_cells, indent=2)
    draft_response = last_message
    review_response = json.dumps(
        {
            "summary": "Synthetic review found no required changes.",
            "requiredFixes": [],
            "optionalSuggestions": [],
        }
    )
    parsed_cells = analyst.extract_json_payload(last_message)
    parsed_temp = tmp_path / "parsed.json"
    normalized_temp = tmp_path / "normalized.json"
    write_payload(parsed_temp, parsed_cells)
    analyst.normalize_cells(parsed_temp, normalized_temp)
    normalized_cells = json.loads(normalized_temp.read_text())
    distribution = analyst.seal_normalized_cells(
        normalized_cells,
        conditional=target["conditional"],
        run_started_at=RUN_STARTED_AT,
        sealed_at=SEALED_AT,
        prompt_mode=policy["promptMode"],
        target_context=target,
    )

    refs: list[dict[str, Any]] = []

    def artifact(
        filename: str, artifact_type: str, payload: str | bytes
    ) -> dict[str, Any]:
        raw = payload.encode() if isinstance(payload, str) else payload
        path = run_path(fixture, filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        ref = {
            "artifactType": artifact_type,
            "path": (RUN_RELATIVE / filename).as_posix(),
            "sha256": sha256_bytes(raw),
            "bytes": len(raw),
            "createdAt": RUN_STARTED_AT,
        }
        refs.append(ref)
        return ref

    artifact("prompt.md", "prompt", prompt)
    command_ticket = {"ticketId": TICKET_ID, "ticketPath": TICKET_RELATIVE.as_posix()}

    def stage(
        *,
        prefix: str,
        model: str,
        search: bool,
        response: str,
        stdout_artifact_type: str,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        argv = command_argv(fixture, prefix=prefix, model=model, search=search)
        command = {
            "backend": "codex",
            "argv": argv,
            "generationTicket": command_ticket,
            "networkAccess": policy["codexNetwork"],
            "timeoutSeconds": policy["timeoutSeconds"],
            "returnCode": 0,
            "processReturnCode": 0,
            "timedOut": False,
            "timeoutReason": None,
            "terminatedAfterOutput": False,
            "startedAt": RUN_STARTED_AT,
            "finishedAt": SEALED_AT,
        }
        artifact(
            f"{prefix}command.json",
            "command",
            json.dumps(command, indent=2),
        )
        raw_jsonl = codex_jsonl(response)
        parsed_stream = analyst.parse_codex_jsonl(raw_jsonl, "")
        artifact(
            f"{prefix}codex_stdout.jsonl", "codex_stdout_jsonl", raw_jsonl
        )
        artifact(f"{prefix}codex_stderr.log", "codex_stderr_log", b"")
        artifact(
            f"{prefix}codex_events.jsonl",
            "codex_events_jsonl",
            parsed_stream["eventsJsonl"],
        )
        artifact(
            f"{prefix}codex_last_message.txt", "codex_last_message", response
        )
        artifact(
            f"{prefix}codex_trace.json",
            "codex_trace",
            json.dumps(
                {
                    "provider": "openai",
                    "backend": "codex-exec",
                    "auth": "codex-cli-subscription",
                    "model": model,
                    "searchEnabled": search,
                    "sandbox": policy["codexSandbox"],
                    "networkAccess": policy["codexNetwork"],
                    "reasoningEffort": policy["codexReasoningEffort"],
                    "timeoutSeconds": policy["timeoutSeconds"],
                    "timedOut": False,
                    "timeoutReason": None,
                    "terminatedAfterOutput": False,
                    "processReturnCode": 0,
                    "effectiveReturnCode": 0,
                    "usage": {},
                    "eventCount": 2,
                    "lastError": None,
                },
                indent=2,
            ),
        )
        stdout_ref = artifact(
            f"{prefix}stdout.txt", stdout_artifact_type, response
        )
        artifact(f"{prefix}stderr.txt", "stderr", b"")
        return command, stdout_ref

    _draft_command, draft_ref = stage(
        prefix="draft_",
        model=policy["codexModel"],
        search=True,
        response=draft_response,
        stdout_artifact_type="draft_forecast",
    )
    review_prompt = analyst.build_pre_submit_review_prompt(
        series=target["series"],
        period=target["period"],
        conditional=target["conditional"],
        target_context=target,
        original_prompt=prompt,
        draft_response=draft_response,
    )
    artifact(
        "pre_submit_review_prompt.md", "review_prompt", review_prompt
    )
    review_command, review_ref = stage(
        prefix="pre_submit_review_",
        model=policy["reviewCodexModel"],
        search=policy["reviewCodexSearch"],
        response=review_response,
        stdout_artifact_type="pre_submit_review",
    )
    revision_prompt = analyst.build_revision_prompt(
        original_prompt=prompt,
        draft_response=draft_response,
        review_response=review_response,
    )
    revision_prompt_ref = artifact(
        "revision_prompt.md", "revision_prompt", revision_prompt
    )
    final_command, _final_ref = stage(
        prefix="",
        model=policy["codexModel"],
        search=True,
        response=last_message,
        stdout_artifact_type="stdout",
    )
    artifact("raw_response.txt", "raw_response", last_message)
    artifact("parsed_cells.json", "parsed_cell", json.dumps(parsed_cells, indent=2))
    artifact(
        "normalized_cells.json",
        "normalized_cell",
        json.dumps(normalized_cells, indent=2) + "\n",
    )
    artifact(
        "distribution.json",
        "run_distribution",
        json.dumps(distribution, indent=2) + "\n",
    )
    artifact(
        "validation.json",
        "validation_report",
        json.dumps({"ok": True, "errors": []}, indent=2),
    )
    runtime_meta = analyst.stamp_runtime_invocation(prompt_meta, final_command)
    pre_submit_review = analyst.build_pre_submit_review_metadata(
        status="completed",
        requested_at=RUN_STARTED_AT,
        review_result=review_command,
        review_payload=analyst.parse_review_payload(review_response),
        draft_ref=draft_ref,
        review_ref=review_ref,
        revision_prompt_ref=revision_prompt_ref,
        normalized_cells=normalized_cells,
    )
    cells_with_activity = analyst.attach_activity_log(
        normalized_cells,
        refs,
        runtime_meta,
        pre_submit_review,
        force_model=True,
    )
    cells_relative = RUN_RELATIVE / "cells.with_activity.json"
    artifact(
        cells_relative.name,
        "cells_with_activity",
        json.dumps(cells_with_activity, indent=2) + "\n",
    )

    binding = generation_tickets.ticket_manifest_binding(prompt_context)
    manifest = {
        "schemaVersion": "thesis_analyst_run_manifest_v1",
        "createdAt": RUN_STARTED_AT,
        "runStartedAt": RUN_STARTED_AT,
        "sealedAt": SEALED_AT,
        "series": target["series"],
        "period": target["period"],
        "conditional": target["conditional"],
        "targetContext": target,
        "promptMode": policy["promptMode"],
        "agent": runtime_meta,
        "preSubmitReview": pre_submit_review,
        "ok": True,
        "cellsPath": cells_relative.as_posix(),
        "artifacts": refs,
        "generationTicket": binding,
        "checkoutSha": ticket_sha,
    }
    write_payload(run_manifest_path(fixture), manifest)

    batch = {
        "schemaVersion": "thesis_batch_manifest_v1",
        "startedAt": RUN_STARTED_AT,
        "finishedAt": "2030-01-10T12:02:00Z",
        "promptMode": policy["promptMode"],
        "codexModel": policy["codexModel"],
        "codexReasoningEffort": policy["codexReasoningEffort"],
        "codexSandbox": policy["codexSandbox"],
        "codexNetwork": policy["codexNetwork"],
        "reviewCodexModel": policy["reviewCodexModel"],
        "reviewCodexSearch": policy["reviewCodexSearch"],
        "timeoutSeconds": policy["timeoutSeconds"],
        "targets": 1,
        "ok": 1,
        "failed": 0,
        "results": [
            {
                "target": target,
                "startedAt": RUN_STARTED_AT,
                "finishedAt": "2030-01-10T12:02:00Z",
                "returnCode": 0,
                "ok": True,
                "manifestPath": (RUN_RELATIVE / "manifest.json").as_posix(),
                "cellsPath": cells_relative.as_posix(),
                "validationErrors": [],
            }
        ],
        "generationTicket": binding,
        "checkoutSha": ticket_sha,
    }
    write_payload(bundle_repo.joinpath(*batch_relative.parts), batch)
    refresh_bundle_manifest(fixture)
    return fixture


def verify(fixture: AttestedFixture, *, now_utc: dt.datetime = NOW_UTC) -> None:
    verifier.verify_attested_bundle(
        fixture.ticket_path,
        fixture.bundle,
        repo_root=fixture.repo,
        now_utc=now_utc,
    )


def test_consistent_attested_bundle_passes(attested_bundle: AttestedFixture) -> None:
    verify(attested_bundle)


def test_expired_ticket_is_refused(attested_bundle: AttestedFixture) -> None:
    expired_at = dt.datetime(2030, 1, 11, 11, tzinfo=dt.timezone.utc)
    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle, now_utc=expired_at)
    assert str(caught.value) == (
        f"ticket check failed: generation ticket {TICKET_ID} expired at "
        "2030-01-11T11:00:00Z"
    )


def test_consumed_ticket_is_refused(attested_bundle: AttestedFixture) -> None:
    consumed = attested_bundle.repo.joinpath(*attested_bundle.batch_relative.parts)
    write_payload(consumed, {"already": "published"})
    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        f"ticket check failed: generation ticket {TICKET_ID} was already "
        f"consumed by {attested_bundle.batch_relative.as_posix()}"
    )


def test_superseded_ticket_is_refused(attested_bundle: AttestedFixture) -> None:
    successor_id = "2030-01-10-cafebabe"
    successor_relative = generation_tickets.ticket_record_path(successor_id)
    successor = copy.deepcopy(attested_bundle.ticket)
    successor.update(
        {
            "ticketId": successor_id,
            "nonce": "b" * 64,
            "mintedAtUtc": "2030-01-10T12:30:00Z",
            "expiresAtUtc": "2030-01-12T12:30:00Z",
            "attempt": 2,
            "supersedesTicketId": TICKET_ID,
            "supersededOutcome": {
                "outcome": "abandoned",
                "reason": "Synthetic retry fixture",
            },
        }
    )
    generation_tickets.validate_ticket(successor)
    write_payload(
        attested_bundle.repo.joinpath(*successor_relative.parts), successor
    )

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        f"ticket check failed: generation ticket {TICKET_ID} was superseded by "
        f"{successor_relative.as_posix()}"
    )


def test_wrong_batch_filename_is_refused(attested_bundle: AttestedFixture) -> None:
    old_path = attested_bundle.bundle.joinpath(
        "repo", *attested_bundle.batch_relative.parts
    )
    wrong_relative = attested_bundle.batch_relative.with_name("attested-wrong.json")
    wrong_path = attested_bundle.bundle.joinpath("repo", *wrong_relative.parts)
    old_path.rename(wrong_path)
    attested_bundle.batch_relative = wrong_relative
    refresh_bundle_manifest(attested_bundle)

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "bundle check failed: batch filename does not match generation ticket: "
        f"attested-wrong.json != attested-{TICKET_ID}.json"
    )


def test_wrong_batch_day_is_refused(attested_bundle: AttestedFixture) -> None:
    old_path = attested_bundle.bundle.joinpath(
        "repo", *attested_bundle.batch_relative.parts
    )
    wrong_relative = pathlib.PurePosixPath(
        "records/thesis-analyst/batches/2030-01-11"
    ) / attested_bundle.batch_relative.name
    wrong_path = attested_bundle.bundle.joinpath("repo", *wrong_relative.parts)
    wrong_path.parent.mkdir(parents=True)
    old_path.rename(wrong_path)
    attested_bundle.batch_relative = wrong_relative
    refresh_bundle_manifest(attested_bundle)

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "bundle check failed: batch path day does not match batch startedAt day: "
        "2030-01-11 != 2030-01-10"
    )


def test_policy_mismatch_is_refused(attested_bundle: AttestedFixture) -> None:
    rewrite_batch(
        attested_bundle,
        lambda batch: batch.__setitem__("codexModel", "gpt-tampered"),
    )
    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "policy check failed: batch codexModel does not match ticket policy: "
        "'gpt-tampered' != 'gpt-ticket-main'"
    )


def test_ticket_id_mismatch_is_refused(attested_bundle: AttestedFixture) -> None:
    def mutate(batch: dict[str, Any]) -> None:
        batch["generationTicket"]["ticketId"] = "2030-01-10-bad"

    rewrite_batch(attested_bundle, mutate)
    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "binding check failed: batch generationTicket does not match the ticket"
    )


def test_nonce_hash_mismatch_is_refused(attested_bundle: AttestedFixture) -> None:
    def mutate(manifest: dict[str, Any]) -> None:
        manifest["generationTicket"]["nonceSha256"] = "0" * 64

    rewrite_run_manifest(attested_bundle, mutate)
    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "binding check failed: run 0 generationTicket does not match ticket"
    )


def test_checkout_sha_mismatch_is_refused(attested_bundle: AttestedFixture) -> None:
    rewrite_run_manifest(
        attested_bundle,
        lambda manifest: manifest.__setitem__("checkoutSha", "f" * 40),
    )
    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "binding check failed: run 0 checkoutSha does not match ticket "
        f"introducing commit: {'f' * 40!r} != {attested_bundle.ticket_sha}"
    )


def test_prompt_hash_mismatch_is_refused(attested_bundle: AttestedFixture) -> None:
    def mutate(manifest: dict[str, Any]) -> None:
        prompt_ref = next(
            artifact
            for artifact in manifest["artifacts"]
            if artifact["artifactType"] == "prompt"
        )
        prompt_ref["sha256"] = "0" * 64

    rewrite_run_manifest(attested_bundle, mutate)
    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "prompt reconstruction check failed: run 0 artifact hash mismatch: prompt.md"
    )


def test_agent_metadata_tamper_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    cells_path = run_path(attested_bundle, "cells.with_activity.json")
    cells = json.loads(cells_path.read_text())
    cells[0]["model"] = "wrong-model"
    rewrite_run_artifact(
        attested_bundle,
        "cells.with_activity.json",
        (json.dumps(cells, indent=2) + "\n").encode(),
    )
    rewrite_run_manifest(
        attested_bundle,
        lambda manifest: manifest["agent"].__setitem__("model", "wrong-model"),
    )

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "prompt reconstruction check failed: run 0 agent metadata does not match "
        "trusted prompt metadata"
    )


def test_review_prompt_tamper_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    path = run_path(attested_bundle, "pre_submit_review_prompt.md")
    rewrite_run_artifact(
        attested_bundle,
        path.name,
        path.read_bytes() + b"\nTampered review instruction.\n",
    )

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "prompt reconstruction check failed: run 0 pre-submit review prompt bytes "
        "do not match trusted reconstruction"
    )


def test_missing_review_stream_artifact_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    filename = "pre_submit_review_codex_events.jsonl"
    run_path(attested_bundle, filename).unlink()

    def remove_ref(manifest: dict[str, Any]) -> None:
        expected = (attested_bundle.run_relative / filename).as_posix()
        manifest["artifacts"] = [
            artifact
            for artifact in manifest["artifacts"]
            if artifact.get("path") != expected
        ]

    rewrite_run_manifest(attested_bundle, remove_ref)

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "prompt reconstruction check failed: run 0 must declare exactly one "
        "pre_submit_review_codex_events.jsonl (codex_events_jsonl); found 0"
    )


def test_forbidden_argv_flag_is_refused(attested_bundle: AttestedFixture) -> None:
    path = run_path(attested_bundle, "command.json")
    command = json.loads(path.read_text())
    command["argv"].insert(1, "--response-file")
    rewrite_run_artifact(
        attested_bundle,
        "command.json",
        json.dumps(command, indent=2).encode(),
    )
    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "command shape check failed: run 0 command.json contains forbidden option "
        "--response-file"
    )


def test_command_timeout_policy_mismatch_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    path = run_path(attested_bundle, "command.json")
    command = json.loads(path.read_text())
    command["timeoutSeconds"] = 2
    rewrite_run_artifact(
        attested_bundle,
        path.name,
        json.dumps(command, indent=2).encode(),
    )

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "command shape check failed: run 0 command.json timeoutSeconds does not "
        "match policy"
    )


def test_boolean_command_timeout_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    path = run_path(attested_bundle, "command.json")
    command = json.loads(path.read_text())
    command["timeoutSeconds"] = True
    rewrite_run_artifact(
        attested_bundle,
        path.name,
        json.dumps(command, indent=2).encode(),
    )

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "command shape check failed: run 0 command.json timeoutSeconds does not "
        "match policy"
    )


def test_nonzero_effective_command_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    path = run_path(attested_bundle, "command.json")
    command = json.loads(path.read_text())
    command["returnCode"] = 124
    rewrite_run_artifact(
        attested_bundle,
        path.name,
        json.dumps(command, indent=2).encode(),
    )

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "command shape check failed: run 0 command.json did not complete "
        "successfully"
    )


def test_boolean_effective_command_code_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    path = run_path(attested_bundle, "command.json")
    command = json.loads(path.read_text())
    command["returnCode"] = False
    rewrite_run_artifact(
        attested_bundle,
        path.name,
        json.dumps(command, indent=2).encode(),
    )

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "command shape check failed: run 0 command.json did not complete "
        "successfully"
    )


def test_output_bearing_timeout_matches_runner_success_semantics(
    attested_bundle: AttestedFixture,
) -> None:
    command_path = run_path(attested_bundle, "command.json")
    command = json.loads(command_path.read_text())
    command.update(
        {
            "timedOut": True,
            "timeoutReason": "wall",
            "processReturnCode": -9,
            "terminatedAfterOutput": False,
        }
    )
    rewrite_run_artifact(
        attested_bundle,
        command_path.name,
        json.dumps(command, indent=2).encode(),
    )
    trace_path = run_path(attested_bundle, "codex_trace.json")
    trace = json.loads(trace_path.read_text())
    trace.update(
        {
            "timedOut": True,
            "timeoutReason": "wall",
            "processReturnCode": -9,
            "terminatedAfterOutput": False,
        }
    )
    rewrite_run_artifact(
        attested_bundle,
        trace_path.name,
        json.dumps(trace, indent=2).encode(),
    )
    manifest = json.loads(run_manifest_path(attested_bundle).read_text())
    cells_path = run_path(attested_bundle, "cells.with_activity.json")
    cells = json.loads(cells_path.read_text())
    cells[0]["activityLog"] = [
        artifact
        for artifact in manifest["artifacts"]
        if artifact.get("artifactType")
        not in {"cells_with_activity", "manifest"}
    ]
    rewrite_run_artifact(
        attested_bundle,
        cells_path.name,
        (json.dumps(cells, indent=2) + "\n").encode(),
    )

    verify(attested_bundle)


def test_read_only_command_workspace_guard_claim_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    path = run_path(attested_bundle, "draft_command.json")
    command = json.loads(path.read_text())
    command["workspaceMutations"] = ["tampered path"]
    rewrite_run_artifact(
        attested_bundle,
        path.name,
        json.dumps(command, indent=2).encode(),
    )

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "command shape check failed: run 0 draft_command.json records unexpected "
        "workspace guard output for the read-only sandbox"
    )


def test_codex_trace_replay_divergence_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    path = run_path(attested_bundle, "codex_trace.json")
    trace = json.loads(path.read_text())
    trace["eventCount"] = 99
    rewrite_run_artifact(
        attested_bundle,
        path.name,
        json.dumps(trace, indent=2).encode(),
    )

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "derivation replay check failed: run 0 codex_trace.json eventCount does "
        "not match the ticket runner"
    )


def test_raw_stream_replay_divergence_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    path = run_path(attested_bundle, "codex_stdout.jsonl")
    lines = path.read_text().splitlines()
    event = json.loads(lines[0])
    event["item"]["text"] = event["item"]["text"].replace(
        "Synthetic agency test rate", "Tampered synthetic rate"
    )
    tampered = "\n".join([json.dumps(event), lines[1]]) + "\n"
    rewrite_run_artifact(attested_bundle, "codex_stdout.jsonl", tampered.encode())

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "derivation replay check failed: run 0 last assistant message differs from "
        "codex_last_message.txt"
    )


def test_published_cells_replay_divergence_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    path = run_path(attested_bundle, "cells.with_activity.json")
    cells = json.loads(path.read_text())
    cells[0]["pointEstimate"] = 99
    rewrite_run_artifact(
        attested_bundle,
        "cells.with_activity.json",
        (json.dumps(cells, indent=2) + "\n").encode(),
    )

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "derivation replay check failed: run 0 published cells differ from "
        "replayed cells"
    )


def test_review_metadata_replay_divergence_is_refused(
    attested_bundle: AttestedFixture,
) -> None:
    cells_path = run_path(attested_bundle, "cells.with_activity.json")
    cells = json.loads(cells_path.read_text())
    cells[0]["preSubmitReview"]["summary"] = "Tampered review summary."
    rewrite_run_artifact(
        attested_bundle,
        cells_path.name,
        (json.dumps(cells, indent=2) + "\n").encode(),
    )
    rewrite_run_manifest(
        attested_bundle,
        lambda manifest: manifest["preSubmitReview"].__setitem__(
            "summary", "Tampered review summary."
        ),
    )

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "derivation replay check failed: run 0 preSubmitReview metadata differs "
        "from replay"
    )


def test_bundle_manifest_must_be_an_object(attested_bundle: AttestedFixture) -> None:
    write_payload(attested_bundle.bundle / "bundle_manifest.json", [])

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "bundle check failed: bundle manifest must be a JSON object"
    )


def test_invalid_utf8_batch_is_a_typed_refusal(
    attested_bundle: AttestedFixture,
) -> None:
    batch_path = attested_bundle.bundle.joinpath(
        "repo", *attested_bundle.batch_relative.parts
    )
    batch_path.write_bytes(b"\xff")
    refresh_bundle_manifest(attested_bundle)

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "bundle check failed: verification could not safely inspect untrusted input "
        "because it raised UnicodeDecodeError"
    )


def test_malformed_codex_event_is_a_typed_refusal(
    attested_bundle: AttestedFixture,
) -> None:
    malformed = json.dumps(
        {"type": "item.completed", "item": "not-an-object"}
    ).encode()
    rewrite_run_artifact(attested_bundle, "codex_stdout.jsonl", malformed)

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "derivation replay check failed: run 0 codex_stdout.jsonl could not be "
        "replayed: AttributeError"
    )


def test_nonnumeric_replayed_cell_is_a_typed_refusal(
    attested_bundle: AttestedFixture,
    tmp_path: pathlib.Path,
) -> None:
    cells = json.loads(run_path(attested_bundle, "parsed_cells.json").read_text())
    cells[0]["pointEstimate"] = "not-a-number"
    rewrite_final_response(attested_bundle, tmp_path, cells)

    with pytest.raises(verifier.AttestedBundleError) as caught:
        verify(attested_bundle)
    assert str(caught.value) == (
        "derivation replay check failed: verification could not safely inspect "
        "untrusted input because it raised ValueError"
    )
