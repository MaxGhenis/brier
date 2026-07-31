"""Selection rules for the awaiting-forecast retry lane.

The lane's entire safety argument is that it cannot mint a registration: every
emitted target is rebuilt from the committed docket registry and re-derived
through ``register_targets.build_contract``, and anything that does not come
back byte-identical to the canonical snapshot is dropped rather than forecast.
These tests fabricate a complete registration world in ``tmp_path`` — registry,
canonical snapshot, generated ledger, expired list — using the production
helpers that build the real ones, so a fixture cannot drift into agreeing with
a rule that no longer exists.
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import awaiting_forecast_targets as awaiting  # noqa: E402
import register_targets as registration  # noqa: E402
from canonical_json import canonical_bytes  # noqa: E402

REGISTERED_AT = "2026-07-31T12:00:00Z"
REGISTRATION_DATE = dt.date(2026, 7, 31)
TODAY = dt.date(2026, 8, 1)

LEDGER_PIN = {
    "repo": "PolicyEngine/ledger",
    "branch": "codex/thesis-ledger-facts",
    "sha": "a" * 40,
    "jsonlSha256": "b" * 64,
    "lineCount": 4096,
}


def registry_entry(release_date: str = "2026-09-15") -> dict:
    """A committed docket registry entry with a future official date."""
    return {
        "series": "fixture.series",
        "cadence": "monthly",
        "slug": "fixture-{month}-{year}",
        "extras": {
            "targetUnit": "percent",
            "expectedReleaseDate": release_date,
            "sourceBinding": {
                "adapter": "alfred-fred",
                "sourceUrl": "https://api.stlouisfed.org/fred/series/observations",
                "sourceSeriesId": "FIXTURE",
                "field": "FIXTURE",
                "table": "Fixture release",
                "transform": {"operation": "identity", "factor": 1},
                "releasePolicy": "first_print",
            },
        },
    }


def rolled_target(entry: dict, period: str = "2026-08") -> dict:
    """The raw target the roll would have emitted for ``entry``/``period``."""
    import roll_docket as roll

    return {
        "series": entry["series"],
        "period": period,
        "catalogSlug": roll.format_slug(entry["slug"], period, entry["cadence"]),
        **roll.target_extras_for_period(entry, period),
    }


class Lane:
    """A writable stand-in for the four files the selector reads."""

    def __init__(self, root: pathlib.Path) -> None:
        self.root = root
        self.registry_path = root / "scripts" / "docket_series.json"
        self.generated_path = root / "site" / "src" / "data" / "gen.ts"
        self.expired_path = root / "site" / "src" / "data" / "expired.ts"
        self.snapshots = root / "records" / "targets"
        for path in (self.registry_path, self.generated_path, self.snapshots):
            path.parent.mkdir(parents=True, exist_ok=True)
        self.snapshots.mkdir(parents=True, exist_ok=True)
        self.entries: list[str] = []
        self.write_registry([])
        self.write_expired([])

    def write_registry(self, series: list[dict]) -> None:
        self.registry_path.write_text(json.dumps({"series": series}, indent=2))

    def write_expired(self, ids: list[str]) -> None:
        body = "\n".join(f'  "{value}",' for value in ids)
        self.expired_path.write_text(
            "export const EXPIRED_UNFORECAST_REGISTRATIONS = [\n"
            f"{body}\n"
            "] as const;\n"
        )

    def write_generated(self) -> None:
        body = "\n".join(self.entries)
        self.generated_path.write_text(
            "export const GENERATED_FORECAST_TARGETS = [\n"
            f"{body}\n"
            "] satisfies GeneratedTarget[];\n"
        )

    def register(
        self,
        target: dict,
        *,
        registered_at: str = REGISTERED_AT,
        registration_date: dt.date = REGISTRATION_DATE,
        state: str = "preregistered",
        overrides: dict | None = None,
    ) -> dict:
        """Preregister ``target`` exactly as the privileged register leg does.

        Returns the canonical contract. ``overrides`` corrupts only the
        generated-ledger block, leaving the snapshot canonical — the shape of
        a tampered or stale ledger.
        """
        snapshot = registration.build_snapshot(
            [target],
            registration_date,
            registered_at_utc=registered_at,
            ledger_pin=LEDGER_PIN,
        )
        content_hash = registration.registration_content_hash(snapshot)
        path = self.snapshots / f"{registration_date.isoformat()}-{content_hash}.json"
        path.write_bytes(canonical_bytes(snapshot) + b"\n")

        contract = snapshot["targets"][0]
        entry = registration._entry_for(
            contract, content_hash, registered_at, ledger_pin=LEDGER_PIN
        )
        entry["registrationState"] = state
        entry.update(overrides or {})
        self.entries.append(registration.ts_literal(entry))
        self.write_generated()
        return contract


@pytest.fixture
def lane(tmp_path, monkeypatch) -> Lane:
    built = Lane(tmp_path)
    monkeypatch.setattr(awaiting, "REGISTRY", built.registry_path)
    monkeypatch.setattr(awaiting, "GENERATED_TARGETS", built.generated_path)
    monkeypatch.setattr(awaiting, "EXPIRED_REGISTRATIONS", built.expired_path)
    monkeypatch.setattr(awaiting, "TARGET_SNAPSHOTS", built.snapshots)
    # _target_registration_fields records the snapshot path relative to the
    # repository root; point it at the fabricated tree instead.
    monkeypatch.setattr(registration, "ROOT", tmp_path)
    return built


def select(today: dt.date = TODAY, catalog: set[str] | None = None) -> list:
    return awaiting.select(today, catalog or set(), {})


def test_registered_but_unforecast_target_is_retried_before_its_window_opens(
    lane,
) -> None:
    entry = registry_entry()
    lane.write_registry([entry])
    contract = lane.register(rolled_target(entry))

    selected = select()

    assert len(selected) == 1
    start, data_point_id, target = selected[0]
    assert start == "2026-09-15"
    assert data_point_id == contract["dataPointId"]
    assert target["catalogSlug"] == "fixture-august-2026"
    # The emitted target carries the committed registration forward rather than
    # asking the privileged leg to mint a fresh one.
    assert target["registrationState"] == "preregistered"
    assert target["registeredAtUtc"] == REGISTERED_AT
    assert (lane.snapshots / f"2026-07-31-{target['targetContentHash']}.json").is_file()
    assert target["targetRegistrationPath"] == (
        f"records/targets/2026-07-31-{target['targetContentHash']}.json"
    )
    assert target["sourceBinding"] == contract["sourceBinding"]


def test_perturbed_registry_entry_is_dropped_rather_than_forecast(lane, capsys) -> None:
    """The property the whole design rests on.

    The registration is untouched and canonical; only the committed registry
    changed. The rebuild must then disagree with the snapshot, and disagreement
    must drop the target — never emit it against a contract nobody registered.
    """
    entry = registry_entry()
    lane.write_registry([entry])
    lane.register(rolled_target(entry))

    perturbed = copy.deepcopy(entry)
    perturbed["extras"]["sourceBinding"]["sourceSeriesId"] = "TAMPERED"
    lane.write_registry([perturbed])

    assert select() == []
    assert "rebuilt contract is not byte-identical" in capsys.readouterr().err


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda e: e["extras"].update(targetUnit="index"), id="unit"),
        pytest.param(
            lambda e: e["extras"].update(expectedReleaseDate="2026-09-16"),
            id="release-date",
        ),
        pytest.param(
            lambda e: e["extras"]["sourceBinding"].update(
                transform={"operation": "identity", "factor": 100}
            ),
            id="transform",
        ),
        pytest.param(
            lambda e: e["extras"]["sourceBinding"].update(
                releasePolicy="advance_vintage"
            ),
            id="release-policy",
        ),
        pytest.param(lambda e: e.update(slug="renamed-{month}-{year}"), id="slug"),
    ],
)
def test_every_contract_bearing_registry_field_is_load_bearing(
    lane, capsys, mutate
) -> None:
    entry = registry_entry()
    lane.write_registry([entry])
    lane.register(rolled_target(entry))

    perturbed = copy.deepcopy(entry)
    mutate(perturbed)
    lane.write_registry([perturbed])

    assert select() == []
    assert "rebuilt contract is not byte-identical" in capsys.readouterr().err


def test_registry_that_no_longer_dates_the_period_drops_the_target(
    lane, capsys
) -> None:
    entry = registry_entry()
    entry["extras"]["sourceBinding"]["adapter"] = "ons-timeseries"
    entry["releaseDates"] = {"2026-08": "2026-09-15"}
    entry["releaseCalendarUrl"] = "https://www.ons.gov.uk/releasecalendar"
    lane.write_registry([entry])
    lane.register(rolled_target(entry))

    dropped = copy.deepcopy(entry)
    dropped["releaseDates"] = {}
    lane.write_registry([dropped])

    assert select() == []
    assert "committed registry no longer dates this period" in capsys.readouterr().err


def test_target_whose_release_window_already_opened_is_not_retried(
    lane, capsys
) -> None:
    """The born-dead case: forecasting it now would fabricate chronology."""
    entry = registry_entry(release_date="2026-07-13")
    lane.write_registry([entry])
    lane.register(rolled_target(entry))

    assert select() == []
    assert "release window opened 2026-07-13" in capsys.readouterr().out


def test_window_opening_today_is_already_closed_to_retries(lane) -> None:
    entry = registry_entry(release_date=TODAY.isoformat())
    lane.write_registry([entry])
    lane.register(rolled_target(entry))

    assert select() == []
    assert len(select(today=TODAY - dt.timedelta(days=1))) == 1


def test_terminally_retired_registration_is_never_retried(lane, capsys) -> None:
    entry = registry_entry()
    lane.write_registry([entry])
    contract = lane.register(rolled_target(entry))
    lane.write_expired([contract["dataPointId"]])

    assert select() == []
    assert "retired as expired unforecast" in capsys.readouterr().out


def test_unreadable_expired_list_refuses_to_select_anything(lane) -> None:
    lane.expired_path.write_text("export const SOMETHING_ELSE = [] as const;\n")

    with pytest.raises(SystemExit) as excinfo:
        select()

    assert "terminally retired" in str(excinfo.value)


def test_slug_already_in_the_live_catalog_is_skipped(lane, capsys) -> None:
    entry = registry_entry()
    lane.write_registry([entry])
    lane.register(rolled_target(entry))

    assert select(catalog={"fixture-august-2026"}) == []
    assert "catalog already publishes fixture-august-2026" in capsys.readouterr().out


def test_published_registrations_are_not_awaiting_a_forecast(lane) -> None:
    entry = registry_entry()
    lane.write_registry([entry])
    lane.register(rolled_target(entry), state="published")

    assert select() == []


def test_generated_ledger_disagreeing_with_its_snapshot_is_dropped(
    lane, capsys
) -> None:
    entry = registry_entry()
    lane.write_registry([entry])
    lane.register(rolled_target(entry), overrides={"catalogSlug": "fixture-july-2026"})

    assert select() == []
    assert "catalogSlug disagrees with" in capsys.readouterr().err


def test_registration_without_a_committed_snapshot_is_dropped(lane, capsys) -> None:
    entry = registry_entry()
    lane.write_registry([entry])
    lane.register(rolled_target(entry))
    for path in lane.snapshots.glob("*.json"):
        path.unlink()

    assert select() == []
    assert "expected exactly one registration snapshot" in capsys.readouterr().err


def test_malformed_content_hash_is_dropped(lane, capsys) -> None:
    entry = registry_entry()
    lane.write_registry([entry])
    lane.register(rolled_target(entry), overrides={"targetContentHash": "not-a-hash"})

    assert select() == []
    assert "malformed targetContentHash" in capsys.readouterr().err


def test_malformed_release_window_is_dropped(lane, capsys) -> None:
    entry = registry_entry()
    lane.write_registry([entry])
    contract = lane.register(rolled_target(entry))
    binding = copy.deepcopy(contract["sourceBinding"])
    binding["expectedReleaseWindow"] = {"start": "soon", "end": "later"}
    lane.entries.clear()
    lane.register(rolled_target(entry), overrides={"sourceBinding": binding})

    assert select() == []
    assert "malformed expected release window" in capsys.readouterr().err


def test_prospect_series_absent_from_the_registry_is_still_checked(lane) -> None:
    """A mined series has no registry template; the restatement is still bound.

    ``rebuild_target`` restates it from the registration's own contract and
    leaves every derived field to ``build_contract``, so the byte-identity gate
    still has to pass.
    """
    entry = registry_entry()
    lane.write_registry([])  # the roll never touches this series
    contract = lane.register(rolled_target(entry))

    selected = select()

    assert len(selected) == 1
    assert selected[0][1] == contract["dataPointId"]
    assert selected[0][2]["sourceBinding"] == contract["sourceBinding"]


def test_emitted_binding_comes_from_the_snapshot_not_the_ledger_block(
    lane,
) -> None:
    """A rewritten generated block cannot steer what gets forecast.

    ``rebuild_target`` restates a prospect target from the canonical snapshot,
    and ``_target_registration_fields`` fills the emitted target from the same
    contract, so a tampered ledger block is ignored rather than obeyed.
    """
    entry = registry_entry()
    lane.write_registry([])
    contract = lane.register(rolled_target(entry))
    binding = copy.deepcopy(contract["sourceBinding"])
    binding["sourceSeriesId"] = "TAMPERED"
    lane.entries.clear()
    lane.register(rolled_target(entry), overrides={"sourceBinding": binding})

    selected = select()

    assert len(selected) == 1
    assert selected[0][2]["sourceBinding"]["sourceSeriesId"] == "FIXTURE"


def test_tampered_snapshot_is_dropped(lane, capsys) -> None:
    """Editing the snapshot breaks the hash its own filename asserts."""
    entry = registry_entry()
    lane.write_registry([entry])
    lane.register(rolled_target(entry))
    (path,) = lane.snapshots.glob("*.json")
    snapshot = json.loads(path.read_text())
    snapshot["targets"][0]["sourceBinding"]["sourceSeriesId"] = "TAMPERED"
    path.write_bytes(canonical_bytes(snapshot) + b"\n")

    assert select() == []
    assert "snapshot hash mismatch" in capsys.readouterr().err


def test_non_canonical_snapshot_is_dropped(lane, capsys) -> None:
    entry = registry_entry()
    lane.write_registry([entry])
    lane.register(rolled_target(entry))
    (path,) = lane.snapshots.glob("*.json")
    path.write_text(json.dumps(json.loads(path.read_text()), indent=2) + "\n")

    assert select() == []
    assert "not canonical" in capsys.readouterr().err


def test_multi_target_snapshot_is_refused(lane, capsys) -> None:
    """A retry rebuilds one target; a batch snapshot is not that."""
    first = registry_entry()
    second = registry_entry(release_date="2026-09-20")
    second["series"] = "fixture.second"
    second["slug"] = "second-{month}-{year}"
    lane.write_registry([first, second])
    snapshot = registration.build_snapshot(
        [rolled_target(first), rolled_target(second)],
        REGISTRATION_DATE,
        registered_at_utc=REGISTERED_AT,
        ledger_pin=LEDGER_PIN,
    )
    content_hash = registration.registration_content_hash(snapshot)
    (lane.snapshots / f"2026-07-31-{content_hash}.json").write_bytes(
        canonical_bytes(snapshot) + b"\n"
    )
    lane.entries.append(
        registration.ts_literal(
            registration._entry_for(
                snapshot["targets"][0], content_hash, REGISTERED_AT, LEDGER_PIN
            )
        )
    )
    lane.write_generated()

    assert select() == []
    assert "single-target registration snapshot" in capsys.readouterr().err


def test_retries_are_ordered_by_window_then_id(lane) -> None:
    early = registry_entry(release_date="2026-09-01")
    early["series"] = "fixture.early"
    early["slug"] = "early-{month}-{year}"
    late = registry_entry(release_date="2026-09-20")
    late["series"] = "fixture.late"
    late["slug"] = "late-{month}-{year}"
    lane.write_registry([late, early])
    lane.register(rolled_target(late))
    lane.register(rolled_target(early))

    starts = [start for start, _, _ in select()]

    assert starts == ["2026-09-01", "2026-09-20"]
