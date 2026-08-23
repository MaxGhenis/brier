"""Shared validation for conditional-policy causal-chain evidence.

The analyst runner and spawned-cell converter are independent publication
boundaries. Keep the literal policy-chain contract here so neither path can
accept a conditional cell that the other refuses.
"""

from __future__ import annotations

import math
import re
from typing import Any
from urllib.parse import unquote, urlparse

POLICY_CHAIN_AGENT_VERSION = "2.5.12"
POLICY_CHAIN_AGENT_VERSION_PARTS = (2, 5, 12)

POLICY_CHAIN_URL_RE = re.compile(r"https?://[^\s<>'\"`]+", re.IGNORECASE)
POLICY_CHAIN_TERM_RE = r"(?:policy[- ](?:term|effect)|effect[- ](?:size|term))"
POLICY_CHAIN_NUMBER_RE = (
    r"(?<![\w.])(?P<{name}>[+\-]?\s*"
    r"(?:(?:\d{{1,3}}(?:,\d{{3}})+|\d+)(?:\.\d+)?|\.\d+)"
    r"(?:[eE][+\-]?\d+)?)(?![\w.])"
)

_VERSION_RE = re.compile(
    r"(?P<major>0|[1-9][0-9]*)\."
    r"(?P<minor>0|[1-9][0-9]*)\."
    r"(?P<patch>0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?"
)
_UNRESERVED = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)
_PERCENT_ESCAPE_RE = re.compile(r"%([0-9A-Fa-f]{2})")
_ENCODED_HTTP_RE = re.compile(
    r"%(?:25)*(?:68)%(?:25)*(?:74)%(?:25)*(?:74)%(?:25)*(?:70)"
    r"(?:%(?:25)*(?:73))?",
    re.IGNORECASE,
)
_ABSOLUTE_HTTP_RE = re.compile(r"https?://", re.IGNORECASE)
_NEGATED_CLAUSE_RE = re.compile(
    r"\b(?:no|not|unknown|unrelated|none)\b",
    re.IGNORECASE,
)
_BRACKETED_TEMPLATE_SLOT_RE = re.compile(
    r"(?:\[\s*|<\s*|\{\{?\s*)"
    r"[A-Za-z][A-Za-z0-9_]*(?:\s*,\s*[A-Za-z][A-Za-z0-9_]*)*"
    r"(?:\s*\]|\s*>|\s*\}\}?)"
)
_ALL_CAPS_TEMPLATE_SLOT_RE = re.compile(
    r"\b(?:POLICY_CHAIN_URL_[0-9]+|(?:[A-Z][A-Z0-9]*_)+[A-Z0-9]+|"
    r"LOW|HIGH|UNIT)\b"
)
_AGENT_AUTHORED_FIELDS = {
    "conditionalOn",
    "country",
    "dataPointId",
    "drivers",
    "historicalContext",
    "question",
    "reasoning",
    "resolutionDate",
    "resolutionRule",
    "resolutionSource",
    "resolutionSourceUrl",
    "runAt",
    "slug",
    "sourceContext",
    "title",
    "type",
    "unit",
}
_POPULATION_CUE_RE = re.compile(
    r"\b(?:touch(?:es|ed|ing)?|affect(?:s|ed|ing)?|eligible|"
    r"cover(?:s|ed|ing)?|appl(?:y|ies|ied|ying)\s+to|"
    r"exposed|treated|touched population|population|recipients?|"
    r"beneficiaries|participants?)\b",
    re.IGNORECASE,
)
_POPULATION_COUNT_NOUN_RE = re.compile(
    r"\b(?:count|people|persons?|households?|famil(?:y|ies)|children|"
    r"students?|teachers?|workers?|employees?|employers?|taxpayers?|"
    r"recipients?|beneficiaries|participants?|firms?|businesses|farms?|"
    r"claims?|returns?|acres?|contracts?|awards?|jobs?)\b",
    re.IGNORECASE,
)
_NUMBER_THEN_POPULATION_RE = re.compile(
    rf"{POLICY_CHAIN_NUMBER_RE.format(name='value')}\s*"
    rf"(?:(?:thousand|million|billion|trillion)s?\s+)?"
    rf"(?:(?:eligible|affected|covered|treated|exposed|touched)\s+)?"
    rf"{_POPULATION_COUNT_NOUN_RE.pattern}",
    re.IGNORECASE,
)
_PROPAGATION_RE = re.compile(
    r"\b(?:translat(?:e|es|ed|ion)|impli(?:es|ed|cation)|"
    r"response(?:s)?\s+(?:per|of|to)|effect(?:s)?\s+(?:on|per|of)|"
    r"elasticit(?:y|ies)|change in (?:the )?(?:(?:measured|target|forecast|"
    r"resolving) (?:quantity|outcome|series|rate|count|total|level)|"
    r"outcome|rate|count|total|level))\b",
    re.IGNORECASE,
)
_MEASURED_QUANTITY_RE = re.compile(
    r"\b(?:(?:measured|target|forecast|resolving)\s+"
    r"(?:quantity|outcome|series|effect|rate|count|total|level)|outcome|series)\b",
    re.IGNORECASE,
)
_PRECEDENT_EVIDENCE_RE = re.compile(
    r"\b(?:precedent|stud(?:y|ies)|evaluation|experiment|quasi[- ]experiment|"
    r"difference[- ]in[- ]differences|regression discontinuity|"
    r"instrumental variables?|causal estimate|impact estimate|"
    r"elasticit(?:y|ies))\b",
    re.IGNORECASE,
)
_OFFSET_RE = re.compile(
    r"(?:\boffset(?:s|ting)?\b.{0,40}\b(?:effect|response|gain|loss|it|them|"
    r"partly|reduce|halve|limit|erase)|\b(?:counteract(?:s|ed|ing)?|"
    r"attenuat(?:e|es|ed|ion)|"
    r"dampen(?:s|ed|ing)?|mitigat(?:e|es|ed|ion)|crowd(?:ing)?[- ]?out|"
    r"displac(?:e|es|ed|ement)|erase(?:s|d)?|partly\s+(?:undo|reverse)|"
    r"(?:behavioral|hiring|supply|demand)\s+responses?\s+"
    r"(?:reduce|limit|weaken))\b)",
    re.IGNORECASE,
)
_TIMING_RE = re.compile(
    r"(?:\bimplementation\b.{0,60}\b(?:lag|delay|timing|begin|start|take|"
    r"during|before|after|within|by|resolution|target)\b|"
    r"\b(?:lags?|delay(?:s|ed)?|phase[- ]?(?:in|out)|arriv(?:e|es|ed|al))"
    r"\b.{0,60}\b(?:effect|implementation|print|release|resolution|target|"
    r"months?|quarters?|years?)\b|"
    r"\b(?:before|after|within|by)\b.{0,60}\b(?:print|release|resolution|"
    r"target|months?|quarters?|years?)\b)",
    re.IGNORECASE,
)
_CLAUSE_BOUNDARY_RE = re.compile(r"[;\n]|(?<=[.!?])\s+")
_SENTENCE_BOUNDARY_RE = re.compile(r"\n+|(?<=[.!?])\s+")
_DATE_CUE_RE = re.compile(
    r"\b(?:years?|fy|cy|date|calendar|fiscal|release|resolution|period|"
    r"months?|quarters?|days?|weeks?|report|publication|vintage)\b",
    re.IGNORECASE,
)
_CONFIDENCE_TOKEN = (
    r"(?:ci\b|confidence(?:\s+interval)?\b|credible\s+interval\b|"
    r"level\s+of\s+confidence\b)"
)
_CONFIDENCE_SUFFIX_RE = re.compile(
    rf"^(?:(?:[^\w()]|\([^)]*\)))*"
    rf"(?:{_CONFIDENCE_TOKEN}|\([^)]*(?:{_CONFIDENCE_TOKEN})[^)]*\))",
    re.IGNORECASE,
)


def _number(name: str) -> str:
    return POLICY_CHAIN_NUMBER_RE.format(name=name)


_BRACKET_BOUND_RE = re.compile(
    rf"\b{POLICY_CHAIN_TERM_RE}\b\s*"
    rf"(?:\s+(?:is\s+)?(?:bound(?:ed)?|range))?\s*"
    rf"(?:\s+is)?\s*(?::|=)?\s*\[\s*{_number('low')}\s*,\s*"
    rf"{_number('high')}\s*\]",
    re.IGNORECASE,
)
_RANGE_BOUND_RE = re.compile(
    rf"\b{POLICY_CHAIN_TERM_RE}\b\s+(?:is\s+)?(?:"
    rf"in\s+(?:the\s+)?range(?:\s+of)?|ranges?\s+from|"
    rf"bound(?:ed)?\s+(?:between|from)|between|spans?)\s+"
    rf"{_number('low')}\s+(?:to|and|through)\s+{_number('high')}",
    re.IGNORECASE,
)
_INEQUALITY_BOUND_RE = re.compile(
    rf"{_number('low')}\s*(?:<=|≤)\s*\b{POLICY_CHAIN_TERM_RE}\b\s*"
    rf"(?:<=|≤)\s*{_number('high')}",
    re.IGNORECASE,
)
_SYMMETRIC_BOUND_RE = re.compile(
    rf"\b{POLICY_CHAIN_TERM_RE}\b\s+(?:is\s+)?"
    rf"(?:(?:bound(?:ed)?\s+)?(?:within|at)|bound(?:ed)?)\s+"
    rf"±\s*{_number('radius')}",
    re.IGNORECASE,
)
_ZERO_BOUND_RE = re.compile(
    rf"\b{POLICY_CHAIN_TERM_RE}\b\s+(?:"
    rf"bound(?:ed)?\s*(?:is\s*)?(?::|=)?|is\s+bounded\s+at|"
    rf"is\s+exactly|(?::|=))\s*(?P<zero>[+]?\s*0(?:\.0+)?)"
    rf"(?![\w.])",
    re.IGNORECASE,
)

_EXPLICIT_UNIT_RE = re.compile(
    r"^(?:%(?!\w)|(?:percentage points?|basis points?|index points?|percent(?:age)?|"
    r"pct|per[- ]cent|dollars?|usd|gbp|euros?|cents?|counts?|people|persons?|"
    r"households?|famil(?:y|ies)|children|students?|teachers?|workers?|"
    r"employees?|employers?|taxpayers?|recipients?|beneficiaries|"
    r"participants?|firms?|businesses|farms?|claims?|returns?|acres?|"
    r"contracts?|awards?|jobs?|units?|minutes?|hours?|days?|weeks?|"
    r"million cubic feet|mmcf|thousands?|millions?|billions?|trillions?)\b)",
    re.IGNORECASE,
)


def agent_version_enforces_policy_chain(agent_version: Any) -> bool:
    """Return whether a sealed analyst version owns the strengthened rubric."""

    if not isinstance(agent_version, str):
        return False
    match = _VERSION_RE.fullmatch(agent_version)
    if match is None:
        return False
    try:
        parts = tuple(int(match.group(name)) for name in ("major", "minor", "patch"))
    except ValueError:
        return False
    return parts >= POLICY_CHAIN_AGENT_VERSION_PARTS


def next_patch_agent_version(agent_version: Any) -> str:
    """Derive a mode-scoped contract version without relabeling future agents."""

    if not isinstance(agent_version, str):
        raise ValueError("base agent version must be a semantic-version string")
    match = _VERSION_RE.fullmatch(agent_version)
    if match is None:
        raise ValueError(f"base agent version is malformed: {agent_version!r}")
    major, minor, patch = (
        int(match.group(name)) for name in ("major", "minor", "patch")
    )
    return f"{major}.{minor}.{patch + 1}"


def policy_chain_urls(text: str) -> list[str]:
    """Extract cited HTTP(S) URLs without surrounding prose punctuation."""

    urls = []
    for match in POLICY_CHAIN_URL_RE.findall(text):
        url = match.rstrip(".,;:!?")
        for closing, opening in ((")", "("), ("]", "["), ("}", "{")):
            while url.endswith(closing) and url.count(closing) > url.count(opening):
                url = url[:-1]
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname
        except ValueError:
            continue
        if parsed.scheme.lower() in {"http", "https"} and hostname:
            urls.append(url)
    return urls


def _normalize_percent_escapes(value: str) -> str:
    def replace(match: re.Match[str]) -> str:
        byte = int(match.group(1), 16)
        character = chr(byte)
        return character if character in _UNRESERVED else f"%{byte:02X}"

    return _PERCENT_ESCAPE_RE.sub(replace, value)


def _remove_dot_segments(path: str) -> str:
    """RFC 3986 section 5.2.4 without collapsing distinct double slashes."""

    remaining = path
    output = ""
    while remaining:
        if remaining.startswith("../"):
            remaining = remaining[3:]
        elif remaining.startswith("./"):
            remaining = remaining[2:]
        elif remaining.startswith("/./"):
            remaining = "/" + remaining[3:]
        elif remaining == "/.":
            remaining = "/"
        elif remaining.startswith("/../"):
            remaining = "/" + remaining[4:]
            output = output.rsplit("/", 1)[0]
        elif remaining == "/..":
            remaining = "/"
            output = output.rsplit("/", 1)[0]
        elif remaining in {".", ".."}:
            remaining = ""
        else:
            separator = remaining.find("/", 1 if remaining.startswith("/") else 0)
            if separator < 0:
                output += remaining
                remaining = ""
            else:
                output += remaining[:separator]
                remaining = remaining[separator:]
    return output


def _redirect_surface_views(value: str) -> list[str]:
    views = []
    current = value
    for _ in range(4):
        views.append(current)
        decoded = unquote(current)
        if decoded == current:
            break
        current = decoded
    return views


def _is_unauthenticated_redirector(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return True
    surface = parsed.path + (f"?{parsed.query}" if parsed.query else "")
    return any(
        _ABSOLUTE_HTTP_RE.search(view) or _ENCODED_HTTP_RE.search(view)
        for view in _redirect_surface_views(surface)
    )


def _url_identity(url: str) -> tuple[str, int | None, str] | None:
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError:
        return None
    if parsed.scheme.lower() not in {"http", "https"} or not hostname:
        return None
    if (parsed.scheme.lower(), port) in {("http", 80), ("https", 443)}:
        port = None
    if _is_unauthenticated_redirector(url):
        return None
    normalized_host = _normalize_percent_escapes(hostname).lower().rstrip(".")
    path = _remove_dot_segments(_normalize_percent_escapes(parsed.path))
    path = path.rstrip("/") or "/"
    # HTTP-to-HTTPS redirects and query aliases do not turn an instrument or
    # series page into a distinct effect precedent. A precedent on a shared
    # endpoint must use a genuinely distinct path so this gate fails closed.
    return normalized_host, port, path


def _urls_in_value(value: Any) -> list[str]:
    if isinstance(value, str):
        return policy_chain_urls(value)
    if isinstance(value, dict):
        return [url for entry in value.values() for url in _urls_in_value(entry)]
    if isinstance(value, list):
        return [url for entry in value for url in _urls_in_value(entry)]
    return []


def _excluded_precedent_identities(
    cell: dict[str, Any], target_context: dict[str, Any] | None
) -> set[tuple[str, int | None, str]]:
    urls = []
    for field in ("conditionalOn", "resolutionSourceUrl"):
        urls.extend(_urls_in_value(cell.get(field)))
    if isinstance(target_context, dict):
        for key, value in target_context.items():
            lowered = key.lower()
            if lowered == "resolutionsourceurl" or any(
                cue in lowered
                for cue in (
                    "conditional",
                    "condition",
                    "bill",
                    "measure",
                    "instrument",
                )
            ):
                urls.extend(_urls_in_value(value))
        source_binding = target_context.get("sourceBinding")
        if isinstance(source_binding, dict):
            urls.extend(_urls_in_value(source_binding.get("sourceUrl")))
    return {identity for url in urls if (identity := _url_identity(url)) is not None}


def _parse_number(raw: str) -> float | None:
    try:
        value = float(re.sub(r"\s+", "", raw).replace(",", ""))
    except ValueError:
        return None
    return value if math.isfinite(value) else None


def _unit_alias_pattern(cell_unit: Any) -> re.Pattern[str] | None:
    if not isinstance(cell_unit, str) or not cell_unit.strip():
        return None
    canonical = cell_unit.strip()
    words = re.sub(r"[_-]+", " ", canonical)
    humanized = r"\s+".join(re.escape(word) for word in words.split())
    alternatives = [re.escape(canonical)]
    if humanized != alternatives[0]:
        alternatives.append(humanized)
    return re.compile(rf"^(?:{'|'.join(alternatives)})(?!\w)", re.IGNORECASE)


def _bound_has_unit(text: str, end: int, cell_unit: Any) -> bool:
    suffix = text[end:].lstrip()
    alias = _unit_alias_pattern(cell_unit)
    match = alias.match(suffix) if alias is not None else None
    if match is None:
        match = _EXPLICIT_UNIT_RE.match(suffix)
    if match is None:
        return False
    return _CONFIDENCE_SUFFIX_RE.match(suffix[match.end() :]) is None


def _year_like_endpoint(text: str, start: int, end: int, raw: str) -> bool:
    compact = re.sub(r"[+\s]", "", raw)
    if "," in compact:
        return False
    cleaned = compact
    if not re.fullmatch(r"[12]\d{3}", cleaned):
        return False
    window = text[max(0, start - 32) : min(len(text), end + 40)]
    return _DATE_CUE_RE.search(window) is not None


def _valid_two_endpoint_bound(text: str, match: re.Match[str], cell_unit: Any) -> bool:
    low_raw = match.group("low")
    high_raw = match.group("high")
    low = _parse_number(low_raw)
    high = _parse_number(high_raw)
    if low is None or high is None or low >= high:
        return False
    if _year_like_endpoint(text, match.start("low"), match.end("low"), low_raw):
        return False
    if _year_like_endpoint(text, match.start("high"), match.end("high"), high_raw):
        return False
    return _bound_has_unit(text, match.end(), cell_unit)


def has_numeric_policy_term_bound(text: str, cell_unit: Any = None) -> bool:
    """Recognize a finite, ordered, unit-bearing policy-effect bound."""

    for pattern in (_BRACKET_BOUND_RE, _RANGE_BOUND_RE, _INEQUALITY_BOUND_RE):
        if any(
            _valid_two_endpoint_bound(text, match, cell_unit)
            for match in pattern.finditer(text)
        ):
            return True
    for match in _SYMMETRIC_BOUND_RE.finditer(text):
        radius_raw = match.group("radius")
        radius = _parse_number(radius_raw)
        if radius is None or radius <= 0:
            continue
        if _year_like_endpoint(
            text, match.start("radius"), match.end("radius"), radius_raw
        ):
            continue
        if _bound_has_unit(text, match.end(), cell_unit):
            return True
    for match in _ZERO_BOUND_RE.finditer(text):
        if _bound_has_unit(text, match.end(), cell_unit):
            return True
    return False


def _clauses(text: str) -> list[str]:
    # Sentence punctuation inside a URL is never followed by whitespace, so
    # the boundary expression can operate directly on source text. Avoiding
    # substitution also removes an author-collidable placeholder namespace.
    return [part.strip() for part in _CLAUSE_BOUNDARY_RE.split(text) if part.strip()]


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in _SENTENCE_BOUNDARY_RE.split(text) if part.strip()]


def _affirmative_clauses(text: str) -> list[str]:
    return [
        clause for clause in _clauses(text) if not _NEGATED_CLAUSE_RE.search(clause)
    ]


def _agent_authored_strings(cell: dict[str, Any]) -> list[str]:
    def strings(value: Any) -> list[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return [text for entry in value for text in strings(entry)]
        if isinstance(value, dict):
            return [text for entry in value.values() for text in strings(entry)]
        return []

    return [
        text
        for field in _AGENT_AUTHORED_FIELDS
        if field in cell
        for text in strings(cell[field])
    ]


def _placeholder_tokens(cell: dict[str, Any]) -> list[str]:
    tokens = []
    for text in _agent_authored_strings(cell):
        for pattern in (_BRACKETED_TEMPLATE_SLOT_RE, _ALL_CAPS_TEMPLATE_SLOT_RE):
            for match in pattern.finditer(text):
                token = match.group(0)
                if token not in tokens:
                    tokens.append(token)
    return tokens


def _has_fetched_population_count(text: str) -> bool:
    for clause in _affirmative_clauses(text):
        if not (
            re.search(r"\bfetched\b", clause, re.IGNORECASE)
            and _POPULATION_CUE_RE.search(clause)
            and _POPULATION_COUNT_NOUN_RE.search(clause)
        ):
            continue
        for match in _NUMBER_THEN_POPULATION_RE.finditer(clause):
            value = _parse_number(match.group("value"))
            if value is None or value < 0:
                continue
            after = clause[match.end() : match.end() + 30]
            if re.match(
                r"\s*(?:%(?!\w)|percent(?:age)?\b|pct\b)",
                after,
                re.IGNORECASE,
            ):
                continue
            number_start = match.start("value")
            fetched = list(
                re.finditer(r"\bfetched\b", clause[:number_start], re.IGNORECASE)
            )
            if not fetched:
                continue
            between = clause[fetched[-1].end() : number_start]
            direct_count = re.fullmatch(
                r"\s*(?:(?:a|the)\s+)?(?:numeric\s+)?"
                r"(?:count|population|total)?\s*(?:of|is|=|:)?\s*",
                between,
                re.IGNORECASE,
            )
            fetched_source_count = re.search(
                r"\b(?:report|table|source|data|dataset|file|print|estimate)\b"
                r".{0,48}\b(?:reports?|shows?|counts?|lists?|gives?|finds?|"
                r"estimates?)(?:\s+(?:(?:a|the)\s+)?(?:count|population|"
                r"total)(?:\s+(?:of|is|=|:))?)?\s*$",
                between,
                re.IGNORECASE,
            )
            if direct_count is None and fetched_source_count is None:
                continue
            if not _year_like_endpoint(
                clause, match.start("value"), match.end("value"), match.group("value")
            ):
                return True
    return False


def _url_segment(text: str, url: str) -> str:
    """Return only the sentence containing ``url``."""

    return next((sentence for sentence in _sentences(text) if url in sentence), "")


def _precedent_is_tied_to_propagation(text: str, urls: list[str]) -> bool:
    return any(
        any(
            _PROPAGATION_RE.search(clause)
            and _MEASURED_QUANTITY_RE.search(clause)
            and _PRECEDENT_EVIDENCE_RE.search(clause)
            for clause in _affirmative_clauses(segment_without_url)
        )
        for url in urls
        if (segment := _url_segment(text, url))
        and (segment_without_url := POLICY_CHAIN_URL_RE.sub("", segment))
    )


def _has_propagation_component(text: str) -> bool:
    return any(
        _PROPAGATION_RE.search(clause)
        and _MEASURED_QUANTITY_RE.search(clause)
        and not _OFFSET_RE.search(clause)
        and not _TIMING_RE.search(clause)
        for clause in _affirmative_clauses(text)
    )


def conditional_target_context_errors(
    cell: dict[str, Any],
    *,
    target_context: dict[str, Any] | None,
    agent_version: Any,
) -> list[str]:
    """Keep a sealed conditional target from being relabeled to bypass the gate."""

    conditional = (
        target_context.get("conditional") if isinstance(target_context, dict) else None
    )
    if (
        agent_version_enforces_policy_chain(agent_version)
        and isinstance(conditional, str)
        and conditional.strip()
        and cell.get("type") != "conditional"
    ):
        return [
            "conditional policy chain: authenticated conditional target requires cell "
            "type 'conditional'"
        ]
    return []


def conditional_policy_chain_errors(
    cell: dict[str, Any], *, target_context: dict[str, Any] | None = None
) -> list[str]:
    """Validate every ordinary conditional Policy chain step fail-closed."""

    if cell.get("type") != "conditional":
        return []
    placeholder_errors = [
        "conditional policy chain: agent-authored text contains an unsubstituted "
        f"placeholder token: {token!r}"
        for token in _placeholder_tokens(cell)
    ]
    reasoning = cell.get("reasoning")
    policy_steps = []
    if isinstance(reasoning, list):
        policy_steps = [
            step["text"]
            for step in reasoning
            if isinstance(step, dict)
            and isinstance(step.get("text"), str)
            and step["text"].startswith("Policy chain:")
        ]
    if not policy_steps:
        return [
            *placeholder_errors,
            "conditional policy chain: missing reasoning step beginning exactly "
            "'Policy chain:'",
        ]

    source_context = cell.get("sourceContext")
    source_urls = (
        {entry for entry in source_context if isinstance(entry, str)}
        if isinstance(source_context, list)
        else set()
    )
    excluded = _excluded_precedent_identities(cell, target_context)
    all_errors = list(placeholder_errors)
    for text in policy_steps:
        errors = []
        component_text = POLICY_CHAIN_URL_RE.sub("", text)
        if not _has_fetched_population_count(component_text):
            errors.append(
                "conditional policy chain: Policy chain step must state a fetched "
                "numeric count for the touched population"
            )
        if not any(
            _OFFSET_RE.search(clause) for clause in _affirmative_clauses(component_text)
        ):
            errors.append(
                "conditional policy chain: Policy chain step must state offsetting "
                "responses"
            )
        if not any(
            _TIMING_RE.search(clause) for clause in _affirmative_clauses(component_text)
        ):
            errors.append(
                "conditional policy chain: Policy chain step must state timing or lag"
            )

        if "no fetched precedent" in text:
            text_without_urls = POLICY_CHAIN_URL_RE.sub("", text)
            if not _has_propagation_component(text_without_urls):
                errors.append(
                    "conditional policy chain: Policy chain step must state "
                    "propagation to the measured quantity"
                )
            if not has_numeric_policy_term_bound(text_without_urls, cell.get("unit")):
                errors.append(
                    "conditional policy chain: 'no fetched precedent' path must "
                    "state a numeric policy-term bound"
                )
            if not re.search(
                rf"(?:\blow-confidence\s+{POLICY_CHAIN_TERM_RE}\b|"
                rf"\b{POLICY_CHAIN_TERM_RE}\b\s*(?::|-)?\s*"
                rf"(?:is\s+|remains\s+|(?:is\s+)?label(?:ed)?(?:\s+as)?\s+)?"
                rf"\blow-confidence\b|"
                rf"\blabel(?:ed)?\s+(?:the\s+)?{POLICY_CHAIN_TERM_RE}\b\s+"
                rf"(?:as\s+)?\blow-confidence\b)",
                text_without_urls,
                re.IGNORECASE,
            ):
                errors.append(
                    "conditional policy chain: 'no fetched precedent' path must "
                    "label the policy term low-confidence"
                )
        else:
            cited_urls = policy_chain_urls(text)
            eligible_urls = []
            redirector_urls = [
                url for url in cited_urls if _is_unauthenticated_redirector(url)
            ]
            for url in cited_urls:
                identity = _url_identity(url)
                if identity is not None and identity not in excluded:
                    eligible_urls.append(url)
            if not cited_urls:
                errors.append(
                    "conditional policy chain: Policy chain step must cite a "
                    "precedent URL also listed exactly in sourceContext or contain "
                    "exact phrase 'no fetched precedent'"
                )
            elif redirector_urls or not eligible_urls:
                errors.append(
                    "conditional policy chain: precedent URL must be distinct from "
                    "the conditional instrument and resolution source URLs"
                )
            for url in eligible_urls:
                if url not in source_urls:
                    errors.append(
                        "conditional policy chain: precedent URL in Policy chain "
                        "step is not listed exactly in sourceContext: "
                        f"{url!r}"
                    )
            if eligible_urls and not _precedent_is_tied_to_propagation(
                text, eligible_urls
            ):
                errors.append(
                    "conditional policy chain: Policy chain step must tie propagation "
                    "to a cited precedent URL"
                )
            elif not eligible_urls and not _has_propagation_component(text):
                errors.append(
                    "conditional policy chain: Policy chain step must state "
                    "propagation to the measured quantity"
                )
        for error in errors:
            if error not in all_errors:
                all_errors.append(error)
    return all_errors
