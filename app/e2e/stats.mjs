// The Stats page: drawer → Stats renders the metrics computed in the browser
// from catalog.json + /api/progress.
//
// This is a RENDERING test against the deterministic seed in seed-golden.mjs —
// every expectation below is a hand-checked consequence of that fixture. The
// numeric fidelity of the fold itself (ties, banker's rounding, streaks, …) is
// proven separately, and far more thoroughly, by parity.mjs.
import { chromium } from 'playwright'
import { seedGolden } from './seed-golden.mjs'

const BASE = process.env.BASE_URL || 'http://localhost:3100'

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

// From the seed: 6 distinct problems solved, 26 runs, 1425001 ms of best times
// (23:45), solve days 01-05/06/07 then 01-10 (longest streak 3, current 1), and
// 3 problems in progress, 'CTCI/2.1-remove-dups' first by raw id.
const EXPECTED = {
  solved: 6,
  runs: 26,
  time: '23:45',
  streak: 1,
  longest: 3,
  difficulties: 3,
  tags: 12,
  fastestFirst: 'Is Unique',
  recentFirst: 'Maximum Subarray',
  inProgress: ['Remove Dups', 'Quicksort', 'Valid Braces'],
}

seedGolden()
const catalog = await (await fetch(`${BASE}/data/catalog.json`)).json()

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
    cards.includes(String(EXPECTED.solved)) && cards.includes(`/ ${catalog.count}`),
    `solved card shows ${EXPECTED.solved} / ${catalog.count}`,
  )
  assert(cards.includes(EXPECTED.time), `time-solving card shows ${EXPECTED.time}`)
  assert(cards.includes(`${EXPECTED.streak}🔥`), `streak card shows ${EXPECTED.streak}`)
  assert(cards.includes(`best ${EXPECTED.longest}`), `longest streak is ${EXPECTED.longest}`)
  assert(cards.includes(String(EXPECTED.runs)), `test-runs card shows ${EXPECTED.runs}`)

  const bars = await page.locator('.bar-row').count()
  assert(
    bars === EXPECTED.difficulties + EXPECTED.tags,
    `difficulty + topic bars render (${bars})`,
  )
  assert((await page.locator('.heat-cell').count()) === 126, 'activity heatmap has 18×7 cells')
  assert(
    /Overall — avg \d+:\d\d · best \d+:\d\d/.test(
      await page.locator('.solvetime-overall').textContent(),
    ),
    'solve-time overall line renders',
  )
  assert(
    (await page.locator('.stat-section', { hasText: 'Topic coverage' }).count()) === 1,
    'topic coverage section present',
  )

  const solveTime = page.locator('.stat-section', { hasText: 'Solve time' })
  assert(
    (await solveTime.locator('.stat-link').first().textContent()) === EXPECTED.fastestFirst,
    `fastest solve is "${EXPECTED.fastestFirst}"`,
  )
  const recent = page.locator('.stat-section', { hasText: 'Recently solved' })
  assert(
    (await recent.locator('.stat-link').first().textContent()) === EXPECTED.recentFirst,
    `most recent solve is "${EXPECTED.recentFirst}"`,
  )
  const inProgress = page.locator('.stat-section', { hasText: 'In progress' })
  assert(
    JSON.stringify(await inProgress.locator('.stat-link').allTextContents())
      === JSON.stringify(EXPECTED.inProgress),
    `in-progress list is ${EXPECTED.inProgress.join(', ')} (sorted by raw id)`,
  )

  // A fastest-solve entry links to its problem.
  await solveTime.locator('.stat-link').first().click()
  await page.waitForURL(/\/problem\//)
  await page.locator('.cm-content').waitFor()
  assert(true, 'a stat entry links to its problem')

  console.log('\nPASS — stats renders the browser-computed metrics, heatmap, and links.')
} catch (e) {
  await page.screenshot({ path: 'e2e/stats-failure.png', fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
