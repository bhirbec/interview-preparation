// Shared test setup: reset a problem's attempt/run state (and optionally seed
// its saved code) so an e2e run is repeatable without manual DB surgery. Runs
// against the same DynamoDB the app uses, via the api container. That store
// holds only user state, so the reference solution is read from the generated
// content instead.
//
// State is per user now, so the fixtures write under one fixed TEST_USER and
// newPage() hands the browser that same id — otherwise the app would mint a
// random one and never see what was seeded.
import { execFileSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

// fixtures.mjs lives at <repo>/app/e2e/ — compose file is at the repo root.
const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const CONTENT = resolve(REPO_ROOT, 'app/public/data')
const BASE = process.env.BASE_URL || 'http://localhost:3100'

// A valid crypto.randomUUID() shape (user.py rejects anything else), fixed so a
// rerun lands on the same rows as the last one.
export const TEST_USER = '00000000-0000-4000-8000-0000000000e2'

// The static content build mirrors an id's path, so nested ids just work.
export function problemContent(id) {
  return JSON.parse(readFileSync(`${CONTENT}/problems/${id}.json`, 'utf8'))
}

// A page whose browser already identifies as TEST_USER. The app only mints a
// cookie when there is none, so seeding it before the first navigation wins.
export async function newPage(browser) {
  const context = await browser.newContext()
  await context.addCookies([{ name: 'user_id', value: TEST_USER, url: BASE }])
  return context.newPage()
}

function runPython(src) {
  execFileSync('docker', ['compose', 'exec', '-T', 'api', 'python', '-c', src], {
    cwd: REPO_ROOT,
    stdio: 'pipe',
  })
}

// Preamble for every fixture: a boto3 handle on the same tables the API uses,
// plus `user` and `pid`. Table access is direct rather than through db.py — a
// fixture deletes rows, which the app itself never does.
function preamble(id) {
  return [
    'import boto3, db',
    'from boto3.dynamodb.conditions import Key',
    'd = boto3.resource("dynamodb", region_name=db.REGION, endpoint_url=db.ENDPOINT_URL)',
    `user = ${JSON.stringify(TEST_USER)}`,
    `pid = ${JSON.stringify(id)}`,
    '',
    'def clear(table):',
    '  t = d.Table(table)',
    '  rows = t.query(KeyConditionExpression=Key("user_id").eq(user)',
    '                 & Key("sk").begins_with(pid + "#"))["Items"]',
    '  for r in rows:',
    '    t.delete_item(Key={"user_id": user, "sk": r["sk"]})',
    '',
  ].join('\n')
}

// Force a problem to "solved" by inserting a completed attempt — used to make
// curriculum progress deterministic without driving the whole solve UI.
export function markSolved(id) {
  runPython(preamble(id) + [
    'clear(db.ATTEMPTS_TABLE)',
    'd.Table(db.ATTEMPTS_TABLE).put_item(Item={',
    '  "user_id": user, "sk": pid + "#" + __import__("ulid").new(),',
    '  "started_at": "2026-01-01T00:00:00+00:00", "accumulated_ms": 60000,',
    '  "solved_at": "2026-01-01T00:01:00+00:00", "elapsed_ms": 60000,',
    '  "attempt_run_count": 0,',
    '})',
  ].join('\n'))
}

// Delete a problem's runs + attempts (→ status "not-started"). With
// { seedSolution: true }, also save its reference solution as the current code
// so "Start clears the editor" style checks have non-stub code to clear.
export function resetProblem(id, { seedSolution = false } = {}) {
  const code = seedSolution
    ? JSON.stringify(problemContent(id).solution)
    : null
  runPython(preamble(id) + [
    'clear(db.RUNS_TABLE)',
    'clear(db.ATTEMPTS_TABLE)',
    // The submissions row carries the lifetime run counter, so it has to go
    // back to zero with the runs it counted.
    'd.Table(db.SUBMISSIONS_TABLE).delete_item(Key={"user_id": user, "sk": pid})',
    ...(code ? [`db.upsert_submission(user, pid, ${code}, "2026-01-01T00:00:00+00:00")`] : []),
  ].join('\n'))
}
