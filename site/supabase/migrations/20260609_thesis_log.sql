create extension if not exists pgcrypto;

create table if not exists prediction_specs (
  spec_id text primary key,
  prediction_id text not null unique,
  created_at timestamptz not null default now()
);

create table if not exists spec_versions (
  spec_version_id text primary key,
  spec_id text not null references prediction_specs (spec_id),
  parent_spec_version_id text references spec_versions (spec_version_id),
  version_label text not null,
  spec_hash text not null unique,
  question text not null,
  country text not null,
  outcome_type text not null,
  unit text not null,
  target_fact_ref text,
  resolution_rule text not null,
  resolution_source text not null,
  resolution_source_url text,
  cdf_point_count integer not null default 201 check (cdf_point_count = 201),
  published_at timestamptz not null,
  created_at timestamptz not null default now(),
  unique (spec_id, version_label)
);

create table if not exists prediction_runs (
  run_id text primary key,
  spec_version_id text not null references spec_versions (spec_version_id),
  agent_id text not null,
  idempotency_key text not null,
  created_at timestamptz not null default now(),
  model_version text,
  agent_version text,
  prompt_hash text not null,
  tool_policy_hash text not null,
  input_bundle_hash text not null,
  status text not null check (status in ('published', 'needs_review', 'failed')),
  unique (spec_version_id, agent_id, idempotency_key)
);

create table if not exists cdf_points (
  run_id text not null references prediction_runs (run_id),
  point_index integer not null check (point_index between 0 and 200),
  value numeric not null,
  probability numeric not null check (probability between 0 and 1),
  unit text not null,
  lower_bound numeric,
  upper_bound numeric,
  interval_mass numeric not null default 0.8 check (interval_mass = 0.8),
  confidence_mass_check_status text not null check (confidence_mass_check_status in ('passed', 'warning', 'failed')),
  validation_status text not null check (validation_status in ('passed', 'warning', 'failed')),
  created_at timestamptz not null default now(),
  primary key (run_id, point_index)
);

create table if not exists public_traces (
  trace_id text primary key,
  run_id text not null references prediction_runs (run_id),
  artifact_type text not null default 'public_trace' check (artifact_type = 'public_trace'),
  body jsonb not null,
  redaction_status text not null check (redaction_status in ('public_only', 'redacted', 'blocked')),
  redaction_metadata jsonb not null default '{}'::jsonb,
  trace_hash text not null,
  publicly_reproducible_enough boolean not null default false,
  created_at timestamptz not null default now(),
  unique (run_id, artifact_type)
);

create table if not exists tool_calls (
  tool_call_id text primary key,
  run_id text not null references prediction_runs (run_id),
  allowed_tool_declaration text not null,
  tool_name text not null,
  tool_version text,
  request_hash text not null,
  response_hash text,
  provider text not null,
  status text not null check (status in ('queued', 'running', 'succeeded', 'failed', 'blocked')),
  cost_usd numeric,
  influenced_final_forecast boolean not null default false,
  started_at timestamptz not null,
  completed_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists resolution_links (
  resolution_ref text primary key,
  spec_version_id text not null references spec_versions (spec_version_id),
  target_fact_ref text,
  ledger_name text not null default 'PolicyEngine Ledger',
  external_resolver_ref text,
  resolver_rule text not null,
  status text not null check (status in ('pending', 'linked', 'disputed', 'superseded')),
  created_at timestamptz not null default now()
);

create table if not exists resolution_events (
  resolution_event_id text primary key,
  resolution_ref text not null references resolution_links (resolution_ref),
  ledger_fact_ref text,
  external_resolver_ref text,
  payload_hash text not null,
  status text not null check (status in ('linked', 'disputed', 'retracted')),
  occurred_at timestamptz not null,
  created_at timestamptz not null default now(),
  check (ledger_fact_ref is not null or external_resolver_ref is not null),
  unique (resolution_ref, ledger_fact_ref),
  unique (resolution_ref, external_resolver_ref)
);

create table if not exists scores (
  score_id text primary key,
  run_id text not null references prediction_runs (run_id),
  resolution_event_id text not null references resolution_events (resolution_event_id),
  scoring_rule text not null,
  crps numeric not null,
  probability_integral_transform numeric not null check (probability_integral_transform between 0 and 1),
  interval80_covered boolean not null,
  signed_error numeric not null,
  absolute_error numeric not null check (absolute_error >= 0),
  score_hash text not null,
  created_at timestamptz not null default now(),
  unique (run_id, resolution_event_id, scoring_rule)
);

create table if not exists quality_gate_results (
  run_id text not null references prediction_runs (run_id),
  gate_name text not null,
  status text not null check (status in ('passed', 'warning', 'failed')),
  detail text,
  created_at timestamptz not null default now(),
  primary key (run_id, gate_name)
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

create or replace function thesis_prevent_update_delete()
returns trigger
language plpgsql
as $$
begin
  raise exception '% is append-only; insert a new version, event, or score instead', tg_table_name;
end;
$$;

create trigger prediction_specs_append_only
before update or delete on prediction_specs
for each row execute function thesis_prevent_update_delete();

create trigger spec_versions_append_only
before update or delete on spec_versions
for each row execute function thesis_prevent_update_delete();

create trigger prediction_runs_append_only
before update or delete on prediction_runs
for each row execute function thesis_prevent_update_delete();

create trigger cdf_points_append_only
before update or delete on cdf_points
for each row execute function thesis_prevent_update_delete();

create trigger public_traces_append_only
before update or delete on public_traces
for each row execute function thesis_prevent_update_delete();

create trigger tool_calls_append_only
before update or delete on tool_calls
for each row execute function thesis_prevent_update_delete();

create trigger resolution_links_append_only
before update or delete on resolution_links
for each row execute function thesis_prevent_update_delete();

create trigger resolution_events_append_only
before update or delete on resolution_events
for each row execute function thesis_prevent_update_delete();

create trigger scores_append_only
before update or delete on scores
for each row execute function thesis_prevent_update_delete();

create trigger quality_gate_results_append_only
before update or delete on quality_gate_results
for each row execute function thesis_prevent_update_delete();

alter table prediction_specs enable row level security;
alter table spec_versions enable row level security;
alter table prediction_runs enable row level security;
alter table cdf_points enable row level security;
alter table public_traces enable row level security;
alter table tool_calls enable row level security;
alter table resolution_links enable row level security;
alter table resolution_events enable row level security;
alter table scores enable row level security;
alter table quality_gate_results enable row level security;
alter table audit_events enable row level security;

create policy prediction_specs_public_read on prediction_specs for select using (true);
create policy spec_versions_public_read on spec_versions for select using (true);
create policy prediction_runs_public_read on prediction_runs for select using (true);
create policy cdf_points_public_read on cdf_points for select using (true);
create policy public_traces_public_read on public_traces for select using (true);
create policy tool_calls_public_read on tool_calls for select using (true);
create policy resolution_links_public_read on resolution_links for select using (true);
create policy resolution_events_public_read on resolution_events for select using (true);
create policy scores_public_read on scores for select using (true);
create policy quality_gate_results_public_read on quality_gate_results for select using (true);
create policy audit_events_public_read on audit_events for select using (true);
