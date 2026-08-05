"""One-off: import the pre-DynamoDB SQLite history into the DynamoDB tables.

Until #77 the trainer stored user state in SQLite. That database was never in
git: it lived at /data/trainer.db inside the Docker volume
`interview-preparation_api_data`, which the compose file stopped mounting when
DynamoDB replaced it. (`backend/trainer.db` in the working tree is a 0-byte
leftover with no tables — it is NOT the source.) The copy this was written and
run against is a `sqlite3 .backup` of that volume, taken 2026-08-05 and kept at
~/dev/interview-preparation-trainer-db-backup-2026-08-05/trainer.db:
35 submissions, 55 attempts (50 solved), 266 runs over 31 problems.

It is kept in the repo rather than thrown away because SQLite state predates
`user_id`: the migration has to be repeated once per target table — DynamoDB
Local first, the deployed table later — and each run has to say, explicitly,
which browser identity the history belongs to.

  python migrate_sqlite_to_dynamo.py --sqlite /tmp/trainer.db \
      --user-id <uuid> --endpoint-url http://dynamodb:8000 --dry-run

`--user-id` is required and never defaulted. The rows land under it as their
partition key, and nothing else in the system knows what it should have been: a
typo produces a table full of live data that no browser can see, with nothing
anywhere to say why. The source database is opened read-only.

Idempotent. The sort keys are ULIDs whose timestamp comes from the row's own
created_at/started_at and whose random half is a hash of the source table and
row id, so a row maps to the same key on every run and a second run is 356
overwrites of identical items. Preserving the original timestamps is not only
about idempotency: the ULID time prefix is what orders the run history and dates
the Stats heatmap, so minting them "now" would flatten a month of history onto
one day.

Two counters are recomputed here rather than carried, because DynamoDB has no
`COUNT(*) … GROUP BY` and db.py maintains them incrementally instead:
`run_count` (runs per problem, on the submissions row) and `attempt_run_count`
(runs per attempt). Note they are SET, not added to: re-running resets them to
what the SQLite source says, discarding anything the app counted since.
"""

import argparse
import hashlib
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime
from decimal import Decimal

import boto3
import ulid
from boto3.dynamodb.conditions import Key

PK = "user_id"
SK = "sk"

# The shape user.current_user() accepts. Duplicated rather than imported so this
# script needs only boto3 and the standard library — user.py pulls in FastAPI,
# which a future run against AWS may well not have on hand.
UUID_RE = re.compile(
    r"\A[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z"
)


def parse_args(argv):
  p = argparse.ArgumentParser(
      description="Import the pre-DynamoDB SQLite history into the DynamoDB "
                  "tables, under one user_id."
  )
  p.add_argument("--sqlite", required=True, help="path to the source trainer.db")
  p.add_argument(
      "--user-id", required=True,
      help="the user_id partition key to write everything under (required; "
           "there is no default and none can be guessed)",
  )
  p.add_argument(
      "--endpoint-url", default=None,
      help="DynamoDB endpoint, e.g. http://dynamodb:8000 for DynamoDB Local; "
           "omit to talk to the real AWS endpoint for --region",
  )
  p.add_argument("--region", default="us-east-1")
  p.add_argument("--submissions-table", default="submissions")
  p.add_argument("--attempts-table", default="attempts")
  p.add_argument("--runs-table", default="runs")
  p.add_argument(
      "--dry-run", action="store_true",
      help="report what would be written and exit without writing",
  )
  return p.parse_args(argv)


def epoch_ms(iso):
  """Epoch milliseconds for one of the source's ISO-8601 timestamps."""
  return int(datetime.fromisoformat(iso).timestamp() * 1000)


def stable_ulid(kind, source_id, iso):
  """The ULID for one source row: its own timestamp, hashed row identity.

  Deliberately independent of the user id, so the same source row keeps the same
  sort key in every table it is imported into and two runs can be diffed.
  """
  seed = f"trainer-sqlite:{kind}:{source_id}".encode()
  return ulid.new(epoch_ms(iso), hashlib.sha256(seed).digest()[:10])


def sk(pid, uid):
  return f"{pid}#{uid}"


def read_source(path):
  """The three source tables, read-only — this must never write to the backup."""
  conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
  conn.row_factory = sqlite3.Row
  try:
    return (
        conn.execute("SELECT * FROM submission").fetchall(),
        conn.execute("SELECT * FROM attempt ORDER BY id").fetchall(),
        conn.execute("SELECT * FROM run ORDER BY id").fetchall(),
    )
  finally:
    conn.close()


def build_items(user, submissions, attempts, runs):
  """(submissions, attempts, runs) items, in db.py's row shapes.

  Attributes that are NULL in SQLite are left off the item rather than written
  as DynamoDB nulls: db.py reads them with .get() and the API removes them
  (`REMOVE running_since`) rather than nulling them, so an absent attribute is
  what a row written by the running app looks like.
  """
  runs_per_problem = Counter(r["problem_id"] for r in runs)
  runs_per_attempt = Counter(
      r["attempt_id"] for r in runs if r["attempt_id"] is not None
  )

  sub_items = [
      {
          PK: user,
          SK: s["problem_id"],
          "code": s["code"],
          "updated_at": s["updated_at"],
          "run_count": runs_per_problem[s["problem_id"]],
      }
      for s in submissions
  ]
  # A problem can have runs without ever having been autosaved; db.py creates a
  # counter-only submissions row for it, so do the same here.
  saved = {s["problem_id"] for s in submissions}
  sub_items += [
      {PK: user, SK: pid, "run_count": n}
      for pid, n in sorted(runs_per_problem.items()) if pid not in saved
  ]

  attempt_items = []
  for a in attempts:
    item = {
        PK: user,
        SK: sk(a["problem_id"], stable_ulid("attempt", a["id"], a["started_at"])),
        "started_at": a["started_at"],
        "accumulated_ms": a["accumulated_ms"],
        "attempt_run_count": runs_per_attempt[a["id"]],
    }
    for col in ("running_since", "solved_at", "elapsed_ms"):
      if a[col] is not None:
        item[col] = a[col]
    attempt_items.append(item)

  run_items = [
      {
          PK: user,
          SK: sk(r["problem_id"], stable_ulid("run", r["id"], r["created_at"])),
          "code": r["code"],
          "passed": r["passed"],
          "failed": r["failed"],
          "total": r["total"],
          # REAL in SQLite; DynamoDB has no float type, and Decimal(str(x)) keeps
          # the value as printed where Decimal(x) would carry the full binary
          # expansion (and be rejected without a wider context).
          "duration_ms": Decimal(str(r["duration_ms"])),
          "all_passed": r["all_passed"],
          "created_at": r["created_at"],
      }
      for r in runs
  ]
  return sub_items, attempt_items, run_items


def report(args, submissions, attempts, runs, sub_items, attempt_items,
           run_items):
  """The dry-run reconciliation: source rows in, items out, side by side."""
  counter_only = len(sub_items) - len(submissions)
  solved = sum(1 for a in attempts if a["solved_at"] is not None)
  linked = sum(1 for r in runs if r["attempt_id"] is not None)
  problems = {r["problem_id"] for r in runs} | {a["problem_id"] for a in attempts}

  print(f"source     {args.sqlite}")
  print(f"target     endpoint={args.endpoint_url or 'AWS ' + args.region}")
  print(f"           submissions={args.submissions_table} "
        f"attempts={args.attempts_table} runs={args.runs_table}")
  print(f"user_id    {args.user_id}")
  print()
  print("  table         source rows   items")
  print(f"  submissions   {len(submissions):>11}   {len(sub_items):>5}"
        f"   (+{counter_only} run-counter-only)")
  print(f"  attempts      {len(attempts):>11}   {len(attempt_items):>5}"
        f"   ({solved} solved)")
  print(f"  runs          {len(runs):>11}   {len(run_items):>5}"
        f"   ({linked} attached to an attempt)")
  print()
  print(f"  {len(problems)} distinct problems with attempts or runs, "
        f"{len(submissions)} with saved code")


def write_items(table, items):
  with table.batch_writer() as batch:
    for item in items:
      batch.put_item(Item=item)


def count_partition(table, user):
  """Items in the user's partition — the post-write check that also shows, on a
  second run, that nothing was duplicated."""
  total, kwargs = 0, {
      "KeyConditionExpression": Key(PK).eq(user), "Select": "COUNT",
  }
  while True:
    resp = table.query(**kwargs)
    total += resp["Count"]
    last = resp.get("LastEvaluatedKey")
    if not last:
      return total
    kwargs["ExclusiveStartKey"] = last


def main(argv=None):
  args = parse_args(argv)
  if not UUID_RE.match(args.user_id):
    sys.exit(f"--user-id {args.user_id!r} is not a canonical UUID; the app only "
             "ever reads state under a value current_user() would accept")
  # current_user() lowercases before it uses the value as a partition key, so
  # write under the lowercased form or the app queries a key that is not there.
  args.user_id = args.user_id.lower()

  submissions, attempts, runs = read_source(args.sqlite)
  sub_items, attempt_items, run_items = build_items(
      args.user_id, submissions, attempts, runs
  )
  report(args, submissions, attempts, runs, sub_items, attempt_items, run_items)

  if args.dry_run:
    print("\nDRY RUN — nothing written.")
    return

  db = boto3.resource(
      "dynamodb", region_name=args.region, endpoint_url=args.endpoint_url
  )
  print()
  for name, items in (
      (args.submissions_table, sub_items),
      (args.attempts_table, attempt_items),
      (args.runs_table, run_items),
  ):
    table = db.Table(name)
    write_items(table, items)
    print(f"  {name}: wrote {len(items)} items, "
          f"partition now holds {count_partition(table, args.user_id)}")


if __name__ == "__main__":
  main()
