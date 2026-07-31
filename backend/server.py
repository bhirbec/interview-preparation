"""Coding-trainer API.

No auth (single implicit user). Problems live in the `problem` table (populated
by etl.py) and are identified by their path-based id (e.g. "maximum-subarray"
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
      "hint": p["hint"],
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
    drows = db.difficulty_counts(conn)
    trows = db.all_tag_json(conn)

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


@app.get("/api/lessons")
def lessons():
  """Curriculum lessons with derived progress (done once any exercise solved)."""
  with db.connect() as conn:
    rows = db.list_lessons(conn)
    solved = db.ever_solved_problem_ids(conn)
  items = []
  for r in rows:
    exercises = _json_list(r["exercises"])
    solved_count = sum(1 for e in exercises if e in solved)
    items.append({
        "id": r["id"],
        "title": r["title"],
        "topic": r["topic"],
        "position": r["position"],
        "exerciseCount": len(exercises),
        "solvedCount": solved_count,
        "done": solved_count >= 1,
    })
  return {"lessons": items}


@app.get("/api/lesson")
def get_lesson(id: str):
  """A lesson's markdown body + its exercises with per-exercise status."""
  with db.connect() as conn:
    lesson = db.get_lesson_row(conn, id)
    if lesson is None:
      raise HTTPException(status_code=404, detail="lesson not found")
    exercises = _json_list(lesson["exercises"])
    briefs = db.problems_brief(conn, exercises)
    solved = db.ever_solved_problem_ids(conn)
    started = db.started_problem_ids(conn)

  items = []
  for e in exercises:
    b = briefs.get(e)
    if b is None:
      continue  # exercise id no longer in the catalog
    status = "solved" if e in solved else "started" if e in started else "not-started"
    items.append({
        "id": e,
        "title": b["title"],
        "difficulty": b["difficulty"],
        "status": status,
    })
  return {
      "id": lesson["id"],
      "title": lesson["title"],
      "topic": lesson["topic"],
      "body": lesson["body"],
      "exercises": items,
  }


# --- attempts / timing ---


def _now_dt() -> datetime:
  return datetime.now(timezone.utc)


def _delta_ms(iso: str, now: datetime) -> float:
  return (now - datetime.fromisoformat(iso)).total_seconds() * 1000


def _attempt_fields(a) -> dict:
  """Status + timing from the latest attempt.

  `a` is either the latest attempt row, None (no attempt), or a LEFT JOIN row
  whose attempt columns are all NULL — the last two both mean "not-started".
  This is the single source of truth for the derived status; db.STATUS_EXPR
  (used only for SQL filtering) must mirror it.
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

  diffs = [d.strip() for d in difficulty.split(",") if d.strip()]
  taglist = [t.strip() for t in tags.split(",") if t.strip()]

  with db.connect() as conn:
    total, rows = db.query_problem_page(
        conn,
        search=search,
        difficulties=diffs,
        taglist=taglist,
        status=status,
        limit=page_size,
        offset=offset,
    )

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
    p = db.get_problem_row(conn, id)
    if p is None:
      raise HTTPException(status_code=404, detail="problem not found")
    code = db.get_submission_code(conn, id)
    a = db.latest_attempt_with_run_count(conn, id)

  return {
      **_problem_dict(p),
      "code": code,
      "attemptRunCount": a["run_count"] if a else 0,
      **_attempt_fields(a),
  }


@app.post("/api/problem/attempt/start")
def start_attempt(id: str):
  """Start (or Retake) — insert a fresh running attempt."""
  ts = now_iso()
  with db.connect() as conn:
    db.insert_attempt(conn, id, ts)
  return {"ok": True}


@app.post("/api/problem/attempt/pause")
def pause_attempt(id: str):
  with db.connect() as conn:
    a = db.latest_attempt(conn, id)
    if a and a["running_since"] and a["solved_at"] is None:
      add = round(_delta_ms(a["running_since"], _now_dt()))
      db.pause_attempt(conn, a["id"], add)
  return {"ok": True}


@app.post("/api/problem/attempt/resume")
def resume_attempt(id: str):
  with db.connect() as conn:
    a = db.latest_attempt(conn, id)
    if a and a["running_since"] is None and a["solved_at"] is None:
      db.resume_attempt(conn, a["id"], now_iso())
  return {"ok": True}


@app.put("/api/problem/code")
def save_code(payload: CodePayload):
  ts = now_iso()
  with db.connect() as conn:
    db.upsert_submission(conn, payload.id, payload.code, ts)
  return {"ok": True, "updatedAt": ts}


@app.get("/api/problem/runs")
def list_runs(id: str, limit: int = 50):
  with db.connect() as conn:
    rows = db.list_run_rows(conn, id, limit)
  return [_run_dict(r) for r in rows]


@app.post("/api/problem/runs")
def create_run(payload: RunPayload):
  all_passed = 1 if payload.failed == 0 and payload.total > 0 else 0
  ts = now_iso()
  with db.connect() as conn:
    a = db.latest_attempt(conn, payload.id)
    attempt_id = a["id"] if a else None
    run_id = db.insert_run(
        conn, payload.id, payload.code, payload.passed, payload.failed,
        payload.total, payload.durationMs, all_passed, ts, attempt_id,
    )
    # Finalize the solve time on the active attempt.
    if all_passed and a and a["solved_at"] is None:
      extra = round(_delta_ms(a["running_since"], _now_dt())) if a["running_since"] else 0
      db.finalize_solve(conn, a["id"], ts, a["accumulated_ms"] + extra)
    row = db.get_run(conn, run_id)
  return _run_dict(row)
