// The stats page, folded in the browser.
//
// A statement-for-statement port of server.stats() (the `server.py:NNN` comments
// mark the line each block came from). The original already folded in Python
// with no SQL aggregation, so this is mechanical — but several steps are
// load-bearing and are called out where they appear. Pure: no React, no
// fetching.
import type {
  CatalogProblem,
  DifficultyTimeStat,
  ProgressEntry,
  StatsResponse,
  TimeStat,
} from './types'

// server.py:175
const DIFF_ORDER: Record<string, number> = { easy: 0, medium: 1, hard: 2 }

const MS_PER_DAY = 86400000

function diffKey(d: string): number {
  return DIFF_ORDER[d] ?? 99 // server.py:241
}

// Python's round() is banker's rounding (half to even); Math.round is half up.
// Invisible in the UI, but it breaks byte-equality with the server's output.
function pyRound(x: number): number {
  const floor = Math.floor(x)
  const frac = x - floor
  if (frac > 0.5) return floor + 1
  if (frac < 0.5) return floor
  return floor % 2 === 0 ? floor : floor + 1
}

// server.py:178
function timeStats(values: number[]): TimeStat {
  return {
    avgMs: values.length ? pyRound(values.reduce((a, b) => a + b, 0) / values.length) : null,
    // reduce, not Math.min(...values): a big spread would blow the call stack.
    bestMs: values.length ? values.reduce((a, b) => (b < a ? b : a)) : null,
    count: values.length,
  }
}

// server.py:186 — longest run of consecutive days, and the run ending on the
// LAST day in the set. `current` deliberately does not reset when that day isn't
// today; that is existing behaviour.
function streaks(dayNumbers: number[]): { current: number; longest: number } {
  if (!dayNumbers.length) return { current: 0, longest: 0 }
  const days = [...dayNumbers].sort((a, b) => a - b)
  let longest = 1
  let run = 1
  for (let i = 1; i < days.length; i++) {
    run = days[i] - days[i - 1] === 1 ? run + 1 : 1
    longest = Math.max(longest, run)
  }
  let current = 1
  for (let i = days.length - 1; i > 0; i--) {
    if (days[i] - days[i - 1] === 1) current++
    else break
  }
  return { current, longest }
}

// Parse 'YYYY-MM-DD' into a UTC day number. Never `new Date(str)` for date
// arithmetic: '2026-01-01' parses as UTC but '2026-01-01T00:00' as local.
const DAY_RE = /^(\d{4})-(\d{2})-(\d{2})$/

function dayNumber(date: string): number {
  const m = DAY_RE.exec(date)
  if (!m) return NaN
  return Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3])) / MS_PER_DAY
}

interface Meta {
  title: string
  difficulty: string
  tags: string[]
}

export function computeStats(
  problems: CatalogProblem[],
  bundle: ProgressEntry[],
): StatsResponse {
  // server.py:207 — the four queries, now the catalog plus the progress bundle.
  // db.solved_attempts was one global "ORDER BY id" list; rebuild it from the
  // per-problem solves, because the folds below tie-break on that row order.
  const solvedRows = bundle
    .flatMap((e) => e.solves.map((s) => ({ problemId: e.id, ...s })))
    .sort((a, b) => a.attemptId - b.attemptId)
  const totalRuns = bundle.reduce((n, e) => n + e.runCount, 0)
  const started = bundle.filter((e) => e.status === 'started').map((e) => e.id)

  // server.py:214 — problem metadata + totals
  const meta = new Map<string, Meta>()
  const diffTotal = new Map<string, number>()
  const tagTotal = new Map<string, number>()
  for (const p of problems) {
    meta.set(p.id, { title: p.title, difficulty: p.difficulty, tags: p.tags })
    diffTotal.set(p.difficulty, (diffTotal.get(p.difficulty) ?? 0) + 1)
    for (const t of p.tags) tagTotal.set(t, (tagTotal.get(t) ?? 0) + 1)
  }

  // server.py:224 — fold the solved attempts
  const bestElapsed = new Map<string, number>() // problem -> min timed elapsedMs
  const latestSolved = new Map<string, { solvedAt: string; elapsedMs: number | null }>()
  const dayProblems = new Map<string, Set<string>>() // 'YYYY-MM-DD' -> set(problem)
  for (const r of solvedRows) {
    const pid = r.problemId
    if (!meta.has(pid)) continue // solved a problem no longer in the catalog
    const e = r.elapsedMs
    const sa = r.solvedAt
    // The `e != null` guard is essential: in JS `null < x` coerces to `0 < x`,
    // which would make every backfilled (untimed) solve the fastest.
    if (e != null && e < (bestElapsed.get(pid) ?? Infinity)) bestElapsed.set(pid, e)
    // Strictly greater, so the FIRST row wins a solvedAt tie.
    const prev = latestSolved.get(pid)
    if (!prev || sa > prev.solvedAt) latestSolved.set(pid, { solvedAt: sa, elapsedMs: e })
    const day = sa.slice(0, 10)
    // A Set, so re-solving one problem twice in a day counts once.
    if (!dayProblems.has(day)) dayProblems.set(day, new Set())
    dayProblems.get(day)!.add(pid)
  }

  // server.py:239
  const solvedIds = [...latestSolved.keys()]

  // server.py:244
  const diffSolved = new Map<string, number>()
  const tagSolved = new Map<string, number>()
  for (const pid of solvedIds) {
    const m = meta.get(pid)!
    diffSolved.set(m.difficulty, (diffSolved.get(m.difficulty) ?? 0) + 1)
    for (const t of m.tags) tagSolved.set(t, (tagSolved.get(t) ?? 0) + 1)
  }

  // server.py:251 — totals come from the catalog, solved from the fold.
  const byDifficulty = [...diffTotal.keys()]
    .sort((a, b) => diffKey(a) - diffKey(b))
    .map((d) => ({
      difficulty: d,
      solved: diffSolved.get(d) ?? 0,
      total: diffTotal.get(d)!,
    }))

  // server.py:255 — ranked by TOTAL (not solved), and sliced to 12 AFTER sorting.
  const byTag = [...tagTotal]
    .sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0))
    .slice(0, 12)
    .map(([t, n]) => ({ tag: t, solved: tagSolved.get(t) ?? 0, total: n }))

  // server.py:258
  const diffVals = new Map<string, number[]>()
  for (const [pid, e] of bestElapsed) {
    const d = meta.get(pid)!.difficulty
    if (!diffVals.has(d)) diffVals.set(d, [])
    diffVals.get(d)!.push(e)
  }
  const solveTime = {
    overall: timeStats([...bestElapsed.values()]),
    byDifficulty: [...diffVals.keys()]
      .sort((a, b) => diffKey(a) - diffKey(b))
      .map((d): DifficultyTimeStat => ({ difficulty: d, ...timeStats(diffVals.get(d)!) })),
  }

  // server.py:269 — 5 smallest by elapsed; ties keep insertion order (JS sort is
  // stable, matching Python's).
  const fastest = [...bestElapsed]
    .sort((a, b) => a[1] - b[1])
    .slice(0, 5)
    .map(([pid, e]) => ({
      id: pid,
      title: meta.get(pid)!.title,
      difficulty: meta.get(pid)!.difficulty,
      elapsedMs: e,
    }))

  // server.py:274 — a DESCENDING comparator, never sort().reverse(): Python's
  // sorted(reverse=True) is stable and keeps tie order, .reverse() inverts it.
  const recent = [...latestSolved]
    .sort((a, b) => (a[1].solvedAt < b[1].solvedAt ? 1 : a[1].solvedAt > b[1].solvedAt ? -1 : 0))
    .slice(0, 6)
    .map(([pid, v]) => ({
      id: pid,
      title: meta.get(pid)!.title,
      difficulty: meta.get(pid)!.difficulty,
      solvedAt: v.solvedAt,
      elapsedMs: v.elapsedMs,
    }))

  // server.py:279 — sorted by ID as a plain string (so "CTCI/..." precedes
  // lowercase ids), not by position or title. Ids absent from the catalog are
  // dropped, as the SQL join dropped them.
  const inProgress = started
    .filter((pid) => meta.has(pid))
    .sort((a, b) => (a < b ? -1 : a > b ? 1 : 0))
    .map((pid) => ({
      id: pid,
      title: meta.get(pid)!.title,
      difficulty: meta.get(pid)!.difficulty,
    }))

  // server.py:284
  return {
    solvedCount: solvedIds.length,
    totalProblems: problems.length,
    // Sums over the WHOLE bundle, including ids not in the catalog: this mirrors
    // SELECT COUNT(*) FROM run. Filtering here silently regresses it.
    totalRuns,
    // sum([]) is 0 in Python, not null.
    totalTimeMs: [...bestElapsed.values()].reduce((a, b) => a + b, 0),
    streak: streaks([...dayProblems.keys()].map(dayNumber)),
    byDifficulty,
    byTag,
    solveTime,
    fastest,
    daily: [...dayProblems]
      .sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0))
      .map(([d, s]) => ({ date: d, count: s.size })),
    recent,
    inProgress,
  }
}
