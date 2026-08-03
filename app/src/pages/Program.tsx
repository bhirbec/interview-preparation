import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { MdCheckCircle } from 'react-icons/md'
import type { LessonSummary } from '../types'
import AppMenu from '../components/AppMenu'
import { api } from '../api'
import { loadLessons } from '../content'
import { lessonSummaries } from '../lessons'
import { indexProgress } from '../progress'

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
  const [lessons, setLessons] = useState<LessonSummary[] | null>(null)

  useEffect(() => {
    Promise.all([loadLessons(), api.getProgress()])
      .then(([content, progress]) =>
        setLessons(lessonSummaries(content.lessons, indexProgress(progress.problems))),
      )
      .catch(() => setLessons([]))
  }, [])

  if (!lessons) return <div className="loading">Loading…</div>

  const done = lessons.filter((l) => l.done).length
  const total = lessons.length

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

      {groupByTopic(lessons).map(([topic, group]) => (
        <section key={topic} className="topic-group">
          <h3>{topic}</h3>
          <ul className="lesson-cards">
            {group.map((l) => (
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
