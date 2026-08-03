// Replays e2e/golden/api.json through the client-side SQLite queries and
// asserts they answer identically to the endpoints they replace.
//
//     node e2e/seed-golden.mjs && node e2e/capture-golden.mjs   # once
//     node e2e/parity.mjs
//
// The queries run inside the page via `import('/src/db.ts')` against the
// running Vite dev server, so this exercises the real module graph and the real
// WASM — not a Node re-implementation of either.
//
// Three divergences from the fixtures are deliberate and are asserted as such
// (see DIVERGENCES below).
import { readFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'
import { chromium } from 'playwright'

const BASE = process.env.BASE_URL || 'http://localhost:3100'
const GOLDEN = resolve(dirname(fileURLToPath(import.meta.url)), 'golden/api.json')

// Queries whose golden response the port intentionally does NOT reproduce.
// The server matched `search` against the raw tags JSON *text*, so the array
// separator '", "' hit every problem; tags now live in their own table, where
// that string is not a tag and correctly matches nothing.
const DIVERGENT_SEARCH = '", "'

let failures = 0
let checks = 0

function assert(cond, msg) {
  checks++
  if (!cond) {
    failures++
    console.log('  FAIL -', msg)
  }
}

function eq(a, b) {
  return JSON.stringify(a) === JSON.stringify(b)
}

const golden = JSON.parse(await readFile(GOLDEN, 'utf8'))
const urls = Object.keys(golden)
const problemUrls = urls.filter((u) => u.startsWith('/api/problems?'))
const lessonUrls = urls.filter((u) => u.startsWith('/api/lesson?'))

const browser = await chromium.launch()
const page = await browser.newPage()
page.on('pageerror', (e) => console.log('  [pageerror]', e.message))

try {
  await page.goto(BASE, { waitUntil: 'networkidle' })

  // One page.evaluate for everything: the database is initialized and both the
  // content and progress tables populated once, then every query replays
  // against it.
  const answers = await page.evaluate(async ({ queries, lessonIds }) => {
    const db = await import('/src/db.ts')
    await db.sync()
    return {
      problems: queries.map((url) => {
        const q = new URLSearchParams(url.split('?')[1])
        const page = db.queryProblems({
          search: q.get('search') ?? '',
          difficulty: (q.get('difficulty') ?? '').split(','),
          tags: (q.get('tags') ?? '').split(','),
          status: q.get('status') ?? '',
          page: Number(q.get('page')),
          pageSize: Number(q.get('pageSize')),
        })
        return {
          total: page.total,
          ids: page.items.map((p) => p.id),
          page: page.page,
          pageSize: page.pageSize,
        }
      }),
      facets: db.queryFacets(),
      lessons: db.queryLessons(),
      lessonDetails: lessonIds.map((id) => db.queryLesson(id)),
      stats: JSON.stringify(db.computeStats()),
    }
  }, {
    queries: problemUrls,
    lessonIds: lessonUrls.map((u) => decodeURIComponent(u.split('id=')[1])),
  })

  // --- /api/problems: same total, and the same ids in the same order ---
  let divergent = 0
  problemUrls.forEach((url, i) => {
    const want = golden[url]
    const got = answers.problems[i]
    const q = new URLSearchParams(url.split('?')[1])
    if (q.get('search') === DIVERGENT_SEARCH) {
      divergent++
      assert(got.total === 0, `${url}: documented divergence should match nothing, got ${got.total}`)
      return
    }
    assert(got.total === want.total, `${url}: total ${got.total} != ${want.total}`)
    assert(
      eq(got.ids, want.items.map((p) => p.id)),
      `${url}: id order differs\n    got  ${JSON.stringify(got.ids)}\n    want ${JSON.stringify(want.items.map((p) => p.id))}`,
    )
    assert(got.page === want.page && got.pageSize === want.pageSize, `${url}: page/pageSize differ`)
  })
  console.log(
    `  /api/problems: ${problemUrls.length} queries replayed ` +
    `(${divergent} documented tags-JSON divergences)`,
  )

  // --- /api/facets ---
  assert(eq(answers.facets, golden['/api/facets']), '/api/facets differs')
  console.log('  /api/facets: compared')

  // --- /api/lessons + every /api/lesson?id= ---
  assert(eq(answers.lessons, golden['/api/lessons']), '/api/lessons differs')
  lessonUrls.forEach((url, i) => {
    assert(eq(answers.lessonDetails[i], golden[url]), `${url} differs`)
  })
  console.log(`  /api/lessons + ${lessonUrls.length} lesson details: compared`)

  // --- /api/stats, byte for byte ---
  const wantStats = JSON.stringify(golden['/api/stats'])
  assert(answers.stats === wantStats, '/api/stats differs')
  if (answers.stats !== wantStats) {
    console.log('    got  ', answers.stats)
    console.log('    want ', wantStats)
  }
  console.log('  /api/stats: compared byte for byte')

  if (failures) {
    console.error(`\nFAIL — ${failures} of ${checks} assertions failed.`)
    process.exitCode = 1
  } else {
    console.log(`\nPASS — ${checks} assertions, the client-side SQL matches the golden API.`)
  }
} catch (e) {
  console.error('\nFAIL —', e.stack || e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
