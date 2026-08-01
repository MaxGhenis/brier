from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import map_bill_metrics  # noqa: E402


def write_json(path: pathlib.Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_maps_all_statuses_and_emits_only_not_yet_drafts(
    tmp_path: pathlib.Path,
) -> None:
    bill_path = tmp_path / "bills" / "example-bill.json"
    docket_path = tmp_path / "scripts" / "docket_series.json"
    drafts_dir = tmp_path / "drafts" / "ledger-entries"
    artifact = {
        "bill": {"slug": "example-bill", "name": "Example bill"},
        "provisions": [
            {
                "heading": "Example provision",
                "metrics": [
                    {
                        "category": "operational",
                        "kind": "Exact",
                        "text": "Exact unemployment metric",
                        "series_hint": "eurostat.unemployment_rate",
                    },
                    {
                        "category": "intended",
                        "kind": "Prefix",
                        "text": "JOLTS hiring metric",
                        "series_hint": "bls.jolts",
                    },
                    {
                        "category": "intended",
                        "kind": "Candidate",
                        "text": "CRP active acres",
                        "series_hint": "usda.fsa.crp.active_acres",
                    },
                    {
                        "category": "unintended",
                        "kind": "Human triage",
                        "text": "No series hint was supplied",
                        "series_hint": None,
                        "registry": "no-series",
                    },
                ],
            }
        ],
    }
    docket = {
        "comment": "fixture",
        "series": [
            {
                "series": "eurostat.unemployment_rate.belgium",
                "cadence": "monthly",
                "slug": "belgium-unemployment-{month}-{year}",
            },
            {
                "series": "eurostat.unemployment_rate",
                "cadence": "monthly",
                "slug": "euro-unemployment-{month}-{year}",
            },
            {
                "series": "bls.jolts.hires_rate",
                "cadence": "monthly",
                "slug": "jolts-hires-rate-{month}-{year}",
            },
        ],
    }
    write_json(bill_path, artifact)
    write_json(docket_path, docket)
    original_bill = bill_path.read_bytes()
    original_docket = docket_path.read_bytes()

    output_path, draft_paths = map_bill_metrics.map_bill_metrics(
        bill_path, docket_path, drafts_dir=drafts_dir
    )

    assert output_path == bill_path.with_suffix(".mapped.json")
    mapped = json.loads(output_path.read_text(encoding="utf-8"))
    metrics = mapped["provisions"][0]["metrics"]
    assert [metric["registry"] for metric in metrics] == [
        "reachable",
        "reachable",
        "not-yet",
        "unmapped",
    ]
    assert metrics[0]["matched_series"] == "eurostat.unemployment_rate"
    assert metrics[1]["matched_series"] == "bls.jolts.hires_rate"
    assert "matched_series" not in metrics[2]
    assert "matched_series" not in metrics[3]
    assert mapped["summary"] == {"reachable": 2, "notYet": 1, "unmapped": 1}

    expected_draft = drafts_dir / "usda-fsa-crp-active-acres.json"
    assert draft_paths == [expected_draft]
    assert json.loads(expected_draft.read_text(encoding="utf-8")) == {
        "series": "usda.fsa.crp.active_acres",
        "cadence": None,
        "slug": None,
        "proposedFrom": "example-bill",
        "metricText": "CRP active acres",
    }
    assert bill_path.read_bytes() == original_bill
    assert docket_path.read_bytes() == original_docket


def test_prefix_matching_requires_a_dot_boundary(tmp_path: pathlib.Path) -> None:
    bill_path = tmp_path / "bill.json"
    docket_path = tmp_path / "docket.json"
    drafts_dir = tmp_path / "drafts"
    write_json(
        bill_path,
        {
            "bill": {"slug": "boundary-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
                            "category": "operational",
                            "kind": "Near prefix",
                            "text": "Should not match",
                            "series_hint": "bls.jolt",
                        }
                    ]
                }
            ],
        },
    )
    write_json(
        docket_path,
        {
            "series": [
                {
                    "series": "bls.jolts.hires_rate",
                    "cadence": "monthly",
                    "slug": "unused",
                }
            ]
        },
    )

    output_path, _ = map_bill_metrics.map_bill_metrics(
        bill_path, docket_path, drafts_dir=drafts_dir
    )

    mapped = json.loads(output_path.read_text(encoding="utf-8"))
    metric = mapped["provisions"][0]["metrics"][0]
    assert metric["registry"] == "not-yet"
    assert "matched_series" not in metric


def test_cli_uses_default_mapped_output_name(
    tmp_path: pathlib.Path, capsys
) -> None:
    bill_path = tmp_path / "cli-bill.json"
    docket_path = tmp_path / "docket.json"
    write_json(
        bill_path,
        {
            "bill": {"slug": "cli-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
                            "category": "unintended",
                            "kind": "No hint",
                            "text": "Needs human triage",
                            "series_hint": "",
                        }
                    ]
                }
            ],
        },
    )
    write_json(docket_path, {"series": []})

    assert map_bill_metrics.main([str(bill_path), "--docket", str(docket_path)]) == 0

    assert bill_path.with_suffix(".mapped.json").exists()
    assert "reachable=0, not-yet=0, unmapped=1, drafts=0" in capsys.readouterr().out


def test_json_writes_replace_symlinks_instead_of_following_them(
    tmp_path: pathlib.Path,
) -> None:
    protected_path = tmp_path / "protected.json"
    protected_path.write_text('{"doNotChange": true}\n', encoding="utf-8")
    output_path = tmp_path / "draft.json"
    output_path.symlink_to(protected_path)

    map_bill_metrics.write_json(output_path, {"proposal": True})

    assert protected_path.read_text(encoding="utf-8") == '{"doNotChange": true}\n'
    assert not output_path.is_symlink()
    assert json.loads(output_path.read_text(encoding="utf-8")) == {"proposal": True}


def test_colliding_draft_slugs_fail_before_writing(tmp_path: pathlib.Path) -> None:
    bill_path = tmp_path / "bill.json"
    docket_path = tmp_path / "docket.json"
    drafts_dir = tmp_path / "drafts"
    write_json(
        bill_path,
        {
            "bill": {"slug": "collision-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
                            "category": "operational",
                            "kind": "First",
                            "text": "First metric",
                            "series_hint": "agency.foo_bar",
                        },
                        {
                            "category": "intended",
                            "kind": "Second",
                            "text": "Second metric",
                            "series_hint": "agency.foo.bar",
                        },
                    ]
                }
            ],
        },
    )
    write_json(docket_path, {"series": []})

    with pytest.raises(map_bill_metrics.MappingError, match="same draft filename"):
        map_bill_metrics.map_bill_metrics(
            bill_path, docket_path, drafts_dir=drafts_dir
        )

    assert not drafts_dir.exists()
    assert not bill_path.with_suffix(".mapped.json").exists()


def test_existing_draft_for_colliding_hint_is_not_overwritten(
    tmp_path: pathlib.Path,
) -> None:
    bill_path = tmp_path / "bill.json"
    docket_path = tmp_path / "docket.json"
    drafts_dir = tmp_path / "drafts"
    write_json(
        bill_path,
        {
            "bill": {"slug": "later-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
                            "category": "intended",
                            "kind": "Collision",
                            "text": "A later metric",
                            "series_hint": "agency.foo.bar",
                        }
                    ]
                }
            ],
        },
    )
    write_json(docket_path, {"series": []})
    existing_path = drafts_dir / "agency-foo-bar.json"
    write_json(
        existing_path,
        {
            "series": "agency.foo_bar",
            "cadence": None,
            "slug": None,
            "proposedFrom": "earlier-bill",
            "metricText": "An earlier metric",
        },
    )
    existing_bytes = existing_path.read_bytes()

    with pytest.raises(map_bill_metrics.MappingError, match="already belongs"):
        map_bill_metrics.map_bill_metrics(
            bill_path, docket_path, drafts_dir=drafts_dir
        )

    assert existing_path.read_bytes() == existing_bytes
    assert not bill_path.with_suffix(".mapped.json").exists()


def test_crp_series_is_registered_with_a_complete_binding() -> None:
    docket = json.loads(
        (ROOT / "scripts" / "docket_series.json").read_text(encoding="utf-8")
    )
    entries = [
        entry
        for entry in docket["series"]
        if entry["series"] == "usda.fsa.crp.enrolled_acres_total"
    ]
    assert len(entries) == 1
    entry = entries[0]

    assert entry["cadence"] == "monthly"
    assert entry["slug"] == "us-crp-enrolled-acres-{month}-{year}"
    # Promotion strips the draft-lifecycle fields; registered entries carry
    # only the shared shape.
    assert "integrationStatus" not in entry
    assert "integrationNote" not in entry
    assert not (
        ROOT
        / "drafts"
        / "ledger-entries"
        / "usda-fsa-crp-enrolled-acres-total.json"
    ).exists()

    extras = entry["extras"]
    assert extras["targetUnit"] == "count"
    assert extras["valueScale"] == 1
    assert "condition" not in extras
    assert set(extras["sourceBinding"]) == {
        "adapter",
        "sourceUrl",
        "sourceSeriesId",
        "field",
        "table",
        "transform",
        "releasePolicy",
    }
    assert extras["sourceBinding"]["adapter"] == "fsa-crp-monthly-summary"
