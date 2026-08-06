"""IRS SOI Publication 1304 Table 3.3 adapter (thesis#106).

The fixtures under tests/fixtures/irs_soi_pub1304/ are the REAL official
workbooks fetched from www.irs.gov on 2026-08-01 (SHA-256 pins in
docs/anchor-verifications.md), so the parse path is armed against the
artifact IRS actually publishes — including the TY2020 pre-ARPA column
label — and every integrator-verified anchor value reproduces from bytes.
"""

from __future__ import annotations

import copy
import hashlib
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
CLEAN_VEHICLE_SERIES = "irs.soi.credit_30d.total_claims"
CLEAN_VEHICLE_SPEC = resolve_pending.IRS_SOI_PUB1304_ADAPTERS[
    CLEAN_VEHICLE_SERIES
]
CLEAN_VEHICLE_AMOUNT_SERIES = "irs.soi.credit_30d.total_credit_amount"
CLEAN_VEHICLE_AMOUNT_SPEC = resolve_pending.IRS_SOI_PUB1304_ADAPTERS[
    CLEAN_VEHICLE_AMOUNT_SERIES
]
ACTC_AMOUNT_SERIES = "irs.actc.total_credit_amount"
ACTC_AMOUNT_SPEC = resolve_pending.IRS_SOI_PUB1304_ADAPTERS[ACTC_AMOUNT_SERIES]
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "irs_soi_pub1304"
FIXTURE_PINS = {
    "2020": (
        103424,
        "7abb8cf1f6f124e1ef481db562d622f46155effe98dad72bd82d0844996dabaa",
    ),
    "2021": (
        113664,
        "b8e3e7ca7bc048dca2b554e78359e4944ce429b4a58c5ea9cbc7e39d71f7ea75",
    ),
    "2022": (
        104960,
        "f04012c527c5bf40e412e112597038d70fd79c017d9476c07eebc3b59e3766a4",
    ),
    "2023": (
        105472,
        "e749d3e9636d9784e2a5e8639f49ce5389a4ca0aaeedca6c671cee0b71264c04",
    ),
}


def fixture_bytes(year: str) -> bytes:
    return (FIXTURE_ROOT / f"{int(year) % 100:02d}in33ar.xls").read_bytes()


@pytest.mark.parametrize("year", sorted(FIXTURE_PINS))
def test_workbook_fixture_bytes_match_reviewed_pins(year: str) -> None:
    raw = fixture_bytes(year)
    expected_bytes, expected_sha256 = FIXTURE_PINS[year]
    assert len(raw) == expected_bytes
    assert hashlib.sha256(raw).hexdigest() == expected_sha256


def docket_entry(series: str = SERIES) -> dict:
    docket = json.loads((ROOT / "scripts" / "docket_series.json").read_text())
    return next(e for e in docket["series"] if e["series"] == series)


@pytest.mark.parametrize(
    "series",
    [
        SERIES,
        CLEAN_VEHICLE_SERIES,
        CLEAN_VEHICLE_AMOUNT_SERIES,
        ACTC_AMOUNT_SERIES,
    ],
)
def test_irs_soi_adapter_and_docket_share_the_exact_seven_key_binding(
    series: str,
) -> None:
    spec = resolve_pending.IRS_SOI_PUB1304_ADAPTERS[series]
    binding = docket_entry(series)["extras"]["sourceBinding"]

    assert "irs-soi-pub1304" in register_targets.SOURCE_ADAPTERS
    assert prospect_targets._source_binding_errors(binding) == []
    assert set(binding) == SOURCE_BINDING_TEMPLATE_KEYS
    assert resolve_pending.irs_soi_pub1304_binding_template(spec) == binding
    assert resolve_pending.irs_soi_pub1304_binding_matches_spec(binding, spec)
    assert resolve_pending.irs_soi_pub1304_binding_matches_spec(
        {
            **binding,
            "allowedHosts": ["www.irs.gov"],
            "expectedReleaseWindow": {
                "start": "2029-01-01",
                "end": "2029-12-31",
            },
        },
        spec,
    )

    for key in SOURCE_BINDING_TEMPLATE_KEYS:
        tampered = copy.deepcopy(binding)
        if key == "transform":
            tampered[key]["factor"] = 2
        else:
            tampered[key] = f"{tampered[key]}-tampered"
        assert not resolve_pending.irs_soi_pub1304_binding_matches_spec(
            tampered, spec
        )
    assert not resolve_pending.irs_soi_pub1304_binding_matches_spec(
        {**binding, "unexpected": True}, spec
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
        assert contract["resolutionDateBasis"] == "resolve-by-bound"
        assert contract["resolutionDate"] == "2029-12-31"
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


def test_legacy_irs_contract_reauthenticates_under_declared_bounded_basis() -> None:
    contract = bindable_arm_contract()
    contract.pop("resolutionDateBasis")
    contract.pop("resolutionDate")

    target = {
        "resolutionDateBasis": "resolve-by-bound",
        "resolutionDate": "2029-12-31",
        "expectedReleaseWindow": contract["sourceBinding"][
            "expectedReleaseWindow"
        ],
        "sourceBinding": contract["sourceBinding"],
    }
    register_targets.validate_target_resolution_projection(
        contract, target, label=contract["dataPointId"]
    )

    register_targets.require_conditional_docket_template(
        contract, [docket_entry()], "2026-08-01T00:00:00Z"
    )


def test_legacy_bounded_compatibility_is_scoped_to_the_known_irs_ids() -> None:
    entry = docket_entry()
    entry["series"] = "agency.legacy.rate"
    entry["conditionalPair"]["arms"][0]["dataPointId"] = (
        "agency.legacy.rate.2027.first_print.enacted"
    )
    entry["conditionalPair"]["arms"][1]["dataPointId"] = (
        "agency.legacy.rate.2027.first_print.current_law"
    )
    entry["extras"]["sourceBinding"]["adapter"] = "generic-url"
    arm = entry["conditionalPair"]["arms"][0]
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
    legacy = register_targets.build_contract(
        target, register_targets.dt.date(2026, 8, 1)
    )
    legacy.pop("resolutionDateBasis")
    legacy.pop("resolutionDate")

    with pytest.raises(register_targets.RegistrationError) as error:
        register_targets.require_conditional_docket_template(
            legacy, [entry], "2026-08-01T00:00:00Z"
        )
    assert str(error.value) == (
        "committed docket entry no longer regenerates the registered "
        "conditional contract (drifted: ['resolutionDate', "
        "'resolutionDateBasis']): "
        "agency.legacy.rate.2027.first_print.enacted in series "
        "agency.legacy.rate"
    )


@pytest.mark.parametrize(
    "ref", sorted(register_targets.LEGACY_BOUNDED_CONDITIONAL_IDS)
)
def test_irs_resolution_basis_keeps_legacy_and_future_gating_identical(
    ref: str,
) -> None:
    legacy = {
        "contract": {
            "dataPointId": ref,
            "sourceBinding": {"adapter": "irs-soi-pub1304"},
        }
    }
    future = {
        "contract": {
            "dataPointId": ref,
            "resolutionDateBasis": "resolve-by-bound",
            "sourceBinding": {"adapter": "irs-soi-pub1304"},
        }
    }

    assert resolve_pending.effective_resolution_date_basis(ref, legacy, SPEC) == (
        "resolve-by-bound",
        None,
    )
    assert resolve_pending.effective_resolution_date_basis(ref, future, SPEC) == (
        "resolve-by-bound",
        None,
    )
    assert resolve_pending.effective_resolution_date_basis(ref, None, {}) == (
        "release-calendar",
        None,
    )
    basis, refusal = resolve_pending.effective_resolution_date_basis(
        ref,
        {"contract": {"resolutionDateBasis": "release-calendar"}},
        SPEC,
    )
    assert basis is None
    assert refusal == (
        "registered basis 'release-calendar' disagrees with adapter basis "
        "'resolve-by-bound'"
    )
    basis, refusal = resolve_pending.effective_resolution_date_basis(
        ref,
        {"contract": {"resolutionDateBasis": ["resolve-by-bound"]}},
        {},
    )
    assert basis is None
    assert refusal == "unsupported registered basis ['resolve-by-bound']"


@pytest.mark.parametrize(
    ("ref", "adapter", "spec"),
    [
        (
            "agency.unrelated.rate.2027.first_print.current_law",
            "irs-soi-pub1304",
            SPEC,
        ),
        (
            "irs.actc.total_claims.2027.first_print.current_law",
            "generic-url",
            SPEC,
        ),
    ],
)
def test_absent_basis_cannot_inherit_bounded_outside_exact_legacy_irs_contract(
    ref: str, adapter: str, spec: dict
) -> None:
    registration = {
        "contract": {
            "dataPointId": ref,
            "sourceBinding": {"adapter": adapter},
        }
    }

    assert resolve_pending.effective_resolution_date_basis(
        ref, registration, spec
    ) == (
        None,
        "absent registered basis defaults to 'release-calendar'; adapter "
        "basis 'resolve-by-bound' may be inherited only by the two legacy "
        "IRS-SOI targets with adapter 'irs-soi-pub1304': "
        f"{ref}",
    )


def test_irs_resolve_by_window_verdicts_remain_byte_identical() -> None:
    ref = "irs.actc.total_claims.2027.first_print.current_law"
    window = {"start": "2029-01-01", "end": "2029-12-31"}
    registration = {
        "contract": {
            "sourceBinding": {
                **resolve_pending.irs_soi_pub1304_binding_template(SPEC),
                "allowedHosts": ["www.irs.gov"],
                "expectedReleaseWindow": window,
            }
        }
    }

    assert resolve_pending.bounded_resolution_window_gate(
        ref, resolve_pending.dt.date(2028, 12, 31), window
    ) == (
        "pending",
        f"  RELEASE WINDOW NOT OPEN (deferring): {ref} — opens 2029-01-01",
    )
    assert resolve_pending.bounded_resolution_window_gate(
        ref, resolve_pending.dt.date(2029, 1, 1), window
    ) == ("open", None)
    assert resolve_pending.bounded_resolution_window_gate(
        ref, resolve_pending.dt.date(2030, 1, 1), window
    ) == (
        "missed",
        f"  FIRST-PRINT WINDOW MISSED (refusing): {ref} — registered window "
        "closed 2029-12-31; adapter has no authenticated immutable-artifact "
        "late-capture capability",
    )
    assert resolve_pending.bounded_resolution_window_gate(
        ref,
        resolve_pending.dt.date(2030, 1, 1),
        window,
        registration=registration,
        spec=SPEC,
    ) == ("missed", None)
    assert resolve_pending.bounded_resolution_window_gate(
        ref, resolve_pending.dt.date(2029, 1, 1), None
    ) == (
        "invalid",
        f"  NO REGISTERED RELEASE WINDOW (refusing): {ref}",
    )


def test_immutable_late_capture_capability_requires_exact_irs_binding() -> None:
    binding = {
        **resolve_pending.irs_soi_pub1304_binding_template(SPEC),
        "allowedHosts": ["www.irs.gov"],
        "expectedReleaseWindow": {
            "start": "2029-01-01",
            "end": "2029-12-31",
        },
    }
    registration = {"contract": {"sourceBinding": binding}}

    assert resolve_pending.authenticated_late_capture_capability(
        registration, SPEC
    )
    drifted = copy.deepcopy(registration)
    drifted["contract"]["sourceBinding"]["field"] = "neighboring-field"
    assert not resolve_pending.authenticated_late_capture_capability(
        drifted, SPEC
    )
    wrong_hosts = copy.deepcopy(registration)
    wrong_hosts["contract"]["sourceBinding"]["allowedHosts"] = [
        "mirror.example"
    ]
    assert not resolve_pending.authenticated_late_capture_capability(
        wrong_hosts, SPEC
    )
    assert not resolve_pending.authenticated_late_capture_capability(
        registration,
        {**SPEC, "late_capture_capability": True},
    )


def run_main_preflight(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    *,
    spec: dict,
    registration: dict,
) -> str:
    ref = "irs.actc.total_claims.2027.first_print.current_law"
    registration = copy.deepcopy(registration)
    registration["contract"].setdefault("dataPointId", ref)
    forecast = {"resolutionDate": "2029-12-31", "unit": "millions"}
    monkeypatch.setattr(
        resolve_pending,
        "load_thesis_log",
        lambda _url: {"entries": [], "resolutionLinks": []},
    )
    monkeypatch.setattr(resolve_pending, "pending_claims_refs", lambda _log: [])
    monkeypatch.setattr(
        resolve_pending,
        "pending_adapter_refs",
        lambda _log: [
            (
                ref,
                "irs_soi_pub1304",
                spec,
                "year",
                "2027",
                "2029-12-31",
                forecast,
            )
        ],
    )
    monkeypatch.setattr(
        resolve_pending,
        "ledger_state",
        lambda *_args: ("", "blob", "a" * 40),
    )
    monkeypatch.setattr(
        resolve_pending, "registration_contracts", lambda: {ref: registration}
    )
    monkeypatch.setattr(resolve_pending, "utc_now", lambda: "2028-12-31T23:59:59Z")

    def unexpected_fetch(*_args, **_kwargs):
        raise AssertionError("IRS adapter fetched before preflight completed")

    monkeypatch.setattr(resolve_pending, "irs_soi_pub1304_fetch_year", unexpected_fetch)
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])
    assert resolve_pending.main() == 0
    return capsys.readouterr().out


def test_irs_binding_drift_refuses_before_pending_window(monkeypatch, capsys) -> None:
    binding = {
        **resolve_pending.irs_soi_pub1304_binding_template(SPEC),
        "allowedHosts": ["www.irs.gov"],
        "expectedReleaseWindow": {
            "start": "2029-01-01",
            "end": "2029-12-31",
        },
    }
    binding["field"] = "drifted_field"
    output = run_main_preflight(
        monkeypatch,
        capsys,
        spec=SPEC,
        registration={"contract": {"sourceBinding": binding}},
    )
    assert (
        "  BINDING/ADAPTER MISMATCH (refusing, full seven-key registry "
        "drift?): irs.actc.total_claims.2027.first_print.current_law"
        in output.splitlines()
    )
    assert "RELEASE WINDOW NOT OPEN" not in output


def test_irs_unverified_adapter_refuses_before_pending_window(
    monkeypatch, capsys
) -> None:
    spec = {**SPEC, "anchor_status": "PENDING"}
    binding = {
        **resolve_pending.irs_soi_pub1304_binding_template(spec),
        "allowedHosts": ["www.irs.gov"],
        "expectedReleaseWindow": {
            "start": "2029-01-01",
            "end": "2029-12-31",
        },
    }
    output = run_main_preflight(
        monkeypatch,
        capsys,
        spec=spec,
        registration={"contract": {"sourceBinding": binding}},
    )
    assert (
        "  IRS SOI ADAPTER UNVERIFIED (refusing): "
        "irs.actc.total_claims.2027.first_print.current_law — three live "
        "official-source anchors are required"
        in output.splitlines()
    )
    assert "RELEASE WINDOW NOT OPEN" not in output


@pytest.mark.parametrize("explicit_basis", [False, True])
def test_irs_valid_legacy_and_explicit_basis_keep_pending_verdict(
    monkeypatch, capsys, explicit_basis
) -> None:
    binding = {
        **resolve_pending.irs_soi_pub1304_binding_template(SPEC),
        "allowedHosts": ["www.irs.gov"],
        "expectedReleaseWindow": {
            "start": "2029-01-01",
            "end": "2029-12-31",
        },
    }
    contract = {"sourceBinding": binding}
    if explicit_basis:
        contract["resolutionDateBasis"] = "resolve-by-bound"
    output = run_main_preflight(
        monkeypatch,
        capsys,
        spec=SPEC,
        registration={"contract": contract},
    )
    assert (
        "  RELEASE WINDOW NOT OPEN (deferring): "
        "irs.actc.total_claims.2027.first_print.current_law — opens 2029-01-01"
        in output
    )


def test_irs_authenticated_immutable_adapter_records_after_window(
    monkeypatch, capsys
) -> None:
    ref = "irs.actc.total_claims.2027.first_print.current_law"
    window = {"start": "2029-01-01", "end": "2029-12-31"}
    binding = {
        **resolve_pending.irs_soi_pub1304_binding_template(SPEC),
        "allowedHosts": ["www.irs.gov"],
        "expectedReleaseWindow": window,
    }
    registration = {
        "contract": {
            "dataPointId": ref,
            "resolutionDateBasis": "resolve-by-bound",
            "sourceBinding": binding,
        }
    }
    forecast = {"resolutionDate": "2029-12-31", "unit": "millions"}
    monkeypatch.setattr(
        resolve_pending,
        "load_thesis_log",
        lambda _url: {"entries": [], "resolutionLinks": []},
    )
    monkeypatch.setattr(resolve_pending, "pending_claims_refs", lambda _log: [])
    monkeypatch.setattr(
        resolve_pending,
        "pending_adapter_refs",
        lambda _log: [
            (
                ref,
                "irs_soi_pub1304",
                SPEC,
                "year",
                "2027",
                "2029-12-31",
                forecast,
            )
        ],
    )
    monkeypatch.setattr(
        resolve_pending,
        "ledger_state",
        lambda *_args: ("", "blob", "a" * 40),
    )
    monkeypatch.setattr(
        resolve_pending, "registration_contracts", lambda: {ref: registration}
    )
    monkeypatch.setattr(
        resolve_pending, "irs_soi_pub1304_verified_anchors", lambda _spec: {}
    )
    monkeypatch.setattr(
        resolve_pending,
        "irs_soi_pub1304_anchor_mismatches",
        lambda _values, _anchors: [],
    )
    monkeypatch.setattr(
        resolve_pending, "utc_now", lambda: "2030-01-01T00:00:01Z"
    )
    fetches: list[str] = []

    def fake_fetch(spec, year):
        assert spec is SPEC
        fetches.append(year)
        return (
            17_626_084.0,
            b"authenticated-static-workbook",
            "https://www.irs.gov/pub/irs-soi/27in33ar.xls",
            "2030-01-01T00:00:00Z",
            None,
        )

    monkeypatch.setattr(
        resolve_pending, "irs_soi_pub1304_fetch_year", fake_fetch
    )
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])

    assert resolve_pending.main() == 0
    assert fetches == ["2027"]
    output = capsys.readouterr().out
    assert (
        f"  LATE FIRST-PRINT CAPTURE (recording): {ref} — capture completed "
        "2030-01-01, after the registered window closed 2029-12-31"
        in output
    )
    assert f"  resolve {ref} -> 17.626084 millions" in output
    assert "dry-run: would append 1 row(s)" in output


def test_irs_runtime_cache_isolated_by_series_and_year(monkeypatch, capsys) -> None:
    refs = {
        SERIES: f"{SERIES}.2027.first_print.current_law",
        CLEAN_VEHICLE_SERIES: f"{CLEAN_VEHICLE_SERIES}.2027.first_print",
        CLEAN_VEHICLE_AMOUNT_SERIES: (
            f"{CLEAN_VEHICLE_AMOUNT_SERIES}.2027.first_print"
        ),
        ACTC_AMOUNT_SERIES: f"{ACTC_AMOUNT_SERIES}.2027.first_print",
    }
    specs = {
        series: resolve_pending.IRS_SOI_PUB1304_ADAPTERS[series]
        for series in refs
    }
    window = {"start": "2029-01-01", "end": "2029-12-31"}
    registrations = {
        ref: {
            "contract": {
                "dataPointId": ref,
                "resolutionDateBasis": "resolve-by-bound",
                "sourceBinding": {
                    **resolve_pending.irs_soi_pub1304_binding_template(
                        specs[series]
                    ),
                    "allowedHosts": ["www.irs.gov"],
                    "expectedReleaseWindow": window,
                },
            }
        }
        for series, ref in refs.items()
    }
    monkeypatch.setattr(
        resolve_pending,
        "load_thesis_log",
        lambda _url: {"entries": [], "resolutionLinks": []},
    )
    monkeypatch.setattr(resolve_pending, "pending_claims_refs", lambda _log: [])
    monkeypatch.setattr(
        resolve_pending,
        "pending_adapter_refs",
        lambda _log: [
            (
                refs[series],
                "irs_soi_pub1304",
                spec,
                "year",
                "2027",
                "2029-12-31",
                {"resolutionDate": "2029-12-31", "unit": spec["unit"]},
            )
            for series, spec in specs.items()
        ],
    )
    monkeypatch.setattr(
        resolve_pending,
        "ledger_state",
        lambda *_args: ("", "blob", "a" * 40),
    )
    monkeypatch.setattr(
        resolve_pending, "registration_contracts", lambda: registrations
    )
    monkeypatch.setattr(
        resolve_pending, "irs_soi_pub1304_verified_anchors", lambda _spec: {}
    )
    monkeypatch.setattr(
        resolve_pending,
        "irs_soi_pub1304_anchor_mismatches",
        lambda _values, _anchors: [],
    )
    monkeypatch.setattr(
        resolve_pending, "utc_now", lambda: "2029-06-01T00:00:00Z"
    )
    raw_by_series = {
        SERIES: 17_626_084.0,
        CLEAN_VEHICLE_SERIES: 493_953.0,
        CLEAN_VEHICLE_AMOUNT_SERIES: 3_231_102.0,
        ACTC_AMOUNT_SERIES: 34_533_251.0,
    }
    fetches: list[tuple[str, str]] = []

    def fake_fetch(spec, year):
        fetches.append((spec["series_id"], year))
        return (
            raw_by_series[spec["series_id"]],
            f"{spec['series_id']}-bytes".encode(),
            f"https://www.irs.gov/pub/irs-soi/{year[-2:]}in33ar.xls",
            "2029-06-01T00:00:00Z",
            None,
        )

    monkeypatch.setattr(
        resolve_pending, "irs_soi_pub1304_fetch_year", fake_fetch
    )
    monkeypatch.setattr(sys, "argv", ["resolve_pending.py", "--dry-run"])

    assert resolve_pending.main() == 0
    assert fetches == [
        (SERIES, "2027"),
        (CLEAN_VEHICLE_SERIES, "2027"),
        (CLEAN_VEHICLE_AMOUNT_SERIES, "2027"),
        (ACTC_AMOUNT_SERIES, "2027"),
    ]
    output = capsys.readouterr().out
    assert f"resolve {refs[SERIES]} -> 17.626084 millions" in output
    assert f"resolve {refs[CLEAN_VEHICLE_SERIES]} -> 493953.0 count" in output
    assert (
        f"resolve {refs[CLEAN_VEHICLE_AMOUNT_SERIES]} -> "
        "3231.102 usd_millions" in output
    )
    assert (
        f"resolve {refs[ACTC_AMOUNT_SERIES]} -> 34533.251 usd_millions"
        in output
    )
    assert "dry-run: would append 4 row(s)" in output


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


@pytest.mark.parametrize(
    "year",
    sorted(CLEAN_VEHICLE_SPEC["anchors"]),
    ids=lambda year: f"30d-ty{year}",
)
def test_real_workbook_fixture_reproduces_clean_vehicle_claims_anchor(
    year: str,
) -> None:
    grid, refusal = resolve_pending.irs_soi_pub1304_grid(
        fixture_bytes(year), CLEAN_VEHICLE_SPEC
    )
    assert refusal is None
    value, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        grid, CLEAN_VEHICLE_SPEC
    )
    assert refusal is None
    assert value == CLEAN_VEHICLE_SPEC["anchors"][year]


@pytest.mark.parametrize(
    "year",
    sorted(CLEAN_VEHICLE_AMOUNT_SPEC["anchors"]),
    ids=lambda year: f"30d-amount-ty{year}",
)
def test_real_workbook_fixture_reproduces_clean_vehicle_amount_anchor(
    year: str,
) -> None:
    grid, refusal = resolve_pending.irs_soi_pub1304_grid(
        fixture_bytes(year), CLEAN_VEHICLE_AMOUNT_SPEC
    )
    assert refusal is None
    value, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        grid, CLEAN_VEHICLE_AMOUNT_SPEC
    )
    assert refusal is None
    assert value == CLEAN_VEHICLE_AMOUNT_SPEC["anchors"][year]


@pytest.mark.parametrize(
    "year",
    sorted(ACTC_AMOUNT_SPEC["anchors"]),
    ids=lambda year: f"actc-amount-ty{year}",
)
def test_real_workbook_fixture_reproduces_actc_amount_anchor(year: str) -> None:
    grid, refusal = resolve_pending.irs_soi_pub1304_grid(
        fixture_bytes(year), ACTC_AMOUNT_SPEC
    )
    assert refusal is None
    value, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        grid, ACTC_AMOUNT_SPEC
    )
    assert refusal is None
    assert value == ACTC_AMOUNT_SPEC["anchors"][year]


def test_amount_parser_requires_the_printed_thousand_dollar_scale() -> None:
    grid, refusal = resolve_pending.irs_soi_pub1304_grid(
        fixture_bytes("2023"), ACTC_AMOUNT_SPEC
    )
    assert refusal is None
    grid[1][0] = "Money amounts are in dollars."
    value, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        grid, ACTC_AMOUNT_SPEC
    )
    assert value is None
    assert "scale declaration" in refusal

    caveated_grid, refusal = resolve_pending.irs_soi_pub1304_grid(
        fixture_bytes("2023"), ACTC_AMOUNT_SPEC
    )
    assert refusal is None
    caveated_grid[1][0] = (
        "(All figures are estimates based on samples—money amounts are in "
        "thousands of dollars except this table, which is in millions)"
    )
    value, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        caveated_grid, ACTC_AMOUNT_SPEC
    )
    assert value is None
    assert "scale declaration" in refusal

    moved_grid, refusal = resolve_pending.irs_soi_pub1304_grid(
        fixture_bytes("2023"), ACTC_AMOUNT_SPEC
    )
    assert refusal is None
    moved_grid[1][1] = moved_grid[1][0]
    moved_grid[1][0] = ""
    value, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(
        moved_grid, ACTC_AMOUNT_SPEC
    )
    assert value is None
    assert "cell (1, 0)" in refusal


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
    assert "nonnegative whole number" in refusal

    zero = synthetic_grid()
    zero[9][3] = 0
    assert resolve_pending.irs_soi_pub1304_count_from_grid(zero, SPEC) == (
        0.0,
        None,
    )

    negative = synthetic_grid()
    negative[9][3] = -1
    _, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(negative, SPEC)
    assert "nonnegative whole number" in refusal

    textual = synthetic_grid()
    textual[9][3] = "17,626,084"
    _, refusal = resolve_pending.irs_soi_pub1304_count_from_grid(textual, SPEC)
    assert "nonnegative whole number" in refusal


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


def test_fetch_normalized_year_returns_registered_clean_vehicle_unit(
    monkeypatch,
) -> None:
    def fake_http_get(url, *, allowed_hosts, timeout=120):
        assert allowed_hosts == CLEAN_VEHICLE_SPEC["allowed_hosts"]
        assert url == "https://www.irs.gov/pub/irs-soi/23in33ar.xls"
        return fixture_bytes("2023"), "2026-08-06T00:00:00Z", url

    monkeypatch.setattr(resolve_pending, "http_get", fake_http_get)
    value, raw, _, _, refusal = (
        resolve_pending.irs_soi_pub1304_fetch_normalized_year(
            CLEAN_VEHICLE_SPEC, "2023"
        )
    )
    assert refusal is None
    assert value == 493953
    assert raw == fixture_bytes("2023")


def test_fetch_normalized_year_returns_actc_usd_millions(monkeypatch) -> None:
    def fake_http_get(url, *, allowed_hosts, timeout=120):
        assert allowed_hosts == ACTC_AMOUNT_SPEC["allowed_hosts"]
        assert url == "https://www.irs.gov/pub/irs-soi/23in33ar.xls"
        return fixture_bytes("2023"), "2026-08-06T00:00:00Z", url

    monkeypatch.setattr(resolve_pending, "http_get", fake_http_get)
    value, raw, _, _, refusal = (
        resolve_pending.irs_soi_pub1304_fetch_normalized_year(
            ACTC_AMOUNT_SPEC, "2023"
        )
    )
    assert refusal is None
    assert value == 34533.251
    assert raw == fixture_bytes("2023")


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


def test_clean_vehicle_claim_transform_is_identity() -> None:
    assert resolve_pending.irs_soi_pub1304_apply_transform(
        CLEAN_VEHICLE_SPEC, 493953
    ) == 493953
    binding = docket_entry(CLEAN_VEHICLE_SERIES)["extras"]["sourceBinding"]
    assert binding["transform"] == {"operation": "multiply", "factor": 1}


def test_actc_amount_transform_is_exact_with_no_extra_rounding() -> None:
    assert resolve_pending.irs_soi_pub1304_apply_transform(
        ACTC_AMOUNT_SPEC, 34533251
    ) == 34533.251
    binding = docket_entry(ACTC_AMOUNT_SERIES)["extras"]["sourceBinding"]
    assert binding["transform"] == {"operation": "multiply", "factor": 0.001}


def test_clean_vehicle_amount_transform_is_exact_with_no_extra_rounding() -> None:
    assert resolve_pending.irs_soi_pub1304_apply_transform(
        CLEAN_VEHICLE_AMOUNT_SPEC, 3231102
    ) == 3231.102
    binding = docket_entry(CLEAN_VEHICLE_AMOUNT_SERIES)["extras"][
        "sourceBinding"
    ]
    assert binding["transform"] == {"operation": "multiply", "factor": 0.001}


@pytest.mark.parametrize(
    "series",
    [CLEAN_VEHICLE_SERIES, CLEAN_VEHICLE_AMOUNT_SERIES, ACTC_AMOUNT_SERIES],
)
def test_new_docket_anchors_are_exactly_normalized_from_raw_pins(
    series: str,
) -> None:
    spec = resolve_pending.IRS_SOI_PUB1304_ADAPTERS[series]
    entry = docket_entry(series)
    extras = entry["extras"]
    factor = spec["value_transform"]["factor"]
    assert extras["valueScale"] == factor
    assert extras["sourceBinding"]["transform"] == spec["value_transform"]
    assert extras["anchors"] == {
        year: resolve_pending.irs_soi_pub1304_apply_transform(spec, raw)
        for year, raw in spec["anchors"].items()
    }


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
        # Period drift now dies even earlier: the committed arms' ids stop
        # matching <series>.<period>.first_print.<token>.
        (lambda e: e.update(period="2028"), "first_print"),
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


def test_symmetric_run_context_catches_committed_field_deletion() -> None:
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
        "registrationState": "preregistered",
        "registrationCommit": "0" * 40,
    }
    contract = bindable_arm_contract()
    stamp = "2026-08-01T00:00:00Z"
    # DELETING a committed run-context field (not just changing it) must
    # fail: the registry no longer generates the context the run used.
    for missing in ("resolutionDate", "anchors"):
        drifted = docket_entry()
        del drifted["extras"][missing]
        with pytest.raises(
            register_targets.RegistrationError, match=missing
        ):
            register_targets.require_conditional_docket_template(
                contract, [drifted], stamp, batch_target=batch_target
            )


def test_conditional_only_rule_survives_duplicate_series_ambiguity() -> None:
    entry = docket_entry()
    plain = {"series": entry["series"], "cadence": "annual"}
    target = {
        "series": entry["series"],
        "period": entry["period"],
        "catalogSlug": "some-fresh-unconditional-slug",
        "dataPointId": "irs.actc.total_claims.2027",
        **entry["extras"],
    }
    contract = register_targets.build_contract(
        target, register_targets.dt.date(2026, 8, 1)
    )
    # A duplicate-series registry state (however it arose) must not launder
    # an unconditional contract past the conditional-only rule.
    for matches in ([entry, plain], [plain, entry]):
        with pytest.raises(
            register_targets.RegistrationError, match="conditional-only"
        ):
            register_targets.require_conditional_docket_template(
                contract, matches
            )


def test_reauthentication_rejects_committed_registry_malformations() -> None:
    contract = bindable_arm_contract()
    stamp = "2026-08-01T00:00:00Z"
    restated = docket_entry()
    restated["extras"]["conditional"] = "override"
    with pytest.raises(
        register_targets.RegistrationError, match="restate reserved"
    ):
        register_targets.require_conditional_docket_template(
            contract, [restated], stamp
        )
    mislabeled = docket_entry()
    mislabeled["conditionalPair"]["arms"][1]["dataPointId"] = (
        "irs.actc.total_claims.2028.first_print.current_law"
    )
    with pytest.raises(
        register_targets.RegistrationError, match="first_print"
    ):
        register_targets.require_conditional_docket_template(
            contract, [mislabeled], stamp
        )
