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
  hint             TEXT,               -- solution hint (the former "Approach")
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

-- Curriculum lessons (populated from lessons/ by build.py). A lesson groups
-- markdown content with an explicit list of exercise problem ids; progress is
-- derived from the attempt table (a lesson is "done" once any exercise has ever
-- been solved).
CREATE TABLE IF NOT EXISTS lesson (
  id        TEXT PRIMARY KEY,
  title     TEXT NOT NULL,
  topic     TEXT,
  body      TEXT,               -- markdown lesson content
  exercises TEXT,               -- JSON array of problem ids
  position  INTEGER
);
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


def _add_problem_hint(conn):
  cols = [r["name"] for r in conn.execute("PRAGMA table_info(problem)").fetchall()]
  if "hint" not in cols:
    conn.execute("ALTER TABLE problem ADD COLUMN hint TEXT")


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
    _add_problem_hint(conn)
    _backfill_solved_attempts(conn)
    conn.execute("DROP TABLE IF EXISTS chapter")  # renamed to lesson


# --- data access -----------------------------------------------------------
# Each function takes an open connection so the caller controls the transaction
# boundary (commit happens when its `with connect()` block exits). Rows are
# returned raw; server.py owns the snake_case→camelCase serialization.

# SQL mirror of server._attempt_fields' status derivation, for the list status
# filter (the latest attempt is joined as `a`). Keep the two in sync.
STATUS_EXPR = """
  CASE
    WHEN a.solved_at IS NOT NULL THEN 'solved'
    WHEN a.id IS NOT NULL THEN 'started'
    ELSE 'not-started'
  END
"""


def get_problem_row(conn, pid):
  return conn.execute("SELECT * FROM problem WHERE id = ?", (pid,)).fetchone()


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


def difficulty_counts(conn):
  return conn.execute(
      "SELECT difficulty, COUNT(*) AS c FROM problem GROUP BY difficulty"
  ).fetchall()


def all_tag_json(conn):
  return conn.execute("SELECT tags FROM problem").fetchall()


def latest_attempt(conn, pid):
  return conn.execute(
      "SELECT * FROM attempt WHERE problem_id = ? ORDER BY id DESC LIMIT 1", (pid,)
  ).fetchone()


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


def query_problem_page(conn, *, search, difficulties, taglist, status, limit, offset):
  """(total, rows) for a filtered catalog page. difficulties/taglist are lists;
  multiple tags are ANDed. status is one of the three states or "" (any)."""
  conds = []
  params = {}

  if search.strip():
    params["like"] = f"%{search.strip().lower()}%"
    conds.append("(lower(p.title) LIKE :like OR lower(p.tags) LIKE :like)")

  if difficulties:
    placeholders = []
    for i, d in enumerate(difficulties):
      params[f"diff{i}"] = d
      placeholders.append(f":diff{i}")
    conds.append(f"p.difficulty IN ({','.join(placeholders)})")

  for i, t in enumerate(taglist):
    params[f"tag{i}"] = f'%"{t}"%'  # tags column is a JSON array of quoted strings
    conds.append(f"p.tags LIKE :tag{i}")

  if status in ("not-started", "started", "solved"):
    conds.append(f"({STATUS_EXPR.strip()}) = :status")
    params["status"] = status

  where = ("WHERE " + " AND ".join(conds)) if conds else ""
  base_from = """
    FROM problem p
    LEFT JOIN attempt a ON a.id = (SELECT MAX(id) FROM attempt WHERE problem_id = p.id)
  """

  total = conn.execute(
      f"SELECT COUNT(*) AS n {base_from} {where}", params
  ).fetchone()["n"]
  rows = conn.execute(
      f"""
      SELECT p.id, p.title, p.difficulty, p.tags,
             a.started_at, a.accumulated_ms, a.running_since,
             a.solved_at, a.elapsed_ms,
             (SELECT COUNT(*) FROM run WHERE attempt_id = a.id) AS attempt_run_count
      {base_from} {where}
      ORDER BY p.position
      LIMIT :limit OFFSET :offset
      """,
      {**params, "limit": limit, "offset": offset},
  ).fetchall()
  return total, rows


# --- curriculum / progress ---


def upsert_lesson(conn, id, title, topic, body, exercises_json, position):
  conn.execute(
      """
      INSERT INTO lesson (id, title, topic, body, exercises, position)
      VALUES (?, ?, ?, ?, ?, ?)
      ON CONFLICT(id) DO UPDATE SET
        title = excluded.title, topic = excluded.topic, body = excluded.body,
        exercises = excluded.exercises, position = excluded.position
      """,
      (id, title, topic, body, exercises_json, position),
  )


def list_lessons(conn):
  return conn.execute("SELECT * FROM lesson ORDER BY position").fetchall()


def get_lesson_row(conn, id):
  return conn.execute("SELECT * FROM lesson WHERE id = ?", (id,)).fetchone()


def ever_solved_problem_ids(conn):
  """Problems solved at least once (a chapter is 'done' once any exercise is
  solved, and a later Retake must not un-complete it)."""
  return {
      r["problem_id"]
      for r in conn.execute(
          "SELECT DISTINCT problem_id FROM attempt WHERE solved_at IS NOT NULL"
      ).fetchall()
  }


def started_problem_ids(conn):
  """Problems whose latest attempt exists but is unsolved (in progress)."""
  return {
      r["problem_id"]
      for r in conn.execute(
          """
          SELECT a.problem_id FROM attempt a
          WHERE a.id = (SELECT MAX(id) FROM attempt WHERE problem_id = a.problem_id)
            AND a.solved_at IS NULL
          """
      ).fetchall()
  }


def problems_brief(conn, ids):
  """id → {title, difficulty} for the given problem ids (missing ids omitted)."""
  if not ids:
    return {}
  placeholders = ",".join("?" for _ in ids)
  rows = conn.execute(
      f"SELECT id, title, difficulty FROM problem WHERE id IN ({placeholders})",
      list(ids),
  ).fetchall()
  return {r["id"]: {"title": r["title"], "difficulty": r["difficulty"]} for r in rows}
