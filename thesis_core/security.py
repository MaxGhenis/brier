"""Shared credential hygiene for recorded agent runs and source capture.

This module is the single implementation of two independent defenses that the
repository already relied on, moved here so the legacy thesis.analyst runner,
the new `thesis_core` execution path and the source adapters all scrub with the
same code:

1. Recorded subprocesses run under a minimal explicit environment
   (``AGENT_ENV_ALLOWLIST``, an allowlist and never a denylist), so an ``env``
   dump inside an agent has nothing secret to print.
2. Every captured stream, response document, URL, header map and metadata
   payload is redacted *before* any artifact is written, hashed or
   content-addressed, so a secret read from disk or echoed by a tool never
   reaches a record and no post-hoc scrub can break an attestation.

Incident 2026-07-21: during an aging-wave batch, the codex agent ran
``env | rg -i 'CENSUS|API|KEY'`` while hunting for a Census API key, and 18
credential env vars inherited from the interactive shell landed verbatim in
recorded trace files; GitHub push protection was the only thing that kept them
out of the public repo.

Two properties are load-bearing and are pinned by tests:

* **Clean content is byte-identical.** Redacting text, a stream, a response
  document, a URL or a JSON payload that contains no credential returns the
  input unchanged. Evidence bytes are not reshaped by passing through here.
* **Redaction is idempotent.** Re-redacting redacted content is a no-op, so a
  value can be scrubbed at more than one boundary safely.

The module is standard library only, by design: `scripts/run_thesis_analyst.py`
and the source adapters must keep working in a checkout without the `core`
extra installed.

These functions are for text and JSON-compatible payloads only. Never route
opaque binary evidence through them — an RFC 3161 request/response DER, a
signature, a raw archived response body — because verification is over exact
bytes and any normalization would break it. Hash and store those as they
arrived; scrub the metadata that describes them instead.

Nothing here reads a keychain, a credential store or a secret file. It only
ever *removes* values that are already in front of it.
"""

from __future__ import annotations

import json
import os
import re
from collections.abc import Iterable, Mapping
from typing import Any
from urllib.parse import unquote_plus, urlsplit, urlunsplit

__all__ = [
    "AGENT_ENV_ALLOWLIST",
    "CREDENTIAL_COLLAPSED_NEEDLES",
    "CREDENTIAL_WORD_PAIRS",
    "NON_CREDENTIAL_TRAILING_WORDS",
    "ENV_SECRET_ASSIGNMENT_RE",
    "JSON_SECRET_FIELD_RE",
    "REDACTED_PLACEHOLDER",
    "SAFE_TRANSPORT_HEADERS",
    "SECRET_TOKEN_RE",
    "STANDALONE_CREDENTIAL_WORDS",
    "agent_subprocess_env",
    "credential_key_words",
    "is_credential_key",
    "redact_headers",
    "redact_json_value",
    "redact_response_text",
    "redact_stream_line",
    "redact_stream_text",
    "redact_text",
    "redact_url",
    "redact_value",
]


# --- Minimal subprocess environment -----------------------------------------

AGENT_ENV_ALLOWLIST = (
    "PATH",
    "HOME",
    "TERM",
    "SHELL",
    "TMPDIR",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    # Non-secret directory path selecting which codex auth/config dir to use.
    "CODEX_HOME",
)


def agent_subprocess_env(
    overrides: dict[str, str] | None = None,
) -> dict[str, str]:
    """Minimal explicit environment for recorded agent subprocesses."""
    env = {
        name: os.environ[name] for name in AGENT_ENV_ALLOWLIST if os.environ.get(name)
    }
    if overrides:
        env.update(overrides)
    return env


# --- Text-level credential patterns -----------------------------------------

REDACTED_PLACEHOLDER = "[REDACTED]"

# `NAME=value` lines for credential-shaped env var names: the incident shape.
ENV_SECRET_ASSIGNMENT_RE = re.compile(
    r"([A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*)=\S+"
)

# `"name": "value"` JSON fields with credential-shaped names — catches an
# agent cat-ing auth/config files (auth.json and friends) into its trace.
JSON_SECRET_FIELD_RE = re.compile(
    r"\"([A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD)[A-Z0-9_]*)\"\s*:\s*\"[^\"]*\"",
    re.IGNORECASE,
)

# Well-known credential token formats (the incident list plus legacy
# OpenAI `sk-` keys, which auth.json can hold under API-key login).
SECRET_TOKEN_RE = re.compile(
    "|".join(
        [
            r"sk-(?:ant|proj|or)-[A-Za-z0-9_-]+",  # Anthropic/OpenAI/OpenRouter
            r"sk-[A-Za-z0-9]{20,}",  # legacy OpenAI secret keys
            r"ghp_[A-Za-z0-9]+",  # GitHub classic PAT
            r"github_pat_[A-Za-z0-9_]+",  # GitHub fine-grained PAT
            r"xox[bp]-[A-Za-z0-9-]+",  # Slack bot/user tokens
            r"AIza[A-Za-z0-9_-]+",  # Google API keys
            r"eyJhbGciOi[A-Za-z0-9_.=-]+",  # JWTs (Supabase service keys, ...)
            r"AKIA[A-Z0-9]+",  # AWS access key ids
        ]
    )
)


def redact_text(text: str) -> str:
    """Redact credential values from plain text (idempotent)."""
    if not text:
        return text
    text = ENV_SECRET_ASSIGNMENT_RE.sub(rf"\1={REDACTED_PLACEHOLDER}", text)
    text = JSON_SECRET_FIELD_RE.sub(rf'"\1": "{REDACTED_PLACEHOLDER}"', text)
    return SECRET_TOKEN_RE.sub(REDACTED_PLACEHOLDER, text)


# --- Credential-shaped names ------------------------------------------------
#
# The text patterns above only recognize credential *values*: a `NAME=value`
# assignment, a quoted JSON field in raw text, or a well-known token format.
# They cannot see an arbitrary opaque credential that arrives as a parsed value
# under a credential-shaped key — `{"api_key": "plain-secret"}` survives a
# value-wise text scrub because "plain-secret" matches no pattern. Source
# adapters hand us exactly that shape (query parameters, request headers,
# archived exchange metadata), so name matching is a separate, structural
# defense.
#
# Names are matched on words, not substrings, so that a credential-shaped word
# is required rather than merely contained: `input_tokens` (a usage count) and
# `dataKey` (an SDMX series key) survive, while `apiKey`, `X-Api-Key`,
# `ANTHROPIC_API_KEY`, `access_token`, `UserID` and `Set-Cookie` do not.

_KEY_WORD_RE = re.compile(r"[A-Z]+(?![a-z])|[A-Z][a-z0-9]*|[a-z0-9]+")

# Words that are credential-shaped standing alone.
STANDALONE_CREDENTIAL_WORDS = frozenset(
    {
        "authentication",
        "authorization",
        "bearer",
        "cookie",
        "cookies",
        "credential",
        "credentials",
        "passphrase",
        "passwd",
        "password",
        "pwd",
        "secret",
        "secrets",
        "token",
    }
)

# Adjacent word pairs that are credential-shaped together. Deliberately absent:
# ("session", "id") and ("account", "id"), which are correlation identifiers
# that agent traces legitimately carry. Bare "auth" is a pair prefix rather
# than a standalone word for the same reason: existing thesis.analyst traces
# record `"auth": "codex-cli-subscription"`, a non-secret provenance label.
CREDENTIAL_WORD_PAIRS = frozenset(
    {
        ("access", "key"),
        ("access", "token"),
        ("account", "key"),
        ("api", "key"),
        ("api", "secret"),
        ("api", "token"),
        ("app", "key"),
        ("application", "key"),
        ("auth", "credential"),
        ("auth", "header"),
        ("auth", "key"),
        ("auth", "secret"),
        ("auth", "token"),
        ("auth", "value"),
        ("bearer", "token"),
        ("client", "secret"),
        ("consumer", "key"),
        ("consumer", "secret"),
        ("csrf", "token"),
        ("encryption", "key"),
        ("id", "token"),
        ("license", "key"),
        ("private", "key"),
        ("refresh", "token"),
        ("registration", "key"),
        ("secret", "key"),
        ("security", "token"),
        ("session", "key"),
        ("session", "token"),
        ("shared", "key"),
        ("shared", "secret"),
        ("signing", "key"),
        ("subscription", "key"),
        ("user", "id"),
        ("xsrf", "token"),
    }
)

# Needles matched against the separator-free lowercase name, for keys written
# without any word boundary at all (`apikey`, `XAPIKEY`, `userid`). Bare
# "token" and bare "key" are deliberately excluded here: they would swallow
# `input_tokens` and `dataKey`. Bare "auth" is excluded because it is a
# substring of "author".
CREDENTIAL_COLLAPSED_NEEDLES = (
    "accesskey",
    "accesstoken",
    "apikey",
    "apisecret",
    "apitoken",
    "authorization",
    "authentication",
    "bearer",
    "clientsecret",
    "cookie",
    "credential",
    "csrftoken",
    "idtoken",
    "licensekey",
    "passphrase",
    "passwd",
    "password",
    "privatekey",
    "refreshtoken",
    "secret",
    "securitytoken",
    "sessiontoken",
    "signingkey",
    "subscriptionkey",
    "userid",
    "xsrftoken",
)

# A name that is exactly this, ignoring case and separators, is credential
# shaped on its own. `?key=` is the Google API-key query convention.
_EXACT_CREDENTIAL_NAMES = frozenset({"key"})

# A trailing word that describes a credential rather than carrying it: the
# *path* to a token file, the *sha256* of a timestamp token, the *size* of a
# key. Existing witness records use `tokenPath` and `tokenSha256` for public
# RFC 3161 evidence, and redacting those would destroy proof, not protect it.
# `records/trust/tsa-anchors-v1.json` likewise configures `maxTokenLeadSeconds`.
# "id" is deliberately absent so `UserID` stays credential-shaped.
NON_CREDENTIAL_TRAILING_WORDS = frozenset(
    {
        "alg",
        "algorithm",
        "at",
        "bytes",
        "count",
        "day",
        "days",
        "digest",
        "dir",
        "directory",
        "exists",
        "file",
        "filename",
        "format",
        "hash",
        "hour",
        "hours",
        "index",
        "length",
        "limit",
        "millis",
        "milliseconds",
        "minute",
        "minutes",
        "mode",
        "offset",
        "path",
        "policy",
        "present",
        "scheme",
        "sha1",
        "sha256",
        "second",
        "seconds",
        "sha512",
        "size",
        "status",
        "timestamp",
        "type",
        "uri",
        "url",
        "version",
    }
)


def credential_key_words(name: str) -> tuple[str, ...]:
    """Split a key/parameter/header name into lowercase words.

    Handles `snake_case`, `kebab-case`, `camelCase`, `PascalCase`, SCREAMING
    case and acronym runs: ``UserID`` -> ``("user", "id")``, ``APIKey`` ->
    ``("api", "key")``, ``X-Api-Key`` -> ``("x", "api", "key")``.
    """
    if not name:
        return ()
    return tuple(word.lower() for word in _KEY_WORD_RE.findall(name))


def is_credential_key(name: Any, extra: Iterable[str] = ()) -> bool:
    """Return True when a key/parameter/header name should hide its value.

    ``extra`` carries adapter-declared credential-bearing names (the plan's
    "adapters declare credential-bearing URL parameters and headers"); they are
    compared case-insensitively and ignoring separators, so an adapter may
    declare ``UserID``, ``userid`` or ``user_id`` interchangeably.
    """
    if not isinstance(name, str) or not name:
        return False
    words = credential_key_words(name)
    if not words:
        return False
    collapsed = "".join(words)
    for declared in extra:
        if not isinstance(declared, str):
            continue
        if "".join(credential_key_words(declared)) == collapsed:
            return True
    if words[-1] in NON_CREDENTIAL_TRAILING_WORDS:
        # A path to, hash of, or size of a credential is not the credential.
        return False
    if collapsed in _EXACT_CREDENTIAL_NAMES:
        return True
    if any(word in STANDALONE_CREDENTIAL_WORDS for word in words):
        return True
    if any(pair in CREDENTIAL_WORD_PAIRS for pair in zip(words, words[1:])):
        return True
    return any(needle in collapsed for needle in CREDENTIAL_COLLAPSED_NEEDLES)


def _redacted_for_credential_key(value: Any) -> Any:
    """Replace a value held under a credential-shaped key.

    ``None`` and booleans carry no secret and are preserved so a payload keeps
    its shape; an empty string is preserved for the same reason. Everything
    else — strings, numbers, objects, arrays — collapses to the placeholder,
    because a credential may hide anywhere inside it.
    """
    if value is None or isinstance(value, bool) or value == "":
        return value
    return REDACTED_PLACEHOLDER


# --- URLs -------------------------------------------------------------------

_URL_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*://")

# Path segments that unambiguously introduce a credential as the next segment
# (`/token/<value>`). Bare "key" is excluded: official series paths use it
# (SDMX data keys) and mangling an evidence URL is worse than the residual
# risk, which adapter-declared parameters cover.
_CREDENTIAL_PATH_LABELS = frozenset(
    {
        "apikey",
        "accesstoken",
        "authorization",
        "credential",
        "credentials",
        "password",
        "secret",
        "token",
    }
)


def _safe_unquote(text: str) -> str:
    """Percent-decode a URL key without ever raising on malformed input."""
    try:
        return unquote_plus(text, errors="replace")
    except (UnicodeDecodeError, ValueError):  # pragma: no cover - defensive
        return text


def _redact_param_string(
    raw: str, separator: str, credential_params: Iterable[str]
) -> tuple[str, bool]:
    """Redact `name=value` pairs in a query, fragment or matrix-param string.

    Non-sensitive pairs are copied through verbatim — including their original
    percent-encoding, ordering and empty segments — so a clean string is
    returned byte-identical.
    """
    if not raw:
        return raw, False
    changed = False
    pieces = []
    for piece in raw.split(separator):
        name, sep, value = piece.partition("=")
        if sep and value and is_credential_key(_safe_unquote(name), credential_params):
            pieces.append(f"{name}={REDACTED_PLACEHOLDER}")
            changed = True
        else:
            pieces.append(piece)
    return separator.join(pieces), changed


def _redact_url_path(path: str, credential_params: Iterable[str]) -> tuple[str, bool]:
    if not path:
        return path, False
    changed = False
    segments = path.split("/")
    previous_label = ""
    for index, segment in enumerate(segments):
        if not segment:
            previous_label = ""
            continue
        if previous_label in _CREDENTIAL_PATH_LABELS:
            segments[index] = REDACTED_PLACEHOLDER
            changed = True
            previous_label = ""
            continue
        if "=" in segment:
            # Matrix parameters: `/data;UserID=secret/`.
            redacted, segment_changed = _redact_param_string(
                segment, ";", credential_params
            )
            segments[index] = redacted
            changed = changed or segment_changed
        previous_label = "".join(credential_key_words(_safe_unquote(segment)))
    return "/".join(segments), changed


def redact_url(url: str, *, credential_params: Iterable[str] = ()) -> str:
    """Redact credentials carried in a URL, preserving a clean URL verbatim.

    Handles the three places a credential actually travels in a URL: the
    userinfo component (``https://key@host/``), ``name=value`` parameters in the
    query, fragment and path matrix segments, and a value that matches a
    well-known token format anywhere in the string. ``credential_params``
    carries the adapter-declared credential-bearing parameter names.

    A URL with nothing to redact is returned unchanged, so archived exchange
    URLs keep their exact bytes and hashes.
    """
    if not isinstance(url, str) or not url:
        return url
    try:
        parts = urlsplit(url)
    except ValueError:
        return redact_text(url)

    netloc = parts.netloc
    changed = False
    if "@" in netloc:
        userinfo, _, hostport = netloc.rpartition("@")
        if userinfo:
            netloc = f"{REDACTED_PLACEHOLDER}@{hostport}"
            changed = True

    path, path_changed = _redact_url_path(parts.path, credential_params)
    query, query_changed = _redact_param_string(parts.query, "&", credential_params)
    fragment, fragment_changed = _redact_param_string(
        parts.fragment, "&", credential_params
    )
    changed = changed or path_changed or query_changed or fragment_changed

    if not changed:
        # Byte-identical for clean URLs: redact_text is the identity on text
        # holding no known credential format.
        return redact_text(url)
    rebuilt = urlunsplit((parts.scheme, netloc, path, query, fragment))
    return redact_text(rebuilt)


# --- Headers ----------------------------------------------------------------

# Response/request headers that describe the exchange rather than authorize it.
# The plan already forbids treating any of them as publication evidence; they
# are retained because they are useful descriptive capture metadata.
SAFE_TRANSPORT_HEADERS = frozenset(
    {
        "accept-ranges",
        "age",
        "cache-control",
        "content-disposition",
        "content-encoding",
        "content-language",
        "content-length",
        "content-location",
        "content-range",
        "content-type",
        "date",
        "etag",
        "expires",
        "last-modified",
        "link",
        "location",
        "retry-after",
        "server",
        "vary",
        "x-cache",
        "x-content-type-options",
    }
)

_URL_VALUED_HEADERS = frozenset({"content-location", "link", "location"})


def _redact_header_value(
    lowered_name: str, value: Any, credential_params: Iterable[str]
) -> Any:
    if isinstance(value, (list, tuple)):
        return [
            _redact_header_value(lowered_name, item, credential_params)
            for item in value
        ]
    if not isinstance(value, str):
        return value
    if lowered_name in _URL_VALUED_HEADERS:
        return redact_url(value, credential_params=credential_params)
    return redact_text(value)


def redact_headers(
    headers: Mapping[str, Any] | Iterable[tuple[str, Any]] | None,
    *,
    credential_headers: Iterable[str] = (),
    safe_headers: Iterable[str] = (),
    drop_unlisted: bool = True,
) -> dict[str, Any]:
    """Return persistable headers: no transport secrets, allowlisted names.

    A credential-shaped header keeps its *name* — that a request carried an
    ``Authorization`` header is worth recording — and loses its value. Any
    other header not on the safe allowlist is removed entirely rather than
    persisted on the hope that it holds nothing sensitive; pass
    ``drop_unlisted=False`` to keep unknown headers with redacted values
    instead. ``credential_headers``/``safe_headers`` carry adapter-declared
    additions.
    """
    if headers is None:
        return {}
    items: Iterable[tuple[str, Any]]
    if isinstance(headers, Mapping):
        items = headers.items()
    else:
        items = headers
    allowed = set(SAFE_TRANSPORT_HEADERS)
    allowed.update(name.strip().lower() for name in safe_headers)

    result: dict[str, Any] = {}
    for name, value in items:
        if not isinstance(name, str):
            continue
        lowered = name.strip().lower()
        if is_credential_key(name, credential_headers):
            result[name] = _redacted_for_credential_key(value)
            continue
        if lowered in allowed:
            result[name] = _redact_header_value(lowered, value, credential_headers)
            continue
        if not drop_unlisted:
            result[name] = _redact_header_value(lowered, value, credential_headers)
    return result


# --- JSON payloads ----------------------------------------------------------


def redact_value(value: Any, *, credential_keys: Iterable[str] = ()) -> Any:
    """Redact a JSON-compatible payload before it is hashed or persisted.

    Three defenses compose:

    * every string is scrubbed for known credential formats and `NAME=value`
      shapes (:func:`redact_text`);
    * every URL-shaped string is scrubbed structurally (:func:`redact_url`);
    * every value held under a credential-shaped key is replaced outright,
      recursively, which is the only defense that catches an opaque secret such
      as ``{"api_key": "plain-secret"}``.

    Object keys themselves are scrubbed too, because a leaked env dump can
    arrive as a key. A payload with nothing to redact compares equal to its
    input, and callers rely on that to keep clean bytes untouched.
    """
    if isinstance(value, str):
        if _URL_SCHEME_RE.match(value):
            return redact_url(value, credential_params=credential_keys)
        return redact_text(value)
    if isinstance(value, list):
        return [redact_value(item, credential_keys=credential_keys) for item in value]
    if isinstance(value, tuple):
        return [redact_value(item, credential_keys=credential_keys) for item in value]
    if isinstance(value, dict):
        redacted: dict[Any, Any] = {}
        for key, item in value.items():
            clean_key = redact_text(key) if isinstance(key, str) else key
            if is_credential_key(key, credential_keys):
                redacted[clean_key] = _redacted_for_credential_key(item)
            else:
                redacted[clean_key] = redact_value(
                    item, credential_keys=credential_keys
                )
        return redacted
    return value


def redact_json_value(value: Any) -> Any:
    """Legacy name for :func:`redact_value`, kept for the analyst runner."""
    return redact_value(value)


# --- Streams and response documents -----------------------------------------


def redact_stream_line(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return line
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        return redact_text(line)
    redacted = redact_value(payload)
    return line if redacted == payload else json.dumps(redacted)


def redact_stream_text(text: str) -> str:
    """Redact a line-oriented agent stream without breaking its structure.

    JSONL event lines are redacted value-wise so they stay parseable;
    non-JSON lines get plain-text redaction. Clean content passes through
    byte-identical.
    """
    if not text:
        return text
    return "\n".join(redact_stream_line(line) for line in text.split("\n"))


def redact_response_text(text: str) -> str:
    """Redact an agent response document.

    A whole-document JSON response (the usual final-message shape) is
    redacted value-wise so it stays parseable even when pretty-printed;
    anything else falls back to line-oriented stream redaction.
    """
    if not text:
        return text
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return redact_stream_text(text)
    redacted = redact_value(payload)
    return text if redacted == payload else json.dumps(redacted, indent=2)
