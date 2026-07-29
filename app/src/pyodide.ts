import type { TestResult } from './types'

declare global {
  interface Window {
    loadPyodide: (config?: { indexURL?: string }) => Promise<PyodideLike>
  }
}

interface PyodideLike {
  runPythonAsync: (code: string, options?: { globals?: unknown }) => Promise<string>
  toPy: (obj: unknown) => { destroy: () => void }
}

const PYODIDE_VERSION = 'v0.28.0'
let pyodidePromise: Promise<PyodideLike> | null = null

// Pyodide is a multi-MB WASM download; load it once and reuse.
function loadPyodideOnce(): Promise<PyodideLike> {
  if (!pyodidePromise) {
    pyodidePromise = window.loadPyodide({
      indexURL: `https://cdn.jsdelivr.net/pyodide/${PYODIDE_VERSION}/full/`,
    })
  }
  return pyodidePromise
}

export function warmUpPyodide(): void {
  void loadPyodideOnce()
}

// Appended after the user's code + the test class. Collects every TestCase
// subclass defined in the run namespace, runs them, and returns JSON.
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

export interface RunOutcome {
  results: TestResult[]
  durationMs: number
}

export async function runTests(
  userCode: string,
  testsCode: string,
): Promise<RunOutcome> {
  const pyodide = await loadPyodideOnce()
  const script = `import unittest\n\n${userCode}\n\n${testsCode}\n${HARNESS}`
  // Fresh namespace each run so classes from a previous problem never linger.
  const namespace = pyodide.toPy({})
  // Time only the test execution, not the (one-time) Pyodide download above.
  const start = performance.now()
  try {
    const json = await pyodide.runPythonAsync(script, { globals: namespace })
    const durationMs = performance.now() - start
    return { results: JSON.parse(json) as TestResult[], durationMs }
  } finally {
    namespace.destroy()
  }
}
