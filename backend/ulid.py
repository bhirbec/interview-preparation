"""ULIDs — the sort-key half of every attempt and run key.

DynamoDB has no autoincrement, so the SQLite `INTEGER PRIMARY KEY AUTOINCREMENT`
ids became ULIDs: 26 Crockford-base32 characters, a 48-bit millisecond timestamp
followed by 80 random bits. Two properties are why this and not uuid4:

  - they sort lexicographically by creation time, so "newest first" is a native
    `ScanIndexForward=False` query with no client-side sorting, and
  - the timestamp is supplied by the caller, so a future import can rebuild
    history under its original timestamps instead of today's.

Ordering is only guaranteed across distinct milliseconds: two ULIDs minted in
the same millisecond are ordered by their random half. Every id here is minted
by a human clicking Run or Start, so that tie is not reachable in practice, and
the consequence would be two same-millisecond rows swapping places.
"""

import os
import time

# Crockford base32: no I, L, O or U, so an id is safe to read aloud or retype.
ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

TIME_LEN = 10   # 50 bits of characters holding a 48-bit millisecond timestamp
RANDOM_LEN = 16  # 80 bits of randomness
LENGTH = TIME_LEN + RANDOM_LEN


def new(ms: int | None = None) -> str:
  """A fresh ULID, timestamped now or at `ms` (epoch milliseconds)."""
  if ms is None:
    ms = int(time.time() * 1000)
  return _encode(ms, TIME_LEN) + _encode(
      int.from_bytes(os.urandom(10), "big"), RANDOM_LEN
  )


def _encode(value: int, length: int) -> str:
  chars = []
  for _ in range(length):
    chars.append(ALPHABET[value & 0x1F])
    value >>= 5
  return "".join(reversed(chars))
