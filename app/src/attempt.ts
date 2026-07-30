import type { AttemptState } from './types'

// Live elapsed ms for the current attempt: accumulated time plus, if the timer
// is running, the time since it last resumed.
export function liveElapsed(a: AttemptState, now: number): number {
  let ms = a.accumulatedMs
  if (a.runningSince) ms += now - Date.parse(a.runningSince)
  return ms
}

export interface AttemptView {
  running: boolean
  paused: boolean
  solved: boolean
  notStarted: boolean
  // Time to display: live while in progress, the final solve time once solved.
  elapsedMs: number
}

// Single source for how an attempt maps to UI state at time `now`. Keeps the
// `status === 'started' && runningSince != null` logic from drifting between the
// timer control and the list badge.
export function attemptView(a: AttemptState, now: number): AttemptView {
  const started = a.status === 'started'
  const solved = a.status === 'solved'
  return {
    running: started && a.runningSince != null,
    paused: started && a.runningSince == null,
    solved,
    notStarted: a.status === 'not-started',
    elapsedMs: solved ? a.elapsedMs ?? 0 : liveElapsed(a, now),
  }
}
