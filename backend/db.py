"""SQLite storage for the coding-trainer API.

User state only — the knowledge content is static JSON built by
build_content.py. Three tables, keyed by the problem slug (a stable id, so a
content rebuild never invalidates them):
  - submission: the latest autosaved implementation per problem.
  - run:        one row per test run (result + the code that produced it).
  - attempt:    a log of timed attempts; the latest one drives a problem's status.

Every access pattern is a key-value read or write keyed by problem_id.
"""

import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.environ.get(
    "DB_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "trainer.db")
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS submission (
  problem_id TEXT PRIMARY KEY,
  code       TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS run (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  problem_id  TEXT NOT NULL,
  code        TEXT NOT NULL,
  passed      INTEGER NOT NULL,
  failed      INTEGER NOT NULL,
  total       INTEGER NOT NULL,
  duration_ms REAL NOT NULL,
  all_passed  INTEGER NOT NULL,
  created_at  TEXT NOT NULL,
  attempt_id  INTEGER              -- FK to attempt.id; _add_run_attempt_id backfills older DBs
);

CREATE INDEX IF NOT EXISTS idx_run_problem ON run (problem_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_run_attempt ON run (attempt_id);

-- A log of timed attempts (one row per Start/Retake). Status is derived from
-- the latest attempt per problem; the log also feeds daily stats later.
CREATE TABLE IF NOT EXISTS attempt (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  problem_id     TEXT NOT NULL,
  started_at     TEXT NOT NULL,
  accumulated_ms INTEGER NOT NULL DEFAULT 0,   -- active time from finished (paused) segments
  running_since  TEXT,                          -- ISO while running; NULL while paused or solved
  solved_at      TEXT,
  elapsed_ms     INTEGER
);

CREATE INDEX IF NOT EXISTS idx_attempt_problem ON attempt (problem_id, id DESC);
"""


@contextmanager
def connect():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  try:
    yield conn
    conn.commit()
  finally:
    conn.close()


def _add_run_attempt_id(conn):
  """Link runs to attempts (SQLite has no ADD COLUMN IF NOT EXISTS)."""
  cols = [r["name"] for r in conn.execute("PRAGMA table_info(run)").fetchall()]
  if "attempt_id" not in cols:
    conn.execute("ALTER TABLE run ADD COLUMN attempt_id INTEGER")


def _backfill_solved_attempts(conn):
  """One-time: seed a solved attempt for problems already solved (no duration)."""
  if conn.execute("SELECT COUNT(*) AS n FROM attempt").fetchone()["n"]:
    return
  rows = conn.execute(
      """
      SELECT problem_id, MAX(created_at) AS solved_at
      FROM run WHERE all_passed = 1
      GROUP BY problem_id
      """
  ).fetchall()
  for r in rows:
    conn.execute(
        "INSERT INTO attempt (problem_id, started_at, solved_at, elapsed_ms) "
        "VALUES (?, ?, ?, NULL)",
        (r["problem_id"], r["solved_at"], r["solved_at"]),
    )


def init_db():
  with connect() as conn:
    conn.executescript(SCHEMA)
    _add_run_attempt_id(conn)
    _backfill_solved_attempts(conn)
    conn.execute("DROP TABLE IF EXISTS chapter")  # renamed to lesson
    # The content moved to static JSON; drop the tables in existing dev volumes.
    conn.execute("DROP TABLE IF EXISTS problem")
    conn.execute("DROP TABLE IF EXISTS lesson")


# --- data access -----------------------------------------------------------
# Each function takes an open connection so the caller controls the transaction
# boundary (commit happens when its `with connect()` block exits). Rows are
# returned raw; server.py owns the snake_case→camelCase serialization.


def get_submission_code(conn, pid):
  r = conn.execute(
      "SELECT code FROM submission WHERE problem_id = ?", (pid,)
  ).fetchone()
  return r["code"] if r else None


def upsert_submission(conn, pid, code, ts):
  conn.execute(
      """
      INSERT INTO submission (problem_id, code, updated_at)
      VALUES (?, ?, ?)
      ON CONFLICT(problem_id)
      DO UPDATE SET code = excluded.code, updated_at = excluded.updated_at
      """,
      (pid, code, ts),
  )


def latest_attempt(conn, pid):
  return conn.execute(
      "SELECT * FROM attempt WHERE problem_id = ? ORDER BY id DESC LIMIT 1", (pid,)
  ).fetchone()


def latest_attempts(conn):
  """The latest attempt of every problem, plus that attempt's run count.

  One query for the whole progress bundle (no N+1); ordered by problem_id so the
  bundle is deterministic."""
  return conn.execute(
      """
      SELECT a.*, (SELECT COUNT(*) FROM run WHERE attempt_id = a.id) AS run_count
      FROM attempt a
      WHERE a.id = (SELECT MAX(id) FROM attempt WHERE problem_id = a.problem_id)
      ORDER BY a.problem_id
      """
  ).fetchall()


def run_counts(conn, pid=None):
  """(problem_id, n) for every problem with runs — all attempts, not just the
  latest. Problems with no runs are absent."""
  if pid is None:
    return conn.execute(
        "SELECT problem_id, COUNT(*) AS n FROM run GROUP BY problem_id "
        "ORDER BY problem_id"
    ).fetchall()
  return conn.execute(
      "SELECT problem_id, COUNT(*) AS n FROM run WHERE problem_id = ? "
      "GROUP BY problem_id",
      (pid,),
  ).fetchall()


def latest_attempt_with_run_count(conn, pid):
  return conn.execute(
      """
      SELECT *, (SELECT COUNT(*) FROM run WHERE attempt_id = attempt.id) AS run_count
      FROM attempt WHERE problem_id = ? ORDER BY id DESC LIMIT 1
      """,
      (pid,),
  ).fetchone()


def insert_attempt(conn, pid, ts):
  conn.execute(
      "INSERT INTO attempt (problem_id, started_at, accumulated_ms, running_since) "
      "VALUES (?, ?, 0, ?)",
      (pid, ts, ts),
  )


def pause_attempt(conn, attempt_id, add_ms):
  conn.execute(
      "UPDATE attempt SET accumulated_ms = accumulated_ms + ?, running_since = NULL "
      "WHERE id = ?",
      (add_ms, attempt_id),
  )


def resume_attempt(conn, attempt_id, ts):
  conn.execute("UPDATE attempt SET running_since = ? WHERE id = ?", (ts, attempt_id))


def finalize_solve(conn, attempt_id, ts, elapsed_ms):
  conn.execute(
      "UPDATE attempt SET solved_at = ?, elapsed_ms = ?, running_since = NULL "
      "WHERE id = ?",
      (ts, elapsed_ms, attempt_id),
  )


def insert_run(conn, pid, code, passed, failed, total, duration_ms, all_passed,
               ts, attempt_id):
  cur = conn.execute(
      """
      INSERT INTO run
        (problem_id, code, passed, failed, total, duration_ms, all_passed,
         created_at, attempt_id)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      """,
      (pid, code, passed, failed, total, duration_ms, all_passed, ts, attempt_id),
  )
  return cur.lastrowid


def get_run(conn, run_id):
  return conn.execute("SELECT * FROM run WHERE id = ?", (run_id,)).fetchone()


def list_run_rows(conn, pid, limit):
  return conn.execute(
      "SELECT * FROM run WHERE problem_id = ? ORDER BY created_at DESC, id DESC LIMIT ?",
      (pid, limit),
  ).fetchall()


def solved_attempts(conn, pid=None):
  """Every solved attempt: problem_id, solved_at, elapsed_ms (may be NULL for
  backfilled solves). Ascending by attempt id — the folds over these rows have
  order-dependent tie-breaks, so the ordering is explicit rather than incidental.
  """
  if pid is None:
    return conn.execute(
        "SELECT id, problem_id, solved_at, elapsed_ms FROM attempt "
        "WHERE solved_at IS NOT NULL ORDER BY id"
    ).fetchall()
  return conn.execute(
      "SELECT id, problem_id, solved_at, elapsed_ms FROM attempt "
      "WHERE solved_at IS NOT NULL AND problem_id = ? ORDER BY id",
      (pid,),
  ).fetchall()
