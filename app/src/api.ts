import type {
  Facets,
  ProblemFull,
  ProblemPage,
  RunRecord,
  StatusFilter,
} from './types'

async function asJson<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`API ${res.status} ${res.statusText}`)
  return res.json() as Promise<T>
}

const jsonHeaders = { 'Content-Type': 'application/json' }
const enc = encodeURIComponent

export interface NewRun {
  code: string
  passed: number
  failed: number
  total: number
  durationMs: number
}

export interface ListParams {
  search?: string
  difficulty?: string[]
  tags?: string[]
  status?: StatusFilter
  page?: number
  pageSize?: number
}

export const api = {
  getFacets: () => fetch('/api/facets').then((r) => asJson<Facets>(r)),

  listProblems: (params: ListParams) => {
    const q = new URLSearchParams()
    if (params.search?.trim()) q.set('search', params.search.trim())
    if (params.difficulty?.length) q.set('difficulty', params.difficulty.join(','))
    if (params.tags?.length) q.set('tags', params.tags.join(','))
    if (params.status && params.status !== 'all') q.set('status', params.status)
    q.set('page', String(params.page ?? 1))
    q.set('pageSize', String(params.pageSize ?? 20))
    return fetch(`/api/problems?${q.toString()}`).then((r) => asJson<ProblemPage>(r))
  },

  getProblem: (id: string) =>
    fetch(`/api/problem?id=${enc(id)}`).then((r) => asJson<ProblemFull>(r)),

  saveCode: (id: string, code: string) =>
    fetch('/api/problem/code', {
      method: 'PUT',
      headers: jsonHeaders,
      body: JSON.stringify({ id, code }),
    }).then((r) => asJson<{ ok: boolean; updatedAt: string }>(r)),

  listRuns: (id: string) =>
    fetch(`/api/problem/runs?id=${enc(id)}`).then((r) => asJson<RunRecord[]>(r)),

  createRun: (id: string, run: NewRun) =>
    fetch('/api/problem/runs', {
      method: 'POST',
      headers: jsonHeaders,
      body: JSON.stringify({ id, ...run }),
    }).then((r) => asJson<RunRecord>(r)),

  // Attempt timer (id in the query so a sendBeacon pause on tab-close works).
  startAttempt: (id: string) =>
    fetch(`/api/problem/attempt/start?id=${enc(id)}`, { method: 'POST' }),
  pauseAttempt: (id: string) =>
    fetch(`/api/problem/attempt/pause?id=${enc(id)}`, { method: 'POST' }),
  resumeAttempt: (id: string) =>
    fetch(`/api/problem/attempt/resume?id=${enc(id)}`, { method: 'POST' }),
}
