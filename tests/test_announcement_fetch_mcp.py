from __future__ import annotations

import hashlib
import io
import json
import pathlib
import socket
import ssl
import subprocess
import sys
from email.message import Message

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import announcement_fetch_mcp as fetch_mcp  # noqa: E402

URL = "https://example.gov/methodology-announcement"


class FakeResponse:
    def __init__(
        self,
        body: bytes,
        *,
        status: int = 200,
        location: str | None = None,
    ):
        self._stream = io.BytesIO(body)
        self.status = status
        self.headers = Message()
        self.headers["Content-Type"] = "text/html; charset=utf-8"
        if location is not None:
            self.headers["Location"] = location

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        return self._stream.read(size)


class FakeConnection:
    def __init__(self, response: FakeResponse):
        self.response = response
        self.closed = False
        self.request_args: tuple[object, ...] | None = None
        self.request_kwargs: dict[str, object] | None = None
        self.request_count = 0

    def request(self, *args: object, **kwargs: object) -> None:
        self.request_count += 1
        self.request_args = args
        self.request_kwargs = kwargs

    def getresponse(self) -> FakeResponse:
        return self.response

    def close(self) -> None:
        self.closed = True


def mock_connection(
    monkeypatch: pytest.MonkeyPatch,
    response: FakeResponse,
) -> FakeConnection:
    fake = FakeConnection(response)

    def build_connection(*_args: object, **_kwargs: object) -> FakeConnection:
        return fake

    monkeypatch.setattr(fetch_mcp, "_PinnedHTTPSConnection", build_connection)
    return fake


def mock_public_dns(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        fetch_mcp.socket,
        "getaddrinfo",
        lambda *_args, **_kwargs: [
            (
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_TCP,
                "",
                ("8.8.8.8", 443),
            )
        ],
    )


def test_fetch_receipt_hashes_terminal_response_bytes(monkeypatch) -> None:
    body = b"<html>official methodology</html>"
    mock_public_dns(monkeypatch)
    connection = mock_connection(monkeypatch, FakeResponse(body))

    receipt = fetch_mcp.fetch_announcement(URL, allowed_url=URL)

    assert receipt["requestedUrl"] == URL
    assert receipt["finalUrl"] == URL
    assert receipt["statusCode"] == 200
    assert receipt["responseSha256"] == hashlib.sha256(body).hexdigest()
    assert receipt["responseBytes"] == len(body)
    assert receipt["excerpt"] == body.decode()
    assert connection.request_args == (
        "GET",
        "/methodology-announcement",
    )
    assert connection.closed is True


def test_fetch_ignores_https_proxy_environment(monkeypatch) -> None:
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:9")
    mock_public_dns(monkeypatch)
    connection = mock_connection(monkeypatch, FakeResponse(b"official"))

    receipt = fetch_mcp.fetch_announcement(URL, allowed_url=URL)

    assert receipt["statusCode"] == 200
    assert connection.request_count == 1


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
    assert tool["outputSchema"]["properties"]["finalUrl"] == {
        "type": "string",
        "const": URL,
    }
    assert tool["outputSchema"]["properties"]["statusCode"] == {
        "type": "integer",
        "minimum": 200,
        "maximum": 299,
    }
    assert tool["outputSchema"]["required"] == [
        "requestedUrl",
        "finalUrl",
        "statusCode",
        "responseSha256",
    ]
    assert tool["annotations"] == {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }


def test_tool_refuses_a_different_url_without_fetching(monkeypatch) -> None:
    monkeypatch.setattr(
        fetch_mcp.socket,
        "getaddrinfo",
        lambda *_args, **_kwargs: pytest.fail("DNS lookup must not run"),
    )
    monkeypatch.setattr(
        fetch_mcp,
        "_PinnedHTTPSConnection",
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


def test_redirect_is_refused_without_following(monkeypatch) -> None:
    mock_public_dns(monkeypatch)
    response = FakeResponse(
        b"redirect body must not be read",
        status=302,
        location="https://elsewhere.example/announcement",
    )
    connection = mock_connection(monkeypatch, response)

    with pytest.raises(
        fetch_mcp.FetchError,
        match=r"^announcement fetch refused HTTP redirect 302$",
    ):
        fetch_mcp.fetch_announcement(URL, allowed_url=URL)

    assert response.read() == b"redirect body must not be read"
    assert connection.request_count == 1
    assert connection.closed is True


@pytest.mark.parametrize(
    ("address", "family"),
    [
        pytest.param("10.0.0.1", socket.AF_INET, id="private"),
        pytest.param("127.0.0.1", socket.AF_INET, id="loopback"),
        pytest.param("169.254.1.1", socket.AF_INET, id="link-local"),
        pytest.param("224.0.0.1", socket.AF_INET, id="multicast"),
        pytest.param("::1", socket.AF_INET6, id="ipv6-loopback"),
    ],
)
def test_non_public_destination_is_refused_before_fetch(
    monkeypatch: pytest.MonkeyPatch,
    address: str,
    family: socket.AddressFamily,
) -> None:
    sockaddr = (address, 443, 0, 0) if family == socket.AF_INET6 else (address, 443)
    monkeypatch.setattr(
        fetch_mcp.socket,
        "getaddrinfo",
        lambda *_args, **_kwargs: [
            (family, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", sockaddr)
        ],
    )
    monkeypatch.setattr(
        fetch_mcp,
        "_PinnedHTTPSConnection",
        lambda *_args, **_kwargs: pytest.fail("network fetch must not run"),
    )

    with pytest.raises(fetch_mcp.FetchError) as caught:
        fetch_mcp.fetch_announcement(URL, allowed_url=URL)

    assert str(caught.value) == (
        "registered announcement URL resolves to a non-public address: " + address
    )


def test_mixed_public_and_private_dns_answers_are_refused(monkeypatch) -> None:
    monkeypatch.setattr(
        fetch_mcp.socket,
        "getaddrinfo",
        lambda *_args, **_kwargs: [
            (
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_TCP,
                "",
                ("8.8.8.8", 443),
            ),
            (
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_TCP,
                "",
                ("10.0.0.1", 443),
            ),
        ],
    )
    monkeypatch.setattr(
        fetch_mcp,
        "_PinnedHTTPSConnection",
        lambda *_args, **_kwargs: pytest.fail("network fetch must not run"),
    )

    with pytest.raises(
        fetch_mcp.FetchError,
        match=(
            r"^registered announcement URL resolves to a non-public address: "
            r"10\.0\.0\.1$"
        ),
    ):
        fetch_mcp.fetch_announcement(URL, allowed_url=URL)


def test_pinned_connection_does_not_resolve_again_and_preserves_tls_host(
    monkeypatch,
) -> None:
    dns_calls = 0

    def resolve_once(*_args: object, **_kwargs: object) -> list[tuple[object, ...]]:
        nonlocal dns_calls
        dns_calls += 1
        if dns_calls > 1:
            pytest.fail("the vetted hostname must not be resolved again")
        return [
            (
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_TCP,
                "",
                ("8.8.8.8", 443),
            )
        ]

    class Socket:
        def __init__(self) -> None:
            self.connected_to: tuple[str, int] | None = None
            self.sent: list[bytes] = []

        def settimeout(self, _timeout: object) -> None:
            return None

        def connect(self, address: tuple[str, int]) -> None:
            self.connected_to = address

        def getpeername(self) -> tuple[str, int]:
            assert self.connected_to is not None
            return self.connected_to

        def setsockopt(self, *_args: object) -> None:
            return None

        def sendall(self, data: bytes) -> None:
            self.sent.append(data)

        def close(self) -> None:
            return None

    class TLSContext:
        def __init__(self) -> None:
            self.server_hostname: str | None = None

        def wrap_socket(self, sock: Socket, *, server_hostname: str) -> Socket:
            self.server_hostname = server_hostname
            return sock

    direct_socket = Socket()
    context = TLSContext()
    monkeypatch.setattr(fetch_mcp.socket, "getaddrinfo", resolve_once)
    monkeypatch.setattr(
        fetch_mcp.socket,
        "socket",
        lambda *_args, **_kwargs: direct_socket,
    )
    destination = fetch_mcp._resolve_public_destinations(URL)[0]
    connection = fetch_mcp._PinnedHTTPSConnection(
        "example.gov",
        443,
        destination,
        timeout=fetch_mcp.FETCH_TIMEOUT_SECONDS,
    )
    connection._context = context

    connection.request("GET", "/methodology-announcement")

    assert dns_calls == 1
    assert direct_socket.connected_to == ("8.8.8.8", 443)
    assert context.server_hostname == "example.gov"
    assert b"Host: example.gov\r\n" in b"".join(direct_socket.sent)


def test_pinned_connection_refuses_an_unexpected_peer(monkeypatch) -> None:
    class Socket:
        closed = False

        def settimeout(self, _timeout: object) -> None:
            return None

        def connect(self, _address: tuple[str, int]) -> None:
            return None

        def getpeername(self) -> tuple[str, int]:
            return ("127.0.0.1", 443)

        def close(self) -> None:
            self.closed = True

    direct_socket = Socket()
    monkeypatch.setattr(
        fetch_mcp.socket,
        "socket",
        lambda *_args, **_kwargs: direct_socket,
    )
    destination = (
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP,
        ("8.8.8.8", 443),
    )

    with pytest.raises(
        fetch_mcp.FetchError,
        match=r"^announcement connection peer did not match the vetted address$",
    ):
        fetch_mcp._connect_vetted_destination(
            destination,
            timeout=fetch_mcp.FETCH_TIMEOUT_SECONDS,
            source_address=None,
        )

    assert direct_socket.closed is True


def test_pinned_connection_refuses_proxy_tunnels() -> None:
    connection = fetch_mcp._PinnedHTTPSConnection(
        "example.gov",
        443,
        (
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
            ("8.8.8.8", 443),
        ),
        timeout=fetch_mcp.FETCH_TIMEOUT_SECONDS,
    )
    connection.set_tunnel("proxy.example")

    with pytest.raises(
        fetch_mcp.FetchError,
        match=r"^announcement fetch refuses proxy tunnels$",
    ):
        connection.connect()


def test_fetch_refuses_an_empty_vetted_destination_set(monkeypatch) -> None:
    monkeypatch.setattr(fetch_mcp, "_resolve_public_destinations", lambda _url: [])
    monkeypatch.setattr(
        fetch_mcp,
        "_PinnedHTTPSConnection",
        lambda *_args, **_kwargs: pytest.fail("network fetch must not run"),
    )

    with pytest.raises(
        fetch_mcp.FetchError,
        match=r"^announcement host resolution returned no IP addresses$",
    ):
        fetch_mcp.fetch_announcement(URL, allowed_url=URL)


def test_pinned_connection_uses_a_verifying_default_tls_context() -> None:
    connection = fetch_mcp._PinnedHTTPSConnection(
        "example.gov",
        443,
        (
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
            ("8.8.8.8", 443),
        ),
        timeout=fetch_mcp.FETCH_TIMEOUT_SECONDS,
    )

    assert connection._context.check_hostname is True
    assert connection._context.verify_mode == ssl.CERT_REQUIRED


def test_fetch_retries_only_vetted_destinations_and_closes_each(monkeypatch) -> None:
    class FailingConnection(FakeConnection):
        def request(self, *args: object, **kwargs: object) -> None:
            super().request(*args, **kwargs)
            raise OSError("first address unavailable")

    destinations = [
        (
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
            "",
            ("8.8.8.8", 443),
        ),
        (
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
            "",
            ("1.1.1.1", 443),
        ),
    ]
    monkeypatch.setattr(
        fetch_mcp.socket,
        "getaddrinfo",
        lambda *_args, **_kwargs: destinations,
    )
    connections: list[FakeConnection] = []
    used_destinations: list[fetch_mcp.ResolvedDestination] = []

    def build_connection(
        _host: str,
        _port: int,
        destination: fetch_mcp.ResolvedDestination,
        *,
        timeout: float,
    ) -> FakeConnection:
        assert timeout == fetch_mcp.FETCH_TIMEOUT_SECONDS
        connection_type = FailingConnection if not connections else FakeConnection
        connection = connection_type(FakeResponse(b"official"))
        connections.append(connection)
        used_destinations.append(destination)
        return connection

    monkeypatch.setattr(fetch_mcp, "_PinnedHTTPSConnection", build_connection)

    receipt = fetch_mcp.fetch_announcement(URL, allowed_url=URL)

    assert receipt["statusCode"] == 200
    assert used_destinations == [
        (family, socktype, proto, sockaddr)
        for family, socktype, proto, _canonname, sockaddr in destinations
    ]
    assert len(connections) == 2
    assert all(connection.closed for connection in connections)


def test_fetch_refuses_when_every_vetted_destination_fails(monkeypatch) -> None:
    class FailingConnection(FakeConnection):
        def request(self, *args: object, **kwargs: object) -> None:
            super().request(*args, **kwargs)
            raise OSError("address unavailable")

    destinations = [
        (
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
            "",
            ("8.8.8.8", 443),
        ),
        (
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
            "",
            ("1.1.1.1", 443),
        ),
    ]
    monkeypatch.setattr(
        fetch_mcp.socket,
        "getaddrinfo",
        lambda *_args, **_kwargs: destinations,
    )
    connections: list[FailingConnection] = []
    used_destinations: list[fetch_mcp.ResolvedDestination] = []

    def build_connection(
        _host: str,
        _port: int,
        destination: fetch_mcp.ResolvedDestination,
        *,
        timeout: float,
    ) -> FailingConnection:
        assert timeout == fetch_mcp.FETCH_TIMEOUT_SECONDS
        connection = FailingConnection(FakeResponse(b"unreachable"))
        connections.append(connection)
        used_destinations.append(destination)
        return connection

    monkeypatch.setattr(fetch_mcp, "_PinnedHTTPSConnection", build_connection)

    with pytest.raises(
        fetch_mcp.FetchError,
        match=r"^announcement fetch failed with OSError$",
    ):
        fetch_mcp.fetch_announcement(URL, allowed_url=URL)

    assert used_destinations == [
        (family, socktype, proto, sockaddr)
        for family, socktype, proto, _canonname, sockaddr in destinations
    ]
    assert len(connections) == 2
    assert all(connection.request_count == 1 for connection in connections)
    assert all(connection.closed for connection in connections)


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


def test_fetch_headers_use_the_transparent_resolver_user_agent() -> None:
    # FSA's WAF resets connections on the old bespoke token
    # ("Thesis-attested-announcement-fetch/1.0": reset in ~1s measured
    # 2026-08-14) while serving the resolver families' transparent
    # compatible form in ~0.3s. An announcement fetch that cannot
    # complete blocks every resolve-by-bound publish, so the UA is
    # pinned to the exact working form here.
    source = pathlib.Path(fetch_mcp.__file__).read_text()
    assert '"User-Agent": "Mozilla/5.0 (compatible; thesis-resolver/1.0)"' in source
    assert "Thesis-attested-announcement-fetch/1.0" not in source
