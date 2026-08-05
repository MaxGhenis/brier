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
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, BinaryIO

SERVER_NAME = "thesis_announcement_fetch"
TOOL_NAME = "fetch_official_announcement"
MAX_RESPONSE_BYTES = 16 * 1024 * 1024
EXCERPT_BYTES = 64 * 1024
FETCH_TIMEOUT_SECONDS = 30


class FetchError(RuntimeError):
    """The registered announcement could not produce a successful receipt."""


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
    request = urllib.request.Request(
        allowed_url,
        headers={
            "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.1",
            "User-Agent": "Thesis-attested-announcement-fetch/1.0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(  # noqa: S310 - exact HTTPS URL is prevalidated.
            request,
            timeout=FETCH_TIMEOUT_SECONDS,
        ) as response:
            body = _read_bounded(response)
            status = response.status
            final_url = response.geturl()
            content_type = response.headers.get_content_type()
    except urllib.error.HTTPError as exc:
        raise FetchError(f"announcement fetch returned HTTP {exc.code}") from exc
    except (OSError, urllib.error.URLError) as exc:
        raise FetchError(
            f"announcement fetch failed with {type(exc).__name__}"
        ) from exc

    if type(status) is not int or not 200 <= status < 300:
        raise FetchError(f"announcement fetch returned HTTP {status!r}")
    excerpt = body[:EXCERPT_BYTES].decode("utf-8", errors="replace")
    return {
        "requestedUrl": allowed_url,
        "finalUrl": final_url,
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
            "finalUrl": {"type": "string"},
            "statusCode": {"type": "integer", "minimum": 100, "maximum": 599},
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
