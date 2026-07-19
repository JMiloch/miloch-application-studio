#!/usr/bin/env python3
"""
MAS audit-log hash-chain verifier — reference implementation.

Independent of MAS. Reads the AuditEntry table from a SQLite database
(default) or from a CSV/JSON dump and reports whether the chain
verifies. Useful for compliance reviews that want to confirm the chain
state with their own tooling.

Algorithm: see docs/user-docs/600-Memory-DB/650-Audit-Chain.md.

Usage:
    python A4-Audit-Chain-Verify-Reference.py <path/to/memory.db>

Output:
    OK     <count>           — chain valid across <count> rows
    BREAK  <index> <Id> <reason> — first broken row, with diagnosis
    EMPTY                    — no audit rows present
"""

import hashlib
import sqlite3
import sys
from datetime import datetime

UNIT_SEPARATOR = b"\x1f"
NULL_PAYLOAD = b"\x00"
GENESIS_PREVHASH = b"\x00" * 32


def compute_row_hash(entry: dict, prev_hash: bytes) -> bytes:
    """Mirror of MAS.Core.Services.AuditHashChain.ComputeRowHash."""
    assert len(prev_hash) == 32, f"prev_hash must be 32 bytes, got {len(prev_hash)}"

    h = hashlib.sha256()

    def append(field: str | None):
        if field is None:
            h.update(NULL_PAYLOAD)
        else:
            h.update(field.encode("utf-8"))

    append(entry["Id"])
    h.update(UNIT_SEPARATOR)
    append(entry["EventType"])
    h.update(UNIT_SEPARATOR)
    append(entry["EntityType"])
    h.update(UNIT_SEPARATOR)
    append(entry["EntityId"])
    h.update(UNIT_SEPARATOR)
    append(entry["Actor"])
    h.update(UNIT_SEPARATOR)
    # MAS writes ActedAt with .NET's "o" (round-trip) format. SQLite stores
    # the original string verbatim — read it back as-is.
    append(entry["ActedAt"])
    h.update(UNIT_SEPARATOR)
    if entry["PayloadJson"] is None:
        h.update(NULL_PAYLOAD)
    else:
        append(entry["PayloadJson"])
    h.update(UNIT_SEPARATOR)
    h.update(prev_hash)
    return h.digest()


def verify_chain(db_path: str) -> tuple[str, int, str | None]:
    """Returns (status, count, detail). status in {OK, BREAK, EMPTY}."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(
        "SELECT Id, EventType, EntityType, EntityId, Actor, ActedAt, "
        "       PayloadJson, PrevHash, RowHash "
        "  FROM AuditEntry "
        " ORDER BY ActedAt, Id"
    )
    rows = list(cur)
    conn.close()

    if not rows:
        return ("EMPTY", 0, None)

    prev_hash = GENESIS_PREVHASH
    for index, row in enumerate(rows):
        entry = dict(row)
        stored_prev = bytes(entry["PrevHash"]) if entry["PrevHash"] else None
        stored_row = bytes(entry["RowHash"]) if entry["RowHash"] else None

        if stored_prev is None or stored_row is None:
            return ("BREAK", index, f"Id={entry['Id']} has NULL PrevHash/RowHash — run BackfillHashChainAsync in MAS")

        if stored_prev != prev_hash:
            return ("BREAK", index, f"Id={entry['Id']} PrevHash does not match previous row's RowHash")

        expected = compute_row_hash(entry, prev_hash)
        if expected != stored_row:
            return ("BREAK", index, f"Id={entry['Id']} stored RowHash does not match recomputed RowHash")

        prev_hash = stored_row

    return ("OK", len(rows), None)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)

    status, count, detail = verify_chain(sys.argv[1])

    if status == "EMPTY":
        print("EMPTY  — no audit rows present in AuditEntry table")
        sys.exit(0)
    if status == "OK":
        print(f"OK     {count} rows verified at {datetime.utcnow().isoformat()}Z")
        sys.exit(0)
    print(f"BREAK  index={count} {detail}")
    sys.exit(1)


if __name__ == "__main__":
    main()
