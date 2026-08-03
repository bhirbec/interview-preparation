// Shared test setup: reset a problem's attempt/run state (and optionally seed
// its saved code) so an e2e run is repeatable without manual DB surgery. Runs
// against the same sqlite DB the app uses, via the api container. The reference
// solution comes from the generated content, not the DB.
import { execFileSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

// fixtures.mjs lives at <repo>/app/e2e/ — compose file is at the repo root.
const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const CONTENT_DIR = resolve(REPO_ROOT, 'app/public/data')

function runPython(src, ...args) {
  execFileSync('docker', ['compose', 'exec', '-T', 'api', 'python', '-c', src, ...args], {
    cwd: REPO_ROOT,
    stdio: 'pipe',
  })
}

// A problem's static content, read straight off disk (built by
// backend/build_content.py). Ids can contain "/", a real path segment.
export function readProblem(id) {
  const path = resolve(CONTENT_DIR, 'problems', ...id.split('/')) + '.json'
  return JSON.parse(readFileSync(path, 'utf8'))
}

// Force a problem to "solved" by inserting a completed attempt — used to make
// curriculum progress deterministic without driving the whole solve UI.
export function markSolved(id) {
  const src = [
    'import db',
    `pid = ${JSON.stringify(id)}`,
    'with db.connect() as c:',
    '    c.execute("DELETE FROM attempt WHERE problem_id=?", (pid,))',
    '    c.execute("INSERT INTO attempt (problem_id, started_at, accumulated_ms,'
      + " running_since, solved_at, elapsed_ms) VALUES"
      + " (?, '2026-01-01T00:00:00+00:00', 60000, NULL,"
      + " '2026-01-01T00:01:00+00:00', 60000)\", (pid,))",
  ].join('\n')
  runPython(src)
}

// Delete a problem's runs + attempts (→ status "not-started"). With
// { seedSolution: true }, also save its reference solution as the current code
// so "Start clears the editor" style checks have non-stub code to clear.
export function resetProblem(id, { seedSolution = false } = {}) {
  const seed = seedSolution
    ? `
    c.execute("INSERT INTO submission (problem_id, code, updated_at) "
              "VALUES (?, ?, '2026-01-01T00:00:00+00:00') "
              "ON CONFLICT(problem_id) DO UPDATE SET code=excluded.code",
              (pid, sys.argv[2]))`
    : ''
  runPython(
    'import sys\n'
    + 'import db\n'
    + 'pid = sys.argv[1]\n'
    + 'with db.connect() as c:\n'
    + '    c.execute("DELETE FROM run WHERE problem_id=?", (pid,))\n'
    + '    c.execute("DELETE FROM attempt WHERE problem_id=?", (pid,))'
    + seed,
    id,
    seedSolution ? readProblem(id).solution : '',
  )
}
