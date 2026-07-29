// End-to-end test of the persistence feature: autosave, run recording,
// history, last-all-passed status, and reload restoring the saved code.
import { chromium } from 'playwright'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const BASE = process.env.BASE_URL || 'http://localhost:3100'
const SLUG = 'maximum-subarray'
const here = dirname(fileURLToPath(import.meta.url))
const problems = JSON.parse(readFileSync(join(here, '..', 'public', 'problems.json'), 'utf8'))
const solution = problems.find((p) => p.slug === SLUG).solution

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

const browser = await chromium.launch()
const page = await browser.newPage()
page.on('pageerror', (e) => console.log('  [pageerror]', e.message))

try {
  // Fresh start: type the solution into the editor.
  await page.goto(`${BASE}/problem/${SLUG}`, { waitUntil: 'networkidle' })
  await page.locator('.cm-content').waitFor()
  const editor = page.locator('.cm-content')
  await editor.click()
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A')
  await page.keyboard.press('Backspace')
  await page.keyboard.insertText(solution)
  await page.waitForTimeout(1500) // let debounced autosave flush

  // Run the tests -> all pass, and the run is recorded.
  console.log('  running tests (Pyodide load on first run)...')
  await page.getByRole('button', { name: /Run Tests/ }).click()
  await page.locator('.summary.all-pass').waitFor({ timeout: 120000 })
  assert(/^10\/10/.test((await page.locator('.summary').textContent()).trim()), 'run passes 10/10')

  // Header now shows the solved status.
  await page.locator('.app-header .solved').waitFor()
  assert(true, 'header shows "solved" status after passing')

  // History tab shows the run.
  await page.getByRole('button', { name: /History/ }).click()
  await page.locator('.history-row').first().waitFor()
  const historyRows = await page.locator('.history-row').count()
  assert(historyRows >= 1, `history tab lists the run (${historyRows} row)`)
  assert(
    (await page.locator('.history-row').first().getAttribute('class')).includes('passed'),
    'the recorded run is marked passed',
  )

  // Reload -> the saved implementation is restored (not the stub).
  await page.reload({ waitUntil: 'networkidle' })
  await page.locator('.cm-content').waitFor()
  const restored = await page.locator('.cm-content').innerText()
  assert(restored.includes('return max_sum'), 'reload restores the saved implementation')
  assert(!restored.includes('# TODO: implement'), 'restored code is not the starter stub')

  // The list shows the last-all-passed time for this problem.
  await page.goto(`${BASE}/`, { waitUntil: 'networkidle' })
  const row = page.locator('.problem-row', { has: page.getByRole('link', { name: 'Maximum Subarray' }) })
  await row.locator('.solved').waitFor()
  const solvedText = (await row.locator('.solved').textContent()).trim()
  assert(solvedText.startsWith('✓'), `list shows solved status: "${solvedText}"`)

  console.log('\nPASS — persistence (autosave, runs, history, status) verified end-to-end.')
} catch (e) {
  await page.screenshot({ path: join(here, 'persist-failure.png'), fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
