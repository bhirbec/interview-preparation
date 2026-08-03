import { useEffect, useState, type CSSProperties } from 'react'
import { Link } from 'react-router-dom'
import type { StatsResponse, TimeStat } from '../types'
import AppMenu from '../components/AppMenu'
import { api } from '../api'
import { loadCatalog } from '../content'
import { computeStats } from '../stats'
import { formatDuration } from '../time'

const HEATMAP_WEEKS = 18

function dur(ms: number | null): string {
  return ms == null ? '—' : formatDuration(ms)
}

function pct(part: number, whole: number): string {
  return `${whole ? (part / whole) * 100 : 0}%`
}

// Last HEATMAP_WEEKS weeks of day cells, ordered Sun→Sat per week (column-major
// in the grid), tagged with each day's solve count.
function heatmapCells(daily: { date: string; count: number }[]) {
  const counts = new Map(daily.map((d) => [d.date, d.count]))
  const end = new Date()
  end.setHours(0, 0, 0, 0)
  end.setDate(end.getDate() + (6 - end.getDay())) // Saturday of this week
  const start = new Date(end)
  start.setDate(start.getDate() - (HEATMAP_WEEKS * 7 - 1)) // a Sunday
  const cells: { date: string; count: number }[] = []
  for (let i = 0; i < HEATMAP_WEEKS * 7; i++) {
    const d = new Date(start)
    d.setDate(start.getDate() + i)
    const key = d.toISOString().slice(0, 10)
    cells.push({ date: key, count: counts.get(key) ?? 0 })
  }
  return cells
}

function heatStyle(count: number): CSSProperties {
  if (!count) return { background: 'var(--border)' }
  return { background: 'var(--pass)', opacity: 0.35 + 0.65 * Math.min(1, count / 4) }
}

function BarRow({ label, solved, total }: { label: string; solved: number; total: number }) {
  return (
    <div className="bar-row">
      <span className="bar-label">{label}</span>
      <span className="bar-count">
        {solved}/{total}
      </span>
      <span className="progress-bar">
        <span className="progress-fill" style={{ width: pct(solved, total) }} />
      </span>
    </div>
  )
}

function timeLine(t: TimeStat): string {
  return t.count ? `avg ${dur(t.avgMs)} · best ${dur(t.bestMs)}` : 'no timed solves'
}

export default function Stats() {
  const [data, setData] = useState<StatsResponse | null>(null)

  useEffect(() => {
    Promise.all([loadCatalog(), api.getProgress()])
      .then(([catalog, progress]) => setData(computeStats(catalog.problems, progress.problems)))
      .catch(() => setData(null))
  }, [])

  if (!data) return <div className="loading">Loading…</div>

  const cells = heatmapCells(data.daily)

  return (
    <div className="page stats-page">
      <header className="app-header">
        <AppMenu />
        <h1>Stats</h1>
      </header>

      <div className="stat-cards">
        <div className="stat-card">
          <span className="stat-value">
            {data.solvedCount} <span className="stat-of">/ {data.totalProblems}</span>
          </span>
          <span className="stat-label">Solved</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{formatDuration(data.totalTimeMs)}</span>
          <span className="stat-label">Time solving</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{data.streak.current}🔥</span>
          <span className="stat-label">Day streak (best {data.streak.longest})</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{data.totalRuns}</span>
          <span className="stat-label">Test runs</span>
        </div>
      </div>

      <section className="stat-section">
        <h3>By difficulty</h3>
        {data.byDifficulty.map((r) => (
          <BarRow key={r.difficulty} label={r.difficulty} solved={r.solved} total={r.total} />
        ))}
      </section>

      <section className="stat-section">
        <h3>Activity</h3>
        <div
          className="heatmap"
          style={{ gridTemplateColumns: `repeat(${HEATMAP_WEEKS}, 1fr)` }}
        >
          {cells.map((c) => (
            <span
              key={c.date}
              className="heat-cell"
              style={heatStyle(c.count)}
              title={`${c.date}: ${c.count} solved`}
            />
          ))}
        </div>
      </section>

      <section className="stat-section">
        <h3>Solve time</h3>
        <p className="solvetime-overall">Overall — {timeLine(data.solveTime.overall)}</p>
        {data.solveTime.byDifficulty.map((t) => (
          <div key={t.difficulty} className="solvetime-row">
            <span className={`badge badge-${t.difficulty}`}>{t.difficulty}</span>
            <span>{timeLine(t)}</span>
          </div>
        ))}
        {data.fastest.length > 0 && (
          <>
            <h4>Fastest solves</h4>
            <ul className="stat-list">
              {data.fastest.map((f) => (
                <li key={f.id}>
                  <Link to={`/problem/${f.id}`} className="stat-link">
                    {f.title}
                  </Link>
                  <span className="stat-time">{dur(f.elapsedMs)}</span>
                </li>
              ))}
            </ul>
          </>
        )}
      </section>

      <section className="stat-section">
        <h3>Topic coverage</h3>
        {data.byTag.map((t) => (
          <BarRow key={t.tag} label={`#${t.tag}`} solved={t.solved} total={t.total} />
        ))}
      </section>

      <div className="stat-cols">
        <section className="stat-section">
          <h3>Recently solved</h3>
          <ul className="stat-list">
            {data.recent.map((r) => (
              <li key={r.id}>
                <Link to={`/problem/${r.id}`} className="stat-link">
                  {r.title}
                </Link>
                <span className="stat-time">{dur(r.elapsedMs)}</span>
              </li>
            ))}
          </ul>
        </section>
        <section className="stat-section">
          <h3>In progress</h3>
          {data.inProgress.length === 0 ? (
            <p className="stat-empty">Nothing in progress.</p>
          ) : (
            <ul className="stat-list">
              {data.inProgress.map((p) => (
                <li key={p.id}>
                  <Link to={`/problem/${p.id}`} className="stat-link">
                    {p.title}
                  </Link>
                  <span className={`badge badge-${p.difficulty}`}>{p.difficulty}</span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  )
}
