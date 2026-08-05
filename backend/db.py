"""DynamoDB storage for the coding-trainer API — user state only.

One table, composite key (pk, sk). Everything a user owns lives in that user's
single partition, so every read below is a GetItem or a Query on one partition —
there is no Scan anywhere, and none should be added.

  pk             sk                        item
  ------------   -----------------------   ----------------------------------
  U#<user_id>    P#<problem_id>            per-problem state: the saved code,
                                           the latest attempt's timer fields,
                                           and the two run counters
  U#<user_id>    RUN#<problem_id>#<ulid>   one test run (result + the code)
  U#<user_id>    SLV#<problem_id>#<ulid>   one solved attempt (the solve log)

Problem ids are the stable path-based slugs, so a content rebuild never
invalidates a key.

Three things that do not carry over from the SQLite schema this replaces:

  - There is no autoincrement, so the RUN#/SLV# sort keys end in a ULID. ULIDs
    are lexicographically time-ordered, which is what keeps "newest run first" a
    native descending Query instead of a client-side sort.
  - There is no COUNT(*) … GROUP BY, so `run_count` (every run of a problem) and
    `attempt_run_count` (runs in the latest attempt) are counter attributes on
    the P# item, maintained with atomic ADD.
  - The latest attempt is folded into the P# item and Retake overwrites it, so
    solved attempts are ALSO written as their own SLV# items. The stats page
    needs every solve ever, not the latest one — see _progress_entry in
    server.py.
"""

import os
import secrets
import threading
import time
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

TABLE_NAME = os.environ.get("DDB_TABLE", "trainer")
# Set only for local development (DynamoDB Local). Empty in AWS, where boto3
# resolves the real endpoint and the credentials come from the task role.
ENDPOINT = os.environ.get("DDB_ENDPOINT") or None
REGION = os.environ.get("AWS_REGION", "us-east-1")

_table = None


def _resource():
  return boto3.resource("dynamodb", region_name=REGION, endpoint_url=ENDPOINT)


def table():
  """The Table resource, created once per process (boto3 clients are cheap to
  reuse and expensive to rebuild per request)."""
  global _table
  if _table is None:
    _table = _resource().Table(TABLE_NAME)
  return _table


def init_db():
  """Create the table, for local development only.

  In AWS the table is infrastructure: it is created by the CDK stack and the
  app's role has no CreateTable permission. DDB_ENDPOINT is set only when
  pointing at DynamoDB Local, so it is what gates this.
  """
  if not ENDPOINT:
    return
  ddb = _resource()
  # `docker compose up` starts uvicorn and dynamodb-local together; the Java
  # process needs a moment before it answers, so retry rather than crash-loop.
  for attempt in range(30):
    try:
      ddb.create_table(
          TableName=TABLE_NAME,
          KeySchema=[
              {"AttributeName": "pk", "KeyType": "HASH"},
              {"AttributeName": "sk", "KeyType": "RANGE"},
          ],
          AttributeDefinitions=[
              {"AttributeName": "pk", "AttributeType": "S"},
              {"AttributeName": "sk", "AttributeType": "S"},
          ],
          BillingMode="PAY_PER_REQUEST",
      )
      return
    except ClientError as e:
      if e.response["Error"]["Code"] == "ResourceInUseException":
        return  # already created by an earlier boot
      raise
    except Exception:
      if attempt == 29:
        raise
      time.sleep(1)


# --- ULID ------------------------------------------------------------------
# 48 bits of millisecond timestamp + 80 bits of randomness, Crockford base32.
# The only property the storage layer relies on is that the string ordering
# matches the creation ordering.

_B32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
_ulid_lock = threading.Lock()
_ulid_last = (0, 0)


def new_ulid() -> str:
  """A 26-character, lexicographically time-ordered id.

  Monotonic within the process: two ids minted in the same millisecond increment
  the random component instead of drawing again, so the run written second also
  sorts second. Without that, "newest first" would be a coin flip for runs a few
  hundred microseconds apart.
  """
  global _ulid_last
  with _ulid_lock:
    ms = int(time.time() * 1000)
    last_ms, last_rand = _ulid_last
    if ms > last_ms:
      rand = secrets.randbits(80)
    else:
      ms, rand = last_ms, last_rand + 1
    _ulid_last = (ms, rand)
  n = (ms << 80) | rand
  return "".join(_B32[(n >> shift) & 31] for shift in range(125, -1, -5))


# --- keys ------------------------------------------------------------------


def user_pk(user_id: str) -> str:
  return f"U#{user_id}"


def problem_sk(pid: str) -> str:
  return f"P#{pid}"


def run_prefix(pid: str) -> str:
  return f"RUN#{pid}#"


def solve_prefix(pid: str) -> str:
  return f"SLV#{pid}#"


# --- row shaping -----------------------------------------------------------
# Items come back with DynamoDB's Decimal numbers and with absent attributes
# simply missing. Everything below normalizes both away, so server.py sees the
# same flat dicts (plain ints/floats, every key present) the SQLite rows gave it
# and still owns the snake_case→camelCase serialization.


def _int(v, default=None):
  return default if v is None else int(v)


def _problem_row(item, pid=None) -> dict:
  return {
      "problem_id": pid if pid is not None else item["sk"][2:],
      "code": item.get("code"),
      "started_at": item.get("started_at"),
      "accumulated_ms": _int(item.get("accumulated_ms"), 0),
      "running_since": item.get("running_since"),
      "solved_at": item.get("solved_at"),
      "elapsed_ms": _int(item.get("elapsed_ms")),
      "run_count": _int(item.get("run_count"), 0),
      "attempt_run_count": _int(item.get("attempt_run_count"), 0),
  }


def _run_row(item) -> dict:
  return {
      # The sort key's ULID suffix is the run id. It replaces the SQLite
      # autoincrement, so run ids are strings now rather than integers; the
      # client only ever uses the value as a React key.
      "id": item["sk"].rsplit("#", 1)[1],
      "problem_id": item["problem_id"],
      "code": item["code"],
      "passed": _int(item["passed"]),
      "failed": _int(item["failed"]),
      "total": _int(item["total"]),
      "duration_ms": float(item["duration_ms"]),
      "all_passed": _int(item["all_passed"]),
      "created_at": item["created_at"],
  }


def _solve_row(item) -> dict:
  return {
      "problem_id": item["problem_id"],
      "solved_at": item["solved_at"],
      "elapsed_ms": _int(item.get("elapsed_ms")),
  }


def _query_all(**kwargs) -> list:
  """Every page of a Query. A single response is capped at 1 MB, which a user
  with a lot of saved code can exceed, so the pages are followed rather than
  assumed to be one."""
  items = []
  while True:
    resp = table().query(**kwargs)
    items.extend(resp["Items"])
    key = resp.get("LastEvaluatedKey")
    if not key:
      return items
    kwargs["ExclusiveStartKey"] = key


# --- reads -----------------------------------------------------------------


def get_problem(user_id, pid) -> dict | None:
  resp = table().get_item(Key={"pk": user_pk(user_id), "sk": problem_sk(pid)})
  item = resp.get("Item")
  return _problem_row(item, pid) if item else None


def list_problems(user_id) -> list[dict]:
  """Every problem this user has state for, ascending by problem id — the whole
  progress bundle in one Query."""
  items = _query_all(
      KeyConditionExpression=Key("pk").eq(user_pk(user_id))
      & Key("sk").begins_with("P#"),
  )
  return [_problem_row(i) for i in items]


def list_solves(user_id, pid=None):
  """Every solved attempt, ascending. The ULID suffix makes that chronological
  within a problem, which the stats folds depend on (their tie-breaks are
  order-dependent, so the ordering is explicit rather than incidental)."""
  prefix = "SLV#" if pid is None else solve_prefix(pid)
  items = _query_all(
      KeyConditionExpression=Key("pk").eq(user_pk(user_id))
      & Key("sk").begins_with(prefix),
  )
  return [_solve_row(i) for i in items]


def list_runs(user_id, pid, limit):
  """A problem's runs, newest first. Descending on the sort key IS newest-first
  because the suffix is a ULID."""
  resp = table().query(
      KeyConditionExpression=Key("pk").eq(user_pk(user_id))
      & Key("sk").begins_with(run_prefix(pid)),
      ScanIndexForward=False,
      Limit=limit,
  )
  return [_run_row(i) for i in resp["Items"]]


# --- writes ----------------------------------------------------------------
# Every write is an UpdateItem on the P# item (upserting it if this is the
# problem's first) or a PutItem of a new RUN#/SLV# item. Nothing read-modify-
# writes a counter: run_count and attempt_run_count use ADD.


def _update_problem(user_id, pid, **kwargs):
  table().update_item(
      Key={"pk": user_pk(user_id), "sk": problem_sk(pid)}, **kwargs
  )


def save_code(user_id, pid, code, ts):
  _update_problem(
      user_id, pid,
      UpdateExpression="SET code = :c, updated_at = :t",
      ExpressionAttributeValues={":c": code, ":t": ts},
  )


def start_attempt(user_id, pid, ts):
  """Start or Retake: the latest attempt is overwritten in place.

  attempt_run_count resets, run_count does not (it counts every run ever), and
  the previous attempt's solve survives as its SLV# item — which is what keeps a
  retaken problem "ever solved" for the lessons and stats.
  """
  _update_problem(
      user_id, pid,
      UpdateExpression=(
          "SET started_at = :t, accumulated_ms = :zero, running_since = :t,"
          " attempt_run_count = :zero REMOVE solved_at, elapsed_ms"
      ),
      ExpressionAttributeValues={":t": ts, ":zero": 0},
  )


def pause_attempt(user_id, pid, add_ms):
  _update_problem(
      user_id, pid,
      UpdateExpression="ADD accumulated_ms :ms REMOVE running_since",
      ExpressionAttributeValues={":ms": int(add_ms)},
  )


def resume_attempt(user_id, pid, ts):
  _update_problem(
      user_id, pid,
      UpdateExpression="SET running_since = :t",
      ExpressionAttributeValues={":t": ts},
  )


def finalize_solve(user_id, pid, ts, elapsed_ms):
  """Stop the timer on the latest attempt and append the solve to the log."""
  _update_problem(
      user_id, pid,
      UpdateExpression="SET solved_at = :t, elapsed_ms = :ms REMOVE running_since",
      ExpressionAttributeValues={":t": ts, ":ms": int(elapsed_ms)},
  )
  table().put_item(Item={
      "pk": user_pk(user_id),
      "sk": solve_prefix(pid) + new_ulid(),
      "problem_id": pid,
      "solved_at": ts,
      "elapsed_ms": int(elapsed_ms),
  })


def create_run(user_id, pid, code, passed, failed, total, duration_ms,
               all_passed, ts, in_attempt):
  """Record a test run and bump the counters it belongs to.

  `in_attempt` says whether a timed attempt is open. Runs outside one still
  count towards run_count but not towards attempt_run_count, mirroring the
  nullable attempt_id of the schema this replaces.
  """
  item = {
      "pk": user_pk(user_id),
      "sk": run_prefix(pid) + new_ulid(),
      "problem_id": pid,
      "code": code,
      "passed": int(passed),
      "failed": int(failed),
      "total": int(total),
      # DynamoDB has no float type; Decimal(str(...)) keeps the decimal digits
      # the client sent rather than the binary float's expansion.
      "duration_ms": Decimal(str(duration_ms)),
      "all_passed": int(all_passed),
      "created_at": ts,
  }
  table().put_item(Item=item)
  counters = "run_count :one, attempt_run_count :one" if in_attempt else "run_count :one"
  _update_problem(
      user_id, pid,
      UpdateExpression=f"ADD {counters}",
      ExpressionAttributeValues={":one": 1},
  )
  return _run_row(item)
