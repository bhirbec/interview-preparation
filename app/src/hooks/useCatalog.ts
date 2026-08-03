import { useEffect, useMemo, useState } from 'react'
import type { CatalogProblem, ProblemPage, ProgressEntry, StatusFilter } from '../types'
import { api } from '../api'
import { loadCatalog } from '../content'
import { attemptStateOf, indexProgress, statusOf } from '../progress'
import { deriveFacets, filterProblems, paginate } from '../search'

const PAGE_SIZE = 20

// Owns the catalog's filter/pagination state. The catalog is static JSON and
// the progress bundle is one request, both loaded once; filtering, faceting and
// pagination then fold in memory, so there is nothing to debounce. Every filter
// change resets to page 1.
export function useCatalog() {
  const [search, setSearchState] = useState('')
  const [difficulty, setDifficulty] = useState<string[]>([])
  const [tags, setTags] = useState<string[]>([])
  const [status, setStatusState] = useState<StatusFilter>('all')
  const [page, setPage] = useState(1)
  const [problems, setProblems] = useState<CatalogProblem[] | null>(null)
  const [entries, setEntries] = useState<ProgressEntry[] | null>(null)

  useEffect(() => {
    loadCatalog()
      .then((c) => setProblems(c.problems))
      .catch(() => setProblems([]))
    api
      .getProgress()
      .then((p) => setEntries(p.problems))
      .catch(() => setEntries([]))
  }, [])

  const facets = useMemo(() => (problems ? deriveFacets(problems) : null), [problems])
  const progress = useMemo(() => indexProgress(entries ?? []), [entries])

  // `data` stays null until BOTH the catalog and the progress bundle arrive, so
  // rows never flash a wrong status.
  const data = useMemo<ProblemPage | null>(() => {
    if (!problems || !entries) return null
    const matched = filterProblems(problems, { search, difficulty, tags, status }, (id) =>
      statusOf(progress, id),
    )
    const { items, total, page: current, pageSize } = paginate(matched, page, PAGE_SIZE)
    return {
      items: items.map((p) => ({
        id: p.id,
        title: p.title,
        difficulty: p.difficulty,
        tags: p.tags,
        ...attemptStateOf(progress.get(p.id)),
      })),
      total,
      page: current,
      pageSize,
    }
  }, [problems, entries, progress, search, difficulty, tags, status, page])

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
