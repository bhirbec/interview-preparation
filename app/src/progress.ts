// Joins /api/progress onto the static catalog. Pure — no React, no fetching.
import type { AttemptState, ProblemStatus, ProgressEntry } from './types'

export type Progress = Map<string, ProgressEntry>

export function indexProgress(entries: ProgressEntry[]): Progress {
  return new Map(entries.map((e) => [e.id, e]))
}

// Mirrors server._attempt_fields' "no attempt row" branch.
const NOT_STARTED: AttemptState = {
  status: 'not-started',
  startedAt: null,
  accumulatedMs: 0,
  runningSince: null,
  solvedAt: null,
  elapsedMs: null,
  attemptRunCount: 0,
}

export function attemptStateOf(entry: ProgressEntry | undefined): AttemptState {
  if (!entry) return NOT_STARTED
  return {
    status: entry.status,
    startedAt: entry.startedAt,
    accumulatedMs: entry.accumulatedMs,
    runningSince: entry.runningSince,
    solvedAt: entry.solvedAt,
    elapsedMs: entry.elapsedMs,
    attemptRunCount: entry.attemptRunCount,
  }
}

// Status of the LATEST attempt — what the catalog list filters and renders on.
export function statusOf(progress: Progress, id: string): ProblemStatus {
  return progress.get(id)?.status ?? 'not-started'
}

// Solved at least once, ever. Not the same as statusOf(...) === 'solved': after
// a Retake the latest attempt is unsolved, but a lesson must stay complete.
export function everSolved(progress: Progress, id: string): boolean {
  return (progress.get(id)?.solves.length ?? 0) > 0
}
