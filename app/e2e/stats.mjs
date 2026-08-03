// The Stats page: drawer → Stats renders the metrics the browser computes from
// the static catalog and /api/progress.
//
// This is a RENDERING test. It asserts the shape the page must have for a given
// catalog — the totals, the number of bars, their ordering, the heatmap grid —
// rather than re-deriving each number, because /api/stats no longer exists to
// compare against. Numeric fidelity is proven separately and exhaustively by
// e2e/parity.mjs, which replays the golden fixtures through computeStats().
import { chromium } from 'playwright'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'
import { markSolved } from './fixtures.mjs'

const BASE = process.env.BASE_URL || 'http://localhost:3100'
const CONTENT = resolve(dirname(fileURLToPath(import.meta.url)), '../public/data')

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

// What the page must show follows from the catalog alone: one difficulty bar
// per distinct difficulty, and topic coverage capped at the top 12 tags.
const catalog = JSON.parse(readFileSync(`${CONTENT}/catalog.json`, 'utf8'))
const difficulties = new Set(catalog.problems.map((p) => p.difficulty).filter(Boolean))
const tags = new Set(catalog.problems.flatMap((p) => p.tags))
const titles = new Set(catalog.problems.map((p) => p.title))
const expectedBars = difficulties.size + Math.min(12, tags.size)

// Guarantee at least one solve so the page isn't empty.
markSolved('three-sum')

const browser = await chromium.launch()
const page = await browser.newPage()
page.on('pageerror', (e) => console.log('  [pageerror]', e.message))

try {
  await page.goto(BASE, { waitUntil: 'networkidle' })
  await page.locator('.problem-list').waitFor()

  // Reach Stats via the drawer menu.
  await page.locator('.menu-btn').click()
  await page.locator('.drawer.open').waitFor()
  await page.locator('.drawer.open .drawer-item', { hasText: 'Stats' }).click()
  await page.waitForURL(`${BASE}/stats`)
  await page.locator('.stat-cards').waitFor()

  const cards = await page.locator('.stat-cards').textContent()
  assert(cards.includes(`/ ${catalog.count}`), `solved card counts out of ${catalog.count} problems`)
  const solved = Number(/(\d+)\s*\/\s*\d+/.exec(cards)?.[1])
  assert(solved >= 1, `solved count reflects the seeded solve (${solved})`)
  assert(/\d+🔥/.test(cards) && /best \d+/.test(cards), 'streak card renders current + best')

  const bars = await page.locator('.bar-row').count()
  assert(bars === expectedBars, `${difficulties.size} difficulty + 12 topic bars render (${bars})`)

  // Topic coverage is ranked by total, so the counts must be non-increasing.
  const topicRows = page.locator('.stat-section', { hasText: 'Topic coverage' }).locator('.bar-row')
  const topicCounts = await topicRows.locator('.bar-count').allTextContents()
  const totals = topicCounts.map((t) => Number(t.split('/')[1]))
  assert(
    totals.every((n, i) => i === 0 || totals[i - 1] >= n),
    `topic bars are ordered by descending total (${totals.join(' ≥ ')})`,
  )
  const topicLabels = await topicRows.locator('.bar-label').allTextContents()
  assert(
    topicLabels.every((l) => tags.has(l.replace(/^#/, ''))),
    'every topic bar names a tag from the catalog',
  )

  assert((await page.locator('.heat-cell').count()) === 126, 'activity heatmap has 18×7 cells')
  assert(
    /Overall — (avg \d+:\d\d|no timed)/.test(
      await page.locator('.solvetime-overall').textContent(),
    ),
    'solve-time overall line renders',
  )

  const recent = page.locator('.stat-section', { hasText: 'Recently solved' }).locator('.stat-link')
  const recentTitles = await recent.allTextContents()
  assert(recentTitles.length >= 1, `recently solved lists ${recentTitles.length} solve(s)`)
  assert(
    recentTitles.every((t) => titles.has(t)),
    'every recent entry names a problem from the catalog',
  )

  // A fastest-solve entry links to its problem.
  await page.locator('.stat-section', { hasText: 'Solve time' }).locator('.stat-link').first().click()
  await page.waitForURL(/\/problem\//)
  await page.locator('.cm-content').waitFor()
  assert(true, 'a stat entry links to its problem')

  console.log('\nPASS — stats renders catalog-consistent metrics, heatmap, and links.')
} catch (e) {
  await page.screenshot({ path: 'e2e/stats-failure.png', fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
