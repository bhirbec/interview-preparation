// Smoke test of the full flow against the static catalog: paginated list,
// client-side search, opening a problem, and running tests in-browser (Pyodide).
import { chromium } from 'playwright'
import { resetProblem } from './fixtures.mjs'

const BASE = process.env.BASE_URL || 'http://localhost:3100'

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

resetProblem('maximum-subarray') // repeatable: back to not-started
const solution = (await (await fetch(`${BASE}/data/problems/maximum-subarray.json`)).json()).solution

const browser = await chromium.launch()
const page = await browser.newPage()
const requests = []
page.on('request', (r) => requests.push(r.url()))
page.on('pageerror', (e) => console.log('  [pageerror]', e.message))

try {
  await page.goto(BASE, { waitUntil: 'networkidle' })
  await page.locator('.problem-row').first().waitFor()
  const rows = await page.locator('.problem-row').count()
  assert(rows === 20, `list shows a page of 20 problems (got ${rows})`)
  assert(/\d+ problems/.test(await page.locator('.list-total').textContent()), 'footer shows a total count')

  // Client-side search: no round trip, so no debounce to wait out.
  const before = requests.length
  await page.locator('.search').fill('graph')
  await page.waitForTimeout(300)
  const g = await page.locator('.problem-row').count()
  assert(g > 0 && g < 20, `search "graph" narrows the list (got ${g})`)
  assert(
    !requests.slice(before).some((u) => u.includes('/api/')),
    'searching issues no API request',
  )

  // Find and open Maximum Subarray (a top-level problem sorted after CTCI).
  await page.locator('.search').fill('maximum subarray')
  await page.waitForTimeout(200)
  await page.getByRole('link', { name: 'Maximum Subarray' }).click()
  await page.getByRole('heading', { name: 'Maximum Subarray' }).waitFor()
  await page.locator('.cm-content').waitFor()
  assert(true, 'problem detail opened from a searched result')

  // Run Tests is gated behind a timed attempt: Start (or Retake, if this problem
  // was already solved) before running.
  await page.locator('.timer-btn.start, .timer-btn.retake').first().click()
  await page.locator('.timer.running').waitFor()
  assert(true, 'started a timed attempt (Run Tests now enabled)')

  // Reset to the starter stub (this problem may have autosaved code from a
  // previous run), then run -> Pyodide loads and tests fail.
  await page.getByRole('button', { name: 'Reset' }).click()
  console.log('  running stub (Pyodide load on first run)...')
  await page.getByRole('button', { name: /Run Tests/ }).click()
  await page.locator('.summary').waitFor({ timeout: 120000 })
  assert(/^0\//.test((await page.locator('.summary').textContent()).trim()), 'stub run fails')
  // Tracebacks reference the editor file (impl.py), not an opaque <exec> blob.
  const stubMsgs = (await page.locator('.msg').allTextContents()).join('\n')
  assert(/impl\.py/.test(stubMsgs) && !/<exec>/.test(stubMsgs), 'stub traceback names impl.py, not <exec>')

  // Paste the real solution -> all pass.
  const editor = page.locator('.cm-content')
  await editor.click()
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A')
  await page.keyboard.press('Backspace')
  await page.keyboard.insertText(solution)
  await page.getByRole('button', { name: /Run Tests/ }).click()
  await page.locator('.summary.all-pass').waitFor({ timeout: 60000 })
  assert(/^10\/10/.test((await page.locator('.summary').textContent()).trim()), 'solution passes 10/10')

  console.log('\nPASS — static catalog, client-side search, and in-browser test run verified.')
} catch (e) {
  await page.screenshot({ path: 'e2e/smoke-failure.png', fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
