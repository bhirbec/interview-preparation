import type { ProblemState, RunRecord, SummaryMap } from './types'

async function asJson<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`API ${res.status} ${res.statusText}`)
  return res.json() as Promise<T>
}

const jsonHeaders = { 'Content-Type': 'application/json' }

export interface NewRun {
  code: string
  passed: number
  failed: number
  total: number
  durationMs: number
}

export const api = {
  summary: () => fetch('/api/summary').then((r) => asJson<SummaryMap>(r)),

  getProblem: (id: string) =>
    fetch(`/api/problems/${id}`).then((r) => asJson<ProblemState>(r)),

  saveCode: (id: string, code: string) =>
    fetch(`/api/problems/${id}/code`, {
      method: 'PUT',
      headers: jsonHeaders,
      body: JSON.stringify({ code }),
    }).then((r) => asJson<{ ok: boolean; updatedAt: string }>(r)),

  listRuns: (id: string) =>
    fetch(`/api/problems/${id}/runs`).then((r) => asJson<RunRecord[]>(r)),

  createRun: (id: string, run: NewRun) =>
    fetch(`/api/problems/${id}/runs`, {
      method: 'POST',
      headers: jsonHeaders,
      body: JSON.stringify(run),
    }).then((r) => asJson<RunRecord>(r)),
}
