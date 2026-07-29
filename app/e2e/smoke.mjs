// Smoke test of the full flow against the API-backed catalog: paginated list,
// server-side search, opening a problem, and running tests in-browser (Pyodide).
import { chromium } from 'playwright'

const BASE = process.env.BASE_URL || 'http://localhost:3100'

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

const solution = (await (await fetch(`${BASE}/api/problem?id=maximum-subarray`)).json()).solution

const browser = await chromium.launch()
const page = await browser.newPage()
page.on('pageerror', (e) => console.log('  [pageerror]', e.message))

try {
  await page.goto(BASE, { waitUntil: 'networkidle' })
  await page.locator('.problem-row').first().waitFor()
  const rows = await page.locator('.problem-row').count()
  assert(rows === 20, `list shows a page of 20 problems (got ${rows})`)
  assert(/\d+ problems/.test(await page.locator('.count').textContent()), 'header shows a total count')

  // Server-side search.
  await page.locator('.search').fill('graph')
  await page.waitForTimeout(500)
  const g = await page.locator('.problem-row').count()
  assert(g > 0 && g < 20, `server search "graph" narrows the list (got ${g})`)

  // Find and open Maximum Subarray (a top-level problem sorted after CTCI).
  await page.locator('.search').fill('maximum subarray')
  await page.waitForTimeout(500)
  await page.getByRole('link', { name: 'Maximum Subarray' }).click()
  await page.getByRole('heading', { name: 'Maximum Subarray' }).waitFor()
  await page.locator('.cm-content').waitFor()
  assert(true, 'problem detail opened from a searched result')

  // Reset to the starter stub (this problem may have autosaved code from a
  // previous run), then run -> Pyodide loads and tests fail.
  await page.getByRole('button', { name: 'Reset' }).click()
  console.log('  running stub (Pyodide load on first run)...')
  await page.getByRole('button', { name: /Run Tests/ }).click()
  await page.locator('.summary').waitFor({ timeout: 120000 })
  assert(/^0\//.test((await page.locator('.summary').textContent()).trim()), 'stub run fails')

  // Paste the real solution -> all pass.
  const editor = page.locator('.cm-content')
  await editor.click()
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A')
  await page.keyboard.press('Backspace')
  await page.keyboard.insertText(solution)
  await page.getByRole('button', { name: /Run Tests/ }).click()
  await page.locator('.summary.all-pass').waitFor({ timeout: 60000 })
  assert(/^10\/10/.test((await page.locator('.summary').textContent()).trim()), 'solution passes 10/10')

  console.log('\nPASS — API-backed list, search, and in-browser test run verified.')
} catch (e) {
  await page.screenshot({ path: 'e2e/smoke-failure.png', fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
