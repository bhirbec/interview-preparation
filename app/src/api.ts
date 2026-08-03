import type {
  Facets,
  LessonDetail,
  LessonsResponse,
  ProblemView,
  ProblemPage,
  ProblemState,
  ProgressBundle,
  RunRecord,
  StatsResponse,
  StatusFilter,
} from './types'

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

export interface ListParams {
  search?: string
  difficulty?: string[]
  tags?: string[]
  status?: StatusFilter
  page?: number
  pageSize?: number
}

export const api = {
  getFacets: () => get<Facets>('/api/facets'),

  listProblems: (params: ListParams) => {
    const q = new URLSearchParams()
    if (params.search?.trim()) q.set('search', params.search.trim())
    if (params.difficulty?.length) q.set('difficulty', params.difficulty.join(','))
    if (params.tags?.length) q.set('tags', params.tags.join(','))
    if (params.status && params.status !== 'all') q.set('status', params.status)
    q.set('page', String(params.page ?? 1))
    q.set('pageSize', String(params.pageSize ?? 20))
    return get<ProblemPage>(`/api/problems?${q.toString()}`)
  },

  getProblem: (id: string) => get<ProblemView>(`/api/problem?id=${enc(id)}`),

  getLessons: () => get<LessonsResponse>('/api/lessons'),
  getLesson: (id: string) => get<LessonDetail>(`/api/lesson?id=${enc(id)}`),

  getStats: () => get<StatsResponse>('/api/stats'),

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
