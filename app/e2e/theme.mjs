// Visual check for the dark/light theme toggle.
import { chromium } from 'playwright'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const BASE = process.env.BASE_URL || 'http://localhost:3100'
const here = dirname(fileURLToPath(import.meta.url))

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

const browser = await chromium.launch()
const page = await browser.newPage()
try {
  await page.goto(`${BASE}/problem/maximum-subarray`, { waitUntil: 'networkidle' })
  await page.locator('.cm-content').waitFor()

  const initial = await page.evaluate(() => document.documentElement.getAttribute('data-theme'))
  assert(initial === 'dark', `dark is the default theme (got "${initial}")`)
  await page.screenshot({ path: join(here, 'theme-dark.png'), fullPage: true })

  await page.locator('.theme-toggle').click()
  const afterToggle = await page.evaluate(() => document.documentElement.getAttribute('data-theme'))
  assert(afterToggle === 'light', `toggle switches to light (got "${afterToggle}")`)
  await page.screenshot({ path: join(here, 'theme-light.png'), fullPage: true })

  // Persistence across reload.
  await page.reload({ waitUntil: 'networkidle' })
  const persisted = await page.evaluate(() => document.documentElement.getAttribute('data-theme'))
  assert(persisted === 'light', `choice persists across reload (got "${persisted}")`)

  console.log('\nPASS — theme toggle works. Screenshots: e2e/theme-dark.png, e2e/theme-light.png')
} catch (e) {
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
