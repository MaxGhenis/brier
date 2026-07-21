#!/usr/bin/env python3
"""Report briefing usage and source overlap for recorded runs.

The briefed-versus-unbriefed contrast measures the marginal value of
curated provision, and a null result is uninterpretable without usage
observability (docs/ontology.md): did the briefed run draw on the
briefing, and did the unbriefed control independently fetch the same
sources? This reads a run's archived activity (codex_events.jsonl) and
compares the URLs it actually fetched against a briefing manifest.

A briefing manifest is a JSON file: {"briefingId": "...", "sources":
["https://...", ...]}. Overlap matches on host+path prefix so mirrors
and query-string variants of the same document count as the same source.

Usage:
  briefing_usage_report.py RUN_DIR --manifest BRIEFING.json [--json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from urllib.parse import urlparse

URL_PATTERN = re.compile(r"""https?://[^\s"'<>)\]\\]+""")


def normalize_source(url: str) -> str:
    """host + path, lowercased, trailing slash stripped — query dropped."""
    parsed = urlparse(url.strip())
    host = (parsed.hostname or "").lower()
    path = parsed.path.rstrip("/").lower()
    return f"{host}{path}"


def fetched_urls(run_dir: pathlib.Path) -> set[str]:
    """Every URL that appears in the run's archived activity events."""
    urls: set[str] = set()
    for events_path in sorted(run_dir.glob("*codex_events.jsonl")):
        for line in events_path.read_text().splitlines():
            if not line.strip():
                continue
            urls.update(URL_PATTERN.findall(line))
    return urls


def usage_report(
    run_urls: set[str], briefing_sources: list[str]
) -> dict[str, object]:
    normalized_run = {normalize_source(url) for url in run_urls}
    matched: list[str] = []
    unmatched: list[str] = []
    for source in briefing_sources:
        key = normalize_source(source)
        if key and any(
            candidate == key or candidate.startswith(key + "/")
            for candidate in normalized_run
        ):
            matched.append(source)
        else:
            unmatched.append(source)
    total = len(briefing_sources)
    return {
        "briefingSources": total,
        "sourcesDrawnOn": len(matched),
        "overlapShare": round(len(matched) / total, 3) if total else None,
        "matched": matched,
        "unmatched": unmatched,
        "runUrlCount": len(run_urls),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    run_dir = pathlib.Path(args.run_dir)
    if not run_dir.is_dir():
        print(f"not a run directory: {run_dir}", file=sys.stderr)
        return 1
    manifest = json.loads(pathlib.Path(args.manifest).read_text())
    sources = manifest.get("sources")
    if not isinstance(sources, list) or not all(
        isinstance(item, str) for item in sources
    ):
        print("manifest must carry a 'sources' list of URLs", file=sys.stderr)
        return 1

    report = {
        "runDir": str(run_dir),
        "briefingId": manifest.get("briefingId"),
        **usage_report(fetched_urls(run_dir), sources),
    }
    if args.json:
        print(json.dumps(report, indent=1))
    else:
        print(
            f"{report['briefingId']}: drew on {report['sourcesDrawnOn']} of "
            f"{report['briefingSources']} briefing sources "
            f"(overlap {report['overlapShare']}); run fetched "
            f"{report['runUrlCount']} distinct URLs"
        )
        for source in report["unmatched"]:
            print(f"  not drawn on: {source}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
