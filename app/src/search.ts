// Catalog search / filtering / pagination / facets, in the browser.
//
// A direct port of db.query_problem_page and server.facets — behaviour is
// deliberately identical, quirks included, except that "%" and "_" are now
// literal (the SQL interpolated the raw search into a LIKE, making them
// wildcards). Pure: no React, no fetching.
import type { CatalogProblem, Facet, Facets, ProblemStatus } from './types'

export interface Filters {
  search: string
  difficulty: string[]
  tags: string[]
  status: string // '' / 'all' / anything else means "any status"
}

export interface Page<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

const DIFF_ORDER: Record<string, number> = { easy: 0, medium: 1, hard: 2 }
const STATUSES = ['not-started', 'started', 'solved']

// The SQL matched the tags COLUMN — the raw JSON text written by Python's
// json.dumps, which puts a space after each comma. JSON.stringify does not, so
// build the haystack by hand or a search for '", "' would find nothing.
function tagsText(tags: string[]): string {
  return `[${tags.map((t) => JSON.stringify(t)).join(', ')}]`
}

function clean(values: string[]): string[] {
  return values.map((v) => v.trim()).filter((v) => v)
}

export function filterProblems(
  problems: CatalogProblem[],
  filters: Filters,
  statusOf: (id: string) => ProblemStatus,
): CatalogProblem[] {
  // Whitespace-only searches match everything (search.strip() server-side).
  const needle = filters.search.trim().toLowerCase()
  const difficulties = clean(filters.difficulty)
  const tags = clean(filters.tags).map((t) => `"${t.toLowerCase()}"`)
  const status = STATUSES.includes(filters.status) ? filters.status : ''

  // No sort call anywhere: catalog.json is already in position order and
  // filtering preserves it. The SQL had no tiebreaker beyond ORDER BY position,
  // so sorting here would be a behaviour change.
  return problems.filter((p) => {
    if (needle) {
      const inTitle = p.title.toLowerCase().includes(needle)
      const inTags = tagsText(p.tags).toLowerCase().includes(needle)
      if (!inTitle && !inTags) return false
    }
    if (difficulties.length && !difficulties.includes(p.difficulty)) return false
    // Multiple tags are ANDed. SQLite's LIKE is ASCII-case-insensitive, so
    // compare the quoted tag against the lowercased haystack, as the SQL did.
    if (tags.length) {
      const haystack = tagsText(p.tags).toLowerCase()
      if (!tags.every((t) => haystack.includes(t))) return false
    }
    if (status && statusOf(p.id) !== status) return false
    return true
  })
}

export function paginate<T>(items: T[], page: number, pageSize: number): Page<T> {
  // Deliberately no clamp to totalPages: an over-range page returns an empty
  // list today, and the pager's `disabled` handles it.
  const size = Math.min(100, Math.max(1, pageSize))
  const current = Math.max(1, page)
  const offset = (current - 1) * size
  return {
    items: items.slice(offset, offset + size),
    total: items.length,
    page: current,
    pageSize: size,
  }
}

// Facet counts are global — always derived from the FULL catalog, never from
// the filtered set (that is what /api/facets returned).
export function deriveFacets(problems: CatalogProblem[]): Facets {
  const diffCounts = new Map<string, number>()
  const tagCounts = new Map<string, number>()
  for (const p of problems) {
    diffCounts.set(p.difficulty, (diffCounts.get(p.difficulty) ?? 0) + 1)
    for (const t of p.tags) tagCounts.set(t, (tagCounts.get(t) ?? 0) + 1)
  }

  const difficulties: Facet[] = [...diffCounts]
    .filter(([value]) => value)
    .map(([value, count]) => ({ value, count }))
    .sort((a, b) => (DIFF_ORDER[a.value] ?? 99) - (DIFF_ORDER[b.value] ?? 99))

  const tags: Facet[] = [...tagCounts]
    .map(([value, count]) => ({ value, count }))
    .sort((a, b) => b.count - a.count || (a.value < b.value ? -1 : a.value > b.value ? 1 : 0))

  return { difficulties, tags }
}
