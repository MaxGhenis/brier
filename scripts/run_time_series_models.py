#!/usr/bin/env python3
"""Emit Thesis time-series model candidates with prediction intervals.

Usage:
  python3 scripts/run_time_series_models.py \
    --target-id fns.snap.overpayment_payment_error_rate.us.fy2026 \
    --target-period FY2026 \
    --history-json '[{"period":"2024","value":9.26},{"period":"2025","value":9.28}]' \
    --models persistence \
    --round-increment 0.1
"""

from brier.timeseries import main

if __name__ == "__main__":
    raise SystemExit(main())
