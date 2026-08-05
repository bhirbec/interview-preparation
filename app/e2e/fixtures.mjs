// Shared test setup: reset a problem's attempt/run state (and optionally seed
// its saved code) so an e2e run is repeatable without manual DB surgery. Runs
// against the same DynamoDB the app uses, via the api container. That store now
// holds only user state, so the reference solution is read from the generated
// content instead.
//
// The server partitions state by the id in the browser's cookie, so seeding and
// browsing have to agree on one. E2E_USER_ID is that id, and newPage() is how a
// test gets a browser already carrying it — a plain browser.newPage() would mint
// a fresh id on load and see none of what was seeded here.
import { execFileSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

// fixtures.mjs lives at <repo>/app/e2e/ — compose file is at the repo root.
const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const CONTENT = resolve(REPO_ROOT, 'app/public/data')
const BASE = process.env.BASE_URL || 'http://localhost:3100'

// A fixed UUID, so a suite run and the state it seeds share a partition. It has
// to satisfy the server's UUID check like any other id.
export const E2E_USER_ID = 'e2e00000-0000-4000-8000-000000000001'

// The static content build mirrors an id's path, so nested ids just work.
export function problemContent(id) {
  return JSON.parse(readFileSync(`${CONTENT}/problems/${id}.json`, 'utf8'))
}

// A page whose browser context already has the id cookie, so it reads and
// writes the same partition the fixtures below seed.
export async function newPage(browser) {
  const context = await browser.newContext()
  await context.addCookies([{ name: 'trainer_uid', value: E2E_USER_ID, url: BASE }])
  return context.newPage()
}

// Piped on stdin rather than passed with -c: these snippets are multi-line and
// quoting them through docker exec is more trouble than it is worth.
function runPython(src) {
  execFileSync('docker', ['compose', 'exec', '-T', 'api', 'python', '-'], {
    cwd: REPO_ROOT,
    input: src,
    stdio: ['pipe', 'pipe', 'pipe'],
  })
}

// Preamble shared by both fixtures: bind the partition and give them a way to
// delete a whole sort-key prefix (there is no DELETE ... WHERE here).
function preamble(id) {
  return `
import db
from boto3.dynamodb.conditions import Key

pid = ${JSON.stringify(id)}
t = db.table()
pk = db.user_pk(${JSON.stringify(E2E_USER_ID)})

def delete_prefix(prefix):
  resp = t.query(
      KeyConditionExpression=Key("pk").eq(pk) & Key("sk").begins_with(prefix),
      ProjectionExpression="sk",
  )
  with t.batch_writer() as batch:
    for item in resp["Items"]:
      batch.delete_item(Key={"pk": pk, "sk": item["sk"]})
`
}

// Force a problem to "solved" by writing a completed attempt plus its solve —
// used to make curriculum progress deterministic without driving the whole
// solve UI. Both items are needed: the P# item is the status the list renders,
// the SLV# item is the "ever solved" the lessons and stats read.
export function markSolved(id) {
  runPython(preamble(id) + `
t.delete_item(Key={"pk": pk, "sk": db.problem_sk(pid)})
delete_prefix(db.solve_prefix(pid))
t.put_item(Item={
    "pk": pk,
    "sk": db.problem_sk(pid),
    "started_at": "2026-01-01T00:00:00+00:00",
    "accumulated_ms": 60000,
    "solved_at": "2026-01-01T00:01:00+00:00",
    "elapsed_ms": 60000,
})
t.put_item(Item={
    "pk": pk,
    "sk": db.solve_prefix(pid) + db.new_ulid(),
    "problem_id": pid,
    "solved_at": "2026-01-01T00:01:00+00:00",
    "elapsed_ms": 60000,
})
`)
}

// Delete a problem's runs, solves and attempt state (→ status "not-started").
// With { seedSolution: true }, also save its reference solution as the current
// code so "Start clears the editor" style checks have non-stub code to clear.
export function resetProblem(id, { seedSolution = false } = {}) {
  const seed = seedSolution
    ? `db.save_code(${JSON.stringify(E2E_USER_ID)}, pid, `
      + `${JSON.stringify(problemContent(id).solution)}, "2026-01-01T00:00:00+00:00")`
    : ''
  runPython(preamble(id) + `
t.delete_item(Key={"pk": pk, "sk": db.problem_sk(pid)})
delete_prefix(db.run_prefix(pid))
delete_prefix(db.solve_prefix(pid))
${seed}
`)
}
