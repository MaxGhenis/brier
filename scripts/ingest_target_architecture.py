#!/usr/bin/env python3
"""Atomically mirror a published Thesis target-architecture snapshot.

The public site remains the source of truth.  This tool downloads the root
manifest and every chunk before opening a database connection, verifies all
canonical hashes and root bindings, then loads a new generation in one
transaction.  A verified staging schema is atomically renamed to
``thesis_projection_active`` and the public singleton pointer is advanced.

Only psycopg is required for live database work; downloads use urllib from the
standard library.  ``--dry-run`` verifies the complete publication without a
database.  ``--verify`` compares every logical database row and canonical row
digest with the current live root and exits nonzero on any drift.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import decimal
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from canonical_json import canonical_sha256

MANIFEST_SCHEMA = "thesis_target_architecture_manifest_v2"
CHUNK_SCHEMA = "thesis_target_architecture_chunk_v2"
ACTIVE_SCHEMA = "thesis_projection_active"
ROOT_PATTERN = re.compile(r"^[0-9a-f]{64}$")

# Insertion order respects the public target schema's foreign-key order.
TABLES = {
    "artifactRefs": "artifact_refs",
    "targets": "targets",
    "targetVersions": "target_versions",
    "sourceSeries": "source_series",
    "observations": "observations",
    "observationVintages": "observation_vintages",
    "targetObservationBindings": "target_observation_bindings",
    "baselineCandidates": "baseline_candidates",
    "forecastStrategies": "forecast_strategies",
    "strategyVersions": "strategy_versions",
    "packs": "packs",
    "packVersions": "pack_versions",
    "forecastRuns": "forecast_runs",
    "runArtifactRefs": "run_artifact_refs",
    "runPackVersions": "run_pack_versions",
    "forecastDistributions": "forecast_distributions",
    "reasoningEvents": "reasoning_events",
    "reviewRuns": "review_runs",
    "judgeRuns": "judge_runs",
    "toolCalls": "tool_calls",
    "resolutionEvents": "resolution_events",
    "scores": "scores",
}


@dataclass(frozen=True)
class Snapshot:
    manifest: dict[str, Any]
    rows: dict[str, list[dict[str, Any]]]

    @property
    def root(self) -> str:
        return self.manifest["projectionRootSha256"]


class SnapshotError(ValueError):
    """The published snapshot is incomplete or fails a commitment."""


class DriftError(ValueError):
    """The active replica differs from the committed site snapshot."""


def snake(name: str) -> str:
    return re.sub(r"(?<=[a-zA-Z0-9])([A-Z])", r"_\1", name).lower()


def row_digest(row: dict[str, Any]) -> str:
    """Return the cross-language canonical digest of one projection row."""

    return canonical_sha256(row)


def chunk_hash_payload(chunk: dict[str, Any]) -> dict[str, Any]:
    payload = dict(chunk)
    payload.pop("projectionRootSha256", None)
    return payload


def root_hash_payload(manifest: dict[str, Any]) -> dict[str, Any]:
    payload = dict(manifest)
    payload.pop("projectionRootSha256", None)
    return payload


def table_hash_payload(entry: dict[str, Any]) -> dict[str, Any]:
    payload = dict(entry)
    payload.pop("sha256", None)
    return payload


def fetch_json(url: str, source_dir: Path | None = None) -> dict[str, Any]:
    if source_dir is not None:
        parsed = urllib.parse.urlparse(url)
        relative = parsed.path.lstrip("/")
        path = source_dir / relative
        try:
            value = json.loads(path.read_text())
        except FileNotFoundError as exc:
            raise SnapshotError(f"missing downloaded surface: {path}") from exc
        if not isinstance(value, dict):
            raise SnapshotError(f"JSON surface is not an object: {path}")
        return value

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "thesis-projection-ingest/2"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        value = json.load(response)
    if not isinstance(value, dict):
        raise SnapshotError(f"JSON surface is not an object: {url}")
    return value


def download_snapshot(base: str, source_dir: Path | None = None) -> Snapshot:
    """Download all bytes first, then return only a fully verified snapshot."""

    base = base.rstrip("/") + "/"
    manifest_url = urllib.parse.urljoin(base, "targets.json")
    manifest = fetch_json(manifest_url, source_dir)
    validate_root_manifest(manifest)

    rows_by_table: dict[str, list[dict[str, Any]]] = {}
    for entry in manifest["tables"]:
        table = entry["table"]
        table_rows: list[dict[str, Any]] = []
        for reference in entry["chunks"]:
            url = urllib.parse.urljoin(manifest_url, reference["url"])
            chunk = fetch_json(url, source_dir)
            validate_chunk(manifest, entry, reference, chunk)
            table_rows.extend(chunk["rows"])
        if len(table_rows) != entry["rowCount"]:
            raise SnapshotError(
                f"{table}: downloaded {len(table_rows)} rows, "
                f"manifest commits {entry['rowCount']}"
            )
        rows_by_table[table] = table_rows
    return Snapshot(manifest=manifest, rows=rows_by_table)


def validate_root_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("schemaVersion") != MANIFEST_SCHEMA:
        raise SnapshotError(
            f"unsupported manifest schema: {manifest.get('schemaVersion')!r}"
        )
    root = manifest.get("projectionRootSha256")
    if not isinstance(root, str) or not ROOT_PATTERN.fullmatch(root):
        raise SnapshotError("manifest projectionRootSha256 is not lowercase SHA-256")
    if manifest.get("hashAlgorithm") != "sha256":
        raise SnapshotError("manifest hashAlgorithm must be sha256")
    if manifest.get("hashCanonicalization") != "canonical_json_v1":
        raise SnapshotError("manifest canonicalization is unsupported")
    if (
        manifest.get("chunkHashSemantics")
        != "canonical_chunk_without_projection_root_v1"
    ):
        raise SnapshotError("manifest chunk hash semantics are unsupported")
    if not manifest.get("builderVersion") or not manifest.get("sourceCommit"):
        raise SnapshotError("manifest must name builderVersion and sourceCommit")

    tables = manifest.get("tables")
    if not isinstance(tables, list):
        raise SnapshotError("manifest tables must be a list")
    names = [entry.get("table") for entry in tables if isinstance(entry, dict)]
    if len(names) != len(tables) or len(names) != len(set(names)):
        raise SnapshotError("manifest table entries must be unique objects")
    if set(names) != set(TABLES):
        raise SnapshotError(
            "manifest table set differs from ingest contract: "
            f"missing={sorted(set(TABLES) - set(names))}, "
            f"unknown={sorted(set(names) - set(TABLES))}"
        )

    for entry in tables:
        table = entry["table"]
        chunks = entry.get("chunks")
        if not isinstance(chunks, list) or not chunks:
            raise SnapshotError(f"{table}: chunks must be non-empty")
        if entry.get("chunkCount") != len(chunks):
            raise SnapshotError(f"{table}: chunkCount mismatch")
        if [chunk.get("index") for chunk in chunks] != list(range(len(chunks))):
            raise SnapshotError(f"{table}: chunk indexes are not contiguous")
        if sum(chunk.get("rowCount", -1) for chunk in chunks) != entry.get(
            "rowCount"
        ):
            raise SnapshotError(f"{table}: chunk row counts do not sum")
        count_key = (
            "forecastDistributionPoints"
            if table == "forecastDistributions"
            else table
        )
        if manifest.get("counts", {}).get(count_key) != entry.get("rowCount"):
            raise SnapshotError(f"{table}: projection count does not match table")
        expected_table_url = f"/forecasts/targets/{table}/manifest.json"
        if entry.get("url") != expected_table_url:
            raise SnapshotError(f"{table}: unexpected table-manifest URL")
        expected_table_hash = entry.get("sha256")
        actual_table_hash = canonical_sha256(table_hash_payload(entry))
        if expected_table_hash != actual_table_hash:
            raise SnapshotError(
                f"{table}: table manifest sha256 mismatch: "
                f"expected {expected_table_hash}, got {actual_table_hash}"
            )
        for chunk in chunks:
            if not ROOT_PATTERN.fullmatch(str(chunk.get("sha256", ""))):
                raise SnapshotError(
                    f"{table} chunk {chunk.get('index')}: invalid sha256"
                )
            expected_url = f"/forecasts/targets/{table}/{chunk['index']}.json"
            if chunk.get("url") != expected_url:
                raise SnapshotError(
                    f"{table} chunk {chunk['index']}: unexpected URL"
                )

    actual_root = canonical_sha256(root_hash_payload(manifest))
    if actual_root != root:
        raise SnapshotError(
            f"projection root mismatch: expected {root}, got {actual_root}"
        )


def validate_chunk(
    manifest: dict[str, Any],
    table_entry: dict[str, Any],
    reference: dict[str, Any],
    chunk: dict[str, Any],
) -> None:
    table = table_entry["table"]
    index = reference["index"]
    if chunk.get("schemaVersion") != CHUNK_SCHEMA:
        raise SnapshotError(f"{table} chunk {index}: unsupported schema")
    if chunk.get("projectionRootSha256") != manifest["projectionRootSha256"]:
        raise SnapshotError(f"{table} chunk {index}: mixed projection root")
    if chunk.get("projectionSchemaVersion") != manifest["projectionSchemaVersion"]:
        raise SnapshotError(f"{table} chunk {index}: projection schema mismatch")
    if chunk.get("generatedAt") != manifest["generatedAt"]:
        raise SnapshotError(f"{table} chunk {index}: generatedAt mismatch")
    if chunk.get("chunkSize") != manifest["chunkSize"]:
        raise SnapshotError(f"{table} chunk {index}: chunkSize mismatch")
    rows = chunk.get("rows")
    if (
        chunk.get("table") != table
        or chunk.get("chunkIndex") != index
        or not isinstance(rows, list)
        or chunk.get("rowCount") != len(rows)
        or reference["rowCount"] != len(rows)
    ):
        raise SnapshotError(f"{table} chunk {index}: identity or rowCount mismatch")
    if not all(isinstance(row, dict) for row in rows):
        raise SnapshotError(f"{table} chunk {index}: every row must be an object")
    actual_hash = canonical_sha256(chunk_hash_payload(chunk))
    if actual_hash != reference["sha256"]:
        raise SnapshotError(
            f"{table} chunk {index}: sha256 mismatch: "
            f"expected {reference['sha256']}, got {actual_hash}"
        )


def table_columns(conn: Any, schema: str, table: str) -> dict[str, str]:
    rows = conn.execute(
        """
        select column_name, data_type
        from information_schema.columns
        where table_schema = %s and table_name = %s
        order by ordinal_position
        """,
        (schema, table),
    ).fetchall()
    return dict(rows)


def adapt(value: Any, data_type: str, psycopg: Any) -> Any:
    if value is None:
        return None
    if data_type == "jsonb":
        return psycopg.types.json.Jsonb(value)
    if data_type == "ARRAY":
        return list(value)
    return value


def create_staging_schema(conn: Any, schema: str, psycopg: Any) -> None:
    sql = psycopg.sql
    conn.execute(
        sql.SQL("drop schema if exists {} cascade").format(sql.Identifier(schema))
    )
    conn.execute(sql.SQL("create schema {}").format(sql.Identifier(schema)))
    for table in TABLES.values():
        conn.execute(
            sql.SQL("create table {}.{} (like public.{} including all)").format(
                sql.Identifier(schema),
                sql.Identifier(table),
                sql.Identifier(table),
            )
        )
        conn.execute(
            sql.SQL(
                "alter table {}.{} "
                "add column _projection_row_payload jsonb not null, "
                "add column _projection_row_digest text not null, "
                "add column _projection_keys text[] not null"
            ).format(sql.Identifier(schema), sql.Identifier(table))
        )


def load_table(
    conn: Any,
    schema: str,
    table_key: str,
    rows: list[dict[str, Any]],
    psycopg: Any,
) -> None:
    table = TABLES[table_key]
    columns = table_columns(conn, schema, table)
    logical_columns = {
        key: snake(key)
        for row in rows
        for key in row
    }
    unknown = sorted(
        key for key, column in logical_columns.items() if column not in columns
    )
    if unknown:
        raise DriftError(
            f"{table}: projection fields have no database column: {unknown}"
        )

    groups: dict[tuple[str, ...], list[dict[str, Any]]] = collections.defaultdict(list)
    for row in rows:
        groups[tuple(sorted(row))].append(row)

    sql = psycopg.sql
    for keys, group_rows in groups.items():
        database_columns = [logical_columns[key] for key in keys]
        copy_columns = database_columns + [
            "_projection_row_payload",
            "_projection_row_digest",
            "_projection_keys",
        ]
        statement = sql.SQL("copy {}.{} ({}) from stdin").format(
            sql.Identifier(schema),
            sql.Identifier(table),
            sql.SQL(", ").join(map(sql.Identifier, copy_columns)),
        )
        with conn.cursor() as cursor:
            with cursor.copy(statement) as copy:
                for row in group_rows:
                    values = [
                        adapt(row[key], columns[logical_columns[key]], psycopg)
                        for key in keys
                    ]
                    values.extend(
                        [
                            psycopg.types.json.Jsonb(row),
                            row_digest(row),
                            list(keys),
                        ]
                    )
                    copy.write_row(tuple(values))


def semantic_equal(actual: Any, expected: Any, data_type: str) -> bool:
    if expected is None:
        return actual is None
    if data_type == "numeric":
        return actual == decimal.Decimal(str(expected))
    if data_type in {"smallint", "integer", "bigint"}:
        return actual == int(expected)
    if data_type == "double precision" or data_type == "real":
        return actual == float(expected)
    if data_type == "date":
        return actual == dt.date.fromisoformat(str(expected))
    if data_type in {"timestamp with time zone", "timestamp without time zone"}:
        parsed = dt.datetime.fromisoformat(str(expected).replace("Z", "+00:00"))
        if data_type == "timestamp without time zone":
            parsed = parsed.replace(tzinfo=None)
        elif parsed.tzinfo is None:
            # A few legacy manifest rows carry date-only or offset-less
            # instants; the column stores them as UTC, and a naive-vs-aware
            # comparison would report false drift.
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return actual == parsed
    if data_type == "ARRAY":
        return list(actual) == list(expected)
    return actual == expected


def verify_table(
    conn: Any,
    schema: str,
    table_key: str,
    expected_rows: list[dict[str, Any]],
    psycopg: Any,
) -> None:
    table = TABLES[table_key]
    columns = table_columns(conn, schema, table)
    if not columns:
        raise DriftError(f"{schema}.{table} is missing")

    expected_digests = collections.Counter(row_digest(row) for row in expected_rows)
    actual_digests: collections.Counter[str] = collections.Counter()
    sql = psycopg.sql
    statement = sql.SQL("select * from {}.{}").format(
        sql.Identifier(schema), sql.Identifier(table)
    )
    with conn.cursor(name=f"verify_{table}") as cursor:
        cursor.itersize = 5_000
        cursor.execute(statement)
        names = [description.name for description in cursor.description]
        for values in cursor:
            database_row = dict(zip(names, values, strict=True))
            payload = database_row["_projection_row_payload"]
            stored_digest = database_row["_projection_row_digest"]
            keys = database_row["_projection_keys"]
            actual_digest = row_digest(payload)
            if stored_digest != actual_digest:
                raise DriftError(
                    f"{table}: stored row digest {stored_digest} does not match "
                    f"payload digest {actual_digest}"
                )
            if sorted(payload) != sorted(keys):
                raise DriftError(f"{table}: stored projection key list drifted")
            for key, expected in payload.items():
                column = snake(key)
                if column not in columns:
                    raise DriftError(f"{table}: payload field {key} has no column")
                if not semantic_equal(database_row[column], expected, columns[column]):
                    raise DriftError(
                        f"{table}: row {stored_digest} field {key} drifted "
                        f"(database={database_row[column]!r}, manifest={expected!r})"
                    )
            actual_digests[actual_digest] += 1

    if actual_digests != expected_digests:
        missing = expected_digests - actual_digests
        unexpected = actual_digests - expected_digests
        raise DriftError(
            f"{table}: canonical row set drifted; "
            f"missing={sum(missing.values())}, unexpected={sum(unexpected.values())}"
        )


def verify_active(conn: Any, snapshot: Snapshot, psycopg: Any) -> None:
    pointer = conn.execute(
        """
        select projection_root_sha256
        from public.thesis_projection_active_generation
        where singleton
        for share
        """
    ).fetchone()
    if pointer is None or pointer[0] != snapshot.root:
        raise DriftError(
            "active generation root differs from site root: "
            f"database={None if pointer is None else pointer[0]}, site={snapshot.root}"
        )
    for table_key in TABLES:
        verify_table(conn, ACTIVE_SCHEMA, table_key, snapshot.rows[table_key], psycopg)


def require_projection_migration(conn: Any) -> None:
    names = (
        "public.thesis_projection_generations",
        "public.thesis_projection_active_generation",
        "public.thesis_audit_chain_head",
    )
    for name in names:
        exists = conn.execute("select to_regclass(%s)", (name,)).fetchone()[0]
        if exists is None:
            raise SystemExit(
                f"missing {name}; apply the 20260710 snapshot migration first"
            )


def ingest_snapshot(conn: Any, snapshot: Snapshot, psycopg: Any) -> bool:
    """Load and swap one snapshot. Return False for an idempotent no-op."""

    root = snapshot.root
    staging_schema = f"thesis_projection_stage_{root[:16]}"
    retired_schema = f"thesis_projection_retired_{root[:16]}"
    sql = psycopg.sql

    conn.execute("set local statement_timeout = '30min'")
    pointer = conn.execute(
        """
        select projection_root_sha256
        from public.thesis_projection_active_generation
        where singleton
        for update
        """
    ).fetchone()
    if pointer is None:
        raise DriftError("active-generation singleton row is missing")
    if pointer[0] == root:
        verify_active(conn, snapshot, psycopg)
        return False

    create_staging_schema(conn, staging_schema, psycopg)
    for table_key in TABLES:
        load_table(
            conn,
            staging_schema,
            table_key,
            snapshot.rows[table_key],
            psycopg,
        )
        verify_table(
            conn,
            staging_schema,
            table_key,
            snapshot.rows[table_key],
            psycopg,
        )

    conn.execute(
        """
        insert into public.thesis_projection_generations (
          projection_root_sha256,
          builder_version,
          source_commit,
          table_row_counts
        ) values (%s, %s, %s, %s)
        on conflict (projection_root_sha256) do nothing
        """,
        (
            root,
            snapshot.manifest["builderVersion"],
            snapshot.manifest["sourceCommit"],
            psycopg.types.json.Jsonb(
                {
                    entry["table"]: entry["rowCount"]
                    for entry in snapshot.manifest["tables"]
                }
            ),
        ),
    )

    active_exists = conn.execute(
        "select exists (select 1 from information_schema.schemata "
        "where schema_name = %s)",
        (ACTIVE_SCHEMA,),
    ).fetchone()[0]
    conn.execute(
        sql.SQL("drop schema if exists {} cascade").format(
            sql.Identifier(retired_schema)
        )
    )
    if active_exists:
        conn.execute(
            sql.SQL("alter schema {} rename to {}").format(
                sql.Identifier(ACTIVE_SCHEMA), sql.Identifier(retired_schema)
            )
        )
    conn.execute(
        sql.SQL("alter schema {} rename to {}").format(
            sql.Identifier(staging_schema), sql.Identifier(ACTIVE_SCHEMA)
        )
    )
    conn.execute(
        """
        update public.thesis_projection_active_generation
        set projection_root_sha256 = %s, updated_at = clock_timestamp()
        where singleton
        """,
        (root,),
    )
    if active_exists:
        conn.execute(
            sql.SQL("drop schema {} cascade").format(
                sql.Identifier(retired_schema)
            )
        )
    return True


def total_rows(snapshot: Snapshot) -> int:
    return sum(len(rows) for rows in snapshot.rows.values())


def print_snapshot(snapshot: Snapshot) -> None:
    print(
        f"verified root {snapshot.root} — {total_rows(snapshot)} rows across "
        f"{len(snapshot.rows)} tables — source {snapshot.manifest['sourceCommit']}"
    )


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="https://app.thesisinstitute.org")
    parser.add_argument(
        "--source-dir",
        type=Path,
        help="read an already-downloaded URL tree instead of the network",
    )
    parser.add_argument("--db", default=os.environ.get("THESIS_SUPABASE_DB_URL"))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--verify", action="store_true")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        snapshot = download_snapshot(args.base, args.source_dir)
        print_snapshot(snapshot)
        if args.dry_run:
            print("dry run OK — no database connection opened")
            return 0
        if not args.db:
            raise SystemExit(
                "no database URL: pass --db, set THESIS_SUPABASE_DB_URL, "
                "or use --dry-run"
            )

        try:
            import psycopg
        except ModuleNotFoundError as exc:
            raise SystemExit(
                "psycopg is required for database work; run with "
                "--with 'psycopg[binary]'"
            ) from exc

        with psycopg.connect(args.db) as conn:
            require_projection_migration(conn)
            if args.verify:
                verify_active(conn, snapshot, psycopg)
                print("verify OK — active replica exactly matches the live root")
                return 0
            changed = ingest_snapshot(conn, snapshot, psycopg)
            if changed:
                print(f"ingest OK — atomically activated {snapshot.root}")
            else:
                print(f"ingest no-op — {snapshot.root} is already active and verified")
            return 0
    except (SnapshotError, DriftError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
