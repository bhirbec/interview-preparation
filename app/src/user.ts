// The id the server partitions this browser's state by.
//
// THIS IS NOT AUTHENTICATION. The value is generated here, in the browser, and
// the server takes it at face value — anyone can put someone else's id in the
// cookie and read their data. It exists so a single-user prototype has a key to
// store state under, and nothing may be built on top of it that assumes more.
//
// A cookie rather than localStorage, specifically because a same-origin fetch
// sends it automatically: no call site in api.ts has to know this exists.
// Deliberately not HttpOnly either — this file has to be able to create it.
//
// Consequence: clearing cookies, or opening the app in another browser or a
// private window, mints a new id and therefore shows an empty history. There is
// no recovery path.
const COOKIE = 'trainer_uid'
const MAX_AGE = 60 * 60 * 24 * 365

function readCookie(name: string): string | null {
  const prefix = `${name}=`
  for (const part of document.cookie.split('; ')) {
    if (part.startsWith(prefix)) return part.slice(prefix.length)
  }
  return null
}

/** Create the id cookie if this browser doesn't have one yet. Must run before
 * the first API call — main.tsx calls it before rendering. */
export function ensureUserId(): string {
  const existing = readCookie(COOKIE)
  if (existing) return existing
  const id = crypto.randomUUID()
  // Secure only over HTTPS: the dev server is plain http on localhost, where a
  // Secure cookie would be dropped.
  const secure = location.protocol === 'https:' ? '; Secure' : ''
  document.cookie = `${COOKIE}=${id}; path=/; max-age=${MAX_AGE}; SameSite=Lax${secure}`
  return id
}
