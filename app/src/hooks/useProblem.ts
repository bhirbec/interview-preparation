import { useEffect, useMemo, useRef, useState } from 'react'
import type { ProblemContent, ProblemState, ProblemView, RunRecord } from '../types'
import { api } from '../api'
import { loadProblem } from '../content'

function merge(content: ProblemContent, state: ProblemState): ProblemView {
  return {
    ...content,
    status: state.status,
    startedAt: state.startedAt,
    accumulatedMs: state.accumulatedMs,
    runningSince: state.runningSince,
    solvedAt: state.solvedAt,
    elapsedMs: state.elapsedMs,
    attemptRunCount: state.attemptRunCount,
    code: state.code,
  }
}

// Loads a problem's static content (one JSON file, straight from public/data —
// the detail page never touches the database) and its dynamic state (saved code
// + latest attempt) side by side, merged into one `problem`, plus its run
// history. `reload` refreshes ONLY the state, so Start/Pause/Resume don't
// re-download the problem text. `onLoad` fires once per id, after BOTH halves
// resolve — it needs `code ?? starter` (reload does NOT call it).
export function useProblem(id: string, onLoad: (p: ProblemView) => void) {
  const [content, setContent] = useState<ProblemContent | null>(null)
  const [state, setState] = useState<ProblemState | null>(null)
  const [notFound, setNotFound] = useState(false)
  const [runs, setRuns] = useState<RunRecord[]>([])
  const onLoadRef = useRef(onLoad)
  onLoadRef.current = onLoad

  useEffect(() => {
    if (!id) return
    let cancelled = false
    setContent(null)
    setState(null)
    setNotFound(false)
    Promise.all([loadProblem(id), api.getProblemState(id)])
      .then(([c, s]) => {
        if (cancelled) return
        setContent(c)
        setState(s)
        onLoadRef.current(merge(c, s))
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
    api.getProblemState(id).then(setState).catch(() => {})
  }

  const problem = useMemo(
    () => (content && state ? merge(content, state) : null),
    [content, state],
  )

  return { problem, setState, notFound, runs, setRuns, reload }
}
