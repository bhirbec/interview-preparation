import { useEffect, useRef, useState } from 'react'
import type { AttemptState } from '../types'
import { api } from '../api'
import { formatDuration } from '../time'

interface Props {
  id: string
  attempt: AttemptState
  onChange: () => void
}

// Live elapsed for the current (unsolved) attempt.
function liveElapsed(a: AttemptState, now: number): number {
  let ms = a.accumulatedMs
  if (a.runningSince) ms += now - Date.parse(a.runningSince)
  return ms
}

export default function AttemptTimer({ id, attempt, onChange }: Props) {
  const [now, setNow] = useState(() => Date.now())
  const running = attempt.status === 'started' && attempt.runningSince != null

  // Tick once a second while running.
  useEffect(() => {
    if (!running) return
    const t = window.setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(t)
  }, [running, attempt.runningSince])

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
          api.pauseAttempt(id).then(() => onChangeRef.current())
        }
      } else if (isPaused && autoPausedRef.current) {
        autoPausedRef.current = false
        api.resumeAttempt(id).then(() => onChangeRef.current())
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

  const act = (fn: (id: string) => Promise<unknown>) => () => {
    autoPausedRef.current = false
    fn(id).then(onChange)
  }

  if (attempt.status === 'not-started') {
    return (
      <button type="button" className="timer-btn start" onClick={act(api.startAttempt)}>
        ▶ Start
      </button>
    )
  }

  if (attempt.status === 'solved') {
    const runs = attempt.attemptRunCount
    return (
      <span className="timer solved">
        ✓ Solved
        {attempt.elapsedMs != null ? ` ${formatDuration(attempt.elapsedMs)}` : ''}
        {runs ? ` · ${runs} run${runs === 1 ? '' : 's'}` : ''}
        <button type="button" className="timer-btn retake" onClick={act(api.startAttempt)}>
          ↻ Retake
        </button>
      </span>
    )
  }

  // started: running or paused
  const elapsed = formatDuration(liveElapsed(attempt, now))
  return running ? (
    <span className="timer running">
      ⏱ {elapsed}
      <button type="button" className="timer-btn icon" title="Pause" onClick={act(api.pauseAttempt)}>
        ⏸
      </button>
    </span>
  ) : (
    <span className="timer paused">
      ⏸ {elapsed}
      <button type="button" className="timer-btn icon" title="Resume" onClick={act(api.resumeAttempt)}>
        ▶
      </button>
    </span>
  )
}
