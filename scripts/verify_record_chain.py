#!/usr/bin/env python3
"""Verify the records/ digest hash chain.

Each daily digest.json (from 2026-07-02 on) carries a `chain` block:

    "chain": {"prevDay": "YYYY-MM-DD", "prevDigestSha256": "<sha256 of that
    day's digest.json file bytes>"}

linking it to the most recent prior day that has a digest. Git timestamps
each link; the chain makes the *contents* self-verifying too — a rewritten
historical digest breaks every later link, so tampering requires rewriting
the whole suffix of the chain in git, not one file.

Days may be missing (see records/*/GAP.md); the chain simply spans them.
Digests written before chaining began (<= 2026-07-01) have no chain block
and are anchored by git history alone.

Usage: python3 scripts/verify_record_chain.py [records_dir]
Exit 0 = chain verifies, 1 = broken link or malformed chain block.
"""

import hashlib
import json
import re
import sys
from pathlib import Path


def day_digests(records: Path) -> list[Path]:
    days = [
        p / "digest.json"
        for p in sorted(records.iterdir())
        if p.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name)
    ]
    return [d for d in days if d.exists()]


def main() -> int:
    records = Path(sys.argv[1] if len(sys.argv) > 1 else "records")
    digests = day_digests(records)
    if not digests:
        print("no daily digests found under", records)
        return 1

    ok = True
    prev_path: Path | None = None
    for path in digests:
        day = path.parent.name
        chain = json.loads(path.read_text()).get("chain")
        if chain is None:
            print(f"  {day}  pre-chain digest (git-anchored only)")
        elif prev_path is None:
            print(f"  {day}  chain block but no prior digest exists — BROKEN")
            ok = False
        else:
            want_day = prev_path.parent.name
            want_sha = hashlib.sha256(prev_path.read_bytes()).hexdigest()
            if chain.get("prevDay") == want_day and chain.get("prevDigestSha256") == want_sha:
                print(f"  {day}  links {want_day} OK")
            else:
                print(
                    f"  {day}  BROKEN link: says {chain.get('prevDay')}/"
                    f"{str(chain.get('prevDigestSha256'))[:12]}…, "
                    f"expected {want_day}/{want_sha[:12]}…"
                )
                ok = False
        prev_path = path

    print("chain OK" if ok else "CHAIN BROKEN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
