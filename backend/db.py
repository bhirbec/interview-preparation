"""SQLite storage for the coding-trainer API.

Four tables, keyed by the problem slug (a stable id, so build.py never changes):
  - problem:    the imported catalog (definition + starter/solution/tests).
  - submission: the latest autosaved implementation per problem.
  - run:        one row per test run (result + the code that produced it).
  - attempt:    a log of timed attempts; the latest one drives a problem's status.
"""

import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.environ.get(
    "DB_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "trainer.db")
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS problem (
  id               TEXT PRIMARY KEY,   -- path relative to coding-questions/, e.g. CTCI/1.1-is-unique
  title            TEXT NOT NULL,
  difficulty       TEXT,
  tags             TEXT,               -- JSON array
  sources          TEXT,               -- JSON array
  description      TEXT,
  primary_function TEXT,
  starter          TEXT,
  solution         TEXT,
  tests            TEXT,
  position         INTEGER
);

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
