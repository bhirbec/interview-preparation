// Records the responses of every endpoint this ticket replaces, so the
// client-side ports (search.ts, stats.ts, the lesson view models) can be
// replayed against them (see parity.mjs).
//
// Run against the CURRENT server, on a frozen database:
//
//     node e2e/seed-golden.mjs
//     node e2e/capture-golden.mjs
//
// and do NOT run other e2e scripts in between — they mutate attempt/run.
// Output: e2e/golden/api.json, a { url: response } map (gitignored).
//
// Note the /api/problems search matrix deliberately contains no "%" or "_":
// query_problem_page interpolates the raw search into a SQL LIKE, so those are
// wildcards server-side. The client's includes() is the intended semantics.
import { mkdir, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const BASE = process.env.BASE_URL || 'http://localhost:3100'
const OUT_DIR = resolve(dirname(fileURLToPath(import.meta.url)), 'golden')

const SEARCHES = ['', 'graph', 'sum', 'Two', 'ARRAY', 'ctci', 'zzz', 'a', '", "', 'two-pointers']
const DIFFICULTIES = ['', 'easy', 'easy,hard', 'medium']
const TAGS = ['', 'array', 'array,two-pointers', 'dp']
const STATUSES = ['', 'not-started', 'started', 'solved']
const PAGES = [1, 2, 7]

const enc = encodeURIComponent

async function getJson(url) {
  const res = await fetch(`${BASE}${url}`)
  if (!res.ok) throw new Error(`${url} -> ${res.status} ${res.statusText}`)
  return res.json()
}

// Fetch with a small concurrency cap; the matrix is ~2k requests.
async function fetchAll(urls, onProgress) {
  const out = {}
  let next = 0
  let done = 0
  async function worker() {
    while (next < urls.length) {
      const url = urls[next++]
      out[url] = await getJson(url)
      if (++done % 200 === 0) onProgress(done, urls.length)
    }
  }
  await Promise.all(Array.from({ length: 8 }, worker))
  return out
}

const urls = ['/api/facets', '/api/stats', '/api/lessons']

const lessons = await getJson('/api/lessons')
for (const l of lessons.lessons) urls.push(`/api/lesson?id=${enc(l.id)}`)

const catalog = await getJson('/api/problems?pageSize=100&page=1')
const ids = [...catalog.items.map((p) => p.id)]
for (let page = 2; ids.length < catalog.total; page++) {
  const next = await getJson(`/api/problems?pageSize=100&page=${page}`)
  if (!next.items.length) break
  ids.push(...next.items.map((p) => p.id))
}
for (const id of ids) urls.push(`/api/problem?id=${enc(id)}`)

for (const search of SEARCHES) {
  for (const difficulty of DIFFICULTIES) {
    for (const tags of TAGS) {
      for (const status of STATUSES) {
        for (const page of PAGES) {
          const q = new URLSearchParams({
            search,
            difficulty,
            tags,
            status,
            page: String(page),
            pageSize: '20',
          })
          urls.push(`/api/problems?${q.toString()}`)
        }
      }
    }
  }
}

console.log(`capturing ${urls.length} responses from ${BASE}…`)
const golden = await fetchAll(urls, (n, total) => console.log(`  ${n}/${total}`))

await mkdir(OUT_DIR, { recursive: true })
await writeFile(`${OUT_DIR}/api.json`, JSON.stringify(golden, null, 1))
console.log(`wrote ${OUT_DIR}/api.json (${Object.keys(golden).length} entries, ${ids.length} problems)`)
