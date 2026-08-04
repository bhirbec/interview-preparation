import { useEffect, useState, type CSSProperties } from 'react'
import { Link } from 'react-router-dom'
import type { StatsResponse, TimeStat } from '../types'
import AppMenu from '../components/AppMenu'
import { computeStats, sync } from '../db'
import { formatDuration } from '../time'

const HEATMAP_WEEKS = 18
// How many topic bars to draw before collapsing the rest into a count.
const TOPIC_BARS = 12

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

// `max` is the largest count in the same section — the bars compare the rows to
// each other, never to a catalog total.
function BarRow({
  label,
  count,
  max,
  raw = false,
}: {
  label: string
  count: number
  max: number
  raw?: boolean
}) {
  return (
    <div className="bar-row">
      <span className={`bar-label${raw ? ' bar-label-raw' : ''}`}>{label}</span>
      <span className="bar-count">{count}</span>
      <span className="progress-bar">
        <span className="progress-fill" style={{ width: pct(count, max) }} />
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
    let cancelled = false
    sync()
      .then(() => !cancelled && setData(computeStats()))
      .catch(() => !cancelled && setData(null))
    return () => {
      cancelled = true
    }
  }, [])

  if (!data) return <div className="loading">Loading…</div>

  const cells = heatmapCells(data.daily)
  const diffMax = Math.max(0, ...data.byDifficulty.map((r) => r.solved))
  const topics = data.byTag.slice(0, TOPIC_BARS)
  const hiddenTopics = data.byTag.length - topics.length
  const topicMax = Math.max(0, ...topics.map((t) => t.solved))

  return (
    <div className="page stats-page">
      <header className="app-header">
        <AppMenu />
        <h1>Stats</h1>
      </header>

      <div className="stat-cards">
        <div className="stat-card">
          <span className="stat-value">{data.solvedCount}</span>
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
        <h3>Solved by difficulty</h3>
        {data.byDifficulty.map((r) => (
          <BarRow key={r.difficulty} label={r.difficulty} count={r.solved} max={diffMax} />
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
        <h3>Solved by topic</h3>
        {topics.length === 0 ? (
          <p className="stat-empty">No solves yet.</p>
        ) : (
          <>
            {topics.map((t) => (
              <BarRow key={t.tag} label={`#${t.tag}`} count={t.solved} max={topicMax} raw />
            ))}
            {hiddenTopics > 0 && (
              <p className="stat-note">
                + {hiddenTopics} more topic{hiddenTopics === 1 ? '' : 's'} solved
              </p>
            )}
          </>
        )}
      </section>

      <section className="stat-section">
        <h3>Not solved yet</h3>
        {data.unsolvedTags.length === 0 ? (
          <p className="stat-empty">Every topic in the catalog has a solve.</p>
        ) : (
          <>
            <p className="stat-note">Topics you have not solved a problem from yet.</p>
            <div className="tags">
              {data.unsolvedTags.map((t) => (
                <span key={t} className="tag">
                  #{t}
                </span>
              ))}
            </div>
          </>
        )}
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
