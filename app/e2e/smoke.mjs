// Headless smoke test: proves the full in-browser flow works — React renders,
// a problem opens, and Pyodide actually runs the unittest suite (both the
// failing stub and the passing solution) with results rendered in the UI.
import { chromium } from 'playwright'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const BASE = process.env.BASE_URL || 'http://localhost:3100'
const here = dirname(fileURLToPath(import.meta.url))
const problems = JSON.parse(
  readFileSync(join(here, '..', 'public', 'problems.json'), 'utf8'),
)
const solution = problems.find((p) => p.slug === 'maximum-subarray').solution

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

const browser = await chromium.launch()
const page = await browser.newPage()
page.on('pageerror', (e) => console.log('  [pageerror]', e.message))

try {
  // 1) Problem list
  await page.goto(BASE, { waitUntil: 'networkidle' })
  await page.getByText('Coding Trainer').waitFor()
  const rows = await page.locator('.problem-row').count()
  assert(rows === problems.length, `list shows all ${problems.length} problems (got ${rows})`)

  // 2) Client-side tag search
  await page.locator('.search').fill('graph')
  const filtered = await page.locator('.problem-row').count()
  assert(filtered > 0 && filtered < problems.length, `tag search "graph" filters the list (got ${filtered})`)
  await page.locator('.search').fill('')

  // 3) Open a problem
  await page.getByRole('link', { name: 'Maximum Subarray' }).click()
  await page.getByRole('heading', { name: 'Maximum Subarray' }).waitFor()
  await page.locator('.cm-content').waitFor()
  assert(true, 'problem detail opened with CodeMirror editor')

  // 4) Run the STUB -> Pyodide loads (first run is slow) and tests should fail
  console.log('  running stub (waiting for Pyodide to load)...')
  await page.getByRole('button', { name: /Run Tests/ }).click()
  await page.locator('.summary').waitFor({ timeout: 120000 })
  const stubSummary = (await page.locator('.summary').textContent())?.trim()
  const resultRows = await page.locator('.result').count()
  assert(/passed/.test(stubSummary), `stub run rendered a summary: "${stubSummary}"`)
  assert(resultRows === 10, `stub run rendered 10 per-test rows (got ${resultRows})`)
  assert(/^0\//.test(stubSummary), `stub fails all tests: "${stubSummary}"`)

  // 5) Paste the real solution and re-run -> all pass
  const editor = page.locator('.cm-content')
  await editor.click()
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A')
  await page.keyboard.press('Backspace')
  await page.keyboard.insertText(solution)
  await page.getByRole('button', { name: /Run Tests/ }).click()
  await page.locator('.summary.all-pass').waitFor({ timeout: 60000 })
  const passSummary = (await page.locator('.summary').textContent())?.trim()
  assert(/^10\/10/.test(passSummary), `solution passes all tests: "${passSummary}"`)

  await page.screenshot({ path: join(here, 'smoke.png'), fullPage: true })
  console.log('\nPASS — full in-browser Pyodide flow verified. Screenshot: e2e/smoke.png')
} catch (e) {
  await page.screenshot({ path: join(here, 'smoke-failure.png'), fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
