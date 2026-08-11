from __future__ import annotations

import copy
import datetime as dt
import json
import pathlib
import re
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

import retry_batch_targets  # noqa: E402
from retry_batch_targets import (  # noqa: E402
    ORPHAN_GRACE_DAYS,
    RetrySelectionError,
    load_manifest,
    select_retry_targets,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent

REAL_MANIFEST = (
    ROOT
    / "records"
    / "thesis-analyst"
    / "batches"
    / "2026-08-07"
    / "auto-roll-31209278963-a1.json"
)

# Inside the 2026-08-07 batch's grace window; both recorded failures are
# retryable at this instant.
WITHIN_GRACE = dt.datetime(2026, 8, 10, 12, 0, tzinfo=dt.timezone.utc)
PAST_GRACE = dt.datetime(2026, 8, 15, 12, 0, tzinfo=dt.timezone.utc)


def real_manifest() -> dict:
    return load_manifest(REAL_MANIFEST)


def failed_row(manifest: dict) -> dict:
    return next(r for r in manifest["results"] if not r.get("ok"))


def test_grace_days_pins_the_site_constant() -> None:
    # The site enforces the same orphan window on every build; the two
    # constants must never drift apart. docket_publication's publication
    # gate pins the same number.
    source = (ROOT / "site" / "src" / "data" / "ledger-targets.ts").read_text()
    match = re.search(
        r"TARGET_PREREGISTRATION_ORPHAN_GRACE_DAYS\s*=\s*(\d+)", source
    )
    assert match, "site grace constant not found"
    assert int(match.group(1)) == ORPHAN_GRACE_DAYS

    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import docket_publication
    finally:
        sys.path.pop(0)
    assert docket_publication.ORPHAN_GRACE_DAYS == ORPHAN_GRACE_DAYS


def test_selects_exactly_the_recorded_failures_by_default() -> None:
    targets = select_retry_targets(
        real_manifest(), slugs=None, allow_succeeded=False, now_utc=WITHIN_GRACE
    )
    assert sorted(t["catalogSlug"] for t in targets) == [
        "us-dod-prime-award-obligations-fy2026",
        "us-dod-prime-contract-obligations-fy2026",
    ]
    for target in targets:
        assert target["targetRegistrationPath"].startswith("records/targets/")
        assert re.fullmatch(r"[0-9a-f]{64}", target["targetContentHash"])
        assert target["registeredAtUtc"] == "2026-08-07T17:54:06Z"
        assert target["registrationState"] == "preregistered"


def test_rebuilds_every_field_from_the_snapshot_not_the_manifest() -> None:
    # The trust property sol's round-1 review demanded: a tampered
    # manifest row cannot smuggle prompt- or validation-affecting fields
    # into the rerun. Forge every field the round-1 exploit used and
    # assert none of it survives — the rebuilt target equals the
    # snapshot-derived one exactly.
    manifest = real_manifest()
    row = failed_row(manifest)["target"]
    clean = retry_batch_targets.rebuild_target_from_snapshot(
        copy.deepcopy(row), label="clean"
    )

    forged = copy.deepcopy(row)
    forged["resolutionSource"] = "attacker"
    forged["resolutionSourceUrl"] = "https://evil.example/"
    forged["resolutionRule"] = "attacker rule"
    forged["resolutionPolicy"] = "attacker policy"
    forged["targetUnit"] = "attacker unit"
    forged["sourceBinding"] = {"adapter": "attacker"}
    rebuilt = retry_batch_targets.rebuild_target_from_snapshot(
        forged, label="forged"
    )
    assert rebuilt == clean
    assert rebuilt["sourceBinding"]["adapter"] != "attacker"
    assert "resolutionSource" not in rebuilt


def test_unreconstructable_row_context_is_refused_not_stripped() -> None:
    manifest = real_manifest()
    for key, value in (
        ("comparisonTarget", True),
        ("anchors", {"2024": 1.0}),
        ("previousTarget", {"dataPointId": "x"}),
        ("expectedReleaseDate", "2026-09-01"),
    ):
        forged = copy.deepcopy(failed_row(manifest)["target"])
        forged[key] = value
        with pytest.raises(RetrySelectionError, match="cannot .*reconstruct|carries"):
            retry_batch_targets.rebuild_target_from_snapshot(
                forged, label=f"forged-{key}"
            )


def test_ticketed_manifests_are_refused(tmp_path: pathlib.Path) -> None:
    data = json.loads(REAL_MANIFEST.read_text())
    data["generationTicket"] = {"ticketId": "t"}
    batches = tmp_path / "records" / "thesis-analyst" / "batches" / "2026-08-07"
    batches.mkdir(parents=True)
    path = batches / "ticketed.json"
    path.write_text(json.dumps(data))
    import pytest as _pytest

    with _pytest.MonkeyPatch.context() as mp:
        mp.setattr(retry_batch_targets, "ROOT", tmp_path)
        with pytest.raises(RetrySelectionError, match="attested local lane"):
            load_manifest(path)


def test_bounded_contracts_are_refused(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Build a fake tree whose snapshot is a resolve-by-bound contract and
    # confirm the selector refuses to cross the lane boundary.
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from register_targets import registration_content_hash
    finally:
        sys.path.pop(0)

    manifest = real_manifest()
    row = copy.deepcopy(failed_row(manifest)["target"])
    real_snapshot = json.loads(
        (ROOT / row["targetRegistrationPath"]).read_text()
    )
    bounded = copy.deepcopy(real_snapshot)
    contract = bounded["targets"][0]
    contract["resolutionDateBasis"] = "resolve-by-bound"
    contract["resolutionDate"] = contract["sourceBinding"][
        "expectedReleaseWindow"
    ]["end"]
    new_hash = registration_content_hash(bounded)

    fake_root = tmp_path
    reg_dir = fake_root / "records" / "targets"
    reg_dir.mkdir(parents=True)
    reg_name = f"2026-08-07-{new_hash}.json"
    (reg_dir / reg_name).write_text(json.dumps(bounded))
    row["targetRegistrationPath"] = f"records/targets/{reg_name}"
    row["targetContentHash"] = new_hash

    monkeypatch.setattr(retry_batch_targets, "ROOT", fake_root)
    with pytest.raises(RetrySelectionError, match="attested generation-ticket lane"):
        retry_batch_targets.rebuild_target_from_snapshot(row, label="bounded")


def test_unknown_contract_fields_are_refused(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from register_targets import registration_content_hash
    finally:
        sys.path.pop(0)

    manifest = real_manifest()
    row = copy.deepcopy(failed_row(manifest)["target"])
    snapshot = json.loads((ROOT / row["targetRegistrationPath"]).read_text())
    snapshot["targets"][0]["novelField"] = 1
    new_hash = registration_content_hash(snapshot)

    reg_dir = tmp_path / "records" / "targets"
    reg_dir.mkdir(parents=True)
    reg_name = f"2026-08-07-{new_hash}.json"
    (reg_dir / reg_name).write_text(json.dumps(snapshot))
    row["targetRegistrationPath"] = f"records/targets/{reg_name}"
    row["targetContentHash"] = new_hash

    monkeypatch.setattr(retry_batch_targets, "ROOT", tmp_path)
    with pytest.raises(RetrySelectionError, match="unknown field"):
        retry_batch_targets.rebuild_target_from_snapshot(row, label="novel")


def test_snapshot_bytes_must_hash_to_the_recorded_content_hash(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Real content hashing, not filename theater: tamper with the
    # snapshot bytes while keeping the filename and manifest hash, and
    # the selector must refuse.
    manifest = real_manifest()
    row = copy.deepcopy(failed_row(manifest)["target"])
    snapshot = json.loads((ROOT / row["targetRegistrationPath"]).read_text())
    snapshot["targets"][0]["valueScale"] = 999.0

    reg_dir = tmp_path / "records" / "targets"
    reg_dir.mkdir(parents=True)
    reg_name = pathlib.PurePosixPath(row["targetRegistrationPath"]).name
    (reg_dir / reg_name).write_text(json.dumps(snapshot))

    monkeypatch.setattr(retry_batch_targets, "ROOT", tmp_path)
    with pytest.raises(RetrySelectionError, match="snapshot bytes hash"):
        retry_batch_targets.rebuild_target_from_snapshot(row, label="tampered")


def test_refuses_every_target_past_its_grace_window() -> None:
    with pytest.raises(RetrySelectionError, match="expired-unforecast ratchet"):
        select_retry_targets(
            real_manifest(), slugs=None, allow_succeeded=False, now_utc=PAST_GRACE
        )


def test_refuses_future_registration_instants() -> None:
    before_registration = dt.datetime(2026, 8, 7, 0, 0, tzinfo=dt.timezone.utc)
    with pytest.raises(RetrySelectionError, match="future registration"):
        select_retry_targets(
            real_manifest(),
            slugs=None,
            allow_succeeded=False,
            now_utc=before_registration,
        )


def test_succeeded_slug_requires_explicit_override() -> None:
    ok_slug = "us-dod-new-prime-awards-fy2026"
    with pytest.raises(RetrySelectionError, match="succeeded in the recorded run"):
        select_retry_targets(
            real_manifest(),
            slugs=[ok_slug],
            allow_succeeded=False,
            now_utc=WITHIN_GRACE,
        )
    targets = select_retry_targets(
        real_manifest(), slugs=[ok_slug], allow_succeeded=True, now_utc=WITHIN_GRACE
    )
    assert [t["catalogSlug"] for t in targets] == [ok_slug]


def test_unknown_slug_is_refused() -> None:
    with pytest.raises(RetrySelectionError, match="not in this batch manifest"):
        select_retry_targets(
            real_manifest(),
            slugs=["no-such-slug"],
            allow_succeeded=False,
            now_utc=WITHIN_GRACE,
        )


def test_manifest_must_live_under_the_committed_batches_tree(
    tmp_path: pathlib.Path,
) -> None:
    stray = tmp_path / "manifest.json"
    stray.write_text(json.dumps({"schemaVersion": "thesis_batch_manifest_v1"}))
    with pytest.raises(RetrySelectionError, match="records/thesis-analyst/batches"):
        load_manifest(stray)


def test_rejects_wrong_schema(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real = json.loads(REAL_MANIFEST.read_text())
    batches = tmp_path / "records" / "thesis-analyst" / "batches" / "2026-08-07"
    batches.mkdir(parents=True)
    monkeypatch.setattr(retry_batch_targets, "ROOT", tmp_path)

    wrong_schema = copy.deepcopy(real)
    wrong_schema["schemaVersion"] = "thesis_batch_manifest_v0"
    path = batches / "wrong-schema.json"
    path.write_text(json.dumps(wrong_schema))
    with pytest.raises(RetrySelectionError, match="schemaVersion"):
        load_manifest(path)


def test_missing_snapshot_is_refused(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real = json.loads(REAL_MANIFEST.read_text())
    batches = tmp_path / "records" / "thesis-analyst" / "batches" / "2026-08-07"
    batches.mkdir(parents=True)
    path = batches / "missing-snapshot.json"
    path.write_text(json.dumps(real))
    monkeypatch.setattr(retry_batch_targets, "ROOT", tmp_path)
    manifest = load_manifest(path)
    with pytest.raises(RetrySelectionError, match="snapshot missing"):
        select_retry_targets(
            manifest, slugs=None, allow_succeeded=False, now_utc=WITHIN_GRACE
        )


def test_publication_grace_gate_refuses_late_runs() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import docket_publication
    finally:
        sys.path.pop(0)

    target = {"registeredAtUtc": "2026-08-07T17:54:06Z"}
    deadline = dt.datetime(2026, 8, 14, 17, 54, 6, tzinfo=dt.timezone.utc)
    in_grace_start = deadline - dt.timedelta(hours=2)
    late_start = deadline + dt.timedelta(seconds=1)

    docket_publication.require_run_within_grace(
        target, in_grace_start, [{"runAt": "2026-08-14T17:00:00Z"}]
    )
    with pytest.raises(
        docket_publication.PublicationError, match="orphan grace deadline"
    ):
        docket_publication.require_run_within_grace(target, late_start, [])
    with pytest.raises(
        docket_publication.PublicationError, match="sealed after"
    ):
        docket_publication.require_run_within_grace(
            target, in_grace_start, [{"runAt": "2026-08-14T17:54:06Z"}]
        )
    # The gate is wired into validate_run_binding behind the flag.
    import inspect

    binding_source = inspect.getsource(docket_publication.validate_run_binding)
    assert "require_run_within_grace" in binding_source
    assert "enforce_run_grace" in binding_source


def test_output_envelope_matches_the_roll_selector(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "roll-targets.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "retry_batch_targets.py",
            "--batch",
            str(REAL_MANIFEST),
            "--out",
            str(out),
            "--now-utc",
            WITHIN_GRACE.isoformat().replace("+00:00", "Z"),
        ],
    )
    assert retry_batch_targets.main() == 0
    raw = out.read_text()
    payload = json.loads(raw)
    assert set(payload) == {"targets"}
    assert raw == json.dumps(payload, indent=1) + "\n"
    assert len(payload["targets"]) == 2
