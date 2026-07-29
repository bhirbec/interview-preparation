import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import type { Facets, ProblemListItem, ProblemPage, StatusFilter } from '../types'
import ThemeToggle from '../components/ThemeToggle'
import { api } from '../api'
import { timeAgo } from '../time'

const STATUS_OPTIONS: { value: StatusFilter; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'not-started', label: 'Not started' },
  { value: 'started', label: 'Started' },
  { value: 'solved', label: 'Solved' },
]

function StatusCell({ p }: { p: ProblemListItem }) {
  if (p.status === 'solved') {
    return (
      <span className="status-badge solved" title={`Solved ${timeAgo(p.lastAllPassedAt)}`}>
        ✓ <span className="when">{timeAgo(p.lastAllPassedAt)}</span>
      </span>
    )
  }
  if (p.status === 'started') {
    return (
      <span
        className="status-badge started"
        title={p.lastActivityAt ? `In progress · ${timeAgo(p.lastActivityAt)}` : 'In progress'}
      >
        ◐ <span className="when">{p.lastActivityAt ? timeAgo(p.lastActivityAt) : 'started'}</span>
      </span>
    )
  }
  return (
    <span className="status-badge none" title="Not started">
      ○
    </span>
  )
}

export default function ProblemList() {
  const [search, setSearch] = useState('')
  const [difficulty, setDifficulty] = useState<string[]>([])
  const [tags, setTags] = useState<string[]>([])
  const [status, setStatus] = useState<StatusFilter>('all')
  const [page, setPage] = useState(1)
  const [data, setData] = useState<ProblemPage | null>(null)
  const [facets, setFacets] = useState<Facets | null>(null)
  const [showAllTags, setShowAllTags] = useState(false)

  const TAG_LIMIT = 12

  useEffect(() => {
    api.getFacets().then(setFacets).catch(() => setFacets({ difficulties: [], tags: [] }))
  }, [])

  // Debounced fetch whenever any filter or the page changes (server-side).
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

  function toggle(list: string[], set: (v: string[]) => void, value: string) {
    set(list.includes(value) ? list.filter((x) => x !== value) : [...list, value])
    setPage(1)
  }

  function clearAll() {
    setSearch('')
    setDifficulty([])
    setTags([])
    setStatus('all')
    setPage(1)
  }

  const hasFilters =
    !!search || difficulty.length > 0 || tags.length > 0 || status !== 'all'
  const totalPages = data ? Math.max(1, Math.ceil(data.total / data.pageSize)) : 1

  return (
    <div className="page list-page">
      <header className="app-header">
        <h1>Coding Trainer</h1>
        <ThemeToggle />
      </header>

      <div className="list-layout">
        <aside className="filters">
          <input
            className="search"
            placeholder="Search title or tag…"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value)
              setPage(1)
            }}
            autoFocus
          />

          <div className="filter-group">
            <h3>Status</h3>
            {STATUS_OPTIONS.map((o) => (
              <label key={o.value}>
                <input
                  type="radio"
                  name="status"
                  checked={status === o.value}
                  onChange={() => {
                    setStatus(o.value)
                    setPage(1)
                  }}
                />
                <span className="fname">{o.label}</span>
              </label>
            ))}
          </div>

          <div className="filter-group">
            <h3>Difficulty</h3>
            {facets?.difficulties.map((d) => (
              <label key={d.value}>
                <input
                  type="checkbox"
                  checked={difficulty.includes(d.value)}
                  onChange={() => toggle(difficulty, setDifficulty, d.value)}
                />
                <span className="fname">{d.value}</span>
                <span className="fcount">{d.count}</span>
              </label>
            ))}
          </div>

          <div className="filter-group">
            <h3>Tags</h3>
            <div className="tag-filter">
              {(facets?.tags ?? [])
                .filter((t, i) => showAllTags || i < TAG_LIMIT || tags.includes(t.value))
                .map((t) => (
                  <button
                    key={t.value}
                    type="button"
                    className={`tag ${tags.includes(t.value) ? 'active' : ''}`}
                    onClick={() => toggle(tags, setTags, t.value)}
                  >
                    #{t.value} <span className="fcount">{t.count}</span>
                  </button>
                ))}
            </div>
            {(facets?.tags.length ?? 0) > TAG_LIMIT && (
              <button
                type="button"
                className="show-more"
                onClick={() => setShowAllTags((v) => !v)}
              >
                {showAllTags
                  ? 'Show less'
                  : `Show more (${(facets?.tags.length ?? 0) - TAG_LIMIT})`}
              </button>
            )}
          </div>

          {hasFilters && (
            <button type="button" className="clear-filters" onClick={clearAll}>
              Clear filters
            </button>
          )}
        </aside>

        <main className="list-main">
          <ul className="problem-list">
            {data?.items.map((p) => (
              <li key={p.id} className="problem-row">
                <Link to={`/problem/${p.id}`} className="problem-title">
                  {p.title}
                </Link>
                <span className={`badge badge-${p.difficulty}`}>{p.difficulty}</span>
                <span className="tags">
                  {p.tags.map((t) => (
                    <button
                      key={t}
                      type="button"
                      className={`tag ${tags.includes(t) ? 'active' : ''}`}
                      onClick={() => toggle(tags, setTags, t)}
                      title={`Filter by #${t}`}
                    >
                      #{t}
                    </button>
                  ))}
                </span>
                <StatusCell p={p} />
              </li>
            ))}
            {data && data.items.length === 0 && (
              <li className="empty">No problems match these filters.</li>
            )}
          </ul>

          <div className="pager">
            <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
              ← Prev
            </button>
            <span className="pageinfo">
              Page {page} of {totalPages}
            </span>
            <button disabled={page >= totalPages} onClick={() => setPage((p) => p + 1)}>
              Next →
            </button>
          </div>

          {data && (
            <p className="list-total">
              {data.total} problem{data.total === 1 ? '' : 's'}
            </p>
          )}
        </main>
      </div>
    </div>
  )
}
