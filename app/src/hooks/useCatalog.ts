import { useEffect, useState } from 'react'
import type { Facets, ProblemPage, StatusFilter } from '../types'
import { api } from '../api'

// Owns the catalog's server-side filter/pagination state and fetching: facets
// (once) and a debounced problem-list query on any filter/page change. Every
// filter change resets to page 1.
export function useCatalog() {
  const [search, setSearchState] = useState('')
  const [difficulty, setDifficulty] = useState<string[]>([])
  const [tags, setTags] = useState<string[]>([])
  const [status, setStatusState] = useState<StatusFilter>('all')
  const [page, setPage] = useState(1)
  const [data, setData] = useState<ProblemPage | null>(null)
  const [facets, setFacets] = useState<Facets | null>(null)

  useEffect(() => {
    api.getFacets().then(setFacets).catch(() => setFacets({ difficulties: [], tags: [] }))
  }, [])

  useEffect(() => {
    let cancelled = false
    const t = setTimeout(() => {
      api
        .listProblems({ search, difficulty, tags, status, page })
        .then((d) => !cancelled && setData(d))
        .catch(() => !cancelled && setData({ items: [], total: 0, page, pageSize: 20 }))
    }, 250)
    return () => {
      cancelled = true
      clearTimeout(t)
    }
  }, [search, difficulty, tags, status, page])

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
