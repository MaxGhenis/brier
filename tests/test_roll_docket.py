from __future__ import annotations

import copy
import datetime as dt
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import register_targets  # noqa: E402
from adopt_proven_series import cadence_of, slug_template  # noqa: E402
from roll_docket import (  # noqa: E402
    latest_published_period,
    next_roll_period,
    not_too_far_ahead,
    snapshot_seed_target,
    step_period,
    template_regex,
)


def registry_entry(cadence: str, slug: str) -> dict[str, str]:
    return {"series": "fixture.series", "cadence": cadence, "slug": slug}


def test_template_regex_supports_repeated_tokens_without_duplicate_groups() -> None:
    template = "fixture-{year}-{month}-{year}-{month}"
    pattern = template_regex(template, "monthly")

    assert pattern.fullmatch("fixture-2026-may-2026-may")
    assert not pattern.fullmatch("fixture-2026-may-2027-may")
    assert latest_published_period(
        registry_entry("monthly", template),
        {"fixture-2026-may-2026-may"},
    ) == ("2026-05", "fixture-2026-may-2026-may")


@pytest.mark.parametrize(
    ("cadence", "template", "slug"),
    [
        ("weekly", "fixture-{period}", "fixture-2026-02-30"),
        ("monthly", "fixture-{month}-{year}", "fixture-notamonth-2026"),
        ("quarterly", "fixture-q{quarter}-{year}", "fixture-q5-2026"),
    ],
)
def test_invalid_captured_periods_are_rejected(
    cadence: str,
    template: str,
    slug: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert latest_published_period(registry_entry(cadence, template), {slug}) is None
    assert "invalid captured period" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("cadence", "period"),
    [
        ("weekly", "week_2026-02-30"),
        ("monthly", "2026-13"),
        ("quarterly", "2026-Q9"),
    ],
)
def test_malformed_period_helpers_warn_and_never_raise(
    cadence: str,
    period: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert step_period(period, cadence) is None
    assert not not_too_far_ahead(period, cadence, dt.date(2026, 3, 15))
    assert "warning: skip malformed" in capsys.readouterr().err


def test_far_future_rogue_slug_recovers_earliest_eligible_gap() -> None:
    entry = registry_entry("monthly", "fixture-{month}-{year}")
    existing = {
        "fixture-january-2026",
        "fixture-february-2026",
        "fixture-december-2099",
    }

    assert next_roll_period(
        entry,
        existing,
        {"fixture-january-2026"},
        dt.date(2026, 3, 15),
    ) == ("2026-03", "fixture-february-2026")


def test_slug_template_replaces_month_names_only_at_token_boundaries() -> None:
    assert (
        slug_template("mayor-may-index-2026", "2026-05", "monthly")
        == "mayor-{month}-index-{year}"
    )
    assert (
        slug_template("may-report-may-2026", "2026-05", "monthly")
        == "may-report-{month}-{year}"
    )


@pytest.mark.parametrize(
    "period",
    ["week_2026-02-30", "2026-00", "2026-13", "2026-Q0", "2026-Q5"],
)
def test_adoption_rejects_semantically_invalid_periods(period: str) -> None:
    assert cadence_of(period) is None


def apel_snapshot_entries() -> list[dict]:
    registry = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    return [
        entry
        for entry in registry["series"]
        if entry["series"].startswith("usaspending.")
    ]


def test_real_apel_seeds_build_six_preregistered_snapshot_contracts() -> None:
    entries = apel_snapshot_entries()
    assert len(entries) == 6

    for entry in entries:
        assert entry["cadence"] == "annual"
        assert entry["period"] == "FY2026"
        assert entry["extras"]["expectedReleaseWindow"] == {
            "start": "2026-10-15",
            "end": "2026-10-22",
        }

        target = snapshot_seed_target(
            entry,
            set(),
            dt.date(2026, 8, 1),
        )
        assert target is not None
        assert target["catalogSlug"] == entry["slug"].format(period="fy2026")
        assert "previousTarget" not in target

        contract = register_targets.build_contract(
            target,
            dt.date(2026, 8, 1),
        )
        assert contract["series"] == entry["series"]
        assert contract["period"] == "FY2026"
        assert contract["dataPointId"] == (
            f"{entry['series']}.fy2026.registered_query_snapshot"
        )
        assert contract["sourceBinding"]["expectedReleaseWindow"] == (
            entry["extras"]["expectedReleaseWindow"]
        )
        assert contract["sourceBinding"]["allowedHosts"] == [
            "api.usaspending.gov"
        ]


@pytest.mark.parametrize(
    ("today", "eligible"),
    [
        (dt.date(2026, 7, 31), False),  # 76 days before the capture date.
        (dt.date(2026, 8, 1), True),  # Exact 75-day horizon boundary.
        (dt.date(2026, 10, 14), True),
        (dt.date(2026, 10, 15), False),  # Never forecast on capture day.
        (dt.date(2026, 10, 16), False),
    ],
)
def test_snapshot_seed_uses_strict_precapture_start_boundary(
    today: dt.date,
    eligible: bool,
) -> None:
    entry = apel_snapshot_entries()[0]
    target = snapshot_seed_target(entry, set(), today)
    assert (target is not None) is eligible


def test_snapshot_seed_is_one_shot_and_never_steps_the_fiscal_year() -> None:
    entry = apel_snapshot_entries()[0]
    slug = entry["slug"].format(period="fy2026")

    assert snapshot_seed_target(
        entry,
        {slug},
        dt.date(2026, 8, 1),
    ) is None
    assert entry["period"] == "FY2026"
    assert "FY2027" not in json.dumps(entry)


@pytest.mark.parametrize(
    "mutation",
    [
        "malformed-period",
        "missing-window",
        "reversed-window",
        "wrong-policy",
    ],
)
def test_snapshot_seed_rejects_unreviewable_annual_entries(
    mutation: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    entry = copy.deepcopy(apel_snapshot_entries()[0])
    if mutation == "malformed-period":
        entry["period"] = "2026"
    elif mutation == "missing-window":
        entry["extras"].pop("expectedReleaseWindow")
    elif mutation == "reversed-window":
        entry["extras"]["expectedReleaseWindow"] = {
            "start": "2026-10-22",
            "end": "2026-10-15",
        }
    else:
        entry["extras"]["sourceBinding"]["releasePolicy"] = "first_print"

    assert snapshot_seed_target(
        entry,
        set(),
        dt.date(2026, 8, 1),
    ) is None
    assert "warning: skip" in capsys.readouterr().err
