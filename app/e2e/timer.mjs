// Solve-timer flow: Run Tests gated behind Start; ticking timer; pause/resume;
// solve records the elapsed time; the list row shows it.
import { chromium } from 'playwright'
import { resetProblem } from './fixtures.mjs'

const BASE = process.env.BASE_URL || 'http://localhost:3100'
const PID = 'make-array-consecutive'

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}
const secs = (t) => {
  const m = /(\d+):(\d\d)/.exec(t)
  return m ? +m[1] * 60 + +m[2] : NaN
}

// Not-started, with the reference solution pre-saved so "Start clears the
// editor" has real code to clear.
resetProblem(PID, { seedSolution: true })
const problem = await (await fetch(`${BASE}/data/problems/${PID}.json`)).json()

const browser = await chromium.launch()
const page = await browser.newPage()
page.on('pageerror', (e) => console.log('  [pageerror]', e.message))

try {
  await page.goto(`${BASE}/problem/${PID}`, { waitUntil: 'networkidle' })
  await page.getByRole('heading', { name: problem.title }).waitFor()
  await page.locator('.cm-content').waitFor()

  // not-started: Run Tests disabled, Start present, editor holds prior saved code.
  assert(await page.getByRole('button', { name: /Run Tests/ }).isDisabled(), 'Run Tests disabled before Start')
  assert(await page.locator('.timer-btn.start').isVisible(), '▶ Start shown in header')
  const beforeStart = await page.locator('.cm-content').textContent()
  assert(!/NotImplementedError/.test(beforeStart), 'editor pre-loads prior saved (non-stub) code')

  // Start -> running, Run Tests enabled, and the editor is cleared to the stub.
  await page.locator('.timer-btn.start').click()
  await page.locator('.timer.running').waitFor()
  assert(await page.getByRole('button', { name: /Run Tests/ }).isEnabled(), 'Run Tests enabled after Start')
  const afterStart = await page.locator('.cm-content').textContent()
  assert(/NotImplementedError/.test(afterStart), 'Start clears the impl tab to the starter stub')

  // Ticks up.
  await page.waitForTimeout(2300)
  const t1 = secs(await page.locator('.timer.running').textContent())
  assert(t1 >= 2, `timer ticked to ${t1}s`)

  // Pause -> frozen.
  await page.locator('.timer.running .timer-btn.icon').click()
  await page.locator('.timer.paused').waitFor()
  const paused1 = secs(await page.locator('.timer.paused').textContent())
  await page.waitForTimeout(1600)
  const paused2 = secs(await page.locator('.timer.paused').textContent())
  assert(paused1 === paused2, `paused timer frozen at ${paused1}s`)

  // Resume -> running again.
  await page.locator('.timer.paused .timer-btn.icon').click()
  await page.locator('.timer.running').waitFor()
  assert(true, 'resumed')

  // Solve: paste solution + Run Tests.
  const editor = page.locator('.cm-content')
  await editor.click()
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A')
  await page.keyboard.press('Backspace')
  await page.keyboard.insertText(problem.solution)
  await page.getByRole('button', { name: /Run Tests/ }).click()
  await page.locator('.summary.all-pass').waitFor({ timeout: 120000 })
  await page.locator('.timer.solved').waitFor()
  const solvedText = await page.locator('.timer.solved').textContent()
  assert(/✓ Solved \d+:\d\d/.test(solvedText), `header shows solve time: "${solvedText.trim()}"`)
  assert(/run/.test(solvedText), 'header shows run count')

  // List row shows the recorded solve time.
  await page.goto(BASE, { waitUntil: 'networkidle' })
  await page.locator('.search').fill(problem.title)
  await page.waitForTimeout(200)
  const badge = page.locator('.problem-row', { hasText: problem.title }).locator('.status-badge.solved')
  await badge.waitFor()
  assert(/\d+:\d\d/.test(await badge.textContent()), 'list row shows ✓ with a m:ss solve time')

  console.log('\nPASS — timer gate, tick, pause/resume, solve, and list display verified.')
} catch (e) {
  await page.screenshot({ path: 'e2e/timer-failure.png', fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
