// The user-state API: saved code, test runs and timed attempts. Everything the
// app renders beyond that is static content — see content.ts.
import type { ProblemState, ProgressBundle, RunRecord } from './types'

async function asJson<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`API ${res.status} ${res.statusText}`)
  return res.json() as Promise<T>
}

const jsonHeaders = { 'Content-Type': 'application/json' }
const enc = encodeURIComponent

function get<T>(url: string): Promise<T> {
  return fetch(url).then((r) => asJson<T>(r))
}

// POST/PUT with an optional JSON body (omit the body for query-param endpoints).
function send<T>(method: string, url: string, body?: unknown): Promise<T> {
  const init: RequestInit = { method }
  if (body !== undefined) {
    init.headers = jsonHeaders
    init.body = JSON.stringify(body)
  }
  return fetch(url, init).then((r) => asJson<T>(r))
}

export type AttemptAction = 'start' | 'pause' | 'resume'

export interface NewRun {
  code: string
  passed: number
  failed: number
  total: number
  durationMs: number
}

export const api = {
  // Dynamic state — never memoized, unlike the static content in content.ts.
  getProgress: () => get<ProgressBundle>('/api/progress'),
  getProblemState: (id: string) => get<ProblemState>(`/api/problem/state?id=${enc(id)}`),

  saveCode: (id: string, code: string) =>
    send<{ ok: boolean; updatedAt: string }>('PUT', '/api/problem/code', { id, code }),

  listRuns: (id: string) => get<RunRecord[]>(`/api/problem/runs?id=${enc(id)}`),

  createRun: (id: string, run: NewRun) =>
    send<RunRecord>('POST', '/api/problem/runs', { id, ...run }),

  // Attempt timer (id in the query so a sendBeacon pause on tab-close works).
  attempt: (action: AttemptAction, id: string) =>
    send<{ ok: boolean }>('POST', `/api/problem/attempt/${action}?id=${enc(id)}`),
}
