import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import type { ProblemPage } from '../types'
import ThemeToggle from '../components/ThemeToggle'
import { api } from '../api'
import { timeAgo } from '../time'

export default function ProblemList() {
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [data, setData] = useState<ProblemPage | null>(null)
  const [loading, setLoading] = useState(true)

  // Debounced fetch whenever the query or page changes (server-side search).
  useEffect(() => {
    let cancelled = false
    setLoading(true)
    const t = setTimeout(() => {
      api
        .listProblems(search, page)
        .then((d) => !cancelled && setData(d))
        .catch(() => !cancelled && setData({ items: [], total: 0, page, pageSize: 20 }))
        .finally(() => !cancelled && setLoading(false))
    }, 250)
    return () => {
      cancelled = true
      clearTimeout(t)
    }
  }, [search, page])

  function onSearch(value: string) {
    setSearch(value)
    setPage(1)
  }

  const totalPages = data ? Math.max(1, Math.ceil(data.total / data.pageSize)) : 1

  return (
    <div className="page">
      <header className="app-header">
        <h1>Coding Trainer</h1>
        <span className="count">{data ? `${data.total} problems` : ''}</span>
        <ThemeToggle />
      </header>

      <input
        className="search"
        placeholder="Search by tag or title…"
        value={search}
        onChange={(e) => onSearch(e.target.value)}
        autoFocus
      />

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
                  className="tag"
                  onClick={() => onSearch(t)}
                  title={`Filter by #${t}`}
                >
                  #{t}
                </button>
              ))}
            </span>
            <span
              className={`solved ${p.lastAllPassedAt ? 'on' : 'off'}`}
              title={p.lastAllPassedAt ? 'Most recent time all tests passed' : 'Not solved yet'}
            >
              {p.lastAllPassedAt ? `✓ ${timeAgo(p.lastAllPassedAt)}` : ''}
            </span>
          </li>
        ))}
        {data && data.items.length === 0 && !loading && (
          <li className="empty">No problems match “{search}”.</li>
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
    </div>
  )
}
