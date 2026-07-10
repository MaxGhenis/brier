from __future__ import annotations

import datetime as dt
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from adopt_proven_series import cadence_of, slug_template  # noqa: E402
from roll_docket import (  # noqa: E402
    latest_published_period,
    next_roll_period,
    not_too_far_ahead,
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
