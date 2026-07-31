// The left drawer menu: 3-dot opens it, it holds Questions + the theme toggle,
// Questions navigates home, and the overlay closes it.
import { chromium } from 'playwright'

const BASE = process.env.BASE_URL || 'http://localhost:3100'

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

const browser = await chromium.launch()
const page = await browser.newPage()
page.on('pageerror', (e) => console.log('  [pageerror]', e.message))

try {
  await page.goto(`${BASE}/problem/maximum-subarray`, { waitUntil: 'networkidle' })
  await page.locator('.cm-content').waitFor()

  assert(!(await page.locator('.drawer.open').count()), 'drawer starts closed')

  await page.locator('.menu-btn').click()
  await page.locator('.drawer.open').waitFor()
  assert(await page.locator('.drawer.open .theme-toggle').isVisible(), 'theme toggle moved into the drawer')
  assert(
    await page.locator('.drawer.open .drawer-item', { hasText: 'Questions' }).isVisible(),
    'drawer has a Questions item',
  )

  // Overlay closes it.
  await page.locator('.drawer-overlay').click()
  await page.locator('.drawer.open').waitFor({ state: 'detached' }).catch(() => {})
  assert(!(await page.locator('.drawer.open').count()), 'overlay click closes the drawer')

  // Questions navigates to the catalog.
  await page.locator('.menu-btn').click()
  await page.locator('.drawer.open .drawer-item', { hasText: 'Questions' }).click()
  await page.waitForURL(`${BASE}/`)
  await page.locator('.problem-list').waitFor()
  assert(true, 'Questions routes to / (catalog)')

  console.log('\nPASS — drawer menu opens, holds Questions + theme, and navigates.')
} catch (e) {
  await page.screenshot({ path: 'e2e/menu-failure.png', fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
