// The per-browser user_id cookie: a fresh browser profile mints one, a reload
// keeps it, and a second profile (like a private window) gets a different one.
import { chromium } from 'playwright'

const BASE = process.env.BASE_URL || 'http://localhost:3100'
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

function assert(cond, msg) {
  if (!cond) throw new Error('ASSERT FAILED: ' + msg)
  console.log('  ok -', msg)
}

async function userId(context) {
  const c = (await context.cookies()).find((c) => c.name === 'user_id')
  return c || null
}

const browser = await chromium.launch()

try {
  // A fresh, empty context is a fresh browser profile.
  const first = await browser.newContext()
  const page = await first.newPage()
  page.on('pageerror', (e) => console.log('  [pageerror]', e.message))
  await page.goto(BASE, { waitUntil: 'networkidle' })
  await page.locator('.problem-row').first().waitFor()

  const cookie = await userId(first)
  assert(cookie !== null, 'a fresh browser profile gets a user_id cookie')
  assert(UUID_RE.test(cookie.value), `the value is a UUID (${cookie.value})`)
  assert(cookie.path === '/', 'path=/')
  assert(cookie.sameSite === 'Lax', 'SameSite=Lax')
  assert(cookie.httpOnly === false, 'not HttpOnly (the frontend writes it)')
  assert(cookie.secure === false, 'not Secure over plain http (else it would not stick)')
  const year = 60 * 60 * 24 * 365
  assert(cookie.expires > Date.now() / 1000 + year * 0.9, 'expires about a year out')

  // Same browser, reloaded: same identity.
  await page.reload({ waitUntil: 'networkidle' })
  await page.locator('.problem-row').first().waitFor()
  assert((await userId(first)).value === cookie.value, 'the same browser keeps its id across a reload')

  // A second context shares nothing with the first — same as a private window.
  const second = await browser.newContext()
  const page2 = await second.newPage()
  await page2.goto(BASE, { waitUntil: 'networkidle' })
  await page2.locator('.problem-row').first().waitFor()
  const other = await userId(second)
  assert(other !== null && UUID_RE.test(other.value), 'a second profile also gets a UUID')
  assert(other.value !== cookie.value, `and it is a different id (${other.value})`)

  // The cookie rides along on API calls without any call site passing it.
  const sent = await page.evaluate(async () => {
    const res = await fetch('/api/progress')
    return res.status
  })
  assert(sent === 200, 'an api.ts-style fetch is accepted (the cookie went with it)')

  console.log('\nAll identity checks passed.')
} finally {
  await browser.close()
}
