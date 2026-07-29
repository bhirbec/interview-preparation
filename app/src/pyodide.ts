import type { TestResult } from './types'

// The test run is capped so an infinite loop in the user's code can't hang the
// page. Pyodide runs in a worker; on timeout we terminate it (killing the loop)
// and the next run transparently spins up a fresh one.
const RUN_TIMEOUT_MS = 2000
const READY_TIMEOUT_MS = 60000

export interface RunOutcome {
  results: TestResult[]
  durationMs: number
}

type Pending = {
  resolve: (m: { json: string; durationMs: number }) => void
  reject: (e: Error) => void
  timer: number
}

let worker: Worker | null = null
let ready: Promise<void> | null = null
let seq = 0
const pending = new Map<number, Pending>()

function ensureWorker() {
  if (worker) return
  const w = new Worker(`${import.meta.env.BASE_URL}pyodide.worker.js`)
  worker = w
  ready = new Promise<void>((resolve, reject) => {
    const readyTimer = window.setTimeout(
      () => reject(new Error('Pyodide failed to load')),
      READY_TIMEOUT_MS,
    )
    w.onmessage = (e: MessageEvent) => {
      const m = e.data
      if (m.type === 'ready') {
        clearTimeout(readyTimer)
        resolve()
      } else if (m.type === 'result') {
        const p = pending.get(m.id)
        if (!p) return
        clearTimeout(p.timer)
        pending.delete(m.id)
        if (m.ok) p.resolve({ json: m.json, durationMs: m.durationMs })
        else p.reject(new Error(m.error))
      }
    }
  })
}

// Terminate the worker (e.g. to kill an infinite loop) and reset state so the
// next run creates a fresh one.
function resetWorker() {
  if (worker) worker.terminate()
  worker = null
  ready = null
  for (const p of pending.values()) clearTimeout(p.timer)
  pending.clear()
}

// Pyodide is a multi-MB WASM download; start it early (once).
export function warmUpPyodide(): void {
  ensureWorker()
}

const HARNESS = `
import unittest as _ut, json as _json

class _Collector(_ut.TestResult):
    def __init__(self):
        super().__init__()
        self.records = []
    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append((test._testMethodName, "pass", ""))
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append((test._testMethodName, "fail", self._exc_info_to_string(err, test)))
    def addError(self, test, err):
        super().addError(test, err)
        self.records.append((test._testMethodName, "error", self._exc_info_to_string(err, test)))

_suite = _ut.TestSuite()
_loader = _ut.TestLoader()
for _obj in list(dict(globals()).values()):
    if isinstance(_obj, type) and issubclass(_obj, _ut.TestCase) and _obj is not _ut.TestCase:
        _suite.addTests(_loader.loadTestsFromTestCase(_obj))

_res = _Collector()
_suite.run(_res)
_json.dumps([{"name": n, "status": s, "message": m} for (n, s, m) in _res.records])
`

export async function runTests(
  userCode: string,
  testsCode: string,
): Promise<RunOutcome> {
  ensureWorker()
  await ready // one-time Pyodide load is not subject to the run timeout

  const script = `import unittest\n\n${userCode}\n\n${testsCode}\n${HARNESS}`
  const id = ++seq
  const w = worker!

  return new Promise<RunOutcome>((resolve, reject) => {
    const timer = window.setTimeout(() => {
      pending.delete(id)
      resetWorker() // kill the (possibly infinite) run
      reject(
        new Error(
          `Timed out after ${RUN_TIMEOUT_MS / 1000}s — your code may have an infinite loop.`,
        ),
      )
    }, RUN_TIMEOUT_MS)

    pending.set(id, {
      resolve: (m) => resolve({ results: JSON.parse(m.json), durationMs: m.durationMs }),
      reject,
      timer,
    })
    w.postMessage({ type: 'run', id, script })
  })
}
