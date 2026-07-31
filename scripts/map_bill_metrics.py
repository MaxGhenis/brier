#!/usr/bin/env python3
"""Map bill metrics to the Thesis docket series registry.

The mapper is deliberately proposal-only.  It annotates a copy of the bill
artifact and writes leads for hinted series that are not yet registered, but
it never changes the docket or any record artifact.

Usage:
    python scripts/map_bill_metrics.py bills/<slug>.json
    python scripts/map_bill_metrics.py bills/<slug>.json \
        --docket scripts/docket_series.json
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import tempfile
from collections.abc import Sequence

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_DOCKET = ROOT / "scripts" / "docket_series.json"
DEFAULT_DRAFTS_DIR = ROOT / "drafts" / "ledger-entries"
RECORDS_DIR = ROOT / "records"


class MappingError(ValueError):
    """Raised when a bill or docket artifact cannot be mapped safely."""


def load_registered_series(docket_path: pathlib.Path) -> list[str]:
    """Load registered series concept IDs, preserving docket order."""
    docket = json.loads(docket_path.read_text(encoding="utf-8"))
    if not isinstance(docket, dict) or not isinstance(docket.get("series"), list):
        raise MappingError("docket must be an object with a series array")

    registered: list[str] = []
    for index, entry in enumerate(docket["series"]):
        if not isinstance(entry, dict):
            raise MappingError(f"docket series entry {index} must be an object")
        concept = entry.get("series")
        if not isinstance(concept, str) or not concept.strip():
            raise MappingError(
                f"docket series entry {index} must have a nonempty series"
            )
        registered.append(concept.strip())
    return registered


def match_registered_series(hint: str, registered: Sequence[str]) -> str | None:
    """Return the exact or first dot-descendant registry match for ``hint``."""
    for concept in registered:
        if concept == hint:
            return concept
    prefix = f"{hint}."
    for concept in registered:
        if concept.startswith(prefix):
            return concept
    return None


def slugify_hint(hint: str) -> str:
    """Convert a dotted series hint to the repository's filename style."""
    slug = re.sub(r"[^a-z0-9]+", "-", hint.lower()).strip("-")
    if not slug:
        raise MappingError(f"series_hint cannot form a draft filename: {hint!r}")
    return slug


def bill_slug(artifact: dict, input_path: pathlib.Path) -> str:
    """Read the canonical slug from the bill artifact."""
    bill = artifact.get("bill")
    slug = bill.get("slug") if isinstance(bill, dict) else None
    if not isinstance(slug, str) or not slug.strip():
        raise MappingError(f"{input_path} must contain a nonempty bill.slug")
    return slug.strip()


def _assert_not_records(path: pathlib.Path) -> None:
    try:
        path.resolve().relative_to(RECORDS_DIR.resolve())
    except ValueError:
        return
    raise MappingError(f"refusing to write under records/: {path}")


def _assert_not_source(path: pathlib.Path, *sources: pathlib.Path) -> None:
    resolved = path.resolve()
    for source in sources:
        if resolved == source.resolve():
            raise MappingError(f"refusing to overwrite source artifact: {source}")


def mapped_output_path(input_path: pathlib.Path) -> pathlib.Path:
    """Return ``<input-stem>.mapped.json`` beside the input artifact."""
    if input_path.suffix == ".json":
        return input_path.with_suffix(".mapped.json")
    return input_path.with_name(f"{input_path.name}.mapped.json")


def map_artifact(
    artifact: dict, registered: Sequence[str], *, proposed_from: str
) -> tuple[dict, list[dict]]:
    """Annotate an artifact in place and return its unique draft proposals."""
    provisions = artifact.get("provisions")
    if not isinstance(provisions, list):
        raise MappingError("bill artifact must contain a provisions array")

    summary = {"reachable": 0, "notYet": 0, "unmapped": 0}
    proposals_by_hint: dict[str, dict] = {}

    for provision_index, provision in enumerate(provisions):
        if not isinstance(provision, dict):
            raise MappingError(f"provision {provision_index} must be an object")
        metrics = provision.get("metrics")
        if not isinstance(metrics, list):
            raise MappingError(
                f"provision {provision_index} must contain a metrics array"
            )

        for metric_index, metric in enumerate(metrics):
            if not isinstance(metric, dict):
                raise MappingError(
                    f"provision {provision_index} metric {metric_index} "
                    "must be an object"
                )
            raw_hint = metric.get("series_hint")
            if raw_hint is not None and not isinstance(raw_hint, str):
                raise MappingError(
                    f"provision {provision_index} metric {metric_index} "
                    "series_hint must be a string or null"
                )
            hint = raw_hint.strip() if isinstance(raw_hint, str) else ""
            match = match_registered_series(hint, registered) if hint else None

            metric.pop("matched_series", None)
            if match is not None:
                metric["registry"] = "reachable"
                metric["matched_series"] = match
                summary["reachable"] += 1
            elif hint:
                metric["registry"] = "not-yet"
                summary["notYet"] += 1
                proposals_by_hint.setdefault(
                    hint,
                    {
                        "series": hint,
                        "cadence": None,
                        "slug": None,
                        "proposedFrom": proposed_from,
                        "metricText": metric.get("text"),
                    },
                )
            else:
                metric["registry"] = "unmapped"
                summary["unmapped"] += 1

    artifact["summary"] = summary
    return artifact, list(proposals_by_hint.values())


def write_json(path: pathlib.Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", text=True
    )
    temporary_path = pathlib.Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as temporary:
            temporary.write(body)
        temporary_path.chmod(0o644)
        temporary_path.replace(path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def map_bill_metrics(
    input_path: pathlib.Path,
    docket_path: pathlib.Path = DEFAULT_DOCKET,
    *,
    drafts_dir: pathlib.Path = DEFAULT_DRAFTS_DIR,
) -> tuple[pathlib.Path, list[pathlib.Path]]:
    """Map one bill artifact and write its mapped copy and draft proposals."""
    artifact = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(artifact, dict):
        raise MappingError("bill artifact must be a JSON object")

    proposed_from = bill_slug(artifact, input_path)
    registered = load_registered_series(docket_path)
    mapped, proposals = map_artifact(
        artifact, registered, proposed_from=proposed_from
    )

    output_path = mapped_output_path(input_path)
    _assert_not_records(output_path)
    _assert_not_records(drafts_dir)
    _assert_not_source(output_path, input_path, docket_path)

    planned_drafts: list[tuple[pathlib.Path, dict]] = []
    slugs: dict[str, str] = {}
    for proposal in proposals:
        hint = proposal["series"]
        draft_slug = slugify_hint(hint)
        previous_hint = slugs.setdefault(draft_slug, hint)
        if previous_hint != hint:
            raise MappingError(
                "series hints produce the same draft filename: "
                f"{previous_hint!r} and {hint!r}"
            )
        draft_path = drafts_dir / f"{draft_slug}.json"
        _assert_not_records(draft_path)
        _assert_not_source(draft_path, input_path, docket_path)
        if draft_path.exists():
            try:
                existing = json.loads(draft_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                raise MappingError(
                    f"existing draft is not readable JSON: {draft_path}"
                ) from error
            existing_hint = (
                existing.get("series") if isinstance(existing, dict) else None
            )
            if existing_hint != hint:
                raise MappingError(
                    f"draft filename {draft_path.name} already belongs to "
                    f"series {existing_hint!r}, not {hint!r}"
                )
        planned_drafts.append((draft_path, proposal))

    for draft_path, proposal in planned_drafts:
        write_json(draft_path, proposal)
    write_json(output_path, mapped)
    return output_path, [path for path, _ in planned_drafts]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Map bill metrics to registered Thesis docket series."
    )
    parser.add_argument("input", type=pathlib.Path, help="bill artifact JSON")
    parser.add_argument(
        "--docket",
        type=pathlib.Path,
        default=DEFAULT_DOCKET,
        help=f"series registry (default: {DEFAULT_DOCKET.relative_to(ROOT)})",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    output_path, draft_paths = map_bill_metrics(args.input, args.docket)
    summary = json.loads(output_path.read_text(encoding="utf-8"))["summary"]
    print(
        f"wrote {output_path} "
        f"(reachable={summary['reachable']}, not-yet={summary['notYet']}, "
        f"unmapped={summary['unmapped']}, drafts={len(draft_paths)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
