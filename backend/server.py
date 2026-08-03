"""Coding-trainer API.

No auth (single implicit user). Problems live in the `problem` table (populated
by etl.py) and are identified by their path-based id (e.g. "maximum-subarray"
or "CTCI/1.1-is-unique"). Ids can contain "/", so id-specific endpoints take the
id as a query parameter or request-body field rather than a path segment.
"""

import json
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta, timezone

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


_DIFF_ORDER = {"easy": 0, "medium": 1, "hard": 2}


def _time_stats(values: list) -> dict:
  return {
      "avgMs": round(sum(values) / len(values)) if values else None,
      "bestMs": min(values) if values else None,
      "count": len(values),
  }


def _streaks(day_set) -> dict:
  """Longest run of consecutive days, and the run ending on the latest solve day."""
  if not day_set:
    return {"current": 0, "longest": 0}
  days = sorted(day_set)
  longest = run = 1
  for i in range(1, len(days)):
    run = run + 1 if days[i] - days[i - 1] == timedelta(days=1) else 1
    longest = max(longest, run)
  current = 1
  for i in range(len(days) - 1, 0, -1):
    if days[i] - days[i - 1] == timedelta(days=1):
      current += 1
    else:
      break
  return {"current": current, "longest": longest}


@app.get("/api/stats")
def stats():
  """Training metrics aggregated from problem + attempt + run (no new tracking)."""
  with db.connect() as conn:
    problems = db.all_problem_meta(conn)
    solved_rows = db.solved_attempts(conn)
    total_runs = db.count_runs(conn)
    started = db.started_problem_ids(conn)
    started_briefs = db.problems_brief(conn, started)

  # problem metadata + totals
  meta = {}
  diff_total, tag_total = {}, {}
  for p in problems:
    tags = _json_list(p["tags"])
    meta[p["id"]] = {"title": p["title"], "difficulty": p["difficulty"], "tags": tags}
    diff_total[p["difficulty"]] = diff_total.get(p["difficulty"], 0) + 1
    for t in tags:
      tag_total[t] = tag_total.get(t, 0) + 1

  # fold the solved attempts
  best_elapsed = {}     # problem -> min timed elapsed_ms
  latest_solved = {}    # problem -> (solved_at, elapsed_ms) at max solved_at
  day_problems = {}     # 'YYYY-MM-DD' -> set(problem)
  for r in solved_rows:
    pid = r["problem_id"]
    if pid not in meta:
      continue  # solved a problem no longer in the catalog
    e, sa = r["elapsed_ms"], r["solved_at"]
    if e is not None and e < best_elapsed.get(pid, float("inf")):
      best_elapsed[pid] = e
    if pid not in latest_solved or sa > latest_solved[pid][0]:
      latest_solved[pid] = (sa, e)
    day_problems.setdefault(sa[:10], set()).add(pid)

  solved_ids = set(latest_solved)

  def diff_key(d):
    return _DIFF_ORDER.get(d, 99)

  diff_solved = {}
  tag_solved = {}
  for pid in solved_ids:
    diff_solved[meta[pid]["difficulty"]] = diff_solved.get(meta[pid]["difficulty"], 0) + 1
    for t in meta[pid]["tags"]:
      tag_solved[t] = tag_solved.get(t, 0) + 1

  by_difficulty = [
      {"difficulty": d, "solved": diff_solved.get(d, 0), "total": diff_total[d]}
      for d in sorted(diff_total, key=diff_key)
  ]
  top_tags = sorted(tag_total.items(), key=lambda kv: (-kv[1], kv[0]))[:12]
  by_tag = [{"tag": t, "solved": tag_solved.get(t, 0), "total": n} for t, n in top_tags]

  diff_vals = {}
  for pid, e in best_elapsed.items():
    diff_vals.setdefault(meta[pid]["difficulty"], []).append(e)
  solve_time = {
      "overall": _time_stats(list(best_elapsed.values())),
      "byDifficulty": [
          {"difficulty": d, **_time_stats(diff_vals.get(d, []))}
          for d in sorted(diff_vals, key=diff_key)
      ],
  }

  fastest = [
      {"id": pid, "title": meta[pid]["title"],
       "difficulty": meta[pid]["difficulty"], "elapsedMs": e}
      for pid, e in sorted(best_elapsed.items(), key=lambda kv: kv[1])[:5]
  ]
  recent = [
      {"id": pid, "title": meta[pid]["title"], "difficulty": meta[pid]["difficulty"],
       "solvedAt": sa, "elapsedMs": e}
      for pid, (sa, e) in sorted(latest_solved.items(), key=lambda kv: kv[1][0], reverse=True)[:6]
  ]
  in_progress = [
      {"id": pid, "title": b["title"], "difficulty": b["difficulty"]}
      for pid, b in sorted(started_briefs.items())
  ]

  return {
      "solvedCount": len(solved_ids),
      "totalProblems": len(problems),
      "totalRuns": total_runs,
      "totalTimeMs": sum(best_elapsed.values()),
      "streak": _streaks({date.fromisoformat(d) for d in day_problems}),
      "byDifficulty": by_difficulty,
      "byTag": by_tag,
      "solveTime": solve_time,
      "fastest": fastest,
      "daily": [{"date": d, "count": len(s)} for d, s in sorted(day_problems.items())],
      "recent": recent,
      "inProgress": in_progress,
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


# --- user state (the only thing still in SQLite) ---


def _progress_entry(pid, a, attempt_run_count, run_count, solves) -> dict:
  """One problem's dynamic state. The client joins this onto the static catalog.

  `solves` is EVERY solved attempt (ascending), not just the latest: the stats
  minimum-elapsed fold, the stats per-day sets and lesson "ever solved" all need
  more than the latest attempt (after a Retake the latest attempt is unsolved,
  but the lesson must stay complete). Each solve carries its attempt id so the
  client can restore db.solved_attempts' global "ORDER BY id" across problems —
  the folds' tie-breaks depend on that row order.
  """
  return {
      "id": pid,
      **_attempt_fields(a),
      "attemptRunCount": attempt_run_count,
      "runCount": run_count,
      "solves": solves,
  }


def _solves_by_problem(rows) -> dict:
  by_id = {}
  for r in rows:
    by_id.setdefault(r["problem_id"], []).append(
        {"attemptId": r["id"], "solvedAt": r["solved_at"], "elapsedMs": r["elapsed_ms"]}
    )
  return by_id


@app.get("/api/progress")
def progress():
  """Every problem's dynamic state, in one bundle (three queries, no N+1).

  Includes problems that have runs but no attempt rows, so the client's sum of
  runCount matches SELECT COUNT(*) FROM run, and ids that are no longer in the
  catalog — both are deliberate.
  """
  with db.connect() as conn:
    attempts = db.latest_attempts(conn)
    counts = db.run_counts(conn)
    solves = _solves_by_problem(db.solved_attempts(conn))

  run_counts = {r["problem_id"]: r["n"] for r in counts}
  seen = {a["problem_id"] for a in attempts}
  items = [
      _progress_entry(a["problem_id"], a, a["run_count"],
                      run_counts.get(a["problem_id"], 0),
                      solves.get(a["problem_id"], []))
      for a in attempts
  ]
  items += [
      _progress_entry(pid, None, 0, n, solves.get(pid, []))
      for pid, n in run_counts.items() if pid not in seen
  ]
  return {"problems": items}


@app.get("/api/problem/state")
def problem_state(id: str):
  """One problem's dynamic state + its saved code.

  Never 404s: whether an id exists is now a *content* question, answered by
  catalog.json. An unknown id is simply not-started with no code.
  """
  with db.connect() as conn:
    a = db.latest_attempt_with_run_count(conn, id)
    counts = db.run_counts(conn, id)
    solves = _solves_by_problem(db.solved_attempts(conn, id))
    code = db.get_submission_code(conn, id)

  entry = _progress_entry(
      id, a, a["run_count"] if a else 0,
      counts[0]["n"] if counts else 0, solves.get(id, []),
  )
  return {**entry, "code": code}


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
