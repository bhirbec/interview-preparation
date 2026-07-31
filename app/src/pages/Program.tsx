import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { MdCheckCircle } from 'react-icons/md'
import type { ChapterSummary, ProgramResponse } from '../types'
import AppMenu from '../components/AppMenu'
import { api } from '../api'

// Group chapters by topic, preserving the order topics first appear.
function groupByTopic(chapters: ChapterSummary[]): [string, ChapterSummary[]][] {
  const order: string[] = []
  const map = new Map<string, ChapterSummary[]>()
  for (const c of chapters) {
    if (!map.has(c.topic)) {
      map.set(c.topic, [])
      order.push(c.topic)
    }
    map.get(c.topic)!.push(c)
  }
  return order.map((t) => [t, map.get(t)!])
}

function pct(part: number, whole: number): string {
  return `${whole ? (part / whole) * 100 : 0}%`
}

export default function Program() {
  const [data, setData] = useState<ProgramResponse | null>(null)

  useEffect(() => {
    api.getProgram().then(setData).catch(() => setData({ chapters: [] }))
  }, [])

  if (!data) return <div className="loading">Loading…</div>

  const done = data.chapters.filter((c) => c.done).length
  const total = data.chapters.length

  return (
    <div className="page program-page">
      <header className="app-header">
        <AppMenu />
        <h1>Program</h1>
      </header>
      <div className="program-summary">
        <p className="program-sub">
          {done} of {total} chapters complete
        </p>
        <span className="progress-bar wide">
          <span className="progress-fill" style={{ width: pct(done, total) }} />
        </span>
      </div>

      {groupByTopic(data.chapters).map(([topic, chapters]) => (
        <section key={topic} className="topic-group">
          <h3>{topic}</h3>
          <ul className="chapter-list">
            {chapters.map((c) => (
              <li key={c.id}>
                <Link to={`/chapter/${c.id}`} className={`chapter-card ${c.done ? 'done' : ''}`}>
                  <span className="chapter-check">{c.done && <MdCheckCircle />}</span>
                  <span className="chapter-title">{c.title}</span>
                  <span className="chapter-count">
                    {c.solvedCount}/{c.exerciseCount}
                  </span>
                  <span className="progress-bar">
                    <span
                      className="progress-fill"
                      style={{ width: pct(c.solvedCount, c.exerciseCount) }}
                    />
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  )
}
