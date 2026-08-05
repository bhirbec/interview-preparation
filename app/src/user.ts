// Per-browser identity. A cookie, not localStorage, for one reason: the API is
// same-origin (Vite proxies /api), so the browser attaches it to every fetch
// and sendBeacon on its own — api.ts never has to know this file exists.
//
// This is not authentication. The id is generated here and trivially forgeable;
// it only scopes state to a browser. See backend/user.py for the server side.

const COOKIE_NAME = 'user_id'
const MAX_AGE = 60 * 60 * 24 * 365 // a year, refreshed on every load

// The canonical UUID shape the backend accepts. Checked here too, so a stale or
// hand-edited cookie is replaced on load instead of 400ing every request.
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

function readCookie(name: string): string | null {
  for (const part of document.cookie.split('; ')) {
    const eq = part.indexOf('=')
    if (eq > 0 && part.slice(0, eq) === name) return decodeURIComponent(part.slice(eq + 1))
  }
  return null
}

/** Return this browser's id, minting and storing one if it has none. */
export function ensureUserId(): string {
  const existing = readCookie(COOKIE_NAME)
  if (existing && UUID_RE.test(existing)) return existing

  const id = crypto.randomUUID()
  // `Secure` only over HTTPS: on plain http (localhost dev) the browser would
  // drop a Secure cookie silently, and every reload would mint a new identity.
  const secure = location.protocol === 'https:' ? '; Secure' : ''
  document.cookie = `${COOKIE_NAME}=${id}; path=/; max-age=${MAX_AGE}; SameSite=Lax${secure}`
  return id
}
