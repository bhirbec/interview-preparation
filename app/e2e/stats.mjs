// The Stats page: drawer → Stats renders metrics consistent with /api/stats —
// solved count, difficulty + topic bars, the activity heatmap, and solve times.
import { chromium } from 'playwright'
import { markSolved } from './fixtures.mjs'

const BASE = process.env.BASE_URL || 'http://localhost:3100'

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

// Guarantee at least one solve so the page isn't empty, then read the API so we
// can assert the rendered numbers match it.
markSolved('three-sum')
const stats = await (await fetch(`${BASE}/api/stats`)).json()

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
  assert(
    cards.includes(String(stats.solvedCount)) && cards.includes(`/ ${stats.totalProblems}`),
    `solved card shows ${stats.solvedCount} / ${stats.totalProblems} (from API)`,
  )
  assert(cards.includes(String(stats.totalRuns)), `test-runs card shows ${stats.totalRuns}`)

  const bars = await page.locator('.bar-row').count()
  assert(
    bars === stats.byDifficulty.length + stats.byTag.length,
    `difficulty + topic bars render (${bars})`,
  )
  assert((await page.locator('.heat-cell').count()) === 126, 'activity heatmap has 18×7 cells')
  assert(
    /Overall — (avg \d+:\d\d|no timed)/.test(
      await page.locator('.solvetime-overall').textContent(),
    ),
    'solve-time overall line renders',
  )
  assert(
    (await page.locator('.stat-section', { hasText: 'Topic coverage' }).count()) === 1,
    'topic coverage section present',
  )

  // A fastest-solve entry links to its problem.
  await page.locator('.stat-section', { hasText: 'Solve time' }).locator('.stat-link').first().click()
  await page.waitForURL(/\/problem\//)
  await page.locator('.cm-content').waitFor()
  assert(true, 'a stat entry links to its problem')

  console.log('\nPASS — stats renders API-consistent metrics, heatmap, and links.')
} catch (e) {
  await page.screenshot({ path: 'e2e/stats-failure.png', fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
