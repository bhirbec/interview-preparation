"""DynamoDB storage for the coding-trainer API — user state only.

Three tables, one per entity, mirroring the SQLite schema this replaced:
  - submissions: the latest autosaved implementation per problem, plus that
                 problem's lifetime run counter.
  - attempts:    a log of timed attempts; the latest one drives a problem's
                 status, and a solved attempt is one with `solved_at` set (there
                 is no separate "solves" table).
  - runs:        one row per test run (result + the code that produced it).

Every table is partitioned by `user_id`, so a request can only ever read the
calling browser's own state and every read below is a GetItem or a
single-partition Query — no scans, no GSIs.

  | table       | user_id (pk) | sk                   | attributes                    |
  |-------------|--------------|----------------------|-------------------------------|
  | submissions | user id      | problem_id           | code, updated_at, run_count   |
  | attempts    | user id      | problem_id#<ulid>    | started_at, accumulated_ms,   |
  |             |              |                      | running_since, solved_at,     |
  |             |              |                      | elapsed_ms, attempt_run_count |
  | runs        | user id      | problem_id#<ulid>    | code, passed, failed, total,  |
  |             |              |                      | duration_ms, all_passed,      |
  |             |              |                      | created_at                    |

Problem ids are paths and can contain "/" ("CTCI/1.1-is-unique"). ULIDs are
base32 and cannot contain "#", so "<problem_id>#<ulid>" always splits back apart
on its LAST "#" whatever the id holds, and `begins_with(sk, "<problem_id>#")`
selects exactly one problem's rows.

The counters exist because DynamoDB has no `COUNT(*) … GROUP BY`: counting runs
would mean querying the runs table, which drags every stored code blob back over
the wire. `run_count` (lifetime, per problem) and `attempt_run_count` (per
attempt) are maintained instead, with atomic `ADD`.

Rows come back as plain dicts under the old SQLite column names, with numbers
already narrowed out of `Decimal` — server.py owns the snake_case→camelCase
serialization and is unaware of any of the above.
"""

import os
import time
from decimal import Decimal

import boto3
import ulid
from boto3.dynamodb.conditions import Key
from botocore.exceptions import EndpointConnectionError

# Set to DynamoDB Local's address in development (docker-compose does this);
# unset in AWS, where the region and the instance role do the addressing.
ENDPOINT_URL = os.environ.get("DYNAMODB_ENDPOINT") or None
REGION = os.environ.get("AWS_REGION", "us-east-1")

SUBMISSIONS_TABLE = os.environ.get("SUBMISSIONS_TABLE", "submissions")
ATTEMPTS_TABLE = os.environ.get("ATTEMPTS_TABLE", "attempts")
RUNS_TABLE = os.environ.get("RUNS_TABLE", "runs")

PK = "user_id"
SK = "sk"

_resource = None


def _db():
  """The shared boto3 resource (one connection pool for the process)."""
  global _resource
  if _resource is None:
    _resource = boto3.resource(
        "dynamodb", region_name=REGION, endpoint_url=ENDPOINT_URL
    )
  return _resource


def _submissions():
  return _db().Table(SUBMISSIONS_TABLE)


def _attempts():
  return _db().Table(ATTEMPTS_TABLE)


def _runs():
  return _db().Table(RUNS_TABLE)


# --- setup -----------------------------------------------------------------


def init_db():
  """Create the tables — development only.

  In AWS the tables are owned by the CDK app in aws/ (RETAIN, on-demand); an API
  process must never create them there, or a typo'd table name would silently
  provision a second, empty table instead of failing loudly. So this is a no-op
  unless DYNAMODB_ENDPOINT points at a local DynamoDB.
  """
  if not ENDPOINT_URL:
    return
  client = _db().meta.client
  for name in (SUBMISSIONS_TABLE, ATTEMPTS_TABLE, RUNS_TABLE):
    try:
      _create_table(client, name)
    except client.exceptions.ResourceInUseException:
      pass  # already created by a previous boot


def _create_table(client, name, attempts=30):
  """Create `name`, waiting for the container to accept connections.

  docker-compose starts the API alongside DynamoDB Local, so the first calls of
  a cold `docker compose up` land before the Java process is listening.
  """
  for i in range(attempts):
    try:
      client.create_table(
          TableName=name,
          KeySchema=[
              {"AttributeName": PK, "KeyType": "HASH"},
              {"AttributeName": SK, "KeyType": "RANGE"},
          ],
          AttributeDefinitions=[
              {"AttributeName": PK, "AttributeType": "S"},
              {"AttributeName": SK, "AttributeType": "S"},
          ],
          BillingMode="PAY_PER_REQUEST",
      )
      return
    except EndpointConnectionError:
      if i == attempts - 1:
        raise
      time.sleep(1)


# --- keys and row shapes ---------------------------------------------------


def _key(user, sk):
  return {PK: user, SK: sk}


def _sk(pid, uid):
  return f"{pid}#{uid}"


def _pid_of(sk):
  return sk.rsplit("#", 1)[0]


def _uid_of(sk):
  return sk.rsplit("#", 1)[1]


def _opt_int(v):
  return None if v is None else int(v)


def _attempt_row(item):
  """An attempt as the old `attempt` table row, plus `sk` (its identity)."""
  return {
      "sk": item[SK],
      "problem_id": _pid_of(item[SK]),
      "started_at": item.get("started_at"),
      "accumulated_ms": int(item.get("accumulated_ms", 0)),
      "running_since": item.get("running_since"),
      "solved_at": item.get("solved_at"),
      "elapsed_ms": _opt_int(item.get("elapsed_ms")),
      # Absent on rows written before their first run — ADD creates the counter.
      "attempt_run_count": int(item.get("attempt_run_count", 0)),
  }


def _run_row(item):
  """A run as the old `run` table row. `id` is the ULID half of the sort key:
  a string where SQLite had an integer, still unique and still the newest-first
  ordering the client renders with."""
  return {
      "id": _uid_of(item[SK]),
      "problem_id": _pid_of(item[SK]),
      "code": item["code"],
      "passed": int(item["passed"]),
      "failed": int(item["failed"]),
      # REAL in SQLite; DynamoDB hands back Decimal, which would serialize as a
      # JSON string unless narrowed here.
      "duration_ms": float(item["duration_ms"]),
      "total": int(item["total"]),
      "all_passed": int(item["all_passed"]),
      "created_at": item["created_at"],
  }


def _query_all(table, **kwargs):
  """Every page of a Query — DynamoDB caps a page at 1 MB regardless of Limit."""
  items = []
  while True:
    resp = table.query(**kwargs)
    items += resp["Items"]
    last = resp.get("LastEvaluatedKey")
    if not last:
      return items
    kwargs["ExclusiveStartKey"] = last


# --- submissions -----------------------------------------------------------


def get_submission(user, pid):
  """(code, run_count) for one problem — one GetItem, both callers' worth.

  A run on a problem that was never autosaved creates the row for its counter
  alone, so an existing row does not imply code.
  """
  item = _submissions().get_item(Key=_key(user, pid)).get("Item") or {}
  return item.get("code"), int(item.get("run_count", 0))


def run_counts(user):
  """(problem_id, n) for every problem the user has ever run, ascending by id.

  Projected down to the counter: the submissions rows carry code blobs, and this
  feeds /api/progress, which wants none of them.
  """
  items = _query_all(
      _submissions(),
      KeyConditionExpression=Key(PK).eq(user),
      ProjectionExpression="#sk, run_count",
      ExpressionAttributeNames={"#sk": SK},
  )
  return [(i[SK], int(i["run_count"])) for i in items if int(i.get("run_count", 0))]


def upsert_submission(user, pid, code, ts):
  _submissions().update_item(
      Key=_key(user, pid),
      UpdateExpression="SET #code = :code, updated_at = :ts",
      ExpressionAttributeNames={"#code": "code"},
      ExpressionAttributeValues={":code": code, ":ts": ts},
  )


# --- attempts --------------------------------------------------------------


def latest_attempt(user, pid):
  """The newest attempt on one problem, or None.

  ULID sort keys are time-ordered, so this is the first row of a descending
  query — no sorting, and one row over the wire.
  """
  resp = _attempts().query(
      KeyConditionExpression=Key(PK).eq(user) & Key(SK).begins_with(f"{pid}#"),
      ScanIndexForward=False,
      Limit=1,
  )
  items = resp["Items"]
  return _attempt_row(items[0]) if items else None


def problem_attempts(user, pid):
  """Every attempt on one problem, ascending (so the last one is the latest).

  /api/problem/state needs the latest attempt *and* the problem's solve log, and
  a problem has a handful of attempts at most — one query answers both.
  """
  return [
      _attempt_row(i)
      for i in _query_all(
          _attempts(),
          KeyConditionExpression=Key(PK).eq(user) & Key(SK).begins_with(f"{pid}#"),
      )
  ]


def all_attempts(user):
  """Every attempt row for the user, ascending by (problem_id, ULID).

  /api/progress needs the latest attempt per problem and every solved attempt,
  and DynamoDB has no top-N-per-group — so it reads the whole (small) partition
  and folds in Python. Attempt rows are a handful of scalars each; the runs
  table, which carries the code blobs, is deliberately not read in that path.
  """
  return [
      _attempt_row(i)
      for i in _query_all(_attempts(), KeyConditionExpression=Key(PK).eq(user))
  ]


def insert_attempt(user, pid, ts):
  _attempts().put_item(
      Item={
          **_key(user, _sk(pid, ulid.new())),
          "started_at": ts,
          "accumulated_ms": 0,
          "running_since": ts,
          "attempt_run_count": 0,
      }
  )


def pause_attempt(user, sk, add_ms):
  _attempts().update_item(
      Key=_key(user, sk),
      UpdateExpression="ADD accumulated_ms :ms REMOVE running_since",
      ExpressionAttributeValues={":ms": add_ms},
  )


def resume_attempt(user, sk, ts):
  _attempts().update_item(
      Key=_key(user, sk),
      UpdateExpression="SET running_since = :ts",
      ExpressionAttributeValues={":ts": ts},
  )


def finalize_solve(user, sk, ts, elapsed_ms):
  _attempts().update_item(
      Key=_key(user, sk),
      UpdateExpression=(
          "SET solved_at = :ts, elapsed_ms = :ms REMOVE running_since"
      ),
      ExpressionAttributeValues={":ts": ts, ":ms": elapsed_ms},
  )


# --- runs ------------------------------------------------------------------


def insert_run(user, pid, code, passed, failed, total, duration_ms, all_passed,
               ts, attempt_sk):
  """Record a run and bump the two counters that summarize it.

  NOT ATOMIC — three separate writes, four when the run solves the problem:
    1. PutItem on `runs`,
    2. ADD run_count on the problem's `submissions` row,
    3. ADD attempt_run_count on the current `attempts` row (skipped when the
       problem has no attempt yet),
    4. finalize_solve() on that same attempt row, issued by server.py right
       after this returns when every test passed.

  If the process dies between them, the run exists but a counter is one low (or,
  on a retried request, one high). What the user sees is a wrong "3 runs" label
  or a wrong run total on the stats page — the run itself, its code and its
  result are intact, and nothing is lost.

  Both counters are derivable from the runs table (count the rows whose sk
  begins with "<problem_id>#" for run_count; group by attempt for
  attempt_run_count), so drift is repairable by a backfill, not by asking the
  user to redo anything.

  TransactWriteItems across the three tables is the fix if this ever matters —
  DynamoDB supports it cross-table and it would make all four writes atomic, at
  double the write cost of every single test run. Not worth paying to protect a
  counter that is both cosmetic and rebuildable, but the trade is here so that
  whoever finds a count off by one can tell at a glance that it is an expected
  partial write and not a new bug.
  """
  item = {
      **_key(user, _sk(pid, ulid.new())),
      "code": code,
      "passed": passed,
      "failed": failed,
      "total": total,
      # DynamoDB has no float type; Decimal(str(x)) keeps the value as printed,
      # unlike Decimal(x), which carries the full binary expansion.
      "duration_ms": Decimal(str(duration_ms)),
      "all_passed": all_passed,
      "created_at": ts,
  }
  _runs().put_item(Item=item)

  _submissions().update_item(
      Key=_key(user, pid),
      UpdateExpression="ADD run_count :one",
      ExpressionAttributeValues={":one": 1},
  )
  if attempt_sk:
    _attempts().update_item(
        Key=_key(user, attempt_sk),
        UpdateExpression="ADD attempt_run_count :one",
        ExpressionAttributeValues={":one": 1},
    )
  return _run_row(item)


def list_run_rows(user, pid, limit):
  """The newest `limit` runs for one problem, newest first."""
  rows = []
  kwargs = {
      "KeyConditionExpression": Key(PK).eq(user) & Key(SK).begins_with(f"{pid}#"),
      "ScanIndexForward": False,
      "Limit": limit,
  }
  while len(rows) < limit:
    resp = _runs().query(**kwargs)
    rows += [_run_row(i) for i in resp["Items"]]
    last = resp.get("LastEvaluatedKey")
    # Runs carry code, so `limit` rows can exceed a 1 MB page; keep paging until
    # the page budget is filled or the problem runs out of runs.
    if not last:
      break
    kwargs["ExclusiveStartKey"] = last
    kwargs["Limit"] = limit - len(rows)
  return rows[:limit]
