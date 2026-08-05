// The server API — user state only. Everything the app knows about the
// knowledge content comes from content.ts (static JSON) and db.ts (the
// in-browser SQLite index over it); nothing here reads or serves content.
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

// The SHA-256 of a request body, hex, or null where the browser has no
// SubtleCrypto — see send() for why either answer is fine.
async function sha256Hex(body: string): Promise<string | null> {
  // Only defined in a secure context: https, or localhost in development.
  if (!globalThis.crypto?.subtle) return null
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(body))
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('')
}

// POST/PUT with an optional JSON body (omit the body for query-param endpoints).
//
// x-amz-content-sha256 is what makes the body-carrying calls work in AWS. The
// deployed API is a Lambda function URL behind this distribution, and CloudFront
// SigV4-signs every /api/* request to it — but it does not read the body, and
// Lambda refuses unsigned payloads. So the *caller* has to hand it the body's
// hash to sign; without it PUT and POST come back 403 while every GET works,
// which is as confusing to debug as it sounds.
// https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-lambda.html
//
// Sent unconditionally: locally the Vite proxy forwards the header to uvicorn,
// which ignores it, so dev and prod stay on one code path. Where SubtleCrypto
// is missing there is no CloudFront in front either (it needs a secure context,
// and so does the deployed site), so omitting it is correct and not a fallback.
async function send<T>(method: string, url: string, body?: unknown): Promise<T> {
  const init: RequestInit = { method }
  if (body !== undefined) {
    const json = JSON.stringify(body)
    const hash = await sha256Hex(json)
    init.headers = hash ? { ...jsonHeaders, 'x-amz-content-sha256': hash } : jsonHeaders
    init.body = json
  }
  return asJson<T>(await fetch(url, init))
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
