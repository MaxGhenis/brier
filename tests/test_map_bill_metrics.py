from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import map_bill_metrics  # noqa: E402

REAL_CATALOG_FIXTURE = ROOT / "tests" / "fixtures" / "ledger" / "series_catalog.json"


def write_json(path: pathlib.Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def catalog_row(concept: str, uuid: str, *, aliases: list[str] | None = None) -> dict:
    """Return one complete row in the frozen Ledger catalog schema."""
    return {
        "uuid": uuid,
        "concept": concept,
        "family_patterns": [f"{concept}.{{P}}"],
        "status": "observed",
        "unit": "count",
        "cadence": "month",
        "geography": {
            "id": "XX",
            "level": "country",
            "name": "Example",
        },
        "entity": {"name": "example", "role": "aggregate"},
        "sources": ["example-agency"],
        "aliases": aliases or [],
        "rid_patterns": [f"{concept}.{{P}}.first_print"],
        "first_observed_period": "2026-01",
        "last_observed_period": "2026-01",
        "observation_count": 1,
    }


def empty_catalog(path: pathlib.Path) -> None:
    write_json(path, {"series": []})


def test_maps_all_registry_states_and_writes_ingestion_request(
    tmp_path: pathlib.Path,
) -> None:
    bill_path = tmp_path / "bills" / "example-bill.json"
    docket_path = tmp_path / "scripts" / "docket_series.json"
    catalog_path = tmp_path / "ledger" / "series_catalog.json"
    drafts_dir = tmp_path / "drafts" / "ledger-ingestion"
    artifact = {
        "bill": {"slug": "example-bill", "name": "Example bill"},
        "provisions": [
            {
                "heading": "Example provision",
                "metrics": [
                    {
                        "text": "Exact docket metric",
                        "series_hint": "docket.exact",
                    },
                    {
                        "text": "Docket descendant metric",
                        "series_hint": "docket.family",
                    },
                    {
                        "text": "Exact Ledger metric",
                        "series_hint": "ledger.exact",
                    },
                    {
                        "text": "Ledger alias metric",
                        "series_hint": "LEDGER_ALIAS",
                    },
                    {
                        "text": "Ledger descendant metric",
                        "series_hint": "ledger.family",
                    },
                    {
                        "text": "Unknown metric",
                        "series_hint": "agency.unknown.metric",
                        "matched_series": "stale.series",
                        "ledger_uuid": "stale-uuid",
                    },
                    {
                        "text": "No series hint was supplied",
                        "series_hint": None,
                        "registry": "no-series",
                        "matched_series": "stale.series",
                        "ledger_uuid": "stale-uuid",
                    },
                ],
            }
        ],
    }
    docket = {
        "series": [
            {"series": "docket.exact.child"},
            {"series": "docket.exact"},
            {"series": "docket.family.child"},
        ]
    }
    catalog = {
        "series": [
            catalog_row("ledger.exact", "uuid-exact"),
            catalog_row(
                "ledger.alias.target",
                "uuid-alias",
                aliases=["LEDGER_ALIAS"],
            ),
            catalog_row("ledger.family.child", "uuid-descendant"),
        ]
    }
    write_json(bill_path, artifact)
    write_json(docket_path, docket)
    write_json(catalog_path, catalog)
    original_bill = bill_path.read_bytes()
    original_docket = docket_path.read_bytes()
    original_catalog = catalog_path.read_bytes()

    output_path, request_paths = map_bill_metrics.map_bill_metrics(
        bill_path, docket_path, catalog_path, drafts_dir=drafts_dir
    )

    assert output_path == bill_path.with_suffix(".mapped.json")
    mapped = json.loads(output_path.read_text(encoding="utf-8"))
    metrics = mapped["provisions"][0]["metrics"]
    assert [metric["registry"] for metric in metrics] == [
        "reachable",
        "reachable",
        "ledger",
        "ledger",
        "ledger",
        "not-yet",
        "unmapped",
    ]
    assert metrics[0]["matched_series"] == "docket.exact"
    assert metrics[1]["matched_series"] == "docket.family.child"
    assert "ledger_uuid" not in metrics[0]
    assert "ledger_uuid" not in metrics[1]
    assert (
        metrics[2]["matched_series"],
        metrics[2]["ledger_uuid"],
    ) == ("ledger.exact", "uuid-exact")
    assert (
        metrics[3]["matched_series"],
        metrics[3]["ledger_uuid"],
    ) == ("ledger.alias.target", "uuid-alias")
    assert (
        metrics[4]["matched_series"],
        metrics[4]["ledger_uuid"],
    ) == ("ledger.family.child", "uuid-descendant")
    for metric in metrics[5:]:
        assert "matched_series" not in metric
        assert "ledger_uuid" not in metric
    assert mapped["summary"] == {
        "reachable": 2,
        "ledger": 3,
        "notYet": 1,
        "unmapped": 1,
    }

    expected_request = drafts_dir / "agency-unknown-metric.json"
    assert request_paths == [expected_request]
    assert json.loads(expected_request.read_text(encoding="utf-8")) == {
        "proposed_concept": "agency.unknown.metric",
        "status": "proposed",
        "unit": None,
        "cadence": None,
        "proposedFrom": "example-bill",
        "metricText": "Unknown metric",
        "note": (
            "Proposed catalog row for PolicyEngine/ledger "
            "series_catalog.json; verify identity, unit, cadence, and "
            "official source before ingestion."
        ),
    }
    assert bill_path.read_bytes() == original_bill
    assert docket_path.read_bytes() == original_docket
    assert catalog_path.read_bytes() == original_catalog


def test_docket_match_wins_over_catalog_match(tmp_path: pathlib.Path) -> None:
    bill_path = tmp_path / "bill.json"
    docket_path = tmp_path / "docket.json"
    catalog_path = tmp_path / "catalog.json"
    write_json(
        bill_path,
        {
            "bill": {"slug": "precedence-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
                            "text": "Shared metric",
                            "series_hint": "shared.series",
                            "registry": "ledger",
                            "matched_series": "old.catalog.series",
                            "ledger_uuid": "old-uuid",
                        }
                    ]
                }
            ],
        },
    )
    write_json(docket_path, {"series": [{"series": "shared.series"}]})
    write_json(
        catalog_path,
        {"series": [catalog_row("shared.series", "catalog-uuid")]},
    )

    output_path, request_paths = map_bill_metrics.map_bill_metrics(
        bill_path,
        docket_path,
        catalog_path,
        drafts_dir=tmp_path / "drafts",
    )

    metric = json.loads(output_path.read_text(encoding="utf-8"))["provisions"][0][
        "metrics"
    ][0]
    assert metric == {
        "text": "Shared metric",
        "series_hint": "shared.series",
        "registry": "reachable",
        "matched_series": "shared.series",
    }
    assert request_paths == []


def test_catalog_exact_concept_wins_over_an_earlier_alias(
    tmp_path: pathlib.Path,
) -> None:
    catalog_path = tmp_path / "catalog.json"
    write_json(
        catalog_path,
        {
            "series": [
                catalog_row(
                    "other.series",
                    "alias-uuid",
                    aliases=["exact.series"],
                ),
                catalog_row("exact.series", "exact-uuid"),
            ]
        },
    )

    catalog = map_bill_metrics.load_catalog_series(catalog_path)

    assert map_bill_metrics.match_catalog_series("exact.series", catalog) == {
        "concept": "exact.series",
        "uuid": "exact-uuid",
        "aliases": [],
    }


def test_prefix_matching_requires_a_dot_boundary(tmp_path: pathlib.Path) -> None:
    bill_path = tmp_path / "bill.json"
    docket_path = tmp_path / "docket.json"
    catalog_path = tmp_path / "catalog.json"
    drafts_dir = tmp_path / "drafts"
    write_json(
        bill_path,
        {
            "bill": {"slug": "boundary-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
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
        {"series": [{"series": "bls.jolts.hires_rate"}]},
    )
    write_json(
        catalog_path,
        {"series": [catalog_row("bls.jolts.openings", "openings-uuid")]},
    )

    output_path, _ = map_bill_metrics.map_bill_metrics(
        bill_path, docket_path, catalog_path, drafts_dir=drafts_dir
    )

    metric = json.loads(output_path.read_text(encoding="utf-8"))["provisions"][0][
        "metrics"
    ][0]
    assert metric["registry"] == "not-yet"
    assert "matched_series" not in metric
    assert "ledger_uuid" not in metric


def test_real_catalog_fixture_propagates_alias_uuid(
    tmp_path: pathlib.Path,
) -> None:
    bill_path = tmp_path / "bill.json"
    docket_path = tmp_path / "docket.json"
    write_json(
        bill_path,
        {
            "bill": {"slug": "real-fixture-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
                            "text": "Core CPI",
                            "series_hint": "CPILFESL",
                        }
                    ]
                }
            ],
        },
    )
    write_json(docket_path, {"series": []})

    output_path, request_paths = map_bill_metrics.map_bill_metrics(
        bill_path,
        docket_path,
        REAL_CATALOG_FIXTURE,
        drafts_dir=tmp_path / "drafts",
    )

    metric = json.loads(output_path.read_text(encoding="utf-8"))["provisions"][0][
        "metrics"
    ][0]
    assert metric == {
        "text": "Core CPI",
        "series_hint": "CPILFESL",
        "registry": "ledger",
        "matched_series": "bls.cpi.u.core_mom",
        "ledger_uuid": "23a58ec2-2d41-4f17-ae3d-8affeda44fc1",
    }
    assert request_paths == []


def test_cli_requires_catalog_and_reports_v2_summary(
    tmp_path: pathlib.Path, capsys
) -> None:
    bill_path = tmp_path / "cli-bill.json"
    docket_path = tmp_path / "docket.json"
    catalog_path = tmp_path / "catalog.json"
    write_json(
        bill_path,
        {
            "bill": {"slug": "cli-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
                            "text": "Needs human triage",
                            "series_hint": "",
                        }
                    ]
                }
            ],
        },
    )
    write_json(docket_path, {"series": []})
    empty_catalog(catalog_path)

    with pytest.raises(SystemExit):
        map_bill_metrics.parse_args([str(bill_path), "--docket", str(docket_path)])

    assert (
        map_bill_metrics.main(
            [
                str(bill_path),
                "--docket",
                str(docket_path),
                "--catalog",
                str(catalog_path),
            ]
        )
        == 0
    )

    assert bill_path.with_suffix(".mapped.json").exists()
    assert (
        "reachable=0, ledger=0, not-yet=0, unmapped=1, ingestion-requests=0"
    ) in capsys.readouterr().out


def test_repeated_hint_and_rerun_are_idempotent(tmp_path: pathlib.Path) -> None:
    bill_path = tmp_path / "bill.json"
    docket_path = tmp_path / "docket.json"
    catalog_path = tmp_path / "catalog.json"
    drafts_dir = tmp_path / "drafts" / "ledger-ingestion"
    write_json(
        bill_path,
        {
            "bill": {"slug": "repeat-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
                            "text": "First mention",
                            "series_hint": "agency.new.series",
                        },
                        {
                            "text": "Second mention",
                            "series_hint": "agency.new.series",
                        },
                    ]
                }
            ],
        },
    )
    write_json(docket_path, {"series": []})
    empty_catalog(catalog_path)

    first_output, first_paths = map_bill_metrics.map_bill_metrics(
        bill_path, docket_path, catalog_path, drafts_dir=drafts_dir
    )
    request_path = drafts_dir / "agency-new-series.json"
    first_request = request_path.read_bytes()
    second_output, second_paths = map_bill_metrics.map_bill_metrics(
        bill_path, docket_path, catalog_path, drafts_dir=drafts_dir
    )

    assert first_output == second_output
    assert first_paths == second_paths == [request_path]
    assert request_path.read_bytes() == first_request
    assert sorted(drafts_dir.glob("*.json")) == [request_path]
    request = json.loads(request_path.read_text(encoding="utf-8"))
    assert request["metricText"] == "First mention"
    mapped = json.loads(second_output.read_text(encoding="utf-8"))
    assert mapped["summary"]["notYet"] == 2


def test_refuses_to_write_ingestion_requests_under_records(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    bill_path = tmp_path / "bill.json"
    docket_path = tmp_path / "docket.json"
    catalog_path = tmp_path / "catalog.json"
    records_dir = tmp_path / "records"
    monkeypatch.setattr(map_bill_metrics, "RECORDS_DIR", records_dir)
    write_json(
        bill_path,
        {
            "bill": {"slug": "records-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
                            "text": "Unknown metric",
                            "series_hint": "agency.unknown",
                        }
                    ]
                }
            ],
        },
    )
    write_json(docket_path, {"series": []})
    empty_catalog(catalog_path)

    with pytest.raises(map_bill_metrics.MappingError, match="records/"):
        map_bill_metrics.map_bill_metrics(
            bill_path,
            docket_path,
            catalog_path,
            drafts_dir=records_dir / "ledger-ingestion",
        )

    assert not records_dir.exists()
    assert not bill_path.with_suffix(".mapped.json").exists()


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


def test_colliding_request_slugs_fail_before_writing(
    tmp_path: pathlib.Path,
) -> None:
    bill_path = tmp_path / "bill.json"
    docket_path = tmp_path / "docket.json"
    catalog_path = tmp_path / "catalog.json"
    drafts_dir = tmp_path / "drafts"
    write_json(
        bill_path,
        {
            "bill": {"slug": "collision-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
                            "text": "First metric",
                            "series_hint": "agency.foo_bar",
                        },
                        {
                            "text": "Second metric",
                            "series_hint": "agency.foo.bar",
                        },
                    ]
                }
            ],
        },
    )
    write_json(docket_path, {"series": []})
    empty_catalog(catalog_path)

    with pytest.raises(map_bill_metrics.MappingError, match="same draft filename"):
        map_bill_metrics.map_bill_metrics(
            bill_path, docket_path, catalog_path, drafts_dir=drafts_dir
        )

    assert not drafts_dir.exists()
    assert not bill_path.with_suffix(".mapped.json").exists()


def test_existing_request_for_colliding_concept_is_not_overwritten(
    tmp_path: pathlib.Path,
) -> None:
    bill_path = tmp_path / "bill.json"
    docket_path = tmp_path / "docket.json"
    catalog_path = tmp_path / "catalog.json"
    drafts_dir = tmp_path / "drafts"
    write_json(
        bill_path,
        {
            "bill": {"slug": "later-bill"},
            "provisions": [
                {
                    "metrics": [
                        {
                            "text": "A later metric",
                            "series_hint": "agency.foo.bar",
                        }
                    ]
                }
            ],
        },
    )
    write_json(docket_path, {"series": []})
    empty_catalog(catalog_path)
    existing_path = drafts_dir / "agency-foo-bar.json"
    write_json(
        existing_path,
        {
            "proposed_concept": "agency.foo_bar",
            "status": "proposed",
            "unit": None,
            "cadence": None,
            "proposedFrom": "earlier-bill",
            "metricText": "An earlier metric",
            "note": (
                "Proposed catalog row for PolicyEngine/ledger "
                "series_catalog.json; verify identity, unit, cadence, and "
                "official source before ingestion."
            ),
        },
    )
    existing_bytes = existing_path.read_bytes()

    with pytest.raises(map_bill_metrics.MappingError, match="already belongs"):
        map_bill_metrics.map_bill_metrics(
            bill_path, docket_path, catalog_path, drafts_dir=drafts_dir
        )

    assert existing_path.read_bytes() == existing_bytes
    assert not bill_path.with_suffix(".mapped.json").exists()
