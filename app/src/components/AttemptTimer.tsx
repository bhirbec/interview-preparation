import { useEffect, useRef } from 'react'
import type { AttemptState } from '../types'
import { api, type AttemptAction } from '../api'
import { formatDuration } from '../time'
import { attemptView } from '../attempt'
import { useTicker } from '../hooks/useTicker'

interface Props {
  id: string
  attempt: AttemptState
  onChange: () => void
  onStart: () => void // clear the editor to the starter stub for a fresh attempt
}

export default function AttemptTimer({ id, attempt, onChange, onStart }: Props) {
  const running = attempt.status === 'started' && attempt.runningSince != null
  const now = useTicker(running)

  // Auto-pause when the tab is hidden/closed; auto-resume on return (only if we
  // auto-paused). Refs keep the handlers from going stale.
  const attemptRef = useRef(attempt)
  attemptRef.current = attempt
  const onChangeRef = useRef(onChange)
  onChangeRef.current = onChange
  const autoPausedRef = useRef(false)

  useEffect(() => {
    function onVisibility() {
      const a = attemptRef.current
      const isRunning = a.status === 'started' && a.runningSince != null
      const isPaused = a.status === 'started' && a.runningSince == null
      if (document.hidden) {
        if (isRunning) {
          autoPausedRef.current = true
          api.attempt('pause', id).then(() => onChangeRef.current())
        }
      } else if (isPaused && autoPausedRef.current) {
        autoPausedRef.current = false
        api.attempt('resume', id).then(() => onChangeRef.current())
      }
    }
    function onPageHide() {
      const a = attemptRef.current
      if (a.status === 'started' && a.runningSince != null) {
        navigator.sendBeacon(`/api/problem/attempt/pause?id=${encodeURIComponent(id)}`)
      }
    }
    document.addEventListener('visibilitychange', onVisibility)
    window.addEventListener('pagehide', onPageHide)
    return () => {
      document.removeEventListener('visibilitychange', onVisibility)
      window.removeEventListener('pagehide', onPageHide)
    }
  }, [id])

  const act = (action: AttemptAction) => () => {
    autoPausedRef.current = false
    api.attempt(action, id).then(onChange)
  }

  // Start/Retake: clear the editor to the starter stub, then begin a fresh attempt.
  const start = () => {
    autoPausedRef.current = false
    onStart()
    api.attempt('start', id).then(onChange)
  }

  const view = attemptView(attempt, now)

  if (view.notStarted) {
    return (
      <button type="button" className="timer-btn start" onClick={start}>
        ▶ Start
      </button>
    )
  }

  if (view.solved) {
    const runs = attempt.attemptRunCount
    return (
      <span className="timer solved">
        ✓ Solved
        {attempt.elapsedMs != null ? ` ${formatDuration(attempt.elapsedMs)}` : ''}
        {runs ? ` · ${runs} run${runs === 1 ? '' : 's'}` : ''}
        <button type="button" className="timer-btn retake" onClick={start}>
          ↻ Retake
        </button>
      </span>
    )
  }

  // started: running or paused
  const elapsed = formatDuration(view.elapsedMs)
  return view.running ? (
    <span className="timer running">
      ⏱ {elapsed}
      <button type="button" className="timer-btn icon" title="Pause" onClick={act('pause')}>
        ⏸
      </button>
    </span>
  ) : (
    <span className="timer paused">
      ⏸ {elapsed}
      <button type="button" className="timer-btn icon" title="Resume" onClick={act('resume')}>
        ▶
      </button>
    </span>
  )
}
