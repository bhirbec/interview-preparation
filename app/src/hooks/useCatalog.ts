import { useEffect, useMemo, useState } from 'react'
import type { Facets, ProblemPage, StatusFilter } from '../types'
import { ensureDb, queryFacets, queryProblems, syncProgress } from '../db'

// Owns the catalog's filter/pagination state. Everything is answered locally:
// the database is initialized once (WASM + the static catalog) and the progress
// tables are rebuilt from /api/progress, after which each filter change is a
// synchronous re-query inside a useMemo — no debounce, because there is no
// round trip left to throttle. Every filter change resets to page 1.
export function useCatalog() {
  const [search, setSearchState] = useState('')
  const [difficulty, setDifficulty] = useState<string[]>([])
  const [tags, setTags] = useState<string[]>([])
  const [status, setStatusState] = useState<StatusFilter>('all')
  const [page, setPage] = useState(1)
  // `ready` gates the queries: WASM instantiation is on this page's critical
  // path, so until it flips, `data` stays null and the page shows its loading
  // state rather than flashing "no problems match".
  const [ready, setReady] = useState(false)

  useEffect(() => {
    let cancelled = false
    Promise.all([ensureDb(), syncProgress()])
      .then(() => !cancelled && setReady(true))
      .catch(() => !cancelled && setReady(true))
    return () => {
      cancelled = true
    }
  }, [])

  const data = useMemo<ProblemPage | null>(() => {
    if (!ready) return null
    try {
      return queryProblems({ search, difficulty, tags, status, page, pageSize: 20 })
    } catch {
      return { items: [], total: 0, page, pageSize: 20 }
    }
  }, [ready, search, difficulty, tags, status, page])

  const facets = useMemo<Facets | null>(() => {
    if (!ready) return null
    try {
      return queryFacets()
    } catch {
      return { difficulties: [], tags: [] }
    }
  }, [ready])

  function toggleIn(list: string[], set: (v: string[]) => void, value: string) {
    set(list.includes(value) ? list.filter((x) => x !== value) : [...list, value])
    setPage(1)
  }

  function setSearch(v: string) {
    setSearchState(v)
    setPage(1)
  }
  function setStatus(v: StatusFilter) {
    setStatusState(v)
    setPage(1)
  }
  const toggleDifficulty = (v: string) => toggleIn(difficulty, setDifficulty, v)
  const toggleTag = (v: string) => toggleIn(tags, setTags, v)

  function clearAll() {
    setSearchState('')
    setDifficulty([])
    setTags([])
    setStatusState('all')
    setPage(1)
  }

  const hasFilters =
    !!search || difficulty.length > 0 || tags.length > 0 || status !== 'all'
  const totalPages = data ? Math.max(1, Math.ceil(data.total / data.pageSize)) : 1

  return {
    search,
    difficulty,
    tags,
    status,
    page,
    data,
    facets,
    hasFilters,
    totalPages,
    setSearch,
    setStatus,
    toggleDifficulty,
    toggleTag,
    setPage,
    clearAll,
  }
}
