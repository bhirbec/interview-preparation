import type { ProblemFull, ProblemPage, RunRecord } from './types'

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

export const api = {
  listProblems: (search: string, page: number, pageSize = 20) =>
    fetch(
      `/api/problems?search=${enc(search)}&page=${page}&pageSize=${pageSize}`,
    ).then((r) => asJson<ProblemPage>(r)),

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
}
