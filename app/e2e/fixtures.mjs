// Shared test setup: reset a problem's attempt/run state (and optionally seed
// its saved code) so an e2e run is repeatable without manual DB surgery. Runs
// against the same sqlite DB the app uses, via the api container.
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

// fixtures.mjs lives at <repo>/app/e2e/ — compose file is at the repo root.
const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..')

function runPython(src) {
  execFileSync('docker', ['compose', 'exec', '-T', 'api', 'python', '-c', src], {
    cwd: REPO_ROOT,
    stdio: 'pipe',
  })
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
    sol = c.execute("SELECT solution FROM problem WHERE id=?", (pid,)).fetchone()["solution"]
    c.execute("INSERT INTO submission (problem_id, code, updated_at) "
              "VALUES (?, ?, '2026-01-01T00:00:00+00:00') "
              "ON CONFLICT(problem_id) DO UPDATE SET code=excluded.code", (pid, sol))`
    : ''
  runPython(
    `import db\n` +
    `pid = ${JSON.stringify(id)}\n` +
    `with db.connect() as c:\n` +
    `    c.execute("DELETE FROM run WHERE problem_id=?", (pid,))\n` +
    `    c.execute("DELETE FROM attempt WHERE problem_id=?", (pid,))` +
    seed,
  )
}
