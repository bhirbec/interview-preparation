// Replays e2e/golden/api.json through the client-side ports and asserts they
// answer identically to the endpoints they replace.
//
//     node e2e/seed-golden.mjs && node e2e/capture-golden.mjs   # once
//     node e2e/parity.mjs
//
// The ports run inside the page via `import('/src/search.ts')` against the
// running Vite dev server, so this exercises the real module graph (same
// transforms, same JSON, no Node-version dependency).
import { readFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'
import { chromium } from 'playwright'

const BASE = process.env.BASE_URL || 'http://localhost:3100'
const GOLDEN = resolve(dirname(fileURLToPath(import.meta.url)), 'golden/api.json')

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

  // --- /api/problems: same total, and the same ids in the same order ---
  const listed = await page.evaluate(async (queries) => {
    const { filterProblems, paginate } = await import('/src/search.ts')
    const { indexProgress, statusOf } = await import('/src/progress.ts')
    const catalog = await (await fetch('/data/catalog.json')).json()
    const progress = indexProgress((await (await fetch('/api/progress')).json()).problems)

    return queries.map((url) => {
      const q = new URLSearchParams(url.split('?')[1])
      const filters = {
        search: q.get('search') ?? '',
        difficulty: (q.get('difficulty') ?? '').split(','),
        tags: (q.get('tags') ?? '').split(','),
        status: q.get('status') ?? '',
      }
      const matched = filterProblems(catalog.problems, filters, (id) => statusOf(progress, id))
      const p = paginate(matched, Number(q.get('page')), Number(q.get('pageSize')))
      return { total: p.total, ids: p.items.map((x) => x.id), page: p.page, pageSize: p.pageSize }
    })
  }, problemUrls)

  problemUrls.forEach((url, i) => {
    const want = golden[url]
    const got = listed[i]
    assert(got.total === want.total, `${url}: total ${got.total} != ${want.total}`)
    assert(
      eq(got.ids, want.items.map((p) => p.id)),
      `${url}: id order differs\n    got  ${JSON.stringify(got.ids)}\n    want ${JSON.stringify(want.items.map((p) => p.id))}`,
    )
    assert(got.page === want.page && got.pageSize === want.pageSize, `${url}: page/pageSize differ`)
  })
  console.log(`  /api/problems: ${problemUrls.length} queries replayed`)

  // --- /api/facets ---
  const facets = await page.evaluate(async () => {
    const { deriveFacets } = await import('/src/search.ts')
    const catalog = await (await fetch('/data/catalog.json')).json()
    return deriveFacets(catalog.problems)
  })
  assert(eq(facets, golden['/api/facets']), '/api/facets differs')
  console.log('  /api/facets: compared')

  // --- /api/lessons + every /api/lesson?id= ---
  const lessonViews = await page.evaluate(async (ids) => {
    const { lessonSummaries, lessonDetail } = await import('/src/lessons.ts')
    const { indexProgress } = await import('/src/progress.ts')
    const catalog = await (await fetch('/data/catalog.json')).json()
    const lessons = await (await fetch('/data/lessons.json')).json()
    const progress = indexProgress((await (await fetch('/api/progress')).json()).problems)
    return {
      summaries: { lessons: lessonSummaries(lessons.lessons, progress) },
      details: ids.map((id) =>
        lessonDetail(lessons.lessons.find((l) => l.id === id), catalog.problems, progress),
      ),
    }
  }, lessonUrls.map((u) => decodeURIComponent(u.split('id=')[1])))

  assert(eq(lessonViews.summaries, golden['/api/lessons']), '/api/lessons differs')
  lessonUrls.forEach((url, i) => {
    assert(eq(lessonViews.details[i], golden[url]), `${url} differs`)
  })
  console.log(`  /api/lessons + ${lessonUrls.length} lesson details: compared`)

  // --- /api/stats, byte for byte ---
  const statsJson = await page.evaluate(async () => {
    const { computeStats } = await import('/src/stats.ts')
    const catalog = await (await fetch('/data/catalog.json')).json()
    const bundle = (await (await fetch('/api/progress')).json()).problems
    return JSON.stringify(computeStats(catalog.problems, bundle))
  })
  const wantStats = JSON.stringify(golden['/api/stats'])
  assert(statsJson === wantStats, '/api/stats differs')
  if (statsJson !== wantStats) {
    console.log('    got  ', statsJson)
    console.log('    want ', wantStats)
  }
  console.log('  /api/stats: compared byte for byte')

  if (failures) {
    console.error(`\nFAIL — ${failures} of ${checks} assertions failed.`)
    process.exitCode = 1
  } else {
    console.log(`\nPASS — ${checks} assertions, client-side ports match the golden API.`)
  }
} catch (e) {
  console.error('\nFAIL —', e.stack || e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
