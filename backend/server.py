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
from fastapi import FastAPI
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


@app.get("/api/health")
def health():
  return {"ok": True}


@app.get("/api/problems")
def list_problems(search: str = "", page: int = 1, pageSize: int = 20):
  """Paginated, searchable problem list for the catalog view."""
  page = max(1, page)
  page_size = max(1, min(100, pageSize))
  offset = (page - 1) * page_size
  like = f"%{search.strip().lower()}%"
  where = "WHERE lower(p.title) LIKE :like OR lower(p.tags) LIKE :like" if search.strip() else ""

  with db.connect() as conn:
    total = conn.execute(
        f"SELECT COUNT(*) AS n FROM problem p {where}", {"like": like}
    ).fetchone()["n"]
    rows = conn.execute(
        f"""
        SELECT p.id, p.title, p.difficulty, p.tags,
               r.last_all_passed_at
        FROM problem p
        LEFT JOIN (
          SELECT problem_id,
                 MAX(CASE WHEN all_passed = 1 THEN created_at END) AS last_all_passed_at
          FROM run GROUP BY problem_id
        ) r ON r.problem_id = p.id
        {where}
        ORDER BY p.position
        LIMIT :limit OFFSET :offset
        """,
        {"like": like, "limit": page_size, "offset": offset},
    ).fetchall()

  items = [
      {
          "id": r["id"],
          "title": r["title"],
          "difficulty": r["difficulty"],
          "tags": json.loads(r["tags"] or "[]"),
          "lastAllPassedAt": r["last_all_passed_at"],
      }
      for r in rows
  ]
  return {"items": items, "total": total, "page": page, "pageSize": page_size}


@app.get("/api/problem")
def get_problem(id: str):
  """Full problem definition + saved code + status."""
  with db.connect() as conn:
    p = conn.execute("SELECT * FROM problem WHERE id = ?", (id,)).fetchone()
    if p is None:
      return {"error": "not found"}
    sub = conn.execute(
        "SELECT code FROM submission WHERE problem_id = ?", (id,)
    ).fetchone()
    agg = conn.execute(
        """
        SELECT COUNT(*) AS runs,
               MAX(CASE WHEN all_passed = 1 THEN created_at END) AS last
        FROM run WHERE problem_id = ?
        """,
        (id,),
    ).fetchone()

  return {
      "id": p["id"],
      "title": p["title"],
      "difficulty": p["difficulty"],
      "tags": json.loads(p["tags"] or "[]"),
      "sources": json.loads(p["sources"] or "[]"),
      "description": p["description"],
      "primaryFunction": p["primary_function"],
      "starter": p["starter"],
      "solution": p["solution"],
      "tests": p["tests"],
      "code": sub["code"] if sub else None,
      "runCount": agg["runs"] or 0,
      "lastAllPassedAt": agg["last"],
  }


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
    cur = conn.execute(
        """
        INSERT INTO run
          (problem_id, code, passed, failed, total, duration_ms, all_passed, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (payload.id, payload.code, payload.passed, payload.failed, payload.total,
         payload.durationMs, all_passed, ts),
    )
    row = conn.execute("SELECT * FROM run WHERE id = ?", (cur.lastrowid,)).fetchone()
  return _run_dict(row)
