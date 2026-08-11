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
        ("previousTarget", {"dataPointId": "x"}),
        ("expectedReleaseDate", "2026-09-01"),
    ):
        forged = copy.deepcopy(failed_row(manifest)["target"])
        forged[key] = value
        with pytest.raises(RetrySelectionError, match="cannot .*reconstruct|carries"):
            retry_batch_targets.rebuild_target_from_snapshot(
                forged, label=f"forged-{key}"
            )


B1_MANIFEST = (
    ROOT
    / "records"
    / "thesis-analyst"
    / "batches"
    / "2026-08-11"
    / "auto-roll-31533876109-a1.json"
)
B1_WITHIN_GRACE = dt.datetime(2026, 8, 12, 12, 0, tzinfo=dt.timezone.utc)


def test_anchored_targets_reconstruct_with_docket_anchors() -> None:
    # The 2026-08-11 B1 batch's failed targets carry anchors — the shape
    # the first live retry refused. Anchors now reconstruct from the
    # committed docket entry (never the manifest row), so the retry
    # emits them equal to the docket's extras.anchors.
    manifest = load_manifest(B1_MANIFEST)
    targets = select_retry_targets(
        manifest, slugs=None, allow_succeeded=False, now_utc=B1_WITHIN_GRACE
    )
    assert len(targets) == 3
    docket = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    by_series = {row.get("series"): row for row in docket["series"]}
    for target in targets:
        expected = by_series[target["series"]]["extras"]["anchors"]
        assert target["anchors"] == expected


def test_bind_refuses_stale_or_absent_anchors(tmp_path: pathlib.Path) -> None:
    # The round-four TOCTOU: selection reads the docket before the sync
    # rebase, so binding must independently authenticate anchors against
    # the committed docket at ITS head — presence and value. A tampered
    # value and a stripped anchor must both fail the bind closed.
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import register_targets
    finally:
        sys.path.pop(0)

    manifest = load_manifest(B1_MANIFEST)
    targets = select_retry_targets(
        manifest, slugs=None, allow_succeeded=False, now_utc=B1_WITHIN_GRACE
    )

    good = tmp_path / "good.json"
    good.write_text(json.dumps({"targets": targets}, indent=1) + "\n")
    bound = register_targets.bind_registration_commits(good, "HEAD")
    assert len(bound["targets"]) == 3

    tampered = copy.deepcopy(targets)
    tampered[0]["anchors"] = {"2025": 999.0}
    bad_value = tmp_path / "bad-value.json"
    bad_value.write_text(json.dumps({"targets": tampered}, indent=1) + "\n")
    with pytest.raises(
        register_targets.RegistrationError,
        match="anchors disagree with the committed docket",
    ):
        register_targets.bind_registration_commits(bad_value, "HEAD")

    stripped = copy.deepcopy(targets)
    del stripped[0]["anchors"]
    bad_absent = tmp_path / "bad-absent.json"
    bad_absent.write_text(json.dumps({"targets": stripped}, indent=1) + "\n")
    with pytest.raises(
        register_targets.RegistrationError,
        match="anchors disagree with the committed docket",
    ):
        register_targets.bind_registration_commits(bad_absent, "HEAD")


def test_row_anchors_disagreeing_with_the_docket_are_refused() -> None:
    manifest = load_manifest(B1_MANIFEST)
    forged = copy.deepcopy(failed_row(manifest)["target"])
    forged["anchors"] = {"2025": 999.0}
    with pytest.raises(RetrySelectionError, match="disagree with the committed docket"):
        retry_batch_targets.rebuild_target_from_snapshot(
            forged, label="forged-anchors"
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


def test_select_output_is_immune_to_forged_manifest_rows() -> None:
    # Mutation pin for the reconstruction boundary at the SELECT level: if
    # a future edit re-merges manifest-row fields after reconstruction,
    # forged rows would leak into the output and this equality breaks.
    clean = select_retry_targets(
        real_manifest(), slugs=None, allow_succeeded=False, now_utc=WITHIN_GRACE
    )
    forged_manifest = real_manifest()
    for result in forged_manifest["results"]:
        if not result.get("ok"):
            result["target"]["resolutionSource"] = "attacker"
            result["target"]["resolutionRule"] = "attacker rule"
            result["target"]["targetUnit"] = "attacker unit"
    forged = select_retry_targets(
        forged_manifest, slugs=None, allow_succeeded=False, now_utc=WITHIN_GRACE
    )
    assert forged == clean


def _fake_pair_tree(tmp_path: pathlib.Path) -> tuple[dict, str, str]:
    # Derive two conditional-arm registrations from a real committed
    # snapshot so the fixture inherits the live schema and ledger-pin
    # shape; only the contract's identity and conditional fields change.
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from register_targets import registration_content_hash
    finally:
        sys.path.pop(0)

    base_row = failed_row(real_manifest())["target"]
    base_snapshot = json.loads(
        (ROOT / base_row["targetRegistrationPath"]).read_text()
    )
    registered_at = base_snapshot["registeredAtUtc"]

    reg_dir = tmp_path / "records" / "targets"
    reg_dir.mkdir(parents=True)
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir(parents=True)
    (scripts_dir / "docket_series.json").write_text(
        json.dumps({"series": []})
    )
    rows = []
    slugs = []
    for cond_id in ("enacted", "current-law"):
        slug = f"test-pair-{cond_id}"
        snapshot = copy.deepcopy(base_snapshot)
        contract = snapshot["targets"][0]
        contract["series"] = "test.pair.series"
        contract["period"] = "2027-09"
        contract["catalogSlug"] = slug
        contract["dataPointId"] = (
            f"test.pair.series.2027_09.first_print.{cond_id.replace('-', '_')}"
        )
        contract["conditional"] = f"condition {cond_id} holds"
        contract["conditionId"] = f"cond.test.{cond_id}"
        contract["conditionDeadline"] = "2027-09-30"
        content_hash = registration_content_hash(snapshot)
        name = f"2026-08-07-{content_hash}.json"
        (reg_dir / name).write_text(json.dumps(snapshot))
        rows.append(
            {
                "ok": False,
                "target": {
                    "catalogSlug": slug,
                    "targetRegistrationPath": f"records/targets/{name}",
                    "targetContentHash": content_hash,
                    "registeredAtUtc": registered_at,
                },
            }
        )
        slugs.append(slug)
    manifest = {
        "schemaVersion": "thesis_batch_manifest_v1",
        "results": rows,
    }
    return manifest, slugs[0], slugs[1]


def test_narrowing_to_one_unpublished_pair_arm_is_refused(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest, arm_a, arm_b = _fake_pair_tree(tmp_path)
    monkeypatch.setattr(retry_batch_targets, "ROOT", tmp_path)
    with pytest.raises(RetrySelectionError, match="retry together or not at all"):
        select_retry_targets(
            manifest, slugs=[arm_a], allow_succeeded=False, now_utc=WITHIN_GRACE
        )
    # Both arms together: fine (and the default failed-set selection
    # naturally includes both).
    both = select_retry_targets(
        manifest,
        slugs=[arm_a, arm_b],
        allow_succeeded=False,
        now_utc=WITHIN_GRACE,
    )
    assert sorted(t["catalogSlug"] for t in both) == sorted([arm_a, arm_b])
    default = select_retry_targets(
        manifest, slugs=None, allow_succeeded=False, now_utc=WITHIN_GRACE
    )
    assert sorted(t["catalogSlug"] for t in default) == sorted([arm_a, arm_b])


def test_lone_failed_arm_with_published_sibling_is_retryable(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest, arm_a, arm_b = _fake_pair_tree(tmp_path)
    for row in manifest["results"]:
        if row["target"]["catalogSlug"] == arm_b:
            row["ok"] = True
    monkeypatch.setattr(retry_batch_targets, "ROOT", tmp_path)
    targets = select_retry_targets(
        manifest, slugs=None, allow_succeeded=False, now_utc=WITHIN_GRACE
    )
    assert [t["catalogSlug"] for t in targets] == [arm_a]
    assert targets[0]["conditional"] == "condition enacted holds"
    # The conditional identity fields survive projection intact.
    assert targets[0]["conditionId"] == "cond.test.enacted"
    assert targets[0]["conditionDeadline"] == "2027-09-30"


def test_sibling_snapshot_substitution_is_refused(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Round-3 attack: keep sibling B's slug and ok:false but point its
    # row at a valid, hash-consistent, UNRELATED unconditional
    # registration — the pair scan must refuse the row rather than
    # conclude no conditional sibling exists.
    manifest, arm_a, arm_b = _fake_pair_tree(tmp_path)
    base_row = failed_row(real_manifest())["target"]
    unrelated_snapshot = json.loads(
        (ROOT / base_row["targetRegistrationPath"]).read_text()
    )
    reg_dir = tmp_path / "records" / "targets"
    name = pathlib.PurePosixPath(base_row["targetRegistrationPath"]).name
    (reg_dir / name).write_text(json.dumps(unrelated_snapshot))
    for row in manifest["results"]:
        if row["target"]["catalogSlug"] == arm_b:
            row["target"]["targetRegistrationPath"] = f"records/targets/{name}"
            row["target"]["targetContentHash"] = base_row["targetContentHash"]
            row["target"]["registeredAtUtc"] = unrelated_snapshot[
                "registeredAtUtc"
            ]
    monkeypatch.setattr(retry_batch_targets, "ROOT", tmp_path)
    with pytest.raises(RetrySelectionError, match="not the manifest row's slug"):
        select_retry_targets(
            manifest, slugs=[arm_a], allow_succeeded=False, now_utc=WITHIN_GRACE
        )


def test_recorded_outcomes_must_be_booleans() -> None:
    manifest = real_manifest()
    failed_row(manifest)["ok"] = "false"
    with pytest.raises(RetrySelectionError, match="boolean recorded outcome"):
        select_retry_targets(
            manifest, slugs=None, allow_succeeded=False, now_utc=WITHIN_GRACE
        )


def test_validate_cells_forwards_the_grace_flag(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Mutation pin for the middle hop the round-3 review flagged:
    # deleting the enforce_run_grace forwarding at the
    # validate_cells → validate_run_binding call must fail here.
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import docket_publication
        import verify_custody
    finally:
        sys.path.pop(0)

    day = "2026-08-07"
    run_dir_name = f"{day}t18-00-00z-test-slug"
    batch_rel = f"records/thesis-analyst/batches/{day}/hop-pin.json"
    manifest_rel = f"records/thesis-analyst/{day}/{run_dir_name}/manifest.json"
    (tmp_path / batch_rel).parent.mkdir(parents=True)
    (tmp_path / manifest_rel).parent.mkdir(parents=True)
    (tmp_path / batch_rel).write_text(
        json.dumps(
            {
                "schemaVersion": "thesis_batch_manifest_v1",
                "promptMode": "fast",
                "startedAt": f"{day}T17:55:00Z",
                "finishedAt": f"{day}T19:00:00Z",
                "results": [
                    {
                        "ok": False,
                        "startedAt": f"{day}T17:56:00Z",
                        "finishedAt": f"{day}T18:30:00Z",
                        "target": {"catalogSlug": "test-slug"},
                        "manifestPath": manifest_rel,
                        "cellsPath": None,
                    }
                ],
            }
        )
    )
    (tmp_path / manifest_rel).write_text(
        json.dumps({"ok": False, "cellsPath": None})
    )

    captured: dict = {}

    def capture_binding(repo, result, manifest, cells, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(
        docket_publication, "validate_run_binding", capture_binding
    )
    monkeypatch.setattr(
        docket_publication, "validate_run_file_inventory", lambda *a, **k: None
    )
    monkeypatch.setattr(verify_custody, "verify_run", lambda *a, **k: None)

    for flag in (True, False):
        captured.clear()
        docket_publication.validate_cells(
            tmp_path,
            batch_rel,
            require_git_binding=False,
            enforce_run_grace=flag,
        )
        assert captured.get("enforce_run_grace") is flag


def test_workflow_wires_the_retry_grace_flag() -> None:
    # Coarse but real: the publish step must pass --enforce-run-grace in
    # retry mode and bind the retry input through env, and the register
    # job must skip adoption and both registration write steps.
    workflow = (ROOT / ".github" / "workflows" / "roll-docket.yml").read_text()
    # Match the executable line, not prose: a comment mentioning the flag
    # must not satisfy this pin.
    assert 'args+=(--enforce-run-grace)' in workflow
    assert workflow.count("RETRY_BATCH: ${{ github.event.inputs.retry_batch }}") >= 2
    assert (
        workflow.count("github.event.inputs.retry_batch == ''") >= 3
    ), "adoption + both registration write steps must skip in retry mode"


def test_final_push_loops_rebind_after_every_rebase() -> None:
    # The round-four publication TOCTOU: the final push loop rebases
    # again after the initial publish bind, so it must re-run the full
    # registration binding at the rebased HEAD and require the identical
    # registration set. Executable-line pins for both docket workflows.
    for name, targets_file in (
        ("roll-docket.yml", "roll-targets.json"),
        ("prospect-docket.yml", "prospect-targets.json"),
    ):
        workflow = (ROOT / ".github" / "workflows" / name).read_text()
        final_push = workflow.split("Rebase, reverify, and push once", 1)[1]
        assert "--bind-registration-commits" in final_push, name
        assert targets_file in final_push, name
        assert (
            'test "$FINAL_SET_HASH" = "$EXPECTED_SET_HASH"' in final_push
        ), name
        assert (
            "EXPECTED_SET_HASH: ${{ needs.register.outputs.registration_set_hash }}"
            in workflow.split("Rebase, reverify, and push once", 1)[0]
            or "EXPECTED_SET_HASH: ${{ needs.register.outputs.registration_set_hash }}"
            in workflow
        ), name


def test_seed_contracts_reconstruct_with_their_seed_period() -> None:
    # Ordinary release-calendar seeds carry seedPeriod in the contract and
    # the sync bind compares it; the projection must emit it.
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import register_targets
    finally:
        sys.path.pop(0)
    seed_path = ROOT / (
        "records/targets/"
        "2026-07-26-270b7d2d593a239ac3373efdb5ec9fa3809df3e9eb60f5b3e1bc8120e239921b.json"
    )
    snapshot = json.loads(seed_path.read_text())
    contract = snapshot["targets"][0]
    assert "seedPeriod" in contract, "fixture registration is no longer a seed"
    assert set(contract) <= retry_batch_targets.KNOWN_CONTRACT_KEYS
    rebuilt = register_targets.rebuild_registered_target(
        snapshot, path=seed_path
    )
    assert rebuilt["seedPeriod"] == contract["seedPeriod"]
    assert rebuilt["registeredAtUtc"] == snapshot["registeredAtUtc"]


def test_enforce_run_grace_cli_flag_reaches_the_binding_check(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import docket_publication
    finally:
        sys.path.pop(0)

    # CLI: the flag parses.
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "docket_publication.py",
            "validate",
            "--bundle-dir",
            str(tmp_path),
            "--batch",
            "records/thesis-analyst/batches/2026-08-07/x.json",
            "--enforce-run-grace",
        ],
    )
    args = docket_publication.parse_args()
    assert args.enforce_run_grace is True

    # validate() forwards it into validate_cells.
    captured: dict = {}

    def fake_load_bundle(bundle, batch, trusted):
        return tmp_path, {"schemaVersion": "x"}

    def fake_validate_cells(repo, batch, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(docket_publication, "load_bundle", fake_load_bundle)
    monkeypatch.setattr(docket_publication, "validate_cells", fake_validate_cells)
    monkeypatch.setattr(
        docket_publication, "validate_batch_path", lambda batch: batch
    )
    args.apply = False
    args.allow_published_wave = False
    args.trusted_targets = "trusted.json"
    args.publish_validated_at_utc = None
    docket_publication.validate(args)
    assert captured.get("enforce_run_grace") is True

    # The real validate_run_binding enforces it before any git-bound
    # work: a grace-late run manifest dies at the grace check with the
    # flag on, and passes that point (failing later, differently) with
    # it off.
    target = {
        "registeredAtUtc": "2026-08-07T17:54:06Z",
        "series": "s",
        "period": "p",
    }
    late_manifest = {
        "schemaVersion": "thesis_analyst_run_manifest_v1",
        "targetContext": target,
        "runStartedAt": "2026-08-20T00:00:00Z",
        "createdAt": "2026-08-20T00:00:00Z",
        "series": "s",
        "period": "p",
        "conditional": None,
    }
    result = {"target": target, "manifestPath": "bad"}
    with pytest.raises(
        docket_publication.PublicationError, match="orphan grace deadline"
    ):
        docket_publication.validate_run_binding(
            tmp_path,
            result,
            late_manifest,
            [],
            require_git_binding=True,
            enforce_run_grace=True,
        )
    with pytest.raises(docket_publication.PublicationError) as excinfo:
        docket_publication.validate_run_binding(
            tmp_path,
            result,
            late_manifest,
            [],
            require_git_binding=True,
            enforce_run_grace=False,
        )
    assert "orphan grace deadline" not in str(excinfo.value)

    # A run that STARTED in grace but sealed a cell after the deadline is
    # refused through the same real path — replacing the cells argument
    # with [] at the grace call would let this pass.
    in_grace_manifest = dict(
        late_manifest,
        runStartedAt="2026-08-14T17:00:00Z",
        createdAt="2026-08-14T17:00:00Z",
    )
    late_cell = [{"runAt": "2026-08-14T17:54:06Z"}]
    with pytest.raises(
        docket_publication.PublicationError, match="sealed after"
    ):
        docket_publication.validate_run_binding(
            tmp_path,
            result,
            in_grace_manifest,
            late_cell,
            require_git_binding=True,
            enforce_run_grace=True,
        )


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
