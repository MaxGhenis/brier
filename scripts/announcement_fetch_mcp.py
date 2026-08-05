#!/usr/bin/env python3
"""Serve one exact, registered announcement URL over a minimal MCP channel.

The attested generation lane configures this server itself.  The model can
therefore fetch the registered methodology announcement without receiving a
general-purpose URL fetcher, while the publisher can authenticate the
resulting structured Codex event during replay.
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import ipaddress
import json
import socket
import sys
import urllib.parse
from typing import Any, BinaryIO, Callable

SERVER_NAME = "thesis_announcement_fetch"
TOOL_NAME = "fetch_official_announcement"
MAX_RESPONSE_BYTES = 16 * 1024 * 1024
EXCERPT_BYTES = 64 * 1024
FETCH_TIMEOUT_SECONDS = 30


class FetchError(RuntimeError):
    """The registered announcement could not produce a successful receipt."""


ResolvedDestination = tuple[int, int, int, tuple[Any, ...]]


def _ip_address(value: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
    address = ipaddress.ip_address(value)
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped:
        return address.ipv4_mapped
    return address


def _direct_socket_factory(
    destination: ResolvedDestination,
) -> Callable[[tuple[str, int], float | None, tuple[str, int] | None], socket.socket]:
    """Build a connection factory that cannot resolve the hostname again."""

    family, socktype, proto, sockaddr = destination
    expected_peer = _ip_address(sockaddr[0])

    def create_connection(
        _address: tuple[str, int],
        timeout: float | None = None,
        source_address: tuple[str, int] | None = None,
    ) -> socket.socket:
        connection = socket.socket(family, socktype, proto)
        try:
            connection.settimeout(timeout)
            if source_address is not None:
                connection.bind(source_address)
            connection.connect(sockaddr)
            actual_peer = _ip_address(connection.getpeername()[0])
            if actual_peer != expected_peer:
                raise FetchError(
                    "announcement connection peer did not match the vetted address"
                )
            return connection
        except Exception:
            connection.close()
            raise

    return create_connection


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """HTTPS with normal hostname verification over one vetted IP socket."""

    def __init__(
        self,
        host: str,
        port: int,
        destination: ResolvedDestination,
        *,
        timeout: float,
    ) -> None:
        super().__init__(host, port=port, timeout=timeout)
        # HTTPSConnection.connect uses this seam before wrapping the socket with
        # TLS using self.host for SNI and certificate hostname verification.
        self._create_connection = _direct_socket_factory(destination)


def validate_allowed_url(value: str) -> str:
    parsed = urllib.parse.urlsplit(value)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise ValueError("allowed announcement URL must be an absolute HTTPS URL")
    return value


def _resolve_public_destinations(url: str) -> list[ResolvedDestination]:
    parsed = urllib.parse.urlsplit(url)
    host = parsed.hostname
    if host is None:  # Kept defensive for direct callers after startup parsing.
        raise FetchError("registered announcement URL has no hostname")
    try:
        port = parsed.port if parsed.port is not None else 443
        resolved = socket.getaddrinfo(
            host,
            port,
            family=socket.AF_UNSPEC,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
    except (OSError, ValueError) as exc:
        raise FetchError("announcement host resolution failed") from exc
    if not resolved:
        raise FetchError("announcement host resolution returned no IP addresses")

    destinations: list[ResolvedDestination] = []
    for family, socktype, proto, _canonname, sockaddr in resolved:
        if family not in {socket.AF_INET, socket.AF_INET6} or not sockaddr:
            raise FetchError("announcement host resolution returned a non-IP address")
        try:
            address = _ip_address(sockaddr[0])
        except ValueError as exc:
            raise FetchError(
                "announcement host resolution returned an invalid IP address"
            ) from exc
        if (
            not address.is_global
            or address.is_private
            or address.is_loopback
            or address.is_link_local
            or address.is_multicast
        ):
            raise FetchError(
                "registered announcement URL resolves to a non-public address: "
                f"{address}"
            )
        destination = (family, socktype, proto, sockaddr)
        if destination not in destinations:
            destinations.append(destination)
    if not destinations:
        raise FetchError("announcement host resolution returned no IP addresses")
    return destinations


def _read_bounded(response: BinaryIO) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(64 * 1024, MAX_RESPONSE_BYTES + 1 - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > MAX_RESPONSE_BYTES:
            raise FetchError(
                "announcement response exceeds the 16 MiB authentication limit"
            )
    return b"".join(chunks)


def fetch_announcement(url: str, *, allowed_url: str) -> dict[str, Any]:
    if url != allowed_url:
        raise FetchError("requested URL does not byte-match the registered URL")
    parsed = urllib.parse.urlsplit(allowed_url)
    host = parsed.hostname
    if host is None:  # Kept defensive for direct callers after startup parsing.
        raise FetchError("registered announcement URL has no hostname")
    try:
        port = parsed.port if parsed.port is not None else 443
    except ValueError as exc:
        raise FetchError("registered announcement URL has an invalid port") from exc
    destinations = _resolve_public_destinations(allowed_url)
    request_target = urllib.parse.urlunsplit(
        ("", "", parsed.path or "/", parsed.query, "")
    )
    headers = {
        "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.1",
        "User-Agent": "Thesis-attested-announcement-fetch/1.0",
    }

    connection_error: OSError | http.client.HTTPException | None = None
    for destination in destinations:
        connection = _PinnedHTTPSConnection(
            host,
            port,
            destination,
            timeout=FETCH_TIMEOUT_SECONDS,
        )
        try:
            connection.request("GET", request_target, headers=headers)
            response = connection.getresponse()
            status = response.status
            if type(status) is int and 300 <= status < 400:
                raise FetchError(f"announcement fetch refused HTTP redirect {status}")
            if type(status) is not int or not 200 <= status < 300:
                raise FetchError(f"announcement fetch returned HTTP {status!r}")
            content_type = response.headers.get_content_type()
            body = _read_bounded(response)
            break
        except (OSError, http.client.HTTPException) as exc:
            connection_error = exc
        finally:
            connection.close()
    else:
        assert connection_error is not None
        raise FetchError(
            f"announcement fetch failed with {type(connection_error).__name__}"
        ) from connection_error

    excerpt = body[:EXCERPT_BYTES].decode("utf-8", errors="replace")
    return {
        "requestedUrl": allowed_url,
        "finalUrl": allowed_url,
        "statusCode": status,
        "responseSha256": hashlib.sha256(body).hexdigest(),
        "contentType": content_type,
        "responseBytes": len(body),
        "excerpt": excerpt,
    }


def tool_definition(allowed_url: str) -> dict[str, Any]:
    receipt_schema = {
        "type": "object",
        "properties": {
            "requestedUrl": {"type": "string", "const": allowed_url},
            "finalUrl": {"type": "string", "const": allowed_url},
            "statusCode": {"type": "integer", "minimum": 200, "maximum": 299},
            "responseSha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        },
        "required": [
            "requestedUrl",
            "finalUrl",
            "statusCode",
            "responseSha256",
        ],
        "additionalProperties": True,
    }
    return {
        "name": TOOL_NAME,
        "title": "Fetch the registered official methodology announcement",
        "description": (
            "Fetch the one exact official announcement URL registered for this "
            "bounded target and return a terminal HTTP receipt plus an excerpt. "
            "The announcement authenticates methodology identity only; it "
            "does not establish the Thesis lab-committed release window or "
            "deadline."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {"url": {"type": "string", "const": allowed_url}},
            "required": ["url"],
            "additionalProperties": False,
        },
        "outputSchema": receipt_schema,
        "annotations": {
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    }


def _result_payload(receipt: dict[str, Any]) -> dict[str, Any]:
    structured = {
        key: receipt[key]
        for key in (
            "requestedUrl",
            "finalUrl",
            "statusCode",
            "responseSha256",
            "contentType",
            "responseBytes",
        )
    }
    text = (
        "Authenticated official announcement fetch receipt:\n"
        + json.dumps(structured, sort_keys=True)
        + "\n\nResponse excerpt:\n"
        + receipt["excerpt"]
    )
    return {
        "content": [{"type": "text", "text": text}],
        "structuredContent": structured,
        "isError": False,
    }


def handle_request(
    message: dict[str, Any], *, allowed_url: str
) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")
    if request_id is None:
        return None
    if method == "initialize":
        params = message.get("params")
        requested_version = (
            params.get("protocolVersion") if isinstance(params, dict) else None
        )
        protocol_version = (
            requested_version
            if isinstance(requested_version, str) and requested_version
            else "2024-11-05"
        )
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": protocol_version,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": "1.0.0"},
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": [tool_definition(allowed_url)]},
        }
    if method == "tools/call":
        params = message.get("params")
        name = params.get("name") if isinstance(params, dict) else None
        arguments = params.get("arguments") if isinstance(params, dict) else None
        if name != TOOL_NAME or not isinstance(arguments, dict):
            return _jsonrpc_error(request_id, -32602, "invalid tool call")
        try:
            if set(arguments) != {"url"} or not isinstance(arguments["url"], str):
                raise FetchError("tool arguments must contain only a string URL")
            receipt = fetch_announcement(arguments["url"], allowed_url=allowed_url)
        except FetchError as exc:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": str(exc)}],
                    "isError": True,
                },
            }
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": _result_payload(receipt),
        }
    return _jsonrpc_error(request_id, -32601, "method not found")


def _jsonrpc_error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }


def serve(*, allowed_url: str) -> int:
    for raw_line in sys.stdin.buffer:
        try:
            message = json.loads(raw_line)
            if not isinstance(message, dict):
                raise ValueError("message is not an object")
            response = handle_request(message, allowed_url=allowed_url)
        except (UnicodeError, json.JSONDecodeError, ValueError) as exc:
            response = _jsonrpc_error(None, -32700, f"invalid JSON-RPC message: {exc}")
        if response is not None:
            sys.stdout.write(json.dumps(response, separators=(",", ":")) + "\n")
            sys.stdout.flush()
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allowed-url", required=True, type=validate_allowed_url)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return serve(allowed_url=args.allowed_url)


if __name__ == "__main__":
    raise SystemExit(main())
