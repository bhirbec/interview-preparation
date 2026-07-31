import { useState } from 'react'
import { Link } from 'react-router-dom'
import type { ProblemListItem, StatusFilter } from '../types'
import AppMenu from '../components/AppMenu'
import { formatDuration } from '../time'
import { attemptView } from '../attempt'
import { useTicker } from '../hooks/useTicker'
import { useCatalog } from '../hooks/useCatalog'

const STATUS_OPTIONS: { value: StatusFilter; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'not-started', label: 'Not started' },
  { value: 'started', label: 'Started' },
  { value: 'solved', label: 'Solved' },
]

function StatusCell({ p, now }: { p: ProblemListItem; now: number }) {
  const v = attemptView(p, now)
  if (v.solved) {
    return (
      <span className="status-badge solved" title="Solved">
        ✓{p.elapsedMs != null && <span className="when">{formatDuration(p.elapsedMs)}</span>}
      </span>
    )
  }
  if (v.running || v.paused) {
    return (
      <span className="status-badge started" title={v.running ? 'In progress' : 'Paused'}>
        {v.running ? '◐' : '⏸'} <span className="when">{formatDuration(v.elapsedMs)}</span>
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
  const {
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
  } = useCatalog()
  const [showAllTags, setShowAllTags] = useState(false)

  const TAG_LIMIT = 12

  // Tick once a second only while a visible row's timer is running.
  const anyRunning = !!data?.items.some((p) => p.status === 'started' && p.runningSince)
  const now = useTicker(anyRunning)

  return (
    <div className="page list-page">
      <header className="app-header">
        <AppMenu />
      </header>

      <div className="list-layout">
        <aside className="filters">
          <input
            className="search"
            placeholder="Search title or tag…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
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
                  onChange={() => setStatus(o.value)}
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
                  onChange={() => toggleDifficulty(d.value)}
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
                    onClick={() => toggleTag(t.value)}
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
                      onClick={() => toggleTag(t)}
                      title={`Filter by #${t}`}
                    >
                      #{t}
                    </button>
                  ))}
                </span>
                <StatusCell p={p} now={now} />
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
