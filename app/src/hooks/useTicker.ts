import { useEffect, useState } from 'react'

// Returns a `now` timestamp (ms) that updates once a second while `active` is
// true, and stays put otherwise. Used to drive live-ticking elapsed timers.
export function useTicker(active: boolean): number {
  const [now, setNow] = useState(() => Date.now())
  useEffect(() => {
    if (!active) return
    const t = window.setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(t)
  }, [active])
  return now
}
