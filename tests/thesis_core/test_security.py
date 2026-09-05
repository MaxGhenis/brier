"""Credential hygiene for the shared thesis_core.security module.

`tests/test_thesis_analyst_env_hygiene.py` still owns the end-to-end legacy
proof that a recorded thesis.analyst run seals clean bytes. These tests own the
shared implementation: the moved primitives are the same objects the runner
uses, the new key-aware/URL/header redaction closes the gap the value-wise text
scrub could not see, and clean content passes through byte-identical so
evidence is never reshaped by being scrubbed.

Planted secrets are assembled by concatenation so no push-protection-shaped
literal ever exists in the repository.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from thesis_core import security

ROOT = Path(__file__).resolve().parents[2]

PLANTED = {
    "anthropic": "sk-ant-" + "planted-core-security-2026-09-04",
    "openai_legacy": "sk-" + "planted0123456789planted",
    "github_pat": "ghp_" + "Planted0123456789abc",
    "google": "AIza" + "PlantedGoogleKey0123",
    "jwt": "eyJhbGciOi" + "JIUzI1NiJ9.planted.signature",
    "aws": "AKIA" + "PLANTED0123456",
    # Opaque values that match no token format and no NAME=value shape: only
    # key-aware redaction can find these.
    "opaque_key": "census-planted-" + "opaque-2026",
    "opaque_token": "bea-planted-" + "opaque-2026",
    "opaque_password": "planted-" + "passphrase-2026",
}

REDACTED = security.REDACTED_PLACEHOLDER


def assert_no_planted(rendered: str) -> None:
    for name, value in PLANTED.items():
        assert value not in rendered, f"{name} survived redaction"


# --- The move is a move, not a copy ------------------------------------------


def test_runner_reexports_the_shared_implementation():
    """The legacy runner must scrub with these exact objects, not a copy."""
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        import run_thesis_analyst as runner
    finally:
        if sys.path[0] == str(ROOT / "scripts"):
            sys.path.pop(0)

    for name in (
        "agent_subprocess_env",
        "redact_text",
        "redact_json_value",
        "redact_stream_line",
        "redact_stream_text",
        "redact_response_text",
        "redact_url",
        "redact_headers",
        "redact_value",
        "is_credential_key",
    ):
        assert getattr(runner, name) is getattr(security, name), name
    for name in (
        "AGENT_ENV_ALLOWLIST",
        "REDACTED_PLACEHOLDER",
        "ENV_SECRET_ASSIGNMENT_RE",
        "JSON_SECRET_FIELD_RE",
        "SECRET_TOKEN_RE",
    ):
        assert getattr(runner, name) is getattr(security, name), name


def test_agent_env_allowlist_is_unchanged_and_holds_no_credential_name():
    assert security.AGENT_ENV_ALLOWLIST == (
        "PATH",
        "HOME",
        "TERM",
        "SHELL",
        "TMPDIR",
        "LANG",
        "LC_ALL",
        "LC_CTYPE",
        "CODEX_HOME",
    )
    assert not [
        name
        for name in security.AGENT_ENV_ALLOWLIST
        if security.is_credential_key(name)
    ]


def test_agent_subprocess_env_is_an_allowlist(monkeypatch):
    monkeypatch.setenv("EVIL_PLANTED_API_KEY", PLANTED["opaque_key"])
    monkeypatch.setenv("PATH", "/usr/bin")
    monkeypatch.setenv("CODEX_HOME", "/tmp/lane")
    env = security.agent_subprocess_env()
    assert "EVIL_PLANTED_API_KEY" not in env
    assert set(env) <= set(security.AGENT_ENV_ALLOWLIST)
    assert env["PATH"] == "/usr/bin"
    assert security.agent_subprocess_env({"CODEX_HOME": "/x"})["CODEX_HOME"] == "/x"
    assert_no_planted(json.dumps(env))


def test_module_imports_without_optional_core_dependencies():
    """Adapters and the legacy runner import this without the `core` extra."""
    probe = (
        "import sys, importlib;"
        "sys.path.insert(0, %r);"
        "importlib.import_module('thesis_core.security');"
        "loaded = sorted(m for m in sys.modules "
        "if m.split('.')[0] in {'pydantic','psycopg','fastapi','uvicorn','numpy'});"
        "print(loaded)" % str(ROOT)
    )
    completed = subprocess.run(
        [sys.executable, "-I", "-c", probe],
        capture_output=True,
        text=True,
        check=True,
        cwd="/",
    )
    assert completed.stdout.strip() == "[]"


# --- Name classification ------------------------------------------------------


@pytest.mark.parametrize(
    "name",
    [
        "api_key",
        "API-key",
        "apiKey",
        "APIKey",
        "APIKEY",
        "X-Api-Key",
        "ANTHROPIC_API_KEY",
        "CENSUS_DATA_API_KEY",
        "AWS_ACCESS_KEY_ID",
        "LEDGER_PRODUCER_SIGNING_KEY",
        "access_token",
        "accessToken",
        "refresh_token",
        "id_token",
        "token",
        "SLACK_BOT_TOKEN",
        "password",
        "Passwd",
        "passphrase",
        "secret",
        "client_secret",
        "Authorization",
        "authorization",
        "Cookie",
        "Set-Cookie",
        "cookies",
        "credentials",
        "UserID",
        "userId",
        "user_id",
        "userid",
        "key",
        "ocp-apim-subscription-key",
        "x-amz-security-token",
        "authToken",
    ],
)
def test_credential_shaped_names(name):
    assert security.is_credential_key(name), name


@pytest.mark.parametrize(
    "name",
    [
        # Usage counts, not credentials.
        "tokens",
        "input_tokens",
        "output_tokens",
        # SDMX/series identifiers.
        "dataKey",
        "seriesId",
        "dataflowIdentifier",
        "keys",
        # Public RFC 3161 witness evidence in records/.
        "tokenPath",
        "tokenSha256",
        "maxTokenLeadSeconds",
        "tokenType",
        # A non-secret provenance label existing traces already record.
        "auth",
        "authMethod",
        "author",
        # Correlation identifiers.
        "session_id",
        "account_id",
        "requestId",
        # Ordinary transport/metadata names.
        "content-type",
        "measurement_period",
        "pointEstimate",
        "",
    ],
)
def test_non_credential_names_survive(name):
    assert not security.is_credential_key(name), name


def test_adapter_declared_names_are_honored_ignoring_separators_and_case():
    assert not security.is_credential_key("registration")
    assert security.is_credential_key("registration", ["REGISTRATION"])
    assert security.is_credential_key("data_key", ["dataKey"])
    assert security.is_credential_key("DataKey", ["data-key"])


def test_credential_key_words_splits_every_naming_convention():
    assert security.credential_key_words("UserID") == ("user", "id")
    assert security.credential_key_words("X-Api-Key") == ("x", "api", "key")
    assert security.credential_key_words("ANTHROPIC_API_KEY") == (
        "anthropic",
        "api",
        "key",
    )
    assert security.credential_key_words("tokenSha256") == ("token", "sha256")


# --- Key-aware JSON redaction -------------------------------------------------


def test_opaque_credential_under_a_credential_key_is_redacted():
    """The gap the value-wise text scrub could not see."""
    payload = {"api_key": PLANTED["opaque_key"]}
    assert security.redact_text(PLANTED["opaque_key"]) == PLANTED["opaque_key"]
    redacted = security.redact_value(payload)
    assert redacted == {"api_key": REDACTED}
    assert_no_planted(json.dumps(redacted))
    # The legacy entry point shares the implementation.
    assert security.redact_json_value(payload) == redacted


def test_key_aware_redaction_reaches_nested_objects_and_arrays():
    payload = {
        "request": {
            "url": "https://apps.bea.gov/api/data",
            "params": [
                {"name": "method", "value": "GetData"},
                {"UserID": PLANTED["opaque_key"]},
            ],
            "headers": {"Authorization": "Bearer " + PLANTED["opaque_token"]},
        },
        "auth": "codex-cli-subscription",
        "usage": {"input_tokens": 7, "output_tokens": 3},
        "credentials": {"nested": {"deeper": PLANTED["opaque_password"]}},
    }
    redacted = security.redact_value(payload)
    assert redacted["request"]["params"][1] == {"UserID": REDACTED}
    assert redacted["request"]["headers"] == {"Authorization": REDACTED}
    assert redacted["credentials"] == REDACTED
    # Non-sensitive clean bytes survive intact.
    assert redacted["request"]["params"][0] == {"name": "method", "value": "GetData"}
    assert redacted["request"]["url"] == "https://apps.bea.gov/api/data"
    assert redacted["auth"] == "codex-cli-subscription"
    assert redacted["usage"] == {"input_tokens": 7, "output_tokens": 3}
    assert_no_planted(json.dumps(redacted))


def test_credential_key_hides_every_value_shape_but_keeps_the_shape_of_none():
    assert security.redact_value({"password": 12345}) == {"password": REDACTED}
    assert security.redact_value({"password": ["a", "b"]}) == {"password": REDACTED}
    assert security.redact_value({"password": None}) == {"password": None}
    assert security.redact_value({"password": False}) == {"password": False}
    assert security.redact_value({"password": ""}) == {"password": ""}


def test_clean_payloads_are_returned_equal_and_redaction_is_idempotent():
    clean = {
        "kind": "forecast_run",
        "measurement_period": "2026-Q2",
        "pointEstimate": 5.1,
        "distribution": {"points": [{"value": 1.0, "probability": 0.0}]},
        "sourceUrl": "https://www.abs.gov.au/statistics/labour-force?series=UR",
        "usage": {"input_tokens": 7},
        "tokenSha256": "a" * 64,
    }
    assert security.redact_value(clean) == clean
    dirty = {"api_key": PLANTED["opaque_key"], "note": PLANTED["anthropic"]}
    once = security.redact_value(dirty)
    assert security.redact_value(once) == once


def test_object_keys_carrying_a_leaked_secret_are_scrubbed_too():
    payload = {f"ANTHROPIC_API_KEY={PLANTED['anthropic']}": 1}
    redacted = security.redact_value(payload)
    assert list(redacted) == [f"ANTHROPIC_API_KEY={REDACTED}"]
    assert_no_planted(json.dumps(redacted))


# --- URLs ---------------------------------------------------------------------


def test_clean_url_is_returned_byte_identical():
    for url in (
        "https://apps.bea.gov/api/data?&method=GetData&TableName=T50305&Year=2026",
        "https://api.statcan.gc.ca/data/v1/vector/41690973?refPer=2026-06",
        "https://data.api.abs.gov.au/rest/data/ABS,LF,1.0.0/M3.3.aus.Q?startPeriod=2026",
        "https://example.gov/path%20with%20space/file.json#section-3",
        "not a url at all",
        "",
    ):
        assert security.redact_url(url) == url


def test_query_credentials_are_redacted_including_percent_encoded_names():
    redacted = security.redact_url(
        "https://apps.bea.gov/api/data?%55serID="
        + PLANTED["opaque_key"]
        + "&method=GetData&api_key="
        + PLANTED["opaque_token"]
    )
    assert redacted == (
        f"https://apps.bea.gov/api/data?%55serID={REDACTED}"
        f"&method=GetData&api_key={REDACTED}"
    )
    assert_no_planted(redacted)


def test_declared_credential_parameters_are_redacted():
    url = "https://example.gov/series?registration=" + PLANTED["opaque_key"]
    assert security.redact_url(url) == url
    assert security.redact_url(url, credential_params=["registration"]) == (
        f"https://example.gov/series?registration={REDACTED}"
    )


def test_userinfo_fragment_and_matrix_credentials_are_redacted():
    assert (
        security.redact_url(
            "https://" + PLANTED["opaque_key"] + ":x@example.gov/data.json"
        )
        == f"https://{REDACTED}@example.gov/data.json"
    )
    assert (
        security.redact_url(
            "https://example.gov/cb#access_token="
            + PLANTED["opaque_token"]
            + "&state=1"
        )
        == f"https://example.gov/cb#access_token={REDACTED}&state=1"
    )
    assert (
        security.redact_url(
            "https://example.gov/data;UserID=" + PLANTED["opaque_key"] + "/rows"
        )
        == f"https://example.gov/data;UserID={REDACTED}/rows"
    )
    assert (
        security.redact_url(
            "https://example.gov/v1/token/" + PLANTED["opaque_token"] + "/rows"
        )
        == f"https://example.gov/v1/token/{REDACTED}/rows"
    )


def test_known_token_formats_are_redacted_anywhere_in_a_url():
    assert (
        security.redact_url(
            "https://example.gov/v1/" + PLANTED["google"] + "/rows?series=UR"
        )
        == f"https://example.gov/v1/{REDACTED}/rows?series=UR"
    )
    assert_no_planted(security.redact_url("https://x.gov/?t=" + PLANTED["jwt"]))


def test_malformed_urls_never_raise():
    for bad in ("http://[::1", "://", "%", "https://%ZZ.example/?key=abc"):
        assert isinstance(security.redact_url(bad), str)


def test_url_shaped_strings_inside_payloads_are_redacted_structurally():
    payload = {"sourceUrl": "https://apps.bea.gov/api/?UserID=" + PLANTED["opaque_key"]}
    assert security.redact_value(payload) == {
        "sourceUrl": f"https://apps.bea.gov/api/?UserID={REDACTED}"
    }


# --- Headers ------------------------------------------------------------------


def test_transport_headers_keep_the_safe_allowlist_and_lose_the_secrets():
    redacted = security.redact_headers(
        {
            "Content-Type": "application/json; charset=utf-8",
            "Last-Modified": "Wed, 02 Sep 2026 12:00:00 GMT",
            "ETag": '"abc123"',
            "Authorization": "Bearer " + PLANTED["opaque_token"],
            "Set-Cookie": "session=" + PLANTED["opaque_token"] + "; HttpOnly",
            "X-Api-Key": PLANTED["opaque_key"],
            "X-Internal-Trace": "worker-7",
        }
    )
    assert redacted == {
        "Content-Type": "application/json; charset=utf-8",
        "Last-Modified": "Wed, 02 Sep 2026 12:00:00 GMT",
        "ETag": '"abc123"',
        "Authorization": REDACTED,
        "Set-Cookie": REDACTED,
        "X-Api-Key": REDACTED,
    }
    assert "X-Internal-Trace" not in redacted
    assert_no_planted(json.dumps(redacted))


def test_unlisted_headers_can_be_kept_with_redacted_values():
    redacted = security.redact_headers(
        {"X-Trace": "ANTHROPIC_API_KEY=" + PLANTED["anthropic"]}, drop_unlisted=False
    )
    assert redacted == {"X-Trace": f"ANTHROPIC_API_KEY={REDACTED}"}


def test_url_valued_headers_and_repeated_values_are_redacted():
    redacted = security.redact_headers(
        {
            "Location": "https://example.gov/next?api_key=" + PLANTED["opaque_key"],
            "Link": ["<https://example.gov/p2>; rel=next"],
        }
    )
    assert redacted["Location"] == f"https://example.gov/next?api_key={REDACTED}"
    assert redacted["Link"] == ["<https://example.gov/p2>; rel=next"]


def test_headers_accept_pairs_declared_names_and_none():
    assert security.redact_headers(None) == {}
    assert security.redact_headers([("Date", "now"), ("X-Serial", "1")]) == {
        "Date": "now"
    }
    assert security.redact_headers(
        {"X-Serial": "s"}, credential_headers=["x-serial"], drop_unlisted=False
    ) == {"X-Serial": REDACTED}
    assert security.redact_headers({"X-Serial": "s"}, safe_headers=["X-Serial"]) == {
        "X-Serial": "s"
    }


# --- Streams and documents ----------------------------------------------------


def test_streams_stay_parseable_and_clean_lines_are_byte_identical():
    event = {
        "type": "item.completed",
        "item": {
            "type": "command_execution",
            "command": "cat $CODEX_HOME/auth.json",
            "aggregated_output": json.dumps(
                {
                    "OPENAI_API_KEY": PLANTED["openai_legacy"],
                    "tokens": {
                        "id_token": PLANTED["jwt"],
                        "access_token": PLANTED["opaque_token"],
                        "account_id": "acct-1",
                    },
                }
            ),
        },
    }
    clean = {"type": "turn.completed", "usage": {"input_tokens": 3}}
    stream = json.dumps(event) + "\n" + json.dumps(clean) + "\n"

    redacted = security.redact_stream_text(stream)
    lines = [line for line in redacted.split("\n") if line]
    parsed = [json.loads(line) for line in lines]
    inner = json.loads(parsed[0]["item"]["aggregated_output"])
    assert inner["OPENAI_API_KEY"] == REDACTED
    assert inner["tokens"]["access_token"] == REDACTED
    assert inner["tokens"]["account_id"] == "acct-1"
    assert lines[1] == json.dumps(clean)
    assert_no_planted(redacted)
    assert security.redact_stream_text(redacted) == redacted


def test_response_documents_keep_their_structure():
    cell = {
        "pointEstimate": 5.1,
        "reasoning": [
            {"kind": "tool", "result": f"stray AWS_ACCESS_KEY_ID={PLANTED['aws']}"}
        ],
        "debug": {"apiKey": PLANTED["opaque_key"]},
    }
    parsed = json.loads(security.redact_response_text(json.dumps(cell, indent=2)))
    assert parsed["reasoning"][0]["result"] == f"stray AWS_ACCESS_KEY_ID={REDACTED}"
    assert parsed["debug"] == {"apiKey": REDACTED}
    clean = json.dumps({"pointEstimate": 5.1}, indent=2)
    assert security.redact_response_text(clean) == clean


def test_plain_text_redaction_still_covers_the_incident_formats():
    for name, token in PLANTED.items():
        if name.startswith("opaque_"):
            continue
        cleaned = security.redact_text(f"prefix {token} suffix")
        assert cleaned == f"prefix {REDACTED} suffix", name
    dump = f"CENSUS_DATA_API_KEY={PLANTED['opaque_key']}\nPATH=/usr/bin:/bin"
    redacted = security.redact_text(dump)
    assert redacted == f"CENSUS_DATA_API_KEY={REDACTED}\nPATH=/usr/bin:/bin"
    assert security.redact_text(redacted) == redacted


def test_maximum_captured_output_redacts_with_a_bounded_runtime():
    """A subprocess timeout makes a regex regression fail without hanging CI."""
    script = """
import json
from thesis_core.execution import MAX_CAPTURED_BYTES
from thesis_core.security import redact_response_text, redact_text
for character in ('A', '7', '_'):
    payload = character * MAX_CAPTURED_BYTES
    assert redact_text(payload) == payload
    encoded = json.dumps(payload)
    assert redact_response_text(encoded) == encoded
# Repeated keyword candidates also cannot induce nested backtracking.
payload = 'KEY' * (MAX_CAPTURED_BYTES // 3)
assert redact_text(payload) == payload
print('bounded redaction complete')
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=True,
    )
    assert result.stdout.strip() == "bounded redaction complete"


@pytest.mark.parametrize(
    "redactor", [security.redact_stream_text, security.redact_response_text]
)
@pytest.mark.parametrize(
    "payload",
    [
        "[" * 1100 + '"planted-opaque"' + "]" * 1100,
        "7" * 5000,
        '{"api_key": {"nested": "planted-opaque"}',
    ],
)
def test_unsafe_json_refuses_instead_of_losing_structural_redaction(redactor, payload):
    with pytest.raises(security.RedactionError):
        redactor(payload)


def test_depth_limit_ignores_json_delimiters_inside_strings():
    clean = json.dumps({"text": '["' * 2000})
    assert security.redact_response_text(clean) == clean


def test_stream_redaction_preserves_log_labels_and_whole_pretty_json():
    label = "[tool] fetched public data\n[REDACTED]\n"
    assert security.redact_stream_text(label) == label
    pretty = json.dumps({"nested": {"api_key": PLANTED["opaque_key"]}}, indent=2)
    assert PLANTED["opaque_key"] not in security.redact_stream_text(pretty)
    clean = json.dumps({"pointEstimate": 5.1}, indent=2)
    assert security.redact_stream_text(clean) == clean


@pytest.mark.parametrize(
    "arguments",
    [
        ["--api-key=planted-opaque"],
        ["--token=planted-opaque"],
        ["--api-key", "planted-opaque"],
        ["--password", "planted-opaque"],
    ],
)
def test_structured_argv_redacts_opaque_equals_and_adjacent_credentials(arguments):
    value = {"argv": ["forecaster", "--max-tokens", "5", *arguments]}
    cleaned = security.redact_value(value)
    assert "planted-opaque" not in json.dumps(cleaned)
    assert cleaned["argv"][:3] == value["argv"][:3]
    assert security.redact_value(cleaned) == cleaned
