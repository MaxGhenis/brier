alter table scores
  add column if not exists normalization_scale numeric
    check (normalization_scale is null or normalization_scale > 0),
  add column if not exists normalization_scale_source text not null
    default 'unavailable'
    check (normalization_scale_source in ('ledger_dispersion', 'unavailable')),
  add column if not exists normalized_absolute_error numeric
    check (normalized_absolute_error is null or normalized_absolute_error >= 0),
  add column if not exists sharpness numeric
    check (sharpness is null or sharpness >= 0);

alter table scores
  add constraint scores_normalization_availability_check
  check (
    scoring_rule <> 'numeric_cdf_crps_v3_ledger_scale'
    or
    (normalization_scale_source = 'ledger_dispersion'
      and normalization_scale is not null
      and normalized_score is not null
      and normalized_crps is not null
      and normalized_absolute_error is not null
      and sharpness is not null)
    or
    (normalization_scale_source = 'unavailable'
      and normalization_scale is null
      and normalized_score is null
      and normalized_crps is null
      and normalized_absolute_error is null
      and sharpness is null)
  );
