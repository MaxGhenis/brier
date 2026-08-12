"""The private-source provenance screen, shared by every projection.

One JSON file (site/src/data/private-source-screen.json) defines the
pattern, its flags, the withholding marker, and behavioral probes. The
spawned-cell converter REFUSES agent-authored text that matches;
reviewer-authored preSubmitReview text is WITHHELD behind the marker in
every published projection (spawned cells, live comparisons, strategy
comparisons) while the immutable run record keeps the original; and the
site's forecast-catalog test enforces the same pattern over the whole
public payload as the fail-closed backstop. Import from here so no
projection can drift from the backstop.
"""

from __future__ import annotations

import json
import pathlib
import re
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCREEN_PATH = ROOT / "site" / "src" / "data" / "private-source-screen.json"

_SCREEN = json.loads(SCREEN_PATH.read_text())

_FLAGS = _SCREEN.get("flags", "")
if _FLAGS != "i":
    # Both engines must agree on case handling; the canary pins "i" and
    # anything else means the shared file was edited without review.
    raise RuntimeError(f"private-source screen flags must be 'i', got {_FLAGS!r}")

# The expected inventory is pinned HERE, outside the mutable JSON (the
# site test pins the same literals): deleting a branch together with its
# sole probe now requires editing reviewed code in both engines, not one
# data file.
_EXPECTED_ALTERNATIONS = (
    "granola",
    "\\btranscripts?\\b",
    "meeting notes?",
    "meeting with max",
    "pasted-text",
    "\\.codex/attachments",
    "codex attachments",
    "private meeting",
    "call notes?",
    "email thread",
)
_EXPECTED_PROBE_COUNT = 21

PRIVATE_SOURCE_ALTERNATIONS: list[str] = _SCREEN["alternations"]
if tuple(PRIVATE_SOURCE_ALTERNATIONS) != _EXPECTED_ALTERNATIONS:
    raise RuntimeError(
        "private-source screen alternations diverge from the pinned inventory"
    )
PRIVATE_SOURCE_PATTERN: str = "|".join(PRIVATE_SOURCE_ALTERNATIONS)
# ASCII case folding: JavaScript's bare "i" flag does not apply Unicode
# case folding, so Python must not either (U+017F long s, dotless i, and
# fullwidth letters would otherwise split the two engines).
PRIVATE_SOURCE_RE = re.compile(PRIVATE_SOURCE_PATTERN, re.IGNORECASE | re.ASCII)
PRIVATE_SOURCE_MARKER: str = _SCREEN["marker"]
PRIVATE_SOURCE_PROBES: list[dict[str, Any]] = _SCREEN["probes"]
if len(PRIVATE_SOURCE_PROBES) != _EXPECTED_PROBE_COUNT:
    raise RuntimeError(
        f"private-source screen must carry exactly {_EXPECTED_PROBE_COUNT} "
        f"probes, found {len(PRIVATE_SOURCE_PROBES)}"
    )

if PRIVATE_SOURCE_RE.search(PRIVATE_SOURCE_MARKER):
    raise RuntimeError("the private-source marker must not match its own screen")
for _probe in PRIVATE_SOURCE_PROBES:
    if bool(PRIVATE_SOURCE_RE.search(_probe["text"])) != bool(_probe["match"]):
        raise RuntimeError(
            "private-source screen probe failed at import: "
            f"{_probe['text']!r} expected match={_probe['match']}"
        )
# Every alternation must be the sole match for at least one probe, so a
# deleted or weakened branch fails even when a broader branch still
# matches the probe text.
for _branch in PRIVATE_SOURCE_ALTERNATIONS:
    _branch_re = re.compile(_branch, re.IGNORECASE | re.ASCII)
    _others = re.compile(
        "|".join(b for b in PRIVATE_SOURCE_ALTERNATIONS if b != _branch),
        re.IGNORECASE | re.ASCII,
    )
    if not any(
        probe.get("sole") == _branch
        and _branch_re.search(probe["text"])
        and not _others.search(probe["text"])
        for probe in PRIVATE_SOURCE_PROBES
    ):
        raise RuntimeError(
            f"no sole-match probe pins the screen branch {_branch!r}"
        )


def screen_pre_submit_review(review: dict) -> dict:
    """Withhold reviewer-authored text that matches the private-source screen.

    Agent-authored cell text is REFUSED on a hit: the agent controls its
    own citations. Reviewer commentary is different — the reviewer writes
    about the run ("attach the fetch transcript") without citing anything,
    and its wording is not evidence. Refusing the whole run for a
    reviewer's word choice burns runs nondeterministically, so published
    projections withhold the matching string behind an explicit marker
    instead. Whole-string replacement only: no partial substitution that
    could splice attacker-chosen text around the marker.
    """

    def clean(value: object) -> object:
        if isinstance(value, str):
            return PRIVATE_SOURCE_MARKER if PRIVATE_SOURCE_RE.search(value) else value
        if isinstance(value, list):
            return [clean(item) for item in value]
        if isinstance(value, dict):
            # A matching KEY is not screenable in place (replacing keys
            # invites collisions), and well-typed review metadata never
            # carries content-bearing keys - withhold the whole node.
            if any(
                isinstance(key, str) and PRIVATE_SOURCE_RE.search(key)
                for key in value
            ):
                return PRIVATE_SOURCE_MARKER
            return {key: clean(item) for key, item in value.items()}
        return value

    return clean(review)  # type: ignore[return-value]
