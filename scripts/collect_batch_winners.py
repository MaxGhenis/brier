#!/usr/bin/env python3
"""Print the cells file of the latest passing run per catalogSlug.

Feeds spawned_cells_to_ts.py after a batch (plus retries): later batches
supersede earlier ones for the same slug, failed runs never publish.

Usage: python3 scripts/collect_batch_winners.py BATCH1.json BATCH2.json ...
Exits 1 listing any slug that has no passing run across the given batches.
"""

import json
import sys

winners: dict[str, str] = {}
wanted: set[str] = set()
for path in sys.argv[1:]:
    batch = json.load(open(path))
    for result in batch["results"]:
        slug = result["target"]["catalogSlug"]
        wanted.add(slug)
        if result["ok"] and result.get("cellsPath"):
            winners[slug] = result["cellsPath"]

missing = sorted(wanted - set(winners))
if missing:
    print("no passing run for: " + ", ".join(missing), file=sys.stderr)
    sys.exit(1)
print("\n".join(winners[slug] for slug in sorted(winners)))
