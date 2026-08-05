// The Program (curriculum): drawer → Program lists lessons with progress;
// opening a lesson renders the markdown body + exercises with status; an
// exercise links to its problem; solving an exercise marks the lesson done.
import { chromium } from 'playwright'
import { newPage, markSolved } from './fixtures.mjs'

const BASE = process.env.BASE_URL || 'http://localhost:3100'

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

// three-sum is a "Two Pointers" exercise → that lesson becomes done.
markSolved('three-sum')

const browser = await chromium.launch()
const page = await newPage(browser)
page.on('pageerror', (e) => console.log('  [pageerror]', e.message))

try {
  await page.goto(BASE, { waitUntil: 'networkidle' })
  await page.locator('.problem-list').waitFor()

  // Reach the Program via the drawer menu.
  await page.locator('.menu-btn').click()
  await page.locator('.drawer.open').waitFor()
  await page.locator('.drawer.open .drawer-item', { hasText: 'Program' }).click()
  await page.waitForURL(`${BASE}/program`)

  await page.locator('.lesson-card').first().waitFor()
  const cards = await page.locator('.lesson-card').count()
  assert(cards >= 5, `program lists lessons (${cards})`)
  assert(
    /\d+ of \d+ lessons complete/.test(await page.locator('.program-sub').textContent()),
    'overall progress shown',
  )

  const twoPointers = page.locator('.lesson-card', { hasText: 'Two Pointers' })
  assert(
    await twoPointers.evaluate((el) => el.classList.contains('done')),
    'Two Pointers marked done after solving an exercise',
  )

  // Open the lesson: markdown body + exercise list.
  await twoPointers.click()
  await page.locator('.lesson').waitFor()
  assert((await page.locator('.lesson pre').count()) > 0, 'lesson renders markdown (code block)')
  assert((await page.locator('.exercise-row').count()) > 0, 'lesson lists exercises')
  assert(
    await page
      .locator('.exercise-row', { hasText: 'Three Sum' })
      .locator('.status-badge.solved')
      .isVisible(),
    'the solved exercise shows a solved badge',
  )

  // An exercise links to its problem page.
  await page.locator('.exercise-row').first().click()
  await page.waitForURL(/\/problem\//)
  await page.locator('.cm-content').waitFor()
  assert(true, 'exercise links to its problem')

  console.log('\nPASS — program lists lessons + progress, lesson body + exercises, navigation.')
} catch (e) {
  await page.screenshot({ path: 'e2e/program-failure.png', fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
