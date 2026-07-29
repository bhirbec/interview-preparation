// Runs Pyodide off the main thread so the UI can enforce a timeout: if a run
// exceeds the budget, the main thread terminates this worker (killing an
// infinite loop) and spins up a fresh one.
/* global importScripts, loadPyodide */
importScripts('https://cdn.jsdelivr.net/pyodide/v0.28.0/full/pyodide.js')

let pyodide = null

async function init() {
  pyodide = await loadPyodide({
    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.28.0/full/',
  })
  postMessage({ type: 'ready' })
}

const ready = init()

self.onmessage = async (e) => {
  const msg = e.data
  if (msg.type !== 'run') return
  const { id, script } = msg
  try {
    await ready
    // Fresh namespace each run so classes from a previous problem never linger.
    const namespace = pyodide.toPy({})
    const start = performance.now()
    let json
    try {
      json = await pyodide.runPythonAsync(script, { globals: namespace })
    } finally {
      namespace.destroy()
    }
    postMessage({ type: 'result', id, ok: true, json, durationMs: performance.now() - start })
  } catch (err) {
    postMessage({ type: 'result', id, ok: false, error: String((err && err.message) || err) })
  }
}
