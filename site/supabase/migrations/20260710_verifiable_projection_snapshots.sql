-- F14: deterministic projection generations and a serialized audit head.
--
-- The site remains the source of truth.  Replica rows live in the schema
-- thesis_projection_active, which the ingest swaps atomically after staging
-- and verification.  These public tables expose the active root and immutable
-- generation history without making partially loaded schemas observable.

set search_path = public, extensions;

alter table audit_events
  add column if not exists chain_sequence bigint;

-- Existing audit rows predate sequence allocation.  Give them a deterministic
-- cutover order without rewriting their historical hashes.  New rows use only
-- the locked singleton below, never timestamp/UUID tail ordering.
alter table audit_events disable trigger audit_events_append_only;

with ordered as (
  select
    audit_event_id,
    row_number() over (order by event_time, audit_event_id)::bigint as sequence
  from audit_events
)
update audit_events
set chain_sequence = ordered.sequence
from ordered
where audit_events.audit_event_id = ordered.audit_event_id
  and audit_events.chain_sequence is null;

alter table audit_events enable trigger audit_events_append_only;

alter table audit_events
  alter column chain_sequence set not null;

create unique index if not exists audit_events_chain_sequence_idx
  on audit_events (chain_sequence);

create table if not exists thesis_audit_chain_head (
  singleton boolean primary key default true check (singleton),
  last_sequence bigint not null check (last_sequence >= 0),
  event_hash text,
  updated_at timestamptz not null default clock_timestamp(),
  check (
    (last_sequence = 0 and event_hash is null)
    or (last_sequence > 0 and event_hash is not null)
  )
);

insert into thesis_audit_chain_head (
  singleton,
  last_sequence,
  event_hash
)
select
  true,
  coalesce(max(chain_sequence), 0),
  (
    array_agg(event_hash order by chain_sequence desc)
      filter (where chain_sequence is not null)
  )[1]
from audit_events
on conflict (singleton) do update
set
  last_sequence = excluded.last_sequence,
  event_hash = excluded.event_hash,
  updated_at = clock_timestamp();

create or replace function thesis_record_insert_audit_event()
returns trigger
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  new_payload jsonb;
  row_identifier text := '';
  payload_hash text;
  previous_hash text;
  next_sequence bigint;
  next_hash text;
  argument_index integer;
begin
  select last_sequence + 1, event_hash
    into next_sequence, previous_hash
    from thesis_audit_chain_head
    where singleton
    for update;

  if next_sequence is null then
    raise exception 'thesis audit-chain singleton is missing';
  end if;

  new_payload := to_jsonb(new);
  for argument_index in 0..tg_nargs - 1 loop
    if argument_index > 0 then
      row_identifier := row_identifier || ':';
    end if;
    row_identifier := row_identifier || coalesce(
      new_payload ->> tg_argv[argument_index],
      ''
    );
  end loop;
  if row_identifier = '' then
    row_identifier := encode(digest(new_payload::text, 'sha256'), 'hex');
  end if;

  payload_hash := encode(digest(new_payload::text, 'sha256'), 'hex');
  next_hash := encode(
    digest(
      'v2:' || next_sequence::text || ':' || tg_table_name || ':' ||
      row_identifier || ':' || payload_hash || ':' ||
      coalesce(previous_hash, ''),
      'sha256'
    ),
    'hex'
  );

  insert into audit_events (
    chain_sequence,
    actor_id,
    table_name,
    row_id,
    action,
    payload_hash,
    previous_event_hash,
    event_hash,
    metadata
  )
  values (
    next_sequence,
    'system.supabase.trigger',
    tg_table_name,
    row_identifier,
    'insert',
    payload_hash,
    previous_hash,
    next_hash,
    jsonb_build_object('schema', 'thesis_target_architecture_v2')
  );

  update thesis_audit_chain_head
  set
    last_sequence = next_sequence,
    event_hash = next_hash,
    updated_at = clock_timestamp()
  where singleton;

  return new;
end;
$$;

drop index if exists audit_events_tail_idx;

create table if not exists thesis_projection_generations (
  projection_root_sha256 text primary key
    check (projection_root_sha256 ~ '^[0-9a-f]{64}$'),
  builder_version text not null check (builder_version <> ''),
  source_commit text not null check (source_commit <> ''),
  table_row_counts jsonb not null,
  ingested_at timestamptz not null default clock_timestamp()
);

create table if not exists thesis_projection_active_generation (
  singleton boolean primary key default true check (singleton),
  projection_root_sha256 text
    references thesis_projection_generations (projection_root_sha256),
  updated_at timestamptz not null default clock_timestamp()
);

insert into thesis_projection_active_generation (singleton)
values (true)
on conflict (singleton) do nothing;

drop trigger if exists thesis_projection_generations_append_only
  on thesis_projection_generations;
create trigger thesis_projection_generations_append_only
before update or delete on thesis_projection_generations
for each row execute function thesis_prevent_update_delete();

drop trigger if exists thesis_projection_generations_insert_audit
  on thesis_projection_generations;
create trigger thesis_projection_generations_insert_audit
after insert on thesis_projection_generations
for each row execute function thesis_record_insert_audit_event(
  'projection_root_sha256'
);

alter table thesis_audit_chain_head enable row level security;
alter table thesis_projection_generations enable row level security;
alter table thesis_projection_active_generation enable row level security;

drop policy if exists thesis_audit_chain_head_public_read
  on thesis_audit_chain_head;
create policy thesis_audit_chain_head_public_read
  on thesis_audit_chain_head for select using (true);

drop policy if exists thesis_projection_generations_public_read
  on thesis_projection_generations;
create policy thesis_projection_generations_public_read
  on thesis_projection_generations for select using (true);

drop policy if exists thesis_projection_active_generation_public_read
  on thesis_projection_active_generation;
create policy thesis_projection_active_generation_public_read
  on thesis_projection_active_generation for select using (true);

grant select on thesis_audit_chain_head to anon, authenticated;
grant select on thesis_projection_generations to anon, authenticated;
grant select on thesis_projection_active_generation to anon, authenticated;

comment on table thesis_projection_generations is
  'Append-only roots ingested from the site target-architecture manifest.';
comment on table thesis_projection_active_generation is
  'Singleton pointer advanced in the same transaction as the replica schema swap.';
comment on table thesis_audit_chain_head is
  'Locked singleton allocating monotonically increasing audit chain positions.';
