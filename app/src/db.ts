// The client-side database: SQLite (sql.js, compiled to WASM) held in memory,
// holding an *index* over the static content plus the user's progress.
//
// Why a database at all: the catalog filters, the curriculum roll-ups and the
// stats aggregation read far better as SQL than as imperative folds, and a new
// filter or metric becomes a query change rather than a new accumulator.
//
// Two rules shape everything below:
//
//   - It holds the index, NOT the content. Descriptions, starter/solution/test
//     code and lesson markdown are fetched as plain JSON (content.ts) and never
//     queried, so they never enter a table.
//   - In-memory only, no persistence. The whole thing is derived from data we
//     already fetch, so persisting it would only buy an invalidation problem;
//     populating 133 problems inside a transaction takes microseconds.
//
// Initialization is async (WASM instantiation) but every query after it is
// synchronous, which is why sql.js was chosen over the official
// @sqlite.org/sqlite-wasm build: filtering stays inside a synchronous useMemo
// with no async races on keystrokes.
import initSqlJs, { type Database, type SqlValue } from 'sql.js'
import type {
  Catalog,
  DifficultyTimeStat,
  Facets,
  LessonDetail,
  LessonsContent,
  LessonsResponse,
  ProblemPage,
  ProblemStatus,
  ProgressEntry,
  StatsResponse,
  StatusFilter,
  TimeStat,
} from './types'
import { api } from './api'
import { loadCatalog, loadLessons } from './content'

// Copied out of node_modules into public/ (see README) so the bundle is
// self-contained.
const WASM_URL = '/sql-wasm.wasm'

const SCHEMA = `
-- Content: built once, when catalog.json and lessons.json land.
CREATE TABLE problem (
  id         TEXT PRIMARY KEY,
  title      TEXT NOT NULL,
  difficulty TEXT,
  position   INTEGER NOT NULL
);

-- Tag order within a problem is the catalog's (rowid order); the list renders
-- them in that order, so nothing here may reorder the insert.
CREATE TABLE problem_tag (
  problem_id TEXT NOT NULL,
  tag        TEXT NOT NULL,
  PRIMARY KEY (problem_id, tag)
);

CREATE TABLE lesson (
  id       TEXT PRIMARY KEY,
  title    TEXT NOT NULL,
  topic    TEXT,
  position INTEGER NOT NULL
);

-- problem_id is deliberately NOT a foreign key: a lesson may reference an id
-- that has left the catalog, and such an exercise still COUNTS toward
-- exerciseCount while being dropped from the displayed list. A FK would make
-- that unrepresentable.
CREATE TABLE lesson_exercise (
  lesson_id  TEXT NOT NULL,
  problem_id TEXT NOT NULL,
  ord        INTEGER NOT NULL,
  PRIMARY KEY (lesson_id, problem_id)
);

-- Dynamic: rebuilt on every /api/progress fetch.
CREATE TABLE progress (
  problem_id        TEXT PRIMARY KEY,
  status            TEXT NOT NULL,   -- latest attempt only
  started_at        TEXT,
  accumulated_ms    INTEGER,
  running_since     TEXT,
  solved_at         TEXT,
  elapsed_ms        INTEGER,
  attempt_run_count INTEGER NOT NULL DEFAULT 0,
  run_count         INTEGER NOT NULL DEFAULT 0
);

-- Kept separate from progress so "ever solved" (EXISTS over this table) stays
-- distinct from "the latest attempt is solved" (progress.status). That
-- distinction is the whole Retake rule; do not collapse the two.
CREATE TABLE solve (
  problem_id TEXT NOT NULL,
  seq        INTEGER NOT NULL,  -- ascending attempt order, for deterministic tie-breaks
  solved_at  TEXT NOT NULL,
  day        TEXT NOT NULL,     -- substr(solved_at, 1, 10), UTC, computed at insert
  elapsed_ms INTEGER,           -- nullable: backfilled solves have no timing
  PRIMARY KEY (problem_id, seq)
);

CREATE INDEX idx_problem_position ON problem (position);
CREATE INDEX idx_problem_tag_tag ON problem_tag (tag);
CREATE INDEX idx_solve_day ON solve (day);
`

// easy < medium < hard < anything else, mirroring server._DIFF_ORDER. The
// trailing name keeps ties (an unknown difficulty) explicitly ordered rather
// than at SQLite's discretion.
const DIFF_ORDER = `
  CASE difficulty WHEN 'easy' THEN 0 WHEN 'medium' THEN 1 WHEN 'hard' THEN 2 ELSE 99 END,
  difficulty
`

let handle: Database | null = null
let lessonBodies = new Map<string, string>()

function db(): Database {
  if (!handle) throw new Error('db.ts: ensureDb() has not resolved yet')
  return handle
}

// --- query helpers ----------------------------------------------------------

type Row = Record<string, SqlValue>

function all(sql: string, params: SqlValue[] = []): Row[] {
  const stmt = db().prepare(sql)
  try {
    stmt.bind(params)
    const rows: Row[] = []
    while (stmt.step()) rows.push(stmt.getAsObject())
    return rows
  } finally {
    stmt.free()
  }
}

function one(sql: string, params: SqlValue[] = []): Row | null {
  return all(sql, params)[0] ?? null
}

// SQLite is dynamically typed and a missing row reads as undefined, so every
// column goes through one of these on its way into a view model.
function num(v: SqlValue | undefined): number {
  return typeof v === 'number' ? v : 0
}

function nullableNum(v: SqlValue | undefined): number | null {
  return typeof v === 'number' ? v : null
}

function str(v: SqlValue | undefined): string {
  return typeof v === 'string' ? v : ''
}

function nullableStr(v: SqlValue | undefined): string | null {
  return typeof v === 'string' ? v : null
}

// Tags are concatenated with a newline (no tag can contain one) so a single
// query can return a problem and its tags in catalog order.
const TAGS_EXPR = `
  (SELECT group_concat(pt.tag, char(10) ORDER BY pt.rowid)
     FROM problem_tag pt WHERE pt.problem_id = p.id)
`

function splitTags(v: SqlValue): string[] {
  return typeof v === 'string' && v ? v.split('\n') : []
}

// Python's round() is half-to-even; SQLite's ROUND() is half-away-from-zero.
// The averages below therefore select SUM and COUNT and divide here.
function pyRound(x: number): number {
  const floor = Math.floor(x)
  const frac = x - floor
  if (frac > 0.5) return floor + 1
  if (frac < 0.5) return floor
  return floor % 2 === 0 ? floor : floor + 1
}

// --- initialization ---------------------------------------------------------

let ready: Promise<void> | null = null

// Memoized: instantiate the WASM, create the schema, then load the static
// content. Hooks await this once and query synchronously afterwards.
export function ensureDb(): Promise<void> {
  if (!ready) {
    const p = (async () => {
      // The wasm is vendored in public/ and served from our own origin, never
      // a CDN — this app is meant to be a self-contained static bundle.
      const SQL = await initSqlJs({ locateFile: () => WASM_URL })
      const [catalog, lessons] = await Promise.all([loadCatalog(), loadLessons()])
      const fresh = new SQL.Database()
      fresh.run(SCHEMA)
      handle = fresh
      loadContent(catalog, lessons)
    })()
    ready = p
    p.catch(() => {
      if (ready === p) ready = null
    })
  }
  return ready
}

function loadContent(catalog: Catalog, lessons: LessonsContent): void {
  const conn = db()
  conn.run('BEGIN')
  try {
    const problem = conn.prepare(
      'INSERT INTO problem (id, title, difficulty, position) VALUES (?, ?, ?, ?)',
    )
    const tag = conn.prepare(
      'INSERT OR IGNORE INTO problem_tag (problem_id, tag) VALUES (?, ?)',
    )
    for (const p of catalog.problems) {
      problem.run([p.id, p.title, p.difficulty, p.position])
      for (const t of p.tags) tag.run([p.id, t])
    }
    problem.free()
    tag.free()

    const lesson = conn.prepare(
      'INSERT INTO lesson (id, title, topic, position) VALUES (?, ?, ?, ?)',
    )
    const exercise = conn.prepare(
      'INSERT OR IGNORE INTO lesson_exercise (lesson_id, problem_id, ord) VALUES (?, ?, ?)',
    )
    lessonBodies = new Map()
    for (const l of lessons.lessons) {
      lesson.run([l.id, l.title, l.topic, l.position])
      l.exercises.forEach((pid, ord) => exercise.run([l.id, pid, ord]))
      lessonBodies.set(l.id, l.body)
    }
    lesson.free()
    exercise.free()
    conn.run('COMMIT')
  } catch (e) {
    conn.run('ROLLBACK')
    throw e
  }
}

// Rebuild the dynamic tables from a /api/progress bundle. THIS IS THE ONE
// SYNCHRONIZATION POINT of the whole design: after any run, attempt
// start/pause/resume or Retake, this must run before the UI re-queries, or the
// page renders stale state.
export function loadProgress(entries: ProgressEntry[]): void {
  const conn = db()
  conn.run('BEGIN')
  try {
    conn.run('DELETE FROM progress')
    conn.run('DELETE FROM solve')
    const progress = conn.prepare(`
      INSERT INTO progress
        (problem_id, status, started_at, accumulated_ms, running_since,
         solved_at, elapsed_ms, attempt_run_count, run_count)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `)
    const solve = conn.prepare(
      'INSERT INTO solve (problem_id, seq, solved_at, day, elapsed_ms) VALUES (?, ?, ?, ?, ?)',
    )
    for (const e of entries) {
      progress.run([
        e.id, e.status, e.startedAt, e.accumulatedMs, e.runningSince,
        e.solvedAt, e.elapsedMs, e.attemptRunCount, e.runCount,
      ])
      e.solves.forEach((s, seq) =>
        solve.run([e.id, seq, s.solvedAt, s.solvedAt.slice(0, 10), s.elapsedMs]),
      )
    }
    progress.free()
    solve.free()
    conn.run('COMMIT')
  } catch (e) {
    conn.run('ROLLBACK')
    throw e
  }
}

// Fetch the progress bundle and rebuild the dynamic tables, initializing the
// database on the way if needed. Every page that renders user state calls this
// on mount and after any mutation.
export async function syncProgress(): Promise<void> {
  const [bundle] = await Promise.all([api.getProgress(), ensureDb()])
  loadProgress(bundle.problems)
}

// --- catalog list -----------------------------------------------------------

export interface ProblemQuery {
  search: string
  difficulty: string[]
  tags: string[]
  status: StatusFilter | string
  page: number
  pageSize: number
}

function placeholders(values: readonly unknown[]): string {
  return values.map(() => '?').join(',')
}

/** The filtered, ordered, paginated catalog page (mirrors GET /api/problems). */
export function queryProblems(q: ProblemQuery): ProblemPage {
  const page = Math.max(1, q.page)
  const pageSize = Math.max(1, Math.min(100, q.pageSize))
  const offset = (page - 1) * pageSize

  const conds: string[] = []
  const params: SqlValue[] = [] // parameters of the WHERE clause, in its order

  const search = q.search.trim().toLowerCase()
  if (search) {
    // instr(), not LIKE: exact substring semantics, so '%' and '_' in the
    // search box are literal characters rather than SQL wildcards.
    conds.push(`(
      instr(lower(p.title), ?) > 0
      OR EXISTS (SELECT 1 FROM problem_tag st
                 WHERE st.problem_id = p.id AND instr(lower(st.tag), ?) > 0)
    )`)
    params.push(search, search)
  }

  const difficulties = q.difficulty.map((d) => d.trim()).filter(Boolean)
  if (difficulties.length) {
    conds.push(`p.difficulty IN (${placeholders(difficulties)})`)
    params.push(...difficulties)
  }

  if (q.status === 'not-started' || q.status === 'started' || q.status === 'solved') {
    conds.push(`COALESCE(pr.status, 'not-started') = ?`)
    params.push(q.status)
  }

  // Multiple tags are ANDed via relational division: join only the requested
  // tags, then require a problem to carry all of them.
  const tags = q.tags.map((t) => t.trim()).filter(Boolean)
  const tagJoin = tags.length
    ? `JOIN problem_tag ft ON ft.problem_id = p.id AND ft.tag IN (${placeholders(tags)})`
    : ''
  const having = tags.length ? 'GROUP BY p.id HAVING COUNT(DISTINCT ft.tag) = ?' : ''

  const where = conds.length ? `WHERE ${conds.join(' AND ')}` : ''
  // Positional parameters bind in the order they appear in the SQL text: the
  // tag join comes before the WHERE clause, the HAVING count after it.
  const bound: SqlValue[] = [...tags, ...params, ...(tags.length ? [tags.length] : [])]
  const from = `FROM problem p LEFT JOIN progress pr ON pr.problem_id = p.id ${tagJoin}`
  const matched = `SELECT p.id AS id, p.position AS position ${from} ${where} ${having}`

  const total = num(one(`SELECT COUNT(*) AS n FROM (${matched})`, bound)?.n ?? 0)

  // Order by position explicitly — catalog order is the only order this list
  // has ever had, and SQLite guarantees none without an ORDER BY.
  const rows = all(
    `
    SELECT p.id AS id, p.title AS title, p.difficulty AS difficulty,
           ${TAGS_EXPR} AS tags,
           COALESCE(pr.status, 'not-started') AS status,
           pr.started_at AS startedAt,
           COALESCE(pr.accumulated_ms, 0) AS accumulatedMs,
           pr.running_since AS runningSince,
           pr.solved_at AS solvedAt,
           pr.elapsed_ms AS elapsedMs,
           COALESCE(pr.attempt_run_count, 0) AS attemptRunCount
    FROM (${matched} ORDER BY position LIMIT ? OFFSET ?) m
    JOIN problem p ON p.id = m.id
    LEFT JOIN progress pr ON pr.problem_id = p.id
    ORDER BY p.position
    `,
    [...bound, pageSize, offset],
  )

  return {
    items: rows.map((r) => ({
      id: str(r.id),
      title: str(r.title),
      difficulty: str(r.difficulty),
      tags: splitTags(r.tags),
      status: str(r.status) as ProblemStatus,
      startedAt: nullableStr(r.startedAt),
      accumulatedMs: num(r.accumulatedMs),
      runningSince: nullableStr(r.runningSince),
      solvedAt: nullableStr(r.solvedAt),
      elapsedMs: nullableNum(r.elapsedMs),
      attemptRunCount: num(r.attemptRunCount),
    })),
    total,
    page,
    pageSize,
  }
}

/** Filter values with counts, always over the WHOLE catalog — never the
 * filtered set, so the sidebar counts don't shift as you filter. */
export function queryFacets(): Facets {
  const difficulties = all(`
    SELECT difficulty AS value, COUNT(*) AS count
    FROM problem
    WHERE difficulty IS NOT NULL AND difficulty <> ''
    GROUP BY difficulty
    ORDER BY ${DIFF_ORDER}
  `)
  const tags = all(`
    SELECT tag AS value, COUNT(*) AS count
    FROM problem_tag
    GROUP BY tag
    ORDER BY count DESC, tag
  `)
  const facet = (r: Row) => ({ value: str(r.value), count: num(r.count) })
  return { difficulties: difficulties.map(facet), tags: tags.map(facet) }
}

// --- curriculum -------------------------------------------------------------

/** Lesson cards with their progress. A lesson is done once ANY exercise has
 * ever been solved — a later Retake must not un-complete it. */
export function queryLessons(): LessonsResponse {
  const rows = all(`
    SELECT l.id AS id, l.title AS title, l.topic AS topic, l.position AS position,
           (SELECT COUNT(*) FROM lesson_exercise le WHERE le.lesson_id = l.id)
             AS exerciseCount,
           (SELECT COUNT(*) FROM lesson_exercise le
             WHERE le.lesson_id = l.id
               AND EXISTS (SELECT 1 FROM solve s WHERE s.problem_id = le.problem_id))
             AS solvedCount
    FROM lesson l
    ORDER BY l.position, l.id
  `)
  return {
    lessons: rows.map((r) => ({
      id: str(r.id),
      title: str(r.title),
      topic: str(r.topic),
      position: num(r.position),
      // Counts every declared exercise, including ids no longer in the
      // catalog — which the exercise list below drops.
      exerciseCount: num(r.exerciseCount),
      solvedCount: num(r.solvedCount),
      done: num(r.solvedCount) >= 1,
    })),
  }
}

/** One lesson: its markdown body (from lessons.json, never a table) plus its
 * exercises with per-exercise status. Null when the id is unknown. */
export function queryLesson(id: string): LessonDetail | null {
  const lesson = one('SELECT id, title, topic FROM lesson WHERE id = ?', [id])
  if (!lesson) return null
  // Ever-solved wins over "the latest attempt is started": a retaken exercise
  // reads solved here and started in the catalog list.
  const exercises = all(
    `
    SELECT le.problem_id AS id, p.title AS title, p.difficulty AS difficulty,
           CASE
             WHEN EXISTS (SELECT 1 FROM solve s WHERE s.problem_id = le.problem_id)
               THEN 'solved'
             WHEN COALESCE(pr.status, 'not-started') = 'started' THEN 'started'
             ELSE 'not-started'
           END AS status
    FROM lesson_exercise le
    JOIN problem p ON p.id = le.problem_id
    LEFT JOIN progress pr ON pr.problem_id = le.problem_id
    WHERE le.lesson_id = ?
    ORDER BY le.ord
    `,
    [id],
  )
  return {
    id: str(lesson.id),
    title: str(lesson.title),
    topic: str(lesson.topic),
    body: lessonBodies.get(id) ?? '',
    exercises: exercises.map((r) => ({
      id: str(r.id),
      title: str(r.title),
      difficulty: str(r.difficulty),
      status: str(r.status) as ProblemStatus,
    })),
  }
}

// --- stats ------------------------------------------------------------------

// Per catalog problem, the fastest TIMED solve and when that timing was first
// recorded. MIN() ignores NULLs natively, so backfilled (untimed) solves drop
// out of the timing metrics without a null guard, while the problem still
// counts as solved.
const BEST_CTE = `
  best AS (
    SELECT s.problem_id AS id, p.title AS title, p.difficulty AS difficulty,
           MIN(s.elapsed_ms) AS best_ms,
           MIN(CASE WHEN s.elapsed_ms IS NOT NULL THEN s.solved_at END) AS first_timed_at
    FROM solve s
    JOIN problem p ON p.id = s.problem_id
    GROUP BY s.problem_id
  )
`

function timeStat(row: Row | null): TimeStat {
  const count = num(row?.count)
  if (!count) return { avgMs: null, bestMs: null, count: 0 }
  return {
    avgMs: pyRound(num(row?.total) / count),
    bestMs: nullableNum(row?.best),
    count,
  }
}

/** The whole stats page, aggregated in SQL (mirrors GET /api/stats). */
export function computeStats(): StatsResponse {
  const totalProblems = num(one('SELECT COUNT(*) AS n FROM problem')?.n)

  // The ONLY stat that does not join `problem`: it sums the whole progress
  // table, ids no longer in the catalog included, so it matches
  // SELECT COUNT(*) FROM run on the server. Every other stat joins and
  // therefore skips them.
  const totalRuns = num(one('SELECT COALESCE(SUM(run_count), 0) AS n FROM progress')?.n)

  const totals = one(`
    WITH ${BEST_CTE}
    SELECT COUNT(*) AS solved, COALESCE(SUM(best_ms), 0) AS total_ms FROM best
  `)

  const byDifficulty = all(`
    SELECT p.difficulty AS difficulty, COUNT(*) AS total,
           SUM(CASE WHEN EXISTS (SELECT 1 FROM solve s WHERE s.problem_id = p.id)
                    THEN 1 ELSE 0 END) AS solved
    FROM problem p
    GROUP BY p.difficulty
    ORDER BY ${DIFF_ORDER}
  `)

  // Ranked by TOTAL, not by solved, and cut to 12 after ordering.
  const byTag = all(`
    SELECT t.tag AS tag, COUNT(*) AS total,
           SUM(CASE WHEN EXISTS (SELECT 1 FROM solve s WHERE s.problem_id = t.problem_id)
                    THEN 1 ELSE 0 END) AS solved
    FROM problem_tag t
    JOIN problem p ON p.id = t.problem_id
    GROUP BY t.tag
    ORDER BY total DESC, t.tag
    LIMIT 12
  `)

  const overall = one(`
    WITH ${BEST_CTE}
    SELECT COUNT(best_ms) AS count, SUM(best_ms) AS total, MIN(best_ms) AS best
    FROM best
  `)

  // Only difficulties that actually have a timed solve, as today.
  const timeByDifficulty = all(`
    WITH ${BEST_CTE}
    SELECT difficulty, COUNT(best_ms) AS count, SUM(best_ms) AS total, MIN(best_ms) AS best
    FROM best WHERE best_ms IS NOT NULL
    GROUP BY difficulty
    ORDER BY ${DIFF_ORDER}
  `)

  // Tie-break: the elapsed times tie in real data, and the Python original
  // relied on a stable sort that kept the order the solves were folded in —
  // i.e. earliest timed solve first, so that is spelled out here.
  const fastest = all(`
    WITH ${BEST_CTE}
    SELECT id, title, difficulty, best_ms AS elapsedMs
    FROM best WHERE best_ms IS NOT NULL
    ORDER BY best_ms, first_timed_at, id
    LIMIT 5
  `)

  const daily = all(`
    SELECT s.day AS date, COUNT(DISTINCT s.problem_id) AS count
    FROM solve s
    JOIN problem p ON p.id = s.problem_id
    GROUP BY s.day
    ORDER BY s.day
  `)

  // Gaps and islands: consecutive days share (day - row number).
  // `current` is the run ending on the LAST day with a solve, which
  // deliberately does not reset when that day isn't today.
  const streak = one(`
    WITH days AS (
      SELECT DISTINCT s.day AS day FROM solve s JOIN problem p ON p.id = s.problem_id
    ),
    grouped AS (
      SELECT day, julianday(day) - ROW_NUMBER() OVER (ORDER BY day) AS grp FROM days
    ),
    runs AS (
      SELECT grp, COUNT(*) AS len, MAX(day) AS last_day FROM grouped GROUP BY grp
    )
    SELECT (SELECT COALESCE(MAX(len), 0) FROM runs) AS longest,
           (SELECT COALESCE(len, 0) FROM runs ORDER BY last_day DESC LIMIT 1) AS current
  `)

  // The latest solve of each problem; on a solved_at tie the earliest attempt
  // wins (seq ascending), matching the fold's strict > comparison.
  const recent = all(`
    WITH latest AS (
      SELECT s.problem_id AS id, s.solved_at AS solvedAt, s.elapsed_ms AS elapsedMs,
             ROW_NUMBER() OVER (
               PARTITION BY s.problem_id ORDER BY s.solved_at DESC, s.seq
             ) AS rn
      FROM solve s
      JOIN problem p ON p.id = s.problem_id
    )
    SELECT l.id AS id, p.title AS title, p.difficulty AS difficulty,
           l.solvedAt AS solvedAt, l.elapsedMs AS elapsedMs
    FROM latest l
    JOIN problem p ON p.id = l.id
    WHERE l.rn = 1
    ORDER BY l.solvedAt DESC, l.id
    LIMIT 6
  `)

  // Ordered by problem id as a plain string, so "CTCI/..." precedes the
  // lowercase ids.
  const inProgress = all(`
    SELECT p.id AS id, p.title AS title, p.difficulty AS difficulty
    FROM progress pr
    JOIN problem p ON p.id = pr.problem_id
    WHERE pr.status = 'started'
    ORDER BY p.id
  `)

  return {
    solvedCount: num(totals?.solved),
    totalProblems,
    totalRuns,
    totalTimeMs: num(totals?.total_ms),
    streak: { current: num(streak?.current), longest: num(streak?.longest) },
    byDifficulty: byDifficulty.map((r) => ({
      difficulty: str(r.difficulty),
      solved: num(r.solved),
      total: num(r.total),
    })),
    byTag: byTag.map((r) => ({
      tag: str(r.tag),
      solved: num(r.solved),
      total: num(r.total),
    })),
    solveTime: {
      overall: timeStat(overall),
      byDifficulty: timeByDifficulty.map(
        (r): DifficultyTimeStat => ({ difficulty: str(r.difficulty), ...timeStat(r) }),
      ),
    },
    fastest: fastest.map((r) => ({
      id: str(r.id),
      title: str(r.title),
      difficulty: str(r.difficulty),
      elapsedMs: num(r.elapsedMs),
    })),
    daily: daily.map((r) => ({ date: str(r.date), count: num(r.count) })),
    recent: recent.map((r) => ({
      id: str(r.id),
      title: str(r.title),
      difficulty: str(r.difficulty),
      solvedAt: str(r.solvedAt),
      elapsedMs: nullableNum(r.elapsedMs),
    })),
    inProgress: inProgress.map((r) => ({
      id: str(r.id),
      title: str(r.title),
      difficulty: str(r.difficulty),
    })),
  }
}
