#!/usr/bin/env python3
"""Canonical JSON compatible with site/src/data/canonical-json.ts.

Object keys are sorted by UTF-16 code units, not Unicode code points.  Python's
normal string ordering differs for astral-plane keys, so callers must use the
key below rather than ``sort_keys=True``.  Number formatting follows
ECMAScript JSON.stringify's fixed/scientific thresholds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from decimal import Decimal
from typing import Any


def utf16_sort_key(value: str) -> bytes:
    """Return the big-endian UTF-16 code units used by JavaScript ordering."""

    return value.encode("utf-16-be", errors="surrogatepass")


def _serialize_string(value: str) -> str:
    pieces = ['"']
    short_escapes = {
        "\b": "\\b",
        "\t": "\\t",
        "\n": "\\n",
        "\f": "\\f",
        "\r": "\\r",
        '"': '\\"',
        "\\": "\\\\",
    }
    for char in value:
        if char in short_escapes:
            pieces.append(short_escapes[char])
        elif ord(char) < 0x20 or 0xD800 <= ord(char) <= 0xDFFF:
            pieces.append(f"\\u{ord(char):04x}")
        else:
            pieces.append(char)
    pieces.append('"')
    return "".join(pieces)


def _serialize_float(value: float) -> str:
    if not math.isfinite(value):
        raise ValueError(
            f"Canonical JSON cannot serialize non-finite number: {value}. JSON "
            "has no NaN or Infinity literal, and this serializer must stay "
            "byte-identical to canonicalStringify in "
            "site/src/data/canonical-json.ts, which JavaScript would silently "
            "render as null. Emitting null here would make two different "
            "payloads hash the same, so the value is refused instead. Fix the "
            "producer to emit a real number or null explicitly; do not coerce "
            "it at the hashing layer."
        )
    if value == 0:
        return "0"

    absolute = abs(value)
    rendered = repr(value).lower()
    if 1e-6 <= absolute < 1e21:
        fixed = format(Decimal(rendered), "f")
        if "." in fixed:
            fixed = fixed.rstrip("0").rstrip(".")
        return fixed

    if "e" not in rendered:
        rendered = format(value, ".15e")
    mantissa, exponent_text = rendered.split("e", 1)
    mantissa = mantissa.rstrip("0").rstrip(".")
    exponent = int(exponent_text)
    sign = "+" if exponent >= 0 else ""
    return f"{mantissa}e{sign}{exponent}"


def _describe(item: Any) -> str:
    """Render a short, safe summary of an offending value for error text."""

    if isinstance(item, dict):
        keys = [repr(key) for key in list(item)[:8]]
        suffix = ", ..." if len(item) > 8 else ""
        return f"{len(item)} key(s): {', '.join(keys)}{suffix}"
    if isinstance(item, list):
        return f"list of {len(item)} item(s)"
    text = repr(item)
    return text if len(text) <= 200 else text[:200] + "..."


def canonical_stringify(value: Any) -> str:
    """Serialize JSON-compatible data exactly like canonicalStringify in TS."""

    ancestors: set[int] = set()

    def serialize(item: Any) -> str:
        if item is None:
            return "null"
        if item is True:
            return "true"
        if item is False:
            return "false"
        if isinstance(item, str):
            return _serialize_string(item)
        if isinstance(item, int):
            if abs(item) > (2**53 - 1):
                try:
                    return _serialize_float(float(item))
                except OverflowError as exc:
                    raise ValueError(
                        f"Canonical JSON integer exceeds Number range: {item}"
                    ) from exc
            return str(item)
        if isinstance(item, float):
            return _serialize_float(item)

        if isinstance(item, (list, dict)):
            identity = id(item)
            if identity in ancestors:
                raise ValueError(
                    "Canonical JSON cannot serialize circular structures: a "
                    f"{type(item).__name__} contains itself "
                    f"(keys/length: {_describe(item)}). Canonical bytes have "
                    "to be finite and reproducible, so a self-referential "
                    "object has no canonical form and cannot be hashed. This "
                    "is nearly always an in-memory graph built by the caller "
                    "(a payload appended to a list it already contains), not "
                    "corrupt data on disk - JSON read from a file can never be "
                    "circular. Deep-copy or rebuild the payload before "
                    "hashing it."
                )
            ancestors.add(identity)
            try:
                if isinstance(item, list):
                    return "[" + ",".join(serialize(entry) for entry in item) + "]"
                entries = []
                for key in sorted(item, key=utf16_sort_key):
                    if not isinstance(key, str):
                        raise TypeError(
                            "Canonical JSON object keys must be strings, found "
                            f"{type(key).__name__} {key!r} in an object with "
                            f"keys {_describe(item)}. Python allows int, bool, "
                            "and None dict keys; JSON does not, and coercing "
                            'them to text would make {1: "a"} and {"1": "a"} '
                            "hash identically. Fix the producer to emit string "
                            "keys."
                        )
                    entries.append(f"{_serialize_string(key)}:{serialize(item[key])}")
                return "{" + ",".join(entries) + "}"
            finally:
                ancestors.remove(identity)

        raise TypeError(
            "Canonical JSON cannot serialize value of type "
            f"{type(item).__name__}: {_describe(item)}. Only None, bool, int, "
            "float, str, list, and dict have a canonical form; this serializer "
            "refuses anything else rather than guessing, because the bytes it "
            "produces are hashed into custody roots and record chains and must "
            "match canonicalStringify in site/src/data/canonical-json.ts "
            "exactly. Convert the value at the producer (datetime -> ISO-8601 "
            "string, Decimal -> float or str, dataclass -> dict) so the "
            "committed JSON and the hashed JSON are the same thing."
        )

    return serialize(value)


def canonical_bytes(value: Any) -> bytes:
    return canonical_stringify(value).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sha256", action="store_true", help="print SHA-256 instead of JSON"
    )
    args = parser.parse_args()
    value = json.load(sys.stdin)
    output = canonical_sha256(value) if args.sha256 else canonical_stringify(value)
    sys.stdout.write(output + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
