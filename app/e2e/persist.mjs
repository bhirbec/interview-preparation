// End-to-end test of persistence against the state API: autosave, run
// recording, history, last-all-passed status, and reload restoring code.
import { chromium } from 'playwright'
import { newPage, problemContent, resetProblem } from './fixtures.mjs'

const BASE = process.env.BASE_URL || 'http://localhost:3100'
const ID = 'maximum-subarray'

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

resetProblem(ID) // repeatable: back to not-started, whatever ran before
const solution = problemContent(ID).solution

const browser = await chromium.launch()
const page = await newPage(browser)
page.on('pageerror', (e) => console.log('  [pageerror]', e.message))

try {
  await page.goto(`${BASE}/problem/${ID}`, { waitUntil: 'networkidle' })
  await page.locator('.cm-content').waitFor()

  // Run Tests is gated behind a timed attempt, so this test owns its own.
  await page.locator('.timer-btn.start, .timer-btn.retake').first().click()
  await page.locator('.timer.running').waitFor()

  const editor = page.locator('.cm-content')
  await editor.click()
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A')
  await page.keyboard.press('Backspace')
  await page.keyboard.insertText(solution)
  await page.waitForTimeout(1500) // let debounced autosave flush

  console.log('  running tests (Pyodide load on first run)...')
  await page.getByRole('button', { name: /Run Tests/ }).click()
  await page.locator('.summary.all-pass').waitFor({ timeout: 120000 })
  assert(/^10\/10/.test((await page.locator('.summary').textContent()).trim()), 'run passes 10/10')

  await page.locator('.app-header .solved').waitFor()
  assert(true, 'header shows solved status after passing')

  await page.getByRole('button', { name: /History/ }).click()
  await page.locator('.history-row').first().waitFor()
  assert((await page.locator('.history-row').count()) >= 1, 'history tab lists the run')
  assert(
    (await page.locator('.history-row').first().getAttribute('class')).includes('passed'),
    'the recorded run is marked passed',
  )

  // Reload -> saved implementation restored (not the stub).
  await page.reload({ waitUntil: 'networkidle' })
  await page.locator('.cm-content').waitFor()
  const restored = await page.locator('.cm-content').innerText()
  assert(restored.includes('return max_sum'), 'reload restores the saved implementation')
  assert(!restored.includes('# TODO: implement'), 'restored code is not the starter stub')

  // The list shows the last-all-passed time (find via search).
  await page.goto(`${BASE}/`, { waitUntil: 'networkidle' })
  await page.locator('.search').fill('maximum subarray')
  await page.waitForTimeout(500)
  const row = page.locator('.problem-row', { has: page.getByRole('link', { name: 'Maximum Subarray' }) })
  await row.locator('.solved').waitFor()
  const solvedText = (await row.locator('.solved').textContent()).trim()
  assert(solvedText.startsWith('✓'), `list shows solved status: "${solvedText}"`)

  console.log('\nPASS — persistence verified end-to-end against the state API.')
} catch (e) {
  await page.screenshot({ path: 'e2e/persist-failure.png', fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
