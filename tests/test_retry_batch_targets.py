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


def test_grace_days_pins_the_site_constant() -> None:
    # The site enforces the same orphan window on every build; the two
    # constants must never drift apart.
    source = (ROOT / "site" / "src" / "data" / "ledger-targets.ts").read_text()
    match = re.search(
        r"TARGET_PREREGISTRATION_ORPHAN_GRACE_DAYS\s*=\s*(\d+)", source
    )
    assert match, "site grace constant not found"
    assert int(match.group(1)) == ORPHAN_GRACE_DAYS


def test_selects_exactly_the_recorded_failures_by_default() -> None:
    manifest = load_manifest(REAL_MANIFEST)
    targets = select_retry_targets(
        manifest, slugs=None, allow_succeeded=False, now_utc=WITHIN_GRACE
    )
    assert sorted(t["catalogSlug"] for t in targets) == [
        "us-dod-prime-award-obligations-fy2026",
        "us-dod-prime-contract-obligations-fy2026",
    ]
    for target in targets:
        # The reconstructed dicts are the exact committed batch targets:
        # registration path + content hash intact, so the workflow's
        # --reuse-existing-only and bind passes verify them unchanged.
        assert target["targetRegistrationPath"].startswith("records/targets/")
        assert re.fullmatch(r"[0-9a-f]{64}", target["targetContentHash"])
        assert target["registeredAtUtc"] == "2026-08-07T17:54:06Z"


def test_refuses_every_target_past_its_grace_window() -> None:
    manifest = load_manifest(REAL_MANIFEST)
    with pytest.raises(RetrySelectionError, match="expired-unforecast ratchet"):
        select_retry_targets(
            manifest, slugs=None, allow_succeeded=False, now_utc=PAST_GRACE
        )


def test_succeeded_slug_requires_explicit_override() -> None:
    manifest = load_manifest(REAL_MANIFEST)
    ok_slug = "us-dod-new-prime-awards-fy2026"
    with pytest.raises(RetrySelectionError, match="succeeded in the recorded run"):
        select_retry_targets(
            manifest,
            slugs=[ok_slug],
            allow_succeeded=False,
            now_utc=WITHIN_GRACE,
        )
    targets = select_retry_targets(
        manifest, slugs=[ok_slug], allow_succeeded=True, now_utc=WITHIN_GRACE
    )
    assert [t["catalogSlug"] for t in targets] == [ok_slug]


def test_unknown_slug_is_refused() -> None:
    manifest = load_manifest(REAL_MANIFEST)
    with pytest.raises(RetrySelectionError, match="not in this batch manifest"):
        select_retry_targets(
            manifest,
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


def test_rejects_wrong_schema_and_tampered_hash(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real = json.loads(REAL_MANIFEST.read_text())

    fake_root = tmp_path
    batches = fake_root / "records" / "thesis-analyst" / "batches" / "2026-08-07"
    batches.mkdir(parents=True)
    monkeypatch.setattr(retry_batch_targets, "ROOT", fake_root)

    wrong_schema = copy.deepcopy(real)
    wrong_schema["schemaVersion"] = "thesis_batch_manifest_v0"
    path = batches / "wrong-schema.json"
    path.write_text(json.dumps(wrong_schema))
    with pytest.raises(RetrySelectionError, match="schemaVersion"):
        load_manifest(path)

    # A manifest whose failed target names a snapshot absent from the
    # tree must be refused — the manifest is committed, but the selector
    # still proves the registration is really present before rerunning.
    missing_snapshot = copy.deepcopy(real)
    path = batches / "missing-snapshot.json"
    path.write_text(json.dumps(missing_snapshot))
    manifest = load_manifest(path)
    with pytest.raises(RetrySelectionError, match="snapshot missing"):
        select_retry_targets(
            manifest, slugs=None, allow_succeeded=False, now_utc=WITHIN_GRACE
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
    # Byte-shape parity with scripts/roll_docket.py's writer:
    # json.dumps({"targets": …}, indent=1) + "\n".
    payload = json.loads(raw)
    assert set(payload) == {"targets"}
    assert raw == json.dumps(payload, indent=1) + "\n"
    assert len(payload["targets"]) == 2
