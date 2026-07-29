"""Coding-trainer API.

No auth (single implicit user). Problems are identified by their slug, which is
stable and comes straight from build.py's problems.json — so this API never has
to know anything about the catalog itself.
"""

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

# No auth; allow any origin (the frontend normally reaches us via a same-origin
# Vite proxy, but this keeps direct access working too).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def now_iso() -> str:
  return datetime.now(timezone.utc).isoformat()


class CodePayload(BaseModel):
  code: str


class RunPayload(BaseModel):
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


@app.get("/api/summary")
def summary():
  """Per-problem aggregate for the list view."""
  with db.connect() as conn:
    rows = conn.execute(
        """
        SELECT problem_id,
               COUNT(*) AS runs,
               MAX(CASE WHEN all_passed = 1 THEN created_at END) AS last_all_passed_at
        FROM run
        GROUP BY problem_id
        """
    ).fetchall()
  return {
      r["problem_id"]: {
          "runCount": r["runs"],
          "lastAllPassedAt": r["last_all_passed_at"],
      }
      for r in rows
  }


@app.get("/api/problems/{pid}")
def get_problem(pid: str):
  """Saved code + status for one problem."""
  with db.connect() as conn:
    sub = conn.execute(
        "SELECT code, updated_at FROM submission WHERE problem_id = ?", (pid,)
    ).fetchone()
    agg = conn.execute(
        """
        SELECT COUNT(*) AS runs,
               MAX(CASE WHEN all_passed = 1 THEN created_at END) AS last
        FROM run WHERE problem_id = ?
        """,
        (pid,),
    ).fetchone()
  return {
      "code": sub["code"] if sub else None,
      "updatedAt": sub["updated_at"] if sub else None,
      "runCount": agg["runs"] or 0,
      "lastAllPassedAt": agg["last"],
  }


@app.put("/api/problems/{pid}/code")
def save_code(pid: str, payload: CodePayload):
  ts = now_iso()
  with db.connect() as conn:
    conn.execute(
        """
        INSERT INTO submission (problem_id, code, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(problem_id)
        DO UPDATE SET code = excluded.code, updated_at = excluded.updated_at
        """,
        (pid, payload.code, ts),
    )
  return {"ok": True, "updatedAt": ts}


@app.get("/api/problems/{pid}/runs")
def list_runs(pid: str, limit: int = 50):
  with db.connect() as conn:
    rows = conn.execute(
        """
        SELECT * FROM run
        WHERE problem_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (pid, limit),
    ).fetchall()
  return [_run_dict(r) for r in rows]


@app.post("/api/problems/{pid}/runs")
def create_run(pid: str, payload: RunPayload):
  all_passed = 1 if payload.failed == 0 and payload.total > 0 else 0
  ts = now_iso()
  with db.connect() as conn:
    cur = conn.execute(
        """
        INSERT INTO run
          (problem_id, code, passed, failed, total, duration_ms, all_passed, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (pid, payload.code, payload.passed, payload.failed, payload.total,
         payload.durationMs, all_passed, ts),
    )
    row = conn.execute("SELECT * FROM run WHERE id = ?", (cur.lastrowid,)).fetchone()
  return _run_dict(row)
