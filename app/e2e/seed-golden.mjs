// Deterministic user-state fixture for the golden-parity harness.
//
// The golden fixtures (capture-golden.mjs) are only meaningful against a
// non-trivial, frozen database, so this wipes attempt/run/submission and
// rebuilds a hand-designed state that exercises every corner the client-side
// search/stats ports have to reproduce:
//
//   - solves across four distinct days (three consecutive, then a gap)
//   - one problem solved twice on the SAME day (day sets must dedupe)
//   - one problem with two solved attempts (the min-elapsed fold must win)
//   - one solve with elapsed_ms = NULL (a backfilled solve)
//   - one paused attempt and one running attempt (status "started")
//   - one retaken problem: solved once, then a fresh unsolved attempt
//   - runs on a problem with NO attempt rows at all
//   - runs and a solved attempt for an id that is no longer in the catalog
//
// Its only consumer is capture-golden.mjs, which — like this file — runs
// against a checkout from before #52, so both still speak to that server's
// SQLite database via the api container. The live app's user state moved to
// DynamoDB in #77; nothing here was ported, because there is nothing left to
// capture.
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..')

// [problem_id, started_at, accumulated_ms, running_since, solved_at, elapsed_ms]
const ATTEMPTS = [
  // three-sum: solved twice on the same day, at the same instant. The min-elapsed
  // fold must pick 90000, "latest solved" must keep the FIRST row on the tie
  // (so recent shows 120000), and the day set must count the problem once.
  ['three-sum', '2026-01-05T09:00:00+00:00', 120000, null, '2026-01-05T09:02:00+00:00', 120000],
  ['three-sum', '2026-01-05T09:00:30+00:00', 90000, null, '2026-01-05T09:02:00+00:00', 90000],
  // A second solve on day 1, from the CTCI namespace (ids sort before lowercase).
  ['CTCI/1.1-is-unique', '2026-01-05T10:00:00+00:00', 45000, null, '2026-01-05T10:00:45+00:00', 45000],
  // Day 2 and day 3 keep the streak going. 300001 makes the "easy" average land
  // on .5 exactly, which Python's banker's rounding resolves down.
  ['valid-braces', '2026-01-06T08:00:00+00:00', 300001, null, '2026-01-06T08:05:00+00:00', 300001],
  // Same elapsed as three-sum (fastest ties) and same solved_at as word-ladder
  // (recent ties) — both orderings must come out of a stable sort.
  ['CTCI/8.4-power-set', '2026-01-07T12:00:00+00:00', 90000, null, '2026-01-07T13:15:00+00:00', 90000],
  ['word-ladder', '2026-01-07T13:00:00+00:00', 900000, null, '2026-01-07T13:15:00+00:00', 900000],
  // Day 4 after a gap: a backfilled solve with no timing at all.
  ['maximum-subarray', '2026-01-10T07:00:00+00:00', 0, null, '2026-01-10T07:00:00+00:00', null],
  // Solved, then retaken: the latest attempt is unsolved so the catalog says
  // "started", while "ever solved" (lessons, stats) still counts it.
  ['valid-braces', '2026-01-11T09:00:00+00:00', 0, '2026-01-11T09:00:00+00:00', null, null],
  // A paused attempt (running_since NULL, never solved).
  ['quicksort', '2026-01-11T10:00:00+00:00', 30000, null, null, null],
  // Another in-progress problem, in the CTCI namespace.
  ['CTCI/2.1-remove-dups', '2026-01-11T11:00:00+00:00', 5000, '2026-01-11T11:00:00+00:00', null, null],
  // A solved attempt for an id no longer in the catalog: the stats solve fold
  // must skip it, but its runs still count toward totalRuns.
  ['retired/gone-problem', '2026-01-12T09:00:00+00:00', 1000, null, '2026-01-12T09:00:01+00:00', 1000],
]

// [problem_id, attempt index into ATTEMPTS (null = no attempt row), run count]
const RUNS = [
  ['three-sum', 0, 3],
  ['three-sum', 1, 1],
  ['CTCI/1.1-is-unique', 2, 2],
  ['valid-braces', 3, 4],
  ['valid-braces', 7, 1],
  ['CTCI/8.4-power-set', 4, 1],
  ['word-ladder', 5, 6],
  ['quicksort', 8, 2],
  ['CTCI/2.1-remove-dups', 9, 1],
  // Runs with no attempt row at all — the progress bundle must still report them
  // or the client's totalRuns drifts from SELECT COUNT(*) FROM run.
  ['spiral-matrix', null, 3],
  // Runs for an id that is not in the catalog.
  ['retired/gone-problem', 10, 2],
]

const SUBMISSIONS = [
  ['three-sum', 'def three_sum(nums):\n  return []\n'],
  ['quicksort', 'def quicksort(arr):\n  return sorted(arr)\n'],
]

// Executed inside the api container with the fixture passed in as JSON.
const PY = `
import json, sys
import db

data = json.loads(sys.argv[1])
with db.connect() as c:
  c.execute("DELETE FROM attempt")
  c.execute("DELETE FROM run")
  c.execute("DELETE FROM submission")
  c.execute("DELETE FROM sqlite_sequence WHERE name IN ('attempt', 'run')")
  attempt_ids = []
  for a in data["attempts"]:
    cur = c.execute(
        "INSERT INTO attempt (problem_id, started_at, accumulated_ms, running_since,"
        " solved_at, elapsed_ms) VALUES (?, ?, ?, ?, ?, ?)", a)
    attempt_ids.append(cur.lastrowid)
  seq = 0
  for pid, idx, count in data["runs"]:
    for _ in range(count):
      seq += 1
      created_at = "2026-01-%02dT%02d:00:00+00:00" % (seq % 20 + 1, seq % 24)
      c.execute(
          "INSERT INTO run (problem_id, code, passed, failed, total, duration_ms,"
          " all_passed, created_at, attempt_id) VALUES (?, 'pass', 1, 0, 1, 12.5, 1, ?, ?)",
          (pid, created_at, None if idx is None else attempt_ids[idx]))
  for pid, code in data["submissions"]:
    c.execute(
        "INSERT INTO submission (problem_id, code, updated_at)"
        " VALUES (?, ?, '2026-01-11T12:00:00+00:00')", (pid, code))
`

export function seedGolden() {
  const payload = JSON.stringify({
    attempts: ATTEMPTS,
    runs: RUNS,
    submissions: SUBMISSIONS,
  })
  execFileSync(
    'docker',
    ['compose', 'exec', '-T', 'api', 'python', '-c', PY, payload],
    { cwd: REPO_ROOT, stdio: 'pipe' },
  )
}

if (import.meta.url === `file://${process.argv[1]}`) {
  seedGolden()
  console.log('seeded golden user state')
}
