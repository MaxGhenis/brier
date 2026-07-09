alter table forecast_distributions
  add column if not exists distribution_provenance text,
  add column if not exists transform_version text;

-- Historical rows are append-only and cannot be classified faithfully from
-- their point arrays alone. Leave them null until they are re-projected from
-- the immutable run payload; all new backfill inserts carry both fields.
alter table forecast_distributions
  add constraint forecast_distributions_provenance_check
    check (
      distribution_provenance is null
      or distribution_provenance in ('agent_reported', 'interval_seeded')
    );

alter table scores
  add column if not exists distribution_provenance text,
  add column if not exists transform_version text;

alter table scores
  add constraint scores_distribution_provenance_check
    check (
      distribution_provenance is null
      or distribution_provenance in ('agent_reported', 'interval_seeded')
    );
