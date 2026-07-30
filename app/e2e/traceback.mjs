// A failing in-browser run must report tracebacks against the editor files
// (impl.py / tests.py) with real line numbers and source, not an opaque <exec>.
import { chromium } from 'playwright'

const BASE = process.env.BASE_URL || 'http://localhost:3100'
const PID = 'merge-m-sorted-arrays'

// The user's buggy solution: `if j < n` should be `if j + 1 < n`, so arr[j + 1]
// runs off the end for the last element of a shorter array (IndexError).
const BUGGY = `import heapq

def merge_sorted_arrays(arrays):
  h = []
  for i, arr in enumerate(arrays):
    if arr:
      heapq.heappush(h, (arr[0], i, 0))
  output = []
  while h:
    value, i, j = heapq.heappop(h)
    output.append(value)
    arr = arrays[i]
    n = len(arr)
    if j < n:
      heapq.heappush(h, (arr[j + 1], i, j + 1))
  return output
`

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

const browser = await chromium.launch()
const page = await browser.newPage()
page.on('pageerror', (e) => console.log('  [pageerror]', e.message))

try {
  await page.goto(`${BASE}/problem/${PID}`, { waitUntil: 'networkidle' })
  await page.locator('.cm-content').waitFor()

  // Start (Run Tests is gated), then replace the editor with the buggy solution.
  await page.locator('.timer-btn.start, .timer-btn.retake').first().click()
  await page.locator('.timer.running').waitFor()
  const editor = page.locator('.cm-content')
  await editor.click()
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A')
  await page.keyboard.press('Backspace')
  await page.keyboard.insertText(BUGGY)

  await page.getByRole('button', { name: /Run Tests/ }).click()
  await page.locator('.summary').waitFor({ timeout: 120000 })

  // Collect every failing test's traceback text.
  const msgs = (await page.locator('.msg').allTextContents()).join('\n---\n')
  assert(msgs.length > 0, 'at least one test failed (traceback shown)')
  assert(!/<exec>/.test(msgs), 'traceback does NOT mention <exec>')
  assert(/File "impl\.py", line \d+/.test(msgs), 'traceback references impl.py with a line number')
  assert(/File "tests\.py", line \d+/.test(msgs), 'traceback references tests.py with a line number')
  assert(/arr\[j \+ 1\]/.test(msgs), 'traceback shows the offending impl source line')
  assert(/IndexError/.test(msgs), 'traceback shows the IndexError')

  const frame = /File "impl\.py", line \d+, in merge_sorted_arrays/.exec(msgs)
  console.log('  →', frame ? frame[0] : '(impl.py frame)')
  console.log('\nPASS — tracebacks point at impl.py / tests.py editor lines.')
} catch (e) {
  await page.screenshot({ path: 'e2e/traceback-failure.png', fullPage: true }).catch(() => {})
  console.error('\nFAIL —', e.message)
  process.exitCode = 1
} finally {
  await browser.close()
}
