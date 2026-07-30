"""Coding-trainer API.

No auth (single implicit user). Problems live in the `problem` table (populated
by build.py) and are identified by their path-based id (e.g. "maximum-subarray"
or "CTCI/1.1-is-unique"). Ids can contain "/", so id-specific endpoints take the
id as a query parameter or request-body field rather than a path segment.
"""

import json
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import db
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(_app: FastAPI):
  db.init_db()
  yield


app = FastAPI(title="Coding Trainer API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def now_iso() -> str:
  return datetime.now(timezone.utc).isoformat()


class CodePayload(BaseModel):
  id: str
  code: str


class RunPayload(BaseModel):
  id: str
  code: str
  passed: int
  failed: int
  total: int
  durationMs: float


def _json_list(s) -> list:
  """Parse a JSON-array text column (tags/sources), tolerating NULL/empty."""
  return json.loads(s or "[]")


def _run_dict(r) -> dict:
  return {
      "id": r["id"],
      "problemId": r["problem_id"],
      "passed": r["passed"],
      "failed": r["failed"],
      "total": r["total"],
      "durationMs": r["duration_ms"],
      "allPassed": bool(r["all_passed"]),
      "createdAt": r["created_at"],
      "code": r["code"],
  }


def _problem_dict(p) -> dict:
  """Static problem definition → JSON (snake_case columns → camelCase keys).

  Timing/status (see _attempt_fields) and the saved `code` are added by callers.
  """
  return {
      "id": p["id"],
      "title": p["title"],
      "difficulty": p["difficulty"],
      "tags": _json_list(p["tags"]),
      "sources": _json_list(p["sources"]),
      "description": p["description"],
      "primaryFunction": p["primary_function"],
      "starter": p["starter"],
      "solution": p["solution"],
      "tests": p["tests"],
  }


@app.get("/api/health")
def health():
  return {"ok": True}


@app.get("/api/facets")
def facets():
  """Available filter values (with counts) for the list sidebar."""
  order = {"easy": 0, "medium": 1, "hard": 2}
  with db.connect() as conn:
    drows = conn.execute(
        "SELECT difficulty, COUNT(*) AS c FROM problem GROUP BY difficulty"
    ).fetchall()
    trows = conn.execute("SELECT tags FROM problem").fetchall()

  difficulties = sorted(
      [{"value": r["difficulty"], "count": r["c"]} for r in drows if r["difficulty"]],
      key=lambda d: order.get(d["value"], 99),
  )
  counter = {}
  for r in trows:
    for t in _json_list(r["tags"]):
      counter[t] = counter.get(t, 0) + 1
  tags = [
      {"value": k, "count": v}
      for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
  ]
  return {"difficulties": difficulties, "tags": tags}


# --- attempts / timing ---


def _now_dt() -> datetime:
  return datetime.now(timezone.utc)


def _delta_ms(iso: str, now: datetime) -> float:
  return (now - datetime.fromisoformat(iso)).total_seconds() * 1000


def _latest_attempt(conn, pid):
  return conn.execute(
      "SELECT * FROM attempt WHERE problem_id = ? ORDER BY id DESC LIMIT 1", (pid,)
  ).fetchone()


def _attempt_fields(a) -> dict:
  """Status + timing from the latest attempt.

  `a` is either the latest attempt row, None (no attempt), or a LEFT JOIN row
  whose attempt columns are all NULL — the last two both mean "not-started".
  This is the single source of truth for the derived status; STATUS_EXPR (used
  only for SQL filtering) must mirror it.
  """
  if a is None or a["started_at"] is None:
    return {
        "status": "not-started",
        "startedAt": None,
        "accumulatedMs": 0,
        "runningSince": None,
        "solvedAt": None,
        "elapsedMs": None,
    }
  return {
      "status": "solved" if a["solved_at"] else "started",
      "startedAt": a["started_at"],
      "accumulatedMs": a["accumulated_ms"],
      "runningSince": a["running_since"],
      "solvedAt": a["solved_at"],
      "elapsedMs": a["elapsed_ms"],
  }


# SQL mirror of _attempt_fields' status derivation, for the list WHERE filter
# (the latest attempt is joined as `a`). Keep in sync with _attempt_fields.
STATUS_EXPR = """
  CASE
    WHEN a.solved_at IS NOT NULL THEN 'solved'
    WHEN a.id IS NOT NULL THEN 'started'
    ELSE 'not-started'
  END
"""


@app.get("/api/problems")
def list_problems(
    search: str = "",
    difficulty: str = "",
    tags: str = "",
    status: str = "",
    page: int = 1,
    pageSize: int = 20,
):
  """Paginated, filterable problem list for the catalog view.

  difficulty/tags are comma-separated. Multiple tags are ANDed (a problem must
  carry all of them). status is "not-started" | "started" | "solved" | "" (any).
  """
  page = max(1, page)
  page_size = max(1, min(100, pageSize))
  offset = (page - 1) * page_size

  conds = []
  params = {}

  if search.strip():
    params["like"] = f"%{search.strip().lower()}%"
    conds.append("(lower(p.title) LIKE :like OR lower(p.tags) LIKE :like)")

  diffs = [d.strip() for d in difficulty.split(",") if d.strip()]
  if diffs:
    placeholders = []
    for i, d in enumerate(diffs):
      params[f"diff{i}"] = d
      placeholders.append(f":diff{i}")
    conds.append(f"p.difficulty IN ({','.join(placeholders)})")

  taglist = [t.strip() for t in tags.split(",") if t.strip()]
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

  with db.connect() as conn:
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
        {**params, "limit": page_size, "offset": offset},
    ).fetchall()

  items = [
      {
          "id": r["id"],
          "title": r["title"],
          "difficulty": r["difficulty"],
          "tags": _json_list(r["tags"]),
          "attemptRunCount": r["attempt_run_count"] or 0,
          **_attempt_fields(r),
      }
      for r in rows
  ]
  return {"items": items, "total": total, "page": page, "pageSize": page_size}


@app.get("/api/problem")
def get_problem(id: str):
  """Full problem definition + saved code + latest-attempt status/timing."""
  with db.connect() as conn:
    p = conn.execute("SELECT * FROM problem WHERE id = ?", (id,)).fetchone()
    if p is None:
      raise HTTPException(status_code=404, detail="problem not found")
    sub = conn.execute(
        "SELECT code FROM submission WHERE problem_id = ?", (id,)
    ).fetchone()
    a = conn.execute(
        """
        SELECT *, (SELECT COUNT(*) FROM run WHERE attempt_id = attempt.id) AS run_count
        FROM attempt WHERE problem_id = ? ORDER BY id DESC LIMIT 1
        """,
        (id,),
    ).fetchone()

  return {
      **_problem_dict(p),
      "code": sub["code"] if sub else None,
      "attemptRunCount": a["run_count"] if a else 0,
      **_attempt_fields(a),
  }


@app.post("/api/problem/attempt/start")
def start_attempt(id: str):
  """Start (or Retake) — insert a fresh running attempt."""
  ts = now_iso()
  with db.connect() as conn:
    conn.execute(
        "INSERT INTO attempt (problem_id, started_at, accumulated_ms, running_since) "
        "VALUES (?, ?, 0, ?)",
        (id, ts, ts),
    )
  return {"ok": True}


@app.post("/api/problem/attempt/pause")
def pause_attempt(id: str):
  with db.connect() as conn:
    a = _latest_attempt(conn, id)
    if a and a["running_since"] and a["solved_at"] is None:
      add = round(_delta_ms(a["running_since"], _now_dt()))
      conn.execute(
          "UPDATE attempt SET accumulated_ms = accumulated_ms + ?, running_since = NULL "
          "WHERE id = ?",
          (add, a["id"]),
      )
  return {"ok": True}


@app.post("/api/problem/attempt/resume")
def resume_attempt(id: str):
  with db.connect() as conn:
    a = _latest_attempt(conn, id)
    if a and a["running_since"] is None and a["solved_at"] is None:
      conn.execute(
          "UPDATE attempt SET running_since = ? WHERE id = ?", (now_iso(), a["id"])
      )
  return {"ok": True}


@app.put("/api/problem/code")
def save_code(payload: CodePayload):
  ts = now_iso()
  with db.connect() as conn:
    conn.execute(
        """
        INSERT INTO submission (problem_id, code, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(problem_id)
        DO UPDATE SET code = excluded.code, updated_at = excluded.updated_at
        """,
        (payload.id, payload.code, ts),
    )
  return {"ok": True, "updatedAt": ts}


@app.get("/api/problem/runs")
def list_runs(id: str, limit: int = 50):
  with db.connect() as conn:
    rows = conn.execute(
        """
        SELECT * FROM run
        WHERE problem_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (id, limit),
    ).fetchall()
  return [_run_dict(r) for r in rows]


@app.post("/api/problem/runs")
def create_run(payload: RunPayload):
  all_passed = 1 if payload.failed == 0 and payload.total > 0 else 0
  ts = now_iso()
  with db.connect() as conn:
    a = _latest_attempt(conn, payload.id)
    attempt_id = a["id"] if a else None
    cur = conn.execute(
        """
        INSERT INTO run
          (problem_id, code, passed, failed, total, duration_ms, all_passed,
           created_at, attempt_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (payload.id, payload.code, payload.passed, payload.failed, payload.total,
         payload.durationMs, all_passed, ts, attempt_id),
    )
    # Finalize the solve time on the active attempt.
    if all_passed and a and a["solved_at"] is None:
      extra = round(_delta_ms(a["running_since"], _now_dt())) if a["running_since"] else 0
      conn.execute(
          "UPDATE attempt SET solved_at = ?, elapsed_ms = ?, running_since = NULL "
          "WHERE id = ?",
          (ts, a["accumulated_ms"] + extra, a["id"]),
      )
    row = conn.execute("SELECT * FROM run WHERE id = ?", (cur.lastrowid,)).fetchone()
  return _run_dict(row)
