create extension if not exists pgcrypto;

create or replace function thesis_prevent_update_delete()
returns trigger
language plpgsql
as $$
begin
  raise exception '% is append-only; insert a new version, event, or score instead', tg_table_name;
end;
$$;

create table if not exists artifact_refs (
  artifact_ref_id text primary key,
  content_hash text not null unique,
  media_type text not null,
  storage_uri text not null,
  public_visibility text not null check (public_visibility in ('public', 'redacted', 'private', 'blocked')),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists targets (
  target_id text primary key,
  slug text not null unique,
  data_point_id text not null unique,
  country text not null,
  agency text,
  source_family text not null,
  source_url text,
  tags text[] not null default '{}'::text[],
  created_at timestamptz not null default now()
);

create table if not exists target_versions (
  target_version_id text primary key,
  target_id text not null references targets (target_id),
  parent_target_version_id text references target_versions (target_version_id),
  version_label text not null,
  question text not null,
  period_label text not null,
  target_period text not null,
  unit text not null,
  value_scale numeric not null default 1,
  scoring_transform text,
  resolver_kind text not null check (resolver_kind in ('public_release', 'policy_state', 'conditional_gate', 'formula_publication')),
  resolution_policy text not null check (resolution_policy in ('first_print', 'fixed_vintage', 'final')),
  resolution_date_basis text not null,
  resolution_rule text not null,
  resolution_source text not null,
  resolution_source_url text,
  cdf_point_count integer not null default 201 check (cdf_point_count = 201),
  published_at timestamptz not null,
  created_at timestamptz not null default now(),
  unique (target_id, version_label)
);

create table if not exists source_series (
  source_series_id text primary key,
  adapter_id text not null,
  source_family text not null,
  agency_series_id text not null default '',
  measure_key text not null,
  country text not null,
  agency text,
  source_url text not null,
  unit text,
  update_cadence text,
  default_vintage_policy text not null check (default_vintage_policy in ('first_print', 'fixed_vintage', 'final', 'unknown')),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (adapter_id, agency_series_id, source_url, unit, measure_key)
);

create table if not exists observations (
  observation_id text primary key,
  source_series_id text not null references source_series (source_series_id),
  data_point_id text,
  period_label text not null,
  period_start date,
  period_end date,
  value numeric,
  unit text,
  value_scale numeric not null default 1,
  numerator numeric,
  denominator numeric,
  source_url text not null,
  retrieved_at timestamptz not null,
  missing_reason text,
  payload_hash text not null,
  created_at timestamptz not null default now(),
  check (value is not null or missing_reason is not null),
  unique (source_series_id, period_label, payload_hash)
);

create table if not exists observation_vintages (
  vintage_id text primary key,
  observation_id text not null references observations (observation_id),
  vintage_kind text not null check (vintage_kind in ('first_print', 'preliminary', 'revised', 'final', 'fixed_vintage', 'unknown')),
  published_at timestamptz,
  retrieved_at timestamptz not null,
  source_snapshot_artifact_ref_id text references artifact_refs (artifact_ref_id),
  normalized_payload_hash text not null,
  created_at timestamptz not null default now(),
  unique (observation_id, vintage_kind, published_at)
);

create table if not exists target_observation_bindings (
  binding_id text primary key,
  target_version_id text not null references target_versions (target_version_id),
  source_series_id text references source_series (source_series_id),
  observation_id text references observations (observation_id),
  binding_role text not null check (binding_role in ('history', 'resolver', 'formula_input', 'timing', 'conditioning', 'registration')),
  transform_kind text not null default 'identity',
  transform_expression text,
  adapter_method text,
  created_at timestamptz not null default now(),
  check (source_series_id is not null or observation_id is not null)
);

create table if not exists baseline_candidates (
  candidate_id text primary key,
  target_version_id text not null references target_versions (target_version_id),
  source_series_id text references source_series (source_series_id),
  model_adapter text not null,
  candidate_label text not null,
  training_cutoff timestamptz not null,
  point_estimate numeric not null,
  p10 numeric,
  p50 numeric,
  p90 numeric,
  interval80_lower numeric,
  interval80_upper numeric,
  interval90_lower numeric,
  interval90_upper numeric,
  interval_method text not null,
  calibration_sample_size integer check (calibration_sample_size is null or calibration_sample_size >= 0),
  walk_forward_score numeric,
  assumptions text,
  failure_modes text[] not null default '{}'::text[],
  artifact_ref_id text references artifact_refs (artifact_ref_id),
  provenance jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  check (artifact_ref_id is not null or source_series_id is not null)
);

create table if not exists forecast_strategies (
  strategy_id text primary key,
  name text not null,
  strategy_kind text not null check (strategy_kind in ('llm_no_pack', 'llm_pack_informed', 'persistence_baseline', 'time_series_baseline', 'official_projection_anchor', 'formula_nowcast', 'reviewer_assisted_llm', 'meta_aggregator')),
  description text,
  created_at timestamptz not null default now()
);

create table if not exists strategy_versions (
  strategy_version_id text primary key,
  strategy_id text not null references forecast_strategies (strategy_id),
  version_label text not null,
  prompt_policy_hash text,
  tool_policy_hash text,
  required_inputs jsonb not null default '{}'::jsonb,
  model_family_constraints jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (strategy_id, version_label)
);

create table if not exists packs (
  pack_id text primary key,
  slug text not null unique,
  name text not null,
  target_family_tags text[] not null default '{}'::text[],
  owner_id text,
  created_at timestamptz not null default now()
);

create table if not exists pack_versions (
  pack_version_id text primary key,
  pack_id text not null references packs (pack_id),
  version_label text not null,
  evidence_requirements jsonb not null default '{}'::jsonb,
  validator_rules jsonb not null default '{}'::jsonb,
  prompt_content_hash text not null,
  examples jsonb not null default '[]'::jsonb,
  ablation_plan text,
  created_at timestamptz not null default now(),
  unique (pack_id, version_label)
);

create table if not exists forecast_runs (
  run_id text primary key,
  target_version_id text not null references target_versions (target_version_id),
  strategy_version_id text not null references strategy_versions (strategy_version_id),
  agent_id text not null,
  model text,
  runtime text,
  prompt_hash text not null,
  tool_policy_hash text not null,
  input_bundle_hash text not null,
  status text not null check (status in ('draft', 'published', 'needs_review', 'failed')),
  idempotency_key text not null,
  run_at timestamptz not null,
  created_at timestamptz not null default now(),
  unique (target_version_id, strategy_version_id, agent_id, idempotency_key)
);

create table if not exists run_artifact_refs (
  run_artifact_ref_id text primary key,
  run_id text not null references forecast_runs (run_id),
  artifact_ref_id text not null references artifact_refs (artifact_ref_id),
  artifact_role text not null,
  sequence_index integer not null check (sequence_index >= 0),
  created_at timestamptz not null default now(),
  unique (run_id, artifact_ref_id, artifact_role)
);

create table if not exists run_pack_versions (
  run_pack_version_id text primary key,
  run_id text not null references forecast_runs (run_id),
  pack_version_id text not null references pack_versions (pack_version_id),
  pack_role text not null check (pack_role in ('required', 'optional', 'ablation', 'comparison')),
  created_at timestamptz not null default now(),
  unique (run_id, pack_version_id, pack_role)
);

create table if not exists forecast_distributions (
  run_id text not null references forecast_runs (run_id),
  point_index integer not null check (point_index between 0 and 200),
  value numeric not null,
  probability numeric not null check (probability between 0 and 1),
  unit text not null,
  interval_mass numeric not null default 0.8 check (interval_mass = 0.8),
  validation_status text not null check (validation_status in ('passed', 'warning', 'failed')),
  created_at timestamptz not null default now(),
  primary key (run_id, point_index)
);

create table if not exists reasoning_events (
  reasoning_event_id text primary key,
  run_id text not null references forecast_runs (run_id),
  sequence_index integer not null check (sequence_index >= 0),
  event_kind text not null check (event_kind in ('prompt', 'model_event', 'assistant_message', 'command', 'source_fetch', 'normalization', 'validation', 'review', 'judge', 'resolution')),
  public_text text,
  artifact_ref_id text references artifact_refs (artifact_ref_id),
  redaction_status text not null check (redaction_status in ('public_only', 'redacted', 'blocked')),
  created_at timestamptz not null default now(),
  unique (run_id, sequence_index)
);

create table if not exists review_runs (
  review_run_id text primary key,
  run_id text not null references forecast_runs (run_id),
  reviewer_agent_id text not null,
  draft_artifact_ref_id text references artifact_refs (artifact_ref_id),
  findings jsonb not null default '[]'::jsonb,
  revision_artifact_ref_id text references artifact_refs (artifact_ref_id),
  disposition text not null check (disposition in ('accepted', 'revised', 'rejected', 'no_change')),
  created_at timestamptz not null default now()
);

create table if not exists judge_runs (
  judge_run_id text primary key,
  run_id text references forecast_runs (run_id),
  batch_id text,
  left_run_id text references forecast_runs (run_id),
  right_run_id text references forecast_runs (run_id),
  judge_model text not null,
  prompt_version text not null,
  findings jsonb not null default '[]'::jsonb,
  recommendations jsonb not null default '[]'::jsonb,
  reward_eligible boolean not null default false check (reward_eligible = false),
  created_at timestamptz not null default now(),
  check (run_id is not null or batch_id is not null),
  check ((left_run_id is null and right_run_id is null) or (left_run_id is not null and right_run_id is not null))
);

create table if not exists tool_calls (
  tool_call_id text primary key,
  run_id text not null references forecast_runs (run_id),
  sequence_index integer not null check (sequence_index >= 0),
  allowed_tool_declaration text not null,
  tool_name text not null,
  request_hash text not null,
  response_hash text,
  provider text not null,
  status text not null check (status in ('queued', 'running', 'succeeded', 'failed', 'blocked')),
  cost_usd numeric,
  influenced_final_forecast boolean not null default false,
  source_role text,
  request_artifact_ref_id text references artifact_refs (artifact_ref_id),
  response_artifact_ref_id text references artifact_refs (artifact_ref_id),
  -- Null for tool calls replayed from recorded public traces, which
  -- carry no wall-clock timing.
  started_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz not null default now(),
  unique (run_id, sequence_index)
);

create table if not exists resolution_events (
  resolution_event_id text primary key,
  target_version_id text not null references target_versions (target_version_id),
  observation_id text references observations (observation_id),
  vintage_id text references observation_vintages (vintage_id),
  resolved_value numeric,
  source_url text,
  resolver_proof jsonb not null default '{}'::jsonb,
  scoreable_status text not null check (scoreable_status in ('scoreable', 'unscoreable', 'disputed', 'retracted')),
  event_timestamp timestamptz not null,
  created_at timestamptz not null default now(),
  check (resolved_value is not null or scoreable_status <> 'scoreable'),
  unique (target_version_id, observation_id, vintage_id)
);

create table if not exists scores (
  score_id text primary key,
  run_id text not null references forecast_runs (run_id),
  resolution_event_id text not null references resolution_events (resolution_event_id),
  scoring_rule text not null,
  crps numeric,
  brier_score numeric,
  normalized_score numeric,
  normalized_crps numeric,
  probability_integral_transform numeric check (probability_integral_transform is null or probability_integral_transform between 0 and 1),
  interval80_covered boolean,
  interval90_covered boolean,
  signed_error numeric,
  absolute_error numeric check (absolute_error is null or absolute_error >= 0),
  score_hash text not null,
  created_at timestamptz not null default now(),
  unique (run_id, resolution_event_id, scoring_rule)
);

create table if not exists audit_events (
  audit_event_id uuid primary key default gen_random_uuid(),
  event_time timestamptz not null default now(),
  actor_id text not null,
  table_name text not null,
  row_id text not null,
  action text not null check (action in ('insert', 'resolution_link', 'score_recompute', 'dispute')),
  payload_hash text not null,
  previous_event_hash text,
  event_hash text not null unique,
  metadata jsonb not null default '{}'::jsonb
);

-- The insert-audit trigger reads the latest event per row inserted; without
-- this index the tail lookup is a full sort and bulk loads go quadratic.
create index if not exists audit_events_tail_idx
  on audit_events (event_time desc, audit_event_id desc);

drop trigger if exists artifact_refs_append_only on artifact_refs;
create trigger artifact_refs_append_only
before update or delete on artifact_refs
for each row execute function thesis_prevent_update_delete();

drop trigger if exists targets_append_only on targets;
create trigger targets_append_only
before update or delete on targets
for each row execute function thesis_prevent_update_delete();

drop trigger if exists target_versions_append_only on target_versions;
create trigger target_versions_append_only
before update or delete on target_versions
for each row execute function thesis_prevent_update_delete();

drop trigger if exists source_series_append_only on source_series;
create trigger source_series_append_only
before update or delete on source_series
for each row execute function thesis_prevent_update_delete();

drop trigger if exists observations_append_only on observations;
create trigger observations_append_only
before update or delete on observations
for each row execute function thesis_prevent_update_delete();

drop trigger if exists observation_vintages_append_only on observation_vintages;
create trigger observation_vintages_append_only
before update or delete on observation_vintages
for each row execute function thesis_prevent_update_delete();

drop trigger if exists target_observation_bindings_append_only on target_observation_bindings;
create trigger target_observation_bindings_append_only
before update or delete on target_observation_bindings
for each row execute function thesis_prevent_update_delete();

drop trigger if exists baseline_candidates_append_only on baseline_candidates;
create trigger baseline_candidates_append_only
before update or delete on baseline_candidates
for each row execute function thesis_prevent_update_delete();

drop trigger if exists forecast_strategies_append_only on forecast_strategies;
create trigger forecast_strategies_append_only
before update or delete on forecast_strategies
for each row execute function thesis_prevent_update_delete();

drop trigger if exists strategy_versions_append_only on strategy_versions;
create trigger strategy_versions_append_only
before update or delete on strategy_versions
for each row execute function thesis_prevent_update_delete();

drop trigger if exists packs_append_only on packs;
create trigger packs_append_only
before update or delete on packs
for each row execute function thesis_prevent_update_delete();

drop trigger if exists pack_versions_append_only on pack_versions;
create trigger pack_versions_append_only
before update or delete on pack_versions
for each row execute function thesis_prevent_update_delete();

drop trigger if exists forecast_runs_append_only on forecast_runs;
create trigger forecast_runs_append_only
before update or delete on forecast_runs
for each row execute function thesis_prevent_update_delete();

drop trigger if exists run_artifact_refs_append_only on run_artifact_refs;
create trigger run_artifact_refs_append_only
before update or delete on run_artifact_refs
for each row execute function thesis_prevent_update_delete();

drop trigger if exists run_pack_versions_append_only on run_pack_versions;
create trigger run_pack_versions_append_only
before update or delete on run_pack_versions
for each row execute function thesis_prevent_update_delete();

drop trigger if exists forecast_distributions_append_only on forecast_distributions;
create trigger forecast_distributions_append_only
before update or delete on forecast_distributions
for each row execute function thesis_prevent_update_delete();

drop trigger if exists reasoning_events_append_only on reasoning_events;
create trigger reasoning_events_append_only
before update or delete on reasoning_events
for each row execute function thesis_prevent_update_delete();

drop trigger if exists review_runs_append_only on review_runs;
create trigger review_runs_append_only
before update or delete on review_runs
for each row execute function thesis_prevent_update_delete();

drop trigger if exists judge_runs_append_only on judge_runs;
create trigger judge_runs_append_only
before update or delete on judge_runs
for each row execute function thesis_prevent_update_delete();

drop trigger if exists tool_calls_append_only on tool_calls;
create trigger tool_calls_append_only
before update or delete on tool_calls
for each row execute function thesis_prevent_update_delete();

drop trigger if exists resolution_events_append_only on resolution_events;
create trigger resolution_events_append_only
before update or delete on resolution_events
for each row execute function thesis_prevent_update_delete();

drop trigger if exists scores_append_only on scores;
create trigger scores_append_only
before update or delete on scores
for each row execute function thesis_prevent_update_delete();

drop trigger if exists audit_events_append_only on audit_events;
create trigger audit_events_append_only
before update or delete on audit_events
for each row execute function thesis_prevent_update_delete();

alter table artifact_refs enable row level security;
alter table targets enable row level security;
alter table target_versions enable row level security;
alter table source_series enable row level security;
alter table observations enable row level security;
alter table observation_vintages enable row level security;
alter table target_observation_bindings enable row level security;
alter table baseline_candidates enable row level security;
alter table forecast_strategies enable row level security;
alter table strategy_versions enable row level security;
alter table packs enable row level security;
alter table pack_versions enable row level security;
alter table forecast_runs enable row level security;
alter table run_artifact_refs enable row level security;
alter table run_pack_versions enable row level security;
alter table forecast_distributions enable row level security;
alter table reasoning_events enable row level security;
alter table review_runs enable row level security;
alter table judge_runs enable row level security;
alter table tool_calls enable row level security;
alter table resolution_events enable row level security;
alter table scores enable row level security;
alter table audit_events enable row level security;

drop policy if exists artifact_refs_public_read on artifact_refs;
create policy artifact_refs_public_read on artifact_refs
  for select using (public_visibility = 'public');
drop policy if exists targets_public_read on targets;
create policy targets_public_read on targets for select using (true);
drop policy if exists target_versions_public_read on target_versions;
create policy target_versions_public_read on target_versions for select using (true);
drop policy if exists source_series_public_read on source_series;
create policy source_series_public_read on source_series for select using (true);
drop policy if exists observations_public_read on observations;
create policy observations_public_read on observations for select using (true);
drop policy if exists observation_vintages_public_read on observation_vintages;
create policy observation_vintages_public_read on observation_vintages
  for select using (
    source_snapshot_artifact_ref_id is null
    or exists (
      select 1
      from artifact_refs
      where artifact_refs.artifact_ref_id = observation_vintages.source_snapshot_artifact_ref_id
        and artifact_refs.public_visibility = 'public'
    )
  );
drop policy if exists target_observation_bindings_public_read on target_observation_bindings;
create policy target_observation_bindings_public_read on target_observation_bindings for select using (true);
drop policy if exists baseline_candidates_public_read on baseline_candidates;
create policy baseline_candidates_public_read on baseline_candidates
  for select using (
    artifact_ref_id is null
    or exists (
      select 1
      from artifact_refs
      where artifact_refs.artifact_ref_id = baseline_candidates.artifact_ref_id
        and artifact_refs.public_visibility = 'public'
    )
  );
drop policy if exists forecast_strategies_public_read on forecast_strategies;
create policy forecast_strategies_public_read on forecast_strategies for select using (true);
drop policy if exists strategy_versions_public_read on strategy_versions;
create policy strategy_versions_public_read on strategy_versions for select using (true);
drop policy if exists packs_public_read on packs;
create policy packs_public_read on packs for select using (true);
drop policy if exists pack_versions_public_read on pack_versions;
create policy pack_versions_public_read on pack_versions for select using (true);
drop policy if exists forecast_runs_public_read on forecast_runs;
create policy forecast_runs_public_read on forecast_runs for select using (true);
drop policy if exists run_artifact_refs_public_read on run_artifact_refs;
create policy run_artifact_refs_public_read on run_artifact_refs
  for select using (
    exists (
      select 1
      from artifact_refs
      where artifact_refs.artifact_ref_id = run_artifact_refs.artifact_ref_id
        and artifact_refs.public_visibility = 'public'
    )
  );
drop policy if exists run_pack_versions_public_read on run_pack_versions;
create policy run_pack_versions_public_read on run_pack_versions for select using (true);
drop policy if exists forecast_distributions_public_read on forecast_distributions;
create policy forecast_distributions_public_read on forecast_distributions for select using (true);
drop policy if exists reasoning_events_public_read on reasoning_events;
create policy reasoning_events_public_read on reasoning_events
  for select using (
    redaction_status = 'public_only'
    and (
      artifact_ref_id is null
      or exists (
        select 1
        from artifact_refs
        where artifact_refs.artifact_ref_id = reasoning_events.artifact_ref_id
          and artifact_refs.public_visibility = 'public'
      )
    )
  );
drop policy if exists review_runs_public_read on review_runs;
create policy review_runs_public_read on review_runs
  for select using (
    (
      draft_artifact_ref_id is null
      or exists (
        select 1
        from artifact_refs
        where artifact_refs.artifact_ref_id = review_runs.draft_artifact_ref_id
          and artifact_refs.public_visibility = 'public'
      )
    )
    and (
      revision_artifact_ref_id is null
      or exists (
        select 1
        from artifact_refs
        where artifact_refs.artifact_ref_id = review_runs.revision_artifact_ref_id
          and artifact_refs.public_visibility = 'public'
      )
    )
  );
drop policy if exists judge_runs_public_read on judge_runs;
create policy judge_runs_public_read on judge_runs for select using (true);

drop policy if exists tool_calls_public_read on tool_calls;
create policy tool_calls_public_read on tool_calls
  for select using (
    (
      request_artifact_ref_id is null
      or exists (
        select 1
        from artifact_refs
        where artifact_refs.artifact_ref_id = tool_calls.request_artifact_ref_id
          and artifact_refs.public_visibility = 'public'
      )
    )
    and (
      response_artifact_ref_id is null
      or exists (
        select 1
        from artifact_refs
        where artifact_refs.artifact_ref_id = tool_calls.response_artifact_ref_id
          and artifact_refs.public_visibility = 'public'
      )
    )
  );
drop policy if exists resolution_events_public_read on resolution_events;
create policy resolution_events_public_read on resolution_events for select using (true);
drop policy if exists scores_public_read on scores;
create policy scores_public_read on scores for select using (true);
drop policy if exists audit_events_public_read on audit_events;
create policy audit_events_public_read on audit_events for select using (true);

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
  argument_index integer;
begin
  perform pg_advisory_xact_lock(hashtext('thesis.audit_events')::bigint);
  new_payload := to_jsonb(new);
  for argument_index in 0..tg_nargs - 1 loop
    if argument_index > 0 then
      row_identifier := row_identifier || ':';
    end if;
    row_identifier := row_identifier || coalesce(new_payload ->> tg_argv[argument_index], '');
  end loop;
  if row_identifier = '' then
    row_identifier := encode(digest(new_payload::text, 'sha256'), 'hex');
  end if;
  payload_hash := encode(digest(new_payload::text, 'sha256'), 'hex');
  select event_hash
    into previous_hash
    from audit_events
    order by event_time desc, audit_event_id desc
    limit 1;
  insert into audit_events (
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
    'system.supabase.trigger',
    tg_table_name,
    row_identifier,
    'insert',
    payload_hash,
    previous_hash,
    encode(
      digest(
        tg_table_name || ':' || row_identifier || ':' || payload_hash || ':' || coalesce(previous_hash, ''),
        'sha256'
      ),
      'hex'
    ),
    jsonb_build_object('schema', 'thesis_target_architecture_v1')
  );
  return new;
end;
$$;

drop trigger if exists artifact_refs_insert_audit on artifact_refs;
create trigger artifact_refs_insert_audit
after insert on artifact_refs
for each row execute function thesis_record_insert_audit_event('artifact_ref_id');

drop trigger if exists targets_insert_audit on targets;
create trigger targets_insert_audit
after insert on targets
for each row execute function thesis_record_insert_audit_event('target_id');

drop trigger if exists target_versions_insert_audit on target_versions;
create trigger target_versions_insert_audit
after insert on target_versions
for each row execute function thesis_record_insert_audit_event('target_version_id');

drop trigger if exists source_series_insert_audit on source_series;
create trigger source_series_insert_audit
after insert on source_series
for each row execute function thesis_record_insert_audit_event('source_series_id');

drop trigger if exists observations_insert_audit on observations;
create trigger observations_insert_audit
after insert on observations
for each row execute function thesis_record_insert_audit_event('observation_id');

drop trigger if exists observation_vintages_insert_audit on observation_vintages;
create trigger observation_vintages_insert_audit
after insert on observation_vintages
for each row execute function thesis_record_insert_audit_event('vintage_id');

drop trigger if exists target_observation_bindings_insert_audit on target_observation_bindings;
create trigger target_observation_bindings_insert_audit
after insert on target_observation_bindings
for each row execute function thesis_record_insert_audit_event('binding_id');

drop trigger if exists baseline_candidates_insert_audit on baseline_candidates;
create trigger baseline_candidates_insert_audit
after insert on baseline_candidates
for each row execute function thesis_record_insert_audit_event('candidate_id');

drop trigger if exists forecast_strategies_insert_audit on forecast_strategies;
create trigger forecast_strategies_insert_audit
after insert on forecast_strategies
for each row execute function thesis_record_insert_audit_event('strategy_id');

drop trigger if exists strategy_versions_insert_audit on strategy_versions;
create trigger strategy_versions_insert_audit
after insert on strategy_versions
for each row execute function thesis_record_insert_audit_event('strategy_version_id');

drop trigger if exists packs_insert_audit on packs;
create trigger packs_insert_audit
after insert on packs
for each row execute function thesis_record_insert_audit_event('pack_id');

drop trigger if exists pack_versions_insert_audit on pack_versions;
create trigger pack_versions_insert_audit
after insert on pack_versions
for each row execute function thesis_record_insert_audit_event('pack_version_id');

drop trigger if exists forecast_runs_insert_audit on forecast_runs;
create trigger forecast_runs_insert_audit
after insert on forecast_runs
for each row execute function thesis_record_insert_audit_event('run_id');

drop trigger if exists run_artifact_refs_insert_audit on run_artifact_refs;
create trigger run_artifact_refs_insert_audit
after insert on run_artifact_refs
for each row execute function thesis_record_insert_audit_event('run_artifact_ref_id');

drop trigger if exists run_pack_versions_insert_audit on run_pack_versions;
create trigger run_pack_versions_insert_audit
after insert on run_pack_versions
for each row execute function thesis_record_insert_audit_event('run_pack_version_id');

drop trigger if exists forecast_distributions_insert_audit on forecast_distributions;
create trigger forecast_distributions_insert_audit
after insert on forecast_distributions
for each row execute function thesis_record_insert_audit_event('run_id', 'point_index');

drop trigger if exists reasoning_events_insert_audit on reasoning_events;
create trigger reasoning_events_insert_audit
after insert on reasoning_events
for each row execute function thesis_record_insert_audit_event('reasoning_event_id');

drop trigger if exists review_runs_insert_audit on review_runs;
create trigger review_runs_insert_audit
after insert on review_runs
for each row execute function thesis_record_insert_audit_event('review_run_id');

drop trigger if exists judge_runs_insert_audit on judge_runs;
create trigger judge_runs_insert_audit
after insert on judge_runs
for each row execute function thesis_record_insert_audit_event('judge_run_id');

drop trigger if exists tool_calls_insert_audit on tool_calls;
create trigger tool_calls_insert_audit
after insert on tool_calls
for each row execute function thesis_record_insert_audit_event('tool_call_id');

drop trigger if exists resolution_events_insert_audit on resolution_events;
create trigger resolution_events_insert_audit
after insert on resolution_events
for each row execute function thesis_record_insert_audit_event('resolution_event_id');

drop trigger if exists scores_insert_audit on scores;
create trigger scores_insert_audit
after insert on scores
for each row execute function thesis_record_insert_audit_event('score_id');
