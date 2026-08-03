import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { MdCheckCircle } from 'react-icons/md'
import type { LessonSummary, LessonsResponse } from '../types'
import AppMenu from '../components/AppMenu'
import { queryLessons, syncProgress } from '../db'

// Group lessons by topic, preserving the order topics first appear.
function groupByTopic(lessons: LessonSummary[]): [string, LessonSummary[]][] {
  const order: string[] = []
  const map = new Map<string, LessonSummary[]>()
  for (const l of lessons) {
    if (!map.has(l.topic)) {
      map.set(l.topic, [])
      order.push(l.topic)
    }
    map.get(l.topic)!.push(l)
  }
  return order.map((t) => [t, map.get(t)!])
}

function pct(part: number, whole: number): string {
  return `${whole ? (part / whole) * 100 : 0}%`
}

export default function Program() {
  const [data, setData] = useState<LessonsResponse | null>(null)

  // Repopulate the progress tables before querying, so a solve made elsewhere
  // in this session is reflected without a page reload.
  useEffect(() => {
    let cancelled = false
    syncProgress()
      .then(() => !cancelled && setData(queryLessons()))
      .catch(() => !cancelled && setData({ lessons: [] }))
    return () => {
      cancelled = true
    }
  }, [])

  if (!data) return <div className="loading">Loading…</div>

  const done = data.lessons.filter((l) => l.done).length
  const total = data.lessons.length

  return (
    <div className="page program-page">
      <header className="app-header">
        <AppMenu />
        <h1>Program</h1>
      </header>
      <div className="program-summary">
        <p className="program-sub">
          {done} of {total} lessons complete
        </p>
        <span className="progress-bar wide">
          <span className="progress-fill" style={{ width: pct(done, total) }} />
        </span>
      </div>

      {groupByTopic(data.lessons).map(([topic, lessons]) => (
        <section key={topic} className="topic-group">
          <h3>{topic}</h3>
          <ul className="lesson-cards">
            {lessons.map((l) => (
              <li key={l.id}>
                <Link to={`/lesson/${l.id}`} className={`lesson-card ${l.done ? 'done' : ''}`}>
                  <span className="lesson-check">{l.done && <MdCheckCircle />}</span>
                  <span className="lesson-name">{l.title}</span>
                  <span className="lesson-count">
                    {l.solvedCount}/{l.exerciseCount}
                  </span>
                  <span className="progress-bar">
                    <span
                      className="progress-fill"
                      style={{ width: pct(l.solvedCount, l.exerciseCount) }}
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
