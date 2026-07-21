from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from briefing_usage_report import (  # noqa: E402
    fetched_urls,
    normalize_source,
    usage_report,
)


def test_normalize_source_collapses_variants() -> None:
    assert normalize_source("https://www.bls.gov/oes/tables.htm?y=2026") == (
        "www.bls.gov/oes/tables.htm"
    )
    assert normalize_source("HTTPS://WWW.BLS.GOV/oes/") == "www.bls.gov/oes"


def test_usage_report_matches_prefix_and_reports_unmatched() -> None:
    run_urls = {
        "https://www.bls.gov/emp/tables/occupational-projections.htm",
        "https://fred.stlouisfed.org/series/PAYEMS?query=1",
    }
    report = usage_report(
        run_urls,
        [
            "https://www.bls.gov/emp/tables",  # prefix of a fetched page
            "https://www.census.gov/programs-surveys/cps.html",  # untouched
        ],
    )
    assert report["sourcesDrawnOn"] == 1
    assert report["briefingSources"] == 2
    assert report["overlapShare"] == 0.5
    assert report["unmatched"] == [
        "https://www.census.gov/programs-surveys/cps.html"
    ]


def test_usage_report_empty_briefing_yields_null_share() -> None:
    report = usage_report({"https://example.gov/a"}, [])
    assert report["overlapShare"] is None
    assert report["sourcesDrawnOn"] == 0


def test_fetched_urls_reads_archived_events(tmp_path: pathlib.Path) -> None:
    events = tmp_path / "draft_codex_events.jsonl"
    events.write_text(
        json.dumps({"type": "item.completed", "item": {
            "text": "fetched https://www.bls.gov/news.release/empsit.nr0.htm ok"
        }}) + "\n"
    )
    urls = fetched_urls(tmp_path)
    assert "https://www.bls.gov/news.release/empsit.nr0.htm" in urls


def test_fetched_urls_on_a_real_run_dir_if_present() -> None:
    records = ROOT / "records" / "thesis-analyst"
    run_dirs = sorted(records.glob("2026-07-21/*")) if records.exists() else []
    if not run_dirs:
        return  # environment without records; unit tests above cover logic
    urls = fetched_urls(run_dirs[0])
    assert urls, "an activity-backed run should have fetched at least one URL"
