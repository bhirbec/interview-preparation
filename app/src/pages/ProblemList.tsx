import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import type { Problem } from '../types'

export default function ProblemList({ problems }: { problems: Problem[] }) {
  const [query, setQuery] = useState('')
  const q = query.trim().toLowerCase()

  const filtered = useMemo(() => {
    if (!q) return problems
    return problems.filter(
      (p) =>
        p.tags.some((t) => t.includes(q)) || p.title.toLowerCase().includes(q),
    )
  }, [problems, q])

  return (
    <div className="page">
      <header className="app-header">
        <h1>Coding Trainer</h1>
        <span className="count">{problems.length} problems</span>
      </header>

      <input
        className="search"
        placeholder="Search by tag or title…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        autoFocus
      />

      <ul className="problem-list">
        {filtered.map((p) => (
          <li key={p.slug} className="problem-row">
            <Link to={`/problem/${p.slug}`} className="problem-title">
              {p.title}
            </Link>
            <span className={`badge badge-${p.difficulty}`}>{p.difficulty}</span>
            <span className="tags">
              {p.tags.map((t) => (
                <button
                  key={t}
                  type="button"
                  className="tag"
                  onClick={() => setQuery(t)}
                  title={`Filter by #${t}`}
                >
                  #{t}
                </button>
              ))}
            </span>
          </li>
        ))}
        {filtered.length === 0 && (
          <li className="empty">No problems match “{query}”.</li>
        )}
      </ul>
    </div>
  )
}
