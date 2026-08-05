from __future__ import annotations

import hashlib
import io
import json
import pathlib
import subprocess
import sys
from email.message import Message

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import announcement_fetch_mcp as fetch_mcp  # noqa: E402

URL = "https://example.gov/methodology-announcement"


class FakeResponse:
    def __init__(self, body: bytes, *, final_url: str = URL, status: int = 200):
        self._stream = io.BytesIO(body)
        self._final_url = final_url
        self.status = status
        self.headers = Message()
        self.headers["Content-Type"] = "text/html; charset=utf-8"

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        return self._stream.read(size)

    def geturl(self) -> str:
        return self._final_url


def test_fetch_receipt_hashes_terminal_response_bytes(monkeypatch) -> None:
    body = b"<html>official methodology</html>"
    monkeypatch.setattr(
        fetch_mcp.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: FakeResponse(body),
    )

    receipt = fetch_mcp.fetch_announcement(URL, allowed_url=URL)

    assert receipt["requestedUrl"] == URL
    assert receipt["finalUrl"] == URL
    assert receipt["statusCode"] == 200
    assert receipt["responseSha256"] == hashlib.sha256(body).hexdigest()
    assert receipt["responseBytes"] == len(body)
    assert receipt["excerpt"] == body.decode()


def test_tool_schema_limits_input_to_registered_url() -> None:
    tool = fetch_mcp.tool_definition(URL)

    assert tool["name"] == "fetch_official_announcement"
    assert tool["description"] == (
        "Fetch the one exact official announcement URL registered for this "
        "bounded target and return a terminal HTTP receipt plus an excerpt. "
        "The announcement authenticates methodology identity only; it does "
        "not establish the Thesis lab-committed release window or deadline."
    )
    assert tool["inputSchema"] == {
        "type": "object",
        "properties": {"url": {"type": "string", "const": URL}},
        "required": ["url"],
        "additionalProperties": False,
    }
    assert tool["annotations"] == {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }


def test_tool_refuses_a_different_url_without_fetching(monkeypatch) -> None:
    monkeypatch.setattr(
        fetch_mcp.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: pytest.fail("network fetch must not run"),
    )
    response = fetch_mcp.handle_request(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": fetch_mcp.TOOL_NAME,
                "arguments": {"url": "https://example.gov/lookalike"},
            },
        },
        allowed_url=URL,
    )

    assert response == {
        "jsonrpc": "2.0",
        "id": 3,
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": "requested URL does not byte-match the registered URL",
                }
            ],
            "isError": True,
        },
    }


def test_stdio_server_uses_newline_delimited_json_rpc() -> None:
    requests = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2025-06-18"},
        },
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
    ]
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "announcement_fetch_mcp.py"),
            "--allowed-url",
            URL,
        ],
        input="".join(json.dumps(request) + "\n" for request in requests),
        capture_output=True,
        text=True,
        check=True,
    )

    responses = [json.loads(line) for line in completed.stdout.splitlines()]
    assert [response["id"] for response in responses] == [1, 2]
    assert responses[0]["result"]["protocolVersion"] == "2025-06-18"
    assert responses[1]["result"]["tools"][0]["name"] == fetch_mcp.TOOL_NAME
    assert completed.stderr == ""
