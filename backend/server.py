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
    for t in json.loads(r["tags"] or "[]"):
      counter[t] = counter.get(t, 0) + 1
  tags = [
      {"value": k, "count": v}
      for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
  ]
  return {"difficulties": difficulties, "tags": tags}


# A problem is: solved (has an all-passing run), started (edited code that
# differs from the starter, or at least one run), or not-started.
STATUS_EXPR = """
  CASE
    WHEN r.last_all_passed_at IS NOT NULL THEN 'solved'
    WHEN (s.code IS NOT NULL AND s.code <> p.starter) OR COALESCE(r.runs, 0) > 0
      THEN 'started'
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
    LEFT JOIN submission s ON s.problem_id = p.id
    LEFT JOIN (
      SELECT problem_id,
             COUNT(*) AS runs,
             MAX(created_at) AS last_run_at,
             MAX(CASE WHEN all_passed = 1 THEN created_at END) AS last_all_passed_at
      FROM run GROUP BY problem_id
    ) r ON r.problem_id = p.id
  """

  with db.connect() as conn:
    total = conn.execute(
        f"SELECT COUNT(*) AS n {base_from} {where}", params
    ).fetchone()["n"]
    rows = conn.execute(
        f"""
        SELECT p.id, p.title, p.difficulty, p.tags,
               r.last_all_passed_at,
               COALESCE(s.updated_at, r.last_run_at) AS last_activity_at,
               {STATUS_EXPR} AS status
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
          "tags": json.loads(r["tags"] or "[]"),
          "status": r["status"],
          "lastAllPassedAt": r["last_all_passed_at"],
          "lastActivityAt": r["last_activity_at"],
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
