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

// What the page must show follows from the catalog plus the seeded solve: one
// difficulty bar per distinct difficulty, and one topic bar per tag the user
// has actually solved (capped at 12) — never one per catalog tag.
const catalog = JSON.parse(readFileSync(`${CONTENT}/catalog.json`, 'utf8'))
const difficulties = new Set(catalog.problems.map((p) => p.difficulty).filter(Boolean))
const tags = new Set(catalog.problems.flatMap((p) => p.tags))
const titles = new Set(catalog.problems.map((p) => p.title))

// Guarantee at least one solve so the page isn't empty.
const SEEDED = 'three-sum'
markSolved(SEEDED)
const seededTags = catalog.problems.find((p) => p.id === SEEDED)?.tags ?? []

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
  const solved = Number(
    await page.locator('.stat-card', { hasText: 'Solved' }).locator('.stat-value').textContent(),
  )
  assert(solved >= 1, `solved card shows a bare count of the user's solves (${solved})`)
  assert(
    !cards.includes(`${catalog.count}`),
    `no card measures progress against the ${catalog.count}-problem catalog`,
  )
  assert(/\d+🔥/.test(cards) && /best \d+/.test(cards), 'streak card renders current + best')

  const diffRows = page.locator('.stat-section', { hasText: 'Solved by difficulty' }).locator('.bar-row')
  assert(
    (await diffRows.count()) === difficulties.size,
    `one bar per catalog difficulty (${difficulties.size})`,
  )

  // Every bar count is now a bare number — no "solved/total" fraction anywhere.
  const allCounts = await page.locator('.bar-count').allTextContents()
  assert(
    allCounts.every((c) => /^\d+$/.test(c.trim())),
    `bar counts are plain solve counts (${allCounts.join(', ')})`,
  )

  // Topics are ranked by the user's own solves, so counts are non-increasing
  // and only solved tags get a bar.
  const topicRows = page.locator('.stat-section', { hasText: 'Solved by topic' }).locator('.bar-row')
  const topicCounts = (await topicRows.locator('.bar-count').allTextContents()).map(Number)
  assert(
    topicCounts.length >= 1 && topicCounts.length <= 12,
    `topic bars are capped at 12 and cover only solved tags (${topicCounts.length})`,
  )
  assert(
    topicCounts.every((n, i) => n >= 1 && (i === 0 || topicCounts[i - 1] >= n)),
    `topic bars are ordered by descending solves (${topicCounts.join(' ≥ ')})`,
  )
  const topicLabels = (await topicRows.locator('.bar-label').allTextContents()).map((l) =>
    l.replace(/^#/, ''),
  )
  assert(
    topicLabels.every((l) => tags.has(l)),
    'every topic bar names a tag from the catalog',
  )
  assert(
    topicCounts.length < 12 ? seededTags.every((t) => topicLabels.includes(t)) : true,
    `the seeded solve's tags are among the solved topics (${seededTags.join(', ')})`,
  )

  // Gap discovery: untouched tags are named, without a completion denominator.
  const gapTags = await page
    .locator('.stat-section', { hasText: 'Not solved yet' })
    .locator('.tag')
    .allTextContents()
  const gaps = gapTags.map((t) => t.replace(/^#/, ''))
  assert(
    gaps.every((t) => tags.has(t) && !topicLabels.includes(t)),
    `unsolved topics name catalog tags with no solve (${gaps.length} listed)`,
  )
  assert(
    seededTags.every((t) => !gaps.includes(t)),
    'a solved tag never shows up as unsolved',
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
