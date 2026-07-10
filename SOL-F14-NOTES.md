# SOL-F14 integrator notes

F14 cannot exercise Supabase in this sandbox. The implementation has no live
database assumptions beyond the committed migrations and psycopg's standard
PostgreSQL behavior. Run these commands from the repository root against the
Supabase direct/session-pooler PostgreSQL URL (not the HTTP API URL).

## 1. Apply the migration

```bash
psql "$THESIS_SUPABASE_DB_URL" \
  -v ON_ERROR_STOP=1 \
  -f site/supabase/migrations/20260710_verifiable_projection_snapshots.sql
```

This adds the locked audit-chain head and monotonic sequence, the append-only
generation ledger, and the active-generation singleton. The original
`20260629_thesis_target_architecture.sql` migration must already be present.

## 2. Verify the site publication without touching the database

```bash
python3 scripts/ingest_target_architecture.py \
  --base https://app.thesisinstitute.org \
  --dry-run
```

This downloads `/targets.json` plus every referenced chunk and verifies all
chunk, table, and projection-root commitments. It deliberately opens no
database connection.

## 3. Run the full atomic ingest

```bash
uv run --with "psycopg[binary]" \
  scripts/ingest_target_architecture.py \
  --base https://app.thesisinstitute.org \
  --db "$THESIS_SUPABASE_DB_URL"
```

Expected final output is `ingest OK — atomically activated <root>`. If that
root is already active, the script verifies the active rows and reports an
idempotent no-op. It does not use `requests`; psycopg is the only non-standard
runtime dependency.

## 4. Corroborate the active replica

```bash
uv run --with "psycopg[binary]" \
  scripts/ingest_target_architecture.py \
  --base https://app.thesisinstitute.org \
  --db "$THESIS_SUPABASE_DB_URL" \
  --verify
```

Expected final output is `verify OK — active replica exactly matches the live
root`. Any root mismatch, missing/extra row digest, changed projection payload,
or typed-column drift exits nonzero.

For an already-downloaded URL tree, all three modes accept `--source-dir DIR`;
the directory must contain `targets.json` and paths such as
`forecasts/targets/targets/0.json` exactly as published.

## Live checks

After ingest, confirm the public metadata and audit sequence:

```sql
select * from public.thesis_projection_active_generation;
select projection_root_sha256, source_commit, ingested_at
from public.thesis_projection_generations
order by ingested_at desc;
select chain_sequence, previous_event_hash, event_hash
from public.audit_events
order by chain_sequence desc
limit 10;
```

The active root must equal `/targets.json`'s `projectionRootSha256`, generation
history must contain that root and source commit, and audit sequences must be
unique and contiguous at the tail.
