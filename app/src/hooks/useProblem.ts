import { useEffect, useRef, useState } from 'react'
import type { ProblemView, RunRecord } from '../types'
import { api } from '../api'

// Loads a problem (definition + saved code + runs) and its run history, and
// exposes a `reload` that refreshes only the problem (attempt status/timing)
// without disturbing the editor. `onLoad` fires once per id, when the problem is
// first fetched — use it to seed editor state (reload does NOT call it).
export function useProblem(id: string, onLoad: (p: ProblemView) => void) {
  const [problem, setProblem] = useState<ProblemView | null>(null)
  const [notFound, setNotFound] = useState(false)
  const [runs, setRuns] = useState<RunRecord[]>([])
  const onLoadRef = useRef(onLoad)
  onLoadRef.current = onLoad

  useEffect(() => {
    if (!id) return
    let cancelled = false
    setProblem(null)
    setNotFound(false)
    api
      .getProblem(id)
      .then((p) => {
        if (cancelled) return
        setProblem(p)
        onLoadRef.current(p)
      })
      .catch(() => !cancelled && setNotFound(true))
    api
      .listRuns(id)
      .then((r) => !cancelled && setRuns(r))
      .catch(() => {})
    return () => {
      cancelled = true
    }
  }, [id])

  function reload() {
    api.getProblem(id).then(setProblem).catch(() => {})
  }

  return { problem, setProblem, notFound, runs, setRuns, reload }
}
