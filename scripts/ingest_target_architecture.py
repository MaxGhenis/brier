#!/usr/bin/env python3
"""Load the published target-architecture projection into the ledger database.

The site build emits the entire target architecture as row-level projections:
`/targets.json` is a manifest of per-table chunk URLs
(`/forecasts/targets/{table}/{index}.json`), matching the Postgres schema in
site/supabase/migrations/20260629_thesis_target_architecture.sql. This script
downloads every chunk and inserts the rows, making the database a faithful
copy of what the public site serves — the site remains the source of truth
until surfaces read from the database directly.

Idempotent: inserts use ON CONFLICT DO NOTHING keyed on each table's primary
key, so re-running against a newer build only adds new rows (the tables are
append-only; UPDATE/DELETE are blocked by trigger).

Usage:
    uv run --with "psycopg[binary]" --with requests \
        scripts/ingest_target_architecture.py \
        [--base https://app.thesisinstitute.org] [--db "$THESIS_SUPABASE_DB_URL"]

The database URL defaults to $THESIS_SUPABASE_DB_URL. Exits 1 if any table's
final row count doesn't match the manifest's rowCount.
"""

import argparse
import json
import os
import re
import sys

import psycopg
import requests

# Manifest table name -> Postgres table. Insertion order respects foreign
# keys (parents before children); this mirrors the migration's CREATE order.
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


def snake(name: str) -> str:
    return re.sub(r"(?<=[a-zA-Z0-9])([A-Z])", r"_\1", name).lower()


def fetch_json(session: requests.Session, url: str):
    response = session.get(url, timeout=120)
    response.raise_for_status()
    return response.json()


def table_columns(conn, table: str) -> dict[str, str]:
    rows = conn.execute(
        """
        select column_name, data_type from information_schema.columns
        where table_schema = 'public' and table_name = %s
        """,
        (table,),
    ).fetchall()
    return dict(rows)


def adapt(value, data_type: str):
    if value is None:
        return None
    if data_type == "jsonb":
        return psycopg.types.json.Jsonb(value)
    if data_type == "ARRAY":
        return list(value)
    return value


def ingest_table(conn, session, base: str, entry: dict) -> tuple[int, int]:
    table = TABLES[entry["table"]]
    columns = table_columns(conn, table)
    inserted = 0
    for chunk in entry["chunks"]:
        payload = fetch_json(session, base + chunk["url"])
        rows = payload["rows"]
        if payload["table"] != entry["table"] or len(rows) != chunk["rowCount"]:
            raise SystemExit(
                f"{table}: chunk {chunk['url']} says table={payload['table']} "
                f"rows={len(rows)}, manifest expects {entry['table']}/{chunk['rowCount']}"
            )
        if not rows:
            continue
        keys = sorted(rows[0].keys())
        mapped = {k: snake(k) for k in keys}
        unknown = [k for k, v in mapped.items() if v not in columns]
        if unknown:
            raise SystemExit(
                f"{table}: projection fields {unknown} have no matching column "
                f"(columns: {sorted(columns)})"
            )
        col_list = ", ".join(mapped[k] for k in keys)
        # COPY into a per-chunk temp staging table, then INSERT … ON CONFLICT
        # DO NOTHING into the real one: bulk speed (the distributions table is
        # ~220k rows) while re-runs stay idempotent against append-only
        # triggers.
        with conn.cursor() as cur:
            cur.execute(
                f"create temp table staging (like {table} including defaults) "
                f"on commit drop"
            )
            with cur.copy(f"copy staging ({col_list}) from stdin") as copy:
                for row in rows:
                    copy.write_row(
                        tuple(adapt(row.get(k), columns[mapped[k]]) for k in keys)
                    )
            cur.execute(
                f"insert into {table} ({col_list}) "
                f"select {col_list} from staging on conflict do nothing"
            )
            inserted += cur.rowcount if cur.rowcount >= 0 else 0
        conn.commit()
        print(f"    {table} chunk {chunk['index']}: {len(rows)} rows", flush=True)
    count = conn.execute(f"select count(*) from {table}").fetchone()[0]
    return inserted, count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="https://app.thesisinstitute.org")
    parser.add_argument("--db", default=os.environ.get("THESIS_SUPABASE_DB_URL"))
    args = parser.parse_args()
    if not args.db:
        raise SystemExit("no database URL: pass --db or set THESIS_SUPABASE_DB_URL")

    session = requests.Session()
    manifest = fetch_json(session, args.base + "/targets.json")
    print(
        f"manifest {manifest['schemaVersion']} — "
        f"{sum(t['rowCount'] for t in manifest['tables'])} rows across "
        f"{len(manifest['tables'])} tables"
    )
    entries = {t["table"]: t for t in manifest["tables"]}
    unknown = set(entries) - set(TABLES)
    if unknown:
        raise SystemExit(f"manifest has tables this script doesn't know: {unknown}")

    ok = True
    with psycopg.connect(args.db) as conn:
        # The audit trigger hash-chains every inserted row; give bulk chunks
        # room beyond the platform's default statement timeout.
        conn.execute("set statement_timeout = '15min'")
        for name in TABLES:
            entry = entries.get(name)
            if entry is None:
                continue
            inserted, count = ingest_table(conn, session, args.base, entry)
            match = count == entry["rowCount"]
            ok &= match
            print(
                f"  {TABLES[name]:<28} +{inserted:>6} rows, {count:>6} total, "
                f"manifest {entry['rowCount']:>6}  {'OK' if match else 'MISMATCH'}"
            )
    print("ingest OK" if ok else "INGEST MISMATCH — row counts differ from manifest")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
