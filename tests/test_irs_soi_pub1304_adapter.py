"""IRS SOI Publication 1304 Table 3.3 adapter (thesis#106).

The fixtures under tests/fixtures/irs_soi_pub1304/ are the REAL official
workbooks fetched from www.irs.gov on 2026-08-01 (SHA-256 pins in
docs/anchor-verifications.md), so the parse path is armed against the
artifact IRS actually publishes — including the TY2020 pre-ARPA column
label — and every integrator-verified anchor value reproduces from bytes.
"""

from __future__ import annotations

import copy
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import prospect_targets  # noqa: E402
import register_targets  # noqa: E402
import resolve_pending  # noqa: E402
from adopt_proven_series import SOURCE_BINDING_TEMPLATE_KEYS  # noqa: E402

SERIES = "irs.actc.total_claims"
SPEC = resolve_pending.IRS_SOI_PUB1304_ADAPTERS[SERIES]
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "irs_soi_pub1304"


def fixture_bytes(year: str) -> bytes:
    return (FIXTURE_ROOT / f"{int(year) % 100:02d}in33ar.xls").read_bytes()


def docket_entry() -> dict:
    docket = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    return next(e for e in docket["series"] if e["series"] == SERIES)


def test_irs_soi_adapter_and_docket_share_the_exact_seven_key_binding() -> None:
    binding = docket_entry()["extras"]["sourceBinding"]

    assert "irs-soi-pub1304" in register_targets.SOURCE_ADAPTERS
    assert prospect_targets._source_binding_errors(binding) == []
    assert set(binding) == SOURCE_BINDING_TEMPLATE_KEYS
    assert resolve_pending.irs_soi_pub1304_binding_template(SPEC) == binding
    assert resolve_pending.irs_soi_pub1304_binding_matches_spec(binding, SPEC)
    assert resolve_pending.irs_soi_pub1304_binding_matches_spec(
        {
            **binding,
            "allowedHosts": ["www.irs.gov"],
            "expectedReleaseWindow": {
                "start": "2029-01-01",
                "end": "2029-12-31",
            },
        },
        SPEC,
    )

    for key in SOURCE_BINDING_TEMPLATE_KEYS:
        tampered = copy.deepcopy(binding)
        if key == "transform":
            tampered[key]["factor"] = 2
        else:
            tampered[key] = f"{tampered[key]}-tampered"
        assert not resolve_pending.irs_soi_pub1304_binding_matches_spec(
            tampered, SPEC
        )
    assert not resolve_pending.irs_soi_pub1304_binding_matches_spec(
        {**binding, "unexpected": True}, SPEC
    )


def test_docket_pair_arms_bind_registrable_conditional_contracts() -> None:
    """Every docket arm builds a v3 contract carrying its conditional."""

    entry = docket_entry()
    pair = entry["conditionalPair"]
    arms = pair["arms"]
    assert len(arms) == 2
    contracts = []
    for arm in arms:
        target = {
            "series": entry["series"],
            "period": entry["period"],
            "catalogSlug": arm["catalogSlug"],
            "dataPointId": arm["dataPointId"],
            "conditional": arm["conditional"],
            "conditionId": arm["conditionId"],
            "conditionDeadline": entry["conditionalPair"]["conditionDeadline"],
            **entry["extras"],
        }
        contract = register_targets.build_contract(
            target, register_targets.dt.date(2026, 8, 1)
        )
        assert contract["conditional"] == arm["conditional"]
        assert contract["sourceBinding"]["adapter"] == "irs-soi-pub1304"
        assert contract["sourceBinding"]["expectedReleaseWindow"] == {
            "start": "2029-01-01",
            "end": "2029-12-31",
        }
        assert contract["unit"] == "millions"
        contracts.append(contract)
    assert contracts[0]["dataPointId"] != contracts[1]["dataPointId"]
    assert contracts[0]["conditional"] != contracts[1]["conditional"]
    # The conditional participates in the immutable content hash.
    snapshot = {
        "schemaVersion": register_targets.REGISTRATION_SCHEMA,
        "registeredAtUtc": "2026-08-01T00:00:00Z",
        "targets": [contracts[0]],
        "ledgerPin": {
            "repo": "PolicyEngine/ledger",
            "branch": "codex/thesis-ledger-facts",
            "sha": "0" * 40,
            "jsonlSha256": "0" * 64,
            "lineCount": 168,
        },
    }
    baseline = register_targets.registration_content_hash(snapshot)
    stripped = copy.deepcopy(snapshot)
    del stripped["targets"][0]["conditional"]
    assert register_targets.registration_content_hash(stripped) != baseline


def test_register_rejects_blank_conditional() -> None:
    entry = docket_entry()
    arm = entry["conditionalPair"]["arms"][0]
    target = {
        "series": entry["series"],
        "period": entry["period"],
        "catalogSlug": arm["catalogSlug"],
        "dataPointId": arm["dataPointId"],
        "conditional": "   ",
        "conditionId": arm["conditionId"],
        "conditionDeadline": entry["conditionalPair"]["conditionDeadline"],
        **entry["extras"],
    }
    with pytest.raises(register_targets.RegistrationError, match="conditional"):
        register_targets.build_contract(
            target, register_targets.dt.date(2026, 8, 1)
        )


@pytest.mark.parametrize(
    "year", sorted(SPEC["anchors"]), ids=lambda year: f"ty{year}"
)
def test_real_workbook_fixture_reproduces_the_verified_anchor(year: str) -> None:
    grid, refusal = resolve_pending.irs_soi_pub1304_grid(
        fixture_bytes(year), SPEC
    )
    assert refusal is None
    count, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(grid, SPEC)
    assert refusal is None
    assert count == SPEC["anchors"][year]


def test_grid_extraction_fails_closed_on_garbage_and_renamed_sheets() -> None:
    grid, refusal = resolve_pending.irs_soi_pub1304_grid(b"not a workbook", SPEC)
    assert grid is None
    assert "parse failed" in refusal

    renamed = dict(SPEC, sheet_name="TBL99")
    grid, refusal = resolve_pending.irs_soi_pub1304_grid(
        fixture_bytes("2023"), renamed
    )
    assert grid is None
    assert "TBL99" in refusal and "extend the adapter" in refusal


def synthetic_grid() -> list[list[object]]:
    grid = [["" for _ in range(6)] for _ in range(14)]
    grid[4][3] = "Refundable child tax credit\nor additional child tax credit"
    grid[6][3] = "Number of\nreturns"
    grid[9][0] = "All returns, total"
    grid[9][3] = 17626084.0
    return grid


def test_synthetic_grid_parses_and_each_guard_fails_closed() -> None:
    count, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        synthetic_grid(), SPEC
    )
    assert (count, refusal) == (17626084.0, None)

    ambiguous = synthetic_grid()
    ambiguous[3][5] = "Additional child tax credit"
    _, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        ambiguous, SPEC
    )
    assert "exactly one concept header" in refusal

    missing_header = synthetic_grid()
    missing_header[4][3] = "Child tax credit"
    _, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        missing_header, SPEC
    )
    assert "exactly one concept header" in refusal

    no_subheader = synthetic_grid()
    no_subheader[6][3] = "Amount"
    _, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        no_subheader, SPEC
    )
    assert "Number of returns" in refusal

    no_row = synthetic_grid()
    no_row[9][0] = "All returns"
    _, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(no_row, SPEC)
    assert "row" in refusal

    duplicate_row = synthetic_grid()
    duplicate_row[11][0] = "All returns, total"
    _, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        duplicate_row, SPEC
    )
    assert "found 2" in refusal

    fractional = synthetic_grid()
    fractional[9][3] = 17626084.5
    _, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        fractional, SPEC
    )
    assert "positive whole number" in refusal

    textual = synthetic_grid()
    textual[9][3] = "17,626,084"
    _, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(textual, SPEC)
    assert "positive whole number" in refusal


def test_offset_and_refundable_portion_columns_never_match() -> None:
    """The longer Table 3.3 sibling labels must not satisfy the exact match."""

    for sibling in (
        "Refundable child tax credit or additional child tax credit "
        "used to offset other taxes",
        "Refundable child tax credit or additional child tax credit "
        "refundable portion",
        "Additional child tax credit used to offset other taxes",
        "Additional child tax credit refundable portion",
    ):
        grid = synthetic_grid()
        grid[4][3] = sibling
        _, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(grid, SPEC)
        assert "exactly one concept header" in refusal


def test_fetch_year_forms_official_urls_and_handles_absence(monkeypatch) -> None:
    fetched: list[str] = []

    def fake_http_get(url, *, allowed_hosts, timeout=120):
        fetched.append(url)
        raise OSError("HTTP 404")

    monkeypatch.setattr(resolve_pending, "http_get", fake_http_get)
    count, raw, url, _, refusal = resolve_pending.irs_soi_pub1304_fetch_year(
        SPEC, "2027"
    )
    assert (count, raw, refusal) == (None, None, None)
    assert fetched == [
        "https://www.irs.gov/pub/irs-soi/27in33ar.xls",
        "https://www.irs.gov/pub/irs-soi/27in33ar.xlsx",
    ]
    assert url.endswith("27in33ar.xls")

    _, _, _, _, refusal = resolve_pending.irs_soi_pub1304_fetch_year(
        SPEC, "not-a-year"
    )
    assert "tax year must be YYYY" in refusal


def test_fetch_year_refuses_a_format_change_instead_of_guessing(
    monkeypatch,
) -> None:
    def fake_http_get(url, *, allowed_hosts, timeout=120):
        if url.endswith(".xls"):
            raise OSError("HTTP 404")
        return b"xlsx-bytes", "2029-09-01T00:00:00Z", url

    monkeypatch.setattr(resolve_pending, "http_get", fake_http_get)
    count, raw, url, _, refusal = resolve_pending.irs_soi_pub1304_fetch_year(
        SPEC, "2027"
    )
    assert count is None and raw is None
    assert url.endswith("27in33ar.xlsx")
    assert "extend the adapter" in refusal


def test_fetch_year_parses_real_bytes_end_to_end(monkeypatch) -> None:
    def fake_http_get(url, *, allowed_hosts, timeout=120):
        assert allowed_hosts == SPEC["allowed_hosts"]
        assert url == "https://www.irs.gov/pub/irs-soi/23in33ar.xls"
        return fixture_bytes("2023"), "2026-08-01T00:00:00Z", url

    monkeypatch.setattr(resolve_pending, "http_get", fake_http_get)
    count, raw, url, retrieved_at, refusal = (
        resolve_pending.irs_soi_pub1304_fetch_year(SPEC, "2023")
    )
    assert refusal is None
    assert count == SPEC["anchors"]["2023"]
    assert raw == fixture_bytes("2023")
    assert retrieved_at == "2026-08-01T00:00:00Z"


def test_anchor_admission_rejects_placeholders_and_bad_values() -> None:
    assert resolve_pending.irs_soi_pub1304_verified_anchors(SPEC) == {
        "2020": 19119249.0,
        "2021": 37771612.0,
        "2022": 18076696.0,
        "2023": 17626084.0,
    }
    unarmed = dict(SPEC, anchor_status="PENDING")
    assert resolve_pending.irs_soi_pub1304_verified_anchors(unarmed) is None
    for bad_anchors in (
        {"2022": 18076696, "2023": 17626084},
        {"2022": 18076696, "2023": 17626084, "TY2021": 37771612},
        {"2021": 37771612, "2022": 18076696, "2023": 17626084.5},
        {"2021": 37771612, "2022": 18076696, "2023": True},
        {"2021": 37771612, "2022": 18076696, "2023": -1},
    ):
        spec = dict(SPEC, anchors=bad_anchors)
        assert resolve_pending.irs_soi_pub1304_verified_anchors(spec) is None


def test_anchor_comparison_requires_exact_values() -> None:
    anchors = resolve_pending.irs_soi_pub1304_verified_anchors(SPEC)
    live = {year: float(value) for year, value in SPEC["anchors"].items()}
    assert resolve_pending.irs_soi_pub1304_anchor_mismatches(live, anchors) == []
    live["2023"] = live["2023"] + 1
    problems = resolve_pending.irs_soi_pub1304_anchor_mismatches(live, anchors)
    assert len(problems) == 1 and "2023" in problems[0]
    live.pop("2021")
    problems = resolve_pending.irs_soi_pub1304_anchor_mismatches(live, anchors)
    assert any("2021=missing" in problem for problem in problems)


def test_family_exclusivity_blocks_generic_url_registrations() -> None:
    registration = {"contract": {"sourceBinding": {"adapter": "generic-url"}}}
    assert (
        resolve_pending.binding_adapter_mismatch("irs_soi_pub1304", registration)
        == "generic-url"
    )
    registration = {
        "contract": {"sourceBinding": {"adapter": "irs-soi-pub1304"}}
    }
    assert (
        resolve_pending.binding_adapter_mismatch("irs_soi_pub1304", registration)
        is None
    )


def test_spec_builds_a_year_fact_in_millions() -> None:
    row = resolve_pending.generic_fact(
        "irs.actc.total_claims.2027.first_print.current_law",
        SPEC,
        "year",
        "2027",
        17.6,
        resolve_pending.dt.date(2029, 12, 31),
        SPEC["source_url"],
        "https://www.irs.gov/pub/irs-soi/27in33ar.xls",
    )
    assert row["measure"]["concept"] == "irs.actc.total_claims"
    assert row["measure"]["unit"] == "millions"
    assert row["period"] == {"type": "year", "value": "2027"}
    assert row["value"] == 17.6
    assert row["source"]["source_name"] == "irs_soi"
    assert "archived" in row["measure"]["concept_evidence_notes"]


def test_fetch_year_refuses_wrong_year_workbook_and_redirects(
    monkeypatch,
) -> None:
    # A mirror/redirect serving the wrong tax year's real workbook must be
    # refused: headers, anchors, and integer checks are identical across
    # years, so identity comes from the printed title and official filename.
    def serve_2023_for_2027(url, *, allowed_hosts, timeout=120):
        return fixture_bytes("2023"), "2029-09-01T00:00:00Z", url

    monkeypatch.setattr(resolve_pending, "http_get", serve_2023_for_2027)
    count, raw, _, _, refusal = resolve_pending.irs_soi_pub1304_fetch_year(
        SPEC, "2027"
    )
    assert count is None and raw is not None
    assert "does not name 'tax year 2027'" in refusal

    def redirect_to_other_file(url, *, allowed_hosts, timeout=120):
        return (
            fixture_bytes("2023"),
            "2026-08-01T00:00:00Z",
            "https://www.irs.gov/pub/irs-soi/23in33ar.xls",
        )

    monkeypatch.setattr(resolve_pending, "http_get", redirect_to_other_file)
    count, raw, _, _, refusal = resolve_pending.irs_soi_pub1304_fetch_year(
        SPEC, "2022"
    )
    assert count is None
    assert "is not the tax year's official '22in33ar.xls'" in refusal


def test_identity_check_accepts_every_fixture_year() -> None:
    for year in sorted(SPEC["anchors"]):
        grid, refusal = resolve_pending.irs_soi_pub1304_grid(
            fixture_bytes(year), SPEC
        )
        assert refusal is None
        url = f"https://www.irs.gov/pub/irs-soi/{int(year) % 100:02d}in33ar.xls"
        assert (
            resolve_pending.irs_soi_pub1304_identity_refusal(grid, url, year)
            is None
        )


def test_registered_transform_is_exact_with_no_extra_rounding() -> None:
    # The recorded observation is exactly count * 1e-06 — the operation the
    # content-hashed transform names — never a further rounding step.
    factor = resolve_pending.IRS_SOI_PUB1304_TRANSFORM["factor"]
    assert 17650000 * factor == 17.65
    assert 17626084 * factor == 17.626084
    binding = docket_entry()["extras"]["sourceBinding"]
    assert binding["transform"] == {"operation": "multiply", "factor": factor}


def bindable_arm_contract(arm_index: int = 0) -> dict:
    entry = docket_entry()
    arm = entry["conditionalPair"]["arms"][arm_index]
    target = {
        "series": entry["series"],
        "period": entry["period"],
        "catalogSlug": arm["catalogSlug"],
        "dataPointId": arm["dataPointId"],
        "conditional": arm["conditional"],
        "conditionId": arm["conditionId"],
        "conditionDeadline": entry["conditionalPair"]["conditionDeadline"],
        **entry["extras"],
    }
    return register_targets.build_contract(
        target, register_targets.dt.date(2026, 8, 1)
    )


def test_bind_reauthenticates_conditional_contracts_against_the_docket() -> None:
    contract = bindable_arm_contract()
    entry = docket_entry()
    stamp = "2026-08-01T00:00:00Z"
    # The committed entry still regenerates the contract exactly: passes.
    register_targets.require_conditional_docket_template(
        contract, [entry], stamp
    )

    with pytest.raises(
        register_targets.RegistrationError, match="exactly one committed"
    ):
        register_targets.require_conditional_docket_template(contract, [], stamp)

    removed = docket_entry()
    del removed["conditionalPair"]
    with pytest.raises(
        register_targets.RegistrationError, match="no two-arm conditionalPair"
    ):
        register_targets.require_conditional_docket_template(
            contract, [removed], stamp
        )

    sibling_removed = docket_entry()
    sibling_removed["conditionalPair"]["arms"].pop()
    with pytest.raises(
        register_targets.RegistrationError, match="no two-arm conditionalPair"
    ):
        register_targets.require_conditional_docket_template(
            contract, [sibling_removed], stamp
        )

    for mutate, pattern in (
        (
            lambda e: e["conditionalPair"]["arms"][0].update(
                conditional="different premise"
            ),
            "no longer regenerates the registered",
        ),
        (
            lambda e: e["conditionalPair"]["arms"][0].update(
                conditionId="cond.other.id"
            ),
            "no longer regenerates the registered",
        ),
        (
            lambda e: e["conditionalPair"].update(conditionDeadline="2027-06-30"),
            "no longer regenerates the registered",
        ),
        (
            lambda e: e["extras"].update(targetUnit="count"),
            "no longer regenerates the registered",
        ),
        (
            lambda e: e["extras"].update(
                expectedReleaseWindow={"start": "2029-02-01", "end": "2029-12-31"}
            ),
            "no longer regenerates the registered",
        ),
        (
            lambda e: e["extras"]["sourceBinding"].update(
                sourceUrl="https://www.irs.gov/other"
            ),
            "no longer regenerates the registered",
        ),
        (lambda e: e.update(period="2028"), "no longer regenerates"),
        (
            lambda e: e["conditionalPair"].update(conditionDeadline="someday"),
            "no longer regenerates a valid",
        ),
        (
            lambda e: e["conditionalPair"]["arms"][0].update(
                conditional=e["conditionalPair"]["arms"][1]["conditional"]
            ),
            "malformed or non-distinct",
        ),
    ):
        drifted = docket_entry()
        mutate(drifted)
        with pytest.raises(register_targets.RegistrationError, match=pattern):
            register_targets.require_conditional_docket_template(
                contract, [drifted], stamp
            )


def test_bind_blocks_every_unconditional_claim_on_a_conditional_series() -> None:
    entry = docket_entry()
    arm = entry["conditionalPair"]["arms"][0]
    # A series whose committed entry carries a conditionalPair is
    # conditional-only: neither an arm's reserved slug NOR a fresh slug
    # (even reusing a reserved dataPointId) may register unconditionally.
    for slug, data_point_id in (
        (arm["catalogSlug"], arm["dataPointId"]),
        ("some-fresh-unconditional-slug", arm["dataPointId"]),
        ("some-fresh-unconditional-slug", "irs.actc.total_claims.2027"),
    ):
        target = {
            "series": entry["series"],
            "period": entry["period"],
            "catalogSlug": slug,
            "dataPointId": data_point_id,
            **entry["extras"],
        }
        contract = register_targets.build_contract(
            target, register_targets.dt.date(2026, 8, 1)
        )
        assert "conditional" not in contract
        with pytest.raises(
            register_targets.RegistrationError, match="conditional-only"
        ):
            register_targets.require_conditional_docket_template(
                contract, [entry]
            )
    # Unconditional contracts for ordinary series stay untouched.
    register_targets.require_conditional_docket_template(
        contract, [{"series": entry["series"], "extras": entry["extras"]}]
    )


def test_bind_reauthenticates_the_full_batch_target_run_context() -> None:
    entry = docket_entry()
    arm = entry["conditionalPair"]["arms"][0]
    batch_target = {
        "series": entry["series"],
        "period": entry["period"],
        "catalogSlug": arm["catalogSlug"],
        "dataPointId": arm["dataPointId"],
        "conditional": arm["conditional"],
        "conditionId": arm["conditionId"],
        "conditionDeadline": entry["conditionalPair"]["conditionDeadline"],
        **entry["extras"],
        # Registration enrichment keys are ignored by the check.
        "registrationState": "preregistered",
        "targetContentHash": "0" * 64,
    }
    contract = bindable_arm_contract()
    stamp = "2026-08-01T00:00:00Z"
    register_targets.require_conditional_docket_template(
        contract, [entry], stamp, batch_target=batch_target
    )
    # Committed drift in run-relevant extras OUTSIDE the contract
    # (resolutionDate, anchors) must fail against the batch target.
    for mutate in (
        lambda e: e["extras"].update(resolutionDate="2030-12-31"),
        lambda e: e["extras"]["anchors"].update({"2023": 99.9}),
    ):
        drifted = docket_entry()
        mutate(drifted)
        with pytest.raises(
            register_targets.RegistrationError,
            match="no longer generates the batch target",
        ):
            register_targets.require_conditional_docket_template(
                contract, [drifted], stamp, batch_target=batch_target
            )


def test_contract_requires_condition_identity_and_deadline() -> None:
    entry = docket_entry()
    arm = entry["conditionalPair"]["arms"][0]
    base = {
        "series": entry["series"],
        "period": entry["period"],
        "catalogSlug": arm["catalogSlug"],
        "dataPointId": arm["dataPointId"],
        "conditional": arm["conditional"],
        "conditionId": arm["conditionId"],
        "conditionDeadline": entry["conditionalPair"]["conditionDeadline"],
        **entry["extras"],
    }
    contract = register_targets.build_contract(
        base, register_targets.dt.date(2026, 8, 1)
    )
    assert contract["conditionId"] == arm["conditionId"]
    assert contract["conditionDeadline"] == "2027-12-31"

    for strip in ("conditionId", "conditionDeadline"):
        broken = dict(base)
        del broken[strip]
        with pytest.raises(register_targets.RegistrationError):
            register_targets.build_contract(
                broken, register_targets.dt.date(2026, 8, 1)
            )
    late = dict(base, conditionDeadline="2029-06-01")
    with pytest.raises(
        register_targets.RegistrationError, match="precede the expected release"
    ):
        register_targets.build_contract(
            late, register_targets.dt.date(2026, 8, 1)
        )
