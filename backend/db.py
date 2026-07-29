"""SQLite storage for the coding-trainer API.

Two tables, keyed by the problem slug (a stable id, so build.py never changes):
  - submission: the latest autosaved implementation per problem.
  - run:        one row per test run (result + the code that produced it).
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
  created_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_run_problem ON run (problem_id, created_at DESC);
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


def init_db():
  with connect() as conn:
    conn.executescript(SCHEMA)
