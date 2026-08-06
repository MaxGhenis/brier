# USAspending ingestion-wave-1 fixture

`dhs-title-vi-fy2026.json` is the unmodified 1,146-byte response body fetched
from the official USAspending API during the wave-1 verification session. The
file deliberately has no trailing newline because the fetched body had none.

- Retrieved: `2026-08-06T20:01:20Z`
- Method: `POST`
- Endpoint: `https://api.usaspending.gov/api/v2/search/spending_over_time/`
- HTTP status: `200`
- SHA-256: `dd51e2eb947fc8b302fe9c33297c85989b542c933801dcb0729edf39ba157720`
- Selected result: FY2026 `aggregated_amount` = `32171899636.26`

The exact request body was:

```json
{
  "filters": {
    "award_type_codes": [
      "02",
      "03",
      "04",
      "05",
      "06",
      "07",
      "08",
      "09",
      "10",
      "11",
      "A",
      "B",
      "C",
      "D",
      "IDV_A",
      "IDV_B",
      "IDV_B_A",
      "IDV_B_B",
      "IDV_B_C",
      "IDV_C",
      "IDV_D",
      "IDV_E"
    ],
    "time_period": [
      {
        "end_date": "2026-09-30",
        "start_date": "2025-10-01"
      }
    ],
    "treasury_account_components": [
      {
        "aid": "070",
        "bpoa": "2025",
        "epoa": "2029",
        "main": "0530",
        "sub": "000"
      },
      {
        "aid": "070",
        "bpoa": "2025",
        "epoa": "2029",
        "main": "0532",
        "sub": "000"
      },
      {
        "aid": "070",
        "bpoa": "2025",
        "epoa": "2029",
        "main": "0509",
        "sub": "000"
      },
      {
        "aid": "070",
        "bpoa": "2025",
        "epoa": "2029",
        "main": "0510",
        "sub": "000"
      },
      {
        "aid": "070",
        "bpoa": "2025",
        "epoa": "2029",
        "main": "0413",
        "sub": "000"
      },
      {
        "aid": "070",
        "main": "0722"
      }
    ]
  },
  "group": "fiscal_year",
  "spending_level": "transactions"
}
```

This response is an award-transaction aggregate associated with the exact
Treasury-account-component union above. It is not a financial-account balance
or outlay total.
